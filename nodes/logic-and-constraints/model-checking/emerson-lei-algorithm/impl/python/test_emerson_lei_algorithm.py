# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/emerson-lei-algorithm/. The authors are listed in prov/N9RYM5.jsonl.

import itertools
import random
from collections import deque

import pytest

from emerson_lei_algorithm import (
    alternation_depth,
    emerson_lei,
    evaluate,
    fixpoints,
    naive_iteration,
    nesting_depth,
)

P, Q = ("ap", "p"), ("ap", "q")


def random_structure(rng: random.Random, n: int):
    states = list(range(n))
    succ = {s: sorted(set(rng.choice(states) for _ in range(rng.randint(1, 3)))) for s in states}
    label = {s: {a for a in "pq" if rng.random() < 0.5} for s in states}
    return states, succ, label


# ---------------------------------------------------------------- reference 1: Knaster-Tarski by brute force


def tarski(states, succ, label, phi) -> set:
    """Evaluate phi by the definition: mu is the meet of all pre-fixed points,
    nu is the join of all post-fixed points. Exponential; for at most 4 states."""
    subsets = [frozenset(c) for k in range(len(states) + 1) for c in itertools.combinations(states, k)]
    full = frozenset(states)

    def ev(f, env) -> frozenset:
        op = f[0]
        if op == "true":
            return full
        if op == "false":
            return frozenset()
        if op == "ap":
            return frozenset(s for s in states if f[1] in label[s])
        if op == "nap":
            return frozenset(s for s in states if f[1] not in label[s])
        if op == "var":
            return env[f[1]]
        if op == "and":
            return ev(f[1], env) & ev(f[2], env)
        if op == "or":
            return ev(f[1], env) | ev(f[2], env)
        if op == "dia":
            a = ev(f[1], env)
            return frozenset(s for s in states if any(t in a for t in succ[s]))
        if op == "box":
            a = ev(f[1], env)
            return frozenset(s for s in states if all(t in a for t in succ[s]))
        x, body = f[1], f[2]
        if op == "mu":
            out = full
            for y in subsets:
                if ev(body, {**env, x: y}) <= y:
                    out &= y
            return out
        out = frozenset()
        for y in subsets:
            if y <= ev(body, {**env, x: y}):
                out |= y
        return out

    return set(ev(phi, {}))


# ---------------------------------------------------------------- reference 2: the CTL labelling algorithm


def ctl_sat(states, succ, label, phi) -> set:
    """A compact copy of the CTL labelling algorithm (backward search and SCCs)."""
    full = set(states)
    pred = {s: [] for s in states}
    for s in states:
        for t in succ[s]:
            pred[t].append(s)

    def back(a, x):
        x = set(x)
        queue = deque(x)
        while queue:
            t = queue.popleft()
            for s in pred[t]:
                if s in a and s not in x:
                    x.add(s)
                    queue.append(s)
        return x

    def eg(a):
        # a state of a is on a cycle inside a if it reaches itself inside a
        on_cycle = set()
        for s in a:
            seen, queue = set(), deque(t for t in succ[s] if t in a)
            while queue:
                v = queue.popleft()
                if v in seen:
                    continue
                seen.add(v)
                queue.extend(t for t in succ[v] if t in a)
            if s in seen:
                on_cycle.add(s)
        return back(a, on_cycle)

    def au(a, b):
        nb = full - b
        return full - (back(nb, nb - a) | eg(nb))

    def go(f):
        op = f[0]
        if op == "true":
            return set(full)
        if op == "ap":
            return {s for s in states if f[1] in label[s]}
        if op == "not":
            return full - go(f[1])
        if op == "and":
            return go(f[1]) & go(f[2])
        if op == "or":
            return go(f[1]) | go(f[2])
        if op == "EX":
            a = go(f[1])
            return {s for s in states if any(t in a for t in succ[s])}
        if op == "AX":
            a = go(f[1])
            return {s for s in states if all(t in a for t in succ[s])}
        if op == "EU":
            return back(go(f[1]), go(f[2]))
        if op == "AU":
            return au(go(f[1]), go(f[2]))
        if op == "EG":
            return eg(go(f[1]))
        if op == "AG":
            return full - back(full, full - go(f[1]))
        if op == "EF":
            return back(full, go(f[1]))
        if op == "AF":
            return full - eg(full - go(f[1]))
        raise ValueError(op)

    return go(phi)


