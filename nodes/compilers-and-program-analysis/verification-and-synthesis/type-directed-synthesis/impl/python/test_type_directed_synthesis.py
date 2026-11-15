# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/type-directed-synthesis/. The authors are listed in prov/3WFWA4.jsonl.

import random

import toylam
from type_directed_synthesis import synthesize

INT, BOOL = ("int",), ("bool",)


def fun(a, b):
    return ("fun", a, b)


# Type inference for the toy language by unification, written for this test:
# toylam.py has the terms and the interpreter, but no inference.


class Infer:
    def __init__(self):
        self.sub = {}
        self.n = 0

    def fresh(self):
        self.n += 1
        return ("tv", self.n)

    def find(self, t):
        while t[0] == "tv" and t[1] in self.sub:
            t = self.sub[t[1]]
        return t

    def resolve(self, t):
        t = self.find(t)
        if t[0] == "fun":
            return fun(self.resolve(t[1]), self.resolve(t[2]))
        return t

    def occurs(self, v, t):
        t = self.find(t)
        if t[0] == "tv":
            return t[1] == v
        if t[0] == "fun":
            return self.occurs(v, t[1]) or self.occurs(v, t[2])
        return False

    def unify(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return
        if a[0] == "tv":
            if self.occurs(a[1], b):
                raise TypeError("occurs check")
            self.sub[a[1]] = b
            return
        if b[0] == "tv":
            self.unify(b, a)
            return
        if a[0] == "fun" and b[0] == "fun":
            self.unify(a[1], b[1])
            self.unify(a[2], b[2])
            return
        raise TypeError(f"cannot unify {a} and {b}")

    def infer(self, env, e):
        tag = e[0]
        if tag == "var":
            if e[1] not in env:
                raise TypeError(f"unbound {e[1]}")
            return env[e[1]]
        if tag == "int":
            return INT
        if tag == "bool":
            return BOOL
        if tag == "lam":
            a = self.fresh()
            return fun(a, self.infer({**env, e[1]: a}, e[2]))
        if tag == "app":
            tf = self.infer(env, e[1])
            ta = self.infer(env, e[2])
            r = self.fresh()
            self.unify(tf, fun(ta, r))
            return r
        if tag == "if":
            self.unify(self.infer(env, e[1]), BOOL)
            t = self.infer(env, e[2])
            self.unify(t, self.infer(env, e[3]))
            return t
        if tag == "prim":
            self.unify(self.infer(env, e[2]), INT)
            self.unify(self.infer(env, e[3]), INT)
            return INT if e[1] in ("+", "-", "*") else BOOL
        if tag == "fix":
            a, r = self.fresh(), self.fresh()
            self.unify(self.infer({**env, e[1]: fun(a, r), e[2]: a}, e[3]), r)
            return fun(a, r)
        raise TypeError(f"unsupported term {e!r}")


def type_of(e):
    inf = Infer()
    return toylam.normalize_type(inf.resolve(inf.infer({}, e)))


def has_type(e, t):
    """e type-checks at t: its inferred type unifies with t."""
    inf = Infer()
    inf.unify(inf.infer({}, e), t)
    return inf.resolve(t) == t


def goal_type(arity):
    t = INT
    for _ in range(arity):
        t = fun(INT, t)
    return t


def run(p, args):
    t = p
    for a in args:
        t = ("app", t, ("int", a))
    return toylam.evaluate(t, 200000)


def check(p, arity, examples):
    assert p is not None
    assert toylam.free_vars(p) == set()
    # The principal type is the goal type, or more general when an argument is unused.
    assert has_type(p, goal_type(arity)), toylam.show(p)
    for args, out in examples:
        assert run(p, args) == ("value", ("int", out)), (toylam.show(p), args, out)


def test_inference_itself():
    assert type_of(("lam", "x", ("var", "x"))) == fun(("tv", 0), ("tv", 0))
    assert type_of(("fix", "f", "x", ("prim", "+", ("var", "x"), ("int", 1)))) == fun(INT, INT)
    try:
        type_of(("prim", "+", ("bool", True), ("int", 1)))
        assert False
    except TypeError:
        pass


def test_classic_tasks():
    tasks = [
        (1, [((n,), n * (n + 1) // 2) for n in range(5)]),
        (1, [((0,), 1), ((1,), 1), ((2,), 2), ((3,), 6), ((4,), 24)]),
        (1, [((n,), 2 ** n) for n in range(5)]),
        (1, [((n,), sum(i * i for i in range(n + 1))) for n in range(5)]),
        (2, [((1, 2), 2), ((3, 1), 3), ((2, 2), 2), ((0, 5), 5), ((4, 0), 4)]),
    ]
    for arity, examples in tasks:
        check(synthesize(arity, examples), arity, examples)


def random_eterm(rng, size, leaves):
    if size <= 1:
        return rng.choice(leaves)
    s1 = rng.randrange(1, size - 1, 2) if size > 2 else 1
    return (rng.choice("+-*"), random_eterm(rng, s1, leaves), random_eterm(rng, size - 1 - s1, leaves))


def value(t, env):
    if isinstance(t, str):
        return env[t]
    a, b = value(t[1], env), value(t[2], env)
    return a + b if t[0] == "+" else a - b if t[0] == "-" else a * b


def test_random_recursive_targets():
    # f 0 = c and f n = g(n, f (n - 1)): trace complete examples on 0 .. 4.
    rng = random.Random(5)
    for _ in range(25):
        c = rng.choice((0, 1))
        g = random_eterm(rng, rng.choice((3, 5)), ["x", "r", "0", "1"])
        outs = [c]
        for n in range(1, 5):
            outs.append(value(g, {"x": n, "r": outs[-1], "0": 0, "1": 1}))
        examples = [((n,), outs[n]) for n in range(5)]
        check(synthesize(1, examples), 1, examples)


def test_random_conditional_targets():
    rng = random.Random(6)
    for _ in range(25):
        a = random_eterm(rng, 1, ["x", "y", "0", "1"])
        b = random_eterm(rng, 1, ["x", "y", "0", "1"])
        e1 = random_eterm(rng, rng.choice((1, 3)), ["x", "y", "0", "1"])
        e2 = random_eterm(rng, rng.choice((1, 3)), ["x", "y", "0", "1"])
        examples = []
        for _ in range(5):
            env = {"x": rng.randint(0, 4), "y": rng.randint(0, 4), "0": 0, "1": 1}
            out = value(e1, env) if value(a, env) < value(b, env) else value(e2, env)
            examples.append(((env["x"], env["y"]), out))
        table = {}
        for args, out in examples:
            table.setdefault(args, out)
        examples = sorted(table.items())
        check(synthesize(2, examples, max_size=5, max_splits=1), 2, examples)


def test_none_within_bounds():
    examples = [((n,), n ** 3) for n in range(5)]
    assert synthesize(1, examples, max_size=3, max_splits=0) is None
    check(synthesize(1, examples, max_size=5, max_splits=0), 1, examples)


def test_underspecified_fibonacci():
    # Fibonacci needs two recursive calls on n - 1 and n - 2, which are not in the
    # language. The search still meets every example, and differs from Fibonacci later.
    fib = [0, 1, 1, 2, 3, 5]
    examples = [((n,), fib[n]) for n in range(6)]
    p = synthesize(1, examples)
    check(p, 1, examples)
    assert run(p, (6,)) != ("value", ("int", 8))
