# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/martelli-montanari-unification/. The authors are listed in prov/RV98XJ.jsonl.

import itertools
import random

from martelli_montanari_unification import apply, martelli_montanari_unification, unify_union_find

A, B = ("a",), ("b",)


def f(*args):
    return ("f", *args)


def g(*args):
    return ("g", *args)


def h(*args):
    return ("h", *args)


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
    return match_all([(sigma.get(x, x), theta.get(x, x)) for x in xs]) is not None


def ground_terms(depth):
    terms = [A, B]
    for _ in range(depth):
        terms = [A, B] + [g(u) for u in terms] + [f(u, v) for u in terms for v in terms]
    return list(dict.fromkeys(terms))


GROUND1 = ground_terms(1)


def ground_unifiers(eqs):
    xs = sorted(set().union(*[variables(s) | variables(t) for s, t in eqs]))
    for vals in itertools.product(GROUND1, repeat=len(xs)):
        theta = dict(zip(xs, vals))
        if all(apply(s, theta) == apply(t, theta) for s, t in eqs):
            yield theta


def reference_unify(s, t):
    """An independent unifier: Robinson-style disagreement search on the instances."""
    sigma = {}
    while True:
        u, v = apply(s, sigma), apply(t, sigma)
        stack, pair = [(u, v)], None
        while stack:
            p, q = stack.pop()
            if p == q:
                continue
            if isinstance(p, str) or isinstance(q, str) or p[0] != q[0] or len(p) != len(q):
                pair = (p, q)
                break
            stack.extend(reversed(list(zip(p[1:], q[1:]))))
        if pair is None:
            return sigma
        p, q = pair
        if not isinstance(p, str):
            p, q = q, p
        if not isinstance(p, str) or p in variables(q):
            return None
        sigma = {y: apply(w, {p: q}) for y, w in sigma.items()}
        sigma[p] = q


def check_mgu(eqs, sigma):
    xs = set().union(*[variables(s) | variables(t) for s, t in eqs])
    for s, t in eqs:
        assert apply(s, sigma) == apply(t, sigma)
    dom = {x for x, w in sigma.items() if w != x}
    rng = set()
    for x in dom:
        variables(sigma[x], rng)
    assert not dom & rng, "not idempotent"
    assert dom <= xs and rng <= xs
    for theta in ground_unifiers(eqs):
        assert more_general(sigma, theta, xs)


def random_term(rng, depth, xs=("x", "y", "z")):
    r = rng.random()
    if depth == 0 or r < 0.3:
        return rng.choice(xs) if rng.random() < 0.6 else rng.choice([A, B])
    if r < 0.55:
        return g(random_term(rng, depth - 1, xs))
    return f(random_term(rng, depth - 1, xs), random_term(rng, depth - 1, xs))


def test_example() -> None:
    eqs = [(g("x2"), "x1"), (f("x1", h("x1"), "x2"), f(g("x3"), "x4", "x3"))]
    sigma = martelli_montanari_unification(eqs)
    assert sigma == {"x1": g("x3"), "x2": "x3", "x4": h(g("x3"))}
    check_mgu(eqs, sigma)
    s = f(g("x2"), f("x1", h("x1"), "x2"))
    t = f("x1", f(g("x3"), "x4", "x3"))
    assert unify_union_find(s, t) is not None
    assert more_general(unify_union_find(s, t), sigma, {"x1", "x2", "x3", "x4"})


def test_edges() -> None:
    for unify in (lambda s, t: martelli_montanari_unification([(s, t)]), unify_union_find):
        assert unify("x", "x") == {}
        assert unify(A, A) == {}
        assert unify(A, B) is None
        assert unify(f("x"), g("x")) is None
        assert unify(f("x"), f("x", "y")) is None
        assert unify("x", f("x")) is None
        assert unify(f("x", "y"), f("y", g("x"))) is None
        assert unify(f("x", "x"), f(A, B)) is None
        assert unify(f("x", A), f(B, "y")) == {"x": B, "y": A}
    assert martelli_montanari_unification([]) == {}


def test_occurs_check_cases() -> None:
    rng = random.Random(4417)
    for _ in range(300):
        x = rng.choice(["x", "y", "z"])
        inner = random_term(rng, 3)
        t = f(inner, x) if rng.random() < 0.5 else g(f(x, inner))
        assert martelli_montanari_unification([(x, t)]) is None
        assert unify_union_find(f(x, A), f(t, A)) is None
    # A cycle through two variables is found only by the final check.
    assert unify_union_find(f("x", "y"), f(g("y"), g("x"))) is None
    assert martelli_montanari_unification([("x", g("y")), ("y", g("x"))]) is None


def test_exponential_example() -> None:
    for n in range(1, 11):
        xs = [f"x{i}" for i in range(n + 1)]
        s = ("f", *xs[1:])
        t = ("f", *[g(xs[i - 1], xs[i - 1]) for i in range(1, n + 1)])
        a = martelli_montanari_unification([(s, t)])
        b = unify_union_find(s, t)
        assert a == b
        assert size(apply(s, a)) == 2 ** (n + 2) - n - 3


def test_random_against_reference_and_brute_force() -> None:
    rng = random.Random(2150)
    unifiable = 0
    for _ in range(600):
        s, t = random_term(rng, 3), random_term(rng, 3)
        xs = variables(s) | variables(t)
        sigma = martelli_montanari_unification([(s, t)])
        uf = unify_union_find(s, t)
        ref = reference_unify(s, t)
        assert (sigma is None) == (ref is None) == (uf is None)
        if sigma is None:
            assert next(ground_unifiers([(s, t)]), None) is None
            continue
        unifiable += 1
        check_mgu([(s, t)], sigma)
        check_mgu([(s, t)], uf)
        for other in (ref, uf):
            assert more_general(sigma, other, xs) and more_general(other, sigma, xs)
    assert unifiable > 100


def test_random_systems() -> None:
    rng = random.Random(77)
    for _ in range(300):
        eqs = [(random_term(rng, 2), random_term(rng, 2)) for _ in range(rng.randint(1, 3))]
        sigma = martelli_montanari_unification(eqs)
        combined = martelli_montanari_unification([(("e", *[s for s, _ in eqs]), ("e", *[t for _, t in eqs]))])
        assert (sigma is None) == (combined is None)
        if sigma is None:
            assert next(ground_unifiers(eqs), None) is None
        else:
            check_mgu(eqs, sigma)
