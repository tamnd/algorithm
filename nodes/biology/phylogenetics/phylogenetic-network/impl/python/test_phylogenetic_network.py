# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phylogenetic-network/. The authors are listed in prov/PV464M.jsonl.

import random

import pytest

from phylogenetic_network import CycleError, PhylogeneticNetwork


def build(arcs, labels):
    net = PhylogeneticNetwork()
    verts = sorted({u for a in arcs for u in a} | set(labels))
    for v in verts:
        net.add_vertex(v, labels.get(v))
    for u, v in arcs:
        net.add_arc(u, v)
    return net


def tree(*clusters):
    return frozenset(frozenset(c) for c in clusters)


# The page example: root 0, tree vertices u = 1 and v = 2, reticulation r = 3.
EXAMPLE_ARCS = [(0, 1), (0, 2), (1, 4), (1, 3), (2, 3), (2, 6), (3, 5)]
EXAMPLE_LABELS = {4: "a", 5: "b", 6: "c"}


def test_example_from_page():
    net = build(EXAMPLE_ARCS, EXAMPLE_LABELS)
    assert net.is_valid()
    assert net.reticulation_number() == 1
    assert net.arc_count() - len(net.children) + 1 == 1
    assert net.is_tree_child()
    t1 = tree("a", "b", "c", "ab", "abc")
    t2 = tree("a", "b", "c", "bc", "abc")
    assert net.displayed_trees() == {t1, t2}
    with pytest.raises(CycleError):
        net.add_arc(3, 1)
    assert net.arc_count() == 7


def test_example_second_reticulation_breaks_tree_child():
    # Add a vertex w on top of c and an arc u -> w: now v has the children r and w, both reticulations.
    arcs = [(0, 1), (0, 2), (1, 4), (1, 3), (2, 3), (2, 7), (7, 6), (1, 7), (3, 5)]
    net = build(arcs, EXAMPLE_LABELS)
    assert net.reticulation_number() == 2
    assert not net.is_tree_child()
    # u has the child a (a leaf), so u is fine; v fails.
    # Four switchings give four trees: ab, bc, ac, and the star when u keeps both reticulations.
    assert net.displayed_trees() == {
        tree("a", "b", "c", "ab", "abc"),
        tree("a", "b", "c", "bc", "abc"),
        tree("a", "b", "c", "ac", "abc"),
        tree("a", "b", "c", "abc"),
    }


def test_triangle_gives_one_tree_twice():
    # Root 0 with children 1 and 2; 1 is a parent of the reticulation 2.
    arcs = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4)]
    net = build(arcs, {3: "a", 4: "b"})
    assert net.reticulation_number() == 1
    assert len(net.displayed_trees()) == 1


def test_validity_rules():
    net = build([(0, 1), (0, 2)], {1: "a", 2: "b"})
    assert net.is_valid()
    net = build([(0, 1), (0, 2), (1, 3)], {2: "a", 3: "b"})
    assert not net.is_valid()  # vertex 1 has one parent and one child
    net = build([(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5), (1, 6), (2, 7)], {4: "a", 5: "b", 6: "c", 7: "d"})
    assert not net.is_valid()  # the reticulation 3 has two children
    net = build([(0, 1), (2, 1)], {1: "a"})
    assert not net.is_valid()  # two roots
    with pytest.raises(ValueError):
        build([], {0: "a", 1: "a"})
    n = build([(0, 1)], {1: "a"})
    with pytest.raises(ValueError):
        n.add_arc(0, 1)
    with pytest.raises(CycleError):
        n.add_arc(1, 1)


def random_network(k, h, rng):
    """A random valid binary network: a random tree on k leaves, then h reticulation arcs."""
    arcs = [(0, 1), (0, 2)]
    leaves = [1, 2]
    nxt = 3
    while len(leaves) < k:
        x = leaves.pop(rng.randrange(len(leaves)))
        arcs += [(x, nxt), (x, nxt + 1)]
        leaves += [nxt, nxt + 1]
        nxt += 2
    for _ in range(h):
        for _attempt in range(30):
            i, j = rng.randrange(len(arcs)), rng.randrange(len(arcs))
            if i == j:
                continue
            (a, b), (c, d) = arcs[i], arcs[j]
            if _reaches(arcs, d, a):
                continue
            x, y = nxt, nxt + 1
            nxt += 2
            arcs = [e for t, e in enumerate(arcs) if t not in (i, j)]
            arcs += [(a, x), (x, b), (c, y), (y, d), (x, y)]
            break
    labels = {v: "t%d" % t for t, v in enumerate(sorted(leaves))}
    return arcs, labels


