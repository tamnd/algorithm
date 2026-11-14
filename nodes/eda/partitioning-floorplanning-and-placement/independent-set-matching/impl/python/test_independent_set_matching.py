# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/independent-set-matching/. The authors are listed in prov/CJ581B.jsonl.

import random
from fractions import Fraction
from itertools import permutations

from independent_set_matching import (
    choose_set,
    cost_matrix,
    hungarian,
    ism,
    nets_of_cells,
    total_hpwl,
)


def brute_assignment(cost):
    k = len(cost)
    return min(sum(cost[a][perm[a]] for a in range(k)) for perm in permutations(range(k)))


def random_instance(rng, rows=3, sites=12, n=14, m=16, q=4):
    """Cells of width 1 or 2 packed on random distinct sites, random nets, pads on the border."""
    W = [rng.choice([1, 1, 2]) for _ in range(n)]
    x, row = [0] * n, [0] * n
    occupied = {r: set() for r in range(rows)}
    for i in range(n):
        while True:
            r = rng.randrange(rows)
            s = rng.randrange(sites - W[i] + 1)
            span = set(range(s, s + W[i]))
            if span.isdisjoint(occupied[r]):
                occupied[r] |= span
                x[i], row[i] = s, r
                break
    pads = [(rng.choice([0, sites]), rng.randint(0, rows)) for _ in range(q)]
    nets, weights = [], []
    for _ in range(m):
        size = rng.randint(2, 4)
        pins = rng.sample(range(n + q), size)
        nets.append(pins)
        weights.append(rng.randint(1, 3))
    return x, row, W, nets, weights, pads


def legal(x, row, W, sites):
    seen = set()
    for i in range(len(x)):
        for s in range(x[i], x[i] + W[i]):
            if (row[i], s) in seen or not (0 <= s < sites):
                return False
            seen.add((row[i], s))
    return True


def test_hungarian_against_all_permutations():
    rng = random.Random(7)
    for _ in range(300):
        k = rng.randint(1, 6)
        cost = [[Fraction(rng.randint(-20, 20), rng.randint(1, 4)) for _ in range(k)] for _ in range(k)]
        assign, value = hungarian(cost)
        assert sorted(assign) == list(range(k))
        assert value == sum(cost[a][assign[a]] for a in range(k))
        assert value == brute_assignment(cost)


def test_separable_cost_equals_direct_hpwl_and_matches_brute_force_on_5_cells():
    rng = random.Random(11)
    checked = 0
    for _ in range(400):
        x, row, W, nets, weights, pads = random_instance(rng)
        n = len(x)
        cell_nets = nets_of_cells(n, nets)
        seed = rng.randrange(n)
        S = choose_set(seed, x, row, W, cell_nets, 5, 12, 3)
        # the chosen cells share no net and have the same width
        for a in range(len(S)):
            assert W[S[a]] == W[seed]
            for b in range(a + 1, len(S)):
                assert set(cell_nets[S[a]]).isdisjoint(cell_nets[S[b]])
        if len(S) < 5:
            continue
        checked += 1
        slots = [(x[c], row[c]) for c in S]
        cost = cost_matrix(S, x, row, W, nets, weights, pads, cell_nets)
        base = total_hpwl(x, row, W, nets, weights, pads)
        rest = base - sum(cost[a][a] for a in range(5))
        best_direct = None
        for perm in permutations(range(5)):
            xx, rr = list(x), list(row)
            for a, c in enumerate(S):
                xx[c], rr[c] = slots[perm[a]]
            direct = total_hpwl(xx, rr, W, nets, weights, pads)
            assert direct == rest + sum(cost[a][perm[a]] for a in range(5))
            if best_direct is None or direct < best_direct:
                best_direct = direct
        _, value = hungarian(cost)
        assert rest + value == best_direct
    assert checked >= 30


def test_ism_pass_is_legal_and_never_increases_hpwl():
    rng = random.Random(3)
    for _ in range(25):
        x, row, W, nets, weights, pads = random_instance(rng)
        before = total_hpwl(x, row, W, nets, weights, pads)
        nx, nr = ism(x, row, W, nets, weights, pads, k=5, wx=6, wy=2, passes=2)
        after = total_hpwl(nx, nr, W, nets, weights, pads)
        assert legal(nx, nr, W, 12)
        assert sorted(zip(nr, nx, W)) == sorted(zip(row, x, W))  # the same slots, permuted
        assert after <= before


def test_page_example():
    # one row; cells a, b, c of width 1 at x = 0, 2, 4; pads P = (5, 1/2), Q = (0, 1/2), R = (3, 1/2)
    x, row, W = [0, 2, 4], [0, 0, 0], [1, 1, 1]
    pads = [(5, Fraction(1, 2)), (0, Fraction(1, 2)), (3, Fraction(1, 2))]
    nets = [[0, 3], [1, 4], [2, 5]]
    weights = [1, 1, 1]
    assert total_hpwl(x, row, W, nets, weights, pads) == Fraction(17, 2)
    cost = cost_matrix([0, 1, 2], x, row, W, nets, weights, pads, nets_of_cells(3, nets))
    assert cost == [[Fraction(9, 2), Fraction(5, 2), Fraction(1, 2)],
                    [Fraction(1, 2), Fraction(5, 2), Fraction(9, 2)],
                    [Fraction(5, 2), Fraction(1, 2), Fraction(3, 2)]]
    assign, value = hungarian(cost)
    assert assign == [2, 0, 1] and value == Fraction(3, 2)
    nx, _ = ism(x, row, W, nets, weights, pads, k=3, wx=4, wy=0)
    assert nx == [4, 0, 2] and total_hpwl(nx, row, W, nets, weights, pads) == Fraction(3, 2)


def test_shared_net_breaks_the_separable_cost():
    # a at x = 0 and b at x = 5 share a net of weight 2; a likes the left pad, b the right pad
    x, row, W = [0, 5], [0, 0], [1, 1]
    pads = [(-1, Fraction(1, 2)), (7, Fraction(1, 2))]
    nets = [[0, 1], [0, 2], [1, 3]]
    weights = [2, 1, 1]
    cell_nets = nets_of_cells(2, nets)
    cost = cost_matrix([0, 1], x, row, W, nets, weights, pads, cell_nets)
    assign, _ = hungarian(cost)
    assert assign == [1, 0]  # the matrix prefers the swap
    assert cost == [[Fraction(23, 2), Fraction(13, 2)], [Fraction(13, 2), Fraction(23, 2)]]
    swapped = total_hpwl([5, 0], row, W, nets, weights, pads)
    kept = total_hpwl(x, row, W, nets, weights, pads)
    assert (swapped, kept) == (23, 13)  # but the swap is worse
