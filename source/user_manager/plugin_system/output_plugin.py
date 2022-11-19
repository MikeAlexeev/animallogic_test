from abc import abstractmethod

from .base_plugin import BasePlugin
from .plugin_type import PluginType


class OutputPlugin(BasePlugin):
    TYPE = PluginType.OUTPUT

    @abstractmethod
    def do_output(self, data: dict) -> None:
        pass
