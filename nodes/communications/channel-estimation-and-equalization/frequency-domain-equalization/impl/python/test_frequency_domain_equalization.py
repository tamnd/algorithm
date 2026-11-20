# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frequency-domain-equalization/. The authors are listed in prov/8TF7E6.jsonl.

import cmath
import math
import random

import pytest

from frequency_domain_equalization import add_cyclic_prefix, channel, fde, fft, mmse_mse, zf_mse


def cn(rng, var):
    s = math.sqrt(var / 2)
    return complex(rng.gauss(0, s), rng.gauss(0, s))


def dft(x):
    n = len(x)
    return [sum(x[t] * cmath.exp(-2j * math.pi * k * t / n) for t in range(n)) for k in range(n)]


def solve(a, b):
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            for k in range(c, n + 1):
                m[r][k] -= f * m[c][k]
    x = [0j] * n
    for r in range(n - 1, -1, -1):
        x[r] = (m[r][n] - sum(m[r][k] * x[k] for k in range(r + 1, n))) / m[r][r]
    return x


QPSK = [complex(a, b) / math.sqrt(2) for a in (-1, 1) for b in (-1, 1)]


def test_example_on_the_page() -> None:
    x = [1, -1, -1, 1]
    r = channel(add_cyclic_prefix(x, 1), [1, 0.5])
    assert r[1:] == [1.5, -0.5, -1.5, 0.5]
    y = fft(r[1:])
    want = [0, 3 + 1j, 0, 3 - 1j]
    assert max(abs(a - b) for a, b in zip(y, want)) < 1e-12
    hf = fft([1, 0.5, 0, 0])
    assert max(abs(a - b) for a, b in zip(hf, [1.5, 1 - 0.5j, 0.5, 1 + 0.5j])) < 1e-12
    assert max(abs(a - b) for a, b in zip(fde(r, [1, 0.5], 4, 1), x)) < 1e-12
    assert abs(mmse_mse([1, 0.5], 4, 0.1) - 0.119104) < 1e-6
    assert abs(zf_mse([1, 0.5], 4, 0.1) - 0.151111) < 1e-6


def test_fft_matches_the_direct_dft() -> None:
    rng = random.Random(7801)
    for n in list(range(1, 17)) + [32, 64]:
        x = [cn(rng, 1.0) for _ in range(n)]
        a, b = fft(x), dft(x)
        assert max(abs(u - v) for u, v in zip(a, b)) < 1e-9
        back = fft(a, inverse=True)
        assert max(abs(u - v) for u, v in zip(back, x)) < 1e-9


def test_zero_forcing_inverts_the_channel_without_noise() -> None:
    rng = random.Random(7802)
    for _ in range(30):
        taps = rng.randint(1, 6)
        h = [cn(rng, 1.0) for _ in range(taps)]
        n = rng.choice((8, 12, 16, 32))
        p = taps - 1 + rng.randint(0, 2)
        prev = [rng.choice(QPSK) for _ in range(n + p)]
        x = [rng.choice(QPSK) for _ in range(n)]
        r = channel(add_cyclic_prefix(x, p), h, prev)  # the previous block's tail falls into the prefix
        est = fde(r, h, n, p)
        assert max(abs(a - b) for a, b in zip(est, x)) < 1e-9


def test_short_prefix_leaves_interblock_interference() -> None:
    rng = random.Random(7803)
    h = [1, 0.6, 0.4, 0.3]
    x = [rng.choice(QPSK) for _ in range(16)]
    prev = [rng.choice(QPSK) for _ in range(17)]
    r = channel(add_cyclic_prefix(x, 1), h, prev)
    with pytest.raises(ValueError):
        fde(r, h, 16, 1)
    # the one-tap equalizer applied anyway: the tail of the previous block stays in the result
    y = r[1:]
    xf, hf = fft(y), fft(h + [0] * 12)
    wrong = fft([a / b for a, b in zip(xf, hf)], inverse=True)
    assert max(abs(a - b) for a, b in zip(wrong, x)) > 1e-2


def test_mmse_equals_the_circulant_matrix_solution() -> None:
    rng = random.Random(7804)
    for _ in range(6):
        n, h = rng.choice((8, 12, 16)), [cn(rng, 1.0) for _ in range(3)]
        n0, es = rng.uniform(0.05, 1.0), rng.uniform(0.5, 2.0)
        r = [cn(rng, 1.0) for _ in range(n + 2)]
        est = fde(r, h, n, 2, n0, es)
        hc = [[h[(i - j) % n] if (i - j) % n < len(h) else 0j for j in range(n)] for i in range(n)]
        y = r[2:]
        a = [[sum(hc[k][i].conjugate() * hc[k][j] for k in range(n)) + (n0 / es if i == j else 0) for j in range(n)] for i in range(n)]
        b = [sum(hc[k][i].conjugate() * y[k] for k in range(n)) for i in range(n)]
        want = solve(a, b)
        assert max(abs(u - v) for u, v in zip(est, want)) < 1e-9


def test_measured_mse_matches_the_formula() -> None:
    # QPSK with Es = 1, N = 64, P = 2, N0 = 0.1, 200 blocks, seed 7805: MMSE on Proakis channel B
    # and ZF on (1, 0.5); ZF on B is useless, because B has |H|^2 = 1e-6 at bin 32
    rng = random.Random(7805)
    n, p, n0 = 64, 2, 0.1
    for h, mode in (([0.407, 0.815, 0.407], n0), ([1, 0.5], None)):
        formula = mmse_mse(h, n, n0) if mode else zf_mse(h, n, n0)
        total, count = 0.0, 0
        prev = [rng.choice(QPSK) for _ in range(n + p)]
        for _ in range(200):
            x = [rng.choice(QPSK) for _ in range(n)]
            s = add_cyclic_prefix(x, p)
            r = [v + cn(rng, n0) for v in channel(s, h, prev)]
            prev = s
            est = fde(r, h, n, p, mode)
            total += sum(abs(a - b) ** 2 for a, b in zip(est, x))
            count += n
        assert abs(total / count - formula) < 0.04 * formula


def test_input_checks() -> None:
    with pytest.raises(ValueError):
        fde([0j] * 9, [1, 0.5, 0.2], 8, 1)
    with pytest.raises(ValueError):
        fde([0j] * 8, [1, 0.5], 8, 1)
