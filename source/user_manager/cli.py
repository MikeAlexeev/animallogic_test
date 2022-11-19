import argparse
import logging
from pathlib import Path

from .plugin_system.plugin_loader import PluginLoader


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin-dirs", nargs="*", type=Path)
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    args = parse_args()

    loader = PluginLoader()
    plugs = []
    for plugin_dir in args.plugin_dirs:
        plugs.extend(loader.load_plugins(plugin_dir))

    print(plugs)
