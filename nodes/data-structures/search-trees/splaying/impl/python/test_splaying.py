# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/splaying/. The authors are listed in prov/AA2JCV.jsonl.

import math
import random

from splaying import Node, check_tree, depth, find, inorder, insert, splay


def build(keys):
    root = None
    for k in keys:
        root, _ = insert(root, k)
    return root


def shape(x):
    """Nested tuples (key, left, right), built with a stack."""
    if x is None:
        return None
    out = {}
    stack = [(x, False)]
    while stack:
        n, done = stack.pop()
        if done:
            out[id(n)] = (n.key, out.get(id(n.left)) if n.left else None, out.get(id(n.right)) if n.right else None)
        else:
            stack.append((n, True))
            for c in (n.left, n.right):
                if c is not None:
                    stack.append((c, False))
    return out[id(x)]


# An independent reference: splaying on immutable tuples, by the three cases.
def ref_splay(t, k):
    path = []  # list of (tree, direction) from the root down to the node of k
    cur = t
    while cur[0] != k:
        d = 0 if k < cur[0] else 1
        path.append((cur, d))
        cur = cur[1] if d == 0 else cur[2]

    def rot_up(parent, d, child):
        """Child is parent's d-child; return the rotated subtree with child on top."""
        if d == 0:
            return (child[0], child[1], (parent[0], child[2], parent[2]))
        return (child[0], (parent[0], parent[1], child[1]), child[2])

    def replace(parent, d, child):
        return (parent[0], child, parent[2]) if d == 0 else (parent[0], parent[1], child)

    x = cur
    while path:
        if len(path) == 1:
            (p, dp) = path.pop()
            x = rot_up(p, dp, x)
        else:
            (p, dp) = path.pop()
            (g, dg) = path.pop()
            if dp == dg:  # zig-zig: rotate p over g, then x over p
                p2 = replace(p, dp, x)
                top = rot_up(g, dg, p2)
                x = rot_up(top, dg, top[1] if dg == 0 else top[2])
            else:  # zig-zag: rotate x over p, then over g
                x1 = rot_up(p, dp, x)
                x = rot_up(g, dg, x1)
    return x


def test_chain_example() -> None:
    root = build([7, 6, 5, 4, 3, 2, 1])
    x = find(root, 1)
    assert depth(x) == 6
    root, rot = splay(x)
    assert rot == 6 and root.key == 1
    check_tree(root)
    assert list(inorder(root)) == [1, 2, 3, 4, 5, 6, 7]
    assert shape(root) == (1, None, (6, (4, (2, None, (3, None, None)), (5, None, None)), (7, None, None)))


def test_zig_zag_example() -> None:
    root = build([50, 30, 70, 20, 40, 35, 45])
    root, rot = splay(find(root, 40))
    assert rot == 2
    assert shape(root) == (40, (30, (20, None, None), (35, None, None)), (50, (45, None, None), (70, None, None)))


def test_random_against_reference() -> None:
    rng = random.Random(9001)
    for _ in range(600):
        n = rng.randint(1, 40)
        keys = rng.sample(range(1000), n)
        root = build(keys)
        k = rng.choice(keys)
        before = shape(root)
        x = find(root, k)
        d = depth(x)
        root, rot = splay(x)
        check_tree(root)
        assert root is x and rot == d
        assert list(inorder(root)) == sorted(keys)
        assert shape(root) == ref_splay(before, k)


def _rank_sum(root):
    total = 0.0
    sizes = {}
    stack = [(root, False)]
    while stack:
        n, done = stack.pop()
        if done:
            s = 1 + sizes.get(id(n.left), 0) + sizes.get(id(n.right), 0)
            sizes[id(n)] = s
            total += math.log2(s)
        else:
            stack.append((n, True))
            for c in (n.left, n.right):
                if c is not None:
                    stack.append((c, False))
    return total, sizes


def test_access_lemma_unit_weights() -> None:
    rng = random.Random(31337)
    for _ in range(500):
        n = rng.randint(1, 60)
        keys = list(range(n))
        if rng.random() < 0.3:
            keys.sort()
        else:
            rng.shuffle(keys)
        root = build(keys)
        x = find(root, rng.randrange(n))
        phi0, sizes = _rank_sum(root)
        bound = 3 * (math.log2(n) - math.log2(sizes[id(x)])) + 1
        root, rot = splay(x)
        phi1, _ = _rank_sum(root)
        assert max(rot, 1) + phi1 - phi0 <= bound + 1e-9
