# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dpccp/. The authors are listed in prov/0ECWZS.jsonl.

import math
import random
import unittest
from collections import Counter
from fractions import Fraction

import dbrel
from dpccp import Query, c_out, csg_cmp_pairs, dpccp, enumerate_csg, hash_cost, members, plan_cost


def random_graph(rng, n, extra=0.3):
    sel = {}
    for i in range(1, n):
        j = rng.randrange(i)
        sel[(j, i)] = Fraction(1, rng.choice([1, 2, 5, 10, 100]))
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) not in sel and rng.random() < extra:
                sel[(i, j)] = Fraction(1, rng.choice([1, 2, 5, 10, 100]))
    perm = list(range(n))
    rng.shuffle(perm)
    sel = {(min(perm[i], perm[j]), max(perm[i], perm[j])): f for (i, j), f in sel.items()}
    card = [rng.choice([1, 5, 10, 50, 100, 1000]) for _ in range(n)]
    return Query(card, sel)


def chain(n):
    return Query([10] * n, {(i, i + 1): Fraction(1, 2) for i in range(n - 1)})


def star(n):
    return Query([10] * n, {(0, i): Fraction(1, 2) for i in range(1, n)})


def clique(n):
    return Query([10] * n, {(i, j): Fraction(1, 2) for i in range(n) for j in range(i + 1, n)})


def brute_pairs(q):
    """Unordered csg-cmp pairs, by definition."""
    out = set()
    full = (1 << q.n) - 1
    for A in range(1, full + 1):
        if not q.connected(A):
            continue
        rest = full & ~A
        B = rest
        while B:
            if q.connected(B) and q.neighborhood(A) & B:
                out.add(frozenset((A, B)))
            B = (B - 1) & rest
    return out


def all_trees(q, S, memo):
    """Every ordered bushy tree without cross products for the set S."""
    if S in memo:
        return memo[S]
    if S & (S - 1) == 0:
        memo[S] = [S.bit_length() - 1]
        return memo[S]
    out = []
    A = (S - 1) & S
    while A:
        B = S & ~A
        if q.connected(A) and q.connected(B) and q.neighborhood(A) & B:
            for ta in all_trees(q, A, memo):
                for tb in all_trees(q, B, memo):
                    out.append((ta, tb))
        A = (A - 1) & S
    memo[S] = out
    return out


def tree_cost(q, t, join_cost, sizes):
    def rec(p):
        if isinstance(p, int):
            return Fraction(0), 1 << p
        cl, sl = rec(p[0])
        cr, sr = rec(p[1])
        S = sl | sr
        for X in (sl, sr, S):
            if X not in sizes:
                sizes[X] = q.size(X)
        return cl + cr + join_cost(sizes[sl], sizes[sr], sizes[S]), S
    return rec(t)[0]


def leaves(t):
    return [t] if isinstance(t, int) else leaves(t[0]) + leaves(t[1])


