# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simulated-annealing-placement/. The authors are listed in prov/ZEMFMQ.jsonl.

import random
from fractions import Fraction
from itertools import permutations

from simulated_annealing_placement import (
    State,
    anneal,
    full_cost,
    overlap,
    pack_rows,
    propose,
)


def instance(rng, n, K, S, q=4):
    pads = [(0, rng.randint(0, K)), (S, rng.randint(0, K)), (rng.randint(0, S), 0), (rng.randint(0, S), K)][:q]
    nets = []
    for i in range(n):  # every cell is on a net to a pad or to an earlier cell
        nets.append([i, n + rng.randrange(q)] if i == 0 or rng.random() < 0.3 else [i, rng.randrange(i)])
    for _ in range(n // 2):
        nets.append(rng.sample(range(n + q), rng.randint(2, 3)))
    return nets, pads


def legal(x, r, W, K, S):
    used = set()
    for i in range(len(x)):
        if not (0 <= r[i] < K and 0 <= x[i] and x[i] + W[i] <= S):
            return False
        for s in range(x[i], x[i] + W[i]):
            if (r[i], s) in used:
                return False
            used.add((r[i], s))
    return True


def direct_hpwl(x, r, W, nets, pads):
    """HPWL from scratch with exact fractions: the pin of cell i is at (x + W/2, r + 1/2)."""
    n = len(x)
    total = Fraction(0)
    for e in nets:
        pts = [(x[p] + Fraction(W[p], 2), r[p] + Fraction(1, 2)) if p < n else tuple(map(Fraction, pads[p - n]))
               for p in e]
        xs, ys = zip(*pts)
        total += max(xs) - min(xs) + max(ys) - min(ys)
    return total


def exhaustive_optimum(n, nets, pads, K, S):
    """The least HPWL over all placements of n unit cells on distinct sites, from doubled integers."""
    sites = [(2 * s + 1, 2 * r + 1) for r in range(K) for s in range(S)]
    pad2 = [(2 * a, 2 * b) for a, b in pads]
    best = None
    for perm in permutations(sites, n):
        pts = list(perm) + pad2
        total = 0
        for e in nets:
            xs = [pts[p][0] for p in e]
            ys = [pts[p][1] for p in e]
            total += max(xs) - min(xs) + max(ys) - min(ys)
        if best is None or total < best:
            best = total
    return Fraction(best, 2)


def test_incremental_delta_equals_full_recomputation():
    rng = random.Random(1)
    for _ in range(30):
        n, K, S = rng.randint(2, 10), rng.randint(1, 4), rng.randint(3, 8)
        W = [rng.choice([1, 1, 2, 3]) for _ in range(n)]
        nets, pads = instance(rng, n, K, S)
        mu = rng.randint(1, 5)
        st = State([rng.randint(0, S - w) for w in W], [rng.randrange(K) for _ in range(n)], W, nets, pads, K, S, mu)
        assert st.cost == full_cost(st.x, st.r, W, nets, pads, K, S, mu)
        for _ in range(100):
            mv = propose(st, rng, rng.randint(1, S), rng.randint(1, K), 0.5)
            if mv is None:
                continue
            before = st.cost
            d, back = st.apply(mv)
            assert st.cost == full_cost(st.x, st.r, W, nets, pads, K, S, mu) == before + d
            assert st.over == overlap(st.x, st.r, W, K, S)
            if rng.random() < 0.5:
                st.apply(back)
                assert st.cost == before


def test_page_example_of_one_swap_and_one_displacement():
    # One row of 4 sites; cells a, b, c at sites 0, 1, 2; nets {a, c} and {b, pad at (0, 0)}.
    W, K, S = [1, 1, 1], 1, 4
    nets = [[0, 2], [1, 3]]
    pads = [(0, 0)]
    st = State([0, 1, 2], [0, 0, 0], W, nets, pads, K, S, 8)
    assert st.cost == 8  # HPWL 4: {a, c} spans 2, {b, pad} spans 1.5 in x and 0.5 in y
    d, _ = st.apply([(0, 1, 0), (1, 0, 0)])  # swap a and b
    assert d == -4  # HPWL falls by 2
    d, _ = st.apply([(2, 3, 0)])  # move c one site right
    assert d == 2  # HPWL rises by 1
    d, _ = st.apply([(2, 1, 0)])  # move c onto a
    assert d == -2 * 2 + 8 * 1 == 4  # HPWL falls by 2, one site is now shared


def test_zero_temperature_never_raises_the_cost():
    rng = random.Random(4)
    for seed in range(5):
        n, K, S = 12, 3, 6
        nets, pads = instance(rng, n, K, S)
        trace = []
        anneal(n, nets, pads, [1] * n, K, S, seed=seed, T0=1e-6, T_end=1e-9, alpha=0.5, trace=trace)
        costs = [c for _, c in trace]
        assert all(b <= a for a, b in zip(costs, costs[1:]))


def test_pack_rows_is_legal():
    rng = random.Random(5)
    for _ in range(300):
        K, S = rng.randint(1, 5), rng.randint(3, 10)
        W = []
        while sum(W) < 0.8 * K * S - 2:
            W.append(rng.choice([1, 1, 1, 2]))
        x = [rng.randint(0, S - w) for w in W]
        r = [rng.randrange(K) for _ in W]
        try:
            nx, nr = pack_rows(x, r, W, K, S)
        except ValueError:
            continue
        assert legal(nx, nr, W, K, S)


def test_anneal_is_legal_and_its_cost_matches_a_direct_sum():
    rng = random.Random(11)
    for seed in range(2):
        n, K, S = 30, 6, 10
        W = [rng.choice([1, 1, 2]) for _ in range(n)]
        nets, pads = instance(rng, n, K, S)
        x, r = anneal(n, nets, pads, W, K, S, seed=seed, moves_per_cell=8)
        assert legal(x, r, W, K, S)
        assert 2 * direct_hpwl(x, r, W, nets, pads) == full_cost(x, r, W, nets, pads, K, S, 0)


def test_anneal_never_beats_the_exhaustive_optimum_on_6_cells():
    rng = random.Random(10)
    for seed in range(3):
        n, K, S = 6, 2, 4
        nets, pads = instance(rng, n, K, S)
        x, r = anneal(n, nets, pads, [1] * n, K, S, seed=seed)
        assert legal(x, r, [1] * n, K, S)
        assert direct_hpwl(x, r, [1] * n, nets, pads) >= exhaustive_optimum(n, nets, pads, K, S)
