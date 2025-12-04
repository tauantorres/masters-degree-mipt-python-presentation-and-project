
from .benchmark_dataclass import *
from .benchmark_pydantic import *
from .benchmark_msgspec import *

__all__ = [
    "UserDataclass",
    "instantiate_dataclass",
    "encode_dataclass",
    "decode_dataclass",
    "UserPydantic",
    "instantiate_pydantic",
    "encode_pydantic",
    "decode_pydantic",
    "UserMsgspec",
    "instantiate_msgspec",
    "encode_msgspec",
    "decode_msgspec",
]