def _reaches(arcs, u, v):
    seen, stack = {u}, [u]
    while stack:
        x = stack.pop()
        if x == v:
            return True
        for a, b in arcs:
            if a == x and b not in seen:
                seen.add(b)
                stack.append(b)
    return False


def brute_displayed(arcs, labels, root):
    """Every subset of arcs in which each vertex has at most one parent and every leaf is reached."""
    out = set()
    m = len(arcs)
    leaves = set(labels)
    for mask in range(1 << m):
        sub = [arcs[t] for t in range(m) if mask >> t & 1]
        indeg = {}
        for _, v in sub:
            indeg[v] = indeg.get(v, 0) + 1
        if any(c > 1 for c in indeg.values()):
            continue
        reach = {root}
        changed = True
        while changed:
            changed = False
            for u, v in sub:
                if u in reach and v not in reach:
                    reach.add(v)
                    changed = True
        if not leaves <= reach:
            continue
        clusters = set()
        for v in reach:
            below = {v}
            changed = True
            while changed:
                changed = False
                for a, b in sub:
                    if a in below and b not in below:
                        below.add(b)
                        changed = True
            c = frozenset(labels[x] for x in below if x in labels)
            if c:
                clusters.add(c)
        out.add(frozenset(clusters))
    return out


def tree_path_child(net):
    """Brute force: every vertex has a path to a sink whose later vertices are not reticulations."""
    for v in net.children:
        ok = False
        stack, seen = [v], {v}
        while stack:
            x = stack.pop()
            if not net.children[x]:
                ok = True
                break
            for y in net.children[x]:
                if len(net.parents[y]) < 2 and y not in seen:
                    seen.add(y)
                    stack.append(y)
        if not ok:
            return False
    return True


@pytest.mark.parametrize("seed", range(4))
def test_displayed_trees_against_arc_subsets(seed):
    rng = random.Random(seed)
    for _ in range(12):
        k = rng.randint(2, 4)
        h = rng.randint(0, 2)
        arcs, labels = random_network(k, h, rng)
        if len(arcs) > 13:
            continue
        net = build(arcs, labels)
        assert net.is_valid()
        got = net.displayed_trees()
        assert got == brute_displayed(arcs, labels, 0)
        assert len(got) <= 2 ** net.reticulation_number()
        full = frozenset(labels.values())
        for t in got:
            assert full in t
            assert all(frozenset([x]) in t for x in full)
            for c1 in t:
                for c2 in t:
                    assert c1 <= c2 or c2 <= c1 or not (c1 & c2)


@pytest.mark.parametrize("seed", range(4))
def test_random_operations_against_model(seed):
    rng = random.Random(100 + seed)
    net = PhylogeneticNetwork()
    verts = []
    arcs = set()
    for _ in range(300):
        op = rng.random()
        if op < 0.25 or len(verts) < 2:
            v = len(verts)
            net.add_vertex(v)
            verts.append(v)
        else:
            u, v = rng.choice(verts), rng.choice(verts)
            cycle = u == v or _reaches(sorted(arcs), v, u)
            parallel = (u, v) in arcs
            if parallel:
                with pytest.raises(ValueError):
                    net.add_arc(u, v)
            elif cycle:
                with pytest.raises(CycleError):
                    net.add_arc(u, v)
            else:
                net.add_arc(u, v)
                arcs.add((u, v))
        assert net.arc_count() == len(arcs)
        roots = sum(1 for v in verts if not any(b == v for _, b in arcs))
        assert net.reticulation_number() == len(arcs) - len(verts) + roots
        assert sorted(net.roots()) == sorted(v for v in verts if not any(b == v for _, b in arcs))
        assert net.is_tree_child() == tree_path_child(net)


@pytest.mark.parametrize("seed", range(3))
def test_tree_child_networks_have_few_reticulations(seed):
    rng = random.Random(200 + seed)
    for _ in range(150):
        k = rng.randint(2, 6)
        arcs, labels = random_network(k, rng.randint(0, 8), rng)
        net = build(arcs, labels)
        assert net.is_valid()
        assert net.is_tree_child() == tree_path_child(net)
        if net.is_tree_child():
            assert net.reticulation_number() <= k - 1
