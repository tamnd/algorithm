# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/winnow/. The authors are listed in prov/ETYSJD.jsonl.

import random

import pytest

from winnow import Winnow, disjunction, run, winnow1_bound

TRACE = [
    (1, 1, 0, 0, 1, 1, 0, 0),
    (0, 0, 0, 1, 1, 0, 1, 1),
    (0, 1, 1, 0, 0, 0, 0, 0),
    (0, 1, 0, 1, 0, 1, 0, 0),
    (1, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 1, 0, 0, 0, 0, 1),
    (0, 1, 0, 0, 1, 0, 1, 0),
    (1, 0, 0, 0, 0, 0, 0, 1),
]


def test_worked_example() -> None:
    f = disjunction([0, 2])
    m = Winnow(8)
    flags = [m.update(x, f(x)) for x in TRACE]
    assert flags == [True, True, True, True, True, True, False, True]
    assert m.w == [8, 0, 4, 0, 0, 0, 0, 0]
    assert winnow1_bound(8, 2, 2, 4) == 14


def random_stream(rng: random.Random, n: int, k: int, length: int):
    rel = rng.sample(range(n), k)
    f = disjunction(rel)
    p = 1 / (k + 1)
    out = []
    for _ in range(length):
        x = [1 if rng.random() < 3.0 / n else 0 for _ in range(n)]
        for i in rel:
            x[i] = 1 if rng.random() < p / 2 else 0
        out.append((x, f(x)))
    return rel, out


@pytest.mark.parametrize("n,k", [(16, 1), (16, 3), (64, 2), (128, 4), (256, 1)])
def test_winnow1_meets_littlestone_bound(n: int, k: int) -> None:
    rng = random.Random(1000 * n + k)
    for alpha, theta in ((2.0, n / 2), (2.0, n), (3.0, n / 3), (1.5, float(n))):
        rel, stream = random_stream(rng, n, k, 3000)
        m = Winnow(n, alpha, theta, variant=1)
        mistakes = run(m, stream)
        assert mistakes <= winnow1_bound(n, k, alpha, theta)
        # relevant weights are never eliminated and never pass alpha * theta
        for i in rel:
            assert 1 <= m.w[i] <= alpha * theta


def test_adversarial_order_still_within_bound() -> None:
    # all single variables first, then pairs: many false positives early
    n, k = 32, 2
    f = disjunction([5, 17])
    stream = []
    for i in range(n):
        x = [0] * n
        x[i] = 1
        stream.append((x, f(x)))
    for i in range(n):
        for j in range(i + 1, n):
            x = [0] * n
            x[i] = x[j] = 1
            stream.append((x, f(x)))
    m = Winnow(n)
    assert run(m, stream * 3) <= winnow1_bound(n, k, 2.0, n / 2)
    assert all(m.predict(x) == y for x, y in stream)


def test_winnow2_demotes() -> None:
    m = Winnow(4, alpha=2.0, theta=1.0, variant=2)
    assert m.update((1, 1, 0, 0), 0)  # sum 2 > 1, false positive
    assert m.w == [0.5, 0.5, 1.0, 1.0]
    assert m.update((1, 0, 0, 0), 1)  # sum 0.5, false negative
    assert m.w == [1.0, 0.5, 1.0, 1.0]
    assert not m.update((1, 0, 1, 0), 1)


def test_bad_parameters() -> None:
    with pytest.raises(ValueError):
        Winnow(3, alpha=1.0)
    with pytest.raises(ValueError):
        Winnow(3, variant=3)
