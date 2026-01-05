import re

LINK_REGEX = re.compile(
    r"(https?:\/\/|www\.|fb\.me|bit\.ly|t\.co)",
    re.IGNORECASE
)

def has_link(text: str) -> bool:
    if not text:
        return False
    return bool(LINK_REGEX.search(text))
