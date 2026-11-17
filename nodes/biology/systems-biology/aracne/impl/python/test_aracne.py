# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aracne/. The authors are listed in prov/VF2D8H.jsonl.

import math
import random

from aracne import (
    aracne,
    aracne_prune,
    gaussian_mutual_information,
    mi_matrix,
    mutual_information_binned,
    simulate_tree,
    tree_correlations,
)


def brute_force_prune(mi, threshold, tolerance):
    """The definition: keep a passing edge unless some passing triangle has it as the weakest edge."""
    m = len(mi)
    passing = {(i, j) for i in range(m) for j in range(i + 1, m) if mi[i][j] > threshold}
    out = set()
    for i, j in passing:
        dropped = False
        for k in range(m):
            if k in (i, j):
                continue
            a, b = tuple(sorted((i, k))), tuple(sorted((j, k)))
            if a in passing and b in passing:
                if mi[i][j] < (1 - tolerance) * mi[a[0]][a[1]] and mi[i][j] < (1 - tolerance) * mi[b[0]][b[1]]:
                    dropped = True
        if not dropped:
            out.add((i, j))
    return out


def gaussian_mi_matrix(rho):
    m = len(rho)
    return [[0.0 if i == j else gaussian_mutual_information(rho[i][j]) for j in range(m)] for i in range(m)]


def random_tree(rng, m):
    parent = [0] + [rng.randrange(c) for c in range(1, m)]
    r = [1.0] + [rng.choice([-1, 1]) * rng.uniform(0.3, 0.95) for _ in range(1, m)]
    return parent, r


def test_binned_mi_identical_variables_is_log_b():
    rng = random.Random(1)
    x = [rng.random() for _ in range(120)]
    for b in (2, 3, 4, 5):
        assert abs(mutual_information_binned(x, x, b) - math.log(b)) < 1e-12
        y = [-v ** 3 for v in x]  # a decreasing map keeps the bins, in reverse
        assert abs(mutual_information_binned(x, y, b) - math.log(b)) < 1e-12


