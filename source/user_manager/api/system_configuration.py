import logging
from pathlib import Path
from typing import List, Optional, Type, cast

from ..plugin_system.base_plugin import BasePlugin
from ..plugin_system.plugin_loader import PluginLoader
from ..plugin_system.plugin_registry import PluginRegistry
from .base_plugins.base_output_plugin import BaseOutputPlugin
from .base_plugins.base_record_plugin import BaseRecordPlugin
from .base_plugins.base_storage_plugin import BaseStoragePlugin


class SystemConfiguration:
    def __init__(self, plugin_folders: Optional[List[Path]] = None):
        self._plugin_registry = PluginRegistry()

        self.load_plugins(self.default_plugins_path)
        self.set_output_implementation_name(
            self._get_default_implementation_cls(BaseOutputPlugin).NAME
        )
        self.set_storage_implementation_name(
            self._get_default_implementation_cls(BaseStoragePlugin).NAME
        )
        self.set_record_implementation_name(
            self._get_default_implementation_cls(BaseRecordPlugin).NAME
        )

        for path in plugin_folders or []:
            self.load_plugins(path)

    def load_plugins(self, plugins_folder: Path) -> None:
        loader = PluginLoader()
        for plugin in loader.load_plugins(plugins_folder):
            self._plugin_registry.register_plugin(plugin)

    @property
    def default_plugins_path(self) -> Path:
        return Path(__file__).parent.parent / "default_plugins"

    def set_output_implementation_name(self, implementation_name: str) -> None:
        self._logger.info(f"set output implementation: '{implementation_name}'")
        self._output_implementation_name = implementation_name

    def set_storage_implementation_name(self, implementation_name: str) -> None:
        self._logger.info(f"set storage implementation: '{implementation_name}'")
        self._storage_implementation_name = implementation_name

    def set_record_implementation_name(self, implementation_name: str) -> None:
        self._logger.info(f"set record implementation: '{implementation_name}'")
        self._record_implementation_name = implementation_name

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

    def _get_default_implementation_cls(
        self, plugin_type: Type[BasePlugin]
    ) -> Type[BasePlugin]:
        plugins = self._plugin_registry.get_registered_subclasses(plugin_type)
        if len(plugins) != 1:
            raise RuntimeError(
                "must be called after default plugins loading and before other plugis loaded"
            )

        return plugins[0]

    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(__name__)
