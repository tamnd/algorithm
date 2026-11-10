# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ellpack-format/. The authors are listed in prov/6VRCR7.jsonl.
import random

from ellpack_format import (
    PAD, csr_scalar_sectors, from_dense, from_rows, get, hyb, hyb_spmv, hyb_width,
    spmv, spmv_simt, storage_words, to_dense,
)


def dense_mv(a, x):
    return [sum(v * xj for v, xj in zip(row, x)) for row in a]


def random_dense(rng, m, n, density):
    return [[rng.randrange(-9, 10) if rng.random() < density else 0 for _ in range(n)] for _ in range(m)]


def test_worked_example():
    a = [[1, 7, 0, 0], [0, 2, 8, 0], [5, 0, 3, 9], [0, 6, 0, 4]]
    e = from_dense(a)
    assert (e.m, e.k, e.nnz) == (4, 3, 9)
    assert e.data == [1, 2, 5, 6, 7, 8, 3, 4, 0, 0, 9, 0]
    assert e.indices == [0, 1, 0, 1, 1, 2, 2, 3, PAD, PAD, 3, PAD]
    assert spmv(e, [1, 2, 3, 4]) == [15, 28, 50, 28]


def test_spmv_matches_dense_product():
    for seed in range(60):
        rng = random.Random(seed)
        m, n = rng.randrange(0, 70), rng.randrange(1, 40)
        a = random_dense(rng, m, n, rng.choice([0.0, 0.05, 0.2, 0.6]))
        x = [rng.randrange(-5, 6) for _ in range(n)]
        e = from_dense(a)
        assert to_dense(e) == a
        assert spmv(e, x) == dense_mv(a, x)
        for use_rowlen in (False, True):
            y, st = spmv_simt(e, x, use_rowlen)
            assert y == dense_mv(a, x)
            assert st["flops"] == 2 * e.nnz
            assert st["lane_slots"] == (e.nnz if use_rowlen else e.m * e.k)
        if m:
            r, c = rng.randrange(m), rng.randrange(n)
            assert get(e, r, c) == a[r][c]


def test_padding_and_storage_formulas():
    for seed in range(40):
        rng = random.Random(100 + seed)
        m, n = rng.randrange(1, 80), rng.randrange(1, 50)
        e = from_dense(random_dense(rng, m, n, rng.random()))
        pads = sum(1 for c in e.indices if c == PAD)
        assert pads == e.m * e.k - e.nnz
        assert len(e.data) == len(e.indices) == storage_words(e.m, e.k, e.nnz, "ell") // 2
        assert storage_words(e.m, e.k, e.nnz, "ellr") == 2 * e.m * e.k + e.m
        assert storage_words(e.m, e.k, e.nnz, "csr") == 2 * e.nnz + e.m + 1


def test_coalescing_ell_against_csr_scalar():
    rng = random.Random(7)
    rows = [[(c, 1) for c in rng.sample(range(100), 8)] for _ in range(64)]
    e = from_rows(rows, 100)
    _, st = spmv_simt(e, [1] * 100)
    # 2 warps, 8 slots, 2 arrays, 4 sectors of 32 bytes for 32 consecutive words
    assert st["matrix_sectors"] == 2 * 8 * 2 * 4
    # CSR with one thread per row: lanes are 8 words apart, one sector each
    assert csr_scalar_sectors(e) == 2 * 8 * 2 * 32


def test_sectors_per_warp_load_are_bounded():
    for seed in range(20):
        rng = random.Random(200 + seed)
        m = rng.randrange(1, 100)
        e = from_dense(random_dense(rng, m, 20, 0.3))
        _, st = spmv_simt(e, [1] * 20)
        assert st["matrix_sectors"] <= 5 * st["warp_loads"]


def test_hyb_split_and_spmv():
    for seed in range(40):
        rng = random.Random(300 + seed)
        m, n = rng.randrange(1, 60), rng.randrange(1, 30)
        a = random_dense(rng, m, n, rng.random() * 0.5)
        if m > 2:
            a[0] = [rng.randrange(1, 9) for _ in range(n)]       # one long row
        rows = [[(j, v) for j, v in enumerate(row) if v] for row in a]
        x = [rng.randrange(-4, 5) for _ in range(n)]
        threshold = max(1, m / 3)
        e, coo = hyb(rows, n, threshold)
        assert hyb_spmv(e, coo, x) == dense_mv(a, x)
        lens = [len(r) for r in rows]
        k = e.k
        assert sum(1 for t in lens if t >= k) >= threshold or k == 0
        assert sum(1 for t in lens if t >= k + 1) < threshold
        assert len(coo) == sum(max(0, t - k) for t in lens)


def test_hyb_default_threshold_is_bell_garland():
    assert hyb_width([5] * 4096) == 5
    assert hyb_width([5] * 4095) == 0          # fewer than 4096 rows: all in COO
    lens = [1] * 6000 + [10] * 3000             # M = 9000, need max(4096, 3000) rows
    assert hyb_width(lens) == 1
