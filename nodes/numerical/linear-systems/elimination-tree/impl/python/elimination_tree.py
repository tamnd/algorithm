# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elimination-tree/. The authors are listed in prov/4Z4VSH.jsonl.
"""Elimination tree of a sparse symmetric matrix and the symbolic Cholesky
factorization built on it. Indices are 0-based; -1 means "no parent"."""


def lower_rows(n, entries):
    """rows[k] = sorted list of i < k with a_ki != 0, from a list of (i, j)
    positions of a symmetric pattern (either triangle, diagonal ignored)."""
    rows = [set() for _ in range(n)]
    for i, j in entries:
        if not (0 <= i < n and 0 <= j < n):
            raise ValueError("index out of range")
        if i != j:
            rows[max(i, j)].add(min(i, j))
    return [sorted(r) for r in rows]


def etree(n, rows, stats=None):
    """Liu's algorithm with path compression. Returns parent[0..n-1]."""
    parent = [-1] * n
    anc = [-1] * n
    steps = 0
    for k in range(n):                       # @line L1
        parent[k] = -1                       # @line L2
        anc[k] = -1
        for i in rows[k]:                    # @line L3
            while i != -1 and i < k:         # @line L4
                nxt = anc[i]                 # @line L5
                anc[i] = k
                steps += 1
                if nxt == -1:                # @line L6
                    parent[i] = k
                i = nxt                      # @line L7
    if stats is not None:
        stats["steps"] = steps
    return parent                            # @line L8


def ereach(rows, k, parent, mark):
    """Pattern of row k of L without the diagonal, using the tree.
    mark is a list of n booleans, all False on entry and on exit."""
    mark[k] = True                           # @line L9
    out = []
    for i in rows[k]:                        # @line L10
        path = []                            # @line L11
        while not mark[i]:                   # @line L12
            path.append(i)                   # @line L13
            mark[i] = True
            i = parent[i]
        out.extend(path)                     # @line L14
    for i in out:                            # @line L15
        mark[i] = False
    mark[k] = False
    return out


def postorder(parent):
    """A postorder of the forest: children before parents, each subtree
    contiguous, roots and children in increasing order."""
    n = len(parent)
    children = [[] for _ in range(n)]        # @line L16
    for j in range(n):
        if parent[j] != -1:
            children[parent[j]].append(j)
    order = []
    for r in range(n):                       # @line L17
        if parent[r] != -1:
            continue
        stack = [(r, 0)]
        while stack:
            v, c = stack.pop()
            if c < len(children[v]):
                stack.append((v, c + 1))
                stack.append((children[v][c], 0))
            else:
                order.append(v)
    return order                             # @line L18


def symbolic_cholesky(n, rows, parent=None):
    """Column patterns of L (strictly below the diagonal), sorted."""
    if parent is None:
        parent = etree(n, rows)
    cols = [[] for _ in range(n)]
    mark = [False] * n
    for k in range(n):
        for j in ereach(rows, k, parent, mark):
            cols[j].append(k)
    return cols


def column_counts(n, rows, parent=None):
    """Number of nonzeros in each column of L, diagonal included."""
    return [len(c) + 1 for c in symbolic_cholesky(n, rows, parent)]


def height(parent):
    """Number of edges on the longest leaf-to-root path."""
    n = len(parent)
    depth = [0] * n
    best = 0
    for j in range(n - 1, -1, -1):           # parent[j] > j, so go downwards
        if parent[j] != -1:
            depth[j] = depth[parent[j]] + 1
        best = max(best, depth[j])
    return best


def permute(n, rows, perm):
    """Rows of P A P^T where new index p corresponds to old index perm[p]."""
    inv = [0] * n
    for p, old in enumerate(perm):
        inv[old] = p
    return lower_rows(n, [(inv[k], inv[i]) for k in range(n) for i in rows[k]])
