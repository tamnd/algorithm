# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gusfield-perfect-phylogeny/. The authors are listed in prov/TF5DB1.jsonl.

"""Gusfield's O(nm) perfect phylogeny algorithm for binary characters.

The input is an n x m matrix M of 0/1 values: row i is taxon i, column c is
character c. The rooted problem assumes that the ancestor is the all-zero row.
The unrooted problem has no known ancestor; it reduces to the rooted problem by
flipping each column in which row 0 holds a 1.
"""

from typing import Dict, List, Optional, Sequence, Tuple

Matrix = Sequence[Sequence[int]]


class PerfectPhylogeny:
    """A rooted tree with nodes 0..k. Node 0 is the root.

    parent[j] is the parent of node j (j >= 1). labels[j] lists the original
    columns that change from 0 to 1 on the edge parent[j] -> j. leaf_of_row[i]
    is the node under which row i hangs as a leaf. flipped lists the columns that
    were complemented (empty for the rooted problem).
    """

    def __init__(self, parent: List[int], labels: List[List[int]], leaf_of_row: List[int], flipped: List[int]):
        self.parent = parent
        self.labels = labels
        self.leaf_of_row = leaf_of_row
        self.flipped = flipped

    def path_characters(self, i: int) -> List[int]:
        """Columns on the path from the root to the leaf of row i (in the possibly flipped matrix)."""
        out: List[int] = []
        j = self.leaf_of_row[i]
        while j != 0:
            out.extend(self.labels[j])
            j = self.parent[j]
        return sorted(out)


def radix_sort_columns(M: Matrix, m: int) -> List[int]:
    """Column indices sorted by decreasing value of the column read as a binary number.

    Row 0 is the most significant digit. LSD radix sort with base 2: one stable
    pass per row, from the last row to the first. Cost: O(nm) time, O(m) extra space.
    """
    order = list(range(m))
    for r in range(len(M) - 1, -1, -1):
        row = M[r]
        ones = [c for c in order if row[c] == 1]
        zeros = [c for c in order if row[c] != 1]
        order = ones + zeros  # 1 before 0 gives decreasing order; both lists keep the old order
    return order


def gusfield_rooted(M: Matrix) -> Optional[PerfectPhylogeny]:
    """Rooted perfect phylogeny with the all-zero ancestor, or None if none exists.

    Precondition: every entry is 0 or 1 and all rows have the same length.
    Cost: O(nm) time and O(n + m) extra space besides the output.
    """
    n = len(M)
    m = len(M[0]) if n else 0
    order = radix_sort_columns(M, m)  # @line L1
    classes: List[List[int]] = []  # @line L2
    prev: Optional[int] = None
    for c in order:
        if all(M[i][c] == 0 for i in range(n)):
            continue
        if prev is not None and all(M[i][c] == M[i][prev] for i in range(n)):
            classes[-1].append(c)
        else:
            classes.append([c])
        prev = c
    k = len(classes)  # @line L3
    rep = [cl[0] for cl in classes]
    parent: List[Optional[int]] = [None] * (k + 1)
    leaf_of_row = [0] * n
    for i in range(n):  # @line L4
        last = 0  # @line L5
        row = M[i]
        for j in range(1, k + 1):  # @line L6
            if row[rep[j - 1]] == 1:  # @line L7
                if parent[j] is None:
                    parent[j] = last  # @line L8
                elif parent[j] != last:
                    return None  # @line L9
                last = j  # @line L10
        leaf_of_row[i] = last  # @line L11
    labels: List[List[int]] = [[]] + [sorted(cl) for cl in classes]
    par = [0] + [p if p is not None else 0 for p in parent[1:]]
    return PerfectPhylogeny(par, labels, leaf_of_row, [])  # @line L12


def gusfield_unrooted(M: Matrix) -> Optional[PerfectPhylogeny]:
    """Unrooted perfect phylogeny: flip the columns where row 0 holds 1, then solve the rooted problem.

    The returned tree has row 0 at the root (leaf_of_row[0] == 0). Read it as an
    unrooted tree: column c changes state exactly on the edge labeled c.
    """
    n = len(M)
    if n == 0:
        return PerfectPhylogeny([0], [[]], [], [])
    m = len(M[0])
    flipped = [c for c in range(m) if M[0][c] == 1]
    fs = set(flipped)
    N = [[(1 - M[i][c]) if c in fs else M[i][c] for c in range(m)] for i in range(n)]
    t = gusfield_rooted(N)
    if t is None:
        return None
    t.flipped = flipped
    return t


def has_four_gametes(M: Matrix, a: int, b: int) -> bool:
    """True if columns a and b show all four pairs 00, 01, 10, 11."""
    return len({(row[a], row[b]) for row in M}) == 4


def four_gamete_test(M: Matrix) -> bool:
    """Pairwise test: True if no pair of columns shows four gametes. O(n m^2) time."""
    m = len(M[0]) if M else 0
    return not any(has_four_gametes(M, a, b) for a in range(m) for b in range(a + 1, m))


def newick(t: PerfectPhylogeny, names: Optional[Sequence[str]] = None) -> str:
    """A Newick-like string of the tree: rows as leaves, internal nodes as their character labels."""
    k = len(t.parent) - 1
    kids: Dict[int, List[int]] = {j: [] for j in range(k + 1)}
    for j in range(1, k + 1):
        kids[t.parent[j]].append(j)
    rows: Dict[int, List[int]] = {j: [] for j in range(k + 1)}
    for i, j in enumerate(t.leaf_of_row):
        rows[j].append(i)
    out: Dict[int, str] = {}
    stack: List[Tuple[int, bool]] = [(0, False)]
    while stack:
        j, done = stack.pop()
        if not done:
            stack.append((j, True))
            for c in kids[j]:
                stack.append((c, False))
            continue
        parts = [names[i] if names else str(i) for i in rows[j]] + [out[c] for c in kids[j]]
        lab = "" if j == 0 else "c" + "+".join(str(c) for c in t.labels[j])
        out[j] = "(" + ",".join(parts) + ")" + lab
    return out[0]
