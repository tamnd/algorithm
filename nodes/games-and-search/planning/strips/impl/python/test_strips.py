# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strips/. The authors are listed in prov/MGC5NA.jsonl.

import random

from strips import (
    applicable,
    bfs_plan,
    blocks_world_actions,
    blocks_world_state,
    is_plan,
    make_action,
    move_actions,
    move_state,
    reachable,
    run_plan,
    successor,
)


def test_successor_hand_cases():
    s = frozenset({"p", "q"})
    a = make_action("a", pre={"p"}, add={"r"}, delete={"q"})
    assert applicable(s, a)
    assert successor(s, a) == frozenset({"p", "r"})
    # A fact in both lists is true afterwards: the delete is applied first.
    b = make_action("b", pre={"p"}, add={"q"}, delete={"q"})
    assert successor(s, b) == s
    # Deleting a fact that is false changes nothing.
    c = make_action("c", pre=(), add=(), delete={"z"})
    assert successor(s, c) == s
    # Preconditions that are not met.
    d = make_action("d", pre={"p", "z"}, add={"r"})
    assert not applicable(s, d)


def test_successor_blocks_hand_case():
    s = blocks_world_state([["a", "c"], ["b"]])
    assert s == frozenset({("ontable", "a"), ("on", "c", "a"), ("clear", "c"), ("ontable", "b"), ("clear", "b"), ("handempty",)})
    acts = {a.name: a for a in blocks_world_actions("abc")}
    t = successor(s, acts["unstack(c,a)"])
    assert t == frozenset({("ontable", "a"), ("clear", "a"), ("holding", "c"), ("ontable", "b"), ("clear", "b")})
    assert not applicable(t, acts["pickup(b)"])
    u = successor(t, acts["putdown(c)"])
    assert u == blocks_world_state([["a"], ["b"], ["c"]])


def test_successor_pointwise_definition():
    rng = random.Random(7)
    universe = list(range(8))
    for _ in range(2000):
        s = frozenset(f for f in universe if rng.random() < 0.5)
        add = frozenset(f for f in universe if rng.random() < 0.3)
        dele = frozenset(f for f in universe if rng.random() < 0.3)
        t = successor(s, make_action("x", (), add, dele))
        for f in universe:
            assert (f in t) == (f in add or (f in s and f not in dele))


def test_run_plan_and_validator():
    acts = {a.name: a for a in blocks_world_actions("abc")}
    init = blocks_world_state([["a", "c"], ["b"]])
    goal = frozenset({("on", "a", "b"), ("on", "b", "c")})
    plan = [acts[n] for n in ["unstack(c,a)", "putdown(c)", "pickup(b)", "stack(b,c)", "pickup(a)", "stack(a,b)"]]
    assert is_plan(init, goal, plan)
    assert run_plan(init, plan[1:]) is None
    assert not is_plan(init, goal, plan[:-1])


def counter_task(n):
    """An n-bit counter: inc(i) needs bit i off and bits 1 to i - 1 on; it sets bit i and clears the lower bits."""
    acts = []
    for i in range(n):
        pre = [("off", i)] + [("on", j) for j in range(i)]
        add = [("on", i)] + [("off", j) for j in range(i)]
        dele = [("off", i)] + [("on", j) for j in range(i)]
        acts.append(make_action(f"inc({i})", pre, add, dele))
    init = frozenset(("off", i) for i in range(n))
    goal = frozenset(("on", i) for i in range(n))
    return init, goal, acts


def test_counter_needs_exponential_plans():
    for n in range(1, 9):
        init, goal, acts = counter_task(n)
        dist = reachable(init, acts)
        assert len(dist) == 2 ** n
        # Exactly one action is applicable in each state except the last one.
        assert sorted(sum(1 for a in acts if applicable(s, a)) for s in dist) == [0] + [1] * (2 ** n - 1)
        assert len(bfs_plan(init, goal, acts)) == 2 ** n - 1


def test_action_counts_and_reachable_states():
    for n in range(1, 6):
        blocks = "abcde"[:n]
        assert len(blocks_world_actions(blocks)) == 2 * n * n
        assert len(move_actions(blocks)) == n * n * (n - 1)
    # Arrangements of n labeled blocks: 1, 3, 13, 73 for n = 1 to 4 (OEIS A000262).
    arrangements = {0: 1, 1: 1, 2: 3, 3: 13, 4: 73}
    for n in range(1, 5):
        blocks = "abcd"[:n]
        init = move_state([list(blocks)])
        assert len(reachable(init, move_actions(blocks))) == arrangements[n]
        init4 = blocks_world_state([list(blocks)])
        # With a hand: every arrangement, plus n choices of the held block times the arrangements of the rest.
        assert len(reachable(init4, blocks_world_actions(blocks))) == arrangements[n] + n * arrangements[n - 1]
