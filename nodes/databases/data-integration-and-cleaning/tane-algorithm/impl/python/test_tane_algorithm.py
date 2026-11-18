# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tane-algorithm/. The authors are listed in prov/HRXFKG.jsonl.

import itertools
import random
from fractions import Fraction

from tane_algorithm import (
    error_count,
    format_fd,
    g3_count,
    partition_of,
    stripped_product,
    tane,
)


def fd_holds(rows, lhs, a):
    """X -> A by the definition: two rows that agree on X agree on A."""
    for r, s in itertools.combinations(rows, 2):
        if all(r[b] == s[b] for b in lhs) and r[a] != s[a]:
            return False
    return True


def g3_brute(rows, lhs, a):
    """The least number of rows to delete so that X -> A holds, by trying all subsets."""
    n = len(rows)
    for m in range(n + 1):
        for drop in itertools.combinations(range(n), m):
            rest = [rows[i] for i in range(n) if i not in drop]
            if fd_holds(rest, lhs, a):
                return m
    return n


def brute_minimal_fds(rows, k, test):
    """All minimal non-trivial X -> A, by checking every X and every subset."""
    out = []
    for a in range(k):
        others = [b for b in range(k) if b != a]
        for size in range(len(others) + 1):
            for lhs in itertools.combinations(others, size):
                X = frozenset(lhs)
                if test(X, a) and all(not test(X - {b}, a) for b in X):
                    out.append((X, a))
    return sorted(out, key=lambda d: (len(d[0]), sorted(d[0]), d[1]))


def random_rows(rng, n, k, dom):
    return [tuple(rng.randrange(dom) for _ in range(k)) for _ in range(n)]


def as_set(fds):
    return {(frozenset(x), a) for x, a in fds}


def test_page_example():
    rows = [(1, "a", "x", 1), (1, "a", "y", 2), (2, "b", "x", 1), (2, "b", "y", 3), (3, "b", "x", 1)]
    got = [format_fd(d) for d in tane(rows, 4)]
    assert got == ["A -> B", "D -> C", "AC -> D", "BC -> D"]
    assert as_set(tane(rows, 4)) == as_set(brute_minimal_fds(rows, 4, lambda X, a: fd_holds(rows, X, a)))
    assert [error_count(partition_of(rows, X)) for X in ([], [0], [1], [2], [3])] == [4, 2, 3, 3, 2]


def test_key_pruning_loses_approximate_dependencies():
    rows = [(1, 0), (0, 0), (2, 2)]
    eps = Fraction(1, 3)
    assert [format_fd(d) for d in tane(rows, 2, eps)] == ["{} -> B", "B -> A"]
    assert [format_fd(d) for d in tane(rows, 2, eps, key_pruning=True)] == ["{} -> B"]


def test_against_brute_force_exact():
    rng = random.Random(20261118)
    for trial in range(300):
        k = rng.randint(1, 6)
        n = rng.randint(0, 14)
        dom = rng.randint(3, 5)
        rows = random_rows(rng, n, k, dom)
        expected = brute_minimal_fds(rows, k, lambda X, a: fd_holds(rows, X, a))
        assert tane(rows, k) == expected, (trial, rows)


def test_larger_relations():
    rng = random.Random(7)
    for trial in range(10):
        k = 6
        n = rng.choice([40, 120, 200])
        rows = random_rows(rng, n, k, 3)
        # plant two dependencies: column 4 is a function of columns 0 and 1,
        # column 5 is a function of column 2
        rows = [r[:4] + ((r[0] + 2 * r[1]) % 3, r[2] % 2) for r in rows]
        expected = brute_minimal_fds(rows, k, lambda X, a: fd_holds(rows, X, a))
        got = tane(rows, k)
        assert got == expected
        assert (frozenset([2]), 5) in as_set(got)


def test_empty_and_one_row():
    for rows in ([], [(1, 2, 3)]):
        assert tane(rows, 3) == [(frozenset(), 0), (frozenset(), 1), (frozenset(), 2)]


def test_exponential_family():
    # pairs (0, 1) and (2, 3), and the row id in column 4
    rows = [(0, 0, 0, 0, 0), (1, 1, 0, 0, 1), (0, 0, 1, 1, 2)]
    lhs_of_id = sorted(sorted(x) for x, a in tane(rows, 5) if a == 4)
    assert lhs_of_id == [[0, 2], [0, 3], [1, 2], [1, 3]]


def test_stripped_product():
    rng = random.Random(3)
    for _ in range(200):
        k = 4
        n = rng.randint(0, 20)
        rows = random_rows(rng, n, k, 3)
        X = frozenset(rng.sample(range(k), 2))
        Y = frozenset(rng.sample(range(k), 2))
        got = stripped_product(partition_of(rows, X), partition_of(rows, Y), n)
        want = partition_of(rows, X | Y)
        assert sorted(map(sorted, got)) == sorted(map(sorted, want))
        assert error_count(got) == error_count(want)


def test_g3_against_deletion():
    rng = random.Random(11)
    for _ in range(150):
        k = 3
        n = rng.randint(0, 8)
        rows = random_rows(rng, n, k, 3)
        lhs = frozenset(rng.sample(range(1, k), rng.randint(0, 2)))
        got = g3_count(partition_of(rows, lhs), partition_of(rows, lhs | {0}))
        assert got == g3_brute(rows, lhs, 0)


def test_approximate_against_brute_force():
    rng = random.Random(5)
    for trial in range(120):
        k = rng.randint(1, 5)
        n = rng.randint(0, 12)
        rows = random_rows(rng, n, k, rng.randint(3, 4))
        eps = rng.choice([Fraction(1, 10), Fraction(1, 5), Fraction(1, 3)])

        def approx(X, a):
            p, q = partition_of(rows, X), partition_of(rows, X | {a})
            return g3_count(p, q) <= eps * n

        assert tane(rows, k, eps) == brute_minimal_fds(rows, k, approx), (trial, rows, eps)
