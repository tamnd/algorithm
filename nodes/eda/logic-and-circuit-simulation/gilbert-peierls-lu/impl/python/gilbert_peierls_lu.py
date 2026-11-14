# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gilbert-peierls-lu/. The authors are listed in prov/6ASGQ9.jsonl.
"""Gilbert-Peierls sparse LU factorization with partial pivoting.

The matrix is factored column by column. Column k of L and U comes from one
sparse triangular solve L x = A(:, k) with the columns of L found so far. The
nonzero pattern of x is found first, by a depth-first search in the graph of
L from the nonzero rows of A(:, k); the numerical solve then visits only
those rows, in a topological order given by the reverse postorder of the
search. The pivot of column k is the largest |x_i| over the rows i that are
not yet pivot rows.

Rows keep their original numbers inside the factorization. L(:, k) is a dict
{row of A: multiplier} without the unit diagonal; U(:, k) is a dict
{pivot step j: u_jk}, with u_kk the pivot. pivrow[k] is the row of A chosen
as pivot k, so (P A)[k] = A[pivrow[k]] and P A = L U.

An entry that cancels to zero is kept as a stored zero, so the patterns are
structural. The counters flops (multiply and subtract operations of the
triangular solves), divs, dfs_nodes and dfs_edges measure the work.
"""

from dataclasses import dataclass, field


class SingularMatrixError(ValueError):
    """Column k has no usable pivot."""


@dataclass
class Factor:
    n: int
    lcols: list = field(default_factory=list)
    ucols: list = field(default_factory=list)
    pivrow: list = field(default_factory=list)
    flops: int = 0
    divs: int = 0
    dfs_nodes: int = 0
    dfs_edges: int = 0
    reach_per_column: list = field(default_factory=list)


def columns_of(a):
    """Columns of a dense list-of-rows matrix as dicts {row: value} of the nonzeros."""
    n = len(a)
    return [{i: a[i][j] for i in range(n) if a[i][j] != 0} for j in range(n)]


def reach(f, pivstep, start):
    """Rows reachable from start in the graph of L, in topological order.

    The graph has an edge i -> r when row i is the pivot row of step j and
    L(r, j) is nonzero. Returns the reverse postorder of an iterative DFS.
    """
    mark, post = set(), []
    for s in start:  # @line R1
        if s in mark:
            continue
        mark.add(s)
        f.dfs_nodes += 1
        stack = [(s, iter(f.lcols[pivstep[s]]) if s in pivstep else iter(()))]
        while stack:
            i, it = stack[-1]
            for r in it:  # @line R2
                f.dfs_edges += 1
                if r not in mark:
                    mark.add(r)
                    f.dfs_nodes += 1
                    stack.append((r, iter(f.lcols[pivstep[r]]) if r in pivstep else iter(())))
                    break
            else:
                stack.pop()
                post.append(i)  # @line R3
    post.reverse()
    return post  # @line R4


def gp_lu(a, tol=0):
    """Factor the square matrix a (a list of rows, or a list of column dicts).

    tol is the magnitude at or below which a pivot counts as zero.
    """
    cols = a if a and isinstance(a[0], dict) else columns_of(a)
    n = len(cols)
    f = Factor(n)
    pivstep = {}  # row of A -> the step at which it became a pivot row
    for k in range(n):  # @line L1
        order = reach(f, pivstep, cols[k].keys())  # @line L2
        f.reach_per_column.append(len(order))
        x = {i: 0 for i in order}  # @line L3
        for i, v in cols[k].items():
            x[i] = v
        for i in order:  # @line L4
            if i in pivstep:  # @line L5
                xi = x[i]
                for r, l in f.lcols[pivstep[i]].items():  # @line L6
                    x[r] -= l * xi
                    f.flops += 1
        cand = [i for i in order if i not in pivstep]
        p = max(cand, key=lambda i: (abs(x[i]), -i), default=None)  # @line L7
        if p is None or abs(x[p]) <= tol:
            raise SingularMatrixError(f"no usable pivot in column {k}")
        piv = x[p]
        u = {pivstep[i]: x[i] for i in order if i in pivstep}  # @line L8
        u[k] = piv
        low = {}
        for i in cand:
            if i != p:
                low[i] = x[i] / piv
                f.divs += 1
        f.ucols.append(u)
        f.lcols.append(low)
        f.pivrow.append(p)
        pivstep[p] = k  # @line L9
    return f  # @line L10


def lu_solve(f, b):
    """Solve A x = b with the factors of gp_lu (column-oriented solves)."""
    n = f.n
    y = list(b)  # y holds P b in original row numbering, updated in place
    z = [None] * n
    for k in range(n):  # L z = P b: z_k sits in the pivot row of step k
        zk = y[f.pivrow[k]]
        z[k] = zk
        for r, l in f.lcols[k].items():
            y[r] = y[r] - l * zk
    x = [None] * n
    for k in range(n - 1, -1, -1):  # U x = z, column-oriented
        xk = z[k] / f.ucols[k][k]
        x[k] = xk
        for j, v in f.ucols[k].items():
            if j != k:
                z[j] = z[j] - v * xk
    return x


def gp_solve(a, b, tol=0):
    return lu_solve(gp_lu(a, tol), b)
