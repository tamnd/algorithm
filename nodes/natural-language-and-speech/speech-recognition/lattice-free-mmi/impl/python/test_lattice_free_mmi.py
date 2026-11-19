# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lattice-free-mmi/. The authors are listed in prov/JBKG30.jsonl.

import math
import random

import pytest

import nlslog
from lattice_free_mmi import (
    brute_force_log_z,
    denominator_graph,
    estimate_phone_bigram,
    forward_backward_log,
    forward_backward_scaled,
    leaky_init,
    lfmmi_objective,
    lfmmi_objective_and_grad,
    numerator_graph,
    with_leaky_arcs,
)
from nlslog import log_add

Q = [[0.6, 0.1, 0.2, 0.1], [0.2, 0.3, 0.4, 0.1], [0.1, 0.1, 0.3, 0.5]]


def example():
    den = denominator_graph([0.5, 0.5], [[0.5, 0.5], [0.5, 0.5]])
    num = numerator_graph([0, 1], den)
    y = [[math.log(v) for v in row] for row in Q]
    return y, num, den


def random_bigram(rng, P):
    start = [rng.random() + 0.1 for _ in range(P)]
    start = [x / sum(start) for x in start]
    bigram = []
    for _ in range(P):
        row = [rng.random() + 0.1 for _ in range(P)]
        bigram.append([x / sum(row) for x in row])
    return start, bigram


def random_outputs(rng, T, P, scale=2.0):
    return [[rng.uniform(-scale, scale) for _ in range(2 * P)] for _ in range(T)]


def test_helper_header():
    with open(nlslog.__file__, encoding="utf-8") as f:
        lines = f.read().splitlines()
    assert lines[1] == "# Shared helper of the natural-language-and-speech pages of https://algorithm.tamnd.com/. The authors are listed in prov/."


def test_log_add_check_value():
    assert log_add(math.log(0.5), math.log(0.25)) == pytest.approx(-0.287682, abs=1e-6)


def test_initial_probabilities_by_averaging():
    den = denominator_graph([0.5, 0.5], [[0.5, 0.5], [0.5, 0.5]])
    assert leaky_init(den) == pytest.approx([0.2525, 0.2475, 0.2525, 0.2475], abs=1e-12)
    rng = random.Random(1)
    start, bigram = random_bigram(rng, 4)
    init = leaky_init(denominator_graph(start, bigram))
    assert sum(init) == pytest.approx(1.0, abs=1e-12)
    # The graph is stochastic: the weights out of each state sum to 1.
    g = denominator_graph(start, bigram)
    for i in range(len(g.pdf)):
        assert math.fsum(math.exp(w) for _, w in g.outgoing[i]) == pytest.approx(1.0, abs=1e-12)


def test_page_example():
    y, num, den = example()
    lz_num, g_num = forward_backward_log(num, y)
    assert math.exp(lz_num) == pytest.approx(0.2525 * 0.125 * (0.12 + 0.054), abs=1e-15)
    assert g_num[1] == pytest.approx([0.0, 0.054 / 0.174, 0.12 / 0.174, 0.0], abs=1e-12)
    F, grad, _, g_den = lfmmi_objective_and_grad(y, num, den, leaky=0.0)
    assert math.exp(lz_num - F) == pytest.approx(0.01597125, abs=1e-12)
    assert F == pytest.approx(-1.067521, abs=1e-6)
    assert grad[0] == pytest.approx([0.3834, -0.1007, -0.1897, -0.0930], abs=1e-4)
    F, _, _, _ = lfmmi_objective_and_grad(y, num, den, leaky=0.1)
    assert math.exp(lz_num - F) == pytest.approx(0.019400699, abs=1e-9)
    assert F == pytest.approx(-1.262039, abs=1e-6)


def test_denominator_against_brute_force():
    rng = random.Random(2)
    for _ in range(12):
        P = rng.randint(1, 2)
        T = rng.randint(1, 4)
        start, bigram = random_bigram(rng, P)
        den = denominator_graph(start, bigram)
        y = random_outputs(rng, T, P)
        for leaky in (0.0, 0.1, 0.5):
            lz, gamma = forward_backward_scaled(den, y, leaky)
            assert lz == pytest.approx(brute_force_log_z(with_leaky_arcs(den, leaky), y), abs=1e-10)
            for t in range(T):
                assert sum(gamma[t]) == pytest.approx(1.0, abs=1e-12)


