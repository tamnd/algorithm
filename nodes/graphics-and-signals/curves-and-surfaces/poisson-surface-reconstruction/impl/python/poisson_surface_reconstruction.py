# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/poisson-surface-reconstruction/. The authors are listed in prov/6BENWT.jsonl.

"""Poisson surface reconstruction (Kazhdan, Bolitho, Hoppe 2006), on a uniform grid.

The input is a set of points with outward unit normals. The vector field V
is the inward normals splatted onto the nodes of a grid with trilinear
weights; it stands for the gradient of the indicator function chi (1 inside,
0 outside), smoothed. chi is the function in the span of the trilinear hat
functions phi_o, zero on the border of the grid, that minimizes
integral |grad chi - V|^2. Its coefficients solve the Galerkin system
L x = b with L[o][o'] = integral grad phi_o . grad phi_o' and
b[o] = integral V . grad phi_o, by conjugate gradients. The surface is the
level set of chi at the mean of chi over the samples, extracted with
marching tetrahedra.

This is the method on the full grid of one depth. The paper uses an adaptive
octree, quadratic B-splines, density weights and marching cubes.
"""

import math

Vec = tuple[float, float, float]

# 1D integrals of hat functions on a uniform grid of spacing h, by offset j - i:
# mass  integral phi_i phi_j  = h * {0: 2/3, +-1: 1/6}
# stiff integral phi_i' phi_j' = (1/h) * {0: 2, +-1: -1}
# mixed integral phi_i phi_j'  = {+1: 1/2, -1: -1/2, 0: 0}  (j = i + offset)
MASS = {-1: 1 / 6, 0: 2 / 3, 1: 1 / 6}
STIFF = {-1: -1.0, 0: 2.0, 1: -1.0}
MIXED = {-1: -0.5, 0: 0.0, 1: 0.5}


