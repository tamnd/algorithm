# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algorithm-w/. The authors are listed in prov/BA10YT.jsonl.
"""Algorithm W of Damas and Milner on the toy lambda language of toylam.py.

W(env, e) returns a pair (S, t): a substitution S and a type t with
S(env) |- e : t. A substitution is a dict from type variable numbers to
types. A type scheme is ("forall", vars, t) with vars a tuple of numbers.
infer(e) returns the principal type of a closed term, or raises TypeErrorHM.
"""

from toylam import normalize_type

INT = ("int",)
BOOL = ("bool",)


class TypeErrorHM(Exception):
    """The term has no type."""


class Fresh:
    """A supply of type variables that were never used before."""

    def __init__(self):
        self.n = 0

    def __call__(self):
        self.n += 1
        return ("tv", self.n - 1)


def fun(a, b):
    return ("fun", a, b)


def apply(s, t):
    """The type t with the substitution s applied."""
    if not s:
        return t
    tag = t[0]
    if tag == "tv":
        return s.get(t[1], t)
    if tag == "fun":
        return ("fun", apply(s, t[1]), apply(s, t[2]))
    return t


def apply_scheme(s, sc):
    bound = sc[1]
    inner = {v: u for v, u in s.items() if v not in bound}
    return ("forall", bound, apply(inner, sc[2]))


def apply_env(s, env):
    if not s:
        return env
    return {x: apply_scheme(s, sc) for x, sc in env.items()}


def compose(s2, s1):
    """The substitution s2 after s1: apply(compose(s2, s1), t) == apply(s2, apply(s1, t))."""
    out = {v: apply(s2, t) for v, t in s1.items()}
    for v, t in s2.items():
        if v not in out:
            out[v] = t
    return out


def ftv(t):
    tag = t[0]
    if tag == "tv":
        return {t[1]}
    if tag == "fun":
        return ftv(t[1]) | ftv(t[2])
    return set()


def ftv_scheme(sc):
    return ftv(sc[2]) - set(sc[1])


def ftv_env(env):
    out = set()
    for sc in env.values():
        out |= ftv_scheme(sc)
    return out


def unify(t1, t2):
    """A most general unifier of t1 and t2 (Robinson), or TypeErrorHM."""
    if t1 == t2:
        return {}
    if t1[0] == "tv":
        return bind(t1[1], t2)
    if t2[0] == "tv":
        return bind(t2[1], t1)
    if t1[0] == "fun" and t2[0] == "fun":
        s1 = unify(t1[1], t2[1])
        s2 = unify(apply(s1, t1[2]), apply(s1, t2[2]))
        return compose(s2, s1)
    raise TypeErrorHM(f"cannot unify {t1} with {t2}")


def bind(v, t):
    if t == ("tv", v):
        return {}
    if v in ftv(t):
        raise TypeErrorHM("occurs check")
    return {v: t}


def instantiate(sc, fresh):
    """Replace the bound variables of the scheme by fresh variables."""
    return apply({v: fresh() for v in sc[1]}, sc[2])


def generalize(env, t):
    """Quantify the variables of t that are not free in env."""
    bound = tuple(sorted(ftv(t) - ftv_env(env)))
    return ("forall", bound, t)


def mono(t):
    return ("forall", (), t)


PRIM_TYPES = {"+": INT, "-": INT, "*": INT, "<": BOOL, "==": BOOL}


def w(env, e, fresh):
    """Algorithm W: returns (S, t) with apply_env(S, env) |- e : t."""
    tag = e[0]
    if tag == "var":  # @line L1
        if e[1] not in env:
            raise TypeErrorHM(f"unbound variable {e[1]}")
        return {}, instantiate(env[e[1]], fresh)  # @line L2
    if tag == "lam":  # @line L3
        a = fresh()
        s1, t1 = w({**env, e[1]: mono(a)}, e[2], fresh)  # @line L4
        return s1, fun(apply(s1, a), t1)  # @line L5
    if tag == "app":  # @line L6
        s1, t1 = w(env, e[1], fresh)
        s2, t2 = w(apply_env(s1, env), e[2], fresh)  # @line L7
        b = fresh()
        s3 = unify(apply(s2, t1), fun(t2, b))  # @line L8
        return compose(s3, compose(s2, s1)), apply(s3, b)  # @line L9
    if tag == "let":  # @line L10
        s1, t1 = w(env, e[2], fresh)
        env1 = apply_env(s1, env)
        sigma = generalize(env1, t1)  # @line L11
        s2, t2 = w({**env1, e[1]: sigma}, e[3], fresh)  # @line L12
        return compose(s2, s1), t2  # @line L13
    if tag == "fix":  # @line L14
        a, b = fresh(), fresh()
        s1, t1 = w({**env, e[1]: mono(fun(a, b)), e[2]: mono(a)}, e[3], fresh)
        s2 = unify(apply(s1, b), t1)  # @line L15
        s = compose(s2, s1)
        return s, apply(s, fun(a, b))
    if tag == "int":
        return {}, INT
    if tag == "bool":
        return {}, BOOL
    if tag == "if":
        s1, t1 = w(env, e[1], fresh)
        s = compose(unify(t1, BOOL), s1)
        s2, t2 = w(apply_env(s, env), e[2], fresh)
        s = compose(s2, s)
        s3, t3 = w(apply_env(s, env), e[3], fresh)
        s = compose(s3, s)
        s4 = unify(apply(s3, t2), t3)
        return compose(s4, s), apply(s4, t3)
    if tag == "prim":
        s1, t1 = w(env, e[2], fresh)
        s = compose(unify(t1, INT), s1)
        s2, t2 = w(apply_env(s, env), e[3], fresh)
        s = compose(s2, s)
        s3 = unify(t2, INT)
        return compose(s3, s), PRIM_TYPES[e[1]]
    raise ValueError(f"not a term: {e!r}")


def infer(e, env=None):
    """The principal type of e, with variables renamed to 0, 1, 2, ... Raises TypeErrorHM."""
    fresh = Fresh()
    s, t = w(dict(env or {}), e, fresh)
    return normalize_type(t)


def principal_type(e):
    """The principal type of the closed term e, or None if e has no type."""
    try:
        return infer(e)
    except TypeErrorHM:
        return None
