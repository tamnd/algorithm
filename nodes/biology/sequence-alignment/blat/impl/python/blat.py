# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blat/. The authors are listed in prov/6CXMHF.jsonl.

"""The search stage of BLAT (Kent, 2002) for DNA.

BLAT indexes the non-overlapping K-mers (tiles) of the database, at the
positions 0, K, 2K, ..., and drops tiles that occur too often. It then looks
up every overlapping K-mer of the query. A hit (q, t) says that the query
K-mer at q equals the tile at t. Three ways to accept hits:

  single perfect hits    every hit counts;
  near-perfect hits      the query K-mer may differ from the tile in 1 letter;
  multiple perfect hits  N hits on one diagonal t - q within W query letters.

Accepted hits are grouped into clumps of nearby diagonals; each clump gives
a candidate region for the alignment stage (not modelled here).
"""

from collections import defaultdict

ALPHABET = "ACGT"


def build_index(db: str, k: int, max_occ: int | None = None) -> dict[str, list[int]]:
    index: dict[str, list[int]] = defaultdict(list)
    for t in range(0, len(db) - k + 1, k):  # @line L1: tiles at 0, K, 2K, ...
        index[db[t:t + k]].append(t)  # @line L2
    if max_occ is not None:
        for tile in [x for x, ps in index.items() if len(ps) > max_occ]:
            del index[tile]  # @line L3: drop overused tiles
    return dict(index)


def perfect_hits(index: dict[str, list[int]], query: str, k: int) -> list[tuple[int, int]]:
    hits = []
    for q in range(len(query) - k + 1):  # @line L4: every query K-mer
        for t in index.get(query[q:q + k], ()):  # @line L5
            hits.append((q, t))  # @line L6
    return hits


def near_perfect_hits(index: dict[str, list[int]], query: str, k: int) -> list[tuple[int, int]]:
    """Hits where the query K-mer and the tile differ in at most 1 letter.

    Each query K-mer needs K * (A - 1) + 1 lookups: itself and all its
    neighbours at Hamming distance 1.
    """
    hits = set()
    for q in range(len(query) - k + 1):
        word = query[q:q + k]
        for t in index.get(word, ()):
            hits.add((q, t))
        for i in range(k):
            for a in ALPHABET:
                if a != word[i]:
                    for t in index.get(word[:i] + a + word[i + 1:], ()):
                        hits.add((q, t))
    return sorted(hits)


def multiple_hits(hits: list[tuple[int, int]], n_hits: int, window: int) -> list[tuple[int, int]]:
    """Hits that lie in a group of n_hits hits on one diagonal t - q whose
    query positions span at most `window` letters."""
    by_diag: dict[int, list[int]] = defaultdict(list)
    for q, t in hits:
        by_diag[t - q].append(q)  # @line L7: bucket the hits by diagonal
    keep = set()
    for d, qs in by_diag.items():
        qs.sort()  # @line L8
        lo = 0
        for hi in range(len(qs)):  # @line L9: two pointers over the diagonal
            while qs[hi] - qs[lo] > window:
                lo += 1
            if hi - lo + 1 >= n_hits:  # @line L10: n_hits hits within the window
                for j in range(lo, hi + 1):
                    keep.add((qs[j], qs[j] + d))  # @line L11
    return sorted(keep)


def clumps(hits: list[tuple[int, int]], max_gap: int) -> list[tuple[int, int, int, int]]:
    """Group hits whose diagonals and query positions are both within
    max_gap of a neighbour. Return bounding boxes (q_lo, q_hi, t_lo, t_hi)."""
    order = sorted(hits, key=lambda h: (h[1] - h[0], h[0]))  # @line L12: sort by diagonal
    parent = list(range(len(order)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(len(order)):  # @line L13
        qi, ti = order[i]
        j = i + 1
        while j < len(order) and (order[j][1] - order[j][0]) - (ti - qi) <= max_gap:
            if abs(order[j][0] - qi) <= max_gap:  # @line L14: close in both coordinates
                parent[find(j)] = find(i)
            j += 1
    groups: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for i, h in enumerate(order):
        groups[find(i)].append(h)
    out = []
    for g in groups.values():  # @line L15: one candidate region per clump
        out.append((min(q for q, _ in g), max(q for q, _ in g),
                    min(t for _, t in g), max(t for _, t in g)))
    return sorted(out)


def blat_candidates(db: str, query: str, k: int = 11, n_hits: int = 2, window: int = 100,
                    max_gap: int = 100, max_occ: int | None = None,
                    near: bool = False) -> list[tuple[int, int, int, int]]:
    index = build_index(db, k, max_occ)
    hits = near_perfect_hits(index, query, k) if near else perfect_hits(index, query, k)
    if n_hits > 1:
        hits = multiple_hits(hits, n_hits, window)
    return clumps(hits, max_gap)


# ---- naive versions for the tests ----

def naive_perfect_hits(db: str, query: str, k: int) -> list[tuple[int, int]]:
    return sorted((q, t) for q in range(len(query) - k + 1)
                  for t in range(len(db) - k + 1)
                  if t % k == 0 and query[q:q + k] == db[t:t + k])


def naive_near_hits(db: str, query: str, k: int) -> list[tuple[int, int]]:
    return sorted((q, t) for q in range(len(query) - k + 1)
                  for t in range(0, len(db) - k + 1, k)
                  if sum(x != y for x, y in zip(query[q:q + k], db[t:t + k])) <= 1)


def naive_multiple_hits(hits: list[tuple[int, int]], n_hits: int, window: int) -> list[tuple[int, int]]:
    keep = []
    for q, t in hits:
        d = t - q
        same = [q2 for q2, t2 in hits if t2 - q2 == d]
        if any(sum(s <= x <= s + window for x in same) >= n_hits and s <= q <= s + window
               for s in same):
            keep.append((q, t))
    return sorted(keep)


def naive_clumps(hits: list[tuple[int, int]], max_gap: int) -> list[tuple[int, int, int, int]]:
    hits = sorted(set(hits))
    comp = list(range(len(hits)))
    changed = True
    while changed:
        changed = False
        for i, (qi, ti) in enumerate(hits):
            for j, (qj, tj) in enumerate(hits):
                if abs((ti - qi) - (tj - qj)) <= max_gap and abs(qi - qj) <= max_gap:
                    if comp[i] != comp[j]:
                        comp[i] = comp[j] = min(comp[i], comp[j])
                        changed = True
    groups: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for i, h in enumerate(hits):
        groups[comp[i]].append(h)
    return sorted((min(q for q, _ in g), max(q for q, _ in g),
                   min(t for _, t in g), max(t for _, t in g)) for g in groups.values())


def whole_tiles(start: int, length: int, k: int) -> int:
    """Number of tiles (multiples of k) that fit in [start, start + length)."""
    return sum(1 for t in range(0, start + length - k + 1, k) if t >= start)
