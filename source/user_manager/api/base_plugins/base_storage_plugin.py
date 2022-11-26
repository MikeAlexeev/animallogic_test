from abc import abstractmethod
from typing import Dict, Optional, Type

from ...plugin_system.base_plugin import BasePlugin
from .base_record_plugin import BaseRecordPlugin


class BaseStoragePlugin(BasePlugin):
    def __init__(self, record_type: Type[BaseRecordPlugin]):
        self._record_type = record_type

    @abstractmethod
    def get_all_records_for_user(
        self, username: str
    ) -> Optional[Dict[str, BaseRecordPlugin]]:
        pass

    @abstractmethod
    def get_user_record(
        self, username: str, dataset_name: str
    ) -> Optional[BaseRecordPlugin]:
        pass

    @abstractmethod
    def get_all_users_records(self) -> Dict[str, Dict[str, BaseRecordPlugin]]:
        pass

    @abstractmethod
    def search_users(
        self, filters: Dict[str, str]
    ) -> Dict[str, Dict[str, BaseRecordPlugin]]:
        pass

    @abstractmethod
    def set_user_record(
        self, username: str, dataset_name: str, record: BaseRecordPlugin
    ) -> None:
        pass

    @abstractmethod
    def remove_user(self, username: str) -> None:
        pass

    @abstractmethod
    def remove_user_record(self, username: str, dataset_name: str) -> None:
        pass
