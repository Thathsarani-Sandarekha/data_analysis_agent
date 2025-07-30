import json
import os
import pandas as pd
import re
from sentence_transformers import SentenceTransformer, util

# ------------------ Canonical Setup ------------------
CANONICAL_FIELDS = ["co2", "temperature", "humidity", "timestamp"]
ABBREVIATIONS = {
    "co2": "co2",
    "co₂": "co2",
    "co2 level": "co2",
    "temperature": "temperature",
    "temp": "temperature",
    "t": "temperature",
    "humidity": "humidity",
    "relative humidity": "humidity",
    "rh": "humidity",
    "humidity (%)": "humidity",
    "timestamp": "timestamp",
    "log_time": "timestamp",
    "time": "timestamp"
}

# Load model and encode canonical fields once
model = SentenceTransformer("all-MiniLM-L6-v2")
canonical_embeddings = model.encode(CANONICAL_FIELDS, convert_to_tensor=True)

# ------------------ Normalization Helpers ------------------
def preprocess_key(key):
    cleaned = (
        key.strip()
           .lower()
           .replace("°c", "")
           .replace("(ppm)", "")
           .replace("%", "")
    )
    return ABBREVIATIONS.get(cleaned, cleaned)

def normalize_fields_auto(entry, threshold=0.6):
    """
    Normalize fields using abbreviation mapping + fuzzy matching fallback
    """
    normalized = {}
    for raw_key, value in entry.items():
        pre_key = preprocess_key(raw_key)

        # Step 1: Abbreviation match
        if pre_key in CANONICAL_FIELDS:
            normalized[pre_key] = value
            continue

        # Step 2: Fuzzy match
        raw_embed = model.encode(pre_key, convert_to_tensor=True)
        sim_scores = util.cos_sim(raw_embed, canonical_embeddings)[0]
        best_idx = int(sim_scores.argmax())
        best_score = float(sim_scores[best_idx])

        if best_score >= threshold:
            normalized_key = CANONICAL_FIELDS[best_idx]
        else:
            normalized_key = raw_key  # fallback to original

        normalized[normalized_key] = value

    return normalized

def clean_timestamps(df: pd.DataFrame) -> pd.DataFrame:
    if "timestamp" in df.columns:
        try:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            if df["timestamp"].dt.tz is not None:
                df["timestamp"] = df["timestamp"].dt.tz_convert(None)
            df["timestamp"] = df["timestamp"].dt.tz_localize(None)
        except Exception as e:
            print(f"[⚠️] Failed to clean timestamps: {e}")
    return df

# ------------------ File Loading ------------------
def load_all_rooms(directory="sensor-data"):
    room_dfs = {}
    for file in os.listdir(directory):
        if file.endswith(".ndjson"):
            match = re.search(r'Room\s*\d+', file)
            room_name = match.group(0) if match else file.split('.')[0]

            with open(os.path.join(directory, file), 'r') as f:
                lines = [json.loads(line) for line in f]

            normalized = [normalize_fields_auto(entry) for entry in lines]
            df = pd.DataFrame(normalized)
            df = clean_timestamps(df)
            df['room'] = room_name
            room_dfs[room_name] = df
    return room_dfs

def load_combined_df(directory="sensor-data"):
    room_dfs = load_all_rooms(directory)
    return pd.concat(room_dfs.values(), ignore_index=True)