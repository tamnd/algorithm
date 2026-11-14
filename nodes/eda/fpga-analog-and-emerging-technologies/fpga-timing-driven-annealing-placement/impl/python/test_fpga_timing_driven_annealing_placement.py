# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fpga-timing-driven-annealing-placement/. The authors are listed in prov/ZDNXW1.jsonl.

import math
import random

from fpga_timing_driven_annealing_placement import (
    Placer,
    alpha,
    bb_cost,
    connections,
    criticalities,
    delay,
    exhaustive_min_bb,
    net_bb,
    q,
)


def random_nets(rng: random.Random, n_blocks: int, n_nets: int, max_fanout: int) -> list[list[int]]:
    """Each net is driven by a block and read by later blocks, so the connections form a DAG."""
    nets = []
    for _ in range(n_nets):
        d = rng.randrange(n_blocks - 1)
        sinks = rng.sample(range(d + 1, n_blocks), rng.randint(1, min(max_fanout, n_blocks - 1 - d)))
        nets.append([d] + sinks)
    return nets


def brute_criticalities(n_blocks, conns, loc):
    d = [delay(loc[u], loc[v]) for u, v in conns]

    def longest_to(v):
        return max((longest_to(u) + d[i] for i, (u, w) in enumerate(conns) if w == v), default=0)

    def longest_from(v):
        return max((d[i] + longest_from(w) for i, (u, w) in enumerate(conns) if u == v), default=0)

    dmax = max(longest_to(v) for v in range(n_blocks))
    return [(longest_to(u) + d[i] + longest_from(v)) / dmax for i, (u, v) in enumerate(conns)]


def test_small_functions():
    assert [q(n) for n in (1, 2, 3)] == [1.0, 1.0, 1.0]
    assert q(4) > 1 and q(50) > q(10) > q(4)
    assert delay((0, 0), (2, 1)) == 4
    assert net_bb([0, 1, 2], [(0, 0), (2, 1), (1, 3)]) == (3 + 4)
    assert [alpha(r) for r in (0.99, 0.9, 0.5, 0.1)] == [0.5, 0.9, 0.95, 0.8]


def test_page_example():
    nets = [[0, 1], [1, 2]]
    p = Placer(3, 2, 3, nets)
    p.loc = [(0, 0), (2, 0), (0, 1)]
    p.weight = criticalities(3, p.conns, p.loc)
    assert p.weight == [1.0, 1.0]
    assert bb_cost(nets, p.loc) == 9 and p.timing_cost() == 7
    assert p._move_delta(1, None, (1, 0)) == (-2, -2)


def test_criticalities_match_path_enumeration():
    rng = random.Random(4)
    for _ in range(200):
        n = rng.randint(2, 7)
        nets = random_nets(rng, n, rng.randint(1, 5), 3)
        conns = connections(nets)
        loc = [(rng.randrange(4), rng.randrange(4)) for _ in range(n)]
        got = criticalities(n, conns, loc)
        want = brute_criticalities(n, conns, loc)
        assert all(math.isclose(a, b) for a, b in zip(got, want))
        assert max(got) == 1.0


def test_incremental_cost_equals_recomputation():
    rng = random.Random(7)
    for trial in range(6):
        n = rng.randint(8, 14)
        nets = random_nets(rng, n, n, 4)
        p = Placer(4, 4, n, nets, lam=0.5 if trial % 2 else 0.0, check_every_move=True)
        loc = p.place(random.Random(trial))
        assert len(set(loc)) == n
        assert all(0 <= x < 4 and 0 <= y < 4 for x, y in loc)


def test_never_below_exhaustive_optimum():
    rng = random.Random(1)
    equal = 0
    trials = 40
    for trial in range(trials):
        nx, ny = 3, 2
        n = rng.randint(3, 5)
        nets = random_nets(rng, n, rng.randint(2, 5), 3)
        best = exhaustive_min_bb(nx, ny, n, nets)
        p = Placer(nx, ny, n, nets, lam=0.0, inner=4.0)
        loc = p.place(random.Random(100 + trial))
        got = bb_cost(nets, loc)
        assert got >= best - 1e-9
        equal += math.isclose(got, best)
    assert equal >= trials * 3 // 4


def test_annealing_beats_random_placement():
    rng = random.Random(2)
    n = 25
    nets = random_nets(rng, n, 30, 3)
    sites = [(x, y) for x in range(5) for y in range(5)]
    rng.shuffle(sites)
    start = bb_cost(nets, sites[:n])
    p = Placer(5, 5, n, nets, lam=0.5, inner=2.0)
    loc = p.place(random.Random(3))
    assert bb_cost(nets, loc) < start
