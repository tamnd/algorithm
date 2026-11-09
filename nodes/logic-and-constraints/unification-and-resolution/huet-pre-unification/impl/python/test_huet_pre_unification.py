# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/huet-pre-unification/. The authors are listed in prov/29K6EF.jsonl.

import itertools
import random

from huet_pre_unification import (
    I, align, arrow, binding, canon, complete, compose, eta, fresh, instantiate, pre_unify, simplify,
)

II = arrow(I, I)
III = arrow(I, I, I)
SIG = {"a": I, "b": I, "f": II, "g": III}


def c(name, *args):
    return ((), ("c", name), tuple(args))


def m(name, *args):
    return ((), ("m", name), tuple(args))


def lam(names_types, body):
    return (tuple(names_types), body[1], body[2])


def bv(name, *args):
    return ((), ("b", name), tuple(args))


def full(theta, sig):
    """theta extended with the identity on the variables of sig."""
    return {f: theta.get(f, eta("m", f, ty)) for f, ty in sig.items()}


def walk(ctx, s, t, ff):
    """Decompose; True when no clash and no flex-rigid pair is left."""
    fs, ft = s[1][0] == "m", t[1][0] == "m"
    if fs and ft:
        ff.append((s, t))
        return True
    if fs or ft or s[1] != t[1]:
        return False
    for x, y in zip(s[2], t[2]):
        ctx2, x2, y2 = align(ctx, x, y)
        if not walk(ctx2, x2, y2, ff):
            return False
    return True


def check_pre_unifier(pairs, theta):
    for s, t in pairs:
        ctx, x, y = align((), instantiate(s, theta), instantiate(t, theta))
        if not walk(ctx, x, y, []):
            return False
    return True


def check_unifier(pairs, theta):
    return all(canon(instantiate(s, theta)) == canon(instantiate(t, theta)) for s, t in pairs)


def results(pairs, sig, depth):
    out = []
    sig = dict(sig)
    for theta, ff in pre_unify(pairs, sig, depth):
        assert check_pre_unifier(pairs, theta)
        u = complete(theta, ff, sig)
        assert check_unifier(pairs, u)
        out.append(theta)
    return out


def gen(ctx, ty, n, consts):
    """All closed eta-long terms of type ty with exactly n head symbols."""
    bs = tuple((fresh("x"), a) for a in ty[0])
    ctx2 = ctx + bs
    heads = [(("c", k), t) for k, t in consts.items()] + [(("b", k), t) for k, t in ctx2]
    for head, hty in heads:
        if hty[1] != ty[1]:
            continue
        for args in gen_args(ctx2, hty[0], n - 1, consts):
            yield (bs, head, args)


def gen_args(ctx, types, n, consts):
    if not types:
        if n == 0:
            yield ()
        return
    for k in range(1, n - len(types) + 2):
        for first in gen(ctx, types[0], k, consts):
            for rest in gen_args(ctx, types[1:], n - k, consts):
                yield (first,) + rest


def small(ty, max_size, consts=SIG):
    return [t for n in range(1, max_size + 1) for t in gen((), ty, n, consts)]


def key(theta, names):
    """The values of theta for names, with the unification variables renamed by first use."""
    ren = {}

    def k(t, env):
        env = dict(env)
        bs, h, args = t
        for n, _ in bs:
            env[n] = len(env)
        if h[0] == "b":
            h = ("b", env[h[1]])
        elif h[0] == "m":
            h = ("m", ren.setdefault(h[1], len(ren)))
        return (tuple(ty for _, ty in bs), h, tuple(k(a, env) for a in args))

    return tuple(k(theta[f], {}) if f in theta else None for f in names)


def guided(pairs, sig, ground):
    """Follow the branch of the search tree that the unifier `ground` selects (Huet's completeness proof)."""
    sig = dict(sig)
    goals = [align((), s, t) for s, t in pairs]
    sigma, ext, depth = {}, dict(ground), 0
    while True:
        res = simplify(goals)
        assert res is not None
        fr, ff = res
        if not fr:
            break
        _, flex, _ = fr[0]
        f = flex[1][1]
        tf = ext[f]
        h = tf[1]
        if h[0] == "c":
            head, head_ty = h, SIG[h[1]]
        else:
            head, head_ty = ("p", [n for n, _ in tf[0]].index(h[1])), None
        val = binding(sig[f], head, head_ty, sig)
        for (zs, hh, _), w in zip(val[2], tf[2]):
            ext[hh[1]] = (tf[0] + w[0], w[1], w[2])
        rho = {f: val}
        goals = [(cx, instantiate(s, rho), instantiate(t, rho)) for cx, s, t in fr + ff]
        sigma = compose(sigma, rho)
        depth += 1
    for f in ground:
        assert canon(instantiate(sigma.get(f, eta("m", f, sig[f])), ext)) == canon(ground[f])
    return {f: v for f, v in sigma.items() if f in ground}, depth


