import re

def is_phone_num(input_str):
    pattern = r"^0?[1-9]\d{8}$" #regex pattern for phone number
    if re.match(pattern, input_str):
        return True
    return False

def is_card_id(input_str):
    pattern = r"^ZYW\d{4}$" #regex pattern for card id
    if re.match(pattern, input_str):
        return True
    return False