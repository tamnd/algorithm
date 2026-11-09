# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algebraic-decision-diagram/. The authors are listed in prov/1TQF00.jsonl.

import operator
import random

from algebraic_decision_diagram import ADD

OPS = [operator.add, operator.mul, max, min]


def random_table(rng: random.Random, n: int) -> list[int]:
    k = rng.randrange(1, 5)
    return [rng.randrange(k) for _ in range(1 << n)]


def test_apply_against_tables() -> None:
    rng = random.Random(1993)
    checked = 0
    for _ in range(600):
        n = rng.randrange(0, 9)
        d = ADD(n)
        s, t = random_table(rng, n), random_table(rng, n)
        f, g = d.from_table(s), d.from_table(t)
        assert [d.evaluate(f, a) for a in range(1 << n)] == s
        op = rng.choice(OPS)
        h = d.apply(op, f, g)
        expect = [op(x, y) for x, y in zip(s, t)]
        assert [d.evaluate(h, a) for a in range(1 << n)] == expect
        assert h == d.from_table(expect)  # canonical
        if n:
            v = rng.randrange(n)
            r = d.sum_out(f, v)
            assert [d.evaluate(r, a) for a in range(1 << n)] == [s[a & ~(1 << v)] + s[a | 1 << v] for a in range(1 << n)]
        th = d.threshold(f, 2)
        assert [d.evaluate(th, a) for a in range(1 << n)] == [int(x >= 2) for x in s]
        d.check_invariant()
        checked += 1
    assert checked >= 500


def test_sum_of_all_values() -> None:
    rng = random.Random(5)
    for n in range(1, 8):
        d = ADD(n)
        s = [rng.randrange(10) for _ in range(1 << n)]
        f = d.from_table(s)
        for v in range(n):
            f = d.sum_out(f, v)
        assert d.is_const(f) and d.value(f) == sum(s)


def test_sum_of_weights_is_small() -> None:
    # f(x) = x_0 + 2 x_1 + 4 x_2 + ... has 2^n values, so its ADD has 2^(n+1) - 1 nodes
    for n in range(1, 8):
        d = ADD(n)
        f = d.from_table(list(range(1 << n)))
        assert d.size(f) == (1 << (n + 1)) - 1