def test_identity_or_constant() -> None:
    sig = {**SIG, "F": II}
    pairs = [(m("F", c("a")), c("a"))]
    got = results(pairs, sig, 5)
    shapes = sorted(canon(th["F"]) for th in got)
    want = sorted(canon(t) for t in [lam([("x", I)], bv("x")), lam([("x", I)], c("a"))])
    assert shapes == want


def test_four_solutions_of_g() -> None:
    sig = {**SIG, "F": II}
    pairs = [(m("F", c("a")), c("g", c("a"), c("a")))]
    got = results(pairs, sig, 6)
    assert len({canon(th["F"]) for th in got}) == 4
    for th in got:
        assert not any(t[1][0] == "m" for t in [th["F"]])


def test_flex_flex_is_left() -> None:
    sig = {**SIG, "F": II}
    pairs = [(m("F", c("a")), m("F", c("b")))]
    got = list(pre_unify(pairs, sig, 3))
    assert len(got) == 1
    theta, ff = got[0]
    assert theta == {} and len(ff) == 1
    u = complete(theta, ff, sig)
    assert check_unifier(pairs, u)
    assert u["F"][1][0] == "m" and u["F"][2] == ()


def test_third_order_finite() -> None:
    G = arrow(II, I)
    sig = {**SIG, "G": G}
    arg = lam([("u", I)], c("f", bv("u")))
    pairs = [(m("G", arg), c("f", c("f", c("a"))))]
    got = results(pairs, sig, 8)
    assert len({canon(th["G"]) for th in got}) == 4


def test_third_order_infinite_family() -> None:
    sig = {**SIG, "G": arrow(II, I)}
    ident = lam([("u", I)], bv("u"))
    pairs = [(m("G", ident), c("a"))]
    for d in range(1, 6):
        got = results(pairs, sig, d)
        assert len({canon(th["G"]) for th in got}) == d
    want = lam([("y", II)], bv("y", bv("y", c("a"))))
    assert canon(want) in {canon(th["G"]) for th in results(pairs, sig, 3)}


def test_no_solution() -> None:
    sig = {**SIG, "F": II}
    assert results([(m("F", c("a")), c("f", m("F", c("a"))))], sig, 7) == []
    assert results([(c("g", c("a"), m("F", c("a"))), c("g", c("b"), c("a")))], sig, 7) == []


def test_bound_variable_rigid_head() -> None:
    sig = {**SIG, "F": II}
    s = lam([("x", I)], m("F", bv("x")))
    t = lam([("y", I)], c("f", bv("y")))
    got = results([(s, t)], sig, 5)
    assert {canon(th["F"]) for th in got} == {canon(lam([("z", I)], c("f", bv("z"))))}


def test_completeness_against_brute_force() -> None:
    rng = random.Random(7)
    sig = {**SIG, "F": II, "G": II}
    cands = small(II, 3)
    shapes = [
        lambda: (m("F", c("a")), c("f", m("G", c("b")))),
        lambda: (m("F", m("G", c("a"))), m("G", m("F", c("a")))),
        lambda: (c("g", m("F", c("a")), m("G", c("b"))), c("g", m("G", c("a")), m("F", c("b")))),
        lambda: (m("F", c("f", c("a"))), c("f", m("F", c("a")))),
    ]
    for build in shapes:
        pairs = [build()]
        found = {key(th, ["F", "G"]) for th in results(pairs, sig, 6)}
        n = 0
        for vf, vg in itertools.product(cands, cands):
            ground = {"F": vf, "G": vg}
            if not check_unifier(pairs, ground):
                continue
            n += 1
            sigma, depth = guided(pairs, sig, ground)
            assert depth <= 6
            assert key(sigma, ["F", "G"]) in found
        assert n > 0
    for _ in range(25):
        th = {"F": rng.choice(cands), "G": rng.choice(cands)}
        s = c("g", m("F", c(rng.choice("ab"))), m("G", m("F", c(rng.choice("ab")))))
        pairs = [(s, instantiate(s, th))]
        found = {key(x, ["F", "G"]) for x in results(pairs, sig, 7)}
        for vf, vg in itertools.product(cands, cands):
            ground = {"F": vf, "G": vg}
            if check_unifier(pairs, ground):
                sigma, depth = guided(pairs, sig, ground)
                if depth <= 7:
                    assert key(sigma, ["F", "G"]) in found
