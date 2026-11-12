# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/locally-decodable-codes/. The authors are listed in prov/53AB3R.jsonl.
"""Two locally decodable codes and their local decoders.

Hadamard code: x in {0,1}^k maps to the 2^k bits <x, a> mod 2. The 2-query decoder for x_i
reads positions a and a XOR e_i for a uniform a and returns their XOR.

Reed-Muller code over GF(p): the message is a polynomial f of total degree at most r in m
variables, the codeword is f on all of GF(p)^m. The (r+1)-query decoder for f(x) picks a
uniform direction y and reads f(x + t y) for t = 1..r+1, then interpolates at t = 0.
"""

import random
from typing import Callable, Dict, List, Sequence, Tuple


# ---------- Hadamard code ----------

def hadamard_encode(x: int, k: int) -> List[int]:
    return [bin(x & a).count("1") & 1 for a in range(1 << k)]


def hadamard_local_decode(word: Callable[[int], int], i: int, k: int, rng: random.Random) -> int:
    """Two queries. word is oracle access to a possibly corrupted codeword."""
    a = rng.randrange(1 << k)
    return word(a) ^ word(a ^ (1 << i))


def hadamard_success(word: Sequence[int], x: int, i: int, k: int) -> float:
    """The exact success probability of the decoder for bit i (all 2^k choices of a)."""
    xi = x >> i & 1
    return sum((word[a] ^ word[a ^ (1 << i)]) == xi for a in range(1 << k)) / (1 << k)


def hadamard_decode_all(word: Sequence[int], k: int, reps: int, rng: random.Random) -> int:
    """Majority of reps independent local decodings for every bit (for corruption < 1/4)."""
    x = 0
    for i in range(k):
        votes = sum(hadamard_local_decode(word.__getitem__, i, k, rng) for _ in range(reps))
        x |= (2 * votes > reps) << i
    return x


# ---------- Reed-Muller code over GF(p) ----------

Point = Tuple[int, ...]


def rm_eval(coeffs: Dict[Tuple[int, ...], int], pt: Point, p: int) -> int:
    """coeffs maps exponent tuples (total degree <= r) to coefficients."""
    total = 0
    for exps, c in coeffs.items():
        term = c
        for v, e in zip(pt, exps):
            term = term * pow(v, e, p) % p
        total += term
    return total % p


def rm_encode(coeffs: Dict[Tuple[int, ...], int], m: int, p: int) -> Dict[Point, int]:
    pts = [()]  # all of GF(p)^m
    for _ in range(m):
        pts = [q + (v,) for q in pts for v in range(p)]
    return {pt: rm_eval(coeffs, pt, p) for pt in pts}


def interpolate_at_zero(ts: Sequence[int], vals: Sequence[int], p: int) -> int:
    """Lagrange interpolation over GF(p) of the points (t, val), evaluated at t = 0."""
    total = 0
    for j, (tj, vj) in enumerate(zip(ts, vals)):
        num = den = 1
        for l, tl in enumerate(ts):
            if l != j:
                num = num * (-tl) % p
                den = den * (tj - tl) % p
        total += vj * num * pow(den, p - 2, p)
    return total % p


def rm_local_decode_line(word: Dict[Point, int], x: Point, y: Point, r: int, p: int) -> int:
    """r + 1 queries on the line x + t y, t = 1..r+1; f restricted to it has degree <= r."""
    ts = list(range(1, r + 2))
    vals = [word[tuple((xi + t * yi) % p for xi, yi in zip(x, y))] for t in ts]
    return interpolate_at_zero(ts, vals, p)


def rm_local_decode(word: Dict[Point, int], x: Point, r: int, p: int, rng: random.Random) -> int:
    m = len(x)
    while True:
        y = tuple(rng.randrange(p) for _ in range(m))
        if any(y):
            return rm_local_decode_line(word, x, y, r, p)


def rm_success(word: Dict[Point, int], truth: Dict[Point, int], x: Point, r: int, p: int) -> float:
    """The exact success probability at x over all nonzero directions y."""
    m = len(x)
    dirs = [()]
    for _ in range(m):
        dirs = [d + (v,) for d in dirs for v in range(p)]
    dirs = [d for d in dirs if any(d)]
    good = sum(rm_local_decode_line(word, x, y, r, p) == truth[x] for y in dirs)
    return good / len(dirs)
