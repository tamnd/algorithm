# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vector-clocks/. The authors are listed in prov/GQ5H12.jsonl.

import random
from collections import deque

from vector_clocks import VectorClock, concurrent, leq, less, less_fast, random_execution, timestamp_execution

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


def check_run(n: int, ex: list[tuple]) -> None:
    v = timestamp_execution(n, ex)
    hb = happened_before(ex)
    for e in range(len(ex)):
        # V(e)[k] counts the events of p_k in the causal past of e, e included.
        for k in range(n):
            past = sum(1 for g in range(len(ex)) if ex[g][0] == k and (g == e or e in hb[g]))
            assert v[e][k] == past
        for f in range(len(ex)):
            if e == f:
                continue
            assert less(v[e], v[f]) == (f in hb[e])
            assert concurrent(v[e], v[f]) == (f not in hb[e] and e not in hb[f])
            assert less_fast(v[e], ex[e][0], v[f]) == (f in hb[e])


def test_example() -> None:
    v = timestamp_execution(3, EXAMPLE)
    assert v == [(1, 0, 0), (2, 0, 0), (0, 1, 0), (1, 2, 0), (1, 3, 0), (0, 0, 1), (1, 3, 2)]
    assert concurrent(v[1], v[4])  # b || e
    assert less(v[0], v[6])  # a -> g
    check_run(3, EXAMPLE)


def test_operations() -> None:
    c = VectorClock(3, 1)
    assert c.tick() == (0, 1, 0)
    assert c.receive((4, 0, 2)) == (4, 2, 2)
    assert leq((0, 0), (0, 0)) and not less((0, 0), (0, 0))
    assert concurrent((1, 0), (0, 1))


def test_characterization_random() -> None:
    rng = random.Random(1988)
    for _ in range(500):
        n = rng.randint(1, 5)
        check_run(n, random_execution(n, rng.randint(0, 25), rng))


def test_reverse_and_delayed_delivery() -> None:
    # Reverse order: P0 sends 6 messages to P1 and P1 takes them last first.
    ex = [(0, "send", (1, k)) for k in range(6)] + [(1, "recv", k) for k in reversed(range(6))]
    check_run(2, ex)
    # One delayed process: P2 receives everything only at the end.
    rng = random.Random(3)
    for _ in range(50):
        ex = []
        held = []
        mid = 0
        for _ in range(20):
            p = rng.randrange(3)
            q = rng.choice([x for x in range(3) if x != p])
            ex.append((p, "send", (q, mid)))
            if q == 2:
                held.append(mid)
            else:
                ex.append((q, "recv", mid))
            mid += 1
        ex += [(2, "recv", m) for m in held]
        check_run(3, ex)
