# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feautrier-array-dataflow/. The authors are listed in prov/61C0MP.jsonl.
"""Feautrier's array dataflow analysis for static control programs.

For a read of an array cell by an instance T(t), the source is the last
instance S(s), in the original order, that wrote that cell before T(t).
The analysis finds it as a quast (a quasi-affine selection tree) in the
coordinates of t and the structure parameters:

  * for each write reference and each depth of common loops, the set of
    candidate sources is a polyhedron in s with parameters (t, N);
  * its lexicographic maximum is found by parametric integer programming
    (PIP), a parametric dual simplex with Gomory cuts, which may add new
    parameters q = floor(e / D);
  * the candidates are combined by keeping, for each value of the
    parameters, the one that runs last.

Affine forms are dicts from variable names to Fractions; the key "" holds
the constant. A constraint is a form e with the meaning e >= 0. Everything is
exact rational arithmetic.

A quast is one of
    ("leaf", None)                     no source: the initial value is read
    ("leaf", (S, [forms]))             the instance S(forms)
    ("if", e, then, else)              e >= 0 ? then : else (e integer-valued)
    ("div", q, e, D, sub)              let q = floor(e / D), then sub
"""

from fractions import Fraction
from itertools import count, product
from math import floor, gcd, lcm

BIG = "M"   # a parameter larger than any other value (big-M, kept symbolic)


# ---------------------------------------------------------------- affine forms

def form(d=None, const=0):
    out = {k: Fraction(v) for k, v in (d or {}).items() if v}
    if const:
        out[""] = out.get("", Fraction(0)) + Fraction(const)
    return out


def add(a, b, k=1):
    out = dict(a)
    for v, c in b.items():
        out[v] = out.get(v, Fraction(0)) + k * c
        if out[v] == 0:
            del out[v]
    return out


def scale(a, k):
    return {v: c * k for v, c in a.items() if c * k != 0}


def evaluate(a, env):
    return sum((c * (env[v] if v else 1) for v, c in a.items()), Fraction(0))


def denom(a):
    return lcm(*[c.denominator for c in a.values()]) if a else 1


def frac(x):
    return x - floor(x)


def rename(a, names):
    return {names.get(v, v): c for v, c in a.items()}


def show_form(a):
    terms = []
    for v in sorted(k for k in a if k):
        c = a[v]
        s = v if c == 1 else f"-{v}" if c == -1 else f"{c}*{v}"
        terms.append(s)
    if a.get("", 0) or not terms:
        terms.append(str(a.get("", 0)))
    return " + ".join(terms).replace("+ -", "- ")


# ------------------------------------------------------------ rational simplex

