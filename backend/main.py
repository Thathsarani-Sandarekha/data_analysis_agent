import os
from ai_agent.generate_code import generate_code_from_query
from ai_agent.code_executor import run_generated_code
from data_loader import load_combined_df
from ai_agent.response_formatter import create_response_package

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load full DataFrame globally
DATA_DIR = "/Users/thathsarani/Desktop/Eutech Assignment/data_analysis_agent/sensor-data"
full_df = load_combined_df(DATA_DIR)

def run_agent_pipeline(user_q: str) -> dict:
    try:
        # Generate code and detect if plot needed
        code, should_plot_flag = generate_code_from_query(user_q, full_df)
        print("✅ Generated code:\n", code)
        
        # Execute generated code
        result_obj, table_obj = run_generated_code(code, full_df, should_plot_flag)

        # Generate final summary + assets
        response = create_response_package(user_q, result_obj, should_plot_flag, table_obj)

        return response

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "summary": f"Error: {str(e)}",
            "table": [],
            "chart_path": None
        }
