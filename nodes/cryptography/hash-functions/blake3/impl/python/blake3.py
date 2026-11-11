# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blake3/. The authors are listed in prov/N2JG8C.jsonl.
"""BLAKE3 (O'Connor, Aumasson, Neves and Wilcox-O'Hearn, 2020): hash, keyed_hash,
derive_key and extendable output.

blake3(data, length) is the default hash; length may be any number of bytes.
blake3(data, length, key=k) is keyed_hash with a 32-byte key.
derive_key(context, material, length) is the key derivation mode.
Hasher is the incremental form with the chaining value stack; it gives the same output.

For study only. The code is not constant time and must not protect real data.
Use the official blake3 crate or the C library, or the blake3 Python package, instead.
"""

IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
MSG_PERMUTATION = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)

CHUNK_START, CHUNK_END, PARENT, ROOT = 1, 2, 4, 8
KEYED_HASH, DERIVE_KEY_CONTEXT, DERIVE_KEY_MATERIAL = 16, 32, 64

BLOCK_LEN, CHUNK_LEN = 64, 1024
M32 = 0xFFFFFFFF


def _rotr(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & M32


def g(s: list[int], a: int, b: int, c: int, d: int, x: int, y: int) -> None:
    """The BLAKE2s mixing function, with rotations 16, 12, 8 and 7."""
    # @line L9
    s[a] = (s[a] + s[b] + x) & M32
    s[d] = _rotr(s[d] ^ s[a], 16)
    s[c] = (s[c] + s[d]) & M32
    s[b] = _rotr(s[b] ^ s[c], 12)
    s[a] = (s[a] + s[b] + y) & M32
    s[d] = _rotr(s[d] ^ s[a], 8)
    s[c] = (s[c] + s[d]) & M32
    s[b] = _rotr(s[b] ^ s[c], 7)


def compress(cv: tuple, block: bytes, counter: int, block_len: int, flags: int) -> list[int]:
    """The compression function: 16 output words (lines L6 to L8)."""
    m = [int.from_bytes(block[4 * i:4 * i + 4], "little") for i in range(16)]
    # @line L6
    s = list(cv) + list(IV[:4]) + [counter & M32, (counter >> 32) & M32, block_len, flags]
    # @line L7
    for r in range(7):
        g(s, 0, 4, 8, 12, m[0], m[1])
        g(s, 1, 5, 9, 13, m[2], m[3])
        g(s, 2, 6, 10, 14, m[4], m[5])
        g(s, 3, 7, 11, 15, m[6], m[7])
        g(s, 0, 5, 10, 15, m[8], m[9])
        g(s, 1, 6, 11, 12, m[10], m[11])
        g(s, 2, 7, 8, 13, m[12], m[13])
        g(s, 3, 4, 9, 14, m[14], m[15])
        if r < 6:
            m = [m[MSG_PERMUTATION[i]] for i in range(16)]
    # @line L8
    return [s[i] ^ s[i + 8] for i in range(8)] + [s[i + 8] ^ cv[i] for i in range(8)]


class Node:
    """The inputs of one compression whose output is not yet used (an "output" in the paper)."""

    def __init__(self, cv: tuple, block: bytes, counter: int, block_len: int, flags: int) -> None:
        self.cv, self.block, self.counter, self.block_len, self.flags = cv, block, counter, block_len, flags

    def chaining_value(self) -> tuple:
        return tuple(compress(self.cv, self.block, self.counter, self.block_len, self.flags)[:8])

    def root_output(self, length: int) -> bytes:
        # @line L5
        out = bytearray()
        t = 0
        while len(out) < length:
            words = compress(self.cv, self.block, t, self.block_len, self.flags | ROOT)
            out += b"".join(w.to_bytes(4, "little") for w in words)
            t += 1
        return bytes(out[:length])


def chunk_node(key: tuple, chunk: bytes, index: int, flags: int) -> Node:
    """Lines L2 and L3: chain the blocks of one chunk; the last block stays open."""
    blocks = [chunk[i:i + BLOCK_LEN] for i in range(0, len(chunk), BLOCK_LEN)] or [b""]
    cv = key
    # @line L2
    for i, b in enumerate(blocks[:-1]):
        f = flags | (CHUNK_START if i == 0 else 0)
        cv = tuple(compress(cv, b, index, BLOCK_LEN, f)[:8])
    # @line L3
    last = blocks[-1]
    f = flags | CHUNK_END | (CHUNK_START if len(blocks) == 1 else 0)
    return Node(cv, last.ljust(BLOCK_LEN, b"\0"), index, len(last), f)


def parent_node(key: tuple, left: tuple, right: tuple, flags: int) -> Node:
    block = b"".join(w.to_bytes(4, "little") for w in left + right)
    return Node(key, block, 0, BLOCK_LEN, flags | PARENT)


def tree_node(key: tuple, data: bytes, first_chunk: int, flags: int) -> Node:
    """Line L4: the left subtree holds the largest power of 2 chunks that leaves data on the right."""
    # @line L1
    if len(data) <= CHUNK_LEN:
        return chunk_node(key, data, first_chunk, flags)
    # @line L4
    left_chunks = 1 << (((len(data) - 1) // CHUNK_LEN).bit_length() - 1)
    split = left_chunks * CHUNK_LEN
    left = tree_node(key, data[:split], first_chunk, flags).chaining_value()
    right = tree_node(key, data[split:], first_chunk + left_chunks, flags).chaining_value()
    return parent_node(key, left, right, flags)


def _key_words(key: bytes) -> tuple:
    if len(key) != 32:
        raise ValueError("the key has 32 bytes")
    return tuple(int.from_bytes(key[4 * i:4 * i + 4], "little") for i in range(8))


def blake3(data: bytes, length: int = 32, key: bytes | None = None) -> bytes:
    """Line L10: hash (key = IV) or keyed_hash (the given key, flag KEYED_HASH)."""
    # @line L10
    if key is None:
        return tree_node(IV, data, 0, 0).root_output(length)
    return tree_node(_key_words(key), data, 0, KEYED_HASH).root_output(length)


def derive_key(context: bytes, material: bytes, length: int = 32) -> bytes:
    """Line L10, derive_key: hash the context to a key, then hash the material with it."""
    ctx_key = tree_node(IV, context, 0, DERIVE_KEY_CONTEXT).root_output(32)
    return tree_node(_key_words(ctx_key), material, 0, DERIVE_KEY_MATERIAL).root_output(length)


class Hasher:
    """Incremental BLAKE3 with a stack of chaining values (Section 5.1 of the paper).

    After chunk number c (counting from 1) is done, the code merges as many
    subtrees as c has trailing zero bits. The stack never holds more than
    one chaining value per bit of the chunk count.
    """

    def __init__(self, key: bytes | None = None) -> None:
        self.key = IV if key is None else _key_words(key)
        self.flags = 0 if key is None else KEYED_HASH
        self.stack: list[tuple] = []
        self.buf = b""
        self.chunks = 0
        self.max_stack = 0

    def update(self, data: bytes) -> "Hasher":
        self.buf += data
        # Keep at least one byte, so the last chunk is never closed early.
        while len(self.buf) > CHUNK_LEN:
            cv = chunk_node(self.key, self.buf[:CHUNK_LEN], self.chunks, self.flags).chaining_value()
            self.buf = self.buf[CHUNK_LEN:]
            self.chunks += 1
            total = self.chunks
            while total & 1 == 0:
                cv = parent_node(self.key, self.stack.pop(), cv, self.flags).chaining_value()
                total >>= 1
            self.stack.append(cv)
            self.max_stack = max(self.max_stack, len(self.stack))
        return self

    def finalize(self, length: int = 32) -> bytes:
        node = chunk_node(self.key, self.buf, self.chunks, self.flags)
        for left in reversed(self.stack):
            node = parent_node(self.key, left, node.chaining_value(), self.flags)
        return node.root_output(length)
