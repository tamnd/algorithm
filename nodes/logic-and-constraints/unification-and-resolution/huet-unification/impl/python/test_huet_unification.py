# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/huet-unification/. The authors are listed in prov/XZKWT3.jsonl.

import random

from huet_unification import unify


def apply(sigma, t):
    if isinstance(t, str):
        return apply(sigma, sigma[t]) if t in sigma and sigma[t] != t else t
    return (t[0],) + tuple(apply(sigma, a) for a in t[1:])


def occurs(x, t):
    return t == x if isinstance(t, str) else any(occurs(x, a) for a in t[1:])


def robinson(s, t):
    """A reference unifier: the classic recursive algorithm with an occurs check, on trees."""
    sigma = {}
    stack = [(s, t)]
    while stack:
        a, b = stack.pop()
        a, b = apply(sigma, a), apply(sigma, b)
        if a == b:
            continue
        if isinstance(b, str) and not isinstance(a, str):
            a, b = b, a
        if isinstance(a, str):
            if occurs(a, b):
                return None
            sigma = {x: apply({a: b}, v) for x, v in sigma.items()}
            sigma[a] = b
        elif a[0] != b[0] or len(a) != len(b):
            return None
        else:
            stack.extend(zip(a[1:], b[1:]))
    return sigma


def variables(t, out=None):
    out = set() if out is None else out
    if isinstance(t, str):
        out.add(t)
    else:
        for a in t[1:]:
            variables(a, out)
    return out


def check_mgu(s, t, sigma, rho):
    """sigma unifies s and t, and sigma and rho are instances of each other (both are idempotent mgus)."""
    assert apply(sigma, s) == apply(sigma, t)
    for x in variables(s) | variables(t):
        assert apply(sigma, apply(rho, x)) == apply(sigma, x)
        assert apply(rho, apply(sigma, x)) == apply(rho, x)


def test_simple() -> None:
    s = ("f", "X", ("g", "Y"))
    t = ("f", ("g", "Z"), "X")
    sigma = unify(s, t)
    assert apply(sigma, s) == apply(sigma, t)
    check_mgu(s, t, sigma, robinson(s, t))


def test_clash_and_occurs() -> None:
    assert unify(("f", "X"), ("g", "X")) is None
    assert unify("X", ("f", "X")) is None
    assert unify(("f", "X", "Y"), ("f", "Y", ("g", "X"))) is None
    assert unify(("a",), ("a",)) == {}
    assert unify("X", "X") == {}


def test_exponential_tree_small_dag() -> None:
    n = 12
    s = ("h",) + tuple(f"X{i}" for i in range(1, n + 1))
    t = ("h",) + tuple(("f", f"X{i}", f"X{i}") for i in range(n))
    sigma = unify(s, t)
    assert sigma is not None
    value = sigma[f"X{n}"]

    def size(u):
        return 1 if isinstance(u, str) else 1 + sum(size(a) for a in u[1:])

    assert size(value) == 2 ** (n + 1) - 1
    assert apply(sigma, s) == apply(sigma, t)


def rand_term(rng, depth, vars_):
    if depth == 0 or rng.random() < 0.3:
        return rng.choice(vars_) if rng.random() < 0.7 else (rng.choice("ab"),)
    f = rng.choice(["f", "g", "h"])
    arity = {"f": 2, "g": 1, "h": 3}[f]
    return (f,) + tuple(rand_term(rng, depth - 1, vars_) for _ in range(arity))


def test_random_against_robinson() -> None:
    rng = random.Random(3)
    agree = fail = 0
    for _ in range(3000):
        vars_ = ["X", "Y", "Z", "W"][: rng.randint(1, 4)]
        s = rand_term(rng, rng.randint(0, 4), vars_)
        t = rand_term(rng, rng.randint(0, 4), vars_)
        if rng.random() < 0.3:
            th = {v: rand_term(rng, 2, ["U", "V"]) for v in vars_}
            t = apply(th, s)
        sigma, rho = unify(s, t), robinson(s, t)
        assert (sigma is None) == (rho is None)
        if sigma is None:
            fail += 1
        else:
            agree += 1
            check_mgu(s, t, sigma, rho)
    assert agree > 300 and fail > 300