class Fresh:
    def __init__(self) -> None:
        self.n = 0

    def __call__(self) -> str:
        self.n += 1
        return f"Z{self.n}"


def to_mu(f, fresh: Fresh, neg: bool = False):
    """Translate a CTL formula to the mu-calculus, in positive normal form."""
    op = f[0]
    if op == "true":
        return ("false",) if neg else ("true",)
    if op == "ap":
        return ("nap", f[1]) if neg else f
    if op == "not":
        return to_mu(f[1], fresh, not neg)
    if op in ("and", "or"):
        dual = {"and": "or", "or": "and"}[op] if neg else op
        return (dual, to_mu(f[1], fresh, neg), to_mu(f[2], fresh, neg))
    if op in ("EX", "AX"):
        e = (op == "EX") != neg
        return ("dia" if e else "box", to_mu(f[1], fresh, neg))
    if op == "EF":
        return to_mu(("EU", ("true",), f[1]), fresh, neg)
    if op == "AF":
        return to_mu(("AU", ("true",), f[1]), fresh, neg)
    if op == "AG":
        return to_mu(("not", ("EF", ("not", f[1]))), fresh, neg)
    if op == "EG":
        z = fresh()
        if not neg:  # EG f = nu Z. f and <>Z
            return ("nu", z, ("and", to_mu(f[1], fresh), ("dia", ("var", z))))
        # not EG f = AF not f = mu Z. not f or []Z
        return ("mu", z, ("or", to_mu(f[1], fresh, True), ("box", ("var", z))))
    if op in ("EU", "AU"):
        z = fresh()
        a, b = f[1], f[2]
        if not neg:  # E[a U b] = mu Z. b or (a and <>Z); A uses []
            mod = "dia" if op == "EU" else "box"
            return ("mu", z, ("or", to_mu(b, fresh), ("and", to_mu(a, fresh), (mod, ("var", z)))))
        # not E[a U b] = nu Z. not b and (not a or []Z); A uses <>
        mod = "box" if op == "EU" else "dia"
        return ("nu", z, ("and", to_mu(b, fresh, True), ("or", to_mu(a, fresh, True), (mod, ("var", z)))))
    raise ValueError(op)


CTL_UNARY = ["not", "EX", "AX", "EF", "AF", "EG", "AG"]
CTL_BINARY = ["and", "or", "EU", "AU"]


def random_ctl(rng: random.Random, depth: int):
    if depth == 0 or rng.random() < 0.25:
        return rng.choice([P, Q, ("true",)])
    if rng.random() < 0.5:
        return (rng.choice(CTL_UNARY), random_ctl(rng, depth - 1))
    return (rng.choice(CTL_BINARY), random_ctl(rng, depth - 1), random_ctl(rng, depth - 1))


def random_mu(rng: random.Random, depth: int, scope: list, fresh: Fresh):
    """A random closed formula in positive normal form, with each variable bound once."""
    r = rng.random()
    if depth == 0 or r < 0.2:
        if scope and rng.random() < 0.6:
            return ("var", rng.choice(scope))
        return rng.choice([P, Q, ("nap", "p"), ("nap", "q"), ("true",), ("false",)])
    if r < 0.5:
        x = fresh()
        return (rng.choice(["mu", "nu"]), x, random_mu(rng, depth - 1, scope + [x], fresh))
    if r < 0.75:
        return (rng.choice(["dia", "box"]), random_mu(rng, depth - 1, scope, fresh))
    op = rng.choice(["and", "or"])
    return (op, random_mu(rng, depth - 1, scope, fresh), random_mu(rng, depth - 1, scope, fresh))