def _reduce(row):
    g = gcd(*row)
    return [x // g for x in row] if g > 1 else row


def lp_feasible(cons):
    """Is {x : e(x) >= 0 for e in cons} nonempty over the rationals? The
    forms must have integer coefficients. Phase 1 of the simplex method with
    Bland's rule, on integer rows (each row is kept up to a positive factor).
    The variables are free, so each one is split as x = x+ - x-."""
    names = sorted({v for e in cons for v in e if v})
    if all(e.get("", 0) >= 0 for e in cons):
        return True                                  # x = 0 works
    nv, m = len(names), len(cons)
    bad = [r for r, e in enumerate(cons) if e.get("", 0) < 0]
    # columns: x+ (nv), x- (nv), slack (m), artificial (len(bad)), rhs
    width = 2 * nv + m + len(bad) + 1
    rows, basis = [], []
    for r, e in enumerate(cons):
        row = [0] * width
        c = int(e.get("", 0))
        for j, v in enumerate(names):
            a = int(e.get(v, 0))
            row[j], row[nv + j] = a, -a
        if c >= 0:                                   # s = a.x + c, basic
            row = [-x for x in row]
            row[2 * nv + r], row[-1] = 1, c
            basis.append(2 * nv + r)
        else:                                        # a.x - s + art = -c
            k = 2 * nv + m + bad.index(r)
            row[2 * nv + r], row[k], row[-1] = -1, 1, -c
            basis.append(k)
        rows.append(row)
    art0 = 2 * nv + m
    obj = [0] * width                                # reduced costs of sum(art)
    for r in bad:
        obj = [x - y for x, y in zip(obj, rows[r])]
    for j in range(art0, width - 1):
        obj[j] = 0
    while True:
        enter = next((j for j in range(width - 1) if obj[j] < 0), None)
        if enter is None:
            break
        leave = None
        for r in range(m):
            a = rows[r][enter]
            if a > 0:
                if leave is None:
                    leave = r
                    continue
                lhs = rows[r][-1] * rows[leave][enter]
                rhs = rows[leave][-1] * a
                if lhs < rhs or (lhs == rhs and basis[r] < basis[leave]):
                    leave = r
        if leave is None:
            break
        pr = rows[leave]
        p = pr[enter]
        for r in range(m):
            k = rows[r][enter]
            if r != leave and k:
                rows[r] = _reduce([p * x - k * y for x, y in zip(rows[r], pr)])
        k = obj[enter]
        obj = _reduce([p * x - k * y for x, y in zip(obj, pr)])
        basis[leave] = enter
    return obj[-1] == 0


_cache = {}


def tighten(e):
    """Scale e >= 0 to integer coefficients with gcd 1 and round the constant
    down. Every variable here is an integer, so no integer point is lost.
    Returns a sorted tuple of (variable, int) pairs."""
    d = 1
    for c in e.values():
        if c.denominator != 1:
            d = lcm(d, c.denominator)
    ints = {v: c.numerator * (d // c.denominator) for v, c in e.items()}
    g = gcd(*[c for v, c in ints.items() if v])
    if g > 1:
        ints = {v: (c // g) for v, c in ints.items()}   # floor for the constant
    return tuple(sorted((v, c) for v, c in ints.items() if c))


def feasible(cons):
    """Rational feasibility of the tightened system. False means that there
    is no integer point; True may hold with no integer point."""
    key = frozenset(tighten(e) for e in cons)
    if key not in _cache:
        _cache[key] = lp_feasible([dict(k) for k in key])
    return _cache[key]


# --------------------------------------------------------------------- PIP

_names = count()


def sign(c, ctx):
    """'pos' if c >= 0 on the context, 'neg' if c < 0, else 'mixed'.
    The big parameter M decides the sign when it appears."""
    m = c.get(BIG, 0)
    if m:
        return "pos" if m > 0 else "neg"
    d = denom(c)
    if not feasible(ctx + [add(scale(c, -d), form(const=-1))]):
        return "pos"
    if not feasible(ctx + [c]):
        return "neg"
    return "mixed"


def pivot(rows, r, n):
    """Lexicographic dual simplex pivot on row r. Returns False if row r has
    no positive entry (no solution)."""
    cand = [j for j, a in enumerate(rows[r][1]) if a > 0]
    if not cand:
        return False
    key = lambda j: [row[1][j] / rows[r][1][j] for row in rows]
    j = min(cand, key=key)
    arj = rows[r][1][j]
    cr, ar = rows[r][0], rows[r][1]
    for i, (ci, ai) in enumerate(rows):
        aij = ai[j]
        if aij == 0:
            continue
        f = aij / arj
        newc = add(ci, cr, -f)
        newa = [a - f * b for a, b in zip(ai, ar)]
        newa[j] = f
        rows[i] = (newc, newa)
    return True


def pip(rows, n, ctx, depth=0, divs=()):
    """Lexicographic minimum of the n unknowns (rows 0..n-1), all >= 0 and
    integer, subject to every row >= 0, as a quast in the parameters.
    `divs` lists the parameters (q, numerator, d) with q = floor(num / d)
    already defined on this path."""
    if not feasible(ctx):  # @line L8
        return ("leaf", None)
    if depth > 80:
        raise RuntimeError("PIP: too deep")
    rows = [(dict(c), list(a)) for c, a in rows]
    while True:
        mixed = None
        for r, (c, a) in enumerate(rows):
            s = sign(c, ctx)
            if s == "neg":
                break
            if s == "mixed" and mixed is None:
                mixed = r
        else:
            r = None
        if r is not None:  # @line L9
            if not pivot(rows, r, n):
                return ("leaf", None)
            continue
        if mixed is not None:  # @line L10
            c = rows[mixed][0]
            e = scale(c, denom(c))
            yes = pip(rows, n, ctx + [e], depth + 1, divs)
            no = pip(rows, n, ctx + [add(scale(e, -1), form(const=-1))], depth + 1, divs)
            return ("if", e, yes, no)
        k = next((k for k in range(n)  # @line L11
                  if any(v.denominator != 1 for v in rows[k][0].values())), None)
        if k is None:
            return ("leaf", [rows[k][0] for k in range(n)])  # @line L12
        c = rows[k][0]
        assert c.get(BIG, Fraction(0)).denominator == 1
        fc = {v: frac(x) for v, x in c.items() if v != BIG and frac(x)}
        # x = c + sum a_j n_j with x and all n_j integer gives the cut
        # sum frac(-a_j) n_j >= frac(c)
        cut_a = [frac(-x) for x in rows[k][1]]
        if not any(fc.get(v) for v in fc if v):
            # a constant fraction: the classic Gomory cut
            rows.append((form(const=-fc[""]), cut_a))  # @line L13
            return pip(rows, n, ctx, depth + 1, divs)
        d = denom(fc)
        num = scale(fc, d)                          # integer-valued numerator
        old = next((q for q, nm, dd in divs if dd == d and nm == num), None)
        if old is not None:
            if not feasible(ctx + [add(num, form({old: -d}, -1))]):
                # the context forces num = d * q, so the fraction is zero
                rows[k] = (add(add(c, fc, -1), form({old: 1})), rows[k][1])
                return pip(rows, n, ctx, depth + 1, divs)
            rows.append((add(form({old: 1}), fc, -1), cut_a))
            return pip(rows, n, ctx, depth + 1, divs)
        q = f"q{next(_names)}"
        ctx2 = ctx + [add(num, form({q: -d})), add(form({q: d}, d - 1), num, -1)]
        rows.append((add(form({q: 1}), fc, -1), cut_a))  # @line L14
        return ("div", q, num, d, pip(rows, n, ctx2, depth + 1, divs + ((q, num, d),)))


def lexmax(svars, cons, ctx):
    """Parametric lexmax of the integer points s with cons(s, params) >= 0.
    Uses x_k = M - s_k >= 0 and the lexicographic minimum of x."""
    n = len(svars)
    rows = []
    for k in range(n):
        a = [Fraction(0)] * n
        a[k] = Fraction(1)
        rows.append((form(), a))
    for e in cons:
        a = [-e.get(v, Fraction(0)) for v in svars]
        c = {v: x for v, x in e.items() if v not in svars}
        msum = sum((e.get(v, Fraction(0)) for v in svars), Fraction(0))
        if msum:
            c[BIG] = c.get(BIG, Fraction(0)) + msum
        rows.append((c, a))
    return map_leaves(pip(rows, n, ctx), lambda xs: [add(form({BIG: 1}), x, -1) for x in xs])


def map_leaves(t, f):
    if t[0] == "leaf":
        if t[1] is None:
            return t
        out = f(t[1])
        for e in out:
            assert BIG not in e, "lexmax is unbounded"
        return ("leaf", out)
    if t[0] == "if":
        return ("if", t[1], map_leaves(t[2], f), map_leaves(t[3], f))
    return ("div", t[1], t[2], t[3], map_leaves(t[4], f))


# ------------------------------------------------------------ static programs

class Stmt:
    """A statement inside loops with iterators `iters`. `betas` has length
    len(iters) + 1 and gives the textual position at each depth, so the
    original schedule is (betas[0], i1, betas[1], i2, ..., betas[d])."""

    def __init__(self, name, iters, betas, domain, write, reads):
        self.name, self.iters, self.betas = name, iters, betas
        self.domain = domain        # list of forms >= 0 over iters and params
        self.write = write          # (array, [forms])
        self.reads = reads          # list of (array, [forms])

    def theta(self, point):
        out = [self.betas[0]]
        for x, b in zip(point, self.betas[1:]):
            out += [x, b]
        return out


class Program:
    def __init__(self, params, context, stmts):
        self.params = params        # names of the structure parameters
        self.context = context      # forms >= 0 over the parameters
        self.stmts = stmts
        self.by_name = {s.name: s for s in stmts}


def common_loops(S, T):
    c = 0
    while c < min(len(S.iters), len(T.iters)) and S.betas[c] == T.betas[c]:
        c += 1
    return c


def theta_forms(S, sforms):
    out = [form(const=S.betas[0])]
    for x, b in zip(sforms, S.betas[1:]):
        out += [x, form(const=b)]
    return out


def split3(e, ctx, pos, neg, zero):
    """Build a quast on the sign of the form e: pos(ctx), neg(ctx), zero(ctx)."""
    d = denom(e)
    e = scale(e, d)
    gt = add(e, form(const=-1))                   # e >= 1
    lt = add(scale(e, -1), form(const=-1))        # e <= -1
    eq = [e, scale(e, -1)]
    branches = []
    if feasible(ctx + [gt]):
        branches.append((gt, pos(ctx + [gt])))
    if feasible(ctx + [lt]):
        branches.append((lt, neg(ctx + [lt])))
    if feasible(ctx + eq):
        branches.append((None, zero(ctx + eq)))
    if not branches:
        return ("leaf", None)
    tree = branches[-1][1]
    for cond, sub in reversed(branches[:-1]):
        tree = ("if", cond, sub, tree)
    return tree


def later(prog, a, b, ctx):
    """Quast that picks, of the leaves a and b, the one that runs later."""
    if a is None:
        return ("leaf", b)
    if b is None:
        return ("leaf", a)
    ta = theta_forms(prog.by_name[a[0]], a[1])
    tb = theta_forms(prog.by_name[b[0]], b[1])

    def cmp(k, ctx):
        if k >= min(len(ta), len(tb)):
            return ("leaf", a)
        return split3(add(tb[k], ta[k], -1), ctx,
                      lambda c: ("leaf", b), lambda c: ("leaf", a), lambda c: cmp(k + 1, c))
    return cmp(0, ctx)


def merge(prog, q1, q2, ctx):
    """For each parameter value, the later of the sources given by q1 and q2."""
    if not feasible(ctx):
        return ("leaf", None)
    if q1[0] == "if":
        e = q1[1]
        no = add(scale(e, -1), form(const=-1))
        return ("if", e, merge(prog, q1[2], q2, ctx + [e]), merge(prog, q1[3], q2, ctx + [no]))
    if q1[0] == "div":
        _, q, num, d, sub = q1
        ctx2 = ctx + [add(num, form({q: -d})), add(form({q: d}, d - 1), num, -1)]
        return ("div", q, num, d, merge(prog, sub, q2, ctx2))
    if q2[0] == "if":
        e = q2[1]
        no = add(scale(e, -1), form(const=-1))
        return ("if", e, merge(prog, q1, q2[2], ctx + [e]), merge(prog, q1, q2[3], ctx + [no]))
    if q2[0] == "div":
        _, q, num, d, sub = q2
        ctx2 = ctx + [add(num, form({q: -d})), add(form({q: d}, d - 1), num, -1)]
        return ("div", q, num, d, merge(prog, q1, sub, ctx2))
    return later(prog, q1[1], q2[1], ctx)


def source(prog, T, ref):
    """The quast of the source of read reference `ref` of statement T, in
    the variables t0, t1, ... (the instance of T) and the parameters."""
    arr, subs = ref
    tn = {v: f"t{k}" for k, v in enumerate(T.iters)}
    tsubs = [rename(e, tn) for e in subs]
    ctx = [rename(e, tn) for e in T.domain] + list(prog.context)
    quast = ("leaf", None)  # @line L1
    for S in prog.stmts:  # @line L2
        if S.write[0] != arr:
            continue
        sn = {v: f"s{k}" for k, v in enumerate(S.iters)}
        svars = [f"s{k}" for k in range(len(S.iters))]
        base = [rename(e, sn) for e in S.domain]
        for a, b in zip(S.write[1], tsubs):
            eq = add(rename(a, sn), b, -1)
            base += [eq, scale(eq, -1)]
        c = common_loops(S, T)
        levels = list(range(1, c + 1))
        if S.betas[c] < T.betas[c]:
            levels.append(None)                   # loop independent
        for l in levels:  # @line L3
            cons = list(base)
            for k in range((c if l is None else l - 1)):
                e = form({svars[k]: 1, f"t{k}": -1})
                cons += [e, scale(e, -1)]
            if l is not None:
                cons.append(form({f"t{l - 1}": 1, svars[l - 1]: -1}, -1))  # @line L4
            cand = lexmax(svars, cons, ctx)  # @line L5
            quast = simplify(merge(prog, quast, tag(cand, S.name), ctx), ctx)  # @line L6
    return quast  # @line L7


def tag(t, name):
    if t[0] == "leaf":
        return t if t[1] is None else ("leaf", (name, t[1]))
    if t[0] == "if":
        return ("if", t[1], tag(t[2], name), tag(t[3], name))
    return ("div", t[1], t[2], t[3], tag(t[4], name))


def eval_quast(t, env):
    """The source at a concrete point: None or (statement, tuple of ints)."""
    env = dict(env)
    while True:
        if t[0] == "leaf":
            if t[1] is None:
                return None
            name, xs = t[1]
            vals = [evaluate(e, env) for e in xs]
            assert all(v.denominator == 1 for v in vals)
            return name, tuple(int(v) for v in vals)
        if t[0] == "if":
            t = t[2] if evaluate(t[1], env) >= 0 else t[3]
        else:
            _, q, num, d, sub = t
            env[q] = floor(evaluate(num, env) / d)
            t = sub


def same_leaf(a, b, ctx):
    """Do two leaves name the same instance for every point of the context?"""
    if a is None or b is None:
        return a is b
    if a[0] != b[0]:
        return False
    for x, y in zip(a[1], b[1]):
        d = add(x, y, -1)
        if feasible(ctx + [add(d, form(const=-1))]) or \
                feasible(ctx + [add(scale(d, -1), form(const=-1))]):
            return False
    return True


def agree(a, b, ctx):
    """Do the quasts a and b give the same instance at every point of ctx?
    The test is sound but may answer False when the answer is True."""
    if not feasible(ctx):
        return True
    for x, y in ((a, b), (b, a)):
        if x[0] == "if":
            e = x[1]
            no = add(scale(e, -1), form(const=-1))
            return agree(x[2], y, ctx + [e]) and agree(x[3], y, ctx + [no])
        if x[0] == "div":
            _, q, num, d, sub = x
            ctx2 = ctx + [add(num, form({q: -d})), add(form({q: d}, d - 1), num, -1)]
            return agree(sub, y, ctx2)
    return same_leaf(a[1], b[1], ctx)


def simplify(t, ctx=()):
    """Drop branches that the context makes empty, and conditions whose two
    branches give the same instance on the context."""
    ctx = list(ctx)
    if t[0] == "if":
        e = t[1]
        no = add(scale(e, -1), form(const=-1))
        if not feasible(ctx + [e]):
            return simplify(t[3], ctx)
        if not feasible(ctx + [no]):
            return simplify(t[2], ctx)
        a, b = simplify(t[2], ctx + [e]), simplify(t[3], ctx + [no])
        if a == b or agree(a, b, ctx + [e]):
            return b
        if agree(a, b, ctx + [no]):
            return a
        return ("if", e, a, b)
    if t[0] == "div":
        _, q, num, d, sub = t
        ctx2 = ctx + [add(num, form({q: -d})), add(form({q: d}, d - 1), num, -1)]
        sub = simplify(sub, ctx2)
        return sub if q not in repr(sub) else ("div", q, num, d, sub)
    return t


def show(t, indent=0):
    pad = "  " * indent
    if t[0] == "leaf":
        if t[1] is None:
            return [pad + "no source (initial value)"]
        name, xs = t[1]
        return [pad + f"{name}[{', '.join(show_form(e) for e in xs)}]"]
    if t[0] == "if":
        return ([pad + f"if {show_form(t[1])} >= 0:"] + show(t[2], indent + 1)
                + [pad + "else:"] + show(t[3], indent + 1))
    return [pad + f"let {t[1]} = floor(({show_form(t[2])}) / {t[3]})"] + show(t[4], indent)


# --------------------------------------------------------------- brute force

def instances(prog, env, box):
    out = []
    for S in prog.stmts:
        for p in product(range(-box, box + 1), repeat=len(S.iters)):
            e = dict(env)
            e.update(zip(S.iters, p))
            if all(evaluate(c, e) >= 0 for c in S.domain):
                out.append((S.theta(p), S, p))
    out.sort(key=lambda x: x[0])
    return out


def brute_sources(prog, env, box):
    """Map (T, read index, t) to the last writer of the cell before T(t)."""
    last, out = {}, {}
    for _, S, p in instances(prog, env, box):
        e = dict(env)
        e.update(zip(S.iters, p))
        for r, (arr, subs) in enumerate(S.reads):
            cell = (arr,) + tuple(evaluate(x, e) for x in subs)
            out[(S.name, r, p)] = last.get(cell)
        arr, subs = S.write
        last[(arr,) + tuple(evaluate(x, e) for x in subs)] = (S.name, p)
    return out


# ------------------------------------------------------------------ examples

def F(**kw):
    c = kw.pop("c", 0)
    return form(kw, c)


def matvec():
    """for i = 0 to N-1: S1: y[i] = 0; for j = 0 to i: S2: y[i] = y[i] + L[i][j] * x[j]"""
    s1 = Stmt("S1", ["i"], [0, 0], [F(i=1), F(N=1, i=-1, c=-1)], ("y", [F(i=1)]), [])
    s2 = Stmt("S2", ["i", "j"], [0, 1, 0], [F(i=1), F(N=1, i=-1, c=-1), F(j=1), F(i=1, j=-1)],
              ("y", [F(i=1)]), [("y", [F(i=1)]), ("L", [F(i=1), F(j=1)]), ("x", [F(j=1)])])
    return Program(["N"], [F(N=1, c=-1)], [s1, s2])


def even_writes():
    """for i = 0 to N: S1: A[2i] = ...;  for j = 0 to 2N: S2: B[j] = A[j]"""
    s1 = Stmt("S1", ["i"], [0, 0], [F(i=1), F(N=1, i=-1)], ("A", [F(i=2)]), [])
    s2 = Stmt("S2", ["j"], [1, 0], [F(j=1), F(N=2, j=-1)], ("B", [F(j=1)]), [("A", [F(j=1)])])
    return Program(["N"], [F(N=1)], [s1, s2])


def diagonal():
    """for i = 0 to N: for j = 0 to N: S: A[i+j] = A[i+j] + 1"""
    s = Stmt("S", ["i", "j"], [0, 0, 0], [F(i=1), F(N=1, i=-1), F(j=1), F(N=1, j=-1)],
             ("A", [F(i=1, j=1)]), [("A", [F(i=1, j=1)])])
    return Program(["N"], [F(N=1)], [s])


if __name__ == "__main__":
    for name, prog, T, r in [("matvec", matvec(), "S2", 0), ("even", even_writes(), "S2", 0),
                             ("diagonal", diagonal(), "S", 0)]:
        print(name)
        print("\n".join(show(source(prog, prog.by_name[T], prog.by_name[T].reads[r]), 1)))
