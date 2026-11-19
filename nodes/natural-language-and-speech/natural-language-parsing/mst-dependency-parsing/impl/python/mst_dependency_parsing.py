# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mst-dependency-parsing/. The authors are listed in prov/Z4H7TB.jsonl.

"""Graph-based dependency parsing with the Chu-Liu-Edmonds algorithm.

The words are 1..n and 0 is the artificial root. scores[h][d] is the score of
the arc h -> d in an (n + 1) x (n + 1) matrix; column 0 and the diagonal are
not read. A tree is a head list heads with heads[0] = -1 and heads[d] the head
of word d. The score of a tree is the sum of its arc scores.

mst_parse() returns a maximum spanning arborescence rooted at 0, so the tree
can be non-projective. This plain recursive version takes O(n^3) time; Tarjan's
implementation takes O(n^2) on a dense graph. With single_root=True the root
gets exactly one child: the code solves one problem per possible root child.

partition_function() and arc_marginals() use the matrix-tree theorem with exact
Fractions, for weights w[h][d] > 0 (for example exp of the scores, or small
integers in the tests).
"""

from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

Arc = Tuple[int, int]


def _check(m: Sequence[Sequence]) -> int:
    n = len(m) - 1
    if n < 0 or any(len(row) != n + 1 for row in m):
        raise ValueError("the matrix must be (n + 1) x (n + 1)")
    return n


def _find_cycle(head: Dict[int, int]):
    """Return the list of nodes of a cycle in the graph v -> head[v], or None."""
    color: Dict[int, int] = {}
    for start in head:
        if start in color:
            continue
        path = []
        v = start
        while v in head and v not in color:
            color[v] = 1
            path.append(v)
            v = head[v]
        if v in color and color[v] == 1:
            return path[path.index(v):]
        for u in path:
            color[u] = 2
    return None


def chu_liu_edmonds(nodes: List[int], root: int, w: Dict[Arc, object]) -> Dict[int, int]:
    """Return a maximum spanning arborescence of the graph (nodes, w) rooted at root.

    w maps an arc (h, d) to its score; every node other than root must have at
    least one entering arc. The result maps each non-root node to its head.
    """
    best: Dict[int, int] = {}
    for d in nodes:  # @line L1
        if d == root:
            continue
        cands = [(h, d) for h in nodes if (h, d) in w]
        if not cands:
            raise ValueError(f"node {d} has no entering arc")
        best[d] = max(cands, key=lambda a: w[a])[0]
    cycle = _find_cycle(best)  # @line L2
    if cycle is None:
        return best  # @line L3
    in_cycle = set(cycle)
    c = max(nodes) + 1  # the new node that stands for the cycle  # @line L4
    cycle_score = sum(w[(best[v], v)] for v in cycle)
    w2: Dict[Arc, object] = {}
    enter: Dict[int, int] = {}  # for an arc (u, c): the cycle node it enters
    leave: Dict[int, int] = {}  # for an arc (c, v): the cycle node it leaves
    for (h, d), s in w.items():  # @line L5
        if h in in_cycle and d in in_cycle:
            continue
        if d in in_cycle:
            s2 = s - w[(best[d], d)] + cycle_score
            if (h, c) not in w2 or s2 > w2[(h, c)]:
                w2[(h, c)], enter[h] = s2, d
        elif h in in_cycle:
            if (c, d) not in w2 or s > w2[(c, d)]:
                w2[(c, d)], leave[d] = s, h
        else:
            w2[(h, d)] = s
    nodes2 = [v for v in nodes if v not in in_cycle] + [c]
    sub = chu_liu_edmonds(nodes2, root, w2)  # @line L6
    heads: Dict[int, int] = {}
    for d, h in sub.items():  # @line L7
        if d == c:
            heads[enter[h]] = h
        elif h == c:
            heads[d] = leave[d]
        else:
            heads[d] = h
    for v in cycle:  # @line L8
        if v not in heads:
            heads[v] = best[v]
    return heads  # @line L9


def mst_parse(scores: Sequence[Sequence], single_root: bool = False) -> Tuple[object, List[int]]:
    """Return (score, heads) of a highest scoring dependency tree, projective or not."""
    n = _check(scores)
    if n == 0:
        return 0, [-1]
    nodes = list(range(n + 1))
    full = {(h, d): scores[h][d] for h in nodes for d in range(1, n + 1) if h != d}
    if not single_root:
        options = [full]
    else:
        options = []
        for m in range(1, n + 1):
            options.append({a: s for a, s in full.items() if a[0] != 0 or a[1] == m})
    best_score, best_heads = None, None
    for w in options:
        sol = chu_liu_edmonds(nodes, 0, w)
        heads = [-1] + [sol[d] for d in range(1, n + 1)]
        s = tree_score(scores, heads)
        if best_score is None or s > best_score:
            best_score, best_heads = s, heads
    return best_score, best_heads


