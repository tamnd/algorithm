# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schwartz-zippel-lemma/. The authors are listed in prov/B38MAX.jsonl.

import itertools
import random

from schwartz_zippel_lemma import (
    all_polys,
    count_zeros,
    evaluate,
    individual_degrees,
    linear_factor_product,
    nonzero_lower_bound,
    normalize,
    random_identity_test,
    random_poly,
    total_degree,
)


def check_bound(poly, S, m, q) -> None:
    d = total_degree(poly)
    z = count_zeros(poly, S, m, q)
    s = len(S)
    # Schwartz-Zippel: zeros <= d |S|^(m-1).
    assert z <= d * s ** (m - 1), (poly, S, z)
    degs = individual_degrees(poly, m)
    if all(e <= s for e in degs):
        assert s**m - z >= nonzero_lower_bound(degs, s), (poly, S, z)


def test_all_quadratics_two_variables_f3() -> None:
    q, m = 3, 2
    subsets = [S for r in (1, 2, 3) for S in itertools.combinations(range(q), r)]
    count = 0
    for poly in all_polys(m, 2, q):
        if not poly:
            continue
        count += 1
        for S in subsets:
            check_bound(poly, S, m, q)
    assert count == 3**6 - 1


def test_all_linear_three_variables_f5() -> None:
    q, m = 5, 3
    for poly in all_polys(m, 1, q):
        if poly:
            check_bound(poly, tuple(range(q)), m, q)
            check_bound(poly, (0, 1, 3), m, q)


def test_random_polys_f5_and_f7() -> None:
    rng = random.Random(1)
    for q, m in ((5, 3), (7, 2)):
        for _ in range(300):
            poly = random_poly(m, 4, q, 4, rng)
            if not poly:
                continue
            S = tuple(sorted(rng.sample(range(q), rng.randint(2, q))))
            check_bound(poly, S, m, q)


def test_tightness_with_linear_factors() -> None:
    q, m = 7, 3
    S = tuple(range(q))
    for d in range(1, q + 1):
        poly = linear_factor_product(list(range(d)), m, q)
        assert total_degree(poly) == d
        assert count_zeros(poly, S, m, q) == d * q ** (m - 1)


def test_two_xy_over_f101() -> None:
    q = 101
    poly = {(1, 1): 2}
    z = count_zeros(poly, tuple(range(q)), 2, q)
    assert z == 201
    assert z * 101 <= 2 * 101**2


def test_identity_over_f2() -> None:
    # (x + y)^2 - x^2 - y^2 = 2xy is the zero polynomial over F_2.
    assert normalize({(1, 1): 2}, 2) == {}
    # x^2 - x is a nonzero polynomial of degree 2 that is zero on all of F_2;
    # the bound 2/2 = 1 allows it.
    poly = normalize({(2,): 1, (1,): -1}, 2)
    assert poly and count_zeros(poly, (0, 1), 1, 2) == 2


def test_fails_without_integral_domain() -> None:
    # Over Z/4, the degree-1 polynomial 2x is zero at x = 0 and x = 2: 2/4 > 1/4.
    assert count_zeros({(1,): 2}, (0, 1, 2, 3), 1, 4) == 2


def test_random_identity_test_one_sided() -> None:
    q, m = 101, 2
    S = tuple(range(q))
    lhs = {(2, 0): 1, (1, 1): 2, (0, 2): 1}  # x^2 + 2xy + y^2
    rhs = {(2, 0): 1, (0, 2): 1}  # x^2 + y^2
    rng = random.Random(7)
    # Equal polynomials are always accepted.
    for _ in range(200):
        assert random_identity_test(lhs, dict(lhs), S, m, q, 3, rng)
    # Different ones are rejected unless 2xy = 0 at every point; Pr <= (2/101)^k.
    accepted = sum(random_identity_test(lhs, rhs, S, m, q, 1, rng) for _ in range(5000))
    assert accepted <= 5000 * 2 / 101 * 1.5
    assert evaluate(lhs, (3, 4), q) == 49
