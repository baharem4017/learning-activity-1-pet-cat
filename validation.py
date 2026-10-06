MAX_TEXT_LENGTH = 30
MAX_NUMBER_DIGITS = 32


def validate_text(raw, field):
    if any(ord(char) < 32 or ord(char) == 127 for char in raw):
        raise ValueError(
            f"Error: {field} contains a control character.\n"
            "Help: Use English letters, spaces, hyphens, or apostrophes."
        )

    text = raw.strip(" ")

    if not text:
        if field == "Cat breed":
            guidance = "Help: Enter a breed, such as Persian."
        else:
            guidance = "Help: Enter a name, such as Dobby."

        raise ValueError(
            f"Error: {field} is empty.\n"
            f"{guidance}"
        )

    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError(
            f"Error: {field} is longer than 30 characters.\n"
            "Help: Enter no more than 30 characters, including spaces."
        )

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    allowed = letters + " -'"

    if any(char not in allowed for char in text):
        raise ValueError(
            f"Error: {field} contains an unsupported character.\n"
            "Help: Use English letters, spaces, hyphens, or apostrophes."
        )

    if not any(char in letters for char in text):
        raise ValueError(
            f"Error: {field} must contain at least one English letter.\n"
            "Help: Enter a name or breed containing English letters."
        )

    return text


def validate_integer(raw, field):
    is_month = field.endswith("additional months")

    if is_month:
        guidance = "Help: Enter a whole number from 0 to 11."
    else:
        guidance = "Help: Enter 0 or a positive integer."

    if any(ord(char) < 32 or ord(char) == 127 for char in raw):
        raise ValueError(
            f"Error: {field} contains a control character.\n"
            f"{guidance}"
        )

    text = raw.strip(" ")

    if not text:
        raise ValueError(
            f"Error: {field} is empty.\n"
            f"{guidance}"
        )

    digits = text

    if text[0] in "+-":
        digits = text[1:]

    if not digits or any(char not in "0123456789" for char in digits):
        raise ValueError(
            f"Error: {field} must be a whole number.\n"
            f"{guidance} Do not enter decimals or words."
        )

    if len(digits) > MAX_NUMBER_DIGITS:
        if is_month:
            size_help = guidance
        else:
            size_help = (
                "Help: Enter a number with no more than 32 digits."
            )

        raise ValueError(
            f"Error: {field} contains too many digits.\n"
            f"{size_help}"
        )

    value = int(text)

    if value < 0:
        raise ValueError(
            f"Error: {field} cannot be negative.\n"
            f"{guidance}"
        )

    # main.py checks the upper month boundary.
    return value