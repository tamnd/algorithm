# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/winternitz-one-time-signature/. The authors are listed in prov/39CCX3.jsonl.
"""Winternitz one-time signature: classic WOTS and WOTS+ (Hulsing 2013).

w is the length parameter of RFC 8391 and FIPS 205: each chain has w values
c^0 .. c^(w-1), and each digit has lg w bits. The message digest has m bytes,
so it gives len1 = ceil(8m / lg w) digits, and the checksum gives len2 more.

Classic WOTS (Merkle 1989, after Winternitz) walks a chain with a plain hash,
c^j = H(c^(j-1)). WOTS+ walks it with a keyed function and a bitmask per step,
c^j = F_k(c^(j-1) XOR r_j), and puts k and the bitmasks r_1 .. r_(w-1) in the
public key, as in the 2013 paper. Standards (RFC 8391, FIPS 205) derive k and
the bitmasks from a public seed and an address; see the XMSS page.

The page is about the signature, not the hash, so SHA-256 comes from hashlib.

For study only. The code is not constant time and it must not protect real
data. A WOTS key must sign only one message.
"""

import hashlib
import secrets
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Params:
    n: int = 32  # bytes of a chain value and of a secret value
    w: int = 16  # chain length; a power of two from 4 to 256
    m: int = 32  # bytes of the message digest
    plus: bool = True  # WOTS+ (keyed function and bitmasks) or classic WOTS

    @property
    def lg_w(self) -> int:
        return self.w.bit_length() - 1

    @property
    def len1(self) -> int:
        return -(-8 * self.m // self.lg_w)

    @property
    def len2(self) -> int:
        # number of base-w digits of the largest checksum len1 * (w - 1)
        top, k = self.len1 * (self.w - 1), 0
        while top > 0:
            top //= self.w
            k += 1
        return k

    @property
    def length(self) -> int:
        return self.len1 + self.len2


@dataclass(frozen=True)
class PublicKey:
    ends: list[bytes]  # c^(w-1) of each chain
    k: bytes  # function key (WOTS+ only)
    masks: list[bytes]  # r_1 .. r_(w-1) (WOTS+ only)


def message_digest(p: Params, message: bytes) -> bytes:
    return hashlib.sha256(message).digest()[: p.m]


def base_w(data: bytes, w: int, count: int) -> list[int]:
    """The first count digits of data in base w, most significant first."""
    lg_w = w.bit_length() - 1
    value, nbits = int.from_bytes(data, "big"), 8 * len(data)
    return [(value >> (nbits - lg_w * (i + 1))) & (w - 1) for i in range(count)]


def checksum_digits(p: Params, digits: list[int]) -> list[int]:
    c = sum(p.w - 1 - d for d in digits)
    return [(c // p.w ** (p.len2 - 1 - i)) % p.w for i in range(p.len2)]


def digits(p: Params, message: bytes) -> list[int]:
    d = base_w(message_digest(p, message), p.w, p.len1)  # @line L1
    c = checksum_digits(p, d)  # @line L2
    return d + c  # @line L3


def f(p: Params, k: bytes, x: bytes) -> bytes:
    if p.plus:
        return hashlib.sha256(b"\x00" + k + x).digest()[: p.n]  # F_k(x)
    return hashlib.sha256(x).digest()[: p.n]  # H(x)


def chain(p: Params, pk: PublicKey | None, x: bytes, start: int, steps: int, k: bytes = b"", masks: list[bytes] | None = None) -> bytes:
    """Walk steps steps up a chain from position start."""
    if pk is not None:
        k, masks = pk.k, pk.masks
    for j in range(start, start + steps):  # @line L4
        if p.plus:
            x = bytes(a ^ b for a, b in zip(x, masks[j]))  # r_(j+1), 0-based
        x = f(p, k, x)
    return x  # @line L5


def keygen(p: Params = Params(), rand: Callable[[int], bytes] = secrets.token_bytes) -> tuple[list[bytes], PublicKey]:
    sk = [rand(p.n) for _ in range(p.length)]  # @line L6
    k, masks = b"", []
    if p.plus:
        k, masks = rand(p.n), [rand(p.n) for _ in range(p.w - 1)]  # @line L7
    ends = [chain(p, None, x, 0, p.w - 1, k, masks) for x in sk]  # @line L8
    return sk, PublicKey(ends, k, masks)  # @line L9


def sign(p: Params, sk: list[bytes], pk: PublicKey, message: bytes) -> list[bytes]:
    b = digits(p, message)  # @line L10
    return [chain(p, pk, sk[i], 0, b[i]) for i in range(p.length)]  # @line L11


def public_key_from_signature(p: Params, pk: PublicKey, message: bytes, sig: list[bytes]) -> list[bytes]:
    """Complete each chain from the signed position to the end."""
    b = digits(p, message)  # @line L12
    return [chain(p, pk, sig[i], b[i], p.w - 1 - b[i]) for i in range(p.length)]


def verify(p: Params, pk: PublicKey, message: bytes, sig: list[bytes]) -> bool:
    if len(sig) != p.length or any(len(s) != p.n for s in sig):
        return False
    return public_key_from_signature(p, pk, message, sig) == pk.ends  # @line L13
