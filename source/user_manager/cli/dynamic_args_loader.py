from typing import List

from ..api.system_configuration import SystemConfiguration


class DynamicArgsLoader:
    def __init__(self, system_configuration: SystemConfiguration):
        self._system_configuration = system_configuration

    def get_record_args(self) -> List[str]:
        field_names = self._system_configuration.get_record_cls().get_option_names()
        return [self._make_arg(field_name) for field_name in field_names]

    def get_storage_args(self) -> List[str]:
        field_names = self._system_configuration.get_storage_cls().get_option_names()
        return [self._make_arg(field_name) for field_name in field_names]

    @staticmethod
    def _make_arg(field_name: str) -> str:
        return f"--{field_name.replace('_', '-')}"
