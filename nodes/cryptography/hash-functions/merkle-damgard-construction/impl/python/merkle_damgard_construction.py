# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merkle-damgard-construction/. The authors are listed in prov/FVJZV5.jsonl.
"""The Merkle-Damgard construction with MD strengthening, over any compression function,
and two of its generic weaknesses shown on a toy compression function.

For study only. The toy compression function has 16-bit values and no
security. Use SHA-256, SHA-512/256 or SHA-3 from hashlib for real hashing.

A compression function here is a callable f(h, block) -> h on integers h and
blocks of `block_size` bytes. The padding is the one of MD5 and SHA-256 in
shape: the byte 0x80, zeros, then the bit length in `len_size` bytes.
"""


def md_pad(msg_len: int, block_size: int, len_size: int, order: str = "big") -> bytes:
    """The padding for a message of msg_len bytes (MD strengthening)."""
    zeros = (-(msg_len + 1 + len_size)) % block_size  # @line L1
    return b"\x80" + b"\x00" * zeros + (8 * msg_len).to_bytes(len_size, order)  # @line L2


def md_hash(f, iv: int, msg: bytes, block_size: int, len_size: int, order: str = "big") -> int:
    """MD^f(msg): pad, split into blocks, and iterate f from the IV."""
    data = msg + md_pad(len(msg), block_size, len_size, order)  # @line L3
    h = iv  # @line L4
    for i in range(0, len(data), block_size):  # @line L5
        h = f(h, data[i:i + block_size])  # @line L6
    return h  # @line L7


def md_continue(f, h: int, total_len: int, suffix: bytes, block_size: int, len_size: int,
                order: str = "big") -> int:
    """Continue the chain from h as if total_len bytes were already hashed and padded.
    This is the length-extension step: it needs h, not the secret prefix."""
    data = suffix + md_pad(total_len + len(suffix), block_size, len_size, order)
    for i in range(0, len(data), block_size):
        h = f(h, data[i:i + block_size])
    return h


# A toy compression function: 16-bit chaining value, 2-byte block.
MASK16 = 0xFFFF


def toy_f(h: int, block: bytes) -> int:
    """A toy mixing function. It is not collision resistant at 16 bits; that is the point."""
    m = int.from_bytes(block, "big")
    x = h ^ 0x9E37
    for r in range(4):
        x = (x + (m ^ (0x3C6E * (r + 1)))) & MASK16
        x = (x * 0x6F4B) & MASK16
        x = ((x << 5) | (x >> 11)) & MASK16
        x ^= x >> 7
    return x ^ h


def find_block_collision(f, h: int, block_size: int, start: int = 0):
    """Two different blocks b, b' with f(h, b) == f(h, b'), by birthday search."""
    seen: dict[int, bytes] = {}
    i = start
    while True:
        b = i.to_bytes(block_size, "big")
        v = f(h, b)
        if v in seen and seen[v] != b:
            return seen[v], b, v
        seen[v] = b
        i += 1


def joux_multicollision(f, iv: int, k: int, block_size: int):
    """Joux (2004): k successive block collisions give 2^k messages of k blocks with the same chain.
    Returns the list of k pairs and the final chaining value (before padding)."""
    pairs = []
    h = iv
    for _ in range(k):
        b0, b1, h = find_block_collision(f, h, block_size)
        pairs.append((b0, b1))
    return pairs, h
