# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/authenticated-key-exchange/. The authors are listed in prov/NYN6YJ.jsonl.
"""A small signed Diffie-Hellman authenticated key exchange with a session state machine.

The protocol has the shape of the ISO/IEC 9798-3 signature-based exchange that
Krawczyk (CRYPTO 2003) discusses before SIGMA:

    m1  A -> B : A, X = g^x
    m2  B -> A : B, Y = g^y, SIG_B(X, Y, A)
    m3  A -> B : SIG_A(Y, X, B)
    K  = SHA-256("ake" || A || B || X || Y || g^(xy))

Each party runs a Session object. A session moves through the states
"start" -> "wait" -> "accepted" (or "rejected"). Its session id is the
tuple (A, B, X, Y). Two sessions are partners when they have the same
session id; partners must hold the same key.

The group is the subgroup of prime order q of Z_p^* for the safe prime
p = 2q + 1 below (256 binary digits), with g = 4. The signature is a
textbook Schnorr signature in the same group. Both are far too small and
too simple for real use.

For study only. This code is not constant time, it branches on secret
data, and it must not protect real data. Use TLS 1.3 or the Noise
framework through a vetted library (for example libsodium, or a FIPS 140
validated module) instead.
"""

from __future__ import annotations

import hashlib
import secrets

# p = 2q + 1, both prime. g = 4 is a square, so it generates the subgroup of order q.
P = 0xC00000000000000000000000000000000000000000000000000000000000A0EB
Q = (P - 1) // 2
G = 4
ELEM_LEN = 32


def enc(x: int) -> bytes:
    """Fixed-length big-endian encoding of a group element or scalar."""
    return x.to_bytes(ELEM_LEN, "big")


def is_group_element(x: int) -> bool:
    """True when x is in the subgroup of order q (public key validation)."""
    return 1 < x < P and pow(x, Q, P) == 1


def h_int(*parts: bytes) -> int:
    """SHA-256 of the length-prefixed parts, as an integer mod q."""
    h = hashlib.sha256()
    for part in parts:
        h.update(len(part).to_bytes(4, "big") + part)
    return int.from_bytes(h.digest(), "big") % Q


# ------------------------------------------------------------ Schnorr signature


def keygen(rng: secrets.SystemRandom | None = None) -> tuple[int, int]:
    """Return (secret key, public key) with a uniform secret in [1, q - 1]."""
    r = rng or secrets.SystemRandom()
    sk = r.randrange(1, Q)
    return sk, pow(G, sk, P)


def sign(sk: int, msg: bytes) -> tuple[int, int]:
    """Schnorr signature (e, s): k from a hash of the key and message, R = g^k, e = H(R, m), s = k + e*sk."""
    k = h_int(b"nonce", enc(sk), msg) or 1
    r_elem = pow(G, k, P)
    e = h_int(b"chal", enc(r_elem), msg)
    return e, (k + e * sk) % Q


def verify(pk: int, msg: bytes, sig: tuple[int, int]) -> bool:
    """Accept when e = H(g^s * pk^(-e), m)."""
    e, s = sig
    if not (0 <= e < Q and 0 <= s < Q and is_group_element(pk)):
        return False
    r_elem = pow(G, s, P) * pow(pk, Q - e, P) % P
    return h_int(b"chal", enc(r_elem), msg) == e


# ------------------------------------------------------------ the session state machine


def session_key(a: str, b: str, x_pub: int, y_pub: int, z: int) -> bytes:
    """K = SHA-256("ake" || A || B || X || Y || Z), A the initiator, B the responder."""
    return hashlib.sha256(b"ake" + a.encode() + b"|" + b.encode() + b"|" + enc(x_pub) + enc(y_pub) + enc(z)).digest()


