# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/urban-nominal-unification/. The authors are listed in prov/5H4NV6.jsonl.

import random

from urban_nominal_unification import act, subst, unify

ATOMS = ["a", "b", "c"]


def A(x):
    return ("atom", x)


def V(x, pi=()):
    return ("susp", tuple(pi), x)


def L(x, t):
    return ("abs", x, t)


def F(f, *ts):
    return ("fn", f, tuple(ts))


def debruijn(t, env=()):
    """A name-free form of a ground term; two ground terms are alpha-equivalent iff the forms are equal."""
    kind = t[0]
    if kind == "atom":
        return ("bound", env.index(t[1])) if t[1] in env else ("free", t[1])
    if kind == "abs":
        return ("lam", debruijn(t[2], (t[1],) + env))
    if kind == "fn":
        return (t[1],) + tuple(debruijn(s, env) for s in t[2])
    raise ValueError("not a ground term")


def free_atoms(t):
    kind = t[0]
    if kind == "atom":
        return {t[1]}
    if kind == "abs":
        return free_atoms(t[2]) - {t[1]}
    if kind == "fn":
        return set().union(*(free_atoms(s) for s in t[2])) if t[2] else set()
    raise ValueError("not a ground term")


def alpha_eq(t, u):
    return debruijn(t) == debruijn(u)


def satisfies(theta, nabla):
    return all(a not in free_atoms(theta[x]) for a, x in nabla)


def rand_perm(rng):
    return tuple(tuple(rng.sample(ATOMS, 2)) for _ in range(rng.randint(0, 2)))


def rand_term(rng, depth, vars_):
    r = rng.random()
    if depth == 0 or r < 0.25:
        if vars_ and rng.random() < 0.5:
            return V(rng.choice(vars_), rand_perm(rng))
        return A(rng.choice(ATOMS)) if rng.random() < 0.8 else F("k")
    if r < 0.55:
        return L(rng.choice(ATOMS), rand_term(rng, depth - 1, vars_))
    if r < 0.75:
        return F("g", rand_term(rng, depth - 1, vars_))
    return F("f", rand_term(rng, depth - 1, vars_), rand_term(rng, depth - 1, vars_))


def rename(rng, t):
    """A random alpha-variant of a ground term."""
    kind = t[0]
    if kind == "abs":
        body = rename(rng, t[2])
        a = t[1]
        c = rng.choice(ATOMS + ["d", "e"])
        if c != a and c not in free_atoms(body):
            return L(c, act(((a, c),), body))
        return L(a, body)
    if kind == "fn":
        return F(t[1], *(rename(rng, s) for s in t[2]))
    return t


def ground_terms(size):
    """All ground terms with exactly `size` symbols over a, b, c, k, g/1, f/2 and abstraction."""
    if size == 1:
        return [A(x) for x in ATOMS] + [F("k")]
    out = [F("g", s) for s in ground_terms(size - 1)]
    out += [L(x, s) for x in ATOMS for s in ground_terms(size - 1)]
    for i in range(1, size - 1):
        out += [F("f", s, u) for s in ground_terms(i) for u in ground_terms(size - 1 - i)]
    return out


SMALL = [t for n in (1, 2, 3) for t in ground_terms(n)]


def test_examples() -> None:
    nabla, sigma = unify([(L("a", V("X")), L("b", V("Y")))])
    assert nabla == {("a", "Y")}
    assert sigma == {"X": V("Y", [("a", "b")])}
    assert unify([(L("a", A("a")), L("b", V("X")))]) == (set(), {"X": A("b")})
    assert unify([(L("a", V("X")), L("b", A("a")))]) is None
    assert unify([(V("X"), F("g", V("X")))]) is None
    assert unify([(V("X", [("a", "b")]), V("X"))]) == ({("a", "X"), ("b", "X")}, {})
    assert unify([(A("a"), A("b"))]) is None
    assert unify([], [("a", L("a", A("a")))]) == (set(), {})
    assert unify([], [("a", V("X", [("a", "b")]))]) == ({("b", "X")}, {})


def test_ground_alpha_equivalence() -> None:
    rng = random.Random(1)
    eq = 0
    for _ in range(3000):
        t = rand_term(rng, rng.randint(0, 4), [])
        u = rename(rng, t) if rng.random() < 0.5 else rand_term(rng, rng.randint(0, 4), [])
        res = unify([(t, u)])
        assert (res is not None) == alpha_eq(t, u)
        if res is not None:
            eq += 1
            assert res == (set(), {})
    assert eq > 1000


def check_solution(rng, s, u, nabla, sigma, vars_):
    """Each ground instance that meets nabla makes sigma(s) and sigma(u) alpha-equivalent."""
    seen = 0
    for _ in range(40):
        tau = {x: rand_term(rng, 2, []) for x in vars_}
        if satisfies(tau, nabla):
            seen += 1
            assert alpha_eq(subst(tau, subst(sigma, s)), subst(tau, subst(sigma, u)))
    return seen


def test_constructed_problems_are_solved_most_generally() -> None:
    rng = random.Random(2)
    vars_ = ["X", "Y"]
    for _ in range(1500):
        s = rand_term(rng, rng.randint(1, 4), vars_)
        theta = {x: rand_term(rng, 2, []) for x in vars_}
        u = rename(rng, subst(theta, s))
        pair = (s, u) if rng.random() < 0.5 else (u, s)
        res = unify([pair])
        assert res is not None
        nabla, sigma = res
        # theta is a solution, so it must be an instance of the result: theta meets nabla and theta o sigma = theta.
        assert satisfies(theta, nabla)
        for x, v in sigma.items():
            assert alpha_eq(subst(theta, v), theta[x])
        check_solution(rng, pair[0], pair[1], nabla, sigma, vars_)


def test_one_variable_against_brute_force() -> None:
    rng = random.Random(3)
    found = failed = 0
    for _ in range(300):
        s = rand_term(rng, rng.randint(1, 3), ["X"])
        u = rand_term(rng, rng.randint(1, 3), ["X"])
        res = unify([(s, u)])
        witness = next((w for w in SMALL if alpha_eq(subst({"X": w}, s), subst({"X": w}, u))), None)
        if witness is not None:
            found += 1
            assert res is not None
        if res is None:
            failed += 1
        else:
            check_solution(rng, s, u, res[0], res[1], ["X"])
            nabla, sigma = res
            if witness is not None and "X" not in sigma:
                assert satisfies({"X": witness}, nabla)
    assert found > 20 and failed > 20
