# Extract the function name from the custom function string
def extract_function_name(custom_function_str: str):
    lines = custom_function_str.splitlines()
    for line in lines:
        if line.strip().startswith("def "):
            return line.split()[1].split("(")[0]
