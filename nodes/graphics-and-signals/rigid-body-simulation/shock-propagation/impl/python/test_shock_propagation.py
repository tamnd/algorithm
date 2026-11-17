# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shock-propagation/. The authors are listed in prov/P1VHW8.jsonl.

import random
from fractions import Fraction as F

from shock_propagation import (Box, contact_graph, find_contacts, levels, penetration, solve_velocities, stack, step,
                               strongly_connected_components)


def closure(n, edges):
    reach = [[i == j for j in range(n)] for i in range(n)]
    for u, v in edges:
        reach[u][v] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    return reach


def test_components_and_levels_match_brute_force():
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 8)
        edges = [(u, v) for u in range(n) for v in range(n) if u != v and rng.random() < 0.2]
        reach = closure(n, edges)
        comps, comp = strongly_connected_components(n, edges)
        for u in range(n):
            for v in range(n):
                assert (comp[u] == comp[v]) == (reach[u][v] and reach[v][u])
        # topological order of the condensation: every edge goes to the same or a later component
        assert all(comp[u] <= comp[v] for u, v in edges)
        level, _ = levels(n, edges)
        # brute force: the level is the largest number of components on a path into the node, minus one
        best = {}

        def longest(c):
            if c not in best:
                ps = {comp[u] for u, v in edges if comp[v] == c and comp[u] != c}
                best[c] = 1 + max(longest(p) for p in ps) if ps else 0
            return best[c]

        assert level == [longest(comp[u]) for u in range(n)]
        for u, v in edges:
            assert level[u] == level[v] if comp[u] == comp[v] else level[u] < level[v]


def test_dominoes_in_a_circle_share_one_level():
    n = 7  # node 0 is the ground, 1..6 are dominoes, each leaning on the next
    edges = [(0, i) for i in range(1, n)] + [(i, i % (n - 1) + 1) for i in range(1, n)]
    level, comp = levels(n, edges)
    assert level == [0] + [1] * (n - 1)
    assert len(set(comp[1:])) == 1


def test_pyramid_contact_graph_from_falling():
    boxes = [Box(0, -1, 10, 1), Box(F(-3, 5), F(1, 2), F(1, 2), F(1, 2), 1), Box(F(3, 5), F(1, 2), F(1, 2), F(1, 2), 1),
             Box(0, F(3, 2), F(1, 2), F(1, 2), 1)]
    edges = contact_graph(boxes, 10, F(1, 60))
    assert sorted(edges) == [(0, 1), (0, 2), (1, 3), (2, 3)]
    level, _ = levels(4, edges)
    assert level == [0, 1, 1, 2]
    assert sorted(find_contacts(boxes, 0)) == [(1, 0), (2, 0), (3, 1), (3, 2)]


def test_page_example_three_box_stack():
    boxes = stack(3, m=F(1), size=F(1, 2))
    for b in boxes[1:]:
        b.vy = F(-1)
    level, _ = levels(4, contact_graph(boxes, 10, F(1, 60)))
    assert level == [0, 1, 2, 3]
    contacts = find_contacts(boxes, 0)
    solve_velocities(boxes, contacts, level, 1, 1, shock=False)
    assert [b.vy for b in boxes[1:]] == [F(-1, 2), F(-3, 4), F(-3, 4)]
    solve_velocities(boxes, contacts, level, 0, 1, shock=True)
    assert [b.vy for b in boxes[1:]] == [0, 0, 0]
    # plain sweeps alone: count the sweeps until every box is slower than 1% of the start
    boxes = stack(3, m=F(1), size=F(1, 2))
    for b in boxes[1:]:
        b.vy = F(-1)
    sweeps = 0
    while max(-b.vy for b in boxes[1:]) > F(1, 100):
        solve_velocities(boxes, contacts, level, 1, 1, shock=False)
        sweeps += 1
    assert sweeps == 17


def skyline_scene(rng):
    """Boxes dropped one by one onto the ground and each other, so that each rests exactly on what is below it."""
    boxes = [Box(0, -1, 100, 1)]
    for _ in range(rng.randint(1, 9)):
        hx, hy = F(rng.randint(1, 4), 4), F(rng.randint(1, 3), 4)
        x = F(rng.randint(-8, 8), 4)
        probe = Box(x, 0, hx, hy, 1)
        top = max([0] + [b.y + b.hy for b in boxes[1:] if min(x + hx, b.x + b.hx) - max(x - hx, b.x - b.hx) > 0])
        probe.y = top + hy
        probe.inv_m = 1 / F(rng.randint(1, 20))
        probe.m = 1 / probe.inv_m
        probe.vy = F(rng.randint(-8, 4), 2)
        boxes.append(probe)
    return boxes


def test_after_the_shock_sweep_no_contact_approaches():
    rng = random.Random(3)
    for _ in range(150):
        boxes = skyline_scene(rng)
        edges = contact_graph(boxes, 10, F(1, 60))
        level, _ = levels(len(boxes), edges)
        contacts = find_contacts(boxes, 0)
        for a, b in contacts:
            assert level[a] > level[b]  # stacks of boxes give an acyclic graph
        solve_velocities(boxes, contacts, level, rng.randint(0, 2), rng.randint(1, 2), shock=True)
        for a, b in contacts:
            assert boxes[a].vy - boxes[b].vy >= 0


def test_shock_sweep_changes_nothing_when_no_contact_approaches():
    rng = random.Random(5)
    for _ in range(60):
        boxes = skyline_scene(rng)
        level, _ = levels(len(boxes), contact_graph(boxes, 10, F(1, 60)))
        contacts = find_contacts(boxes, 0)
        solve_velocities(boxes, contacts, level, 0, 1, shock=True)
        before = [b.vy for b in boxes]
        solve_velocities(boxes, contacts, level, 0, 1, shock=True)
        assert [b.vy for b in boxes] == before


def test_shock_propagation_changes_momentum():
    lower = Box(0, 0, F(1, 2), F(1, 2), F(1), vy=F(1))
    upper = Box(0, 1, F(1, 2), F(1, 2), F(3), vy=F(-1))
    boxes = [lower, upper]
    contacts = find_contacts(boxes, 0)
    assert contacts == [(1, 0)]
    p0 = lower.m * lower.vy + upper.m * upper.vy
    solve_velocities(boxes, contacts, [0, 1], 0, 1, shock=True)
    assert (lower.vy, upper.vy) == (1, 1)
    assert (p0, lower.m * lower.vy + upper.m * upper.vy) == (-2, 4)
    # a plastic collision without shock propagation keeps the momentum
    lower.vy, upper.vy = F(1), F(-1)
    solve_velocities(boxes, contacts, [0, 1], 1, 1, shock=False)
    assert (lower.vy, upper.vy) == (F(-1, 2), F(-1, 2))


def test_stack_sinks_without_shock_and_holds_with_it():
    results = {}
    for shock in (False, True):
        boxes = stack(10)
        for _ in range(120):
            _, contacts = step(boxes, 1 / 60, 9.81, 4, 1, shock)
        results[shock] = (penetration(boxes, contacts), boxes[-1].y)
    assert results[True][0] < 1e-12 and abs(results[True][1] - 9.5) < 1e-12
    assert results[False][0] > 0.3 and results[False][1] < 8  # measured: the top box sinks by more than 3 m
