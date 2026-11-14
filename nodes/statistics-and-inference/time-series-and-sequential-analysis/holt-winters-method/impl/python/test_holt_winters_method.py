# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/holt-winters-method/. The authors are listed in prov/56FTG8.jsonl.

import math
import random
from fractions import Fraction

import pytest

from holt_winters_method import arima022_forecasts, fit, holt_winters, initial_states

HOLT_Y = [Fraction(v) for v in (10, 12, 15, 14, 18, 21)]
SEASONAL_Y = [Fraction(v) for v in (12, 8, 14, 10, 16, 11, 17, 14, 19, 14, 21, 17)]


def test_holt_worked_example() -> None:
    r = holt_winters(HOLT_Y, Fraction(1, 2), Fraction(1, 2), h=3)
    assert r["fitted"] == [12, Fraction(25, 2), Fraction(109, 8), Fraction(513, 32), Fraction(2077, 128),
                           Fraction(9609, 512)]
    assert r["level"] == Fraction(20361, 1024) and r["trend"] == Fraction(4531, 2048)
    assert r["forecasts"] == [Fraction(45253, 2048), Fraction(6223, 256), Fraction(54315, 2048)]
    assert r["sse"] == Fraction(4822241, 262144)


def test_seasonal_worked_example() -> None:
    assert initial_states(SEASONAL_Y, 4, "add") == (11, Fraction(7, 8), [1, -3, 3, -1])
    r = holt_winters(SEASONAL_Y, Fraction(1, 2), Fraction(1, 4), Fraction(1, 4), 4, "add", h=4)
    assert r["fitted"][0] == Fraction(103, 8) and r["errors"][0] == Fraction(-7, 8)
    assert r["fitted"][1] == Fraction(589, 64)
    want = [21.439065563, 16.842204589, 23.499558342, 20.134910795]
    assert all(abs(float(p) - q) < 1e-9 for p, q in zip(r["forecasts"], want))


@pytest.mark.parametrize("alpha,beta", [(Fraction(1, 2), Fraction(1, 2)), (Fraction(3, 10), Fraction(1, 5)),
                                        (Fraction(9, 10), Fraction(1, 10)), (Fraction(1), Fraction(0))])
def test_holt_equals_arima_0_2_2(alpha, beta) -> None:
    # One-step forecasts agree exactly with theta1 = alpha (1 + beta) - 2 and
    # theta2 = 1 - alpha, from the same start, and so do all h-step forecasts.
    rng = random.Random(5)
    y = [Fraction(rng.randint(-20, 20)) for _ in range(15)]
    r = holt_winters(y, alpha, beta, h=6)
    th1, th2 = alpha * (1 + beta) - 2, 1 - alpha
    fc = arima022_forecasts(y, th1, th2, r["fitted"][1], r["errors"][0])
    assert fc == r["fitted"][1:]
    # h-step ARIMA(0,2,2) forecasts: yhat(n+1), then 2 yhat(n+1) - y_n + theta2 e_n, then a straight line.
    n = len(y)
    e = r["errors"]
    f1 = 2 * y[-1] - y[-2] + th1 * e[-1] + th2 * e[-2]
    arima = [f1, 2 * f1 - y[-1] + th2 * e[-1]]
    while len(arima) < 6:
        arima.append(2 * arima[-1] - arima[-2])
    assert arima == r["forecasts"]
    # and the errors satisfy the MA(2) recursion for the second differences
    for t in range(2, n):
        assert y[t] - 2 * y[t - 1] + y[t - 2] == e[t] + th1 * e[t - 1] + th2 * e[t - 2]


