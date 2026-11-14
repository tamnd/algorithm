# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/klu-solver/. The authors are listed in prov/SR6DG7.jsonl.
"""A small KLU-style sparse solver: BTF, a fill-reducing order per block,
Gilbert-Peierls LU per block, block back substitution and refactorization.

The matrix is a list of rows; a zero is a structural zero.

analyze(a) does the symbolic work:
  1. a maximum transversal (augmenting paths, as in MC21) gives a column
     permutation with a zero-free diagonal;
  2. Tarjan's strongly connected components of the graph of the permuted
     matrix give a symmetric permutation to block upper triangular form;
  3. each diagonal block gets a minimum degree order of the pattern of
     B + B^T. This is the exact minimum degree rule on the elimination graph,
     not the approximate minimum degree (AMD) of the real KLU.
factor(a, sym) does the numerical work: Gilbert-Peierls LU with threshold
partial pivoting on each diagonal block, preferring the diagonal entry.
refactor(a, num) reuses the pivots and patterns for new values.
solve(num, b) does block back substitution.

The returned permutations satisfy: row k of the permuted matrix is row
sym.prow[k] of A and column k is column sym.pcol[k] of A.
"""

from dataclasses import dataclass, field


class SingularMatrixError(ValueError):
    """The matrix is structurally or numerically singular."""


# ---------------------------------------------------------------- symbolic


def max_transversal(rows, n):
    """match[j] = the row matched to column j, by augmenting paths from each column.

    rows[i] is the set of columns of row i. Raises SingularMatrixError when
    the structural rank is less than n.
    """
    cols = [[] for _ in range(n)]
    for i in range(n):
        for j in sorted(rows[i]):
            cols[j].append(i)
    rmatch = [-1] * n  # rmatch[i] = column matched to row i
    cmatch = [-1] * n
    def look_ahead(j):  # free rows first, as in the cheap assignment of MC21
        return iter(sorted(cols[j], key=lambda i: (rmatch[i] >= 0, i)))

    for j0 in range(n):
        # iterative DFS for an augmenting path from column j0
        seen = set()
        parent = {}
        stack = [(j0, look_ahead(j0))]
        found = -1
        while stack and found < 0:
            j, it = stack[-1]
            for i in it:
                if i in seen:
                    continue
                seen.add(i)
                parent[i] = j
                if rmatch[i] < 0:
                    found = i
                    break
                stack.append((rmatch[i], look_ahead(rmatch[i])))
                break
            else:
                stack.pop()
        if found < 0:
            raise SingularMatrixError(f"structurally singular: column {j0} cannot be matched")
        i = found
        while True:  # flip the path
            j = parent[i]
            prev = cmatch[j]
            cmatch[j], rmatch[i] = i, j
            if j == j0:
                break
            i = prev
    return cmatch


def tarjan_scc(adj, n):
    """Strongly connected components in the order Tarjan's algorithm emits them."""
    index, low, on, stack, comps = [-1] * n, [0] * n, [False] * n, [], []
    counter = 0
    for s in range(n):
        if index[s] >= 0:
            continue
        work = [(s, iter(adj[s]))]
        index[s] = low[s] = counter
        counter += 1
        stack.append(s)
        on[s] = True
        while work:
            v, it = work[-1]
            advanced = False
            for w in it:
                if index[w] < 0:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on[w] = True
                    work.append((w, iter(adj[w])))
                    advanced = True
                    break
                if on[w]:
                    low[v] = min(low[v], index[w])
            if advanced:
                continue
            work.pop()
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop()
                    on[w] = False
                    comp.append(w)
                    if w == v:
                        break
                comps.append(sorted(comp))
    return comps


def minimum_degree(adj):
    """Exact minimum degree order of an undirected graph (dict node -> set)."""
    g = {v: set(nb) - {v} for v, nb in adj.items()}
    order = []
    while g:
        v = min(g, key=lambda x: (len(g[x]), x))
        nb = g.pop(v)
        for a in nb:
            g[a].discard(v)
            g[a] |= nb - {a}
        order.append(v)
    return order


@dataclass
class Symbolic:
    n: int
    prow: list
    pcol: list
    blocks: list  # list of (start, end) in the permuted numbering


def analyze(a):
    n = len(a)
    rows = [{j for j in range(n) if a[i][j] != 0} for i in range(n)]
    match = max_transversal(rows, n)  # @line L1
    # In A(:, match^-1) the entry (i, i) is nonzero: column j moves to place match[j].
    colof = [0] * n
    for j in range(n):
        colof[match[j]] = j  # column of A placed at position i has its match in row i
    adj = [sorted({match[j] for j in rows[i]} - {i}) for i in range(n)]
    comps = tarjan_scc(adj, n)  # @line L2
    comps.reverse()  # upper block triangular: an edge i -> j goes to the same or a later block
    prow, pcol, blocks = [], [], []
    for comp in comps:  # @line L3
        start = len(prow)
        sub = {v: {w for w in adj[v] if w in comp} for v in comp}
        for v in comp:
            for w in list(sub[v]):
                sub[w].add(v)
        for v in minimum_degree(sub):
            prow.append(v)
            pcol.append(colof[v])
        blocks.append((start, len(prow)))
    return Symbolic(n, prow, pcol, blocks)


# ---------------------------------------------------------------- numerical


@dataclass
class Numeric:
    sym: Symbolic
    lu: list = field(default_factory=list)  # per block: (pivrow, lcols, ucols)
    offdiag: list = field(default_factory=list)  # per block: list of (local row, global col, value)
    a: list = None


