# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/offset-qpsk/. The authors are listed in prov/HPEG9T.jsonl.

import math
import random

from offset_qpsk import demodulate, levels, modulate, phase_steps, rrc_taps

LS = 8


def random_bits(seed: int, n: int) -> list[int]:
    rng = random.Random(seed)
    return [rng.randrange(2) for _ in range(n)]


def test_levels() -> None:
    a_i, a_q = levels([0, 1, 1, 1])
    s = 1 / math.sqrt(2)
    assert a_i == [s, -s] and a_q == [-s, -s]
    assert all(abs(complex(x, y)) == 1.0 or abs(abs(complex(x, y)) - 1) < 1e-15 for x, y in zip(a_i, a_q))


def test_rectangular_oqpsk_never_jumps_by_180_degrees() -> None:
    bits = random_bits(1, 400)
    s = modulate(bits, [1.0] * LS, LS, offset=True)
    nsym = len(bits) // 2
    # Between T/2 and the end of the last I pulse both branches are on, and |s| = 1.
    body = s[LS // 2 : nsym * LS]
    assert max(abs(abs(v) - 1) for v in body) < 1e-12
    steps = phase_steps(s, LS, LS // 2, 2 * nsym - 2)
    assert all(min(abs(d), abs(abs(d) - 90)) < 1e-9 for d in steps)
    assert any(abs(abs(d) - 90) < 1e-9 for d in steps)


def test_rectangular_qpsk_has_180_degree_jumps() -> None:
    bits = random_bits(1, 400)
    s = modulate(bits, [1.0] * LS, LS, offset=False)
    steps = phase_steps(s, LS, 0, len(bits) - 1)
    assert any(abs(abs(d) - 180) < 1e-9 for d in steps)
    assert all(min(abs(d), abs(abs(d) - 90), abs(abs(d) - 180)) < 1e-9 for d in steps)


def test_envelope_with_rrc_pulses() -> None:
    # beta = 0.5, ls = 8, span 8, seed 7, 1500 symbols: QPSK passes near zero, OQPSK does not.
    taps = rrc_taps(0.5, LS, 8)
    bits = random_bits(7, 3000)
    ratios = {}
    for offset in (False, True):
        s = modulate(bits, taps, LS, offset)
        env = [abs(v) for v in s[len(taps) + 50 * LS : (1500 - 50) * LS]]
        rms = math.sqrt(sum(e * e for e in env) / len(env))
        ratios[offset] = (min(env) / rms, max(env) / rms)
    assert ratios[False][0] < 0.05
    assert ratios[True][0] > 0.4
    assert ratios[True][1] < ratios[False][1]


def test_matched_filter_round_trip() -> None:
    taps = rrc_taps(0.35, LS, 8)
    bits = random_bits(3, 400)
    for offset in (False, True):
        r = modulate(bits, taps, LS, offset)
        assert demodulate(r, taps, LS, len(bits) // 2, offset) == bits


def test_no_isi_at_the_sampling_instants() -> None:
    taps = rrc_taps(0.35, LS, 8)
    bits = random_bits(4, 200)
    a_i, a_q = levels(bits)
    r = modulate(bits, taps, LS, True)
    d = len(taps) - 1
    for k in range(20, 80):
        zi = sum(r[k * LS + n] * h for n, h in enumerate(taps))
        zq = sum(r[k * LS + LS // 2 + n] * h for n, h in enumerate(taps))
        # The truncated filters leave a residual ISI below 1% of the level 1/sqrt(2).
        assert abs(zi.real - a_i[k]) < 5e-3
        assert abs(zq.imag - a_q[k]) < 5e-3
    assert d == 128
