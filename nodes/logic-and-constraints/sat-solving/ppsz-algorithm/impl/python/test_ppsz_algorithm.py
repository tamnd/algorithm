# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ppsz-algorithm/. The authors are listed in prov/ECTVB1.jsonl.

import itertools
import random
from fractions import Fraction

from ppsz_algorithm import bounded_resolution, ppsz_algorithm, ppsz_pass, satisfies


def models(n: int, clauses: list[list[int]]) -> list[list[bool]]:
    return [list(b) for b in itertools.product([False, True], repeat=n) if satisfies(clauses, list(b))]


def occ_of(n: int, g: list[frozenset[int]]) -> list[list[frozenset[int]]]:
    occ: list[list[frozenset[int]]] = [[] for _ in range(n + 1)]
    for c in g:
        for l in c:
            occ[abs(l)].append(c)
    return occ


def exact_success(n: int, g: list[frozenset[int]], target: list[bool]) -> Fraction:
    """The exact probability that one try returns target: the average of 2^-(guesses) over all orders."""
    occ = occ_of(n, g)
    total = Fraction(0)
    perms = list(itertools.permutations(range(1, n + 1)))
    for order in perms:
        x, forced = ppsz_pass(n, occ, list(order), lambda v: int(target[v - 1]))
        assert x == target  # forced values agree with the model when the guesses do
        total += Fraction(1, 2 ** (n - sum(forced)))
    return total / len(perms)


# all sign patterns over x1, x2, x3 except (-x1 or x2 or x3): the only model is 100
EXAMPLE = [[1, 2, 3], [-1, -2, 3], [1, -2, -3], [-1, 2, -3], [1, 2, -3], [-1, -2, -3], [1, -2, 3]]
A_STAR = [True, False, False]


def test_example() -> None:
    assert models(3, EXAMPLE) == [A_STAR]
    plain = bounded_resolution(EXAMPLE, 0)  # no resolvents: the PPZ algorithm
    assert len(plain) == 7
    occ = occ_of(3, plain)
    x, forced = ppsz_pass(3, occ, [2, 3, 1], lambda v: 0)
    assert x == A_STAR and forced == [True, False, False]  # x1 is forced by (x1 or x2 or x3)
    assert exact_success(3, plain, A_STAR) == Fraction(1, 4)  # the last variable is always forced
    closed = bounded_resolution(EXAMPLE, 3)
    assert {frozenset([1]), frozenset([-2]), frozenset([-3])} <= set(closed)
    assert exact_success(3, closed, A_STAR) == 1  # each variable is forced
    assert ppsz_algorithm(3, EXAMPLE, rng=random.Random(1)) == A_STAR


def test_edges() -> None:
    assert ppsz_algorithm(0, [], tries=1) == []
    assert ppsz_algorithm(2, [[]]) is None
    assert ppsz_algorithm(1, [[1], [-1]], tries=10) is None
    assert ppsz_algorithm(1, [[1, 1]], rng=random.Random(0)) == [True]
    assert ppsz_algorithm(2, [[1, -1]], tries=1, rng=random.Random(0)) is not None  # a tautology


def test_resolution_is_sound() -> None:
    rng = random.Random(4)
    for _ in range(150):
        n = rng.randint(1, 7)
        clauses = [[rng.choice([1, -1]) * rng.randint(1, n) for _ in range(rng.randint(1, 3))] for _ in range(rng.randint(1, 10))]
        ms = models(n, clauses)
        g = bounded_resolution(clauses, 4)
        assert all(len(c) <= 4 or list(c) in [list(frozenset(cl)) for cl in clauses] for c in g)
        for c in g:
            assert all(any(x[abs(l) - 1] == (l > 0) for l in c) for x in ms)


def test_random_against_brute_force() -> None:
    rng = random.Random(2024)
    sat = unsat = 0
    for _ in range(500):
        n = rng.randint(3, 8)
        k = rng.choice([2, 3, 3, 4])
        m = rng.randint(1, int(4.5 * n))
        clauses = [[rng.choice([1, -1]) * v for v in rng.sample(range(1, n + 1), min(k, n))] for _ in range(m)]
        x = ppsz_algorithm(n, clauses, tries=100, rng=random.Random(rng.randrange(10**9)))
        truth = bool(models(n, clauses))
        if x is not None:
            assert satisfies(clauses, x)
        if truth:
            assert x is not None
            sat += 1
        else:
            assert x is None
            unsat += 1
    assert sat > 200 and unsat > 50


def unique_instance(rng: random.Random, n: int) -> tuple[list[list[int]], list[bool]]:
    a = [rng.random() < 0.5 for _ in range(n)]
    clauses: list[list[int]] = []
    while len(models(n, clauses)) != 1:
        cl = [rng.choice([1, -1]) * v for v in rng.sample(range(1, n + 1), 3)]
        if satisfies([cl], a):
            clauses.append(cl)
    return clauses, a


def test_critical_clause_lemma() -> None:
    # on a formula with one model, a variable that comes last in one of its critical clauses is forced
    rng = random.Random(8)
    for _ in range(30):
        n = 7
        clauses, a = unique_instance(rng, n)
        g = bounded_resolution(clauses, 0)
        occ = occ_of(n, g)
        critical = {}
        for v in range(1, n + 1):
            b = a[:]
            b[v - 1] = not b[v - 1]
            critical[v] = [set(abs(l) for l in cl) for cl in clauses if not satisfies([cl], b)]
            assert critical[v]  # a unique model has a critical clause for each variable
        for _ in range(20):
            order = list(range(1, n + 1))
            rng.shuffle(order)
            pos = {v: i for i, v in enumerate(order)}
            x, forced = ppsz_pass(n, occ, order, lambda v: int(a[v - 1]))
            assert x == a
            for v in range(1, n + 1):
                if any(all(pos[u] <= pos[v] for u in c) for c in critical[v]):
                    assert forced[v - 1]


def test_ppz_bound_on_unique_formulas() -> None:
    # exact success probability of one try, against the proved bound 2^(-(1 - 1/3) n)
    rng = random.Random(12)
    for _ in range(3):
        n = 6
        clauses, a = unique_instance(rng, n)
        p_plain = exact_success(n, bounded_resolution(clauses, 0), a)
        p_closed = exact_success(n, bounded_resolution(clauses, 4), a)
        assert p_plain >= 2 ** (-(2 / 3) * n)
        assert p_closed >= p_plain  # more clauses force more variables
