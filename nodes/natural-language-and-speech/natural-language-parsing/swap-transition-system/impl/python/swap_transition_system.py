# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/swap-transition-system/. The authors are listed in prov/CCPJNB.jsonl.

"""The swap transition system of Nivre (2009) for non-projective dependency parsing.

The words are 1..n and 0 is the artificial root. A configuration is
(stack, buffer, arcs); the stack starts as [0] with its top s0 last and s1
under it, and the buffer starts as [1, ..., n]. The transitions are
("SH", None), ("LA", label), ("RA", label) and ("SW", None):

    SHIFT        (sigma, b|beta, A)        => (sigma|b, beta, A)
    LEFT-ARC_l   (sigma|s1|s0, beta, A)    => (sigma|s0, beta, A + {(s0, l, s1)})    needs s1 != 0
    RIGHT-ARC_l  (sigma|s1|s0, beta, A)    => (sigma|s1, beta, A + {(s1, l, s0)})
    SWAP         (sigma|s1|s0, beta, A)    => (sigma|s0, s1|beta, A)                 needs 0 < s1 < s0

The terminal configuration is ([0], [], A). Without SWAP this is arc-standard.
A complete sequence with k swaps has 2n + 2k transitions, and k <= n(n - 1) / 2.

The oracle is the one of Nivre (2009), figure 4: LEFT-ARC or RIGHT-ARC when the
gold arc joins s0 and s1 and the dependent has all its own dependents, SWAP
when s0 comes before s1 in the projective order of the gold tree, else SHIFT.
"""

from typing import Callable, List, Optional, Sequence, Tuple

Transition = Tuple[str, Optional[str]]
SHIFT: Transition = ("SH", None)
SWAP: Transition = ("SW", None)


class Config:
    def __init__(self, n: int):
        self.n = n
        self.stack: List[int] = [0]
        self.buffer: List[int] = list(range(1, n + 1))
        self.heads = [-1] * (n + 1)
        self.labels: List[Optional[str]] = [None] * (n + 1)

    def is_terminal(self) -> bool:
        return not self.buffer and len(self.stack) == 1

    def copy(self) -> "Config":
        c = Config(self.n)
        c.stack = list(self.stack)
        c.buffer = list(self.buffer)
        c.heads = list(self.heads)
        c.labels = list(self.labels)
        return c


def is_legal(c: Config, t: Transition) -> bool:
    kind = t[0]
    if kind == "SH":
        return bool(c.buffer)
    if len(c.stack) < 2:
        return False
    s1, s0 = c.stack[-2], c.stack[-1]
    if kind == "LA":
        return s1 != 0
    if kind == "RA":
        return True
    if kind == "SW":
        return 0 < s1 < s0
    raise ValueError(f"unknown transition {t}")


def apply(c: Config, t: Transition) -> None:
    kind, label = t
    if kind == "SH":
        c.stack.append(c.buffer.pop(0))  # @line L5
    elif kind == "LA":
        s0 = c.stack.pop()  # @line L6
        s1 = c.stack.pop()
        c.heads[s1], c.labels[s1] = s0, label
        c.stack.append(s0)
    elif kind == "RA":
        s0 = c.stack.pop()  # @line L7
        c.heads[s0], c.labels[s0] = c.stack[-1], label
    else:
        s0 = c.stack.pop()  # @line L8
        s1 = c.stack.pop()
        c.stack.append(s0)
        c.buffer.insert(0, s1)


def legal_transitions(c: Config, label_set: Sequence[str]) -> List[Transition]:
    out = [t for t in (SHIFT, SWAP) if is_legal(c, t)]
    for kind in ("LA", "RA"):
        for lab in label_set:
            if is_legal(c, (kind, lab)):
                out.append((kind, lab))
    return out


Scorer = Callable[[Config, Transition], float]


def parse(n: int, score: Scorer, label_set: Sequence[str] = ("dep",)):
    """Greedy parsing. Returns (heads, labels, transitions)."""
    c = Config(n)  # @line L1
    seq: List[Transition] = []
    while not c.is_terminal():  # @line L2
        best = None
        for t in legal_transitions(c, label_set):  # @line L3
            s = score(c, t)  # @line L4
            if best is None or s > best[0]:
                best = (s, t)
        apply(c, best[1])
        seq.append(best[1])
    return c.heads, c.labels, seq  # @line L9


def projective_order(heads: Sequence[int]) -> List[int]:
    """Return pos with pos[w] the rank of word w in the inorder traversal of the tree.

    Each node comes after the subtrees of its left dependents and before the
    subtrees of its right dependents, all in word order. Ordering the words by
    pos makes the tree projective.
    """
    n = len(heads) - 1
    kids: List[List[int]] = [[] for _ in range(n + 1)]
    for d in range(1, n + 1):
        kids[heads[d]].append(d)
    order: List[int] = []
    todo: List[Tuple[int, bool]] = [(0, False)]
    while todo:
        v, emit = todo.pop()
        if emit:
            order.append(v)
            continue
        left = [d for d in kids[v] if d < v]
        right = [d for d in kids[v] if d > v]
        for d in reversed(right):
            todo.append((d, False))
        todo.append((v, True))
        for d in reversed(left):
            todo.append((d, False))
    pos = [0] * (n + 1)
    for r, v in enumerate(order):
        pos[v] = r
    return pos


def oracle(c: Config, gold_heads: Sequence[int], gold_labels: Sequence[Optional[str]], pos: Sequence[int]) -> Optional[Transition]:
    if len(c.stack) >= 2:
        s1, s0 = c.stack[-2], c.stack[-1]

        def complete(w):
            return all(c.heads[d] == w for d in range(1, c.n + 1) if gold_heads[d] == w)

        if s1 != 0 and gold_heads[s1] == s0 and complete(s1):
            return ("LA", gold_labels[s1])
        if gold_heads[s0] == s1 and complete(s0):
            return ("RA", gold_labels[s0])
        if pos[s0] < pos[s1]:
            return SWAP
    return SHIFT if c.buffer else None


def oracle_sequence(gold_heads: Sequence[int], gold_labels: Optional[Sequence[Optional[str]]] = None) -> List[Transition]:
    """Return the oracle sequence that builds the gold tree, projective or not."""
    n = len(gold_heads) - 1
    if gold_labels is None:
        gold_labels = [None] + ["dep"] * n
    pos = projective_order(gold_heads)
    c = Config(n)
    seq: List[Transition] = []
    while not c.is_terminal():
        t = oracle(c, gold_heads, gold_labels, pos)
        if t is None or not is_legal(c, t):
            raise ValueError("the oracle is stuck")
        apply(c, t)
        seq.append(t)
    if c.heads != list(gold_heads):
        raise ValueError("the oracle built another tree")
    return seq
