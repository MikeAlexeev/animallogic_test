import sys
from typing import Dict, Optional

from ..api.base_plugins.base_output_plugin import BaseOutputPlugin
from ..api.base_plugins.base_record_plugin import BaseRecordPlugin


class OutputSimplePlugin(BaseOutputPlugin):
    NAME = "simple"

    def output_user(
        self, username: str, user_records: Dict[str, BaseRecordPlugin]
    ) -> None:
        for dataset_name, user_record in sorted(user_records.items()):
            self.output_user_record(username, dataset_name, user_record)

    def output_users(
        self, users_records: Dict[str, Dict[str, BaseRecordPlugin]]
    ) -> None:
        for username, user_records in users_records.items():
            self.output_user(username, user_records)

    def output_user_record(
        self, username: str, dataset_name: str, user_record: BaseRecordPlugin
    ) -> None:
        print(
            f"user: '{username}', dataset: '{dataset_name}', data: {user_record.to_dict()}"
        )

    def output_not_found_error(
        self, username: str, dataset_name: Optional[str] = None
    ) -> None:
        if dataset_name:
            msg = (
                f"record from '{dataset_name}' dataset for '{username}' user not found"
            )
        else:
            msg = f"records for '{username}' user not found"

        print(msg, file=sys.stderr)
