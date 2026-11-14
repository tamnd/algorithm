# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algorithm-w/. The authors are listed in prov/BA10YT.jsonl.

import random

import pytest

import toylam as L
from algorithm_w import TypeErrorHM, infer, principal_type


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


def parse_type(s):
    """Read a type such as "(a -> b) -> a -> b"; a, b, c, ... are variables 0, 1, 2, ..."""
    toks = s.replace("(", " ( ").replace(")", " ) ").replace("->", " -> ").split()
    pos = [0]

    def atom():
        t = toks[pos[0]]
        pos[0] += 1
        if t == "(":
            r = arrow()
            pos[0] += 1
            return r
        if t in ("int", "bool"):
            return (t,)
        return ("tv", ord(t) - ord("a"))

    def arrow():
        left = atom()
        if pos[0] < len(toks) and toks[pos[0]] == "->":
            pos[0] += 1
            return ("fun", left, arrow())
        return left

    return arrow()


# ---------------------------------------------------------------- the reference check
# The reference does not use W. It expands every let (let x = e1 in e2 becomes
# (fun u -> e2[x := e1]) e1, which also asks e1 to be typable), generates
# the equations of the simply typed rules, and solves them by plain
# unification. A target type is given with rigid variables ("rig", n). Then
# e checks against the target if the equations plus "type of e = target"
# have a solution.


def rename_apart(e, env=None, counter=None):
    """Give every binder a new unique name."""
    env = env or {}
    counter = counter if counter is not None else [0]

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


def open_subst(e, x, r):
    """e[x := r] for a term r with free variables; safe after rename_apart."""
    tag = e[0]
    if tag == "var":
        return r if e[1] == x else e
    if tag == "lam":
        return ("lam", e[1], open_subst(e[2], x, r))
    if tag == "let":
        return ("let", e[1], open_subst(e[2], x, r), open_subst(e[3], x, r))
    if tag == "fix":
        return ("fix", e[1], e[2], open_subst(e[3], x, r))
    if tag == "app":
        return ("app", open_subst(e[1], x, r), open_subst(e[2], x, r))
    if tag == "if":
        return ("if",) + tuple(open_subst(a, x, r) for a in e[1:])
    if tag == "prim":
        return ("prim", e[1], open_subst(e[2], x, r), open_subst(e[3], x, r))
    return e


def expand_lets(e):
    tag = e[0]
    if tag == "let":
        e1, e2 = expand_lets(e[2]), expand_lets(e[3])
        return ("app", ("lam", "_unused", open_subst(e2, e[1], e1)), e1)
    if tag == "lam":
        return ("lam", e[1], expand_lets(e[2]))
    if tag == "fix":
        return ("fix", e[1], e[2], expand_lets(e[3]))
    if tag == "app":
        return ("app", expand_lets(e[1]), expand_lets(e[2]))
    if tag == "if":
        return ("if",) + tuple(expand_lets(a) for a in e[1:])
    if tag == "prim":
        return ("prim", e[1], expand_lets(e[2]), expand_lets(e[3]))
    return e


def equations(e):
    """(t, eqs): the type of the let-free term e and the equations of the simple rules."""
    eqs, n = [], [0]

    def new():
        n[0] += 1
        return ("tv", n[0])

    def go(env, e):
        tag = e[0]
        if tag == "var":
            return env[e[1]]
        if tag == "int":
            return ("int",)
        if tag == "bool":
            return ("bool",)
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
            eqs.append((go(env, e[1]), ("bool",)))
            t2 = go(env, e[2])
            eqs.append((t2, go(env, e[3])))
            return t2
        if tag == "prim":
            eqs.append((go(env, e[2]), ("int",)))
            eqs.append((go(env, e[3]), ("int",)))
            return ("int",) if e[1] in "+-*" else ("bool",)
        raise ValueError(tag)

    return go({}, e), eqs


