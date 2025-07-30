import pandas as pd

# ------------------ plot_prompt_generator ---------------------------
def plot_prompt_generator(data: pd.DataFrame, user_question: str) -> str:
    """
    Creates a prompt to ask the LLM to write Python code using pandas and matplotlib 
    to generate a plot based on the given question.
    """
    column_names = list(data.columns)
    sample_rows = data.head(10).to_string(index=False)

    return f"""
You are given a pandas DataFrame named `df`.

Schema:
Columns: {', '.join(column_names)}

Preview:
{sample_rows}

Write Python code using pandas and matplotlib (as plt) to answer:
"{user_question}"

Rules
-----
- Use pandas for data manipulation and matplotlib.pyplot (as plt) for plotting.
- DO NOT use .resample() alone when analyzing data with multiple categorical values — it drops group context. Instead, extract the date and use groupby for aggregation.
- Assume the 'timestamp' column is already in datetime format with clean values.
- When analyzing time-based trends (e.g., by hour or weekday), extract components like df['timestamp'].dt.hour or df['timestamp'].dt.day_name().
- When filtering, always use `.copy()` to avoid chained assignment warnings.
- When filtering by date, use comparisons like df['timestamp'] >= pd.Timestamp('2025-07-10') to avoid type errors.
- When using reset_index(), use named group keys (not anonymous functions), or extract and rename columns explicitly after.
- Assign the final result (DataFrame, Series, scalar *or* matplotlib Figure) to a variable named `result`.
- Create only ONE relevant plot. Set `figsize=(10, 6)`, add title/labels.
- Do NOT include `plt.show()` or any interactive display methods.
- Return your answer inside a single markdown fence that starts with ```python and ends with ```.
- If the code includes grouped or aggregated data, assign that DataFrame or Series to `table_result`, and also return `result = fig` for the plot.

Plotting Guidelines
-------------------
- Use a clear, descriptive title that summarizes the chart.
- Always label both axes with full words and units if available.
- Avoid numeric tick labels for categories — prefer names.
- Sort categorical x-axis values in logical order.
- Use marker='o' in line plots to show each point.
- Avoid raw timestamps on the x-axis; extract readable components like hour, weekday, or date.
"""

# ------------------ analysis_prompt_generator -------------------------
def analysis_prompt_generator(data: pd.DataFrame, user_question: str) -> str:
    """
    Creates a prompt to ask the LLM to write Python code using only pandas 
    (no plots) to analyze the data based on the given question.
    """
    column_names = list(data.columns)
    sample_rows = data.head(10).to_string(index=False)

    return f"""
You are given a pandas DataFrame named `df`.

Schema:
Columns: {', '.join(column_names)}

Preview:
{sample_rows}

Write Python code using pandas only (no plotting) to answer:
"{user_question}"

Rules
-----
- Use pandas operations on `df` only.
- DO NOT use .resample(). Instead, extract the date and use groupby for aggregation.
- Assume `df['timestamp']` is already a clean pandas datetime column.
- When analyzing by date, hour, or day of week, use: df['timestamp'].dt.date, .dt.hour, or .dt.day_name() as needed.
- When filtering a specific date, compute next_day = target_day + pd.Timedelta(days=1) and filter between [target_day, next_day).
- When filtering, always use `.copy()` to avoid chained assignment warnings.
- When using reset_index(), use named group keys (not anonymous functions), or extract and rename columns explicitly after.
- Assign the final result to result.
- Always return the code inside a single fenced code block that starts with ```python and ends with ```. Never include prose or explanation outside this code block.
"""
