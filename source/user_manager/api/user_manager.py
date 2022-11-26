from ..plugin_system.system_configuration import SystemConfiguration


class UserManager:
    def __init__(self, system_configuration: SystemConfiguration):
        self._record_cls = system_configuration.get_record_cls()
        self._output = system_configuration.get_output_cls()()
        self._storage = system_configuration.get_storage_cls()(record_type=self._record_cls)

    def output_user(self, username: str) -> None:
        record = self._storage.get(username)

        if not record:
            self._output.output_not_found_error(username)
            # TODO exception ?
            return

        self._output.output_user(username, record)

    def save_user(self, username: str, values: dict) -> None:
        data = {key: val for key, val in values.items() if val is not None}
        existing_record = self._storage.get(username)
        if existing_record:
            data = {**existing_record.to_dict(), **data}

        record = self._record_cls.from_dict(data)
        self._storage.set(username, record)
