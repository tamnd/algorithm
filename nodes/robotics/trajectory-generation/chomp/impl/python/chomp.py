# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chomp/. The authors are listed in prov/ZMPYZV.jsonl.
"""CHOMP: covariant gradient descent on a waypoint trajectory.

A point robot moves in the plane from q_0 to q_(n+1) through n free
waypoints q_1, ..., q_n, spaced dt apart in time. Obstacles are discs
(ox, oy, r). The objective is

    U(xi) = F_obs(xi) + lam * F_smooth(xi),
    F_smooth = 1/2 sum_(t=0..n) |(q_(t+1) - q_t) / dt|^2 = 1/2 xi^T A xi + xi^T b + c,
    F_obs = sum_t sum_j c(D_j(q_t)),

where D_j is the signed distance to disc j and c is the CHOMP cost

    c(D) = -D + eps/2           if D < 0,
           (D - eps)^2 / (2 eps) if 0 <= D <= eps,
           0                    otherwise.

The update is xi <- xi - (1/eta) A^(-1) grad U(xi). A is tridiagonal with
2/dt^2 on the diagonal and -1/dt^2 next to it, the same for each coordinate,
so A^(-1) g costs O(n) per coordinate (Thomas algorithm).

The paper weights the obstacle cost by the workspace speed and projects its
gradient across the direction of motion. This code uses the plain sum over
the waypoints, which keeps the gradient exact; see the page.
"""

import math


def straight_line(q0, q1, n):
    """n waypoints equally spaced on the segment from q0 to q1 (ends excluded)."""
    return [[q0[d] + (q1[d] - q0[d]) * t / (n + 1) for d in range(2)] for t in range(1, n + 1)]


def _full(xi, q0, q1):
    return [list(q0)] + [list(p) for p in xi] + [list(q1)]


def smoothness(xi, q0, q1, dt):
    pts = _full(xi, q0, q1)
    s = 0.0
    for t in range(len(pts) - 1):
        for d in range(2):
            v = (pts[t + 1][d] - pts[t][d]) / dt
            s += 0.5 * v * v
    return s


def smoothness_grad(xi, q0, q1, dt):
    """A xi + b: the gradient of F_smooth."""
    pts = _full(xi, q0, q1)
    return [[(2.0 * pts[t][d] - pts[t - 1][d] - pts[t + 1][d]) / (dt * dt) for d in range(2)]
            for t in range(1, len(pts) - 1)]


def disc_distance(p, disc):
    """Signed distance to a disc and its gradient (zero vector at the center)."""
    ox, oy, r = disc
    dx, dy = p[0] - ox, p[1] - oy
    rho = math.hypot(dx, dy)
    if rho == 0.0:
        return -r, (0.0, 0.0)
    return rho - r, (dx / rho, dy / rho)


def cost_c(dist, eps):
    if dist < 0.0:
        return -dist + 0.5 * eps
    if dist <= eps:
        return (dist - eps) ** 2 / (2.0 * eps)
    return 0.0


def cost_dc(dist, eps):
    if dist < 0.0:
        return -1.0
    if dist <= eps:
        return (dist - eps) / eps
    return 0.0


def obstacle_cost(xi, discs, eps):
    return sum(cost_c(disc_distance(p, o)[0], eps) for p in xi for o in discs)


def obstacle_grad(xi, discs, eps):
    g = []
    for p in xi:
        gx = gy = 0.0
        for o in discs:
            dist, (ux, uy) = disc_distance(p, o)
            w = cost_dc(dist, eps)
            gx += w * ux
            gy += w * uy
        g.append([gx, gy])
    return g


def objective(xi, q0, q1, dt, discs, lam, eps):
    return obstacle_cost(xi, discs, eps) + lam * smoothness(xi, q0, q1, dt)


def solve_a(rhs, dt):
    """Solve A x = rhs for one coordinate, A = tridiag(-1, 2, -1) / dt^2 (Thomas)."""
    n = len(rhs)
    c = [0.0] * n
    d = [0.0] * n
    beta = 2.0
    c[0] = -1.0 / beta
    d[0] = rhs[0] * dt * dt / beta
    for i in range(1, n):
        beta = 2.0 + c[i - 1]
        c[i] = -1.0 / beta
        d[i] = (rhs[i] * dt * dt + d[i - 1]) / beta
    x = [0.0] * n
    x[n - 1] = d[n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = d[i] - c[i] * x[i + 1]
    return x


def safe_eta(n, dt, lam, eps, n_discs):
    """A step parameter for which every step decreases U (see the proof).

    The obstacle term has a gradient that is Lipschitz with constant
    n_discs / eps up to a concave part; the smallest eigenvalue of A is
    4 sin^2(pi / (2 (n + 1))) / dt^2.
    """
    mu = 4.0 * math.sin(math.pi / (2.0 * (n + 1))) ** 2 / (dt * dt)
    return lam + n_discs / (eps * mu)


def chomp(q0, q1, n, discs, lam=0.02, eps=0.2, eta=None, iters=3000, tol=1e-6, xi0=None):
    """Run CHOMP. Returns (xi, history of U, number of iterations done)."""
    dt = 1.0 / (n + 1)
    if eta is None:
        eta = safe_eta(n, dt, lam, eps, len(discs))
    xi = straight_line(q0, q1, n) if xi0 is None else [list(p) for p in xi0]  # @line L1
    hist = [objective(xi, q0, q1, dt, discs, lam, eps)]
    for it in range(iters):  # @line L2
        g = obstacle_grad(xi, discs, eps)  # @line L3
        gs = smoothness_grad(xi, q0, q1, dt)
        g = [[g[t][d] + lam * gs[t][d] for d in range(2)] for t in range(n)]  # @line L4
        if math.sqrt(sum(v * v for row in g for v in row)) <= tol:  # @line L5
            return xi, hist, it
        delta = [solve_a([g[t][d] for t in range(n)], dt) for d in range(2)]  # @line L6
        xi = [[xi[t][d] - delta[d][t] / eta for d in range(2)] for t in range(n)]  # @line L7
        hist.append(objective(xi, q0, q1, dt, discs, lam, eps))
    return xi, hist, iters  # @line L8


def min_clearance(xi, discs):
    return min(disc_distance(p, o)[0] for p in xi for o in discs)


def path_length(xi, q0, q1):
    pts = _full(xi, q0, q1)
    return sum(math.dist(pts[t], pts[t + 1]) for t in range(len(pts) - 1))
