# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regenerating-codes/. The authors are listed in prov/SKYSW3.jsonl.

import itertools
import random
from fractions import Fraction as F

from regenerating_codes import (ProductMatrixMBR, ReedSolomonStorage, cut_set, mbr_point,
                                min_alpha, msr_point)

CASES = [(5, 3, 4), (6, 3, 4), (10, 5, 9), (14, 10, 13), (12, 6, 8), (7, 2, 2)]


def test_msr_and_mbr_formulas_meet_the_cut_set_bound():
    for n, k, d in CASES:
        b = F(k * (d - k + 1) * (2 * d - k + 1))  # a size that makes all values integers
        a_s, b_s = msr_point(b, k, d)
        a_b, b_b = mbr_point(b, k, d)
        assert a_s == b / k and b_s == b / (k * (d - k + 1))
        assert a_b == 2 * b * d / (k * (2 * d - k + 1)) and a_b == d * b_b
        assert cut_set(a_s, b_s, k, d) == b and cut_set(a_b, b_b, k, d) == b
        # MSR: no node can store less than B/k
        assert cut_set(a_s - F(1, 1000), 10 ** 6 * b_s, k, d) < b
        # MBR: no repair can download less than d beta_MBR, whatever alpha is
        assert min_alpha(b, b_b - F(1, 1000), k, d) is None
        # at d beta_MBR the least alpha is exactly alpha_MBR; at beta_MSR it is B/k
        assert min_alpha(b, b_b, k, d) == a_b
        assert min_alpha(b, b_s, k, d) == a_s


def test_tradeoff_curve_is_monotone_and_lies_between_the_points():
    n, k, d = 10, 5, 9
    b = F(1)
    a_s, b_s = msr_point(b, k, d)
    a_b, b_b = mbr_point(b, k, d)
    prev = None
    for t in range(41):
        beta = b_b + (b_s - b_b) * F(t, 40)
        alpha = min_alpha(b, beta, k, d)
        assert a_s <= alpha <= a_b
        if prev is not None:
            assert alpha <= prev
        prev = alpha
    # the numbers quoted on the page: B = 1, n = 10, k = 5, d = 9
    assert (a_s, d * b_s) == (F(1, 5), F(9, 25))
    assert (a_b, d * b_b) == (F(9, 35), F(9, 35))


def test_product_matrix_mbr_exact_repair_every_node_every_helper_set():
    n, k, d, p = 6, 3, 4, 13
    code = ProductMatrixMBR(n, k, d, p)
    assert code.size == 9 and cut_set(F(d), F(1), k, d) == code.size  # it sits on the MBR point
    rng = random.Random(1)
    for _ in range(5):
        data = [rng.randrange(p) for _ in range(code.size)]
        nodes = code.encode(data)
        m = code.message_matrix(data)
        assert all(m[i][j] == m[j][i] for i in range(d) for j in range(d))
        for f in range(n):
            others = [j for j in range(n) if j != f]
            for helpers in itertools.combinations(others, d):
                sent = [code.helper_symbol(nodes[j], f) for j in helpers]  # beta = 1 each
                assert code.repair(f, helpers, sent) == nodes[f]  # exact, not functional


def test_product_matrix_mbr_any_k_nodes_rebuild_the_file():
    for n, k, d, p in ((6, 3, 4, 13), (5, 2, 4, 11), (7, 3, 3, 11)):
        code = ProductMatrixMBR(n, k, d, p)
        rng = random.Random(n * 100 + d)
        for _ in range(3):
            data = [rng.randrange(p) for _ in range(code.size)]
            nodes = code.encode(data)
            for subset in itertools.combinations(range(n), k):
                assert code.reconstruct(subset, [nodes[i] for i in subset]) == data


def test_reed_solomon_baseline_repair_traffic():
    n, k, p = 6, 3, 13
    rs = ReedSolomonStorage(n, k, stripes=3, p=p)  # B = 9, alpha = 3: minimum storage
    rng = random.Random(2)
    data = [rng.randrange(p) for _ in range(9)]
    nodes = rs.encode(data)
    stored = dict(enumerate(nodes))
    for f in range(n):
        for helpers in itertools.combinations([j for j in range(n) if j != f], k):
            rebuilt, traffic = rs.repair(f, helpers, stored)
            assert rebuilt == nodes[f]
            assert traffic == 9  # the whole file size B
    # for the same B = 9 and d = 4: MBR moves 4 symbols and stores 4; MSR would move 6, store 3
    assert mbr_point(F(9), 3, 4) == (F(4), F(1))
    assert msr_point(F(9), 3, 4) == (F(3), F(3, 2))
