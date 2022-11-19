import json
from dataclasses import asdict
from pathlib import Path
from typing import Type

from user_manager.storage.base_storage import BaseStorage
from user_manager.storage.base_user_record import BaseUserRecord


class JsonStorage(BaseStorage):
    def __init__(self, json_path: Path, record_type: Type[BaseUserRecord]):
        self._json_path = json_path
        self._record_type = record_type

    def get(self, username: str) -> BaseUserRecord:
        raw = self._load_raw_data()[username]
        return self._record_type(**raw)

    def set(self, username: str, record: BaseUserRecord) -> None:
        raw = self._load_raw_data()
        raw[username] = asdict(record)
        self._save_raw_data(raw)

    def _load_raw_data(self) -> dict:
        with self._json_path.open() as f:
            return json.load(f)

    def _save_raw_data(self, data: dict) -> None:
        with self._json_path.open('w') as f:
            # TODO use temp file
            json.dump(data, f)
