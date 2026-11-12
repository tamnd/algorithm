# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dimension-order-routing/. The authors are listed in prov/RHGNKB.jsonl.

from dimension_order_routing import (
    channel_number,
    dependency_graph,
    find_cycle,
    next_hop_mesh,
    next_hop_torus,
    nodes,
    route,
    union,
)


def yx_hop(cur, dst):
    """Y first, then X: the other dimension order on a 2-D mesh."""
    step = next_hop_mesh(cur[::-1], dst[::-1])
    return None if step is None else (1 - step[0], step[1])


def test_example_route() -> None:
    chans = route((0, 0), (3, 2), next_hop_mesh, 4)
    assert [(c[1], c[2]) for c in chans] == [(0, 1), (0, 1), (0, 1), (1, 1), (1, 1)]


def test_routes_are_shortest_on_meshes_and_hypercubes() -> None:
    for k, n in ((4, 2), (3, 3), (2, 4), (5, 2)):
        for s in nodes(k, n):
            for t in nodes(k, n):
                assert len(route(s, t, next_hop_mesh, k)) == sum(abs(a - b) for a, b in zip(s, t))


def test_mesh_and_hypercube_dependency_graphs_are_acyclic() -> None:
    for k, n in ((4, 2), (3, 3), (2, 4), (5, 2), (2, 6)):
        g = dependency_graph(k, n, next_hop_mesh)
        assert find_cycle(g) is None
        # The channel numbering increases along every dependency.
        assert all(channel_number(a, k) < channel_number(b, k) for a in g for b in g[a])


def test_mixing_xy_and_yx_creates_a_cycle() -> None:
    g = union(dependency_graph(3, 2, next_hop_mesh), dependency_graph(3, 2, yx_hop))
    assert find_cycle(g) is not None
    # The four turns around one unit square form a cycle of dependencies.
    square = [((0, 0), 0, 1, 0), ((1, 0), 1, 1, 0), ((1, 1), 0, -1, 0), ((0, 1), 1, -1, 0)]
    assert all(square[(i + 1) % 4] in g[square[i]] for i in range(4))


def test_torus_needs_virtual_channels() -> None:
    assert find_cycle(dependency_graph(3, 2, next_hop_torus(3), torus=True)) is None
    for k in (4, 5, 6):
        cycle = find_cycle(dependency_graph(k, 1, next_hop_torus(k), torus=True))
        assert cycle is not None and len(cycle) == k
        assert find_cycle(dependency_graph(k, 2, next_hop_torus(k), torus=True)) is not None
    for k in (4, 5, 6, 7):
        g = dependency_graph(k, 2, next_hop_torus(k), torus=True, dateline=True)
        assert find_cycle(g) is None


def test_torus_routes_are_minimal() -> None:
    k = 5
    for s in nodes(k, 2):
        for t in nodes(k, 2):
            dist = sum(min((a - b) % k, (b - a) % k) for a, b in zip(s, t))
            assert len(route(s, t, next_hop_torus(k), k, torus=True)) == dist
