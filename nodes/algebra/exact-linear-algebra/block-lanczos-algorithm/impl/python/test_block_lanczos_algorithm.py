# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-lanczos-algorithm/. The authors are listed in prov/ZXGZZS.jsonl.

import random

from block_lanczos_algorithm import (add, b_times, block_lanczos_kernel, bt_times, inner,
                                     select, times_small)


# Dense GF(2) references: a matrix is a list of rows, each a list of 0/1.

def dense(b, n):
    return [[1 if j in set(row) else 0 for j in range(n)] for row in b]


def matmul(p, q):
    if not p:
        return []
    k = len(q)
    cols = len(q[0]) if q else 0
    return [[sum(p[i][t] & q[t][j] for t in range(k)) & 1 for j in range(cols)] for i in range(len(p))]


def transpose(p, cols):
    return [[p[i][j] for i in range(len(p))] for j in range(cols)]


def to_dense(block, s):
    return [[x >> c & 1 for c in range(s)] for x in block]


def from_dense(rows):
    return [sum(bit << c for c, bit in enumerate(r)) for r in rows]


def rank(rows):
    """Rank over GF(2) of a list of 0/1 vectors, by elimination on bit masks."""
    basis = {}
    for r in rows:
        vec = sum(bit << c for c, bit in enumerate(r))
        while vec:
            top = vec.bit_length() - 1
            if top not in basis:
                basis[top] = vec
                break
            vec ^= basis[top]
    return len(basis)


def nullity(b, n):
    return n - rank(dense(b, n))


def random_sparse(rng, m, n, per_row):
    return [sorted(rng.sample(range(n), min(per_row, n))) for _ in range(m)]


def check_output(b, n, vecs):
    """Every vector is nonzero with B x = 0, and the vectors are independent."""
    d = dense(b, n)
    for x in vecs:
        assert len(x) == n and any(x)
        assert all(sum(r[j] & x[j] for j in range(n)) % 2 == 0 for r in d)
    assert rank(vecs) == len(vecs)
    assert len(vecs) <= nullity(b, n)


def test_helpers_against_dense():
    rng = random.Random(1)
    for _ in range(60):
        m, n, s = rng.randint(0, 9), rng.randint(1, 9), rng.randint(1, 6)
        b = random_sparse(rng, m, n, rng.randint(0, n))
        bd = dense(b, n)
        v = [rng.getrandbits(s) for _ in range(n)]
        u = [rng.getrandbits(s) for _ in range(m)]
        w = [rng.getrandbits(s) for _ in range(n)]
        sm = [rng.getrandbits(s) for _ in range(s)]
        vd, ud, wd, smd = to_dense(v, s), to_dense(u, s), to_dense(w, s), to_dense(sm, s)
        if m:
            assert to_dense(b_times(b, v), s) == matmul(bd, vd)
            assert to_dense(bt_times(b, u, n), s) == matmul(transpose(bd, n), ud)
        assert to_dense(inner(v, w, s), s) == matmul(transpose(vd, s), wd)
        assert to_dense(times_small(v, sm), s) == matmul(vd, smd)
        assert add(v, w) == [a ^ c for a, c in zip(v, w)]


def test_select_defining_conditions():
    rng = random.Random(2)
    seen_ok = 0
    for _ in range(400):
        s = rng.randint(1, 6)
        full = (1 << s) - 1
        g = [[rng.getrandbits(1) for _ in range(s)] for _ in range(rng.randint(1, 8))]
        t = from_dense(matmul(transpose(g, s), g))  # symmetric, like V^T A V
        prev = rng.getrandbits(s)
        res = select(t, prev, s)
        if res is None:
            continue
        seen_ok += 1
        winv, mask = res
        assert mask | prev == full
        sel = [c for c in range(s) if mask >> c & 1]
        td, wd = to_dense(t, s), to_dense(winv, s)
        # winv vanishes outside the selected rows and columns
        assert all(wd[i][j] == 0 for i in range(s) for j in range(s) if i not in sel or j not in sel)
        # on the selected part, winv is the inverse of S^T T S
        sub = [[td[i][j] for j in sel] for i in sel]
        wsub = [[wd[i][j] for j in sel] for i in sel]
        assert matmul(sub, wsub) == [[int(i == j) for j in range(len(sel))] for i in range(len(sel))]
        # S^T T S has full rank, and adding any other column of T makes it singular
        r_t = rank(td)
        assert len(sel) == r_t
    assert seen_ok > 100


