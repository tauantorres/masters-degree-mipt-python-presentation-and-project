import json
from dataclasses import dataclass, asdict


@dataclass
class UserDataclass:
    id: int
    name: str
    email: str
    age: int
    is_active: bool


def instantiate_dataclass(user_data: dict) -> UserDataclass:
    return UserDataclass(**user_data)

def encode_dataclass(user_dataclass_instance: UserDataclass) -> bytes:
    return json.dumps(asdict(user_dataclass_instance), ensure_ascii=False).encode()

def decode_dataclass(user_dataclass_bytes: bytes) -> UserDataclass:
    return instantiate_dataclass(json.loads(user_dataclass_bytes.decode()))
