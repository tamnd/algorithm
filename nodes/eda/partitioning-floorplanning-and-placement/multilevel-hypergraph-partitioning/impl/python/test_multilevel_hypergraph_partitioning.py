# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multilevel-hypergraph-partitioning/. The authors are listed in prov/FYFXXW.jsonl.

import random

from multilevel_hypergraph_partitioning import (
    coarsen,
    cut_weight,
    fm_refine,
    multilevel_hypergraph_partitioning,
)


def exhaustive_best(n: int, nets, netw, lo: int, hi: int) -> int:
    """Least cut over all 2^n assignments with lo <= |side 0| <= hi (the brute force)."""
    masks = [sum(1 << v for v in e) for e in nets]
    full = (1 << n) - 1
    best = None
    for s in range(1 << n):
        if not lo <= bin(s).count("1") <= hi:
            continue
        c = 0
        for m, w in zip(masks, netw):
            if m & s and m & (full ^ s):
                c += w
        if best is None or c < best:
            best = c
    return best


def random_hypergraph(rng: random.Random, n: int, m: int) -> list[list[int]]:
    nets = []
    for _ in range(m):
        size = rng.choice([2, 2, 2, 3, 3, 4, 5])
        nets.append(rng.sample(range(n), min(size, n)))
    return nets


def page_example():
    # Two clusters {0..4} and {5..9} joined by the nets {4, 5} and {2, 3, 7}.
    nets = [[0, 1, 2], [1, 2, 3], [0, 3, 4], [2, 4], [0, 1], [5, 6, 7], [6, 7, 8], [5, 8, 9], [7, 9], [5, 6], [4, 5], [2, 3, 7]]
    return 10, nets


def test_page_example():
    n, nets = page_example()
    side = multilevel_hypergraph_partitioning(n, nets, 4, 6, random.Random(7))
    assert 4 <= side.count(0) <= 6
    c = cut_weight(nets, [1] * len(nets), side)
    assert c == 2 == exhaustive_best(n, nets, [1] * len(nets), 4, 6)


def test_coarsening_keeps_cut_and_weight():
    rng = random.Random(11)
    for _ in range(200):
        n = rng.randint(2, 12)
        nets = [sorted(set(e)) for e in random_hypergraph(rng, n, rng.randint(1, 15))]
        netw = [rng.randint(1, 3) for _ in nets]
        vw = [1] * n
        for scheme in ("hec", "ec"):
            cap = rng.randint(1, 4)
            cmap, k, cn, cw, cv = coarsen(n, nets, netw, vw, cap, rng, scheme)
            assert sum(cv) == n and max(cv) <= cap and k <= n
            assert all(len(e) >= 2 for e in cn) and len({tuple(e) for e in cn}) == len(cn)
            # Every coarse partition projects to a fine partition with the same cut.
            for _ in range(5):
                cs = [rng.randint(0, 1) for _ in range(k)]
                fs = [cs[cmap[v]] for v in range(n)]
                assert cut_weight(cn, cw, cs) == cut_weight(nets, netw, fs)
            # Restricted coarsening merges only vertices on the same side.
            side = [rng.randint(0, 1) for _ in range(n)]
            cmap, k, cn, cw, cv = coarsen(n, nets, netw, vw, cap, rng, scheme, side)
            for u in range(n):
                for v in range(n):
                    if cmap[u] == cmap[v]:
                        assert side[u] == side[v]


def test_fm_refine_never_worse_and_balanced():
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(2, 10)
        nets = [sorted(set(e)) for e in random_hypergraph(rng, n, rng.randint(1, 12))]
        netw = [rng.randint(1, 3) for _ in nets]
        vw = [rng.randint(1, 2) for _ in range(n)]
        side = [rng.randint(0, 1) for _ in range(n)]
        w0 = sum(vw[v] for v in range(n) if side[v] == 0)
        lo, hi = max(0, w0 - rng.randint(0, 2)), w0 + rng.randint(0, 2)
        out = fm_refine(n, nets, netw, vw, side, lo, hi)
        assert lo <= sum(vw[v] for v in range(n) if out[v] == 0) <= hi
        assert cut_weight(nets, netw, out) <= cut_weight(nets, netw, side)


def test_against_exhaustive_bisection():
    rng = random.Random(2026)
    for trial in range(300):
        n = rng.randint(2, 12) if trial < 260 else 14
        nets = random_hypergraph(rng, n, rng.randint(1, 2 * n))
        netw = [rng.randint(1, 2) for _ in nets]
        half = n // 2
        slack = rng.choice([0, 1, 2])
        lo, hi = max(0, half - slack), min(n, half + slack)
        scheme = rng.choice(["hec", "ec"])
        side = multilevel_hypergraph_partitioning(n, nets, lo, hi, random.Random(trial), netw=netw, scheme=scheme, coarsest=rng.choice([2, 4, 8]))
        assert len(side) == n and set(side) <= {0, 1}
        assert lo <= side.count(0) <= hi
        c = cut_weight(nets, netw, side)
        # The cut recomputed by bitmasks agrees.
        full = (1 << n) - 1
        s = sum(1 << v for v in range(n) if side[v] == 0)
        masks = [sum(1 << v for v in e) for e in nets]
        assert c == sum(w for m, w in zip(masks, netw) if m & s and m & (full ^ s))
        assert c >= exhaustive_best(n, nets, netw, lo, hi)


def test_edge_cases():
    assert multilevel_hypergraph_partitioning(1, [], 0, 1, random.Random(0)) in ([0], [1])
    side = multilevel_hypergraph_partitioning(4, [[0, 1, 2, 3]], 2, 2, random.Random(0))
    assert side.count(0) == 2
    side = multilevel_hypergraph_partitioning(6, [[0, 1], [0, 1], [2, 3]], 3, 3, random.Random(1))
    assert side.count(0) == 3
