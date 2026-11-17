# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-likelihood-admixture-estimation/. The authors are listed in prov/KYJWNZ.jsonl.
"""Maximum likelihood estimation of ancestry proportions Q and population
allele frequencies F, the model of STRUCTURE and ADMIXTURE.

g[i][j] in {0, 1, 2} is the count of allele 1 of individual i at site j.
q[i] is a point of the simplex in R^K, and f[k][j] is in [0, 1]. With
phi_ij = sum_k q_ik f_kj the log-likelihood is

    L(Q, F) = sum_ij g_ij ln(phi_ij) + (2 - g_ij) ln(1 - phi_ij).

The fit is block relaxation: improve Q with F fixed, then F with Q fixed.
ADMIXTURE (Alexander, Novembre and Lange 2009) solves each block by
sequential quadratic programming. Here each block takes one EM step, in
which the hidden data are the source population of each allele copy. The
EM step is simpler and also never lowers L. A quasi-Newton step of the
form of Zhou, Alexander and Lange (2011), with one secant pair, speeds up
the iteration; a step that lowers L is replaced by two plain rounds.
"""

from __future__ import annotations

import math
import random

Matrix = list[list[float]]

F_MIN = 1e-9
Q_MIN = 1e-6


def _phi(q: Matrix, f: Matrix) -> Matrix:
    """phi_ij = sum_k q_ik f_kj."""
    cols = list(zip(*f))
    return [[sum(a * b for a, b in zip(qi, col)) for col in cols] for qi in q]


def _weights(g: list[list[int]], q: Matrix, f: Matrix) -> tuple[Matrix, Matrix]:
    """wa_ij = g_ij / phi_ij and wb_ij = (2 - g_ij) / (1 - phi_ij), with 0 for a zero count."""
    phi = _phi(q, f)
    wa = [[x / p if x > 0 else 0.0 for x, p in zip(row, prow)] for row, prow in zip(g, phi)]
    wb = [[(2 - x) / (1.0 - p) if x < 2 else 0.0 for x, p in zip(row, prow)] for row, prow in zip(g, phi)]
    return wa, wb


def log_likelihood(g: list[list[int]], q: Matrix, f: Matrix) -> float:
    total = 0.0
    for row, prow in zip(g, _phi(q, f)):
        for x, p in zip(row, prow):
            if x > 0:
                total += x * math.log(p)
            if x < 2:
                total += (2 - x) * math.log(1.0 - p)
    return total


def update_q(g: list[list[int]], q: Matrix, f: Matrix) -> Matrix:
    """One EM step for Q with F fixed: q_ik <- q_ik sum_j (f_kj wa_ij + (1 - f_kj) wb_ij) / (2m).

    The term q_ik f_kj wa_ij is the expected number of the g_ij copies of
    allele 1 that come from population k, and q_ik (1 - f_kj) wb_ij is the
    same for allele 0."""
    m = len(g[0])
    wa, wb = _weights(g, q, f)
    out = []
    for qi, ra, rb in zip(q, wa, wb):
        out.append([qk * sum(fk[j] * ra[j] + (1.0 - fk[j]) * rb[j] for j in range(m)) / (2.0 * m)
                    for qk, fk in zip(qi, f)])
    return out


def update_f(g: list[list[int]], q: Matrix, f: Matrix) -> Matrix:
    """One EM step for F with Q fixed: f_kj <- A_kj / (A_kj + B_kj), where A_kj is the
    expected number of copies of allele 1 from population k at site j, and B_kj of allele 0."""
    n = len(g)
    m = len(g[0])
    wa, wb = _weights(g, q, f)
    out = []
    for c, fk in enumerate(f):
        sa = [sum(q[i][c] * wa[i][j] for i in range(n)) for j in range(m)]
        sb = [sum(q[i][c] * wb[i][j] for i in range(n)) for j in range(m)]
        row = []
        for j in range(m):
            a = fk[j] * sa[j]
            b = (1.0 - fk[j]) * sb[j]
            row.append(a / (a + b) if a + b > 0 else fk[j])
        out.append(row)
    return out


def block_round(g: list[list[int]], q: Matrix, f: Matrix) -> tuple[Matrix, Matrix]:
    """Block relaxation: first the Q block, then the F block with the new Q."""
    q2 = update_q(g, q, f)
    return q2, update_f(g, q2, f)


