# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/station-to-station-protocol/. The authors are listed in prov/NT8D3J.jsonl.
"""The station-to-station (STS) protocol of Diffie, van Oorschot and Wiener (1992).

    m1  A -> B : A, X = g^x
    m2  B -> A : B, Y = g^y, E_K( SIG_B(Y, X) )
    m3  A -> B : E_K( SIG_A(X, Y) )
    K  = KDF(g^(xy))

SIG is a Schnorr signature in the same group. E_K is a toy stream cipher
(SHA-256 in counter mode, with a different nonce for m2 and m3, because both
use the same K). Encrypting the signatures under K gives key confirmation.

The group is the subgroup of prime order q of Z_p^* for a 256-bit safe prime
p = 2q + 1, with g = 4. For study only. This code is not constant time, it
branches on secret data, and the parameters are toys. It must not protect
real data. Use TLS 1.3 or IKEv2 (SIGMA-based) through a vetted library such
as OpenSSL or strongSwan, or a FIPS 140 validated module.

Cost per party: two exponentiations for DH, one for the subgroup check, one
for signing and two for verifying, so Theta(m^3) bit operations for m-bit p.
"""

from __future__ import annotations

import hashlib
import secrets

P = 0xC00000000000000000000000000000000000000000000000000000000000A0EB
Q = (P - 1) // 2
G = 4


def b32(x: int) -> bytes:
    return x.to_bytes(32, "big")


def in_group(v: int) -> bool:
    """Public value check: 1 < v < p and v^q = 1 (v lies in the subgroup of order q)."""
    return 1 < v < P and pow(v, Q, P) == 1


def h_int(*parts: bytes) -> int:
    return int.from_bytes(hashlib.sha256(b"".join(len(p).to_bytes(4, "big") + p for p in parts)).digest(), "big") % Q


def keygen(rng=None) -> tuple[int, int]:
    sk = (rng or secrets.SystemRandom()).randrange(1, Q)
    return sk, pow(G, sk, P)


def sign(sk: int, msg: bytes) -> bytes:
    """Schnorr: k = H(sk, m), R = g^k, e = H(R, m), s = k + e*sk mod q. Returns e || s (64 bytes)."""
    k = h_int(b"nonce", b32(sk), msg) or 1
    e = h_int(b"chal", b32(pow(G, k, P)), msg)
    return b32(e) + b32((k + e * sk) % Q)


def verify(pk: int, msg: bytes, sig: bytes) -> bool:
    if len(sig) != 64 or not in_group(pk):
        return False
    e, s = int.from_bytes(sig[:32], "big"), int.from_bytes(sig[32:], "big")
    if e >= Q or s >= Q:
        return False
    return h_int(b"chal", b32(pow(G, s, P) * pow(pk, Q - e, P) % P), msg) == e


def kdf(z: int) -> bytes:
    return hashlib.sha256(b"sts key" + b32(z)).digest()


def e_k(key: bytes, nonce: bytes, data: bytes) -> bytes:
    """Toy stream cipher: data XOR SHA-256(key || nonce || counter). Encryption and decryption are the same."""
    stream = b"".join(hashlib.sha256(key + nonce + i.to_bytes(4, "big")).digest() for i in range((len(data) + 31) // 32))
    return bytes(a ^ b for a, b in zip(data, stream))


class Initiator:
    def __init__(self, name: str, sk: int, directory: dict[str, int], rng=None):
        self.name, self.sk, self.directory = name, sk, directory
        self.rng = rng or secrets.SystemRandom()
        self.x = self.x_pub = 0

    def start(self) -> tuple[str, int]:
        self.x = self.rng.randrange(1, Q)  # @line L1
        self.x_pub = pow(G, self.x, P)
        return self.name, self.x_pub

    def finish(self, m2: tuple[str, int, bytes]) -> tuple[bytes, tuple[bytes, str]] | None:
        """Check m2; return (m3, (K, peer)) or None. Erases x."""
        peer, y_pub, c_b = m2
        if peer not in self.directory or not in_group(y_pub):  # @line L5
            return None
        key = kdf(pow(y_pub, self.x, P))
        self.x = 0  # erase the ephemeral exponent
        if not verify(self.directory[peer], b32(y_pub) + b32(self.x_pub), e_k(key, b"m2", c_b)):  # @line L6
            return None
        m3 = e_k(key, b"m3", sign(self.sk, b32(self.x_pub) + b32(y_pub)))  # @line L7
        return m3, (key, peer)


class Responder:
    def __init__(self, name: str, sk: int, directory: dict[str, int], rng=None):
        self.name, self.sk, self.directory = name, sk, directory
        self.rng = rng or secrets.SystemRandom()
        self.peer = ""
        self.x_pub = self.y_pub = 0
        self.key = b""

    def reply(self, m1: tuple[str, int]) -> tuple[str, int, bytes] | None:
        peer, x_pub = m1
        if peer not in self.directory or not in_group(x_pub):  # @line L2
            return None
        y = self.rng.randrange(1, Q)
        self.peer, self.x_pub, self.y_pub = peer, x_pub, pow(G, y, P)
        self.key = kdf(pow(x_pub, y, P))  # @line L3
        return self.name, self.y_pub, e_k(self.key, b"m2", sign(self.sk, b32(self.y_pub) + b32(x_pub)))  # @line L4

    def finish(self, m3: bytes, claimed_peer: str | None = None) -> tuple[bytes, str] | None:
        """Check m3. claimed_peer lets a test model a certificate swapped on the wire."""
        peer = claimed_peer or self.peer
        if peer not in self.directory:
            return None
        if not verify(self.directory[peer], b32(self.x_pub) + b32(self.y_pub), e_k(self.key, b"m3", m3)):  # @line L8
            return None
        return self.key, peer  # @line L9


def run(a: Initiator, b: Responder) -> tuple:
    """Honest delivery of m1, m2, m3. Returns (A's result, B's result)."""
    m2 = b.reply(a.start())
    if m2 is None:
        return None, None
    out = a.finish(m2)
    if out is None:
        return None, None
    m3, a_res = out
    return a_res, b.finish(m3)
