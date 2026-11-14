# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algorithm-j/. The authors are listed in prov/M228A9.jsonl.

import random

import pytest

import toylam as L
from algorithm_j import J, TypeErrorHM, dag_size, infer, principal_type


def V(x):
    return ("var", x)


def lam(x, e):
    return ("lam", x, e)


def app(a, b):
    return ("app", a, b)


def let(x, a, b):
    return ("let", x, a, b)


I = ("int", 1)
T = ("bool", True)
INT, BOOL = ("int",), ("bool",)
OPS = {"+": INT, "-": INT, "*": INT, "<": BOOL, "==": BOOL}


# ---------------------------------------------------------------- a small algorithm W
# W with explicit substitutions, written apart from J, to compare the two.


def apply(s, t):
    if t[0] == "tv":
        return apply(s, s[t[1]]) if t[1] in s else t
    if t[0] == "fun":
        return ("fun", apply(s, t[1]), apply(s, t[2]))
    return t


def unify_w(s, a, b):
    a, b = apply(s, a), apply(s, b)
    if a == b:
        return
    if b[0] == "tv":
        a, b = b, a
    if a[0] == "tv":
        if a[1] in L.type_vars(b):
            raise TypeErrorHM("occurs")
        s[a[1]] = b
    elif a[0] == "fun" and b[0] == "fun":
        unify_w(s, a[1], b[1])
        unify_w(s, a[2], b[2])
    else:
        raise TypeErrorHM("clash")


def reference_w(e):
    s, n = {}, [0]

    def new():
        n[0] += 1
        return ("tv", n[0])

    def env_vars(env):
        out = set()
        for bound, t in env.values():
            out |= set(L.type_vars(apply(s, t))) - set(bound)
        return out

    def go(env, e):
        tag = e[0]
        if tag == "var":
            if e[1] not in env:
                raise TypeErrorHM("unbound")
            bound, t = env[e[1]]
            m = {v: new() for v in bound}
            return L.rename_type(apply(s, t), {}) if not m else apply(m, apply(s, t))
        if tag == "lam":
            a = new()
            return ("fun", a, go({**env, e[1]: ((), a)}, e[2]))
        if tag == "app":
            t1, t2, b = go(env, e[1]), go(env, e[2]), new()
            unify_w(s, t1, ("fun", t2, b))
            return b
        if tag == "let":
            t1 = apply(s, go(env, e[2]))
            bound = tuple(v for v in L.type_vars(t1) if v not in env_vars(env))
            return go({**env, e[1]: (bound, t1)}, e[3])
        if tag == "fix":
            a, b = new(), new()
            unify_w(s, b, go({**env, e[1]: ((), ("fun", a, b)), e[2]: ((), a)}, e[3]))
            return ("fun", a, b)
        if tag == "int":
            return INT
        if tag == "bool":
            return BOOL
        if tag == "if":
            unify_w(s, go(env, e[1]), BOOL)
            t2, t3 = go(env, e[2]), go(env, e[3])
            unify_w(s, t2, t3)
            return t2
        if tag == "prim":
            unify_w(s, go(env, e[2]), INT)
            unify_w(s, go(env, e[3]), INT)
            return OPS[e[1]]
        raise ValueError(tag)

    try:
        return L.normalize_type(apply(s, go({}, e)))
    except TypeErrorHM:
        return None


# ---------------------------------------------------------------- the brute-force check
# let x = e1 in e2 becomes (fun u -> e2[x := e1]) e1, then the simple rules
# give equations, solved by plain unification. A target type has rigid
# variables ("rig", n). The term checks against the target if the equations
# plus "type of e = target" have a solution. No let and no J is involved.


