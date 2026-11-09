# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sldnf-resolution/. The authors are listed in prov/N5VQ4A.jsonl.

import itertools
import random

from sldnf_resolution import CUT, FINITE, FLOUNDER, sldnf

CONSTS = ["a", "b", "c"]
ARITY = {"e": 2, "r1": 1, "r2": 2, "r3": 1}
STRATA = ["e", "r1", "r2", "r3"]


def ground(t, env):
    return env[t] if isinstance(t, str) else (t[0],) + tuple(ground(a, env) for a in t[1:])


def lit_vars(lits):
    out = []
    for lit in lits:
        atom = lit[1] if lit[0] == "not" else lit
        for a in atom[1:]:
            if isinstance(a, str) and a not in out:
                out.append(a)
    return out


def perfect_model(program, order):
    """Stratum by stratum: the least fixed point of T_P for each predicate, with negation read in the lower strata."""
    model = set()
    for pred in order:
        rules = [(h, b) for h, b in program if h[0] == pred]
        changed = True
        while changed:
            changed = False
            for head, body in rules:
                vs = lit_vars([head] + body)
                for combo in itertools.product([(c,) for c in CONSTS], repeat=len(vs)):
                    env = dict(zip(vs, combo))
                    ok = all(
                        (ground(l[1], env) not in model) if l[0] == "not" else (ground(l, env) in model) for l in body
                    )
                    h = ground(head, env)
                    if ok and h not in model:
                        model.add(h)
                        changed = True
    return model


def rand_stratified(rng):
    prog = [(("e", (x,), (y,)), []) for x in CONSTS for y in CONSTS if rng.random() < 0.35]
    for level in range(1, 4):
        pred = STRATA[level]
        lower = STRATA[:level]
        for _ in range(rng.randint(1, 3)):
            pos = []
            for _ in range(rng.randint(1, 2)):
                p = rng.choice(lower)
                pos.append((p,) + tuple(rng.choice("XYZ") for _ in range(ARITY[p])))
            vs = lit_vars(pos)
            neg = []
            for _ in range(rng.randint(0, 2)):
                p = rng.choice(lower)
                neg.append(("not", (p,) + tuple(rng.choice(vs) for _ in range(ARITY[p]))))
            head = (pred,) + tuple(rng.choice(vs) for _ in range(ARITY[pred]))
            prog.append((head, pos + neg))
    return prog


def test_random_stratified_against_perfect_model() -> None:
    rng = random.Random(11)
    nonempty = 0
    for _ in range(200):
        prog = rand_stratified(rng)
        model = perfect_model(prog, STRATA)
        for pred in STRATA[1:]:
            query = [(pred,) + tuple("UV"[: ARITY[pred]])]
            answers, status = sldnf(prog, query, depth=40)
            assert status == FINITE
            got = {(pred,) + tuple(a[v] for v in "UV"[: ARITY[pred]]) for a in answers}
            want = {f for f in model if f[0] == pred}
            assert got == want
            nonempty += bool(want)
            # A ground negative query succeeds exactly when the atom is not in the perfect model.
            for args in itertools.product([(c,) for c in CONSTS], repeat=ARITY[pred]):
                atom = (pred,) + args
                answers, status = sldnf(prog, [("not", atom)], depth=40)
                assert status == FINITE
                assert bool(answers) == (atom not in model)
    assert nonempty > 100


def test_recursion_with_negation() -> None:
    edges = [("a", "b"), ("b", "c")]
    prog = [(("e", (x,), (y,)), []) for x, y in edges]
    prog += [(("node", (x,)), []) for x in CONSTS]
    prog += [
        (("tc", "X", "Y"), [("e", "X", "Y")]),
        (("tc", "X", "Y"), [("e", "X", "Z"), ("tc", "Z", "Y")]),
        (("unreach", "X", "Y"), [("node", "X"), ("node", "Y"), ("not", ("tc", "X", "Y"))]),
    ]
    answers, status = sldnf(prog, [("unreach", "X", "Y")])
    assert status == FINITE
    got = {(a["X"][0], a["Y"][0]) for a in answers}
    assert got == {(x, y) for x in CONSTS for y in CONSTS} - {("a", "b"), ("b", "c"), ("a", "c")}


def test_incomplete_for_the_completion() -> None:
    # comp(P) contains p <-> q or not q, so p follows from comp(P). SLDNF cannot show it: the tree for q is infinite.
    prog = [(("p",), [("q",)]), (("p",), [("not", ("q",))]), (("q",), [("q",)])]
    for depth in (5, 20, 60):
        answers, status = sldnf(prog, [("p",)], depth=depth)
        assert answers == [] and status == CUT


def test_floundering() -> None:
    prog = [(("p", "X"), [("not", ("q", "X"))]), (("q", ("a",)), [])]
    assert sldnf(prog, [("p", "X")]) == ([], FLOUNDER)
    assert sldnf(prog, [("p", ("b",))]) == ([{}], FINITE)
    assert sldnf(prog, [("p", ("a",))]) == ([], FINITE)


def test_negation_is_not_classical() -> None:
    # The query "not q" succeeds, although q is not false in every model of P.
    prog = [(("p",), [])]
    assert sldnf(prog, [("not", ("q",))]) == ([{}], FINITE)
    assert sldnf(prog, [("not", ("p",))]) == ([], FINITE)
