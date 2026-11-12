# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/guruswami-sudan/. The authors are listed in prov/S3KZM9.jsonl.

import itertools
import math
import random

from guruswami_sudan import (decoding_radius, gs_parameters, guruswami_sudan, interpolate, num_monomials,
                             peval, roth_ruckenstein, sudan)


def brute_force(p: int, xs: list[int], ys: list[int], k: int, t: int) -> list[list[int]]:
    """The oracle: every f with deg f < k that agrees with ys in at least t places."""
    out = []
    for f in itertools.product(range(p), repeat=k):
        if sum(1 for a, b in zip(xs, ys) if peval(p, list(f), a) == b) >= t:
            out.append(list(f))
    return sorted(out)


def shifted_low_terms(p: int, q: list[list[int]], a: int, b: int, r: int) -> list[int]:
    """The coefficients of Q(x + a, y + b) of total degree < r, by direct binomial expansion."""
    out = {}
    for j, row in enumerate(q):
        for i, c in enumerate(row):
            if not c:
                continue
            for u in range(min(i, r - 1) + 1):
                for v in range(min(j, r - 1 - u) + 1):
                    term = c * math.comb(i, u) * math.comb(j, v) * pow(a, i - u, p) * pow(b, j - v, p)
                    out[(u, v)] = (out.get((u, v), 0) + term) % p
    return [v for v in out.values()]


def poly_mul_y(p: int, q: list[list[int]], f: list[int]) -> list[list[int]]:
    """Q(x, y) (y - f(x))."""
    width = max(len(row) for row in q) + len(f)
    out = [[0] * width for _ in range(len(q) + 1)]
    for j, row in enumerate(q):
        for i, c in enumerate(row):
            out[j + 1][i] = (out[j + 1][i] + c) % p
            for s, fc in enumerate(f):
                out[j][i + s] = (out[j][i + s] - c * fc) % p
    return out


def test_page_example() -> None:
    xs, ys = [1, 2, 3, 4, 5, 6], [0, 0, 0, 4, 5, 6]
    assert gs_parameters(6, 2, 1) == (3, 4)  # Sudan: agreement 4, two errors
    assert gs_parameters(6, 2, 2) == (5, 3)  # r = 2: agreement 3, three errors
    assert sudan(7, xs, ys, 2) == []
    assert guruswami_sudan(7, xs, ys, 2, 2) == [[0, 0], [0, 1]]  # f = 0 and f = x
    assert brute_force(7, xs, ys, 2, 3) == [[0, 0], [0, 1]]
    # y^2 (y - x)^2 has weighted degree 4 <= 5 and a double zero at every point
    q = poly_mul_y(7, poly_mul_y(7, [[0], [0], [1]], [0, 1]), [0, 1])
    for a, b in zip(xs, ys):
        assert not any(shifted_low_terms(7, q, a, b, 2))


def test_radius_values() -> None:
    # n = 16, k = 2: unique decoding 7, Sudan 10, r = 2 reaches the limit 11
    assert (n := 16) and decoding_radius(n, 2, 1) == 10 and decoding_radius(n, 2, 2) == 11
    # n = 16, k = 4: unique decoding 6, Sudan 7, r = 2 gives 8, and the limit 9 is first reached at r = 28
    assert decoding_radius(n, 4, 1) == 7 and decoding_radius(n, 4, 2) == 8
    assert decoding_radius(n, 4, 27) == 8 and decoding_radius(n, 4, 28) == 9
    # never at or beyond n - sqrt(n (k - 1)): the radius is at most n - floor(sqrt(n (k - 1))) - 1
    for n in range(4, 40):
        for k in range(2, n):
            limit = n - math.isqrt(n * (k - 1)) - 1
            radii = [decoding_radius(n, k, r) for r in range(1, 7)]
            assert all(e <= limit for e in radii)
            assert radii == sorted(radii)  # more multiplicity never hurts in this range
    assert num_monomials(5, 2) == 21 and num_monomials(8, 4) == 18


