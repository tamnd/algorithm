# SPDX-License-Identifier: MIT
# Shared helper of the compilers and program analysis pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""The toy lambda language: terms, types, call-by-value small steps.

Terms are tuples:
    ("var", x)              a variable, x is a str
    ("lam", x, e)           fun x -> e
    ("app", e1, e2)         e1 e2
    ("let", x, e1, e2)      let x = e1 in e2
    ("int", k)              an integer constant, k is a Python int
    ("bool", b)             true or false, b is a Python bool
    ("if", e1, e2, e3)      if e1 then e2 else e3
    ("prim", op, e1, e2)    e1 op e2, op is one of + - * < ==
    ("fix", f, x, e)        a recursive function: f is the function itself, x its argument

Types are tuples:
    ("int",)  ("bool",)  ("fun", t1, t2)  ("tv", n)   with n an int

Values are int and bool constants, lambdas and fix terms. The semantics is
call by value, left to right. step(e) returns the next term when e can step,
e itself when e is a value, and the marker "stuck" otherwise. A free
variable, an application of a non-function, a non-boolean condition and an
operator on non-integers are stuck. Substitution only ever puts closed values
into terms, because evaluation starts from closed terms, so no renaming is
needed.
"""

STUCK = "stuck"

PRIMS = ("+", "-", "*", "<", "==")


def is_value(e):
    return e[0] in ("int", "bool", "lam", "fix")


def free_vars(e):
    """The set of free term variables of e."""
    tag = e[0]
    if tag == "var":
        return {e[1]}
    if tag == "lam":
        return free_vars(e[2]) - {e[1]}
    if tag == "app":
        return free_vars(e[1]) | free_vars(e[2])
    if tag == "let":
        return free_vars(e[2]) | (free_vars(e[3]) - {e[1]})
    if tag in ("int", "bool"):
        return set()
    if tag == "if":
        return free_vars(e[1]) | free_vars(e[2]) | free_vars(e[3])
    if tag == "prim":
        return free_vars(e[2]) | free_vars(e[3])
    if tag == "fix":
        return free_vars(e[3]) - {e[1], e[2]}
    raise ValueError(f"not a term: {e!r}")


def subst(e, x, v):
    """Replace the free occurrences of x in e by the closed value v."""
    tag = e[0]
    if tag == "var":
        return v if e[1] == x else e
    if tag == "lam":
        return e if e[1] == x else ("lam", e[1], subst(e[2], x, v))
    if tag == "app":
        return ("app", subst(e[1], x, v), subst(e[2], x, v))
    if tag == "let":
        body = e[3] if e[1] == x else subst(e[3], x, v)
        return ("let", e[1], subst(e[2], x, v), body)
    if tag in ("int", "bool"):
        return e
    if tag == "if":
        return ("if", subst(e[1], x, v), subst(e[2], x, v), subst(e[3], x, v))
    if tag == "prim":
        return ("prim", e[1], subst(e[2], x, v), subst(e[3], x, v))
    if tag == "fix":
        if x in (e[1], e[2]):
            return e
        return ("fix", e[1], e[2], subst(e[3], x, v))
    raise ValueError(f"not a term: {e!r}")


def _prim(op, a, b):
    if op == "+":
        return ("int", a + b)
    if op == "-":
        return ("int", a - b)
    if op == "*":
        return ("int", a * b)
    if op == "<":
        return ("bool", a < b)
    if op == "==":
        return ("bool", a == b)
    raise ValueError(f"unknown operator {op!r}")


def step(e):
    """One call-by-value step: the next term, e itself if e is a value, or STUCK."""
    if is_value(e):
        return e
    tag = e[0]
    if tag == "var":
        return STUCK
    if tag == "app":
        f, a = e[1], e[2]
        if not is_value(f):
            f2 = step(f)
            return STUCK if f2 == STUCK else ("app", f2, a)
        if not is_value(a):
            a2 = step(a)
            return STUCK if a2 == STUCK else ("app", f, a2)
        if f[0] == "lam":
            return subst(f[2], f[1], a)
        if f[0] == "fix":
            return subst(subst(f[3], f[1], f), f[2], a)
        return STUCK
    if tag == "let":
        if not is_value(e[2]):
            e1 = step(e[2])
            return STUCK if e1 == STUCK else ("let", e[1], e1, e[3])
        return subst(e[3], e[1], e[2])
    if tag == "if":
        c = e[1]
        if not is_value(c):
            c2 = step(c)
            return STUCK if c2 == STUCK else ("if", c2, e[2], e[3])
        if c[0] == "bool":
            return e[2] if c[1] else e[3]
        return STUCK
    if tag == "prim":
        a, b = e[2], e[3]
        if not is_value(a):
            a2 = step(a)
            return STUCK if a2 == STUCK else ("prim", e[1], a2, b)
        if not is_value(b):
            b2 = step(b)
            return STUCK if b2 == STUCK else ("prim", e[1], a, b2)
        if a[0] == "int" and b[0] == "int":
            return _prim(e[1], a[1], b[1])
        return STUCK
    raise ValueError(f"not a term: {e!r}")


def evaluate(e, fuel=10000):
    """Run e. Returns ("value", v), ("stuck", t) with the stuck term t, or ("fuel",)."""
    for _ in range(fuel):
        if is_value(e):
            return ("value", e)
        nxt = step(e)
        if nxt == STUCK:
            return ("stuck", e)
        e = nxt
    return ("value", e) if is_value(e) else ("fuel",)


NAMES = ("x", "y", "z", "f", "g")


def random_term(rng, depth, scope=()):
    """A random term of height at most depth whose free variables are in scope.

    With the default empty scope the term is closed. rng is a random.Random.
    """
    scope = tuple(scope)
    if depth <= 0 or rng.random() < 0.15:
        r = rng.random()
        if scope and r < 0.6:
            return ("var", rng.choice(scope))
        if r < 0.8:
            return ("int", rng.randint(0, 3))
        return ("bool", rng.random() < 0.5)
    d = depth - 1
    kind = rng.choice(("var", "lam", "lam", "app", "app", "let", "let", "if", "prim", "fix"))
    if kind == "var" and scope:
        return ("var", rng.choice(scope))
    if kind == "lam" or kind == "var":
        x = rng.choice(NAMES)
        return ("lam", x, random_term(rng, d, scope + (x,)))
    if kind == "app":
        return ("app", random_term(rng, d, scope), random_term(rng, d, scope))
    if kind == "let":
        x = rng.choice(NAMES)
        return ("let", x, random_term(rng, d, scope), random_term(rng, d, scope + (x,)))
    if kind == "if":
        return ("if", random_term(rng, d, scope), random_term(rng, d, scope), random_term(rng, d, scope))
    if kind == "prim":
        return ("prim", rng.choice(PRIMS), random_term(rng, d, scope), random_term(rng, d, scope))
    f, x = rng.sample(NAMES, 2)
    return ("fix", f, x, random_term(rng, d, scope + (f, x)))


def size(e):
    """The number of nodes of the syntax tree of e."""
    tag = e[0]
    if tag in ("var", "int", "bool"):
        return 1
    if tag == "lam":
        return 1 + size(e[2])
    if tag == "app":
        return 1 + size(e[1]) + size(e[2])
    if tag == "let":
        return 1 + size(e[2]) + size(e[3])
    if tag == "if":
        return 1 + size(e[1]) + size(e[2]) + size(e[3])
    if tag == "prim":
        return 1 + size(e[2]) + size(e[3])
    if tag == "fix":
        return 1 + size(e[3])
    raise ValueError(f"not a term: {e!r}")


def show(e):
    """The surface syntax: fun x -> e, e1 e2, let x = e1 in e2."""
    tag = e[0]
    if tag == "var":
        return e[1]
    if tag == "int":
        return str(e[1])
    if tag == "bool":
        return "true" if e[1] else "false"
    if tag == "lam":
        return f"(fun {e[1]} -> {show(e[2])})"
    if tag == "app":
        return f"({show(e[1])} {show(e[2])})"
    if tag == "let":
        return f"(let {e[1]} = {show(e[2])} in {show(e[3])})"
    if tag == "if":
        return f"(if {show(e[1])} then {show(e[2])} else {show(e[3])})"
    if tag == "prim":
        return f"({show(e[2])} {e[1]} {show(e[3])})"
    if tag == "fix":
        return f"(fix {e[1]} {e[2]} -> {show(e[3])})"
    raise ValueError(f"not a term: {e!r}")


def type_vars(t):
    """The type variables of t, in order of first occurrence, left to right."""
    out = []

    def go(u):
        if u[0] == "tv":
            if u[1] not in out:
                out.append(u[1])
        elif u[0] == "fun":
            go(u[1])
            go(u[2])

    go(t)
    return out


def rename_type(t, mapping):
    if t[0] == "tv":
        return ("tv", mapping.get(t[1], t[1]))
    if t[0] == "fun":
        return ("fun", rename_type(t[1], mapping), rename_type(t[2], mapping))
    return t


def normalize_type(t):
    """Rename the type variables of t to 0, 1, 2, ... in order of first occurrence."""
    return rename_type(t, {v: i for i, v in enumerate(type_vars(t))})


def type_size(t):
    """The number of nodes of t as a tree."""
    if t[0] == "fun":
        return 1 + type_size(t[1]) + type_size(t[2])
    return 1


def show_type(t):
    """int, bool, a, b, ... with right-associative arrows."""
    if t[0] == "int":
        return "int"
    if t[0] == "bool":
        return "bool"
    if t[0] == "tv":
        n = t[1]
        return chr(ord("a") + n) if 0 <= n < 26 else f"t{n}"
    left = show_type(t[1])
    if t[1][0] == "fun":
        left = f"({left})"
    return f"{left} -> {show_type(t[2])}"
