# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-finite-element-method/. The authors are listed in prov/ZK2C1A.jsonl.

"""Adaptive P1 finite elements for -Laplacian(u) = f with Dirichlet data in 2D.

The loop is SOLVE, ESTIMATE, MARK, REFINE:
- SOLVE: conforming P1 elements on triangles, conjugate gradients
  (scisparse.cg) on the free nodes;
- ESTIMATE: the residual estimator eta_K^2 = h_K^2 ||f||_K^2
  + h_K sum over the interior edges E of K of ||[du_h/dn]||_E^2,
  with h_K = |K|^(1/2), the form used by Cascon, Kreuzer, Nochetto and
  Siebert (2008), because h_K shrinks under every bisection;
- MARK: Dorfler marking with parameter theta (sort, then take the largest);
- REFINE: newest vertex bisection with closure, so the mesh stays conforming.

A mesh is (coords, elements, boundary). coords is a list of (x, y).
An element [z1, z2, z3] has the refinement edge z1 z2 and the newest
vertex z3. boundary is a list of Dirichlet edges [a, b]. Real-RAM cost
per step: O(M log M) for M elements plus the cost of the CG solve.
"""

import math

import scisparse


def l_shape_mesh():
    """Return the six-triangle mesh of the L-shaped domain (-1, 1)^2 minus [0, 1) x (-1, 0].

    The refinement edges are the diagonals of the three squares, so the
    labeling is compatible: each diagonal is the refinement edge of both
    triangles that share it.
    """
    coords = [(-1.0, -1.0), (0.0, -1.0), (-1.0, 0.0), (0.0, 0.0),
              (1.0, 0.0), (-1.0, 1.0), (0.0, 1.0), (1.0, 1.0)]
    elements = [[0, 3, 1], [3, 0, 2], [3, 5, 2], [5, 3, 6], [3, 7, 4], [7, 3, 6]]
    boundary = [[0, 1], [1, 3], [3, 4], [4, 7], [7, 6], [6, 5], [5, 2], [2, 0]]
    return coords, elements, boundary


def square_mesh():
    """Return the two-triangle mesh of the unit square with the diagonal as refinement edge."""
    coords = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    elements = [[0, 2, 1], [2, 0, 3]]
    boundary = [[0, 1], [1, 2], [2, 3], [3, 0]]
    return coords, elements, boundary


def _edge(a, b):
    return (a, b) if a < b else (b, a)


def refine_nvb(coords, elements, boundary, marked):
    """Newest vertex bisection of the marked elements, with closure.

    Return new (coords, elements, boundary). Every marked element is bisected
    at least once; more elements are bisected only to remove hanging nodes.
    """
    coords = list(coords)
    touching = {}
    for t, z in enumerate(elements):
        for r in range(3):
            touching.setdefault(_edge(z[r], z[(r + 1) % 3]), []).append(t)
    edge_mark = {}
    stack = []
    for t in marked:
        z = elements[t]
        e = _edge(z[0], z[1])
        if e not in edge_mark:
            edge_mark[e] = None
            stack.append(e)
    while stack:  # closure: a marked edge forces the refinement edge
        for t in touching[stack.pop()]:
            z = elements[t]
            r = _edge(z[0], z[1])
            if r not in edge_mark:
                edge_mark[r] = None
                stack.append(r)
    for e in edge_mark:
        (xa, ya), (xb, yb) = coords[e[0]], coords[e[1]]
        edge_mark[e] = len(coords)
        coords.append(((xa + xb) / 2, (ya + yb) / 2))
    new = []
    for z1, z2, z3 in elements:
        m = edge_mark.get(_edge(z1, z2))
        if m is None:
            new.append([z1, z2, z3])
            continue
        m2 = edge_mark.get(_edge(z3, z1))
        m1 = edge_mark.get(_edge(z2, z3))
        if m2 is None:
            new.append([z3, z1, m])
        else:
            new.extend([[m, z3, m2], [z1, m, m2]])
        if m1 is None:
            new.append([z2, z3, m])
        else:
            new.extend([[m, z2, m1], [z3, m, m1]])
    bnew = []
    for a, b in boundary:
        m = edge_mark.get(_edge(a, b))
        if m is None:
            bnew.append([a, b])
        else:
            bnew.extend([[a, m], [m, b]])
    return coords, new, bnew


