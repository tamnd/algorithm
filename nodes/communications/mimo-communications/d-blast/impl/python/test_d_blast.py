# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-blast/. The authors are listed in prov/YCBK18.jsonl.

import math
import random

import pytest

import cbb
import constel
from d_blast import block_sinrs, dblast_detect, dblast_transmit, layer_map, nearest, rate_fraction


def rayleigh(rng, m, n):
    return [[cbb.cn(rng, 1.0) for _ in range(n)] for _ in range(m)]


def test_layer_map_and_rate() -> None:
    grid = layer_map(3, 4)
    assert grid == [[0, -1, -1], [1, 0, -1], [2, 1, 0], [3, 2, 1], [-1, 3, 2], [-1, -1, 3]]
    assert rate_fraction(3, 4) == 4 / 6
    for layer in range(4):  # every layer visits every antenna once
        assert sorted(k for row in grid for k in range(3) if row[k] == layer) == [0, 1, 2]


def test_example_on_the_page() -> None:
    h = [[2, 1], [1, 1]]
    assert layer_map(2, 3) == [[0, -1], [1, 0], [2, 1], [-1, 2]] and rate_fraction(2, 3) == 0.75
    zf = block_sinrs(h, 3, 1.0, 1.0, mmse=False)  # in units of Es/N0
    assert all(abs(a - b) < 1e-12 for a, b in zip(sum(zf, []), [5, 0.2, 5, 0.2, 5, 2]))
    mm = block_sinrs(h, 3, 1.0, 0.1)  # Es/N0 = 10 dB
    assert abs(mm[0][0] - 50) < 1e-9 and abs(mm[0][1] - 0.4 / 0.17) < 1e-9 and abs(mm[2][1] - 20) < 1e-9
    assert abs((1 + mm[1][0]) * (1 + mm[1][1]) - 171) < 1e-9  # det(I + 10 H^T H) = 171
    bpsk = constel.pam(2)
    x = [[[bpsk[0]], [bpsk[1]]], [[bpsk[1]], [bpsk[1]]], [[bpsk[0]], [bpsk[0]]]]
    ys = [cbb.matvec(h, v) for v in dblast_transmit(x, 2)]
    assert ys == [[2, 1], [-3, -2], [1, 0], [1, 1]]
    assert dblast_detect(ys, h, bpsk, 3) == [[[0], [1]], [[1], [1]], [[0], [0]]]


def test_transmit_puts_block_k_of_layer_l_on_antenna_k_at_time_l_plus_k() -> None:
    blocks = [[[complex(10 * l + k, s) for s in range(2)] for k in range(3)] for l in range(4)]
    xs = dblast_transmit(blocks, 3)
    assert len(xs) == 6 * 2
    for l in range(4):
        for k in range(3):
            for s in range(2):
                assert xs[(l + k) * 2 + s][k] == blocks[l][k][s]
    assert xs[0][1] == 0j and xs[11][0] == 0j


def test_noiseless_frames_are_recovered() -> None:
    rng = random.Random(1501)
    pts = constel.qam(16)
    for _ in range(25):
        n = rng.randint(1, 4)
        m = rng.randint(n, 5)
        layers = rng.randint(1, 5)
        h = rayleigh(rng, m, n)
        idx = [[[rng.randrange(16) for _ in range(2)] for _ in range(n)] for _ in range(layers)]
        blocks = [[[pts[i] for i in b] for b in lay] for lay in idx]
        ys = [cbb.matvec(h, x) for x in dblast_transmit(blocks, n)]
        assert dblast_detect(ys, h, pts, layers) == idx
        assert dblast_detect(ys, h, pts, layers, n0=1e-9, mmse=True) == idx
        rep = [[rng.randrange(16) for _ in range(3)] for _ in range(layers)]
        blocks = [[[pts[i] for i in r] for _ in range(n)] for r in rep]
        ys = [cbb.matvec(h, x) for x in dblast_transmit(blocks, n)]
        assert dblast_detect(ys, h, pts, layers, repeat=True) == rep


