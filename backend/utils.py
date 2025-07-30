def get_first_python_code_block(markdown_text: str) -> str:
    """
    Extracts the first Python code block from a markdown-formatted string.
    Returns an empty string if no code block is found.
    """
    # Find the start of the ```python block
    start_index = markdown_text.find("```python")
    if start_index == -1:
        return ""

    # Move past the ```python tag
    start_index += len("```python")

    # Find the end of the code block
    end_index = markdown_text.find("```", start_index)
    if end_index == -1:
        return ""

    # Return the code inside the block, stripped of extra whitespace
    return markdown_text[start_index:end_index].strip()