def test_winters_form_equals_component_form() -> None:
    # Winters (1960) smooths the season with y_t - l_t; that equals the component
    # form with gamma = gamma_star (1 - alpha).
    a, b, gs = Fraction(2, 5), Fraction(1, 3), Fraction(1, 2)
    level, trend, season = initial_states(SEASONAL_Y, 4, "add")
    season = list(season)
    fitted = []
    for t, obs in enumerate(SEASONAL_Y):
        s = season[t % 4]
        fitted.append(level + trend + s)
        new_level = a * (obs - s) + (1 - a) * (level + trend)
        season[t % 4] = gs * (obs - new_level) + (1 - gs) * s
        trend = b * (new_level - level) + (1 - b) * trend
        level = new_level
    r = holt_winters(SEASONAL_Y, a, b, gs * (1 - a), 4, "add")
    assert r["fitted"] == fitted


@pytest.mark.parametrize("seasonal", ["add", "mul"])
def test_exact_on_noise_free_data(seasonal) -> None:
    # A line plus a fixed season (or a line times a fixed season) is forecast
    # with zero error for any smoothing constants, from the classical start.
    m = 4
    s_add = [3, -1, -4, 2]
    s_mul = [Fraction(5, 4), Fraction(3, 4), Fraction(1, 2), Fraction(3, 2)]
    y = []
    for t in range(20):
        line = Fraction(50) + Fraction(3, 2) * (t + 1)
        y.append(line + s_add[t % m] if seasonal == "add" else line * s_mul[t % m])
    # the true start: level and trend at t = 0, the season for t = 1..m
    init = (Fraction(50), Fraction(3, 2), s_add if seasonal == "add" else s_mul)
    r = holt_winters(y, Fraction(1, 3), Fraction(1, 5), Fraction(1, 7), m, seasonal, h=5, init=init)
    assert all(e == 0 for e in r["errors"])
    for k in range(1, 6):
        t = 20 + k
        line = Fraction(50) + Fraction(3, 2) * t
        want = line + s_add[(t - 1) % m] if seasonal == "add" else line * s_mul[(t - 1) % m]
        assert r["forecasts"][k - 1] == want


def test_simple_exponential_smoothing_special_case() -> None:
    # beta = 0 and b_0 = 0 give simple exponential smoothing, an exponential moving average.
    y = [Fraction(v) for v in (3, 7, 4, 8, 6)]
    a = Fraction(1, 3)
    r = holt_winters(y, a, Fraction(0), init=(y[0], Fraction(0), []))
    ema = y[0]
    for t, obs in enumerate(y):
        assert r["fitted"][t] == ema
        ema = a * obs + (1 - a) * ema
    assert r["level"] == ema


def test_fit_recovers_seasonal_structure() -> None:
    # Simulate ETS(A,A,A) with alpha = 0.3, beta* = 0.1, gamma = 0.2, noise SD 2;
    # the fitted Holt-Winters forecasts beat the seasonal naive forecast.
    rng = random.Random(2026)
    m, n = 12, 144
    level, trend = 100.0, 0.5
    season = [10 * math.sin(2 * math.pi * i / m) for i in range(m)]
    y = []
    for t in range(n):
        e = rng.gauss(0, 2)
        y.append(level + trend + season[t % m] + e)
        level, trend = level + trend + 0.3 * e, trend + 0.03 * e
        season[t % m] += 0.2 * e
    a, b, g, sse = fit(y[:120], m, "add")
    assert 0 < a < 1 and 0 < b < 1 and 0 <= g <= 1 - a
    fc = holt_winters(y[:120], a, b, g, m, "add", h=24)["forecasts"]
    rmse = math.sqrt(sum((p - q) ** 2 for p, q in zip(fc, y[120:])) / 24)
    snaive = math.sqrt(sum((y[120 + k - 12 * (1 + k // 12)] - y[120 + k]) ** 2 for k in range(24)) / 24)
    assert rmse < 3.0 < snaive


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        holt_winters([1, 2, 3, 4, 5, 6, 7, 8], 0.5, 0.5, 0.5, 4, "xyz")
    with pytest.raises(ValueError):
        initial_states([1, 2, 3], 4, "add")
    with pytest.raises(ValueError):
        initial_states([1])
