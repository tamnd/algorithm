# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/normalized-cut/. The authors are listed in prov/HDGW2G.jsonl.

"""The normalized cut of Shi and Malik (2000).

W is a symmetric matrix of non-negative weights with a zero diagonal. The 2-way
algorithm takes the second smallest generalized eigenvector y of (D - W) y = lambda D y
and returns the best sweep cut along y. The recursive algorithm splits each part
again while the normalized cut of the split stays below a threshold. Exact helpers
(the cut values and a brute force minimum over all bipartitions) are for tests.
"""

import math
from typing import Iterable, Sequence

Matrix = list


def cut_value(W: Matrix, A: Iterable[int], B: Iterable[int]):
    B = list(B)
    return sum(W[i][j] for i in A for j in B)


def volume(W: Matrix, A: Iterable[int]):
    return sum(sum(W[i]) for i in A)


def ncut(W: Matrix, A: Sequence[int], B: Sequence[int]):
    """cut(A, B)/vol(A) + cut(A, B)/vol(B). Exact if W holds Fractions or ints."""
    c = cut_value(W, A, B)
    return c / volume(W, A) + c / volume(W, B)


def ratio_cut(W: Matrix, A: Sequence[int], B: Sequence[int]):
    """cut(A, B)/|A| + cut(A, B)/|B|."""
    c = cut_value(W, A, B)
    return c / len(A) + c / len(B)


def bipartitions(n: int):
    """All splits of range(n) into two non-empty parts, each split once (0 is in A)."""
    for mask in range(1 << (n - 1)):
        A = [0] + [i for i in range(1, n) if (mask >> (i - 1)) & 1]
        if len(A) < n:
            yield A, [i for i in range(n) if i not in A]


def brute_force_min(W: Matrix, objective=ncut):
    """The exact minimum of the objective over all bipartitions, and one minimizer."""
    return min(((objective(W, A, B), A, B) for A, B in bipartitions(len(W))),
               key=lambda t: t[0])


def jacobi_eigh(A: Matrix, tol: float = 1e-13, max_sweeps: int = 100):
    """Eigenvalues (ascending) and eigenvectors (columns of V) of a symmetric matrix."""
    n = len(A)
    a = [[float(x) for x in row] for row in A]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    scale = max(1.0, max((abs(x) for row in a for x in row), default=0.0))
    for _ in range(max_sweeps):
        if sum(a[p][q] ** 2 for p in range(n) for q in range(p + 1, n)) <= (tol * scale) ** 2:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for r in range(n):
                    arp, arq = a[r][p], a[r][q]
                    a[r][p], a[r][q] = c * arp - s * arq, s * arp + c * arq
                for r in range(n):
                    apr, aqr = a[p][r], a[q][r]
                    a[p][r], a[q][r] = c * apr - s * aqr, s * apr + c * aqr
                for r in range(n):
                    vrp, vrq = V[r][p], V[r][q]
                    V[r][p], V[r][q] = c * vrp - s * vrq, s * vrp + c * vrq
    order = sorted(range(n), key=lambda i: a[i][i])
    return [a[i][i] for i in order], [[V[r][i] for i in order] for r in range(n)]


def fiedler_generalized(W: Matrix):
    """lambda_2 and y with (D - W) y = lambda_2 D y, through L_sym. Needs each degree > 0."""
    n = len(W)
    d = [float(sum(row)) for row in W]  # @line L1
    if any(x <= 0 for x in d):
        raise ValueError("each vertex needs a positive degree")
    M = [[(1.0 if i == j else 0.0) - W[i][j] / math.sqrt(d[i] * d[j]) for j in range(n)]
         for i in range(n)]  # @line L2
    vals, V = jacobi_eigh(M)  # @line L3
    y = [V[i][1] / math.sqrt(d[i]) for i in range(n)]  # @line L4
    return vals[1], y


def sweep_cut(W: Matrix, y: Sequence[float]):
    """The best Ncut among the n - 1 threshold cuts along y. O(n^2) time."""
    n = len(W)
    order = sorted(range(n), key=lambda i: y[i])  # @line L5
    deg = [float(sum(row)) for row in W]
    total = sum(deg)
    inA = [False] * n
    cut, volA = 0.0, 0.0
    best = (math.inf, None)
    for s in range(n - 1):  # @line L6
        v = order[s]
        cut += sum(W[v][u] for u in range(n) if not inA[u] and u != v)
        cut -= sum(W[v][u] for u in range(n) if inA[u])
        inA[v] = True
        volA += deg[v]
        value = cut / volA + cut / (total - volA)
        if value < best[0]:
            best = (value, s)
    A = sorted(order[:best[1] + 1])  # @line L7
    return A, sorted(order[best[1] + 1:])


def normalized_cut_bipartition(W: Matrix):
    """Shi and Malik 2-way cut: the best sweep cut of the second generalized eigenvector."""
    _, y = fiedler_generalized(W)
    return sweep_cut(W, y)


def components(W: Matrix, nodes: Sequence[int]):
    nodes = list(nodes)
    seen, comps = set(), []
    for s in nodes:
        if s in seen:
            continue
        seen.add(s)
        stack, comp = [s], []
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in nodes:
                if v not in seen and W[u][v] > 0:
                    seen.add(v)
                    stack.append(v)
        comps.append(sorted(comp))
    return comps


def recursive_ncut(W: Matrix, threshold: float, nodes=None):
    """Split recursively while the Ncut of the best split is at most the threshold.

    A part that is not connected is first split into its components (Ncut 0).
    Uses an explicit stack instead of recursion. Returns a list of sorted parts.
    """
    nodes = list(range(len(W))) if nodes is None else list(nodes)
    out, stack = [], [nodes]
    while stack:
        part = stack.pop()
        if len(part) < 2:  # @line L8
            out.append(sorted(part))
            continue
        comps = components(W, part)
        if len(comps) > 1:
            stack.extend(comps)
            continue
        sub = [[W[i][j] for j in part] for i in part]
        A, B = normalized_cut_bipartition(sub)  # @line L9
        if ncut(sub, A, B) > threshold:  # @line L10
            out.append(sorted(part))
            continue
        stack.append([part[i] for i in A])  # @line L11
        stack.append([part[i] for i in B])
    return sorted(out)
