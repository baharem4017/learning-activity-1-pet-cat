"""Check names, breed text, and age numbers using explicit loops.

This module uses no any() or strip(). Invalid input raises ValueError;
main.py displays the message and asks the user to try again.
"""

MAX_TEXT_LENGTH = 30  # Maximum accepted text length after edge spaces are removed.
MAX_NUMBER_DIGITS = 32  # Maximum digits, excluding an optional sign.


def remove_edge_spaces(raw):
    """Remove ordinary spaces at the edges while preserving internal spaces.

    Move two positions inward using while loops, then return the text between
    them. This has the same purpose as the previous strip(" ") call.
    Tabs and other control characters are not removed by this helper.
    """
    start = 0  # Begin at the first character.
    end = len(raw)  # End is the position just after the last character.

    # Stop at the first non-space, or when the string contains only spaces.
    while start < end and raw[start] == " ":
        start = start + 1

    # Move backward over trailing spaces without passing the start position.
    while end > start and raw[end - 1] == " ":
        end = end - 1

    # Slicing includes start but excludes end; equal positions return empty text.
    return raw[start:end]


def validate_text(raw, field):
    """Return valid name/breed text, preserving capitalization and internal spaces.

    Reject control characters, empty text, more than 30 characters, unsupported
    symbols, and text without an English letter. field labels error messages.
    This checks text format; breed_service.py checks breed-list membership.
    """
    # Inspect one character at a time before removing ordinary edge spaces.
    for char in raw:
        # ord gives the character code; these codes represent control characters.
        if ord(char) < 32 or ord(char) == 127:
            raise ValueError(
                f"Error: {field} contains a control character.\n"
                "Help: Use English letters, spaces, hyphens, or apostrophes."
            )

    text = remove_edge_spaces(raw)  # Keep spaces inside the text unchanged.

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

    # Reject the first character that is not in the allowed string.
    for char in text:
        if char not in allowed:
            raise ValueError(
                f"Error: {field} contains an unsupported character.\n"
                "Help: Use English letters, spaces, hyphens, or apostrophes."
            )

    # A flag remembers whether the loop has found an English letter.
    has_letter = False
    for char in text:
        if char in letters:
            has_letter = True
            break  # One letter is enough; stop searching.

    if not has_letter:
        raise ValueError(
            f"Error: {field} must contain at least one English letter.\n"
            "Help: Enter a name or breed containing English letters."
        )

    return text


def validate_integer(raw, field):
    """Return a nonnegative integer entered using at most 32 ASCII digits.

    Allow surrounding ordinary spaces and an optional plus/minus sign.
    Reject empty input, control characters, decimals, words, and negative values.
    main.py separately checks that additional months do not exceed eleven.
    """
    # Choose month-specific help when the field label ends with these words.
    is_month = field.endswith("additional months")

    if is_month:
        guidance = "Help: Enter a whole number from 0 to 11."
    else:
        guidance = "Help: Enter 0 or a positive integer."

    # Inspect one character at a time before removing ordinary edge spaces.
    for char in raw:
        # ord gives the character code; these codes represent control characters.
        if ord(char) < 32 or ord(char) == 127:
            raise ValueError(
                f"Error: {field} contains a control character.\n"
                f"{guidance}"
            )

    text = remove_edge_spaces(raw)  # Keep spaces inside the text unchanged.

    if not text:
        raise ValueError(
            f"Error: {field} is empty.\n"
            f"{guidance}"
        )

    digits = text

    # The earlier empty check makes accessing the first character safe.
    if text[0] in "+-":
        digits = text[1:]  # Exclude the sign when checking/counting digits.

    # Empty digits (for example, just "+") cannot represent an integer.
    valid_digits = True
    if digits == "":
        valid_digits = False

    # Check each remaining character against the ten allowed digits.
    for char in digits:
        if char not in "0123456789":
            valid_digits = False
            break  # One invalid character is enough to reject the input.

    if not valid_digits:
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

    value = int(text)  # Convert only after the text passes the digit checks.

    if value < 0:
        raise ValueError(
            f"Error: {field} cannot be negative.\n"
            f"{guidance}"
        )

    # main.py checks the upper month boundary.
    return value