# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sussman-anomaly/. The authors are listed in prov/0Z947C.jsonl.

from sussman_anomaly import (
    GOAL,
    ON_A_B,
    ON_B_C,
    bfs_plan,
    plans_up_to,
    protected_plan,
    run_plan,
    serial_plans,
    shortest_length,
    sussman_task,
)


def names(seq):
    return [a.name for a in seq]


def test_optimal_plan_by_enumeration():
    init, acts = sussman_task(hand=False)
    plans = plans_up_to(init, GOAL, acts, 3)
    assert [names(p) for p in plans] == [["move(c,a,table)", "move(b,table,c)", "move(a,table,b)"]]
    assert plans_up_to(init, GOAL, acts, 2) == []
    init4, acts4 = sussman_task(hand=True)
    plans4 = plans_up_to(init4, GOAL, acts4, 6)
    assert [names(p) for p in plans4] == [["unstack(c,a)", "putdown(c)", "pickup(b)", "stack(b,c)", "pickup(a)", "stack(a,b)"]]
    assert plans_up_to(init4, GOAL, acts4, 5) == []


def test_serial_plans_are_longer():
    for hand, optimal, serial in ((False, 3, 5), (True, 6, 10)):
        init, acts = sussman_task(hand)
        assert shortest_length(init, GOAL, acts) == optimal
        for first in (ON_A_B, ON_B_C):
            found = serial_plans(init, first, GOAL, acts, serial)
            assert found, "a serial plan exists in each order"
            assert min(len(p) for p in found) == serial
            assert serial_plans(init, first, GOAL, acts, serial - 1) == []


def test_serial_plan_shapes():
    init, acts = sussman_task(hand=False)
    first_ab = bfs_plan(init, ON_A_B, acts)
    assert names(first_ab) == ["move(c,a,table)", "move(a,table,b)"]
    first_bc = bfs_plan(init, ON_B_C, acts)
    assert names(first_bc) == ["move(b,table,c)"]
    # After the shortest plan for on(B, C), the stack is A, C, B and the goal is 4 moves away.
    assert shortest_length(run_plan(init, first_bc), GOAL, acts) == 4
    assert shortest_length(run_plan(init, first_ab), GOAL, acts) == 3


def test_protecting_the_first_goal_fails():
    for hand in (False, True):
        init, acts = sussman_task(hand)
        assert protected_plan(init, ON_A_B, GOAL, acts) is None
        assert protected_plan(init, ON_B_C, GOAL, acts) is None


def test_optimal_plan_is_not_serial():
    init, acts = sussman_task(hand=False)
    (plan,) = plans_up_to(init, GOAL, acts, 3)
    # on(B, C) first holds after 2 moves, but its own shortest plan has 1 move.
    states = [init]
    for a in plan:
        states.append(run_plan(states[-1], [a]))
    first_bc = next(i for i, s in enumerate(states) if ON_B_C <= s)
    first_ab = next(i for i, s in enumerate(states) if ON_A_B <= s)
    assert (first_bc, first_ab) == (2, 3)
    assert shortest_length(init, ON_B_C, acts) == 1
