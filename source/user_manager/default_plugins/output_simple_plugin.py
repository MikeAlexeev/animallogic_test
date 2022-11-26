import sys
from typing import Dict, Optional

from user_manager.plugin_system.base_output_plugin import BaseOutputPlugin
from user_manager.plugin_system.base_record_plugin import BaseRecordPlugin


class OutputSimplePlugin(BaseOutputPlugin):
    NAME = "simple"

    def output_user(
        self, username: str, user_records: Dict[str, BaseRecordPlugin]
    ) -> None:
        for dataset_name, record in sorted(user_records.items()):
            print(
                f"user: '{username}', dataset: '{dataset_name}', data: {record.to_dict()}"
            )

    def output_not_found_error(self, username: str, dataset: Optional[str]) -> None:
        if dataset:
            msg = f"record from '{dataset}' dataset for '{username}' user not found"
        else:
            msg = f"records for '{username}' user not found"

        print(msg, file=sys.stderr)
