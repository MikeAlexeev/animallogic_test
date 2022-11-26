from typing import List

from ..api.system_configuration import SystemConfiguration


class DynamicArgsLoader:
    def __init__(self, system_configuration: SystemConfiguration):
        self._system_configuration = system_configuration

    def get_record_args(self) -> List[str]:
        field_names = self._system_configuration.get_record_cls().get_field_names()
        return [f"--{field_name}" for field_name in field_names]
