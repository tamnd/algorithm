# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/matrix-clocks/. The authors are listed in prov/J3RKBA.jsonl.

import random
from collections import deque

from matrix_clocks import MatrixClock, random_execution, timestamp_execution

EXAMPLE = [
    (0, "send", (1, 0)),  # a
    (0, "local", None),  # b
    (1, "local", None),  # c
    (1, "recv", 0),  # d
    (1, "send", (2, 1)),  # e
    (2, "local", None),  # f
    (2, "recv", 1),  # g
]


def causal_past(execution: list[tuple]) -> list[set[int]]:
    """Oracle: past[e] = {g : g -> e} plus e itself, by BFS backwards on the event graph."""
    pred: list[list[int]] = [[] for _ in execution]
    last: dict[int, int] = {}
    send_of: dict[int, int] = {}
    for e, (p, kind, x) in enumerate(execution):
        if p in last:
            pred[e].append(last[p])
        last[p] = e
        if kind == "send":
            send_of[x[1]] = e
        elif kind == "recv":
            pred[e].append(send_of[x])
    out = []
    for e in range(len(execution)):
        seen = {e}
        todo = deque(pred[e])
        while todo:
            g = todo.popleft()
            if g not in seen:
                seen.add(g)
                todo.extend(pred[g])
        out.append(seen)
    return out


def check_run(n: int, ex: list[tuple]) -> None:
    mats = timestamp_execution(n, ex)
    past = causal_past(ex)

    def vec(g: int | None) -> tuple[int, ...]:
        if g is None:
            return (0,) * n
        return tuple(sum(1 for h in past[g] if ex[h][0] == k) for k in range(n))

    for e in range(len(ex)):
        for j in range(n):
            mine = [g for g in past[e] if ex[g][0] == j]
            g_j = max(mine) if mine else None
            # Row j is the vector clock of the latest event of p_j in the causal past of e.
            assert mats[e][j] == vec(g_j)
        assert mats[e][ex[e][0]] == vec(e)
        # Knowledge claim behind garbage collection.
        for k in range(n):
            t = min(mats[e][row][k] for row in range(n))
            for j in range(n):
                mine = [g for g in past[e] if ex[g][0] == j]
                g_j = max(mine) if mine else None
                assert vec(g_j)[k] >= t


def test_example() -> None:
    mats = timestamp_execution(3, EXAMPLE)
    assert mats[6] == ((1, 0, 0), (1, 3, 0), (1, 3, 2))  # g
    assert mats[3] == ((1, 0, 0), (1, 2, 0), (0, 0, 0))  # d
    check_run(3, EXAMPLE)


def test_known_by_all() -> None:
    c = [MatrixClock(2, 0), MatrixClock(2, 1)]
    w = c[0].send()
    c[1].receive(w, 0)
    assert c[1].known_by_all(0) == 1
    assert c[0].known_by_all(0) == 0  # p0 does not yet know that p1 received
    back = c[1].send()
    c[0].receive(back, 1)
    assert c[0].known_by_all(0) == 1


def test_random_runs() -> None:
    rng = random.Random(1984)
    for _ in range(500):
        n = rng.randint(1, 4)
        check_run(n, random_execution(n, rng.randint(0, 20), rng))


def test_reverse_delivery() -> None:
    ex = [(0, "send", (1, k)) for k in range(5)] + [(1, "recv", k) for k in reversed(range(5))]
    ex += [(1, "send", (2, 5)), (2, "recv", 5), (2, "send", (0, 6)), (0, "recv", 6)]
    check_run(3, ex)
