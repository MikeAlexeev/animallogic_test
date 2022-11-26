from typing import Type, cast

from .base_output_plugin import BaseOutputPlugin
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

    def get_output_implementation(self) -> Type[BaseOutputPlugin]:
        plug = self._plugin_registry.get_implementation_class(
            BaseOutputPlugin, self._output_implementation_name
        )
        return cast(Type[BaseOutputPlugin], plug)

    def get_storage_implementation(self) -> Type[BaseStoragePlugin]:
        plug = self._plugin_registry.get_implementation_class(
            BaseStoragePlugin, self._storage_implementation_name
        )
        return cast(Type[BaseStoragePlugin], plug)

    def get_record_implementation(self) -> Type[BaseRecordPlugin]:
        plug = self._plugin_registry.get_implementation_class(
            BaseRecordPlugin, self._record_implementation_name
        )
        return cast(Type[BaseRecordPlugin], plug)
