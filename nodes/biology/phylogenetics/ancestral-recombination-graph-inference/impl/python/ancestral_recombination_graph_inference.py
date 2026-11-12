# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ancestral-recombination-graph-inference/. The authors are listed in prov/EM1WEQ.jsonl.

"""The minimum number of recombinations R_min of a binary matrix under infinite sites.

Rows are sequences and columns are sites in their order along the sequence.
Each site mutates once, from 0 to 1, so the root sequence is all 0.

* hudson_kaplan: the lower bound R_M of Hudson and Kaplan (1985). Each pair of
  incompatible sites needs a recombination between them, and R_M is the least
  number of breakpoints that hit every such interval.
* haplotype_bound: the lower bound R_h of Myers and Griffiths (2003). A set S
  of sites on a tree gives at most |S| + 1 distinct haplotypes, and each
  recombination adds at most one more. Local bounds are combined along the
  sequence by dynamic programming.
* r_min: the exact value, by a 0-1 breadth-first search backward in time over
  ancestral states. Coalescence and the removal of a lone derived allele are
  free, and a recombination costs 1. This is exponential and is meant for
  small matrices.
"""

from collections import deque
from itertools import combinations
from typing import Dict, List, Sequence, Tuple

Matrix = Sequence[Sequence[int]]
STAR = 2  # not ancestral material at this site


# ---------- pairwise incompatibility ----------

def gametes(M: Matrix, i: int, j: int) -> set:
    return {(row[i], row[j]) for row in M}


def incompatible(M: Matrix, i: int, j: int, rooted: bool = True) -> bool:
    """Four-gamete test. With rooted=True the root sequence 0...0 counts as a row."""
    g = gametes(M, i, j)
    if rooted:
        g.add((0, 0))
    return len(g) == 4


def incompatible_intervals(M: Matrix, rooted: bool = True) -> List[Tuple[int, int]]:
    m = len(M[0]) if M else 0
    return [(i, j) for i, j in combinations(range(m), 2) if incompatible(M, i, j, rooted)]


def stab(intervals: List[Tuple[int, int]]) -> int:
    """Least number of gaps (g between sites g-1 and g) that hit every interval (i, j),
    meaning i < g <= j. Greedy by right end, as for interval scheduling."""
    count, last = 0, -1
    for i, j in sorted(intervals, key=lambda p: p[1]):
        if i >= last:          # no chosen gap in (i, j]
            count += 1
            last = j           # choose the gap just left of site j
    return count


def hudson_kaplan(M: Matrix, rooted: bool = True) -> int:
    """R_M. Hudson and Kaplan first drop the intervals that contain another one and then
    count disjoint intervals from the left. The greedy stab gives the same number."""
    return stab(incompatible_intervals(M, rooted))


def hudson_kaplan_original(M: Matrix, rooted: bool = True) -> int:
    """The procedure as Hudson and Kaplan state it, for the tests."""
    iv = incompatible_intervals(M, rooted)
    keep = [p for p in iv if not any(q != p and p[0] <= q[0] and q[1] <= p[1] for q in iv)]
    keep.sort()
    count, end = 0, -1
    for i, j in keep:
        if i >= end:
            count += 1
            end = j
    return count


# ---------- the haplotype bound ----------

def local_haplotype_bound(M: Matrix, a: int, b: int, rooted: bool = True) -> int:
    """max over sets S of sites in [a, b] of (distinct haplotypes on S) - |S| - 1."""
    best = 0
    sites = range(a, b + 1)
    rows = [tuple(r) for r in M] + ([tuple(0 for _ in M[0])] if rooted else [])
    for k in range(1, b - a + 2):
        for S in combinations(sites, k):
            h = len({tuple(r[s] for s in S) for r in rows})
            best = max(best, h - k - 1)
    return best


def composite(m: int, local: Dict[Tuple[int, int], int]) -> int:
    """Combine local bounds B(a, b) on site intervals: R[b] = max over a < b of R[a] + B(a, b).
    Two intervals that share only an end site use disjoint gaps, so their bounds add."""
    R = [0] * m
    for b in range(1, m):
        R[b] = max(R[a] + local.get((a, b), 0) for a in range(b))
    return R[m - 1] if m else 0


def haplotype_bound(M: Matrix, rooted: bool = True) -> int:
    m = len(M[0]) if M else 0
    local = {(a, b): local_haplotype_bound(M, a, b, rooted) for a in range(m) for b in range(a + 1, m)}
    for i, j in incompatible_intervals(M, rooted):
        local[(i, j)] = max(local[(i, j)], 1)
    return composite(m, local)


# ---------- the exact minimum ----------

State = Tuple[Tuple[int, ...], ...]


def _clean(seqs: List[Tuple[int, ...]]) -> State:
    """Free reductions that are always safe: drop rows with no material, merge equal rows,
    and turn a derived allele carried by one row only back into 0."""
    seqs = [s for s in seqs if any(c != STAR for c in s)]
    changed = True
    while changed:
        changed = False
        seqs = sorted(set(seqs))
        m = len(seqs[0]) if seqs else 0
        for site in range(m):
            carriers = [r for r, s in enumerate(seqs) if s[site] == 1]
            if len(carriers) == 1:
                r = carriers[0]
                s = list(seqs[r])
                s[site] = 0
                seqs[r] = tuple(s)
                changed = True
    return tuple(sorted(set(seqs)))


def _compatible(a: Tuple[int, ...], b: Tuple[int, ...]) -> bool:
    return all(x == y or x == STAR or y == STAR for x, y in zip(a, b))


def _merge(a: Tuple[int, ...], b: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(y if x == STAR else x for x, y in zip(a, b))


def _moves(state: State):
    """(cost, next state) for each backward event."""
    seqs = list(state)
    for i, j in combinations(range(len(seqs)), 2):
        if _compatible(seqs[i], seqs[j]):
            rest = [s for q, s in enumerate(seqs) if q not in (i, j)]
            yield 0, _clean(rest + [_merge(seqs[i], seqs[j])])
    m = len(seqs[0])
    for i, s in enumerate(seqs):
        rest = seqs[:i] + seqs[i + 1:]
        for g in range(1, m):
            left = s[:g] + (STAR,) * (m - g)
            right = (STAR,) * g + s[g:]
            if any(c != STAR for c in s[:g]) and any(c != STAR for c in s[g:]):
                yield 1, _clean(rest + [left, right])


def r_min(M: Matrix, limit: int = 50) -> int:
    """Least number of recombinations in an infinite-sites history of M with root 0...0."""
    start = _clean([tuple(r) for r in M])
    dist = {start: 0}
    done = set()
    q = deque([start])
    while q:
        x = q.popleft()
        if x in done:
            continue
        done.add(x)
        d = dist[x]
        if len(x) <= 1:
            return d
        if d > limit:
            break
        for c, y in _moves(x):
            if y not in dist or d + c < dist[y]:
                dist[y] = d + c
                if c == 0:
                    q.appendleft(y)
                else:
                    q.append(y)
    raise ValueError("limit reached")


def parse(rows: Sequence[str]) -> List[List[int]]:
    return [[int(c) for c in r] for r in rows]
