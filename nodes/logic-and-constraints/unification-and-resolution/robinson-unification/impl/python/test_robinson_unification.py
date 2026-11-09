# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robinson-unification/. The authors are listed in prov/JGY442.jsonl.

import itertools
import random

from robinson_unification import apply, robinson_unification

A, B = ("a",), ("b",)


def f(*args):
    return ("f", *args)


def g(*args):
    return ("g", *args)


def variables(t, acc=None):
    acc = set() if acc is None else acc
    stack = [t]
    while stack:
        u = stack.pop()
        if isinstance(u, str):
            acc.add(u)
        else:
            stack.extend(u[1:])
    return acc


def size(t):
    n, stack = 0, [t]
    while stack:
        u = stack.pop()
        n += 1
        if not isinstance(u, str):
            stack.extend(u[1:])
    return n


def match_all(pairs):
    """Return lam with p lam == q for every (p, q), or None (syntactic matching)."""
    lam, stack = {}, list(pairs)
    while stack:
        p, q = stack.pop()
        if isinstance(p, str):
            if lam.setdefault(p, q) != q:
                return None
        elif isinstance(q, str) or p[0] != q[0] or len(p) != len(q):
            return None
        else:
            stack.extend(zip(p[1:], q[1:]))
    return lam


def more_general(sigma, theta, xs):
    """True when theta = sigma lam on the variables xs, for some lam."""
    return match_all([(sigma.get(x, x), theta.get(x, x)) for x in xs]) is not None


def ground_terms(depth):
    terms = [A, B]
    for _ in range(depth):
        terms = [A, B] + [g(u) for u in terms] + [f(u, v) for u in terms for v in terms]
    return list(dict.fromkeys(terms))


GROUND1 = ground_terms(1)


def ground_unifiers(s, t):
    xs = sorted(variables(s) | variables(t))
    for vals in itertools.product(GROUND1, repeat=len(xs)):
        theta = dict(zip(xs, vals))
        if apply(s, theta) == apply(t, theta):
            yield theta


def reference_unify(s, t):
    """An independent unifier by recursive descent with eager substitution."""
    sigma, todo = {}, [(s, t)]
    while todo:
        u, v = todo.pop()
        u, v = apply(u, sigma), apply(v, sigma)
        if u == v:
            continue
        if not isinstance(u, str) and isinstance(v, str):
            u, v = v, u
        if isinstance(u, str):
            if u in variables(v):
                return None
            sigma = {y: apply(w, {u: v}) for y, w in sigma.items()}
            sigma[u] = v
        elif u[0] != v[0] or len(u) != len(v):
            return None
        else:
            todo.extend(zip(u[1:], v[1:]))
    return sigma


def check_mgu(s, t, sigma):
    xs = variables(s) | variables(t)
    assert apply(s, sigma) == apply(t, sigma)
    dom = {x for x, w in sigma.items() if w != x}
    rng = set()
    for x in dom:
        variables(sigma[x], rng)
    assert not dom & rng, "not idempotent"
    assert dom <= xs and rng <= xs
    for theta in ground_unifiers(s, t):
        assert more_general(sigma, theta, xs)


def random_term(rng, depth, xs=("x", "y", "z")):
    r = rng.random()
    if depth == 0 or r < 0.3:
        return rng.choice(xs) if rng.random() < 0.6 else rng.choice([A, B])
    if r < 0.55:
        return g(random_term(rng, depth - 1, xs))
    return f(random_term(rng, depth - 1, xs), random_term(rng, depth - 1, xs))


def test_example() -> None:
    s = f("x", g("y"), "y")
    t = f(g("z"), "w", A)
    sigma = robinson_unification(s, t)
    assert sigma == {"x": g("z"), "w": g(A), "y": A}
    check_mgu(s, t, sigma)


def test_edges() -> None:
    assert robinson_unification("x", "x") == {}
    assert robinson_unification(A, A) == {}
    assert robinson_unification(A, B) is None
    assert robinson_unification(f("x"), g("x")) is None
    assert robinson_unification(f("x"), f("x", "y")) is None
    assert robinson_unification("x", "y") == {"x": "y"}
    assert robinson_unification("x", f("x")) is None
    assert robinson_unification(f("x", "y"), f("y", g("x"))) is None
    assert robinson_unification(f("x", "x"), f(A, B)) is None


def test_occurs_check_cases() -> None:
    rng = random.Random(4417)
    for _ in range(300):
        x = rng.choice(["x", "y", "z"])
        inner = random_term(rng, 3)
        t = f(inner, x) if rng.random() < 0.5 else g(f(x, inner))
        assert robinson_unification(x, t) is None
        assert robinson_unification(f(x, A), f(t, A)) is None


def test_exponential_example_sizes() -> None:
    for n in range(1, 13):
        xs = [f"x{i}" for i in range(n + 1)]
        s = ("f", *xs[1:])
        t = ("f", *[g(xs[i - 1], xs[i - 1]) for i in range(1, n + 1)])
        sigma = robinson_unification(s, t)
        assert sigma is not None
        assert size(apply(s, sigma)) == 2 ** (n + 2) - n - 3
        assert size(sigma[f"x{n}"]) == 2 ** (n + 1) - 1


def test_random_against_reference_and_brute_force() -> None:
    rng = random.Random(2150)
    unifiable = 0
    for _ in range(600):
        s, t = random_term(rng, 3), random_term(rng, 3)
        sigma = robinson_unification(s, t)
        ref = reference_unify(s, t)
        assert (sigma is None) == (ref is None)
        if sigma is None:
            assert next(ground_unifiers(s, t), None) is None
            continue
        unifiable += 1
        check_mgu(s, t, sigma)
        xs = variables(s) | variables(t)
        assert more_general(sigma, ref, xs) and more_general(ref, sigma, xs)
    assert unifiable > 100
