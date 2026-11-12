# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/modified-discrete-cosine-transform/. The authors are listed in prov/PVNJ5C.jsonl.

import math
import random

from modified_discrete_cosine_transform import (
    analysis, dct4, fast_imdct, fast_mdct, imdct, kbd_window, mdct, sine_window, synthesis,
)

TOL = 1e-9


def close(a, b, tol=TOL):
    return len(a) == len(b) and max((abs(p - q) for p, q in zip(a, b)), default=0.0) < tol


def test_aliasing_of_one_frame():
    # The example of the page, N = 4, rectangular window (all ones):
    # the first half comes back as a - J a and the second half as b + J b.
    x = [1.0, 2.0, 3.0, 4.0, 4.0, 3.0, 2.0, 1.0]
    ones = [1.0] * 8
    assert close(imdct(mdct(x, ones), ones), [-3.0, -1.0, 1.0, 3.0, 5.0, 5.0, 5.0, 5.0])


def test_worked_example_sine_window():
    w = sine_window(4)
    assert close(w, [math.sin(math.pi * (i + 0.5) / 8) for i in range(8)])
    sig = [3.0, 1.0, 4.0, 1.0, 5.0, 9.0, 2.0, 6.0]
    frames = analysis(sig, 4, w)
    assert len(frames) == 3
    want = [[-3.9625, -1.3626, 0.9762, 0.8113], [-10.0693, -2.8524, -0.8468, 2.8895], [-1.4682, 2.0937, 1.2848, -5.2007]]
    for f, g in zip(frames, want):
        assert close(f, g, 1e-4)
    assert close(synthesis(frames, 4, w, len(sig)), sig)


def test_princen_bradley_condition():
    for n in [2, 4, 16, 128]:
        for w in [sine_window(n), kbd_window(n, 4.0), kbd_window(n, 6.0)]:
            assert all(abs(w[i] ** 2 + w[i + n] ** 2 - 1.0) < 1e-12 for i in range(n))
            assert all(abs(w[i] - w[2 * n - 1 - i]) < 1e-15 for i in range(n))


def test_perfect_reconstruction_random():
    rng = random.Random(15)
    for trial in range(500):
        n = rng.choice([2, 4, 8])
        w = sine_window(n) if trial % 2 == 0 else kbd_window(n, rng.uniform(0.5, 6.0))
        length = rng.randint(0, 5 * n)
        sig = [rng.uniform(-1, 1) for _ in range(length)]
        out = synthesis(analysis(sig, n, w), n, w, length)
        assert close(out, sig, 1e-10)


def test_fast_against_definition():
    rng = random.Random(16)
    for n in [2, 4, 8, 16, 32, 64]:
        for w in [sine_window(n), kbd_window(n, 4.0)]:
            x = [rng.uniform(-1, 1) for _ in range(2 * n)]
            assert close(fast_mdct(x, w), mdct(x, w), 1e-10)
            c = [rng.uniform(-1, 1) for _ in range(n)]
            assert close(fast_imdct(c, w), imdct(c, w), 1e-10)


def test_fast_pipeline_long_signal():
    rng = random.Random(17)
    n = 256
    w = kbd_window(n, 4.0)
    sig = [rng.uniform(-1, 1) for _ in range(4 * n + 7)]
    out = synthesis(analysis(sig, n, w, fast_mdct), n, w, len(sig), fast_imdct)
    assert close(out, sig, 1e-10)


def test_dct4_definition_and_involution():
    rng = random.Random(18)
    for n in [2, 4, 8, 16]:
        u = [rng.uniform(-1, 1) for _ in range(n)]
        want = [sum(u[j] * math.cos(math.pi / n * (j + 0.5) * (k + 0.5)) for j in range(n)) for k in range(n)]
        assert close(dct4(u), want)
        # C4 C4 = (N/2) I.
        assert close([v * 2 / n for v in dct4(dct4(u))], u)


def test_window_without_condition_fails():
    # A rectangular window has w^2 + w^2 = 2, so TDAC does not hold.
    rng = random.Random(19)
    sig = [rng.uniform(-1, 1) for _ in range(20)]
    ones = [1.0] * 8
    out = synthesis(analysis(sig, 4, ones), 4, ones, 20)
    assert max(abs(p - q) for p, q in zip(out, sig)) > 0.1


def test_orthogonality_of_lapped_transform():
    # The analysis of a whole signal is an orthogonal map: energy is kept.
    rng = random.Random(20)
    n = 8
    w = sine_window(n)
    sig = [rng.uniform(-1, 1) for _ in range(6 * n)]
    frames = analysis(sig, n, w)
    e_sig = sum(v * v for v in sig)
    e_coef = sum(v * v for f in frames for v in f)
    assert abs(e_sig - e_coef) < 1e-9
