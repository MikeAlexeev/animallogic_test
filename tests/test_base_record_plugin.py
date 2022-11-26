from dataclasses import dataclass

import pytest

from user_manager.api.base_plugins.base_record_plugin import BaseRecordPlugin


@dataclass
class TestRecord(BaseRecordPlugin):
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
            TestRecord(field_1=10, field_2="str_value"),
        ),
        (
            {
                "field_1": 10,
                "field_2": "str_value",
                "field_3": "garbage",
            },
            TestRecord(field_1=10, field_2="str_value"),
        ),
    ],
)
def test_base_record_from_dict(data_dict: dict, expected_model: TestRecord):
    assert TestRecord.from_dict(data_dict) == expected_model


@pytest.mark.parametrize(
    "model,expected_dict",
    [
        (
            TestRecord(field_1=10, field_2="str_value"),
            {
                "field_1": 10,
                "field_2": "str_value",
            },
        ),
    ],
)
def test_base_record_to_dict(model: TestRecord, expected_dict: dict):
    assert model.to_dict() == expected_dict
