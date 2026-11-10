# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-decay/. The authors are listed in prov/SAPQHG.jsonl.

import random
from fractions import Fraction as F

import pytest

from forward_decay import ForwardDecayed


def backward(items, beta, t):
    """Backward exponential decay with factor beta per time unit, by brute force."""
    ws = [(beta ** (t - ti), x) for ti, x in items]
    return (
        sum(w for w, _ in ws),
        sum(w * x for w, x in ws),
        max(w * x for w, x in ws),
    )


def random_items(rng, n, start=0):
    t, out = start, []
    for _ in range(n):
        t += rng.choice([0, 0, 1, 2, 5])
        out.append((t, F(rng.randint(-20, 20))))
    return out


def test_page_example():
    fd = ForwardDecayed(lambda n: F(2) ** n, landmark=0)
    for t, x in [(0, 4), (1, 8), (1, 6), (3, 2)]:
        fd.add(t, x)
    assert (fd.nc, fd.ns) == (13, 48)
    assert fd.count(3) == F(13, 8) and fd.total(3) == 6
    assert fd.average() == F(48, 13)
    poly = ForwardDecayed(lambda n: F(n) ** 2, landmark=-1)
    for t, x in [(0, 4), (1, 8), (1, 6), (3, 2)]:
        poly.add(t, x)
    assert poly.nc == 25 and poly.count(3) == F(25, 16) and poly.count(7) == F(25, 64)


def test_exponential_forward_equals_backward_exactly():
    rng = random.Random(1)
    for _ in range(150):
        b = F(rng.randint(11, 30), 10)  # g(n) = b^n, so beta = 1/b
        landmark = rng.randint(-5, 0)
        items = random_items(rng, rng.randint(1, 25))
        fd = ForwardDecayed(lambda n, b=b: b ** n, landmark)
        for k, (ti, x) in enumerate(items):
            fd.add(ti, x)
            for q in (ti, ti + 1, ti + 4):
                c, s, m = backward(items[: k + 1], 1 / b, q)
                assert (fd.count(q), fd.total(q), fd.max(q)) == (c, s, m)


def test_landmark_move_keeps_every_query():
    rng = random.Random(2)
    for _ in range(80):
        b = F(rng.randint(11, 30), 10)
        items = random_items(rng, rng.randint(1, 20))
        fd = ForwardDecayed(lambda n, b=b: b ** n, 0)
        for it in items:
            fd.add(*it)
        q = items[-1][0] + 1
        before = (fd.count(q), fd.total(q), fd.max(q))
        new_l = items[-1][0]
        fd.move_landmark(new_l, b ** (0 - new_l))
        assert (fd.count(q), fd.total(q), fd.max(q)) == before
        fd.add(q, F(3))
        c, s, m = backward(items + [(q, F(3))], 1 / b, q + 2)
        assert (fd.count(q + 2), fd.total(q + 2), fd.max(q + 2)) == (c, s, m)


def test_merge():
    rng = random.Random(3)
    g = lambda n: F(n + 1) ** 3
    for _ in range(80):
        items = random_items(rng, rng.randint(2, 20))
        a, b, whole = ForwardDecayed(g), ForwardDecayed(g), ForwardDecayed(g)
        for it in items:
            (a if rng.random() < 0.5 else b).add(*it)
            whole.add(*it)
        m = a.merge(b)
        q = items[-1][0] + 3
        assert (m.count(q), m.total(q), m.max(q)) == (whole.count(q), whole.total(q), whole.max(q))
    with pytest.raises(ValueError):
        ForwardDecayed(g, 0).merge(ForwardDecayed(g, 1))


def test_weight_properties_and_fixed_ratios():
    g = lambda n: F(n) ** 2
    landmark = -1
    rng = random.Random(4)
    times = sorted(rng.randint(0, 30) for _ in range(10))
    for ti in times:
        w = lambda t: g(ti - landmark) / g(t - landmark)
        assert w(ti) == 1
        prev = 1
        for t in range(ti, 60):
            assert 0 <= w(t) <= prev
            prev = w(t)
    # the ratio of two item weights does not change with t
    a, b = times[0], times[-1]
    ratios = {g(a - landmark) / g(t - landmark) / (g(b - landmark) / g(t - landmark)) for t in range(b, 60)}
    assert len(ratios) == 1


def test_only_exponential_weights_depend_on_age_alone():
    # polynomial g: two items of the same age get different weights for different landmarks
    g = lambda n: F(n) ** 2
    w = lambda ti, t, L: g(ti - L) / g(t - L)
    assert w(5, 7, 0) != w(5, 7, -10)
    b = F(3, 2)
    e = lambda ti, t, L: b ** (ti - L) / b ** (t - L)
    assert e(5, 7, 0) == e(5, 7, -10) == e(105, 107, 0) == 1 / b ** 2


def test_item_before_landmark_rejected():
    with pytest.raises(ValueError):
        ForwardDecayed(lambda n: n + 1, landmark=5).add(4)
