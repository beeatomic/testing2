from typing import Sequence
from .utils import pack_u32, unpack_u32
from .suffix_array import suffix_array

def bwt_compress(data: bytes) -> bytes:
    if not data:
        return b''
    s = list(data) + [-1]
    sa = suffix_array(s)
    bwt = [s[i - 1] if i > 0 else -1 for i in sa]
    p = bwt.index(-1)
    return pack_u32(p) + bytes(x & 0xFF for x in bwt if x != -1)

def bwt_decompress(compressed: bytes) -> bytes:
    if not compressed:
        return b''
    p = unpack_u32(compressed[:4])
    bwt_list = list(compressed[4:])
    n = len(bwt_list)
    table = bwt_list[:p] + [-1] + bwt_list[p:]
    counts = [0] * 257
    for c in table:
        counts[0 if c == -1 else c + 1] += 1
    cum = [0] * 257
    total = 0
    for i in range(257):
        cum[i] = total
        total += counts[i]
    occ = [0] * 257
    lf = [0] * (n + 1)
    for i in range(n + 1):
        idx = 0 if table[i] == -1 else table[i] + 1
        lf[i] = cum[idx] + occ[idx]
        occ[idx] += 1
    out = bytearray(n)
    row = lf[p]
    for pos in range(n - 1, -1, -1):
        out[pos] = table[row]
        row = lf[row]
    return bytes(out)
