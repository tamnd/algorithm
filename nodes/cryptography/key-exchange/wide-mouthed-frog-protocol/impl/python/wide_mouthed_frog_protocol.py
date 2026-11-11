# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wide-mouthed-frog-protocol/. The authors are listed in prov/CYAP9N.jsonl.
"""The wide-mouthed frog protocol (Burrows, Abadi and Needham, 1989), and the replay that keeps a key alive.

    1  A -> S : A, {Ta, B, K}K_AS
    2  S -> B : {Ts, A, K}K_BS

A makes the session key K. The server checks that Ta is recent, and passes
K on with its own timestamp Ts. B checks that Ts is recent.

Messages 1 and 2 have the same form. So message 2 can be sent back to S as a
message 1 from B, and S answers with a new timestamp. Repeating this keeps
a timestamp on K fresh for as long as the attacker likes (the "ding-dong"
attack in the survey of Clark and Jacob). With tagged=True each plaintext
says which message it is, and the attack fails.

Encryption is a toy encrypt-then-MAC (SHA-256 counter mode, HMAC tag).
Clocks are integers. For study only. This code is not constant time, and
this protocol must not be used. Use Kerberos (MIT Kerberos, Heimdal) or TLS 1.3.
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


def _body(tagged: bool, label: bytes, t: int, name: bytes, k: bytes) -> tuple[bytes, ...]:
    return ((label,) if tagged else ()) + (t8(t), name, k)


def _read(tagged: bool, label: bytes, plain: list[bytes] | None) -> tuple[int, bytes, bytes] | None:
    if plain is None:
        return None
    if tagged:
        if len(plain) != 4 or plain[0] != label:
            return None
        plain = plain[1:]
    if len(plain) != 3:
        return None
    return int.from_bytes(plain[0], "big"), plain[1], plain[2]


def message1(a: bytes, k_as: bytes, b: bytes, clock: int, tagged: bool = False) -> tuple[bytes, bytes, bytes]:
    """Returns (A, box, K)."""
    k = _rng.randbytes(32)
    return a, enc(k_as, *_body(tagged, b"msg1", clock, b, k)), k  # @line L1


class Server:
    def __init__(self, keys: dict[bytes, bytes], window: int, tagged: bool = False):
        self.keys, self.window, self.tagged = keys, window, tagged

    def forward(self, sender: bytes, box: bytes, clock: int) -> tuple[bytes, bytes] | None:
        """Message 1 in, message 2 out: returns (recipient, box)."""
        if sender not in self.keys:
            return None
        got = _read(self.tagged, b"msg1", dec(self.keys[sender], box))
        if got is None or abs(clock - got[0]) > self.window or got[1] not in self.keys:  # @line L2
            return None
        _, peer, k = got
        return peer, enc(self.keys[peer], *_body(self.tagged, b"msg2", clock, sender, k))


def receive(k_bs: bytes, box: bytes, clock: int, window: int, tagged: bool = False) -> tuple[bytes, bytes] | None:
    """B's check of message 2. Returns (peer, K) or None."""
    got = _read(tagged, b"msg2", dec(k_bs, box))
    if got is None or abs(clock - got[0]) > window:  # @line L3
        return None
    return got[1], got[2]


def ding_dong(server: Server, msg2_to_b: bytes, a: bytes, b: bytes, start: int, end: int, step: int) -> tuple[bytes, bytes] | None:
    """Eve bounces the last message 2 back to S, in alternate directions, every `step` seconds.

    Returns the last (recipient, box) she holds at time `end`, or None if S stops answering.
    """
    holder, box, t = b, msg2_to_b, start
    while t + step <= end:
        t += step
        out = server.forward(holder, box, t)  # present it as a message 1 from its recipient
        if out is None:
            return None
        holder, box = out
    return holder, box
