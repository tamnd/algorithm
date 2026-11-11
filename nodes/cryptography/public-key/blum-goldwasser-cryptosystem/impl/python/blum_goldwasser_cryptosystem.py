# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blum-goldwasser-cryptosystem/. The authors are listed in prov/QJYEG7.jsonl.
"""Blum-Goldwasser probabilistic encryption (1984), as in HAC Algorithm 8.56.

The sender squares a random seed x0 modulo a Blum integer n = p q and XORs
the h low bits of each x_i onto an h-bit message block (the Blum-Blum-Shub
generator). It sends the blocks and x_{t+1}. The receiver takes square roots
t + 1 times at once with the exponents ((p + 1)/4)^(t+1) to get x0 back.

For study only. This code is not constant time, the primes are supplied by
the caller, and the scheme is insecure against chosen-ciphertext attacks.
"""

import random
import secrets
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class PrivateKey:
    p: int
    q: int
    a: int
    b: int


def block_size(n: int) -> int:
    """h = floor(lg k) with k = floor(lg n), as in HAC Algorithm 8.56."""
    k = n.bit_length() - 1
    return k.bit_length() - 1


def keygen(p: int, q: int) -> tuple[int, PrivateKey]:
    """Make a key from distinct primes p, q = 3 (mod 4). Cost: one extended gcd, O(b^2)."""
    if p == q or p % 4 != 3 or q % 4 != 3:
        raise ValueError("p and q must be distinct primes congruent to 3 modulo 4")
    n = p * q  # @line L1
    old_r, r, old_s, s = p, q, 1, 0  # extended Euclid on (p, q): a p + b q = 1
    while r:
        quo = old_r // r
        old_r, r = r, old_r - quo * r
        old_s, s = s, old_s - quo * s
    a = old_s
    b = (1 - a * p) // q  # @line L2
    return n, PrivateKey(p, q, a, b)  # @line L3


def encrypt(n: int, blocks: list[int], rng: random.Random | None = None) -> tuple[list[int], int]:
    """Encrypt t blocks of h binary digits. Cost: t + 2 multiplications modulo n."""
    h = block_size(n)
    mask = (1 << h) - 1
    while True:
        r = rng.randrange(1, n) if rng is not None else secrets.randbelow(n - 1) + 1
        if gcd(r, n) == 1:
            break
    x = r * r % n  # @line L4
    cs = []
    for m in blocks:  # @line L5
        if not 0 <= m <= mask:
            raise ValueError("each block must have at most h binary digits")
        x = x * x % n  # @line L6
        cs.append((x & mask) ^ m)  # @line L7
    x = x * x % n  # @line L8
    return cs, x  # @line L9


def recover_seed(sk: PrivateKey, t: int, x_last: int) -> int:
    """x0 from x_{t+1}, by t + 1 principal square roots at once. Cost: four exponentiations."""
    p, q = sk.p, sk.q
    d1 = pow((p + 1) // 4, t + 1, p - 1)  # @line L10
    d2 = pow((q + 1) // 4, t + 1, q - 1)
    u = pow(x_last % p, d1, p)  # @line L11
    v = pow(x_last % q, d2, q)
    return (v * sk.a * p + u * sk.b * q) % (p * q)  # @line L12


def decrypt(sk: PrivateKey, cs: list[int], x_last: int) -> list[int]:
    """Decrypt t blocks. Cost: four exponentiations and t multiplications modulo n."""
    n = sk.p * sk.q
    mask = (1 << block_size(n)) - 1
    x = recover_seed(sk, len(cs), x_last)
    ms = []
    for c in cs:  # @line L13
        x = x * x % n
        ms.append((x & mask) ^ c)
    return ms  # @line L14


def to_blocks(data: bytes, h: int) -> list[int]:
    """Split a byte string into h-bit blocks, most significant first, padding the end with zeros."""
    bits = "".join(f"{byte:08b}" for byte in data)
    bits += "0" * (-len(bits) % h)
    return [int(bits[i : i + h], 2) for i in range(0, len(bits), h)]


def from_blocks(blocks: list[int], h: int, length: int) -> bytes:
    """The inverse of to_blocks for a message of the given byte length."""
    bits = "".join(f"{b:0{h}b}" for b in blocks)[: 8 * length]
    return bytes(int(bits[i : i + 8], 2) for i in range(0, len(bits), 8))