def test_first_block_of_a_layer_sees_maximal_ratio_combining() -> None:
    rng = random.Random(1502)
    h = rayleigh(rng, 3, 3)
    s = block_sinrs(h, 5, 1.0, 0.2)
    mrc = cbb.norm2([row[0] for row in h]) / 0.2
    assert all(abs(row[0] - mrc) < 1e-9 * mrc for row in s)


def test_middle_layer_sinrs_add_up_to_the_capacity() -> None:
    # theorem: for a layer l <= L - n, sum_k log2(1 + SINR_k) = log2 det(I + (Es/N0) H^H H)
    rng = random.Random(1503)
    for _ in range(30):
        n = rng.randint(1, 4)
        m = rng.randint(1, 5)
        layers = rng.randint(n, 6)
        h = rayleigh(rng, m, n)
        snr = rng.uniform(0.5, 30.0)
        g = cbb.matmul(cbb.herm(h), h)
        cap = math.log2(abs(cbb.det(cbb.add(cbb.eye(n), cbb.scale(snr, g)))))
        s = block_sinrs(h, layers, 1.0, 1.0 / snr)
        for l in range(layers - n + 1):
            assert abs(sum(math.log2(1 + v) for v in s[l]) - cap) < 1e-9 * (1 + cap)
        for l in range(layers - n + 1, layers):  # the last layers see fewer interferers
            assert sum(math.log2(1 + v) for v in s[l]) >= cap - 1e-9


def test_bad_arguments() -> None:
    with pytest.raises(ValueError):
        dblast_detect([[0j]] * 3, [[1, 1]], constel.pam(2), 2, n0=0.0, mmse=True)
    with pytest.raises(ValueError):
        dblast_detect([[0j]] * 4, [[1, 1]], constel.pam(2), 2)
    with pytest.raises(ValueError):
        dblast_detect([[0j]] * 3, [[1, 1]], constel.pam(2), 2)  # ZF with n > m


def test_diagonal_repetition_beats_vertical_repetition_in_slow_fading() -> None:
    # measured: 4-QAM, m = n = 2, L = 6, Es/N0 = 6 dB, seed 1505, 300 frames of 6 symbols each
    rng = random.Random(1505)
    pts = constel.qam(4)
    n, m, layers = 2, 2, 6
    n0 = 1 / cbb.undb(6.0)
    err_d = err_v = 0
    for _ in range(300):
        h = rayleigh(rng, m, n)
        data = [rng.randrange(4) for _ in range(layers)]
        blocks = [[[pts[d]] for _ in range(n)] for d in data]
        ys = [cbb.awgn(rng, cbb.matvec(h, x), n0) for x in dblast_transmit(blocks, n)]
        got = dblast_detect(ys, h, pts, layers, n0, mmse=True, repeat=True)
        err_d += sum(g[0] != d for g, d in zip(got, data))
        for _ in range(layers // n):  # each antenna repeats its own symbol n times
            idx = [rng.randrange(4) for _ in range(n)]
            x = [pts[i] for i in idx]
            ysum = [0j] * m
            for _ in range(n):
                ysum = cbb.add(ysum, cbb.awgn(rng, cbb.matvec(h, x), n0))
            err_v += sum(a != b for a, b in zip(mmse_sic([v / n for v in ysum], h, pts, n0 / n), idx))
    print(err_d, err_v)
    assert 2 * err_d < err_v


def mmse_sic(y, h, pts, a):
    """MMSE nulling and cancelling with the V-BLAST order, for the vertical baseline."""
    r, rem, out = list(y), list(range(len(h[0]))), [0] * len(h[0])
    while rem:
        hk = [[row[c] for c in rem] for row in h]
        g = cbb.add(cbb.matmul(cbb.herm(hk), hk), cbb.scale(a, cbb.eye(len(rem))))
        p = cbb.inv(g)
        w = cbb.matmul(p, cbb.herm(hk))
        i = min(range(len(rem)), key=lambda t: p[t][t].real)
        k = rem.pop(i)
        out[k] = nearest(sum(c * v for c, v in zip(w[i], r)) / (1 - a * p[i][i].real), pts)
        r = [rv - row[k] * pts[out[k]] for rv, row in zip(r, h)]
    return out
