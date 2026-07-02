import re


def is_empty(value):
    return value is None or str(value).strip() == ""


def is_valid_email(email):
    if is_empty(email):
        return False

    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email.strip()) is not None


def is_valid_phone(phone):
    if is_empty(phone):
        return True

    pattern = r"^(0|\+84)[0-9]{9}$"
    return re.match(pattern, phone.strip()) is not None
