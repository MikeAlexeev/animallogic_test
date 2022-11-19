import argparse
import logging
from pathlib import Path
from typing import cast, Type

from .plugin_system.plugin_loader import PluginLoader
from .plugin_system.plugin_registry import PluginRegistry
from .plugin_system.base_output_plugin import BaseOutputPlugin


def output_user(args: argparse.Namespace, plugin_registry: PluginRegistry) -> None:
    output_impl = plugin_registry.get_implementation_class(BaseOutputPlugin, args.output)
    output_impl = cast(Type[BaseOutputPlugin], output_impl)
    output_impl().run_action({'x': 10})


def list_plugins(args: argparse.Namespace, plugin_registry: PluginRegistry) -> None:
    for plug in plugin_registry.plugins:
        print(plug)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin-dir", type=Path)

    subparsers = parser.add_subparsers(dest="command")
    output_parser = subparsers.add_parser("get")
    output_parser.set_defaults(func=output_user)
    output_parser.add_argument('--output')

    list_parser = subparsers.add_parser("list-plugins")
    list_parser.set_defaults(func=list_plugins)

    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    args = parse_args()

    loader = PluginLoader()
    plugins = loader.load_plugins(loader.default_plugins_folder)
    if args.plugin_dir:
        plugins.extend(loader.load_plugins(args.plugin_dir))

    plugin_registry = PluginRegistry()
    for plugin in plugins:
        plugin_registry.register_plugin(plugin)

    args.func(args, plugin_registry)
