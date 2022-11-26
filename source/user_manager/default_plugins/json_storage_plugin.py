import json
import re
from pathlib import Path
from typing import Dict, Optional, Set

from user_manager.plugin_system.base_record_plugin import BaseRecordPlugin
from user_manager.plugin_system.base_storage_plugin import BaseStoragePlugin


class FilterMatcher:
    @classmethod
    def match_filter(cls, value: str, pattern: str) -> bool:
        return bool(re.match(pattern, value))

    @classmethod
    def match_filters_dict(cls, data: Dict[str, str], filters: Dict[str, str]) -> bool:
        for key, value in data.items():
            if key not in filters:
                continue
            if cls.match_filter(value, filters[key]):
                return True

        return False


class JsonStoragePlugin(BaseStoragePlugin):
    NAME = "json"
    STORAGE_PATH = Path("/tmp/users.json")  # defined here for simplicity

    def get_all_records_for_user(
        self, username: str
    ) -> Optional[Dict[str, BaseRecordPlugin]]:
        raw_data = self._load_raw_data()
        if username not in raw_data:
            return None

        user_data = raw_data[username]

        return {
            dataset_name: self._record_type.from_dict(data)
            for dataset_name, data in user_data.items()
        }

    def get_user_record(
        self, username: str, dataset_name: str
    ) -> Optional[BaseRecordPlugin]:
        user_records = self.get_all_records_for_user(username)
        if not user_records:
            return None

        if dataset_name not in user_records:
            return None

        return user_records[dataset_name]

    def get_all_users_records(self) -> Dict[str, Dict[str, BaseRecordPlugin]]:
        raw_data = self._load_raw_data()

        parsed_data: Dict[str, Dict[str, BaseRecordPlugin]] = {}
        for username, user_records in raw_data.items():
            parsed_data[username] = {}
            for dataset_name, data in user_records.items():
                parsed_data[username][dataset_name] = self._record_type.from_dict(data)

        return parsed_data

    def search_users(self, filters: Dict[str, str]) -> Dict[str, Dict[str, BaseRecordPlugin]]:
        found_users: Set[str] = set()
        all_users_records = self.get_all_users_records()
        for username, user_records in all_users_records.items():
            if 'username' in filters and FilterMatcher.match_filter(username, filters['username']):
                found_users.add(username)
                continue

            for _, record in user_records.items():
                if FilterMatcher.match_filters_dict(record.to_dict(), filters):
                    found_users.add(username)
                    continue

        return {username: records for username, records in all_users_records.items() if username in found_users}

    def set_user_record(
        self, username: str, dataset_name: str, record: BaseRecordPlugin
    ) -> None:
        raw = self._load_raw_data()
        if username not in raw:
            raw[username] = {}

        raw[username][dataset_name] = record.to_dict()
        self._save_raw_data(raw)

    def remove_user(self, username: str) -> None:
        raw_data = self._load_raw_data()

        # not raise exception for absent user, behavior is not specified
        raw_data.pop(username, None)
        self._save_raw_data(raw_data)

    def remove_user_record(self, username: str, dataset_name: str) -> None:
        raw_data = self._load_raw_data()

        # not raise exception for absent user or dataset, behavior is not specified
        raw_data.get(username, {}).pop(dataset_name, None)
        self._save_raw_data(raw_data)

    def _load_raw_data(self) -> dict:
        if not self.STORAGE_PATH.exists():
            return {}

        with self.STORAGE_PATH.open() as f:
            return json.load(f)

    def _save_raw_data(self, data: dict) -> None:
        with self.STORAGE_PATH.open("w") as f:
            # TODO use temp file, then move
            json.dump(data, f)
