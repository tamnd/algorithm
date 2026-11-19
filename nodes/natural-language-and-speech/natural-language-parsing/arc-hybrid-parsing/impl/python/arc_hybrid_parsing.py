# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arc-hybrid-parsing/. The authors are listed in prov/TTAZ45.jsonl.

"""The arc-hybrid transition system, its oracles and its cubic-time dynamic program.

The words are 1..n and 0 is the artificial root. A configuration is
(stack, buffer, arcs); the stack starts as [0], its top is s0 and the element
under it s1; the buffer front is b. The transitions are ("SH", None),
("LA", label) and ("RA", label):

    SHIFT         (sigma, b|beta, A)         => (sigma|b, beta, A)
    LEFT-ARC_l    (sigma|s0, b|beta, A)      => (sigma, b|beta, A + {(b, l, s0)})    needs s0 != 0
    RIGHT-ARC_l   (sigma|s1|s0, beta, A)     => (sigma|s1, beta, A + {(s1, l, s0)})

The terminal configuration is ([0], [], A). Every complete sequence has n shifts
and n arcs, so exactly 2n transitions. A word gets its head when it is popped,
so the words on the stack never have a head.

cost() is the dynamic oracle of Goldberg and Nivre (2013), section 4.5, with the
root at the bottom of the stack. viterbi_dp() and count_dp() are the deduction
system of Kuhlmann, Gomez-Rodriguez and Satta (2011), section 6, for scores
that add one score per arc.
"""

from typing import Callable, List, Optional, Sequence, Tuple

Transition = Tuple[str, Optional[str]]
SHIFT: Transition = ("SH", None)


class Config:
    def __init__(self, n: int):
        self.n = n
        self.stack: List[int] = [0]
        self.next = 1
        self.heads = [-1] * (n + 1)
        self.labels: List[Optional[str]] = [None] * (n + 1)

    def is_terminal(self) -> bool:
        return self.next > self.n and len(self.stack) == 1

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
    if kind == "SH":
        return c.next <= c.n
    if kind == "LA":
        return c.next <= c.n and c.stack[-1] != 0
    if kind == "RA":
        return len(c.stack) >= 2
    raise ValueError(f"unknown transition {t}")


def apply(c: Config, t: Transition) -> None:
    kind, label = t
    if kind == "SH":
        c.stack.append(c.next)  # @line L5
        c.next += 1
    elif kind == "LA":
        s0 = c.stack.pop()  # @line L6
        c.heads[s0], c.labels[s0] = c.next, label
    else:
        s0 = c.stack.pop()  # @line L7
        c.heads[s0], c.labels[s0] = c.stack[-1], label


def legal_transitions(c: Config, label_set: Sequence[str]) -> List[Transition]:
    out = [SHIFT] if is_legal(c, SHIFT) else []
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
    return c.heads, c.labels, seq  # @line L8


def _complete(c: Config, w: int, gold_heads: Sequence[int]) -> bool:
    return all(c.heads[d] == w for d in range(1, c.n + 1) if gold_heads[d] == w)


def static_oracle(c: Config, gold_heads: Sequence[int], gold_labels: Sequence[Optional[str]]) -> Optional[Transition]:
    """LEFT-ARC or RIGHT-ARC when s0 has all its dependents and its gold head is b or s1; else SHIFT."""
    s0 = c.stack[-1]
    if s0 != 0 and _complete(c, s0, gold_heads):
        if c.next <= c.n and gold_heads[s0] == c.next:
            return ("LA", gold_labels[s0])
        if len(c.stack) >= 2 and gold_heads[s0] == c.stack[-2]:
            return ("RA", gold_labels[s0])
    return SHIFT if c.next <= c.n else None


def oracle_sequence(gold_heads: Sequence[int], gold_labels: Optional[Sequence[Optional[str]]] = None) -> List[Transition]:
    """Run the static oracle; raise ValueError if it cannot build the gold tree (not projective)."""
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
    if c.heads != list(gold_heads):
        raise ValueError("the oracle built another tree")
    return seq


def cost(c: Config, t: Transition, gold_heads: Sequence[int]) -> int:
    """The number of gold arcs that t makes unreachable (unlabeled, projective gold tree)."""
    if not is_legal(c, t):
        raise ValueError("illegal transition")
    n, b = c.n, c.next
    s0 = c.stack[-1]
    s1 = c.stack[-2] if len(c.stack) >= 2 else None
    rest = set(range(b + 1, n + 1))  # beta, the buffer after b
    kind = t[0]
    if kind == "LA":
        heads_lost = ({s1} | rest) - {None}
        deps_lost = {b} | rest
    elif kind == "RA":
        heads_lost = {b} | rest if b <= n else set()
        deps_lost = heads_lost
    else:
        below = set(c.stack[:-2])
        heads_lost = below | ({s1} - {None})
        deps_lost = below | {s0} | ({s1} - {None})
        g = gold_heads[b]
        return int(g in heads_lost) + sum(1 for d in deps_lost if d != 0 and gold_heads[d] == b)
    return int(gold_heads[s0] in heads_lost) + sum(1 for d in deps_lost if gold_heads[d] == s0)


def dynamic_oracle(c: Config, gold_heads: Sequence[int]) -> List[Transition]:
    return [t for t in legal_transitions(c, ["dep"]) if cost(c, t, gold_heads) == 0]


def viterbi_dp(scores: Sequence[Sequence]) -> Tuple[object, List[int]]:
    """The deduction system of Kuhlmann et al. (2011) for the hybrid system, with arc scores.

    The item [i, j] (0 <= i < j <= n + 1) stands for a computation that pushes
    word i and moves the buffer front from i to j. Rules: [i, j] gives [j, j + 1]
    (shift); [i, k] and [k, j] give [i, j] with the arc j -> k when j <= n
    (left-arc) or with the arc i -> k (right-arc). The goal is [0, n + 1].
    Returns the best total score over all complete computations and its tree.
    """
    n = len(scores) - 1
    m = n + 1
    V = [[None] * (m + 1) for _ in range(m + 1)]
    back = [[None] * (m + 1) for _ in range(m + 1)]
    for i in range(m):
        V[i][i + 1] = 0
    for length in range(2, m + 1):
        for i in range(0, m - length + 1):
            j = i + length
            for k in range(i + 1, j):
                if V[i][k] is None or V[k][j] is None:
                    continue
                base = V[i][k] + V[k][j]
                if j <= n and (V[i][j] is None or base + scores[j][k] > V[i][j]):
                    V[i][j], back[i][j] = base + scores[j][k], (k, j)
                if V[i][j] is None or base + scores[i][k] > V[i][j]:
                    V[i][j], back[i][j] = base + scores[i][k], (k, i)
    heads = [-1] * (n + 1)
    todo = [(0, m)]
    while todo:
        i, j = todo.pop()
        if j == i + 1:
            continue
        k, h = back[i][j]
        heads[k] = h
        todo.append((i, k))
        todo.append((k, j))
    return V[0][m], heads


def count_dp(n: int) -> int:
    """The number of complete computations, by the same deduction system."""
    m = n + 1
    N = [[0] * (m + 1) for _ in range(m + 1)]
    for i in range(m):
        N[i][i + 1] = 1
    for length in range(2, m + 1):
        for i in range(0, m - length + 1):
            j = i + length
            ways = 2 if j <= n else 1
            N[i][j] = sum(N[i][k] * N[k][j] for k in range(i + 1, j)) * ways
    return N[0][m]
