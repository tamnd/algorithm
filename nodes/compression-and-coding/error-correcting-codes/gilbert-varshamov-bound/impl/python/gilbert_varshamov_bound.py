# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gilbert-varshamov-bound/. The authors are listed in prov/12WDFJ.jsonl.

"""The Gilbert-Varshamov bound: Gilbert's greedy code, Varshamov's column-by-column
construction of a parity-check matrix, and random linear codes.

Words over GF(p), p prime, are tuples of ints in range(p).
"""

import random
from itertools import product
from math import comb, log


def volume(q: int, n: int, r: int) -> int:
    """V_q(n, r): the number of words within distance r of a fixed word."""
    return sum(comb(n, i) * (q - 1) ** i for i in range(min(r, n) + 1))


def gilbert_bound(q: int, n: int, d: int) -> int:
    """ceil(q^n / V_q(n, d - 1)): A_q(n, d) is at least this, for every n and d."""
    v = volume(q, n, d - 1)
    return -(-q ** n // v)


def varshamov_dimension(q: int, n: int, d: int) -> int:
    """The largest k with V_q(n - 1, d - 2) < q^(n - k): a linear [n, k, >= d]_q code exists."""
    v = volume(q, n - 1, d - 2)
    k = n
    while k > 0 and not v < q ** (n - k):
        k -= 1
    return k


def distance(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return sum(a != b for a, b in zip(x, y))


def gilbert_greedy(q: int, n: int, d: int, order: list[tuple[int, ...]] | None = None) -> list[tuple[int, ...]]:
    """Gilbert's construction: scan the words and keep each one at distance >= d from all
    words kept so far. The result is a maximal code, so the balls of radius d - 1 around
    its words cover the whole space. Default order is lexicographic (a lexicode)."""
    words = order if order is not None else list(product(range(q), repeat=n))
    code: list[tuple[int, ...]] = []
    for x in words:
        if all(distance(x, c) >= d for c in code):
            code.append(x)
    return code


def varshamov_parity_check(q: int, n: int, k: int, d: int, rng: random.Random | None = None) -> list[tuple[int, ...]]:
    """Varshamov's construction: choose n columns of length r = n - k one at a time, each
    outside the set of combinations of at most d - 2 earlier columns. Returns the columns.

    Possible when V_q(n - 1, d - 2) < q^r, because that set has at most V_q(j - 1, d - 2)
    elements when column j is chosen. Then every d - 1 columns are independent, so the
    code with these columns as parity-check matrix has minimum distance >= d.
    """
    r = n - k
    space = list(product(range(q), repeat=r))
    zero = tuple([0] * r)
    # combos[i] = set of combinations with exactly i nonzero coefficients (i <= d - 2)
    combos: list[set[tuple[int, ...]]] = [{zero}] + [set() for _ in range(max(d - 2, 0))]
    cols: list[tuple[int, ...]] = []
    for _ in range(n):
        bad = set().union(*combos)
        free = [v for v in space if v not in bad]
        if not free:
            raise ValueError("no column left: V_q(n - 1, d - 2) >= q^(n - k)")
        c = rng.choice(free) if rng else free[0]
        cols.append(c)
        for i in range(len(combos) - 1, 0, -1):  # add a multiple of c to combos with i - 1 terms
            new = set()
            for s in combos[i - 1]:
                for a in range(1, q):
                    new.add(tuple((x + a * y) % q for x, y in zip(s, c)))
            combos[i] |= new
    return cols


def null_space(cols: list[tuple[int, ...]], q: int) -> list[tuple[int, ...]]:
    """A basis (rows) of {x : sum x_j cols[j] = 0} over GF(q), by Gaussian elimination."""
    n, r = len(cols), len(cols[0])
    m = [[cols[j][i] for j in range(n)] for i in range(r)]
    pivots = []
    row = 0
    for c in range(n):
        piv = next((i for i in range(row, r) if m[i][c]), None)
        if piv is None:
            continue
        m[row], m[piv] = m[piv], m[row]
        inv = pow(m[row][c], q - 2, q)
        m[row] = [(x * inv) % q for x in m[row]]
        for i in range(r):
            if i != row and m[i][c]:
                f = m[i][c]
                m[i] = [(x - f * y) % q for x, y in zip(m[i], m[row])]
        pivots.append(c)
        row += 1
    free = [c for c in range(n) if c not in pivots]
    basis = []
    for f in free:
        x = [0] * n
        x[f] = 1
        for i, pc in enumerate(pivots):
            x[pc] = (-m[i][f]) % q
        basis.append(tuple(x))
    return basis


def span(gen: list[tuple[int, ...]], q: int) -> list[tuple[int, ...]]:
    n = len(gen[0])
    return [tuple(sum(a * g[j] for a, g in zip(m, gen)) % q for j in range(n))
            for m in product(range(q), repeat=len(gen))]


def min_distance_linear(words: list[tuple[int, ...]]) -> int:
    return min(sum(1 for a in w if a) for w in words if any(w))


def random_parity_check_distance(n: int, k: int, rng: random.Random) -> int:
    """Minimum distance of the binary code with a uniformly random (n - k) x n parity-check
    matrix (words as ints; the code may have dimension above k)."""
    r = n - k
    cols = [rng.randrange(2 ** r) for _ in range(n)]
    best = n + 1
    for x in range(1, 2 ** n):
        s = 0
        y = x
        j = 0
        while y:
            if y & 1:
                s ^= cols[j]
            y >>= 1
            j += 1
        if s == 0:
            best = min(best, x.bit_count())
    return best


def entropy_q(x: float, q: int) -> float:
    if x <= 0:
        return 0.0
    return x * log(q - 1, q) - x * log(x, q) - (1 - x) * log(1 - x, q)


def gv_rate(delta: float, q: int = 2) -> float:
    """Asymptotic GV bound: rate 1 - h_q(delta) is achievable for delta <= 1 - 1/q."""
    return max(0.0, 1.0 - entropy_q(delta, q))
