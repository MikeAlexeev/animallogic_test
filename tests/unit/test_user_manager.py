from typing import Dict, Optional, Type

import mock
import pytest

from user_manager.api.base_plugins.base_record_plugin import BaseRecordPlugin
from user_manager.api.system_configuration import SystemConfiguration
from user_manager.api.user_manager import UserManager
from user_manager.default_plugins.user_record_plugin import UserRecordPlugin


class _TestStorage:
    @classmethod
    def __new__(cls, *args, **kwargs):
        # workaround for __new__ patch problem (https://github.com/pytest-dev/pytest/discussions/8009)
        return super().__new__(cls)

    def __init__(self, record_type: Type[BaseRecordPlugin]):
        pass

    def set_user_record(
        self, username: str, dataset_name: str, record: BaseRecordPlugin
    ) -> None:
        if username not in self._data:
            self._data[username] = {}

        self._data[username][dataset_name] = record

    def get_user_record(
        self, username: str, dataset_name: str
    ) -> Optional[BaseRecordPlugin]:
        return self._data.get(username, {}).get(dataset_name)

    def get_all_records_for_user(self, username: str) -> Dict[str, BaseRecordPlugin]:
        return self._data.get(username, {})

    def remove_user_record(self, username: str, dataset_name: str) -> None:
        self._data.get(username, {}).pop(dataset_name, None)

    def remove_user(self, username: str) -> None:
        self._data.pop(username, {})


@pytest.fixture
def test_storage() -> _TestStorage:
    storage = _TestStorage(record_type=UserRecordPlugin)
    storage._data = {}
    yield storage


def test_user_manager_save_user(test_storage):
    system_configuration = SystemConfiguration()
    user_manager = UserManager(system_configuration)

    with mock.patch.object(
        system_configuration, "get_storage_cls", return_value=_TestStorage
    ), mock.patch.object(_TestStorage, "__new__", return_value=test_storage):

        user_manager.save_user(
            "user_1", "work", {"address": "addr", "phone_number": "+12345"}
        )

        assert test_storage.get_user_record("user_1", "work").to_dict() == {
            "address": "addr",
            "phone_number": "+12345",
        }

        user_manager.save_user("user_1", "work", {"address": "changed_addr"})

        assert test_storage.get_user_record("user_1", "work").to_dict() == {
            "address": "changed_addr",
            "phone_number": "+12345",
        }


def test_user_manager_remove_user(test_storage):
    system_configuration = SystemConfiguration()
    user_manager = UserManager(system_configuration)

    with mock.patch.object(
        system_configuration, "get_storage_cls", return_value=_TestStorage
    ), mock.patch.object(_TestStorage, "__new__", return_value=test_storage):

        user_manager.save_user(
            "user_1", "work", {"address": "addr", "phone_number": "+12345"}
        )

        user_manager.save_user(
            "user_1", "personal", {"address": "home_addr", "phone_number": "+234"}
        )

        assert test_storage.get_user_record("user_1", "work").to_dict() == {
            "address": "addr",
            "phone_number": "+12345",
        }

        assert test_storage.get_user_record("user_1", "personal").to_dict() == {
            "address": "home_addr",
            "phone_number": "+234",
        }

        user_manager.remove_user("user_1", "personal")

        assert test_storage.get_user_record("user_1", "personal") is None
        assert test_storage.get_user_record("user_1", "work")

        user_manager.remove_user("user_1")

        assert test_storage.get_user_record("user_1", "work") is None
        assert test_storage.get_user_record("user_1", "personal") is None
        assert not test_storage.get_all_records_for_user("user_1")
