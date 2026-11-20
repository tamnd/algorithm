# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subspace-channel-identification/. The authors are listed in prov/8ZFGWM.jsonl.

import math
import random

import pytest

from subspace_channel_identification import (
    block_toeplitz,
    hermitian_eigh,
    identify_from_samples,
    q_eigenvalues,
    subspace_identify,
)


def conv(a, b):
    out = [0j] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for k, y in enumerate(b):
            out[i + k] += x * y
    return out


def stack_subchannels(subs):
    # h[l * P + p] is tap l of subchannel p
    return [complex(subs[p][l]) for l in range(len(subs[0])) for p in range(len(subs))]


def exact_covariance(h, p, n, s2):
    hn = block_toeplitz(h, p, n)
    d = len(hn)
    return [[sum(hn[i][m] * hn[k][m].conjugate() for m in range(len(hn[0]))) + (s2 if i == k else 0) for k in range(d)] for i in range(d)]


def misalignment(he, h):
    # 1 - |he^H h|^2 / (|he|^2 |h|^2): 0 when he is a scalar times h
    ip = sum(a.conjugate() * b for a, b in zip(he, h))
    return 1 - abs(ip) ** 2 / (sum(abs(v) ** 2 for v in he) * sum(abs(v) ** 2 for v in h))


H3 = stack_subchannels([[1, 0.5 + 0.2j, -0.3], [0.4j, 1, 0.6]])


def test_hermitian_eigensolver() -> None:
    rng = random.Random(1)
    n = 5
    a = [[0j] * n for _ in range(n)]
    for i in range(n):
        a[i][i] = complex(rng.gauss(0, 1))
        for k in range(i + 1, n):
            a[i][k] = complex(rng.gauss(0, 1), rng.gauss(0, 1))
            a[k][i] = a[i][k].conjugate()
    vals, vecs = hermitian_eigh(a)
    assert all(vals[i] <= vals[i + 1] for i in range(len(vals) - 1))
    for lam, v in zip(vals, vecs):
        av = [sum(a[i][k] * v[k] for k in range(n)) for i in range(n)]
        assert max(abs(x - lam * y) for x, y in zip(av, v)) < 1e-10


def test_hand_example() -> None:
    # subchannels (1, 0.5) and (0.5, 1), N = 2: the noise vector is (-1, 2, -2, 1) up to scale
    h = stack_subchannels([[1, 0.5], [0.5, 1]])
    r = exact_covariance(h, 2, 2, 0.3)
    vals, vecs = hermitian_eigh(r)
    g = vecs[0]
    ref = [-1, 2, -2, 1]
    assert misalignment(g, [complex(v) for v in ref]) < 1e-12
    assert abs(vals[0] - 0.3) < 1e-10
    he = subspace_identify(r, 2, 2, 2)
    assert misalignment(he, h) < 1e-12


def test_exact_covariance_gives_the_channel_up_to_a_scalar() -> None:
    for n in (3, 4):
        he = subspace_identify(exact_covariance(H3, 2, n, 0.1), 2, 3, n)
        assert misalignment(he, H3) < 1e-12
        assert abs(sum(abs(v) ** 2 for v in he) - 1) < 1e-12


def test_sample_covariance_gives_a_small_error() -> None:
    rng = random.Random(1)
    k = 2000
    s = math.sqrt(0.005)
    a = [complex(rng.choice((-1, 1)), rng.choice((-1, 1))) / math.sqrt(2) for _ in range(k)]
    y = [
        [sum(H3[l * 2 + q] * a[t - l] for l in range(3) if t - l >= 0) + complex(rng.gauss(0, s), rng.gauss(0, s)) for q in range(2)]
        for t in range(k)
    ]
    for n in (3, 4):
        assert misalignment(identify_from_samples(y, 2, 3, n), H3) < 0.005


def test_a_common_zero_makes_the_channel_unidentifiable() -> None:
    common = stack_subchannels([conv([1, -0.5], [1, 0.3]), conv([1, -0.5], [0.2, 1])])
    q_bad = q_eigenvalues(exact_covariance(common, 2, 3, 0.1), 2, 3, 3)
    q_good = q_eigenvalues(exact_covariance(H3, 2, 3, 0.1), 2, 3, 3)
    # each eigenvalue appears twice; entries 0, 1 are the null vector, entries 2, 3 the next one
    assert abs(q_bad[2]) < 1e-10
    assert q_good[2] > 1e-3


def test_bad_input() -> None:
    r = exact_covariance(H3, 2, 3, 0.1)
    with pytest.raises(ValueError):
        subspace_identify(r, 2, 3, 2)
    with pytest.raises(ValueError):
        subspace_identify(r, 1, 3, 6)
