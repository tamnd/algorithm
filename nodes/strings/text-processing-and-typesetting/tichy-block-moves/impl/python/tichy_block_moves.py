# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tichy-block-moves/. The authors are listed in prov/ZJTFAN.jsonl.
"""Tichy's greedy covering of a target string by block moves from a source (TOCS 2(4), 1984).

A block move ("copy", p, l) appends s[p:p + l] to the output. An add ("add", x)
appends the symbol x, which is needed when x does not occur in s. The greedy
method takes, at each position of t, the longest prefix of the rest of t that
occurs in s. The function block_moves does this with direct comparisons in
O(|s| |t|) time; block_moves_linear finds the same lengths with a suffix
automaton of s in linear expected time.
"""

from collections.abc import Sequence
from typing import Any

Move = tuple  # ("copy", p, l) or ("add", x)


def block_moves(s: Sequence[Any], t: Sequence[Any]) -> list[Move]:
    """Return a shortest list of copies and adds that builds t from s, by the greedy rule."""
    moves: list[Move] = []
    q = 0  # @line L1
    while q < len(t):  # @line L2
        best_p, best_l = -1, 0
        for p in range(len(s)):  # @line L3
            l = 0
            while p + l < len(s) and q + l < len(t) and s[p + l] == t[q + l]:
                l += 1
            if l > best_l:  # @line L4
                best_p, best_l = p, l
        if best_l == 0:  # @line L5
            moves.append(("add", t[q]))
            q += 1
        else:
            moves.append(("copy", best_p, best_l))  # @line L6
            q += best_l
    return moves  # @line L7


class _SuffixAutomaton:
    """The suffix automaton of s, with the end of the first occurrence for each state."""

    def __init__(self, s: Sequence[Any]) -> None:
        self.next: list[dict[Any, int]] = [{}]
        self.link = [-1]
        self.length = [0]
        self.first_end = [-1]
        last = 0
        for i, x in enumerate(s):
            cur = self._new(self.length[last] + 1, i)
            v = last
            while v != -1 and x not in self.next[v]:
                self.next[v][x] = cur
                v = self.link[v]
            if v == -1:
                self.link[cur] = 0
            else:
                w = self.next[v][x]
                if self.length[v] + 1 == self.length[w]:
                    self.link[cur] = w
                else:
                    clone = self._new(self.length[v] + 1, self.first_end[w])
                    self.next[clone] = dict(self.next[w])
                    self.link[clone] = self.link[w]
                    while v != -1 and self.next[v].get(x) == w:
                        self.next[v][x] = clone
                        v = self.link[v]
                    self.link[w] = self.link[cur] = clone
            last = cur

    def _new(self, length: int, first_end: int) -> int:
        self.next.append({})
        self.link.append(-1)
        self.length.append(length)
        self.first_end.append(first_end)
        return len(self.length) - 1


def block_moves_linear(s: Sequence[Any], t: Sequence[Any]) -> list[Move]:
    """Return the greedy moves, with each longest prefix found by walking the suffix automaton of s."""
    sam = _SuffixAutomaton(s)
    moves: list[Move] = []
    q = 0
    while q < len(t):
        v, l = 0, 0
        while q + l < len(t) and t[q + l] in sam.next[v]:
            v = sam.next[v][t[q + l]]
            l += 1
        if l == 0:
            moves.append(("add", t[q]))
            q += 1
        else:
            moves.append(("copy", sam.first_end[v] - l + 1, l))
            q += l
    return moves


def apply_moves(s: Sequence[Any], moves: Sequence[Move]) -> list[Any]:
    """Return the sequence that the moves build from s."""
    out: list[Any] = []
    for move in moves:
        if move[0] == "copy":
            _, p, l = move
            if not (0 <= p and l >= 1 and p + l <= len(s)):
                raise ValueError(f"bad copy {move}")
            out.extend(s[p:p + l])
        elif move[0] == "add":
            out.append(move[1])
        else:
            raise ValueError(f"bad move {move}")
    return out
