# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequential-counter-encoding/. The authors are listed in prov/JYYPDZ.jsonl.

import itertools
import random
from math import comb

from sequential_counter_encoding import at_least_k, at_most_k


def satisfies(clauses: list[list[int]], val: dict[int, bool]) -> bool:
    return all(any(val[abs(a)] == (a > 0) for a in c) for c in clauses)


def unit_propagate(clauses: list[list[int]], assign: dict[int, bool]) -> dict[int, bool] | None:
    """Return the closure of assign under unit propagation, or None on a conflict."""
    a = dict(assign)
    changed = True
    while changed:
        changed = False
        for c in clauses:
            free = []
            sat = False
            for lit in c:
                v = a.get(abs(lit))
                if v is None:
                    free.append(lit)
                elif v == (lit > 0):
                    sat = True
                    break
            if sat:
                continue
            if not free:
                return None
            if len(free) == 1:
                a[abs(free[0])] = free[0] > 0
                changed = True
    return a


def projected_models(clauses: list[list[int]], n: int, top: int) -> set[tuple[bool, ...]]:
    """The inputs x in {0,1}^n that extend to a model. Unit propagation is sound,
    so a conflict proves that no extension exists. Without a conflict, the
    propagated values with all other registers false must form a model."""
    out = set()
    for bits in itertools.product([False, True], repeat=n):
        res = unit_propagate(clauses, dict(zip(range(1, n + 1), bits)))
        if res is None:
            continue
        full = {v: res.get(v, False) for v in range(1, top + 1)}
        assert satisfies(clauses, full)
        out.add(bits)
    return out


def test_counts() -> None:
    for n in range(2, 12):
        for k in range(1, n):
            cl, top = at_most_k(list(range(1, n + 1)), k, n)
            assert top - n == k * (n - 1)
            assert len(cl) == 2 * n * k + n - 3 * k - 1
    cl, _ = at_most_k(list(range(1, 11)), 3, 10)
    assert len(cl) == 60 and comb(10, 4) == 210


def test_projection_is_the_constraint() -> None:
    for n in range(1, 7):
        for k in range(0, n + 1):
            cl, top = at_most_k(list(range(1, n + 1)), k, n)
            want = {b for b in itertools.product([False, True], repeat=n) if sum(b) <= k}
            assert projected_models(cl, n, top) == want
            cl, top = at_least_k(list(range(1, n + 1)), k, n)
            want = {b for b in itertools.product([False, True], repeat=n) if sum(b) >= k}
            assert projected_models(cl, n, top) == want


def test_unit_propagation_is_arc_consistent() -> None:
    for n in range(1, 8):
        for k in range(0, n + 1):
            cl, _ = at_most_k(list(range(1, n + 1)), k, n)
            for part in itertools.product([None, False, True], repeat=n):
                start = {i + 1: v for i, v in enumerate(part) if v is not None}
                ones = sum(v is True for v in part)
                res = unit_propagate(cl, start)
                if ones > k:
                    assert res is None
                    continue
                assert res is not None
                for i in range(1, n + 1):
                    if part[i - 1] is None:
                        assert res.get(i) == (False if ones == k else None)


def test_random_literals_and_offsets() -> None:
    rng = random.Random(2005)
    for _ in range(200):
        n = rng.randint(1, 6)
        xs = [v if rng.random() < 0.5 else -v for v in range(1, n + 1)]
        k = rng.randint(0, n)
        cl, top = at_most_k(xs, k, n)
        want = {b for b in itertools.product([False, True], repeat=n)
                if sum(b[abs(x) - 1] == (x > 0) for x in xs) <= k}
        assert projected_models(cl, n, top) == want
