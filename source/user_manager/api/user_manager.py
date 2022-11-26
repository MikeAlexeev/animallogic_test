from typing import Dict, Optional

from ..plugin_system.system_configuration import SystemConfiguration


class UserManager:
    def __init__(self, system_configuration: SystemConfiguration):
        self._record_cls = system_configuration.get_record_cls()
        self._output = system_configuration.get_output_cls()()
        self._storage = system_configuration.get_storage_cls()(
            record_type=self._record_cls
        )

    def save_user(self, username: str, dataset_name: str, values: Dict[str, str]) -> None:
        existing_user_record = self._storage.get_user_record(username, dataset_name)
        if existing_user_record:
            merged_data = {**existing_user_record.to_dict(), **values}
        else:
            merged_data = values

        record = self._record_cls.from_dict(merged_data)
        self._storage.set_user_record(username, dataset_name, record)

    def output_user(self, username: str, dataset_name: Optional[str] = None) -> None:
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
        users_records = self._storage.get_all_users_records()
        if not users_records:
            return

        self._output.output_users(users_records)

    def search_users(self, filters: Dict[str, str]) -> None:
        self._output.output_users(self._storage.search_users(filters))

    def remove_user(self, username: str, dataset: Optional[str]) -> None:
        if dataset:
            self._storage.remove_user_record(username, dataset)
        else:
            self._storage.remove_user(username)