def test_worked_example():
    b = [[0, 1], [1, 2], [0, 2], [3, 4], [4, 5]]
    trace = []
    vecs = block_lanczos_kernel(b, 6, s=2, seed=0, tries=1, trace=trace)
    assert sorted(vecs) == [[1, 1, 1, 0, 0, 0], [1, 1, 1, 1, 1, 1]]
    assert len(trace) == 1
    v0, mask = trace[0]
    assert to_dense(v0, 2) == [[0, 1], [0, 0], [0, 1], [0, 1], [1, 1], [1, 0]] and mask == 3
    check_output(b, 6, vecs)


def test_edge_cases():
    assert block_lanczos_kernel([], 0) == []
    assert block_lanczos_kernel([[], []], 0) == []
    # no rows: every vector is in the kernel
    vecs = block_lanczos_kernel([], 5, s=8)
    check_output([], 5, vecs)
    assert len(vecs) == 5
    # zero matrix
    vecs = block_lanczos_kernel([[], [], []], 4, s=8)
    check_output([[], [], []], 4, vecs)
    assert len(vecs) == 4
    # 1 x 1
    assert block_lanczos_kernel([[0]], 1, s=4) == []
    vecs = block_lanczos_kernel([[]], 1, s=4)
    assert vecs == [[1]]
    # identity: nullity 0, nothing to find
    for n in (1, 2, 7, 30):
        assert block_lanczos_kernel([[i] for i in range(n)], n, s=8) == []
    # zero columns: e_j for an unused column j is in the kernel
    b = [[0, 1], [1, 3], [0, 3]]
    vecs = block_lanczos_kernel(b, 5, s=8)
    check_output(b, 5, vecs)
    assert len(vecs) == nullity(b, 5) == 3
    # more columns than rows
    rng = random.Random(3)
    b = random_sparse(rng, 10, 25, 4)
    vecs = block_lanczos_kernel(b, 25, s=16)
    check_output(b, 25, vecs)
    assert len(vecs) >= 1
    # repeated rows
    b = [[0, 2, 5]] * 6 + [[1, 3]]
    vecs = block_lanczos_kernel(b, 6, s=8)
    check_output(b, 6, vecs)
    assert len(vecs) == 4


def test_orthogonality_of_w_blocks():
    rng = random.Random(4)
    for _ in range(5):
        n, m = 60, 58
        b = random_sparse(rng, m, n, 4)
        trace = []
        block_lanczos_kernel(b, n, s=8, seed=rng.randrange(10**6), tries=1, trace=trace)
        assert len(trace) >= 3
        ws = [[x & mask for x in v] for v, mask in trace]  # W_i spanned by V_i S_i
        aws = [bt_times(b, b_times(b, w), n) for w in ws]
        for i in range(len(ws)):
            for j in range(i):
                assert not any(inner(ws[j], aws[i], 8))


def test_random_correctness_and_success():
    rng = random.Random(5)
    with_kernel = hit = found_total = null_total = 0
    for case in range(500):
        n = rng.randint(1, 24)
        m = rng.randint(0, n + 3)
        b = random_sparse(rng, m, n, rng.randint(1, 4))
        s = rng.choice((4, 8, 16))
        vecs = block_lanczos_kernel(b, n, s=s, seed=case, tries=3)
        check_output(b, n, vecs)
        k = nullity(b, n)
        if k:
            with_kernel += 1
            hit += bool(vecs)
            found_total += len(vecs)
            null_total += min(k, s)  # one run yields at most about s vectors
        else:
            assert vecs == []
    assert with_kernel > 200
    assert hit >= 0.95 * with_kernel
    assert found_total >= 0.85 * null_total


def test_large_sparse():
    rng = random.Random(6)
    n, m = 300, 290
    b = random_sparse(rng, m, n, 5)
    vecs = block_lanczos_kernel(b, n, s=32, seed=1)
    check_output(b, n, vecs)
    assert len(vecs) >= 1