def walk(s, t):
    while t[0] == "tv" and t[1] in s:
        t = s[t[1]]
    return t


def full(s, t):
    t = walk(s, t)
    if t[0] == "fun":
        return ("fun", full(s, t[1]), full(s, t[2]))
    return t


def solve(eqs, s=None):
    """A solution of the equations as a triangular substitution, or None."""
    s = dict(s or {})
    work = list(eqs)
    while work:
        a, b = work.pop()
        a, b = walk(s, a), walk(s, b)
        if a == b:
            continue
        if b[0] == "tv":
            a, b = b, a
        if a[0] == "tv":
            if a[1] in L.type_vars(full(s, b)):
                return None
            s[a[1]] = b
        elif a[0] == "fun" and b[0] == "fun":
            work.append((a[1], b[1]))
            work.append((a[2], b[2]))
        else:
            return None
    return s


class Reference:
    def __init__(self, e):
        if L.free_vars(e):
            self.s = None  # an open term has no type in the empty context
            return
        self.t, eqs = equations(expand_lets(rename_apart(e)))
        self.s = solve(eqs)

    def typable(self):
        return self.s is not None

    def checks(self, target):
        """Does e have the type target? Variables of target are rigid."""
        if self.s is None:
            return False
        return solve([(self.t, rigid(target))], self.s) is not None


def rigid(t):
    if t[0] == "tv":
        return ("rig", t[1])
    if t[0] == "fun":
        return ("fun", rigid(t[1]), rigid(t[2]))
    return t


def is_instance(t, p):
    """Is the type t an instance of the type p? Variables of t are constants."""
    m = {}

    def go(t, p):
        if p[0] == "tv":
            if p[1] in m:
                return m[p[1]] == t
            m[p[1]] = t
            return True
        if p[0] == "fun":
            return t[0] == "fun" and go(t[1], p[1]) and go(t[2], p[2])
        return t == p

    return go(t, p)


def all_types(size):
    """Every type with at most size nodes over int, bool and the variables a, b."""
    by = {1: [("int",), ("bool",), ("tv", 0), ("tv", 1)]}
    for k in range(2, size + 1):
        by[k] = [("fun", x, y) for i in range(1, k - 1) for x in by[i] for y in by[k - 1 - i]]
    return [t for k in by for t in by[k]]


TYPES = all_types(5)


# ---------------------------------------------------------------- tests


@pytest.mark.parametrize(
    "term, expected",
    [
        (lam("x", V("x")), "a -> a"),
        (lam("x", lam("y", V("x"))), "a -> b -> a"),
        (lam("x", lam("y", lam("z", app(app(V("x"), V("z")), app(V("y"), V("z")))))), "(a -> b -> c) -> (a -> b) -> a -> c"),
        (lam("f", lam("g", lam("x", app(V("f"), app(V("g"), V("x")))))), "(a -> b) -> (c -> a) -> c -> b"),
        (let("id", lam("x", V("x")), app(V("id"), V("id"))), "a -> a"),
        (let("id", lam("x", V("x")), ("if", app(V("id"), T), app(V("id"), I), ("int", 0))), "int"),
        (lam("x", let("y", V("x"), V("y"))), "a -> a"),
        (("fix", "f", "n", ("if", ("prim", "<", V("n"), I), I, ("prim", "*", V("n"), app(V("f"), ("prim", "-", V("n"), I))))), "int -> int"),
        (let("k", lam("x", lam("y", V("x"))), app(app(V("k"), V("k")), I)), "a -> b -> a"),
    ],
)
def test_known_principal_types(term, expected):
    assert infer(term) == L.normalize_type(parse_type(expected))


