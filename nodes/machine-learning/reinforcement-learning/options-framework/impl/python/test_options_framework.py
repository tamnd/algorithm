# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/options-framework/. The authors are listed in prov/QWHW45.jsonl.

import random

from options_framework import (FourRooms, hallway_option, hallway_options, primitive_option,
                               smdp_value_iteration)


def primitive_value_iteration(env, tol=1e-13):
    """Plain value iteration on the primitive MDP, written without options."""
    v = {s: 0.0 for s in env.states()}
    while True:
        new = {}
        for s in v:
            new[s] = max(sum(p * (r if d else r + env.gamma * v[s2])
                             for p, r, s2, d in env.outcomes(s, a)) for a in range(4))
        delta = max(abs(new[s] - v[s]) for s in v)
        v = new
        if delta < tol:
            return v


def test_layout():
    env = FourRooms()
    assert env.n == 40
    assert len(env.hallways) == 4
    assert len(hallway_options(env)) == 8


def test_primitives_and_hallway_options_match_primitive_value_iteration():
    env = FourRooms()
    vstar = primitive_value_iteration(env)
    prims = [primitive_option(env, a) for a in range(4)]
    v_a, _, _ = smdp_value_iteration(env, prims)
    v_ah, _, _ = smdp_value_iteration(env, prims + hallway_options(env))
    for s in vstar:
        assert abs(v_a[s] - vstar[s]) < 1e-9
        assert abs(v_ah[s] - vstar[s]) < 1e-9


def test_hallway_options_alone_are_no_better_and_sometimes_worse():
    env = FourRooms()
    vstar = primitive_value_iteration(env)
    v_h, _, _ = smdp_value_iteration(env, hallway_options(env))
    assert all(v_h[s] <= vstar[s] + 1e-9 for s in vstar)
    assert any(v_h[s] < vstar[s] - 1e-3 for s in vstar)


def test_options_spread_value_in_fewer_sweeps():
    env = FourRooms()
    prims = [primitive_option(env, a) for a in range(4)]
    _, _, h_prim = smdp_value_iteration(env, prims)
    _, _, h_opt = smdp_value_iteration(env, prims + hallway_options(env))
    total = len(env.states())
    first_prim = next(k for k, c in enumerate(h_prim) if c == total)
    first_opt = next(k for k, c in enumerate(h_opt) if c == total)
    assert first_opt < first_prim


def test_option_model_matches_simulation():
    env = FourRooms()
    room = env.rooms[0]
    model = hallway_option(env, room, (2, 4))
    s = env.index[(1, 1)]
    rew, dist = model[s]
    assert rew == 0.0  # the goal is not in this room
    assert 0.0 < sum(dist.values()) < env.gamma
    # Monte Carlo estimate of sum_x P_o(x | s), the expected gamma^duration
    rng = random.Random(5)
    inside = {env.index[c] for c in room}
    from options_framework import MOVES
    total, runs = 0.0, 20000
    for _ in range(runs):
        cur, disc = s, 1.0
        while True:
            r, c = env.cells[cur]
            # follow the option's own policy: recompute it from the model's BFS order
            a = policy_toward(env, room, (2, 4), cur, MOVES)
            u = rng.random()
            acc = 0.0
            for p, _, s2, _ in env.outcomes(cur, a):
                acc += p
                if u < acc:
                    break
            disc *= env.gamma
            cur = s2
            if cur not in inside:
                break
        total += disc
    assert abs(total / runs - sum(dist.values())) < 0.01


def policy_toward(env, room, target, s, moves):
    dist = {target: 0}
    frontier = [target]
    while frontier:
        nxt = []
        for r, c in frontier:
            for dr, dc in moves:
                cell = (r + dr, c + dc)
                if cell in room and cell not in dist:
                    dist[cell] = dist[(r, c)] + 1
                    nxt.append(cell)
        frontier = nxt
    r, c = env.cells[s]
    return min(range(4), key=lambda a: (dist.get((r + moves[a][0], c + moves[a][1]), 99), a))
