# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-max-flow/. The authors are listed in prov/6669RS.jsonl.

import random

from distributed_max_flow import bottleneck_fan, edmonds_karp, push_relabel_pulses


def random_arcs(n: int, p: float, rng: random.Random) -> list[tuple[int, int, int]]:
    return [(u, v, rng.randrange(1, 9)) for u in range(n) for v in range(n) if u != v and rng.random() < p]


def check_flow(n: int, arcs: list[tuple[int, int, int]], s: int, t: int, st: dict) -> None:
    cap: dict[tuple[int, int], int] = {}
    for u, v, c in arcs:
        cap[(u, v)] = cap.get((u, v), 0) + c
        cap.setdefault((v, u), 0)
    f = st["flow"]
    for e, c in cap.items():
        assert f[e] <= c  # capacity
        assert f[e] == -f[(e[1], e[0])]  # skew symmetry
    for v in range(n):
        net = sum(f[e] for e in f if e[1] == v)
        if v not in (s, t):
            assert net == 0  # conservation: the preflow is a flow at the end
    assert sum(f[e] for e in f if e[1] == t) == st["value"]


def test_example() -> None:
    n, arcs, s, t = bottleneck_fan(3)
    st = push_relabel_pulses(n, arcs, s, t)
    assert st["value"] == 2
    assert (st["pulses"], st["rounds"], st["messages"], st["max_label"]) == (7, 15, 62, 6)


def test_matches_edmonds_karp() -> None:
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randrange(2, 14)
        arcs = random_arcs(n, rng.random() * 0.5, rng)
        st = push_relabel_pulses(n, arcs, 0, n - 1)
        assert st["value"] == edmonds_karp(n, arcs, 0, n - 1)
        check_flow(n, arcs, 0, n - 1, st)
        assert st["max_label"] <= 2 * n - 1  # the label bound of push-relabel
        assert st["pulses"] <= 4 * n * n


def test_rounds_grow_with_n_at_diameter_two() -> None:
    for k in (4, 8, 16, 32, 64):
        n, arcs, s, t = bottleneck_fan(k)
        st = push_relabel_pulses(n, arcs, s, t)
        assert st["value"] == k - 1 == edmonds_karp(n, arcs, s, t)
        assert st["pulses"] >= n  # the excess must climb back over s, at label n
