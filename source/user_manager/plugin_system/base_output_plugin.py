from abc import abstractmethod
from typing import Dict, Optional

from .base_plugin import BasePlugin
from .base_record_plugin import BaseRecordPlugin


class BaseOutputPlugin(BasePlugin):
    @abstractmethod
    def output_user(
        self, username: str, user_records: Dict[str, BaseRecordPlugin]
    ) -> None:
        pass

    @abstractmethod
    def output_users(
        self, users_records: Dict[str, Dict[str, BaseRecordPlugin]]
    ) -> None:
        pass

    def output_user_record(
        self, username: str, dataset_name: str, user_record: BaseRecordPlugin
    ) -> None:
        pass

    @abstractmethod
    def output_not_found_error(
        self, username: str, dataset_name: Optional[str] = None
    ) -> None:
        pass
