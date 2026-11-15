# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/describing-function/. The authors are listed in prov/4JVRZW.jsonl.

"""Describing functions and the harmonic balance prediction of limit cycles.

A static nonlinearity phi gets the describing function
N(a) = (b1 + i a1) / a, where b1 and a1 are the first Fourier coefficients
of phi(a sin t) on one period. The closed forms below are for the ideal
relay, the saturation, the dead zone and the relay with hysteresis.

harmonic_balance() follows the pseudocode of the page (lines L1 to L8): for
a real describing function and a linear part G(s) it finds the phase
crossover w of G, solves N(a) = -1 / G(i w) for the amplitude a, and
reports whether the predicted cycle is attracting and how strongly G
filters the third harmonic.

simulate_loop() integrates the loop u = phi(-y), y = G(s) u for a strictly
proper G in controllable canonical form with the classical fourth-order
Runge-Kutta method, so that a prediction can be compared with the true
oscillation. The method is approximate: the prediction can be wrong, and
the tests show by how much in each example.
"""

import cmath
import math


# ------------------------------------------------------------ nonlinearities
def relay(d):
    return lambda x: d if x > 0 else (-d if x < 0 else 0.0)


def saturation(k, delta):
    return lambda x: k * max(-delta, min(delta, x))


def dead_zone(k, delta):
    def phi(x):
        if x > delta:
            return k * (x - delta)
        if x < -delta:
            return k * (x + delta)
        return 0.0
    return phi


# ------------------------------------------------- closed-form describing functions
def df_relay(d, a):
    return 4.0 * d / (math.pi * a)


def df_saturation(k, delta, a):
    if a <= delta:
        return float(k)
    r = delta / a
    return 2.0 * k / math.pi * (math.asin(r) + r * math.sqrt(1.0 - r * r))


def df_dead_zone(k, delta, a):
    return k - df_saturation(k, delta, a)


def df_relay_hysteresis(d, h, a):
    """Complex N(a) of a relay with output +-d that switches at +-h (a > h)."""
    if a <= h:
        raise ValueError("the relay does not switch when a <= h")
    return 4.0 * d / (math.pi * a) * cmath.exp(-1j * math.asin(h / a))


# ------------------------------------------------- numerical describing function
def describing_function(phi, a, m=4096):
    """N(a) = (b1 + i a1) / a for a static phi, by the midpoint rule."""
    h = 2.0 * math.pi / m
    b1 = a1 = 0.0
    for k in range(m):
        t = (k + 0.5) * h
        y = phi(a * math.sin(t))
        b1 += y * math.sin(t)
        a1 += y * math.cos(t)
    return complex(b1 * h / math.pi, a1 * h / math.pi) / a


def describing_function_hysteresis(d, h, a, m=4096):
    """N(a) of the relay with hysteresis from its output on one period."""
    step = 2.0 * math.pi / m
    state = -d  # on the way up from -a the relay is at -d
    b1 = a1 = 0.0
    for k in range(m):
        t = (k + 0.5) * step
        x = a * math.sin(t)
        if x >= h:
            state = d
        elif x <= -h:
            state = -d
        b1 += state * math.sin(t)
        a1 += state * math.cos(t)
    return complex(b1 * step / math.pi, a1 * step / math.pi) / a


# ------------------------------------------------------------- linear parts
def tf(num, den):
    """G(s) = num(s) / den(s), coefficients with the highest power first."""
    def ev(c, s):
        v = 0j
        for x in c:
            v = v * s + x
        return v
    return lambda s: ev(num, s) / ev(den, s)


def _bisect(f, lo, hi, tol=1e-13, it=200):
    flo = f(lo)
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
        if hi - lo < tol * max(1.0, abs(hi)):
            break
    return 0.5 * (lo + hi)


# ------------------------------------------------------------ harmonic balance
def harmonic_balance(G, N, w_lo, w_hi, a_lo, a_hi):
    """Predict a limit cycle for a real describing function N(a).

    G(s) is the linear part, Im G(i w) must change sign once on
    [w_lo, w_hi], and N(a) - r must change sign once on [a_lo, a_hi].
    Returns None when harmonic balance has no solution there. The flag
    'attracting' assumes the usual case in which the loop with a constant
    gain k in place of N is asymptotically stable for k < r and unstable
    for k > r near the crossing.
    """
    if (G(1j * w_lo).imag > 0) == (G(1j * w_hi).imag > 0):  # @line L1
        return None  # @line L1
    w = _bisect(lambda x: G(1j * x).imag, w_lo, w_hi)  # @line L1
    g = G(1j * w).real  # @line L2
    if g >= 0:  # @line L2
        return None  # @line L2
    r = -1.0 / g  # @line L3
    if (N(a_lo) - r > 0) == (N(a_hi) - r > 0):  # @line L4
        return None  # @line L4
    a = _bisect(lambda x: N(x) - r, a_lo, a_hi)  # @line L5
    da = 1e-6 * a  # @line L6
    slope = (N(a + da) - N(a - da)) / (2 * da)  # @line L6
    q = abs(G(3j * w)) / abs(G(1j * w))  # @line L7
    return {"a": a, "w": w, "period": 2 * math.pi / w, "gain": r,  # @line L8
            "attracting": slope < 0, "filter": q}  # @line L8


