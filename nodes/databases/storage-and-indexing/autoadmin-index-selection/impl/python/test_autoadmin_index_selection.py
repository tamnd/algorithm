# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/autoadmin-index-selection/. The authors are listed in prov/Q7Z4FQ.jsonl.

import random
import unittest
from itertools import combinations

from autoadmin_index_selection import (Select, Table, Tool, Update, WhatIf,
                                       all_indexes, brute_force)


def page_example():
    t = Table("T", 100000, (("a", 1000), ("b", 100), ("c", 10), ("d", 50000)))
    w = [Select(50, "T", eq=("a",), out=("d",)),
         Select(30, "T", eq=("a", "b")),
         Select(20, "T", rng="d", rng_sel=0.001, out=("c",)),
         Update(10, "T", ("b",))]
    return [t], w


def random_instance(rng):
    cols = ["a", "b", "c", "d", "e"]
    t = Table("T", 100000, tuple((c, rng.choice([2, 10, 100, 1000, 50000])) for c in cols))
    s = Table("S", 20000, tuple((c, rng.choice([2, 10, 100, 1000])) for c in ["x", "y", "z"]))
    w = []
    for _ in range(rng.randrange(3, 7)):
        tab, cs = (t, cols) if rng.random() < 0.7 else (s, ["x", "y", "z"])
        eq = tuple(rng.sample(cs, rng.randrange(0, 3)))
        rest = [c for c in cs if c not in eq]
        rc = rng.choice(rest) if (rng.random() < 0.5 or not eq) else None
        pool = [c for c in rest if c != rc]
        out = tuple(rng.sample(pool, min(len(pool), rng.randrange(0, 2))))
        w.append(Select(rng.randrange(1, 50), tab.name, eq, rc, rng.choice([0.001, 0.01, 0.1]), out))
    for _ in range(rng.randrange(0, 2)):
        w.append(Update(rng.randrange(1, 200), "T", tuple(rng.sample(cols, 1))))
    return [t, s], w


class TestExample(unittest.TestCase):
    def test_page_example(self):
        tabs, w = page_example()
        wi = WhatIf(tabs)
        tool = Tool(wi, w, k=2, m=2, width=2)
        chosen = tool.run()
        self.assertEqual(tool.trace[0][2], [("T", ("a",)), ("T", ("d",))])
        self.assertEqual(tool.trace[1][1], [("T", ("a",)), ("T", ("a", "b")), ("T", ("a", "d")),
                                            ("T", ("d",)), ("T", ("d", "c"))])
        self.assertEqual(sorted(chosen), [("T", ("a", "d")), ("T", ("d", "c"))])
        self.assertEqual(tool.cost(w, ()), 50 * 5000 + 30 * 5000 + 20 * 5000 + 10)
        self.assertEqual(tool.cost(w, [("T", ("a",)), ("T", ("d",))]), 10310)
        self.assertEqual(tool.cost(w, chosen), 3660)
        self.assertEqual(tool.cost(w, [("T", ("a", "b")), ("T", ("d", "c"))]), 5451.5)
        self.assertEqual(wi.calls, 21)
        self.assertEqual(len(tool.pairs), 84)
        self.assertEqual(brute_force(Tool(WhatIf(tabs), w, k=2))[0], 3660)


class TestParts(unittest.TestCase):
    def test_atomic_configurations_give_the_optimizer_cost(self):
        """cost(Q, C) from single-index what-if calls equals the optimizer on all of C."""
        rng = random.Random(1)
        for seed in range(40):
            tabs, w = random_instance(random.Random(seed))
            wi = WhatIf(tabs)
            tool = Tool(wi, w, k=3)
            idx = all_indexes(tool)
            for _ in range(20):
                c = frozenset(rng.sample(idx, min(len(idx), rng.randrange(0, 5))))
                for q in w:
                    self.assertAlmostEqual(tool.query_cost(q, c), wi.optimize(q, c))

    def test_greedy_with_m_at_least_k_is_exhaustive(self):
        for seed in range(25):
            tabs, w = random_instance(random.Random(seed))
            tool = Tool(WhatIf(tabs), w, k=2, m=2)
            cands = all_indexes(tool)
            got = tool.cost(w, tool.enumerate(w, cands, 2))
            best = min(tool.cost(w, s) for r in range(3) for s in combinations(cands, r))
            self.assertAlmostEqual(got, best)

    def test_greedy_steps_only_lower_the_cost(self):
        for seed in range(25):
            tabs, w = random_instance(random.Random(seed))
            tool = Tool(WhatIf(tabs), w, k=4, m=1)
            cands = all_indexes(tool)
            prev = tool.cost(w, ())
            for k in range(1, 5):
                c = tool.cost(w, tool.enumerate(w, cands, k))
                self.assertLessEqual(c, prev + 1e-9)
                prev = c
            self.assertLessEqual(len(tool.enumerate(w, cands, 4)), 4)

    def test_mc_lead_extends_chosen_indexes(self):
        tabs, w = page_example()
        tool = Tool(WhatIf(tabs), w, k=2)
        ext = tool.admissible(2, [("T", ("a",))])
        self.assertEqual(sorted(ext), [("T", ("a", "b")), ("T", ("a", "c")), ("T", ("a", "d"))])


class TestAgainstBruteForce(unittest.TestCase):
    def test_tool_against_the_optimum(self):
        found, ratios = 0, []
        calls = pairs = 0
        for seed in range(40):
            tabs, w = random_instance(random.Random(seed))
            wi = WhatIf(tabs)
            tool = Tool(wi, w, k=3, m=2, width=2)
            chosen = tool.run()
            self.assertLessEqual(len(chosen), 3)
            got = tool.cost(w, chosen)
            best, _ = brute_force(Tool(WhatIf(tabs), w, k=3, width=2))
            self.assertGreaterEqual(got, best - 1e-6)            # never better than the optimum
            self.assertLessEqual(got, tool.cost(w, ()) + 1e-9)   # never worse than no index
            found += abs(got - best) < 1e-6
            ratios.append(got / best)
            calls += wi.calls
            pairs += len(tool.pairs)
        self.assertGreaterEqual(found, 15)       # a heuristic: it often, not always, finds the optimum
        self.assertLess(calls * 3, pairs)        # atomic configurations save what-if calls


if __name__ == "__main__":
    unittest.main()
