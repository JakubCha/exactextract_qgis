def extract_function_name(custom_function_str: str) -> str:
    """
    Extract the function name from the custom function string

    Args:
        custom_function_str (str): function string defined by user.

    Returns:
        str: function string without def
    """
    lines = custom_function_str.splitlines()
    for line in lines:
        if line.strip().startswith("def "):
            return line.split()[1].split("(")[0]
