import time
from source.compressor import compress, decompress
import zstandard as zstd
import brotli
import zlib

with open("input.txt", "rb") as f:
    data = f.read()

start = time.time()
c_data = compress(data)
print(f"\n   compressor:\n      > compression time:   {time.time()-start:.4f} s")
start = time.time()
d_data = decompress(c_data)
print(f"      > decompression time: {time.time()-start:.4f} s")
with open("d-input.txt", "wb") as f:
    f.write(d_data)
print(f"      > compression ratio:  {(1 - len(c_data)/len(data))*100:.2f} %")
with open("out.txt", "wb") as f:
    f.write(c_data)

start = time.time()
c_data = zstd.ZstdCompressor(level=22).compress(data)
start = time.time()
d_data = zstd.ZstdDecompressor().decompress(c_data)
print(f"\n   zstd, brotli, zlib\n      > compression ratio:  {(1 - len(c_data)/len(data))*100:.2f} %")

start = time.time()
c_data = brotli.compress(data, quality=11)
start = time.time()
d_data = brotli.decompress(c_data)
print(f"      > compression ratio:  {(1 - len(c_data)/len(data))*100:.2f} %")

start = time.time()
c_data = zlib.compress(data, level=9)
start = time.time()
d_data = zlib.decompress(c_data)
print(f"      > compression ratio:  {(1 - len(c_data)/len(data))*100:.2f} %")
