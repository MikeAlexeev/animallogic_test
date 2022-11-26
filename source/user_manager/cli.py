import argparse
import logging
from pathlib import Path

from .api.system_configuration import SystemConfiguration
from .api.user_manager import UserManager
from .plugin_system.plugin_loader import PluginLoader
from .plugin_system.plugin_registry import PluginRegistry


def remove_none_values(data: dict) -> dict:
    return {key: val for key, val in data.items() if val is not None}


def output_user_info(
    args: argparse.Namespace, system_configuration: SystemConfiguration
) -> None:
    UserManager(system_configuration=system_configuration).output_user(
        args.username, args.dataset
    )


def output_all_users_info(
    args: argparse.Namespace, system_configuration: SystemConfiguration
) -> None:
    UserManager(system_configuration=system_configuration).output_users()


def search_users(
    args: argparse.Namespace, system_configuration: SystemConfiguration
) -> None:
    filters = remove_none_values(vars(args))
    UserManager(system_configuration=system_configuration).search_users(filters)


def save_user(
    args: argparse.Namespace, system_configuration: SystemConfiguration
) -> None:
    values = remove_none_values(vars(args))
    UserManager(system_configuration=system_configuration).save_user(
        args.username, args.dataset, values
    )


def remove_user(
    args: argparse.Namespace, system_configuration: SystemConfiguration
) -> None:
    UserManager(system_configuration=system_configuration).remove_user(
        args.username, args.dataset
    )


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
    output_all_parser = subparsers.add_parser("get-all")
    remove_parser = subparsers.add_parser("remove")
    search_parser = subparsers.add_parser("search")
    list_parser = subparsers.add_parser("list-plugins")

    save_parser.set_defaults(func=save_user)
    output_parser.set_defaults(func=output_user_info)
    output_all_parser.set_defaults(func=output_all_users_info)
    remove_parser.set_defaults(func=remove_user)
    search_parser.set_defaults(func=search_users)
    list_parser.set_defaults(func=list_plugins)

    for sub_parser in [
        save_parser,
        output_parser,
        output_all_parser,
        remove_parser,
        search_parser,
        list_parser,
    ]:
        # args not actualy used in all sub parsers. Added for unification and simplicity
        sub_parser.add_argument("--output-type", default="simple")
        sub_parser.add_argument("--storage-type", default="json")
        sub_parser.add_argument("--record-type", default="user-record")

    for sub_parser in [save_parser, output_parser, remove_parser]:
        sub_parser.add_argument("username")

    for sub_parser in [output_parser, remove_parser]:
        sub_parser.add_argument("dataset", nargs="?")

    for sub_parser in [save_parser, search_parser]:
        sub_parser.add_argument("--phone-number")
        sub_parser.add_argument("--address")

    save_parser.add_argument("dataset", nargs="?", default="personal")
    search_parser.add_argument("--username")

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