def rename_apart(e, env, counter):
    def new(x):
        counter[0] += 1
        return f"{x}_{counter[0]}"

    tag = e[0]
    if tag == "var":
        return ("var", env.get(e[1], e[1]))
    if tag == "lam":
        x = new(e[1])
        return ("lam", x, rename_apart(e[2], {**env, e[1]: x}, counter))
    if tag == "let":
        x = new(e[1])
        return ("let", x, rename_apart(e[2], env, counter), rename_apart(e[3], {**env, e[1]: x}, counter))
    if tag == "fix":
        f, x = new(e[1]), new(e[2])
        return ("fix", f, x, rename_apart(e[3], {**env, e[1]: f, e[2]: x}, counter))
    if tag == "app":
        return ("app", rename_apart(e[1], env, counter), rename_apart(e[2], env, counter))
    if tag == "if":
        return ("if",) + tuple(rename_apart(a, env, counter) for a in e[1:])
    if tag == "prim":
        return ("prim", e[1], rename_apart(e[2], env, counter), rename_apart(e[3], env, counter))
    return e


def expand(e, sub):
    """Expand every let; sub maps let-bound names to their expanded definitions."""
    tag = e[0]
    if tag == "var":
        return sub.get(e[1], e)
    if tag == "let":
        e1 = expand(e[2], sub)
        return ("app", ("lam", "_unused", expand(e[3], {**sub, e[1]: e1})), e1)
    if tag == "lam":
        return ("lam", e[1], expand(e[2], sub))
    if tag == "fix":
        return ("fix", e[1], e[2], expand(e[3], sub))
    if tag == "app":
        return ("app", expand(e[1], sub), expand(e[2], sub))
    if tag == "if":
        return ("if",) + tuple(expand(a, sub) for a in e[1:])
    if tag == "prim":
        return ("prim", e[1], expand(e[2], sub), expand(e[3], sub))
    return e


def equations(e):
    eqs, n = [], [0]

    def new():
        n[0] += 1
        return ("tv", n[0])

    def go(env, e):
        tag = e[0]
        if tag == "var":
            return env[e[1]]
        if tag in ("int", "bool"):
            return (tag,)
        if tag == "lam":
            a = new()
            return ("fun", a, go({**env, e[1]: a}, e[2]))
        if tag == "app":
            r = new()
            eqs.append((go(env, e[1]), ("fun", go(env, e[2]), r)))
            return r
        if tag == "fix":
            a, b = new(), new()
            eqs.append((b, go({**env, e[1]: ("fun", a, b), e[2]: a}, e[3])))
            return ("fun", a, b)
        if tag == "if":
            eqs.append((go(env, e[1]), BOOL))
            t2 = go(env, e[2])
            eqs.append((t2, go(env, e[3])))
            return t2
        eqs.append((go(env, e[2]), INT))
        eqs.append((go(env, e[3]), INT))
        return OPS[e[1]]

    return go({}, e), eqs


def solve(eqs, s):
    s = dict(s)
    s_ok = {}
    try:
        for a, b in eqs:
            unify_w(s, a, b)
    except TypeErrorHM:
        return None
    s_ok.update(s)
    return s_ok


def rigid(t):
    if t[0] == "tv":
        return ("rig", t[1])
    if t[0] == "fun":
        return ("fun", rigid(t[1]), rigid(t[2]))
    return t


class Reference:
    def __init__(self, e):
        self.s = None
        if not L.free_vars(e):
            self.t, eqs = equations(expand(rename_apart(e, {}, [0]), {}))
            self.s = solve(eqs, {})

    def checks(self, target):
        return self.s is not None and solve([(self.t, rigid(target))], self.s) is not None


def is_instance(t, p):
    m = {}

    def go(t, p):
        if p[0] == "tv":
            return m.setdefault(p[1], t) == t
        if p[0] == "fun":
            return t[0] == "fun" and go(t[1], p[1]) and go(t[2], p[2])
        return t == p

    return go(t, p)


def all_types(size):
    by = {1: [INT, BOOL, ("tv", 0), ("tv", 1)]}
    for k in range(2, size + 1):
        by[k] = [("fun", x, y) for i in range(1, k - 1) for x in by[i] for y in by[k - 1 - i]]
    return [t for k in by for t in by[k]]


TYPES = all_types(5)


def random_terms(seed, count, depth):
    rng = random.Random(seed)
    return [L.random_term(rng, rng.randint(1, depth)) for _ in range(count)]


def nested_let(k):
    """let y0 = fun x -> x in let y1 = fun z -> z y0 y0 in ... in yk"""
    body = V(f"y{k}")
    for i in range(k, 0, -1):
        body = let(f"y{i}", lam("z", app(app(V("z"), V(f"y{i - 1}")), V(f"y{i - 1}"))), body)
    return let("y0", lam("x", V("x")), body)


