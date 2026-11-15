# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feautrier-scheduling/. The authors are listed in prov/7EMC3G.jsonl.
"""Feautrier's multidimensional affine scheduling (greedy version).

A static control program has statements with polyhedral domains in their
loop counters and the parameters. Each dependence edge e : S -> T is a
polyhedron P_e of pairs (s, t). A schedule gives each statement a list of
affine forms; it is legal when Theta_S(s) <lex Theta_T(t) on every P_e.

One dimension at a time, a linear program finds affine forms theta that
weakly satisfy every remaining edge (theta_T(t) - theta_S(s) >= eps_e with
0 <= eps_e <= 1) and maximizes the sum of the eps_e. Legality on the whole
polyhedron is linear thanks to the affine form of Farkas' lemma. Edges with
eps_e = 1 are strongly satisfied and leave; the rest go to the next
dimension.

Affine forms are dicts from names to Fractions; the key "" is the constant.
A constraint e means e >= 0.
"""

from fractions import Fraction
from itertools import product
from math import gcd, lcm


# ---------------------------------------------------------------- affine forms

def form(d=None, const=0):
    out = {k: Fraction(v) for k, v in (d or {}).items() if v}
    if const:
        out[""] = Fraction(const)
    return out


def F(**kw):
    c = kw.pop("c", 0)
    return form(kw, c)


def add(a, b, k=1):
    out = dict(a)
    for v, c in b.items():
        out[v] = out.get(v, Fraction(0)) + k * c
        if out[v] == 0:
            del out[v]
    return out


def evaluate(a, env):
    return sum((c * (env[v] if v else 1) for v, c in a.items()), Fraction(0))


def rename(a, names):
    return {names.get(v, v): c for v, c in a.items()}


# ------------------------------------------------------- exact simplex method

