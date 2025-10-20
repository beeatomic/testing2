import numpy as np
from struct import pack, unpack
from typing import Sequence

def pack_u32(v: int) -> bytes:
    return pack(">I", v)

def unpack_u32(b: bytes) -> int:
    return unpack(">I", b)[0]

def to_int_keys_best(l: Sequence[int]) -> np.ndarray:
    arr = np.asarray(l)
    _, inv = np.unique(arr, return_inverse=True)
    return inv
