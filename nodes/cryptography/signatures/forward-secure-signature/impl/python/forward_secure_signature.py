# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-secure-signature/. The authors are listed in prov/CZN1Q6.jsonl.
"""A simple forward-secure signature built from Merkle trees and WOTS.

This is a small tree-based construction for study, in the spirit of the
generic tree schemes of Bellare and Miner (1999) and of forward-secure
XMSS (Buchmann, Dahmen and Hulsing, 2011). It is not one of their exact
schemes. There are T = 2**h periods. Period t has 2**b Winternitz one-time
keys made from a period seed s_t; the root of their tree is leaf t of the
top tree, whose root is the public key. The seeds form a one-way chain,
s_{t+1} = G(s_t), and the update deletes s_t. A key leaked in period t holds
s_t and public tree nodes only, so it cannot sign for an earlier period.

The class FixedSeedSigner shows the contrast: its period seeds all come from
one master seed (as in RFC 8391 key generation), so a leak gives every period.

For study only. The code is not constant time and it must not protect real
data. Python cannot really erase memory; deletion here is only modelled.
"""

import hashlib
import secrets
from dataclasses import dataclass

N = 32
W = 16
LEN1, LEN2 = 64, 3
LEN = LEN1 + LEN2


def H(tag: bytes, *parts: bytes) -> bytes:
    return hashlib.sha256(tag + b"".join(parts)).digest()


def u32(x: int) -> bytes:
    return x.to_bytes(4, "big")


def G(seed: bytes) -> bytes:
    """The one-way step of the seed chain."""
    return H(b"evolve", seed)


# --------------------------------------------- Winternitz one-time signature


def digits(d: bytes) -> list[int]:
    out = []
    for byte in d:
        out += [byte >> 4, byte & 15]
    c = sum(W - 1 - x for x in out)  # at most 960 < 16**3
    return out + [(c >> 8) & 15, (c >> 4) & 15, c & 15]


def step(x: bytes, t: int, j: int, i: int, k: int) -> bytes:
    return H(b"chain", u32(t), u32(j), u32(i), bytes([k]), x)


def chain(x: bytes, t: int, j: int, i: int, start: int, steps: int) -> bytes:
    for k in range(start, start + steps):
        x = step(x, t, j, i, k)
    return x


def ots_secret(seed: bytes, j: int, i: int) -> bytes:
    return H(b"secret", seed, u32(j), u32(i))


def ots_leaf(seed: bytes, t: int, j: int) -> bytes:
    ends = [chain(ots_secret(seed, j, i), t, j, i, 0, W - 1) for i in range(LEN)]
    return H(b"leaf", u32(t), u32(j), *ends)


def ots_sign(seed: bytes, t: int, j: int, d: bytes) -> list[bytes]:
    return [chain(ots_secret(seed, j, i), t, j, i, 0, b) for i, b in enumerate(digits(d))]


def ots_leaf_from_sig(sig: list[bytes], t: int, j: int, d: bytes) -> bytes:
    ends = [chain(sig[i], t, j, i, b, W - 1 - b) for i, b in enumerate(digits(d))]
    return H(b"leaf", u32(t), u32(j), *ends)


# ------------------------------------------------------------- Merkle trees


def node(tag: bytes, height: int, index: int, left: bytes, right: bytes) -> bytes:
    return H(b"node", tag, u32(height), u32(index), left, right)


