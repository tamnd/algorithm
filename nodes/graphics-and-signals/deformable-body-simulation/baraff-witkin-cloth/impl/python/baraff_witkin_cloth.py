# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baraff-witkin-cloth/. The authors are listed in prov/7F3XVP.jsonl.

"""Large steps in cloth simulation (Baraff and Witkin 1998), in 3D.

The cloth is a triangle mesh with rest coordinates (u, v) for each vertex.
Each triangle has a stretch condition C = a (|w_u| - b_u, |w_v| - b_v) and a
shear condition C = a w_u . w_v, where (w_u w_v) = (dx1 dx2) [[du1, du2], [dv1, dv2]]^-1
and a is the rest area. Each interior edge has a bend condition C = theta, the
signed angle between the normals of its two triangles. A condition with
stiffness k has the energy k/2 C^2, the force f_i = -k dC/dx_i C and the
force Jacobian K_ij = -k (dC/dx_i dC/dx_j^T + d2C/dx_i dx_j C)
(equations (7) and (8) of the paper). The damping force is
d_i = -k_d dC/dx_i Cdot (equation (11)).

One step solves the linearized backward Euler system
(M - h df/dv - h^2 df/dx) dv = h (f0 + h df/dx v0) (equation (15)) with the
modified preconditioned conjugate gradient method of Section 5.3, which keeps
the constrained velocity components of each particle at the values z_i.

Simplifications of this code, not of the paper:
- The bend Jacobian keeps only the term -k dC/dx_i dC/dx_j^T (Gauss-Newton).
  It is exact where theta = 0. The bend force itself is exact.
- No collisions. Constraints are given by the caller as {i: (S_i, z_i)}.
"""

import math

from anim import add, cross, dot, norm, scale, sub

GRAVITY = (0.0, -9.81, 0.0)
IDENTITY = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
ZERO3 = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))


# ---------------------------------------------------------------- 3 by 3 blocks


def outer(a, b, s=1.0):
    return [[s * a[r] * b[c] for c in range(3)] for r in range(3)]


def block_vec(m, x):
    return (m[0][0] * x[0] + m[0][1] * x[1] + m[0][2] * x[2],
            m[1][0] * x[0] + m[1][1] * x[1] + m[1][2] * x[2],
            m[2][0] * x[0] + m[2][1] * x[1] + m[2][2] * x[2])


def add_block(mat, i, j, blk, s=1.0):
    """mat[i][j] += s blk for a sparse block matrix stored as {i: {j: 3 by 3}}."""
    row = mat.setdefault(i, {})
    cur = row.get(j)
    if cur is None:
        cur = [[0.0] * 3 for _ in range(3)]
        row[j] = cur
    for r in range(3):
        for c in range(3):
            cur[r][c] += s * blk[r][c]


def sparse_matvec(mat, x):
    out = []
    for i in range(len(x)):
        s0 = s1 = s2 = 0.0
        for j, m in mat.get(i, {}).items():
            xj = x[j]
            s0 += m[0][0] * xj[0] + m[0][1] * xj[1] + m[0][2] * xj[2]
            s1 += m[1][0] * xj[0] + m[1][1] * xj[1] + m[1][2] * xj[2]
            s2 += m[2][0] * xj[0] + m[2][1] * xj[1] + m[2][2] * xj[2]
        out.append((s0, s1, s2))
    return out


def vdot(a, b):
    """Dot product of two lists of 3-vectors."""
    return sum(p[0] * q[0] + p[1] * q[1] + p[2] * q[2] for p, q in zip(a, b))


# ---------------------------------------------------------------- the cloth


