# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dred-algorithm/. The authors are listed in prov/K2D6D5.jsonl.

import random

from dred_algorithm import dred, least_model

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
# A nonrecursive view: the pairs joined by a path of length 2, and a view over it.
HOP2 = [
    (("hop2", ("X", "Y")), [("edge", ("X", "Z")), ("edge", ("Z", "Y"))]),
    (("tri", ("X",)), [("hop2", ("X", "Y")), ("edge", ("Y", "X"))]),
]


def e(a, b):
    return ("edge", (a, b))


def p(a, b):
    return ("path", (a, b))


def test_example_of_the_page() -> None:
    edb = {e(1, 2), e(2, 3), e(3, 4), e(1, 3)}
    model = least_model(TC_RIGHT, edb)
    edb2, model2, over, red, ins = dred(TC_RIGHT, edb, model, [e(2, 3)], [])
    assert edb2 == {e(1, 2), e(3, 4), e(1, 3)}
    assert model2 == edb2 | {p(1, 2), p(1, 3), p(1, 4), p(3, 4)}
    assert (over, red, ins) == (4, 2, 0)
    # Insert the edge back: the semi-naive insert phase derives the two lost facts.
    edb3, model3, over, red, ins = dred(TC_RIGHT, edb2, model2, [], [e(2, 3)])
    assert model3 == model and (over, red, ins) == (0, 0, 2)


def test_cycle_is_not_kept_alive() -> None:
    # On a cycle every path fact supports the others. Counting the derivations would keep
    # them; DRed removes them all.
    edb = {e(1, 2), e(2, 3), e(3, 1)}
    model = least_model(TC_RIGHT, edb)
    edb2, model2, over, red, ins = dred(TC_RIGHT, edb, model, [e(3, 1)], [])
    assert model2 == least_model(TC_RIGHT, edb2)
    # All 9 path facts are overdeleted. Path(1, 2) and path(2, 3) are rederived from
    # their edges, and the insert phase then derives path(1, 3) from them.
    assert (over, red, ins) == (9, 2, 1)


def run_sequence(rng, program, preds, n, steps) -> None:
    edb = set()
    model = least_model(program, edb)
    for _ in range(steps):
        dels = rng.sample(sorted(edb), min(len(edb), rng.randint(0, 3)))
        ins = [(rng.choice(preds), (rng.randrange(n), rng.randrange(n))) for _ in range(rng.randint(0, 3))]
        edb, model, over, red, _ = dred(program, edb, model, dels, ins)
        assert model == least_model(program, edb)
        assert red <= over


def test_random_updates_transitive_closure() -> None:
    rng = random.Random(51)
    for _ in range(60):
        for prog in (TC_RIGHT, TC_LEFT, TC_DOUBLE):
            run_sequence(rng, prog, ["edge"], rng.randint(2, 6), 12)


def test_random_updates_nonrecursive_view() -> None:
    rng = random.Random(52)
    for _ in range(100):
        run_sequence(rng, HOP2, ["edge"], rng.randint(2, 5), 10)


def random_program(rng):
    variables = "XYZW"
    program = []
    for _ in range(rng.randint(1, 4)):
        body = []
        for _ in range(rng.randint(1, 3)):
            pred = rng.choice(("e", "f", "p", "q"))
            terms = tuple(rng.choice(variables) if rng.random() < 0.9 else rng.randrange(3) for _ in range(2))
            body.append((pred, terms))
        used = sorted({t for _, ts in body for t in ts if isinstance(t, str)}) or [0]
        head = (rng.choice(("p", "q")), (rng.choice(used), rng.choice(used)))
        program.append((head, body))
    return program


def test_random_programs_and_updates() -> None:
    rng = random.Random(53)
    for _ in range(400):
        run_sequence(rng, random_program(rng), ["e", "f"], rng.randint(1, 4), 6)


def test_edges() -> None:
    edb = {e(1, 2)}
    model = least_model(TC_RIGHT, edb)
    # Deleting a fact that is not stored, or deleting and inserting the same fact, changes nothing.
    assert dred(TC_RIGHT, edb, model, [e(5, 6)], [])[1] == model
    assert dred(TC_RIGHT, edb, model, [e(1, 2)], [e(1, 2)])[1] == model
    assert dred(TC_RIGHT, edb, model, [e(1, 2)], [])[1] == set()
    try:
        dred(TC_RIGHT, edb, model, [p(1, 2)], [])
    except ValueError:
        pass
    else:
        raise AssertionError("derived facts cannot be deleted directly")
