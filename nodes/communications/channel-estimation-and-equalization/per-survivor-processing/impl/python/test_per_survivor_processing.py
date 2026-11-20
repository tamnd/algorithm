# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/per-survivor-processing/. The authors are listed in prov/24BB6C.jsonl.

import math
import random
from itertools import product

import pytest

from per_survivor_processing import drifting_channel, psp_viterbi, transmit


def ml_by_search(y, f, pre, alphabet=(-1.0, 1.0)):
    best = None
    for x in product(alphabet, repeat=len(y)):
        r = transmit(list(x), [f] * len(y), pre)
        cost = sum((a - b) ** 2 for a, b in zip(y, r))
        if best is None or cost < best[0]:
            best = (cost, list(x))
    return best[1]


def genie_viterbi(y, taps, pre, alphabet=(-1.0, 1.0)):
    # the Viterbi equalizer that knows the channel at every time
    m = len(taps[0]) - 1
    metric = {tuple(reversed(pre)): 0.0}
    back = []
    for n, yn in enumerate(y):
        best = {}
        for s, ms in metric.items():
            for a in alphabet:
                x = (a,) + s
                e = yn - sum(f * v for f, v in zip(taps[n], x))
                if x[:m] not in best or ms + e * e < best[x[:m]][0]:
                    best[x[:m]] = (ms + e * e, s, a)
        metric = {t: v[0] for t, v in best.items()}
        back.append({t: (v[1], v[2]) for t, v in best.items()})
    t = min(metric, key=metric.get)
    out = []
    for bp in reversed(back):
        t, a = bp[t]
        out.append(a)
    return out[::-1]


def errors(a, b):
    return sum(u != v for u, v in zip(a, b))


def test_step_zero_is_the_viterbi_equalizer() -> None:
    rng = random.Random(8002)
    for _ in range(20):
        f = [1.0] + [rng.uniform(-0.8, 0.8) for _ in range(rng.randint(0, 2))]
        pre = [rng.choice((-1.0, 1.0)) for _ in range(len(f) - 1)]
        x = [rng.choice((-1.0, 1.0)) for _ in range(9)]
        y = [v + rng.gauss(0, 0.6) for v in transmit(x, [f] * 9, pre)]
        d, est = psp_viterbi(y, f, 0.0, pre=pre)
        assert d == ml_by_search(y, f, pre)
        assert est == f


def test_drifting_channel() -> None:
    # taps 1, 0.5, 0.3 plus 0.4 sin(2 pi n / 500 + k), noise variance 0.05, seed 8001
    rng = random.Random(8001)
    n = 3000
    taps = drifting_channel(n, [1.0, 0.5, 0.3], 0.4, 500)
    x = [rng.choice((-1.0, 1.0)) for _ in range(n)]
    pre = [-1.0, -1.0]
    y = [v + rng.gauss(0, math.sqrt(0.05)) for v in transmit(x, taps, pre)]
    genie = genie_viterbi(y, taps, pre)
    fixed, _ = psp_viterbi(y, taps[0], 0.0, pre=pre)
    psp, _ = psp_viterbi(y, taps[0], 0.05, pre=pre)
    assert errors(genie, x) == 1
    assert errors(fixed, x) == 297
    assert errors(psp, x) == 0
    assert errors(psp, genie) == 1  # agrees with the genie on 2999 of 3000 symbols
    slow, _ = psp_viterbi(y, taps[0], 0.01, pre=pre)
    assert errors(slow, x) == 70  # a small step lags behind the drift


def test_learns_the_channel_from_a_wrong_start() -> None:
    rng = random.Random(8003)
    n = 1000
    h = [1.0, 0.5, 0.3]
    x = [rng.choice((-1.0, 1.0)) for _ in range(n)]
    pre = [-1.0, -1.0]
    y = [v + rng.gauss(0, math.sqrt(0.05)) for v in transmit(x, [h] * n, pre)]
    blind, _ = psp_viterbi(y, [1.0, 0.0, 0.0], 0.0, pre=pre)
    d, est = psp_viterbi(y, [1.0, 0.0, 0.0], 0.02, pre=pre)
    assert errors(blind, x) == 44
    assert errors(d, x) == 0
    assert max(abs(a - b) for a, b in zip(est, h)) < 0.05


def test_no_memory_and_input_checks() -> None:
    d, est = psp_viterbi([0.9, -1.2, 0.1], [1.0], 0.1)
    assert d == [1.0, -1.0, 1.0]
    # f = 1 + 0.1(-0.1) = 0.99, then 0.99 + 0.1(-0.21)(-1) = 1.011, then 1.011 + 0.1(-0.911) = 0.9199
    assert abs(est[0] - 0.9199) < 1e-12
    with pytest.raises(ValueError):
        psp_viterbi([1.0], [], 0.1)
    with pytest.raises(ValueError):
        psp_viterbi([1.0], [1.0, 0.5], 0.1, pre=[1.0, 1.0])
