# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deterministic-nonce-generation/. The authors are listed in prov/DR8QGH.jsonl.
"""RFC 6979 Section 3.2 nonce generation, and a fault attack on deterministic signing.

rfc6979_k follows RFC 6979 Section 3.2, steps a to h, with HMAC from the
standard library hmac module and the hash from hashlib. It needs only the
group order q, so it serves DSA and ECDSA alike.

The second part signs with a toy Schnorr scheme in a group of order 1019 and
a deterministic nonce, injects a simulated fault, and recovers the key from
one correct and one faulty signature of the same message. A hedged nonce,
which mixes fresh randomness into the deterministic one, stops this attack.
The hedged function here is a simple variant in the spirit of
draft-irtf-cfrg-det-sigs-with-noise; it is not the exact construction of
that draft.

For study only. This code is not constant time, the group is tiny, and the
attack runs only against a local simulated signer.
"""

import hashlib
import hmac
import random


def bits2int(b: bytes, qlen: int) -> int:
    """RFC 6979 Section 2.3.2: keep the leftmost qlen binary digits."""
    v = int.from_bytes(b, "big")
    blen = 8 * len(b)
    return v >> (blen - qlen) if blen > qlen else v


def int2octets(x: int, rlen: int) -> bytes:
    """RFC 6979 Section 2.3.3: x as rlen bytes in big endian."""
    return x.to_bytes(rlen, "big")


def bits2octets(b: bytes, q: int, qlen: int, rlen: int) -> bytes:
    """RFC 6979 Section 2.3.4: bits2int, then reduce mod q once, then int2octets."""
    return int2octets(bits2int(b, qlen) % q, rlen)


def rfc6979_k(x: int, h1: bytes, q: int, hash_name: str = "sha256") -> int:
    """The nonce k of RFC 6979 Section 3.2 for the secret key x and the message hash h1."""
    qlen = q.bit_length()
    rlen = (qlen + 7) // 8
    hlen = hashlib.new(hash_name).digest_size

    def mac(key: bytes, data: bytes) -> bytes:
        return hmac.new(key, data, hash_name).digest()

    v = b"\x01" * hlen  # @line L1
    k = b"\x00" * hlen
    seed = int2octets(x, rlen) + bits2octets(h1, q, qlen, rlen)
    k = mac(k, v + b"\x00" + seed)  # @line L2
    v = mac(k, v)
    k = mac(k, v + b"\x01" + seed)  # @line L3
    v = mac(k, v)
    while True:  # @line L4
        t = b""
        while 8 * len(t) < qlen:  # @line L5
            v = mac(k, v)
            t += v
        cand = bits2int(t, qlen)  # @line L6
        if 1 <= cand <= q - 1:  # @line L7
            return cand
        k = mac(k, v + b"\x00")  # @line L8
        v = mac(k, v)


# ------------------------------------------------------ the fault attack
P, Q, G = 2039, 1019, 4  # a toy Schnorr group: G has prime order Q in Z_P^*


def challenge(r_elem: int, msg: bytes) -> int:
    return int.from_bytes(hashlib.sha256(r_elem.to_bytes(2, "big") + msg).digest(), "big") % Q


def det_sign(x: int, msg: bytes, fault: bool = False) -> tuple[int, int]:
    """Schnorr with the RFC 6979 nonce. With fault=True, one binary digit of R is
    flipped after R is computed (a glitch in a register), and the faulty R is
    both hashed and output, as in the attacks on EdDSA."""
    k = rfc6979_k(x, hashlib.sha256(msg).digest(), Q)
    r_elem = pow(G, k, P)
    if fault:
        r_elem ^= 1
    e = challenge(r_elem, msg)
    return r_elem, (k + e * x) % Q


def hedged_sign(x: int, msg: bytes, rng: random.Random, fault: bool = False) -> tuple[int, int]:
    """The same signer, but the nonce also hashes 32 fresh random bytes."""
    noise = rng.getrandbits(256).to_bytes(32, "big")
    k = rfc6979_k(x, hashlib.sha256(noise + msg).digest(), Q)
    r_elem = pow(G, k, P)
    if fault:
        r_elem ^= 1
    e = challenge(r_elem, msg)
    return r_elem, (k + e * x) % Q


def recover_from_fault(msg: bytes, good: tuple[int, int], bad: tuple[int, int]) -> int | None:
    """Both signatures used the same k: s1 - s2 = (e1 - e2) x mod Q."""
    e1, e2 = challenge(good[0], msg), challenge(bad[0], msg)
    if e1 == e2:
        return None
    return (good[1] - bad[1]) * pow(e1 - e2, -1, Q) % Q
