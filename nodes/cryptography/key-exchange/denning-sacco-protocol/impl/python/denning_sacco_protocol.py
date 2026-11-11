# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/denning-sacco-protocol/. The authors are listed in prov/X3KF0J.jsonl.
"""The two Denning-Sacco protocols (1981), and Abadi's attack on the public-key one.

Shared-key protocol, with a server S and timestamps T:

    1  A -> S : A, B
    2  S -> A : {B, K, T, {A, K, T}K_BS}K_AS
    3  A -> B : {A, K, T}K_BS
    A and B accept only if |clock - T| <= d1 + d2.

Public-key protocol, with certificates C_X = Sig_S(X, pk_X, T) from S:

    1  A -> S : A, B
    2  S -> A : C_A, C_B
    3  A -> B : C_A, C_B, {Sig_A(K, T_A)}pk_B
    fixed (Abadi and Needham):  {Sig_A(A, B, K, T_A)}pk_B

Symmetric encryption is a toy encrypt-then-MAC. Signatures and public-key
encryption are modelled symbolically (Dolev-Yao): only the named signer makes
a signature, and only the named recipient opens a box. Clocks are integers.

For study only. This code is not constant time, and these protocols must not
be used as they are. Use Kerberos (MIT Kerberos, Heimdal) or TLS 1.3.
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


def t8(t: int) -> bytes:
    return t.to_bytes(8, "big")


# ---------------------------------------------------------------- shared-key protocol


def server_reply(keys: dict[bytes, bytes], a: bytes, b: bytes, clock: int) -> bytes:
    k = _rng.randbytes(32)
    ticket = enc(keys[b], a, k, t8(clock))
    return enc(keys[a], b, k, t8(clock), ticket)  # @line L2


def request(a: bytes, b: bytes) -> tuple[bytes, bytes]:
    return a, b  # @line L1


def initiator_receive(k_as: bytes, peer: bytes, msg2: bytes, clock: int, window: int) -> tuple[bytes, bytes] | None:
    """A's check. Returns (K, ticket) or None."""
    parts = dec(k_as, msg2)
    if parts is None or parts[0] != peer or abs(clock - int.from_bytes(parts[2], "big")) > window:  # @line L3
        return None
    return parts[1], parts[3]


def responder_receive(k_bs: bytes, ticket: bytes, clock: int, window: int) -> tuple[bytes, bytes] | None:
    """B's check. Returns (peer, K) or None."""
    parts = dec(k_bs, ticket)
    if parts is None or abs(clock - int.from_bytes(parts[2], "big")) > window:  # @line L4
        return None
    return parts[0], parts[1]


# ---------------------------------------------------------------- public-key protocol (symbolic)


def sig(signer: bytes, *parts: bytes) -> tuple[bytes, bytes]:
    """Sig_signer(parts); in this model only the code of `signer` calls it."""
    return (signer, lp(*parts))


def pk_enc(recipient: bytes, payload) -> tuple[bytes, object]:
    return (recipient, payload)


def pk_dec(me: bytes, box) -> object | None:
    return box[1] if box[0] == me else None


def cert(name: bytes, t: int):
    return sig(b"S", name, b"pk_" + name, t8(t))


def pk_message3(a: bytes, b: bytes, k: bytes, t_a: int, fixed: bool):
    body = sig(a, a, b, k, t8(t_a)) if fixed else sig(a, k, t8(t_a))
    return cert(a, t_a), cert(b, t_a), pk_enc(b, body)


def pk_receive(me: bytes, msg3, clock: int, window: int, fixed: bool) -> tuple[bytes, bytes] | None:
    """The receiver's check. Returns (peer, K) or None."""
    c_a, c_me, box = msg3
    signed = pk_dec(me, box)
    if signed is None or c_a[0] != b"S" or c_me[0] != b"S" or unlp(c_me[1])[0] != me:
        return None
    peer = unlp(c_a[1])[0]
    if signed[0] != peer:  # the signature must be by the party in C_A
        return None
    parts = unlp(signed[1])
    if fixed:
        if parts[0] != peer or parts[1] != me:
            return None
        parts = parts[2:]
    k, t_a = parts
    if abs(clock - int.from_bytes(t_a, "big")) > window:
        return None
    return peer, k


def abadi_attack(msg3_to_b, b: bytes, c: bytes, t: int):
    """B, dishonest, opens A's message and re-encrypts A's signature for C (Abadi and Needham)."""
    c_a, _, box = msg3_to_b
    signed = pk_dec(b, box)
    return c_a, cert(c, t), pk_enc(c, signed)
