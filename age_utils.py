def format_age(years, months):
    parts = []

    if years > 0:
        unit = "year" if years == 1 else "years"
        parts.append(f"{years} {unit}")

    if months > 0:
        unit = "month" if months == 1 else "months"
        parts.append(f"{months} {unit}")

    if not parts:
        return "0 months"

    return " and ".join(parts)