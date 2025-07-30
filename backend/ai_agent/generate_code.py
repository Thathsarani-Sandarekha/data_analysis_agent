import pandas as pd
from ai_agent.query_understanding import is_visual_query
from ai_agent.code_prompt_templates import plot_prompt_generator, analysis_prompt_generator
from ai_agent.llm_client import client, GROQ_MODEL
from utils import get_first_python_code_block

def generate_code_from_query(user_question: str, data_frame: pd.DataFrame):
    """Generate Python code using LLM based on user's question and dataset."""

    # Decide whether the question is asking for a plot or just analysis
    needs_plot = is_visual_query(user_question)

    # Create the prompt depending on whether a plot is needed
    if needs_plot:
        prompt_text = plot_prompt_generator(data_frame, user_question)
    else:
        prompt_text = analysis_prompt_generator(data_frame, user_question)

    # Prepare the message to send to the language model
    messages = [
        {
            "role": "system",
            "content": (
                "detailed thinking off. You are a Python data-analysis expert who writes clean, efficient code. "
                "Solve the given problem with optimal pandas operations. Be concise and focused. "
                "Your response must contain ONLY a properly-closed ```python code block with no explanations before or after. "
                "Ensure your solution is correct, handles edge cases, and follows best practices for data analysis."
            ),
        },
        {"role": "user", "content": prompt_text}
    ]

    # Call the language model to generate code
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.2
    )

    # Extract the actual Python code from the response
    full_text = response.choices[0].message.content
    generated_code = get_first_python_code_block(full_text)

    return generated_code, needs_plot