# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geometric-programming-power-control/. The authors are listed in prov/BD2KKJ.jsonl.

"""Power control by geometric programming, with a small teaching GP solver.

There are K links. g[i][j] >= 0 is the power gain from transmitter j to
receiver i, noise[i] > 0 is the noise at receiver i, and pmax[i] > 0 is the
power limit of link i. The SINR of link i is

    SINR_i(p) = g[i][i] p[i] / N_i(p),  N_i(p) = sum over j != i of g[i][j] p[j] + noise[i].

A monomial is c * prod_k x_k^(a_k) with c > 0 and real a_k; a posynomial is a
sum of monomials. With y = log x, the log of a posynomial is a log-sum-exp of
affine functions of y, which is convex. A posynomial is stored as a list of
terms (b, a) with b = log c, so its log is log sum_m exp(b_m + a_m . y).

gp_solve minimizes a sum of logs of posynomials subject to log P(y) <= 0 for
each constraint posynomial P, by the barrier method with damped Newton steps.
It is meant to be read, not to be fast: K is small and the linear algebra is
plain Gaussian elimination.
"""

import math

Posy = list[tuple[float, list[float]]]


def monomial(c: float, a: list[float]) -> Posy:
    """The posynomial with the single term c * prod x_k^(a_k)."""
    return [(math.log(c), list(a))]


def lse(posy: Posy, y: list[float]) -> tuple[float, list[float], list[list[float]]]:
    """The value, gradient and Hessian of f(y) = log sum_m exp(b_m + a_m . y)."""
    n = len(y)
    z = [b + sum(ak * yk for ak, yk in zip(a, y)) for b, a in posy]
    zmax = max(z)
    w = [math.exp(v - zmax) for v in z]
    s = sum(w)
    w = [v / s for v in w]
    f = zmax + math.log(s)
    grad = [sum(w[m] * posy[m][1][k] for m in range(len(posy))) for k in range(n)]
    hess = [[0.0] * n for _ in range(n)]
    for m, (_, a) in enumerate(posy):
        for r in range(n):
            if a[r]:
                wa = w[m] * a[r]
                row = hess[r]
                for c in range(n):
                    row[c] += wa * a[c]
    for r in range(n):
        for c in range(n):
            hess[r][c] -= grad[r] * grad[c]
    return f, grad, hess


