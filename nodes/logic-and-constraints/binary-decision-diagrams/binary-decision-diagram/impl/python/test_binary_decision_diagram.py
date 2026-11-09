# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-decision-diagram/. The authors are listed in prov/DBR5MN.jsonl.

import itertools
import random

from binary_decision_diagram import BDD, FALSE, TRUE


def cnf_value(clauses: list[list[int]], x: list[int]) -> int:
    return int(all(any((x[abs(l) - 1] == 1) == (l > 0) for l in c) for c in clauses))


def test_example() -> None:
    f = [[1, -2], [2, 3], [-1, -3]]
    b = BDD(3)
    r = b.from_cnf(f)
    assert b.size(r) == 8
    models = [x for x in itertools.product((0, 1), repeat=3) if b.evaluate(r, list(x))]
    assert models == [(0, 0, 1), (1, 1, 0)]
    assert not b.is_free(r)


def test_inconsistent_path() -> None:
    # x1 AND NOT x1: TRUE is reachable, but the function is 0.
    b = BDD(1)
    r = b.from_cnf([[1], [-1]])
    assert TRUE in b.reachable(r)
    assert b.evaluate(r, [0]) == 0 and b.evaluate(r, [1]) == 0
    assert not b.is_free(r)


def test_edges() -> None:
    b = BDD(2)
    assert b.from_cnf([]) == TRUE
    assert b.from_cnf([[]]) == FALSE
    assert b.evaluate(TRUE, [0, 0]) == 1 and b.evaluate(FALSE, [1, 1]) == 0
    assert b.is_free(TRUE) and b.sat_free(TRUE) and not b.sat_free(FALSE)


def test_from_cnf_against_truth_table() -> None:
    rng = random.Random(1959)
    for n in range(1, 11):
        for _ in range(5):
            m = rng.randint(1, 3 * n)
            f = [[rng.choice((1, -1)) * rng.randint(1, n) for _ in range(rng.randint(1, 3))] for _ in range(m)]
            b = BDD(n)
            r = b.from_cnf(f)
            assert b.size(r) <= sum(len(c) for c in f) + 2
            for a in range(1 << n):
                x = [(a >> j) & 1 for j in range(n)]
                assert b.evaluate(r, x) == cnf_value(f, x)


def random_free(rng: random.Random, n: int, count: int) -> tuple[BDD, int]:
    """A random free BDD: each node only uses variables not tested above it."""
    b = BDD(n)
    pool: list[tuple[int, int]] = [(0, FALSE), (0, TRUE)]  # (mask of variables used, node)
    for _ in range(count):
        i = rng.randrange(n)
        ok = [p for p in pool if not p[0] >> i & 1]
        (m0, lo), (m1, hi) = rng.choice(ok), rng.choice(ok)
        pool.append((m0 | m1 | (1 << i), b.node(i, lo, hi)))
    return b, pool[-1][1]


def test_free_bdds() -> None:
    rng = random.Random(1978)
    for n in range(1, 9):
        for _ in range(30):
            b, r = random_free(rng, n, rng.randint(1, 12))
            assert b.is_free(r)
            sat = any(b.evaluate(r, [(a >> j) & 1 for j in range(n)]) for a in range(1 << n))
            assert b.sat_free(r) == sat


def test_is_free_detects_repeats() -> None:
    b = BDD(3)
    u = b.node(2, FALSE, TRUE)
    v = b.node(1, u, TRUE)
    w = b.node(2, v, FALSE)  # x_2 above x_1 above x_2 again
    assert b.is_free(v) and not b.is_free(w)
    assert b.is_free(b.node(0, v, u))
