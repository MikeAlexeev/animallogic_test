from user_manager.plugin_system.output_plugin import OutputPlugin


class OutputSimple(OutputPlugin):
    NAME = 'simple'

    def run_action(self, data: dict):
        print(data)
