# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-movement-primitives/. The authors are listed in prov/DHD4FD.jsonl.
"""Tests: the DMP reproduces a minimum-jerk demonstration, converges to the goal, and scales in time and goal."""

from dynamic_movement_primitives import DMP


def demo(y0, g, T, n=1001):
    """Samples of the minimum-jerk motion from y0 to g in time T."""
    ts, ys, vs, accs = [], [], [], []
    for k in range(n):
        t = T * k / (n - 1)
        u = t / T
        d = g - y0
        ts.append(t)
        ys.append(y0 + d * u ** 3 * (10 - 15 * u + 6 * u * u))
        vs.append(d * 30 * u * u * (1 - u) ** 2 / T)
        accs.append(d * 60 * u * (1 - u) * (1 - 2 * u) / (T * T))
    return ts, ys, vs, accs


def fitted():
    dmp = DMP()
    ts, ys, vs, accs = demo(0.0, 1.0, 1.0)
    dmp.fit(ts, ys, vs, accs, tau=1.0)
    return dmp, ys


def test_reproduces_demonstration():
    dmp, ys = fitted()
    _, out = dmp.rollout(tau=1.0, duration=1.0)
    err = max(abs(a - b) for a, b in zip(out, ys))
    assert err < 0.03  # measured: the fit with 20 basis functions is close, not exact


def test_converges_to_goal():
    dmp, _ = fitted()
    _, out = dmp.rollout(tau=1.0, duration=3.0)
    y, z, x = dmp.last_state
    assert abs(y - 1.0) < 1e-3 and abs(z) < 1e-2 and x < 1e-5


def test_new_goal_and_start_still_converge():
    dmp, _ = fitted()
    for y0, g in ((0.0, 2.0), (1.0, -0.5), (0.3, 0.3)):
        _, out = dmp.rollout(tau=1.0, duration=3.0, y0=y0, g=g)
        assert out[0] == y0
        assert abs(out[-1] - g) < 1e-3 * max(1.0, abs(g - y0))


def test_without_forcing_term_is_critically_damped():
    dmp = DMP()
    _, out = dmp.rollout(tau=1.0, duration=2.0)
    # No overshoot: the position rises monotonically toward the goal 1.
    assert all(b >= a - 1e-12 for a, b in zip(out, out[1:]))
    assert out[-1] <= 1.0 + 1e-12


def test_time_scaling():
    dmp, _ = fitted()
    _, fast = dmp.rollout(tau=1.0, duration=1.0, dt=0.001)
    _, slow = dmp.rollout(tau=2.0, duration=2.0, dt=0.002)
    # Doubling tau plays the same motion at half speed.
    assert max(abs(a - b) for a, b in zip(fast, slow)) < 1e-9
