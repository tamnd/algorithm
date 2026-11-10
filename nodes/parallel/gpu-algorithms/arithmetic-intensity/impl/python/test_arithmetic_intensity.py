# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arithmetic-intensity/.

from fractions import Fraction as F

from arithmetic_intensity import (csr_spmv, dot_product, ideal_matmul, intensity, matvec,
                                  naive_matmul, tiled_matmul, trace_dot_product, trace_matvec,
                                  trace_tiled_matmul, trace_vector_add, vector_add)


def ai(pair):
    return intensity(*pair)


def test_traces_match_closed_forms():
    for n in (1, 2, 7, 64):
        assert trace_vector_add(n) == vector_add(n)
        assert trace_dot_product(n) == dot_product(n)
        assert trace_matvec(n) == matvec(n)
        assert trace_matvec(n, x_cached=False) == matvec(n, x_cached=False)
    for n, t in ((8, 1), (8, 2), (16, 4), (32, 8), (64, 16), (64, 32)):
        assert trace_tiled_matmul(n, t) == tiled_matmul(n, t)


def test_vector_add_and_dot_product():
    assert ai(vector_add(10**6)) == F(1, 12)
    assert ai(vector_add(10**6, s=8)) == F(1, 24)
    assert ai(dot_product(10**6)) == F(2 * 10**6, 8 * 10**6 + 4)
    assert abs(ai(dot_product(10**6)) - F(1, 4)) < F(1, 10**6)
    assert abs(ai(dot_product(10**6, s=8)) - F(1, 8)) < F(1, 10**6)


def test_matvec():
    assert ai(matvec(1000)) == F(1000, 2004)
    assert abs(ai(matvec(10**4)) - F(1, 2)) < F(1, 10**3)
    assert abs(ai(matvec(10**4, x_cached=False)) - F(1, 4)) < F(1, 10**4)
    assert abs(ai(matvec(10**4, s=8)) - F(1, 4)) < F(1, 10**3)


def test_matmul_intensities():
    n = 4096
    assert abs(ai(naive_matmul(n)) - F(1, 4)) < F(1, 10**4)
    for t in (16, 32):
        exact = ai(tiled_matmul(n, t))
        assert exact == F(2 * n, 8 * n // t + 4) and abs(exact - F(t, 4)) < F(t, 4) / 100
    assert abs(ai(tiled_matmul(n, 16)) - 4) < F(1, 10) and abs(ai(tiled_matmul(n, 32)) - 8) < F(1, 10)
    assert ai(ideal_matmul(n)) == F(n, 6)


def test_intensity_grows_with_the_tile():
    n = 1024
    values = [ai(tiled_matmul(n, t)) for t in (1, 2, 4, 8, 16, 32, 64)]
    assert values == sorted(values) and values[0] == ai(naive_matmul(n))


def test_fusion_raises_intensity():
    from arithmetic_intensity import fused_add_mul, unfused_add_mul
    assert ai(unfused_add_mul(1000)) == F(1, 12) and ai(fused_add_mul(1000)) == F(1, 8)


def test_csr_spmv_page_example():
    nnz, rows = 10**7, 10**6
    exact = ai(csr_spmv(nnz, rows))
    assert exact == F(2 * nnz, 212 * rows + 4) and 0.0943 < float(exact) < 0.0944  # 10 per row
    best = ai(csr_spmv(nnz, rows, x_bytes_per_nnz=0))
    assert best == F(2 * nnz, 132 * rows + 4) and 0.1515 < float(best) < 0.1516
    assert ai(csr_spmv(10**9, 1, x_bytes_per_nnz=0)) < F(1, 6)
