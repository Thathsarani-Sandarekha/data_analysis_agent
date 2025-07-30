from ai_agent.llm_client import client, GROQ_MODEL

def is_visual_query(user_question: str) -> bool:
    """
    Checks if the user is asking for a chart or visual output.
    Uses the LLM to detect if the question needs a plot.
    Returns True if it's a visual request, otherwise False.
    """
    
    messages = [
        {
            "role": "system",
            "content": (
                "detailed thinking off. You are an assistant that determines if a query is requesting a data visualization. "
                "Respond with only 'true' if the query is asking for a plot, chart, graph, or any visual representation of data. "
                "Otherwise, respond with 'false'."
            )
        },
        {"role": "user", "content": user_question}
    ]

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.1,
        max_tokens=5
    )

    answer = response.choices[0].message.content.strip().lower()
    return answer == "true"
