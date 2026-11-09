# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/miller-pattern-unification/. The authors are listed in prov/6TZ7KA.jsonl.

import functools
import itertools
import random

import pytest

from miller_pattern_unification import I, NotAPattern, arrow, canon, eta, fresh, instantiate, unify

II = arrow(I, I)
III = arrow(I, I, I)
CONSTS = {"a": I, "b": I, "f": II, "g": III}
SIG = {"F": III, "G": II}


def c(name, *args):
    return ((), ("c", name), tuple(args))


def m(name, *args):
    return ((), ("m", name), tuple(args))


def bv(name, *args):
    return ((), ("b", name), tuple(args))


def lam(names_types, body):
    return (tuple(names_types), body[1], body[2])


def xy(body):
    return lam([("x", I), ("y", I)], body)


def is_unifier(pairs, theta):
    """Both sides are equal up to alpha after instantiation; all terms are beta-normal and eta-long."""
    return all(canon(instantiate(s, theta)) == canon(instantiate(t, theta)) for s, t in pairs)


def gen(ctx, ty, n):
    """All closed eta-long terms of type ty with exactly n head symbols."""
    bs = tuple((fresh("x"), a) for a in ty[0])
    ctx2 = ctx + bs
    heads = [(("c", k), t) for k, t in CONSTS.items()] + [(("b", k), t) for k, t in ctx2]
    for head, hty in heads:
        if hty[1] != ty[1]:
            continue
        for args in gen_args(ctx2, hty[0], n - 1):
            yield (bs, head, args)


def gen_args(ctx, types, n):
    if not types:
        if n == 0:
            yield ()
        return
    for k in range(1, n - len(types) + 2):
        for first in gen(ctx, types[0], k):
            for rest in gen_args(ctx, types[1:], n - k):
                yield (first,) + rest


@functools.lru_cache(maxsize=None)
def cands():
    return {f: [t for n in range(1, 4) for t in gen((), ty, n)] for f, ty in SIG.items()}


def is_instance(sigma, sig, ground):
    """True when some rho gives rho(sigma(F)) == ground(F) for every F of SIG."""
    pairs = [(sigma.get(f, eta("m", f, SIG[f])), ground[f]) for f in SIG]
    rho = unify(pairs, dict(sig))
    return rho is not None and is_unifier(pairs, rho)


def check_against_brute_force(pairs):
    """Run the algorithm and compare it with all small ground solutions."""
    sig = dict(SIG)
    sigma = unify(pairs, sig)
    if sigma is not None:
        assert is_unifier(pairs, sigma)
    found = 0
    for values in itertools.product(*(cands()[f] for f in SIG)):
        ground = dict(zip(SIG, values))
        if is_unifier(pairs, ground):
            found += 1
            assert sigma is not None
            assert is_instance(sigma, sig, ground)
    return sigma, found


def test_swap_arguments() -> None:
    pairs = [(xy(m("F", bv("x"), bv("y"))), xy(m("F", bv("y"), bv("x"))))]
    sigma, found = check_against_brute_force(pairs)
    assert found > 0
    assert sigma["F"][1][0] == "m" and sigma["F"][2] == ()


def test_different_heads_keep_common_variables() -> None:
    pairs = [(xy(m("F", bv("x"), bv("y"))), xy(m("G", bv("y"))))]
    sigma, _ = check_against_brute_force(pairs)
    f, g = sigma["F"], sigma["G"]
    assert f[1] == g[1] and len(f[2]) == 1
    assert f[2][0][1] == ("b", f[0][1][0])


def test_prune() -> None:
    check_against_brute_force([(xy(m("G", bv("x"))), xy(c("g", bv("x"), m("F", bv("y"), bv("x")))))])
    check_against_brute_force([(xy(m("G", bv("y"))), xy(c("f", m("F", bv("x"), bv("y")))))])
    sigma, found = check_against_brute_force([(xy(m("G", bv("x"))), xy(c("f", m("F", bv("y"), bv("x")))))])
    f = sigma["F"]
    assert found > 0 and len(f[2]) == 1 and f[2][0][1] == ("b", f[0][1][0])


def test_failures() -> None:
    occurs = [(xy(m("G", bv("x"))), xy(c("f", m("G", bv("x")))))]
    assert check_against_brute_force(occurs) == (None, 0)
    escape = [(xy(m("G", bv("x"))), xy(bv("y")))]
    assert check_against_brute_force(escape) == (None, 0)
    clash = [(xy(c("f", m("G", bv("x")))), xy(c("g", bv("x"), bv("y"))))]
    assert unify(clash, dict(SIG)) is None


def test_higher_type_argument() -> None:
    sig = {"K": arrow(II, I)}
    arg = lam([("z", I)], bv("h", bv("z")))
    s = lam([("h", II)], m("K", arg))
    t = lam([("h", II)], bv("h", c("a")))
    theta = unify([(s, t)], sig)
    assert is_unifier([(s, t)], theta)
    assert canon(theta["K"]) == canon(lam([("k", II)], bv("k", c("a"))))


def test_not_a_pattern() -> None:
    with pytest.raises(NotAPattern):
        unify([(xy(m("F", bv("x"), bv("x"))), xy(c("a")))], dict(SIG))
    with pytest.raises(NotAPattern):
        unify([(xy(m("G", c("a"))), xy(c("a")))], dict(SIG))


def rand_term(rng, depth):
    r = rng.random()
    if depth == 0 or r < 0.3:
        return rng.choice([c("a"), c("b"), bv("x"), bv("y")])
    if r < 0.55:
        u, v = rng.choice([("x", "y"), ("y", "x")])
        return m("F", bv(u), bv(v))
    if r < 0.7:
        return m("G", bv(rng.choice("xy")))
    if r < 0.85:
        return c("f", rand_term(rng, depth - 1))
    return c("g", rand_term(rng, depth - 1), rand_term(rng, depth - 1))


def test_random_against_brute_force() -> None:
    rng = random.Random(11)
    solved = failed = 0
    for _ in range(60):
        s = rand_term(rng, 2)
        if rng.random() < 0.5:
            t = instantiate(s, {"G": rng.choice(cands()["G"])})
        else:
            t = rand_term(rng, 2)
        sigma, found = check_against_brute_force([(xy(s), xy(t))])
        if sigma is None:
            assert found == 0
            failed += 1
        else:
            solved += 1
    assert solved > 5 and failed > 5
