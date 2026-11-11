# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/needham-schroeder-protocol/. The authors are listed in prov/9NTM5E.jsonl.
"""The Needham-Schroeder protocols (1978), with the attacks on them and the fixes.

Shared-key protocol (NSSK), with a server S that shares K_AS with A and K_BS with B:

    1  A -> S : A, B, Na
    2  S -> A : {Na, B, K, {K, A}K_BS}K_AS
    3  A -> B : {K, A}K_BS
    4  B -> A : {Nb}K
    5  A -> B : {Nb - 1}K

Public-key protocol (NSPK), core three messages, and Lowe's fix (NSL):

    1  A -> B : {Na, A}pk_B
    2  B -> A : {Na, Nb}pk_A          NSL: {Na, Nb, B}pk_A
    3  A -> B : {Nb}pk_B

Symmetric encryption is a toy encrypt-then-MAC (SHA-256 counter mode with an
HMAC-SHA-256 tag). Public-key encryption is modelled symbolically, as in the
Dolev-Yao model: a box addressed to a name can be opened only by the party
with that name. The attacks are protocol-level and need no broken cipher.

For study only. This code is not constant time, and these protocols, in this
form, must not be used. Use Kerberos (MIT Kerberos, Heimdal) or TLS 1.3.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets

_rng = secrets.SystemRandom()


def lp(*parts: bytes) -> bytes:
    return b"".join(len(t).to_bytes(2, "big") + t for t in parts)


def unlp(data: bytes) -> list[bytes]:
    out, i = [], 0
    while i < len(data):
        n = int.from_bytes(data[i : i + 2], "big")
        out.append(data[i + 2 : i + 2 + n])
        i += 2 + n
    return out


def _stream(key: bytes, iv: bytes, n: int) -> bytes:
    return b"".join(hashlib.sha256(key + iv + i.to_bytes(4, "big")).digest() for i in range(n // 32 + 1))[:n]


def enc(key: bytes, *parts: bytes) -> bytes:
    """{parts}key: authenticated encryption (toy)."""
    iv = _rng.randbytes(16)
    plain = lp(*parts)
    ct = bytes(a ^ b for a, b in zip(plain, _stream(key, iv, len(plain))))
    return iv + ct + hmac.new(key, iv + ct, hashlib.sha256).digest()[:16]


def dec(key: bytes, box: bytes) -> list[bytes] | None:
    iv, ct, tag = box[:16], box[16:-16], box[-16:]
    if len(box) < 32 or not hmac.compare_digest(hmac.new(key, iv + ct, hashlib.sha256).digest()[:16], tag):
        return None
    return unlp(bytes(a ^ b for a, b in zip(ct, _stream(key, iv, len(ct)))))


def minus_one(n: bytes) -> bytes:
    return ((int.from_bytes(n, "big") - 1) % (1 << 128)).to_bytes(16, "big")


# ---------------------------------------------------------------- NSSK


class Server:
    def __init__(self, keys: dict[bytes, bytes]):
        self.keys = keys  # long-term keys K_XS

    def handle(self, a: bytes, b: bytes, na: bytes, nb_fix: bytes | None = None) -> bytes | None:
        if a not in self.keys or b not in self.keys:
            return None
        k = _rng.randbytes(32)
        ticket = enc(self.keys[b], k, a) if nb_fix is None else enc(self.keys[b], k, a, nb_fix)
        return enc(self.keys[a], na, b, k, ticket)  # @line L2


class Initiator:
    def __init__(self, name: bytes, k_as: bytes):
        self.name, self.k_as, self.key = name, k_as, None

    def request(self, b: bytes) -> tuple[bytes, bytes, bytes]:
        self.peer, self.na = b, _rng.randbytes(16)
        return self.name, b, self.na  # @line L1

    def receive(self, msg2: bytes) -> bytes | None:
        parts = dec(self.k_as, msg2)
        if parts is None or parts[0] != self.na or parts[1] != self.peer:  # @line L3
            return None
        self.key = parts[2]
        return parts[3]  # the ticket, forwarded to B

    def answer(self, msg4: bytes) -> bytes | None:
        parts = dec(self.key, msg4)
        if parts is None:
            return None
        return enc(self.key, minus_one(parts[0]))  # @line L5


class Responder:
    """B. With fixed=True, B first gives A a nonce Nb' that the server puts into the ticket (1987 fix)."""

    def __init__(self, name: bytes, k_bs: bytes, fixed: bool = False):
        self.name, self.k_bs, self.fixed = name, k_bs, fixed
        self.accepted: tuple[bytes, bytes] | None = None
        self.nb_fix = None

    def hello(self) -> bytes:
        self.nb_fix = _rng.randbytes(16)
        return self.nb_fix

    def ticket(self, ticket: bytes) -> bytes | None:
        parts = dec(self.k_bs, ticket)
        if parts is None:
            return None
        if self.fixed and (len(parts) != 3 or self.nb_fix is None or parts[2] != self.nb_fix):
            return None
        self.key, self.peer = parts[0], parts[1]
        self.nb = _rng.randbytes(16)
        return enc(self.key, self.nb)  # @line L4

    def confirm(self, msg5: bytes) -> bool:
        parts = dec(self.key, msg5)
        if parts is None or parts[0] != minus_one(self.nb):  # @line L6
            return False
        self.accepted = (self.peer, self.key)
        return True


