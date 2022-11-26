import pytest

from user_manager.default_plugins.json_storage_plugin import FilterMatcher


@pytest.mark.parametrize(
    "value,pattern,is_matched",
    [
        ("abc", "abc", True),
        ("abc", "ab", True),
        ("abc", "..", True),
        ("abc", "b", False),
        ("abc", "x", False),
    ],
)
def test_filter_matcher_match_pattern(value: str, pattern: str, is_matched: bool):
    assert FilterMatcher.match_pattern(value, pattern) == is_matched


@pytest.mark.parametrize(
    "values_dict,patterns_dict,is_matched",
    [
        (
            {
                "field_1": "abc",
                "field_2": "567",
            },
            {
                "field_2": "56",
            },
            True,
        ),
        ({}, {}, True),
        (
            {
                "field_1": "abc",
                "field_2": "567",
            },
            {
                "field_3": "other pattern",
            },
            False,
        ),
    ],
)
def test_filter_matcher_match_patterns_dict(
    values_dict: dict, patterns_dict: dict, is_matched: bool
):
    assert FilterMatcher.match_patterns_dict(values_dict, patterns_dict) == is_matched
