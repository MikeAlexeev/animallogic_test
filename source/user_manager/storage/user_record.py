from .base_user_record import BaseUserRecord


class UserRecord(BaseUserRecord):
    address: str
    phone_number: str   # TODO can be validated, with pydantic for example
