# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gyo-reduction/. The authors are listed in prov/AMABKP.jsonl.

import itertools
import random

from gyo_reduction import gyo_reduction, is_alpha_acyclic, is_join_tree, join_tree


def all_trees(m):
    """Yield the edge lists of all labeled trees on the nodes 0 .. m - 1 (Pruefer codes)."""
    if m == 1:
        yield []
        return
    if m == 2:
        yield [(0, 1)]
        return
    for code in itertools.product(range(m), repeat=m - 2):
        degree = [1] * m
        for x in code:
            degree[x] += 1
        tree = []
        for x in code:
            leaf = min(i for i in range(m) if degree[i] == 1)
            tree.append((leaf, x))
            degree[leaf] -= 1
            degree[x] -= 1
        u, w = [i for i in range(m) if degree[i] == 1]
        tree.append((u, w))
        yield tree


def brute_force_acyclic(edges):
    """The definition: some tree on the edges has the running intersection property."""
    if not edges:
        return True
    return any(is_join_tree(edges, t) for t in all_trees(len(edges)))


def random_hypergraph(rng, m, domain):
    return [frozenset(rng.sample(domain, rng.randint(0, min(3, len(domain))))) for _ in range(m)]


def test_page_example():
    edges = [set("ABC"), set("BCD"), set("CDE"), set("DF"), set("AB")]
    acyclic, parent, steps = gyo_reduction(edges)
    assert acyclic
    assert steps == [
        ("vertex", "E", 2),
        ("vertex", "F", 3),
        ("edge", 2, 1),
        ("edge", 3, 1),
        ("vertex", "D", 1),
        ("edge", 1, 0),
        ("vertex", "C", 0),
        ("edge", 0, 4),
        ("vertex", "A", 4),
        ("vertex", "B", 4),
    ]
    assert parent == {2: 1, 3: 1, 1: 0, 0: 4}
    # A cyclic case: the triangle stays after the pendant edge CD goes.
    acyclic, parent, steps = gyo_reduction([set("AB"), set("BC"), set("CA"), set("CD")])
    assert not acyclic
    assert steps == [("vertex", "D", 3), ("edge", 3, 1)]
    assert is_join_tree(edges, join_tree(edges))


def test_hand_cases():
    assert is_alpha_acyclic([])
    assert is_alpha_acyclic([set()])
    assert is_alpha_acyclic([set("AB")])
    assert is_alpha_acyclic([set("AB"), set("AB")])
    assert is_alpha_acyclic([set("AB"), set("CD")])
    assert is_alpha_acyclic([set("AB"), set("BC"), set("CD")])
    assert not is_alpha_acyclic([set("AB"), set("BC"), set("CA")])
    # Adding the edge ABC makes the triangle alpha-acyclic.
    assert is_alpha_acyclic([set("AB"), set("BC"), set("CA"), set("ABC")])
    assert not is_alpha_acyclic([set("AB"), set("BC"), set("CD"), set("DA")])
    # The 4-cycle with a chord edge ABC is still cyclic: ACD remains a cycle part.
    assert not is_alpha_acyclic([set("AB"), set("BC"), set("CD"), set("DA"), set("ABC")])
    assert is_alpha_acyclic([set("AB"), set("BC"), set("CD"), set("DA"), set("ABC"), set("ACD")])
    # Three edges of size 2 out of a 3-set, plus a vertex outside.
    assert not is_alpha_acyclic([set("ABE"), set("BCE"), set("CAE")])


def test_against_brute_force():
    rng = random.Random(20261118)
    for trial in range(400):
        m = rng.randint(1, 5) if trial % 8 else 6
        domain = list("ABCDEF"[: rng.randint(3, 6)])
        edges = random_hypergraph(rng, m, domain)
        expected = brute_force_acyclic(edges)
        assert is_alpha_acyclic(edges) == expected, edges
        tree = join_tree(edges)
        if expected:
            assert is_join_tree(edges, tree), (edges, tree)
        else:
            assert tree is None


def test_order_does_not_matter():
    rng = random.Random(7)
    for _ in range(150):
        m = rng.randint(1, 6)
        domain = list("ABCDE")
        edges = random_hypergraph(rng, m, domain)
        first = is_alpha_acyclic(edges)
        for _ in range(4):
            acyclic, parent, _ = gyo_reduction(edges, rng=rng)
            assert acyclic == first
            if acyclic:
                assert is_join_tree(edges, sorted(parent.items()))


def test_cycles_are_cyclic():
    for n in range(3, 8):
        names = [f"v{i}" for i in range(n)]
        cycle = [{names[i], names[(i + 1) % n]} for i in range(n)]
        assert not is_alpha_acyclic(cycle)
        path = cycle[:-1]
        assert is_alpha_acyclic(path)
        assert is_alpha_acyclic(cycle + [set(names)])


def test_number_of_steps():
    # Each step deletes one vertex occurrence or one edge, so the number of steps is at most
    # the total size of the edges plus the number of edges.
    rng = random.Random(3)
    for _ in range(100):
        edges = random_hypergraph(rng, rng.randint(1, 6), list("ABCDE"))
        _, _, steps = gyo_reduction(edges)
        assert len(steps) <= sum(len(e) for e in edges) + len(edges)
