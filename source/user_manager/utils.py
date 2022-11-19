import random
import string
from pathlib import Path


def random_string(length: int) -> str:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def convert_path_to_module_name(path: Path) -> str:
    underscore = "_"

    def _process_char(char: str) -> str:
        return char if char.isalnum() else underscore

    processed = "".join(_process_char(char) for char in str(path).lower())
    if not processed.startswith(underscore):
        processed = underscore + processed

    if not processed.isidentifier():
        raise ValueError(f"not a valid identifier: {processed}, converted from: {path}")

    return processed
