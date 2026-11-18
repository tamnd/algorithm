# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dphyp/. The authors are listed in prov/CD2W8Y.jsonl.

import random
import unittest
from collections import Counter
from fractions import Fraction

import dbrel
from dphyp import DPhyp, Hypergraph, c_out, dphyp, hash_cost, members, plan_cost


def connected_sets(h):
    """The connected sets by the recursive definition."""
    conn = set()
    for S in sorted(range(1, 1 << h.n), key=lambda s: bin(s).count("1")):
        if S & (S - 1) == 0:
            conn.add(S)
            continue
        A = (S - 1) & S
        while A:
            if A in conn and S & ~A in conn and h.joins(A, S & ~A):
                conn.add(S)
                break
            A = (A - 1) & S
    return conn


def brute_pairs(h):
    cs = connected_sets(h)
    return {frozenset((A, B)) for A in cs for B in cs if A & B == 0 and h.joins(A, B)}


def all_trees(h, S, memo):
    if S in memo:
        return memo[S]
    if S & (S - 1) == 0:
        memo[S] = [S.bit_length() - 1]
        return memo[S]
    out = []
    A = (S - 1) & S
    while A:
        B = S & ~A
        if h.joins(A, B):
            for ta in all_trees(h, A, memo):
                for tb in all_trees(h, B, memo):
                    out.append((ta, tb))
        A = (A - 1) & S
    memo[S] = out
    return out


def random_hypergraph(rng, n, hyper=3):
    edges = []
    for i in range(1, n):
        edges.append((1 << rng.randrange(i), 1 << i, Fraction(1, rng.choice([1, 2, 10]))))
    for _ in range(rng.randint(0, hyper)):
        if n < 2:
            break
        vs = rng.sample(range(n), rng.randint(2, n))
        cut = rng.randint(1, len(vs) - 1)
        edges.append((sum(1 << v for v in vs[:cut]), sum(1 << v for v in vs[cut:]),
                      Fraction(1, rng.choice([1, 2, 10]))))
    if n >= 2 and rng.random() < 0.5:
        edges = edges[rng.randint(0, n - 1):]
    return Hypergraph([rng.choice([1, 10, 100]) for _ in range(n)], edges)


def simple(n, pairs):
    return Hypergraph([10] * n, [(1 << i, 1 << j, Fraction(1, 2)) for i, j in pairs])


def leaves(t):
    return [t] if isinstance(t, int) else leaves(t[0]) + leaves(t[1])


class Recorder(DPhyp):
    def __init__(self, h):
        super().__init__(h)
        self.csgs = []

    def emit_csg(self, S1):
        self.csgs.append(S1)
        super().emit_csg(S1)


