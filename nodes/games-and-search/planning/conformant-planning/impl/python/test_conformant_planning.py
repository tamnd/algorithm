# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conformant-planning/. The authors are listed in prov/9DV4RS.jsonl.

import random
from itertools import product

from conformant_planning import bomb_in_toilet, conformant_bfs, is_conformant, progress


def brute_force_length(init, goal, actions, succ, max_len):
    """The length of a shortest conformant plan, by trying every action sequence in order of length."""
    for k in range(max_len + 1):
        for plan in product(actions, repeat=k):
            if is_conformant(list(plan), init, goal, succ):
                return k
    return None


def test_bomb_in_the_toilet():
    for n in range(1, 6):
        init, goal, actions, succ = bomb_in_toilet(n)
        plan, expanded = conformant_bfs(init, goal, actions, succ)
        assert len(plan) == 2 * n - 1
        assert is_conformant(plan, init, goal, succ)
        assert expanded == 2 ** (n + 1) - 3
    init, goal, actions, succ = bomb_in_toilet(3)
    assert brute_force_length(init, goal, actions, succ, 5) == 5
    # without the flush the toilet stays clogged and there is no plan for two packages
    init, goal, actions, succ = bomb_in_toilet(2)
    plan, _ = conformant_bfs(init, goal, [a for a in actions if a[0] == "dunk"], succ)
    assert plan is None


def test_corridor_without_sensing():
    succ = lambda s, a: {max(s - 1, 1)} if a == "left" else {min(s + 1, 4)}
    plan, _ = conformant_bfs([1, 2, 3, 4], lambda s: s == 1, ["left", "right"], succ)
    assert plan == ["left"] * 3
    b = frozenset([1, 2, 3, 4])
    sizes = []
    for a in plan:
        b = progress(b, a, succ)
        sizes.append(len(b))
    assert sizes == [3, 2, 1]
    # a slippery right move that goes one or two cells
    slip = lambda s, a: {max(s - 1, 1)} if a == "left" else {min(s + 1, 4), min(s + 2, 4)}
    plan, _ = conformant_bfs([1, 2], lambda s: s == 4, ["left", "right"], slip)
    assert plan == ["right"] * 3
    assert is_conformant(plan, [1, 2], lambda s: s == 4, slip)
    assert brute_force_length([1, 2], lambda s: s == 4, ["left", "right"], slip, 4) == 3


def random_problem(rng, n, k):
    states = list(range(n))
    table = {}
    for s in states:
        for a in range(k):
            if rng.random() < 0.15:
                table[s, a] = set()
            else:
                table[s, a] = {t for t in states if rng.random() < 0.3} or {rng.choice(states)}
    init = [s for s in states if rng.random() < 0.6] or [0]
    goals = {s for s in states if rng.random() < 0.3} or {n - 1}
    return init, (lambda s: s in goals), list(range(k)), (lambda s, a: table[s, a])


def test_against_all_action_sequences():
    rng = random.Random(12)
    found = 0
    for _ in range(150):
        n = rng.randint(1, 3)
        init, goal, actions, succ = random_problem(rng, n, rng.randint(1, 3))
        plan, _ = conformant_bfs(init, goal, actions, succ)
        # a shortest plan visits distinct beliefs, so its length is below 2^n - 1
        exact = brute_force_length(init, goal, actions, succ, 2 ** n - 2)
        if plan is None:
            assert exact is None
        else:
            found += 1
            assert is_conformant(plan, init, goal, succ)
            assert len(plan) == exact
    assert found > 30


def test_plans_for_four_states():
    rng = random.Random(13)
    for _ in range(40):
        init, goal, actions, succ = random_problem(rng, 4, 2)
        plan, _ = conformant_bfs(init, goal, actions, succ)
        exact = brute_force_length(init, goal, actions, succ, 9)
        if plan is not None and len(plan) <= 9:
            assert exact == len(plan) and is_conformant(plan, init, goal, succ)
        else:
            assert exact is None
