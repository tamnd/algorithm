# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fasta-algorithm/. The authors are listed in prov/VK9YGQ.jsonl.

"""The FASTA heuristic of Pearson and Lipman (1988), as described by
Pearson (1990): ktup lookup, diagonal regions, init1, initn and opt.

score(a, b) -> int is the substitution score. Gaps in the opt step have a
linear cost: a gap of length L costs gap * L. A region is a tuple
(query start, subject start, length, score) of an ungapped segment pair.
"""

from typing import Callable, Iterable

Score = Callable[[str, str], int]
Region = tuple[int, int, int, int]


def ktup_matches(q: str, y: str, ktup: int) -> list[tuple[int, int]]:
    """All (i, j) with q[i : i + ktup] == y[j : j + ktup], by a lookup table of q."""
    table: dict[str, list[int]] = {}
    for i in range(len(q) - ktup + 1):
        table.setdefault(q[i : i + ktup], []).append(i)
    return [(i, j) for j in range(len(y) - ktup + 1) for i in table.get(y[j : j + ktup], ())]


def diagonal_regions(matches: Iterable[tuple[int, int]], ktup: int, value: int, keep: int = 10) -> list[Region]:
    """Step 1. Join ktup matches on each diagonal into regions.

    A region starts with score `value` at a match. A later match on the
    same diagonal at distance g (residues between the end of the region and
    the match) extends the region when g <= its score: the score becomes
    score - g + value. Otherwise the region is closed and a new one starts.
    The `keep` best regions are returned.
    """
    by_diag: dict[int, list[tuple[int, int]]] = {}
    for i, j in matches:
        by_diag.setdefault(j - i, []).append((i, j))
    regions: list[Region] = []
    for d, hits in by_diag.items():
        hits.sort()
        start_i = start_j = end_j = score = None
        for i, j in hits:
            if score is not None:
                g = max(0, j - end_j)
                if g <= score:
                    score = score - g + value
                    end_j = max(end_j, j + ktup)
                    continue
                regions.append((start_i, start_j, end_j - start_j, score))
            start_i, start_j, end_j, score = i, j, j + ktup, value
        if score is not None:
            regions.append((start_i, start_j, end_j - start_j, score))
    regions.sort(key=lambda r: (-r[3], r[0], r[1]))
    return regions[:keep]


def rescore(q: str, y: str, region: Region, score: Score) -> Region:
    """Step 2. Rescore the region's diagonal stretch with the substitution
    scores and trim it to its best-scoring sub-segment (Kadane's scan)."""
    i0, j0, length, _ = region
    best, best_a, best_b = 0, 0, 0
    run, a = 0, 0
    for k in range(length):
        run += score(q[i0 + k], y[j0 + k])
        if run <= 0:
            run, a = 0, k + 1
        elif run > best:
            best, best_a, best_b = run, a, k + 1
    return (i0 + best_a, j0 + best_a, best_b - best_a, best)


def join_regions(regions: list[Region], penalty: int) -> int:
    """Step 3. initn: the best score of a chain of compatible regions, each
    after the previous one in both sequences, minus `penalty` per join."""
    rs = sorted(regions, key=lambda r: (r[0], r[1]))
    best_end: list[int] = []
    best = 0
    for b, (ib, jb, lb, sb) in enumerate(rs):
        v = sb
        for a in range(b):
            ia, ja, la, _ = rs[a]
            if ia + la <= ib and ja + la <= jb:
                v = max(v, best_end[a] + sb - penalty)
        best_end.append(v)
        best = max(best, v)
    return best


def banded_local_score(q: str, y: str, score: Score, gap: int, center: int, half: int) -> int:
    """Step 4. Smith-Waterman score with linear gap cost, over the cells
    (i, j) whose diagonal j - i lies in [center - half, center + half]."""
    n = len(y)
    neg = float("-inf")
    prev: dict[int, float] = {j: 0 for j in range(n + 1)}  # row 0 is 0
    best = 0
    for i in range(1, len(q) + 1):
        cur: dict[int, float] = {0: 0}  # column 0 is 0
        lo = max(1, i + center - half)
        hi = min(n, i + center + half)
        for j in range(lo, hi + 1):
            v = max(
                0,
                prev.get(j - 1, neg) + score(q[i - 1], y[j - 1]),
                prev.get(j, neg) - gap,
                cur.get(j - 1, neg) - gap,
            )
            cur[j] = v
            if v > best:
                best = v
        prev = cur
    return int(best)


def fasta_pair(
    q: str,
    y: str,
    ktup: int,
    score: Score,
    value: int,
    penalty: int = 20,
    gap: int = 4,
    width: int = 32,
) -> dict[str, int]:
    """The three FASTA scores of one pair: init1, initn and opt."""
    matches = ktup_matches(q, y, ktup)  # @line L1
    regions = diagonal_regions(matches, ktup, value)  # @line L2
    if not regions:
        return {"init1": 0, "initn": 0, "opt": 0}
    trimmed = [rescore(q, y, r, score) for r in regions]  # @line L3
    best = max(trimmed, key=lambda r: r[3])
    init1 = best[3]  # @line L4
    initn = join_regions([r for r in trimmed if r[3] > 0], penalty)  # @line L5
    center = best[1] - best[0]
    opt = banded_local_score(q, y, score, gap, center, width // 2)  # @line L6
    return {"init1": init1, "initn": initn, "opt": opt}


def fasta_search(q: str, database: list[str], ktup: int, score: Score, value: int, top: int = 10, **kw: int) -> list[tuple[int, dict[str, int]]]:
    """Rank the library by initn and report the scores of the best `top`."""
    scored = [(i, fasta_pair(q, y, ktup, score, value, **kw)) for i, y in enumerate(database)]
    scored.sort(key=lambda t: (-t[1]["initn"], t[0]))
    return scored[:top]


def smith_waterman(q: str, y: str, score: Score, gap: int) -> int:
    """Full local alignment score with linear gap cost, for reference."""
    prev = [0] * (len(y) + 1)
    best = 0
    for a in q:
        cur = [0] * (len(y) + 1)
        for j, b in enumerate(y, 1):
            cur[j] = max(0, prev[j - 1] + score(a, b), prev[j] - gap, cur[j - 1] - gap)
            best = max(best, cur[j])
        prev = cur
    return best
