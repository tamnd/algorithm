# SPDX-License-Identifier: MIT
"""Binding-time analysis for the toy lambda language (toylam.py).

The program is a term whose free variables are its inputs. Some inputs are
static (known before the run) and the others are dynamic. annotate gives
every node of the term an annotated type: its simple type with a binding
time, S or D, on every type constructor. It works in two passes:

1. simple types by monomorphic unification (let is not generalized, and a
   type variable that is left over is read as int);
2. a binding-time variable on each constructor, Horn constraints from the
   rules of the language, and the least solution by propagation.

congruent checks an annotation against the congruence rules directly, and
specialize is a specializer guided by the annotation: it runs the static
parts and builds a residual term from the dynamic parts.
"""

import itertools

import toylam


class NotTypable(Exception):
    """The term has no simple type (monomorphic let)."""


class StaticInputForced(Exception):
    """A static input would have to be dynamic."""


class Budget(Exception):
    """The specializer unfolded more static calls than its budget allows."""


# ------------------------------------------------------------- simple types


class _Types:
    def __init__(self):
        self.parent = {}
        self.count = itertools.count()

    def fresh(self):
        return ("tv", next(self.count))

    def find(self, t):
        while t[0] == "tv" and t in self.parent:
            t = self.parent[t]
        return t

    def occurs(self, v, t):
        t = self.find(t)
        if t == v:
            return True
        return t[0] == "fun" and (self.occurs(v, t[1]) or self.occurs(v, t[2]))

    def unify(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return
        if b[0] == "tv":
            a, b = b, a
        if a[0] == "tv":
            if self.occurs(a, b):
                raise NotTypable("occurs check")
            self.parent[a] = b
            return
        if a[0] != b[0]:
            raise NotTypable("%s and %s" % (a[0], b[0]))
        if a[0] == "fun":
            self.unify(a[1], b[1])
            self.unify(a[2], b[2])

    def resolve(self, t):
        t = self.find(t)
        if t[0] == "tv":
            return ("int",)
        if t[0] == "fun":
            return ("fun", self.resolve(t[1]), self.resolve(t[2]))
        return t


def infer(e, inputs):
    """Simple types of every node (keyed by path) and of every binder.

    A path is the tuple of indices into the term tuples from the root. A
    binder key is ("in", x) for an input x, and (path, name) for a lam, let
    or fix binder at path.
    """
    ty = _Types()
    node, binder = {}, {}
    env0 = {}
    for x in inputs:
        env0[x] = binder[("in", x)] = ty.fresh()

    def walk(e, path, env):
        tag = e[0]
        if tag == "var":
            if e[1] not in env:
                raise NotTypable("unbound " + e[1])
            t = env[e[1]]
        elif tag == "int":
            t = ("int",)
        elif tag == "bool":
            t = ("bool",)
        elif tag == "lam":
            tx = binder[(path, e[1])] = ty.fresh()
            t = ("fun", tx, walk(e[2], path + (2,), {**env, e[1]: tx}))
        elif tag == "app":
            tf = walk(e[1], path + (1,), env)
            ta = walk(e[2], path + (2,), env)
            t = ty.fresh()
            ty.unify(tf, ("fun", ta, t))
        elif tag == "let":
            t1 = binder[(path, e[1])] = walk(e[2], path + (2,), env)
            t = walk(e[3], path + (3,), {**env, e[1]: t1})
        elif tag == "if":
            ty.unify(walk(e[1], path + (1,), env), ("bool",))
            t = walk(e[2], path + (2,), env)
            ty.unify(t, walk(e[3], path + (3,), env))
        elif tag == "prim":
            ty.unify(walk(e[2], path + (2,), env), ("int",))
            ty.unify(walk(e[3], path + (3,), env), ("int",))
            t = ("int",) if e[1] in ("+", "-", "*") else ("bool",)
        elif tag == "fix":
            tx, tr = ty.fresh(), ty.fresh()
            t = ("fun", tx, tr)
            binder[(path, e[1])] = t
            binder[(path, e[2])] = tx
            ty.unify(walk(e[3], path + (3,), {**env, e[1]: t, e[2]: tx}), tr)
        else:
            raise ValueError("not a term: %r" % (e,))
        node[path] = t
        return t

    walk(e, (), env0)
    return ({p: ty.resolve(t) for p, t in node.items()},
            {k: ty.resolve(t) for k, t in binder.items()})


# ---------------------------------------------------------- binding times
#
# An annotated type is ("base", v) or ("fun", v, t1, t2), where v is the
# number of a binding-time variable. The solution is the set of variables
# that are D; every other variable is S.


def top(t):
    return t[1]


def bt_vars(t):
    if t[0] == "base":
        return [t[1]]
    return [t[1]] + bt_vars(t[2]) + bt_vars(t[3])


class Annotation:
    """The result of annotate: node and binder annotated types and the
    set D of the dynamic binding-time variables."""

    def __init__(self, term, dynamic, node, binder, dyn, nvars, constraints):
        self.term = term
        self.dynamic = list(dynamic)
        self.node = node
        self.binder = binder
        self.dyn = dyn
        self.nvars = nvars
        self.constraints = constraints

    def is_dynamic(self, t):
        return top(t) in self.dyn


def annotate(e, static, dynamic):
    """Binding-time analysis of e, whose free variables are the static and
    the dynamic inputs. Returns an Annotation with the least solution."""
    inputs = list(static) + list(dynamic)
    if not toylam.free_vars(e) <= set(inputs):
        raise NotTypable("free variable that is not an input")
    stype, btype = infer(e, inputs)  # @line L1
    count = itertools.count()
    implies = []  # pairs (a, b): if a is D then b is D
    facts = []
    made = []

    def ann(t):  # @line L2
        if t[0] == "fun":
            a = ("fun", next(count), ann(t[1]), ann(t[2]))
        else:
            a = ("base", next(count))
        made.append(a)
        return a

    def equal(a, b):
        for u, v in zip(bt_vars(a), bt_vars(b)):
            implies.append((u, v))
            implies.append((v, u))

    def flow(a, b):
        """A value of type a is used where type b is expected. At base type
        an S value can be lifted to D; function types must be equal."""
        if a[0] == "base":
            implies.append((top(a), top(b)))
        else:
            equal(a, b)

    node, binder = {}, {}
    env0 = {}
    for x in inputs:
        if btype[("in", x)][0] == "fun":
            raise NotTypable("an input of function type")
        env0[x] = binder[("in", x)] = ann(btype[("in", x)])
        if x in dynamic:
            facts.append(top(env0[x]))  # @line L3

    def walk(e, path, env):  # @line L4
        tag = e[0]
        if tag == "var":
            t = ann(stype[path])
            flow(env[e[1]], t)
        elif tag in ("int", "bool"):
            t = ann(stype[path])
        elif tag == "lam":
            tx = binder[(path, e[1])] = ann(btype[(path, e[1])])
            tb = walk(e[2], path + (2,), {**env, e[1]: tx})
            t = ("fun", next(count), tx, ann(stype[path + (2,)]))
            made.append(t)
            flow(tb, t[3])
            implies.append((top(tx), top(t[3])))
        elif tag == "app":
            tf = walk(e[1], path + (1,), env)
            ta = walk(e[2], path + (2,), env)
            t = ann(stype[path])
            flow(ta, tf[2])
            flow(tf[3], t)
        elif tag == "let":
            t1 = walk(e[2], path + (2,), env)
            tx = binder[(path, e[1])] = ann(btype[(path, e[1])])
            flow(t1, tx)
            t2 = walk(e[3], path + (3,), {**env, e[1]: tx})
            t = ann(stype[path])
            flow(t2, t)
            implies.append((top(tx), top(t)))
        elif tag == "if":
            tc = walk(e[1], path + (1,), env)
            ta = walk(e[2], path + (2,), env)
            tb = walk(e[3], path + (3,), env)
            t = ann(stype[path])
            flow(ta, t)
            flow(tb, t)
            implies.append((top(tc), top(t)))
        elif tag == "prim":
            ta = walk(e[2], path + (2,), env)
            tb = walk(e[3], path + (3,), env)
            t = ann(stype[path])
            implies.append((top(ta), top(t)))
            implies.append((top(tb), top(t)))
        elif tag == "fix":
            tx = binder[(path, e[2])] = ann(btype[(path, e[2])])
            t = ("fun", next(count), tx, ann(stype[path + (3,)]))
            made.append(t)
            binder[(path, e[1])] = t
            tb = walk(e[3], path + (3,), {**env, e[1]: t, e[2]: tx})
            flow(tb, t[3])
            implies.append((top(tx), top(t[3])))
            # A recursive function with a dynamic parameter is not unfolded.
            implies.append((top(tx), top(t)))
        else:
            raise ValueError("not a term: %r" % (e,))
        node[path] = t
        return t

    root = walk(e, (), env0)
    for a in made:  # @line L5
        if a[0] == "fun":
            implies.append((top(a), top(a[2])))
            implies.append((top(a), top(a[3])))
    if root[0] == "fun":
        # A function result is code. A base result can stay static: the
        # specializer lifts it at the end.
        facts.append(top(root))  # @line L6

    # Least solution: everything reachable from a fact along implications.
    nvars = next(count)
    succ = [[] for _ in range(nvars)]
    for a, b in implies:
        succ[a].append(b)
    dyn, work = set(), list(facts)
    while work:  # @line L7
        v = work.pop()
        if v not in dyn:
            dyn.add(v)
            work.extend(succ[v])
    for x in static:  # @line L8
        if top(binder[("in", x)]) in dyn:
            raise StaticInputForced(x)
    return Annotation(e, dynamic, node, binder, dyn, nvars, (implies, facts))  # @line L9


# ------------------------------------------------------------- congruence


def congruent(a, dyn=None):
    """Check that the binding times dyn (default: the solution) obey the
    congruence rules: no static part depends on a dynamic one, a dynamic
    function has dynamic parts, and the result is dynamic. Returns a list
    of the violated rules (empty when congruent)."""
    if dyn is None:
        dyn = a.dyn
    bad = []

    def D(t):
        return top(t) in dyn

    def same(s, t):
        return all((u in dyn) == (v in dyn) for u, v in zip(bt_vars(s), bt_vars(t)))

    def at_least(s, t):
        """A value of type s may be used at type t."""
        if s[0] == "base":
            return D(t) or not D(s)
        return same(s, t)

    def wf(t):
        if t[0] == "fun":
            if D(t) and not (D(t[2]) and D(t[3])):
                bad.append("a dynamic function with a static part")
            wf(t[2])
            wf(t[3])

    for t in list(a.node.values()) + list(a.binder.values()):
        wf(t)

    def walk(e, path, env):
        t = a.node[path]
        tag = e[0]
        if tag == "var":
            if not at_least(env[e[1]], t):
                bad.append("a static use of a dynamic variable")
        elif tag == "lam":
            tx = a.binder[(path, e[1])]
            if not same(tx, t[2]):
                bad.append("lam parameter")
            tb = walk(e[2], path + (2,), {**env, e[1]: tx})
            if not at_least(tb, t[3]):
                bad.append("a static lam result from a dynamic body")
            if D(tx) and not D(t[3]):
                bad.append("a static result of a call with a dynamic argument")
        elif tag == "app":
            tf = walk(e[1], path + (1,), env)
            ta = walk(e[2], path + (2,), env)
            if not at_least(ta, tf[2]):
                bad.append("a dynamic argument to a static parameter")
            if not at_least(tf[3], t):
                bad.append("a static application with a dynamic result")
        elif tag == "let":
            tx = a.binder[(path, e[1])]
            t1 = walk(e[2], path + (2,), env)
            t2 = walk(e[3], path + (3,), {**env, e[1]: tx})
            if not at_least(t1, tx):
                bad.append("a static let variable bound to a dynamic value")
            if not at_least(t2, t) or (D(tx) and not D(t)):
                bad.append("a static let with a dynamic part")
        elif tag == "if":
            tc = walk(e[1], path + (1,), env)
            ta = walk(e[2], path + (2,), env)
            tb = walk(e[3], path + (3,), env)
            if (D(tc) and not D(t)) or not at_least(ta, t) or not at_least(tb, t):
                bad.append("a static if with a dynamic part")
        elif tag == "prim":
            ta = walk(e[2], path + (2,), env)
            tb = walk(e[3], path + (3,), env)
            if (D(ta) or D(tb)) and not D(t):
                bad.append("a static operation on a dynamic operand")
        elif tag == "fix":
            tx = a.binder[(path, e[2])]
            if not same(a.binder[(path, e[1])], t) or not same(tx, t[2]):
                bad.append("fix binders")
            tb = walk(e[3], path + (3,), {**env, e[1]: t, e[2]: tx})
            if not at_least(tb, t[3]):
                bad.append("a static fix result from a dynamic body")
            if D(tx) and not D(t[3]):
                bad.append("a static result of a call with a dynamic argument")
            if D(tx) and not D(t):
                bad.append("a static recursive function with a dynamic parameter")
        return t

    env0 = {k[1]: t for k, t in a.binder.items() if k[0] == "in"}
    for x in a.dynamic:
        if not D(env0[x]):
            bad.append("a static dynamic input")
    root = walk(a.term, (), env0)
    if root[0] == "fun" and not D(root):
        bad.append("a static function as the result")
    return bad


# ------------------------------------------------------------ specializer


def specialize(a, static_values, budget=300):
    """The residual term of a.term for the given static input values.

    Static parts are run, dynamic parts are rebuilt with fresh names. A
    static call with a dynamic argument binds the argument with a residual
    let, unless it is a variable or a constant, so the residual term keeps
    the call-by-value meaning. Raises Budget when more than budget static
    calls are unfolded: specialization need not terminate.
    """
    fresh = itertools.count(1)
    left = [budget]
    D = a.is_dynamic

    def name(x):
        return "%s%d" % (x, next(fresh))

    def code(r):
        if r[0] == "D":
            return r[1]
        if r[1][0] in ("int", "bool"):
            return r[1]  # lift a static constant
        raise ValueError("cannot lift a static function")

    def coerce(r, t):
        if D(t):
            return ("D", code(r))
        if r[0] == "D":
            raise ValueError("a dynamic value at a static type")
        return r

    def bind(x, r, t, body):
        """Bind x to the argument r of type t around spec of body."""
        r = coerce(r, t)
        if r[0] == "S" or r[1][0] in ("var", "int", "bool"):
            return body(r)
        x2 = name(x)
        res = body(("D", ("var", x2)))
        return ("D", ("let", x2, r[1], code(res)))

    def call(f, arg):
        left[0] -= 1
        if left[0] < 0:
            raise Budget()
        _, e, path, env = f
        t = a.node[path]
        if e[0] == "lam":
            x, bpath, extra = e[1], path + (2,), {}
        else:
            x, bpath, extra = e[2], path + (3,), {e[1]: ("S", f)}
        return bind(x, arg, t[2], lambda r: coerce(
            spec(e[3] if e[0] == "fix" else e[2], bpath, {**env, **extra, x: r}), t[3]))

    def spec(e, path, env):  # returns ("S", value) or ("D", code)
        t = a.node[path]
        tag = e[0]
        if tag == "var":
            return coerce(env[e[1]], t)
        if tag in ("int", "bool"):
            return ("D", e) if D(t) else ("S", e)
        if tag == "lam":
            if not D(t):
                return ("S", ("clo", e, path, env))
            x = name(e[1])
            body = spec(e[2], path + (2,), {**env, e[1]: ("D", ("var", x))})
            return ("D", ("lam", x, code(body)))
        if tag == "fix":
            if not D(t):
                return ("S", ("clo", e, path, env))
            f, x = name(e[1]), name(e[2])
            body = spec(e[3], path + (3,), {**env, e[1]: ("D", ("var", f)), e[2]: ("D", ("var", x))})
            return ("D", ("fix", f, x, code(body)))
        if tag == "app":
            rf = spec(e[1], path + (1,), env)
            ra = spec(e[2], path + (2,), env)
            if rf[0] == "D":
                return ("D", ("app", rf[1], code(ra)))
            return coerce(call(rf[1], ra), t)
        if tag == "let":
            tx = a.binder[(path, e[1])]
            r1 = spec(e[2], path + (2,), env)
            if D(tx):
                x = name(e[1])
                r2 = spec(e[3], path + (3,), {**env, e[1]: ("D", ("var", x))})
                return ("D", ("let", x, code(r1), code(r2)))
            return coerce(spec(e[3], path + (3,), {**env, e[1]: r1}), t)
        if tag == "if":
            rc = spec(e[1], path + (1,), env)
            if rc[0] == "D":
                ra = spec(e[2], path + (2,), env)
                rb = spec(e[3], path + (3,), env)
                return ("D", ("if", rc[1], code(ra), code(rb)))
            branch = 2 if rc[1][1] else 3
            return coerce(spec(e[branch], path + (branch,), env), t)
        if tag == "prim":
            ra = spec(e[2], path + (2,), env)
            rb = spec(e[3], path + (3,), env)
            if D(t):
                return ("D", ("prim", e[1], code(ra), code(rb)))
            out = toylam.evaluate(("prim", e[1], ra[1], rb[1]))
            return ("S", out[1])
        raise ValueError("not a term: %r" % (e,))

    env0 = {x: ("S", v) for x, v in static_values.items()}
    for k in a.binder:
        if k[0] == "in" and k[1] not in static_values:
            env0[k[1]] = ("D", ("var", k[1]))
    try:
        return code(spec(a.term, (), env0))
    except RecursionError:
        raise Budget() from None


def show_annotated(a):
    """The term with each dynamic node underlined by a leading underscore
    on its keyword or operator: _fun, _if, _let, _+, @ for a dynamic call,
    and lift(...) around a static base value that is used where a dynamic
    one is expected."""
    def D(path):
        return a.is_dynamic(a.node[path])

    def sub(e, path, env, want):
        """The child e at path, lifted when it is a static base value and
        the place it goes to (annotated type want) is dynamic."""
        s = go(e, path, env)
        t = a.node[path]
        if t[0] == "base" and not a.is_dynamic(t) and a.is_dynamic(want):
            s = "lift(%s)" % s
        return s

    def go(e, path, env):
        tag = e[0]
        t = a.node[path]
        if tag == "var":
            s = e[1]
            if D(path) and not a.is_dynamic(env[e[1]]):
                s = "lift(%s)" % s
            return s
        if tag == "int":
            return "%d" % e[1]
        if tag == "bool":
            return "true" if e[1] else "false"
        if tag == "lam":
            env2 = {**env, e[1]: a.binder[(path, e[1])]}
            kw = "_fun" if D(path) else "fun"
            return "(%s %s -> %s)" % (kw, e[1], sub(e[2], path + (2,), env2, t[3]))
        if tag == "app":
            tf = a.node[path + (1,)]
            sep = " @ " if a.is_dynamic(tf) else " "
            s = "(%s%s%s)" % (go(e[1], path + (1,), env), sep, sub(e[2], path + (2,), env, tf[2]))
            if tf[3][0] == "base" and not a.is_dynamic(tf[3]) and D(path):
                s = "lift(%s)" % s
            return s
        if tag == "let":
            tx = a.binder[(path, e[1])]
            env2 = {**env, e[1]: tx}
            kw = "_let" if a.is_dynamic(tx) else "let"
            return "(%s %s = %s in %s)" % (kw, e[1], sub(e[2], path + (2,), env, tx),
                                           sub(e[3], path + (3,), env2, t))
        if tag == "if":
            kw = "_if" if a.is_dynamic(a.node[path + (1,)]) else "if"
            return "(%s %s then %s else %s)" % (kw, go(e[1], path + (1,), env),
                                                sub(e[2], path + (2,), env, t), sub(e[3], path + (3,), env, t))
        if tag == "prim":
            op = "_" + e[1] if D(path) else e[1]
            return "(%s %s %s)" % (sub(e[2], path + (2,), env, t), op, sub(e[3], path + (3,), env, t))
        if tag == "fix":
            env2 = {**env, e[1]: a.binder[(path, e[1])], e[2]: a.binder[(path, e[2])]}
            kw = "_fix" if D(path) else "fix"
            return "(%s %s %s -> %s)" % (kw, e[1], e[2], sub(e[3], path + (3,), env2, t[3]))
        raise ValueError("not a term: %r" % (e,))

    env0 = {k[1]: t for k, t in a.binder.items() if k[0] == "in"}
    return go(a.term, (), env0)
