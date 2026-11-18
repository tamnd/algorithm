# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-blended-oit/. The authors are listed in prov/ZP9G80.jsonl.

"""Weighted blended OIT against exact sorted over compositing, in Fractions."""

import random
from fractions import Fraction as F

from weighted_blended_oit import (
    constant_weight,
    mcguire_blog_weight,
    over_composite,
    transmittance,
    visibility_weight,
    wboit,
)


def random_fragments(rng: random.Random, k: int, same_color=None):
    frags = []
    depths = rng.sample(range(1, 1000), k)
    for z in depths:
        a = F(rng.randint(1, 99), 100)
        base = same_color or (F(rng.randint(0, 100), 100), F(rng.randint(0, 100), 100), F(rng.randint(0, 100), 100))
        frags.append((tuple(a * x for x in base), a, F(z, 10)))
    return frags


def rational_depth_weight(c, a, z):
    """A positive weight that falls with depth, in exact arithmetic. For the
    depths of the tests (z < 100) and alpha >= 0.01 it keeps alpha * w above
    the guard eps of wboit, so the guard never changes an exact result."""
    return 1 / (1 + z / 10)


def test_coverage_is_exact_in_any_order() -> None:
    rng = random.Random(41)
    bg = (F(1, 5), F(2, 5), F(3, 5))
    for _ in range(60):
        frags = random_fragments(rng, rng.randint(1, 8))
        rng.shuffle(frags)
        # With a black background the alpha of the result is not needed;
        # the transmittance is read from the blend of a white background.
        white, black = (F(1),), (F(0),)
        mono = [((F(0),), a, z) for _, a, z in frags]
        assert wboit(mono, white, constant_weight) == over_composite(mono, white)
        assert wboit(mono, black, rational_depth_weight)[0] == 0
        assert transmittance(frags) == over_composite(mono, white)[0]
        out = wboit(frags, bg, rational_depth_weight)
        assert len(out) == 3


def test_order_independent_in_exact_arithmetic() -> None:
    rng = random.Random(42)
    bg = (F(1, 3), F(1, 7), F(0))
    for _ in range(40):
        frags = random_fragments(rng, rng.randint(2, 6))
        ref = wboit(frags, bg, rational_depth_weight)
        for _ in range(5):
            rng.shuffle(frags)
            assert wboit(frags, bg, rational_depth_weight) == ref


def test_exact_for_one_fragment() -> None:
    rng = random.Random(43)
    bg = (F(1, 2), F(1, 4), F(1, 8))
    for _ in range(50):
        frags = random_fragments(rng, 1)
        assert wboit(frags, bg, rational_depth_weight) == over_composite(frags, bg)


def test_exact_when_all_colors_are_equal() -> None:
    rng = random.Random(44)
    bg = (F(1, 2), F(1, 4), F(1, 8))
    color = (F(9, 10), F(3, 10), F(1, 10))
    for _ in range(50):
        frags = random_fragments(rng, rng.randint(1, 7), same_color=color)
        for weight in (constant_weight, rational_depth_weight):
            assert wboit(frags, bg, weight) == over_composite(frags, bg)


def test_exact_with_the_visibility_weight() -> None:
    rng = random.Random(45)
    bg = (F(1, 2), F(1, 4), F(1, 8))
    for _ in range(50):
        frags = random_fragments(rng, rng.randint(1, 7))
        rng.shuffle(frags)
        assert wboit(frags, bg, visibility_weight(frags)) == over_composite(frags, bg)


def test_red_and_blue_example() -> None:
    red = ((F(1, 2), F(0), F(0)), F(1, 2), F(1))
    blue = ((F(0), F(0), F(1, 2)), F(1, 2), F(2))
    black = (F(0), F(0), F(0))
    assert over_composite([red, blue], black) == (F(1, 2), F(0), F(1, 4))
    assert wboit([red, blue], black, constant_weight) == (F(3, 8), F(0), F(3, 8))
    near_first = wboit([red, blue], black, lambda c, a, z: 3 if z == 1 else 1)
    assert near_first == (F(9, 16), F(0), F(3, 16))


def test_color_is_in_the_hull_times_coverage() -> None:
    rng = random.Random(46)
    black = (F(0), F(0), F(0))
    for _ in range(50):
        frags = random_fragments(rng, rng.randint(1, 6))
        cov = 1 - transmittance(frags)
        out = wboit(frags, black, rational_depth_weight)
        for k in range(3):
            lo = min(c[k] / a for c, a, _ in frags)
            hi = max(c[k] / a for c, a, _ in frags)
            assert lo * cov <= out[k] <= hi * cov


def test_blog_weight_is_positive_and_falls_with_depth() -> None:
    c, a = (0.4, 0.2, 0.1), 0.5
    prev = None
    for z in (0.1, 1.0, 10.0, 50.0, 100.0, 200.0, 400.0, 1000.0, 1e5):
        w = mcguire_blog_weight(c, a, z)
        assert 0.0 < w <= 3e3
        if prev is not None:
            assert w <= prev
        prev = w
    assert mcguire_blog_weight(c, a, 1e5) == 0.5 * 1e-2


def test_float_run_is_close_to_exact() -> None:
    rng = random.Random(47)
    bg = (0.2, 0.3, 0.4)
    for _ in range(30):
        frags = random_fragments(rng, rng.randint(1, 6))
        fl = [(tuple(float(x) for x in c), float(a), float(z)) for c, a, z in frags]
        exact = wboit(frags, tuple(F(x) for x in bg), lambda c, a, z: F(mcguire_blog_weight(tuple(float(x) for x in c), float(a), float(z))))
        approx = wboit(fl, bg)
        assert all(abs(float(e) - x) < 1e-9 for e, x in zip(exact, approx))
