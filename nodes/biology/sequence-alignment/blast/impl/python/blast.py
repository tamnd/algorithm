# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blast/. The authors are listed in prov/0132T2.jsonl.

"""BLAST, the ungapped method of Altschul et al. (1990), with the two-hit
trigger of Altschul et al. (1997) as an option.

The scoring scheme is a function score(a, b) -> int. A segment pair is a
tuple (i, j, length, score): the query segment q[i : i + length] aligned
without gaps to the subject segment y[j : j + length].
"""

import math
from typing import Callable, Iterable, Sequence

Score = Callable[[str, str], int]
HSP = tuple[int, int, int, int]  # (query start, subject start, length, score)


def neighborhood(query: str, w: int, t: int, alphabet: Sequence[str], score: Score) -> dict[str, list[int]]:
    """Map each word of length w that scores at least t against some query
    word to the list of query positions of those query words.

    Words are built letter by letter. A prefix is cut when its score plus the
    best possible score of the remaining positions is below t.
    """
    table: dict[str, list[int]] = {}
    for i in range(len(query) - w + 1):
        qw = query[i : i + w]
        best = [max(score(c, b) for b in alphabet) for c in qw]
        rest = [0] * (w + 1)  # rest[k] = best score of positions k .. w-1
        for k in range(w - 1, -1, -1):
            rest[k] = rest[k + 1] + best[k]
        stack: list[tuple[str, int]] = [("", 0)]
        while stack:
            prefix, s = stack.pop()
            k = len(prefix)
            if k == w:
                table.setdefault(prefix, []).append(i)
                continue
            for b in alphabet:
                s2 = s + score(qw[k], b)
                if s2 + rest[k + 1] >= t:
                    stack.append((prefix + b, s2))
    return table


def extend(q: str, y: str, i: int, j: int, w: int, x: float, score: Score) -> HSP:
    """Ungapped X-drop extension of the word pair q[i:i+w], y[j:j+w].

    Each direction stops at the end of a sequence or when the running score
    falls more than x below the best score seen in that direction. The best
    end in each direction is kept (the shortest one on ties).
    """
    s = sum(score(q[i + k], y[j + k]) for k in range(w))
    # right
    run = best = 0
    right = 0
    k = 0
    while i + w + k < len(q) and j + w + k < len(y):
        run += score(q[i + w + k], y[j + w + k])
        k += 1
        if run > best:
            best, right = run, k
        elif run < best - x:
            break
    s += best
    # left
    run = best = 0
    left = 0
    k = 0
    while i - k - 1 >= 0 and j - k - 1 >= 0:
        run += score(q[i - k - 1], y[j - k - 1])
        k += 1
        if run > best:
            best, left = run, k
        elif run < best - x:
            break
    s += best
    return (i - left, j - left, left + w + right, s)


def blast_pair(
    query: str,
    subject: str,
    table: dict[str, list[int]],
    w: int,
    x: float,
    cutoff: int,
    score: Score,
    two_hit: bool = False,
    a: int = 40,
    skip_covered: bool = True,
) -> list[HSP]:
    """The HSPs with score >= cutoff that BLAST finds between query and subject."""
    found: set[HSP] = set()
    covered: dict[int, int] = {}  # diagonal -> subject end of the last extension
    last_hit: dict[int, int] = {}  # diagonal -> subject start of the last hit (two-hit)
    for j in range(len(subject) - w + 1):  # @line L3
        for i in table.get(subject[j : j + w], ()):  # @line L4
            d = j - i  # @line L5
            if skip_covered and j < covered.get(d, -1):  # @line L6
                continue
            if two_hit:  # @line L7
                prev = last_hit.get(d)
                if prev is None or j - prev < w:
                    if prev is None:
                        last_hit[d] = j
                    continue  # no earlier hit, or one that overlaps: wait
                last_hit[d] = j
                if j - prev > a:
                    continue  # too far apart: this hit starts a new pair
            hsp = extend(query, subject, i, j, w, x, score)  # @line L8
            covered[d] = hsp[1] + hsp[2]
            if hsp[3] >= cutoff:  # @line L9
                found.add(hsp)
    return sorted(found)


def blast(
    query: str,
    database: Iterable[str],
    w: int,
    t: int,
    x: float,
    cutoff: int,
    alphabet: Sequence[str],
    score: Score,
    two_hit: bool = False,
    a: int = 40,
) -> list[tuple[int, HSP]]:
    """Search each database sequence; return (sequence index, HSP) pairs."""
    table = neighborhood(query, w, t, alphabet, score)  # @line L1
    out = []
    for idx, y in enumerate(database):  # @line L2
        for hsp in blast_pair(query, y, table, w, x, cutoff, score, two_hit, a):
            out.append((idx, hsp))
    return out


def segment_score(q: str, y: str, i: int, j: int, length: int, score: Score) -> int:
    return sum(score(q[i + k], y[j + k]) for k in range(length))


def best_ungapped(q: str, y: str, score: Score) -> int:
    """Brute force: the maximal segment pair score (0 for the empty pair)."""
    best = 0
    for i in range(len(q)):
        for j in range(len(y)):
            s = 0
            k = 0
            while i + k < len(q) and j + k < len(y):
                s += score(q[i + k], y[j + k])
                best = max(best, s)
                k += 1
    return best


def smith_waterman_linear(q: str, y: str, score: Score, gap: int) -> int:
    """Reference local alignment score with a linear gap cost gap > 0 per letter."""
    prev = [0] * (len(y) + 1)
    best = 0
    for a in q:
        cur = [0] * (len(y) + 1)
        for jj, b in enumerate(y, 1):
            cur[jj] = max(0, prev[jj - 1] + score(a, b), prev[jj] - gap, cur[jj - 1] - gap)
            best = max(best, cur[jj])
        prev = cur
    return best


INF = math.inf
