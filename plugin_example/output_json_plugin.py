import json
from typing import Any, Dict, Iterable, Optional

from user_manager.api.base_plugins.base_output_plugin import BaseOutputPlugin
from user_manager.api.base_plugins.base_record_plugin import BaseRecordPlugin


class RecordJsonEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Iterable:
        if isinstance(obj, BaseRecordPlugin):
            return obj.to_dict()

        return super().default(obj)


class OutputJsonPlugin(BaseOutputPlugin):
    NAME = "json"

    def output_user(
        self, username: str, user_records: Dict[str, BaseRecordPlugin]
    ) -> None:
        self._do_output({username: user_records})

    def output_users(
        self, users_records: Dict[str, Dict[str, BaseRecordPlugin]]
    ) -> None:
        self._do_output(users_records)

    def output_user_record(
        self, username: str, dataset_name: str, user_record: BaseRecordPlugin
    ) -> None:
        data = {username: {dataset_name: user_record}}
        self._do_output(data)

    def output_not_found_error(
        self, username: str, dataset_name: Optional[str] = None
    ) -> None:
        if dataset_name:
            msg = (
                f"record from '{dataset_name}' dataset for '{username}' user not found"
            )
        else:
            msg = f"records for '{username}' user not found"

        self._do_output({"error": msg})

    def _dump_json(self, data: dict) -> str:
        return json.dumps(data, indent=2, sort_keys=True, cls=RecordJsonEncoder)

    def _do_output(self, data: Any) -> None:
        print(self._dump_json(data))
