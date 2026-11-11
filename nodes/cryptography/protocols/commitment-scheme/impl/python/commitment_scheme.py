# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/commitment-scheme/. The authors are listed in prov/AZDCQJ.jsonl.
"""Two commitment schemes: the hash commitment and Naor's bit commitment.

The hash commitment is c = SHA-256(r || m) with a 32-byte random r. It is
hiding and binding in the random oracle model, and binding when SHA-256 is
collision resistant.

Naor's bit commitment (J. Cryptology 1991) is built from a pseudorandom
generator G that stretches n bits to 3n bits. The receiver first sends a random
3n-bit string R. The committer picks a seed s and sends G(s) for b = 0 or
G(s) xor R for b = 1. Here G is SHA-256 in counter mode, a stand-in for a
proven PRG.

For study only. The code is not constant time and must not be used to protect
real data. Use a reviewed library (libsodium, or a FIPS 140 validated module)
and a protocol that has been analysed as a whole.
"""

import hashlib
import secrets

R_BYTES = 32


# ------------------------------------------------------------ hash commitment
def hash_commit(message: bytes, r: bytes = None):
    """Return (c, r) with c = SHA-256(r || message)."""
    if r is None:
        r = secrets.token_bytes(R_BYTES)
    return hashlib.sha256(r + message).digest(), r


def hash_open(c: bytes, message: bytes, r: bytes) -> bool:
    """Check an opening (message, r) against the commitment c."""
    return hashlib.sha256(r + message).digest() == c


def truncated_commit(message: bytes, r: bytes, out_bits: int) -> int:
    """The hash commitment cut to out_bits bits. Only for the toy tests."""
    d = int.from_bytes(hashlib.sha256(r + message).digest(), "big")
    return d >> (256 - out_bits)


# --------------------------------------------------- Naor's bit commitment
def prg(seed: int, n: int) -> int:
    """Stretch an n-bit seed to a 3n-bit string (as an int).

    SHA-256 of (seed, counter) in counter mode, cut to 3n bits.
    """
    seed_bytes = seed.to_bytes((n + 7) // 8, "big")
    out = b""
    counter = 0
    while len(out) * 8 < 3 * n:
        out += hashlib.sha256(seed_bytes + counter.to_bytes(4, "big")).digest()
        counter += 1
    return int.from_bytes(out, "big") >> (len(out) * 8 - 3 * n)


def naor_receiver_first(n: int) -> int:
    """Move 1 of the commit phase: the receiver sends a random 3n-bit R."""
    return secrets.randbits(3 * n)


def naor_commit(bit: int, r_string: int, n: int, seed: int = None):
    """Move 2: return (c, seed). c = G(seed) if bit = 0, else G(seed) xor R."""
    if bit not in (0, 1):
        raise ValueError("bit must be 0 or 1")
    if seed is None:
        seed = secrets.randbits(n)
    y = prg(seed, n)
    return (y ^ r_string if bit else y), seed


def naor_open(c: int, r_string: int, n: int, bit: int, seed: int) -> bool:
    """The receiver checks the opening (bit, seed)."""
    if bit not in (0, 1) or not 0 <= seed < (1 << n):
        return False
    y = prg(seed, n)
    return c == (y ^ r_string if bit else y)


def naor_bad_strings(n: int) -> set:
    """All R for which some commitment opens to both bits.

    A commitment c opens to 0 with seed s0 and to 1 with seed s1 exactly when
    c = G(s0) = G(s1) xor R, so R = G(s0) xor G(s1). Exhaustive, so only for
    small n.
    """
    outs = [prg(s, n) for s in range(1 << n)]
    return {a ^ b for a in outs for b in outs}
