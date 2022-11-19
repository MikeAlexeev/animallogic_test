from abc import abstractmethod

from .base_plugin import BasePlugin
from .base_record_plugin import BaseRecordPlugin


class BaseOutputPlugin(BasePlugin):
    @abstractmethod
    def do_output(self, username: str, record: BaseRecordPlugin) -> None:
        pass
