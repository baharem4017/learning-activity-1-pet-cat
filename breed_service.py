"""Validate cat breeds against a fixed, local Python list.

The supported names were copied from the supplied cat_breeds_reference(10).json.
This is the project's reference list, not a claim to include every cat breed.
The program does not read JSON, contact an API, or require an API key at runtime.
"""

# Reuse the project's existing checks for text length and allowed characters.
from validation import validate_text

# Store all names from the supplied reference as lowercase Python strings.
# Lists do not have docstrings, so this explanation is a regular comment.
CAT_BREEDS = [
    "abyssinian",
    "aegean",
    "american bobtail",
    "american curl",
    "american ringtail",
    "american shorthair",
    "american wirehair",
    "aphrodite giant",
    "arabian mau",
    "asian semi-longhair",
    "australian mist",
    "balinese",
    "bambino",
    "bengal",
    "birman",
    "bombay",
    "brazilian shorthair",
    "british longhair",
    "british shorthair",
    "british tipped",
    "burmese",
    "burmilla",
    "burmoir",
    "california spangled",
    "caracat",
    "chantilly-tiffany",
    "chartreux",
    "chausie",
    "cheetoh",
    "colorpoint shorthair",
    "cornish rex",
    "cymric",
    "cyprus",
    "devon rex",
    "domestic longhair",
    "domestic mediumhair",
    "domestic shorthair",
    "donskoy",
    "dragon li",
    "dwelf",
    "egyptian mau",
    "elf cat",
    "european burmese",
    "european shorthair",
    "exotic longhair",
    "exotic shorthair",
    "foldex",
    "genetta",
    "german rex",
    "havana brown",
    "highlander",
    "himalayan",
    "japanese bobtail",
    "javanese",
    "kanaani",
    "kellas cat",
    "khao manee",
    "korat",
    "kurilian bobtail",
    "laperm",
    "lykoi",
    "maine coon",
    "malayan",
    "manx",
    "minskin",
    "minuet",
    "munchkin",
    "napoleon longhair",
    "nebelung",
    "norwegian forest cat",
    "ocicat",
    "ojos azules",
    "oriental longhair",
    "oriental shorthair",
    "pantherette",
    "persian",
    "peterbald",
    "pixie-bob",
    "polydactyl",
    "raas",
    "ragamuffin",
    "ragdoll",
    "russian blue",
    "safari",
    "savannah",
    "scottish fold",
    "selkirk rex",
    "serengeti",
    "siamese",
    "siberian",
    "singapura",
    "singapura tabby",
    "skookum",
    "snowshoe",
    "sokoke",
    "somali",
    "sphynx",
    "suphalak",
    "thai",
    "tonkinese",
    "toybob",
    "toyger",
    "turkish angora",
    "turkish van",
    "ukrainian levkoy",
    "york chocolate"
]


def validate_breed(raw, field):
    """Return accepted text when its breed appears in CAT_BREEDS.

    Args:
        raw: The text entered by the user.
        field: The field label used in validation error messages.

    First apply the existing text validator. Then compare lowercase names,
    ignoring repeated spaces for comparison only. Preserve the validated text's
    capitalization and internal spaces in the returned value.

    Raises:
        ValueError: The text is invalid or its breed is not in the local list.

    The Cat constructor calls this function before storing the public breed.
    The interactive input loop catches ValueError and asks for another entry.
    """
    # Reject invalid text and obtain the accepted text from the shared validator.
    text = validate_text(raw, field)

    # Make a comparison-only copy: lowercase letters and single word spaces.
    # split() separates words; join() reconnects them with one space.
    comparison_name = " ".join(text.lower().split())

    # Check membership in the local list; no file or network access is needed.
    if comparison_name in CAT_BREEDS:
        # Return the original validated text, not the comparison-only copy.
        return text

    # Report an unsupported name; the caller decides how to handle the error.
    raise ValueError(
        f"Error: {field} was not found in the supported breed list.\n"
        "Help: Check the spelling and enter a supported breed name, "
        "such as Persian or Scottish Fold."
    )
