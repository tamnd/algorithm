# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/davies-meyer-construction/. The authors are listed in prov/MYQDY5.jsonl.
"""Davies-Meyer on a toy 16-bit block cipher: the compression function, its fixed points,
and why the feed-forward is needed.

For study only. The toy cipher has a 16-bit block and a 16-bit key and no
security; it is only invertible. Real Davies-Meyer hashes are SHA-1, SHA-2 and
MD5 (MD5 and SHA-1 are broken). Use SHA-256 or SHA-3 from hashlib instead.
"""

MASK16 = 0xFFFF
MUL = 0x6F4B
MUL_INV = pow(MUL, -1, 1 << 16)
ROUNDS = 6
N_BITS = 16


def _rotl(x: int, s: int) -> int:
    return ((x << s) | (x >> (16 - s))) & MASK16


def _round_key(k: int, r: int) -> int:
    return _rotl(k, (3 * r + 1) % 16) ^ ((0x5A5A + 0x1234 * r) & MASK16)


def encrypt(k: int, x: int) -> int:
    """E_k(x) of the toy cipher."""
    for r in range(ROUNDS):
        x = (x + _round_key(k, r)) & MASK16
        x = (x * MUL) & MASK16
        x = _rotl(x, 5)
        x ^= x >> 7
    return x


def decrypt(k: int, y: int) -> int:
    """E_k^(-1)(y) of the toy cipher."""
    for r in reversed(range(ROUNDS)):
        y ^= (y >> 7) ^ (y >> 14)
        y = _rotl(y, 11)
        y = (y * MUL_INV) & MASK16
        y = (y - _round_key(k, r)) & MASK16
    return y


def davies_meyer(h: int, m: int) -> int:
    """f(h, m) = E_m(h) XOR h: the message block is the key, the chaining value is the plaintext."""
    y = encrypt(m, h)  # @line L1
    return y ^ h  # @line L2


def fixed_point(m: int) -> int:
    """The chaining value h with f(h, m) = h: since E_m(h) XOR h = h iff E_m(h) = 0, h = E_m^(-1)(0)."""
    return decrypt(m, 0)  # @line L3


def no_feed_forward(h: int, m: int) -> int:
    """f(h, m) = E_m(h) without the XOR. Not secure: it can be inverted."""
    return encrypt(m, h)


def preimage_without_feed_forward(target: int, m: int) -> int:
    """For any block m, the chaining value h = E_m^(-1)(target) maps to target."""
    return decrypt(m, target)


def collision_search(h: int, limit: int = 1 << 16):
    """Birthday search for blocks m != m' with f(h, m) == f(h, m'). Returns (m, m', queries)."""
    seen: dict[int, int] = {}
    for q, m in enumerate(range(limit), start=1):
        v = davies_meyer(h, m)
        if v in seen:
            return seen[v], m, q
        seen[v] = m
    return None


def brs_collision_bound(q: int, n: int = N_BITS) -> float:
    """Black, Rogaway and Shrimpton (2002), Theorem 3.1: Adv^coll <= q(q + 1) / 2^n
    for the iterated group-1 hashes, Davies-Meyer included, in the ideal cipher model."""
    return min(1.0, q * (q + 1) / 2 ** n)
