# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-valued-decision-diagram/. The authors are listed in prov/C9XT2M.jsonl.

import operator
import random
from itertools import product

from multi_valued_decision_diagram import MDD

OPS = [operator.and_, operator.or_, operator.xor, max, operator.add]


def points(d: list[int]) -> list[list[int]]:
    """All x in index order (x_0 is the least significant digit)."""
    return [list(reversed(p)) for p in product(*[range(k) for k in reversed(d)])]


def test_apply_and_count_against_tables() -> None:
    rng = random.Random(1990)
    checked = 0
    for _ in range(600):
        n = rng.randrange(0, 5)
        d = [rng.randrange(1, 5) for _ in range(n)]
        m = MDD(d)
        xs = points(d)
        assert [m.index(x) for x in xs] == list(range(len(xs)))
        s = [rng.randrange(2) for _ in xs]
        t = [rng.randrange(2) for _ in xs]
        f, g = m.from_table(s), m.from_table(t)
        assert [m.evaluate(f, x) for x in xs] == s
        op = rng.choice(OPS)
        h = m.apply(op, f, g)
        expect = [op(a, b) for a, b in zip(s, t)]
        assert [m.evaluate(h, x) for x in xs] == expect
        assert h == m.from_table(expect)
        assert m.count(f) == sum(s)
        m.check_invariant()
        checked += 1
    assert checked >= 500


def test_all_different() -> None:
    for k in range(1, 5):
        m = MDD([k] * k)
        xs = points([k] * k)
        f = m.from_table([int(len(set(x)) == k) for x in xs])
        assert m.count(f) == [1, 2, 6, 24][k - 1]
        # one node for each set of used values on each level, and the two sinks;
        # with k = 1 the one variable has one value, so f is the constant 1
        assert m.size(f) == (2 ** k + 1 if k > 1 else 1)
