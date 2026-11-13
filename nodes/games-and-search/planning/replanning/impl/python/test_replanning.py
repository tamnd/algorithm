# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/replanning/. The authors are listed in prov/S4BFGJ.jsonl.

import random
from fractions import Fraction as F
from itertools import product

from replanning import (Replanner, all_outcomes, bfs_plan, is_plan, most_likely, repair, run,
                        stability_distance)


# ---- exact references ----

def solve(rows, rhs):
    """Gaussian elimination over fractions."""
    n = len(rows)
    m = [list(r) + [b] for r, b in zip(rows, rhs)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def absorb(trans, goal_nodes, start, cost=False):
    """Probability of reaching a goal node (or the expected number of steps) in a finite Markov chain.

    trans maps a node to a list of (p, node); nodes with no entry are absorbing."""
    nodes, stack = {start}, [start]
    while stack:
        u = stack.pop()
        for _, v in trans.get(u, []):
            if v not in nodes:
                nodes.add(v)
                stack.append(v)
    good = set(goal_nodes) & nodes
    changed = True
    while changed:
        changed = False
        for u in nodes:
            if u not in good and any(v in good for p, v in trans.get(u, []) if p > 0):
                good.add(u)
                changed = True
    if start in goal_nodes:
        return F(0) if cost else F(1)
    if start not in good:
        return None if cost else F(0)
    var = sorted((u for u in good if u not in goal_nodes), key=repr)
    idx = {u: i for i, u in enumerate(var)}
    rows, rhs = [], []
    for u in var:
        row = [F(0)] * len(var)
        row[idx[u]] += 1
        b = F(1) if cost else F(0)
        for p, v in trans[u]:
            if v in idx:
                row[idx[v]] -= p
            elif v in goal_nodes and not cost:
                b += p
        rows.append(row)
        rhs.append(b)
    return solve(rows, rhs)[idx[start]]


def replanner_chain(dom, det, s0, goal):
    """The Markov chain of (state, memory of the replanner)."""
    trans, start = {}, (s0, (None, ()))
    stack, seen = [start], {start}
    while stack:
        node = stack.pop()
        s, (exp, rest) = node
        if s in goal or s == "stuck":
            continue
        agent = Replanner(det, goal)
        agent.expected, agent.rest = exp, list(rest)
        a = agent.act(s)
        if a is None:
            nxt = [(F(1), ("stuck", (None, ())))]
        else:
            nxt = [(p, (t, agent.memory())) for p, t in dom[s][a]]
        trans[node] = nxt
        for _, v in nxt:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    goal_nodes = {n for n in seen if n[0] in goal}
    return trans, goal_nodes, start


def replanner_success(dom, det, s0, goal):
    return absorb(*replanner_chain(dom, det, s0, goal))


def best_success(dom, s0, goal):
    """Max probability of reaching the goal, over all deterministic memoryless policies."""
    states = [s for s in dom if s not in goal and dom[s]]
    best = F(0)
    for pick in product(*[sorted(dom[s], key=repr) for s in states]):
        pol = dict(zip(states, pick))
        trans = {s: dom[s][a] for s, a in pol.items()}
        best = max(best, absorb(trans, goal, s0))
    return best


# ---- examples of the page ----

def risky():
    return {
        "start": {"risky": [(F(3, 5), "goal"), (F(2, 5), "dead")], "safe": [(F(1), "a")]},
        "a": {"safe": [(F(1), "goal")]},
        "dead": {},
        "goal": {},
    }


def test_replanning_takes_the_risky_shortcut():
    dom = risky()
    assert replanner_success(dom, all_outcomes(dom), "start", {"goal"}) == F(3, 5)
    assert replanner_success(dom, most_likely(dom), "start", {"goal"}) == F(3, 5)
    assert best_success(dom, "start", {"goal"}) == 1


def slippery(n, p):
    dom = {i: {"right": [(p, i + 1), (1 - p, i)]} for i in range(n)}
    dom[n] = {}
    return dom


def test_slippery_corridor_is_solved_optimally():
    n, p = 4, F(1, 2)
    dom = slippery(n, p)
    trans, goal_nodes, start = replanner_chain(dom, all_outcomes(dom), 0, {n})
    assert absorb(trans, goal_nodes, start) == 1
    assert absorb(trans, goal_nodes, start, cost=True) == n / p == 8


def test_most_likely_outcome_can_hide_the_goal():
    dom = {"s": {"try": [(F(1, 10), "goal"), (F(9, 10), "s")]}, "goal": {}}
    assert bfs_plan(most_likely(dom), "s", {"goal"}) is None
    assert replanner_success(dom, most_likely(dom), "s", {"goal"}) == 0
    trans, goal_nodes, start = replanner_chain(dom, all_outcomes(dom), "s", {"goal"})
    assert absorb(trans, goal_nodes, start) == 1
    assert absorb(trans, goal_nodes, start, cost=True) == 10
    reached, steps, calls = run(dom, all_outcomes(dom), "s", {"goal"}, random.Random(20))
    assert reached and calls == steps


def random_domain(rng, n, k):
    dom = {}
    for s in range(n):
        dom[s] = {}
        for a in range(k):
            outs = sorted({rng.randrange(n + 1) for _ in range(rng.randint(1, 3))})
            w = [rng.randint(1, 4) for _ in outs]
            dom[s][a] = [(F(x, sum(w)), t) for x, t in zip(w, outs)]
    dom[n] = {}
    return dom


def test_replanning_against_the_best_policy():
    rng = random.Random(21)
    full = 0
    for _ in range(150):
        n = rng.randint(1, 4)
        dom = random_domain(rng, n, rng.randint(1, 2))
        det = all_outcomes(dom)
        got = replanner_success(dom, det, 0, {n})
        best = best_success(dom, 0, {n})
        assert got <= best
        # with no dead end in the determinization, replanning reaches the goal with probability 1
        if all(bfs_plan(det, s, {n}) is not None for s in dom):
            full += 1
            assert got == best == 1
    assert full > 30


# ---- plan repair ----

def grid(w, h, walls):
    det = {}
    for x, y in product(range(w), range(h)):
        if (x, y) in walls:
            continue
        det[x, y] = {}
        for a, (dx, dy) in (("E", (1, 0)), ("N", (0, 1)), ("W", (-1, 0)), ("S", (0, -1))):
            t = (x + dx, y + dy)
            if 0 <= t[0] < w and 0 <= t[1] < h and t not in walls:
                det[x, y][a, (x, y)] = t  # a ground action: a move from a given cell
    return det


def test_repair_keeps_the_rest_of_the_plan():
    det = grid(5, 5, {(2, 1), (2, 2), (2, 3)})
    goal = {(4, 4)}
    old = bfs_plan(det, (0, 0), goal)
    assert [a[0] for a, _ in old] == ["E", "E", "E", "E", "N", "N", "N", "N"]
    # after two steps the agent is pushed from (2, 0) to (1, 1)
    fixed = repair(det, old, (0, 0), (1, 1), goal)
    scratch = bfs_plan(det, (1, 1), goal)
    assert is_plan(det, (1, 1), fixed, goal) and is_plan(det, (1, 1), scratch, goal)
    assert [a[0] for a, _ in fixed] == ["S", "E", "E", "E", "N", "N", "N", "N"]
    assert [a[0] for a, _ in scratch] == ["N", "N", "N", "E", "E", "E"]
    rest = old[2:]
    assert stability_distance(rest, fixed) == 2
    assert stability_distance(rest, scratch) == 12


def test_repair_is_valid_on_random_grids():
    rng = random.Random(22)
    for _ in range(200):
        walls = {(rng.randrange(5), rng.randrange(5)) for _ in range(6)} - {(0, 0), (4, 4)}
        det = grid(5, 5, walls)
        goal = {(4, 4)}
        old = bfs_plan(det, (0, 0), goal)
        if old is None:
            continue
        s = rng.choice(sorted(det))
        fixed = repair(det, old, (0, 0), s, goal)
        best = bfs_plan(det, s, goal)
        assert (fixed is None) == (best is None)
        if fixed is not None:
            assert is_plan(det, s, fixed, goal)
            assert len(fixed) >= len(best)
