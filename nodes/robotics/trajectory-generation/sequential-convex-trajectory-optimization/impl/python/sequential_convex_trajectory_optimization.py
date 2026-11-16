# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequential-convex-trajectory-optimization/. The authors are listed in prov/7KE72T.jsonl.
"""Sequential convex trajectory optimization with an l1 penalty and a trust region.

A point robot moves in the plane from q_0 to q_(n+1) through n free
waypoints x_1, ..., x_n. Each constraint is a signed distance function
sd(p) that must stay at least d_safe at every waypoint. The merit is

    phi(x) = f(x) + mu * sum_t sum_j max(0, d_safe - sd_j(x_t)),
    f(x)   = sum_(t=0..n) |x_(t+1) - x_t|^2.

At the current x the signed distances are linearized, sd_j(x_t + d_t) ~
sd_j(x_t) + g_jt . d_t, and the convex model

    phi_hat(d) = f(x + d) + mu * sum max(0, d_safe - sd_j(x_t) - g_jt . d_t)

is minimized subject to |d|_inf <= Delta. The step is accepted when the
true decrease is at least a fraction c of the decrease predicted by the
model; the trust region Delta grows after an accepted step and shrinks
after a rejected one. When no more progress is possible, mu grows until the
constraints hold.

The convex subproblem is a quadratic program with one slack variable per
linearized constraint. It is solved by a log-barrier method with Newton
steps. The slacks are eliminated from each Newton system, which leaves a
block tridiagonal system with 2 x 2 blocks, solved in O(n) by block
elimination. Everything uses the standard library only.
"""

import math


# ---------- signed distance functions: each returns (value, gradient) ----------

def disc_sd(ox, oy, r):
    """Signed distance to a disc obstacle; convex in p. Gradient 0 at the center."""
    def sd(p):
        dx, dy = p[0] - ox, p[1] - oy
        rho = math.hypot(dx, dy)
        if rho == 0.0:
            return -r, (0.0, 0.0)
        return rho - r, (dx / rho, dy / rho)
    return sd


def inside_circle_sd(ox, oy, big_r):
    """Signed distance to the boundary of an allowed circular region; concave in p."""
    def sd(p):
        dx, dy = p[0] - ox, p[1] - oy
        rho = math.hypot(dx, dy)
        if rho == 0.0:
            return big_r, (0.0, 0.0)
        return big_r - rho, (-dx / rho, -dy / rho)
    return sd


# ---------- objective and merit ----------

def straight_line(q0, q1, n):
    return [[q0[d] + (q1[d] - q0[d]) * t / (n + 1) for d in range(2)] for t in range(1, n + 1)]


def smoothness(x, q0, q1):
    pts = [q0] + x + [q1]
    return sum((pts[t + 1][0] - pts[t][0]) ** 2 + (pts[t + 1][1] - pts[t][1]) ** 2 for t in range(len(pts) - 1))


def violation(x, sds, d_safe):
    return sum(max(0.0, d_safe - sd(p)[0]) for p in x for sd in sds)


def max_violation(x, sds, d_safe):
    return max([0.0] + [d_safe - sd(p)[0] for p in x for sd in sds])


def merit(x, q0, q1, sds, d_safe, mu):
    return smoothness(x, q0, q1) + mu * violation(x, sds, d_safe)


def add(x, d):
    return [[x[t][0] + d[2 * t], x[t][1] + d[2 * t + 1]] for t in range(len(x))]


# ---------- 2 x 2 helpers and the block tridiagonal solve ----------

def inv2(m):
    a, b, c, d = m[0][0], m[0][1], m[1][0], m[1][1]
    det = a * d - b * c
    return [[d / det, -b / det], [-c / det, a / det]]


def mul2(m, v):
    return [m[0][0] * v[0] + m[0][1] * v[1], m[1][0] * v[0] + m[1][1] * v[1]]


