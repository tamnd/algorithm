# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multifrontal-method/. The authors are listed in prov/QT9W33.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from multifrontal_method import (
    children_lists, column_structures, dense_ldlt_exact, elimination_tree, liu_child_order,
    multifrontal, postorder, stack_peaks, tri,
)

U = 2.0 ** -53


def random_spd(rng, n, p, exact=False):
    a = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i):
            if rng.random() < p:
                v = rng.randint(-9, 9) or 1
                a[i][j] = a[j][i] = v
    for i in range(n):
        a[i][i] = sum(abs(x) for x in a[i]) + rng.randint(1, 5)
    if exact:
        return [[Fraction(x) for x in row] for row in a]
    return [[float(x) * rng.uniform(0.5, 2.0) if x and i != j else float(x) for j, x in enumerate(row)]
            for i, row in enumerate(a)]


def symmetrize(a):
    n = len(a)
    for i in range(n):
        for j in range(i):
            a[j][i] = a[i][j]
    for i in range(n):
        a[i][i] = math.fsum(abs(a[i][j]) for j in range(n) if j != i) + 1.0
    return a


def grid_matrix(k):
    n = k * k
    a = [[0.0] * n for _ in range(n)]
    for i in range(k):
        for j in range(k):
            v = i * k + j
            a[v][v] = 4.0
            for w in ((v + 1) if j + 1 < k else None, (v + k) if i + 1 < k else None):
                if w is not None:
                    a[v][w] = a[w][v] = -1.0
    return a


def test_edge_cases():
    assert multifrontal([[4.0]]) == [[2.0]]
    l = multifrontal([[4.0, 2.0], [2.0, 5.0]])
    assert l == [[2.0, 0.0], [1.0, 2.0]]
    diag = [[float(i + 1) if i == j else 0.0 for j in range(5)] for i in range(5)]
    st = {}
    l = multifrontal(diag, stats=st)
    assert all(l[i][i] == math.sqrt(i + 1) for i in range(5))
    assert st["parent"] == [-1] * 5 and st["assembly"] == 0
    with pytest.raises(ValueError):
        multifrontal([[1.0, 2.0], [2.0, 1.0]])


def test_exact_ldlt_matches_dense_reference():
    rng = random.Random(31)
    for _ in range(60):
        n = rng.randint(1, 14)
        a = random_spd(rng, n, rng.uniform(0.1, 0.5), exact=True)
        ref_l, ref_d = dense_ldlt_exact(a)
        for order in ("liu", "natural"):
            l, d = multifrontal(a, mode="ldlt", child_order=order)
            assert l == ref_l and d == ref_d


def test_elimination_tree_and_structures():
    rng = random.Random(32)
    for _ in range(60):
        n = rng.randint(1, 16)
        a = random_spd(rng, n, rng.uniform(0.05, 0.4), exact=True)
        parent = elimination_tree(a)
        struct = column_structures(a, parent)
        ref_l, _ = dense_ldlt_exact(a)
        for j in range(n):
            nz = [i for i in range(j + 1, n) if ref_l[i][j] != 0]
            assert set(nz) <= set(struct[j])  # exact cancellation can only remove entries
            assert parent[j] == (struct[j][0] if struct[j] else -1)
            assert all(c < j for c in children_lists(parent)[j])
        po = postorder(parent)
        assert sorted(po) == list(range(n))
        seen = set()
        for j in po:
            assert all(c in seen for c in children_lists(parent)[j])
            seen.add(j)


def test_backward_error_of_float_cholesky():
    rng = random.Random(33)
    for _ in range(40):
        n = rng.randint(1, 12)
        a = random_spd(rng, n, rng.uniform(0.1, 0.5))
        a = symmetrize(a)
        l = multifrontal(a)
        gam = (n + 1) * U / (1 - (n + 1) * U)
        for i in range(n):
            for j in range(i + 1):
                exact = sum(Fraction(l[i][t]) * Fraction(l[j][t]) for t in range(j + 1))
                absl = sum(abs(l[i][t]) * abs(l[j][t]) for t in range(j + 1))
                assert abs(Fraction(a[i][j]) - exact) <= Fraction(gam * absl)


def test_flop_and_assembly_counts():
    rng = random.Random(34)
    for _ in range(40):
        n = rng.randint(1, 20)
        a = symmetrize(random_spd(rng, n, rng.uniform(0.05, 0.4)))
        st = {}
        multifrontal(a, stats=st)
        c = [len(s) for s in st["struct"]]
        assert st["flops"] == sum(1 + cj + cj * (cj + 1) for cj in c)
        assert st["assembly"] == sum(tri(c[j]) for j in range(n) if st["parent"][j] != -1)
        assert st["fronts"] == [cj + 1 for cj in c]


def test_stack_peak_matches_liu_recurrence_and_is_optimal():
    rng = random.Random(35)
    tried = 0
    for _ in range(80):
        n = rng.randint(2, 11)
        a = symmetrize(random_spd(rng, n, rng.uniform(0.05, 0.3)))
        parent = elimination_tree(a)
        struct = column_structures(a, parent)
        roots = [j for j in range(n) if parent[j] == -1]
        for mode in ("liu", "natural"):
            st = {}
            multifrontal(a, child_order=mode, stats=st)
            ch = liu_child_order(parent, struct) if mode == "liu" else children_lists(parent)
            assert st["peak"] == max(stack_peaks(parent, struct, ch)[r] for r in roots)
        ch0 = children_lists(parent)
        if math.prod(math.factorial(len(c)) for c in ch0) > 2000:
            continue
        tried += 1
        liu = stack_peaks(parent, struct, liu_child_order(parent, struct))
        best = min(max(stack_peaks(parent, struct, list(map(list, combo)))[r] for r in roots)
                   for combo in itertools.product(*[itertools.permutations(c) for c in ch0]))
        assert max(liu[r] for r in roots) == best
    assert tried > 40


def test_grid_fronts_and_agreement_with_dense_cholesky():
    k = 6
    a = grid_matrix(k)
    n = k * k
    st = {}
    l = multifrontal(a, stats=st)
    # natural order: band of width k, so every front has order at most k + 1
    assert max(st["fronts"]) == k + 1
    # compare with a plain dense Cholesky
    r = [[0.0] * n for _ in range(n)]
    for j in range(n):
        s = a[j][j] - math.fsum(r[j][t] ** 2 for t in range(j))
        r[j][j] = math.sqrt(s)
        for i in range(j + 1, n):
            r[i][j] = (a[i][j] - math.fsum(r[i][t] * r[j][t] for t in range(j))) / r[j][j]
    assert all(abs(l[i][j] - r[i][j]) <= 1e-14 * 4 for i in range(n) for j in range(n))


def test_worked_example():
    a = [[4.0, 0.0, 2.0, 0.0], [0.0, 9.0, 3.0, 3.0], [2.0, 3.0, 6.0, -1.0], [0.0, 3.0, -1.0, 6.0]]
    st = {}
    l = multifrontal(a, stats=st)
    assert st["parent"] == [2, 2, 3, -1]
    assert st["struct"] == [[2], [2, 3], [3], []]
    assert l == [[2.0, 0.0, 0.0, 0.0], [0.0, 3.0, 0.0, 0.0], [1.0, 1.0, 2.0, 0.0], [0.0, 1.0, -1.0, 2.0]]
