# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sphere-tracing/. The authors are listed in prov/W0Z18J.jsonl.

import math
import random
from fractions import Fraction as Q

from sphere_tracing import lipschitz_scaled, sphere_trace

# Rational unit vectors, so that the exact test can use Fraction arithmetic.
BASE = [(1, 0, 0), (Q(3, 5), Q(4, 5), 0), (Q(2, 3), Q(2, 3), Q(1, 3)), (Q(2, 7), Q(3, 7), Q(6, 7)), (Q(1, 3), Q(2, 3), Q(2, 3)), (Q(12, 13), Q(4, 13), Q(3, 13))]


def rational_unit(rng):
    v = list(rng.choice(BASE))
    rng.shuffle(v)
    return tuple(Q(x) * rng.choice((-1, 1)) for x in v)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def polytope(rng):
    """Random convex polytope {p : n.p + h <= 0 for all planes} that contains the origin."""
    planes = [((1, 0, 0), -Q(rng.randint(2, 6), 2)), ((-1, 0, 0), -Q(rng.randint(2, 6), 2)), ((0, 1, 0), -Q(rng.randint(2, 6), 2)), ((0, -1, 0), -Q(rng.randint(2, 6), 2)), ((0, 0, 1), -Q(rng.randint(2, 6), 2)), ((0, 0, -1), -Q(rng.randint(2, 6), 2))]
    for _ in range(rng.randint(1, 5)):
        planes.append((rational_unit(rng), -Q(rng.randint(2, 8), 4)))
    return planes


def exact_first_hit(planes, o, d):
    """Slab clipping in Fraction arithmetic: the first t >= 0 with all n.(o + t d) + h <= 0, and
    the plane that gives it. Returns (None, None) for a miss."""
    t_in, t_out, face = Q(0), None, None
    for n, h in planes:
        num, den = dot(n, o) + h, dot(n, d)
        if den == 0:
            if num > 0:
                return None, None
            continue
        t = -num / den
        if den < 0 and t > t_in:
            t_in, face = t, (n, h)
        if den > 0 and (t_out is None or t < t_out):
            t_out = t
    if t_out is not None and t_in > t_out:
        return None, None
    return t_in, face


def test_exact_polytopes_never_overstep():
    rng = random.Random(21)
    eps = Q(1, 10 ** 6)
    hits = 0
    for _ in range(150):
        planes = polytope(rng)

        def f(p):
            return max(dot(n, p) + h for n, h in planes)

        u = rational_unit(rng)
        o = (6 * u[0], 6 * u[1], 6 * u[2])
        # aim roughly at the origin: the best of a few random rational directions
        cands = [rational_unit(rng) for _ in range(rng.randint(1, 60))]
        d = max(cands, key=lambda v: -dot(v, o))
        t_star, face = exact_first_hit(planes, o, d)
        seen = []
        t = sphere_trace(f, o, d, Q(40), eps, max_steps=400, record=seen)
        if t_star is not None:
            assert all(s <= t_star for s in seen)  # never past the first hit, exactly
        if t is not None:
            p = tuple(o[i] + t * d[i] for i in range(3))
            assert f(p) < eps
            if t_star is not None:
                hits += 1
                # the entry face alone already bounds the gap: f >= (t* - t) |n.d|
                assert 0 <= t_star - t <= eps / -dot(face[0], d)
    assert hits > 30


def sphere_first_hit(o, d, c, r):
    oc = [o[i] - c[i] for i in range(3)]
    b = sum(oc[i] * d[i] for i in range(3))
    disc = b * b - (sum(x * x for x in oc) - r * r)
    if disc < 0:
        return None
    t = -b - math.sqrt(disc)
    return t if t >= 0 else None


def test_float_spheres_against_exact_first_hit():
    rng = random.Random(22)
    eps = 1e-7
    for _ in range(200):
        spheres = [((rng.uniform(-3, 3), rng.uniform(-3, 3), rng.uniform(4, 12)), rng.uniform(0.2, 1.5)) for _ in range(5)]

        def f(p):
            return min(math.dist(p, c) - r for c, r in spheres)

        o = (0.0, 0.0, 0.0)
        d = (rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3), 1.0)
        n = math.sqrt(dot(d, d))
        d = tuple(x / n for x in d)
        hits = [h for h in (sphere_first_hit(o, d, c, r) for c, r in spheres) if h is not None]
        t_star = min(hits) if hits else None
        seen = []
        t = sphere_trace(f, o, d, 30.0, eps, max_steps=5000, record=seen)
        if t_star is not None:
            assert all(s <= t_star + 1e-9 for s in seen)
        if t is not None:
            assert f(tuple(o[i] + t * d[i] for i in range(3))) < eps
        if t_star is not None and t is not None:
            # a near miss of a closer sphere can stop the trace early, within eps of that sphere
            assert t <= t_star + 1e-9


def steps_to_converge(sin_a, eps):
    """Exact number of field evaluations for a ray toward the plane z = 0 at angle a, from height 1."""
    cos_a = None
    for n, s in [((Q(4, 5), 0, -Q(3, 5)), Q(3, 5)), ((Q(24, 25), 0, -Q(7, 25)), Q(7, 25)), ((Q(40, 41), 0, -Q(9, 41)), Q(9, 41)), ((0, 0, Q(-1)), Q(1))]:
        if s == sin_a:
            cos_a = n
    seen = []
    t = sphere_trace(lambda p: p[2], (0, 0, Q(1)), cos_a, Q(10 ** 6), eps, max_steps=10 ** 5, record=seen)
    return t, len(seen)


def test_grazing_rays_converge_linearly():
    eps = Q(1, 10 ** 4)
    for s in (Q(1), Q(3, 5), Q(7, 25), Q(9, 41)):
        t, evals = steps_to_converge(s, eps)
        # the height after k steps is (1 - sin a)^k; the trace stops at the first height < eps
        k = 0
        h = Q(1)
        while h >= eps:
            h *= 1 - s
            k += 1
        assert evals == k + 1
        assert t == (1 - (1 - s) ** k) / s
    _, head_on = steps_to_converge(Q(1), eps)
    _, grazing = steps_to_converge(Q(7, 25), eps)
    assert head_on == 2 and grazing > 25


def test_a_function_that_is_not_a_bound_oversteps():
    def shell(p):
        return abs(math.dist(p, (0.0, 0.0, 0.0)) - 2.0) - 0.05

    o, d = (0.0, 0.0, -5.0), (0.0, 0.0, 1.0)
    t = sphere_trace(shell, o, d, 20.0, 1e-9)
    assert abs(t - 2.95) < 1e-9
    seen = []
    sphere_trace(lambda p: 3 * shell(p), o, d, 20.0, 1e-9, record=seen)
    assert any(s > 2.95 + 1e-6 for s in seen)  # the first step already passes the shell


def test_lipschitz_scaling_of_an_algebraic_sphere():
    def algebraic(p):
        return dot(p, p) - 1.0  # gradient length 2|p| <= 12 on the ball of radius 6

    o, d = (0.0, 0.0, -5.0), (0.0, 0.0, 1.0)
    seen = []
    t = sphere_trace(lipschitz_scaled(algebraic, 12.0), o, d, 20.0, 1e-9, max_steps=10 ** 4, record=seen)
    assert all(s <= 4.0 + 1e-12 for s in seen)
    assert abs(t - 4.0) < 1e-8
    exact = []
    sphere_trace(lambda p: math.dist(p, (0.0, 0.0, 0.0)) - 1.0, o, d, 20.0, 1e-9, record=exact)
    assert len(exact) == 2 and len(seen) > 20
