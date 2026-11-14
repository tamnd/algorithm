# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/petricks-method/. The authors are listed in prov/P7JR23.jsonl.

import itertools
import random

from petricks_method import absorb, cheapest, covers, literals, petrick_products, petricks_method


def brute_minimal_covers(rows: list[set[int]], ncols: int) -> list[frozenset[int]]:
    """Every set of columns that meets every row and has no proper subset that does."""
    def ok(s: frozenset[int]) -> bool:
        return all(s & r for r in rows)
    good = [frozenset(s) for k in range(ncols + 1) for s in itertools.combinations(range(ncols), k) if ok(frozenset(s))]
    return sorted((s for s in good if not any(t < s for t in good)), key=lambda s: (len(s), sorted(s)))


def all_cubes(n: int) -> list[str]:
    return ["".join(t) for t in itertools.product("01-", repeat=n)]


def primes_of(n: int, allowed: set[int]) -> list[str]:
    def inside(c: str) -> bool:
        return all(m in allowed for m in range(2 ** n) if covers(c, m))
    imps = [c for c in all_cubes(n) if inside(c) and any(covers(c, m) for m in range(2 ** n))]
    return sorted(c for c in imps if not any(inside(c[:i] + "-" + c[i + 1:]) for i in range(n) if c[i] != "-"))


def test_cyclic_example() -> None:
    # f = sum of m(0, 1, 2, 5, 6, 7): six primes, each minterm in two of them.
    primes = ["00-", "0-0", "-01", "-10", "1-1", "11-"]
    on = [0, 1, 2, 5, 6, 7]
    rows = [{j for j, p in enumerate(primes) if covers(p, m)} for m in on]
    products = petrick_products(rows)
    assert sorted(sorted(t) for t in products if len(t) == 3) == [[0, 3, 4], [1, 2, 5]]
    assert len(products) == 5  # two covers of 3 primes and three of 4 primes
    cover = petricks_method(on, primes)
    assert cover in (sorted(["00-", "-10", "1-1"]), sorted(["0-0", "-01", "11-"]))


def test_absorb() -> None:
    a, b, c = frozenset({1}), frozenset({1, 2}), frozenset({2, 3})
    assert absorb([b, a, c, b]) == [a, c]
    assert absorb([]) == []


def test_edges() -> None:
    assert petrick_products([]) == [frozenset()]
    assert petrick_products([set()]) == []
    assert petrick_products([{0}, {0, 1}]) == [frozenset({0})]
    try:
        petricks_method([3], ["00"])
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


def test_products_are_the_minimal_covers() -> None:
    rng = random.Random(3)
    for _ in range(300):
        ncols = rng.randint(1, 8)
        rows = [{j for j in range(ncols) if rng.random() < 0.35} for _ in range(rng.randint(1, 7))]
        got = sorted(petrick_products(rows), key=lambda s: (len(s), sorted(s)))
        assert got == brute_minimal_covers(rows, ncols)


def test_cheapest_against_brute_force() -> None:
    rng = random.Random(5)
    for _ in range(300):
        ncols = rng.randint(1, 8)
        rows = [{j for j in range(ncols) if rng.random() < 0.4} | {rng.randrange(ncols)} for _ in range(rng.randint(1, 7))]
        w = [(1, rng.randint(1, 4)) for _ in range(ncols)]
        best = cheapest(petrick_products(rows), lambda j: w[j])
        def total(s: frozenset[int]) -> tuple[int, int]:
            return (len(s), sum(w[j][1] for j in s))
        every = [frozenset(s) for k in range(ncols + 1) for s in itertools.combinations(range(ncols), k) if all(set(s) & r for r in rows)]
        assert total(best) == min(total(s) for s in every)


def test_minimum_sop_on_random_functions() -> None:
    rng = random.Random(9)
    for n in (2, 3, 4):
        for _ in range(40):
            on = {m for m in range(2 ** n) if rng.random() < 0.4}
            dc = {m for m in range(2 ** n) if m not in on and rng.random() < 0.2}
            primes = primes_of(n, on | dc)
            cover = petricks_method(on, primes)
            got = {m for m in range(2 ** n) if any(covers(c, m) for c in cover)}
            assert on <= got <= on | dc
            key = (len(cover), sum(literals(c) for c in cover))
            best = None
            for k in range(len(primes) + 1):
                for s in itertools.combinations(primes, k):
                    if all(any(covers(c, m) for c in s) for m in on):
                        t = (k, sum(literals(c) for c in s))
                        best = t if best is None or t < best else best
                if best is not None:
                    break
            assert key == best