def _gp_block(cols, m, u, tol, pivrow_fixed=None):
    """Gilbert-Peierls LU of one block given as column dicts {local row: value}.

    With pivrow_fixed, reuse that row order (refactorization).
    """
    lcols, ucols, pivrow, pivstep = [], [], [], {}
    for k in range(m):
        mark, post = set(), []
        for s in cols[k]:
            if s in mark:
                continue
            mark.add(s)
            stack = [(s, iter(lcols[pivstep[s]]) if s in pivstep else iter(()))]
            while stack:
                i, it = stack[-1]
                for r in it:
                    if r not in mark:
                        mark.add(r)
                        stack.append((r, iter(lcols[pivstep[r]]) if r in pivstep else iter(())))
                        break
                else:
                    stack.pop()
                    post.append(i)
        post.reverse()
        x = {i: 0 for i in post}
        for i, v in cols[k].items():
            x[i] = v
        for i in post:
            if i in pivstep:
                xi = x[i]
                for r, l in lcols[pivstep[i]].items():
                    x[r] -= l * xi
        cand = [i for i in post if i not in pivstep]
        if pivrow_fixed is not None:
            p = pivrow_fixed[k]
            if p not in x or abs(x[p]) <= tol:
                raise SingularMatrixError("refactorization met a zero pivot")
        else:
            if not cand:
                raise SingularMatrixError("numerically singular block")
            big = max(abs(x[i]) for i in cand)
            if big <= tol:
                raise SingularMatrixError("numerically singular block")
            if k in x and k not in pivstep and abs(x[k]) >= u * big:
                p = k  # the diagonal entry of the ordered block passes the threshold
            else:
                p = max(cand, key=lambda i: (abs(x[i]), -i))
        piv = x[p]
        uc = {pivstep[i]: x[i] for i in post if i in pivstep}
        uc[k] = piv
        lc = {i: x[i] / piv for i in cand if i != p}
        lcols.append(lc)
        ucols.append(uc)
        pivrow.append(p)
        pivstep[p] = k
    return pivrow, lcols, ucols


def _split(a, sym):
    """Diagonal blocks as local column dicts, and the off-diagonal entries."""
    pos_c = {c: k for k, c in enumerate(sym.pcol)}
    blocks, off = [], []
    for s, e in sym.blocks:
        cols = [{} for _ in range(e - s)]
        rest = []
        for k in range(s, e):
            r = sym.prow[k]
            for c, v in enumerate(a[r]):
                if v == 0:
                    continue
                kc = pos_c[c]
                if s <= kc < e:
                    cols[kc - s][k - s] = v
                elif kc < s:
                    raise AssertionError("entry below the block diagonal")
                else:
                    rest.append((k - s, kc, v))
        blocks.append(cols)
        off.append(rest)
    return blocks, off


def factor(a, sym, u=0.001, tol=0):
    num = Numeric(sym, a=a)
    blocks, num.offdiag = _split(a, sym)
    for (s, e), cols in zip(sym.blocks, blocks):  # @line L4
        num.lu.append(_gp_block(cols, e - s, u, tol))  # @line L5
    return num


def refactor(a, num, tol=0):
    """New values on the same pattern: reuse the pivot rows and the order."""
    sym = num.sym
    new = Numeric(sym, a=a)
    blocks, new.offdiag = _split(a, sym)
    for (s, e), cols, old in zip(sym.blocks, blocks, num.lu):
        new.lu.append(_gp_block(cols, e - s, 0, tol, pivrow_fixed=old[0]))
    return new


def _block_solve(lu, rhs):
    pivrow, lcols, ucols = lu
    m = len(pivrow)
    y = list(rhs)
    z = [None] * m
    for k in range(m):
        zk = y[pivrow[k]]
        z[k] = zk
        for r, l in lcols[k].items():
            y[r] = y[r] - l * zk
    x = [None] * m
    for k in range(m - 1, -1, -1):
        xk = z[k] / ucols[k][k]
        x[k] = xk
        for j, v in ucols[k].items():
            if j != k:
                z[j] = z[j] - v * xk
    return x


def solve(num, b):
    sym = num.sym
    n = sym.n
    xp = [None] * n  # solution in the permuted column numbering
    for bi in range(len(sym.blocks) - 1, -1, -1):  # @line L6
        s, e = sym.blocks[bi]
        rhs = [b[sym.prow[k]] for k in range(s, e)]
        for lr, kc, v in num.offdiag[bi]:  # @line L7
            rhs[lr] = rhs[lr] - v * xp[kc]
        xb = _block_solve(num.lu[bi], rhs)  # @line L8
        for t, v in enumerate(xb):
            xp[s + t] = v
    x = [None] * n
    for k, c in enumerate(sym.pcol):
        x[c] = xp[k]
    return x  # @line L9


def klu_solve(a, b, u=0.001, tol=0):
    return solve(factor(a, analyze(a), u, tol), b)


def determinant(num):
    """det A as the product of the block determinants, with the permutation signs."""
    def sign(perm):
        seen, s = set(), 1
        for i in range(len(perm)):
            if i in seen:
                continue
            j, length = i, 0
            while j not in seen:
                seen.add(j)
                j = perm[j]
                length += 1
            if length % 2 == 0:
                s = -s
        return s

    d = sign(num.sym.prow) * sign(num.sym.pcol)
    for pivrow, _, ucols in num.lu:
        d *= sign(pivrow)
        for k, uc in enumerate(ucols):
            d *= uc[k]
    return d
