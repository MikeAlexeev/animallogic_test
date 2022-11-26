from pathlib import Path

import pytest

from user_manager.api.base_plugins.base_output_plugin import BaseOutputPlugin
from user_manager.api.system_configuration import SystemConfiguration


def test_system_configuration_default():
    system_configuration = SystemConfiguration()

    assert system_configuration.get_output_cls().NAME == "simple"
    assert system_configuration.get_record_cls().NAME == "user"
    assert system_configuration.get_storage_cls().NAME == "json"


def test_system_configuration_extra_plugins(plugins_dir: Path):
    system_configuration = SystemConfiguration(plugin_folders=[plugins_dir])

    assert system_configuration.get_output_cls().NAME == "simple"
    assert system_configuration.get_record_cls().NAME == "user"
    assert system_configuration.get_storage_cls().NAME == "json"

    system_configuration.set_output_implementation_name("module2-class1")

    assert system_configuration.get_output_cls().NAME == "module2-class1"
    assert system_configuration.get_record_cls().NAME == "user"
    assert system_configuration.get_storage_cls().NAME == "json"

    with pytest.raises(RuntimeError) as err:
        system_configuration._get_default_implementation_cls(BaseOutputPlugin)

    assert "must be called" in str(err.value)
