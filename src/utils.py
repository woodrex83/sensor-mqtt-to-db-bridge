import re

def convert_keys(message: dict) -> dict:
    """
    Convert keys to a suitable format for a database.
    It replaces any camelCase keys with snake_case
    """
    new_dict = {}
    for key, value in message.items():
        if isinstance(value, dict):
            value = convert_keys(value)
        new_key = re.sub("([a-z0-9])([A-Z])", r"\1_\2", key)
        new_key = new_key.lower()
        new_dict[new_key] = value
    return new_dict

def rename_fields(payload: dict, field_mapping: dict) -> dict:
    for old_name, new_name in field_mapping.items():
        if old_name in payload:
            payload[new_name] = payload.pop(old_name)
    return payload