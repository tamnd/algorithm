# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zippel-sparse-interpolation/. The authors are listed in prov/GB4A8V.jsonl.
"""Tests for Zippel's sparse interpolation over Z/pZ.

Black boxes are built from known random sparse polynomials. The output must
equal the hidden polynomial, agree with it at many random points, and match
dense tensor-product interpolation on small cases. The number of probes is
checked against the bound (d + 1)(1 + (n - 1) t).
"""

import random
from itertools import product

import pytest

from zippel_sparse_interpolation import interp_dense, solve_vandermonde, zippel

P = 2_147_483_647  # 2^31 - 1, prime


def evaluate(poly, pt, p):
    s = 0
    for e, c in poly.items():
        v = c
        for x, k in zip(pt, e):
            v = v * pow(x, k, p) % p
        s = (s + v) % p
    return s


class Box:
    def __init__(self, poly, p):
        self.poly, self.p, self.calls = poly, p, 0

    def __call__(self, pt):
        self.calls += 1
        return evaluate(self.poly, pt, self.p)


def random_sparse(rng, n, d, t, p):
    mons = set()
    while len(mons) < t:
        mons.add(tuple(rng.randint(0, d) for _ in range(n)))
    return {m: rng.randrange(1, p) for m in mons}


def dense_reference(f, n, d, p):
    """Tensor-product Lagrange interpolation on the grid {1..d+1}^n."""
    grid = list(range(1, d + 2))
    vals = {pt: f(list(pt)) for pt in product(grid, repeat=n)}
    for axis in range(n):  # interpolate along one axis at a time
        new = {}
        for key in {k[:axis] + k[axis + 1:] for k in vals}:
            ys = [vals[key[:axis] + (g,) + key[axis:]] for g in grid]
            for e, c in enumerate(interp_dense(grid, ys, p)):
                new[key[:axis] + (e,) + key[axis:]] = c
        vals = new
    return {e: c for e, c in vals.items() if c}


def test_helpers():
    rng = random.Random(1)
    for _ in range(50):
        deg = rng.randint(0, 8)
        poly = [rng.randrange(P) for _ in range(deg + 1)]
        xs = rng.sample(range(1, P), deg + 1)
        ys = [sum(c * pow(x, k, P) for k, c in enumerate(poly)) % P for x in xs]
        assert interp_dense(xs, ys, P) == poly
        T = rng.randint(1, 8)
        nodes = rng.sample(range(P), T)
        c = [rng.randrange(P) for _ in range(T)]
        w = [sum(ci * pow(v, k, P) for ci, v in zip(c, nodes)) % P for k in range(T)]
        assert solve_vandermonde(nodes, w, P) == c


def test_example():
    # f = 3 x^2 y + 5 x y^3 - 2, d = 3
    f = {(2, 1): 3, (1, 3): 5, (0, 0): P - 2}
    assert zippel(Box(f, P), 2, 3, P, random.Random(7)) == f


def test_edges():
    rng = random.Random(3)
    assert zippel(Box({}, P), 3, 4, P, rng) == {}            # zero polynomial
    assert zippel(Box({(0, 0, 0): 9}, P), 3, 4, P, rng) == {(0, 0, 0): 9}  # constant
    one = {(5,): 2, (0,): 1}
    assert zippel(Box(one, P), 1, 5, P, rng) == one           # one variable
    dense = {e: 1 + sum(e) for e in product(range(3), repeat=2)}
    assert zippel(Box(dense, P), 2, 2, P, rng) == dense       # all (d+1)^n terms
    last = {(0, 0, 0, 4): 1}                                   # only the last variable
    assert zippel(Box(last, P), 4, 4, P, rng) == last
    # a degree bound larger than the true degree is fine
    f = {(1, 1): 4, (0, 2): 6}
    assert zippel(Box(f, P), 2, 7, P, rng) == f


@pytest.mark.parametrize("seed", range(6))
def test_random_sparse(seed):
    rng = random.Random(100 + seed)
    for _ in range(10):
        n, d = rng.randint(1, 5), rng.randint(1, 8)
        t = rng.randint(1, min(20, (d + 1) ** n))
        f = random_sparse(rng, n, d, t, P)
        box = Box(f, P)
        g = zippel(box, n, d, P, random.Random(seed * 1000 + n))
        assert g == f
        assert box.calls <= (d + 1) * (1 + (n - 1) * t)
        for _ in range(20):
            pt = [rng.randrange(P) for _ in range(n)]
            assert evaluate(g, pt, P) == evaluate(f, pt, P)


@pytest.mark.parametrize("seed", range(3))
def test_against_dense(seed):
    rng = random.Random(900 + seed)
    for _ in range(10):
        n, d = rng.randint(1, 3), rng.randint(1, 3)
        f = random_sparse(rng, n, d, rng.randint(1, (d + 1) ** n), P)
        ref = dense_reference(Box(f, P), n, d, P)
        assert ref == f
        assert zippel(Box(f, P), n, d, P, random.Random(seed)) == ref


def test_small_prime():
    # with p = 10007 the failure bound is still small for these sizes
    p = 10007
    rng = random.Random(42)
    for _ in range(30):
        n, d = rng.randint(2, 3), rng.randint(1, 4)
        f = random_sparse(rng, n, d, rng.randint(1, min(6, (d + 1) ** n)), p)
        assert zippel(Box(f, p), n, d, p, random.Random(rng.randrange(10**6))) == f
