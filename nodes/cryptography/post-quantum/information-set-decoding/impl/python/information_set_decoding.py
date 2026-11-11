# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/information-set-decoding/. The authors are listed in prov/97Z92V.jsonl.
"""A common harness for information set decoding (ISD) over GF(2).

A binary matrix is a list of rows, and each row is a Python int whose bit j is
the entry in column j. H has r = n - k rows, and the syndrome s is an int with
r bits (bit i belongs to row i).

isd() is the template of the page. Each round picks r random columns, makes
them the identity by Gauss-Jordan elimination, and asks a variant for
candidate sets A of columns outside the identity. The variants here are the
ones of Prange (A empty), Lee-Brickell (|A| <= p) and Stern (p columns in each
half, matched on a window of l rows). The harness counts rounds and the
number of candidates, so that the variants can be compared on the same
random instances.

For study only. The code is not constant time, uses the random module, and
runs only on toy sizes. Use a vetted library, for example a FIPS 140
validated module, to protect real data.
"""

import random
from itertools import combinations
from math import comb, log2
from typing import Callable, Dict, Iterator, List, Optional, Sequence, Tuple

Candidates = Callable[[Dict[int, int], int, List[int], int, random.Random], Iterator[Tuple[Tuple[int, ...], int]]]


def weight(x: int) -> int:
    """Hamming weight of an int seen as a bit vector."""
    return bin(x).count("1")


def syndrome(h: Sequence[int], e: int) -> int:
    """H e over GF(2)."""
    s = 0
    for i, row in enumerate(h):
        if weight(row & e) & 1:
            s |= 1 << i
    return s


def rank(h: Sequence[int]) -> int:
    """Rank over GF(2) of the rows of H."""
    basis: List[int] = []
    for row in h:
        for b in basis:
            row = min(row, row ^ b)
        if row:
            basis.append(row)
            basis.sort(reverse=True)
    return len(basis)


def eliminate(h: Sequence[int], s: int, cols: Sequence[int]) -> Optional[Tuple[List[int], int]]:
    """Gauss-Jordan elimination that makes the columns `cols` of H the identity.

    Returns (U H, U s), with row i pivoting on cols[i], or None if singular.
    """
    r = len(h)
    rows = list(h)
    synd = [(s >> i) & 1 for i in range(r)]
    for i, c in enumerate(cols):
        bit = 1 << c
        piv = next((j for j in range(i, r) if rows[j] & bit), None)
        if piv is None:
            return None
        rows[i], rows[piv] = rows[piv], rows[i]
        synd[i], synd[piv] = synd[piv], synd[i]
        for j in range(r):
            if j != i and rows[j] & bit:
                rows[j] ^= rows[i]
                synd[j] ^= synd[i]
    return rows, sum(b << i for i, b in enumerate(synd))


def column(rows: Sequence[int], j: int) -> int:
    """Column j of a matrix given by rows, as an int with one bit per row."""
    c = 0
    for i, row in enumerate(rows):
        c |= ((row >> j) & 1) << i
    return c


def prange_candidates() -> Candidates:
    """Prange: the only candidate is A = {} (all errors on the identity columns)."""
    def gen(hcol, s2, info, w, rng):
        yield (), s2
    return gen


def lee_brickell_candidates(p: int) -> Candidates:
    """Lee-Brickell: every A outside the identity with |A| <= p."""
    def gen(hcol, s2, info, w, rng):
        for size in range(p + 1):
            for a in combinations(info, size):
                t = s2
                for j in a:
                    t ^= hcol[j]
                yield a, t
    return gen