def random_body(rng: random.Random, depth: int, scope: list):
    if depth == 0 or rng.random() < 0.15:
        if rng.random() < 0.6:
            return ("var", rng.choice(scope))
        return rng.choice([P, Q, ("nap", "p"), ("nap", "q")])
    if rng.random() < 0.5:
        return (rng.choice(["dia", "box"]), random_body(rng, depth - 1, scope))
    return (rng.choice(["and", "or"]), random_body(rng, depth - 1, scope), random_body(rng, depth - 1, scope))


def random_alternating(rng: random.Random):
    """sigma1 X. (g1 op sigma2 Y. (g2 op ... body)), with the signs alternating."""
    k = rng.randint(2, 3)
    signs = (["mu", "nu"] if rng.random() < 0.5 else ["nu", "mu"]) * 2
    names = ["X", "Y", "W"][:k]
    f = random_body(rng, 4, names)
    for i in range(k - 1, -1, -1):
        if i < k - 1:
            f = (rng.choice(["and", "or"]), random_body(rng, 2, names[: i + 1]), f)
        f = (signs[i], names[i], f)
    return f


# ---------------------------------------------------------------- the worked example

EX_STATES = [0, 1, 2, 3]
EX_SUCC = {0: [1, 2], 1: [0], 2: [3], 3: [3]}
EX_LABEL = {0: set(), 1: {"p"}, 2: {"p"}, 3: set()}
# "some path visits p infinitely often", E GF p, of alternation depth 2
GF_P = ("nu", "X", ("mu", "Y", ("or", ("and", P, ("dia", ("var", "X"))), ("dia", ("var", "Y")))))
# E[p U E[q U r]]: two least fixed points, one inside the other
EU_IN = ("mu", "Y", ("or", ("ap", "r"), ("and", Q, ("dia", ("var", "Y")))))
NESTED_EU = ("mu", "X", ("or", EU_IN, ("and", P, ("dia", ("var", "X")))))
CHAIN = {0: [1], 1: [2], 2: [3], 3: [4], 4: [5], 5: [5]}
CHAIN_LABEL = {0: {"p"}, 1: {"p"}, 2: {"p"}, 3: {"q"}, 4: {"q"}, 5: {"r"}}


def test_worked_example() -> None:
    s, n, lb = EX_STATES, EX_SUCC, EX_LABEL
    assert alternation_depth(GF_P) == 2 and nesting_depth(GF_P) == 2
    assert evaluate(s, n, lb, GF_P, reuse=True) == ({0, 1}, 12)
    assert evaluate(s, n, lb, GF_P, reuse=False) == ({0, 1}, 12)
    assert alternation_depth(NESTED_EU) == 1 and nesting_depth(NESTED_EU) == 2
    six = list(range(6))
    assert evaluate(six, CHAIN, CHAIN_LABEL, NESTED_EU, reuse=True) == (set(six), 13)
    assert evaluate(six, CHAIN, CHAIN_LABEL, NESTED_EU, reuse=False) == (set(six), 25)


# ---------------------------------------------------------------- edge cases


def test_rejects_bad_formulas() -> None:
    with pytest.raises(ValueError):
        emerson_lei([0], {0: [0]}, {0: set()}, ("mu", "X", ("nu", "X", ("var", "X"))))
    with pytest.raises(ValueError):
        emerson_lei([0], {0: [0]}, {0: set()}, ("var", "X"))


def test_trivial_fixed_points() -> None:
    states, succ, label = [0, 1], {0: [1], 1: [1]}, {0: {"p"}, 1: set()}
    assert emerson_lei(states, succ, label, ("mu", "X", ("var", "X"))) == set()
    assert emerson_lei(states, succ, label, ("nu", "X", ("var", "X"))) == {0, 1}
    assert emerson_lei(states, succ, label, ("nu", "X", ("and", P, ("box", ("var", "X"))))) == set()
    assert fixpoints(("mu", "X", ("nu", "Y", ("var", "X"))))["X"][2] == ["Y"]


# ---------------------------------------------------------------- against the references


