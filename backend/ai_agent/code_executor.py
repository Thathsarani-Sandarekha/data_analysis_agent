import pandas as pd
import matplotlib.pyplot as plt
import io

def run_generated_code(generated_code: str, data: pd.DataFrame, needs_plot: bool):
    """
    Executes the AI-generated Python code safely with the given dataset.
    If a plot is needed, it also provides access to matplotlib.
    """

    # Setup the environment with necessary libraries and the DataFrame
    execution_env = {
        "pd": pd,
        "df": data
    }

    # If the result includes a plot, add plotting tools
    if needs_plot:
        plt.rcParams["figure.dpi"] = 100 
        execution_env["plt"] = plt
        execution_env["io"] = io

    try:
        # Run the code in the prepared environment
        exec(generated_code, {}, execution_env)

        # Get plot (if any) and table result
        plot_result = execution_env.get("result", None)
        table_result = execution_env.get("table_result", None)

        return (plot_result, table_result)

    except Exception as error:
        # Return the error if code fails
        return (f"Error executing code: {error}", None)