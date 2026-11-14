# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-noise-analysis/. The authors are listed in prov/Y2MTGG.jsonl.
"""Oscillator phase noise with the perturbation projection vector (PPV).

The oscillator is a state equation dx/dt = F(x) + B xi(t), where xi is a
vector of independent white noises with unit two-sided spectral density
(E xi(t) xi(s)^T = I delta(t - s)). A circuit with a nonsingular capacitance
matrix C reaches this form as dx/dt = -C^-1 f(x) plus the noise currents
scaled by C^-1.

The noiseless oscillator has a stable periodic orbit x_s(t) of period T. The
PPV v(t) is the periodic solution of the adjoint equation dv/dt = -A(t)^T v
with v(t)^T dx_s/dt = 1. Demir, Mehrotra and Roychowdhury showed that noise
makes the phase drift as a random walk, x(t) ~ x_s(t + alpha(t)), with
Var alpha(t) ~ c t and c = (1/T) int_0^T v^T B B^T v dt.
"""

import math

import sim3dense

BOLTZMANN = 1.380649e-23


class NoConvergence(RuntimeError):
    pass


class Oscillator:
    """dx/dt = F(x) + B xi with the Jacobian A(x) = dF/dx."""

    def __init__(self, n, F, A, B):
        self.n, self.F, self.A, self.B = n, F, A, B


def lc_oscillator(l, c, r, gm, v0, temperature=300.0, noise_scale=1.0):
    """LC tank with loss r and a negative conductance i = gm v0 tanh(v / v0).

    States (v, i_L). The tanh law models a cross-coupled differential pair;
    its gm and v0 are fitted to the transistor pair. The noise is the thermal
    current of r, two-sided density 2kT/r, times noise_scale.
    """

    def F(x):
        v, i = x
        return [(-v / r - i + gm * v0 * math.tanh(v / v0)) / c, v / l]

    def A(x):
        s = 1.0 / math.cosh(x[0] / v0)
        return [[(-1.0 / r + gm * s * s) / c, -1.0 / c], [1.0 / l, 0.0]]

    amp = noise_scale * math.sqrt(2 * BOLTZMANN * temperature / r) / c
    return Oscillator(2, F, A, [[amp], [0.0]])


def hopf_oscillator(mu, omega, sigma):
    """Hopf normal form with white noise sigma on both states; the orbit has radius sqrt(mu)."""

    def F(x):
        a, b = x
        r2 = a * a + b * b
        return [mu * a - omega * b - r2 * a, omega * a + mu * b - r2 * b]

    def A(x):
        a, b = x
        r2 = a * a + b * b
        return [[mu - r2 - 2 * a * a, -omega - 2 * a * b], [omega - 2 * a * b, mu - r2 - 2 * b * b]]

    return Oscillator(2, F, A, [[sigma, 0.0], [0.0, sigma]])


def _add(x, y, s):
    return [a + s * b for a, b in zip(x, y)]


