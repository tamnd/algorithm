# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-sieving/. The authors are listed in prov/Y3ARK8.jsonl.
"""The Gauss sieve with its partner searches done by quantum search (BBHT).

Each search runs over the list of the sieve. The list index register has
q = ceil(log2 |list|) qubits; indices at or above |list| are padding and never
marked. A run of j Grover iterations followed by a measurement is simulated
exactly: with M marked indices out of 2^q and sin^2(theta) = M / 2^q, the
measured index is marked with probability sin^2((2j + 1) theta), and it is uniform
among the marked (or among the unmarked) indices. The simulator evaluates the
predicate on every item to know M; that work is the simulation, not the
algorithm, and is not counted as queries. The test file checks this sampling
rule against a full state-vector simulation with qsim.
"""

import math
import random
from typing import Callable, List, Optional, Sequence, Tuple

Vec = Tuple[int, ...]
LAMBDA = 6 / 5  # the growth factor of Boyer, Brassard, Hoyer and Tapp


def norm2(v: Sequence[int]) -> int:
    return sum(x * x for x in v)


def dot(u: Sequence[int], v: Sequence[int]) -> int:
    return sum(x * y for x, y in zip(u, v))


def add(u: Sequence[int], v: Sequence[int], s: int = 1) -> Vec:
    return tuple(x + s * y for x, y in zip(u, v))


class Counter:
    """Counts oracle queries: Grover iterations plus the classical check of each measured item."""

    def __init__(self) -> None:
        self.queries = 0
        self.searches = 0
        self.missed = 0


def grover_measure(marked: Sequence[bool], q: int, j: int, rng: random.Random) -> int:
    """Measure the index register after j Grover iterations on q qubits (exact sampling)."""
    size = 1 << q
    good = [i for i, m in enumerate(marked) if m]
    bad_count = size - len(good)
    theta = math.asin(math.sqrt(len(good) / size))
    p_good = math.sin((2 * j + 1) * theta) ** 2
    if good and rng.random() < p_good:
        return rng.choice(good)
    k = rng.randrange(bad_count)  # the k-th unmarked index of 0 .. size - 1
    marked_set = set(good)
    for i in range(size):
        if i not in marked_set:
            if k == 0:
                return i
            k -= 1
    raise AssertionError("unreachable")


def quantum_search(items: Sequence, pred: Callable, rng: random.Random, counter: Counter,
                   c: float = 9.0) -> Optional[int]:
    """BBHT search for an index i with pred(items[i]); None if none is found within c sqrt(2^q) queries."""
    K = len(items)
    counter.searches += 1
    if K == 0:
        return None
    q = max(1, (K - 1).bit_length())
    size = 1 << q
    marked = [i < K and pred(items[i]) for i in range(size)]  # simulation only
    budget = math.ceil(c * math.sqrt(size))
    m, spent = 1.0, 0  # @line L9
    while spent < budget:  # @line L10
        j = rng.randrange(math.ceil(m))  # @line L11
        i = grover_measure(marked, q, j, rng)  # @line L11
        spent += j + 1  # j oracle calls in the iterations and one classical check
        if i < K and pred(items[i]):  # @line L12
            counter.queries += spent
            return i
        m = min(LAMBDA * m, math.sqrt(size))  # @line L13
    counter.queries += spent
    if any(marked):
        counter.missed += 1
    return None  # @line L14


def classical_search(items: Sequence, pred: Callable, counter: Counter) -> Optional[int]:
    """A linear scan; every predicate evaluation counts as one query."""
    counter.searches += 1
    for i, w in enumerate(items):
        counter.queries += 1
        if pred(w):
            return i
    return None


def sample_vector(basis: Sequence[Vec], rng: random.Random, width: int = 2) -> Vec:
    """A random lattice vector: a combination of the basis with coefficients in [-width, width]."""
    v = tuple(0 for _ in basis[0])
    for b in basis:
        v = add(v, b, rng.randint(-width, width))
    return v


def gauss_sieve(basis: Sequence[Vec], rng: random.Random, collisions: int = 50,
                quantum: bool = True, max_samples: int = 5000,
                counter: Optional[Counter] = None) -> Tuple[Optional[Vec], List[Vec], Counter]:
    """The Gauss sieve. Returns the shortest list vector, the final list and the query counts."""
    counter = counter or Counter()

    def search(items: Sequence[Vec], pred: Callable) -> Optional[int]:
        if quantum:
            return quantum_search(items, pred, rng, counter)
        return classical_search(items, pred, counter)

    L: List[Vec] = []  # @line L1
    S: List[Vec] = [tuple(b) for b in basis]  # @line L1
    c, samples = 0, 0  # @line L1
    while c < collisions and samples < max_samples:  # @line L2
        v = S.pop() if S else sample_vector(basis, rng)  # @line L3
        samples += 1
        while True:  # @line L4: reduce v by the list
            i = search(L, lambda w: 2 * abs(dot(v, w)) > norm2(w))
            if i is None:
                break
            w = L[i]
            v = add(v, w, -1) if dot(v, w) > 0 else add(v, w, 1)
        if norm2(v) == 0:  # @line L5
            c += 1
            continue
        while True:  # @line L6: reduce the list by v
            i = search(L, lambda w: 2 * abs(dot(v, w)) > norm2(v))
            if i is None:
                break
            w = L.pop(i)
            S.append(add(w, v, -1) if dot(v, w) > 0 else add(w, v, 1))
        L.append(v)  # @line L7
    best = min(L, key=norm2) if L else None  # @line L8
    return best, L, counter


# ---------------------------------------------------------------- test lattices


def goldstein_mayer_basis(n: int, p: int, rng: random.Random) -> List[Vec]:
    """Rows (p, 0, ..., 0) and (x_i, e_i): the lattice of y with y_0 = sum_i x_i y_i mod p."""
    basis = [tuple([p] + [0] * (n - 1))]
    xs = [rng.randrange(1, p) for _ in range(n - 1)]
    for i, x in enumerate(xs):
        row = [0] * n
        row[0], row[i + 1] = x, 1
        basis.append(tuple(row))
    return basis


def in_goldstein_mayer(y: Sequence[int], basis: Sequence[Vec]) -> bool:
    p = basis[0][0]
    return (y[0] - sum(b[0] * yi for b, yi in zip(basis[1:], y[1:]))) % p == 0


def shortest_length2(basis: Sequence[Vec], bound: int) -> int:
    """The exact squared length of a shortest nonzero vector, given that it is at most bound^2 (brute force)."""
    n, p = len(basis), basis[0][0]
    best = bound * bound
    rng_range = range(-bound, bound + 1)

    def rec(prefix: List[int]) -> None:
        nonlocal best
        partial = sum(x * x for x in prefix)
        if partial > best:
            return
        if len(prefix) == n - 1:
            r = sum(b[0] * yi for b, yi in zip(basis[1:], prefix)) % p
            for y0 in (r, r - p):
                if abs(y0) <= bound:
                    t = partial + y0 * y0
                    if 0 < t < best or (t == best and t > 0):
                        best = t
            return
        for y in rng_range:
            rec(prefix + [y])

    rec([])
    return best
