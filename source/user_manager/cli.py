import argparse
import logging
from pathlib import Path
from typing import cast, Type

from .plugin_system.plugin_loader import PluginLoader
from .plugin_system.plugin_registry import PluginRegistry
from .plugin_system.base_output_plugin import BaseOutputPlugin
from .plugin_system.base_storage_plugin import BaseStoragePlugin
from .plugin_system.base_record_plugin import BaseRecordPlugin


def output_user(args: argparse.Namespace, plugin_registry: PluginRegistry) -> None:
    output_impl = plugin_registry.get_implementation_class(
        BaseOutputPlugin, args.output
    )
    storage_impl = plugin_registry.get_implementation_class(
        BaseStoragePlugin, args.storage
    )
    storage_record_impl = plugin_registry.get_implementation_class(
        BaseRecordPlugin, args.record_type
    )
    output_impl = cast(Type[BaseOutputPlugin], output_impl)
    storage_impl = cast(Type[BaseStoragePlugin], storage_impl)
    storage_record_impl = cast(Type[BaseRecordPlugin], storage_record_impl)
    record = storage_impl(record_type=storage_record_impl).get(args.username)
    output_impl().do_output(args.username, record)


def set_user(args: argparse.Namespace, plugin_registry: PluginRegistry) -> None:
    storage_impl = plugin_registry.get_implementation_class(
        BaseStoragePlugin, args.storage
    )
    storage_record_impl = plugin_registry.get_implementation_class(
        BaseRecordPlugin, args.record_type
    )
    storage_impl = cast(Type[BaseStoragePlugin], storage_impl)
    storage_record_impl = cast(Type[BaseRecordPlugin], storage_record_impl)
    storage = storage_impl(record_type=storage_record_impl)
    record = storage_record_impl.from_dict(vars(args))
    storage.set(args.username, record)


def list_plugins(args: argparse.Namespace, plugin_registry: PluginRegistry) -> None:
    for plug in plugin_registry.plugins:
        print(plug)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin-dir", type=Path)

    subparsers = parser.add_subparsers(dest="command")
    output_parser = subparsers.add_parser("get")
    output_parser.set_defaults(func=output_user)
    list_parser = subparsers.add_parser("list-plugins")
    list_parser.set_defaults(func=list_plugins)
    set_parser = subparsers.add_parser("set")
    set_parser.set_defaults(func=set_user)

    output_parser.add_argument("--output", default="simple")
    output_parser.add_argument("--storage", default="json")
    output_parser.add_argument("--record-type", default="user-record")
    output_parser.add_argument("username")

    set_parser.add_argument("--output", default="simple")
    set_parser.add_argument("--storage", default="json")
    set_parser.add_argument("--record-type", default="user-record")
    set_parser.add_argument("--phone-number", required=True)  # TODO partial update
    set_parser.add_argument("--address", required=True)
    set_parser.add_argument("username")

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
