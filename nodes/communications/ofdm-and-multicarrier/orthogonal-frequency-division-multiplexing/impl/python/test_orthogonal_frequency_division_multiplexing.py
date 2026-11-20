# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orthogonal-frequency-division-multiplexing/. The authors are listed in prov/2QCF2N.jsonl.

import cmath
import math
import random

import cbb
from orthogonal_frequency_division_multiplexing import (
    channel_response,
    demodulate,
    equalize,
    fft,
    modulate,
    receive,
    transmit,
    ufft,
    uifft,
)

S = 1 / math.sqrt(2)


def qpsk(rng: random.Random, n: int) -> list[complex]:
    """n unit-energy 4-QAM symbols (+-1 +-j) / sqrt(2)."""
    return [complex(rng.choice((S, -S)), rng.choice((S, -S))) for _ in range(n)]


def slice_qpsk(z: complex) -> complex:
    return complex(S if z.real >= 0 else -S, S if z.imag >= 0 else -S)


def maxerr(a: list[complex], b: list[complex]) -> float:
    return max(abs(x - y) for x, y in zip(a, b))


def test_fft_matches_the_direct_dft() -> None:
    rng = random.Random(1)
    for n in (1, 2, 4, 8, 64, 256, 12):
        x = [cbb.cn(rng, 1.0) for _ in range(n)]
        assert maxerr(fft(x), cbb.dft(x)) < 1e-9 * max(1, n)
        assert maxerr([v / n for v in fft(x, inverse=True)], cbb.idft(x)) < 1e-9
        assert maxerr(ufft(x), cbb.udft(x)) < 1e-9
        assert maxerr(uifft(ufft(x)), x) < 1e-12 * max(1, n)


def test_parseval_with_the_unitary_pair() -> None:
    rng = random.Random(2)
    xf = qpsk(rng, 64)
    s = modulate(xf, 0)
    assert abs(cbb.norm2(s) - cbb.norm2(xf)) < 1e-9
    assert abs(cbb.norm2(xf) - 64) < 1e-9


def test_prefix_is_a_copy_of_the_tail() -> None:
    rng = random.Random(3)
    xf = qpsk(rng, 16)
    s = modulate(xf, 4)
    assert len(s) == 20
    assert s[:4] == s[16:]


def test_round_trip_without_channel() -> None:
    rng = random.Random(4)
    for n, ncp in ((8, 0), (64, 16), (256, 32)):
        xf = qpsk(rng, n)
        assert maxerr(demodulate(modulate(xf, ncp), n, ncp), xf) < 1e-12


def test_one_tap_per_subcarrier_through_a_channel() -> None:
    rng = random.Random(5)
    channels = [
        [1.0, 0.5],
        [0.407, 0.815, 0.407],  # Proakis channel B
        [cbb.cn(rng, 1 / 8) for _ in range(8)],
    ]
    n, ncp = 64, 7
    for h in channels:
        xf = qpsk(rng, n)
        r = cbb.conv(modulate(xf, ncp), h)
        yf = demodulate(r, n, ncp)
        hf = channel_response(h, n)
        assert maxerr(hf, cbb.dft(list(h) + [0] * (n - len(h)))) < 1e-9
        assert maxerr(yf, [a * b for a, b in zip(hf, xf)]) < 1e-9
        assert maxerr(equalize(yf, hf), xf) < 1e-9


def test_a_stream_of_symbols_keeps_them_apart() -> None:
    rng = random.Random(6)
    n, ncp, count = 32, 4, 6
    h = [0.8, -0.4j, 0.3, 0.2 + 0.1j, 0.1]  # 5 taps, ncp = L - 1
    blocks = [qpsk(rng, n) for _ in range(count)]
    r = cbb.conv(transmit(blocks, ncp), h)
    out = receive(r, h, n, ncp, count)
    for xf, xh in zip(blocks, out):
        assert maxerr(xh, xf) < 1e-9


def test_a_short_prefix_leaves_interference() -> None:
    rng = random.Random(7)
    n, h = 32, [0.8, -0.4j, 0.3, 0.2 + 0.1j, 0.1]
    blocks = [qpsk(rng, n) for _ in range(3)]
    for ncp in (2, 3):  # ncp < L - 1 = 4
        r = cbb.conv(transmit(blocks, ncp), h)
        out = receive(r, h, n, ncp, 3)
        assert maxerr(out[1], blocks[1]) > 1e-3


def test_symbol_error_rate_matches_the_per_subcarrier_formula() -> None:
    # Es = 1 on each subcarrier, time-domain noise CN(0, N0), Es/N0 = 10 dB, h = (1, 0.5).
    # With the unitary DFT, W[k] is CN(0, N0), so subcarrier k sees SNR |H[k]|^2 / N0
    # and the 4-QAM symbol error rate 2Q(sqrt(g)) - Q(sqrt(g))^2. The mean over k is
    # 0.018549, so 200 symbols of 64 subcarriers (12800 trials, seed 8) expect about 237 errors.
    rng = random.Random(8)
    n, ncp, n0, h, count = 64, 8, 0.1, [1.0, 0.5], 200
    hf = channel_response(h, n)
    expect = 0.0
    for hk in hf:
        q = cbb.qfunc(math.sqrt(abs(hk) ** 2 / n0))
        expect += (2 * q - q * q) / n
    assert abs(expect - 0.018549) < 1e-6
    errors = 0
    for _ in range(count):
        xf = qpsk(rng, n)
        r = cbb.awgn(rng, cbb.conv(modulate(xf, ncp), h), n0)
        xh = equalize(demodulate(r, n, ncp), hf)
        errors += sum(slice_qpsk(z) != x for z, x in zip(xh, xf))
    lo, hi = cbb.wilson(errors, count * n)
    assert lo <= expect <= hi


def test_flat_channel_check_value() -> None:
    q = cbb.qfunc(math.sqrt(10.0))
    assert abs(2 * q - q * q - 1.5648e-3) < 1e-7


def test_rate_loss_and_spacing() -> None:
    # 802.11a-like numbers: N = 64, ncp = 16, sample rate 20 MHz.
    n, ncp, fs = 64, 16, 20e6
    assert n / (n + ncp) == 0.8
    assert fs / n == 312500.0
    assert abs((n + ncp) / fs - 4e-6) < 1e-15
    assert cmath.isclose(channel_response([1.0], 4)[2], 1)