class Session:
    """One run of the protocol at one party. Cost: two exponentiations for DH, one signature, one verification."""

    def __init__(self, me: str, sk: int, directory: dict[str, int], role: str, rng: secrets.SystemRandom | None = None):
        if role not in ("initiator", "responder"):
            raise ValueError("role is initiator or responder")
        self.me, self.sk, self.directory, self.role = me, sk, directory, role
        self.rng = rng or secrets.SystemRandom()
        self.state = "start"
        self.peer: str | None = None
        self.key: bytes | None = None
        self.sid: tuple | None = None
        self._x = 0
        self._x_pub = 0
        self._y_pub = 0

    def _reject(self) -> None:
        self.state, self.key, self._x = "rejected", None, 0

    def _accept(self, key: bytes, a: str, b: str) -> None:
        self.state, self.key = "accepted", key
        self.sid = (a, b, self._x_pub, self._y_pub)  # X is always the initiator's value
        self._x = 0  # erase the ephemeral exponent: needed for forward secrecy

    def start(self, peer: str) -> tuple:
        """Initiator: send m1 = (A, X)."""
        if self.role != "initiator" or self.state != "start":
            raise RuntimeError("start is only for a fresh initiator session")
        self.peer = peer
        self._x = self.rng.randrange(1, Q)
        self._x_pub = pow(G, self._x, P)
        self.state = "wait"
        return (self.me, self._x_pub)

    def respond(self, m1: tuple) -> tuple | None:
        """Responder: read m1, send m2 = (B, Y, SIG_B(X, Y, A))."""
        if self.role != "responder" or self.state != "start":
            raise RuntimeError("respond is only for a fresh responder session")
        a, x_pub = m1
        if a not in self.directory or not is_group_element(x_pub):
            self._reject()
            return None
        self.peer = a
        self._x = self.rng.randrange(1, Q)  # the responder's ephemeral exponent y
        self._y_pub = pow(G, self._x, P)
        self._x_pub = x_pub
        sig = sign(self.sk, b"m2" + enc(x_pub) + enc(self._y_pub) + a.encode())
        self.state = "wait"
        return (self.me, self._y_pub, sig)

    def finish(self, m2: tuple) -> tuple | None:
        """Initiator: check m2, send m3 = SIG_A(Y, X, B), and accept."""
        if self.role != "initiator" or self.state != "wait":
            raise RuntimeError("finish is only for a waiting initiator")
        b, y_pub, sig = m2
        if b != self.peer or not is_group_element(y_pub):
            self._reject()
            return None
        if not verify(self.directory[b], b"m2" + enc(self._x_pub) + enc(y_pub) + self.me.encode(), sig):
            self._reject()
            return None
        self._y_pub = y_pub
        z = pow(y_pub, self._x, P)
        m3 = (sign(self.sk, b"m3" + enc(y_pub) + enc(self._x_pub) + b.encode()),)
        self._accept(session_key(self.me, b, self._x_pub, y_pub, z), self.me, b)
        return m3

    def complete(self, m3: tuple) -> bool:
        """Responder: check m3 and accept."""
        if self.role != "responder" or self.state != "wait":
            raise RuntimeError("complete is only for a waiting responder")
        (sig,) = m3
        a = self.peer
        if not verify(self.directory[a], b"m3" + enc(self._y_pub) + enc(self._x_pub) + self.me.encode(), sig):
            self._reject()
            return False
        z = pow(self._x_pub, self._x, P)
        self._accept(session_key(a, self.me, self._x_pub, self._y_pub, z), a, self.me)
        return True


def run(a: Session, b: Session, peer_of_a: str) -> None:
    """Deliver the three messages between two honest sessions without change."""
    m1 = a.start(peer_of_a)
    m2 = b.respond(m1)
    if m2 is None:
        return
    m3 = a.finish(m2)
    if m3 is None:
        return
    b.complete(m3)


# ------------------------------------------------------------ the unauthenticated baseline


def plain_dh_key(x_pub: int, y_pub: int, z: int) -> bytes:
    """Plain DH with no authentication: K = SHA-256(X || Y || Z). Used to show what the Test game catches."""
    return hashlib.sha256(b"plain" + enc(x_pub) + enc(y_pub) + enc(z)).digest()
