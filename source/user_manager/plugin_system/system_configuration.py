from typing import List, Type, cast

from .base_output_plugin import BaseOutputPlugin
from .base_plugin import BasePlugin
from .base_record_plugin import BaseRecordPlugin
from .base_storage_plugin import BaseStoragePlugin
from .plugin_registry import PluginRegistry


class SystemConfiguration:
    def __init__(
        self,
        plugin_registry: PluginRegistry,
        output_implementation_name: str,
        storage_implementation_name: str,
        record_implementation_name: str,
    ):
        self._plugin_registry = plugin_registry
        self._output_implementation_name = output_implementation_name
        self._storage_implementation_name = storage_implementation_name
        self._record_implementation_name = record_implementation_name

    @property
    def plugins(self) -> List[Type[BasePlugin]]:
        return self._plugin_registry.plugins

    def get_output_cls(self) -> Type[BaseOutputPlugin]:
        plug = self._plugin_registry.get_implementation_class(
            BaseOutputPlugin, self._output_implementation_name
        )
        return cast(Type[BaseOutputPlugin], plug)

    def get_storage_cls(self) -> Type[BaseStoragePlugin]:
        plug = self._plugin_registry.get_implementation_class(
            BaseStoragePlugin, self._storage_implementation_name
        )
        return cast(Type[BaseStoragePlugin], plug)

    def get_record_cls(self) -> Type[BaseRecordPlugin]:
        plug = self._plugin_registry.get_implementation_class(
            BaseRecordPlugin, self._record_implementation_name
        )
        return cast(Type[BaseRecordPlugin], plug)
