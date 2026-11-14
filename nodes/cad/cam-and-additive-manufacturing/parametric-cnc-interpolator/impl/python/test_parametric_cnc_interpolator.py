# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parametric-cnc-interpolator/. The authors are listed in prov/QFCNX0.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from parametric_cnc_interpolator import exact_parameters, feed_errors, interpolate, taylor_step

# The Pythagorean hodograph cubic C(t) = (t - t^3/3, t^2): |C'(t)| = 1 + t^2,
# so its arc length s(t) = t + t^3/3 is a polynomial and exact with Fractions.


def ph_d1(t):
    return (1 - t * t, 2 * t)


def ph_d2(t):
    return (-2 * t, 2)


def ph_speed(t):
    return 1 + t * t


def ph_s(t):
    return t + t ** 3 / 3


def ph_leading(t):
    """The limit of (step arc length - L) / L^3 at t, from -|C'| u'''(s) / 6."""
    return (1 - 5 * t * t) / (3 * (1 + t * t) ** 4)


# The parabola C(t) = (t, t^2) is not a PH curve; its arc length has a closed form.


def pa_d1(t):
    return (1.0, 2.0 * t)


def pa_d2(t):
    return (0.0, 2.0)


def pa_s(t):
    return t * math.sqrt(1 + 4 * t * t) / 2 + math.asinh(2 * t) / 4


def pa_s_inverse(S):
    lo, hi = 0.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if pa_s(mid) < S:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def step_error(u, L, order):
    du = taylor_step(ph_d1, ph_d2, u, L, order, speed=ph_speed)
    return ph_s(u + du) - ph_s(u) - L


def test_step_at_zero_is_exact_to_the_cubic_term():
    for L in [F(1, 10), F(1, 100), F(3, 1000)]:
        assert taylor_step(ph_d1, ph_d2, F(0), L, 2, ph_speed) == L
        assert step_error(F(0), L, 2) == L ** 3 / 3


def test_step_at_one_closed_forms():
    for L in [F(1, 10), F(1, 100), F(1, 1000)]:
        # first order: du = L/2, the error is L^2/4 + L^3/24 exactly
        assert step_error(F(1), L, 1) == L ** 2 / 4 + L ** 3 / 24
        # second order: du = L/2 - L^2/8, the error is -L^3/12 + O(L^4)
        e = step_error(F(1), L, 2)
        assert abs(e / L ** 3 + F(1, 12)) <= L


def test_leading_term_exact_on_random_parameters():
    rng = random.Random(11)
    L = F(1, 2000)
    for _ in range(40):
        u = F(rng.randint(0, 300), 100)
        e = step_error(u, L, 2)
        assert abs(e / L ** 3 - ph_leading(u)) <= 4 * L
        # the first order step is wrong already at L^2
        e1 = step_error(u, L, 1)
        c1 = u / (1 + u * u) ** 2  # -|C'| u''(s) / 2 = (C'.C'') / (2 |C'|^3)
        assert abs(e1 / L ** 2 - c1) <= 4 * L


def max_rel_error(order, L, curve):
    if curve == "ph":
        params = interpolate(ph_d1, ph_d2, 0.0, 2.0, L, 1.0, order, speed=ph_speed)
        errs = feed_errors(params, ph_s, L)
    else:
        params = interpolate(pa_d1, pa_d2, 0.0, 2.0, L, 1.0, order)
        errs = feed_errors(params, pa_s, L)
    return max(abs(e) for e in errs), params


@pytest.mark.parametrize("curve", ["ph", "parabola"])
def test_feed_error_orders_against_exact_arc_length(curve):
    e2 = [max_rel_error(2, L, curve)[0] for L in (0.02, 0.01, 0.005)]
    e1 = [max_rel_error(1, L, curve)[0] for L in (0.02, 0.01, 0.005)]
    for a, b in zip(e2, e2[1:]):
        assert 3.5 <= a / b <= 4.5  # relative error O(L^2)
    for a, b in zip(e1, e1[1:]):
        assert 1.8 <= a / b <= 2.2  # relative error O(L)
    assert e2[-1] < e1[-1] / 50


def test_parabola_bound():
    # |relative error| <= max|C'| max|u'''(s)| L^2 / 6; on the parabola over [0, 2],
    # u'(s) = (1 + 4t^2)^(-1/2), and u''' is largest in size at t = 0, where it is -4.
    # max |C'| = sqrt(17).
    for L in (0.02, 0.01, 0.005):
        e2, _ = max_rel_error(2, L, "parabola")
        assert e2 <= math.sqrt(17) * 4 * L * L / 6


def test_matches_the_exact_arc_length_reference():
    L = 0.01
    _, params = max_rel_error(2, L, "parabola")
    ref = exact_parameters(pa_s, pa_s_inverse, 0.0, 2.0, L, 1.0)
    assert abs(len(params) - len(ref)) <= 1
    n = min(len(params), len(ref)) - 1
    # the arc length positions drift by at most the sum of the step errors
    drift = max(abs(pa_s(params[k]) - pa_s(ref[k])) for k in range(n))
    assert drift <= n * (math.sqrt(17) * 4 * L ** 3 / 6)


def test_chord_is_shorter_by_the_curvature_term():
    # chord = arc - kappa^2 arc^3 / 24 + O(arc^4); check at t = 0 on the parabola, kappa = 2
    for L in (0.02, 0.01):
        du = taylor_step(pa_d1, pa_d2, 0.0, L, 2)
        arc = pa_s(du)
        chord = math.hypot(du, du * du)
        assert abs((arc - chord) / arc ** 3 - 4 / 24) <= 2 * L


def test_errors():
    with pytest.raises(ValueError):
        interpolate(ph_d1, ph_d2, 0.0, 1.0, 0.0, 1.0)
    with pytest.raises(ValueError):
        interpolate(lambda t: (0.0, 0.0), ph_d2, 0.0, 1.0, 1.0, 0.01)
    with pytest.raises(ValueError):
        interpolate(ph_d1, ph_d2, 0.0, 1.0, 1.0, 0.01, order=3)
    with pytest.raises(ValueError):
        taylor_step(ph_d1, ph_d2, 0.0, 0.1, order=3)
