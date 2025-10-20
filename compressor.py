from typing import Union
from .required.utils import pack_u32, unpack_u32
from .required.bwt import bwt_compress, bwt_decompress
from .required.mtf import mtf_compress, mtf_decompress
from .required.rle import rle1_compress, rle1_decompress, rle2_compress, rle2_decompress
from .required.arithmetic import arith_compress, arith_decompress

BLOCK_SIZE = 900000

def _compress_single(data: bytes) -> bytes:
    data = rle1_compress(data)
    data = bwt_compress(data)
    data = mtf_compress(data)
    data = rle2_compress(list(data))
    return arith_compress(data)

def _decompress_single(data: bytes) -> bytes:
    data = arith_decompress(data)
    data = rle2_decompress(data)
    data = mtf_decompress(bytes(data))
    data = bwt_decompress(data)
    return rle1_decompress(data)

def compress(data: Union[bytes, str]) -> bytes:
    if isinstance(data, str):
        data = data.encode()
    if not data:
        return b''
    blocks = [data[i:i + BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]
    out = bytearray(pack_u32(len(blocks)))
    for block in blocks:
        comp = _compress_single(block)
        out += pack_u32(len(block)) + pack_u32(len(comp)) + comp
    return bytes(out)

def decompress(data: bytes) -> bytes:
    if not data:
        return b''
    num_blocks = unpack_u32(data[:4])
    pos = 4
    out = bytearray()
    for _ in range(num_blocks):
        orig_len = unpack_u32(data[pos:pos + 4])
        comp_len = unpack_u32(data[pos + 4:pos + 8])
        pos += 8
        block = _decompress_single(data[pos:pos + comp_len])
        out += block
        pos += comp_len
    return bytes(out)