class TestDPhyp(unittest.TestCase):
    def test_every_cut_of_a_connected_set_is_crossed(self):
        rng = random.Random(1)
        for _ in range(100):
            h = random_hypergraph(rng, rng.randint(2, 6))
            for T in connected_sets(h):
                S = (T - 1) & T
                while S:
                    self.assertTrue(h.joins(S, T & ~S))
                    S = (S - 1) & T

    def test_pairs_once_and_plans_final_when_used(self):
        rng = random.Random(2)
        for _ in range(400):
            h = random_hypergraph(rng, rng.randint(1, 7))
            want = brute_pairs(h)
            total = Counter(A | B for A, B in want)
            done, got = Counter(), []

            def check(S1, S2):
                got.append(frozenset((S1, S2)))
                self.assertLess(S1 & -S1, S2 & -S2)
                self.assertEqual(done[S1], total[S1])
                self.assertEqual(done[S2], total[S2])
                done[S1 | S2] += 1

            r = DPhyp(h, on_pair=check)
            try:
                r.solve()
            except ValueError:
                self.assertNotIn((1 << h.n) - 1, connected_sets(h))
            self.assertEqual(len(got), len(set(got)))
            self.assertEqual(set(got), want)

    def test_each_connected_set_is_emitted_once(self):
        rng = random.Random(3)
        for _ in range(150):
            h = random_hypergraph(rng, rng.randint(1, 7))
            r = Recorder(h)
            try:
                r.solve()
            except ValueError:
                pass
            self.assertEqual(sorted(r.csgs), sorted(connected_sets(h)))

    def test_simple_graphs_give_the_dpccp_counts(self):
        for n in range(2, 9):
            chain = simple(n, [(i, i + 1) for i in range(n - 1)])
            star = simple(n, [(0, i) for i in range(1, n)])
            clique = simple(n, [(i, j) for i in range(n) for j in range(i + 1, n)])
            for h, want in ((chain, (n ** 3 - n) // 6), (star, (n - 1) * 2 ** (n - 2)),
                            (clique, (3 ** n - 2 ** (n + 1) + 1) // 2)):
                pairs = []
                dphyp(h, on_pair=lambda a, b: pairs.append((a, b)))
                self.assertEqual(len(pairs), want)

    def test_optimal_against_all_trees(self):
        rng = random.Random(4)
        tried = 0
        while tried < 60:
            h = random_hypergraph(rng, rng.randint(1, 5 if tried % 10 else 6))
            full = (1 << h.n) - 1
            trees = all_trees(h, full, {})
            if not trees:
                with self.assertRaises(ValueError):
                    dphyp(h)
                continue
            tried += 1
            for join_cost in (c_out, hash_cost):
                cost, plan = dphyp(h, join_cost)
                self.assertIn(plan, trees)
                self.assertEqual(plan_cost(h, plan, join_cost), cost)
                self.assertEqual(min(plan_cost(h, t, join_cost) for t in trees), cost)

    def test_plan_runs_and_gives_the_join(self):
        rng = random.Random(5)
        runs = 0
        while runs < 25:
            h = random_hypergraph(rng, rng.randint(1, 4))
            try:
                _, plan = dphyp(h)
            except ValueError:
                continue
            runs += 1
            db = {v: dbrel.random_relation(rng, ["id%d" % v, "x%d" % v], rng.randint(0, 4), domain=3,
                                           null_rate=0.1) for v in range(h.n)}

            def pred_of(u, w):
                def pred(row):
                    xs = [row["x%d" % i] for i in members(u) + members(w)]
                    if any(x is None for x in xs):
                        return None
                    return (sum(row["x%d" % i] for i in members(u)) - sum(row["x%d" % j] for j in members(w))) % 3 == 0
                return pred

            def conj(preds):
                def pred(row):
                    v = True
                    for p in preds:
                        v = dbrel.tv_and(v, p(row))
                    return v
                return pred

            def run(p):
                if isinstance(p, int):
                    return db[p], 1 << p
                (left, sl), (right, sr) = run(p[0]), run(p[1])
                S = sl | sr
                preds = [pred_of(u, w) for u, w, _ in h.edges
                         if (u | w) & ~S == 0 and (u | w) & ~sl and (u | w) & ~sr]
                self.assertTrue(preds)
                return dbrel.theta_join(left, right, conj(preds)), S

            naive = db[0]
            for v in range(1, h.n):
                naive = dbrel.product(naive, db[v])
            naive = dbrel.select(naive, conj([pred_of(u, w) for u, w, _ in h.edges]))
            self.assertEqual(run(plan)[0], naive)

    def test_worked_example(self):
        A, B, C, D = 1, 2, 4, 8
        h = Hypergraph([10, 20, 30, 40], [(A, B, Fraction(1, 10)), (C, D, Fraction(1, 10)),
                                          (A | B, C | D, Fraction(1, 100))])
        pairs = []
        cost, plan = dphyp(h, on_pair=lambda a, b: pairs.append((a, b)))
        self.assertEqual(pairs, [(C, D), (A, B), (A | B, C | D)])
        self.assertEqual(cost, 164)
        self.assertEqual(plan, ((0, 1), (2, 3)))
        r = Recorder(h)
        r.solve()
        self.assertEqual(r.csgs, [D, C, C | D, B, A, A | B, A | B | C | D])

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            Hypergraph([1, 2], [(1, 1, Fraction(1))])
        with self.assertRaises(ValueError):
            dphyp(Hypergraph([1, 2, 3], [(1, 2, Fraction(1, 2))]))
        self.assertEqual(dphyp(Hypergraph([5], [])), (0, 0))


if __name__ == "__main__":
    unittest.main()
