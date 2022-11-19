from abc import abstractmethod

from .base_plugin import BasePlugin
from ..action_type import ActionType


class OutputPlugin(BasePlugin):
    TYPE = ActionType.OUTPUT

    @abstractmethod
    def run_action(self, data: dict) -> None:
        pass
