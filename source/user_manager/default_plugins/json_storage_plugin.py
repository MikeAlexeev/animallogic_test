import json
from pathlib import Path
from typing import Optional

from user_manager.plugin_system.base_record_plugin import BaseRecordPlugin
from user_manager.plugin_system.base_storage_plugin import BaseStoragePlugin


class JsonStoragePlugin(BaseStoragePlugin):
    NAME = "json"
    STORAGE_PATH = Path("/tmp/users.json")  # defined here for simplicity

    def get(self, username: str) -> Optional[BaseRecordPlugin]:
        raw_data = self._load_raw_data()
        if username not in raw_data:
            return None
        raw_user_data = raw_data[username]
        return self._record_type(**raw_user_data)

    def set(self, username: str, record: BaseRecordPlugin) -> None:
        raw = self._load_raw_data()
        raw[username] = record.to_dict()
        self._save_raw_data(raw)

    def remove(self, username: str) -> None:
        raw_data = self._load_raw_data()
        raw_data.pop(
            username, None
        )  # not raise exception for absent user, behavior is not specified
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