def test_scaled_and_log_forward_backward_agree():
    rng = random.Random(3)
    start, bigram = random_bigram(rng, 3)
    den = denominator_graph(start, bigram)
    for leaky in (0.0, 0.1):
        y = random_outputs(rng, 30, 3, scale=40.0)
        lz_s, g_s = forward_backward_scaled(den, y, leaky)
        lz_l, g_l = forward_backward_log(with_leaky_arcs(den, leaky), y)
        assert lz_s == pytest.approx(lz_l, rel=1e-12)
        for t in range(30):
            assert g_s[t] == pytest.approx(g_l[t], abs=1e-10)


def test_long_chunk_does_not_underflow():
    # 300 frames with outputs near -40: exp(-40 * 300) underflows, the scaled pass does not.
    rng = random.Random(4)
    start, bigram = random_bigram(rng, 2)
    den = denominator_graph(start, bigram)
    y = [[-40.0 + rng.uniform(-1, 1) for _ in range(4)] for _ in range(300)]
    lz_s, _ = forward_backward_scaled(den, y, 0.1)
    lz_l, _ = forward_backward_log(with_leaky_arcs(den, 0.1), y)
    assert math.isfinite(lz_s)
    assert lz_s == pytest.approx(lz_l, rel=1e-12)
    assert lz_s < -11000


def test_numerator_windows_against_brute_force():
    rng = random.Random(5)
    start, bigram = random_bigram(rng, 3)
    den = denominator_graph(start, bigram)
    for _ in range(20):
        T = rng.randint(2, 6)
        phones = [rng.randrange(3) for _ in range(rng.randint(1, min(3, T)))]
        windows = None
        if rng.random() < 0.6:
            windows = []
            for k in range(len(phones)):
                c = round((k + 0.5) * T / len(phones))
                windows.append((max(0, c - 2), min(T - 1, c + 1)))
        num = numerator_graph(phones, den, windows)
        y = random_outputs(rng, T, 3)
        bf = brute_force_log_z(num, y)
        if bf == -math.inf:
            with pytest.raises(ValueError):
                forward_backward_log(num, y)
            continue
        lz, gamma = forward_backward_log(num, y)
        assert lz == pytest.approx(bf, abs=1e-10)
        # Every numerator path is a denominator path with the same score.
        assert lz <= forward_backward_scaled(den, y, 0.0)[0] + 1e-12


def test_gradient_against_finite_differences():
    rng = random.Random(6)
    start, bigram = random_bigram(rng, 2)
    den = denominator_graph(start, bigram)
    h = 1e-6
    for leaky, l2 in ((0.0, 0.0), (0.1, 0.0005), (0.3, 0.1)):
        T = 5
        num = numerator_graph([0, 1, 1], den, [(0, 2), (1, 3), (2, 4)])
        y = random_outputs(rng, T, 2)
        F, grad, _, _ = lfmmi_objective_and_grad(y, num, den, leaky, l2)
        assert F <= 0
        for t in range(T):
            for p in range(4):
                up = [r[:] for r in y]
                dn = [r[:] for r in y]
                up[t][p] += h
                dn[t][p] -= h
                fd = (lfmmi_objective(up, num, den, leaky, l2) - lfmmi_objective(dn, num, den, leaky, l2)) / (2 * h)
                assert grad[t][p] == pytest.approx(fd, abs=1e-5)
            # Both posteriors sum to 1, so only the l2 term is left in the sum.
            assert sum(grad[t]) == pytest.approx(-l2 * sum(y[t]), abs=1e-12)


def test_estimate_phone_bigram():
    start, bigram = estimate_phone_bigram([[0, 1, 1], [1, 0], [0, 1]], 3)
    assert start == pytest.approx([2 / 3, 1 / 3, 0.0])
    assert bigram[0] == pytest.approx([0.0, 1.0, 0.0])
    assert bigram[1] == pytest.approx([0.5, 0.5, 0.0])
    assert bigram[2] == pytest.approx([1 / 3, 1 / 3, 1 / 3])
    den = denominator_graph(start, bigram)
    with pytest.raises(ValueError):
        numerator_graph([0, 0], den)  # the bigram gives 0 to a -> a
    with pytest.raises(ValueError):
        numerator_graph([2], den)  # phone 2 never starts a sequence and is never reached


def test_no_path_raises():
    y, num, den = example()
    short = numerator_graph([0, 1, 0, 1], den)
    with pytest.raises(ValueError):
        forward_backward_log(short, y)  # 4 phones need 4 frames
    windowed = numerator_graph([0, 1], den, [(0, 0), (0, 0)])
    with pytest.raises(ValueError):
        forward_backward_log(windowed, y)
