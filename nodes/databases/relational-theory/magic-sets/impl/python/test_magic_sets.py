# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/magic-sets/. The authors are listed in prov/SCYM7S.jsonl.

import random

from magic_sets import answer_full, answer_with_magic, magic_rewrite

TC_RIGHT = [
    (("path", ("X", "Y")), [("edge", ("X", "Y"))]),
    (("path", ("X", "Y")), [("edge", ("X", "Z")), ("path", ("Z", "Y"))]),
]
TC_LEFT = [
    (("path", ("X", "Y")), [("edge", ("X", "Y"))]),
    (("path", ("X", "Y")), [("path", ("X", "Z")), ("edge", ("Z", "Y"))]),
]
TC_DOUBLE = [
    (("path", ("X", "Y")), [("edge", ("X", "Y"))]),
    (("path", ("X", "Y")), [("path", ("X", "Z")), ("path", ("Z", "Y"))]),
]
SAME_GENERATION = [
    (("sg", ("X", "Y")), [("flat", ("X", "Y"))]),
    (("sg", ("X", "Y")), [("up", ("X", "U")), ("sg", ("U", "V")), ("down", ("V", "Y"))]),
]


def chain(n):
    return {("edge", (i, i + 1)) for i in range(1, n)}


def test_rewritten_program_shape() -> None:
    program, qname = magic_rewrite(TC_RIGHT, ("path", (5, "Y")))
    assert qname == "path_bf"
    assert (("magic_path_bf", (5,)), []) in program
    assert (("magic_path_bf", ("Z",)), [("magic_path_bf", ("X",)), ("edge", ("X", "Z"))]) in program
    assert (
        ("path_bf", ("X", "Y")),
        [("magic_path_bf", ("X",)), ("edge", ("X", "Z")), ("path_bf", ("Z", "Y"))],
    ) in program
    assert len(program) == 4


def test_chain_counts_of_the_page() -> None:
    db = chain(20)
    for prog, full_count, magic_count in (
        (TC_RIGHT, 190, 66),
        (TC_LEFT, 190, 11),
        (TC_DOUBLE, 190, 66),
    ):
        a1, c1 = answer_full(prog, db, ("path", (10, "Y")))
        a2, c2 = answer_with_magic(prog, db, ("path", (10, "Y")))
        assert a1 == a2 == {(10, y) for y in range(11, 21)}
        assert (c1, c2) == (full_count, magic_count)
        assert c2 < c1


def test_same_generation_tree_counts() -> None:
    # A complete binary tree of depth 5: up goes to the parent, down to a child, and
    # flat joins each node to itself.
    nodes = range(1, 64)
    db = {("up", (v, v // 2)) for v in nodes if v > 1}
    db |= {("down", (v // 2, v)) for v in nodes if v > 1}
    db |= {("flat", (v, v)) for v in nodes}
    a1, c1 = answer_full(SAME_GENERATION, db, ("sg", (40, "Y")))
    a2, c2 = answer_with_magic(SAME_GENERATION, db, ("sg", (40, "Y")))
    assert a1 == a2 == {(40, y) for y in range(32, 64)}
    assert c2 < c1
    # 6 magic facts (node 40 and its ancestors) and 63 sg facts for them.
    assert (c1, c2) == (1365, 69)


def test_random_graphs_match_full_evaluation() -> None:
    rng = random.Random(41)
    smaller = 0
    for _ in range(300):
        n = rng.randint(1, 9)
        db = {("edge", (rng.randrange(n), rng.randrange(n))) for _ in range(rng.randint(0, 12))}
        c = rng.randrange(n)
        for prog in (TC_RIGHT, TC_LEFT, TC_DOUBLE):
            for query in (("path", (c, "Y")), ("path", ("X", c)), ("path", ("X", "Y"))):
                a1, c1 = answer_full(prog, db, query)
                a2, c2 = answer_with_magic(prog, db, query)
                assert a1 == a2
                smaller += c2 < c1
    assert smaller > 300


def test_random_same_generation() -> None:
    rng = random.Random(42)
    for _ in range(300):
        n = rng.randint(1, 7)
        db = set()
        for name in ("up", "down", "flat"):
            db |= {(name, (rng.randrange(n), rng.randrange(n))) for _ in range(rng.randint(0, 8))}
        c = rng.randrange(n)
        for query in (("sg", (c, "Y")), ("sg", ("X", c)), ("sg", (c, c))):
            assert answer_full(SAME_GENERATION, db, query)[0] == answer_with_magic(SAME_GENERATION, db, query)[0]


def random_program(rng):
    variables = "XYZW"
    program = []
    for _ in range(rng.randint(1, 4)):
        body = []
        for _ in range(rng.randint(1, 3)):
            pred = rng.choice(("e", "e", "p", "q"))
            terms = tuple(rng.choice(variables) if rng.random() < 0.85 else rng.randrange(3) for _ in range(2))
            body.append((pred, terms))
        used = sorted({t for _, ts in body for t in ts if isinstance(t, str)}) or [0]
        head = (rng.choice(("p", "q")), (rng.choice(used), rng.choice(used)))
        program.append((head, body))
    return program


def test_random_programs() -> None:
    rng = random.Random(43)
    for _ in range(600):
        program = random_program(rng)
        n = rng.randint(1, 4)
        db = {("e", (rng.randrange(n), rng.randrange(n))) for _ in range(rng.randint(0, 8))}
        pred = rng.choice(sorted({h[0] for h, _ in program}))
        terms = tuple(rng.choice(("X", "Y", rng.randrange(n))) for _ in range(2))
        query = (pred, terms)
        assert answer_full(program, db, query)[0] == answer_with_magic(program, db, query)[0]


def test_edges() -> None:
    assert answer_with_magic(TC_RIGHT, set(), ("path", (1, "Y")))[0] == set()
    assert answer_with_magic(TC_RIGHT, chain(3), ("path", (1, 3)))[0] == {(1, 3)}
    assert answer_with_magic(TC_RIGHT, chain(3), ("path", (3, 1)))[0] == set()
    assert answer_with_magic(TC_RIGHT, {("edge", (1, 1))}, ("path", ("X", "X")))[0] == {(1, 1)}
