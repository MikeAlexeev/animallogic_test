from user_manager.plugin_system.base_output_plugin import BaseOutputPlugin


class OutputSimple(BaseOutputPlugin):
    NAME = 'simple'

    def run_action(self, data: dict) -> None:
        print(data)
