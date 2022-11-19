from dataclasses import dataclass

from user_manager.plugin_system.base_record_plugin import BaseRecordPlugin


@dataclass
class UserRecordPlugin(BaseRecordPlugin):
    address: str
    phone_number: str  # TODO can be validated, with pydantic for example

    NAME: str = "user-record"
