# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schulze-method/. The authors are listed in prov/PFHMFN.jsonl.

from typing import Sequence

Ranking = Sequence[int]


def margin_matrix(profile: Sequence[Ranking], m: int) -> list[list[int]]:
    """Return M with M[a][b] = (voters who rank a above b) - (voters who rank b above a)."""
    M = [[0] * m for _ in range(m)]
    for r in profile:
        for i, a in enumerate(r):
            for b in r[i + 1:]:
                M[a][b] += 1
                M[b][a] -= 1
    return M


def strongest_paths(profile: Sequence[Ranking], m: int) -> list[list[int]]:
    """Return p with p[a][b] the strength of the strongest path from a to b.

    A link a -> b has strength M[a][b] when M[a][b] > 0, and there is no link otherwise. The
    strength of a path is its weakest link, and p[a][b] = 0 when there is no path. The
    diagonal is not used. Time O(n m^2 + m^3).
    """
    M = margin_matrix(profile, m)  # @line L1
    p = [[M[a][b] if M[a][b] > 0 else 0 for b in range(m)] for a in range(m)]  # @line L2
    for k in range(m):  # @line L3
        pk = p[k]
        for i in range(m):  # @line L4
            if i == k:
                continue
            pik = p[i][k]
            if pik == 0:
                continue
            pi = p[i]
            for j in range(m):
                if j != i and j != k:
                    via = pik if pik < pk[j] else pk[j]
                    if via > pi[j]:  # @line L5
                        pi[j] = via
    return p


def schulze_winners(profile: Sequence[Ranking], m: int) -> frozenset[int]:
    """Return the Schulze winners: the a with p[a][b] >= p[b][a] for every b."""
    p = strongest_paths(profile, m)
    return frozenset(a for a in range(m)  # @line L6
                     if all(p[a][b] >= p[b][a] for b in range(m) if b != a))


def schulze(profile: Sequence[Ranking], m: int) -> int:
    """Return the Schulze winner; a tie goes to the candidate with the smallest index."""
    return min(schulze_winners(profile, m))  # @line L7


def schulze_ranking(profile: Sequence[Ranking], m: int) -> tuple[int, ...]:
    """Return a ranking that extends the Schulze relation (a above b when p[a][b] > p[b][a]).

    It repeatedly takes the smallest candidate that no remaining candidate beats.
    """
    p = strongest_paths(profile, m)
    left = set(range(m))
    out = []
    while left:
        top = min(a for a in left if all(p[a][b] >= p[b][a] for b in left if b != a))
        out.append(top)
        left.remove(top)
    return tuple(out)
