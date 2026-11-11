# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/miyaguchi-preneel-construction/. The authors are listed in prov/A2T8E9.jsonl.
"""Matyas-Meyer-Oseas and Miyaguchi-Preneel on a toy 16-bit block cipher.

For study only. The toy cipher has no security; it is only invertible. A real
Miyaguchi-Preneel hash is Whirlpool. Use SHA-256 or SHA-3 from hashlib instead.

The chaining value is the key, through a map g from chaining values to keys;
the message block is the plaintext. Here keys and blocks are both 16 bits, so g
can be the identity, as in Whirlpool. g_fixed shows a map that fixes some key
bits, as needed when keys are shorter than blocks or some keys must be avoided.
"""

MASK16 = 0xFFFF
MUL = 0x6F4B
MUL_INV = pow(MUL, -1, 1 << 16)
ROUNDS = 6


def _rotl(x: int, s: int) -> int:
    return ((x << s) | (x >> (16 - s))) & MASK16


def _round_key(k: int, r: int) -> int:
    return _rotl(k, (3 * r + 1) % 16) ^ ((0x5A5A + 0x1234 * r) & MASK16)


def encrypt(k: int, x: int) -> int:
    for r in range(ROUNDS):
        x = (x + _round_key(k, r)) & MASK16
        x = (x * MUL) & MASK16
        x = _rotl(x, 5)
        x ^= x >> 7
    return x


def decrypt(k: int, y: int) -> int:
    for r in reversed(range(ROUNDS)):
        y ^= (y >> 7) ^ (y >> 14)
        y = _rotl(y, 11)
        y = (y * MUL_INV) & MASK16
        y = (y - _round_key(k, r)) & MASK16
    return y


def g_identity(h: int) -> int:
    return h


def g_fixed(h: int) -> int:
    """A g that forces bit 0 to 1 and bit 1 to 0: 2^14 keys only, so 4 chaining values share a key."""
    return (h | 1) & ~2 & MASK16


def mmo(h: int, m: int, g=g_identity) -> int:
    """Matyas-Meyer-Oseas: f(h, m) = E_g(h)(m) XOR m."""
    k = g(h)  # @line L1
    return encrypt(k, m) ^ m  # @line L2


def mp(h: int, m: int, g=g_identity) -> int:
    """Miyaguchi-Preneel: f(h, m) = E_g(h)(m) XOR m XOR h."""
    k = g(h)  # @line L1
    c = encrypt(k, m)  # @line L2
    return c ^ m ^ h  # @line L3


def mp_fixed_points(h: int, g=g_identity) -> list[int]:
    """All m with mp(h, m) = h, that is, the fixed points of the permutation E_g(h). Needs 2^16 work."""
    k = g(h)
    return [m for m in range(1 << 16) if encrypt(k, m) == m]


def iterate(f, iv: int, blocks: list[int], g=g_identity) -> int:
    h = iv  # @line L4
    for m in blocks:  # @line L5
        h = f(h, m, g)  # @line L6
    return h  # @line L7
