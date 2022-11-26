from dataclasses import asdict, dataclass, fields
from typing import List

from ...plugin_system.base_plugin import BasePlugin


@dataclass
class BaseRecordPlugin(BasePlugin):
    @classmethod
    def from_dict(cls, data: dict) -> "BaseRecordPlugin":
        values = {
            key: val for key, val in data.items() if key in cls.get_option_names()
        }
        return cls(**values)

    def to_dict(self) -> dict:
        data = asdict(self)
        data.pop("NAME", None)
        return data

    @classmethod
    def get_option_names(cls) -> List[str]:
        return [field.name for field in fields(cls)]
