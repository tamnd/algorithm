# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yahalom-protocol/. The authors are listed in prov/00SN4E.jsonl.
"""The Yahalom protocol, as given by Burrows, Abadi and Needham (1989).

    1  A -> B : A, Na
    2  B -> S : B, {A, Na, Nb}K_BS
    3  S -> A : {B, K, Na, Nb}K_AS, {A, K}K_BS
    4  A -> B : {A, K}K_BS, {Nb}K

B's nonce Nb never travels in clear. B learns that K is fresh only because Nb
comes back under K, so the protocol depends on the secrecy of Nb, which in
turn depends on the secrecy of K (Paulson's "relations between secrets").

Encryption is a toy encrypt-then-MAC (SHA-256 counter mode, HMAC tag).
For study only. This code is not constant time, and this protocol must not
be used as it is. Use Kerberos (MIT Kerberos, Heimdal) or TLS 1.3.
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
    iv = _rng.randbytes(16)
    plain = lp(*parts)
    ct = bytes(a ^ b for a, b in zip(plain, _stream(key, iv, len(plain))))
    return iv + ct + hmac.new(key, iv + ct, hashlib.sha256).digest()[:16]


def dec(key: bytes, box: bytes) -> list[bytes] | None:
    iv, ct, tag = box[:16], box[16:-16], box[-16:]
    if len(box) < 32 or not hmac.compare_digest(hmac.new(key, iv + ct, hashlib.sha256).digest()[:16], tag):
        return None
    return unlp(bytes(a ^ b for a, b in zip(ct, _stream(key, iv, len(ct)))))


class Initiator:
    def __init__(self, name: bytes, k_as: bytes):
        self.name, self.k_as, self.accepted = name, k_as, None

    def message1(self, peer: bytes) -> tuple[bytes, bytes]:
        self.peer, self.na = peer, _rng.randbytes(16)
        return self.name, self.na  # @line L1

    def message4(self, msg3: tuple[bytes, bytes]) -> tuple[bytes, bytes] | None:
        part, ticket = msg3
        p = dec(self.k_as, part)
        if p is None or len(p) != 4 or p[0] != self.peer or p[2] != self.na:  # @line L4
            return None
        k, nb = p[1], p[3]
        self.accepted = (self.peer, k)
        return ticket, enc(k, nb)


class Responder:
    def __init__(self, name: bytes, k_bs: bytes):
        self.name, self.k_bs, self.accepted = name, k_bs, None

    def message2(self, msg1: tuple[bytes, bytes]) -> tuple[bytes, bytes]:
        a, na = msg1
        self.peer, self.nb = a, _rng.randbytes(16)
        return self.name, enc(self.k_bs, a, na, self.nb)  # @line L2

    def finish(self, msg4: tuple[bytes, bytes]) -> bool:
        ticket, proof = msg4
        t = dec(self.k_bs, ticket)
        if t is None or len(t) != 2 or t[0] != self.peer:
            return False
        p = dec(t[1], proof)
        if p is None or p != [self.nb]:  # @line L5
            return False
        self.accepted = (t[0], t[1])
        return True


class Server:
    def __init__(self, keys: dict[bytes, bytes]):
        self.keys = keys

    def message3(self, msg2: tuple[bytes, bytes]) -> tuple[bytes, bytes] | None:
        b, box = msg2
        p = dec(self.keys[b], box) if b in self.keys else None
        if p is None or len(p) != 3 or p[0] not in self.keys:
            return None
        a, na, nb = p
        k = _rng.randbytes(32)
        return enc(self.keys[a], b, k, na, nb), enc(self.keys[b], a, k)  # @line L3


def run(a: Initiator, b: Responder, s: Server) -> bool:
    msg3 = s.message3(b.message2(a.message1(b.name)))
    msg4 = a.message4(msg3) if msg3 else None
    return msg4 is not None and b.finish(msg4)
