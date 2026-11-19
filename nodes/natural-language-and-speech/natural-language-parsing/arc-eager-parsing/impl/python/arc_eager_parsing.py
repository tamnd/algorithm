# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arc-eager-parsing/. The authors are listed in prov/BSRJBW.jsonl.

"""The arc-eager transition system, its static oracle and its dynamic oracle.

The words are 1..n and 0 is the artificial root. A configuration is
(stack, buffer, arcs). The stack starts as [0] and its top s is the last
element; the buffer front is b. The transitions are ("SH", None),
("LA", label), ("RA", label) and ("RE", None):

    SHIFT         (sigma, b|beta, A)    => (sigma|b, beta, A)
    LEFT-ARC_l    (sigma|s, b|beta, A)  => (sigma, b|beta, A + {(b, l, s)})    needs s != 0 and s without a head
    RIGHT-ARC_l   (sigma|s, b|beta, A)  => (sigma|s|b, beta, A + {(s, l, b)})
    REDUCE        (sigma|s, beta, A)    => (sigma, beta, A)                     needs s with a head

A configuration with an empty buffer is terminal. The words that still have no
head then get the root 0 as head, with the label "root". A complete sequence
has n moves out of the buffer (SHIFT or RIGHT-ARC) and at most n pops (LEFT-ARC
or REDUCE), so at most 2n transitions.

The dynamic oracle follows Goldberg and Nivre (2012, 2013): the cost of a
transition is the number of gold arcs that it makes unreachable. The formulas
are adapted to this page's convention, the root at the bottom of the stack and
the final attachment to the root; the tests compare them with the cost found by
search over all transition sequences.
"""

from typing import Callable, List, Optional, Sequence, Tuple

Transition = Tuple[str, Optional[str]]
SHIFT: Transition = ("SH", None)
REDUCE: Transition = ("RE", None)


class Config:
    def __init__(self, n: int):
        self.n = n
        self.stack: List[int] = [0]
        self.next = 1  # the buffer is next, ..., n
        self.heads = [-1] * (n + 1)
        self.labels: List[Optional[str]] = [None] * (n + 1)

    def is_terminal(self) -> bool:
        return self.next > self.n

    def copy(self) -> "Config":
        c = Config(self.n)
        c.stack = list(self.stack)
        c.next = self.next
        c.heads = list(self.heads)
        c.labels = list(self.labels)
        return c

    def key(self):
        return (tuple(self.stack), self.next, tuple(self.heads))


def is_legal(c: Config, t: Transition) -> bool:
    kind = t[0]
    s = c.stack[-1]
    if kind == "RE":
        return s != 0 and c.heads[s] != -1
    if c.next > c.n:
        return False
    if kind == "SH" or kind == "RA":
        return True
    if kind == "LA":
        return s != 0 and c.heads[s] == -1
    raise ValueError(f"unknown transition {t}")


def apply(c: Config, t: Transition) -> None:
    kind, label = t
    if kind == "SH":
        c.stack.append(c.next)  # @line L5
        c.next += 1
    elif kind == "LA":
        s = c.stack.pop()  # @line L6
        c.heads[s], c.labels[s] = c.next, label
    elif kind == "RA":
        b = c.next  # @line L7
        c.heads[b], c.labels[b] = c.stack[-1], label
        c.stack.append(b)
        c.next += 1
    else:
        c.stack.pop()  # @line L8


def legal_transitions(c: Config, label_set: Sequence[str]) -> List[Transition]:
    out = [t for t in (SHIFT, REDUCE) if is_legal(c, t)]
    for kind in ("LA", "RA"):
        for lab in label_set:
            if is_legal(c, (kind, lab)):
                out.append((kind, lab))
    return out


def finish(c: Config) -> Tuple[List[int], List[Optional[str]]]:
    """Return the tree of a terminal configuration: headless words go to the root."""
    heads, labels = list(c.heads), list(c.labels)
    for d in range(1, c.n + 1):  # @line L9
        if heads[d] == -1:
            heads[d], labels[d] = 0, "root"
    return heads, labels


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
    heads, labels = finish(c)
    return heads, labels, seq  # @line L10


def static_oracle(c: Config, gold_heads: Sequence[int], gold_labels: Sequence[Optional[str]]) -> Transition:
    """A static oracle for a projective gold tree.

    LEFT-ARC if b is the gold head of s; RIGHT-ARC if s is the gold head of b;
    REDUCE if s has its head and no gold dependent of s is left in the buffer;
    SHIFT otherwise.
    """
    s, b = c.stack[-1], c.next
    if s != 0 and gold_heads[s] == b:
        return ("LA", gold_labels[s])
    if gold_heads[b] == s:
        return ("RA", gold_labels[b])
    if s != 0 and c.heads[s] != -1 and not any(gold_heads[k] == s for k in range(b, c.n + 1)):
        return REDUCE
    return SHIFT


def oracle_sequence(gold_heads: Sequence[int], gold_labels: Optional[Sequence[Optional[str]]] = None) -> List[Transition]:
    """Run the static oracle; raise ValueError if it builds another tree (a non-projective gold tree)."""
    n = len(gold_heads) - 1
    if gold_labels is None:
        gold_labels = [None] + ["dep"] * n
    c = Config(n)
    seq: List[Transition] = []
    while not c.is_terminal():
        t = static_oracle(c, gold_heads, gold_labels)
        if not is_legal(c, t):
            raise ValueError("the oracle is stuck: the tree is not projective")
        apply(c, t)
        seq.append(t)
    heads, _ = finish(c)
    if heads != list(gold_heads):
        raise ValueError("the oracle built another tree: the gold tree is not projective")
    return seq


def cost(c: Config, t: Transition, gold_heads: Sequence[int]) -> int:
    """The number of gold arcs that are reachable from c but not after t (unlabeled).

    The gold tree must be projective. Here sigma is the stack below s and beta
    is the buffer after b.
    """
    if not is_legal(c, t):
        raise ValueError("illegal transition")
    s, b, n = c.stack[-1], c.next, c.n
    below = set(c.stack[:-1])
    beta = range(b + 1, n + 1)
    kind = t[0]
    if kind == "LA":
        lost = 1 if (gold_heads[s] == 0 or gold_heads[s] > b) else 0
        return lost + sum(1 for k in range(b, n + 1) if gold_heads[k] == s)
    if kind == "RA":
        g = gold_heads[b]
        lost = 1 if (g in below or g > b) else 0
        return lost + sum(1 for k in below | {s} if k != 0 and c.heads[k] == -1 and gold_heads[k] == b)
    if kind == "RE":
        return sum(1 for k in range(b, n + 1) if gold_heads[k] == s)
    g = gold_heads[b]
    lost = 1 if (g != 0 and (g in below or g == s)) else 0
    return lost + sum(1 for k in below | {s} if k != 0 and c.heads[k] == -1 and gold_heads[k] == b)


def dynamic_oracle(c: Config, gold_heads: Sequence[int]) -> List[Transition]:
    """Return the legal unlabeled transitions of cost 0 (labels are ignored)."""
    return [t for t in legal_transitions(c, ["dep"]) if cost(c, t, gold_heads) == 0]
