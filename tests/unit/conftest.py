from pathlib import Path

import pytest


@pytest.fixture
def data_dir() -> Path:
    return Path(__file__).resolve().parent / "data"


@pytest.fixture
def plugins_dir(data_dir: Path) -> Path:
    return data_dir / "plugins"
