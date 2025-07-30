# 🌿 Air Quality Data Assistant

An AI-powered web application that allows users to ask natural language questions about air quality sensor data across multiple rooms. The system uses LLMs to generate, execute, and summarize data analyses — all without needing a database.

---

## 🚀 Features

- ✅ Upload `.ndjson` files (1 per room) — each line is a JSON object with timestamped sensor readings.
- ✅ Ask natural language questions like:
  - "How does CO2 vary by day of the week?"
  - "Which room had the highest temperature last week?"
- ✅ Automatically detects whether a **table**, **chart**, or both are needed.
- ✅ Summarizes results in plain English using LLM-generated reasoning.
- ✅ Supports inconsistent field names using semantic normalization.
- ✅ Includes clean error handling and chart/table formatting.

---

## 🧠 How It Works

### 🔄 Flow

1. **Upload**: User uploads one or more `.ndjson` files.
2. **Normalization**: Field names are auto-mapped to standard terms (`CO2`, `Temperature`, `Humidity`, etc.).
3. **Query Understanding**: LLM detects whether a chart is needed.
4. **Code Generation**: LLM writes pandas/matplotlib code based on data and query.
5. **Execution**: Generated code is run in a safe environment.
6. **Response Packaging**: Table is prettified, chart is saved, and summary is generated.

---

## 🧪 Example Questions

- How does CO2 in Room 1 vary by day of the week?
- How do average CO2 levels, humidity, and temperature vary across different rooms?
- Give daily CO2 levels for Room 1 and Room 2 between July 10 and July 15.
- Which room had the highest temperature reading on July 12?
- Which room had the biggest variation in CO2 levels?
- List the rooms in order of hottest to coolest using average temperature in a day.
- What is the average temperature of each room in mornings and evenings?

---

## 🤖 LLM Details

- **Model**: `llama3-70b-8192` via Groq API  
- **Temperature**: `0.2` (for deterministic, clean outputs)  
- **Prompting**: Structured with schema, preview, and strict rule sets  
- **Tools**: Code generation, summarization, reasoning  

---

## Setting up and Running the project
### 1. Clone the repository
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/Thathsarani-Sandarekha/data_analysis_agent.git)
cd data_analysis_agent/backend
```

#### 2. Create a virtual environment (you can use conda too) and activate it
```bash
python -m venv venv
source venv/bin/activate 
```

### 🌐 Frontend Setup
#### 1. Open a new terminal and go to the frontend directory
```bash
cd ../frontend
```

#### 2. Install frontend dependencies
```bash
npm install
```

### ⚙️ Backend Setup
#### 1. Install dependencies
```bash
pip install -r requirements.txt
```

#### 2. Set environment variables in .env
Create a .env file in the backend/ folder with the following content:
```
env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama3-70b-8192
```
If you're using OpenAI instead of Groq, adjust the base URL and key in llm_client.py.

#### 3. Ensure your sensor data is in this path:

<pre><code>``` backend/ └── sensor-data/ ├── Room A.ndjson ├── Room B.ndjson └── ... ```</code></pre>

#### 4. Run the backend server
```bash
uvicorn api_server:app --reload --port 8000
```

---

## 👨‍💻 Author

Built with ❤️ by **Thathsarani Sandarekha**  
BSc (Hons) AI & Data Science | Aspiring Machine Learning Engineer and Researcher

