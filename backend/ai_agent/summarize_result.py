from typing import Any
from ai_agent.llm_client import client, GROQ_MODEL
from ai_agent.build_summary_prompt import create_reasoning_prompt

def explain_result_to_user(user_question: str, result_data: Any, table_info: Any = None) -> str:
    """
    Uses the LLM to generate a simple explanation for the given result or chart.
    Returns a 3-5 sentence user-friendly summary.
    """

    # Prepare the input message for the LLM
    prompt_text = create_reasoning_prompt(user_question, result_data, table_info)

    # Ask the LLM to explain the result clearly and politely
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior data analyst. If the result contains valid data, explain the findings clearly in 3–5 user-friendly sentences. "
                    "Focus on patterns, comparisons, or anomalies. Avoid generic phrases like 'This analysis shows...' — get straight to the insight. "
                    "If the result indicates an error or failed code execution, DO NOT include technical error messages. "
                    "Instead, briefly explain that something went wrong and suggest the user rephrase the question or try again later. "
                    "Keep the tone polite, professional, and reassuring."
                )
            },
            {
                "role": "user",
                "content": prompt_text
            }
        ],
        temperature=0.2,
        max_tokens=512
    )

    return response.choices[0].message.content.strip()
