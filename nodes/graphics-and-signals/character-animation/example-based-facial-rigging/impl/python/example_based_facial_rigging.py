# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/example-based-facial-rigging/. The authors are listed in prov/3M9YWE.jsonl.
"""Example-based facial rigging (after Li, Weise and Pauly 2010), on 2D triangle meshes.

The input is a generic blendshape rig (a neutral A0 and targets A1..An), the
neutral B0 of an actor, m example expressions S1..Sm of the actor, and a
first guess of the blend weights of each example. All meshes share one
triangulation. The output is a blendshape rig of the actor: targets B1..Bn
and the weights of the examples.

The method works with deformation gradients. For triangle t, the gradient
of a mesh X relative to the actor neutral is the 2 by 2 matrix
F = [x_b - x_a, x_c - x_a] [b_b - b_a, b_c - b_a]^(-1). Let D_i = F(B_i) - I
for the unknown targets, R_j = F(S_j) - I for the examples, and H_i =
G_i - I for the gradients G_i of the generic target i relative to the
generic neutral. The energy is

    E(D, alpha) = sum_j sum_t |sum_i alpha_ij D_i - R_j|_F^2
                  + beta sum_i sum_t |D_i - H_i|_F^2.

The first term asks the rig to reproduce the examples. The second is the
prior: each actor target should change its triangles like the generic
target, which is deformation transfer when the two meshes share a
triangulation. The start is D = H, the deformation transfer of the generic
rig. The method alternates an exact least squares step in D and a bounded
least squares step in alpha, with 0 <= alpha <= 1, and at the end recovers
the vertex positions of each target by a Poisson (least squares) solve.

The paper works on 3D meshes, weights the prior per triangle, and has
further terms; this file keeps the structure of the method only.
"""

from anim import inv, solve, sub


def gradient(rest, deformed, tri):
    """Return the 2 by 2 deformation gradient of one triangle."""
    a, b, c = tri
    e1, e2 = sub(rest[b], rest[a]), sub(rest[c], rest[a])
    f1, f2 = sub(deformed[b], deformed[a]), sub(deformed[c], deformed[a])
    q = inv([[e1[0], e2[0]], [e1[1], e2[1]]])
    return [[f1[r] * q[0][k] + f2[r] * q[1][k] for k in range(2)] for r in range(2)]


def flat_offsets(rest, deformed, tris):
    """Return the list over triangles of the 4 entries of F - I, flattened."""
    out = []
    for tri in tris:
        g = gradient(rest, deformed, tri)
        out.extend([g[0][0] - 1.0, g[0][1], g[1][0], g[1][1] - 1.0])
    return out


def energy(d, alpha, r, h, beta):
    """Return E(D, alpha) for flattened D_i, R_j and H_i."""
    e = 0.0
    for j, rj in enumerate(r):
        for p in range(len(rj)):
            s = sum(alpha[j][i] * d[i][p] for i in range(len(d))) - rj[p]
            e += s * s
    for di, hi in zip(d, h):
        e += beta * sum((x - y) ** 2 for x, y in zip(di, hi))
    return e


def blendshape_step(alpha, r, h, beta):
    """Return the D that minimizes E for fixed alpha.

    For each entry p, the vector (D_1[p], ..., D_n[p]) solves
    (A^T A + beta I) z = A^T (R_1[p], ..., R_m[p]) + beta (H_1[p], ..., H_n[p]),
    where A is the m by n matrix of the weights. The matrix is the same for
    every entry, so it is solved once with all entries as right hand sides.
    """
    n, m, size = len(h), len(r), len(h[0])
    mat = [[sum(alpha[j][a] * alpha[j][b] for j in range(m)) + (beta if a == b else 0.0) for b in range(n)] for a in range(n)]
    rhs = [[sum(alpha[j][a] * r[j][p] for j in range(m)) + beta * h[a][p] for p in range(size)] for a in range(n)]
    z = solve(mat, rhs)
    return [list(row) for row in z]


