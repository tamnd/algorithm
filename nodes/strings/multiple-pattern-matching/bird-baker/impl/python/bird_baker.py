# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bird-baker/. The authors are listed in prov/WZE4CC.jsonl.
"""Bird-Baker two-dimensional matching for a set of rectangular patterns.

A text or a pattern is a list of rows, all of the same length. The result is the sorted
list of triples (r, c, j) such that pattern j occurs with its top-left corner at row r
and column c of the text. Indices are 0-based and occurrences may overlap. Patterns of
different widths are handled by one pass per width.
"""

from __future__ import annotations

from collections import deque
from typing import Hashable, Sequence

Grid = Sequence[Sequence[Hashable]]


class _Automaton:
    """Aho-Corasick automaton over sequences of hashable symbols."""

    def __init__(self, words: Sequence[Sequence[Hashable]]) -> None:
        self.goto: list[dict[Hashable, int]] = [{}]
        self.depth: list[int] = [0]
        self.word: list[int] = [-1]  # index of the word that ends at this node, or -1
        self.out: list[list[int]] = [[]]  # all words that end at this node (with failure links)
        for index, w in enumerate(words):
            q = 0
            for a in w:
                nxt = self.goto[q].get(a)
                if nxt is None:
                    nxt = len(self.goto)
                    self.goto[q][a] = nxt
                    self.goto.append({})
                    self.depth.append(self.depth[q] + 1)
                    self.word.append(-1)
                    self.out.append([])
                q = nxt
            if self.word[q] < 0:
                self.word[q] = index
            self.out[q].append(index)
        self.fail = [0] * len(self.goto)
        queue: deque[int] = deque(self.goto[0].values())
        while queue:
            v = queue.popleft()
            for a, u in self.goto[v].items():
                f = self.fail[v]
                while f and a not in self.goto[f]:
                    f = self.fail[f]
                g = self.goto[f].get(a, 0)
                self.fail[u] = g if g != u else 0
                self.out[u] = self.out[u] + self.out[self.fail[u]]
                queue.append(u)

    def step(self, q: int, a: Hashable) -> int:
        while q and a not in self.goto[q]:
            q = self.fail[q]
        return self.goto[q].get(a, 0)


def _shape(grid: Grid, name: str) -> tuple[int, int]:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if any(len(row) != cols for row in grid):
        raise ValueError(f"{name} is not rectangular")
    return rows, cols


def _one_width(text: Grid, n2: int, patterns: list[tuple[int, Grid]], w: int,
               out: list[tuple[int, int, int]], labels: list[list[int]] | None) -> None:
    # @line L2
    row_ids: dict[tuple[Hashable, ...], int] = {}
    for _, p in patterns:
        for row in p:
            row_ids.setdefault(tuple(row), len(row_ids))
    rows_ac = _Automaton(list(row_ids))
    # @line L3
    columns = [[row_ids[tuple(row)] for row in p] for _, p in patterns]
    # @line L4
    cols_ac = _Automaton(columns)
    heights = [len(p) for _, p in patterns]
    # @line L5
    state = [0] * n2
    # @line L6
    for r, text_row in enumerate(text):
        # @line L7
        label = [-1] * n2
        q = 0
        for c, a in enumerate(text_row):
            q = rows_ac.step(q, a)
            if rows_ac.depth[q] == w:
                label[c] = rows_ac.word[q]
        if labels is not None:
            labels.append(label)
        # @line L8
        for c in range(w - 1, n2):
            # @line L9
            state[c] = cols_ac.step(state[c], label[c])
            # @line L10
            for i in cols_ac.out[state[c]]:
                out.append((r - heights[i] + 1, c - w + 1, patterns[i][0]))


def bird_baker(text: Grid, patterns: Sequence[Grid],
               labels: list[list[int]] | None = None) -> list[tuple[int, int, int]]:
    """Return all (r, c, j) with pattern j occurring at row r, column c of the text."""
    n1, n2 = _shape(text, "text")
    out: list[tuple[int, int, int]] = []
    by_width: dict[int, list[tuple[int, Grid]]] = {}
    # @line L1
    for j, p in enumerate(patterns):
        m1, m2 = _shape(p, f"pattern {j}")
        if m1 == 0 or m2 == 0:
            for r in range(n1 - m1 + 1):
                for c in range(n2 + 1):
                    out.append((r, c, j))
        else:
            by_width.setdefault(m2, []).append((j, p))
    for w in sorted(by_width):
        _one_width(text, n2, by_width[w], w, out, labels)
    out.sort()
    return out
