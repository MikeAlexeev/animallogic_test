from pathlib import Path

import pytest

from user_manager import utils


@pytest.mark.parametrize(
    "path,module_name",
    [
        ("/a/b/c", "_a_b_c"),
        ("/a/b c", "_a_b_c"),
        ("./a/b c", "_a_b_c"),  # ./ is removed in Path
    ],
)
def test_convert_path_to_module_name(path: str, module_name: str):
    print(Path(path))
    assert utils.convert_path_to_module_name(Path(path)) == module_name
