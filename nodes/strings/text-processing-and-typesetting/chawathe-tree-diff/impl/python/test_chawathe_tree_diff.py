# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chawathe-tree-diff/. The authors are listed in prov/Y3W16W.jsonl.

import random

from chawathe_tree_diff import (Del, Ins, Mov, Tree, Upd, add_root, apply_script, edit_script, fast_match,
                                isomorphic, lower_bound, word_compare)


def S(value: str) -> tuple:
    return ("S", value)


# Figure 1 of the paper: documents (D) of paragraphs (P) of sentences (S).
T1 = Tree.from_nested(("D", None, [("P", None, [S("a"), S("b"), S("c")]), ("P", None, [S("d"), S("e")]),
                                   ("P", None, [S("f")])]))
T2 = Tree.from_nested(("D", None, [("P", None, [S("a"), S("c")]), ("P", None, [S("f")]),
                                   ("P", None, [S("d"), S("e"), S("g")])]), first_id=11)


def test_running_example() -> None:
    m = fast_match(T1, T2)
    # The matching of Example 5.1, which Algorithm Match finds there.
    assert m == sorted([(5, 15), (7, 16), (8, 18), (9, 19), (10, 17), (2, 12), (3, 14), (4, 13), (1, 11)])
    result = edit_script(T1, T2, m)
    # The paper moves node 4 where this LCS moves node 3; both scripts have three operations.
    assert result.script == [Mov(3, 1, 3), Ins(21, "S", "g", 3, 3), Del(6)]
    assert [str(op) for op in result.script] == ["MOV(3,1,3)", "INS((21,S,g),3,3)", "DEL(6)"]
    assert isomorphic(apply_script(T1, result.script), T2)
    assert isomorphic(apply_script(T1, [Mov(4, 1, 2), Ins(21, "S", "g", 3, 3), Del(6)]), T2)
    assert lower_bound(T1, T2, m) == 3 and result.root1 is None
    assert result.matching[21] == 20 and all(result.matching[x] == y for x, y in m)


def test_align_children_of_figure_7() -> None:
    t1 = Tree.from_nested(("A", None, [("B", i) for i in range(5)]))
    t2 = Tree.from_nested(("A", None, [("B", i) for i in (1, 3, 4, 0, 2)]), first_id=11)
    m = [(1, 11), (3, 12), (5, 13), (6, 14), (2, 15), (4, 16)]
    result = edit_script(t1, t2, m)
    assert result.script == [Mov(2, 1, 5), Mov(4, 1, 5)]
    assert isomorphic(apply_script(t1, result.script), t2)


def test_find_pos_counts_all_children() -> None:
    # The unmatched child d is still there when b is inserted; counting only the
    # children marked in order would put b at position 2, before a.
    t1 = Tree.from_nested(("r", None, [("x", "d"), ("x", "a")]))
    t2 = Tree.from_nested(("r", None, [("x", "a"), ("x", "b")]), first_id=11)
    result = edit_script(t1, t2, [(1, 11), (3, 12)])
    assert result.script == [Ins(14, "x", "b", 1, 3), Del(2)]
    assert isomorphic(apply_script(t1, result.script), t2)
    assert not isomorphic(apply_script(t1, [Ins(14, "x", "b", 1, 2), Del(2)]), t2)
    # Two new nodes in a row: the first one must count as placed when the second is placed.
    t3 = Tree.from_nested(("r", None, [("x", "a"), ("x", "b"), ("x", "c")]), first_id=11)
    result = edit_script(t1, t3, [(1, 11), (3, 12)])
    assert result.script == [Ins(15, "x", "b", 1, 3), Ins(16, "x", "c", 1, 4), Del(2)]
    assert isomorphic(apply_script(t1, result.script), t3)