def _reduce(row):
    g = gcd(*row)
    return [x // g for x in row] if g > 1 else row


def _ints(xs):
    xs = [Fraction(x) for x in xs]
    d = lcm(*[x.denominator for x in xs if x])
    return [int(x * d) if x else 0 for x in xs]


def _update(row, pr, nz, p, k):
    """p * row - k * pr, touching only the nonzero places nz of pr."""
    out = row[:] if p == 1 else [p * x for x in row]
    for t in nz:
        out[t] -= k * pr[t]
    return out if p == 1 else _reduce(out)


def _pivot(rows, obj, basis, r, j):
    pr, p = rows[r], rows[r][j]
    nz = [t for t, y in enumerate(pr) if y]
    for i in range(len(rows)):
        k = rows[i][j]
        if i != r and k:
            rows[i] = _update(rows[i], pr, nz, p, k)
    k = obj[j]
    if k:
        obj[:] = _update(obj, pr, nz, p, k)
    basis[r] = j


def _run(rows, obj, basis, allowed, lexcols):
    """Maximize; obj holds the reduced costs (up to a positive factor) and
    obj[j] > 0 means column j improves. Dantzig's rule picks the largest
    reduced cost, and ties in the ratio test are broken lexicographically on
    the columns `lexcols` (the start basis), which avoids cycling. After a
    fixed number of pivots the run moves to Bland's rule for good, as a second
    guard. Returns False if the problem is unbounded."""
    cap = 50 * (len(rows) + len(obj))
    steps = 0
    while True:
        steps += 1
        if steps > cap:
            j = next((j for j in allowed if obj[j] > 0), None)
        else:
            j = max(allowed, key=lambda j: obj[j], default=None)
            if j is not None and obj[j] <= 0:
                j = None
        if j is None:
            return True
        leave = None
        for r, row in enumerate(rows):
            if row[j] <= 0:
                continue
            if leave is None:
                leave = r
                continue
            a, b = row[j], rows[leave][j]
            if steps > cap:
                lhs, rhs = row[-1] * b, rows[leave][-1] * a
                if lhs < rhs or (lhs == rhs and basis[r] < basis[leave]):
                    leave = r
                continue
            for t in [-1] + list(lexcols):
                lhs, rhs = row[t] * b, rows[leave][t] * a
                if lhs != rhs:
                    if lhs < rhs:
                        leave = r
                    break
        if leave is None:
            return False
        _pivot(rows, obj, basis, leave, j)


def lp_max(c, A, b):
    """Maximize c.x subject to A x = b and x >= 0, in exact arithmetic.
    Returns the list of optimal values (Fractions), or None if infeasible.
    Raises ValueError if the problem is unbounded."""
    m, n = len(A), len(c)
    rows, basis = [], []
    for i in range(m):
        row = _ints(list(A[i]) + [b[i]])
        if row[-1] < 0:
            row = [-x for x in row]
        art = [0] * m
        art[i] = 1
        rows.append(_reduce(row[:n] + art + row[n:]))
        basis.append(n + i)
    # phase 1: maximize -sum(art), reduced costs = sum of rows on non-art cols
    width = n + m + 1
    den = lcm(*[rows[i][n + i] for i in range(m)]) if m else 1
    obj = [0] * width
    for i in range(m):
        f = den // rows[i][n + i]
        for t in range(width):
            if not (n <= t < n + m):
                obj[t] += f * rows[i][t]
    _run(rows, obj, basis, range(n), range(n, n + m))
    if obj[-1] != 0:
        return None
    # drive artificials out of the basis, drop redundant rows
    for r in range(len(rows) - 1, -1, -1):
        if basis[r] >= n:
            j = next((j for j in range(n) if rows[r][j] != 0), None)
            if j is None:
                del rows[r], basis[r]
            else:
                if rows[r][j] < 0:
                    rows[r] = [-x for x in rows[r]]
                _pivot(rows, [0] * width, basis, r, j)
    # phase 2
    cz = _ints(list(c))
    obj = cz[:n] + [0] * m + [0]
    for r in range(len(rows)):
        k = obj[basis[r]]
        if k:
            p = rows[r][basis[r]]
            obj = _reduce([p * x - k * y for x, y in zip(obj, rows[r])])
    if not _run(rows, obj, basis, range(n), range(n, n + m)):
        raise ValueError("unbounded")
    x = [Fraction(0)] * n
    for r, j in enumerate(basis):
        if j < n:
            x[j] = Fraction(rows[r][-1], rows[r][j])
    return x


class LP:
    """A small modelling layer: named variables (free or >= 0), linear
    equalities and inequalities, and an objective to maximize."""

    def __init__(self):
        self.cols = {}          # name -> list of (column, sign)
        self.eqs = []           # (dict name -> coef, rhs)
        self.ncol = 0

    def var(self, name, free=False):
        if name not in self.cols:
            cs = [(self.ncol, 1)]
            self.ncol += 1
            if free:
                cs.append((self.ncol, -1))
                self.ncol += 1
            self.cols[name] = cs
        return name

    def eq(self, coefs, rhs):
        self.eqs.append((dict(coefs), Fraction(rhs)))

    def ge(self, coefs, rhs):
        """sum coefs >= rhs, with a new slack."""
        s = self.var(f"_slack{len(self.eqs)}")
        coefs = dict(coefs)
        coefs[s] = Fraction(-1)
        self.eq(coefs, rhs)

    def maximize(self, objective):
        A, b = [], []
        for coefs, rhs in self.eqs:
            row = [Fraction(0)] * self.ncol
            for v, a in coefs.items():
                for j, sg in self.cols[v]:
                    row[j] += sg * a
            A.append(row)
            b.append(rhs)
        c = [Fraction(0)] * self.ncol
        for v, a in objective.items():
            for j, sg in self.cols[v]:
                c[j] += sg * a
        x = lp_max(c, A, b)
        if x is None:
            return None
        return {v: sum((sg * x[j] for j, sg in cs), Fraction(0)) for v, cs in self.cols.items()}


# ------------------------------------------------------------ static programs

class Stmt:
    def __init__(self, name, iters, betas, domain, write, reads):
        self.name, self.iters, self.betas = name, iters, betas
        self.domain = domain        # forms >= 0 over iters and params
        self.write = write          # (array, [forms])
        self.reads = reads          # list of (array, [forms])

    def theta(self, point):
        out = [self.betas[0]]
        for x, b in zip(point, self.betas[1:]):
            out += [x, b]
        return out


class Program:
    def __init__(self, params, context, stmts):
        self.params, self.context, self.stmts = params, context, stmts
        self.by_name = {s.name: s for s in stmts}


def common_loops(S, T):
    c = 0
    while c < min(len(S.iters), len(T.iters)) and S.betas[c] == T.betas[c]:
        c += 1
    return c


def feasible(cons):
    """Rational feasibility of {x : e(x) >= 0}, with free variables."""
    lp = LP()
    for v in sorted({v for e in cons for v in e if v}):
        lp.var(v, free=True)
    for e in cons:
        lp.ge({v: c for v, c in e.items() if v}, -e.get("", 0))
    return lp.maximize({}) is not None


def dependences(prog):
    """Dependence polyhedra by level: a list of (S, T, constraints) in the
    variables s0.., t0.. and the parameters. A pair (S(s), T(t)) is in it when
    both touch one element, one of them writes it, and S(s) runs first."""
    edges, seen = [], set()
    for S, T in product(prog.stmts, repeat=2):
        sn = {v: f"s{k}" for k, v in enumerate(S.iters)}
        tn = {v: f"t{k}" for k, v in enumerate(T.iters)}
        accs = []
        for (arr, sub) in [S.write] + S.reads:
            for (arr2, sub2) in [T.write] + T.reads:
                if arr == arr2 and ((arr, sub) == S.write or (arr2, sub2) == T.write):
                    accs.append((sub, sub2))
        if not accs:
            continue
        base = [rename(e, sn) for e in S.domain] + [rename(e, tn) for e in T.domain] + list(prog.context)
        c = common_loops(S, T)
        levels = list(range(1, c + 1)) + ([None] if S.betas[c] < T.betas[c] else [])
        for sub, sub2 in accs:
            acc = []
            for a, b in zip(sub, sub2):
                e = add(rename(a, sn), rename(b, tn), -1)
                acc += [e, add({}, e, -1)]
            for l in levels:
                cons = base + acc
                for k in range(c if l is None else l - 1):
                    e = F(**{f"s{k}": 1, f"t{k}": -1})
                    cons += [e, add({}, e, -1)]
                if l is not None:
                    cons.append(F(**{f"t{l - 1}": 1, f"s{l - 1}": -1, "c": -1}))
                key = (S.name, T.name, frozenset(tuple(sorted(e.items())) for e in cons))
                if key not in seen and feasible(cons):
                    seen.add(key)
                    edges.append((S, T, cons))
    return edges


# ------------------------------------------------------- Feautrier scheduling

def coef(S, k, x):
    return f"{S.name}.{x}.{k}"


def theta_terms(prog, S, k, sign, prefix):
    """theta_S at dimension k, renamed: {variable: column name}, as pairs
    (variable or "", column, sign)."""
    out = [(f"{prefix}{j}", coef(S, k, f"i{j}"), sign) for j in range(len(S.iters))]
    out += [(p, coef(S, k, p), sign) for p in prog.params]
    out.append(("", coef(S, k, "c"), sign))
    return out


def farkas(lp, terms, cons, tag, eps):
    """Add: psi - eps = lambda_0 + sum lambda_i c_i, identically in all the
    variables, with lambda >= 0 (the affine form of Farkas' lemma). Here psi
    is an affine form whose coefficients are LP columns, given by `terms`,
    and the c_i >= 0 are the constraints `cons`. Then psi >= eps on cons.
    When both c and -c are in cons, one free multiplier serves the pair."""
    keys = [tuple(sorted(c.items())) for c in cons]
    neg = {tuple(sorted((v, -a) for v, a in c.items())) for c in cons}
    kept, free, seen = [], [], set()
    for c, key in zip(cons, keys):
        if key in seen:
            continue
        seen.add(key)
        if key in neg:
            seen.add(tuple(sorted((v, -a) for v, a in c.items())))
        kept.append(c)
        free.append(key in neg)
    cons = kept
    lams = [lp.var(f"lam.{tag}.{i}", free=f) for i, f in enumerate(free)]
    lam0 = lp.var(f"lam.{tag}.const")
    eq = {}
    for v, col, sg in terms:
        eq.setdefault(v, {})
        eq[v][col] = eq[v].get(col, 0) + sg
    variables = set(eq) | {v for c in cons for v in c}
    for v in variables:
        row = dict(eq.get(v, {}))
        for lam, c in zip(lams, cons):
            if c.get(v):
                row[lam] = row.get(lam, 0) - c[v]
        if v == "":
            row[lam0] = row.get(lam0, 0) - 1
            if eps is not None:
                row[eps] = row.get(eps, 0) - 1
        lp.eq(row, 0)


def edge_terms(prog, e, k):
    S, T, _ = e
    return theta_terms(prog, T, k, 1, "t") + theta_terms(prog, S, k, -1, "s")


def nonnegative(lp, prog, k):
    """theta_S >= 0 on the domain of S, for every statement (Feautrier's
    convention: time starts at 0)."""
    for S in prog.stmts:
        sn = {v: f"s{j}" for j, v in enumerate(S.iters)}
        cons = [rename(c, sn) for c in S.domain] + list(prog.context)
        farkas(lp, theta_terms(prog, S, k, 1, "s"), cons, f"pos.{S.name}", None)


def new_lp(prog, k):
    lp = LP()
    for S in prog.stmts:
        for x in [f"i{j}" for j in range(len(S.iters))] + prog.params + ["c"]:
            lp.var(coef(S, k, x), free=True)
    nonnegative(lp, prog, k)
    return lp


def one_dimension(prog, edges, k):
    """Return (theta, strong): theta maps a statement name to an affine form
    in its iterators and the parameters; strong is the set of edge indices
    that this dimension satisfies strongly."""
    lp = new_lp(prog, k)
    eps = {}
    for idx, e in enumerate(edges):
        eps[idx] = lp.var(f"eps{k}.{idx}")
        lp.ge({eps[idx]: -1}, -1)                                  # eps <= 1
        farkas(lp, edge_terms(prog, e, k), e[2], f"e{idx}", eps[idx])  # @line L4
    sol = lp.maximize({eps[i]: 1 for i in eps})  # @line L5
    strong = {i for i in eps if sol[eps[i]] == 1}
    assert all(sol[eps[i]] in (0, 1) for i in eps)
    # second LP: the same strong set, with the smallest coefficients
    lp2 = new_lp(prog, k)
    absvars = {}
    for S in prog.stmts:
        for x in [f"i{j}" for j in range(len(S.iters))] + prog.params + ["c"]:
            v = coef(S, k, x)
            a = lp2.var("abs." + v)
            lp2.ge({a: 1, v: -1}, 0)
            lp2.ge({a: 1, v: 1}, 0)
            absvars[a] = 1 if x != "c" else Fraction(1, 1000)
    one = lp2.var("one")
    lp2.eq({one: 1}, 1)
    for idx, e in enumerate(edges):
        farkas(lp2, edge_terms(prog, e, k), e[2], f"e{idx}", one if idx in strong else None)
    sol = lp2.maximize({a: -w for a, w in absvars.items()})  # @line L6
    theta = {}
    for S in prog.stmts:
        f = {}
        for j in range(len(S.iters)):
            f[S.iters[j]] = sol[coef(S, k, f"i{j}")]
        for p in prog.params:
            f[p] = sol[coef(S, k, p)]
        f[""] = sol[coef(S, k, "c")]
        theta[S.name] = {v: c for v, c in f.items() if c}
    return theta, strong


def feautrier_schedule(prog):
    """Multidimensional schedule: a dict from statement names to lists of
    affine forms, and the list of strong sets per dimension."""
    edges = dependences(prog)  # @line L1
    left = list(range(len(edges)))
    sched = {S.name: [] for S in prog.stmts}
    report = []
    k = 0
    while left:  # @line L2
        sub = [edges[i] for i in left]  # @line L3
        theta, strong = one_dimension(prog, sub, k)
        assert strong, "no edge satisfied: impossible for a static control program"
        d = lcm(*[c.denominator for f in theta.values() for c in f.values()] or [1])
        for name in sched:  # @line L7
            sched[name].append({v: c * d for v, c in theta[name].items()})
        report.append({left[i] for i in strong})
        left = [left[i] for i in range(len(left)) if i not in strong]  # @line L8
        k += 1  # @line L9
    return sched, edges, report  # @line L10


# ------------------------------------------------------------ brute force

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


def cells(S, p, env):
    e = dict(env)
    e.update(zip(S.iters, p))
    w = (S.write[0],) + tuple(int(evaluate(x, e)) for x in S.write[1])
    rs = [(a,) + tuple(int(evaluate(x, e)) for x in sub) for a, sub in S.reads]
    return w, rs


def brute_dependences(prog, env, box):
    """All pairs of instances (a, b), a before b, that touch one cell with
    at least one write."""
    inst = instances(prog, env, box)
    acc = [cells(S, p, env) for _, S, p in inst]
    out = []
    for x in range(len(inst)):
        wx, rx = acc[x]
        for y in range(x + 1, len(inst)):
            wy, ry = acc[y]
            if wx == wy or wx in ry or wy in rx:
                out.append(((inst[x][1].name, inst[x][2]), (inst[y][1].name, inst[y][2])))
    return out


def schedule_vector(prog, sched, name, point, env):
    S = prog.by_name[name]
    e = dict(env)
    e.update(zip(S.iters, point))
    return tuple(evaluate(f, e) for f in sched[name])


def run(prog, env, box, order_key=None, rng=None):
    """Run the instances in the original order, or sorted by order_key; ties
    are run in a random order (they are the parallel instances)."""
    inst = instances(prog, env, box)
    if order_key is not None:
        if rng is not None:
            rng.shuffle(inst)
        inst.sort(key=lambda x: order_key(x[1].name, x[2]))
    mem = {}
    for _, S, p in inst:
        w, rs = cells(S, p, env)
        val = 7 * prog.stmts.index(S) + sum(p) + 1
        for r in rs:
            val = (3 * val + mem.get(r, hash(r) % 97)) % 1000003
        mem[w] = val
    return mem


def show(sched):
    def fmt(f):
        terms = [(f"{c}*{v}" if c != 1 else v) if v else str(c) for v, c in sorted(f.items(), key=lambda t: (t[0] == "", t[0]))]
        return " + ".join(terms).replace("+ -", "- ") or "0"
    return {n: "(" + ", ".join(fmt(f) for f in fs) + ")" for n, fs in sched.items()}


# ------------------------------------------------------------------ examples

def running_sum():
    """for i = 0 to N: for j = 0 to N: S: s = s + A[i][j]"""
    s = Stmt("S", ["i", "j"], [0, 0, 0], [F(i=1), F(N=1, i=-1), F(j=1), F(N=1, j=-1)],
             ("s", []), [("s", []), ("A", [F(i=1), F(j=1)])])
    return Program(["N"], [F(N=1)], [s])


def matvec():
    """for i = 0 to N-1: S1: y[i] = 0; for j = 0 to i: S2: y[i] += L[i][j] * x[j]"""
    s1 = Stmt("S1", ["i"], [0, 0], [F(i=1), F(N=1, i=-1, c=-1)], ("y", [F(i=1)]), [])
    s2 = Stmt("S2", ["i", "j"], [0, 1, 0], [F(i=1), F(N=1, i=-1, c=-1), F(j=1), F(i=1, j=-1)],
              ("y", [F(i=1)]), [("y", [F(i=1)]), ("L", [F(i=1), F(j=1)]), ("x", [F(j=1)])])
    return Program(["N"], [F(N=1, c=-1)], [s1, s2])


def reverse_copy():
    """for i = 0 to N: S1: x[i] = f(i);  for j = 0 to N: S2: y[j] = x[N - j]"""
    s1 = Stmt("S1", ["i"], [0, 0], [F(i=1), F(N=1, i=-1)], ("x", [F(i=1)]), [])
    s2 = Stmt("S2", ["j"], [1, 0], [F(j=1), F(N=1, j=-1)], ("y", [F(j=1)]), [("x", [F(N=1, j=-1)])])
    return Program(["N"], [F(N=1)], [s1, s2])


def stencil():
    """for i = 1 to N: for j = 1 to N: S: A[i][j] = A[i-1][j] + A[i][j-1]"""
    s = Stmt("S", ["i", "j"], [0, 0, 0], [F(i=1, c=-1), F(N=1, i=-1), F(j=1, c=-1), F(N=1, j=-1)],
             ("A", [F(i=1), F(j=1)]), [("A", [F(i=1, c=-1), F(j=1)]), ("A", [F(i=1), F(j=1, c=-1)])])
    return Program(["N"], [F(N=1, c=-1)], [s])


if __name__ == "__main__":
    for name, prog in [("running sum", running_sum()), ("matvec", matvec()),
                       ("reverse copy", reverse_copy()), ("stencil", stencil())]:
        sched, edges, report = feautrier_schedule(prog)
        print(name, len(edges), "edges", show(sched), [sorted(r) for r in report])
