# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aks-sorting-network/. The authors are listed in prov/9EWBX0.jsonl.

import random

from aks_sorting_network import aks_network, aks_sorting_network, expander_halver, halver_error, stages


def run_zero_one(net: list[tuple[int, int]], order: list[int], n: int) -> bool:
    """Run all 2^n inputs at once: bit v of wire[k] is item k of input v."""
    m = 1 << n
    wire = []
    for k in range(n):
        h = 1 << k
        wire.append((((1 << h) - 1) << h) * (((1 << m) - 1) // ((1 << (2 * h)) - 1)))
    for i, j in net:
        wire[i], wire[j] = wire[i] & wire[j], wire[i] | wire[j]
    out = [wire[r] for r in order]
    return all(out[k] & ~out[k + 1] == 0 for k in range(n - 1))


def test_example() -> None:
    a = [11, 3, 14, 0, 9, 6, 15, 1, 12, 5, 8, 2, 13, 7, 10, 4]
    aks_sorting_network(a)
    assert a == list(range(16))


def test_stage_counts() -> None:
    assert [stages(1 << k) for k in range(1, 11)] == [0, 0, 5, 12, 19, 26, 33, 40, 47, 54]


def test_all_zero_one_inputs() -> None:
    for n in (2, 4, 8, 16):
        net, order = aks_network(n)
        assert run_zero_one(net, order, n)
        assert sorted(order) == list(range(n))


def test_permutations_large() -> None:
    rng = random.Random(7)
    for n in (32, 64, 128, 256):
        net, order = aks_network(n)
        for _ in range(20):
            x = list(range(n))
            rng.shuffle(x)
            for i, j in net:
                if x[j] < x[i]:
                    x[i], x[j] = x[j], x[i]
            assert [x[r] for r in order] == list(range(n))


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 2], [3, 3, 3], [5, 4, 3, 2, 1], list(range(40, 0, -1)), ["b", "a", "c"]):
        b = list(a)
        aks_sorting_network(b)
        assert b == sorted(a)


def test_halvers() -> None:
    # A single matching between the halves is a 1/2-halver and no better.
    assert halver_error(expander_halver(4, 1, 1), 4) == 0.5
    # The complete bipartite graph K_{m,m}, as m matchings, is an exact halver.
    m = 4
    layers = [[(u, m + (u + s) % m) for u in range(m)] for s in range(m)]
    assert halver_error(layers, m) == 0
    # A layer only moves zeros down and ones up, so more layers never increase the error.
    errors = [halver_error(expander_halver(6, d, 3), 6) for d in range(1, 5)]
    assert errors == sorted(errors, reverse=True)


def test_random() -> None:
    rng = random.Random(2024)
    for _ in range(600):
        n = rng.randrange(0, 70)
        a = [rng.randrange(-20, 20) for _ in range(n)]
        b = list(a)
        aks_sorting_network(b)
        assert b == sorted(a)
