# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/repetition-penalty/. The authors are listed in prov/9K28B7.jsonl.

import math
import random

from nlslog import argmax, softmax
from repetition_penalty import additive_penalty, ctrl_penalty, scaled_penalty


def test_identity_settings() -> None:
    z = [2.0, -1.0, 0.0, 0.5]
    h = [0, 1, 1, 3]
    assert ctrl_penalty(z, h, 1.0) == z
    assert scaled_penalty(z, h, 1.0) == z
    assert additive_penalty(z, h, 0.0, 0.0) == z
    assert additive_penalty(z, [], 1.0, 1.0) == z


def test_division_alone_raises_a_negative_logit() -> None:
    z = [2.0, -1.0, 0.0]
    before = softmax(z)[1]
    after = softmax(ctrl_penalty(z, [1], 2.0))[1]
    assert after > before
    assert softmax(scaled_penalty(z, [1], 2.0))[1] < before


def test_sign_aware_scaling_never_raises_a_seen_token() -> None:
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(2, 8)
        z = [rng.uniform(-5, 5) for _ in range(n)]
        h = [rng.randrange(n) for _ in range(rng.randint(1, 5))]
        theta = rng.uniform(1.0, 3.0)
        p = softmax(z)
        zz = scaled_penalty(z, h, theta)
        q = softmax(zz)
        for j in range(n):
            if j in h:
                assert zz[j] <= z[j]
            else:
                assert q[j] >= p[j] - 1e-12
        if len(set(h)) == 1:
            assert q[h[0]] <= p[h[0]] + 1e-12
    # with two seen tokens, the weaker one can gain probability
    z = [4.0, 0.5, 0.0]
    p, q = softmax(z), softmax(scaled_penalty(z, [0, 1], 2.0))
    assert abs(p[1] - 0.0288) < 1e-4 and abs(q[1] - 0.1327) < 1e-4


def test_additive_form_has_exact_odds_and_ignores_shifts() -> None:
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(2, 8)
        z = [rng.uniform(-5, 5) for _ in range(n)]
        h = [rng.randrange(n) for _ in range(rng.randint(1, 6))]
        af, ap = rng.uniform(0, 1), rng.uniform(0, 1)
        p = softmax(z)
        q = softmax(additive_penalty(z, h, af, ap))
        # the odds of j against i change by exp(-(c_j af + [c_j > 0] ap) + (c_i af + [c_i > 0] ap))
        for i in range(n):
            for j in range(n):
                ci, cj = h.count(i), h.count(j)
                cost = lambda c: c * af + (ap if c > 0 else 0.0)
                want = math.log(p[j] / p[i]) - cost(cj) + cost(ci)
                assert abs(math.log(q[j] / q[i]) - want) < 1e-9
        c = rng.uniform(-50, 50)
        q2 = softmax(additive_penalty([x + c for x in z], h, af, ap))
        for a, b in zip(q, q2):
            assert abs(a - b) < 1e-9


def test_scaling_forms_depend_on_the_offset_of_the_logits() -> None:
    # the same probabilities, logits shifted by 3: the penalized results differ
    z = [2.0, 1.0, 0.0]
    shifted = [x - 3.0 for x in z]
    assert max(abs(a - b) for a, b in zip(softmax(z), softmax(shifted))) < 1e-12
    a = softmax(scaled_penalty(z, [0], 1.5))
    b = softmax(scaled_penalty(shifted, [0], 1.5))
    assert abs(a[0] - 0.5050) < 1e-4 and abs(b[0] - 0.5465) < 1e-4
    # a logit of exactly 0 is not changed by the scaling forms
    assert scaled_penalty([0.0, 1.0], [0], 5.0) == [0.0, 1.0]


def test_presence_counts_once_and_frequency_counts_each_time() -> None:
    z = [1.0, 1.0]
    assert additive_penalty(z, [0, 0, 0], 0.0, 0.5) == [0.5, 1.0]
    assert additive_penalty(z, [0, 0, 0], 0.5, 0.0) == [-0.5, 1.0]


def test_greedy_loop_is_broken() -> None:
    z = [2.0, 1.5, 1.0]
    plain, pen = [], []
    for _ in range(6):
        plain.append(argmax(z))
        pen.append(argmax(scaled_penalty(z, pen, 1.5)))
    assert plain == [0] * 6
    # the scaling counts presence only: once a and b are both seen, a wins again for good
    assert pen == [0, 1, 0, 0, 0, 0]
    add = []
    for _ in range(6):
        add.append(argmax(additive_penalty(z, add, 0.4, 0.0)))
    # the frequency penalty grows with each use and keeps rotating the tokens
    assert add == [0, 0, 1, 0, 1, 2]


def test_bad_theta() -> None:
    try:
        scaled_penalty([1.0], [0], 0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("no ValueError")
