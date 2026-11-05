# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-parallel-regex-matching/. The authors are listed in prov/045TZR.jsonl.

"""Bit-parallel simulation of the Glushkov automaton of a regular expression.

A regular expression is a tuple:
("empty",) for the empty language, ("eps",) for the empty string,
("sym", a) for one symbol, ("alt", r, s), ("cat", r, s) and ("star", r).
A set of Glushkov states 0..k is an integer whose bit p is state p.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

Regex = tuple[Any, ...]


def _positions(regex: Regex) -> tuple[list[str], list[int], int]:
    """Return sym, the Follow masks (Follow[0] = First) and the accepting mask.

    Glushkov's construction on bit masks, in postorder with an explicit stack.
    """
    sym = [""]
    follow = [0]
    done: list[tuple[bool, int, int]] = []
    todo: list[tuple[Regex, bool]] = [(regex, False)]
    while todo:
        node, ready = todo.pop()
        tag = node[0]
        if not ready and tag in ("alt", "cat", "star"):
            todo.append((node, True))
            for child in reversed(node[1:]):
                todo.append((child, False))
            continue
        if tag == "empty":
            done.append((False, 0, 0))
        elif tag == "eps":
            done.append((True, 0, 0))
        elif tag == "sym":
            sym.append(node[1])
            follow.append(0)
            bit = 1 << (len(sym) - 1)
            done.append((False, bit, bit))
        elif tag == "alt":
            n2, f2, l2 = done.pop()
            n1, f1, l1 = done.pop()
            done.append((n1 or n2, f1 | f2, l1 | l2))
        elif tag == "cat":
            n2, f2, l2 = done.pop()
            n1, f1, l1 = done.pop()
            _add_follow(follow, l1, f2)
            done.append((n1 and n2, f1 | f2 if n1 else f1, l1 | l2 if n2 else l2))
        elif tag == "star":
            n1, f1, l1 = done.pop()
            _add_follow(follow, l1, f1)
            done.append((True, f1, l1))
        else:
            raise ValueError(f"unknown node {node!r}")
    nullable, first, last = done.pop()
    follow[0] = first
    return sym, follow, last | (1 if nullable else 0)


def _add_follow(follow: list[int], last: int, first: int) -> None:
    while last:
        low = last & -last
        follow[low.bit_length() - 1] |= first
        last ^= low


@dataclass
class BitParallelMatcher:
    """Tables for the update D <- T[D] & B[c] on bit masks of Glushkov states."""

    b: int
    chunks: int
    tables: list[list[int]]
    masks: dict[str, int]
    final: int

    def step(self, d: int, c: str) -> int:
        """One text symbol: OR the chunk tables, then AND the symbol mask."""
        e = 0  # @line L8
        low = (1 << self.b) - 1
        for j in range(self.chunks):
            e |= self.tables[j][(d >> (j * self.b)) & low]
        return e & self.masks.get(c, 0)  # @line L9


def compile_matcher(regex: Regex, chunk_bits: int = 8) -> BitParallelMatcher:
    """Build the masks and the split tables of `regex`.

    Cost: O(m k^2) for the Glushkov sets, then O(2^b) table entries for
    each of the ceil((k + 1) / b) chunks, each entry a (k + 1)-bit integer.
    """
    if chunk_bits < 1:
        raise ValueError("chunk_bits must be at least 1")
    sym, follow, final = _positions(regex)  # @line L1
    masks: dict[str, int] = {}
    for q in range(1, len(sym)):  # @line L2
        masks[sym[q]] = masks.get(sym[q], 0) | (1 << q)
    states = len(sym)  # @line L3
    b = chunk_bits
    chunks = (states + b - 1) // b  # @line L4
    tables = []
    for j in range(chunks):  # @line L5
        width = min(b, states - j * b)
        table = [0] * (1 << b)
        for v in range(1, 1 << width):
            low = v & -v
            table[v] = table[v ^ low] | follow[j * b + low.bit_length() - 1]
        tables.append(table)
    return BitParallelMatcher(b, chunks, tables, masks, final)


def run(mt: BitParallelMatcher, word: str) -> bool:
    """Decide whether `word` is accepted, with tables built by compile_matcher.

    Cost: ceil((k + 1) / b) table lookups and ORs of (k + 1)-bit masks per symbol.
    """
    d = 1  # @line L6
    for c in word:  # @line L7
        d = mt.step(d, c)
        if d == 0:  # @line L10
            return False
    return d & mt.final != 0  # @line L11


def bit_parallel_match(regex: Regex, word: str, chunk_bits: int = 8) -> bool:
    """Decide whether `word` is in L(regex): compile_matcher, then run."""
    return run(compile_matcher(regex, chunk_bits), word)


def bit_parallel_search(regex: Regex, text: str, chunk_bits: int = 8) -> list[int]:
    """Return every end position e such that some text[s:e] is in L(regex).

    The initial state is added again before each symbol, so a match may start
    anywhere. Same cost per symbol as bit_parallel_match.
    """
    mt = compile_matcher(regex, chunk_bits)
    ends = []
    d = 1
    if d & mt.final:
        ends.append(0)
    for i, c in enumerate(text):
        d = mt.step(d, c) | 1
        if d & mt.final:
            ends.append(i + 1)
    return ends