def test_interpolation_conditions() -> None:
    rng = random.Random(1999)
    for _ in range(30):
        p, k, r = rng.choice([(7, 2, 2), (11, 3, 2), (13, 2, 3), (17, 4, 2)])
        n = rng.randrange(k + 1, p)
        xs = rng.sample(range(p), n)
        ys = [rng.randrange(p) for _ in xs]
        d, _ = gs_parameters(n, k, r)
        q = interpolate(p, xs, ys, k, r, d)
        assert any(any(row) for row in q)
        assert all(c == 0 for j, row in enumerate(q) for i, c in enumerate(row) if c and i + (k - 1) * j > d)
        for a, b in zip(xs, ys):
            assert not any(shifted_low_terms(p, q, a, b, r))


def test_roth_ruckenstein_finds_planted_factors() -> None:
    rng = random.Random(2000)
    for _ in range(100):
        p, k = rng.choice([(5, 2), (7, 3), (11, 2), (13, 3)])
        fs = [[rng.randrange(p) for _ in range(k)] for _ in range(rng.randrange(1, 4))]
        q = [[rng.randrange(1, p)]]  # a nonzero constant
        if rng.random() < 0.5:
            q = [[rng.randrange(p) for _ in range(3)]]  # a factor without y
            q[0][rng.randrange(3)] = rng.randrange(1, p)
        for f in fs:
            q = poly_mul_y(p, q, f)
        roots = roth_ruckenstein(p, q, k)
        assert sorted(set(map(tuple, roots))) == sorted(set(map(tuple, fs)))


def planted_word(rng: random.Random, p: int, xs: list[int], k: int, errors: int) -> list[int]:
    """A codeword with `errors` changed places; sometimes the changes follow a second codeword."""
    f = [rng.randrange(p) for _ in range(k)]
    g = [rng.randrange(p) for _ in range(k)]
    ys = [peval(p, f, a) for a in xs]
    for i in rng.sample(range(len(xs)), errors):
        if rng.random() < 0.6:
            ys[i] = peval(p, g, xs[i])
        else:
            ys[i] = (ys[i] + rng.randrange(1, p)) % p
    return ys


def test_against_brute_force_sudan() -> None:
    rng = random.Random(1997)
    count = 0
    for p, n, k, trials in [(17, 16, 2, 300), (11, 10, 3, 150), (13, 12, 2, 100)]:
        d, t = gs_parameters(n, k, 1)
        for _ in range(trials):
            xs = rng.sample(range(p), n)
            ys = planted_word(rng, p, xs, k, rng.randrange(n - t + 1))
            got = sudan(p, xs, ys, k)
            assert got == brute_force(p, xs, ys, k, t)
            assert got  # the planted word is within the radius
            count += 1
    assert count >= 500


def test_against_brute_force_multiplicity() -> None:
    rng = random.Random(1998)
    for p, n, k, r, trials in [(17, 16, 2, 2, 60), (11, 10, 2, 3, 20), (13, 12, 3, 2, 30)]:
        _, t = gs_parameters(n, k, r)
        assert n - t > decoding_radius(n, k, 1) or k == 3
        for _ in range(trials):
            xs = rng.sample(range(p), n)
            ys = planted_word(rng, p, xs, k, n - t if rng.random() < 0.7 else rng.randrange(n - t + 1))
            got = guruswami_sudan(p, xs, ys, k, r)
            assert got == brute_force(p, xs, ys, k, t)
            assert got


def test_edges() -> None:
    # no errors: the codeword alone (k = 2, n = 16 has distance 15, so no other word agrees in 6 places)
    xs = list(range(1, 17))
    f = [3, 5]
    ys = [peval(17, f, a) for a in xs]
    assert sudan(17, xs, ys, 2) == [f]
    assert guruswami_sudan(17, xs, ys, 2, 3) == [f]
    # a word far from every codeword gives an empty list
    assert brute_force(7, [1, 2, 3, 4, 5, 6], [0, 1, 0, 1, 0, 1], 2, 4) == sudan(7, [1, 2, 3, 4, 5, 6], [0, 1, 0, 1, 0, 1], 2)