def test_dummy_roots_and_updates() -> None:
    t1 = Tree.from_nested(("r", None, [("x", "u")]))
    t2 = Tree.from_nested(("s", None, [("x", "v")]), first_id=11)
    result = edit_script(t1, t2, [(2, 12)])
    assert (result.root1, result.root2) == (13, 14)
    assert result.script == [Ins(15, "s", None, 13, 1), Upd(2, "v"), Mov(2, 15, 1), Del(1)]
    assert isomorphic(apply_script(add_root(t1, 13), result.script), add_root(t2, 14))
    assert len(result.script) == lower_bound(t1, t2, [(2, 12)])
    # The script respects the matching: without the pair (2, 12), x is deleted and inserted.
    t3 = Tree.from_nested(("r", None, [("x", "v")]), first_id=11)
    assert edit_script(t1, t3, [(1, 11), (2, 12)]).script == [Upd(2, "v")]
    assert edit_script(t1, t3, [(1, 11)]).script == [Ins(13, "x", "v", 1, 1), Del(2)]
    for bad in ([(1, 12)], [(1, 11), (2, 11)], [(9, 11)]):
        try:
            edit_script(t1, t3, bad)
        except ValueError:
            continue
        raise AssertionError(f"{bad} was accepted")


def _random_spec(rng: random.Random, depth: int) -> tuple:
    if depth == 0 or rng.random() < 0.3:
        return (rng.choice("xy"), rng.choice("pqr"))
    return (rng.choice("AB"), None, [_random_spec(rng, depth - 1) for _ in range(rng.randint(1, 4))])


def _random_matching(rng: random.Random, t1: Tree, t2: Tree) -> list[tuple[int, int]]:
    nodes2 = list(t2.label)
    rng.shuffle(nodes2)
    used: set[int] = set()
    pairs = []
    for x in t1.label:
        if rng.random() < 0.75:
            for y in nodes2:
                if y not in used and t2.label[y] == t1.label[x]:
                    pairs.append((x, y))
                    used.add(y)
                    break
    return pairs


def test_random_scripts_are_correct_and_minimal() -> None:
    rng = random.Random(16)
    for trial in range(400):
        t1 = Tree.from_nested(_random_spec(rng, 3))
        t2 = Tree.from_nested(_random_spec(rng, 3), first_id=1 if trial % 2 else 100)
        m = _random_matching(rng, t1, t2)
        result = edit_script(t1, t2, m)
        start, goal = t1, t2
        if result.root1 is not None:
            start, goal = add_root(t1, result.root1), add_root(t2, result.root2)
        final = apply_script(start, result.script)
        assert isomorphic(final, goal)
        # The total matching extends the given one and maps the final tree onto T2.
        total = result.matching
        assert all(total[x] == y for x, y in m)
        assert sorted(total) == sorted(final.label) and sorted(total.values()) == sorted(goal.label)
        for w, x in total.items():
            assert final.label[w] == goal.label[x] and final.value[w] == goal.value[x]
            if w != final.root:
                assert total[final.parent[w]] == goal.parent[x]
        assert len(result.script) == lower_bound(t1, t2, m)


def test_fast_match() -> None:
    assert word_compare("the cat sat", "the cat sat") == 0
    assert word_compare("the cat sat", "a dog ran") == 2
    assert word_compare("the cat sat", "the cat ran") == 2 - 4 * 2 / 6
    rng = random.Random(5)
    words = "alpha beta gamma delta epsilon zeta eta theta".split()
    for _ in range(100):
        # Distinct sentences meet Matching Criterion 3, so a copy with moved subtrees matches in full.
        values = iter(rng.sample([f"{a} {b}" for a in words for b in words], 40))

        def spec(depth: int) -> tuple:
            if depth == 0 or rng.random() < 0.3:
                return ("S", next(values))
            return ("P", None, [spec(depth - 1) for _ in range(rng.randint(1, 3))])

        t1 = Tree.from_nested(("D", None, [spec(2) for _ in range(rng.randint(1, 3))]))
        nested = t1.nested()
        kids = list(nested[2])
        rng.shuffle(kids)

        def to_spec(n: tuple) -> tuple:
            return (n[0], n[1], [to_spec(c) for c in n[2]]) if n[0] != "S" else (n[0], n[1])

        t2 = Tree.from_nested(to_spec((nested[0], nested[1], tuple(kids))), first_id=100)
        m = fast_match(t1, t2)
        assert len(m) == len(t1.label)
        result = edit_script(t1, t2, m)
        assert not any(isinstance(op, (Ins, Del, Upd)) for op in result.script)
        assert isomorphic(apply_script(t1, result.script), t2)
    try:
        fast_match(T1, T2, t=0.4)
    except ValueError:
        return
    raise AssertionError("t below 1/2 was accepted")
