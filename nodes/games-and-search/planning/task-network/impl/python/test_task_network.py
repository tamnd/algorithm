# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/task-network/. The authors are listed in prov/DKGG4M.jsonl.

import random
from itertools import permutations

from task_network import TaskNetwork


def brute_linearizations(net):
    out = set()
    for perm in permutations(sorted(net.nodes)):
        pos = {n: i for i, n in enumerate(perm)}
        if all(pos[u] < pos[v] for u, v in net.order):
            out.add(perm)
    return out


def random_network(rng, size, density, acyclic=False):
    nodes = {i: rng.choice("abc") for i in range(size)}
    order = set()
    for u in range(size):
        for v in range(size):
            if u != v and rng.random() < density and (not acyclic or u < v):
                order.add((u, v))
    return TaskNetwork(nodes, order)


def test_consistency_is_acyclicity():
    rng = random.Random(61)
    seen = {True: 0, False: 0}
    for _ in range(400):
        net = random_network(rng, rng.randint(1, 6), rng.choice([0.1, 0.2, 0.3]))
        expected = bool(brute_linearizations(net))
        assert net.is_consistent() == expected
        seen[expected] += 1
    assert seen[True] > 50 and seen[False] > 50


def test_linearizations_equal_brute_force():
    rng = random.Random(62)
    for _ in range(300):
        net = random_network(rng, rng.randint(0, 6), rng.choice([0.0, 0.2, 0.5]))
        lins = list(net.linearizations())
        assert len(lins) == len(set(lins))
        assert set(lins) == brute_linearizations(net)


def test_decomposition_inherits_orderings():
    rng = random.Random(63)
    for _ in range(300):
        net = random_network(rng, rng.randint(1, 5), 0.3, acyclic=True)
        sub = random_network(rng, rng.randint(0, 3), 0.4, acyclic=True)
        n = rng.choice(sorted(net.nodes))
        result, rename = net.decompose(n, sub)
        new = set(rename.values())
        lins = set(result.linearizations())
        assert lins == brute_linearizations(result)
        for lin in lins:
            # Every predecessor of n is before all new nodes, every successor after them.
            pos = {x: i for i, x in enumerate(lin)}
            for x in new:
                assert all(pos[u] < pos[x] for u in net.predecessors(n))
                assert all(pos[x] < pos[v] for v in net.successors(n))
            # Collapsing the new nodes to the place of the first one gives a linearization of net.
            if new:
                first = min(pos[x] for x in new)
                collapsed = tuple(x for i, x in enumerate(lin) if x not in new or i == first)
                collapsed = tuple(n if x in new else x for x in collapsed)
                assert collapsed in brute_linearizations(net)
        # Conversely, splicing a linearization of sub into a linearization of net gives one of the result.
        inverse = {v: k for k, v in rename.items()}
        for lin in brute_linearizations(net):
            for sublin in brute_linearizations(sub):
                i = lin.index(n)
                spliced = lin[:i] + tuple(rename[m] for m in sublin) + lin[i + 1:]
                assert spliced in lins
        assert all(inverse[x] in sub.nodes for x in new)


def test_empty_decomposition_keeps_transitive_order():
    net = TaskNetwork.of(["a", "b", "c"])
    result, _ = net.decompose(1, TaskNetwork({}))
    assert result.task_sequences() == {("a", "c")}
    unordered = TaskNetwork({0: "a", 1: "b", 2: "c"}, [(0, 1), (1, 2)])
    result, _ = unordered.decompose(1, TaskNetwork({}))
    assert (0, 2) in result.order


def test_total_order_splices():
    net = TaskNetwork.of(["get", "travel", "pay"])
    result, _ = net.decompose(1, TaskNetwork.of(["call", "ride"]))
    assert result.task_sequences() == {("get", "call", "ride", "pay")}
    result, _ = net.decompose(1, TaskNetwork({0: "call", 1: "ride"}))
    assert result.task_sequences() == {("get", "call", "ride", "pay"), ("get", "ride", "call", "pay")}


def test_bad_ordering_is_rejected():
    try:
        TaskNetwork({0: "a"}, [(0, 1)])
        assert False
    except ValueError:
        pass
    assert not TaskNetwork({0: "a", 1: "b"}, [(0, 1), (1, 0)]).is_consistent()
    assert TaskNetwork({0: "a"}).is_primitive({"a"})
