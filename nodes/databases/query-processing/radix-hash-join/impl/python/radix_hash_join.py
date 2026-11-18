# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radix-hash-join/. The authors are listed in prov/Y1EV4Y.jsonl.

"""Radix hash join: multi-pass radix clustering, then one small hash join per cluster.

A relation is a list of tuples, and the join key is the column r_col of R and
s_col of S. The hash of an integer key is h(k) = (k * 2654435761) mod 2^32.
The radix bits are the low b bits of h(k), where b = b_1 + ... + b_P and pass p
uses b_p of them, most significant first. After the last pass, cluster i holds
the tuples with h(k) mod 2^b = i, in their input order.

The join of cluster i of R with cluster i of S uses a bucket-chained hash table
(an array of bucket heads and an array of next links), indexed by the bits of h
above the low b bits, because the low b bits are equal inside a cluster.

An optional trace list records the memory addresses that the algorithm touches,
one per word, and count_misses runs them through a fully associative LRU cache.
"""

from collections import OrderedDict
from collections.abc import Sequence

MASK32 = (1 << 32) - 1
# Base addresses of the arrays in the traced address space.
BASE = {"x0": 0, "x1": 1 << 20, "count": 2 << 20, "r": 3 << 20, "s": 4 << 20, "head": 5 << 20, "next": 6 << 20}


def h(key: int) -> int:
    """Multiplicative hash of an integer key, 32 bits."""
    return (key * 2654435761) & MASK32


def radix_cluster(rows: Sequence[tuple], col: int, passes: Sequence[int], trace: list | None = None):
    """Cluster rows on the low sum(passes) bits of h(row[col]).

    Returns (out, bounds, moves): out is the clustered list, cluster i is
    out[bounds[i]:bounds[i + 1]], and moves[p] is the number of tuples that
    pass p copied.
    """
    x = list(rows)
    n = len(x)
    b = sum(passes)  # @line L1
    clusters = [(0, n)]
    moves = []
    src, dst = "x0", "x1"
    done = 0
    for bp in passes:  # @line L2
        done += bp
        shift = b - done  # @line L3
        fan = 1 << bp
        y = [None] * n
        new_clusters = []
        moved = 0
        for lo, hi in clusters:  # @line L4
            count = [0] * fan
            for i in range(lo, hi):
                j = (h(x[i][col]) >> shift) & (fan - 1)
                count[j] += 1  # @line L5
                if trace is not None:
                    trace += [BASE[src] + i, BASE["count"] + j]
            start = [0] * fan
            pos = lo
            for j in range(fan):
                start[j] = pos  # @line L6
                new_clusters.append((pos, pos + count[j]))
                pos += count[j]
            for i in range(lo, hi):
                j = (h(x[i][col]) >> shift) & (fan - 1)
                y[start[j]] = x[i]  # @line L7
                if trace is not None:
                    trace += [BASE[src] + i, BASE["count"] + j, BASE[dst] + start[j]]
                start[j] += 1
                moved += 1
        x, clusters = y, new_clusters  # @line L8
        src, dst = dst, src
        moves.append(moved)
    bounds = [lo for lo, _ in clusters] + [n]
    return x, bounds, moves  # @line L9


def _pow2_at_least(m: int) -> int:
    size = 1
    while size < m:
        size *= 2
    return size


def radix_join(r_rows: Sequence[tuple], s_rows: Sequence[tuple], r_col: int, s_col: int,
               passes: Sequence[int], trace: list | None = None):
    """Equi-join R and S on r[r_col] == s[s_col]. Output rows are r + s.

    passes lists the radix bits per pass; an empty list gives the plain hash
    join with one table on all of R. Returns (out, stats) with the moves of
    each relation per pass and the number of key comparisons. A NULL key
    (None) never matches, so those rows are dropped before the clustering.
    """
    r_rows = [r for r in r_rows if r[r_col] is not None]
    s_rows = [s for s in s_rows if s[s_col] is not None]
    rc, rb, rmoves = radix_cluster(r_rows, r_col, passes)  # @line L10
    sc, sb, smoves = radix_cluster(s_rows, s_col, passes)
    b = sum(passes)
    out = []
    compares = 0
    for i in range(1 << b):  # @line L11
        rlo, rhi = rb[i], rb[i + 1]
        slo, shi = sb[i], sb[i + 1]
        if rlo == rhi or slo == shi:
            continue
        size = _pow2_at_least(rhi - rlo)
        head = [-1] * size
        nxt = [-1] * (rhi - rlo)
        for t in range(rlo, rhi):  # @line L12
            j = (h(rc[t][r_col]) >> b) & (size - 1)
            nxt[t - rlo] = head[j]
            head[j] = t - rlo
            if trace is not None:
                trace += [BASE["r"] + t, BASE["head"] + j, BASE["next"] + t - rlo]
        for u in range(slo, shi):  # @line L13
            s = sc[u]
            j = (h(s[s_col]) >> b) & (size - 1)
            t = head[j]
            if trace is not None:
                trace += [BASE["s"] + u, BASE["head"] + j]
            while t != -1:
                compares += 1
                r = rc[rlo + t]
                if trace is not None:
                    trace += [BASE["r"] + rlo + t, BASE["next"] + t]
                if r[r_col] == s[s_col]:
                    out.append(r + s)
                t = nxt[t]
    stats = {"r_moves": rmoves, "s_moves": smoves, "compares": compares}
    return out, stats  # @line L14


def count_misses(trace: Sequence[int], lines: int, line_size: int) -> int:
    """Misses of a fully associative LRU cache with `lines` lines of `line_size` words."""
    cache: OrderedDict = OrderedDict()
    misses = 0
    for addr in trace:
        line = addr // line_size
        if line in cache:
            cache.move_to_end(line)
        else:
            misses += 1
            cache[line] = None
            if len(cache) > lines:
                cache.popitem(last=False)
    return misses
