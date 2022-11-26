from typing import Optional
from dataclasses import dataclass

from user_manager.plugin_system.base_record_plugin import BaseRecordPlugin


@dataclass
class UserRecordPlugin(BaseRecordPlugin):
    address: Optional[str] = None
    phone_number: Optional[str] = None   # TODO can be validated, with pydantic for example

    NAME: str = "user-record"
