# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hmqv/. The authors are listed in prov/294GKW.jsonl.
"""HMQV, the hashed MQV protocol of Krawczyk (CRYPTO 2005), two-message form.

Party A has (a, A = g^a) and ephemeral (x, X = g^x); party B has (b, B), (y, Y).

    d = Hbar(X, B_id), e = Hbar(Y, A_id)          (l = ceil(|q| / 2) bits)
    A: sigma = (Y * B^e)^(x + d*a)                B: sigma = (X * A^d)^(y + e*b)
    K = H(sigma)

The only change from MQV is that d and e are hashes of the ephemeral value
together with the identity of the peer, and the key is a hash of sigma.

The group is the subgroup of prime order q of Z_p^* for a 256-bit safe prime.
For study only. This code is not constant time, it branches on secret data,
and the parameters are toys. Use a vetted library for real key agreement,
for example the Noise or TLS 1.3 support of a maintained library.
"""

from __future__ import annotations

import hashlib
import secrets

P = 0xC00000000000000000000000000000000000000000000000000000000000A0EB
Q = (P - 1) // 2
G = 4
L = (Q.bit_length() + 1) // 2  # 128 bits


def lp(*parts: bytes) -> bytes:
    return b"".join(len(t).to_bytes(2, "big") + t for t in parts)


def hbar(r: int, ident: str) -> int:
    """Hbar(R, id): SHA-256 truncated to l bits."""
    return int.from_bytes(hashlib.sha256(lp(r.to_bytes(32, "big"), ident.encode())).digest(), "big") >> (256 - L)


def in_group(v: int) -> bool:
    return 1 < v < P and pow(v, Q, P) == 1


def keypair(rng=None) -> tuple[int, int]:
    k = (rng or secrets.SystemRandom()).randrange(1, Q)
    return k, pow(G, k, P)


def hmqv_sigma(me: str, peer: str, own_static: int, own_eph: int, peer_static_pub: int, peer_eph_pub: int) -> int | None:
    """sigma seen from party `me`: (Y * B^e)^(x + d*a) with d = Hbar(X, peer), e = Hbar(Y, me)."""
    own_eph_pub = pow(G, own_eph, P)  # @line L1
    if not (in_group(peer_eph_pub) and in_group(peer_static_pub)):  # @line L2
        return None
    d, e = hbar(own_eph_pub, peer), hbar(peer_eph_pub, me)  # @line L3
    s = (own_eph + d * own_static) % Q  # @line L4
    return pow(peer_eph_pub * pow(peer_static_pub, e, P) % P, s, P)  # @line L5


def hmqv_key(me: str, peer: str, own_static: int, own_eph: int, peer_static_pub: int, peer_eph_pub: int) -> bytes | None:
    sigma = hmqv_sigma(me, peer, own_static, own_eph, peer_static_pub, peer_eph_pub)
    if sigma is None:
        return None
    return hashlib.sha256(sigma.to_bytes(32, "big")).digest()  # @line L6
