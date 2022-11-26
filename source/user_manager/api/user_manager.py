import logging
from typing import Dict, Optional, Type

from .base_plugins.base_output_plugin import BaseOutputPlugin
from .base_plugins.base_record_plugin import BaseRecordPlugin
from .base_plugins.base_storage_plugin import BaseStoragePlugin
from .system_configuration import SystemConfiguration


class UserManager:
    def __init__(self, system_configuration: SystemConfiguration):
        self._system_configuration = system_configuration

    def save_user(
        self, username: str, dataset_name: str, values: Dict[str, str]
    ) -> None:
        existing_user_record = self._storage.get_user_record(username, dataset_name)
        if existing_user_record:
            self._logger.info(
                f"updating existing record for '{username}' in dataset '{dataset_name}', values: {values}"
            )
            merged_data = {**existing_user_record.to_dict(), **values}
        else:
            self._logger.info(
                f"creating new record for '{username}' in dataset '{dataset_name}', values: {values}"
            )
            merged_data = values

        record = self._record_cls.from_dict(merged_data)
        self._storage.set_user_record(username, dataset_name, record)

    def output_user(self, username: str, dataset_name: Optional[str] = None) -> None:
        self._logger.info(
            f"printing '{username}', dataset: '{dataset_name or 'not set'}'"
        )
        if dataset_name is not None:
            record = self._storage.get_user_record(username, dataset_name)
            if not record:
                self._output.output_not_found_error(username)
                return

            self._output.output_user_record(username, dataset_name, record)
            return

        user_records = self._storage.get_all_records_for_user(username)

        if not user_records:
            self._output.output_not_found_error(username, dataset_name)
            return

        self._output.output_user(username, user_records)

    def output_users(self) -> None:
        self._logger.info("printing all users")
        users_records = self._storage.get_all_users_records()
        self._output.output_users(users_records)

    def search_users(self, **filters: str) -> None:
        self._logger.info(f"searching users with filters: {filters}")
        self._output.output_users(self._storage.search_users(filters))

    def remove_user(self, username: str, dataset_name: Optional[str] = None) -> None:
        if dataset_name:
            self._logger.info(f"removing '{username}' from dataset: '{dataset_name}'")
            self._storage.remove_user_record(username, dataset_name)
        else:
            self._logger.info(f"removing '{username}' from all datasets")
            self._storage.remove_user(username)

    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(__name__)

    @property
    def _record_cls(self) -> Type[BaseRecordPlugin]:
        return self._system_configuration.get_record_cls()

    @property
    def _output(self) -> BaseOutputPlugin:
        # instantiate it for simplicity
        return self._system_configuration.get_output_cls()()

    @property
    def _storage(self) -> BaseStoragePlugin:
        # instantiate it for simplicity
        return self._system_configuration.get_storage_cls()(
            record_type=self._record_cls
        )