def harmonic_balance_complex(G, N, w0, a0, tol=1e-12, it=100):
    """Solve G(i w) N(a) + 1 = 0 for (w, a) by Newton's method.

    N may be complex, for example a relay with hysteresis. The Jacobian is
    taken by central differences. Returns None if Newton does not converge.
    """
    w, a = float(w0), float(a0)
    for _ in range(it):
        F = G(1j * w) * N(a) + 1
        if abs(F) < tol:
            return {"a": a, "w": w, "period": 2 * math.pi / w}
        hw, ha = 1e-7 * w, 1e-7 * a
        Fw = (G(1j * (w + hw)) * N(a) - G(1j * (w - hw)) * N(a)) / (2 * hw)
        Fa = (G(1j * w) * N(a + ha) - G(1j * w) * N(a - ha)) / (2 * ha)
        det = Fw.real * Fa.imag - Fa.real * Fw.imag
        if det == 0:
            return None
        dw = (F.real * Fa.imag - Fa.real * F.imag) / det
        step_a = (Fw.real * F.imag - F.real * Fw.imag) / det
        w, a = w - dw, a - step_a
        if w <= 0 or a <= 0:
            return None
    return None


# ------------------------------------------------------------------ simulation
def simulate_loop(num, den, nonlinearity, x0, dt, T, hysteresis=None):
    """Simulate u = phi(-y), y = (num/den) u, with den monic and deg num < deg den.

    The state is the controllable canonical form. The input is held over
    each RK4 step. With hysteresis = (d, h) the relay with hysteresis is
    used instead of 'nonlinearity'. Returns the samples of y and the step.
    """
    n = len(den) - 1
    if abs(den[0] - 1.0) > 0 or len(num) > n:
        raise ValueError("den must be monic and G strictly proper")
    c = [0.0] * (n - len(num)) + [float(v) for v in num]
    c = list(reversed(c))  # c[i] multiplies x_{i+1}
    a = [float(v) for v in reversed(den[1:])]  # a[i] multiplies x_{i+1}

    def out(x):
        return sum(ci * xi for ci, xi in zip(c, x))

    def f(x, u):
        dx = x[1:] + [u - sum(ai * xi for ai, xi in zip(a, x))]
        return dx

    x = [float(v) for v in x0]
    steps = int(round(T / dt))
    ys = [out(x)]
    state = None
    if hysteresis is not None:
        d, h = hysteresis
        state = d if -out(x) >= 0 else -d
    for _ in range(steps):
        e = -out(x)
        if hysteresis is not None:
            if e >= h:
                state = d
            elif e <= -h:
                state = -d
            u = state
        else:
            u = nonlinearity(e)
        k1 = f(x, u)
        k2 = f([xi + dt / 2 * ki for xi, ki in zip(x, k1)], u)
        k3 = f([xi + dt / 2 * ki for xi, ki in zip(x, k2)], u)
        k4 = f([xi + dt * ki for xi, ki in zip(x, k3)], u)
        x = [xi + dt / 6 * (p + 2 * q + 2 * r + s) for xi, p, q, r, s in zip(x, k1, k2, k3, k4)]
        ys.append(out(x))
    return ys


def measure_cycle(ys, dt, last=4):
    """Amplitude and period of the oscillation over the last upward zero crossings."""
    ups = []
    for k in range(1, len(ys)):
        if ys[k - 1] < 0 <= ys[k]:
            ups.append((k - 1) + (-ys[k - 1]) / (ys[k] - ys[k - 1]))
    if len(ups) < last + 1:
        return None
    period = (ups[-1] - ups[-1 - last]) / last * dt
    start = int(ups[-1 - last])
    seg = ys[start:int(ups[-1]) + 1]
    amp = (max(seg) - min(seg)) / 2
    return {"a": amp, "period": period}