def doubling(k):
    """let f0 = fun x -> fun z -> z x x in let f1 = fun y -> f0 (f0 y) in ... in fk"""
    body = V(f"f{k}")
    for i in range(k, 0, -1):
        body = let(f"f{i}", lam("y", app(V(f"f{i - 1}"), app(V(f"f{i - 1}"), V("y")))), body)
    return let("f0", lam("x", lam("z", app(app(V("z"), V("x")), V("x")))), body)


# ---------------------------------------------------------------- tests


@pytest.mark.parametrize("levels", [False, True])
def test_known_types(levels):
    S = lam("x", lam("y", lam("z", app(app(V("x"), V("z")), app(V("y"), V("z"))))))
    assert L.show_type(infer(S, levels)) == "(a -> b -> c) -> (a -> b) -> a -> c"
    assert L.show_type(infer(let("id", lam("x", V("x")), app(V("id"), V("id"))), levels)) == "a -> a"
    assert L.show_type(infer(lam("x", let("y", V("x"), V("y"))), levels)) == "a -> a"
    two_uses = let("id", lam("x", V("x")), ("if", app(V("id"), T), app(V("id"), I), ("int", 0)))
    assert infer(two_uses, levels) == INT


@pytest.mark.parametrize("levels", [False, True])
@pytest.mark.parametrize(
    "term",
    [
        lam("x", app(V("x"), V("x"))),
        app(I, I),
        lam("f", ("if", app(V("f"), T), app(V("f"), I), ("int", 0))),
        lam("x", let("y", V("x"), ("if", app(V("y"), T), app(V("y"), I), ("int", 0)))),
        V("free"),
    ],
)
def test_untypable(term, levels):
    with pytest.raises(TypeErrorHM):
        infer(term, levels)


def test_j_w_and_levels_agree_on_random_terms():
    seen = {True: 0, False: 0}
    for e in random_terms(21, 1500, 6):
        w = reference_w(e)
        assert principal_type(e) == w, L.show(e)
        assert principal_type(e, True) == w, L.show(e)
        seen[w is not None] += 1
    assert seen[True] >= 400 and seen[False] >= 400


def test_against_brute_force_enumeration_of_types():
    typable = 0
    for e in random_terms(22, 300, 5):
        p = principal_type(e, True)
        ref = Reference(e)
        assert (p is not None) == (ref.s is not None), L.show(e)
        if p is None:
            assert not any(ref.checks(t) for t in TYPES)
            continue
        typable += 1
        for t in TYPES:
            assert ref.checks(t) == is_instance(t, p), (L.show(e), L.show_type(t))
    assert typable >= 80


def test_typable_terms_do_not_get_stuck():
    for e in random_terms(23, 600, 6):
        if principal_type(e, True) is not None:
            assert L.evaluate(e, 2000)[0] != "stuck", L.show(e)


def test_nested_let_tree_and_dag_sizes():
    for k in range(0, 9):
        e = nested_let(k)
        t = infer(e, True)
        assert L.type_size(t) == 8 * 2**k - 5
        assert t == reference_w(e)
        # the copies made at each use of y(i-1) have new variables, so sharing
        # does not help here: the DAG is exponential too
        assert dag_size(e) == 6 * 2**k - 4


def test_doubling_family_is_small_as_a_dag_and_huge_as_a_tree():
    for k in range(0, 8):
        e = doubling(k)
        assert L.size(e) == 7 * k + 9
        assert dag_size(e) == 2 ** (k + 2) + 2
    sizes = [L.type_size(infer(doubling(k), True)) for k in range(3)]
    assert sizes == [9, 21, 93]


def test_union_by_rank_and_path_compression_keep_finds_short():
    st = J(levels=True)
    vs = [st.new() for _ in range(64)]
    for i in range(0, 64, 1):
        st.unify(vs[0], vs[i])
    assert max(st.rank.values()) <= 6
    root = st.find(vs[63])
    assert all(st.find(v) == root for v in vs)