def run_nssk(server: Server, a: Initiator, b: Responder) -> bool:
    nb_fix = b.hello() if b.fixed else None
    msg2 = server.handle(*a.request(b.name), nb_fix=nb_fix)
    ticket = a.receive(msg2)
    msg4 = b.ticket(ticket)
    return msg4 is not None and b.confirm(a.answer(msg4))


def denning_sacco_replay(b: Responder, old_ticket: bytes, old_key: bytes) -> bool:
    """Eve replays an old ticket {K, A}K_BS whose session key K she has learned."""
    if b.fixed:
        b.hello()  # B makes a fresh Nb' that the old ticket does not contain
    msg4 = b.ticket(old_ticket)
    if msg4 is None:
        return False
    nb = dec(old_key, msg4)[0]
    return b.confirm(enc(old_key, minus_one(nb)))


# ---------------------------------------------------------------- NSPK and NSL (symbolic public-key encryption)


def pk_enc(recipient: bytes, *parts: bytes) -> tuple[bytes, bytes]:
    return (recipient, lp(*parts))


def pk_dec(me: bytes, box: tuple[bytes, bytes]) -> list[bytes] | None:
    return unlp(box[1]) if box[0] == me else None


class PkParty:
    def __init__(self, name: bytes, lowe_fix: bool = False):
        self.name, self.lowe_fix = name, lowe_fix
        self.done: tuple[bytes, bytes, bytes] | None = None  # (peer, Na, Nb)

    # initiator role
    def start(self, peer: bytes):
        self.peer, self.na = peer, _rng.randbytes(16)
        return pk_enc(peer, self.na, self.name)

    def step3(self, msg2):
        parts = pk_dec(self.name, msg2)
        if parts is None or parts[0] != self.na:
            return None
        if self.lowe_fix and (len(parts) != 3 or parts[2] != self.peer):
            return None  # the responder named in message 2 is not the intended peer
        self.done = (self.peer, self.na, parts[1])
        return pk_enc(self.peer, parts[1])

    # responder role
    def step2(self, msg1):
        parts = pk_dec(self.name, msg1)
        if parts is None:
            return None
        self.na, self.peer, self.nb = parts[0], parts[1], _rng.randbytes(16)
        extra = (self.name,) if self.lowe_fix else ()
        return pk_enc(self.peer, self.na, self.nb, *extra)

    def finish(self, msg3) -> bool:
        parts = pk_dec(self.name, msg3)
        if parts is None or parts[0] != self.nb:
            return False
        self.done = (self.peer, self.na, self.nb)
        return True


def lowe_attack(alice: PkParty, bob: PkParty) -> tuple[bool, set[bytes]]:
    """Alice starts a run with Eve. Eve uses it to pose as Alice to Bob.

    Returns (Bob accepts Alice as peer, the nonces that Eve has learned).
    """
    eve = b"E"
    m1 = alice.start(eve)
    na, a = pk_dec(eve, m1)
    m2 = bob.step2(pk_enc(bob.name, na, a))  # Eve re-encrypts message 1 for Bob
    m3 = alice.step3(m2)  # Eve forwards Bob's reply to Alice unchanged
    if m3 is None:
        return False, {na}
    nb = pk_dec(eve, m3)[0]  # Alice encrypts Nb for Eve
    ok = bob.finish(pk_enc(bob.name, nb))
    return ok and bob.done[0] == alice.name, {na, nb}
