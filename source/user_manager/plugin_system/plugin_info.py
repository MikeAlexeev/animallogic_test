from dataclasses import dataclass
from pathlib import Path

from ..action_type import ActionType


@dataclass(frozen=True)
class PluginInfo:
    class_: type
    type_: ActionType
    name: str
    module_path: Path
