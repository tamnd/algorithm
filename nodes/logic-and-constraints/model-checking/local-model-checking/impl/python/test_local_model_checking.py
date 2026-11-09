# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-model-checking/. The authors are listed in prov/SYAG8V.jsonl.

import itertools
import random

from local_model_checking import LocalChecker, dual, local_model_checking


def global_eval(model, f, env=None):
    """Oracle: the set of states that satisfy f, by Knaster-Tarski iteration over all states."""
    env = env or {}
    states = set(model["succ"])
    op = f[0]
    if op == "true":
        return set(states)
    if op == "false":
        return set()
    if op == "ap":
        return {s for s in states if f[1] in model["label"][s]}
    if op == "nap":
        return {s for s in states if f[1] not in model["label"][s]}
    if op == "and":
        return global_eval(model, f[1], env) & global_eval(model, f[2], env)
    if op == "or":
        return global_eval(model, f[1], env) | global_eval(model, f[2], env)
    if op == "dia":
        a = global_eval(model, f[1], env)
        return {s for s in states if any(t in a for t in model["succ"][s])}
    if op == "box":
        a = global_eval(model, f[1], env)
        return {s for s in states if all(t in a for t in model["succ"][s])}
    if op == "var":
        return env[f[1]]
    cur = set() if op == "mu" else set(states)
    while True:
        nxt = global_eval(model, f[2], {**env, f[1]: cur})
        if nxt == cur:
            return cur
        cur = nxt


P, Q = ("ap", "p"), ("ap", "q")


def EF(f, x):
    return ("mu", x, ("or", f, ("dia", ("var", x))))


def AG(f, x):
    return ("nu", x, ("and", f, ("box", ("var", x))))


def EU(f, g, x):
    return ("mu", x, ("or", g, ("and", f, ("dia", ("var", x)))))


def AF(f, x):
    return ("mu", x, ("or", f, ("and", ("box", ("var", x)), ("dia", ("true",)))))


def EG(f, x):
    return ("nu", x, ("and", f, ("dia", ("var", x))))


class Gen:
    """Random closed alternation-free formulas: each fixed-point body uses only its own
    variable and closed subformulas."""

    def __init__(self, rng):
        self.rng = rng
        self.count = 0

    def fresh(self):
        self.count += 1
        return f"X{self.count}"

    def closed(self, depth):
        r = self.rng
        if depth == 0 or r.random() < 0.2:
            return r.choice([P, Q, ("nap", "p"), ("nap", "q"), ("true",), ("false",)])
        k = r.randint(0, 5)
        if k == 0:
            return (r.choice(["and", "or"]), self.closed(depth - 1), self.closed(depth - 1))
        if k == 1:
            return (r.choice(["dia", "box"]), self.closed(depth - 1))
        x = self.fresh()
        return (r.choice(["mu", "nu"]), x, self.body(x, depth - 1))

    def body(self, x, depth):
        r = self.rng
        if depth == 0 or r.random() < 0.25:
            return r.choice([("var", x), self.closed(0)])
        k = r.randint(0, 2)
        if k == 0:
            return (r.choice(["and", "or"]), self.body(x, depth - 1), self.body(x, depth - 1))
        if k == 1:
            return (r.choice(["dia", "box"]), self.body(x, depth - 1))
        return self.closed(depth - 1)


def random_model(rng, n):
    succ = {s: rng.sample(range(n), rng.randint(0, min(2, n))) for s in range(n)}
    label = {s: {a for a in ("p", "q") if rng.random() < 0.4} for s in range(n)}
    return {"succ": succ, "label": label}


CHAIN = {
    "succ": {0: [1, 2], 1: [3], 2: [4], 3: [5], 4: [4], 5: [5]},
    "label": {0: set(), 1: {"p"}, 2: set(), 3: set(), 4: set(), 5: {"q"}},
}


def test_example() -> None:
    c = LocalChecker(CHAIN)
    assert c.holds(0, EF(P, "X"))
    assert c.vertices == 8  # only states 0 and 1 are touched
    assert not local_model_checking(CHAIN, 0, AF(P, "X"))
    assert local_model_checking(CHAIN, 1, AG(("nap", "q"), "Y")) is False
    assert local_model_checking(CHAIN, 2, AG(("nap", "q"), "Y")) is True


def test_named_operators() -> None:
    rng = random.Random(5)
    ops = [EF(P, "A"), AG(P, "B"), EU(P, Q, "C"), AF(Q, "D"), EG(("nap", "q"), "E"),
           AG(EF(P, "F1"), "F2"), EF(AG(Q, "G1"), "G2")]
    for _ in range(150):
        m = random_model(rng, rng.randint(1, 6))
        for f in ops:
            truth = global_eval(m, f)
            for s in m["succ"]:
                assert local_model_checking(m, s, f) == (s in truth), (m, f, s)


def test_random_formulas_against_global_iteration() -> None:
    rng = random.Random(1998)
    gen = Gen(rng)
    checked = 0
    for _ in range(600):
        m = random_model(rng, rng.randint(1, 5))
        f = gen.closed(4)
        truth = global_eval(m, f)
        c = LocalChecker(m)
        for s in m["succ"]:
            assert c.holds(s, f) == (s in truth), (m, f, s)
            checked += 1
    assert checked > 1500


def test_dual_is_negation() -> None:
    rng = random.Random(3)
    gen = Gen(rng)
    for _ in range(200):
        m = random_model(rng, 4)
        f = gen.closed(3)
        assert global_eval(m, dual(f)) == set(m["succ"]) - global_eval(m, f)


def test_locality_on_a_long_chain() -> None:
    n = 20000
    m = {"succ": {s: [s + 1] for s in range(n)}, "label": {s: set() for s in range(n)}}
    m["succ"][n - 1] = [n - 1]
    m["label"][1] = {"p"}
    c = LocalChecker(m)
    assert c.holds(0, EF(P, "X"))
    assert c.vertices < 20
    assert local_model_checking(m, 2, EF(P, "X")) is False


def test_deadlock_states() -> None:
    m = {"succ": {0: []}, "label": {0: set()}}
    assert local_model_checking(m, 0, ("box", ("false",)))
    assert not local_model_checking(m, 0, ("dia", ("true",)))
    assert local_model_checking(m, 0, AG(("nap", "p"), "X"))
    assert not local_model_checking(m, 0, EG(("true",), "Y"))


def test_all_states_small_exhaustive_models() -> None:
    f = AG(EF(P, "X"), "Y")
    for edges in itertools.product([[], [0], [1], [0, 1]], repeat=2):
        for labs in itertools.product([set(), {"p"}], repeat=2):
            m = {"succ": dict(enumerate(edges)), "label": dict(enumerate(labs))}
            truth = global_eval(m, f)
            for s in (0, 1):
                assert local_model_checking(m, s, f) == (s in truth)
