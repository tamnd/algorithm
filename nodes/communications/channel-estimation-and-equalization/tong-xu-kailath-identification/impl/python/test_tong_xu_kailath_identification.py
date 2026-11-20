# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tong-xu-kailath-identification/. The authors are listed in prov/WX9EA1.jsonl.

import math
import random

import pytest

from tong_xu_kailath_identification import block_toeplitz, correlations, hermitian_eigh, txk_identify


def conv(a, b):
    out = [0j] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for k, y in enumerate(b):
            out[i + k] += x * y
    return out


def stack_subchannels(subs):
    return [complex(subs[p][l]) for l in range(len(subs[0])) for p in range(len(subs))]


def exact_correlations(h, p, n, s2):
    hn = block_toeplitz(h, p, n)
    d, c = len(hn), len(hn[0])
    r0 = [[sum(hn[i][m] * hn[k][m].conjugate() for m in range(c)) + (s2 if i == k else 0) for k in range(d)] for i in range(d)]
    r1 = [[sum(hn[i][m] * hn[k][m - 1].conjugate() for m in range(1, c)) + (s2 if i == k + p else 0) for k in range(d)] for i in range(d)]
    return r0, r1


def phase_aligned_error(he, h):
    # max |e^(j phi) he - h| over the entries, with the best phase phi
    ip = sum(a.conjugate() * b for a, b in zip(he, h))
    ph = ip / abs(ip)
    return max(abs(a * ph - b) for a, b in zip(he, h))


H3 = stack_subchannels([[1, 0.5 + 0.2j, -0.3], [0.4j, 1, 0.6]])


def test_eigensolver_splits_the_pairs() -> None:
    rng = random.Random(2)
    n = 4
    a = [[0j] * n for _ in range(n)]
    for i in range(n):
        a[i][i] = complex(rng.gauss(0, 1))
        for k in range(i + 1, n):
            a[i][k] = complex(rng.gauss(0, 1), rng.gauss(0, 1))
            a[k][i] = a[i][k].conjugate()
    vals, vecs = hermitian_eigh(a)
    assert len(vals) == n
    for lam, v in zip(vals, vecs):
        av = [sum(a[i][k] * v[k] for k in range(n)) for i in range(n)]
        assert max(abs(x - lam * y) for x, y in zip(av, v)) < 1e-10
    for i in range(n):
        for k in range(n):
            ip = sum(x.conjugate() * y for x, y in zip(vecs[i], vecs[k]))
            assert abs(ip - (1 if i == k else 0)) < 1e-10


def test_hand_example() -> None:
    h = stack_subchannels([[1, 0.5], [0.5, 1]])
    r0, r1 = exact_correlations(h, 2, 2, 0.3)
    he = txk_identify(r0, r1, 2, 2, 2, 0.3)
    assert phase_aligned_error(he, h) < 1e-9


def test_exact_statistics_give_the_channel_up_to_a_phase() -> None:
    for n in (3, 4):
        r0, r1 = exact_correlations(H3, 2, n, 0.1)
        assert phase_aligned_error(txk_identify(r0, r1, 2, 3, n, 0.1), H3) < 1e-9
        # the noise power estimated from the smallest eigenvalues of R(0) is exact too
        assert phase_aligned_error(txk_identify(r0, r1, 2, 3, n), H3) < 1e-9


def test_sample_statistics_give_a_small_error() -> None:
    rng = random.Random(1)
    k = 3000
    s = math.sqrt(0.005)
    a = [complex(rng.choice((-1, 1)), rng.choice((-1, 1))) / math.sqrt(2) for _ in range(k)]
    y = [
        [sum(H3[l * 2 + q] * a[t - l] for l in range(3) if t - l >= 0) + complex(rng.gauss(0, s), rng.gauss(0, s)) for q in range(2)]
        for t in range(k)
    ]
    norm = math.sqrt(sum(abs(v) ** 2 for v in H3))
    for n in (3, 4):
        r0, r1 = correlations(y, n)
        assert phase_aligned_error(txk_identify(r0, r1, 2, 3, n), H3) / norm < 0.05


def test_a_common_zero_flipped_by_an_allpass_gives_the_same_statistics() -> None:
    # (1 - 0.5 z^-1) and (-0.5 + z^-1) have the same magnitude on the unit circle
    q1, q2 = [1, 0.3], [0.2, 1]
    ha = stack_subchannels([conv([1, -0.5], q1), conv([1, -0.5], q2)])
    hb = stack_subchannels([conv([-0.5, 1], q1), conv([-0.5, 1], q2)])
    a0, a1 = exact_correlations(ha, 2, 3, 0.1)
    b0, b1 = exact_correlations(hb, 2, 3, 0.1)
    assert max(abs(a0[i][k] - b0[i][k]) for i in range(6) for k in range(6)) < 1e-12
    assert max(abs(a1[i][k] - b1[i][k]) for i in range(6) for k in range(6)) < 1e-12
    assert phase_aligned_error(ha, hb) > 0.1


def test_bad_input() -> None:
    r0, r1 = exact_correlations(H3, 2, 3, 0.1)
    with pytest.raises(ValueError):
        txk_identify(r0, r1, 2, 3, 2)
    with pytest.raises(ValueError):
        txk_identify(r0, r1, 1, 3, 6)
