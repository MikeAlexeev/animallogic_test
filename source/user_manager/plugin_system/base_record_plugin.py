from dataclasses import asdict, dataclass, fields

from .base_plugin import BasePlugin


@dataclass
class BaseRecordPlugin(BasePlugin):
    @classmethod
    def from_dict(cls, data: dict) -> "BaseRecordPlugin":
        field_names = [field.name for field in fields(cls)]
        values = {key: val for key, val in data.items() if key in field_names}
        return cls(**values)

    def to_dict(self) -> dict:
        data = asdict(self)
        data.pop("NAME", None)
        return data
