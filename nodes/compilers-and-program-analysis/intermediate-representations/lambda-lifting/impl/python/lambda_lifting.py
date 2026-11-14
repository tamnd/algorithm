# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lambda-lifting/. The authors are listed in prov/ZHK5BH.jsonl.
"""Johnsson's lambda lifting for the toy lambda language of toylam.py.

lambda_lift(e) returns (defs, main). defs maps a global name F to
(params, body), and main is the term to run. No body and no main contains a
fun or a fix. A source function with extra parameters p1 ... pk becomes the
global F p1 ... pk x, and the function value itself becomes the partial
application F p1 ... pk.

The source may also use ("letrec", ((f1, x1, b1), ..., (fk, xk, bk)), e),
which binds k mutually recursive functions in all the bodies and in e. The
toy evaluator of toylam.py does not run it, but the lifter accepts it, so that
the fixed point over mutual recursion can be tested.

Target terms are the toy terms without "lam" and "fix", plus the leaf
("global", F). A global applied to fewer arguments than its parameters is a
value; applied to all of them, it steps to its body with the arguments put in
for the parameters. evaluate(defs, main) runs a target program.
"""

import toylam

STUCK = toylam.STUCK


def var(x):
    return ("var", x)


def names(e):
    """Every variable name in the source term e, bound or free."""
    tag = e[0]
    if tag == "var":
        return {e[1]}
    if tag in ("int", "bool"):
        return set()
    if tag == "lam":
        return {e[1]} | names(e[2])
    if tag == "let":
        return {e[1]} | names(e[2]) | names(e[3])
    if tag == "fix":
        return {e[1], e[2]} | names(e[3])
    if tag == "prim":
        return names(e[2]) | names(e[3])
    if tag == "letrec":
        out = names(e[2])
        for f, x, b in e[1]:
            out |= {f, x} | names(b)
        return out
    out = set()
    for part in e[1:]:
        out |= names(part)
    return out


class Fresh:
    """Makes names that are not in avoid and were not made before."""

    def __init__(self, avoid=()):
        self.avoid = set(avoid)
        self.n = 0

    def __call__(self, base):
        while True:
            self.n += 1
            name = f"{base}{self.n}"
            if name not in self.avoid:
                self.avoid.add(name)
                return name


def prepare(e, fresh):
    """Rename every binder of e apart and turn each fun and fix into
    ("fn", F, f, x, body), with F a new global name and f the name of the fix
    (None for a fun)."""
    env = {}

    def bind(x):
        old = env.get(x)
        env[x] = fresh(x)
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
            g = fresh("F")
            y, old = bind(e[1])
            body = go(e[2])
            unbind(e[1], old)
            return ("fn", g, None, y, body)
        if tag == "fix":
            g = fresh("F")
            f2, old_f = bind(e[1])
            y, old_x = bind(e[2])
            body = go(e[3])
            unbind(e[2], old_x)
            unbind(e[1], old_f)
            return ("fn", g, f2, y, body)
        if tag == "let":
            rhs = go(e[2])
            y, old = bind(e[1])
            body = go(e[3])
            unbind(e[1], old)
            return ("let", y, rhs, body)
        if tag == "prim":
            return ("prim", e[1], go(e[2]), go(e[3]))
        if tag == "letrec":
            gs = [fresh("F") for _ in e[1]]
            olds = [bind(f) for f, _, _ in e[1]]
            fns = []
            for g, (f, x, b) in zip(gs, e[1]):
                y, old = bind(x)
                fns.append(("fn", g, env[f], y, go(b)))
                unbind(x, old)
            body = go(e[2])
            for (f, _, _), (_, old) in reversed(list(zip(e[1], olds))):
                unbind(f, old)
            return ("letrec", tuple(fns), body)
        return (tag,) + tuple(go(p) for p in e[1:])

    return go(e)


def fv(e):
    """Free variables of a prepared term."""
    tag = e[0]
    if tag == "var":
        return {e[1]}
    if tag in ("int", "bool"):
        return set()
    if tag == "fn":
        return fv(e[4]) - {e[2], e[3]}
    if tag == "let":
        return fv(e[2]) | (fv(e[3]) - {e[1]})
    if tag == "prim":
        return fv(e[2]) | fv(e[3])
    if tag == "letrec":
        out = fv(e[2])
        for fn in e[1]:
            out |= fv(fn)
        return out - {fn[2] for fn in e[1]}
    out = set()
    for p in e[1:]:
        out |= fv(p)
    return out


def functions(e):
    """All ("fn", ...) nodes of a prepared term."""
    tag = e[0]
    if tag in ("var", "int", "bool"):
        return []
    if tag == "fn":
        return [e] + functions(e[4])
    if tag in ("let", "prim"):
        return functions(e[2]) + functions(e[3])
    if tag == "letrec":
        out = []
        for fn in e[1]:
            out += functions(fn)
        return out + functions(e[2])
    out = []
    for p in e[1:]:
        out += functions(p)
    return out


def call(g, args):
    out = ("global", g)
    for a in args:
        out = ("app", out, var(a))
    return out


def reachable(start, refs):
    """The globals reachable from start along refs, start included."""
    seen, stack = {start}, [start]
    while stack:
        for g in refs[stack.pop()]:
            if g not in seen:
                seen.add(g)
                stack.append(g)
    return seen