class TestDPccp(unittest.TestCase):
    def test_csgs_are_all_connected_sets_once(self):
        rng = random.Random(1)
        for _ in range(60):
            q = random_graph(rng, rng.randint(1, 8))
            got = list(enumerate_csg(q))
            want = [S for S in range(1, 1 << q.n) if q.connected(S)]
            self.assertEqual(sorted(got), want)

    def test_pairs_are_all_csg_cmp_pairs_once(self):
        rng = random.Random(2)
        for _ in range(60):
            q = random_graph(rng, rng.randint(1, 8))
            got = list(csg_cmp_pairs(q))
            for S1, S2 in got:
                self.assertLess((S1 & -S1), (S2 & -S2))
            self.assertEqual(len(got), len(set(frozenset(p) for p in got)))
            self.assertEqual(set(frozenset(p) for p in got), brute_pairs(q))

    def test_pair_counts_for_chain_star_clique(self):
        for n in range(2, 10):
            self.assertEqual(sum(1 for _ in csg_cmp_pairs(chain(n))), (n ** 3 - n) // 6)
            self.assertEqual(sum(1 for _ in csg_cmp_pairs(star(n))), (n - 1) * 2 ** (n - 2))
            self.assertEqual(sum(1 for _ in csg_cmp_pairs(clique(n))), (3 ** n - 2 ** (n + 1) + 1) // 2)
            if n <= 7:
                for q in (chain(n), star(n), clique(n)):
                    self.assertEqual(sum(1 for _ in csg_cmp_pairs(q)), len(brute_pairs(q)))

    def test_best_plans_are_final_when_used(self):
        rng = random.Random(3)
        for _ in range(60):
            q = random_graph(rng, rng.randint(2, 8))
            for bfs in (True, False):
                total = Counter(A | B for A, B in brute_pairs(q))
                done = Counter()

                def check(S1, S2):
                    self.assertEqual(done[S1], total[S1])
                    self.assertEqual(done[S2], total[S2])
                    done[S1 | S2] += 1

                dpccp(q, on_pair=check, bfs=bfs)
                self.assertEqual(done, total)

    def test_optimal_against_all_trees(self):
        rng = random.Random(4)
        for trial in range(50):
            n = rng.randint(1, 6) if trial % 10 == 0 else rng.randint(1, 5)
            q = random_graph(rng, n, extra=rng.choice([0.0, 0.3, 0.7]))
            trees = all_trees(q, (1 << n) - 1, {})
            sizes = {}
            for join_cost in (c_out, hash_cost):
                for bfs in (True, False):
                    cost, plan = dpccp(q, join_cost, bfs=bfs)
                    self.assertIn(plan, trees)
                    self.assertEqual(plan_cost(q, plan, join_cost), cost)
                    self.assertEqual(min(tree_cost(q, t, join_cost, sizes) for t in trees), cost)

    def test_shape_counts_without_cross_products(self):
        f = math.factorial
        for n in range(1, 6):
            catalan = math.comb(2 * n - 2, n - 1) // n
            self.assertEqual(len(all_trees(chain(n), (1 << n) - 1, {})), catalan * 2 ** (n - 1))
            self.assertEqual(len(all_trees(star(n), (1 << n) - 1, {})), f(n - 1) * 2 ** (n - 1))
            self.assertEqual(len(all_trees(clique(n), (1 << n) - 1, {})), f(2 * n - 2) // f(n - 1))

    def test_plan_runs_and_gives_the_join(self):
        rng = random.Random(5)
        for _ in range(30):
            n = rng.randint(1, 5)
            q = random_graph(rng, n)
            _, plan = dpccp(q, hash_cost)
            self.assertEqual(sorted(leaves(plan)), list(range(n)))
            schema = {v: ["id%d" % v] for v in range(n)}
            for (i, j) in q.sel:
                schema[i].append("k%d_%d" % (i, j))
                schema[j].append("k%d_%d" % (i, j))
            db = {v: dbrel.random_relation(rng, schema[v], rng.randint(0, 5), domain=3, null_rate=0.1)
                  for v in range(n)}

            def run(p):
                if isinstance(p, int):
                    return db[p]
                left, right = run(p[0]), run(p[1])
                self.assertTrue(set(left.schema) & set(right.schema))
                return dbrel.natural_join(left, right)

            naive = db[0]
            for v in range(1, n):
                naive = dbrel.natural_join(naive, db[v])
            self.assertEqual(run(plan), naive)

    def test_worked_example(self):
        q = Query([100, 1000, 100, 10], {(0, 1): Fraction(1, 100), (1, 2): Fraction(1, 2), (2, 3): Fraction(1, 2)})
        cost, plan = dpccp(q)
        self.assertEqual(cost, 251500)
        self.assertEqual(sorted(leaves(plan[0])), [0, 1])

    def test_rejects_disconnected_graphs(self):
        with self.assertRaises(ValueError):
            dpccp(Query([1, 2, 3], {(0, 1): Fraction(1, 2)}))
        self.assertEqual(dpccp(Query([5], {})), (0, 0))

    def test_members(self):
        self.assertEqual(members(0b10110), [1, 2, 4])


if __name__ == "__main__":
    unittest.main()
