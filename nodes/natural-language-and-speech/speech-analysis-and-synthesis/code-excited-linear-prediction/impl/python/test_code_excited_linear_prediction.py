# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/code-excited-linear-prediction/. The authors are listed in prov/X96A2P.jsonl.

import itertools
import random

from code_excited_linear_prediction import (
    Filters,
    adaptive_vector,
    bandwidth_expand,
    convolve,
    decode,
    dot,
    encode,
    impulse_response,
    random_codebook,
    search,
    snr_db,
)
from nlsdsp import all_pole, pulse_train

FS = 8000


def vowel(seed=7, n=1280):
    rng = random.Random(seed)
    src = [p + 0.05 * rng.gauss(0, 1) for p in pulse_train(125, FS, n)]
    s = all_pole(src, [1.662983, -0.81])
    peak = max(abs(v) for v in s)
    return [0.5 * v / peak for v in s]


def error(t, y, g):
    return sum((a - g * b) ** 2 for a, b in zip(t, y))


def test_search_matches_brute_force_on_tiny_codebooks():
    rng = random.Random(1)
    for _ in range(40):
        n = 4
        h = [rng.uniform(-1, 1) for _ in range(n)]
        t = [rng.uniform(-1, 1) for _ in range(n)]
        book = [[rng.choice((-1.0, 0.0, 1.0)) for _ in range(n)] for _ in range(6)]
        ys = [convolve(h, c) for c in book]
        k, g, err = search(t, ys)
        # brute force over the vectors and over gains on a fine grid
        grid = [i / 200 for i in range(-1000, 1001)]
        brute = min(error(t, y, gg) for y in ys for gg in grid)
        assert err <= brute + 1e-12
        assert abs(err - error(t, ys[k], g)) < 1e-9
        assert all(err <= error(t, y, dot(t, y) / dot(y, y)) + 1e-12 for y in ys if dot(y, y) > 0)


def test_search_example_of_the_page():
    t = [1.0, 0.5, -0.25, 0.0]
    h = [1.0, 0.5, 0.25, 0.125]
    book = [[1, 0, 0, 0], [0, 1, 0, 0], [1, -1, 0, 0], [0.5, 0.5, 0.5, 0.5]]
    ys = [convolve(h, c) for c in book]
    assert ys[2] == [1.0, -0.5, -0.25, -0.125]
    k, g, err = search(t, ys)
    assert k == 0
    assert abs(g - 1.1875 / 1.328125) < 1e-15
    assert abs(err - (1.3125 - 1.1875**2 / 1.328125)) < 1e-15


def test_weighted_error_is_affine_in_the_excitation():
    rng = random.Random(2)
    a = [1.2, -0.6, 0.1]
    w1, w2 = bandwidth_expand(a, 0.9), bandwidth_expand(a, 0.6)
    state = Filters(3)
    state.run([rng.uniform(-1, 1) for _ in range(30)], [rng.uniform(-1, 1) for _ in range(30)], a, w1, w2)
    s = [rng.uniform(-1, 1) for _ in range(20)]
    e = [rng.uniform(-1, 1) for _ in range(20)]
    _, t = state.copy().run(s, [0.0] * 20, a, w1, w2)
    _, ew = state.copy().run(s, e, a, w1, w2)
    he = convolve(impulse_response(a, w1, w2, 20), e)
    assert max(abs(x - (u - v)) for x, u, v in zip(ew, t, he)) < 1e-12


def test_equal_gammas_give_no_weighting():
    a = [1.2, -0.6]
    h = impulse_response(a, bandwidth_expand(a, 0.8), bandwidth_expand(a, 0.8), 30)
    plain = all_pole([1.0] + [0.0] * 29, a)
    assert max(abs(x - y) for x, y in zip(h, plain)) < 1e-12


def test_adaptive_vector_repeats_short_lags():
    past = [float(i) for i in range(10)]
    assert adaptive_vector(past, 4, 7) == [6.0, 7.0, 8.0, 9.0, 6.0, 7.0, 8.0]
    assert adaptive_vector(past, 8, 5) == [2.0, 3.0, 4.0, 5.0, 6.0]


def test_exact_recovery_when_the_excitation_is_in_the_codebook():
    rng = random.Random(3)
    book = random_codebook(16, 20, seed=5)
    a = [1.3, -0.7]
    choice = [(rng.randrange(16), rng.uniform(0.5, 2.0) * rng.choice((-1, 1))) for _ in range(8)]
    e = [g * x for k, g in choice for x in book[k]]
    s = all_pole(e, a)
    params, out = encode(s, book, order=2, frame_len=40, sub_len=20, lags=None, lpc_given=[a] * 4)
    assert [p["k"] for p in params] == [k for k, _ in choice]
    assert all(abs(p["g_f"] - g) < 1e-9 for p, (_, g) in zip(params, choice))
    assert max(abs(x - y) for x, y in zip(out, s)) < 1e-9


def test_decoder_matches_the_encoder_and_the_pitch_lag_is_found():
    s = vowel()
    book = random_codebook(128, 40)
    params, out = encode(s, book)
    assert decode(params, book) == out  # the encoder runs the same decoder
    lags = [p["lag"] for p in params[4:]]
    assert sum(1 for t in lags if t in (63, 64, 65, 127, 128, 129)) >= 0.5 * len(lags)  # period 64 or twice it


def test_adaptive_codebook_raises_the_snr():
    s = vowel()
    book = random_codebook(128, 40)
    with_pitch = snr_db(s, encode(s, book)[1])
    without = snr_db(s, encode(s, book, lags=None)[1])
    assert with_pitch > 8.0  # a measurement on this signal, without quantization
    assert with_pitch > without + 3.0


def test_sequential_search_is_no_better_than_joint_search():
    rng = random.Random(4)
    for _ in range(50):
        t = [rng.uniform(-1, 1) for _ in range(5)]
        ya = [[rng.uniform(-1, 1) for _ in range(5)] for _ in range(3)]
        yf = [[rng.uniform(-1, 1) for _ in range(5)] for _ in range(3)]
        j, ga, _ = search(t, ya)
        rest = [x - ga * y for x, y in zip(t, ya[j])]
        _, _, seq = search(rest, yf)
        best = min(
            error(t, [p * ga2 + q * gf2 for p, q in zip(u, v)], 1.0)
            for u, v in itertools.product(ya, yf)
            for ga2, gf2 in [solve2(t, u, v)]
        )
        assert best <= seq + 1e-12


def solve2(t, u, v):
    """The least squares gains of t ~ ga u + gf v."""
    uu, vv, uv, tu, tv = dot(u, u), dot(v, v), dot(u, v), dot(t, u), dot(t, v)
    det = uu * vv - uv * uv
    return (tu * vv - tv * uv) / det, (tv * uu - tu * uv) / det