def block_tridiag_solve(diag, off, rhs):
    """Solve the system with 2 x 2 diagonal blocks diag[t] and off-diagonal blocks off * I."""
    n = len(diag)
    dprime, rprime = [None] * n, [None] * n
    dprime[0], rprime[0] = [row[:] for row in diag[0]], rhs[0][:]
    for t in range(1, n):
        iv = inv2(dprime[t - 1])
        dprime[t] = [[diag[t][i][j] - off * off * iv[i][j] for j in range(2)] for i in range(2)]
        w = mul2(iv, rprime[t - 1])
        rprime[t] = [rhs[t][i] - off * w[i] for i in range(2)]
    x = [None] * n
    x[n - 1] = mul2(inv2(dprime[n - 1]), rprime[n - 1])
    for t in range(n - 2, -1, -1):
        x[t] = mul2(inv2(dprime[t]), [rprime[t][i] - off * x[t + 1][i] for i in range(2)])
    return x


# ---------- the convex subproblem ----------

def model_value(x, q0, q1, lin, d_safe, mu, d):
    """phi_hat(d): exact smoothness plus the l1 penalty of the linearized constraints."""
    pen = sum(max(0.0, d_safe - v - g[0] * d[2 * t] - g[1] * d[2 * t + 1]) for t, v, g in lin)
    return smoothness(add(x, d), q0, q1) + mu * pen


