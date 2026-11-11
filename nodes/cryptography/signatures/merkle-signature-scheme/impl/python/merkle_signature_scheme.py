# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merkle-signature-scheme/. The authors are listed in prov/RTX97D.jsonl.
"""Merkle signature scheme (Merkle 1979, 1989) with Winternitz leaves.

A binary hash tree of height h has 2^h leaves. Leaf q is the hash of the
public key of one-time key number q. The public key is the root. A signature
is the leaf index q, the one-time signature, and the authentication path:
the h sibling nodes on the way from leaf q to the root.

The one-time scheme is classic Winternitz (w = 16, plain hash chains) with
the secret values made from one seed. The signer keeps the whole tree in
memory, which is fine for the small heights of the tests (h up to 6); real
signers use a traversal algorithm (Szydlo 2004, BDS 2008) instead.

The scheme is stateful: the signer must never use a leaf twice. The class
below raises an error when the leaves run out.

The page is about the signature, not the hash, so SHA-256 comes from hashlib.
For study only. The code is not constant time and it must not protect real
data. For real use take LMS or XMSS (NIST SP 800-208).
"""

import hashlib
import secrets
from dataclasses import dataclass

N = 32  # bytes of a hash value
W = 16  # Winternitz chain length
LEN1 = 64  # digits of a 256-bit digest, 4 bits each
LEN2 = 3  # digits of the checksum (at most 64 * 15 = 960 < 16^3)
LEN = LEN1 + LEN2


def H(tag: int, *parts: bytes) -> bytes:
    """SHA-256 with a one-byte domain tag."""
    return hashlib.sha256(bytes([tag]) + b"".join(parts)).digest()


# ------------------------------------------------------ Winternitz leaves


def wots_digits(message: bytes) -> list[int]:
    d = hashlib.sha256(message).digest()
    digits = []
    for byte in d:
        digits += [byte >> 4, byte & 15]
    c = sum(W - 1 - x for x in digits)
    return digits + [(c >> 8) & 15, (c >> 4) & 15, c & 15]


def wots_chain(x: bytes, start: int, steps: int) -> bytes:
    for _ in range(steps):
        x = H(0, x)
    return x


def wots_secret(seed: bytes, q: int, i: int) -> bytes:
    """Secret value i of one-time key q, from the seed by a PRF."""
    return H(1, seed, q.to_bytes(4, "big"), i.to_bytes(2, "big"))


def wots_sign(seed: bytes, q: int, message: bytes) -> list[bytes]:
    b = wots_digits(message)
    return [wots_chain(wots_secret(seed, q, i), 0, b[i]) for i in range(LEN)]


def wots_pk_from_sig(message: bytes, sig: list[bytes]) -> list[bytes]:
    b = wots_digits(message)
    return [wots_chain(sig[i], b[i], W - 1 - b[i]) for i in range(LEN)]


def leaf_from_wots_pk(ends: list[bytes]) -> bytes:
    """The leaf compresses the one-time public key to one hash value."""
    return H(2, *ends)


def wots_leaf(seed: bytes, q: int) -> bytes:
    ends = [wots_chain(wots_secret(seed, q, i), 0, W - 1) for i in range(LEN)]
    return leaf_from_wots_pk(ends)


def parent(left: bytes, right: bytes) -> bytes:
    return H(3, left, right)


# ------------------------------------------------------- the Merkle scheme


@dataclass
class Signature:
    q: int
    ots: list[bytes]
    auth: list[bytes]


class MerkleSigner:
    """A stateful signer for 2^h messages."""

    def __init__(self, h: int, seed: bytes | None = None) -> None:
        self.h = h
        self.seed = seed if seed is not None else secrets.token_bytes(N)  # @line L1
        level = [wots_leaf(self.seed, q) for q in range(1 << h)]  # @line L2
        self.tree = [level]
        for _ in range(h):  # @line L3
            level = [parent(level[2 * i], level[2 * i + 1]) for i in range(len(level) // 2)]
            self.tree.append(level)
        self.root = self.tree[h][0]  # @line L4
        self.next_q = 0

    def auth_path(self, q: int) -> list[bytes]:
        return [self.tree[j][(q >> j) ^ 1] for j in range(self.h)]

    def sign(self, message: bytes) -> Signature:
        q = self.next_q  # @line L5
        if q >= 1 << self.h:
            raise RuntimeError("all one-time keys are used")
        self.next_q = q + 1  # @line L6
        ots = wots_sign(self.seed, q, message)  # @line L7
        auth = self.auth_path(q)  # @line L8
        return Signature(q, ots, auth)  # @line L9


def verify(root: bytes, h: int, message: bytes, sig: Signature) -> bool:
    if not 0 <= sig.q < 1 << h or len(sig.auth) != h or len(sig.ots) != LEN:
        return False
    node = leaf_from_wots_pk(wots_pk_from_sig(message, sig.ots))  # @line L10
    for j in range(h):  # @line L11
        if (sig.q >> j) & 1 == 0:
            node = parent(node, sig.auth[j])
        else:
            node = parent(sig.auth[j], node)
    return node == root  # @line L12
