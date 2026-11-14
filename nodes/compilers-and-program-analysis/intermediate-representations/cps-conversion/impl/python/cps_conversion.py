# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cps-conversion/. The authors are listed in prov/J9VE11.jsonl.
"""Call-by-value CPS conversion of the toy lambda language of toylam.py.

The output is again a toylam term, so toylam.evaluate runs it. A function
fun x -> e becomes fun x -> fun k -> ..., a curried function that takes its
argument and then its continuation k. A call becomes a b k.

cps(e) is the one-pass translation of Danvy and Filinski: the translator
keeps the continuation of a non-tail expression as a Python function (the
meta-continuation) and builds object code only when it has a trivial term to
give it. So the output has no administrative redex.

plotkin(e, fresh) is Plotkin's translation, rule by rule. It makes many
redexes whose operator is a lambda of the translation itself; reducing them
(administrative_normal) gives the output of the one-pass translation, up to
the names of bound variables.
"""

import toylam


def var(x):
    return ("var", x)


def names(e):
    """Every variable name in e, bound or free."""
    tag = e[0]
    if tag == "var":
        return {e[1]}
    if tag in ("int", "bool"):
        return set()
    if tag == "lam":
        return {e[1]} | names(e[2])
    if tag == "app":
        return names(e[1]) | names(e[2])
    if tag == "let":
        return {e[1]} | names(e[2]) | names(e[3])
    if tag == "if":
        return names(e[1]) | names(e[2]) | names(e[3])
    if tag == "prim":
        return names(e[2]) | names(e[3])
    if tag == "fix":
        return {e[1], e[2]} | names(e[3])
    raise ValueError(f"not a term: {e!r}")


class Fresh:
    """Makes names that are new: not in avoid and not made before."""

    def __init__(self, avoid=()):
        self.avoid = set(avoid)
        self.n = 0
        self.source = set()  # the new names of the binders of the source term

    def __call__(self, base):
        while True:
            self.n += 1
            name = f"{base}{self.n}"
            if name not in self.avoid:
                self.avoid.add(name)
                return name

    def binder(self, x):
        y = self(x)
        self.source.add(y)
        return y


def rename_apart(e, fresh):
    """Give every binder of e its own new name. Free variables stay."""
    env = {}

    def bind(x):
        old = env.get(x)
        env[x] = fresh.binder(x)
        return env[x], old

    def unbind(x, old):
        if old is None:
            del env[x]
        else:
            env[x] = old

    def go(e):
        tag = e[0]
        if tag == "var":
            return var(env.get(e[1], e[1]))
        if tag in ("int", "bool"):
            return e
        if tag == "lam":
            y, old = bind(e[1])
            body = go(e[2])
            unbind(e[1], old)
            return ("lam", y, body)
        if tag == "app":
            return ("app", go(e[1]), go(e[2]))
        if tag == "let":
            rhs = go(e[2])
            y, old = bind(e[1])
            body = go(e[3])
            unbind(e[1], old)
            return ("let", y, rhs, body)
        if tag == "if":
            return ("if", go(e[1]), go(e[2]), go(e[3]))
        if tag == "prim":
            return ("prim", e[1], go(e[2]), go(e[3]))
        if tag == "fix":
            g, old_f = bind(e[1])
            y, old_x = bind(e[2])
            body = go(e[3])
            unbind(e[2], old_x)
            unbind(e[1], old_f)
            return ("fix", g, y, body)
        raise ValueError(f"not a term: {e!r}")

    return go(e)


def trivial(e):
    """Variables, constants and functions: terms that need no continuation."""
    return e[0] in ("var", "int", "bool", "lam", "fix")


# ------------------------------------------------------------ one pass


def cps(e, fresh=None):
    """The CPS program of the term e. It returns the value of e when run."""
    if fresh is None:
        fresh = Fresh(names(e))
    e = rename_apart(e, fresh)  # @line L1
    k0, a = fresh("k"), fresh("a")  # @line L2
    return ("let", k0, ("lam", a, var(a)), tail(e, var(k0), fresh))  # @line L3


def val(v, fresh):
    """The CPS image of a trivial term."""
    if v[0] in ("var", "int", "bool"):  # @line L4
        return v
    k = fresh("k")
    if v[0] == "lam":  # @line L5
        return ("lam", v[1], ("lam", k, tail(v[2], var(k), fresh)))
    return ("fix", v[1], v[2], ("lam", k, tail(v[3], var(k), fresh)))  # @line L6


def tail(e, k, fresh):
    """The CPS of e, which gives its value to k, a variable of the output."""
    tag = e[0]
    if trivial(e):  # @line L7
        return ("app", k, val(e, fresh))
    if tag == "app":  # @line L8
        return meta(e[1], lambda a: meta(e[2], lambda b: ("app", ("app", a, b), k), fresh), fresh)
    if tag == "let":  # @line L9
        return meta(e[2], lambda a: ("let", e[1], a, tail(e[3], k, fresh)), fresh)
    if tag == "if":  # @line L10
        return meta(e[1], lambda a: ("if", a, tail(e[2], k, fresh), tail(e[3], k, fresh)), fresh)
    return meta(e, lambda a: ("app", k, a), fresh)  # @line L11


