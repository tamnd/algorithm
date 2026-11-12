# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slab-method/. The authors are listed in prov/2SZ2M7.jsonl.

import math
import random
from fractions import Fraction

from slab_method import inverse_direction, slab_test


def exact_interval(lo, hi, o, d, t0=0.0, t1=math.inf):
    """Reference: the exact parameter interval of the ray inside the closed box, by Fraction."""
    t_lo = Fraction(t0)
    t_hi = t1 if math.isinf(t1) else Fraction(t1)
    for a in range(3):
        la, ha, oa = Fraction(lo[a]), Fraction(hi[a]), Fraction(o[a])
        if d[a] == 0:
            if oa < la or oa > ha:
                return None
            continue
        da = Fraction(d[a])
        ta, tb = (la - oa) / da, (ha - oa) / da
        if ta > tb:
            ta, tb = tb, ta
        t_lo = max(t_lo, ta)
        t_hi = min(t_hi, tb)
    return (t_lo, t_hi) if t_lo <= t_hi else None


def same(got, want) -> bool:
    if got is None or want is None:
        return got is None and want is None
    if math.isinf(got[1]) or (isinstance(want[1], float) and math.isinf(want[1])):
        return Fraction(got[0]) == want[0] and got[1] == want[1]
    return Fraction(got[0]) == want[0] and Fraction(got[1]) == want[1]


def test_example() -> None:
    lo, hi = (1.0, 1.0, 0.0), (3.0, 2.0, 2.0)
    o, d = (0.0, 0.0, 1.0), (2.0, 1.0, 0.0)
    inv = inverse_direction(d)
    assert inv == (0.5, 1.0, math.inf)
    assert slab_test(lo, hi, o, inv) == (1.0, 1.5)
    # The same ray moved up to z = 2 lies in the top face plane: 0 * inf is NaN there.
    assert slab_test(lo, hi, (0.0, 0.0, 2.0), inv) == (1.0, 1.5)
    assert slab_test(lo, hi, (0.0, 0.0, 0.0), inv) == (1.0, 1.5)
    assert slab_test(lo, hi, (0.0, 0.0, 2.5), inv) is None


def test_nan_cases() -> None:
    lo, hi = (0.0, 0.0, 0.0), (1.0, 1.0, 1.0)
    for z in (0.0, 1.0):
        for dz in (0.0, -0.0):
            inv = inverse_direction((1.0, 0.0, dz))
            for y in (0.0, 0.5, 1.0):
                assert slab_test(lo, hi, (-1.0, y, z), inv) == (1.0, 2.0)
    # A flat box: both planes of the z slab hold the origin, so both values are NaN.
    assert slab_test((0.0, 0.0, 0.5), (1.0, 1.0, 0.5), (-1.0, 0.5, 0.5), inverse_direction((1.0, 0.0, 0.0))) == (1.0, 2.0)
    # The naive min and max of Python return the NaN when it comes first, which breaks the test.
    nan = 0.0 * math.inf
    assert math.isnan(min(nan, 1.0)) and min(1.0, nan) == 1.0


def test_edges() -> None:
    lo, hi = (0.0, 0.0, 0.0), (1.0, 1.0, 1.0)
    inv = inverse_direction((1.0, 1.0, 1.0))
    assert slab_test(lo, hi, (0.5, 0.5, 0.5), inv) == (0.0, 0.5)  # origin inside
    assert slab_test(lo, hi, (2.0, 2.0, 2.0), inv) is None  # box behind the origin
    assert slab_test(lo, hi, (-1.0, -1.0, -1.0), inv) == (1.0, 2.0)  # through two corners
    assert slab_test(lo, hi, (-1.0, -1.0, -1.0), inv, 0.0, 0.5) is None  # ends before the box
    assert slab_test(lo, hi, (-1.0, -1.0, -1.0), inv, 0.0, 1.0) == (1.0, 1.0)  # ends on the box
    assert slab_test(lo, hi, (-1.0, 2.0, 0.5), inverse_direction((1.0, 0.0, 0.0))) is None  # parallel, outside
    # A negative zero component: the near plane is chosen by the sign of inv, which is -inf.
    assert slab_test(lo, hi, (-1.0, 0.5, 0.5), inverse_direction((1.0, -0.0, -0.0))) == (1.0, 2.0)


def test_against_exact_on_exact_grid() -> None:
    # Integer boxes and origins with power-of-two directions: every float step is exact,
    # so the float result must equal the Fraction result, NaN cases included.
    rng = random.Random(2)
    comps = [0.0, -0.0, 0.5, -0.5, 1.0, -1.0, 2.0, -2.0, 4.0, -4.0]
    for _ in range(8000):
        lo = [float(rng.randint(-3, 3)) for _ in range(3)]
        hi = [lo[a] + float(rng.randint(0, 3)) for a in range(3)]
        o = [float(rng.randint(-5, 5)) for _ in range(3)]
        d = [rng.choice(comps) for _ in range(3)]
        if all(x == 0 for x in d):
            continue
        t0 = float(rng.randint(0, 2))
        t1 = rng.choice([math.inf, float(rng.randint(0, 6))])
        if t1 < t0:
            continue
        got = slab_test(lo, hi, o, inverse_direction(d), t0, t1)
        assert same(got, exact_interval(lo, hi, o, d, t0, t1))


def test_random_floats_against_exact() -> None:
    rng = random.Random(3)
    for _ in range(8000):
        lo = [rng.uniform(-2, 2) for _ in range(3)]
        hi = [lo[a] + rng.uniform(0, 2) for a in range(3)]
        o = [rng.uniform(-4, 4) for _ in range(3)]
        d = [rng.uniform(-1, 1) if rng.random() < 0.8 else 0.0 for _ in range(3)]
        if rng.random() < 0.2:
            a = rng.randrange(3)
            o[a] = rng.choice([lo[a], hi[a]])  # origin on a slab plane
        if all(x == 0 for x in d):
            continue
        want = exact_interval(lo, hi, o, d)
        inv = inverse_direction(d)
        if want is not None:
            assert slab_test(lo, hi, o, inv, robust=True) is not None
            if want[1] - want[0] > Fraction(1, 10**9):
                got = slab_test(lo, hi, o, inv)
                assert got is not None
                assert abs(Fraction(got[0]) - want[0]) < Fraction(1, 10**9)


def test_grazing_rays_robust_never_misses() -> None:
    # Rays aimed at a point on an edge of the box: the exact answer is often a hit with an
    # empty-width interval, and the plain float test may miss it. The padded test never does.
    rng = random.Random(4)
    plain_misses = 0
    for _ in range(8000):
        lo = [rng.uniform(-1, 0) for _ in range(3)]
        hi = [rng.uniform(1, 2) for _ in range(3)]
        p = [rng.uniform(lo[a], hi[a]) for a in range(3)]
        a, b = rng.sample(range(3), 2)
        p[a] = rng.choice([lo[a], hi[a]])
        p[b] = rng.choice([lo[b], hi[b]])
        o = [rng.uniform(-5, 5) for _ in range(3)]
        d = [p[i] - o[i] for i in range(3)]
        want = exact_interval(lo, hi, o, d)
        inv = inverse_direction(d)
        if want is not None:
            assert slab_test(lo, hi, o, inv, robust=True) is not None
            if slab_test(lo, hi, o, inv) is None:
                plain_misses += 1
    assert plain_misses > 0
