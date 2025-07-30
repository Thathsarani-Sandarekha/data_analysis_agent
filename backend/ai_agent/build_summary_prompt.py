from typing import Any
import pandas as pd
import matplotlib.pyplot as plt

def create_reasoning_prompt(user_question: str, result_output: Any, table_preview: Any = None) -> str:
    """
    Builds a reasoning prompt for the LLM using the user question, the result (plot, table, or error),
    and optional table data to describe the output clearly.
    """

    # Check if the result is an error
    is_error = isinstance(result_output, str) and result_output.startswith("Error executing code")

    # Check if the result is a matplotlib plot
    is_chart = isinstance(result_output, (plt.Figure, plt.Axes))

    # Build description depending on the result type
    if is_error:
        description = result_output

    elif is_chart:
        # Try to get the chart title if available
        chart_title = ""
        if isinstance(result_output, plt.Figure):
            chart_title = result_output._suptitle.get_text() if result_output._suptitle else ""
        elif isinstance(result_output, plt.Axes):
            chart_title = result_output.get_title()

        description = f"[Chart Title: {chart_title or 'Untitled'}]"

        # Include table preview if available
        if table_preview is not None and isinstance(table_preview, pd.DataFrame):
            preview = table_preview.head(10).to_string(index=False)
            description += f"\nChart data preview:\n{preview}"

    else:
        # Just convert the result to a string, limit to 500 chars
        description = str(result_output)[:500]

    # Final prompt depending on chart or non-chart result
    if is_chart:
        return f'''
User question: "{user_question}"

The following chart is generated in response. {description}

Summarize the insights shown in this chart in 3-5 sentences. Focus on patterns, extremes, and trends. Avoid mentioning chart or code.
'''.strip()
    else:
        return f'''
User question: "{user_question}"

The following result was returned from the analysis: {description}

Explain in 3-5 sentences what this tells us about the data. Focus on what stands out, changes over time, or comparisons between values.
'''.strip()