def solve_subproblem(x, q0, q1, lin, d_safe, mu, delta, gap=1e-8):
    """Minimize phi_hat(d) subject to |d|_inf <= delta by a log-barrier method.

    Variables: d (2n entries) and s (one slack per linearized constraint k).
    Minimize f(x + d) + mu sum s subject to s_k >= 0,
    s_k + g_k . d_t - b_k >= 0 with b_k = d_safe - v_k, and -delta <= d <= delta.
    """
    n = len(x)
    nd, ns = 2 * n, len(lin)
    pts = [q0] + x + [q1]
    gf = [0.0] * nd  # gradient of f at d = 0; the Hessian of f is 2 (L kron I2)
    for t in range(n):
        for c in range(2):
            gf[2 * t + c] = 2.0 * (2.0 * pts[t + 1][c] - pts[t][c] - pts[t + 2][c])
    b = [d_safe - v for _, v, _ in lin]
    d = [0.0] * nd
    s = [max(0.0, bk) + 1.0 for bk in b]

    def hf(d, i, t):
        return 4.0 * d[i] - (2.0 * d[i - 2] if t > 0 else 0.0) - (2.0 * d[i + 2] if t < n - 1 else 0.0)

    def barrier(d, s, tau):
        q = sum(gf[i] * d[i] for i in range(nd))
        q += 0.5 * sum(d[2 * t + c] * hf(d, 2 * t + c, t) for t in range(n) for c in range(2))
        val = tau * (q + mu * sum(s))
        for k, (t, _, g) in enumerate(lin):
            lc = s[k] + g[0] * d[2 * t] + g[1] * d[2 * t + 1] - b[k]
            if s[k] <= 0.0 or lc <= 0.0:
                return math.inf
            val -= math.log(s[k]) + math.log(lc)
        for i in range(nd):
            if d[i] >= delta or d[i] <= -delta:
                return math.inf
            val -= math.log(delta - d[i]) + math.log(delta + d[i])
        return val

    m_c = 2 * ns + 2 * nd
    tau = 1.0
    while True:
        for _ in range(200):
            # gradient and Hessian of the barrier function, blocks per waypoint
            gd = [tau * (gf[i] + hf(d, i, i // 2)) for i in range(nd)]
            diag = [[[4.0 * tau, 0.0], [0.0, 4.0 * tau]] for _ in range(n)]
            for i in range(nd):
                v1, v2 = delta - d[i], delta + d[i]
                gd[i] += 1.0 / v1 - 1.0 / v2
                diag[i // 2][i % 2][i % 2] += 1.0 / (v1 * v1) + 1.0 / (v2 * v2)
            gs, hs, cross = [0.0] * ns, [0.0] * ns, [None] * ns
            for k, (t, _, g) in enumerate(lin):
                lc = s[k] + g[0] * d[2 * t] + g[1] * d[2 * t + 1] - b[k]
                w = 1.0 / (lc * lc)
                gs[k] = tau * mu - 1.0 / s[k] - 1.0 / lc
                gd[2 * t] -= g[0] / lc
                gd[2 * t + 1] -= g[1] / lc
                hs[k] = 1.0 / (s[k] * s[k]) + w
                cross[k] = [g[0] * w, g[1] * w]
                for p in range(2):
                    for q in range(2):
                        diag[t][p][q] += g[p] * g[q] * w
            # eliminate the slacks: Schur complement on the d blocks
            rhs = [[-gd[2 * t], -gd[2 * t + 1]] for t in range(n)]
            for k, (t, _, g) in enumerate(lin):
                cr = cross[k]
                for p in range(2):
                    rhs[t][p] -= cr[p] * (-gs[k]) / hs[k]
                    for q in range(2):
                        diag[t][p][q] -= cr[p] * cr[q] / hs[k]
            stepd_blocks = block_tridiag_solve(diag, -2.0 * tau, rhs)
            stepd = [stepd_blocks[i // 2][i % 2] for i in range(nd)]
            steps = [(-gs[k] - cross[k][0] * stepd[2 * t] - cross[k][1] * stepd[2 * t + 1]) / hs[k]
                     for k, (t, _, _) in enumerate(lin)]
            dec = -(sum(gd[i] * stepd[i] for i in range(nd)) + sum(gs[k] * steps[k] for k in range(ns)))
            if dec / 2.0 <= 1e-10:
                break
            alpha, cur = 1.0, barrier(d, s, tau)
            while alpha > 1e-12:
                nd_ = [d[i] + alpha * stepd[i] for i in range(nd)]
                ns_ = [s[k] + alpha * steps[k] for k in range(ns)]
                if barrier(nd_, ns_, tau) <= cur - 0.25 * alpha * dec:
                    d, s = nd_, ns_
                    break
                alpha *= 0.5
            else:
                break
        if m_c / tau <= gap:
            break
        tau *= 20.0
    return d


# ---------- the trust region loop ----------

def scp(q0, q1, n, sds, d_safe=0.1, mu0=10.0, delta0=0.1, c=0.1, tau_plus=1.5, tau_minus=0.5,
        delta_min=1e-4, xtol=1e-4, ctol=1e-4, k_mu=10.0, outer=5, x0=None, log=None):
    """Run the method. Returns (x, info) with info = dict(mu, accepted, rejected, merits)."""
    x = straight_line(q0, q1, n) if x0 is None else [list(p) for p in x0]
    mu, delta = mu0, delta0  # @line L1
    accepted = rejected = 0
    merits = []
    for _ in range(outer):  # @line L2
        while True:  # @line L3
            lin = []
            for t in range(n):
                for sd in sds:
                    v, g = sd(x[t])  # @line L4
                    lin.append((t, v, g))
            d = solve_subproblem(x, q0, q1, lin, d_safe, mu, delta)  # @line L5
            cur = merit(x, q0, q1, sds, d_safe, mu)
            pred = cur - model_value(x, q0, q1, lin, d_safe, mu, d)  # @line L6
            if pred <= xtol:
                break
            new = add(x, d)
            ratio = (cur - merit(new, q0, q1, sds, d_safe, mu)) / pred  # @line L7
            if log is not None:
                log.append((mu, delta, pred, ratio))
            if ratio >= c:  # @line L8
                x, delta = new, min(tau_plus * delta, 1.0)
                accepted += 1
                merits.append((mu, merit(x, q0, q1, sds, d_safe, mu)))
            else:
                delta *= tau_minus
                rejected += 1
            if delta < delta_min:  # @line L9
                break
        if max_violation(x, sds, d_safe) <= ctol:  # @line L10
            return x, dict(mu=mu, accepted=accepted, rejected=rejected, merits=merits)
        mu *= k_mu  # @line L11
    return x, dict(mu=mu, accepted=accepted, rejected=rejected, merits=merits)  # @line L12


def min_clearance(x, sds):
    return min(sd(p)[0] for p in x for sd in sds)


def path_length(x, q0, q1):
    pts = [q0] + x + [q1]
    return sum(math.hypot(pts[t + 1][0] - pts[t][0], pts[t + 1][1] - pts[t][1]) for t in range(len(pts) - 1))
