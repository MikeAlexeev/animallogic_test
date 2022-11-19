from abc import abstractmethod

from ..action_type import ActionType
from .base_plugin import BasePlugin


class OutputPlugin(BasePlugin):
    TYPE = ActionType.OUTPUT

    @abstractmethod
    def run_action(self, data: dict) -> None:
        pass
