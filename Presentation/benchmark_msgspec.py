from msgspec import Struct, json


class UserMsgspec(Struct, kw_only=True, omit_defaults=True):
    id: int
    name: str
    email: str
    age: int
    is_active: bool


def instantiate_msgspec(user_data: dict) -> UserMsgspec:
    return UserMsgspec(**user_data)

def encode_msgspec(user_msgspec_instance: UserMsgspec) -> bytes:
    return json.encode(user_msgspec_instance)

def decode_msgspec(user_msgspec_bytes: bytes) -> UserMsgspec:
    return json.decode(user_msgspec_bytes, type=UserMsgspec)

