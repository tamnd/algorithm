# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strips-plan-existence-pspace-complete/. The authors are listed in prov/NF2ETY.jsonl.

import random
import unittest

from strips_plan_existence_pspace_complete import (
    all_states, bfs_distance, decode, hanoi_task, make_action, ntm_accepts, plan_exists_savitch,
    reachable_states, run_dtm, savitch_reach, tm_to_strips,
)

BLANK = "_"
ALPHABET = ["0", "1", BLANK]


def random_machine(rng, n_states, deterministic):
    states = [f"q{k}" for k in range(n_states)] + ["acc"]
    delta = {}
    for q in states[:-1]:
        for x in ALPHABET:
            r = rng.random()
            if r < 0.15:
                continue                                   # no move: the machine halts
            count = 1 if deterministic else rng.randint(1, 2)
            delta[(q, x)] = [(rng.choice(states), rng.choice(ALPHABET), rng.choice((-1, 0, 1))) for _ in range(count)]
    return states, ALPHABET, delta, "q0", "acc", BLANK


class TestReduction(unittest.TestCase):
    def test_deterministic_machines(self):
        rng = random.Random(1994)
        accepted = 0
        for _ in range(300):
            machine = random_machine(rng, rng.randint(1, 4), True)
            p = rng.randint(1, 4)
            word = [rng.choice("01") for _ in range(rng.randint(0, p))]
            init, goal, acts = tm_to_strips(machine, word, p)
            has_plan = bfs_distance(init, goal, acts) is not None
            self.assertEqual(has_plan, run_dtm(machine, word, p))
            accepted += has_plan
        self.assertGreater(accepted, 30)
        self.assertLess(accepted, 270)

    def test_nondeterministic_machines(self):
        rng = random.Random(7)
        for _ in range(200):
            machine = random_machine(rng, rng.randint(1, 3), False)
            p = rng.randint(1, 3)
            word = [rng.choice("01") for _ in range(rng.randint(0, p))]
            init, goal, acts = tm_to_strips(machine, word, p)
            self.assertEqual(bfs_distance(init, goal, acts) is not None, ntm_accepts(machine, word, p))

    def test_states_encode_configurations(self):
        rng = random.Random(3)
        for _ in range(100):
            machine = random_machine(rng, 3, False)
            p = 3
            init, goal, acts = tm_to_strips(machine, ["1", "0"], p)
            states, alphabet = machine[0], machine[1]
            n_facts = p * len(states) + p * len(alphabet) + 1
            self.assertLessEqual(len({f for a in acts for f in a.pre | a.add | a.delete} | init), n_facts)
            for a in acts:
                self.assertTrue(len(a.pre) <= 2 and not (a.add & a.delete))
            for s in reachable_states(init, acts):
                self.assertIsNotNone(decode(s - {("accept",)}, p))

    def test_size_of_the_task(self):
        machine = random_machine(random.Random(0), 4, True)
        init, goal, acts = tm_to_strips(machine, ["1"], 5)
        moves = sum(len(m) for m in machine[2].values())
        self.assertLessEqual(len(acts), 5 * moves + 5)


class TestMembership(unittest.TestCase):
    def test_savitch_agrees_with_bfs(self):
        rng = random.Random(1970)
        yes = 0
        for _ in range(150):
            nf = rng.randint(1, 3)
            facts = list(range(nf))
            acts = []
            for k in range(rng.randint(1, 4)):
                pre = rng.sample(facts, rng.randint(0, nf))
                add = rng.sample(facts, rng.randint(1, nf))
                delete = rng.sample([f for f in facts if f not in add], rng.randint(0, nf - len(add)))
                acts.append(make_action(f"a{k}", pre, add, delete))
            init = frozenset(f for f in facts if rng.random() < 0.5)
            goal = frozenset(rng.sample(facts, rng.randint(1, nf)))
            ref = bfs_distance(init, goal, acts) is not None
            self.assertEqual(plan_exists_savitch(facts, init, goal, acts), ref)
            yes += ref
        self.assertGreater(yes, 20)

    def test_reach_bound_is_tight_on_a_counter(self):
        # a 3-bit binary counter: inc_k needs bits 0..k-1, sets bit k and clears
        # the lower bits; 7 increments go from 000 to 111 and no path is shorter
        facts = [0, 1, 2]
        acts = [make_action(f"inc{k}", list(range(k)), [k], list(range(k))) for k in range(3)]
        start, top = frozenset(), frozenset(facts)
        self.assertEqual(bfs_distance(start, top, acts), 7)
        universe = all_states(facts)
        self.assertTrue(savitch_reach(start, top, 3, acts, universe))
        self.assertFalse(savitch_reach(start, top, 2, acts, universe))


class TestLongPlans(unittest.TestCase):
    def test_hanoi_needs_exponentially_many_moves(self):
        for n in range(1, 7):
            init, goal, acts = hanoi_task(n)
            self.assertEqual(bfs_distance(init, goal, acts), 2 ** n - 1)
            self.assertEqual(len(reachable_states(init, acts)), 3 ** n)


if __name__ == "__main__":
    unittest.main()