def build(tag: bytes, leaves: list[bytes]) -> list[list[bytes]]:
    levels = [leaves]
    while len(levels[-1]) > 1:
        lv = levels[-1]
        h = len(levels) - 1
        levels.append([node(tag, h, k, lv[2 * k], lv[2 * k + 1]) for k in range(len(lv) // 2)])
    return levels


def path(levels: list[list[bytes]], q: int) -> list[bytes]:
    return [levels[k][(q >> k) ^ 1] for k in range(len(levels) - 1)]


def climb(tag: bytes, v: bytes, q: int, auth: list[bytes]) -> bytes:
    for k, sib in enumerate(auth):
        p = q >> (k + 1)
        v = node(tag, k, p, v, sib) if (q >> k) & 1 == 0 else node(tag, k, p, sib, v)
    return v


def period_tree(seed: bytes, t: int, b: int) -> list[list[bytes]]:
    return build(b"period" + u32(t), [ots_leaf(seed, t, j) for j in range(1 << b)])


# ------------------------------------------------------- the key-evolving scheme


@dataclass
class Signature:
    t: int
    j: int
    ots: list[bytes]
    inner: list[bytes]
    outer: list[bytes]


class ForwardSecureSigner:
    """Secret key of period t: (t, s_t, public tree nodes, counter j)."""

    def __init__(self, h: int, b: int, seed: bytes | None = None) -> None:
        self.h, self.b = h, b
        s0 = seed or secrets.token_bytes(N)  # @line L1
        s = s0
        roots = []
        for t in range(1 << h):
            roots.append(period_tree(s, t, b)[-1][0])  # @line L2
            s = G(s)  # the later seeds are dropped at once
        self.top = build(b"top", roots)  # @line L3
        self.public_key = self.top[-1][0]
        self.t = 0
        self._enter(s0)

    def _enter(self, s: bytes) -> None:
        self.seed: bytes | None = s
        self.inner = period_tree(s, self.t, self.b)
        self.j = 0

    def update(self) -> None:
        if self.t + 1 >= 1 << self.h:  # @line L4
            raise RuntimeError("the last period is over")
        nxt = G(self.seed)
        self.seed = None  # @line L5
        self.t += 1
        self._enter(nxt)

    def sign(self, message: bytes) -> Signature:
        if self.j >= 1 << self.b:  # @line L6
            raise RuntimeError("all keys of this period are used")
        j = self.j
        self.j += 1
        d = H(b"msg", message)
        ots = ots_sign(self.seed, self.t, j, d)  # @line L7
        return Signature(self.t, j, ots, path(self.inner, j), path(self.top, self.t))  # @line L8

    def leak(self) -> tuple[int, bytes, list[list[bytes]]]:
        """What an attacker gets if it breaks in now: the whole secret key."""
        return self.t, self.seed, self.top


def verify(pk: bytes, h: int, b: int, message: bytes, sig: Signature) -> bool:
    if not (0 <= sig.t < 1 << h and 0 <= sig.j < 1 << b):
        return False
    if len(sig.ots) != LEN or len(sig.inner) != b or len(sig.outer) != h:
        return False
    v = ots_leaf_from_sig(sig.ots, sig.t, sig.j, H(b"msg", message))
    v = climb(b"period" + u32(sig.t), v, sig.j, sig.inner)  # @line L9
    return climb(b"top", v, sig.t, sig.outer) == pk  # @line L10


def sign_with_leak(leak: tuple[int, bytes, list[list[bytes]]], t: int, b: int, j: int, message: bytes) -> Signature:
    """An attacker signs for period t with a leaked key of period t0 <= t.

    It moves the seed forward with G. For t < t0 it would need to invert G.
    """
    t0, s, top = leak
    if t < t0:
        raise ValueError("an earlier period needs a preimage of G")
    for _ in range(t - t0):
        s = G(s)
    inner = period_tree(s, t, b)
    return Signature(t, j, ots_sign(s, t, j, H(b"msg", message)), path(inner, j), path(top, t))


class FixedSeedSigner(ForwardSecureSigner):
    """NOT forward secure: s_t = H(master, t), and the key keeps the master."""

    def __init__(self, h: int, b: int, master: bytes) -> None:
        self.master = master
        self.h, self.b = h, b
        roots = [period_tree(self.seed_of(t), t, b)[-1][0] for t in range(1 << h)]
        self.top = build(b"top", roots)
        self.public_key = self.top[-1][0]
        self.t = 0
        self._enter(self.seed_of(0))

    def seed_of(self, t: int) -> bytes:
        return H(b"fixed", self.master, u32(t))

    def update(self) -> None:
        if self.t + 1 >= 1 << self.h:
            raise RuntimeError("the last period is over")
        self.t += 1
        self._enter(self.seed_of(self.t))
