# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boomerang-attack/. The authors are listed in prov/008RPY.jsonl.
"""The boomerang attack (Wagner 1999) on the Heys toy SPN.

For study only: a teaching attack on a 16-bit toy cipher. Nothing here is
constant time or fit for real use; for real data use AES from a validated
library (for example the Python package "cryptography").

Split the 4-round cipher as E = E1 o E0: E0 is rounds 1 and 2, E1 is rounds
3 and 4. Take a differential alpha -> beta for E0 (probability p) and a
differential gamma -> delta for E1 (probability q). One quartet:

    P' = P ^ alpha,  C = E(P),  C' = E(P'),
    D = C ^ delta,   D' = C' ^ delta,  Q = E^-1(D),  Q' = E^-1(D'),

and the quartet "returns" when Q ^ Q' = alpha. Wagner's estimate of the
return rate is p^2 q^2 for one beta and one gamma, or phat^2 qhat^2 with
phat^2 = sum over beta of P[alpha -> beta]^2 (and the same for qhat).
Since the block has 16 bits, this module can work with full codebooks.
"""

from collections import Counter

from heys_spn import PERM, SUB

ALPHA = 0x00B0
DELTA = 0x0008


def tables(keys: list[int]) -> tuple[list[int], list[int], list[int], list[int]]:
    """Codebooks for E0, E1, E = E1 o E0 and E^-1 under five round keys."""
    e0 = [PERM[SUB[PERM[SUB[x ^ keys[0]]] ^ keys[1]]] for x in range(1 << 16)]
    e1 = [SUB[PERM[SUB[x ^ keys[2]]] ^ keys[3]] ^ keys[4] for x in range(1 << 16)]
    e = [e1[y] for y in e0]
    d = [0] * (1 << 16)
    for p, c in enumerate(e):
        d[c] = p
    return e0, e1, e, d


def quartet_returns(enc, dec, p: int, alpha: int = ALPHA, delta: int = DELTA) -> bool:
    """The quartet check: two encryptions, two decryptions, one comparison."""
    c, c2 = enc(p), enc(p ^ alpha)
    return dec(c ^ delta) ^ dec(c2 ^ delta) == alpha


def boomerang_count(enc, dec, plaintexts: list[int], alpha: int = ALPHA, delta: int = DELTA) -> float:
    """The boomerang distinguisher: the fraction of quartets that return."""
    count = 0  # @line L1
    for p in plaintexts:  # @line L2
        p2 = p ^ alpha  # @line L3
        c, c2 = enc(p), enc(p2)  # @line L4
        d, d2 = c ^ delta, c2 ^ delta  # @line L5
        q, q2 = dec(d), dec(d2)  # @line L6
        if q ^ q2 == alpha:  # @line L7
            count += 1
    return count / len(plaintexts)  # @line L8


def boomerang_rate(e: list[int], d: list[int], alpha: int = ALPHA, delta: int = DELTA) -> float:
    """Exact return rate over all 2^16 plaintexts."""
    hits = sum(1 for p in range(1 << 16) if d[e[p] ^ delta] ^ d[e[p ^ alpha] ^ delta] == alpha)
    return hits / (1 << 16)


def differential_profile(f: list[int], a: int) -> Counter:
    """How often each output difference appears for input difference a."""
    return Counter(f[x] ^ f[x ^ a] for x in range(1 << 16))


def estimates(e0: list[int], e1: list[int], alpha: int = ALPHA, delta: int = DELTA) -> dict:
    """Wagner's estimates p^2 q^2 (best beta, gamma) and phat^2 qhat^2."""
    n = float(1 << 16)
    prof0 = differential_profile(e0, alpha)
    e1_inv = [0] * (1 << 16)
    for x, y in enumerate(e1):
        e1_inv[y] = x
    prof1 = differential_profile(e1_inv, delta)  # gamma -> delta, counted backwards
    beta, cb = prof0.most_common(1)[0]
    gamma, cg = prof1.most_common(1)[0]
    p, q = cb / n, cg / n
    p_hat2 = sum((v / n) ** 2 for v in prof0.values())
    q_hat2 = sum((v / n) ** 2 for v in prof1.values())
    return {"beta": beta, "p": p, "gamma": gamma, "q": q,
            "p2q2": p * p * q * q, "phat2qhat2": p_hat2 * q_hat2}


def best_long_differential(e: list[int], alpha: int = ALPHA) -> float:
    """The best probability of any output difference for alpha through all of E."""
    return differential_profile(e, alpha).most_common(1)[0][1] / (1 << 16)
