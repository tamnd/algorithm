# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/execution-monitoring/. The authors are listed in prov/SF0N1W.jsonl.

import random

from execution_monitoring import (act, applicable, apply, blocks_world, choose_step, execute, execute_naive,
                                  kernels, table_kernel, triangle_table)


# ---- reference: run the rest of the plan ----

def suffix_works(s, plan, k, goal):
    for a in plan[k:]:
        if not applicable(s, a):
            return False
        s = apply(s, a)
    return frozenset(goal) <= s


# ---- the Sussman anomaly ----

A = blocks_world("ABC")
INIT = frozenset({"on C A", "table A", "table B", "clear C", "clear B", "hand empty"})
GOAL = {"on A B", "on B C"}
PLAN = [A[n] for n in ("unstack C A", "putdown C", "pickup B", "stack B C", "pickup A", "stack A B")]


def world_with(events):
    """The real world: the planned effect, unless events[t] gives another next state."""
    return lambda t, s, a: events[t](s, a) if t in events else apply(s, a)


def test_kernels_of_the_sussman_plan():
    ks = kernels(PLAN, GOAL)
    assert ks[0] == {"on C A", "clear C", "hand empty", "table B", "clear B", "table A"}
    assert ks[4] == {"on B C", "clear B", "table A", "clear A", "hand empty"}
    assert ks[6] == GOAL
    table = triangle_table(INIT, PLAN, GOAL)
    assert all(table_kernel(table, len(PLAN), k) == ks[k] for k in range(len(PLAN) + 1))


def test_nominal_run():
    assert execute(INIT, PLAN, GOAL, world_with({})) == ("goal", [0, 1, 2, 3, 4, 5])


def test_serendipity_skips_a_step():
    # someone takes C from the hand and puts it on the table
    events = {0: lambda s, a: apply(apply(s, a), A["putdown C"])}
    assert execute(INIT, PLAN, GOAL, world_with(events)) == ("goal", [0, 2, 3, 4, 5])


def test_failure_repeats_a_step():
    # B slips from the hand and lands on the table
    events = {3: lambda s, a: apply(s, A["putdown B"])}
    assert execute(INIT, PLAN, GOAL, world_with(events)) == ("goal", [0, 1, 2, 3, 2, 3, 4, 5])


def test_undo_goes_back_to_an_earlier_step():
    # someone puts C back on A: the state is the initial state again
    events = {1: lambda s, a: INIT}
    assert execute(INIT, PLAN, GOAL, world_with(events)) == ("goal", [0, 1, 0, 1, 2, 3, 4, 5])
    # a monitor of the next precondition only runs two more steps and then fails
    assert execute_naive(INIT, PLAN, GOAL, world_with(events)) == ("replan", [0, 1, 2, 3])


def test_a_lost_block_is_seen_at_once():
    events = {0: lambda s, a: apply(s, a) - {"table A", "clear A"}}
    assert execute(INIT, PLAN, GOAL, world_with(events)) == ("replan", [0])
    assert execute_naive(INIT, PLAN, GOAL, world_with(events)) == ("replan", [0, 1, 2, 3])


# ---- random STRIPS problems ----

def random_actions(rng, facts, m):
    out = []
    for i in range(m):
        pre = {f for f in facts if rng.random() < 0.25}
        add = {f for f in facts if rng.random() < 0.3}
        dele = {f for f in facts if rng.random() < 0.3} - add
        out.append(act(f"a{i}", pre, add, dele))
    return out


def test_kernel_holds_exactly_when_the_rest_of_the_plan_works():
    rng = random.Random(18)
    facts = [f"f{i}" for i in range(5)]
    for _ in range(300):
        acts = random_actions(rng, facts, 4)
        plan = [rng.choice(acts) for _ in range(rng.randint(0, 5))]
        goal = {f for f in facts if rng.random() < 0.3}
        ks = kernels(plan, goal)
        for _ in range(10):
            s = frozenset(f for f in facts if rng.random() < 0.5)
            for k in range(len(plan) + 1):
                assert (ks[k] is not None and ks[k] <= s) == suffix_works(s, plan, k, goal)
            k = choose_step(s, ks)
            assert k is None or suffix_works(s, plan, k, goal)
            assert k is None or not any(suffix_works(s, plan, j, goal) for j in range(k + 1, len(plan) + 1))


def test_triangle_table_kernels_equal_regression():
    rng = random.Random(19)
    facts = [f"f{i}" for i in range(6)]
    tested = 0
    for _ in range(300):
        acts = random_actions(rng, facts, 5)
        init = frozenset(f for f in facts if rng.random() < 0.5)
        s, plan = init, []
        for _ in range(rng.randint(0, 6)):
            ok = [a for a in acts if applicable(s, a)]
            if not ok:
                break
            a = rng.choice(ok)
            plan.append(a)
            s = apply(s, a)
        goal = {f for f in s if rng.random() < 0.5}
        ks = kernels(plan, goal)
        table = triangle_table(init, plan, goal)
        for k in range(len(plan) + 1):
            assert table_kernel(table, len(plan), k) == ks[k]
        tested += len(plan) > 0
    assert tested > 100
