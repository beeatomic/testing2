from typing import Sequence

def rle1_compress(data: bytes) -> bytes:
    out = bytearray()
    mv = memoryview(data)
    n = len(mv)
    i = 0
    while i < n:
        c = mv[i]
        limit = min(255, n - i)
        run = 1
        while run < limit and mv[i + run] == c:
            run += 1
        if run > 3 or (c == 0 and run > 2):
            out += bytes((c, 0, run))
        else:
            out += bytes([c] * run)
        i += run
    return bytes(out)

def rle1_decompress(data: bytes) -> bytes:
    out = bytearray()
    mv = memoryview(data)
    i = 0
    n = len(mv)
    while i < n:
        c = mv[i]
        if i + 2 < n and mv[i + 1] == 0:
            out += bytes([c]) * mv[i + 2]
            i += 3
        else:
            out.append(c)
            i += 1
    return bytes(out)

def rle2_compress(data: Sequence[int]) -> list[int]:
    out = []
    n = len(data)
    i = 0
    while i < n:
        v = data[i]
        if v != 0:
            out.append(v + 1)
            i += 1
            continue
        run = 0
        while i < n and data[i] == 0:
            run += 1
            i += 1
        k = run - 1
        while k:
            out.append(k & 1)
            k >>= 1
        if run == 1:
            out.append(0)
    return out

def rle2_decompress(data: Sequence[int]) -> list[int]:
    out = []
    n = len(data)
    i = 0
    while i < n:
        v = data[i]
        if v >= 2:
            out.append(v - 1)
            i += 1
            continue
        k = 0
        s = 0
        while i < n and data[i] <= 1:
            k |= data[i] << s
            s += 1
            i += 1
        out.extend([0] * (k + 1))
    return out
