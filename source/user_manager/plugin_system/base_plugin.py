from typing import List


class BasePlugin:
    NAME: str = "base_plugin"

    @classmethod
    def get_option_names(cls) -> List[str]:
        return []
