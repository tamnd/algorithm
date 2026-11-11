# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lamport-signature/. The authors are listed in prov/4WMP39.jsonl.
"""Lamport one-time signature (Lamport 1979), with SHA-256 as the hash.

The message is hashed to a digest of n bits. The secret key is 2n random
values x[i][0], x[i][1]; the public key is their hashes y[i][b] = H(x[i][b]).
A signature reveals x[i][d_i] for each bit d_i of the digest.

The page is about the signature, not the hash, so SHA-256 comes from hashlib.
A small n (the first n bits of the digest) is allowed for toy experiments.

For study only. The code is not constant time and it must not protect real
data. A Lamport key must sign only one message. For real use take a standard
hash-based scheme (LMS or XMSS of NIST SP 800-208, or SLH-DSA of FIPS 205)
from a FIPS 140 validated module or a reviewed library.
"""

import hashlib
import secrets
from collections.abc import Callable

VALUE_BYTES = 32  # length of each secret value and of each hash value

SecretKey = list[list[bytes]]
PublicKey = list[list[bytes]]
Signature = list[bytes]


def h(data: bytes) -> bytes:
    """The one-way function applied to the secret values."""
    return hashlib.sha256(data).digest()


def digest_bits(message: bytes, n: int = 256) -> list[int]:
    """The first n bits of SHA-256(message), most significant bit first."""
    if not 1 <= n <= 256:
        raise ValueError("n must be in 1..256")
    d = hashlib.sha256(message).digest()
    return [(d[i // 8] >> (7 - i % 8)) & 1 for i in range(n)]


def keygen(n: int = 256, rand: Callable[[int], bytes] = secrets.token_bytes) -> tuple[SecretKey, PublicKey]:
    """Make a key pair for digests of n bits."""
    sk = [[rand(VALUE_BYTES), rand(VALUE_BYTES)] for _ in range(n)]  # @line L1
    pk = [[h(x0), h(x1)] for x0, x1 in sk]  # @line L2
    return sk, pk  # @line L3


def sign(sk: SecretKey, message: bytes) -> Signature:
    """Reveal one secret value for each bit of the digest."""
    d = digest_bits(message, len(sk))  # @line L4
    return [sk[i][d[i]] for i in range(len(sk))]  # @line L5


def verify(pk: PublicKey, message: bytes, sig: Signature) -> bool:
    """Check that each revealed value hashes to the public value for its bit."""
    if len(sig) != len(pk) or any(len(s) != VALUE_BYTES for s in sig):  # @line L6
        return False
    d = digest_bits(message, len(pk))  # @line L7
    for i in range(len(pk)):  # @line L8
        if h(sig[i]) != pk[i][d[i]]:  # @line L9
            return False
    return True  # @line L10


def compress_public_key(pk: PublicKey) -> bytes:
    """One hash of the 2n public values, so that the public key is 32 bytes."""
    return h(b"".join(y0 + y1 for y0, y1 in pk))


class OneTimeSigner:
    """A signer that refuses to sign a second message with the same key."""

    def __init__(self, n: int = 256, rand: Callable[[int], bytes] = secrets.token_bytes) -> None:
        self._sk: SecretKey | None
        self._sk, self.pk = keygen(n, rand)

    def sign(self, message: bytes) -> Signature:
        if self._sk is None:
            raise RuntimeError("this one-time key has already signed a message")
        sig = sign(self._sk, message)
        self._sk = None  # forget the secret key after one use
        return sig
