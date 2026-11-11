# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/batch-verification/. The authors are listed in prov/VY28AZ.jsonl.
"""Batch verification of toy Schnorr signatures with the small exponents test.

batch_verify follows the small exponents test of Bellare, Garay and Rabin:
each signature equation g^s_i = R_i y_i^e_i is raised to a random l-bit
weight z_i, and the product of all weighted equations is checked with one
multi-exponentiation. A batch with at least one bad signature passes with
probability at most 2^(-l) in a group of prime order.

naive_batch_verify drops the weights. Two bad signatures whose errors cancel
then pass, which the tests show.

For study only. The group has order 1019 and offers no security, the code is
not constant time, and the attacks run only against this local verifier.
"""

import hashlib
import random

P, Q, G = 2039, 1019, 4  # G has prime order Q in Z_P^*

Sig = tuple[int, int]  # (R, s)
Item = tuple[int, bytes, Sig]  # (public key y, message, signature)


def in_group(a: int) -> bool:
    return 1 <= a < P and pow(a, Q, P) == 1


def challenge(r_elem: int, y: int, msg: bytes) -> int:
    data = r_elem.to_bytes(2, "big") + y.to_bytes(2, "big") + msg
    return int.from_bytes(hashlib.sha256(data).digest(), "big") % Q


def keygen(rng: random.Random) -> tuple[int, int]:
    x = rng.randrange(1, Q)
    return x, pow(G, x, P)


def sign(x: int, msg: bytes, rng: random.Random) -> Sig:
    k = rng.randrange(1, Q)
    r_elem = pow(G, k, P)
    return r_elem, (k + challenge(r_elem, pow(G, x, P), msg) * x) % Q


def verify(y: int, msg: bytes, sig: Sig) -> bool:
    r_elem, s = sig
    if not in_group(r_elem) or not in_group(y) or not 0 <= s < Q:
        return False
    return pow(G, s, P) == r_elem * pow(y, challenge(r_elem, y, msg), P) % P


def multi_exp(bases: list[int], exps: list[int]) -> int:
    """Straus (Shamir's trick): one shared run of squarings for all the bases."""
    acc = 1
    for bit in range(max((e.bit_length() for e in exps), default=0) - 1, -1, -1):
        acc = acc * acc % P
        for b, e in zip(bases, exps):
            if (e >> bit) & 1:
                acc = acc * b % P
    return acc


def batch_verify(items: list[Item], rng: random.Random, l: int = 64) -> bool:
    """The small exponents test on the equations g^s_i = R_i y_i^e_i."""
    for y, _, (r_elem, s) in items:  # @line L1
        if not in_group(r_elem) or not in_group(y) or not 0 <= s < Q:
            return False
    es = [challenge(r, y, m) for y, m, (r, _) in items]  # @line L2
    zs = [rng.getrandbits(l) for _ in items]  # @line L3
    big_s = sum(z * s for z, (_, _, (_, s)) in zip(zs, items)) % Q  # @line L4
    bases, exps = [], []
    for z, e, (y, _, (r_elem, _)) in zip(zs, es, items):
        bases += [r_elem, y]
        exps += [z % Q, z * e % Q]
    return pow(G, big_s, P) == multi_exp(bases, exps)  # @line L5


def naive_batch_verify(items: list[Item]) -> bool:
    """Wrong: the product of the equations with no random weights."""
    for y, _, (r_elem, s) in items:
        if not in_group(r_elem) or not in_group(y) or not 0 <= s < Q:
            return False
    big_s = sum(s for _, _, (_, s) in items) % Q
    rhs = 1
    for y, m, (r_elem, _) in items:
        rhs = rhs * r_elem * pow(y, challenge(r_elem, y, m), P) % P
    return pow(G, big_s, P) == rhs


def cancel_two(items: list[Item], i: int, j: int, delta: int) -> list[Item]:
    """Make signatures i and j invalid with errors +delta and -delta that cancel in a sum."""
    out = list(items)
    yi, mi, (ri, si) = out[i]
    yj, mj, (rj, sj) = out[j]
    out[i] = (yi, mi, (ri, (si + delta) % Q))
    out[j] = (yj, mj, (rj, (sj - delta) % Q))
    return out
