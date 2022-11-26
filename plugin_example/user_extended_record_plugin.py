from dataclasses import dataclass
from typing import Optional

from user_manager.default_plugins.user_record_plugin import UserRecordPlugin


@dataclass
class ExtendedUserRecordPlugin(UserRecordPlugin):
    NAME: str = "user-extended"

    email: Optional[str] = None
