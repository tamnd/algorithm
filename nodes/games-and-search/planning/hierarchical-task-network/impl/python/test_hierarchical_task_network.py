# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hierarchical-task-network/. The authors are listed in prov/8H40VK.jsonl.

import random
from itertools import product

from hierarchical_task_network import (Labeled, accepts, anbn_domain, operator, reachable_states, solution_set,
                                       strips_as_htn)


def run(init, ops, names):
    table = {o.name: o for o in ops}
    state = frozenset(init)
    for n in names:
        o = table[n]
        if not o.pre <= state:
            return None
        state = (state - o.delete) | o.add
    return state


def random_ops(rng, facts, k):
    return [operator(f"o{i}", rng.sample(facts, rng.randint(0, 2)), rng.sample(facts, rng.randint(1, 2)),
                     rng.sample(facts, rng.randint(0, 1))) for i in range(k)]


def test_anbn_is_the_solution_set():
    domain = anbn_domain()
    for depth in range(7):
        expected = {("a",) * n + ("b",) * n for n in range(1, depth + 1)}
        assert solution_set([], ["S"], domain, depth) == expected


def test_strips_task_as_tail_recursive_htn():
    rng = random.Random(71)
    nonempty = 0
    for _ in range(150):
        facts = ["p", "q", "r"]
        ops = random_ops(rng, facts, rng.randint(1, 3))
        init = [f for f in facts if rng.random() < 0.4]
        goal = rng.sample(facts, rng.randint(1, 2))
        depth = 4
        expected = set()
        for length in range(depth):
            for names in product([o.name for o in ops], repeat=length):
                final = run(init, ops, names)
                if final is not None and set(goal) <= final:
                    expected.add(names)
        found = solution_set(init, ["solve"], strips_as_htn(ops, goal), depth)
        assert found == expected
        for plan in found:
            assert set(goal) <= run(init, ops, plan)
        nonempty += bool(found)
    assert nonempty > 50


def random_labeled(rng, n_facts):
    facts = [f"f{i}" for i in range(n_facts)]
    actions = []
    for i in range(rng.randint(2, 4)):
        op = operator(f"x{i}", rng.sample(facts, rng.randint(0, 1)), rng.sample(facts, rng.randint(0, 1)),
                      rng.sample(facts, rng.randint(0, 1)))
        actions.append(Labeled(rng.choice("ab"), op))
    init = [f for f in facts if rng.random() < 0.5]
    goal = rng.sample(facts, rng.randint(0, 2))
    return init, goal, actions


def test_strips_plan_sets_are_pumpable():
    """If a^n b^n is a plan and n is at least the number of reachable states, then the
    a-part revisits a state, so a^(n+i) b^n is a plan for some i between 1 and n.
    Hence no STRIPS task has exactly the plans a^n b^n."""
    rng = random.Random(72)
    pumped = 0
    for _ in range(400):
        init, goal, actions = random_labeled(rng, 3)
        size = len(reachable_states(init, actions))
        for n in range(size, size + 3):
            if accepts(init, goal, actions, "a" * n + "b" * n):
                assert any(accepts(init, goal, actions, "a" * (n + i) + "b" * n) for i in range(1, n + 1))
                pumped += 1
    assert pumped > 30


def test_no_small_strips_task_matches_the_htn():
    rng = random.Random(73)
    words = ["a" * i + "b" * j for i in range(7) for j in range(7)]
    htn = {"a" * n + "b" * n for n in range(1, 7)}
    for _ in range(400):
        init, goal, actions = random_labeled(rng, 3)
        accepted = {w for w in words if accepts(init, goal, actions, w)}
        assert accepted != htn