def bounded_lsq(gram, lin, start, tol=1e-14, max_iter=100000):
    """Minimize a^T G a - 2 b^T a over the box [0, 1]^n by cyclic coordinate descent.

    Each coordinate is set to its exact minimizer, clipped to [0, 1]. The
    objective never increases. The loop stops when no coordinate moves by
    more than tol.
    """
    a = [min(1.0, max(0.0, x)) for x in start]
    n = len(a)
    for _ in range(max_iter):
        move = 0.0
        for i in range(n):
            if gram[i][i] <= 0.0:
                continue
            v = (lin[i] - sum(gram[i][k] * a[k] for k in range(n) if k != i)) / gram[i][i]
            v = min(1.0, max(0.0, v))
            move = max(move, abs(v - a[i]))
            a[i] = v
        if move <= tol:
            break
    return a


def weight_step(d, r, alpha):
    """Return the weights that minimize E for fixed D, each in [0, 1]."""
    n = len(d)
    gram = [[sum(x * y for x, y in zip(d[a], d[b])) for b in range(n)] for a in range(n)]
    out = []
    for j, rj in enumerate(r):
        lin = [sum(x * y for x, y in zip(d[a], rj)) for a in range(n)]
        out.append(bounded_lsq(gram, lin, alpha[j]))
    return out


def poisson_reconstruct(rest, tris, grads, fixed=0):
    """Return the meshes whose triangle gradients fit grads in least squares.

    grads[k] is the list over triangles of 2 by 2 matrices for mesh k. The
    vertex fixed keeps its rest position. The normal matrix depends only on
    the rest mesh, so it is built once for all meshes and both coordinates.
    """
    nv = len(rest)
    free = [v for v in range(nv) if v != fixed]
    col = {v: i for i, v in enumerate(free)}
    qs = []
    for a, b, c in tris:
        e1, e2 = sub(rest[b], rest[a]), sub(rest[c], rest[a])
        qs.append(inv([[e1[0], e2[0]], [e1[1], e2[1]]]))
    size = len(free)
    ata = [[0.0] * size for _ in range(size)]
    atb = [[0.0] * (2 * len(grads)) for _ in range(size)]
    fp = rest[fixed]
    for t, (a, b, c) in enumerate(tris):
        q = qs[t]
        for k in range(2):
            coef = {b: q[0][k], c: q[1][k]}
            coef[a] = coef.get(a, 0.0) - q[0][k] - q[1][k]
            items = [(col[v], w) for v, w in coef.items() if v != fixed]
            shift = coef.get(fixed, 0.0)
            for i, wi in items:
                for j, wj in items:
                    ata[i][j] += wi * wj
            for g, gk in enumerate(grads):
                for r in range(2):
                    val = gk[t][r][k] - shift * fp[r]
                    for i, wi in items:
                        atb[i][2 * g + r] += wi * val
    x = solve(ata, atb)
    meshes = []
    for g in range(len(grads)):
        meshes.append([tuple(fp) if v == fixed else (x[col[v]][2 * g], x[col[v]][2 * g + 1]) for v in range(nv)])
    return meshes


def unflatten(dvec, ntri):
    """Return the list of 2 by 2 matrices I + D for one flattened D."""
    return [[[1.0 + dvec[4 * t], dvec[4 * t + 1]], [dvec[4 * t + 2], 1.0 + dvec[4 * t + 3]]] for t in range(ntri)]


def facial_rig(generic, actor_neutral, examples, alpha0, tris, beta=0.1, iterations=20):
    """Return (targets, alpha, history).

    generic is [A0, A1, ..., An], actor_neutral is B0, examples is
    [S1, ..., Sm], and alpha0[j] is the first guess of the weights of
    example j. history holds E after the start and after each step.
    """
    a0 = generic[0]
    h = [flat_offsets(a0, ai, tris) for ai in generic[1:]]  # @line L1
    r = [flat_offsets(actor_neutral, s, tris) for s in examples]  # @line L2
    d = [list(x) for x in h]
    alpha = [[min(1.0, max(0.0, x)) for x in row] for row in alpha0]
    history = [energy(d, alpha, r, h, beta)]
    for _ in range(iterations):  # @line L3
        d = blendshape_step(alpha, r, h, beta)  # @line L4
        history.append(energy(d, alpha, r, h, beta))
        alpha = weight_step(d, r, alpha)  # @line L5
        history.append(energy(d, alpha, r, h, beta))  # @line L6
    grads = [unflatten(di, len(tris)) for di in d]
    targets = poisson_reconstruct(actor_neutral, tris, grads)  # @line L7
    return targets, alpha, history  # @line L8
