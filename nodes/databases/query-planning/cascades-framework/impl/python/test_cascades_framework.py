# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cascades-framework/. The authors are listed in prov/SJBPXM.jsonl.

import itertools
import random
import unittest

import dbrel
from cascades_framework import ANY, INF, SORTED, Cascades, Model, cascades, delivered, group_of


def cost(m, p):
    """The cost model of the module docstring, written again for the tests."""
    op, S = p[0], group_of(p)
    if op == "TableScan":
        return m.size(S)
    if op == "IndexScan":
        assert m.indexed[p[1]]
        return 2 * m.size(S)
    if op == "Sort":
        return 2 * m.size(S) + cost(m, p[1])
    if op == "MergeJoin":
        assert delivered(p[1]) == SORTED and delivered(p[2]) == SORTED
    a, b = m.size(group_of(p[1])), m.size(group_of(p[2]))
    local = {"HashJoin": a + 2 * b, "MergeJoin": a + b, "NestedLoop": a * b}[op]
    return local + cost(m, p[1]) + cost(m, p[2])


def all_plans(m, S, memo):
    """Every physical plan for S, with at most one Sort directly above each operator."""
    if S in memo:
        return memo[S]
    base = []
    if len(S) == 1:
        (i,) = S
        base.append(("TableScan", i))
        if m.indexed[i]:
            base.append(("IndexScan", i))
    else:
        items = sorted(S)
        for k in range(1, (1 << len(items)) - 1):
            A = frozenset(x for j, x in enumerate(items) if k >> j & 1)
            for pa in all_plans(m, A, memo):
                for pb in all_plans(m, S - A, memo):
                    base.append(("HashJoin", pa, pb))
                    base.append(("NestedLoop", pa, pb))
                    if delivered(pa) == SORTED and delivered(pb) == SORTED:
                        base.append(("MergeJoin", pa, pb))
    memo[S] = base + [("Sort", p) for p in base]
    return memo[S]


def dp_oracle(m):
    """Bottom-up dynamic program over subsets and the two properties."""
    best = {}
    for r in range(1, m.n + 1):
        for S in map(frozenset, itertools.combinations(range(m.n), r)):
            a = s = INF
            if r == 1:
                (i,) = S
                a = m.card[i]
                if m.indexed[i]:
                    s = 2 * m.card[i]
                    a = min(a, s)
            else:
                items = sorted(S)
                for k in range(1, (1 << r) - 1):
                    A = frozenset(x for j, x in enumerate(items) if k >> j & 1)
                    sa, sb = m.size(A), m.size(S - A)
                    (aa, as_), (ba, bs) = best[A], best[S - A]
                    a = min(a, sa + 2 * sb + aa + ba, sa + sb + as_ + bs, sa * sb + aa + ba)
                    s = min(s, sa + sb + as_ + bs, sa * sb + as_ + ba)
            s = min(s, 2 * m.size(S) + a)
            best[S] = (a, s)
    return best


def random_model(rng, n):
    return Model([rng.choice([1, 10, 50, 100, 1000]) for _ in range(n)],
                 [rng.choice([1, 2, 10, 50, 100]) for _ in range(n)],
                 [rng.random() < 0.4 for _ in range(n)])


def key(row):
    return dbrel.value_key(row["k"])


def execute(p, db, rng):
    """Run a physical plan on lists of rows; the operators without an order shuffle their output."""
    op = p[0]
    if op in ("TableScan", "IndexScan"):
        rows = [dict(zip(db[p[1]].schema, t)) for t in db[p[1]].sorted_rows()]
        rng.shuffle(rows)
        return sorted(rows, key=key) if op == "IndexScan" else rows
    if op == "Sort":
        return sorted(execute(p[1], db, rng), key=key)
    left, right = execute(p[1], db, rng), execute(p[2], db, rng)
    out = []
    if op == "HashJoin":
        table = {}
        for r in right:
            if r["k"] is not None:
                table.setdefault(r["k"], []).append(r)
        out = [{**l, **r} for l in left for r in table.get(l["k"], [])]
        rng.shuffle(out)
    elif op == "NestedLoop":
        out = [{**l, **r} for l in left for r in right if l["k"] is not None and l["k"] == r["k"]]
    else:
        assert [key(r) for r in left] == sorted(map(key, left))
        assert [key(r) for r in right] == sorted(map(key, right))
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i]["k"] is None:
                i += 1
            elif right[j]["k"] is None:
                j += 1
            elif left[i]["k"] < right[j]["k"]:
                i += 1
            elif left[i]["k"] > right[j]["k"]:
                j += 1
            else:
                k, j0 = left[i]["k"], j
                while i < len(left) and left[i]["k"] == k:
                    j = j0
                    while j < len(right) and right[j]["k"] == k:
                        out.append({**left[i], **right[j]})
                        j += 1
                    i += 1
    return out


