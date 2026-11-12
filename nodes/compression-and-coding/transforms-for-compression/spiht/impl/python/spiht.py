# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spiht/. The authors are listed in prov/0AFRWT.jsonl.

"""SPIHT (Said and Pearlman 1996): an embedded coder of a wavelet image by
set partitioning in hierarchical trees, with the binary output of the
paper (no arithmetic coding of the symbols).

The wavelet here is the integer S-transform (the Haar transform by lifting
with rounding), applied in the Mallat layout, so that the full stream is
lossless. The image has R rows and C columns, both multiples of 2^(levels+1),
so that the LL band has even sides and splits into 2 x 2 groups.

For N = R C coefficients and p bit planes, the encoder and the decoder cost
O(N p) time and O(N) space.
"""

from typing import Dict, List, Optional, Sequence, Tuple

Matrix = List[List[int]]
Coord = Tuple[int, int]


# ---------------------------------------------------------------- the transform


def s_forward(x: Sequence[int]) -> Tuple[List[int], List[int]]:
    """Integer Haar (S-transform): d = a - b, s = b + floor(d / 2) = floor((a + b) / 2)."""
    d = [x[2 * k] - x[2 * k + 1] for k in range(len(x) // 2)]
    s = [x[2 * k + 1] + (d[k] >> 1) for k in range(len(x) // 2)]
    return s, d


def s_inverse(s: Sequence[int], d: Sequence[int]) -> List[int]:
    """Inverse of s_forward: b = s - floor(d / 2), a = d + b."""
    out: List[int] = []
    for sk, dk in zip(s, d):
        b = sk - (dk >> 1)
        out += [dk + b, b]
    return out


def wavelet_forward(img: Matrix, levels: int) -> Matrix:
    """Multilevel 2D S-transform in the Mallat layout (rows, then columns, on LL)."""
    a = [list(r) for r in img]
    h, w = len(a), len(a[0])
    for _ in range(levels):
        for r in range(h):
            s, d = s_forward(a[r][:w])
            a[r][:w] = s + d
        for c in range(w):
            s, d = s_forward([a[r][c] for r in range(h)])
            for r, v in enumerate(s + d):
                a[r][c] = v
        h, w = h // 2, w // 2
    return a


def wavelet_inverse(coef: Matrix, levels: int) -> Matrix:
    """Inverse of wavelet_forward."""
    a = [list(r) for r in coef]
    h, w = len(a) >> (levels - 1), len(a[0]) >> (levels - 1)
    for _ in range(levels):
        for c in range(w):
            col = s_inverse([a[r][c] for r in range(h // 2)], [a[r][c] for r in range(h // 2, h)])
            for r in range(h):
                a[r][c] = col[r]
        for r in range(h):
            a[r][:w] = s_inverse(a[r][: w // 2], a[r][w // 2: w])
        h, w = h * 2, w * 2
    return a


# ---------------------------------------------------------------- the trees


class Trees:
    """The spatial orientation trees of an R x C Mallat layout with `levels` levels."""

    def __init__(self, rows: int, cols: int, levels: int) -> None:
        if levels < 1 or rows % (2 << levels) or cols % (2 << levels):
            raise ValueError("rows and cols must be multiples of 2^(levels+1), levels >= 1")
        self.R, self.C = rows, cols
        self.R0, self.C0 = rows >> levels, cols >> levels

    def roots(self) -> List[Coord]:
        """H: the coefficients of the LL band, in raster order."""
        return [(i, j) for i in range(self.R0) for j in range(self.C0)]

    def offspring(self, i: int, j: int) -> List[Coord]:
        """O(i, j): the four direct descendants, or none.

        In the LL band the roots form 2 x 2 groups; the top-left root of a
        group has no offspring, and the other three point to a 2 x 2 block
        in the HL, LH and HH bands of the coarsest level. Elsewhere the
        offspring of (i, j) are the 2 x 2 block at (2i, 2j), if it exists.
        """
        if i < self.R0 and j < self.C0:
            di, dj = i & 1, j & 1
            if di == 0 and dj == 0:
                return []
            r, c = (i - di) + di * self.R0, (j - dj) + dj * self.C0
        else:
            if 2 * i >= self.R or 2 * j >= self.C:
                return []
            r, c = 2 * i, 2 * j
        return [(r, c), (r, c + 1), (r + 1, c), (r + 1, c + 1)]

    def max_tables(self, mag: Matrix) -> Tuple[Matrix, Matrix]:
        """maxD[i][j] = max |c| over D(i, j), maxL[i][j] = max |c| over L(i, j).

        D is the set of all descendants and L = D minus O. Computed bottom-up:
        every child has a larger i + j than its parent, so nodes are visited
        in decreasing order of i + j. Cost O(N).
        """
        R, C = self.R, self.C
        max_d = [[-1] * C for _ in range(R)]
        max_l = [[-1] * C for _ in range(R)]
        for s in range(R + C - 2, -1, -1):
            for i in range(max(0, s - C + 1), min(R, s + 1)):
                j = s - i
                for a, b in self.offspring(i, j):
                    max_d[i][j] = max(max_d[i][j], mag[a][b], max_d[a][b])
                    max_l[i][j] = max(max_l[i][j], max_d[a][b])
        return max_d, max_l


# ---------------------------------------------------------------- the coder

A, B = 0, 1  # the two types of LIS entries


def spiht_encode(coef: Matrix, levels: int) -> Tuple[List[int], int, list]:
    """Encode a wavelet image. Returns (bits, n_max, snapshots).

    n_max is the top plane, floor(lg max |c|), which goes in the header
    (-1 for an all-zero image). snapshots[k] = (n, LIP, LIS, LSP, bits so
    far) after the refinement pass of plane n, for comparison with the
    decoder.
    """
    t = Trees(len(coef), len(coef[0]), levels)
    mag = [[abs(v) for v in row] for row in coef]
    max_d, max_l = t.max_tables(mag)
    n_max = max(max(row) for row in mag).bit_length() - 1
    lip: List[Coord] = t.roots()  # @line L1
    lis: List[Optional[Tuple[int, int, int]]] = [(i, j, A) for i, j in lip if t.offspring(i, j)]
    lsp: List[Coord] = []
    out: List[int] = []
    snaps = []
    n = n_max
    while n >= 0:  # @line L2
        old = len(lsp)
        th = 1 << n
        keep = []
        for i, j in lip:  # @line L3
            s = 1 if mag[i][j] >= th else 0
            out.append(s)
            if s:
                lsp.append((i, j))
                out.append(1 if coef[i][j] < 0 else 0)
            else:
                keep.append((i, j))
        lip = keep
        k = 0
        while k < len(lis):  # @line L4
            i, j, kind = lis[k]
            if kind == A:
                s = 1 if max_d[i][j] >= th else 0  # @line L5
                out.append(s)
                if s:
                    for a, b in t.offspring(i, j):  # @line L6
                        s2 = 1 if mag[a][b] >= th else 0
                        out.append(s2)
                        if s2:
                            lsp.append((a, b))
                            out.append(1 if coef[a][b] < 0 else 0)
                        else:
                            lip.append((a, b))
                    if max_l[i][j] >= 0:  # @line L7
                        lis.append((i, j, B))
                    lis[k] = None
            else:
                s = 1 if max_l[i][j] >= th else 0  # @line L8
                out.append(s)
                if s:
                    for a, b in t.offspring(i, j):  # @line L9
                        lis.append((a, b, A))
                    lis[k] = None
            k += 1
            while k < len(lis) and lis[k] is None:
                k += 1
        lis = [e for e in lis if e is not None]
        for i, j in lsp[:old]:  # @line L10
            out.append((mag[i][j] >> n) & 1)
        snaps.append((n, list(lip), list(lis), list(lsp), len(out)))
        n -= 1  # @line L11
    return out, n_max, snaps


class _OutOfBits(Exception):
    pass


def spiht_decode(bits: Sequence[int], rows: int, cols: int, levels: int, n_max: int) -> Tuple[Matrix, int, list]:
    """Decode any prefix of an SPIHT stream.

    Returns (estimates, n, snapshots): n is the plane of the pass in which
    the bits ran out (-1 if the stream was complete), and snapshots are as
    in spiht_encode, for the passes that were completed. A significant
    coefficient whose magnitude bits are known down to plane k is
    reconstructed at the middle of its interval, m + 2^(k-1).
    """
    t = Trees(rows, cols, levels)
    known_mag = [[0] * cols for _ in range(rows)]
    neg = [[False] * cols for _ in range(rows)]
    low = [[-1] * cols for _ in range(rows)]  # lowest known plane, -1 while insignificant
    pos = 0

    def read() -> int:
        nonlocal pos
        if pos >= len(bits):
            raise _OutOfBits
        pos += 1
        return bits[pos - 1]

    def significant(a: int, b: int, n: int) -> None:
        sign = read()  # if this read fails, the coefficient stays insignificant
        neg[a][b] = sign == 1
        known_mag[a][b] = 1 << n
        low[a][b] = n
        lsp.append((a, b))

    lip: List[Coord] = t.roots()
    lis: List[Optional[Tuple[int, int, int]]] = [(i, j, A) for i, j in lip if t.offspring(i, j)]
    lsp: List[Coord] = []
    snaps = []
    has_l = lambda i, j: any(t.offspring(a, b) for a, b in t.offspring(i, j))
    n = n_max
    try:
        while n >= 0:
            old = len(lsp)
            keep = []
            for idx, (i, j) in enumerate(lip):
                try:
                    if read():
                        significant(i, j, n)
                    else:
                        keep.append((i, j))
                except _OutOfBits:
                    lip = keep + lip[idx:]
                    raise
            lip = keep
            k = 0
            while k < len(lis):
                i, j, kind = lis[k]
                if kind == A:
                    if read():
                        for a, b in t.offspring(i, j):
                            if read():
                                significant(a, b, n)
                            else:
                                lip.append((a, b))
                        if has_l(i, j):
                            lis.append((i, j, B))
                        lis[k] = None
                else:
                    if read():
                        for a, b in t.offspring(i, j):
                            lis.append((a, b, A))
                        lis[k] = None
                k += 1
                while k < len(lis) and lis[k] is None:
                    k += 1
            lis = [e for e in lis if e is not None]
            for i, j in lsp[:old]:
                if read():
                    known_mag[i][j] |= 1 << n
                low[i][j] = n
            snaps.append((n, list(lip), list(lis), list(lsp), pos))
            n -= 1
    except _OutOfBits:
        pass
    est = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            k = low[i][j]
            if k >= 0:
                m = known_mag[i][j] + ((1 << (k - 1)) if k > 0 else 0)
                est[i][j] = -m if neg[i][j] else m
    return est, n, snaps


def compress(img: Matrix, levels: int) -> Tuple[List[int], int]:
    """Transform and encode an integer image; returns (bits, n_max)."""
    bits, n_max, _ = spiht_encode(wavelet_forward(img, levels), levels)
    return bits, n_max


def decompress(bits: Sequence[int], rows: int, cols: int, levels: int, n_max: int) -> Matrix:
    """Decode a prefix and invert the transform (rounded estimates)."""
    est, _, _ = spiht_decode(bits, rows, cols, levels, n_max)
    return wavelet_inverse(est, levels)
