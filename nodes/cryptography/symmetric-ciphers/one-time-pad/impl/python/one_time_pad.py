# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/one-time-pad/. The authors are listed in prov/K0CNG3.jsonl.
"""The one-time pad over bytes, the two-time pad attack, and malleability.

For study only. The one-time pad is perfectly secret only when the key is
truly random, as long as the message, kept secret and never used again; it
gives no integrity. The code is not constant time. Do not use it to protect
real data; use AES-GCM or ChaCha20-Poly1305 from libsodium, a FIPS 140
validated module, or the standard library of your language.
"""

import secrets
from fractions import Fraction


def generate_key(n: int) -> bytes:
    """n bytes from the operating system's random source. Use each key only once."""
    return secrets.token_bytes(n)  # @line L1


def xor(a: bytes, b: bytes) -> bytes:
    """The byte by byte exclusive or of a and b; b must be at least as long as a."""
    if len(b) < len(a):
        raise ValueError("the key must be at least as long as the message")
    out = bytearray(len(a))
    for i in range(len(a)):  # @line L2
        out[i] = a[i] ^ b[i]  # @line L3
    return bytes(out)  # @line L4


def otp_encrypt(message: bytes, key: bytes) -> bytes:
    if len(key) != len(message):
        raise ValueError("the key must have the length of the message")
    return xor(message, key)


def otp_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    return otp_encrypt(ciphertext, key)


# The two-time pad: if c1 = m1 ^ k and c2 = m2 ^ k, then c1 ^ c2 = m1 ^ m2,
# and the key is gone.

TEXT_BYTES = set(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ")


def crib_drag(x: bytes, crib: bytes) -> list[tuple[int, bytes]]:
    """Slide a guessed word along x = m1 ^ m2.

    At offset i, if the crib is in one message there, then x[i:i+len] ^ crib
    is the text of the other message there. Returns the offsets where that
    text consists only of letters and spaces; a person or a language model
    then judges which fragments are real words.
    """
    out = []
    for i in range(len(x) - len(crib) + 1):
        frag = xor(crib, x[i : i + len(crib)])
        if all(b in TEXT_BYTES for b in frag):
            out.append((i, frag))
    return out


def extend(x: bytes, known: bytes, offset: int) -> bytes:
    """Given a piece of one message at offset, return the matching piece of the other."""
    return xor(known, x[offset : offset + len(known)])


def malleate(ciphertext: bytes, old: bytes, new: bytes, offset: int) -> bytes:
    """Change known plaintext old at offset into new, without the key.

    c ^ (old ^ new) decrypts to the message with old replaced by new.
    """
    if len(old) != len(new):
        raise ValueError("old and new must have the same length")
    delta = xor(old, new)
    out = bytearray(ciphertext)
    for i, d in enumerate(delta):
        out[offset + i] ^= d
    return bytes(out)


def posterior(prior: dict[int, Fraction], keys: list[int]) -> dict[int, dict[int, Fraction]]:
    """Exact P(M = m | C = c) for the XOR cipher c = m ^ k with k uniform on keys.

    Returns a map from each ciphertext c of positive probability to its
    posterior distribution on the messages.
    """
    pk = Fraction(1, len(keys))
    joint: dict[int, dict[int, Fraction]] = {}
    for m, pm in prior.items():
        for k in keys:
            c = m ^ k
            row = joint.setdefault(c, {})
            row[m] = row.get(m, Fraction(0)) + pm * pk
    out = {}
    for c, row in joint.items():
        total = sum(row.values())
        out[c] = {m: row.get(m, Fraction(0)) / total for m in prior}
    return out


def is_perfectly_secret(prior: dict[int, Fraction], keys: list[int]) -> bool:
    """True when every posterior equals the prior."""
    return all(post == prior for post in posterior(prior, keys).values())
