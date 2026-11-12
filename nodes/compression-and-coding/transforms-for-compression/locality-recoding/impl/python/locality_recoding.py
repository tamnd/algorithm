# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/locality-recoding/. The authors are listed in prov/K1G2D0.jsonl.

"""Two online recodings that turn recent symbols into small integers.

Both use a virtual prefix: before time 0, the symbols A[sigma-1], ..., A[1],
A[0] are used at the times -sigma, ..., -2, -1, so every symbol has a last
use.

  interval code (Elias, 1987): Y[t] = t - last(X[t]), the number of steps
      back to the last use. O(1) time per symbol each way with a hash map and
      the decoded history.
  recency rank (Elias, 1987; the move-to-front transform): Y[t] = the number
      of distinct symbols used after last(X[t]) and before t. Here it is
      computed with a Fenwick tree over the times, which marks the last use
      of each symbol: O(log(n + sigma)) time per symbol.

For every t, recency_rank[t] + 1 <= interval[t].
"""

from collections.abc import Hashable, Sequence
from typing import TypeVar

S = TypeVar("S", bound=Hashable)


def interval_encode(x: Sequence[S], alphabet: Sequence[S]) -> list[int]:
    """Elias interval code: the distance back to the last use of each symbol."""
    last = {a: -1 - k for k, a in enumerate(alphabet)}  # @line L1
    out = []
    for t in range(len(x)):  # @line L2
        out.append(t - last[x[t]])  # @line L3
        last[x[t]] = t  # @line L4
    return out  # @line L5


def interval_decode(y: Sequence[int], alphabet: Sequence[S]) -> list[S]:
    """Read each symbol from the history: X[t] = history[t - Y[t]]."""
    sigma = len(alphabet)
    history = list(reversed(alphabet))  # times -sigma .. -1 at indices 0 .. sigma-1
    out: list[S] = []
    for t, d in enumerate(y):
        if not 1 <= d <= t + sigma:
            raise ValueError("interval out of range")
        x = history[t - d + sigma]
        history.append(x)
        out.append(x)
    return out


class _Fenwick:
    def __init__(self, n: int) -> None:
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, i: int, v: int) -> None:
        i += 1
        while i <= self.n:
            self.tree[i] += v
            i += i & -i

    def prefix(self, i: int) -> int:
        """Sum of the entries 0 .. i-1."""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s


def recency_rank_encode(x: Sequence[S], alphabet: Sequence[S]) -> list[int]:
    """Move-to-front ranks, by counting the marked last uses after last(X[t])."""
    sigma = len(alphabet)
    fen = _Fenwick(len(x) + sigma)
    last = {}
    for k, a in enumerate(alphabet):
        last[a] = sigma - 1 - k  # time -1-k, shifted by sigma
        fen.add(last[a], 1)
    out = []
    for t, s in enumerate(x):
        now = t + sigma
        p = last[s]
        out.append(fen.prefix(now) - fen.prefix(p + 1))
        fen.add(p, -1)
        fen.add(now, 1)
        last[s] = now
    return out


def recency_rank_decode(y: Sequence[int], alphabet: Sequence[S]) -> list[S]:
    """Inverse of recency_rank_encode, with the move-to-front list."""
    table = list(alphabet)
    out = []
    for r in y:
        s = table.pop(r)
        table.insert(0, s)
        out.append(s)
    return out


def inversion_frequencies(x: Sequence[S], alphabet: Sequence[S]) -> list[list[int]]:
    """Inversion frequencies of Arnavut and Magliveras: for each symbol a in
    alphabet order, and each use of a, the number of symbols larger than a
    (in alphabet order) since the previous use of a, or since the start."""
    rank = {a: k for k, a in enumerate(alphabet)}
    out = []
    for a in alphabet:
        row, count = [], 0
        for s in x:
            if s == a:
                row.append(count)
                count = 0
            elif rank[s] > rank[a]:
                count += 1
        out.append(row)
    return out


def inversion_frequencies_decode(rows: Sequence[Sequence[int]], alphabet: Sequence[S]) -> list[S]:
    """Rebuild x from the rows, the largest symbol first: each symbol a is
    placed into the gaps between the symbols already placed, which are all
    larger than a."""
    seq: list[S] = []
    for a, row in zip(reversed(alphabet), reversed(rows)):
        new: list[S] = []
        i = 0
        for c in row:
            new.extend(seq[i : i + c])
            i += c
            new.append(a)
        new.extend(seq[i:])
        seq = new
    return seq
