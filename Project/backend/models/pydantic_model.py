from pydantic import BaseModel


class UserPydantic(BaseModel):
    id: int
    name: str
    email: str
    age: int
    is_active: bool


def instantiate_pydantic(user_data: dict) -> UserPydantic:
    return UserPydantic(**user_data)

def encode_pydantic(user_pydantic_instance: UserPydantic) -> bytes:
    return user_pydantic_instance.model_dump_json(exclude_defaults=True).encode()

def decode_pydantic(user_pydantic_bytes: bytes) -> UserPydantic:
    return UserPydantic.model_validate_json(user_pydantic_bytes.decode())

def measure_pydantic_size(user_pydantic_instance: UserPydantic) -> int:
    return len(encode_pydantic(user_pydantic_instance))
