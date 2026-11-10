# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lamport-clocks/. The authors are listed in prov/R8TGNF.jsonl.

import random
from collections import deque

from lamport_clocks import random_execution, timestamp_execution, total_order_key

# The example of the page: p0 = P1, p1 = P2, p2 = P3.
# a: P1 sends m0 to P2; b: P1 local; c: P2 local; d: P2 receives m0;
# e: P2 sends m1 to P3; f: P3 local; g: P3 receives m1.
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


def test_example() -> None:
    assert timestamp_execution(3, EXAMPLE) == [1, 2, 1, 2, 3, 1, 4]


def test_converse_fails_on_example() -> None:
    c = timestamp_execution(3, EXAMPLE)
    hb = happened_before(EXAMPLE)
    b, e = 1, 4
    assert c[b] < c[e]
    assert e not in hb[b] and b not in hb[e]


def test_example_total_order() -> None:
    c = timestamp_execution(3, EXAMPLE)
    keys = [total_order_key(c[i], EXAMPLE[i][0]) for i in range(len(EXAMPLE))]
    order = sorted(range(len(EXAMPLE)), key=lambda i: keys[i])
    assert "".join("abcdefg"[i] for i in order) == "acfbdeg"


def test_edges() -> None:
    assert timestamp_execution(1, []) == []
    assert timestamp_execution(1, [(0, "local", None)] * 4) == [1, 2, 3, 4]
    # A receive jumps past a large timestamp.
    ex = [(0, "local", None)] * 5 + [(0, "send", (1, 0)), (1, "recv", 0), (1, "local", None)]
    assert timestamp_execution(2, ex)[-2:] == [7, 8]


def test_clock_condition_random() -> None:
    rng = random.Random(1978)
    for _ in range(300):
        n = rng.randint(1, 5)
        ex = random_execution(n, rng.randint(0, 40), rng)
        c = timestamp_execution(n, ex)
        hb = happened_before(ex)
        for e in range(len(ex)):
            for f in hb[e]:
                assert c[e] < c[f]


def test_total_order_extends_hb_random() -> None:
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(1, 5)
        ex = random_execution(n, rng.randint(0, 40), rng)
        c = timestamp_execution(n, ex)
        keys = [total_order_key(c[i], ex[i][0]) for i in range(len(ex))]
        assert len(set(keys)) == len(keys)  # a total order: no two events tie
        hb = happened_before(ex)
        for e in range(len(ex)):
            for f in hb[e]:
                assert keys[e] < keys[f]


def test_value_is_longest_chain_random() -> None:
    rng = random.Random(42)
    for _ in range(200):
        n = rng.randint(1, 4)
        ex = random_execution(n, rng.randint(0, 30), rng)
        c = timestamp_execution(n, ex)
        hb = happened_before(ex)
        depth = [1] * len(ex)
        for f in range(len(ex)):  # execution order is a topological order of ->
            for e in range(f):
                if f in hb[e]:
                    depth[f] = max(depth[f], depth[e] + 1)
        assert c == depth


def test_reverse_delivery_order() -> None:
    # Adversarial schedule: P0 sends 10 messages to P1, P1 receives them in reverse order.
    ex = [(0, "send", (1, k)) for k in range(10)] + [(1, "recv", k) for k in reversed(range(10))]
    c = timestamp_execution(2, ex)
    hb = happened_before(ex)
    for e in range(len(ex)):
        for f in hb[e]:
            assert c[e] < c[f]
    assert c[10] == 11 and c[-1] == 20
