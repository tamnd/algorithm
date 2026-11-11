# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/otway-rees-protocol/. The authors are listed in prov/GDNTC9.jsonl.
"""The Otway-Rees protocol (1987), and the type flaw attack on it.

    1  A -> B : M, A, B, {Na, M, A, B}K_AS
    2  B -> S : M, A, B, {Na, M, A, B}K_AS, {Nb, M, A, B}K_BS
    3  S -> B : M, {Na, K}K_AS, {Nb, K}K_BS
    4  B -> A : M, {Na, K}K_AS

M is a run identifier, Na and Nb are nonces, K is the new session key.

With typed=False, plaintexts are plain concatenations and a party takes the
key to be "the bytes after the nonce". Then the reply {Na, M, A, B}K_AS of
message 1 also parses as {Na, K}K_AS with K = M | A | B, which is the type
flaw attack. With typed=True each field carries a type tag, and the attack fails.

Encryption is a toy encrypt-then-MAC (SHA-256 counter mode, HMAC tag).
For study only. This code is not constant time, and this protocol must not
be used. Use Kerberos (MIT Kerberos, Heimdal) or TLS 1.3.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets

_rng = secrets.SystemRandom()
NONCE, KEY, RUN = 16, 32, 16  # byte lengths; names are 8 bytes, so |M| + |A| + |B| = |K|


def _stream(key: bytes, iv: bytes, n: int) -> bytes:
    return b"".join(hashlib.sha256(key + iv + i.to_bytes(4, "big")).digest() for i in range(n // 32 + 1))[:n]


def enc(key: bytes, plain: bytes) -> bytes:
    iv = _rng.randbytes(16)
    ct = bytes(a ^ b for a, b in zip(plain, _stream(key, iv, len(plain))))
    return iv + ct + hmac.new(key, iv + ct, hashlib.sha256).digest()[:16]


def dec(key: bytes, box: bytes) -> bytes | None:
    iv, ct, tag = box[:16], box[16:-16], box[-16:]
    if len(box) < 32 or not hmac.compare_digest(hmac.new(key, iv + ct, hashlib.sha256).digest()[:16], tag):
        return None
    return bytes(a ^ b for a, b in zip(ct, _stream(key, iv, len(ct))))


def pack(typed: bool, *fields: tuple[str, bytes]) -> bytes:
    """Untyped: plain concatenation. Typed: each field as (type, length, value)."""
    if not typed:
        return b"".join(v for _, v in fields)
    return b"".join(t.encode()[:1] + len(v).to_bytes(2, "big") + v for t, v in fields)


def unpack_nonce_key(typed: bool, plain: bytes) -> tuple[bytes, bytes] | None:
    """Read {nonce, key}."""
    if not typed:
        return plain[:NONCE], plain[NONCE:]  # the key is whatever follows the nonce
    out, i = [], 0
    while i < len(plain):
        t, n = plain[i : i + 1], int.from_bytes(plain[i + 1 : i + 3], "big")
        out.append((t, plain[i + 3 : i + 3 + n]))
        i += 3 + n
    if [t for t, _ in out] != [b"n", b"k"]:
        return None
    return out[0][1], out[1][1]


def unpack_request(typed: bool, plain: bytes) -> tuple[bytes, bytes, bytes, bytes] | None:
    """Read {nonce, M, A, B}, as the server does."""
    if not typed:
        return plain[:NONCE], plain[NONCE : NONCE + RUN], plain[NONCE + RUN : NONCE + RUN + 8], plain[NONCE + RUN + 8 :]
    out, i = [], 0
    while i < len(plain):
        t, n = plain[i : i + 1], int.from_bytes(plain[i + 1 : i + 3], "big")
        out.append((t, plain[i + 3 : i + 3 + n]))
        i += 3 + n
    if [t for t, _ in out] != [b"n", b"m", b"i", b"i"]:
        return None
    return tuple(v for _, v in out)


class Party:
    def __init__(self, name: bytes, k_s: bytes, typed: bool):
        assert len(name) == 8
        self.name, self.k_s, self.typed = name, k_s, typed
        self.accepted: tuple[bytes, bytes] | None = None

    # A's role
    def message1(self, b: bytes):
        self.m, self.na, self.peer = _rng.randbytes(RUN), _rng.randbytes(NONCE), b
        box = enc(self.k_s, pack(self.typed, ("n", self.na), ("m", self.m), ("i", self.name), ("i", b)))
        return self.m, self.name, b, box  # @line L1

    def message4_received(self, msg4) -> bool:
        m, box = msg4
        plain = dec(self.k_s, box)
        got = None if plain is None or m != self.m else unpack_nonce_key(self.typed, plain)
        if got is None or got[0] != self.na:  # @line L5
            return False
        self.accepted = (self.peer, got[1])
        return True

    # B's role
    def message2(self, msg1):
        m, a, b, box_a = msg1
        self.m, self.peer, self.nb = m, a, _rng.randbytes(NONCE)
        box_b = enc(self.k_s, pack(self.typed, ("n", self.nb), ("m", m), ("i", a), ("i", b)))
        return m, a, b, box_a, box_b  # @line L2

    def message3_received(self, msg3):
        m, box_a, box_b = msg3
        plain = dec(self.k_s, box_b)
        got = None if plain is None or m != self.m else unpack_nonce_key(self.typed, plain)
        if got is None or got[0] != self.nb:  # @line L4
            return None
        self.accepted = (self.peer, got[1])
        return m, box_a


class Server:
    def __init__(self, keys: dict[bytes, bytes], typed: bool):
        self.keys, self.typed = keys, typed

    def message3(self, msg2):
        m, a, b, box_a, box_b = msg2
        pa = dec(self.keys[a], box_a) if a in self.keys else None
        pb = dec(self.keys[b], box_b) if b in self.keys else None
        ra = None if pa is None else unpack_request(self.typed, pa)
        rb = None if pb is None else unpack_request(self.typed, pb)
        if ra is None or rb is None or ra[1:] != (m, a, b) or rb[1:] != (m, a, b):  # @line L3
            return None
        k = _rng.randbytes(KEY)
        return m, enc(self.keys[a], pack(self.typed, ("n", ra[0]), ("k", k))), enc(self.keys[b], pack(self.typed, ("n", rb[0]), ("k", k)))


def type_flaw_attack(alice: Party, b: bytes) -> bytes | None:
    """Eve stops message 1 and sends its encrypted part straight back to A as message 4.

    Returns the key that Alice accepts, or None if she rejects it.
    """
    m, _, _, box = alice.message1(b)
    if alice.message4_received((m, box)):
        return alice.accepted[1]
    return None
