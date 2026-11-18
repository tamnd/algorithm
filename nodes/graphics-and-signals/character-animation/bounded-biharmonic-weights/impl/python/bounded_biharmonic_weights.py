# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounded-biharmonic-weights/. The authors are listed in prov/W8RNMB.jsonl.
"""Bounded biharmonic weights (Jacobson, Baran, Popovic and Sorkine 2011), in 2D.

The domain is a triangle mesh with vertices v_i, and the handles are points
at mesh vertices. For each handle k, the weight w_k minimizes the discrete
Laplacian energy

    (1/2) w^T Q w,   Q = L M^(-1) L,

where L is the cotangent stiffness matrix and M the lumped mass matrix,
subject to w_k = 1 at handle k, w_k = 0 at the other handles, and
0 <= w_k <= 1 at every vertex. This is the faster variant of the paper: the
partition of unity is not a constraint, each handle is solved on its own,
and the weights are divided by their sum at the end.

Each problem is a convex quadratic program with box constraints. It is
solved by a primal active set method: keep a working set of variables held
at a bound, solve the equality problem on the others, step to the first
bound that blocks, and release the bound with the most negative multiplier
when no step is possible.
"""

import itertools
import math

from anim import solve, sub


def cotangent_laplacian(verts, tris):
    """Return the symmetric stiffness matrix L with L_ij = -(cot a + cot b) / 2 and zero row sums."""
    n = len(verts)
    lap = [[0.0] * n for _ in range(n)]
    for t in tris:
        for c in range(3):
            o, u, v = t[c], t[(c + 1) % 3], t[(c + 2) % 3]
            a, b = sub(verts[u], verts[o]), sub(verts[v], verts[o])
            cot = (a[0] * b[0] + a[1] * b[1]) / abs(a[0] * b[1] - a[1] * b[0])
            lap[u][v] -= 0.5 * cot
            lap[v][u] -= 0.5 * cot
            lap[u][u] += 0.5 * cot
            lap[v][v] += 0.5 * cot
    return lap


def lumped_mass(verts, tris):
    """Return the lumped (barycentric) mass of each vertex: a third of the area of its triangles."""
    m = [0.0] * len(verts)
    for t in tris:
        a, b = sub(verts[t[1]], verts[t[0]]), sub(verts[t[2]], verts[t[0]])
        area = 0.5 * abs(a[0] * b[1] - a[1] * b[0])
        for i in t:
            m[i] += area / 3.0
    return m


def bilaplacian(lap, m):
    """Return Q = L M^(-1) L."""
    n = len(lap)
    return [[sum(lap[i][k] * lap[k][j] / m[k] for k in range(n)) for j in range(n)] for i in range(n)]


def energy(q, w):
    """Return (1/2) w^T Q w."""
    return 0.5 * sum(w[i] * sum(q[i][j] * w[j] for j in range(len(w))) for i in range(len(w)))


def _solve_free(q, x, free):
    """Return the values on free that minimize (1/2) x^T Q x with the other entries of x fixed."""
    others = [j for j in range(len(x)) if j not in free]
    a = [[q[i][j] for j in free] for i in free]
    rhs = [-sum(q[i][j] * x[j] for j in others) for i in free]
    return solve(a, rhs)


def box_qp(q, fixed, lo=0.0, hi=1.0, tol=1e-12, max_iter=10000):
    """Minimize (1/2) x^T Q x subject to x_i = fixed[i] for i in fixed and lo <= x <= hi elsewhere.

    Q restricted to the variables that are not fixed must be positive
    definite. Return (x, iterations).
    """
    n = len(q)
    x = [fixed.get(i, lo) for i in range(n)]
    var = [i for i in range(n) if i not in fixed]
    work = {i: lo for i in var}  # every variable starts at its lower bound
    for it in range(max_iter):
        free = [i for i in var if i not in work]
        p = {}
        if free:
            new = _solve_free(q, x, free)
            p = {i: new[k] - x[i] for k, i in enumerate(free)}
        if all(abs(d) <= tol for d in p.values()):
            for i, d in p.items():
                x[i] += d
            g = [sum(q[i][j] * x[j] for j in range(n)) for i in range(n)]
            mult = {i: (g[i] if b == lo else -g[i]) for i, b in work.items()}
            if not mult or min(mult.values()) >= -tol:
                return x, it
            del work[min(mult, key=mult.get)]
            continue
        alpha, block = 1.0, None
        for i, d in p.items():
            if d < 0.0 and (lo - x[i]) / d < alpha:
                alpha, block = (lo - x[i]) / d, (i, lo)
            elif d > 0.0 and (hi - x[i]) / d < alpha:
                alpha, block = (hi - x[i]) / d, (i, hi)
        for i, d in p.items():
            x[i] += alpha * d
        if block is not None:
            x[block[0]] = block[1]
            work[block[0]] = block[1]
    raise RuntimeError("active set method did not converge")


def brute_force_box_qp(q, fixed, lo=0.0, hi=1.0):
    """Return the minimizer of the same problem by trying every face of the box."""
    n = len(q)
    var = [i for i in range(n) if i not in fixed]
    best, best_e = None, math.inf
    for states in itertools.product((lo, hi, None), repeat=len(var)):
        x = [fixed.get(i, 0.0) for i in range(n)]
        free = []
        for i, s in zip(var, states):
            if s is None:
                free.append(i)
            else:
                x[i] = s
        if free:
            for i, val in zip(free, _solve_free(q, x, free)):
                x[i] = val
        if any(x[i] < lo - 1e-12 or x[i] > hi + 1e-12 for i in var):
            continue
        e = energy(q, x)
        if e < best_e:
            best, best_e = x, e
    return best, best_e


def bbw(verts, tris, handles, bounded=True, normalize=True):
    """Return w with w[k][i] the weight of handle k at vertex i.

    handles is a list of vertex indices. With bounded=False the weights are
    the unbounded biharmonic weights (the same problem without 0 <= w <= 1).
    """
    lap = cotangent_laplacian(verts, tris)  # @line L1
    m = lumped_mass(verts, tris)
    q = bilaplacian(lap, m)  # @line L2
    n = len(verts)
    weights = []
    for k in range(len(handles)):  # @line L3
        fixed = {h: (1.0 if j == k else 0.0) for j, h in enumerate(handles)}
        if bounded:
            w, _ = box_qp(q, fixed)  # @line L4
        else:
            w = [fixed.get(i, 0.0) for i in range(n)]
            free = [i for i in range(n) if i not in fixed]
            for i, val in zip(free, _solve_free(q, w, free)):
                w[i] = val
        weights.append(w)
    if normalize:
        for i in range(n):  # @line L5
            s = sum(w[i] for w in weights)
            for w in weights:
                w[i] /= s
    return weights  # @line L6


def grid(nx, ny, width=1.0, height=1.0):
    """Return (verts, tris) of a regular grid split into right triangles."""
    verts = [(width * i / (nx - 1), height * j / (ny - 1)) for j in range(ny) for i in range(nx)]
    tris = []
    for j in range(ny - 1):
        for i in range(nx - 1):
            a, b = j * nx + i, j * nx + i + 1
            c, d = a + nx, b + nx
            tris.append((a, b, d))
            tris.append((a, d, c))
    return verts, tris
