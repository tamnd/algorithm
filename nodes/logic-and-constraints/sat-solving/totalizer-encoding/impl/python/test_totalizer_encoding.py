# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/totalizer-encoding/. The authors are listed in prov/MT2AEY.jsonl.

import itertools
import random
from math import comb

from totalizer_encoding import at_least_k, at_most_k, totalizer


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
    """Inputs that extend to a model. A conflict under unit propagation proves
    that there is no extension. Otherwise the propagated values, with every
    other new variable false, must be a model."""
    out = set()
    for bits in itertools.product([False, True], repeat=n):
        res = unit_propagate(clauses, dict(zip(range(1, n + 1), bits)))
        if res is None:
            continue
        full = {v: res.get(v, False) for v in range(1, top + 1)}
        assert satisfies(clauses, full)
        out.add(bits)
    return out


def test_page_example() -> None:
    cl, top = at_most_k([1, 2, 3, 4], 2, 4)
    assert top == 11 and len(cl) == 14
    assert cl[-1] == [-11]
    res = unit_propagate(cl, {1: True, 3: True})
    assert res is not None and res[2] is False and res[4] is False
    assert res[9] and res[10] and not res[11] and not res[6] and not res[8]


def test_full_counts() -> None:
    for n in range(1, 80):
        cl, outs, top = totalizer(list(range(1, n + 1)), n, n)
        assert len(outs) == n
        assert len(cl) == comb(n, 2) + (top - n)
    for d in range(1, 9):
        n = 2 ** d
        cl, _, top = totalizer(list(range(1, n + 1)), n, n)
        assert top - n == n * d


def test_truncated_counts_are_order_nk() -> None:
    for n in [10, 50, 200, 1000]:
        for k in [1, 2, 3, 5, 10, 30]:
            if k < n:
                cl, top = at_most_k(list(range(1, n + 1)), k, n)
                assert len(cl) <= 4 * n * k


def test_outputs_count_in_every_model() -> None:
    """Each model with at least t true inputs has r_t true (the upward lemma)."""
    rng = random.Random(7)
    for n in range(1, 8):
        for cap in range(1, n + 1):
            cl, outs, top = totalizer(list(range(1, n + 1)), cap, n)
            for bits in itertools.product([False, True], repeat=n):
                res = unit_propagate(cl, dict(zip(range(1, n + 1), bits)))
                assert res is not None
                t = sum(bits)
                for s, o in enumerate(outs, start=1):
                    assert (res.get(abs(o)) is True) == (s <= t)
                # a random completion that is a model obeys the lemma too
                full = {v: res.get(v, rng.random() < 0.5) for v in range(1, top + 1)}
                if satisfies(cl, full):
                    assert all(full[o] for o in outs[:t])


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
        for k in range(0, n):
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


def test_random_literals() -> None:
    rng = random.Random(2003)
    for _ in range(200):
        n = rng.randint(1, 6)
        xs = [v if rng.random() < 0.5 else -v for v in range(1, n + 1)]
        rng.shuffle(xs)
        k = rng.randint(0, n)
        cl, top = at_most_k(xs, k, n)
        want = {b for b in itertools.product([False, True], repeat=n)
                if sum(b[abs(x) - 1] == (x > 0) for x in xs) <= k}
        assert projected_models(cl, n, top) == want
