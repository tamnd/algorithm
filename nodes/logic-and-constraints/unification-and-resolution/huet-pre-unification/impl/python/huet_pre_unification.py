# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/huet-pre-unification/. The authors are listed in prov/29K6EF.jsonl.
"""Huet's pre-unification for simply typed lambda terms.

A type is a pair (args, base): args is a tuple of types and base is a string.
The base type i is ((), "i"), and A -> B is arrow(A, B).

A term is in beta-normal eta-long form and is a triple (binders, head, args):
binders is a tuple of (name, type), head is ("b", name) for a bound
variable, ("c", name) for a constant or ("m", name) for a unification
variable, and args is a tuple of terms. The head gets all the arguments
that its type asks for, so the body of a term always has a base type.

The search is a depth-first search with a depth bound. Call pre_unify with
the bounds 1, 2, 3, ... (iterative deepening) to get a fair search.
"""

import itertools

I = ((), "i")
_ids = itertools.count()


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
    """A copy of t with fresh names for all its binders."""
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
    """Beta-normal form of the term v applied to args (hereditary substitution)."""
    vbs, h, vargs = rename(v)
    k = len(args)
    sub = {vbs[j][0]: args[j] for j in range(k)}
    return subst((vbs[k:], h, vargs), sub, {})


def instantiate(t, theta):
    return subst(t, {}, theta)


def compose(theta, rho):
    """The substitution 'first theta, then rho'."""
    out = {f: instantiate(v, rho) for f, v in theta.items()}
    for f, v in rho.items():
        out.setdefault(f, v)
    return out


def canon(t, env=None):
    """A key that is equal for two terms exactly when they are alpha-equivalent."""
    env = dict(env or {})
    bs, h, args = t
    for n, _ in bs:
        env[n] = len(env)
    if h[0] == "b" and h[1] in env:
        h = ("b", env[h[1]])
    return (tuple(ty for _, ty in bs), h, tuple(canon(a, env) for a in args))


def metas(t, out=None):
    out = set() if out is None else out
    if t[1][0] == "m":
        out.add(t[1][1])
    for a in t[2]:
        metas(a, out)
    return out


def align(ctx, s, t):
    """Put s and t of the same type under common binders. Returns (ctx', body_s, body_t)."""
    bs, bt = s[0], t[0]
    sub = {bt[j][0]: eta("b", bs[j][0], bs[j][1]) for j in range(len(bs))}
    body_t = subst(((),) + t[1:], sub, {})
    return ctx + bs, ((),) + s[1:], body_t


def simplify(goals):
    """Decompose rigid-rigid pairs (SIMPL). Return (flex_rigid, flex_flex), or None on a clash."""
    work = list(goals)
    fr, ff = [], []
    while work:  # @line L12
        ctx, s, t = work.pop()
        fs, ft = s[1][0] == "m", t[1][0] == "m"
        if fs and ft:
            ff.append((ctx, s, t))
        elif fs:
            fr.append((ctx, s, t))
        elif ft:
            fr.append((ctx, t, s))  # @line L15
        elif s[1] != t[1]:
            return None  # @line L13
        else:
            for a, b in zip(s[2], t[2]):
                work.append(align(ctx, a, b))  # @line L14
    return fr, ff  # @line L16


def match(fty, a, sig):
    """The heads of the general bindings for a flex head of type fty and a rigid head a (MATCH)."""
    heads = []  # @line L17
    if a[0] == "c":  # @line L18
        heads.append((a, sig[a[1]]))  # @line L19
    for j, xt in enumerate(fty[0]):  # @line L20
        if xt[1] == fty[1]:
            heads.append((("p", j), None))  # @line L21
    return heads  # @line L22


def binding(fty, head, head_ty, sig):
    """The general binding lambda xs. head(H1(xs), ..., Hm(xs)) for a variable of type fty.

    head is ("c", name) for an imitation, or ("p", index) for the projection on x_index.
    New variables get their types in sig.
    """
    xs = tuple((fresh("x"), a) for a in fty[0])
    if head[0] == "p":
        head, head_ty = ("b", xs[head[1]][0]), xs[head[1]][1]
    hargs = []
    for sj in head_ty[0]:
        zs = tuple((fresh("z"), r) for r in sj[0])
        name = fresh("H")
        sig[name] = (tuple(a for _, a in xs) + sj[0], sj[1])
        args = tuple(eta("b", x, a) for x, a in xs + zs)
        hargs.append((zs, ("m", name), args))
    return (xs, head, tuple(hargs))


def pre_unify(pairs, sig, max_depth):
    """Yield (theta, flex_flex) for each pre-unifier at depth at most max_depth.

    pairs is a list of (s, t), two closed terms of the same type. sig maps each
    constant and each unification variable to its type. theta is restricted to
    the variables of the problem; flex_flex lists the pairs that are left.
    The types of the new variables are added to sig.
    """
    goals = [align((), s, t) for s, t in pairs]
    start = set()
    for s, t in pairs:
        metas(s, start)
        metas(t, start)
    stack = [(goals, {}, 0)]  # @line L1
    while stack:  # @line L2
        goals, theta, depth = stack.pop()  # @line L3
        res = simplify(goals)  # @line L4
        if res is None:
            continue  # @line L5
        fr, ff = res
        if not fr:  # @line L6
            yield {f: v for f, v in theta.items() if f in start}, ff  # @line L7
            continue  # @line L8
        if depth == max_depth:
            continue
        ctx, flex, rigid = fr[0]  # @line L9
        f = flex[1][1]
        fty = sig[f]
        for head, head_ty in reversed(match(fty, rigid[1], sig)):  # @line L10
            rho = {f: binding(fty, head, head_ty, sig)}
            new_goals = [(c, instantiate(s, rho), instantiate(t, rho)) for c, s, t in fr + ff]
            stack.append((new_goals, compose(theta, rho), depth + 1))  # @line L11


def complete(theta, flex_flex, sig):
    """Solve the flex-flex pairs: each flex head F becomes lambda xs. H_base (Huet's lemma)."""
    sig = dict(sig)
    rho, shared = {}, {}
    for _, s, t in flex_flex:
        for side in (s, t):
            f = side[1][1]
            if f in rho:
                continue
            ty = sig[f]
            if ty[1] not in shared:
                shared[ty[1]] = fresh("H")
                sig[shared[ty[1]]] = ((), ty[1])
            xs = tuple((fresh("x"), a) for a in ty[0])
            rho[f] = (xs, ("m", shared[ty[1]]), ())
    return compose(theta, rho)
