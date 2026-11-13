# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/window-functions/. The authors are listed in prov/YX4DES.jsonl.

import cmath
import math
import random

from window_functions import (
    bessel_i0,
    blackman,
    coherent_gain,
    dtft_magnitude,
    enbw_bins,
    hamming,
    hann,
    kaiser,
    measure,
    rectangular,
)

N = 64


def dirichlet(n: int, omega: float) -> complex:
    """DTFT of the box of length n, closed form."""
    s = math.sin(omega / 2)
    if abs(s) < 1e-14:
        return complex(n)
    return cmath.exp(-1j * omega * (n - 1) / 2) * math.sin(n * omega / 2) / s


def test_hann_spectrum_is_three_shifted_dirichlet_kernels() -> None:
    rng = random.Random(1)
    w = hann(N)
    b = 2 * math.pi / N
    for _ in range(200):
        om = rng.uniform(-math.pi, math.pi)
        closed = 0.5 * dirichlet(N, om) - 0.25 * dirichlet(N, om - b) - 0.25 * dirichlet(N, om + b)
        assert abs(abs(closed) - dtft_magnitude(w, om)) <= 1e-9


def test_rectangular_figures() -> None:
    m = measure(rectangular(N))
    assert m["first_null_bins"] == 1.0
    assert abs(m["bandwidth_3db_bins"] - 0.886) <= 0.002
    assert abs(m["peak_sidelobe_db"] - (-13.26)) <= 0.01
    assert abs(m["scalloping_db"] - 20 * math.log10(1 / (N * math.sin(math.pi / (2 * N))))) <= 1e-9


def test_measured_table() -> None:
    want = {
        "hann": (hann(N), 2.0, 1.441, -31.47, -1.42),
        "hamming": (hamming(N), 2.0, 1.303, -42.45, -1.75),
        "blackman": (blackman(N), 3.0, 1.644, -58.11, -1.10),
    }
    for name, (w, null, bw, psl, scallop) in want.items():
        m = measure(w)
        assert m["first_null_bins"] == null, name
        assert abs(m["bandwidth_3db_bins"] - bw) <= 0.002, name
        assert abs(m["peak_sidelobe_db"] - psl) <= 0.01, name
        assert abs(m["scalloping_db"] - scallop) <= 0.01, name


def test_rectangular_has_the_narrowest_main_lobe_and_the_highest_side_lobes() -> None:
    figures = {name: measure(f(N)) for name, f in (("rect", rectangular), ("hann", hann), ("hamming", hamming), ("blackman", blackman))}
    widths = sorted(figures, key=lambda k: figures[k]["bandwidth_3db_bins"])
    levels = sorted(figures, key=lambda k: figures[k]["peak_sidelobe_db"], reverse=True)
    assert widths == ["rect", "hamming", "hann", "blackman"]
    assert levels == ["rect", "hann", "hamming", "blackman"]


def test_gains_have_closed_forms() -> None:
    # For the periodic cosine sums: coherent gain a0, ENBW (a0^2 + sum a_j^2 / 2) / a0^2.
    for w, a in ((rectangular(N), [1.0]), (hann(N), [0.5, 0.5]), (hamming(N), [0.54, 0.46]), (blackman(N), [0.42, 0.5, 0.08])):
        assert abs(coherent_gain(w) - a[0]) <= 1e-12
        assert abs(enbw_bins(w) - (a[0] ** 2 + sum(v * v for v in a[1:]) / 2) / a[0] ** 2) <= 1e-12


def test_periodic_and_symmetric_forms() -> None:
    sym = hann(N + 1, symmetric=True)
    assert sym[0] == 0 and abs(sym[-1]) <= 1e-15
    assert all(abs(a - b) <= 1e-15 for a, b in zip(hann(N), sym[:N]))
    s = hamming(33, symmetric=True)
    assert all(abs(s[k] - s[32 - k]) <= 1e-15 for k in range(33))


def test_bessel_i0_against_its_integral() -> None:
    for x in (0.0, 0.5, 3.0, 8.6, 15.0):
        n = 2000
        h = math.pi / n
        integral = sum((1 if j in (0, n) else (4 if j % 2 else 2)) * math.exp(x * math.cos(j * h)) for j in range(n + 1)) * h / 3 / math.pi
        assert abs(bessel_i0(x) - integral) <= 1e-10 * integral


def test_kaiser_trades_width_for_side_lobes() -> None:
    assert kaiser(N, 0.0) == [1.0] * N
    a = measure(kaiser(N, 6.0))
    b = measure(kaiser(N, 8.6))
    assert a["bandwidth_3db_bins"] < b["bandwidth_3db_bins"]
    assert a["peak_sidelobe_db"] > b["peak_sidelobe_db"]
    assert abs(a["peak_sidelobe_db"] - (-43.97)) <= 0.02
    assert abs(b["peak_sidelobe_db"] - (-62.78)) <= 0.02
    # first null against the continuous-window estimate sqrt(1 + (beta/pi)^2) N/(N-1)
    for m, beta in ((a, 6.0), (b, 8.6)):
        assert abs(m["first_null_bins"] - math.sqrt(1 + (beta / math.pi) ** 2) * N / (N - 1)) <= 0.02
    assert abs(coherent_gain(kaiser(N, 6.0)) - 0.492) <= 5e-4 and abs(enbw_bins(kaiser(N, 6.0)) - 1.489) <= 5e-4
    assert abs(coherent_gain(kaiser(N, 8.6)) - 0.414) <= 5e-4 and abs(enbw_bins(kaiser(N, 8.6)) - 1.749) <= 5e-4


def width_at(w, level: float) -> float:
    """Full width in bins where |W| falls to level times its peak, by bisection on the direct DTFT."""
    peak = dtft_magnitude(w, 0.0)
    lo, hi = 0.0, measure(w)["first_null_bins"] * 2 * math.pi / len(w)
    for _ in range(60):
        mid = (lo + hi) / 2
        if dtft_magnitude(w, mid) > level * peak:
            lo = mid
        else:
            hi = mid
    return 2 * lo / (2 * math.pi / len(w))


def test_six_db_widths() -> None:
    for w, want in ((rectangular(N), 1.207), (hann(N), 2.000), (hamming(N), 1.815), (blackman(N), 2.299), (kaiser(N, 6.0), 1.984), (kaiser(N, 8.6), 2.328)):
        assert abs(width_at(w, 0.5) - want) <= 0.001
