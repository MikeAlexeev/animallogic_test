from typing import Any, List

from ..plugin_system.plugin_info import PluginInfo
from ..action_type import ActionType


class BaseActionChain:
    def __init__(self) -> None:
        self._plugins: List[PluginInfo] = []

    def register_plugin(self, plugin: PluginInfo) -> None:
        self._plugins.append(plugin)

    def run_action(self, action_type: ActionType, plug_name: str, arg: Any) -> None:
        for plug in self._plugins:
            if plug.type_ != action_type or plug.name != plug_name:
                continue

            plug_instance = plug.class_()
            plug_instance.run_action(arg)
            return None

        raise RuntimeError(f'implementation not found for {plug_name}')

    @property
    def plugins(self) -> List[PluginInfo]:
        return self._plugins
