import argparse
import logging
from pathlib import Path

from .api.user_manager import UserManager
from .plugin_system.plugin_loader import PluginLoader
from .plugin_system.plugin_registry import PluginRegistry
from .plugin_system.system_configuration import SystemConfiguration


def output_user(
    args: argparse.Namespace, system_configuration: SystemConfiguration
) -> None:
    UserManager(system_configuration=system_configuration).output_user(args.username)


def save_user(
    args: argparse.Namespace, system_configuration: SystemConfiguration
) -> None:
    UserManager(system_configuration=system_configuration).save_user(
        args.username, vars(args)
    )


def remove_user(
    args: argparse.Namespace, system_configuration: SystemConfiguration
) -> None:
    UserManager(system_configuration=system_configuration).remove_user(args.username)


def list_plugins(
    args: argparse.Namespace, system_configuration: SystemConfiguration
) -> None:
    for plug in system_configuration.plugins:
        print(plug)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin-dir", type=Path)
    parser.add_argument("--log-level", default="ERROR")

    subparsers = parser.add_subparsers(dest="command")
    save_parser = subparsers.add_parser("set")
    output_parser = subparsers.add_parser("get")
    remove_parser = subparsers.add_parser("remove")
    list_parser = subparsers.add_parser("list-plugins")

    save_parser.set_defaults(func=save_user)
    output_parser.set_defaults(func=output_user)
    remove_parser.set_defaults(func=remove_user)
    list_parser.set_defaults(func=list_plugins)

    for sub_parser in [save_parser, output_parser, remove_parser, list_parser]:
        # args not actualy used in all sub parsers. Added for unification and simplicity
        sub_parser.add_argument("--output-type", default="simple")
        sub_parser.add_argument("--storage-type", default="json")
        sub_parser.add_argument("--record-type", default="user-record")

    for sub_parser in [save_parser, output_parser, remove_parser]:
        sub_parser.add_argument("username")

    save_parser.add_argument("--phone-number")
    save_parser.add_argument("--address")

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
