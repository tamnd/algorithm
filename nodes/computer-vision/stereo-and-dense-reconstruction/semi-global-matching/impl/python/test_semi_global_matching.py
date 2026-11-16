# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semi-global-matching/. The authors are listed in prov/NJ87X5.jsonl.

import itertools
import random

from semi_global_matching import (
    DIRECTIONS_2,
    DIRECTIONS_4,
    DIRECTIONS_8,
    DIRECTIONS_16,
    absolute_difference_volume,
    aggregate,
    path_cost,
    sgm,
    winner_takes_all,
)


def random_volume(rng, H, W, D, hi=9):
    return [[[rng.randint(0, hi) for _ in range(D)] for _ in range(W)] for _ in range(H)]


def jump_cost(a, b, P1, P2):
    if a == b:
        return 0
    if abs(a - b) == 1:
        return min(P1, P2)
    return P2


def chain_minimum(costs, P1, P2, d_last):
    """Brute force: the least sum of costs and jump costs over all
    disparity sequences along the chain that end with d_last."""
    D = len(costs[0])
    best = None
    for seq in itertools.product(range(D), repeat=len(costs) - 1):
        seq = seq + (d_last,)
        e = sum(costs[t][seq[t]] for t in range(len(seq)))
        e += sum(jump_cost(seq[t - 1], seq[t], P1, P2) for t in range(1, len(seq)))
        if best is None or e < best:
            best = e
    return best


def test_path_cost_is_the_chain_minimum_minus_the_subtracted_minima():
    rng = random.Random(1)
    for _ in range(40):
        H, W, D = rng.randint(1, 3), rng.randint(1, 4), rng.randint(1, 4)
        C = random_volume(rng, H, W, D)
        P1 = rng.randint(0, 4)
        P2 = P1 + rng.randint(0, 6)
        r = rng.choice(DIRECTIONS_16)
        L = path_cost(C, P1, P2, r)
        for v in range(H):
            for u in range(W):
                path = [(u, v)]  # walk back along -r to the border
                while True:
                    pu, pv = path[-1][0] - r[0], path[-1][1] - r[1]
                    if not (0 <= pu < W and 0 <= pv < H):
                        break
                    path.append((pu, pv))
                path.reverse()
                offset = sum(min(L[pv][pu]) for (pu, pv) in path[:-1])
                costs = [C[pv][pu] for (pu, pv) in path]
                for d in range(D):
                    assert L[v][u][d] + offset == chain_minimum(costs, P1, P2, d)


def test_bounds_of_the_path_cost():
    rng = random.Random(2)
    for _ in range(30):
        H, W, D = rng.randint(1, 5), rng.randint(1, 5), rng.randint(1, 6)
        C = random_volume(rng, H, W, D, hi=50)
        P1 = rng.randint(0, 10)
        P2 = P1 + rng.randint(0, 30)
        cmax = max(max(max(c) for c in row) for row in C)
        for r in DIRECTIONS_8:
            L = path_cost(C, P1, P2, r)
            for v in range(H):
                for u in range(W):
                    for d in range(D):
                        assert C[v][u][d] <= L[v][u][d] <= C[v][u][d] + P2 <= cmax + P2


def test_zero_penalties_give_winner_takes_all():
    rng = random.Random(3)
    C = random_volume(rng, 4, 5, 6)
    assert sgm(C, 0, 0) == winner_takes_all(C)


def test_one_direction_on_one_row_is_exact_at_the_end():
    rng = random.Random(4)
    for _ in range(30):
        W, D = rng.randint(1, 5), rng.randint(2, 4)
        C = random_volume(rng, 1, W, D)
        P1, P2 = 2, 5
        S = aggregate(C, P1, P2, [(1, 0)])
        best = min(chain_minimum(C[0], P1, P2, d) for d in range(D))
        offset = sum(min(path_cost(C, P1, P2, (1, 0))[0][u]) for u in range(W - 1))
        assert min(S[0][W - 1]) + offset == best


def make_pair(rng, W, H, dmap, noise):
    """Random texture on the left; the right image shows at each column j
    the left pixel u with u - d(u) = j of the largest disparity."""
    left, right, truth = [], [], []
    for v in range(H):
        lrow = [rng.randint(0, 255) for _ in range(W)]
        owner = [None] * W
        for u in range(W):
            j = u - dmap[v][u]
            if j >= 0 and (owner[j] is None or dmap[v][owner[j]] < dmap[v][u]):
                owner[j] = u
        rrow = [lrow[owner[j]] if owner[j] is not None else rng.randint(0, 255)
                for j in range(W)]
        rrow = [min(255, max(0, x + rng.randint(-noise, noise))) for x in rrow]
        t = [None] * W
        for j in range(W):
            if owner[j] is not None:
                t[owner[j]] = dmap[v][owner[j]]
        left.append(lrow)
        right.append(rrow)
        truth.append(t)
    return left, right, truth


def accuracy(disp, truth):
    good = total = 0
    for drow, trow in zip(disp, truth):
        for d, t in zip(drow, trow):
            if t is not None:
                total += 1
                good += d == t
    return good / total


def test_recovers_a_noisy_step_better_than_winner_takes_all():
    rng = random.Random(5)
    W, H, D = 32, 16, 8
    dmap = [[2 if u < 14 else 6 for u in range(W)] for _ in range(H)]
    left, right, truth = make_pair(rng, W, H, dmap, noise=30)
    C = absolute_difference_volume(left, right, D)
    wta = accuracy(winner_takes_all(C), truth)
    acc = accuracy(sgm(C, 20, 200), truth)
    assert wta < 0.6  # the noise makes single pixels unreliable
    assert acc >= 0.93
    assert accuracy(sgm(C, 20, 200, DIRECTIONS_2), truth) < acc


def test_direction_sets():
    assert len(DIRECTIONS_2) == 2 and len(DIRECTIONS_4) == 4
    assert len(DIRECTIONS_8) == 8 and len(DIRECTIONS_16) == 16
    assert len(set(DIRECTIONS_16)) == 16
    for (du, dv) in DIRECTIONS_16:
        assert (-du, -dv) in DIRECTIONS_16
