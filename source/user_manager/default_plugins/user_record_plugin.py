from dataclasses import dataclass
from typing import Optional

from user_manager.plugin_system.base_record_plugin import BaseRecordPlugin


@dataclass
class UserRecordPlugin(BaseRecordPlugin):
    NAME: str = "user-record"

    address: Optional[str] = None

    # TODO can be validated, with pydantic for example
    phone_number: Optional[str] = None
