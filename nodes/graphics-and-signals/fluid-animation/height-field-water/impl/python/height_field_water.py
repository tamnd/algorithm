# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/height-field-water/. The authors are listed in prov/CH9SFZ.jsonl.
"""Height field water: the linearized shallow water wave equation with implicit steps.

The water surface is a grid of heights h[i][j] over cells of size dx. The
wave equation is d^2 h / dt^2 = div(g d grad h), with the water depth d. One
step is

    r = h + (1 - damping) (h - h_prev),
    (I + A_x) z = r       (a tridiagonal solve along each row),
    (I + A_y) h_new = z   (a tridiagonal solve along each column),

where A_x adds e (z_i - z_k) for each x neighbor k of cell i, with
e = g dt^2 (d_i + d_k) / (2 dx^2), or e = 0 if one of the two cells is dry,
and A_y is the same along y. There is no
flow through the border of the grid (Neumann boundary). The scheme follows
the idea of Kass and Miller (1990): implicit steps with tridiagonal solves
along the rows and the columns. It is not claimed to be their exact equations.

The functions work with float or with fractions.Fraction values.
"""

G = 9.81


def thomas(sub, diag, sup, rhs):
    """Solve a tridiagonal system by the Thomas algorithm.

    sub[i] is the entry left of the diagonal in row i (sub[0] is not used),
    sup[i] the entry right of it (sup[n-1] is not used). No pivoting: the
    matrix must be strictly diagonally dominant or symmetric positive definite.
    """
    n = len(diag)
    c = [0] * n
    d = [0] * n
    c[0] = sup[0] / diag[0] if n > 1 else 0
    d[0] = rhs[0] / diag[0]
    for i in range(1, n):
        m = diag[i] - sub[i] * c[i - 1]
        c[i] = sup[i] / m if i < n - 1 else 0
        d[i] = (rhs[i] - sub[i] * d[i - 1]) / m
    x = [0] * n
    x[n - 1] = d[n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = d[i] - c[i] * x[i + 1]
    return x


def solve_line(values, depths, s):
    """Solve (I + A) z = values on one line, with e_k = s (depths[k] + depths[k + 1]) between neighbors k and k + 1.

    e_k is 0 if one of the two cells is dry (depth 0), so no water flows into
    or out of a dry cell. This is a choice of this file.
    """
    n = len(values)
    zero = 0 * s  # a zero of the type of s, so that Fraction input gives Fraction output
    e = [s * (depths[k] + depths[k + 1]) if depths[k] > 0 and depths[k + 1] > 0 else zero for k in range(n - 1)]
    sub = [zero] + [-x for x in e]
    sup = [-x for x in e] + [zero]
    diag = [1 + (e[k - 1] if k > 0 else zero) + (e[k] if k < n - 1 else zero) for k in range(n)]
    return thomas(sub, diag, sup, values)


def step(h, h_prev, depth, dt, dx, g=G, damping=0):
    """One implicit step. h, h_prev and depth are lists of columns, indexed [i][j]. Returns (h_new, h)."""
    nx, ny = len(h), len(h[0])
    r = [[h[i][j] + (1 - damping) * (h[i][j] - h_prev[i][j]) for j in range(ny)] for i in range(nx)]  # @line L1
    s = g * dt * dt / (2 * dx * dx)  # @line L2
    z = [[0] * ny for _ in range(nx)]
    for j in range(ny):
        row = solve_line([r[i][j] for i in range(nx)], [depth[i][j] for i in range(nx)], s)  # @line L3
        for i in range(nx):
            z[i][j] = row[i]
    h_new = [solve_line(z[i], depth[i], s) for i in range(nx)]  # @line L4
    return h_new, h  # @line L5


def water_depth(h, ground):
    """The depth d = max(h - ground, 0) of each cell."""
    return [[max(hv - gv, 0) for hv, gv in zip(hc, gc)] for hc, gc in zip(h, ground)]


def simulate(h, ground, dt, dx, steps, g=G, damping=0):
    """Run steps from rest at h, with the depth from the ground updated before each step. Returns the last h."""
    h_prev = [list(col) for col in h]
    for _ in range(steps):
        h, h_prev = step(h, h_prev, water_depth(h, ground), dt, dx, g, damping)
    return h


def volume(h, dx):
    """The water volume above the zero level, dx^2 times the sum of the heights."""
    return dx * dx * sum(sum(col) for col in h)


def discrete_energy(h, h_prev, depth, dt, dx, g=G):
    """|h - h_prev|^2 + (<M h, h> + <M h_prev, h_prev>) / 2 with M = A_x + A_y + A_x A_y; see the proof page.

    The step does not increase it when the depth is the same in every cell.
    """
    nx, ny = len(h), len(h[0])

    def apply_a(q, axis):
        s = g * dt * dt / (2 * dx * dx)
        out = [[0.0] * ny for _ in range(nx)]
        for i in range(nx):
            for j in range(ny):
                acc = 0.0
                for di, dj in ((1, 0), (-1, 0)) if axis == 0 else ((0, 1), (0, -1)):
                    k, l = i + di, j + dj
                    if 0 <= k < nx and 0 <= l < ny and depth[i][j] > 0 and depth[k][l] > 0:
                        acc += s * (depth[i][j] + depth[k][l]) * (q[i][j] - q[k][l])
                out[i][j] = acc
        return out

    def m_dot(q):
        ax = apply_a(q, 0)
        ay = apply_a(q, 1)
        axy = apply_a(ay, 0)
        return sum(q[i][j] * (ax[i][j] + ay[i][j] + axy[i][j]) for i in range(nx) for j in range(ny))

    kinetic = sum((h[i][j] - h_prev[i][j]) ** 2 for i in range(nx) for j in range(ny))
    return kinetic + 0.5 * (m_dot(h) + m_dot(h_prev))
