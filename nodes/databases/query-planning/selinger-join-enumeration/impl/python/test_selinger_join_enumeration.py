# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selinger-join-enumeration/. The authors are listed in prov/BKRT7Y.jsonl.

import random
from fractions import Fraction
from itertools import permutations

from selinger_join_enumeration import (Query, access_paths, join_order, join_steps, plan_cost, selinger,
                                       selinger_without_orders)


def brute_force(q):
    """Try every left-deep order, every access path for the first relation,
    and every join method at every step."""
    best = None
    for perm in permutations(range(q.n)):
        prefixes = [frozenset(perm[:i]) for i in range(1, q.n)]
        if not q.cross and any(not q.shared(L, j) for L, j in zip(prefixes, perm[1:])):
            continue
        states = [(c, o) for c, o, _ in access_paths(q, perm[0])]
        for L, j in zip(prefixes, perm[1:]):
            states = [(c + extra, out) for c, o in states for extra, out, _, _ in join_steps(q, L, o, j)]
        for c, o in states:
            if q.order_by is not None and o != q.order_by:
                c += 2 * q.size(frozenset(range(q.n)))
            if best is None or c < best:
                best = c
    return best


def random_query(rng, n):
    classes = list(range(rng.randrange(1, 4)))
    cols = [frozenset(k for k in classes if rng.random() < 0.6) for _ in range(n)]
    idx = [frozenset(k for k in cols[i] if rng.random() < 0.4) for i in range(n)]
    card = [rng.choice([1, 5, 10, 50, 100, 1000]) for _ in range(n)]
    sel = {k: Fraction(1, rng.choice([1, 2, 10, 100])) for k in classes}
    order_by = rng.choice([None] + classes)
    return Query(card, cols, idx, sel, order_by, cross=rng.random() < 0.5)


def test_dp_equals_brute_force_on_random_queries():
    rng = random.Random(1979)
    checked = 0
    for t in range(700):
        q = random_query(rng, 5 if t % 50 == 0 else rng.randrange(1, 5))
        cost, plan = selinger(q)
        want = brute_force(q)
        assert cost == want
        if plan is not None:
            again, order, S = plan_cost(q, plan)
            assert again == cost and S == frozenset(range(q.n))
            assert q.order_by is None or order == q.order_by
            assert sorted(join_order(plan)) == list(range(q.n))
            checked += 1
    assert checked >= 500


def test_without_interesting_orders_is_never_better_and_sometimes_worse():
    rng = random.Random(7)
    worse = 0
    for _ in range(400):
        q = random_query(rng, rng.randrange(2, 6))
        c1, _ = selinger(q)
        c2, p2 = selinger_without_orders(q)
        assert (c1 is None) == (c2 is None)
        if c1 is not None:
            assert c1 <= c2 and plan_cost(q, p2)[0] == c2
            worse += c1 < c2
    assert worse > 0


def test_worked_example():
    # Emp(0) 1000 rows, Dept(1) 10 rows, Job(2) 50 rows; Emp.dno = Dept.dno is
    # class 0, Emp.job = Job.job is class 1; Emp has an index on job; ORDER BY job.
    q = Query([1000, 10, 50], [frozenset({0, 1}), frozenset({0}), frozenset({1})],
              [frozenset({1}), frozenset(), frozenset({1})],
              {0: Fraction(1, 10), 1: Fraction(1, 50)}, order_by=1)
    cost, plan = selinger(q)
    assert cost == brute_force(q) == 2210
    assert join_order(plan) == [2, 0, 1]
    # index scan of Job in job order, index nested loop into Emp, nested loop with Dept
    assert plan == ("nlj", ("inl", ("iscan", 2, 1), 0, 1), 1, None)
    assert plan_cost(q, plan)[1] == 1  # the output is in job order, so no final sort
    # Forgetting orders keeps only the cheaper unordered plan for {Emp, Job}
    # (1150 against 1200) and then pays 2000 for the final sort.
    c2, p2 = selinger_without_orders(q)
    assert c2 == 4160 and p2[0] == "sort"
    q.cross = True  # a cross product of Dept and Job is now allowed and helps
    assert selinger(q)[0] == brute_force(q) == 2160


def test_interesting_order_example():
    # Two relations joined on class 0, ORDER BY class 0.
    q = Query([100, 100], [frozenset({0}), frozenset({0})], [frozenset({0}), frozenset({0})],
              {0: Fraction(1, 100)}, order_by=0)
    cost, plan = selinger(q)
    assert cost == brute_force(q)
    assert plan[0] != "sort" and plan_cost(q, plan)[1] == 0


def test_disconnected_without_cross_products():
    q = Query([10, 20], [frozenset({0}), frozenset({1})], [frozenset(), frozenset()],
              {0: Fraction(1, 2), 1: Fraction(1, 2)})
    assert selinger(q) == (None, None) and brute_force(q) is None
    q.cross = True
    cost, plan = selinger(q)
    assert cost == brute_force(q) and plan[0] == "nlj"


def test_single_relation():
    q = Query([7], [frozenset()], [frozenset()], {})
    assert selinger(q) == (7, ("scan", 0))
