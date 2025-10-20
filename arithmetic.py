from typing import Sequence
from .utils import pack_u32, unpack_u32

MASK64 = (1 << 64) - 1
TOP_BYTE_SHIFT = 56
SCALE_LIMIT = 1 << 48

class Fenwick:
    def __init__(self, freqs):
        self.n = len(freqs)
        self.tree = list(freqs)
        for i in range(self.n):
            j = i | (i + 1)
            if j < self.n:
                self.tree[j] += self.tree[i]

    def add(self, idx, delta):
        while idx < self.n:
            self.tree[idx] += delta
            idx |= idx + 1

    def sum(self, idx):
        s = 0
        while idx >= 0:
            s += self.tree[idx]
            idx = (idx & (idx + 1)) - 1
        return s

    def prefix_find(self, value):
        idx = -1
        bit = 1 << (self.n.bit_length() - 1)
        while bit:
            nxt = idx + bit
            if nxt < self.n and self.tree[nxt] <= value:
                value -= self.tree[nxt]
                idx = nxt
            bit >>= 1
        return idx + 1

    def rebuild(self, freqs):
        self.__init__(freqs)

def _encode_range(l, h, total, cl, ch):
    r = h - l + 1
    nl = l + (r * cl) // total
    nh = l + (r * ch) // total - 1
    return nl & MASK64, nh & MASK64

def arith_compress(symbols: Sequence[int]) -> bytes:
    if not symbols:
        return pack_u32(0) + b"\x00\x00"

    a = max(symbols) + 1
    out = bytearray(pack_u32(len(symbols)))
    out.extend([(a >> 8) & 0xFF, a & 0xFF])

    freqs = [1] * a
    bit = Fenwick(freqs)
    total = a
    l, h = 0, MASK64
    out_bytes = []

    append_byte = out_bytes.append
    for sym in symbols:
        cl = bit.sum(sym - 1) if sym else 0
        ch = cl + freqs[sym]
        l, h = _encode_range(l, h, total, cl, ch)
        while (l ^ h) >> TOP_BYTE_SHIFT == 0:
            append_byte(l >> TOP_BYTE_SHIFT)
            l = (l << 8) & MASK64
            h = ((h << 8) | 0xFF) & MASK64
        freqs[sym] += 1
        bit.add(sym, 1)
        total += 1
        if total > SCALE_LIMIT:
            total = 0
            for i in range(a):
                freqs[i] = (freqs[i] + 1) >> 1 or 1
                total += freqs[i]
            bit.rebuild(freqs)

    for _ in range(8):
        append_byte(l >> TOP_BYTE_SHIFT)
        l = (l << 8) & MASK64

    out.extend(out_bytes)
    return bytes(out)

def arith_decompress(data: bytes) -> list[int]:
    if not data:
        return []

    ts = unpack_u32(data[:4])
    if ts == 0:
        return []

    a = (data[4] << 8) | data[5]
    idx = 6
    freqs = [1] * a
    bit = Fenwick(freqs)
    total = a

    code = 0
    for _ in range(8):
        code = ((code << 8) | data[idx]) & MASK64
        idx += 1

    l, h = 0, MASK64
    out = [0] * ts

    for i in range(ts):
        r = h - l + 1
        scaled = ((code - l + 1) * total - 1) // r
        sym = bit.prefix_find(scaled)
        cl = bit.sum(sym - 1) if sym else 0
        ch = cl + freqs[sym]
        l, h = _encode_range(l, h, total, cl, ch)
        while (l ^ h) >> TOP_BYTE_SHIFT == 0:
            l = (l << 8) & MASK64
            h = ((h << 8) | 0xFF) & MASK64
            if idx < len(data):
                code = ((code << 8) | data[idx]) & MASK64
                idx += 1
        out[i] = sym
        freqs[sym] += 1
        bit.add(sym, 1)
        total += 1
        if total > SCALE_LIMIT:
            total = 0
            for j in range(a):
                freqs[j] = (freqs[j] + 1) >> 1 or 1
                total += freqs[j]
            bit.rebuild(freqs)

    return out