@pytest.mark.parametrize(
    "term",
    [
        lam("x", app(V("x"), V("x"))),
        app(I, I),
        ("if", I, T, T),
        lam("f", ("if", app(V("f"), T), app(V("f"), I), ("int", 0))),
        # y is bound to x, whose type is in the context, so y is not generalized
        lam("x", let("y", V("x"), ("if", app(V("y"), T), app(V("y"), I), ("int", 0)))),
        V("free"),
    ],
)
def test_untypable(term):
    with pytest.raises(TypeErrorHM):
        infer(term)
    assert not Reference(term).typable()


def test_unsound_generalization_would_accept_a_stuck_term():
    # If W generalized over the variable of x, y would get the scheme
    # forall a. a, the function fun x -> let y = x in if y true then y 1 else 0
    # would get the type a -> int, and this application would type check,
    # yet it gets stuck at "5 true".
    bad = lam("x", let("y", V("x"), ("if", app(V("y"), T), app(V("y"), I), ("int", 0))))
    run = app(bad, ("int", 5))
    assert principal_type(bad) is None
    assert principal_type(run) is None
    assert L.evaluate(run)[0] == "stuck"


def random_terms(seed, count, depth):
    rng = random.Random(seed)
    return [L.random_term(rng, rng.randint(1, depth)) for _ in range(count)]


def test_against_brute_force_enumeration_of_types():
    typable = 0
    for e in random_terms(11, 400, 5):
        p = principal_type(e)
        ref = Reference(e)
        assert (p is not None) == ref.typable(), L.show(e)
        if p is None:
            assert not any(ref.checks(t) for t in TYPES)
            continue
        typable += 1
        assert ref.checks(p), L.show(e)
        for t in TYPES:
            assert ref.checks(t) == is_instance(t, p), (L.show(e), L.show_type(p), L.show_type(t))
    assert typable >= 100


def test_typable_terms_do_not_get_stuck():
    for e in random_terms(12, 600, 6):
        p = principal_type(e)
        if p is None:
            continue
        out = L.evaluate(e, 2000)
        assert out[0] != "stuck", L.show(e)
        if out[0] == "value":
            v = out[1]
            if p == ("int",):
                assert v[0] == "int"
            elif p == ("bool",):
                assert v[0] == "bool"
            elif p[0] == "fun":
                assert v[0] in ("lam", "fix")


def nested_let(k):
    """let y0 = fun x -> x in let y1 = fun z -> z y0 y0 in ... in yk"""
    body = V(f"y{k}")
    for i in range(k, 0, -1):
        body = let(f"y{i}", lam("z", app(app(V("z"), V(f"y{i - 1}")), V(f"y{i - 1}"))), body)
    return let("y0", lam("x", V("x")), body)


def test_nested_let_types_grow_exponentially():
    for k in range(0, 11):
        e = nested_let(k)
        assert L.size(e) == 7 * k + 4
        t = infer(e)
        assert L.type_size(t) == 8 * 2**k - 5
        assert len(L.type_vars(t)) == 2 ** (k + 1) - 1
    assert L.show_type(infer(nested_let(1))) == "((a -> a) -> (b -> b) -> c) -> c"


def doubling(k):
    """let f0 = fun x -> fun z -> z x x in let f1 = fun y -> f0 (f0 y) in ... in fk"""
    body = V(f"f{k}")
    for i in range(k, 0, -1):
        body = let(f"f{i}", lam("y", app(V(f"f{i - 1}"), app(V(f"f{i - 1}"), V("y")))), body)
    return let("f0", lam("x", lam("z", app(app(V("z"), V("x")), V("x")))), body)


def test_doubling_family_types_grow_doubly_exponentially_as_trees():
    for k in range(0, 4):
        e = doubling(k)
        assert L.size(e) == 7 * k + 9
        assert L.type_size(infer(e)) == 6 * 2 ** (2**k) - 3
    assert L.show_type(infer(doubling(0))) == "a -> (a -> a -> b) -> b"


def test_principal_type_of_small_family_member_checks():
    e = nested_let(2)
    p = infer(e)
    ref = Reference(e)
    assert ref.checks(p)
    assert not ref.checks(("int",))
