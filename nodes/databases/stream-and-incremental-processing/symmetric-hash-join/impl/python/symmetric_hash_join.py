# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symmetric-hash-join/. The authors are listed in prov/2VN9MN.jsonl.

"""Symmetric hash join: a pipelined equi-join that keeps one hash table per input.

The join is the natural join of R and S on their common attributes, under bag
semantics. Tuples arrive one at a time from either input, in any order. Each
arriving tuple is inserted into the table of its own input and probes the
table of the other input, so every result pair is emitted as soon as its
second tuple arrives. A tuple with NULL (None) in a join attribute never
matches, as in SQL, so it is not stored at all.

The output tuple has the attributes of R followed by the attributes of S that
are not in R, the order that dbrel.natural_join uses.
"""

from collections.abc import Iterable, Sequence

R = "R"
S = "S"


class SymmetricHashJoin:
    """The state of one symmetric hash join: two hash tables on the join key."""

    def __init__(self, schema_r: Sequence[str], schema_s: Sequence[str]) -> None:
        self.schema_r = tuple(schema_r)
        self.schema_s = tuple(schema_s)
        self.common = tuple(a for a in self.schema_r if a in self.schema_s)
        self.key_pos = {
            R: [self.schema_r.index(a) for a in self.common],
            S: [self.schema_s.index(a) for a in self.common],
        }
        self.rest_pos = [i for i, a in enumerate(self.schema_s) if a not in self.common]
        self.out_schema = self.schema_r + tuple(self.schema_s[i] for i in self.rest_pos)
        self.tables: dict[str, dict[tuple, list[tuple]]] = {R: {}, S: {}}  # @line L1
        self.stored = 0
        self.probes = 0

    def _key(self, side: str, t: tuple) -> tuple:
        return tuple(t[i] for i in self.key_pos[side])

    def _combine(self, r: tuple, s: tuple) -> tuple:
        return r + tuple(s[i] for i in self.rest_pos)

    def insert(self, side: str, t: Sequence) -> list[tuple]:
        """Process one arriving tuple and return the result tuples it completes."""
        if side not in (R, S):
            raise ValueError("side must be 'R' or 'S'")
        t = tuple(t)
        own, other = (R, S) if side == R else (S, R)  # @line L3
        k = self._key(side, t)  # @line L4
        if any(v is None for v in k):  # @line L5
            return []
        self.tables[own].setdefault(k, []).append(t)  # @line L6
        self.stored += 1
        out = []
        for u in self.tables[other].get(k, ()):  # @line L7
            self.probes += 1
            out.append(self._combine(t, u) if side == R else self._combine(u, t))  # @line L8
        return out

    def memory(self) -> int:
        """The number of tuples held in the two tables."""
        return self.stored


def symmetric_hash_join(schema_r: Sequence[str], schema_s: Sequence[str],
                        arrivals: Iterable[tuple[str, Sequence]]) -> list[list[tuple]]:
    """Run the join over a sequence of (side, tuple) arrivals.

    Returns one list per arrival: the result tuples emitted at that step.
    """
    join = SymmetricHashJoin(schema_r, schema_s)
    steps = []
    for side, t in arrivals:  # @line L2
        steps.append(join.insert(side, t))
    return steps
