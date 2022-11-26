from dataclasses import dataclass

import pytest

from user_manager.api.base_plugins.base_record_plugin import BaseRecordPlugin


@dataclass
class _TestRecord(BaseRecordPlugin):
    field_1: int
    field_2: str

    NAME: str = "test_record"


@pytest.mark.parametrize(
    "data_dict,expected_model",
    [
        (
            {
                "field_1": 10,
                "field_2": "str_value",
            },
            _TestRecord(field_1=10, field_2="str_value"),
        ),
        (
            {
                "field_1": 10,
                "field_2": "str_value",
                "field_3": "garbage",
            },
            _TestRecord(field_1=10, field_2="str_value"),
        ),
    ],
)
def test_base_record_from_dict(data_dict: dict, expected_model: _TestRecord):
    assert _TestRecord.from_dict(data_dict) == expected_model


@pytest.mark.parametrize(
    "model,expected_dict",
    [
        (
            _TestRecord(field_1=10, field_2="str_value"),
            {
                "field_1": 10,
                "field_2": "str_value",
            },
        ),
    ],
)
def test_base_record_to_dict(model: _TestRecord, expected_dict: dict):
    assert model.to_dict() == expected_dict
