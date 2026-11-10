# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wavefront-parallelism/. The authors are listed in prov/PPA3V1.jsonl.
"""Wavefront (anti-diagonal) evaluation of 2D dynamic programs.

A table D[0..n][0..m] has its row 0 and column 0 given, and each inner cell
(i, j), 1 <= i <= n, 1 <= j <= m, depends on (i-1, j), (i, j-1) and (i-1, j-1).
The wavefront order computes all cells with i + j = d in one parallel round,
for d = 2, ..., n + m.  Each round reads only the two previous diagonals, so the
cells of a round are independent; the code builds each round from the old
diagonals before it writes any cell of it.

The CUDA kernel on the page is not run by these tests.
"""


def cells_on_diagonal(d, n, m):
    """The number of inner cells with i + j = d."""
    return max(0, min(n, d - 1) - max(1, d - m) + 1)


def edit_distance_rows(a, b):
    """The row-by-row Wagner-Fischer program, the sequential reference."""
    n, m = len(a), len(b)
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [i] + [0] * m
        for j in range(1, m + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1]))
        prev = cur
    return prev[m]


def wavefront(n, m, init, cell):
    """Evaluate the table by anti-diagonals.

    init(i, j) gives the cells of row 0 and column 0; cell(i, j, up, left, diag)
    gives an inner cell.  Returns (table, rounds, widths) where widths[k] is the
    number of cells computed in round k.
    """
    D = {}
    for i in range(n + 1):
        D[(i, 0)] = init(i, 0)
    for j in range(m + 1):
        D[(0, j)] = init(0, j)
    widths = []
    for d in range(2, n + m + 1):  # @line L1: one round per diagonal
        lo, hi = max(1, d - m), min(n, d - 1)  # @line L2
        new = [(i, d - i, cell(i, d - i, D[(i - 1, d - i)], D[(i, d - i - 1)], D[(i - 1, d - i - 1)]))
               for i in range(lo, hi + 1)]  # @line L3: all cells of the round in parallel
        for i, j, v in new:  # @line L4: barrier, then write
            D[(i, j)] = v
        widths.append(len(new))
    return D, len(widths), widths


def edit_distance_wavefront(a, b):
    n, m = len(a), len(b)
    D, rounds, widths = wavefront(
        n, m,
        lambda i, j: i + j,
        lambda i, j, up, left, diag: min(up + 1, left + 1, diag + (a[i - 1] != b[j - 1])),
    )
    return D[(n, m)], rounds, widths


def smith_waterman_rows(a, b, match=2, mismatch=-1, gap=-1):
    """Best local alignment score with a linear gap cost, row by row."""
    n, m = len(a), len(b)
    prev = [0] * (m + 1)
    best = 0
    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            s = match if a[i - 1] == b[j - 1] else mismatch
            cur[j] = max(0, prev[j - 1] + s, prev[j] + gap, cur[j - 1] + gap)
            best = max(best, cur[j])
        prev = cur
    return best


def smith_waterman_wavefront(a, b, match=2, mismatch=-1, gap=-1):
    n, m = len(a), len(b)
    D, rounds, _ = wavefront(
        n, m,
        lambda i, j: 0,
        lambda i, j, up, left, diag: max(0, diag + (match if a[i - 1] == b[j - 1] else mismatch), up + gap, left + gap),
    )
    return max(D.values()), rounds


def simt_diagonal_buffers(a, b, threads):
    """Edit distance as one thread block: `threads` threads sweep the diagonals,
    each thread handles cells i = t, t + threads, ...; three diagonal buffers live
    in shared memory, and a barrier ends each round.  Returns (distance, barriers,
    lane_slots, busy) where lane_slots counts thread-rounds and busy the useful ones."""
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return n + m, 0, 0, 0
    # diagonal d is stored by row index i in 0..n
    d2 = {0: 0}                                   # diagonal 0: cell (0, 0)
    d1 = {0: 1, 1: 1}                             # diagonal 1: cells (0, 1) and (1, 0)
    barriers = lane_slots = busy = 0
    for d in range(2, n + m + 1):
        cur = {}
        if d <= m:
            cur[0] = d                            # boundary cell (0, d)
        if d <= n:
            cur[d] = d                            # boundary cell (d, 0)
        lo, hi = max(1, d - m), min(n, d - 1)
        rounds = max(0, -(-(hi - lo + 1) // threads))
        for k in range(rounds):                   # each thread does one cell per pass
            for t in range(threads):
                i = lo + k * threads + t
                lane_slots += 1
                if i <= hi:
                    busy += 1
                    j = d - i
                    cur[i] = min(d1[i - 1] + 1, d1[i] + 1, d2[i - 1] + (a[i - 1] != b[j - 1]))
        barriers += 1                             # __syncthreads() before the next diagonal
        d2, d1 = d1, cur
    return d1[n], barriers, lane_slots, busy


def tiled_wavefront_rounds(n, m, b):
    """Rounds of a wavefront over b x b tiles: one round per tile anti-diagonal."""
    tn, tm = -(-n // b), -(-m // b)
    return tn + tm - 1 if tn and tm else 0
