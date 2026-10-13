"""Format a pet's accepted age as readable text.

This module only builds text. validation.py and main.py check the input;
Pet.print_info() prints the text returned by format_age().
"""


def format_age(years, months):
    """Return completed years and additional months as an age description.

    Args:
        years: A nonnegative integer representing completed years.
        months: An integer from 0 to 11 representing additional months.

    Returns:
        A string such as "1 year and 3 months", "2 years", or "1 month".
        If both values are zero, return "0 months".

    Positive units are added to a list with append(). join() connects the
    parts with " and ". Singular words are used when the value is one.
    This function does not validate input or convert excess months to years.
    """
    # Start with an empty list to hold the years and months descriptions.
    parts = []

    # Include years only when the value is positive.
    if years > 0:
        # Choose "year" for one, otherwise choose "years".
        unit = "year" if years == 1 else "years"
        # Add the number and its unit as one string in the list.
        parts.append(f"{years} {unit}")

    # Include months only when the value is positive.
    if months > 0:
        # Choose "month" for one, otherwise choose "months".
        unit = "month" if months == 1 else "months"
        # Add the months description after any years description.
        parts.append(f"{months} {unit}")

    # An empty list means neither a years part nor a months part was added.
    if not parts:
        return "0 months"

    # Connect two parts with "and"; a single part is returned without a separator.
    return " and ".join(parts)
