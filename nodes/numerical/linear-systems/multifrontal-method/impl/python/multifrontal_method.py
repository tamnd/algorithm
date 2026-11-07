# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multifrontal-method/. The authors are listed in prov/QT9W33.jsonl.

"""Multifrontal Cholesky (and exact LDL^T) factorization of a sparse symmetric
positive definite matrix, along the elimination tree, with frontal matrices,
update matrices on a stack, and extend-add.

The matrix is given as a dense list of lists (zeros are structural zeros) that is
already in the desired elimination order. Entries may be floats (mode
"cholesky", A = L L^T) or Fractions (mode "ldlt", A = L D L^T with unit L, exact).
Everything is iterative; there is no recursion.
"""

import math


def elimination_tree(a) -> list[int]:
    """Liu's algorithm with path compression; parent[j] = -1 for roots."""
    n = len(a)
    parent = [-1] * n
    anc = [-1] * n
    for i in range(n):
        for k in range(i):
            if a[i][k] != 0:
                while k != -1 and k != i:  # climb from k to the root of its current subtree
                    nxt = anc[k]
                    anc[k] = i
                    if nxt == -1:
                        parent[k] = i
                    k = nxt
    return parent


def column_structures(a, parent) -> list[list[int]]:
    """struct[j] = sorted rows i > j with l_ij != 0: the pattern of column j of A
    below the diagonal, merged with the structures of the children minus j."""
    n = len(a)
    s = [set(i for i in range(j + 1, n) if a[i][j] != 0) for j in range(n)]
    for j in range(n):  # children have smaller indices, so they are complete
        p = parent[j]
        if p != -1:
            s[p] |= s[j] - {p}
    return [sorted(x) for x in s]


def children_lists(parent) -> list[list[int]]:
    ch = [[] for _ in parent]
    for j, p in enumerate(parent):
        if p != -1:
            ch[p].append(j)
    return ch


def postorder(parent, child_order=None) -> list[int]:
    """Iterative postorder; child_order[j] lists the children of j in visiting order."""
    ch = child_order if child_order is not None else children_lists(parent)
    out = []
    for r in [j for j, p in enumerate(parent) if p == -1]:
        stack = [(r, 0)]
        while stack:
            v, t = stack.pop()
            if t < len(ch[v]):
                stack.append((v, t + 1))
                stack.append((ch[v][t], 0))
            else:
                out.append(v)
    return out


def tri(k: int) -> int:
    return k * (k + 1) // 2


def stack_peaks(parent, struct, child_order):
    """Liu's recurrence for the working storage (lower triangles) of the
    multifrontal stack: peak[j] over the subtree of j, front included."""
    n = len(parent)
    peak = [0] * n
    for j in postorder(parent, child_order):
        acc, best = 0, 0
        for c in child_order[j]:
            best = max(best, acc + peak[c])
            acc += tri(len(struct[c]))
        peak[j] = max(best, acc + tri(len(struct[j]) + 1))
    return peak


def liu_child_order(parent, struct):
    """Children sorted by decreasing peak - update size (Liu, 1986), bottom up."""
    ch = children_lists(parent)
    n = len(parent)
    peak = [0] * n
    for j in postorder(parent, ch):
        ch[j].sort(key=lambda c: -(peak[c] - tri(len(struct[c]))))
        acc, best = 0, 0
        for c in ch[j]:
            best = max(best, acc + peak[c])
            acc += tri(len(struct[c]))
        peak[j] = max(best, acc + tri(len(struct[j]) + 1))
    return ch


def multifrontal(a, mode: str = "cholesky", child_order: str = "liu", stats=None):
    """Return L (mode "cholesky") or (L, D) (mode "ldlt"), both dense lists.

    If stats is a dict it receives: flops (multiplications, divisions and
    subtractions of the partial factorizations), assembly (additions in
    extend-add), peak (largest number of words on the stack plus the current
    front, lower triangles), fronts (front orders by column).
    """
    n = len(a)
    parent = elimination_tree(a)  # @line L1
    struct = column_structures(a, parent)
    ch = liu_child_order(parent, struct) if child_order == "liu" else children_lists(parent)
    zero = a[0][0] * 0 if n else 0
    lmat = [[zero] * n for _ in range(n)]
    dvec = [zero] * n
    stack = []  # @line L2
    flops = assembly = peak = used = 0
    fronts = [0] * n
    for j in postorder(parent, ch):  # @line L3
        idx = [j] + struct[j]
        pos = {g: t for t, g in enumerate(idx)}
        f = len(idx)
        fronts[j] = f
        front = [[zero] * (t + 1) for t in range(f)]  # @line L4
        peak = max(peak, used + tri(f))
        for t, g in enumerate(idx):  # @line L5
            front[t][0] = a[g][j]
        for _ in ch[j]:  # @line L6
            uidx, u = stack.pop()  # @line L7
            used -= tri(len(uidx))
            loc = [pos[g] for g in uidx]
            for r, lr in enumerate(loc):
                row = u[r]
                fr = front[lr]
                for c in range(r + 1):
                    fr[loc[c]] += row[c]
                    assembly += 1
        piv = front[0][0]  # @line L8
        if mode == "cholesky":
            if not piv > 0:
                raise ValueError("matrix is not positive definite")
            d = math.sqrt(piv)
            col = [front[t][0] / d for t in range(1, f)]
            lmat[j][j] = d
            mult = col
            flops += 1 + (f - 1)
        else:
            if piv == 0:
                raise ZeroDivisionError("zero pivot")
            dvec[j] = piv
            lmat[j][j] = piv / piv
            col = [front[t][0] / piv for t in range(1, f)]
            mult = [front[t][0] for t in range(1, f)]
            flops += f - 1
        for t in range(1, f):
            lmat[idx[t]][j] = col[t - 1]
        upd = []  # @line L9
        for r in range(1, f):
            fr = front[r]
            lr = col[r - 1]
            upd.append([fr[c] - lr * mult[c - 1] for c in range(1, r + 1)])
            flops += 2 * r
        if upd:  # @line L10
            stack.append((struct[j], upd))
            used += tri(len(struct[j]))
    if stats is not None:
        stats.update(flops=flops, assembly=assembly, peak=peak, fronts=fronts,
                     parent=parent, struct=struct)
    if mode == "cholesky":
        return lmat  # @line L11
    return lmat, dvec


def dense_ldlt_exact(a):
    """Reference right-looking LDL^T in the arithmetic of the entries (use Fractions)."""
    n = len(a)
    b = [row[:] for row in a]
    lmat = [[b[0][0] * 0] * n for _ in range(n)]
    d = [0] * n
    for k in range(n):
        d[k] = b[k][k]
        lmat[k][k] = d[k] / d[k]
        for i in range(k + 1, n):
            lmat[i][k] = b[i][k] / d[k]
        for i in range(k + 1, n):
            for j in range(k + 1, i + 1):
                b[i][j] -= lmat[i][k] * b[j][k]
                b[j][i] = b[i][j]
    return lmat, d
