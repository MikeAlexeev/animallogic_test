import importlib.util
import inspect
import logging
from pathlib import Path
from types import ModuleType
from typing import List, Optional

from .base_plugin import BasePlugin
from .plugin_info import PluginInfo
from ..utils import convert_path_to_module_name


class PluginLoader:

    def load_plugins(self, folder: Path) -> List[PluginInfo]:
        plugins: List[PluginInfo] = []
        for path in folder.glob("*.py"):
            self._logger.info(f'loading plugins from "{path}"')
            module = self._load_module(path)
            if not module:
                self._logger.warning("module is not loaded")
                continue

            classes = self._get_module_classes(module)
            self._logger.debug(f"loaded classes: {classes}")

            classes = [cls for cls in classes if issubclass(cls, BasePlugin)]
            self._logger.debug(f"plugin classes: {classes}")

            for cls in classes:
                plugin_info = PluginInfo(
                    class_=cls,
                    type_=cls.TYPE,  # type: ignore
                    name=cls.NAME,  # type: ignore
                    module_path=path,
                )
                plugins.append(plugin_info)

        return plugins

    def _load_module(self, path: Path) -> Optional[ModuleType]:
        module_name = convert_path_to_module_name(path)
        self._logger.debug(f'loading "{path}" as module "{module_name}"')
        spec = importlib.util.spec_from_file_location(module_name, path)
        if not spec:
            return None

        module = importlib.util.module_from_spec(spec)
        if not module or not spec.loader:
            return None

        spec.loader.exec_module(module)
        return module

    def _get_module_classes(self, module: ModuleType) -> List[type]:
        classes = inspect.getmembers(module, inspect.isclass)

        # remove classes imported from other modules
        return [cls for _, cls in classes if cls.__module__ == module.__name__]

    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(__name__)
