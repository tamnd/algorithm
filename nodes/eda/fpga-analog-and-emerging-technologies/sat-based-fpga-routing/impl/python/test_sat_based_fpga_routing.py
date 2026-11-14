# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sat-based-fpga-routing/. The authors are listed in prov/1K07JP.jsonl.

import itertools
import random

from sat_based_fpga_routing import (
    disjoint_pattern,
    encode,
    exhaustive_route,
    is_legal,
    min_width,
    sat_route,
    twisted_pattern,
)
from small_dpll import solve

KINDS = ["WN", "NE", "ES", "SW", "EW", "NS"]
W_SIDE, N_SIDE, E_SIDE = 0, 1, 2
PAGE_NETS = [
    ([W_SIDE, N_SIDE], [(W_SIDE, N_SIDE, "WN")]),
    ([N_SIDE, E_SIDE], [(N_SIDE, E_SIDE, "NE")]),
    ([E_SIDE, W_SIDE], [(E_SIDE, W_SIDE, "EW")]),
]


def random_nets(rng, n_segments, n_nets, max_len):
    nets = []
    for _ in range(n_nets):
        segs = rng.sample(range(n_segments), rng.randint(1, max_len))
        edges = [(segs[rng.randrange(i)], segs[i], rng.choice(KINDS)) for i in range(1, len(segs))]
        nets.append((segs, edges))
    return nets


def random_pattern(rng, w):
    table = {(k, t): set(rng.sample(range(w), rng.randint(1, w))) for k in KINDS for t in range(w)}
    return lambda kind, t, width: table[(kind, t)]


def brute_sat(n, clauses):
    for bits in itertools.product([False, True], repeat=n):
        if all(any(bits[abs(l) - 1] == (l > 0) for l in c) for c in clauses):
            return True
    return False


def test_small_dpll_matches_truth_tables():
    rng = random.Random(9)
    for _ in range(300):
        n = rng.randint(1, 7)
        clauses = [[rng.choice([-1, 1]) * rng.randint(1, n) for _ in range(rng.randint(1, 3))] for _ in range(rng.randint(1, 20))]
        model = solve(n, clauses)
        assert (model is not None) == brute_sat(n, clauses)
        if model is not None:
            assert all(any(model[abs(l)] == (l > 0) for l in c) for c in clauses)


def test_page_example():
    n_vars, clauses, _ = encode(PAGE_NETS, 2, twisted_pattern)
    assert (n_vars, len(clauses)) == (12, 24)
    assert sat_route(PAGE_NETS, 2, disjoint_pattern) is None
    assert exhaustive_route(PAGE_NETS, 2, disjoint_pattern) is None
    assert min_width(PAGE_NETS, disjoint_pattern, 4) == 3
    tracks = sat_route(PAGE_NETS, 2, twisted_pattern)
    assert tracks is not None and is_legal(PAGE_NETS, 2, twisted_pattern, tracks)
    assert min_width(PAGE_NETS, twisted_pattern, 4) == 2


def test_agrees_with_exhaustive_search():
    rng = random.Random(1)
    sat = unsat = 0
    while sat < 60 or unsat < 60:
        w = rng.randint(1, 3)
        nets = random_nets(rng, 4, rng.randint(1, 4), 3)
        keys = sum(len(segs) for segs, _ in nets)
        if w ** keys > 5000:
            continue
        pattern = random_pattern(rng, w)
        got = sat_route(nets, w, pattern)
        want = exhaustive_route(nets, w, pattern)
        assert (got is None) == (want is None)
        if got is None:
            unsat += 1
        else:
            assert is_legal(nets, w, pattern, got)
            sat += 1


def test_models_correspond_one_to_one_to_routings():
    """The number of models of the CNF equals the number of legal detailed routings."""
    rng = random.Random(3)
    for _ in range(40):
        w = rng.randint(1, 3)
        nets = random_nets(rng, 3, rng.randint(1, 3), 2)
        pattern = random_pattern(rng, w)
        n_vars, clauses, _ = encode(nets, w, pattern)
        if n_vars > 14:
            continue
        models = sum(
            all(any(bits[abs(l) - 1] == (l > 0) for l in c) for c in clauses)
            for bits in itertools.product([False, True], repeat=n_vars)
        )
        keys = [(n, s) for n, (segs, _) in enumerate(nets) for s in segs]
        routings = sum(
            is_legal(nets, w, pattern, dict(zip(keys, choice))) for choice in itertools.product(range(w), repeat=len(keys))
        )
        assert models == routings


def test_disjoint_pattern_is_graph_coloring():
    """With the disjoint pattern a net keeps one track, so routability is W-colorability of the conflict graph."""
    rng = random.Random(2)
    for _ in range(150):
        nets = random_nets(rng, 5, rng.randint(2, 6), 3)
        conflicts = [(a, b) for a, b in itertools.combinations(range(len(nets)), 2) if set(nets[a][0]) & set(nets[b][0])]
        for w in (1, 2, 3):
            colorable = any(
                all(col[a] != col[b] for a, b in conflicts) for col in itertools.product(range(w), repeat=len(nets))
            )
            assert (sat_route(nets, w, disjoint_pattern) is not None) == colorable


def test_min_width_matches_exhaustive():
    rng = random.Random(4)
    for _ in range(40):
        nets = random_nets(rng, 3, rng.randint(1, 3), 2)
        want = next(w for w in range(1, 5) if exhaustive_route(nets, w, disjoint_pattern) is not None)
        assert min_width(nets, disjoint_pattern, 4) == want
