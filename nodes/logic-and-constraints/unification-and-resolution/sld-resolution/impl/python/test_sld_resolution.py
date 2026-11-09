# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sld-resolution/. The authors are listed in prov/1G4RR0.jsonl.

import itertools
import random

import pytest

from sld_resolution import StepLimit, leftmost, rightmost, solve


def middle(goal):
    return len(goal) // 2


RULES = [leftmost, rightmost, middle]
CONSTS = ["a", "b", "c"]


def ground(t, env):
    return env[t] if isinstance(t, str) else (t[0],) + tuple(ground(a, env) for a in t[1:])


def clause_vars(head, body):
    out = []
    for atom in [head] + body:
        for a in atom[1:]:
            if isinstance(a, str) and a not in out:
                out.append(a)
    return out


def least_model_with_sizes(program):
    """Bottom-up: iterate T_P to its least fixed point. For each atom also find the size of its smallest proof tree."""
    size = {}
    changed = True
    while changed:
        changed = False
        for head, body in program:
            vs = clause_vars(head, body)
            for combo in itertools.product([(c,) for c in CONSTS], repeat=len(vs)):
                env = dict(zip(vs, combo))
                if all(ground(b, env) in size for b in body):
                    cost = 1 + sum(size[ground(b, env)] for b in body)
                    h = ground(head, env)
                    if cost < size.get(h, float("inf")):
                        size[h] = cost
                        changed = True
    return size


def t_p_stages(program):
    """The sets T_P up to n of the empty set, for n = 1, 2, ... until the fixed point."""
    stages, model = [], set()
    while True:
        new = set()
        for head, body in program:
            vs = clause_vars(head, body)
            for combo in itertools.product([(c,) for c in CONSTS], repeat=len(vs)):
                env = dict(zip(vs, combo))
                if all(ground(b, env) in model for b in body):
                    new.add(ground(head, env))
        if new == model:
            return stages
        model = new
        stages.append(model)


def rand_program(rng):
    edb = [(("e", (x,), (y,)), []) for x in CONSTS for y in CONSTS if rng.random() < 0.3]
    rules = []
    for _ in range(rng.randint(1, 4)):
        body = []
        for _ in range(rng.randint(1, 2)):
            p = rng.choice(["e", "p", "q"])
            arity = 1 if p == "q" else 2
            body.append((p,) + tuple(rng.choice("XYZ") for _ in range(arity)))
        bvars = sorted({a for b in body for a in b[1:]})
        hp = rng.choice(["p", "q"])
        harity = 1 if hp == "q" else 2
        rules.append(((hp,) + tuple(rng.choice(bvars) for _ in range(harity)), body))
    rng.shuffle(rules)
    return edb + rules


def test_append_splits() -> None:
    nil = ("nil",)

    def lst(*xs):
        out = nil
        for x in reversed(xs):
            out = ("cons", (x,), out)
        return out

    app = [
        (("app", nil, "L", "L"), []),
        (("app", ("cons", "H", "T"), "L", ("cons", "H", "R")), [("app", "T", "L", "R")]),
    ]
    got = solve(app, [("app", "X", "Y", lst("a", "b"))])
    assert got == [
        {"X": nil, "Y": lst("a", "b")},
        {"X": lst("a"), "Y": lst("b")},
        {"X": lst("a", "b"), "Y": nil},
    ]
    # A computed answer can keep variables: app([a], Y, Z) gives Z = [a | Y].
    (ans,) = solve(app, [("app", lst("a"), "Y", "Z")])
    assert ans["Z"] == ("cons", ("a",), ans["Y"])


def test_independence_of_the_computation_rule_on_append() -> None:
    nil = ("nil",)
    app = [
        (("app", nil, "L", "L"), []),
        (("app", ("cons", "H", "T"), "L", ("cons", "H", "R")), [("app", "T", "L", "R")]),
    ]
    goal = [("app", "X", "Y", "Z"), ("app", "Z", "W", ("cons", ("a",), ("cons", ("b",), nil)))]
    results = [sorted(map(repr, solve(app, goal, rule=r, depth=6))) for r in RULES]
    assert results[0] == results[1] == results[2]
    assert len(results[0]) == 6


def test_prolog_search_is_incomplete() -> None:
    prog = [(("p",), [("p",)]), (("p",), [])]
    with pytest.raises(StepLimit) as info:
        solve(prog, [("p",)], max_steps=10000)
    assert info.value.args[0] == []
    assert solve(prog, [("p",)], depth=3) == [{}, {}, {}]
    # With the clauses in the other order, the first answer comes at once.
    prog2 = [(("p",), []), (("p",), [("p",)])]
    with pytest.raises(StepLimit) as info:
        solve(prog2, [("p",)], max_steps=10)
    assert len(info.value.args[0]) > 0


def test_transitive_closure_stages() -> None:
    edges = [("a", "b"), ("b", "c")]
    prog = [(("e", (x,), (y,)), []) for x, y in edges]
    prog += [(("path", "X", "Y"), [("e", "X", "Y")]), (("path", "X", "Y"), [("e", "X", "Z"), ("path", "Z", "Y")])]
    stages = t_p_stages(prog)
    assert [len(s) for s in stages] == [2, 4, 5]
    got = {(a["X"], a["Y"]) for a in solve(prog, [("path", "X", "Y")])}
    assert got == {(("a",), ("b",)), (("b",), ("c",)), (("a",), ("c",))}


def test_random_datalog_against_least_model() -> None:
    rng = random.Random(5)
    depth = 7
    nonempty = 0
    for _ in range(150):
        prog = rand_program(rng)
        size = least_model_with_sizes(prog)
        for pred, arity in (("p", 2), ("q", 1)):
            query = [(pred,) + tuple("UV"[:arity])]
            want = {atom for atom, k in size.items() if atom[0] == pred and k <= depth}
            for r in RULES:
                got = {(pred,) + tuple(ans[v] for v in "UV"[:arity]) for ans in solve(prog, query, rule=r, depth=depth)}
                assert all(g in size for g in got)  # soundness: each answer is in the least model
                assert got == want  # completeness up to the depth bound, for each computation rule
            nonempty += bool(want)
    assert nonempty > 50
