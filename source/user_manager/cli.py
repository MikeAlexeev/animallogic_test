import argparse
import logging
import sys
from pathlib import Path

from .plugin_system.plugin_loader import PluginLoader
from .plugin_system.plugin_registry import PluginRegistry
from .plugin_system.system_configuration import SystemConfiguration


def output_user(
    args: argparse.Namespace, system_configuration: SystemConfiguration
) -> None:
    output_cls = system_configuration.get_output_implementation()
    storage_cls = system_configuration.get_storage_implementation()
    record_cls = system_configuration.get_record_implementation()

    record = storage_cls(record_type=record_cls).get(args.username)
    if not record:
        print(f"record for {args.username} doesn`t exist", file=sys.stderr)
        exit(1)
    output_cls().do_output(args.username, record)


def set_user(
    args: argparse.Namespace, system_configuration: SystemConfiguration
) -> None:
    storage_cls = system_configuration.get_storage_implementation()
    record_cls = system_configuration.get_record_implementation()
    existing_record = storage_cls(record_type=record_cls).get(args.username)
    data = {key: val for key, val in vars(args).items() if val is not None}
    if existing_record:
        data = {**existing_record.to_dict(), **data}

    record = record_cls.from_dict(data)
    storage_cls(record_type=record_cls).set(args.username, record)


def list_plugins(args: argparse.Namespace, system_configuration: SystemConfiguration) -> None:
    for plug in system_configuration.plugins:
        print(plug)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin-dir", type=Path)
    parser.add_argument("--log-level", default="ERROR")

    subparsers = parser.add_subparsers(dest="command")
    output_parser = subparsers.add_parser("get")
    output_parser.set_defaults(func=output_user)
    list_parser = subparsers.add_parser("list-plugins")
    list_parser.set_defaults(func=list_plugins)
    set_parser = subparsers.add_parser("set")
    set_parser.set_defaults(func=set_user)

    for sub_parser in [output_parser, set_parser, list_parser]:
        # args not actualy used in list_parser. Added for unification and simplicity
        sub_parser.add_argument("--output-type", default="simple")
        sub_parser.add_argument("--storage-type", default="json")
        sub_parser.add_argument("--record-type", default="user-record")

    set_parser.add_argument("--phone-number")
    set_parser.add_argument("--address")
    set_parser.add_argument("username")
    output_parser.add_argument("username")

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    log_level = logging.getLevelName(args.log_level)
    logging.basicConfig(level=log_level)

    loader = PluginLoader()
    plugins = loader.load_plugins(loader.default_plugins_folder)
    if args.plugin_dir:
        plugins.extend(loader.load_plugins(args.plugin_dir))

    plugin_registry = PluginRegistry()
    for plugin in plugins:
        plugin_registry.register_plugin(plugin)

    system_configuration = SystemConfiguration(
        plugin_registry,
        output_implementation_name=args.output_type,
        storage_implementation_name=args.storage_type,
        record_implementation_name=args.record_type,
    )
    args.func(args, system_configuration)
