import sys

from user_manager.plugin_system.base_output_plugin import BaseOutputPlugin
from user_manager.plugin_system.base_record_plugin import BaseRecordPlugin


class OutputSimplePlugin(BaseOutputPlugin):
    NAME = "simple"

    def output_user(self, username: str, record: BaseRecordPlugin) -> None:
        print(f"user: {username}, data: {record.to_dict()}")

    def output_not_found_error(self, username: str) -> None:
        print(f"record for '{username}' user not found", file=sys.stderr)
