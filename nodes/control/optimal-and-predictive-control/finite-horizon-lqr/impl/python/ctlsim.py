# SPDX-License-Identifier: MIT
# Shared helper of the control pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Fixed step simulation for the control pages.

Conventions:
- A continuous-time system is a function f(t, x, u) that returns x' as a
  flat list. x is a flat list. u is whatever the control returns (a flat
  list, a scalar, or None when there is no control).
- A discrete-time system is a function F(k, x, u) that returns x_(k+1).
- The integrator is the classical 4th order Runge-Kutta method with a fixed
  step dt. The input is held constant over each step.
- Time t_k = t0 + k dt is computed by multiplication, not by summation.
- The number of steps round((t1 - t0) / dt) and the hold ratio
  round(hold / dt) must match the real ratios within 1e-9 (relative), or
  ValueError is raised.

This file holds no controller or observer of a control page.
"""

__all__ = ["rk4_step", "simulate", "simulate_discrete", "lti"]


def _axpy(a, x, y):
    return [yi + a * xi for xi, yi in zip(x, y)]


def rk4_step(f, t, x, u, dt):
    """Return x(t + dt) after one RK4 step of x' = f(t, x, u), u held constant."""
    k1 = f(t, x, u)
    k2 = f(t + dt / 2, _axpy(dt / 2, k1, x), u)
    k3 = f(t + dt / 2, _axpy(dt / 2, k2, x), u)
    k4 = f(t + dt, _axpy(dt, k3, x), u)
    return [xi + dt / 6 * (a + 2 * b + 2 * c + d) for xi, a, b, c, d in zip(x, k1, k2, k3, k4)]


def _ratio(num, den, what):
    r = round(num / den)
    if abs(r * den - num) > 1e-9 * max(abs(num), abs(den)):
        raise ValueError(what + " is not an integer multiple of dt")
    return r


def simulate(f, x0, t0, t1, dt, control=None, hold=None):
    """Simulate x' = f(t, x, u) from x(t0) = x0 to t1 with RK4 and step dt.

    control(t, x) gives the input. It is called at each sampling instant
    t0 + j hold, and its value is held (zero-order hold) until the next
    instant. hold must be an integer multiple of dt; hold = None means
    hold = dt. With control = None the input is None.

    Returns (ts, xs, us): ts has N + 1 times, xs the N + 1 states, and us the
    N inputs, where us[k] acts on [ts[k], ts[k + 1]].
    """
    if dt <= 0:
        raise ValueError("dt must be positive")
    n_steps = _ratio(t1 - t0, dt, "t1 - t0")
    if n_steps < 0:
        raise ValueError("t1 is before t0")
    r = 1 if hold is None else _ratio(hold, dt, "hold")
    if r < 1:
        raise ValueError("hold must be at least dt")
    x = list(x0)
    ts = [t0]
    xs = [list(x)]
    us = []
    u = None
    for k in range(n_steps):
        t = t0 + k * dt
        if control is not None and k % r == 0:
            u = control(t, list(x))
        x = rk4_step(f, t, x, u, dt)
        ts.append(t0 + (k + 1) * dt)
        xs.append(x)
        us.append(u)
    return ts, xs, us


def simulate_discrete(F, x0, N, control=None):
    """Run x_(k+1) = F(k, x_k, u_k) for k = 0, ..., N - 1.

    u_k = control(k, x_k), or None if control is None. Returns (xs, us) with
    N + 1 states and N inputs. Exact if F and control are exact.
    """
    x = list(x0)
    xs = [list(x)]
    us = []
    for k in range(N):
        u = control(k, list(x)) if control is not None else None
        x = list(F(k, x, u))
        xs.append(x)
        us.append(u)
    return xs, us


def lti(A, B=None):
    """Return f(t, x, u) = A x + B u for the system x' = A x + B u.

    u may be a flat list, a scalar (one input) or None (zero input). B may
    be None for a system with no input.
    """
    def f(t, x, u):
        dx = [sum(a * xi for a, xi in zip(row, x)) for row in A]
        if B is None or u is None:
            return dx
        uu = u if isinstance(u, (list, tuple)) else [u]
        return [d + sum(b * ui for b, ui in zip(row, uu)) for d, row in zip(dx, B)]
    return f


def _self_test():
    import math
    f = lti([[-1.0]])
    _, xs, _ = simulate(f, [1.0], 0.0, 1.0, 0.01)
    assert abs(xs[-1][0] - math.exp(-1.0)) < 1e-9
    return True


if __name__ == "__main__":
    _self_test()
