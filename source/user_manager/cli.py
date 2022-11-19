import argparse
import logging
from pathlib import Path

from .action_chains.base_action_chain import BaseActionChain
from .action_type import ActionType
from .plugin_system.plugin_loader import PluginLoader


def output_users(args: argparse.Namespace, chain: BaseActionChain) -> None:
    chain.run_action(ActionType.OUTPUT, args.output, {'x': 10})


def list_plugins(args: argparse.Namespace, chain: BaseActionChain) -> None:
    for plug in chain.plugins:
        print(plug)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin-dir", type=Path)

    subparsers = parser.add_subparsers(dest="command")
    output_parser = subparsers.add_parser("get")
    output_parser.set_defaults(func=output_users)
    output_parser.add_argument('--output')

    list_parser = subparsers.add_parser("list-plugins")
    list_parser.set_defaults(func=list_plugins)

    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    args = parse_args()

    loader = PluginLoader()
    plugins = loader.load_plugins(args.plugin_dir)
    chain = BaseActionChain()
    for plugin in plugins:
        chain.register_plugin(plugin)

    args.func(args, chain)
