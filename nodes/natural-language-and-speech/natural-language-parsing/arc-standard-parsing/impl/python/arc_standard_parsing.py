# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arc-standard-parsing/. The authors are listed in prov/D0MMXM.jsonl.

"""The arc-standard transition system for dependency parsing.

The words are 1..n and 0 is the artificial root. A configuration is
(stack, buffer, arcs). The stack starts as [0] and its top is the last element;
the buffer is the list of words not yet shifted, front first. The transitions
are ("SH", None), ("LA", label) and ("RA", label):

    SHIFT         (sigma, b|beta, A)       => (sigma|b, beta, A)                 needs a non-empty buffer
    LEFT-ARC_l    (sigma|s1|s0, beta, A)   => (sigma|s0, beta, A + {(s0, l, s1)})  needs s1 != 0
    RIGHT-ARC_l   (sigma|s1|s0, beta, A)   => (sigma|s1, beta, A + {(s1, l, s0)})

The terminal configuration is ([0], [], A). Every complete sequence has exactly
2n transitions: n shifts and n arcs. With single_root=True, RIGHT-ARC from the
root needs an empty buffer, so the root gets exactly one child.

A tree is a pair (heads, labels) of lists of length n + 1 with heads[0] = -1.
"""

from typing import Callable, List, Optional, Sequence, Tuple

Transition = Tuple[str, Optional[str]]
SHIFT: Transition = ("SH", None)


class Config:
    """A parser configuration. heads[d] is -1 while word d has no head."""

    def __init__(self, n: int):
        self.n = n
        self.stack: List[int] = [0]
        self.next = 1  # the buffer is next, next + 1, ..., n
        self.heads = [-1] * (n + 1)
        self.labels: List[Optional[str]] = [None] * (n + 1)

    def buffer(self) -> List[int]:
        return list(range(self.next, self.n + 1))

    def is_terminal(self) -> bool:
        return self.next > self.n and len(self.stack) == 1

    def copy(self) -> "Config":
        c = Config(self.n)
        c.stack = list(self.stack)
        c.next = self.next
        c.heads = list(self.heads)
        c.labels = list(self.labels)
        return c


def is_legal(c: Config, t: Transition, single_root: bool = False) -> bool:
    kind = t[0]
    if kind == "SH":
        return c.next <= c.n
    if len(c.stack) < 2:
        return False
    s1 = c.stack[-2]
    if kind == "LA":
        return s1 != 0
    if kind == "RA":
        return not (single_root and s1 == 0 and c.next <= c.n)
    raise ValueError(f"unknown transition {t}")


def apply(c: Config, t: Transition) -> None:
    """Apply the legal transition t to c in place."""
    kind, label = t
    if kind == "SH":
        c.stack.append(c.next)  # @line L5
        c.next += 1
    elif kind == "LA":
        s0 = c.stack.pop()  # @line L6
        s1 = c.stack.pop()
        c.heads[s1], c.labels[s1] = s0, label
        c.stack.append(s0)
    else:
        s0 = c.stack.pop()  # @line L7
        s1 = c.stack[-1]
        c.heads[s0], c.labels[s0] = s1, label


def legal_transitions(c: Config, label_set: Sequence[str], single_root: bool = False) -> List[Transition]:
    out = [SHIFT] if is_legal(c, SHIFT) else []
    for kind in ("LA", "RA"):
        for lab in label_set:
            if is_legal(c, (kind, lab), single_root):
                out.append((kind, lab))
    return out


Scorer = Callable[[Config, Transition], float]


def parse(n: int, score: Scorer, label_set: Sequence[str] = ("dep",), single_root: bool = False):
    """Greedy parsing: in each configuration take the legal transition of highest score.

    Returns (heads, labels, transitions). Ties go to the first transition in the
    order SHIFT, then LEFT-ARC, then RIGHT-ARC, labels in the given order.
    """
    c = Config(n)  # @line L1
    seq: List[Transition] = []
    while not c.is_terminal():  # @line L2
        cands = legal_transitions(c, label_set, single_root)  # @line L3
        best = None
        for t in cands:  # @line L4
            s = score(c, t)
            if best is None or s > best[0]:
                best = (s, t)
        apply(c, best[1])
        seq.append(best[1])
    return c.heads, c.labels, seq  # @line L8


def static_oracle(c: Config, gold_heads: Sequence[int], gold_labels: Sequence[Optional[str]]) -> Optional[Transition]:
    """Return the transition of the static oracle, or None if no transition can lead to the gold tree.

    LEFT-ARC when s1 is a dependent of s0; RIGHT-ARC when s0 is a dependent of s1
    and has all its own dependents; SHIFT otherwise.
    """
    if len(c.stack) >= 2:
        s1, s0 = c.stack[-2], c.stack[-1]
        if s1 != 0 and gold_heads[s1] == s0:
            return ("LA", gold_labels[s1])
        if gold_heads[s0] == s1:
            done = all(c.heads[d] == s0 for d in range(1, c.n + 1) if gold_heads[d] == s0)
            if done:
                return ("RA", gold_labels[s0])
    if c.next <= c.n:
        return SHIFT
    return None


def oracle_sequence(gold_heads: Sequence[int], gold_labels: Optional[Sequence[Optional[str]]] = None) -> List[Transition]:
    """Return the static oracle sequence that builds the gold tree.

    Raise ValueError if the oracle gets stuck or builds another tree, which
    happens exactly when the gold tree is not projective.
    """
    n = len(gold_heads) - 1
    if gold_labels is None:
        gold_labels = [None] + ["dep"] * n
    c = Config(n)
    seq: List[Transition] = []
    while not c.is_terminal():
        t = static_oracle(c, gold_heads, gold_labels)
        if t is None:
            raise ValueError("the oracle is stuck: the tree is not projective")
        apply(c, t)
        seq.append(t)
    if c.heads[1:] != list(gold_heads[1:]):
        raise ValueError("the oracle built another tree")
    return seq


def run(n: int, seq: Sequence[Transition], single_root: bool = False) -> Config:
    """Apply a transition sequence from the initial configuration; raise ValueError on an illegal step."""
    c = Config(n)
    for t in seq:
        if not is_legal(c, t, single_root):
            raise ValueError(f"illegal transition {t}")
        apply(c, t)
    return c