class Cloth:
    def __init__(self, uv, triangles, density=1.0, k_stretch=1.0, k_shear=1.0, k_bend=0.0,
                 kd_stretch=0.0, kd_shear=0.0, kd_bend=0.0, b_u=1.0, b_v=1.0, gravity=GRAVITY):
        self.n = len(uv)
        self.triangles = [tuple(t) for t in triangles]
        self.k_stretch, self.k_shear, self.k_bend = k_stretch, k_shear, k_bend
        self.kd_stretch, self.kd_shear, self.kd_bend = kd_stretch, kd_shear, kd_bend
        self.b_u, self.b_v = b_u, b_v
        self.rest = []  # per triangle: (area, cu, cv) with w_u = sum cu_i x_i and w_v = sum cv_i x_i
        self.mass = [0.0] * self.n
        for t in self.triangles:
            p0, p1, p2 = (uv[i] for i in t)
            du1, dv1 = p1[0] - p0[0], p1[1] - p0[1]
            du2, dv2 = p2[0] - p0[0], p2[1] - p0[1]
            det = du1 * dv2 - du2 * dv1
            if det == 0.0:
                raise ValueError("degenerate triangle in (u, v)")
            cu1, cu2 = dv2 / det, -dv1 / det
            cv1, cv2 = -du2 / det, du1 / det
            area = 0.5 * abs(det)
            self.rest.append((area, (-cu1 - cu2, cu1, cu2), (-cv1 - cv2, cv1, cv2)))
            for i in t:
                self.mass[i] += density * area / 3.0  # one third of each incident triangle
        self.f_ext = [scale(gravity, m) for m in self.mass]
        # bend edges (x1, x2, x3, x4): x3 -> x4 is the shared edge as it runs in the first
        # triangle, x1 is opposite in that triangle and x2 is opposite in the other one
        first = {}
        self.edges = []
        for t in self.triangles:
            for e in range(3):
                a, b, c = t[e], t[(e + 1) % 3], t[(e + 2) % 3]
                if (b, a) in first:
                    self.edges.append((first.pop((b, a)), c, b, a))
                else:
                    first[(a, b)] = c

    # ------------------------------------------------------------ conditions

    def conditions(self, x):
        """Return (indices, C, gradients, s, B, k, k_d) for every scalar condition.

        The second derivative of C is d2C/dx_i dx_j = s[i][j] B, or s is None if
        the code does not use it.
        """
        out = []
        for t, (area, cu, cv) in zip(self.triangles, self.rest):
            xs = [x[i] for i in t]
            wu = add(add(scale(xs[0], cu[0]), scale(xs[1], cu[1])), scale(xs[2], cu[2]))
            wv = add(add(scale(xs[0], cv[0]), scale(xs[1], cv[1])), scale(xs[2], cv[2]))
            for w, coef, b in ((wu, cu, self.b_u), (wv, cv, self.b_v)):
                length = norm(w)
                wh = scale(w, 1.0 / length)
                grads = [scale(wh, area * coef[i]) for i in range(3)]
                s = [[area * coef[i] * coef[j] / length for j in range(3)] for i in range(3)]
                proj = [[(1.0 if r == c else 0.0) - wh[r] * wh[c] for c in range(3)] for r in range(3)]
                out.append((t, area * (length - b), grads, s, proj, self.k_stretch, self.kd_stretch))
            grads = [add(scale(wv, area * cu[i]), scale(wu, area * cv[i])) for i in range(3)]
            s = [[area * (cu[i] * cv[j] + cv[i] * cu[j]) for j in range(3)] for i in range(3)]
            out.append((t, area * dot(wu, wv), grads, s, IDENTITY, self.k_shear, self.kd_shear))
        if self.k_bend != 0.0 or self.kd_bend != 0.0:
            for e in self.edges:
                theta, grads = bend_angle(*(x[i] for i in e))
                out.append((e, theta, grads, None, None, self.k_bend, self.kd_bend))
        return out

    def energy(self, x):
        return sum(0.5 * k * c * c for _, c, _, _, _, k, _ in self.conditions(x))

    def forces(self, x, v):
        """Return (f, K, D): internal forces (elastic and damping), df/dx and df/dv as block matrices."""
        f = [[0.0, 0.0, 0.0] for _ in range(self.n)]
        kmat, dmat = {}, {}
        for idx, c, grads, s, base, k, kd in self.conditions(x):
            cdot = sum(dot(g, v[i]) for g, i in zip(grads, idx))
            for a, i in enumerate(idx):
                fi = f[i]
                coef = -k * c - kd * cdot  # equations (7) and (11)
                for r in range(3):
                    fi[r] += coef * grads[a][r]
                for b, j in enumerate(idx):
                    gg = outer(grads[a], grads[b])
                    add_block(kmat, i, j, gg, -k)  # equation (8), first term
                    if s is not None:
                        # equation (8), second term, and equation (12) without its asymmetric term
                        add_block(kmat, i, j, base, -(k * c + kd * cdot) * s[a][b])
                    if kd != 0.0:
                        add_block(dmat, i, j, gg, -kd)  # dd/dv
        return [tuple(fi) for fi in f], kmat, dmat

    # ------------------------------------------------------------ one step

    def system(self, x, v, h):
        """Return the block matrix A = M - h df/dv - h^2 df/dx and b = h (f0 + h df/dx v0)."""
        f, kmat, dmat = self.forces(x, v)  # @line L1
        amat = {}
        for i in range(self.n):
            add_block(amat, i, i, IDENTITY, self.mass[i])
        for src, w in ((kmat, -h * h), (dmat, -h)):
            for i, row in src.items():
                for j, blk in row.items():
                    add_block(amat, i, j, blk, w)
        kv = sparse_matvec(kmat, v)
        b = [scale(add(add(f[i], self.f_ext[i]), scale(kv[i], h)), h) for i in range(self.n)]  # @line L2
        return amat, b

    def step(self, x, v, h, constraints=None, eps=1e-8, max_iter=2000):
        """One step. Return (x, v, iterations of modified-pcg)."""
        amat, b = self.system(x, v, h)
        dv, iters = modified_pcg(amat, b, constraints or {}, eps, max_iter)
        new_v = [add(v[i], dv[i]) for i in range(self.n)]
        new_x = [add(x[i], scale(new_v[i], h)) for i in range(self.n)]  # @line L11
        return new_x, new_v, iters


