from typing import List, Type

from .base_plugin import BasePlugin


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: List[Type[BasePlugin]] = []

    def register_plugin(self, plugin: Type[BasePlugin]) -> None:
        self._plugins.append(plugin)

    def get_implementation_class(self, base_class: Type[BasePlugin], implementation_name: str) -> Type[BasePlugin]:
        if not implementation_name:
            raise RuntimeError(f'implementation not found for {base_class}')

        for plug in self._plugins:
            if issubclass(plug, base_class) and plug.NAME == implementation_name:
                return plug

        raise RuntimeError(f'implementation not found for {base_class}')

    @property
    def plugins(self) -> List[Type[BasePlugin]]:
        return self._plugins
