import pydivsufsort
import numpy as np

def suffix_array(s):
    if not s:
        return np.array([], dtype=np.int64)

    if isinstance(s, str):
        s_bytes = s.encode('utf-8')
        return pydivsufsort.divsufsort(s_bytes)

    arr = np.asarray(s, dtype=np.int64)
    if arr.size == 0:
        return np.array([], dtype=np.int64)

    _, inv = np.unique(arr, return_inverse=True)
    mapped = inv.astype(np.uint8, copy=False)
    return pydivsufsort.divsufsort(mapped.tobytes())
