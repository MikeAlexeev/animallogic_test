from dataclasses import dataclass
from typing import Optional

from user_manager.default_plugins.user_record_plugin import UserRecordPlugin


@dataclass
class ExtendedUserRecordPlugin(UserRecordPlugin):
    NAME: str = "extended-user"

    email: Optional[str] = None
