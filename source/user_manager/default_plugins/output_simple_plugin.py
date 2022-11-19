from user_manager.plugin_system.base_output_plugin import BaseOutputPlugin
from user_manager.plugin_system.base_record_plugin import BaseRecordPlugin


class OutputSimplePlugin(BaseOutputPlugin):
    NAME = "simple"

    def do_output(self, username: str, record: BaseRecordPlugin) -> None:
        print(f"user: {username}, data: {record.to_dict()}")
