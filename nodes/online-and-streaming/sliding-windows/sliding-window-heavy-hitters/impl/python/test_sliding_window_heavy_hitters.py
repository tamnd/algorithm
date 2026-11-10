# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-heavy-hitters/. The authors are listed in prov/130NZR.jsonl.

import math
import random
from collections import Counter

import pytest

from sliding_window_heavy_hitters import WindowFrequencies, mg_update


def test_page_example():
    wf = WindowFrequencies(8, 0.5)  # b = 2, k = 4
    assert (wf.b, wf.k) == (2, 4)
    for x in "aabacaabdda":
        wf.step(x)
    # t = 11, window = items 4..11 = "acaabdda"; the block 3..4 straddles and is gone
    assert [s for s, _ in wf.blocks] == [5, 7, 9]
    assert wf.cur == {"a": 1}
    assert wf.estimate("a") == 3 and Counter("acaabdda")["a"] == 4
    assert wf.estimate("d") == 2 and wf.estimate("b") == 1 and wf.estimate("c") == 1
    assert wf.heavy_hitters(0.5, 0.5) == ["a", "b", "c", "d"]
    assert wf.heavy_hitters(0.75, 0.5) == ["a", "d"]


def test_misra_gries_bound():
    rng = random.Random(1)
    for _ in range(100):
        k = rng.randint(1, 6)
        xs = [rng.randint(0, 9) for _ in range(rng.randint(0, 80))]
        c = {}
        for x in xs:
            mg_update(c, x, k)
        f = Counter(xs)
        assert len(c) <= k
        for x in set(xs) | set(c):
            assert f[x] - len(xs) / (k + 1) <= c.get(x, 0) <= f[x]


def streams(rng, n):
    yield [0] * n
    yield [i % 7 for i in range(n)]
    yield [i for i in range(n)]
    yield [(i // 13) % 4 for i in range(n)]  # bursts
    yield [0 if i % 3 else i for i in range(n)]
    for _ in range(25):
        s = rng.choice([1.1, 1.5, 2.0])
        weights = [1 / (r + 1) ** s for r in range(30)]
        yield rng.choices(range(30), weights, k=n)


@pytest.mark.parametrize("w,eps", [(1, 0.5), (10, 0.2), (50, 0.1), (64, 0.25), (100, 0.05)])
def test_error_bound_and_report(w, eps):
    rng = random.Random(w)
    for xs in streams(rng, 300):
        wf = WindowFrequencies(w, eps)
        for t, x in enumerate(xs, 1):
            wf.step(x)
            if t % 7 and t != len(xs):
                continue
            f = Counter(xs[max(0, t - w): t])
            for y in set(f) | {-1}:
                est = wf.estimate(y)
                assert f[y] - eps * w < est <= f[y] or (f[y] == est == 0)
            phi = 0.3
            got = set(wf.heavy_hitters(phi, eps))
            assert {y for y in f if f[y] >= phi * w} <= got
            assert all(f[y] >= (phi - eps) * w for y in got)
            blocks = math.floor(w / wf.b) + 1
            assert wf.words() <= blocks * wf.k


def test_bad_arguments():
    with pytest.raises(ValueError):
        WindowFrequencies(0, 0.1)
    with pytest.raises(ValueError):
        WindowFrequencies(5, 0)
