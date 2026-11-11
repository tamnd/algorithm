# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-based-group-diffie-hellman/. The authors are listed in prov/B6HWGP.jsonl.
#
# TGDH has no official test vectors. These tests check agreement after joins
# and leaves, the O(log n) cost, and forward and backward secrecy.

import random

from tree_based_group_diffie_hellman import G, P, Member, Tree, all_keys, f


def seeded(seed: int):
    r = random.Random(seed)
    return lambda n: r.randrange(n)


def build(n: int, rng):
    members = [Member("m%d" % i, rng) for i in range(n)]
    tree = Tree(members[0])
    for m in members[1:]:
        tree.join(m)
    return tree, members


def test_agreement_after_joins():
    tree, members = build(6, seeded(1))
    keys = all_keys(tree)
    assert len(keys) == 6 and len(set(keys.values())) == 1
    assert tree.height() == 3


def test_join_cost_is_logarithmic():
    tree, members = build(8, seeded(2))
    assert tree.height() == 3
    new = Member("new", seeded(3))
    sponsor = tree.join(new)
    before = sponsor.exps
    assert tree.height() == 4
    keys = all_keys(tree)
    assert len(set(keys.values())) == 1
    # The sponsor did 1 + 2h exponentiations in its refresh, h = depth of its leaf.
    depth, node = 0, sponsor.leaf
    while node.parent is not None:
        depth, node = depth + 1, node.parent
    assert sponsor.exps - before == depth            # recomputing the path: one per level
    assert all(m.exps <= 1 + 2 * 4 + 4 * 4 for m in tree.leaves())


def test_backward_secrecy_on_join():
    tree, members = build(4, seeded(4))
    old_key = next(iter(all_keys(tree).values()))
    newcomer = Member("late", seeded(5))
    tree.join(newcomer)
    new_key = newcomer.group_key(tree)
    assert new_key != old_key
    # The newcomer's only secret is its leaf key; with the public blinded keys it gets
    # nothing that equals the old group key.
    seen = {f(pow(n.bk, newcomer.k, P)) for n in nodes(tree) if n.bk is not None}
    assert old_key not in seen


def nodes(tree):
    out, stack = [], [tree.root]
    while stack:
        n = stack.pop()
        out.append(n)
        if n.member is None:
            stack += [n.left, n.right]
    return out


def test_removed_member_cannot_compute_new_key():
    tree, members = build(5, seeded(6))
    gone = members[3]
    # Everything the removed member knew: its leaf key and every key on its old path.
    known, k, node = [gone.k], gone.k, gone.leaf
    while node.parent is not None:
        k = f(pow(tree.sibling(node).bk, k, P))
        known.append(k)
        node = node.parent
    old_group_key = known[-1]
    tree.leave(gone)
    keys = all_keys(tree)
    assert len(keys) == 4 and len(set(keys.values())) == 1
    new_key = next(iter(keys.values()))
    assert new_key != old_group_key and new_key not in known
    # Combine every old secret with every new public blinded key: no hit.
    guesses = {f(pow(n.bk, s, P)) for n in nodes(tree) if n.bk is not None for s in known}
    assert new_key not in guesses
    assert tree.root.bk is None or tree.root.bk != pow(G, new_key, P)
