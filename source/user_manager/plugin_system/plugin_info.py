from dataclasses import dataclass
from pathlib import Path

from .plugin_type import PluginType


@dataclass(frozen=True)
class PluginInfo:
    class_: type
    type_: PluginType
    name: str
    module_path: Path