def rk4_step(osc, x, h):
    """One classical Runge-Kutta step and its exact Jacobian d x_new / d x."""
    n = osc.n
    I = sim3dense.identity(n, 1.0)
    k1, A1 = osc.F(x), osc.A(x)
    d1 = A1
    x2 = _add(x, k1, h / 2)
    k2, A2 = osc.F(x2), osc.A(x2)
    d2 = sim3dense.matmul(A2, [[I[i][j] + h / 2 * d1[i][j] for j in range(n)] for i in range(n)])
    x3 = _add(x, k2, h / 2)
    k3, A3 = osc.F(x3), osc.A(x3)
    d3 = sim3dense.matmul(A3, [[I[i][j] + h / 2 * d2[i][j] for j in range(n)] for i in range(n)])
    x4 = _add(x, k3, h)
    k4, A4 = osc.F(x4), osc.A(x4)
    d4 = sim3dense.matmul(A4, [[I[i][j] + h * d3[i][j] for j in range(n)] for i in range(n)])
    xn = [x[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(n)]
    P = [[I[i][j] + h / 6 * (d1[i][j] + 2 * d2[i][j] + 2 * d3[i][j] + d4[i][j]) for j in range(n)] for i in range(n)]
    return xn, P


def orbit(osc, x0, T, S):
    """S RK4 steps over [0, T]; returns the states x_0..x_S and the step Jacobians."""
    h = T / S
    xs, mats = [list(x0)], []
    for _ in range(S):
        x, P = rk4_step(osc, xs[-1], h)
        xs.append(x)
        mats.append(P)
    return xs, mats


def limit_cycle(osc, x0, T0, S, p=1, value=0.0, tol=1e-12, max_iter=50):
    """Shooting Newton for an autonomous orbit with the phase condition x_0[p] = value.

    The unknowns are x_0 and T. The derivative of x_S with respect to T is
    taken as F(x_S), the derivative of the exact flow; the residual is exact,
    so the iteration converges to the orbit of the discrete map.
    Returns (x_0, T, states, step Jacobians, iterations).
    """
    n = osc.n
    x, T = list(x0), T0
    x[p] = value
    for it in range(1, max_iter + 1):
        xs, mats = orbit(osc, x, T, S)
        M = sim3dense.identity(n, 1.0)
        for P in mats:
            M = sim3dense.matmul(P, M)
        fT = osc.F(xs[-1])
        J = [[M[i][j] - (i == j) for j in range(n)] + [fT[i]] for i in range(n)]
        J.append([1.0 if j == p else 0.0 for j in range(n)] + [0.0])
        r = [xs[-1][i] - x[i] for i in range(n)] + [x[p] - value]
        d = sim3dense.solve(J, [-v for v in r])
        x = [x[i] + d[i] for i in range(n)]
        T += d[n]
        if max(abs(v) for v in d[:n]) <= tol * (1 + max(abs(v) for v in x)) and abs(d[n]) <= tol * T:
            xs, mats = orbit(osc, x, T, S)
            return x, T, xs, mats, it
    raise NoConvergence("limit cycle")


def ppv(osc, xs, mats):
    """The PPV at x_0..x_S of the orbit, by the discrete adjoint recurrence."""
    n = osc.n
    M = sim3dense.identity(n, 1.0)
    for P in mats:  # @line L2
        M = sim3dense.matmul(P, M)
    f0 = osc.F(xs[0])
    # bordered system: (M^T - I) v + mu f0 = 0, f0^T v = 1 (mu is 0 up to the step error)
    K = [[M[j][i] - (i == j) for j in range(n)] + [f0[i]] for i in range(n)]
    K.append(list(f0) + [0.0])
    v0 = sim3dense.solve(K, [0.0] * n + [1.0])[:n]  # @line L3
    vs = [None] * len(xs)
    vs[-1] = v0
    for k in range(len(mats) - 1, -1, -1):  # @line L4
        P = mats[k]
        vs[k] = [sum(P[a][b] * vs[k + 1][a] for a in range(n)) for b in range(n)]
    return vs


def diffusion_constant(osc, vs):
    """c = (1/T) int v^T B B^T v dt, by the rectangle rule on the periodic samples."""
    S = len(vs) - 1
    total = 0.0
    for v in vs[:S]:
        w = [sum(v[a] * osc.B[a][j] for a in range(osc.n)) for j in range(len(osc.B[0]))]
        total += sum(t * t for t in w)
    return total / S


def ssb_phase_noise(c, f0, fm):
    """Single-sideband phase noise L(fm) in dBc/Hz from the Lorentzian of the first harmonic."""
    return 10 * math.log10(f0 * f0 * c / (math.pi ** 2 * f0 ** 4 * c * c + fm * fm))


def phase_noise(osc, x0, T0, S, offsets, p=1, value=0.0):
    """PPV phase noise analysis.

    Returns a dict with the orbit (x0, T, states), the PPV samples v, the
    diffusion constant c (in s^2/s) and L(fm) in dBc/Hz for each offset fm.
    """
    x, T, xs, mats, _ = limit_cycle(osc, x0, T0, S, p, value)  # @line L1
    vs = ppv(osc, xs, mats)
    c = diffusion_constant(osc, vs)  # @line L5
    L = [ssb_phase_noise(c, 1 / T, fm) for fm in offsets]  # @line L6
    return {"x0": x, "T": T, "states": xs, "v": vs, "c": c, "L": L}  # @line L7


def stochastic_heun(osc, x0, h, steps, rng):
    """One sample path of dx = F dt + B dW by the stochastic Heun method.

    The noise is additive, so the method has strong order 1 and the drift
    error of a deterministic second-order method; Euler-Maruyama would grow
    the orbit of a fast oscillator and bias the phase variance.
    Returns the states at every step.
    """
    n, p = osc.n, len(osc.B[0])
    sq = math.sqrt(h)
    x = list(x0)
    out = [list(x)]
    for _ in range(steps):
        dw = [rng.gauss(0.0, sq) for _ in range(p)]
        noise = [sum(osc.B[i][j] * dw[j] for j in range(p)) for i in range(n)]
        f = osc.F(x)
        y = [x[i] + h * f[i] + noise[i] for i in range(n)]
        g = osc.F(y)
        x = [x[i] + h / 2 * (f[i] + g[i]) + noise[i] for i in range(n)]
        out.append(x)
    return out
