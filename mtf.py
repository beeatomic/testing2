def mtf_compress(data: bytes) -> bytes:
    order = bytearray(range(256))
    pos = list(range(256))
    out = bytearray(len(data))
    o = 0
    for c in data:
        idx = pos[c]
        out[o] = idx
        o += 1
        if idx:
            order[1:idx+1] = order[0:idx]
            order[0] = c
            for j in range(idx+1):
                pos[order[j]] = j
    return bytes(out)

def mtf_decompress(data: bytes) -> bytes:
    order = bytearray(range(256))
    out = bytearray(len(data))
    o = 0
    for idx in data:
        c = order[idx]
        out[o] = c
        o += 1
        if idx:
            order[1:idx+1] = order[0:idx]
            order[0] = c
    return bytes(out)
