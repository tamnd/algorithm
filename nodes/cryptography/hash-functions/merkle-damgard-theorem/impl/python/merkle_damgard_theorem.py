# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merkle-damgard-theorem/. The authors are listed in prov/0WC6B8.jsonl.
"""The Merkle-Damgard theorem on a toy scale: the reduction of the proof, and the counterexample
that shows why the padding must encode the length.

For study only. Every function here has 16-bit or smaller values, so collisions
are found in milliseconds; nothing here is secure. Use SHA-256 or SHA-3 from
hashlib for real hashing.

The toy compression function is Davies-Meyer on a small invertible cipher:
f(h, m) = E_m(h) XOR h, with 16-bit chaining values h and 2-byte blocks m. It
can be truncated to n < 16 bits so that birthday search finds collisions fast.
"""

MASK16 = 0xFFFF
MUL = 0x6F4B  # odd, so invertible modulo 2^16
MUL_INV = pow(MUL, -1, 1 << 16)
ROUNDS = 6
BLOCK = 2  # bytes per message block


def _rotl(x: int, s: int) -> int:
    return ((x << s) | (x >> (16 - s))) & MASK16


def _round_key(k: int, r: int) -> int:
    return _rotl(k, (3 * r + 1) % 16) ^ ((0x5A5A + 0x1234 * r) & MASK16)


def toy_encrypt(k: int, x: int) -> int:
    """A toy 16-bit block cipher with a 16-bit key. Not secure; only invertible and mixing."""
    for r in range(ROUNDS):
        x = (x + _round_key(k, r)) & MASK16
        x = (x * MUL) & MASK16
        x = _rotl(x, 5)
        x ^= x >> 7
    return x


def toy_decrypt(k: int, y: int) -> int:
    for r in reversed(range(ROUNDS)):
        y ^= (y >> 7) ^ (y >> 14)
        y = _rotl(y, 11)
        y = (y * MUL_INV) & MASK16
        y = (y - _round_key(k, r)) & MASK16
    return y


def make_f(nbits: int = 16):
    """The toy compression function f(h, m) = E_m(h) XOR h, keeping the low nbits bits."""
    mask = (1 << nbits) - 1

    def f(h: int, m: int) -> int:
        return (toy_encrypt(m, h) ^ h) & mask

    return f


def pad_strengthened(msg: bytes) -> list[int]:
    """MD strengthening: 0x80, zeros to a whole block, then one block with the byte length."""
    assert len(msg) < 1 << 16
    data = msg + b"\x80" + b"\x00" * ((-len(msg) - 1) % BLOCK)
    blocks = [int.from_bytes(data[i:i + BLOCK], "big") for i in range(0, len(data), BLOCK)]
    return blocks + [len(msg)]


def pad_no_length(msg: bytes) -> list[int]:
    """The padding without the length: 0x80 and zeros only. It is injective but not suffix-free."""
    data = msg + b"\x80" + b"\x00" * ((-len(msg) - 1) % BLOCK)
    return [int.from_bytes(data[i:i + BLOCK], "big") for i in range(0, len(data), BLOCK)]


def md(f, iv: int, blocks: list[int]) -> list[int]:
    """The chain h_0 = iv, h_i = f(h_(i-1), m_i). Returns all chaining values."""
    hs = [iv]  # @line L1
    for m in blocks:  # @line L2
        hs.append(f(hs[-1], m))  # @line L3
    return hs  # @line L4


def extract_collision(f, iv: int, msg1: bytes, msg2: bytes):
    """The reduction of the proof: from msg1 != msg2 with equal strengthened MD hash,
    return two different inputs (h, m) and (h', m') of f with f(h, m) == f(h', m')."""
    b1, b2 = pad_strengthened(msg1), pad_strengthened(msg2)  # @line L5
    h1, h2 = md(f, iv, b1), md(f, iv, b2)  # @line L6
    assert msg1 != msg2 and h1[-1] == h2[-1]
    i, j = len(b1), len(b2)  # @line L7
    while True:  # @line L8
        x, y = (h1[i - 1], b1[i - 1]), (h2[j - 1], b2[j - 1])  # @line L9
        if x != y:  # @line L10
            return x, y  # @line L11
        i, j = i - 1, j - 1  # @line L12


def plant_fixed_point(block: int) -> int:
    """An IV with f(IV, block) = IV for the 16-bit toy f: IV = E_block^(-1)(0)."""
    return toy_decrypt(block, 0)


def birthday_md_collision(f, iv: int, tries: int = 1 << 14):
    """Find two different 4-byte messages with equal strengthened MD hash, by birthday search."""
    seen: dict[int, bytes] = {}
    for t in range(tries):
        msg = t.to_bytes(4, "big")
        d = md(f, iv, pad_strengthened(msg))[-1]
        if d in seen:
            return seen[d], msg
        seen[d] = msg
    return None