def _apply(x: list[float], m: int, weights: tuple[dict[int, float], dict[int, float], dict[int, float]]) -> list[float]:
    """Apply the tensor product of three 1D stencils to a grid vector (index i + m (j + m k)),
    keeping the border nodes at zero."""
    out = x
    for axis, w in enumerate(weights):
        step = m ** axis
        nxt = [0.0] * len(out)
        for idx in range(len(out)):
            i = (idx // step) % m
            s = 0.0
            for off, c in w.items():
                if c and 0 <= i + off < m:
                    s += c * out[idx + off * step]
            nxt[idx] = s
        out = nxt
    return out


def _interior(m: int) -> list[bool]:
    return [0 < i < m - 1 and 0 < j < m - 1 and 0 < k < m - 1
            for k in range(m) for j in range(m) for i in range(m)]


def laplacian(x: list[float], m: int, h: float) -> list[float]:
    """L x restricted to the interior nodes (x must be zero on the border)."""
    a = _apply(x, m, (STIFF, MASS, MASS))
    b = _apply(x, m, (MASS, STIFF, MASS))
    c = _apply(x, m, (MASS, MASS, STIFF))
    inner = _interior(m)
    return [h * (a[t] + b[t] + c[t]) if inner[t] else 0.0 for t in range(len(x))]


def divergence_rhs(field: list[list[float]], m: int, h: float) -> list[float]:
    """b[o] = integral V . grad phi_o, where V = sum_node V_node phi_node (3 components)."""
    out = [0.0] * (m ** 3)
    for axis in range(3):
        w = [MASS, MASS, MASS]
        w[axis] = {-off: c for off, c in MIXED.items()}  # out[o] = sum_n V_n * mixed(n -> o)
        part = _apply(field[axis], m, (w[0], w[1], w[2]))
        for t in range(len(out)):
            out[t] += h * h * part[t]
    inner = _interior(m)
    return [out[t] if inner[t] else 0.0 for t in range(len(out))]


def conjugate_gradient(apply, b: list[float], tol: float = 1e-10, max_iter: int = 2000) -> list[float]:
    x = [0.0] * len(b)
    r = b[:]
    p = r[:]
    rr = sum(v * v for v in r)
    stop = tol * tol * max(rr, 1e-300)
    for _ in range(max_iter):
        if rr <= stop:
            break
        ap = apply(p)
        alpha = rr / sum(p[t] * ap[t] for t in range(len(p)))
        for t in range(len(x)):
            x[t] += alpha * p[t]
            r[t] -= alpha * ap[t]
        rr_new = sum(v * v for v in r)
        beta = rr_new / rr
        rr = rr_new
        for t in range(len(p)):
            p[t] = r[t] + beta * p[t]
    return x


def _trilinear(p: Vec, origin: Vec, h: float, m: int):
    """The 8 (node index, weight) pairs of point p."""
    u = [(p[a] - origin[a]) / h for a in range(3)]
    base = [min(max(int(math.floor(u[a])), 0), m - 2) for a in range(3)]
    f = [u[a] - base[a] for a in range(3)]
    out = []
    for dz in (0, 1):
        for dy in (0, 1):
            for dx in (0, 1):
                wgt = (f[0] if dx else 1 - f[0]) * (f[1] if dy else 1 - f[1]) * (f[2] if dz else 1 - f[2])
                out.append((base[0] + dx + m * (base[1] + dy + m * (base[2] + dz)), wgt))
    return out


def setup(points: list[Vec], normals: list[Vec], depth: int, pad: float = 0.25):
    """The grid (origin, h, m), the splatted field V and the right hand side b."""
    lo = [min(p[a] for p in points) for a in range(3)]
    hi = [max(p[a] for p in points) for a in range(3)]
    side = max(hi[a] - lo[a] for a in range(3)) * (1 + 2 * pad)
    mid = [(lo[a] + hi[a]) / 2 for a in range(3)]
    m = 2 ** depth + 1
    h = side / (m - 1)
    origin = (mid[0] - side / 2, mid[1] - side / 2, mid[2] - side / 2)  # @line L1
    field = [[0.0] * (m ** 3) for _ in range(3)]
    for p, n in zip(points, normals):
        for idx, wgt in _trilinear(p, origin, h, m):  # @line L2
            for a in range(3):
                field[a][idx] -= wgt * n[a]  # inward normals: the gradient of chi points inward
    b = divergence_rhs(field, m, h)  # @line L3
    return origin, h, m, field, b


# marching tetrahedra on the grid (inside: value < c), as on the marching tetrahedra page
_TETS = [(0, 1, 3, 7), (0, 3, 2, 7), (0, 2, 6, 7), (0, 6, 4, 7), (0, 4, 5, 7), (0, 5, 1, 7)]


def _tet_table():
    ref = [(0, 0, 0), (2, 0, 0), (0, 2, 0), (0, 0, 2)]
    table = []
    for mask in range(16):
        ins = [i for i in range(4) if mask >> i & 1]
        out = [i for i in range(4) if not mask >> i & 1]
        if len(ins) in (0, 4):
            table.append([])
            continue
        if len(ins) == 1:
            polys = [[(ins[0], o) for o in out]]
        elif len(ins) == 3:
            polys = [[(i, out[0]) for i in ins]]
        else:
            a, b = ins
            c, d = out
            polys = [[(a, c), (a, d), (b, d)], [(a, c), (b, d), (b, c)]]
        tris = []
        for tri in polys:
            q = [tuple(ref[i][k] + ref[j][k] for k in range(3)) for i, j in tri]
            u = [q[1][k] - q[0][k] for k in range(3)]
            v = [q[2][k] - q[0][k] for k in range(3)]
            nrm = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
            o = [2 * ref[out[0]][k] - q[0][k] for k in range(3)]
            if sum(nrm[k] * o[k] for k in range(3)) < 0:
                tri = [tri[0], tri[2], tri[1]]
            tris.append(tuple(tri))
        table.append(tris)
    return table


_TABLE = _tet_table()


def marching_tetrahedra(vals: list[float], m: int, origin: Vec, h: float, c: float):
    verts: list[Vec] = []
    index: dict[tuple[int, int], int] = {}
    tris: list[tuple[int, int, int]] = []
    corner = [dx + m * (dy + m * dz) for dz in (0, 1) for dy in (0, 1) for dx in (0, 1)]

    def pos(t: int) -> Vec:
        return (origin[0] + h * (t % m), origin[1] + h * (t // m % m), origin[2] + h * (t // (m * m)))

    def vertex(a: int, b: int) -> int:
        key = (a, b) if a < b else (b, a)
        k = index.get(key)
        if k is None:
            s = (c - vals[a]) / (vals[b] - vals[a])
            pa, pb = pos(a), pos(b)
            k = len(verts)
            verts.append(tuple(pa[i] + s * (pb[i] - pa[i]) for i in range(3)))
            index[key] = k
        return k

    for z in range(m - 1):
        for y in range(m - 1):
            for x in range(m - 1):
                base = x + m * (y + m * z)
                g = [base + d for d in corner]
                ins = [vals[t] < c for t in g]
                for tet in _TETS:
                    mask = sum(1 << i for i in range(4) if ins[tet[i]])
                    for tri in _TABLE[mask]:
                        tris.append(tuple(vertex(g[tet[i]], g[tet[j]]) for i, j in tri))
    return verts, tris


def evaluate(x: list[float], p: Vec, origin: Vec, h: float, m: int) -> float:
    return sum(wgt * x[idx] for idx, wgt in _trilinear(p, origin, h, m))


def poisson_reconstruction(points: list[Vec], normals: list[Vec], depth: int = 4, tol: float = 1e-10):
    """Return (vertices, triangles, chi, grid) for oriented points.

    The mesh is the level set of chi at the mean of chi over the samples,
    oriented outward. chi is zero on the border of the grid, so the mesh is a
    closed manifold when the iso value is positive. Cost: O(m^3) per conjugate
    gradient step on a grid of m = 2^depth + 1 nodes per axis.
    """
    origin, h, m, _, b = setup(points, normals, depth)
    x = conjugate_gradient(lambda v: laplacian(v, m, h), b, tol)  # @line L4
    iso = sum(evaluate(x, p, origin, h, m) for p in points) / len(points)  # @line L5
    neg = [-v for v in x]  # inside is chi > iso, which is -chi < -iso
    verts, tris = marching_tetrahedra(neg, m, origin, h, -iso)  # @line L6
    return verts, tris, x, (origin, h, m, iso)  # @line L7
