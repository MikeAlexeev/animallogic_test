from dataclasses import dataclass

import mock

from user_manager.api.base_plugins.base_record_plugin import BaseRecordPlugin
from user_manager.api.system_configuration import SystemConfiguration
from user_manager.cli.dynamic_args_loader import DynamicArgsLoader


@dataclass
class _TestRecordPlugin(BaseRecordPlugin):
    email: str
    age: int


def test_dynamic_args_loader():
    system_configuration = SystemConfiguration()
    dyn_args_loader = DynamicArgsLoader(system_configuration)
    with mock.patch.object(
        system_configuration,
        "get_record_cls",
        return_value=_TestRecordPlugin,
    ):
        args = dyn_args_loader.get_record_args()

    assert sorted(args) == sorted(['--email', '--age'])
