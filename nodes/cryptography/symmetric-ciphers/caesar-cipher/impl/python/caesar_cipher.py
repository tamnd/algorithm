# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/caesar-cipher/. The authors are listed in prov/CZPQ1B.jsonl.
"""The Caesar cipher (the shift cipher) and the brute-force attack on it.

For study only. The cipher has 26 keys and gives no protection. The code is
not constant time. Do not use it to protect real data; use AES-GCM or
ChaCha20-Poly1305 from libsodium, a FIPS 140 validated module, or the
standard library of your language.

Letters A to Z and a to z are shifted, and their case is kept. Each other
character is copied unchanged. Cost: one addition modulo 26 for each letter.
"""

from english import chi_squared


def _shift(ch: str, k: int) -> str:
    if "A" <= ch <= "Z":
        return chr((ord(ch) - 65 + k) % 26 + 65)
    if "a" <= ch <= "z":
        return chr((ord(ch) - 97 + k) % 26 + 97)
    return ch


def caesar_encrypt(plaintext: str, k: int) -> str:
    """Shift each letter of plaintext forward by k places, modulo 26."""
    out = []
    for p in plaintext:  # @line L1
        out.append(_shift(p, k))  # @line L2
    return "".join(out)  # @line L3


def caesar_decrypt(ciphertext: str, k: int) -> str:
    """Shift each letter of ciphertext back by k places, modulo 26."""
    return caesar_encrypt(ciphertext, -k)


def caesar_break(ciphertext: str) -> list[tuple[float, int]]:
    """Try all 26 keys and rank them by the chi-squared score of the decryption.

    Returns the pairs (score, key), best first. The best key is the first
    entry. Cost: 26 decryptions and 26 scores, so linear in the length.
    """
    ranked = []
    for k in range(26):
        ranked.append((chi_squared(caesar_decrypt(ciphertext, k)), k))
    ranked.sort()
    return ranked
