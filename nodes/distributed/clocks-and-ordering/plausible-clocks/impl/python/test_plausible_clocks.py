# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plausible-clocks/. The authors are listed in prov/DY2814.jsonl.

import random
from collections import deque

from plausible_clocks import (
    CombClock,
    KLAClock,
    REVClock,
    comb_before,
    kla_before,
    random_execution,
    rev_before,
    timestamp_execution,
)

EXAMPLE = [
    (0, "send", (1, 0)),  # a
    (0, "local", None),  # b
    (1, "local", None),  # c
    (1, "recv", 0),  # d
    (1, "send", (2, 1)),  # e
    (2, "local", None),  # f
    (2, "recv", 1),  # g
]


def happened_before(execution: list[tuple]) -> list[set[int]]:
    """Oracle: hb[e] is the set of events f with e -> f, by BFS on the event graph."""
    succ: list[list[int]] = [[] for _ in execution]
    last: dict[int, int] = {}
    send_of: dict[int, int] = {}
    for e, (p, kind, x) in enumerate(execution):
        if p in last:
            succ[last[p]].append(e)
        last[p] = e
        if kind == "send":
            send_of[x[1]] = e
        elif kind == "recv":
            succ[send_of[x]].append(e)
    out = []
    for e in range(len(execution)):
        seen: set[int] = set()
        todo = deque(succ[e])
        while todo:
            f = todo.popleft()
            if f not in seen:
                seen.add(f)
                todo.extend(succ[f])
        out.append(seen)
    return out


def false_orders(stamps: list, before, hb: list[set[int]]) -> set[tuple[int, int]]:
    """Check plausibility and return the concurrent pairs that the clock orders."""
    wrong = set()
    for e in range(len(stamps)):
        for f in range(len(stamps)):
            if e == f:
                continue
            assert not (before(stamps[e], stamps[f]) and before(stamps[f], stamps[e]))
            if f in hb[e]:
                assert before(stamps[e], stamps[f])  # a causal pair is never missed
                assert not before(stamps[f], stamps[e])  # and never reversed
            elif e not in hb[f] and before(stamps[e], stamps[f]):
                wrong.add((e, f))
    return wrong


def run_all(n: int, ex: list[tuple], r: int, k: int) -> tuple[int, int, int]:
    hb = happened_before(ex)
    rev = timestamp_execution([REVClock(p, r) for p in range(n)], ex)
    kla = timestamp_execution([KLAClock(p, k) for p in range(n)], ex)
    comb = timestamp_execution([CombClock(p, r, k) for p in range(n)], ex)
    w_rev = false_orders(rev, lambda a, b: rev_before(a, b, r), hb)
    w_kla = false_orders(kla, kla_before, hb)
    w_comb = false_orders(comb, lambda a, b: comb_before(a, b, r), hb)
    assert w_comb <= w_rev and w_comb <= w_kla
    # Equal stamps only for the same event.
    for stamps in (rev, kla):
        keys = [(s, v[s % r]) if stamps is rev else (s, v[0]) for s, v in stamps]
        assert len(set(keys)) == len(keys)
    return len(w_rev), len(w_kla), len(w_comb)


def test_example_rev_false_order() -> None:
    rev = timestamp_execution([REVClock(p, 2) for p in range(3)], EXAMPLE)
    b, f = rev[1], rev[5]
    assert b == (0, (2, 0)) and f == (2, (1, 0))
    assert rev_before(f, b, 2)  # f || b in truth, but REV with R = 2 orders f before b
    run_all(3, EXAMPLE, 2, 3)


def test_rev_with_r_equal_n_is_exact() -> None:
    rng = random.Random(5)
    for _ in range(100):
        n = rng.randint(1, 4)
        ex = random_execution(n, rng.randint(0, 20), rng)
        assert run_all(n, ex, n, 2)[0] == 0


def test_plausible_random() -> None:
    rng = random.Random(1999)
    for _ in range(500):
        n = rng.randint(1, 6)
        ex = random_execution(n, rng.randint(0, 20), rng)
        run_all(n, ex, rng.randint(1, 3), rng.randint(2, 4))


def test_reverse_delivery() -> None:
    ex = [(0, "send", (1, k)) for k in range(4)] + [(2, "send", (1, 4)), (1, "recv", 4)]
    ex += [(1, "recv", k) for k in reversed(range(4))] + [(3, "local", None), (1, "send", (3, 5)), (3, "recv", 5)]
    run_all(4, ex, 2, 3)
