# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fujisaki-okamoto-transform/. The authors are listed in prov/4ZNST2.jsonl.
"""The Fujisaki-Okamoto transform FO with implicit rejection (Hofheinz,
Hovelmanns and Kiltz 2017), applied to ElGamal in the squares modulo a
safe prime.

T:   Enc'(pk, m) = Enc(pk, m; G(m)), and Dec' re-encrypts to check.
U:   Encaps picks a random m, sends c = Enc'(pk, m), and keys K = H(m, c).
     Decaps returns H(m', c) if c re-encrypts correctly and the
     pseudorandom H_rej(s, c) with a secret s otherwise.

G, H and H_rej are SHA-256 with distinct prefixes. The security proof
models them as random oracles.

For study only. This code is not constant time (the comparison and the
branch on the check leak timing), and the 64-digit group is far too small.
"""

import hashlib
import secrets
from dataclasses import dataclass

P = 9223372036854778487  # the smallest safe prime above 2^63
Q = (P - 1) // 2  # prime order of the group of squares
GEN = 4
NBYTES = (P.bit_length() + 7) // 8

Ciphertext = tuple[int, int]


@dataclass(frozen=True)
class PublicKey:
    h: int


@dataclass(frozen=True)
class PrivateKey:
    x: int
    s: bytes  # the implicit-rejection secret
    pk: PublicKey


def _enc_int(a: int) -> bytes:
    return a.to_bytes(NBYTES, "big")


def hash_g(m: int) -> int:
    """G: the message to the encryption randomness in Z_q."""
    return int.from_bytes(hashlib.sha256(b"FO-G" + _enc_int(m)).digest(), "big") % Q


def hash_h(m: int, c: Ciphertext) -> bytes:
    """H: the message and ciphertext to a 32-byte key."""
    return hashlib.sha256(b"FO-H" + _enc_int(m) + _enc_int(c[0]) + _enc_int(c[1])).digest()


def hash_rej(s: bytes, c: Ciphertext) -> bytes:
    """H_rej: the rejection secret and ciphertext to a 32-byte pseudorandom key."""
    return hashlib.sha256(b"FO-R" + s + _enc_int(c[0]) + _enc_int(c[1])).digest()


def in_group(a: int) -> bool:
    return 0 < a < P and pow(a, Q, P) == 1


def elgamal_encrypt(pk: PublicKey, m: int, r: int) -> Ciphertext:
    """The base scheme with explicit randomness r. Cost: two exponentiations."""
    return pow(GEN, r, P), m * pow(pk.h, r, P) % P


def elgamal_decrypt(x: int, c: Ciphertext) -> int:
    """The base decryption c2 / c1^x. Cost: one exponentiation."""
    return c[1] * pow(c[0], (Q - x) % Q, P) % P


def keygen(rng_bytes=secrets.token_bytes) -> tuple[PublicKey, PrivateKey]:
    """ElGamal key plus a 32-byte rejection secret."""
    x = int.from_bytes(rng_bytes(16), "big") % Q
    pk = PublicKey(pow(GEN, x, P))
    return pk, PrivateKey(x, rng_bytes(32), pk)


def encaps(pk: PublicKey, rng_bytes=secrets.token_bytes) -> tuple[Ciphertext, bytes]:
    """Return (c, K). Cost: three exponentiations and two hashes."""
    m = pow(GEN, int.from_bytes(rng_bytes(16), "big") % Q, P)  # @line L1
    c = elgamal_encrypt(pk, m, hash_g(m))  # @line L2
    return c, hash_h(m, c)  # @line L3


def decaps(sk: PrivateKey, c: Ciphertext) -> bytes:
    """Return the key; never fails. Cost: about four exponentiations and two hashes."""
    if not (in_group(c[0]) and in_group(c[1])):
        return hash_rej(sk.s, c)
    m = elgamal_decrypt(sk.x, c)  # @line L4
    if elgamal_encrypt(sk.pk, m, hash_g(m)) == c:  # @line L5
        return hash_h(m, c)  # @line L6
    return hash_rej(sk.s, c)  # @line L7


def insecure_decaps_hash_m_only(sk: PrivateKey, c: Ciphertext) -> bytes:
    """A broken variant for the tests: no re-encryption check and K = H(m) only."""
    m = elgamal_decrypt(sk.x, c)
    return hashlib.sha256(b"FO-H" + _enc_int(m)).digest()


def insecure_encaps_hash_m_only(pk: PublicKey, rng_bytes=secrets.token_bytes) -> tuple[Ciphertext, bytes]:
    """The matching broken encapsulation: plain randomized ElGamal and K = H(m)."""
    m = pow(GEN, int.from_bytes(rng_bytes(16), "big") % Q, P)
    r = int.from_bytes(rng_bytes(16), "big") % Q
    c = elgamal_encrypt(pk, m, r)
    return c, hashlib.sha256(b"FO-H" + _enc_int(m)).digest()