def stern_candidates(p: int, l: int) -> Candidates:
    """Stern: |A1| = |A2| = p in two random halves, with t zero on rows 0 .. l-1."""
    window = (1 << l) - 1

    def gen(hcol, s2, info, w, rng):
        info = list(info)
        rng.shuffle(info)
        j1, j2 = info[: len(info) // 2], info[len(info) // 2:]
        table: Dict[int, List[Tuple[Tuple[int, ...], int]]] = {}
        for a1 in combinations(j1, p):
            v = s2
            for j in a1:
                v ^= hcol[j]
            table.setdefault(v & window, []).append((a1, v))
        for a2 in combinations(j2, p):
            u = 0
            for j in a2:
                u ^= hcol[j]
            for a1, v in table.get(u & window, ()):
                yield a1 + a2, v ^ u
    return gen


def isd(h: Sequence[int], s: int, n: int, w: int, candidates: Candidates, rng: random.Random,
        max_iter: int = 1_000_000) -> Tuple[Optional[int], int, int]:
    """The ISD template. Returns (e, rounds, tried): e has H e = s and weight w,
    or e is None after max_iter rounds. rounds counts the rounds with an
    invertible column set, and tried counts the candidates checked."""
    r = len(h)
    rounds = draws = tried = 0
    while rounds < max_iter and draws < 8 * max_iter:     # @line L1
        draws += 1
        cols = rng.sample(range(n), r)                    # @line L2
        chosen = set(cols)
        info = [j for j in range(n) if j not in chosen]
        res = eliminate(h, s, cols)                       # @line L3
        if res is None:                                   # @line L4
            continue
        rounds += 1
        rows, s2 = res
        hcol = {j: column(rows, j) for j in info}
        for a, t in candidates(hcol, s2, info, w, rng):   # @line L5
            tried += 1                                    # @line L6
            if weight(t) == w - len(a):                   # @line L7
                e = 0
                for i, c in enumerate(cols):
                    if (t >> i) & 1:
                        e |= 1 << c
                for j in a:
                    e |= 1 << j
                return e, rounds, tried                   # @line L8
    return None, rounds, tried


def random_instance(n: int, k: int, w: int, rng: random.Random) -> Tuple[List[int], int, int]:
    """A random full rank (n - k) x n matrix H, a random e of weight w, and s = H e."""
    r = n - k
    while True:
        h = [rng.getrandbits(n) for _ in range(r)]
        if rank(h) == r:
            break
    e = 0
    for c in rng.sample(range(n), w):
        e |= 1 << c
    return h, syndrome(h, e), e


def success_prange(n: int, k: int, w: int) -> float:
    return comb(n - k, w) / comb(n, w)


def success_lee_brickell(n: int, k: int, w: int, p: int) -> float:
    return sum(comb(k, i) * comb(n - k, w - i) for i in range(min(p, w) + 1)) / comb(n, w)


def success_stern(n: int, k: int, w: int, p: int, l: int) -> float:
    k1 = k // 2
    return comb(k1, p) * comb(k - k1, p) * comb(n - k - l, w - 2 * p) / comb(n, w)


def mean_rounds(n: int, k: int, w: int, candidates: Candidates, trials: int, seed: int) -> Tuple[float, float]:
    """Mean rounds and mean candidates over random instances made from `seed`.

    The instances depend only on the seed, so two variants with the same seed
    run on the same instances.
    """
    inst_rng = random.Random(seed)
    alg_rng = random.Random(seed + 1)
    rounds = tried = 0
    for _ in range(trials):
        h, s, _ = random_instance(n, k, w, inst_rng)
        e, a, b = isd(h, s, n, w, candidates, alg_rng)
        assert e is not None and syndrome(h, e) == s and weight(e) == w
        rounds += a
        tried += b
    return rounds / trials, tried / trials


def binary_entropy(x: float) -> float:
    return 0.0 if x <= 0 or x >= 1 else -x * log2(x) - (1 - x) * log2(1 - x)


def gv_distance(rate: float) -> float:
    """The relative Gilbert-Varshamov distance: the omega < 1/2 with H2(omega) = 1 - rate."""
    lo, hi = 0.0, 0.5
    for _ in range(80):
        mid = (lo + hi) / 2
        if binary_entropy(mid) < 1 - rate:
            lo = mid
        else:
            hi = mid
    return lo


def prange_exponent(rate: float, omega: float) -> float:
    """c with 2^(c n) rounds of Prange: H2(omega) - (1 - rate) H2(omega / (1 - rate))."""
    return binary_entropy(omega) - (1 - rate) * binary_entropy(omega / (1 - rate))
