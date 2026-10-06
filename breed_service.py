import json
import os

from functools import lru_cache
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from validation import validate_text


API_URL = "https://api.thecatapi.com/v1/breeds?lang=en"
TIMEOUT_SECONDS = 10
MAX_RESPONSE_BYTES = 2_000_000

REFERENCE_FILE = (
    Path(__file__).resolve().parent
    / "data"
    / "cat_breeds_reference.json"
)


class BreedServiceError(Exception):
    pass


def comparison_key(text):
    # Normalize only for comparison.
    return " ".join(text.split()).casefold()


def get_online_breed_names():
    api_key = os.environ.get("CAT_API_KEY", "").strip()

    if not api_key:
        raise BreedServiceError(
            "Notice: The API key is missing.\n"
            "Help: Configure CAT_API_KEY or use the saved reference."
        )

    request = Request(
        API_URL,
        headers={
            "x-api-key": api_key,
            "Accept": "application/json",
            "User-Agent": "PetCatLearningActivity/1.0"
        }
    )

    try:
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            payload = response.read(MAX_RESPONSE_BYTES + 1)

    except HTTPError as error:
        raise BreedServiceError(
            f"Notice: The online reference returned HTTP {error.code}.\n"
            "Help: Check your API settings or try again later."
        ) from None

    except (URLError, TimeoutError, OSError):
        raise BreedServiceError(
            "Notice: The online reference is unavailable.\n"
            "Help: Check your connection or use the saved reference."
        ) from None

    if len(payload) > MAX_RESPONSE_BYTES:
        raise BreedServiceError(
            "Notice: The online reference response is too large.\n"
            "Help: Try again later."
        )

    try:
        records = json.loads(payload.decode("utf-8"))

    except (UnicodeDecodeError, json.JSONDecodeError):
        raise BreedServiceError(
            "Notice: The online reference returned unreadable data.\n"
            "Help: Try again later."
        ) from None

    if not isinstance(records, list) or not records:
        raise BreedServiceError(
            "Notice: The online reference returned no usable breed list.\n"
            "Help: Try again later."
        )

    names = set()

    for record in records:
        if not isinstance(record, dict):
            raise BreedServiceError(
                "Notice: The online breed data has an unexpected format.\n"
                "Help: Try again later."
            )

        name = record.get("name")

        if not isinstance(name, str) or not name.strip():
            raise BreedServiceError(
                "Notice: The online breed data is incomplete.\n"
                "Help: Try again later."
            )

        names.add(comparison_key(name))

    return frozenset(names)


def get_saved_breed_names():
    try:
        with REFERENCE_FILE.open("rb") as file:
            payload = file.read(MAX_RESPONSE_BYTES + 1)

    except OSError:
        raise BreedServiceError(
            "Notice: The saved breed reference could not be opened.\n"
            "Help: Include data/cat_breeds_reference.json "
            "in the project and try again."
        ) from None

    if len(payload) > MAX_RESPONSE_BYTES:
        raise BreedServiceError(
            "Notice: The saved breed reference is too large.\n"
            "Help: Replace it with the original reference file."
        )

    try:
        snapshot = json.loads(payload.decode("utf-8"))

    except (UnicodeDecodeError, json.JSONDecodeError):
        raise BreedServiceError(
            "Notice: The saved breed reference is unreadable.\n"
            "Help: Replace it with the original reference file."
        ) from None

    if not isinstance(snapshot, dict):
        raise BreedServiceError(
            "Notice: The saved reference has an unexpected format.\n"
            "Help: Replace it with the original reference file."
        )

    names = snapshot.get("breed_names")

    if not isinstance(names, list) or not names:
        raise BreedServiceError(
            "Notice: The saved reference contains no usable breed list.\n"
            "Help: Replace it with the original reference file."
        )

    if any(
        not isinstance(name, str) or not name.strip()
        for name in names
    ):
        raise BreedServiceError(
            "Notice: The saved reference contains incomplete breed data.\n"
            "Help: Replace it with the original reference file."
        )

    return frozenset(comparison_key(name) for name in names)


@lru_cache(maxsize=1)
def get_breed_names():
    api_key = os.environ.get("CAT_API_KEY", "").strip()
    online_error = None

    if api_key:
        try:
            return get_online_breed_names()

        except BreedServiceError as error:
            online_error = error

    try:
        names = get_saved_breed_names()

    except BreedServiceError as saved_error:
        if online_error is not None:
            raise BreedServiceError(
                f"{online_error}\n{saved_error}"
            ) from None

        if not api_key:
            raise BreedServiceError(
                "Notice: No API key is configured and the saved "
                "breed reference is unavailable or unreadable.\n"
                "Help: Restore data/cat_breeds_reference.json "
                "or configure CAT_API_KEY."
            ) from None

        raise

    if online_error is not None:
        print(
            "Notice: Online verification is unavailable. "
            "Using the saved breed reference."
        )
    else:
        print(
            "Notice: Using the saved breed reference "
            "without an API key."
        )

    return names


def validate_breed(raw, field):
    text = validate_text(raw, field)
    known_names = get_breed_names()

    if comparison_key(text) not in known_names:
        raise ValueError(
            f"Error: {field} was not found in the breed reference.\n"
            "Help: Check the spelling and enter the full breed name, "
            "such as Persian or Scottish Fold."
        )

    # Preserve the user's capitalization and internal spaces.
    return text