def test_binned_mi_balanced_grid_is_zero():
    b, c = 4, 5
    n = b * b * c
    x = list(range(n))
    # within each x bin, the y bins are filled in turn, so every cell gets c points
    y = [((s % (n // b)) % b) * (n // b) + s // b for s in range(n)]
    assert sorted(y) == list(range(n))
    assert abs(mutual_information_binned(x, y, b)) < 1e-12


def test_binned_mi_symmetric_and_nonnegative():
    rng = random.Random(2)
    for _ in range(20):
        x = [rng.gauss(0, 1) for _ in range(60)]
        y = [v + rng.gauss(0, 1) for v in x]
        a = mutual_information_binned(x, y, 3)
        assert a >= -1e-12
        assert abs(a - mutual_information_binned(y, x, 3)) < 1e-12


def test_worked_example_of_the_page():
    # genes A, B, C, D = 0, 1, 2, 3; B is the hub of a tree
    parent = [1, 0, 1, 1]
    rho = [[1.0] * 4 for _ in range(4)]
    edge = {(0, 1): 0.9, (1, 2): 0.8, (1, 3): 0.7}
    for (i, j), v in edge.items():
        rho[i][j] = rho[j][i] = v
    for i, j in ((0, 2), (0, 3), (2, 3)):
        rho[i][j] = rho[j][i] = rho[i][1] * rho[1][j]
    mi = gaussian_mi_matrix(rho)
    assert abs(mi[0][1] - 0.830366) < 1e-6
    assert abs(mi[2][3] - 0.188147) < 1e-6
    assert aracne_prune(mi, 0.1, 0.0) == {(0, 1), (1, 2), (1, 3)}
    assert aracne_prune(mi, 0.1, 0.15) == {(0, 1), (1, 2), (1, 3)}
    assert aracne_prune(mi, 0.1, 0.3) == {(0, 1), (1, 2), (1, 3), (0, 2), (0, 3)}
    assert aracne_prune(mi, 0.3, 0.0) == {(0, 1), (1, 2), (1, 3)}
    assert parent[0] == 1


def test_prune_matches_brute_force():
    rng = random.Random(3)
    for trial in range(200):
        m = rng.randint(3, 8)
        mi = [[0.0] * m for _ in range(m)]
        for i in range(m):
            for j in range(i + 1, m):
                mi[i][j] = mi[j][i] = rng.choice([rng.random(), round(rng.random(), 1)])
        th = rng.choice([0.0, 0.2, 0.5])
        tol = rng.choice([0.0, 0.1, 0.3])
        assert aracne_prune(mi, th, tol) == brute_force_prune(mi, th, tol)


def test_result_does_not_depend_on_gene_order():
    rng = random.Random(4)
    for _ in range(50):
        m = 7
        mi = [[0.0] * m for _ in range(m)]
        for i in range(m):
            for j in range(i + 1, m):
                mi[i][j] = mi[j][i] = rng.random()
        perm = list(range(m))
        rng.shuffle(perm)
        inv = [0] * m
        for a, p in enumerate(perm):
            inv[p] = a
        mi2 = [[mi[perm[a]][perm[b]] for b in range(m)] for a in range(m)]
        e1 = aracne_prune(mi, 0.1, 0.05)
        e2 = {tuple(sorted((perm[a], perm[b]))) for a, b in aracne_prune(mi2, 0.1, 0.05)}
        assert e1 == e2


def test_larger_tolerance_keeps_more_edges():
    rng = random.Random(5)
    for _ in range(50):
        m = 6
        mi = [[0.0] * m for _ in range(m)]
        for i in range(m):
            for j in range(i + 1, m):
                mi[i][j] = mi[j][i] = rng.random()
        prev = aracne_prune(mi, 0.0, 0.0)
        for tol in (0.05, 0.1, 0.2, 0.5, 0.9):
            cur = aracne_prune(mi, 0.0, tol)
            assert prev <= cur
            prev = cur


def test_exact_mi_on_a_tree_gives_the_tree():
    # Theorem 1 of Margolin et al. 2006: exact MI values of a tree network
    rng = random.Random(6)
    for _ in range(100):
        m = rng.randint(2, 12)
        parent, r = random_tree(rng, m)
        mi = gaussian_mi_matrix(tree_correlations(m, parent, r))
        truth = {tuple(sorted((c, parent[c]))) for c in range(1, m)}
        assert aracne_prune(mi, 0.0, 0.0) == truth


def test_tree_correlation_products():
    parent = [0, 0, 1, 1]
    r = [1.0, 0.5, -0.6, 0.8]
    rho = tree_correlations(4, parent, r)
    assert abs(rho[2][3] - (-0.6 * 0.8)) < 1e-15
    assert abs(rho[0][3] - 0.5 * 0.8) < 1e-15
    assert abs(rho[0][2] - 0.5 * -0.6) < 1e-15


def test_recovery_on_simulated_data_is_measured():
    # a measurement for one seed, not a guarantee: 8 genes, 250 samples, 4 bins
    rng = random.Random(7)
    m, n = 8, 250
    parent = [0, 0, 1, 1, 2, 2, 3, 0]
    r = [1.0, 0.85, 0.8, 0.75, 0.8, 0.7, 0.85, 0.8]
    data = simulate_tree(rng, m, parent, r, n)
    truth = {tuple(sorted((c, parent[c]))) for c in range(1, m)}
    mi = mi_matrix(data, 4)
    relevance = {(i, j) for i in range(m) for j in range(i + 1, m) if mi[i][j] > 0.05}
    pruned = aracne(data, 0.05, 0.0, 4)
    assert pruned <= relevance
    assert truth <= relevance
    fp_rel = len(relevance - truth)
    fp_ar = len(pruned - truth)
    tp_ar = len(pruned & truth)
    assert fp_ar < fp_rel
    assert tp_ar >= 6
    # the measured numbers quoted on the page
    assert (len(relevance), tp_ar, fp_ar) == MEASURED


# all 28 pairs pass the threshold; ARACNE keeps the 7 true edges and no other
MEASURED = (28, 7, 0)
