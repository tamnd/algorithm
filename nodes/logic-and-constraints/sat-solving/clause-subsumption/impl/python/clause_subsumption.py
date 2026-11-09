# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clause-subsumption/. The authors are listed in prov/YEK621.jsonl.

"""Backward subsumption and self-subsuming resolution (strengthening).

The result is logically equivalent to the input over the same variables.
At the fixpoint no clause subsumes another one and no pair of clauses
allows self-subsuming resolution. Clauses are lists of DIMACS ints.
"""

from collections import deque


def subsume(clauses: list[list[int]]) -> list[list[int]]:
    """Return an equivalent clause list without subsumed clauses.

    Tautologies are dropped and duplicate literals are merged first.
    If the empty clause is derived, the result is [[]].
    """
    cls: list[set[int] | None] = []
    for c in clauses:
        s = set(c)
        if any(-a in s for a in s):
            continue  # a tautology is always true
        if not s:
            return [[]]
        cls.append(s)
    occ: dict[int, set[int]] = {}
    for i, c in enumerate(cls):
        for a in c:
            occ.setdefault(a, set()).add(i)

    def count(v: int) -> int:
        return len(occ.get(v, ())) + len(occ.get(-v, ()))

    queue = deque(range(len(cls)))  # @line L1
    queued = set(queue)
    while queue:  # @line L2
        i = queue.popleft()  # @line L3
        queued.discard(i)
        c = cls[i]
        if c is None:
            continue
        v = abs(min(c, key=lambda a: count(abs(a))))  # @line L4
        cands = occ.get(v, set()) | occ.get(-v, set())
        for j in sorted(cands):  # @line L5
            d = cls[j]
            if j == i or d is None or len(d) < len(c):
                continue
            flipped = [a for a in c if a not in d]
            if not flipped:  # @line L6
                cls[j] = None  # C subsumes D: remove D
                for a in d:
                    occ[a].discard(j)
            elif len(flipped) == 1 and -flipped[0] in d:  # @line L7
                gone = -flipped[0]  # resolve on the flipped literal
                d.discard(gone)  # @line L8
                occ[gone].discard(j)
                if not d:
                    return [[]]
                if j not in queued:
                    queue.append(j)
                    queued.add(j)
    return [sorted(c, key=lambda a: (abs(a), a)) for c in cls if c is not None]  # @line L9
