import os
import uuid
import pandas as pd
import matplotlib.pyplot as plt
import re
from ai_agent.summarize_result import explain_result_to_user

# ------------------ format_column_name ----------------------------------
def format_column_name(column: str) -> str:
    """
    Make column names look nice: add spaces, capitalize words, and handle special cases like CO2.
    """
    column = column.strip()
    if column.lower() in {'co2', 'pm2.5', 'pm10', 'o2', 'no2', 'rh'}:
        return column.upper()

    # Add spaces for underscores, hyphens, or camelCase
    spaced = re.sub(r'[_\-]+', ' ', column)
    spaced = re.sub(r'([a-z])([A-Z])', r'\1 \2', spaced)
    words = spaced.strip().split()
    return ' '.join(word.capitalize() for word in words)

# ------------------ create_response_package ------------------------------
def create_response_package(user_question, chart_object, is_plot, table_object=None):
    """
    Combines the explanation, table formatting, and chart saving into one result dictionary.
    """

    # Use table for explanation if available, otherwise use chart
    explanation_input = table_object if table_object is not None else chart_object
    summary = explain_result_to_user(user_question, explanation_input)

    # Prepare table data (if any)
    table_data = None

    if isinstance(table_object, pd.DataFrame):
        df = table_object.copy()

        # Try to extract chart legend labels
        legend_labels = []
        if is_plot and isinstance(chart_object, (plt.Figure, plt.Axes)):
            ax = chart_object.gca() if isinstance(chart_object, plt.Figure) else chart_object
            legend = ax.get_legend()
            if legend:
                legend_labels = [label.get_text() for label in legend.get_texts()]

        # Rename columns using legend labels or just beautify them
        if legend_labels:
            value_columns = [col for col in df.columns if df[col].dtype in ['float64', 'int64']]
            if len(value_columns) == len(legend_labels):
                rename_map = {value_columns[i]: legend_labels[i] for i in range(len(value_columns))}
                df.rename(columns=rename_map, inplace=True)
            else:
                df.rename(columns=lambda col: format_column_name(str(col)), inplace=True)
        else:
            df.rename(columns=lambda col: format_column_name(str(col)), inplace=True)

        # Round numbers for better display
        rounded_df = df.copy()
        for col in rounded_df.select_dtypes(include='number').columns:
            rounded_df[col] = rounded_df[col].round(2)

        table_data = rounded_df.head(20).to_dict(orient="records")

    elif isinstance(table_object, pd.Series):
        df = table_object.to_frame().reset_index()
        df.rename(columns=lambda col: format_column_name(str(col)), inplace=True)
        table_data = df.to_dict(orient="records")

    # Save chart to file
    chart_path = None
    if is_plot and isinstance(chart_object, (plt.Figure, plt.Axes)):
        fig = chart_object.figure if isinstance(chart_object, plt.Axes) else chart_object
        output_folder = "charts"
        os.makedirs(output_folder, exist_ok=True)
        filename = f"{uuid.uuid4().hex[:8]}.png"
        full_path = os.path.join(output_folder, filename)
        fig.savefig(full_path)
        chart_path = f"{output_folder}/{filename}"

    # Final response with all parts
    return {
        "summary": summary,
        "table": table_data,
        "chart_path": chart_path
    }
