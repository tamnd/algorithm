# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ellpack-format/. The authors are listed in prov/6VRCR7.jsonl.
"""The ELLPACK (ELL) sparse format, ELLPACK-R and the HYB format, with a SIMT SpMV simulator.

An M x N matrix with at most K nonzeros per row is stored in two arrays of
M*K slots, data and indices, in column-major order: slot k of row r is at
position k*M + r.  Rows with fewer than K nonzeros are padded with the value 0
and the column PAD.  ELLPACK-R adds the array rowlen of the row lengths.

The SIMT simulator runs one thread per row in warps of 32 and counts the
32-byte sectors that each warp load touches, with 4-byte values and indices.
The CUDA kernels on the page are not run by these tests.
"""

PAD = -1
WARP = 32
WORD = 4          # bytes per value and per index
SECTOR = 32       # bytes per memory sector


class Ell:
    def __init__(self, m, n, k, data, indices, rowlen):
        self.m, self.n, self.k = m, n, k
        self.data, self.indices, self.rowlen = data, indices, rowlen

    @property
    def nnz(self):
        return sum(self.rowlen)


def from_rows(rows, n, k=None):
    """Build ELL from a list of rows, each a list of (column, value) with distinct columns."""
    m = len(rows)
    rowlen = [len(r) for r in rows]
    width = max(rowlen, default=0) if k is None else k  # @line L1: K = max row length
    if any(x > width for x in rowlen):
        raise ValueError("a row has more than K entries")
    data = [0] * (m * width)  # @line L2: M*K slots of padding
    indices = [PAD] * (m * width)
    for r, row in enumerate(rows):  # @line L3
        for s, (c, v) in enumerate(sorted(row)):  # @line L4
            data[s * m + r] = v  # @line L5: column-major slot
            indices[s * m + r] = c
    return Ell(m, n, width, data, indices, rowlen)


def from_dense(a):
    n = len(a[0]) if a else 0
    rows = [[(j, v) for j, v in enumerate(row) if v != 0] for row in a]
    return from_rows(rows, n)


def to_dense(e):
    a = [[0] * e.n for _ in range(e.m)]
    for s in range(e.k):
        for r in range(e.m):
            c = e.indices[s * e.m + r]
            if c != PAD:
                a[r][c] = e.data[s * e.m + r]
    return a


def get(e, r, c):
    """Entry (r, c) by a scan of the K slots of row r."""
    for s in range(e.k):
        if e.indices[s * e.m + r] == c:
            return e.data[s * e.m + r]
    return 0


def spmv(e, x):
    """y = A x, one row after another (the sequential reference for the layout)."""
    y = [0] * e.m
    for r in range(e.m):  # @line L6: one thread per row
        acc = 0
        for s in range(e.k):  # @line L7
            c = e.indices[s * e.m + r]  # @line L8
            if c != PAD:  # @line L9: skip padding
                acc += e.data[s * e.m + r] * x[c]  # @line L10
        y[r] = acc  # @line L11
    return y


def _sectors(addresses):
    return len({a * WORD // SECTOR for a in addresses})


def spmv_simt(e, x, use_rowlen=False):
    """SpMV with one thread per row in warps of 32, counting memory sectors.

    Without use_rowlen (plain ELL) every lane runs all K slots and loads the
    padding.  With use_rowlen (ELLPACK-R) lane r stops after rowlen[r] slots,
    and the warp runs max(rowlen) over its lanes.
    Returns (y, stats).
    """
    y = [0] * e.m
    st = {"matrix_sectors": 0, "warp_loads": 0, "lane_slots": 0, "x_loads": 0, "flops": 0}
    for w0 in range(0, e.m, WARP):
        lanes = list(range(w0, min(e.m, w0 + WARP)))
        acc = {r: 0 for r in lanes}
        steps = max((e.rowlen[r] for r in lanes), default=0) if use_rowlen else e.k
        for s in range(steps):
            active = [r for r in lanes if not use_rowlen or s < e.rowlen[r]]
            addr = [s * e.m + r for r in active]
            st["warp_loads"] += 2
            st["matrix_sectors"] += 2 * _sectors(addr)  # data and indices
            st["lane_slots"] += len(active)
            for r in active:
                c = e.indices[s * e.m + r]
                if c != PAD:
                    acc[r] += e.data[s * e.m + r] * x[c]
                    st["x_loads"] += 1
                    st["flops"] += 2
        for r in lanes:
            y[r] = acc[r]
    return y, st


def csr_scalar_sectors(e):
    """Sectors that a one-thread-per-row CSR kernel touches for values and column indices."""
    rowptr = [0]
    for x in e.rowlen:
        rowptr.append(rowptr[-1] + x)
    total = 0
    for w0 in range(0, e.m, WARP):
        lanes = list(range(w0, min(e.m, w0 + WARP)))
        for s in range(max((e.rowlen[r] for r in lanes), default=0)):
            addr = [rowptr[r] + s for r in lanes if s < e.rowlen[r]]
            total += 2 * _sectors(addr)
    return total


def storage_words(m, k, nnz, fmt):
    """Words of 4 bytes for the matrix arrays of each format."""
    if fmt == "ell":
        return 2 * m * k
    if fmt == "ellr":
        return 2 * m * k + m
    if fmt == "csr":
        return 2 * nnz + m + 1
    if fmt == "coo":
        return 3 * nnz
    raise ValueError(fmt)


def hyb_width(rowlen, threshold=None):
    """Bell and Garland: the largest K such that at least max(4096, M/3) rows have K or more entries."""
    m = len(rowlen)
    need = max(4096, m / 3) if threshold is None else threshold
    k = 0
    while sum(1 for x in rowlen if x >= k + 1) >= need:
        k += 1
    return k


def hyb(rows, n, threshold=None):
    """Split rows into an ELL part of width K and a COO list of (row, column, value) for the rest."""
    rowlen = [len(r) for r in rows]
    k = hyb_width(rowlen, threshold)
    ell_rows, coo = [], []
    for r, row in enumerate(rows):
        row = sorted(row)
        ell_rows.append(row[:k])
        coo.extend((r, c, v) for c, v in row[k:])
    return from_rows(ell_rows, n, k), coo


def hyb_spmv(e, coo, x):
    y = spmv(e, x)
    for r, c, v in coo:
        y[r] += v * x[c]
    return y
