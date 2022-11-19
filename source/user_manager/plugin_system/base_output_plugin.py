from abc import abstractmethod

from .base_plugin import BasePlugin


class BaseOutputPlugin(BasePlugin):

    @abstractmethod
    def run_action(self, data: dict) -> None:
        pass