def solve(a: list[list[float]], b: list[float]) -> list[float]:
    """Solve a x = b by Gaussian elimination with partial pivoting."""
    n = len(a)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[piv][c] == 0.0:
            raise ZeroDivisionError("singular Newton system")
        m[c], m[piv] = m[piv], m[c]
        for r in range(c + 1, n):
            fac = m[r][c] / m[c][c]
            if fac:
                for k in range(c, n + 1):
                    m[r][k] -= fac * m[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (m[r][n] - sum(m[r][k] * x[k] for k in range(r + 1, n))) / m[r][r]
    return x


def gp_value(objective: list[Posy], y: list[float]) -> float:
    """The objective sum of log P_m(y)."""
    return sum(lse(p, y)[0] for p in objective)


def gp_solve(
    objective: list[Posy],
    constraints: list[Posy],
    y0: list[float],
    gap: float = 1e-10,
    mu: float = 20.0,
) -> list[float]:
    """Minimize sum_m log P_m(y) subject to log Q_i(y) <= 0, from a strictly feasible y0.

    This is the barrier method: for t = 1, mu, mu^2, ..., minimize
    f0(y) - (1/t) sum_i log(-f_i(y)) by Newton's method, and stop when the
    duality gap bound len(constraints) / t is below gap. (This is the usual
    t f0 - sum log(-f_i) divided by t, which keeps the numbers near 1.)
    """
    n = len(y0)
    y = list(y0)
    if any(lse(q, y)[0] >= 0.0 for q in constraints):
        raise ValueError("the start is not strictly feasible")

    def parts(y: list[float], t: float, hess_too: bool):
        val = 0.0
        grad = [0.0] * n
        hess = [[0.0] * n for _ in range(n)]
        for p in objective:
            f, g, h = lse(p, y)
            val += f
            for r in range(n):
                grad[r] += g[r]
                if hess_too:
                    for c in range(n):
                        hess[r][c] += h[r][c]
        w = 1.0 / t
        for q in constraints:
            f, g, h = lse(q, y)
            if f >= 0.0:
                return math.inf, None, None
            val -= w * math.log(-f)
            for r in range(n):
                grad[r] += w * g[r] / -f
                if hess_too:
                    for c in range(n):
                        hess[r][c] += w * (h[r][c] / -f + g[r] * g[c] / (f * f))
        return val, grad, hess

    t = 1.0
    while True:
        for _ in range(100):
            val, grad, hess = parts(y, t, True)
            for r in range(n):
                hess[r][r] += 1e-14 * (1.0 + abs(hess[r][r]))
            step = solve(hess, [-v for v in grad])
            dec = -sum(a * b for a, b in zip(grad, step))
            if dec / 2.0 <= 1e-13:
                break
            s = 1.0
            cand = None
            while s >= 1e-6:
                trial = [a + s * d for a, d in zip(y, step)]
                v2, _, _ = parts(trial, t, False)
                if v2 <= val - 0.25 * s * dec:
                    cand = trial
                    break
                s *= 0.5
            if cand is None:
                break  # rounding stops the progress; y is already centered to working precision
            y = cand
        if len(constraints) / t < gap:
            return y
        t *= mu


def interference_posy(g: list[list[float]], noise: list[float], i: int, n: int) -> Posy:
    """N_i(p) = sum over j != i of g[i][j] p_j + noise_i, as a posynomial in n variables."""
    k = len(g)
    terms = monomial(noise[i], [0.0] * n)
    for j in range(k):
        if j != i and g[i][j] > 0.0:
            a = [0.0] * n
            a[j] = 1.0
            terms += monomial(g[i][j], a)
    return terms


def scale_posy(posy: Posy, c: float, a: list[float]) -> Posy:
    """The posynomial posy(x) * c * prod x_k^(a_k)."""
    lc = math.log(c)
    return [(b + lc, [u + v for u, v in zip(e, a)]) for b, e in posy]


def sinr(g: list[list[float]], noise: list[float], p: list[float]) -> list[float]:
    k = len(p)
    return [g[i][i] * p[i] / (sum(g[i][j] * p[j] for j in range(k) if j != i) + noise[i]) for i in range(k)]


def sum_rate(g: list[list[float]], noise: list[float], p: list[float]) -> float:
    """The sum of log2(1 + SINR_i) in bits per channel use."""
    return sum(math.log2(1.0 + s) for s in sinr(g, noise, p))


def least_powers(g: list[list[float]], gamma: list[float], noise: list[float]) -> list[float] | None:
    """The least powers that meet the targets gamma (the Foschini-Miljanic fixed point), or None."""
    k = len(g)
    a = [[(1.0 if i == j else -gamma[i] * g[i][j] / g[i][i]) for j in range(k)] for i in range(k)]
    u = [gamma[i] * noise[i] / g[i][i] for i in range(k)]
    try:
        p = solve(a, u)
    except ZeroDivisionError:
        return None
    return p if min(p) > 0.0 else None


def target_constraints(g, noise, gamma, pmax, n):
    """The posynomial constraints gamma_i N_i(p) / (g_ii p_i) <= 1 and p_i / pmax_i <= 1."""
    k = len(g)
    cons = []
    for i in range(k):
        a = [0.0] * n
        a[i] = -1.0
        cons.append(scale_posy(interference_posy(g, noise, i, n), gamma[i] / g[i][i], a))
        b = [0.0] * n
        b[i] = 1.0
        cons.append(monomial(1.0 / pmax[i], b))
    return cons


def strict_start(g, noise, gamma, pmax) -> list[float]:
    """A strictly feasible power vector for the targets gamma and the limits pmax."""
    p = least_powers(g, [1.01 * v for v in gamma], noise)
    if p is None or any(a >= b for a, b in zip(p, pmax)):
        raise ValueError("the targets cannot be met within the power limits")
    return p


def min_total_power(g, noise, gamma, pmax) -> list[float]:
    """Minimize sum_i p_i subject to SINR_i >= gamma_i and p <= pmax, as a GP."""
    k = len(g)
    obj = [[term for i in range(k) for term in monomial(1.0, [1.0 if j == i else 0.0 for j in range(k)])]]
    cons = target_constraints(g, noise, gamma, pmax, k)
    y = gp_solve(obj, cons, [math.log(v) for v in strict_start(g, noise, gamma, pmax)])
    return [math.exp(v) for v in y]


def max_min_sinr(g, noise, pmax) -> tuple[float, list[float]]:
    """Maximize t subject to SINR_i >= t and p <= pmax. Variables (p, t); minimize 1/t."""
    k = len(g)
    n = k + 1
    cons = []
    for i in range(k):
        a = [0.0] * n
        a[i] = -1.0
        a[k] = 1.0
        cons.append(scale_posy(interference_posy(g, noise, i, n), 1.0 / g[i][i], a))
        b = [0.0] * n
        b[i] = 1.0
        cons.append(monomial(1.0 / pmax[i], b))
    p0 = [0.5 * v for v in pmax]
    t0 = 0.5 * min(sinr(g, noise, p0))
    obj = [monomial(1.0, [0.0] * k + [-1.0])]
    y = gp_solve(obj, cons, [math.log(v) for v in p0] + [math.log(t0)])
    return math.exp(y[k]), [math.exp(v) for v in y[:k]]


def high_sinr_rate(g, noise, pmax, gmin) -> list[float]:
    """Maximize sum_i log SINR_i subject to SINR_i >= gmin_i and p <= pmax.

    log(1 + SINR) ~ log SINR at high SINR, and minimizing sum_i log(N_i(p) / (g_ii p_i))
    is a GP objective (a sum of logs of posynomials).
    """
    k = len(g)
    obj = []
    for i in range(k):
        a = [0.0] * k
        a[i] = -1.0
        obj.append(scale_posy(interference_posy(g, noise, i, k), 1.0 / g[i][i], a))
    cons = target_constraints(g, noise, gmin, pmax, k)
    y = gp_solve(obj, cons, [math.log(v) for v in strict_start(g, noise, gmin, pmax)])
    return [math.exp(v) for v in y]


def condense(g, noise, i, p, n):
    """The monomial that matches D_i(q) = sum_j g[i][j] q_j + noise_i at q = p, with D_i >= it everywhere.

    With the terms u_m of D_i(p) and alpha_m = u_m / D_i(p), the arithmetic-geometric
    mean inequality gives D_i(q) >= prod_m (u_m(q) / alpha_m)^alpha_m.
    """
    k = len(g)
    d = sum(g[i][j] * p[j] for j in range(k)) + noise[i]
    alpha0 = noise[i] / d
    logc = alpha0 * math.log(noise[i] / alpha0)
    a = [0.0] * n
    for j in range(k):
        if g[i][j] > 0.0:
            al = g[i][j] * p[j] / d
            logc += al * math.log(g[i][j] / al)
            a[j] = al
    return logc, a


def sca_sum_rate(g, noise, pmax, gmin, p0=None, iters=50, tol=1e-9) -> tuple[list[float], list[float]]:
    """Successive GP approximation for max sum_i log2(1 + SINR_i), SINR_i >= gmin_i, p <= pmax.

    1 / (1 + SINR_i) = N_i(p) / D_i(p) with D_i = N_i + g_ii p_i. Each round replaces D_i by
    its monomial lower bound at the current p, which gives an upper bound on the objective
    sum_i log(N_i / D_i) that touches it at p, and minimizes that bound as a GP.
    Return the final powers and the sum rate after each round (the first entry is for p0).
    """
    k = len(g)
    p = list(p0) if p0 is not None else strict_start(g, noise, gmin, pmax)  # @line L1
    cons = target_constraints(g, noise, gmin, pmax, k)
    rates = [sum_rate(g, noise, p)]
    for _ in range(iters):  # @line L2
        obj = []
        for i in range(k):
            logc, a = condense(g, noise, i, p, k)  # @line L3
            neg = [-v for v in a]
            obj.append(scale_posy(interference_posy(g, noise, i, k), math.exp(-logc), neg))  # @line L4
        y = gp_solve(obj, cons, [math.log(v) for v in p])  # @line L5
        p = [math.exp(v) for v in y]
        rates.append(sum_rate(g, noise, p))
        if rates[-1] - rates[-2] <= tol:  # @line L6
            break
    return p, rates  # @line L7