def test_ctl_fragment_against_ctl_algorithm() -> None:
    rng = random.Random(1986)
    for _ in range(400):
        states, succ, label = random_structure(rng, rng.randint(1, 7))
        phi = random_ctl(rng, 3)
        mu = to_mu(phi, Fresh())
        expected = ctl_sat(states, succ, label, phi)
        assert emerson_lei(states, succ, label, mu) == expected, (succ, label, phi)
        assert naive_iteration(states, succ, label, mu) == expected


def test_random_against_tarski() -> None:
    rng = random.Random(1928)
    for _ in range(250):
        states, succ, label = random_structure(rng, rng.randint(1, 4))
        phi = random_mu(rng, 5, [], Fresh())
        if nesting_depth(phi) > 3:
            continue
        expected = tarski(states, succ, label, phi)
        assert emerson_lei(states, succ, label, phi) == expected, (succ, label, phi)
        assert naive_iteration(states, succ, label, phi) == expected


def test_naive_against_emerson_lei_and_the_bounds() -> None:
    rng = random.Random(1998)
    for _ in range(400):
        states, succ, label = random_structure(rng, rng.randint(1, 8))
        phi = random_mu(rng, 7, [], Fresh())
        el, el_count = evaluate(states, succ, label, phi, reuse=True)
        nv, nv_count = evaluate(states, succ, label, phi, reuse=False)
        assert el == nv
        k = len(fixpoints(phi))
        d, q, n = alternation_depth(phi), nesting_depth(phi), len(states)
        assert el_count <= k * (k + 1) ** d * n**d
        assert nv_count <= k * (n + 1) ** q


def test_alternating_formulas_against_naive() -> None:
    rng = random.Random(2017)
    for _ in range(4000):
        states, succ, label = random_structure(rng, rng.randint(3, 8))
        phi = random_alternating(rng)
        assert emerson_lei(states, succ, label, phi) == naive_iteration(states, succ, label, phi), (succ, label, phi)


def test_reset_of_the_opposite_sign_is_needed() -> None:
    # Without the reset of Y when X shrinks, Y would keep the cycle at 3, which
    # is a fixed point of <>Y but not the least one.
    states, succ, label = [2, 3, 4], {2: [4], 3: [3, 2], 4: [4]}, {2: {"p"}, 3: set(), 4: set()}
    assert emerson_lei(states, succ, label, GF_P) == set()
    assert tarski(states, succ, label, GF_P) == set()


def test_fair_eg_by_the_emerson_lei_formula() -> None:
    # E_f G p = nu Z. p and AND_i <> E[p U (Z and f_i)], checked against fair SCCs by brute force.
    rng = random.Random(1987)
    for _ in range(200):
        n = rng.randint(1, 6)
        states = list(range(n))
        succ = {s: sorted(set(rng.choice(states) for _ in range(rng.randint(1, 3)))) for s in states}
        label = {s: {a for a in ("p", "f1", "f2") if rng.random() < 0.5} for s in states}
        body = P
        for i, f in enumerate(("f1", "f2")):
            y = f"Y{i}"
            until = ("mu", y, ("or", ("and", ("var", "Z"), ("ap", f)), ("and", P, ("dia", ("var", y)))))
            body = ("and", body, ("dia", until))
        formula = ("nu", "Z", body)
        a = {s for s in states if "p" in label[s]}
        good = set()
        for k in range(1, len(a) + 1):
            for c in itertools.combinations(sorted(a), k):
                cs = set(c)
                ok = True
                for s in cs:
                    seen, queue = set(), deque(t for t in succ[s] if t in cs)
                    while queue:
                        v = queue.popleft()
                        if v not in seen:
                            seen.add(v)
                            queue.extend(t for t in succ[v] if t in cs)
                    ok = ok and cs <= seen
                if ok and all(any(f in label[v] for v in cs) for f in ("f1", "f2")):
                    good |= cs
        expected = set()
        for s in a:
            seen, queue = {s}, deque([s])
            while queue:
                v = queue.popleft()
                for t in succ[v]:
                    if t in a and t not in seen:
                        seen.add(t)
                        queue.append(t)
            if seen & good:
                expected.add(s)
        assert emerson_lei(states, succ, label, formula) == expected