def _geometry(coords, z):
    (x0, y0), (x1, y1), (x2, y2) = coords[z[0]], coords[z[1]], coords[z[2]]
    d = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
    grads = [((y1 - y2) / d, (x2 - x1) / d), ((y2 - y0) / d, (x0 - x2) / d),
             ((y0 - y1) / d, (x1 - x0) / d)]
    return abs(d) / 2, grads


def solve_p1(coords, elements, boundary, f, g, tol=1e-10):
    """Return the nodal values U of the P1 Galerkin solution.

    u = g on the boundary nodes (nodal interpolation of g); the load uses the
    centroid rule f(c) |K| / 3 for each vertex of K, which is exact for
    constant f. The free system is solved by conjugate gradients.
    """
    n = len(coords)
    dirichlet = sorted({v for e in boundary for v in e})
    U = [0.0] * n
    is_dir = [False] * n
    for v in dirichlet:
        is_dir[v] = True
        U[v] = g(*coords[v])
    free = [v for v in range(n) if not is_dir[v]]
    index = {v: i for i, v in enumerate(free)}
    A = [dict() for _ in free]
    b = [0.0] * len(free)
    for z in elements:
        area, grads = _geometry(coords, z)
        cx = sum(coords[v][0] for v in z) / 3
        cy = sum(coords[v][1] for v in z) / 3
        fk = f(cx, cy) * area / 3
        for r in range(3):
            i = index.get(z[r])
            if i is None:
                continue
            b[i] += fk
            gr = grads[r]
            row = A[i]
            for s in range(3):
                gs = grads[s]
                val = area * (gr[0] * gs[0] + gr[1] * gs[1])
                j = index.get(z[s])
                if j is None:
                    b[i] -= val * U[z[s]]
                else:
                    row[j] = row.get(j, 0.0) + val
    if free:
        x, _ = scisparse.cg(A, b, tol=tol, maxit=20 * len(free) + 100)
        for v, val in zip(free, x):
            U[v] = val
    return U


def gradient(coords, z, U):
    """Return the constant gradient of the P1 function U on the element z."""
    _, grads = _geometry(coords, z)
    return (sum(U[z[r]] * grads[r][0] for r in range(3)),
            sum(U[z[r]] * grads[r][1] for r in range(3)))


def estimate(coords, elements, U, f):
    """Return the list of squared residual indicators eta_K^2 for P1 and -Laplacian(u) = f."""
    eta2 = []
    owner = {}
    grads = []
    hk = []
    for t, z in enumerate(elements):
        area, _ = _geometry(coords, z)
        cx = sum(coords[v][0] for v in z) / 3
        cy = sum(coords[v][1] for v in z) / 3
        eta2.append(area * area * f(cx, cy) ** 2)  # h_K^2 ||f||^2 with h_K^2 = |K|
        hk.append(math.sqrt(area))
        grads.append(gradient(coords, z, U))
        for r in range(3):
            owner.setdefault(_edge(z[r], z[(r + 1) % 3]), []).append(t)
    for (a, b), ts in owner.items():
        if len(ts) != 2:
            continue  # a boundary edge: no jump term for Dirichlet data
        (xa, ya), (xb, yb) = coords[a], coords[b]
        length = math.hypot(xb - xa, yb - ya)
        nx, ny = (yb - ya) / length, (xa - xb) / length
        g0, g1 = grads[ts[0]], grads[ts[1]]
        jump = (g0[0] - g1[0]) * nx + (g0[1] - g1[1]) * ny
        term = length * jump * jump  # ||J||_E^2, J constant on E
        eta2[ts[0]] += hk[ts[0]] * term  # h_K ||J||_E^2 on both sides of E
        eta2[ts[1]] += hk[ts[1]] * term
    return eta2


