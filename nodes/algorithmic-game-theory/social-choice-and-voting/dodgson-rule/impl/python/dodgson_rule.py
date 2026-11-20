# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dodgson-rule/. The authors are listed in prov/81D8GC.jsonl.

from typing import Optional, Sequence

Ranking = Sequence[int]


def pairwise_counts(profile: Sequence[Ranking], m: int) -> list[list[int]]:
    """Return N with N[a][b] the number of voters who rank a above b."""
    N = [[0] * m for _ in range(m)]
    for r in profile:
        for i, a in enumerate(r):
            for b in r[i + 1:]:
                N[a][b] += 1
    return N


def dodgson_score(profile: Sequence[Ranking], m: int, c: int) -> Optional[int]:
    """Return the least number of swaps of adjacent candidates on the ballots that make c a
    Condorcet winner, or None when no number of swaps does (only when there are no voters).

    A dynamic program over the voters. Its state is the vector of deficits: for each b != c,
    how many more voters must put c above b. On each ballot it tries every k, moving c up past
    the k candidates just above it at cost k.
    """
    n = len(profile)
    others = [b for b in range(m) if b != c]
    if not others:
        return 0
    if n == 0:
        return None
    N = pairwise_counts(profile, m)  # @line L1
    q = n // 2 + 1
    slot = {b: t for t, b in enumerate(others)}
    start = tuple(max(0, q - N[c][b]) for b in others)  # @line L2
    F = {start: 0}  # @line L3
    for r in profile:  # @line L4
        pos = list(r).index(c)
        above = [slot[r[pos - 1 - t]] for t in range(pos)]  # nearest first
        G: dict[tuple[int, ...], int] = {}  # @line L5
        for d, cost in F.items():  # @line L6
            cur = list(d)
            for k in range(pos + 1):
                if k > 0:
                    t = above[k - 1]
                    if cur[t] > 0:
                        cur[t] -= 1  # @line L7
                key = tuple(cur)
                if cost + k < G.get(key, cost + k + 1):
                    G[key] = cost + k  # @line L8
        F = G  # @line L9
    return F[tuple(0 for _ in others)]  # @line L10


def dodgson_scores(profile: Sequence[Ranking], m: int) -> list[Optional[int]]:
    """Return the Dodgson score of every candidate."""
    return [dodgson_score(profile, m, c) for c in range(m)]


def dodgson_winners(profile: Sequence[Ranking], m: int) -> frozenset[int]:
    """Return the candidates with the least Dodgson score (all candidates if there are no voters)."""
    s = dodgson_scores(profile, m)
    if any(x is None for x in s):
        return frozenset(range(m))
    best = min(s)
    return frozenset(c for c in range(m) if s[c] == best)  # @line L11


def dodgson(profile: Sequence[Ranking], m: int) -> int:
    """Return the Dodgson winner; a tie goes to the candidate with the smallest index."""
    return min(dodgson_winners(profile, m))
