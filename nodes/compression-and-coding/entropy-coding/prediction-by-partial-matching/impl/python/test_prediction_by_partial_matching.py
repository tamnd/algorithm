# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prediction-by-partial-matching/. The authors are listed in prov/3NN434.jsonl.

import math
import random

import pytest

from prediction_by_partial_matching import decode, encode, ideal_length, probabilities


def test_abracadabra_probabilities() -> None:
    msg = list(b"abracadabra")
    steps = probabilities(msg, 2)
    expected = [
        [1 / 256],
        [1 / 2, 1 / 255],
        [1 / 2, 1 / 254],
        [1 / 6],
        [1 / 2, 2 / 5, 1 / 253],
        [2 / 9],
        [1 / 2, 1 / 3, 1 / 252],
        [1 / 4],
        [1 / 6],
        [1 / 2],
        [1 / 2],
    ]
    assert [len(ev) for ev in steps] == [len(e) for e in expected]
    for ev, e in zip(steps, expected):
        assert [p for _, p in ev] == pytest.approx(e)
    assert [ev[-1][0] for ev in steps][-3:] == ["order 1", "order 2", "order 2"]
    code = encode(msg, 2)
    assert decode(code, len(msg), 2) == msg
    assert 8 * len(code) <= ideal_length(msg, 2) + 16


def test_roundtrip() -> None:
    rng = random.Random(1984)
    for trial in range(60):
        k = rng.randint(0, 4)
        sigma = rng.choice((2, 5, 256))
        n = rng.randint(0, 400)
        skew = rng.random() * 3
        data = [min(int(rng.random() ** skew * sigma), sigma - 1) for _ in range(n)]
        code = encode(data, k, sigma)
        assert decode(code, n, k, sigma) == data
    text = list(b"the theory of the thing is that the theme is there " * 20)
    for k in range(6):
        assert decode(encode(text, k), len(text), k) == text


def test_edges() -> None:
    assert decode(encode([], 3), 0, 3) == []
    assert decode(encode([7], 3), 1, 3) == [7]
    run = [0] * 5000
    code = encode(run, 3)
    assert decode(code, len(run), 3) == run
    assert len(code) < 30
    with pytest.raises(ValueError):
        encode([300], 2)


def _markov_text(n: int, seed: int) -> list[int]:
    rng = random.Random(seed)
    table = {}
    for a in range(8):
        for b in range(8):
            w = [rng.random() ** 3 for _ in range(8)]
            table[(a, b)] = w
    seq = [0, 0]
    while len(seq) < n:
        seq.append(rng.choices(range(8), weights=table[(seq[-2], seq[-1])])[0])
    return [97 + s for s in seq]


def test_beats_order_zero_on_markov_text() -> None:
    data = _markov_text(20000, 4)
    sizes = {k: len(encode(data, k)) for k in (0, 2, 3)}
    assert sizes[2] < 0.85 * sizes[0]
    assert sizes[3] < 0.9 * sizes[0]
    code = encode(data, 2)
    assert decode(code, len(data), 2) == data
    ideal = ideal_length(data, 2)
    assert ideal - 8 <= 8 * len(code) <= ideal + 0.001 * len(data) + 16
    # Order 0 with escapes is close to the order-0 empirical entropy of the text.
    n = len(data)
    h0 = -sum(c / n * math.log2(c / n) for c in (data.count(s) for s in set(data)))
    assert 8 * sizes[0] <= n * h0 + 0.01 * n + 200