def bend_angle(x1, x2, x3, x4):
    """Signed angle theta between the triangles (x3, x4, x1) and (x4, x3, x2), and d theta/dx.

    theta = atan2((n2 x n1) . e, n1 . n2) with the unit edge e from x3 to x4 and
    n1 = (x1 - x3) x (x1 - x4), n2 = (x2 - x4) x (x2 - x3). The gradient is the
    formula of Bridson, Marino and Fedkiw (2003). The tests check it against
    central differences of theta.
    """
    e = sub(x4, x3)
    n1 = cross(sub(x1, x3), sub(x1, x4))
    n2 = cross(sub(x2, x4), sub(x2, x3))
    le = norm(e)
    q1, q2 = dot(n1, n1), dot(n2, n2)
    theta = math.atan2(dot(cross(n2, n1), e) / le, dot(n1, n2))
    a1, a2 = scale(n1, 1.0 / q1), scale(n2, 1.0 / q2)
    u1 = scale(a1, le)
    u2 = scale(a2, le)
    u3 = add(scale(a1, dot(sub(x1, x4), e) / le), scale(a2, dot(sub(x2, x4), e) / le))
    u4 = scale(add(scale(a1, dot(sub(x1, x3), e) / le), scale(a2, dot(sub(x2, x3), e) / le)), -1.0)
    return theta, [u1, u2, u3, u4]


# ---------------------------------------------------------------- modified-pcg


def modified_pcg(amat, b, constraints, eps=1e-8, max_iter=2000):
    """Solve A dv = b with the components of particle i in the range of I - S_i fixed at z_i.

    constraints maps a particle i to (S_i, z_i), with S_i one of the filters of
    equation (13) and z_i in the range of I - S_i. The preconditioner is the
    diagonal of A, so applying P^-1 divides each component by A_ii.
    Return (dv, iterations).
    """
    n = len(b)

    def filt(a):
        return [block_vec(constraints[i][0], a[i]) if i in constraints else a[i] for i in range(n)]

    inv_diag = [tuple(1.0 / amat[i][i][r][r] for r in range(3)) for i in range(n)]

    def precond(a):
        return [(p[0] * q[0], p[1] * q[1], p[2] * q[2]) for p, q in zip(inv_diag, a)]

    dv = [tuple(constraints[i][1]) if i in constraints else (0.0, 0.0, 0.0) for i in range(n)]  # @line L3
    fb = filt(b)
    delta0 = vdot(fb, precond(fb))
    av = sparse_matvec(amat, dv)
    r = filt([sub(b[i], av[i]) for i in range(n)])  # @line L4
    c = filt(precond(r))
    delta_new = vdot(r, c)  # @line L5
    iters = 0
    while delta_new > eps * eps * delta0 and iters < max_iter:  # @line L6
        q = filt(sparse_matvec(amat, c))
        alpha = delta_new / vdot(c, q)  # @line L7
        dv = [add(dv[i], scale(c[i], alpha)) for i in range(n)]
        r = [sub(r[i], scale(q[i], alpha)) for i in range(n)]  # @line L8
        s = precond(r)
        delta_old, delta_new = delta_new, vdot(r, s)  # @line L9
        beta = delta_new / delta_old
        c = filt([add(s[i], scale(c[i], beta)) for i in range(n)])  # @line L10
        iters += 1
    return dv, iters


def constraint_force(amat, b, dv):
    """e = A dv - b. For a constrained particle, e_i is the force that kept the constraint (Section 5.3)."""
    av = sparse_matvec(amat, dv)
    return [sub(av[i], b[i]) for i in range(len(b))]


# ---------------------------------------------------------------- filters and meshes


def pin(z=(0.0, 0.0, 0.0)):
    """A filter that fixes all three components of dv at z."""
    return (ZERO3, tuple(z))


def plane(p, z_along):
    """A filter that fixes the dv component along the unit vector p at z_along."""
    s = [[(1.0 if r == c else 0.0) - p[r] * p[c] for c in range(3)] for r in range(3)]
    return (s, scale(p, z_along))


def grid(nx, ny, spacing):
    """A grid cloth in the plane z = 0. Return (uv, triangles, x) with x = (u, -v, 0)."""
    def idx(i, j):
        return j * nx + i

    uv = [(i * spacing, j * spacing) for j in range(ny) for i in range(nx)]
    tris = []
    for j in range(ny - 1):
        for i in range(nx - 1):
            tris.append((idx(i, j), idx(i + 1, j), idx(i + 1, j + 1)))
            tris.append((idx(i, j), idx(i + 1, j + 1), idx(i, j + 1)))
    x = [(u, -w, 0.0) for u, w in uv]
    return uv, tris, x
