# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mqv/. The authors are listed in prov/9AG3KC.jsonl.
"""The MQV key agreement (two-pass, full form) in a prime order subgroup of Z_p^*.

Each party has a static key pair (a, A = g^a) and makes an ephemeral pair
(x, X = g^x) for each session. With the "associate value function"
avf(R) = (R mod 2^w) + 2^w, w = ceil(bitlen(q) / 2), party A computes

    d = avf(X), e = avf(Y), s_A = x + d*a mod q, sigma = (Y * B^e)^(h * s_A),

and B computes sigma = (X * A^d)^(h * s_B) with s_B = y + e*b. Both get
g^(h * s_A * s_B). The cofactor h is 1 here because every received value is
checked to lie in the subgroup of order q; in a group with cofactor h > 1 and
only partial validation, the factor h kills small-order components.

The function kaliski_uks shows Kaliski's 2001 unknown key-share attack, which
works when the key derivation does not include the identities.

The group is the subgroup of prime order q of Z_p^* for a 256-bit safe prime.
For study only. This code is not constant time, it branches on secret data,
and the parameters are toys. Use a vetted library, such as an SP 800-56A
validated module, for real key agreement; prefer HMQV-style or signed
protocols for new designs.
"""

from __future__ import annotations

import hashlib
import secrets

P = 0xC00000000000000000000000000000000000000000000000000000000000A0EB
Q = (P - 1) // 2
G = 4
H = 1  # cofactor used in the exponent; 1 with full subgroup validation
W = (Q.bit_length() + 1) // 2


def avf(r: int, w: int = W) -> int:
    """Associate value function: the low w bits of r, with bit w set. Half the length of q."""
    return (r % (1 << w)) + (1 << w)


def in_group(v: int, p: int = P, q: int = Q) -> bool:
    return 1 < v < p and pow(v, q, p) == 1


def kdf(sigma: int, context: tuple[bytes, ...] = ()) -> bytes:
    """K = SHA-256(sigma || context). An empty context is K = KDF(sigma), the original MQV setting."""
    parts = (sigma.to_bytes(32, "big"),) + context
    return hashlib.sha256(b"".join(len(t).to_bytes(2, "big") + t for t in parts)).digest()


def keypair(rng=None) -> tuple[int, int]:
    k = (rng or secrets.SystemRandom()).randrange(1, Q)
    return k, pow(G, k, P)


def mqv_sigma(own_static: int, own_eph: int, own_eph_pub: int, peer_static_pub: int, peer_eph_pub: int, p: int = P, q: int = Q, w: int = W) -> int | None:
    """The shared value sigma, seen from one party. Cost: one full and one half-length exponentiation."""
    if not (in_group(peer_eph_pub, p, q) and in_group(peer_static_pub, p, q)):  # @line L2
        return None
    d, e = avf(own_eph_pub, w), avf(peer_eph_pub, w)  # @line L3
    s = (own_eph + d * own_static) % q  # @line L4
    sigma = pow(peer_eph_pub * pow(peer_static_pub, e, p) % p, H * s, p)  # @line L5
    if sigma == 1:  # @line L6
        return None
    return sigma


def mqv_key(me: str, peer: str, initiator: bool, own_static: int, own_eph: int, peer_static_pub: int, peer_eph_pub: int, bind: bool = True) -> bytes | None:
    """Full two-pass MQV for one party: sigma, then K = KDF(sigma, A, B, X, Y) with A the initiator.

    bind=False gives K = KDF(sigma) with no identities or transcript, as in the original protocol.
    """
    own_eph_pub = pow(G, own_eph, P)  # @line L1
    sigma = mqv_sigma(own_static, own_eph, own_eph_pub, peer_static_pub, peer_eph_pub)
    if sigma is None:
        return None
    if not bind:
        return kdf(sigma)
    a_id, b_id = (me, peer) if initiator else (peer, me)
    x_pub, y_pub = (own_eph_pub, peer_eph_pub) if initiator else (peer_eph_pub, own_eph_pub)
    return kdf(sigma, (a_id.encode(), b_id.encode(), x_pub.to_bytes(32, "big"), y_pub.to_bytes(32, "big")))  # @line L7


def kaliski_uks(a_static_pub: int, x_pub: int, rng) -> tuple[int, int, int]:
    """Kaliski (2001). Eve sees A's X, then makes a static key E and ephemeral X_E with X_E * E^avf(X_E) = X * A^avf(X).

    She picks u, sets X_E = X * A^avf(X) * g^(-u), then c = u / avf(X_E) mod q and E = g^c.
    She knows c, so she can register E with proof of possession. Returns (c, E, X_E).
    B, talking to "E" with X_E, computes the same sigma as A, talking to B with X.
    """
    target = x_pub * pow(a_static_pub, avf(x_pub), P) % P
    while True:
        u = rng.randrange(1, Q)
        x_e = target * pow(G, Q - u, P) % P
        if in_group(x_e):
            c = u * pow(avf(x_e), -1, Q) % Q
            return c, pow(G, c, P), x_e
