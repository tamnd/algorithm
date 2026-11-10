# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/roofline-model/.

import random
from fractions import Fraction as F

from roofline_model import (A100, attainable, bound, hierarchical, ridge, time_lower_bound,
                            with_ceilings)


def test_ridge_points_of_the_a100():
    assert ridge(A100["fp32"], A100["hbm"]) == F(19500, 1555)
    assert 12.54 < float(ridge(A100["fp32"], A100["hbm"])) < 12.55
    assert 6.23 < float(ridge(A100["fp64"], A100["hbm"])) < 6.24
    assert 200.6 < float(ridge(A100["fp16_tensor"], A100["hbm"])) < 200.7
    assert 1.0004 < float(ridge(A100["fp32"], A100["shared"])) < 1.0005


def test_volkov_gtx480_ridge():
    assert 7.34 < float(ridge(F(13, 10) * 10**12, 177 * 10**9)) < 7.35


def test_page_worked_example():
    pk, bw = A100["fp32"], A100["hbm"]
    vec_add = attainable(F(1, 12), pk, bw)
    assert vec_add == F(1555, 12) * 10**9  # about 129.6 GFLOP/s
    assert 0.0066 < float(vec_add / pk) < 0.0067
    assert attainable(8, pk, bw) == 12440 * 10**9 and bound(8, pk, bw) == "memory"
    assert attainable(32, pk, bw) == pk and bound(32, pk, bw) == "compute"
    n = 10**8
    t = time_lower_bound(n, 12 * n, pk, bw)
    assert 0.000771 < float(t) < 0.000772  # about 0.77 ms


def test_shared_memory_roof_of_the_plain_tiled_kernel():
    pk = A100["fp32"]
    # 2 FLOP per 8 bytes from shared memory; 8 FLOP per byte from HBM at T = 32.
    roof = hierarchical(pk, [(F(1, 4), A100["shared"]), (8, A100["hbm"])])
    assert roof == A100["shared"] / 4
    assert 4.87e12 < float(roof) < 4.88e12 and 0.249 < float(roof / pk) < 0.25


def test_roof_is_the_minimum_and_continuous_at_the_ridge():
    rng = random.Random(17)
    for _ in range(200):
        pk = F(rng.randrange(1, 10**6))
        bw = F(rng.randrange(1, 10**4))
        r = ridge(pk, bw)
        assert attainable(r, pk, bw) == pk == r * bw
        i = F(rng.randrange(1, 10**5), rng.randrange(1, 10**3))
        a = attainable(i, pk, bw)
        assert a <= pk and a <= i * bw and a in (pk, i * bw)
        assert attainable(2 * i, pk, bw) >= a


def test_time_bound_matches_the_roof():
    rng = random.Random(18)
    for _ in range(200):
        w, q = F(rng.randrange(1, 10**9)), F(rng.randrange(1, 10**9))
        pk, bw = F(rng.randrange(1, 10**6)), F(rng.randrange(1, 10**6))
        assert time_lower_bound(w, q, pk, bw) == w / attainable(w / q, pk, bw)


def test_ceilings_lower_the_roof():
    pk, bw = A100["fp32"], A100["hbm"]
    no_fma = pk / 2
    assert with_ceilings(100, [pk, no_fma], [bw]) == no_fma
    assert with_ceilings(1, [pk, no_fma], [bw, bw / 2]) == bw / 2
