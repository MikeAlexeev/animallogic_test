from pathlib import Path

from user_manager.plugin_system.plugin_loader import PluginLoader


def test_plugin_loader(plugins_dir: Path) -> None:
    loader = PluginLoader()
    plugins = loader.load_plugins(plugins_dir)
    expected_names = ["module1-class1", "module1-class2", "module2-class1"]
    actual_names = [plug.NAME for plug in plugins]

    assert sorted(actual_names) == sorted(expected_names)