def tree_score(scores: Sequence[Sequence], heads: Sequence[int]):
    total = 0
    for d in range(1, len(heads)):
        total = total + scores[heads[d]][d]
    return total


def is_tree(heads: Sequence[int]) -> bool:
    """Return True if every word reaches the root 0 by following heads, with no cycle."""
    n = len(heads) - 1
    if n < 0 or heads[0] != -1:
        return False
    for d in range(1, n + 1):
        if not 0 <= heads[d] <= n or heads[d] == d:
            return False
    for d in range(1, n + 1):
        x, steps = d, 0
        while x != 0:
            x, steps = heads[x], steps + 1
            if steps > n:
                return False
    return True


# The matrix-tree theorem (Koo, Globerson, Carreras and Collins 2007).


def _det_and_inverse(a: List[List[Fraction]]):
    """Return (det a, inverse of a) by Gauss-Jordan elimination over Fractions."""
    n = len(a)
    m = [list(row) + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(a)]
    det = Fraction(1)
    for col in range(n):
        piv = next((r for r in range(col, n) if m[r][col] != 0), None)
        if piv is None:
            return Fraction(0), None
        if piv != col:
            m[col], m[piv] = m[piv], m[col]
            det = -det
        p = m[col][col]
        det *= p
        m[col] = [x / p for x in m[col]]
        for r in range(n):
            if r != col and m[r][col] != 0:
                f = m[r][col]
                m[r] = [x - f * y for x, y in zip(m[r], m[col])]
    return det, [row[n:] for row in m]


def _laplacian(w: Sequence[Sequence], single_root: bool):
    """The n x n matrix of Koo et al.: rows and columns are the words 1..n.

    Without single_root, L[d][d] = sum of w[h][d] over all heads h (root included)
    and L[h][d] = -w[h][d]. With single_root, the root weights leave the
    diagonal and the first row becomes w[0][d].
    """
    n = len(w) - 1
    L = [[Fraction(0)] * n for _ in range(n)]
    for d in range(1, n + 1):
        for h in range(0, n + 1):
            if h == d:
                continue
            if h > 0:
                L[h - 1][d - 1] -= Fraction(w[h][d])
            if h > 0 or not single_root:
                L[d - 1][d - 1] += Fraction(w[h][d])
    if single_root:
        L[0] = [Fraction(w[0][d]) for d in range(1, n + 1)]
    return L


def partition_function(w: Sequence[Sequence], single_root: bool = False) -> Fraction:
    """Return Z = sum over all trees of the product of w[h][d] over their arcs."""
    n = _check(w)
    if n == 0:
        return Fraction(1)
    det, _ = _det_and_inverse(_laplacian(w, single_root))
    return det


def arc_marginals(w: Sequence[Sequence], single_root: bool = False) -> List[List[Fraction]]:
    """Return mu[h][d], the total weight of the trees that contain h -> d, divided by Z.

    mu[h][d] = w[h][d] times the derivative of log Z with respect to w[h][d], and
    d log det L / d L[a][b] = (L^-1)[b][a].
    """
    n = _check(w)
    L = _laplacian(w, single_root)
    det, inv = _det_and_inverse(L)
    if det == 0:
        raise ValueError("the total weight of the trees is 0")
    mu = [[Fraction(0)] * (n + 1) for _ in range(n + 1)]
    for d in range(1, n + 1):
        for h in range(0, n + 1):
            if h == d:
                continue
            # (row, column, coefficient) of each entry of L that contains w[h][d]
            entries = []
            if single_root:
                if h == 0:
                    entries.append((0, d - 1, 1))
                else:
                    if d - 1 != 0:
                        entries.append((d - 1, d - 1, 1))
                    if h - 1 != 0:
                        entries.append((h - 1, d - 1, -1))
            else:
                entries.append((d - 1, d - 1, 1))
                if h > 0:
                    entries.append((h - 1, d - 1, -1))
            g = sum(c * inv[b][a] for a, b, c in entries)
            mu[h][d] = Fraction(w[h][d]) * g
    return mu
