from abc import abstractmethod
from typing import Dict, Optional, Type

from .base_plugin import BasePlugin
from .base_record_plugin import BaseRecordPlugin


class BaseStoragePlugin(BasePlugin):
    def __init__(self, record_type: Type[BaseRecordPlugin]):
        self._record_type = record_type

    @abstractmethod
    def get_records_for_user(
        self, username: str, dataset_name: Optional[str]
    ) -> Optional[Dict[str, BaseRecordPlugin]]:
        pass

    @abstractmethod
    def get_all_users_records(self) -> Dict[str, Dict[str, BaseRecordPlugin]]:
        pass

    @abstractmethod
    def set(self, username: str, dataset_name: str, record: BaseRecordPlugin) -> None:
        pass

    @abstractmethod
    def remove_user(self, username: str) -> None:
        pass

    @abstractmethod
    def remove_user_dataset(self, username: str, dataset_name: str) -> None:
        pass