def meta(e, kappa, fresh):
    """The CPS of e, which gives its value to kappa, a Python function from a
    trivial output term to an output term."""
    tag = e[0]
    if trivial(e):  # @line L12
        return kappa(val(e, fresh))
    if tag == "app":  # @line L13
        t = fresh("t")
        return meta(e[1], lambda a: meta(e[2], lambda b: ("app", ("app", a, b), ("lam", t, kappa(var(t)))), fresh), fresh)
    if tag == "let":  # @line L14
        return meta(e[2], lambda a: ("let", e[1], a, meta(e[3], kappa, fresh)), fresh)
    if tag == "if":  # @line L15
        j, t = fresh("j"), fresh("t")
        return meta(e[1], lambda a: ("let", j, ("lam", t, kappa(var(t))), ("if", a, tail(e[2], var(j), fresh), tail(e[3], var(j), fresh))), fresh)
    t = fresh("t")  # @line L16
    return meta(e[2], lambda a: meta(e[3], lambda b: ("let", t, ("prim", e[1], a, b), kappa(var(t))), fresh), fresh)


# ------------------------------------------------------------ Plotkin


def plotkin(e, fresh):
    """Plotkin's call-by-value translation of e: a function of a continuation."""
    tag = e[0]
    k = fresh("k")
    if tag in ("var", "int", "bool"):
        return ("lam", k, ("app", var(k), e))
    if tag == "lam":
        return ("lam", k, ("app", var(k), ("lam", e[1], plotkin(e[2], fresh))))
    if tag == "fix":
        return ("lam", k, ("app", var(k), ("fix", e[1], e[2], plotkin(e[3], fresh))))
    if tag == "app":
        a, b = fresh("v"), fresh("v")
        call = ("app", ("app", var(a), var(b)), var(k))
        return ("lam", k, ("app", plotkin(e[1], fresh), ("lam", a, ("app", plotkin(e[2], fresh), ("lam", b, call)))))
    if tag == "let":
        a = fresh("v")
        body = ("let", e[1], var(a), ("app", plotkin(e[3], fresh), var(k)))
        return ("lam", k, ("app", plotkin(e[2], fresh), ("lam", a, body)))
    if tag == "if":
        a = fresh("v")
        branch = ("if", var(a), ("app", plotkin(e[2], fresh), var(k)), ("app", plotkin(e[3], fresh), var(k)))
        return ("lam", k, ("app", plotkin(e[1], fresh), ("lam", a, branch)))
    if tag == "prim":
        a, b, t = fresh("v"), fresh("v"), fresh("t")
        op = ("let", t, ("prim", e[1], var(a), var(b)), ("app", var(k), var(t)))
        return ("lam", k, ("app", plotkin(e[2], fresh), ("lam", a, ("app", plotkin(e[3], fresh), ("lam", b, op)))))
    raise ValueError(f"not a term: {e!r}")


def plotkin_program(e, fresh=None):
    """Plotkin's translation of e applied to the identity continuation."""
    if fresh is None:
        fresh = Fresh(names(e))
    e = rename_apart(e, fresh)
    a = fresh("a")
    return ("app", plotkin(e, fresh), ("lam", a, var(a)))


def administrative_normal(e, source):
    """Reduce every redex (fun x -> b) a whose binder x is not in source, that
    is every redex that the translation made. The names of e must be distinct
    and each such x must occur at most once, as in Plotkin's output for terms
    without if."""
    tag = e[0]
    if tag == "app":
        f, a = administrative_normal(e[1], source), administrative_normal(e[2], source)
        if f[0] == "lam" and f[1] not in source:
            return administrative_normal(toylam.subst(f[2], f[1], a), source)
        return ("app", f, a)
    if tag == "lam":
        return ("lam", e[1], administrative_normal(e[2], source))
    if tag == "fix":
        return ("fix", e[1], e[2], administrative_normal(e[3], source))
    if tag == "let":
        return ("let", e[1], administrative_normal(e[2], source), administrative_normal(e[3], source))
    if tag == "if":
        return ("if",) + tuple(administrative_normal(x, source) for x in e[1:])
    if tag == "prim":
        return ("prim", e[1], administrative_normal(e[2], source), administrative_normal(e[3], source))
    return e


def administrative_redexes(e, source):
    """The number of redexes (fun x -> b) a in e with x not in source."""
    tag = e[0]
    here = 1 if tag == "app" and e[1][0] == "lam" and e[1][1] not in source else 0
    if tag in ("var", "int", "bool"):
        return 0
    if tag == "lam":
        return administrative_redexes(e[2], source)
    if tag == "fix":
        return administrative_redexes(e[3], source)
    parts = e[2:] if tag in ("prim", "let") else e[1:]
    return here + sum(administrative_redexes(x, source) for x in parts)


def alpha_equal(a, b):
    """True if a and b differ only in the names of bound variables."""

    def go(a, b, ea, eb, d):
        if a[0] != b[0]:
            return False
        tag = a[0]
        if tag == "var":
            ia, ib = ea.get(a[1]), eb.get(b[1])
            return ia == ib and (ia is not None or a[1] == b[1])
        if tag in ("int", "bool"):
            return a == b
        if tag == "lam":
            return go(a[2], b[2], {**ea, a[1]: d}, {**eb, b[1]: d}, d + 1)
        if tag == "fix":
            return go(a[3], b[3], {**ea, a[1]: d, a[2]: d + 1}, {**eb, b[1]: d, b[2]: d + 1}, d + 2)
        if tag == "let":
            return go(a[2], b[2], ea, eb, d) and go(a[3], b[3], {**ea, a[1]: d}, {**eb, b[1]: d}, d + 1)
        if tag == "prim":
            return a[1] == b[1] and go(a[2], b[2], ea, eb, d) and go(a[3], b[3], ea, eb, d)
        return all(go(x, y, ea, eb, d) for x, y in zip(a[1:], b[1:]))

    return go(a, b, {}, {}, 0)