def project_simplex(v: list[float]) -> list[float]:
    """Euclidean projection onto {x : x >= 0, sum x = 1}."""
    u = sorted(v, reverse=True)
    run = 0.0
    tau = 0.0
    for idx, val in enumerate(u, start=1):
        run += val
        t = (run - 1.0) / idx
        if val - t > 0:
            tau = t
    return [max(x - tau, 0.0) for x in v]


def _flatten(q: Matrix, f: Matrix) -> list[float]:
    return [x for row in q for x in row] + [x for row in f for x in row]


def _unflatten(x: list[float], n: int, k: int, m: int) -> tuple[Matrix, Matrix]:
    q = [x[i * k:(i + 1) * k] for i in range(n)]
    base = n * k
    f = [x[base + c * m: base + (c + 1) * m] for c in range(k)]
    return q, f


def _feasible(q: Matrix, f: Matrix) -> tuple[Matrix, Matrix]:
    """Project Q rows onto the simplex with a small floor, and clip F to [F_MIN, 1 - F_MIN]."""
    q_out = []
    for row in q:
        p = [max(v, Q_MIN) for v in project_simplex(row)]
        s = sum(p)
        q_out.append([v / s for v in p])
    f_out = [[min(1.0 - F_MIN, max(F_MIN, v)) for v in row] for row in f]
    return q_out, f_out


def random_start(n: int, k: int, m: int, rng: random.Random) -> tuple[Matrix, Matrix]:
    q = []
    for _ in range(n):
        w = [rng.random() + 0.1 for _ in range(k)]
        s = sum(w)
        q.append([v / s for v in w])
    f = [[rng.uniform(0.05, 0.95) for _ in range(m)] for _ in range(k)]
    return q, f


def admixture(g: list[list[int]], k: int, rng: random.Random, max_iter: int = 2000, tol: float = 1e-9,
              accelerate: bool = True, start: tuple[Matrix, Matrix] | None = None):
    """Fit Q and F. Return (q, f, trace), where trace is the log-likelihood after each round."""
    n = len(g)
    if n == 0 or k < 1:
        raise ValueError("need at least one individual and k >= 1")
    m = len(g[0])
    for row in g:
        if len(row) != m or any(x not in (0, 1, 2) for x in row):
            raise ValueError("genotypes must be rows of equal length with values 0, 1 or 2")
    q, f = start if start is not None else random_start(n, k, m, rng)  # @line L1
    ll = log_likelihood(g, q, f)
    trace = [ll]
    for _ in range(max_iter):  # @line L2
        q1, f1 = block_round(g, q, f)  # @line L3
        if not accelerate:
            chosen = (q1, f1, log_likelihood(g, q1, f1))
        else:
            q2, f2 = block_round(g, q1, f1)  # @line L4
            x0, x1, x2 = _flatten(q, f), _flatten(q1, f1), _flatten(q2, f2)
            u = [b - a for a, b in zip(x0, x1)]  # @line L5
            v = [b - a for a, b in zip(x1, x2)]
            uu = sum(a * a for a in u)
            u_vu = sum(a * (b - a) for a, b in zip(u, v))
            chosen = (q2, f2, log_likelihood(g, q2, f2))
            if uu > 0 and u_vu < 0:
                c = -uu / u_vu  # @line L6
                y = [(1.0 - c) * a + c * b for a, b in zip(x1, x2)]
                qy, fy = _feasible(*_unflatten(y, n, k, m))  # @line L7
                lly = log_likelihood(g, qy, fy)
                if lly >= chosen[2]:  # @line L8
                    chosen = (qy, fy, lly)
        q, f, new_ll = chosen  # @line L9
        trace.append(new_ll)
        if new_ll - ll < tol * (1.0 + abs(ll)):  # @line L10
            break
        ll = new_ll
    return q, f, trace  # @line L11


def gradients(g: list[list[int]], q: Matrix, f: Matrix) -> tuple[Matrix, Matrix]:
    """Partial derivatives of L, with 1 - phi written as sum_k q_ik (1 - f_kj) for Q."""
    k = len(f)
    m = len(g[0])
    gq = [[0.0] * k for _ in g]
    gf = [[0.0] * m for _ in range(k)]
    for i, row in enumerate(g):
        qi = q[i]
        for j, x in enumerate(row):
            phi = sum(qi[c] * f[c][j] for c in range(k))
            s1 = x / phi if x > 0 else 0.0
            s0 = (2 - x) / (1.0 - phi) if x < 2 else 0.0
            for c in range(k):
                gq[i][c] += s1 * f[c][j] + s0 * (1.0 - f[c][j])
                gf[c][j] += qi[c] * (s1 - s0)
    return gq, gf
