# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/a-star-parsing/. The authors are listed in prov/MZTBB1.jsonl.

"""A* parsing: exact Viterbi parsing of a PCFG with an agenda ordered by b + a.

A grammar is a list of rules (A, rhs, q): A -> B C with B and C nonterminals, or
A -> w with w a terminal, and q > 0 the rule probability. A rule with q = 0 is
ignored. The scores are natural logs. A chart item is (X, i, j) over the
fencepost span (i, j), which covers the words w[i], ..., w[j - 1] (0-based), so
the words i + 1 to j in 1-based numbering.

b(e) is the best inside log score found so far for item e. An estimate a(X, i, j)
must return an upper bound on the best outside log score of the item (it is
admissible) and must not decrease b + a along a derivation (it is consistent).
null_estimate (a = 0) and sx_estimate have both properties. With such an
estimate, the first goal item popped has the Viterbi score.

A parse tree is (A, children), where each child is a tree or a word, as on the
probabilistic CKY page.

Cost: O(n^3 g log(n g)) time in the worst case for n words and g rules, plus
the estimate; space O(n^2 m) for the chart of m nonterminals and O(n^3 g) for
the agenda with lazy deletion.
"""

import heapq
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from nlslog import NEG_INF, safe_log

Rule = Tuple[str, Tuple[str, ...], float]
Item = Tuple[str, int, int]
Estimate = Callable[[str, int, int], float]


def _index(rules: Sequence[Rule]):
    """Split the rules into lexical, by-left-child and by-right-child indexes."""
    nts = {a for a, _, _ in rules}
    lexical: Dict[str, List[Tuple[str, float]]] = {}
    by_left: Dict[str, Dict[str, List[Tuple[str, float]]]] = {}
    by_right: Dict[str, Dict[str, List[Tuple[str, float]]]] = {}
    binary: List[Tuple[str, str, str, float]] = []
    for a, rhs, q in rules:
        if q < 0:
            raise ValueError(f"negative probability for {a} -> {rhs}")
        if q == 0:
            continue
        lq = safe_log(q)
        if len(rhs) == 1 and rhs[0] not in nts:
            lexical.setdefault(rhs[0], []).append((a, lq))
        elif len(rhs) == 2 and rhs[0] in nts and rhs[1] in nts:
            b, c = rhs
            by_left.setdefault(b, {}).setdefault(c, []).append((a, lq))
            by_right.setdefault(c, {}).setdefault(b, []).append((a, lq))
            binary.append((a, b, c, lq))
        else:
            raise ValueError(f"not in Chomsky normal form: {a} -> {rhs}")
    return nts, lexical, by_left, by_right, binary


def null_estimate(x: str, i: int, j: int) -> float:
    """The trivial estimate a = 0: admissible and consistent, A* becomes uniform cost search."""
    return 0.0


def sx_estimate(rules: Sequence[Rule], start: str, n: int) -> Estimate:
    """Return the SX estimate for sentences of n words.

    in_any(X, k) is the best inside log score of X over any k words, and
    out_sx(X, l, r) the best outside log score of X with l words to its left
    and r to its right, the words inside the context being free. Both are
    computed bottom up in O(n^3 g) time. The estimate is admissible and
    consistent for every sentence of n words.
    """
    nts, lexical, _, _, binary = _index(rules)
    best_lex: Dict[str, float] = {}
    for _, entries in lexical.items():
        for a, lq in entries:
            if lq > best_lex.get(a, NEG_INF):
                best_lex[a] = lq
    in_any: Dict[Tuple[str, int], float] = {}
    for x in nts:
        in_any[(x, 1)] = best_lex.get(x, NEG_INF)
    for k in range(2, n + 1):
        for x in nts:
            in_any[(x, k)] = NEG_INF
        for a, b, c, lq in binary:
            for m in range(1, k):
                s = lq + in_any[(b, m)] + in_any[(c, k - m)]
                if s > in_any[(a, k)]:
                    in_any[(a, k)] = s
    out: Dict[Tuple[str, int, int], float] = {}
    for x in nts:
        out[(x, 0, 0)] = 0.0 if x == start else NEG_INF
    for t in range(1, n):  # t = l + r words outside the span
        for l in range(t + 1):
            r = t - l
            for x in nts:
                out[(x, l, r)] = NEG_INF
            for a, b, c, lq in binary:
                # parent a -> b c, the item is b, the sibling c on the right takes k words
                for k in range(1, r + 1):
                    s = out[(a, l, r - k)] + lq + in_any[(c, k)]
                    if s > out[(b, l, r)]:
                        out[(b, l, r)] = s
                # the item is c, the sibling b on the left takes k words
                for k in range(1, l + 1):
                    s = out[(a, l - k, r)] + lq + in_any[(b, k)]
                    if s > out[(c, l, r)]:
                        out[(c, l, r)] = s

    def estimate(x: str, i: int, j: int) -> float:
        return out.get((x, i, n - j), NEG_INF)

    return estimate


