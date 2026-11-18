# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/denial-constraint/. The authors are listed in prov/HJ9YV3.jsonl.

import itertools
import random

from denial_constraint import arity, from_fd, satisfies, violations, violations_brute

# Attributes: 0 = Name, 1 = State, 2 = Salary, 3 = Rate.
TAX = [
    ("Ann", "NY", 50, 10),
    ("Bob", "NY", 70, 8),
    ("Cat", "NY", 90, 12),
    ("Dan", "CA", 40, 9),
    ("Eve", "CA", -5, 7),
]
# In one state, a higher salary may not have a lower tax rate.
RATE_DC = [((1, 1), "=", (2, 1)), ((1, 2), "<", (2, 2)), ((1, 3), ">", (2, 3))]
NO_NEGATIVE_SALARY = [((1, 2), "<", ("c", 0))]


def test_tax_example():
    assert violations(TAX, RATE_DC) == {(0, 1)}
    assert violations(TAX, NO_NEGATIVE_SALARY) == {(4,)}
    assert arity(RATE_DC) == 2 and arity(NO_NEGATIVE_SALARY) == 1


def fd_holds(rows, lhs, rhs):
    return all(
        not all(s[a] == t[a] for a in lhs) or all(s[b] == t[b] for b in rhs)
        for s, t in itertools.product(rows, repeat=2)
    )


def random_dc(rng, nattrs):
    dc = []
    for _ in range(rng.randint(1, 3)):
        op = rng.choice(["=", "=", "!=", "<", "<=", ">", ">="])
        left = (rng.choice([1, 1, 2]), rng.randrange(nattrs))
        r = rng.random()
        if r < 0.7:
            right = (rng.choice([1, 2, 2]), rng.randrange(nattrs))
        else:
            right = ("c", rng.randint(0, 3))
        dc.append((left, op, right))
    return dc


def test_against_brute_force_over_pairs():
    rng = random.Random(42)
    for _ in range(300):
        nattrs = rng.randint(1, 4)
        rows = list({tuple(rng.randint(0, 3) for _ in range(nattrs)) for _ in range(rng.randint(0, 12))})
        dc = random_dc(rng, nattrs)
        assert violations(rows, dc) == violations_brute(rows, dc)


def test_functional_dependency_as_denial_constraints():
    rng = random.Random(7)
    for _ in range(200):
        rows = list({tuple(rng.randint(0, 2) for _ in range(3)) for _ in range(rng.randint(0, 8))})
        lhs = rng.sample(range(3), rng.randint(0, 2))
        rhs = [b for b in range(3) if b not in lhs][:1]
        assert satisfies(rows, from_fd(lhs, rhs)) == fd_holds(rows, lhs, rhs)


def test_same_row_is_not_a_pair():
    # t1.A = t2.A alone would be violated by any row paired with itself.
    rows = [(1,), (2,)]
    assert violations(rows, [((1, 0), "=", (2, 0))]) == set()
    assert violations(rows, [((1, 0), "<", (2, 0))]) == {(0, 1)}
