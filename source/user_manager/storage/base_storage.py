from abc import abstractmethod

from .base_user_record import BaseUserRecord


class BaseStorage:
    @abstractmethod
    def get(self, username: str) -> BaseUserRecord:
        pass

    @abstractmethod
    def set(self, username: str, record: BaseUserRecord) -> None:
        pass