class CountingCascades(Cascades):
    def __init__(self, m, prune=True):
        super().__init__(m, prune)
        self.rule_tasks = 0
        self.goals = []

    def APPLY_RULE(self, S, e, rule):
        self.rule_tasks += 1
        super().APPLY_RULE(S, e, rule)

    def FINISH(self, ctx):
        self.goals.append((ctx.S, ctx.prop))
        super().FINISH(ctx)


class TestCascades(unittest.TestCase):
    def test_oracle_matches_exhaustive_search(self):
        rng = random.Random(1)
        for n in (1, 2, 2, 3):
            m = random_model(rng, n)
            plans = all_plans(m, frozenset(range(n)), {})
            want = dp_oracle(m)[frozenset(range(n))]
            self.assertEqual(min(cost(m, p) for p in plans), want[0])
            self.assertEqual(min(cost(m, p) for p in plans if delivered(p) == SORTED), want[1])

    def test_optimal_for_both_properties(self):
        rng = random.Random(2)
        for trial in range(40):
            m = random_model(rng, rng.randint(1, 4) if trial % 5 else 5)
            want = dp_oracle(m)
            for j, prop in enumerate((ANY, SORTED)):
                for prune in (True, False):
                    c = Cascades(m, prune)
                    got, p = c.optimize(prop)
                    self.assertEqual(got, want[frozenset(range(m.n))][j])
                    self.assertEqual(cost(m, p), got)
                    if prop == SORTED:
                        self.assertEqual(delivered(p), SORTED)
                    for (S, q), w in c.winner.items():
                        self.assertEqual(w[0], want[S][0 if q == ANY else 1])
                        self.assertEqual(cost(m, c.plan(S, q)), w[0])
                    for (S, q), bound in c.failed.items():
                        self.assertTrue(prune)
                        self.assertLessEqual(bound, want[S][0 if q == ANY else 1])
                    self.assertEqual(c.active, set())
                    self.assertEqual(c.exploring, set())

    def test_exploration_is_complete_and_each_rule_runs_once(self):
        for n in range(1, 7):
            c = CountingCascades(random_model(random.Random(n), n))
            c.optimize(ANY)
            self.assertEqual(len(c.explored), 2 ** n - 1)
            for S in c.explored:
                if len(S) > 1:
                    splits = {(A, S - A) for r in range(1, len(S))
                              for A in map(frozenset, itertools.combinations(sorted(S), r))}
                    self.assertEqual(set(c.exprs[S]), splits)
                    self.assertEqual(len(c.exprs[S]), len(splits))
            self.assertEqual(c.rule_tasks, 2 * (3 ** n - 2 ** (n + 1) + 1))

    def test_without_pruning_each_goal_is_optimized_once(self):
        rng = random.Random(4)
        for n in range(1, 6):
            c = CountingCascades(random_model(rng, n), prune=False)
            c.optimize(SORTED)
            self.assertEqual(len(c.goals), len(set(c.goals)))
            self.assertEqual(set(c.goals), set(c.winner))

    def test_plans_run_and_give_the_join(self):
        rng = random.Random(3)
        for _ in range(40):
            n = rng.randint(1, 4)
            m = random_model(rng, n)
            db = {i: dbrel.random_relation(rng, ["k", "v%d" % i], rng.randint(0, 4),
                                           domain={"k": [0, 1, 2], "v%d" % i: [0, 1]}, null_rate=0.15)
                  for i in range(n)}
            want = db[0]
            for i in range(1, n):
                want = dbrel.natural_join(want, db[i])
            for prop in (ANY, SORTED):
                _, p = cascades(m, prop)
                rows = execute(p, db, rng)
                self.assertEqual(dbrel.Relation(want.schema, [tuple(r[a] for a in want.schema) for r in rows]), want)
                if prop == SORTED:
                    self.assertEqual([key(r) for r in rows], sorted(key(r) for r in rows))

    def test_worked_example(self):
        m = Model([200, 100, 50], [100, 50, 10], [True, False, False])
        c = Cascades(m)
        self.assertEqual(c.optimize(ANY), (950, ("HashJoin", ("TableScan", 0),
                                                 ("HashJoin", ("TableScan", 1), ("TableScan", 2)))))
        self.assertEqual(c.failed, {(frozenset([0, 2]), SORTED): 750})
        self.assertEqual(c.winner[(frozenset([0, 2]), ANY)][0], 550)
        self.assertEqual(cascades(m, SORTED), (1250, ("MergeJoin", ("IndexScan", 0),
                                                      ("Sort", ("HashJoin", ("TableScan", 1), ("TableScan", 2))))))

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            Model([], [], [])
        with self.assertRaises(ValueError):
            Model([1, 2], [1], [False, False])
        with self.assertRaises(ValueError):
            Model([1], [0], [False])
        with self.assertRaises(ValueError):
            cascades(Model([1], [1], [False]), "hashed")
        self.assertEqual(cascades(Model([7], [1], [False]), SORTED), (21, ("Sort", ("TableScan", 0))))
        self.assertEqual(cascades(Model([0, 5], [1, 1], [False, False]))[0], 5)


if __name__ == "__main__":
    unittest.main()