def lambda_lift(e, transitive=True):
    """Lift every function of the closed term e to the top level: (defs, main).

    With transitive=False each function gets only its own free variables as
    extra parameters. That is wrong in general; it exists to show why line L4
    is needed."""
    fresh = Fresh(names(e))
    e = prepare(e, fresh)  # @line L1
    fns = functions(e)
    global_of = {fn[2]: fn[1] for fn in fns if fn[2] is not None}
    direct, refs = {}, {}
    for fn in fns:  # @line L2
        free = fv(fn)
        direct[fn[1]] = {y for y in free if y not in global_of}
        refs[fn[1]] = [global_of[y] for y in free if y in global_of]
    extra = {}
    for fn in fns:  # @line L3
        extra[fn[1]] = set(direct[fn[1]])
        if transitive:
            for g in reachable(fn[1], refs):  # @line L4
                extra[fn[1]] |= direct[g]
    params = {g: sorted(s) for g, s in extra.items()}  # @line L5

    def lift(e):
        tag = e[0]
        if tag == "var":  # @line L9
            g = global_of.get(e[1])
            return e if g is None else call(g, params[g])
        if tag == "fn":  # @line L10
            return call(e[1], params[e[1]])
        if tag in ("int", "bool"):  # @line L11
            return e
        if tag == "let":
            return ("let", e[1], lift(e[2]), lift(e[3]))
        if tag == "prim":
            return ("prim", e[1], lift(e[2]), lift(e[3]))
        if tag == "letrec":
            return lift(e[2])
        return (tag,) + tuple(lift(p) for p in e[1:])

    defs = {}
    for fn in fns:  # @line L6
        defs[fn[1]] = (params[fn[1]] + [fn[3]], lift(fn[4]))  # @line L7
    return defs, lift(e)  # @line L8


# ------------------------------------------------------------ the target language


def spine(e):
    """(head, args) of a chain of calls."""
    args = []
    while e[0] == "app":
        args.append(e[2])
        e = e[1]
    return e, args[::-1]


def is_value(e, defs):
    tag = e[0]
    if tag in ("int", "bool", "global"):
        return True
    if tag != "app":
        return False
    head, args = spine(e)
    return head[0] == "global" and len(args) < len(defs[head[1]][0]) and all(is_value(a, defs) for a in args)


def subst(e, x, v):
    """Replace the free occurrences of x in the target term e by the closed value v."""
    tag = e[0]
    if tag == "var":
        return v if e[1] == x else e
    if tag in ("int", "bool", "global"):
        return e
    if tag == "let":
        return ("let", e[1], subst(e[2], x, v), e[3] if e[1] == x else subst(e[3], x, v))
    if tag == "prim":
        return ("prim", e[1], subst(e[2], x, v), subst(e[3], x, v))
    return (tag,) + tuple(subst(p, x, v) for p in e[1:])


def step(e, defs):
    """One call-by-value step of a target term: the next term, e if e is a value, or STUCK."""
    if is_value(e, defs):
        return e
    tag = e[0]
    if tag == "var":
        return STUCK
    if tag == "app":
        f, a = e[1], e[2]
        if not is_value(f, defs):
            q = step(f, defs)
            return STUCK if q == STUCK else ("app", q, a)
        if not is_value(a, defs):
            q = step(a, defs)
            return STUCK if q == STUCK else ("app", f, q)
        head, args = spine(e)
        if head[0] != "global":
            return STUCK
        ps, body = defs[head[1]]
        for p, arg in zip(ps, args):
            body = subst(body, p, arg)
        return body
    if tag == "let":
        if not is_value(e[2], defs):
            q = step(e[2], defs)
            return STUCK if q == STUCK else ("let", e[1], q, e[3])
        return subst(e[3], e[1], e[2])
    if tag == "if":
        if not is_value(e[1], defs):
            q = step(e[1], defs)
            return STUCK if q == STUCK else ("if", q, e[2], e[3])
        if e[1][0] == "bool":
            return e[2] if e[1][1] else e[3]
        return STUCK
    if tag == "prim":
        a, b = e[2], e[3]
        if not is_value(a, defs):
            q = step(a, defs)
            return STUCK if q == STUCK else ("prim", e[1], q, b)
        if not is_value(b, defs):
            q = step(b, defs)
            return STUCK if q == STUCK else ("prim", e[1], a, q)
        if a[0] == "int" and b[0] == "int":
            return toylam._prim(e[1], a[1], b[1])
        return STUCK
    raise ValueError(f"not a term: {e!r}")


def evaluate(defs, e, fuel=10000):
    """Run the target program: ("value", v), ("stuck", t) or ("fuel",)."""
    for _ in range(fuel):
        if is_value(e, defs):
            return ("value", e)
        nxt = step(e, defs)
        if nxt == STUCK:
            return ("stuck", e)
        e = nxt
    return ("value", e) if is_value(e, defs) else ("fuel",)


def show(e):
    """The surface syntax of a target term; a global is written by its name."""
    if e[0] == "global":
        return e[1]
    if e[0] == "app":
        head, args = spine(e)
        return "(" + " ".join(show(p) for p in [head] + args) + ")"
    if e[0] in ("let", "if", "prim"):
        parts = list(e)
        start = 2 if e[0] in ("let", "prim") else 1
        for i in range(start, len(parts)):
            parts[i] = ("var", show(parts[i]))
        return toylam.show(tuple(parts))
    return toylam.show(e)


def show_program(defs, main):
    lines = [f"{g} {' '.join(ps)} = {show(body)}" for g, (ps, body) in defs.items()]
    return lines + [f"main = {show(main)}"]
