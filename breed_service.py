import json
import os

from functools import lru_cache
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from validation import validate_text


API_URL = "https://api.thecatapi.com/v1/breeds?lang=en"
TIMEOUT_SECONDS = 10
MAX_RESPONSE_BYTES = 2_000_000


class BreedServiceError(Exception):
    pass


def comparison_key(text):
    # Normalize for comparison only.
    return " ".join(text.split()).casefold()


@lru_cache(maxsize=1)
def get_breed_names():
    api_key = os.environ.get("CAT_API_KEY", "").strip()

    if not api_key:
        raise BreedServiceError(
            "Notice: Cat breed could not be checked because "
            "the API key is missing.\n"
            "Help: Set CAT_API_KEY in PyCharm's environment variables "
            "and restart the program."
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
        if error.code in (401, 403):
            guidance = (
                "Help: Check CAT_API_KEY in PyCharm "
                "and restart the program."
            )

        elif error.code == 429:
            guidance = (
                "Help: The service has limited requests. "
                "Wait a moment and try again."
            )

        else:
            guidance = "Help: Try again later."

        raise BreedServiceError(
            "Notice: Cat breed could not be checked because "
            f"the reference returned HTTP {error.code}.\n"
            f"{guidance}"
        ) from None

    except URLError as error:
        raise BreedServiceError(
            "Notice: The online reference could not be reached.\n"
            f"Connection detail: {error.reason}\n"
            "Help: Check the connection detail to identify the problem."
        ) from None

    except (TimeoutError, OSError) as error:
        raise BreedServiceError(
            "Notice: The connection failed or timed out.\n"
            f"Connection detail: {error}\n"
            "Help: Check your connection and try again."
        ) from None

    if len(payload) > MAX_RESPONSE_BYTES:
        raise BreedServiceError(
            "Notice: The reference response is too large to process.\n"
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
                "Notice: The reference returned an unexpected data format.\n"
                "Help: Try again later."
            )

        name = record.get("name")

        if not isinstance(name, str) or not name.strip():
            raise BreedServiceError(
                "Notice: The reference returned incomplete breed data.\n"
                "Help: Try again later."
            )

        names.add(comparison_key(name))

    # Reuse successful results during this program session.
    # Failed requests are not cached.
    return frozenset(names)


def validate_breed(raw, field):
    text = validate_text(raw, field)
    known_names = get_breed_names()

    if comparison_key(text) not in known_names:
        raise ValueError(
            f"Error: {field} was not found in the online reference.\n"
            "Help: Check the spelling and enter the full breed name, "
            "such as Persian or Scottish Fold."
        )

    # Preserve the user's capitalization and internal spaces.
    return text