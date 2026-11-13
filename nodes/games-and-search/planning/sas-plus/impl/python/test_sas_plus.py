# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sas-plus/. The authors are listed in prov/8Z7BSB.jsonl.

import random

from sas_plus import (
    NONE,
    bfs_plan,
    blocks_world_actions,
    blocks_world_facts,
    blocks_world_groups,
    blocks_world_state,
    encode,
    is_exactly_one_group,
    is_mutex_group,
    reachable,
    sas_plan_length,
    sas_reachable,
    sas_successors,
    successor,
    translate,
)


def setup(n):
    blocks = "abcde"[:n]
    acts = blocks_world_actions(blocks)
    init = blocks_world_state([list(blocks)])
    return blocks, acts, init


def test_groups_are_invariants():
    for n in (2, 3, 4):
        blocks, acts, init = setup(n)
        states = reachable(init, acts)
        for g in blocks_world_groups(blocks):
            assert is_mutex_group(g, init, acts)
            assert is_exactly_one_group(g, init, acts)
            assert all(len(g & s) == 1 for s in states)
    blocks, acts, init = setup(3)
    bad = frozenset({("clear", "a"), ("clear", "b")})
    assert not is_mutex_group(bad, init, acts)
    assert any(len(bad & s) == 2 for s in reachable(init, acts))


def test_variables_of_blocks_world():
    for n in (2, 3, 4):
        blocks, acts, init = setup(n)
        task, var_of = translate(blocks_world_facts(blocks), init, acts, blocks_world_groups(blocks))
        sizes = sorted(len(v) for v in task.variables)
        # n position variables with n + 1 values, n clear variables and one hand variable, all binary.
        assert sizes == [2] * (n + 1) + [n + 1] * n
        assert len(blocks_world_facts(blocks)) == (n + 1) ** 2
        product = 1
        for k in sizes:
            product *= k
        assert product == (n + 1) ** n * 2 ** (n + 1)


def test_state_spaces_are_isomorphic():
    for n in (2, 3, 4):
        blocks, acts, init = setup(n)
        task, var_of = translate(blocks_world_facts(blocks), init, acts, blocks_world_groups(blocks))
        strips_states = reachable(init, acts)
        sas_states = sas_reachable(task)
        assert len(strips_states) == len(sas_states)
        phi = {s: encode(s, task.variables, var_of) for s in strips_states}
        assert len(set(phi.values())) == len(phi)  # injective
        assert set(phi.values()) == set(sas_states)  # onto the reachable SAS+ states
        by_name = {a.name: a for a in acts}
        for s in strips_states:
            assert sas_states[phi[s]] == strips_states[s]
            strips_edges = {(a.name, phi[successor(s, a)]) for a in acts if a.pre <= s}
            assert strips_edges == set(sas_successors(task, phi[s]))
        assert set(by_name) >= {name for name, _, _ in task.actions}


def test_same_plan_lengths():
    rng = random.Random(17)
    blocks, acts, init = setup(4)
    task, var_of = translate(blocks_world_facts(blocks), init, acts, blocks_world_groups(blocks))
    states = list(reachable(init, acts))
    states.sort(key=repr)
    for _ in range(25):
        target = rng.choice(states)
        goal = frozenset(rng.sample(sorted(target, key=repr), 2))
        sas_goal = {var_of[f]: f for f in goal}
        assert sas_plan_length(task, sas_goal) == len(bfs_plan(init, goal, acts))


def test_none_value_for_partial_groups():
    blocks, acts, init = setup(3)
    task, var_of = translate(blocks_world_facts(blocks), init, acts, blocks_world_groups(blocks))
    clear_a = task.variables[var_of[("clear", "a")]]
    assert clear_a == (("clear", "a"), NONE)
    pos_a = task.variables[var_of[("ontable", "a")]]
    assert NONE not in pos_a and len(pos_a) == 4
