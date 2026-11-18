# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blendshape-direct-manipulation/. The authors are listed in prov/RFBXKQ.jsonl.
"""Direct manipulation of blendshapes (Lewis and Anjyo 2010).

The rig is the delta form v = b_0 + D w, where D has one column per target
and three rows per vertex. The user pins or drags some vertices to goals p_i.
The rows of D at those vertices form the matrix S, and m = p - b_0 at them.
The weights minimize

    E(w) = |S w - m|^2 + alpha |w - w0|^2 + mu |w|^2,

where w0 are the current weights. The minimizer solves the linear system

    (S^T S + (alpha + mu) I) w = S^T m + alpha w0.

With the bound 0 <= w <= t the problem is a convex quadratic program with
box constraints. This file solves it by projected Gauss-Seidel (cyclic
coordinate descent with clamping), which converges to the unique minimizer
because the matrix is symmetric positive definite when alpha + mu > 0.
The paper uses a general QP solver; the minimizer is the same.
"""

from anim import solve

ALPHA = 0.1  # the value in the paper, a tuning choice
MU = 0.001  # the value in the paper, a tuning choice


def constraint_rows(deltas, b0, goals):
    """Return (S, m) for goals {vertex index: goal point}.

    deltas[k][i] is the offset of target k at vertex i (a 3-tuple).
    """
    s, m = [], []
    for i, p in goals.items():  # @line L1
        for c in range(len(p)):
            s.append([d[i][c] for d in deltas])
            m.append(p[c] - b0[i][c])
    return s, m


def normal_system(s, m, w0, alpha, mu):
    """Return (A, c) with A = S^T S + (alpha + mu) I and c = S^T m + alpha w0."""
    k = len(w0)
    a = [[sum(row[p] * row[q] for row in s) for q in range(k)] for p in range(k)]  # @line L2
    for p in range(k):
        a[p][p] += alpha + mu
    c = [sum(row[p] * mi for row, mi in zip(s, m)) + alpha * w0[p] for p in range(k)]  # @line L3
    return a, c


def energy(s, m, w, w0, alpha, mu):
    """Return E(w) of the module docstring."""
    r = sum((sum(a * b for a, b in zip(row, w)) - mi) ** 2 for row, mi in zip(s, m))
    return r + alpha * sum((a - b) ** 2 for a, b in zip(w, w0)) + mu * sum(a * a for a in w)


def box_qp(a, c, lo, hi, w_start, tol=1e-13, max_sweeps=100000):
    """Minimize w^T A w / 2 - c^T w subject to lo <= w <= hi by projected Gauss-Seidel."""
    w = [min(hi, max(lo, x)) for x in w_start]  # @line L5
    for _ in range(max_sweeps):  # @line L6
        big = 0.0
        for k in range(len(w)):  # @line L7
            r = c[k] - sum(a[k][l] * w[l] for l in range(len(w)) if l != k)
            new = min(hi, max(lo, r / a[k][k]))
            big = max(big, abs(new - w[k]))
            w[k] = new
        if big <= tol:  # @line L8
            return w
    raise RuntimeError("projected Gauss-Seidel did not converge")


def manipulate(deltas, b0, goals, w0, alpha=ALPHA, mu=MU, bound=None):
    """Return the new weights for the goals, the current weights w0 and the tuning alpha, mu.

    bound is None for free weights, or t for the box 0 <= w <= t.
    """
    if alpha + mu <= 0.0:
        raise ValueError("alpha + mu must be positive")
    s, m = constraint_rows(deltas, b0, goals)
    a, c = normal_system(s, m, w0, alpha, mu)
    if bound is None:
        return solve(a, c)  # @line L4
    return box_qp(a, c, 0.0, bound, w0)  # @line L9


def evaluate(deltas, b0, w):
    """Return the mesh b_0 + sum_k w_k d_k."""
    out = []
    for i, p in enumerate(b0):
        out.append(tuple(p[c] + sum(wk * d[i][c] for wk, d in zip(w, deltas)) for c in range(len(p))))
    return out
