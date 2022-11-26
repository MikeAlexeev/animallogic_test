from abc import abstractmethod

from .base_plugin import BasePlugin
from .base_record_plugin import BaseRecordPlugin


class BaseOutputPlugin(BasePlugin):
    @abstractmethod
    def output_user(self, username: str, record: BaseRecordPlugin) -> None:
        pass

    @abstractmethod
    def output_not_found_error(self, username: str) -> None:
        pass
