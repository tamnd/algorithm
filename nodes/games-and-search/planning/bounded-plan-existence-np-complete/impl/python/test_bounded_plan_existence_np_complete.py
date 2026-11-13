# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounded-plan-existence-np-complete/. The authors are listed in prov/T3WXP4.jsonl.

import random
import unittest

from bounded_plan_existence_np_complete import (
    assignment_from_plan, bounded_plan_exists, make_action, plan_from_assignment, sat_to_bounded_planning,
    satisfiable, shortest_plan_length, unbounded_to_bounded, verify_plan,
)


def random_cnf(rng, m, n):
    clauses = []
    for _ in range(n):
        vs = rng.sample(range(1, m + 1), rng.randint(1, min(3, m)))
        clauses.append([v if rng.random() < 0.5 else -v for v in vs])
    return clauses


def shortest_plan(init, goal, acts, k):
    """Breadth-first search that also returns the plan."""
    from collections import deque
    parent = {init: None}
    queue = deque([(init, 0)])
    while queue:
        s, d = queue.popleft()
        if goal <= s:
            plan = []
            while parent[s] is not None:
                s, a = parent[s]
                plan.append(a)
            return plan[::-1]
        if d < k:
            for a in acts:
                if a.pre <= s:
                    t = s | a.add
                    if t != s and t not in parent:
                        parent[t] = (s, a)
                        queue.append((t, d + 1))
    return None


class TestReduction(unittest.TestCase):
    def test_plan_within_bound_iff_satisfiable(self):
        rng = random.Random(1994)
        sat = unsat = 0
        cases = [(1, [[1], [-1]]), (2, [[1, 2], [-1, 2], [1, -2], [-1, -2]])]
        cases += [(3, random_cnf(rng, 3, rng.randint(1, 5))) for _ in range(40)]
        for m, clauses in cases:
            init, goal, acts, k = sat_to_bounded_planning(m, clauses)
            self.assertEqual(k, 2 * m + len(clauses))
            model = satisfiable(m, clauses)
            found = shortest_plan(init, goal, acts, k)
            self.assertEqual(found is not None, model is not None)
            # without the bound the task always has a plan: set both values of every variable
            loose = [x for x in acts if not x.name.startswith("doneF")]
            self.assertTrue(verify_plan(init, goal, loose, len(loose)))
            if model is None:
                unsat += 1
            else:
                sat += 1
                plan = plan_from_assignment(m, clauses, model)
                self.assertTrue(verify_plan(init, goal, plan, k))
                self.assertEqual(len(found), k)
                bits = assignment_from_plan(m, found)
                self.assertTrue(all(any(bits[abs(l) - 1] == (l > 0) for l in c) for c in clauses))
        self.assertGreater(sat, 10)
        self.assertGreater(unsat, 3)

    def test_shape_of_the_task(self):
        init, goal, acts, k = sat_to_bounded_planning(3, [[1, -2, 3], [-1, 2]])
        self.assertEqual(init, frozenset())
        for a in acts:
            self.assertLessEqual(len(a.pre), 1)
            self.assertEqual(len(a.add), 1)
            self.assertEqual(a.delete, frozenset())
        self.assertEqual(len(acts), 4 * 3 + 5)

    def test_certificate_check(self):
        a = make_action("a", [], ["p"])
        b = make_action("b", ["p"], ["q"], ["p"])
        self.assertTrue(verify_plan([], ["q"], [a, b], 2))
        self.assertFalse(verify_plan([], ["q"], [a, b], 1))
        self.assertFalse(verify_plan([], ["q"], [b], 5))
        self.assertFalse(verify_plan([], ["p", "q"], [a, b], 5))


class TestBinaryBound(unittest.TestCase):
    def test_bound_two_to_the_facts_minus_one_is_enough(self):
        rng = random.Random(8)
        for _ in range(300):
            nf = rng.randint(1, 6)
            facts = list(range(nf))
            acts = []
            for j in range(rng.randint(1, 8)):
                pre = rng.sample(facts, rng.randint(0, min(2, nf)))
                add = rng.sample(facts, rng.randint(1, min(2, nf)))
                delete = rng.sample([f for f in facts if f not in add], rng.randint(0, min(2, nf - len(add))))
                acts.append(make_action(f"a{j}", pre, add, delete))
            init = frozenset(f for f in facts if rng.random() < 0.4)
            goal = frozenset(rng.sample(facts, rng.randint(1, nf)))
            i2, g2, a2, k = unbounded_to_bounded(facts, init, goal, acts)
            self.assertEqual(bounded_plan_exists(i2, g2, a2, k), shortest_plan_length(init, goal, acts) is not None)

    def test_counter_reaches_the_bound(self):
        for n in range(1, 7):
            acts = [make_action(f"inc{b}", list(range(b)), [b], list(range(b))) for b in range(n)]
            facts = list(range(n))
            init, goal, a2, k = unbounded_to_bounded(facts, frozenset(), frozenset(facts), acts)
            self.assertEqual(shortest_plan_length(init, goal, a2), k)
            self.assertFalse(bounded_plan_exists(init, goal, a2, k - 1))


if __name__ == "__main__":
    unittest.main()
