# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conflict-graph/. The authors are listed in prov/R82KKG.jsonl.

import itertools
import random

from conflict_graph import (
    committed_projection,
    conflict,
    conflict_equivalent,
    conflict_graph,
    find_cycle,
    parse,
    serial_order,
    serial_schedule,
)


def random_schedule(rng: random.Random, ntx: int, nops: int, items: str) -> list:
    """Interleave ntx transactions with nops random actions each."""
    tx = {t: [(rng.choice("rw"), t, rng.choice(items)) for _ in range(nops)] for t in range(1, ntx + 1)}
    out = []
    while any(tx.values()):
        t = rng.choice([t for t in tx if tx[t]])
        out.append(tx[t].pop(0))
    return out


def test_worked_example() -> None:
    s = parse("r1(x) r2(y) w1(x) r3(x) w3(z) w2(z)")
    g = conflict_graph(s)
    assert g == {1: {3}, 2: set(), 3: {2}}
    assert serial_order(g) == [1, 3, 2]
    assert find_cycle(g) is None
    assert conflict_equivalent(s, serial_schedule(s, [1, 3, 2]))


def test_cycle_example() -> None:
    s = parse("r1(x) r2(y) w1(y) w2(x)")
    g = conflict_graph(s)
    assert g == {1: {2}, 2: {1}}
    assert serial_order(g) is None
    assert find_cycle(g) == [1, 2]


def test_projection_drops_aborted() -> None:
    s = parse("w1(x) r2(x) a1 c2")
    assert committed_projection(s) == [("r", 2, "x")]
    assert committed_projection(parse("r1(x) w2(x)")) == parse("r1(x) w2(x)")


def test_edges_against_pair_scan() -> None:
    rng = random.Random(7)
    for _ in range(300):
        s = random_schedule(rng, rng.randint(1, 4), rng.randint(1, 4), "xyz")
        want: dict[int, set[int]] = {t: set() for _, t, _ in s}
        for i, j in itertools.combinations(range(len(s)), 2):
            if conflict(s[i], s[j]):
                want[s[i][1]].add(s[j][1])
        assert conflict_graph(s) == want


def test_order_and_cycle_agree() -> None:
    rng = random.Random(11)
    for _ in range(400):
        s = random_schedule(rng, rng.randint(2, 5), rng.randint(1, 3), "xy")
        g = conflict_graph(s)
        order = serial_order(g)
        cyc = find_cycle(g)
        assert (order is None) == (cyc is not None)
        if order is not None:
            pos = {t: i for i, t in enumerate(order)}
            assert all(pos[u] < pos[v] for u in g for v in g[u])
            assert conflict_equivalent(s, serial_schedule(s, order))
        else:
            k = len(cyc)
            assert len(set(cyc)) == k
            assert all(cyc[(i + 1) % k] in g[cyc[i]] for i in range(k))


def test_topological_orders_are_exactly_the_equivalent_serial_orders() -> None:
    rng = random.Random(3)
    for _ in range(150):
        s = random_schedule(rng, rng.randint(2, 4), rng.randint(1, 3), "xy")
        g = conflict_graph(s)
        for perm in itertools.permutations(sorted(g)):
            pos = {t: i for i, t in enumerate(perm)}
            topo = all(pos[u] < pos[v] for u in g for v in g[u])
            assert topo == conflict_equivalent(s, serial_schedule(s, list(perm)))
