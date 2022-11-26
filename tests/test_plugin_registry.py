import pytest

from user_manager.plugin_system.plugin_registry import PluginRegistry
from user_manager.plugin_system.base_plugin import BasePlugin


class PluginA(BasePlugin):
    NAME = 'plugin_a'


class PluginB(BasePlugin):
    NAME = 'plugin_b'


class PluginOtherType(BasePlugin):
    pass


class PluginOtherTypeA(PluginOtherType):
    NAME = 'plugin_a'


def test_plugin_registry_get_implementation_class():
    plugin_registry = PluginRegistry()
    plugin_registry.register_plugin(PluginA)
    plugin_registry.register_plugin(PluginB)

    assert plugin_registry.get_implementation_class(BasePlugin, 'plugin_a') == PluginA
    assert plugin_registry.get_implementation_class(BasePlugin, 'plugin_b') == PluginB

    with pytest.raises(RuntimeError) as e:
        plugin_registry.get_implementation_class(PluginOtherType, 'plugin_a')

    assert 'implementation not found' in str(e.value)

    plugin_registry.register_plugin(PluginOtherTypeA)
    plugin_registry.get_implementation_class(PluginOtherType, 'plugin_a') == PluginOtherTypeA
