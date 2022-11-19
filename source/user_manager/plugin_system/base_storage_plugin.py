from abc import abstractmethod
from typing import Type

from .base_record_plugin import BaseRecordPlugin
from .base_plugin import BasePlugin


class BaseStoragePlugin(BasePlugin):
    def __init__(self, record_type: Type[BaseRecordPlugin]):
        self._record_type = record_type

    @abstractmethod
    def get(self, username: str) -> BaseRecordPlugin:
        pass

    @abstractmethod
    def set(self, username: str, record: BaseRecordPlugin) -> None:
        pass
