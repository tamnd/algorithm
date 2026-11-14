# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sdc-modulo-scheduling/. The authors are listed in prov/6XQDH6.jsonl.

import itertools
import random

from sdc_modulo_scheduling import (exact_min_ii, exact_schedule, is_valid, rec_mii, res_mii, sdc_modulo_schedule)

# m1 = acc * c, m2 = x[i] * y[i], a = m1 + m2, and acc of the next iteration is a.
ACC = (3, [(0, 2, 0), (1, 2, 0), (2, 0, 1)], [2, 2, 1], ["mul", "mul", "add"], {"mul": 1})


def random_loop(rng: random.Random, max_n: int):
    n = rng.randint(2, max_n)
    edges = [(u, v, 0) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.35]
    for _ in range(rng.randint(1, 2)):
        u, v = rng.randrange(n), rng.randrange(n)
        if u >= v:
            edges.append((u, v, rng.randint(1, 2)))
    lat = [rng.randint(0, 2) for _ in range(n)]
    kind = [rng.choice("ab") for _ in range(n)]
    limits = {k: 1 for k in "ab" if rng.random() < 0.8}
    return n, edges, lat, kind, limits


def test_accumulator_example():
    n, edges, lat, kind, limits = ACC
    assert res_mii(kind, limits) == 2 and rec_mii(n, edges, lat) == 3
    ii, s = sdc_modulo_schedule(*ACC)
    assert (ii, s) == (4, [0, 1, 3])
    assert is_valid(n, edges, lat, kind, limits, ii, s)
    assert exact_min_ii(*ACC, 6) == 3
    t = exact_schedule(*ACC, 3)
    assert is_valid(n, edges, lat, kind, limits, 3, t)
    assert is_valid(n, edges, lat, kind, limits, 3, [1, 0, 3])
    assert not is_valid(n, edges, lat, kind, limits, 3, [0, 1, 3])


def test_no_resource_limit_reaches_rec_mii():
    rng = random.Random(21)
    for _ in range(100):
        n, edges, lat, kind, _ = random_loop(rng, 7)
        ii, s = sdc_modulo_schedule(n, edges, lat, kind, {})
        assert ii == rec_mii(n, edges, lat)
        assert is_valid(n, edges, lat, kind, {}, ii, s)


def test_heuristic_against_exhaustive_search():
    rng = random.Random(22)
    worse = 0
    for _ in range(150):
        n, edges, lat, kind, limits = random_loop(rng, 5)
        ii, s = sdc_modulo_schedule(n, edges, lat, kind, limits)
        assert is_valid(n, edges, lat, kind, limits, ii, s)
        best = exact_min_ii(n, edges, lat, kind, limits, ii)
        assert max(res_mii(kind, limits), rec_mii(n, edges, lat)) <= best <= ii
        worse += ii > best
    assert worse < 150


def test_exact_search_against_bounded_enumeration():
    rng = random.Random(23)
    for _ in range(40):
        n, edges, lat, kind, limits = random_loop(rng, 4)
        ii = max(res_mii(kind, limits), rec_mii(n, edges, lat))
        found = exact_schedule(n, edges, lat, kind, limits, ii)
        horizon = 2 * ii + sum(lat) + 1
        brute = any(is_valid(n, edges, lat, kind, limits, ii, list(p))
                    for p in itertools.product(range(horizon), repeat=n))
        assert (found is not None) == brute
        if found is not None:
            assert is_valid(n, edges, lat, kind, limits, ii, found)
