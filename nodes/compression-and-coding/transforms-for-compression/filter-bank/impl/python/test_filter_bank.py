# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/filter-bank/. The authors are listed in prov/A2J8ZX.jsonl.

import math
import random

from filter_bank import (
    D4_H0, D4_H1, HAAR_H0, HAAR_H1, LEGALL_H0, LEGALL_H1, alias_cancelling_synthesis, analysis,
    analysis_polyphase, convolve, cqf_highpass, qmf_pair, reconstruction_delay, synthesis, two_channel,
)

TOL = 1e-9


def close(a, b, tol=TOL):
    return len(a) == len(b) and max((abs(p - q) for p, q in zip(a, b)), default=0.0) < tol


def test_haar_worked_example():
    x = [4.0, 6.0, 10.0, 12.0, 8.0, 6.0, 5.0, 5.0]
    low, high = analysis(x, [HAAR_H0, HAAR_H1], 2)
    r = 1 / math.sqrt(2)
    assert close(low, [4 * r, 16 * r, 20 * r, 11 * r, 5 * r])
    assert close(high, [4 * r, 4 * r, -4 * r, -1 * r, -5 * r])
    f0, f1 = alias_cancelling_synthesis(HAAR_H0, HAAR_H1)
    y = synthesis([low, high], [f0, f1], 2)
    assert close(y, [0.0] + x + [0.0, 0.0])


def test_perfect_reconstruction_of_standard_filters():
    rng = random.Random(21)
    cases = [(HAAR_H0, HAAR_H1, 1.0, 1), (LEGALL_H0, LEGALL_H1, -1.0, 3), (D4_H0, D4_H1, 1.0, 3)]
    for _ in range(500):
        x = [rng.uniform(-1, 1) for _ in range(rng.randint(1, 30))]
        if all(abs(v) < 1e-6 for v in x):
            continue
        for h0, h1, gain, delay in cases:
            f0, f1 = alias_cancelling_synthesis(h0, h1)
            got = reconstruction_delay(x, two_channel(x, h0, h1, f0, f1))
            assert got is not None
            assert abs(got[0] - gain) < 1e-9 and got[1] == delay


def test_orthogonal_filters_use_time_reversed_synthesis():
    rng = random.Random(22)
    x = [rng.uniform(-1, 1) for _ in range(25)]
    for h0, delay in [(HAAR_H0, 1), (D4_H0, 3)]:
        h1 = cqf_highpass(h0)
        got = reconstruction_delay(x, two_channel(x, h0, h1, h0[::-1], h1[::-1]))
        assert got is not None and abs(got[0] - 1.0) < 1e-9 and got[1] == delay
        # Orthonormal to the even shifts: sum h0[n] h0[n + 2k] = delta(k).
        for k in range(len(h0) // 2):
            s = sum(h0[n] * h0[n + 2 * k] for n in range(len(h0) - 2 * k))
            assert abs(s - (1.0 if k == 0 else 0.0)) < 1e-12


def test_qmf_fails_with_three_taps_and_works_with_two():
    rng = random.Random(23)
    x = [rng.uniform(-1, 1) for _ in range(40)]
    h0, h1, f0, f1 = qmf_pair([0.25 * math.sqrt(2), 0.5 * math.sqrt(2), 0.25 * math.sqrt(2)])
    assert reconstruction_delay(x, two_channel(x, h0, h1, f0, f1)) is None
    # The distortion function is T(z) = (H0(z)^2 - H0(-z)^2)/2 = z^-1/2 + z^-3/2.
    t = [(p - q) / 2 for p, q in zip(convolve(h0, h0), convolve(h1, h1))]
    assert close(t, [0.0, 0.5, 0.0, 0.5, 0.0])
    h0, h1, f0, f1 = qmf_pair(HAAR_H0)
    got = reconstruction_delay(x, two_channel(x, h0, h1, f0, f1))
    assert got is not None and got[1] == 1


def test_misaligned_highpass_breaks_alias_cancellation():
    # Shifting the 5/3 highpass by one sample changes which phase is kept: no PR.
    rng = random.Random(24)
    x = [rng.uniform(-1, 1) for _ in range(30)]
    h1 = [0.0] + LEGALL_H1
    f0, f1 = alias_cancelling_synthesis(LEGALL_H0, h1)
    assert reconstruction_delay(x, two_channel(x, LEGALL_H0, h1, f0, f1)) is None


def test_polyphase_equals_direct():
    rng = random.Random(25)
    for _ in range(200):
        m = rng.randint(1, 4)
        x = [rng.uniform(-1, 1) for _ in range(rng.randint(1, 20))]
        hs = [[rng.uniform(-1, 1) for _ in range(rng.randint(1, 6))] for _ in range(m)]
        a = analysis(x, hs, m)
        b = analysis_polyphase(x, hs, m)
        for u, v in zip(a, b):
            assert close(u, v, 1e-12)


def test_block_dct_is_an_m_channel_filter_bank():
    # Analysis filters h_k[n] = c_k[M - 1 - n], synthesis filters f_k = c_k.
    m = 4
    c = [[(math.sqrt(1 / m) if k == 0 else math.sqrt(2 / m)) * math.cos(math.pi * (2 * i + 1) * k / (2 * m)) for i in range(m)] for k in range(m)]
    rng = random.Random(26)
    x = [rng.uniform(-1, 1) for _ in range(12)]
    sub = analysis([0.0] + x, [row[::-1] for row in c], m)
    for b in range(3):
        block = [sum(c[k][i] * x[b * m + i] for i in range(m)) for k in range(m)]
        assert close([sub[k][b + 1] for k in range(m)], block)
    got = reconstruction_delay(x, synthesis(analysis(x, [row[::-1] for row in c], m), c, m))
    assert got is not None and abs(got[0] - 1.0) < 1e-9 and got[1] == m - 1


def test_edges():
    assert convolve([], [1.0]) == []
    assert reconstruction_delay([0.0, 0.0], [0.0]) is None
    f0, f1 = alias_cancelling_synthesis(HAAR_H0, HAAR_H1)
    assert close(two_channel([1.0], HAAR_H0, HAAR_H1, f0, f1), [0.0, 1.0, 0.0])
