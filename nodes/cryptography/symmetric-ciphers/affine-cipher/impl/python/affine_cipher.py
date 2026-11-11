# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/affine-cipher/. The authors are listed in prov/WCAD3J.jsonl.
"""The affine cipher E(x) = a x + b mod 26, its key recovery from two known
letter pairs, and a brute-force search of its 312 keys.

For study only. The cipher has 312 keys and gives no protection. The code is
not constant time. Do not use it to protect real data; use AES-GCM or
ChaCha20-Poly1305 from libsodium, a FIPS 140 validated module, or the
standard library of your language.

Letters A to Z and a to z are mapped, and their case is kept. Each other
character is copied unchanged. Cost: one multiplication and one addition
modulo 26 for each letter.
"""

from english import chi_squared

M = 26


def inverse_mod(a: int, m: int = M) -> int:
    """The inverse of a modulo m by the extended Euclidean algorithm.

    Raises ValueError when gcd(a, m) is not 1.
    """
    r0, r1, s0, s1 = m, a % m, 0, 1
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if r0 != 1:
        raise ValueError(f"{a} has no inverse modulo {m}")
    return s0 % m


def _map(text: str, f) -> str:
    out = []
    for ch in text:
        if "A" <= ch <= "Z":
            out.append(chr(f(ord(ch) - 65) + 65))
        elif "a" <= ch <= "z":
            out.append(chr(f(ord(ch) - 97) + 97))
        else:
            out.append(ch)
    return "".join(out)


def affine_encrypt(plaintext: str, a: int, b: int) -> str:
    """Map each letter x of plaintext to (a x + b) mod 26; gcd(a, 26) must be 1."""
    inverse_mod(a)  # @line L1
    return _map(plaintext, lambda x: (a * x + b) % M)  # @line L2


def affine_decrypt(ciphertext: str, a: int, b: int) -> str:
    """Map each letter y of ciphertext to a^-1 (y - b) mod 26."""
    a_inv = inverse_mod(a)  # @line L3
    return _map(ciphertext, lambda y: a_inv * (y - b) % M)  # @line L4


def all_keys() -> list[tuple[int, int]]:
    """The 312 keys (a, b) with gcd(a, 26) = 1."""
    return [(a, b) for a in range(M) if a % 2 == 1 and a != 13 for b in range(M)]


def recover_key(x1: int, y1: int, x2: int, y2: int) -> list[tuple[int, int]]:
    """All keys (a, b) with a x1 + b = y1 and a x2 + b = y2 modulo 26.

    The letters are numbers 0 to 25. When x1 - x2 is not 0 or 13 modulo 26,
    the list has at most one key. Cost: at most 12 tries of a.
    """
    dx, dy = (x1 - x2) % M, (y1 - y2) % M
    keys = []
    for a in range(1, M, 2):
        if a == 13 or (a * dx - dy) % M != 0:
            continue
        keys.append((a, (y1 - a * x1) % M))
    return keys


def affine_break(ciphertext: str) -> list[tuple[float, int, int]]:
    """Try all 312 keys and rank them by the chi-squared score of the decryption.

    Returns the triples (score, a, b), best first.
    """
    ranked = [(chi_squared(affine_decrypt(ciphertext, a, b)), a, b) for a, b in all_keys()]
    ranked.sort()
    return ranked