def a_star_parse(rules: Sequence[Rule], start: str, w: Sequence[str],
                 estimate: Optional[Estimate] = None):
    """Return (best log score, a best tree, number of items finished).

    The best log score is NEG_INF and the tree None when w has no parse. The
    estimate defaults to null_estimate. Ties in b + a are broken first in,
    first out, so the result is deterministic.
    """
    if estimate is None:
        estimate = null_estimate
    _, lexical, by_left, by_right, _ = _index(rules)
    n = len(w)
    if n == 0:
        return NEG_INF, None, 0
    b: Dict[Item, float] = {}
    back: Dict[Item, object] = {}
    finished = set()
    starts: List[List[Tuple[str, int]]] = [[] for _ in range(n + 1)]  # finished items by left end
    ends: List[List[Tuple[str, int]]] = [[] for _ in range(n + 1)]  # finished items by right end
    agenda: List[Tuple[float, int, str, int, int]] = []
    counter = 0

    def relax(e: Item, s: float, bp: object) -> None:
        nonlocal counter
        if e in finished or s <= b.get(e, NEG_INF):  # @line L10
            return
        a = estimate(*e)
        b[e] = s
        back[e] = bp
        if a == NEG_INF:
            return  # the item is in no complete parse
        heapq.heappush(agenda, (-(s + a), counter, e[0], e[1], e[2]))
        counter += 1

    for i in range(n):  # @line L1
        for x, lq in lexical.get(w[i], ()):
            relax((x, i, i + 1), lq, w[i])
    pops = 0
    while agenda:  # @line L2
        _, _, x, i, j = heapq.heappop(agenda)  # @line L3
        e = (x, i, j)
        if e in finished:  # @line L4
            continue
        finished.add(e)  # @line L5
        pops += 1
        starts[i].append((x, j))
        ends[j].append((x, i))
        be = b[e]
        if e == (start, 0, n):  # @line L6
            return be, _tree(back, e), pops
        right = by_left.get(x, {})
        for y, k in starts[j]:  # @line L7
            for z, lq in right.get(y, ()):
                relax((z, i, k), lq + be + b[(y, j, k)], (j, x, y))
        left = by_right.get(x, {})
        for y, h in ends[i]:  # @line L8
            for z, lq in left.get(y, ()):
                relax((z, h, j), lq + b[(y, h, i)] + be, (i, y, x))
    return NEG_INF, None, pops  # @line L9


def _tree(back: Dict[Item, object], goal: Item):
    """Build the tree of goal from the back pointers, with an explicit stack."""
    done: Dict[Item, object] = {}
    stack = [(goal, False)]
    while stack:
        e, expanded = stack.pop()
        bp = back[e]
        if isinstance(bp, str):
            done[e] = (e[0], (bp,))
            continue
        k, y, z = bp
        left, right = (y, e[1], k), (z, k, e[2])
        if expanded:
            done[e] = (e[0], (done[left], done[right]))
        else:
            stack.append((e, True))
            stack.append((right, False))
            stack.append((left, False))
    return done[goal]


def tree_log_score(rules: Sequence[Rule], t) -> float:
    """Return the log probability of a tree: the sum of the log rule probabilities."""
    q: Dict[Tuple[str, Tuple[str, ...]], float] = {}
    for a, rhs, p in rules:
        q[(a, tuple(rhs))] = q.get((a, tuple(rhs)), 0) + p
    total = 0.0
    stack = [t]
    while stack:
        a, kids = stack.pop()
        rhs = tuple(k if isinstance(k, str) else k[0] for k in kids)
        total += safe_log(q.get((a, rhs), 0))
        stack.extend(k for k in kids if not isinstance(k, str))
    return total
