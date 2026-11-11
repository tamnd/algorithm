# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unknown-key-share-attack/. The authors are listed in prov/BECMKR.jsonl.
"""An unknown key-share (UKS) attack on a "sign only" Diffie-Hellman exchange, and three fixes.

The weak protocol (signed DH with no identities in the signed data or the key):

    m1  A -> B : X = g^x
    m2  B -> A : B, Y = g^y, SIG_B(Y, X)
    m3  A -> B : A, SIG_A(X, Y)
    K  = H(g^(xy))

Eve registers Alice's public key under the name "E" at a CA that does not ask
for proof of possession. She lets m1 and m2 pass, and in m3 she replaces the
name A by E. Bob checks SIG_A(X, Y) under E's public key, which is Alice's
key, so it verifies. Bob now believes he shares K with Eve; Alice believes she
shares K with Bob. Eve does not know K. That is a UKS.

Fixes shown in the tests:
  1. the CA checks proof of possession of the private key;
  2. the identities are in the key derivation, K = H(g^(xy), A, B);
  3. SIGMA style: each side sends MAC_Km(own identity) under a MAC key from g^(xy).

The group is the subgroup of prime order q of Z_p^* for a 256-bit safe prime.
For study only. This code is not constant time, it runs the attack only
against local simulated parties, and it must not protect real data. Use a
vetted library or a FIPS 140 validated module.
"""

from __future__ import annotations

import hashlib
import hmac

P = 0xC00000000000000000000000000000000000000000000000000000000000A0EB
Q = (P - 1) // 2
G = 4


def b32(x: int) -> bytes:
    return x.to_bytes(32, "big")


def h(*parts: bytes) -> bytes:
    return hashlib.sha256(b"".join(len(p).to_bytes(4, "big") + p for p in parts)).digest()


def sign(sk: int, msg: bytes) -> tuple[int, int]:
    k = int.from_bytes(h(b"k", b32(sk), msg), "big") % Q or 1
    e = int.from_bytes(h(b32(pow(G, k, P)), msg), "big") % Q
    return e, (k + e * sk) % Q


def verify(pk: int, msg: bytes, sig: tuple[int, int]) -> bool:
    e, s = sig
    if not (0 <= e < Q and 0 <= s < Q):
        return False
    r = pow(G, s, P) * pow(pk, Q - e, P) % P
    return int.from_bytes(h(b32(r), msg), "big") % Q == e


class CA:
    """A directory of name -> public key. With check_pop, a key needs a signature by its owner on the name."""

    def __init__(self, check_pop: bool):
        self.check_pop = check_pop
        self.keys: dict[str, int] = {}

    def register(self, name: str, pk: int, pop: tuple[int, int] | None = None) -> bool:
        if name in self.keys:
            return False
        if self.check_pop and (pop is None or not verify(pk, b"pop" + name.encode(), pop)):
            return False
        self.keys[name] = pk
        return True


def derive(z: int, a: str, b: str, ids_in_kdf: bool) -> tuple[bytes, bytes]:
    """Return (session key K, MAC key Km). Km is used only by the SIGMA-style fix."""
    ctx = (a.encode(), b.encode()) if ids_in_kdf else ()
    return h(b"K", b32(z), *ctx), h(b"Km", b32(z))


def run(ca: CA, keys: dict[str, int], x: int, y: int, *, attack: bool, ids_in_kdf: bool = False, mac_identity: bool = False):
    """Alice starts a session with Bob. Returns (Alice's view, Bob's view); a view is (peer, K) or None.

    With attack=True, Eve replaces the name in m3 (and in the KDF view of Bob) by "E".
    Cost: four exponentiations, two signatures, two verifications per run.
    """
    x_pub, y_pub = pow(G, x, P), pow(G, y, P)
    z = pow(y_pub, x, P)
    # m2 (Bob -> Alice), passed unchanged
    sig_b = sign(keys["B"], b32(y_pub) + b32(x_pub))
    if not verify(ca.keys["B"], b32(y_pub) + b32(x_pub), sig_b):
        return None, None
    k_a, km_a = derive(z, "A", "B", ids_in_kdf)
    alice = ("B", k_a)
    # m3 (Alice -> Bob)
    m3 = {"id": "A", "sig": sign(keys["A"], b32(x_pub) + b32(y_pub))}
    if mac_identity:
        m3["mac"] = hmac.new(km_a, b"A", hashlib.sha256).digest()
    if attack:
        m3["id"] = "E"  # Eve cannot change the signature or the MAC, only the claimed name
    peer = m3["id"]
    if peer not in ca.keys or not verify(ca.keys[peer], b32(x_pub) + b32(y_pub), m3["sig"]):
        return alice, None
    k_b, km_b = derive(pow(x_pub, y, P), peer, "B", ids_in_kdf)
    if mac_identity and not hmac.compare_digest(m3["mac"], hmac.new(km_b, peer.encode(), hashlib.sha256).digest()):
        return alice, None
    return alice, (peer, k_b)


def is_uks(alice, bob) -> bool:
    """Both accepted with the same key, but Bob names a peer that is not Alice."""
    return alice is not None and bob is not None and alice[1] == bob[1] and alice[0] == "B" and bob[0] != "A"
