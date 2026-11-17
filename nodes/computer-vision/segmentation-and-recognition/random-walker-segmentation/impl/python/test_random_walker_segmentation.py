# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-walker-segmentation/. The authors are listed in prov/TCA3BR.jsonl.

import math
import random

from random_walker_segmentation import (
    conjugate_gradient,
    dirichlet_energy,
    edge_weights,
    grid_edges,
    laplacian,
    monte_carlo,
    random_walker,
    random_walker_all,
    solve_labels,
)


def random_case(rng, h, w, k):
    img = [[rng.choice((20, 90, 160, 230)) + rng.randrange(15) for _ in range(w)] for _ in range(h)]
    pix = list(range(h * w))
    rng.shuffle(pix)
    seeds = {}
    for s in range(k):
        seeds[pix[2 * s]] = s
        seeds[pix[2 * s + 1]] = s
    return img, seeds


def test_chain_is_resistors_in_series():
    img = [[10, 20, 60, 70, 80]]
    probs, labels = random_walker(img, {0: 0, 4: 1}, 2.0)
    w = edge_weights(img, grid_edges(1, 5), 2.0)
    res = [1.0 / x for x in w]
    total = sum(res)
    want = [sum(res[:i]) / total for i in range(5)]
    assert all(abs(a - b) < 1e-12 for a, b in zip(probs[1], want))
    assert [round(x, 4) for x in probs[1]] == [0.0, 0.105, 0.7899, 0.895, 1.0]
    assert labels == [0, 0, 1, 1, 1]


def test_sum_range_and_sum_rule():
    rng = random.Random(11)
    for _ in range(20):
        k = rng.randint(2, 4)
        img, seeds = random_case(rng, 4, 5, k)
        probs, _ = random_walker(img, seeds, 5.0)
        full = random_walker_all(img, seeds, 5.0, k)
        for p in range(20):
            assert abs(sum(full[s][p] for s in range(k)) - 1.0) < 1e-9
            for s in range(k):
                assert -1e-12 <= probs[s][p] <= 1.0 + 1e-12
                assert abs(probs[s][p] - full[s][p]) < 1e-9


def test_mean_value_property():
    rng = random.Random(5)
    for _ in range(10):
        img, seeds = random_case(rng, 4, 4, 3)
        h, w = 4, 4
        edges = grid_edges(h, w)
        wts = edge_weights(img, edges, 50.0)
        nbr = [[] for _ in range(h * w)]
        for (p, q), x in zip(edges, wts):
            nbr[p].append((q, x))
            nbr[q].append((p, x))
        probs, _ = random_walker(img, seeds, 50.0)
        for xs in probs:
            for p in range(h * w):
                if p in seeds:
                    continue
                avg = sum(x * xs[q] for q, x in nbr[p]) / sum(x for _, x in nbr[p])
                assert abs(xs[p] - avg) < 1e-9


def test_minimizes_dirichlet_energy():
    rng = random.Random(3)
    img, seeds = random_case(rng, 3, 4, 2)
    edges = grid_edges(3, 4)
    wts = edge_weights(img, edges, 20.0)
    probs, _ = random_walker(img, seeds, 20.0)
    best = dirichlet_energy(edges, wts, probs[0])
    for _ in range(200):
        y = [x if p in seeds else x + rng.uniform(-0.1, 0.1) for p, x in enumerate(probs[0])]
        assert dirichlet_energy(edges, wts, y) >= best - 1e-12


def test_two_labels_each_segment_part_touches_its_seed():
    rng = random.Random(8)
    h, w = 5, 5
    for _ in range(15):
        img, seeds = random_case(rng, h, w, 2)
        _, labels = random_walker(img, seeds, 20.0)
        for s in range(2):
            reach = [p for p in seeds if seeds[p] == s]
            seen = set(reach)
            while reach:
                p = reach.pop()
                u, v = p % w, p // w
                for uu, vv in ((u + 1, v), (u - 1, v), (u, v + 1), (u, v - 1)):
                    q = vv * w + uu
                    if 0 <= uu < w and 0 <= vv < h and q not in seen and labels[q] == s:
                        seen.add(q)
                        reach.append(q)
            assert seen == {p for p in range(h * w) if labels[p] == s}


def test_three_labels_can_give_a_part_without_seed():
    # Node 0 joins nodes 1 and 2. Node 1 joins a seed of label 0 and a seed
    # of label 1, node 2 a seed of label 0 and a seed of label 2.
    edges = [(0, 1), (0, 2), (1, 5), (1, 3), (2, 6), (2, 4)]
    lap = laplacian(7, edges, [1.0, 1.0, 1.2, 1.0, 1.2, 1.0])
    seeds = {3: 0, 4: 0, 5: 1, 6: 2}
    x = solve_labels(lap, 7, seeds, [0, 1, 2])
    label = [max(range(3), key=lambda s: x[s][p]) for p in range(3)]
    assert label == [0, 1, 2]
    assert abs(x[0][0] - 1 / 2.2) < 1e-12
    assert x[1][1] > x[0][1] and x[2][2] > x[0][2]
    # The same pattern on a 2 x 5 image: pixel 7 gets label 0, but its
    # neighbors 2, 6 and 8 get labels 1, 1 and 2.
    img = [[250, 90, 250, 90, 250], [100, 100, 110, 100, 100]]
    _, labels = random_walker(img, {1: 0, 3: 0, 5: 1, 9: 2, 2: 1}, 60.0)
    assert labels[7] == 0
    assert [labels[2], labels[6], labels[8]] == [1, 1, 2]


def test_agrees_with_simulated_walks():
    rng = random.Random(2024)
    img = [[20, 25, 200], [22, 180, 210], [30, 190, 220]]
    seeds = {0: 0, 8: 1}
    probs, _ = random_walker(img, seeds, 4.0)
    for start in (1, 4, 6):
        est = monte_carlo(img, seeds, 4.0, start, 3000, rng)
        assert abs(est[1] - probs[1][start]) < 0.04


def test_conjugate_gradient_matches_direct_solve():
    rng = random.Random(9)
    img, seeds = random_case(rng, 4, 4, 2)
    edges = grid_edges(4, 4)
    lap = laplacian(16, edges, edge_weights(img, edges, 10.0))
    free = [p for p in range(16) if p not in seeds]
    lu = [[lap[i][j] for j in free] for i in free]
    b = [-sum(lap[i][p] for p in seeds if seeds[p] == 1) for i in free]
    x = conjugate_gradient(lu, b)
    probs, _ = random_walker(img, seeds, 10.0)
    assert all(abs(x[r] - probs[1][p]) < 1e-8 for r, p in enumerate(free))
    assert math.isfinite(sum(x))
