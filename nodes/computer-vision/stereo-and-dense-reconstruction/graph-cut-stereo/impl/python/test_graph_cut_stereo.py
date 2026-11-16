# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/graph-cut-stereo/. The authors are listed in prov/A0NX9X.jsonl.

import itertools
import random

from graph_cut_stereo import (
    INF,
    Problem,
    disparity_map,
    energy,
    expansion_move,
    graph_cut_stereo,
    move_energy,
    result_of,
)


def random_problem(rng, H, W, D):
    left = [[rng.choice([10, 20, 50, 90]) for _ in range(W)] for _ in range(H)]
    right = [[rng.choice([10, 20, 50, 90]) for _ in range(W)] for _ in range(H)]
    return Problem(left, right, D, K=rng.choice([5, 10, 20]), lam=rng.choice([1, 2, 4]))


def random_valid_configuration(rng, P):
    A, used_l, used_r = set(), set(), set()
    cand = P.assignments()
    rng.shuffle(cand)
    for (v, u, d) in cand:
        if rng.random() < 0.5 and (v, u) not in used_l and (v, u - d) not in used_r:
            A.add((v, u, d))
            used_l.add((v, u))
            used_r.add((v, u - d))
    return A


def binary_value(unary, terms, const, x):
    e = const + sum(unary[i][x[i]] for i in range(len(x)))
    for (p, q, A, B, C, Dd) in terms:
        e += ((A, B), (C, Dd))[x[p]][x[q]]
    return e


def test_move_energy_equals_the_stereo_energy():
    rng = random.Random(1)
    for _ in range(40):
        P = random_problem(rng, rng.randint(1, 2), rng.randint(2, 4), rng.randint(2, 3))
        A = random_valid_configuration(rng, P)
        alpha = rng.randrange(P.D)
        var, n_old, unary, terms, const, big = move_energy(P, A, alpha)
        for _ in range(30):
            x = [rng.randint(0, 1) for _ in var]
            e = energy(P, result_of(var, n_old, x))
            b = binary_value(unary, terms, const, x)
            if e == INF:
                assert b >= big
            else:
                assert b == e
        for (p, q, A_, B, C, Dd) in terms:
            assert A_ + Dd <= B + C  # every term is regular


def test_expansion_move_is_the_best_move():
    rng = random.Random(2)
    for _ in range(40):
        P = random_problem(rng, 1, rng.randint(2, 4), rng.randint(2, 3))
        A = random_valid_configuration(rng, P)
        alpha = rng.randrange(P.D)
        var, n_old, _, _, _, _ = move_energy(P, A, alpha)
        assert len(var) <= 10
        best = min(energy(P, result_of(var, n_old, x))
                   for x in itertools.product((0, 1), repeat=len(var)))
        A2 = expansion_move(P, A, alpha)
        assert energy(P, A2) == best <= energy(P, A)


def all_configurations(P):
    cand = P.assignments()
    for mask in range(1 << len(cand)):
        yield {cand[i] for i in range(len(cand)) if mask >> i & 1}


def test_result_is_a_local_minimum_and_never_below_the_optimum():
    rng = random.Random(3)
    for H, W, D in ((1, 3, 2), (1, 4, 2), (2, 3, 2), (1, 4, 3)):
        for _ in range(3):
            P = random_problem(rng, H, W, D)
            assert len(P.assignments()) <= 12
            A, cycles = graph_cut_stereo(P)
            e = energy(P, A)
            assert e < INF and e <= energy(P, set())
            for alpha in range(D):
                assert energy(P, expansion_move(P, A, alpha)) >= e
            opt = min(energy(P, B) for B in all_configurations(P))
            assert opt <= e


def make_pair(rng, W, H, dmap):
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
        t = [None] * W
        for j in range(W):
            if owner[j] is not None:
                t[owner[j]] = dmap[v][owner[j]]
        left.append(lrow)
        right.append(rrow)
        truth.append(t)
    return left, right, truth


def test_recovers_a_step_with_occlusions():
    rng = random.Random(4)
    W, H, D = 14, 6, 5
    dmap = [[1 if u < 7 else 4 for u in range(W)] for _ in range(H)]
    left, right, truth = make_pair(rng, W, H, dmap)
    P = Problem(left, right, D, K=20, lam=4)
    A, cycles = graph_cut_stereo(P)
    disp = disparity_map(P, A)
    good = total = 0
    for v in range(H):
        for u in range(W):
            if truth[v][u] is not None:
                total += 1
                good += disp[v][u] == truth[v][u]
    assert good >= 0.95 * total
    hidden = sum(disp[v][u] is None for v in range(H) for u in range(W)
                 if truth[v][u] is None)
    assert hidden >= 1  # some truly occluded pixels come out as occluded


def test_worked_example():
    left = [[10, 50, 50, 90]]
    right = [[50, 50, 90, 20]]
    P = Problem(left, right, 2, K=10, lam=2)
    A, cycles = graph_cut_stereo(P)
    assert disparity_map(P, A) == [[None, 1, 1, 1]]
    assert energy(P, A) == 20
    assert energy(P, set()) == 80
    first = expansion_move(P, set(), 0)
    assert first == {(0, 1, 0)} and energy(P, first) == 64
    assert expansion_move(P, first, 1) == A
    assert min(energy(P, B) for B in all_configurations(P)) == 20
