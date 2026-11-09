# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/miller-pattern-unification/. The authors are listed in prov/6TZ7KA.jsonl.
"""Miller's pattern unification for simply typed lambda terms.

A type is a pair (args, base): args is a tuple of types and base is a string.
A term is in beta-normal eta-long form and is a triple (binders, head, args):
binders is a tuple of (name, type), head is ("b", name) for a bound variable,
("c", name) for a constant or ("m", name) for a unification variable.
A term is a pattern when each unification variable is applied to distinct
bound variables (each argument is the eta-long form of a bound variable).
"""

import itertools

I = ((), "i")
_ids = itertools.count()


class NotAPattern(ValueError):
    pass


class _Fail(Exception):
    pass


def arrow(*types):
    """arrow(A, B, C) is the type A -> B -> C."""
    *args, res = types
    return (tuple(args) + res[0], res[1])


def fresh(prefix):
    return f"{prefix}{next(_ids)}"


def eta(kind, name, ty):
    """The eta-long form of the atom (kind, name) of type ty."""
    bs = tuple((fresh("y"), a) for a in ty[0])
    return (bs, (kind, name), tuple(eta("b", y, a) for y, a in bs))


def rename(t, ren=None):
    ren = dict(ren or {})
    bs, h, args = t
    nbs = []
    for n, ty in bs:
        ren[n] = fresh("x")
        nbs.append((ren[n], ty))
    if h[0] == "b" and h[1] in ren:
        h = ("b", ren[h[1]])
    return (tuple(nbs), h, tuple(rename(a, ren) for a in args))


def subst(t, bsub, msub):
    """Replace bound variables (bsub) and unification variables (msub), and normalize."""
    bs, h, args = t
    new_args = tuple(subst(a, bsub, msub) for a in args)
    if h[0] == "b" and h[1] in bsub:
        body = apply(bsub[h[1]], new_args)
    elif h[0] == "m" and h[1] in msub:
        body = apply(msub[h[1]], new_args)
    else:
        return (bs, h, new_args)
    return (bs + body[0], body[1], body[2])


def apply(v, args):
    vbs, h, vargs = rename(v)
    k = len(args)
    return subst((vbs[k:], h, vargs), {vbs[j][0]: args[j] for j in range(k)}, {})


def instantiate(t, theta):
    return subst(t, {}, theta)


def canon(t, env=None):
    """A key that is equal for two terms exactly when they are alpha-equivalent."""
    env = dict(env or {})
    bs, h, args = t
    for n, _ in bs:
        env[n] = len(env)
    if h[0] == "b" and h[1] in env:
        h = ("b", env[h[1]])
    return (tuple(ty for _, ty in bs), h, tuple(canon(a, env) for a in args))


def occurs(f, t):
    return (t[1] == ("m", f)) or any(occurs(f, a) for a in t[2])


def align(ctx, s, t):
    bs, bt = s[0], t[0]
    sub = {bt[j][0]: eta("b", bs[j][0], bs[j][1]) for j in range(len(bs))}
    return ctx + bs, ((),) + s[1:], subst(((),) + t[1:], sub, {})


def bound_var(t):
    """The name x when t is the eta-long form of the bound variable x, else None."""
    bs, h, args = t
    if h[0] != "b" or h[1] in {n for n, _ in bs} or len(args) != len(bs):
        return None
    for (n, _), a in zip(bs, args):
        if bound_var(a) != n:
            return None
    return h[1]


def pattern_args(t):
    xs = [bound_var(a) for a in t[2]]
    if None in xs or len(set(xs)) != len(xs):
        raise NotAPattern("a unification variable has an argument that is not a distinct bound variable")
    return xs


def check_pattern(t):
    if t[1][0] == "m":
        pattern_args(t)
    for a in t[2]:
        check_pattern(a)


def unify(pairs, sig):
    """A most general unifier of the pattern pairs, or None when there is no unifier.

    pairs is a list of (s, t), two closed patterns of the same type; sig maps each
    unification variable to its type. New variables get their types in sig.
    The result maps each unification variable that it binds to a closed term,
    and no value holds a variable that the result binds. Raises NotAPattern
    when an input is not a pattern.
    """
    for s, t in pairs:
        check_pattern(s)
        check_pattern(t)
    theta = {}  # @line L1

    def bind(f, value):
        rho = {f: value}
        for g in list(theta):
            theta[g] = instantiate(theta[g], rho)
        theta[f] = value

    def lam_h(fty, keep, h):
        """lambda w1 ... wn. H(w_j for j in keep), with H new."""
        ws = tuple((fresh("w"), a) for a in fty[0])
        sig[h] = (tuple(fty[0][j] for j in keep), fty[1])
        return (ws, ("m", h), tuple(eta("b", ws[j][0], ws[j][1]) for j in keep))

    def prune(t, allowed):
        bs, h, args = t
        allowed = allowed | {n for n, _ in bs}
        if h[0] == "m":  # @line L15
            if h[1] in theta:
                body = instantiate(((), h, args), theta)
                return prune((bs + body[0], body[1], body[2]), allowed - {n for n, _ in bs})
            ws = pattern_args(t)
            keep = [j for j, w in enumerate(ws) if w in allowed]  # @line L16
            if len(keep) < len(ws):
                new = fresh("H")
                bind(h[1], lam_h(sig[h[1]], keep, new))  # @line L17
                return (bs, ("m", new), tuple(args[j] for j in keep))
            return t  # @line L18
        if h[0] == "b" and h[1] not in allowed:
            raise _Fail  # @line L19
        return (bs, h, tuple(prune(a, allowed) for a in args))  # @line L20

    work = [align((), s, t) for s, t in pairs]
    try:
        while work:  # @line L2
            ctx, s, t = work.pop()
            s, t = instantiate(s, theta), instantiate(t, theta)  # @line L3
            fs, ft = s[1][0] == "m", t[1][0] == "m"
            if fs and ft:
                f, g = s[1][1], t[1][1]
                ys, zs = pattern_args(s), pattern_args(t)
                if f == g:  # @line L4
                    if ys != zs:
                        keep = [j for j in range(len(ys)) if ys[j] == zs[j]]
                        bind(f, lam_h(sig[f], keep, fresh("H")))  # @line L5
                else:
                    common = [y for y in ys if y in zs]  # @line L6
                    h = fresh("H")
                    bind(f, lam_h(sig[f], [ys.index(y) for y in common], h))
                    bind(g, lam_h(sig[g], [zs.index(y) for y in common], h))  # @line L7
            elif fs or ft:  # @line L8
                if ft:
                    s, t = t, s
                f = s[1][1]
                ys = pattern_args(s)
                if occurs(f, t):
                    return None  # @line L9
                t = instantiate(prune(t, set(ys)), theta)  # @line L10
                ws = tuple((fresh("w"), a) for a in sig[f][0])
                body = subst(t, {y: eta("b", w, a) for y, (w, a) in zip(ys, ws)}, {})
                bind(f, (ws, body[1], body[2]))  # @line L11
            elif s[1] != t[1]:
                return None  # @line L12
            else:
                for a, b in zip(s[2], t[2]):
                    work.append(align(ctx, a, b))  # @line L13
    except _Fail:
        return None
    return theta  # @line L14