def dorfler_mark(eta2, theta):
    """Return a set of minimal size with sum of eta2 over it >= theta times the total."""
    order = sorted(range(len(eta2)), key=lambda t: -eta2[t])
    goal = theta * sum(eta2)
    marked, acc = [], 0.0
    for t in order:
        if acc >= goal and marked:
            break
        marked.append(t)
        acc += eta2[t]
    return marked


def afem(mesh, f, g, theta=0.5, max_nodes=400, max_steps=40):
    """Run SOLVE, ESTIMATE, MARK, REFINE until the mesh has more than max_nodes nodes.

    Return a list of (coords, elements, boundary, U, eta2), one entry per step.
    theta = 1 marks every element, which is uniform bisection.
    """
    coords, elements, boundary = mesh
    history = []
    for _ in range(max_steps):  # @line L1
        U = solve_p1(coords, elements, boundary, f, g)  # @line L2
        eta2 = estimate(coords, elements, U, f)  # @line L3
        history.append((coords, elements, boundary, U, eta2))
        if len(coords) > max_nodes:  # @line L4
            break  # @line L5
        marked = dorfler_mark(eta2, theta) if theta < 1 else list(range(len(elements)))  # @line L6
        coords, elements, boundary = refine_nvb(coords, elements, boundary, marked)  # @line L7
    return history  # @line L8


# Points and weights of the 7-point rule of degree 5 on the reference triangle (Radon).
_A1, _B1 = 0.059715871789770, 0.470142064105115
_A2, _B2 = 0.797426985353087, 0.101286507323456
_W0, _W1, _W2 = 0.225, 0.132394152788506, 0.125939180544827
QUAD7 = [((1 / 3, 1 / 3, 1 / 3), _W0),
         ((_A1, _B1, _B1), _W1), ((_B1, _A1, _B1), _W1), ((_B1, _B1, _A1), _W1),
         ((_A2, _B2, _B2), _W2), ((_B2, _A2, _B2), _W2), ((_B2, _B2, _A2), _W2)]


def energy_error(coords, elements, U, grad_u):
    """Return |u - u_h|_1, the H1 seminorm error, by the 7-point rule on each element.

    The rule has no point on the boundary of the element, so it can be used
    when grad_u is singular at a vertex. Near such a vertex the result is a
    quadrature approximation.
    """
    total = 0.0
    for z in elements:
        area, _ = _geometry(coords, z)
        gx, gy = gradient(coords, z, U)
        for lam, w in QUAD7:
            x = sum(lam[r] * coords[z[r]][0] for r in range(3))
            y = sum(lam[r] * coords[z[r]][1] for r in range(3))
            ux, uy = grad_u(x, y)
            total += w * area * ((ux - gx) ** 2 + (uy - gy) ** 2)
    return math.sqrt(total)


def l_shape_exact(x, y):
    """u = r^(2/3) sin(2 phi / 3) with phi in [0, 3 pi / 2]; harmonic, zero on the reentrant edges."""
    r = math.hypot(x, y)
    if r == 0.0:
        return 0.0
    phi = math.atan2(y, x)
    if phi < 0:
        phi += 2 * math.pi
    return r ** (2 / 3) * math.sin(2 * phi / 3)


def l_shape_gradient(x, y):
    """Gradient of l_shape_exact (not defined at the origin)."""
    r = math.hypot(x, y)
    phi = math.atan2(y, x)
    if phi < 0:
        phi += 2 * math.pi
    c = (2 / 3) * r ** (-1 / 3)
    ur, uphi = c * math.sin(2 * phi / 3), c * math.cos(2 * phi / 3)
    return (ur * math.cos(phi) - uphi * math.sin(phi), ur * math.sin(phi) + uphi * math.cos(phi))
