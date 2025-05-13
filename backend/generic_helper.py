import re

def extract_session_id(session_str: str):
    pattern = r"sessions/(.*?)/contexts"
    match = re.search(pattern, session_str)
    if match:
        extracted_session_id = match.group(1)
        return extracted_session_id

    return ""

def get_str_from_food_dict(food_dict: dict):
    result = ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
    return result