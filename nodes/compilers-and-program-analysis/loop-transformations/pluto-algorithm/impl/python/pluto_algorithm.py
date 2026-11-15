# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pluto-algorithm/. The authors are listed in prov/8AZ5A6.jsonl.
"""The Pluto algorithm (Bondhugula, Hartono, Ramanujam and Sadayappan, 2008).

Pluto looks for tiling hyperplanes: one affine form phi_S(i) = c_S . i + c_S0
per statement, with c >= 0, such that every dependence e : S -> T that is not
yet satisfied has

    phi_T(t) - phi_S(s) >= 0           on P_e   (legal for tiling)
    u . N + w - (phi_T(t) - phi_S(s)) >= 0   on P_e   (the cost bound)

Both are made linear by the affine form of Farkas' lemma. Among the integer
solutions it takes the lexicographic minimum of (u, w, sum of c, sum of
constants), by branch and bound over an exact simplex method. Hyperplanes
found one after the other form a band. A new hyperplane must be linearly
independent of the earlier ones of each statement; Pluto asks for a
nonnegative component in the orthogonal complement. When no hyperplane is
found, the band closes and the dependences it satisfies leave. If none leave,
the statements are split by the strongly connected components of the
dependence graph.

Affine forms are dicts from names to Fractions; the key "" is the constant.
A constraint e means e >= 0.
"""

from fractions import Fraction
from itertools import product
from math import floor, gcd, lcm

COEF_MAX = 4      # bounds on the integer unknowns keep branch and bound finite
U_MAX = 4
W_MAX = 30


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
    """Maximize; obj[j] > 0 means column j improves. Dantzig's rule with a
    lexicographic ratio test on the start basis columns, which cannot cycle;
    after a fixed number of pivots, Bland's rule as a second guard. Returns
    False if the problem is unbounded."""
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
    Returns the optimal values, None if infeasible; raises ValueError if the
    problem is unbounded."""
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
    for r in range(len(rows) - 1, -1, -1):
        if basis[r] >= n:
            j = next((j for j in range(n) if rows[r][j] != 0), None)
            if j is None:
                del rows[r], basis[r]
            else:
                if rows[r][j] < 0:
                    rows[r] = [-x for x in rows[r]]
                _pivot(rows, [0] * width, basis, r, j)
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
    """Named variables (free or >= 0), linear equalities and inequalities,
    and an objective to maximize."""

    def __init__(self):
        self.cols, self.eqs, self.ncol = {}, [], 0

    def copy(self):
        other = LP()
        other.cols, other.eqs, other.ncol = dict(self.cols), list(self.eqs), self.ncol
        return other

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


def ilp_min(lp, obj, ints):
    """Minimize obj (integer coefficients on integer variables) with the
    variables `ints` integer, by depth-first branch and bound. The integer
    variables must be bounded. Returns (value, solution) or (None, None)."""
    best, best_sol = None, None
    stack = [[]]
    while stack:
        extra = stack.pop()
        cur = lp.copy()
        for v, lo, val in extra:
            if lo:
                cur.ge({v: 1}, val)
            else:
                cur.ge({v: -1}, -val)
        sol = cur.maximize({k: -c for k, c in obj.items()})
        if sol is None:
            continue
        val = sum(c * sol[k] for k, c in obj.items())
        if best is not None and -floor(-val) >= best:
            continue
        x = next((v for v in ints if sol[v].denominator != 1), None)
        if x is None:
            best, best_sol = val, sol
            continue
        f = floor(sol[x])
        stack.append(extra + [(x, True, f + 1)])
        stack.append(extra + [(x, False, f)])
    return best, best_sol


def ilp_lexmin(lp, objectives, ints):
    """Lexicographic minimum: minimize each objective in turn and fix it."""
    lp, sol = lp.copy(), None
    for obj in objectives:
        best, sol = ilp_min(lp, obj, ints)
        if best is None:
            return None
        lp.eq(obj, best)
    return sol


def min_over(f, cons):
    """The rational minimum of the affine form f on {x : c(x) >= 0}, or None
    if it is unbounded below."""
    lp = LP()
    for v in sorted({v for e in cons + [f] for v in e if v}):
        lp.var(v, free=True)
    for e in cons:
        lp.ge({v: c for v, c in e.items() if v}, -e.get("", 0))
    try:
        sol = lp.maximize({v: -c for v, c in f.items() if v})
    except ValueError:
        return None
    return evaluate(f, {v: sol.get(v, 0) for v in f if v})


# ------------------------------------------------------------ static programs

class Stmt:
    def __init__(self, name, iters, betas, domain, write, reads):
        self.name, self.iters, self.betas = name, iters, betas
        self.domain = domain        # forms >= 0 over iters and params
        self.write = write          # (array, [forms])
        self.reads = reads          # list of (array, [forms])

    def theta(self, point):
        """The original schedule vector (beta_0, i_1, beta_1, ...)."""
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
    lp = LP()
    for v in sorted({v for e in cons for v in e if v}):
        lp.var(v, free=True)
    for e in cons:
        lp.ge({v: c for v, c in e.items() if v}, -e.get("", 0))
    return lp.maximize({}) is not None


def dependences(prog):
    """Dependence polyhedra by depth: a list of (S, T, constraints, p) in the
    variables s0.., t0.. and the parameters, where p is the place of the
    original schedule vector that orders the pair (counted from 1)."""
    edges, seen = [], set()
    for S, T in product(prog.stmts, repeat=2):
        sn = {v: f"s{k}" for k, v in enumerate(S.iters)}
        tn = {v: f"t{k}" for k, v in enumerate(T.iters)}
        accs = []
        for (arr, sub) in [S.write] + S.reads:
            for (arr2, sub2) in [T.write] + T.reads:
                if arr == arr2 and ((arr, sub) == S.write or (arr2, sub2) == T.write):
                    accs.append((sub, sub2))
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
                    edges.append((S, T, cons, 2 * c + 1 if l is None else 2 * l))
    return edges


# ------------------------------------------------------------ Farkas and ILP

def farkas(lp, terms, cons, tag):
    """Add psi >= 0 on {c >= 0 for c in cons}, where psi = sum of
    sign * column * variable over `terms`, as the identity
    psi = lambda_0 + sum lambda_i c_i with lambda >= 0 (affine Farkas
    lemma). A pair c, -c gets one free multiplier."""
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
    lams = [lp.var(f"lam.{tag}.{i}", free=f) for i, f in enumerate(free)]
    lam0 = lp.var(f"lam.{tag}.const")
    eq = {}
    for v, col, sg in terms:
        eq.setdefault(v, {})
        eq[v][col] = eq[v].get(col, 0) + sg
    for v in set(eq) | {v for c in kept for v in c}:
        row = dict(eq.get(v, {}))
        for lam, c in zip(lams, kept):
            if c.get(v):
                row[lam] = row.get(lam, 0) - c[v]
        if v == "":
            row[lam0] = row.get(lam0, 0) - 1
        lp.eq(row, 0)


def coef(S, j):
    return f"{S.name}.c{j}"


def const(S):
    return f"{S.name}.c0"


def phi_terms(S, prefix, sign):
    out = [(f"{prefix}{j}", coef(S, j + 1), sign) for j in range(len(S.iters))]
    out.append(("", const(S), sign))
    return out


def orthogonal_rows(H, d):
    """Integer rows spanning the orthogonal complement of the rows of H in
    Q^d: the nonzero rows of I - H^T (H H^T)^{-1} H, scaled to integers."""
    r = len(H)
    M = [[sum(Fraction(H[a][k]) * H[b][k] for k in range(d)) for b in range(r)] for a in range(r)]
    inv = [[Fraction(int(a == b)) for b in range(r)] for a in range(r)]
    for col in range(r):                       # Gauss-Jordan on M
        piv = next(i for i in range(col, r) if M[i][col] != 0)
        M[col], M[piv], inv[col], inv[piv] = M[piv], M[col], inv[piv], inv[col]
        p = M[col][col]
        M[col] = [x / p for x in M[col]]
        inv[col] = [x / p for x in inv[col]]
        for i in range(r):
            if i != col and M[i][col] != 0:
                k = M[i][col]
                M[i] = [x - k * y for x, y in zip(M[i], M[col])]
                inv[i] = [x - k * y for x, y in zip(inv[i], inv[col])]
    out = []
    for a in range(d):
        row = []
        for b in range(d):
            s = sum(H[x][a] * inv[x][y] * H[y][b] for x in range(r) for y in range(r))
            row.append(Fraction(int(a == b)) - s)
        if any(row):
            ints = _reduce(_ints(row))
            if ints not in out:
                out.append(ints)
    return out


def find_hyperplane(prog, edges, H):
    """One ILP: the lexmin of (u, w, sum c, sum c0) over legal, bounded,
    independent hyperplanes. Returns ({S: form}, u, w) or None."""
    lp = LP()
    ints = ["u", "w"]
    lp.var("u")
    lp.var("w")
    lp.ge({"u": -1}, -U_MAX)
    lp.ge({"w": -1}, -W_MAX)
    loop_sum, const_sum = {}, {}
    for S in prog.stmts:
        cs = [coef(S, j + 1) for j in range(len(S.iters))] + [const(S)]
        for v in cs:
            lp.var(v)
            lp.ge({v: -1}, -COEF_MAX)
            ints.append(v)
        for v in cs[:-1]:
            loop_sum[v] = 1
        const_sum[const(S)] = 1
        d = len(S.iters)
        if len(H[S.name]) < d:
            rows = orthogonal_rows(H[S.name], d) if H[S.name] else [[1] * d]
            for h in rows:
                lp.ge({coef(S, j + 1): h[j] for j in range(d) if h[j]}, 0)
            total = {}
            for h in rows:
                for j in range(d):
                    total[coef(S, j + 1)] = total.get(coef(S, j + 1), 0) + h[j]
            lp.ge({v: a for v, a in total.items() if a}, 1)
    for idx, (S, T, cons, _) in enumerate(edges):
        delta = phi_terms(T, "t", 1) + phi_terms(S, "s", -1)
        farkas(lp, delta, cons, f"leg{idx}")
        bound = [("N", "u", 1), ("", "w", 1)] + [(v, c, -sg) for v, c, sg in delta]
        farkas(lp, bound, cons, f"cost{idx}")
    # The unknowns are bounded integers, so the lexicographic minimum of
    # (u, w, sum c, sum c0, tie) is the minimum of one weighted sum: each
    # weight is larger than the largest value of everything after it. The
    # last term, sum of (depth - 1) * c, breaks ties toward the original
    # loop order.
    tie = {coef(S, j + 1): j for S in prog.stmts for j in range(1, len(S.iters))}
    w4 = COEF_MAX * sum(tie.values()) + 1
    w3 = w4 * (COEF_MAX * len(const_sum) + 1)
    w2 = w3 * (COEF_MAX * len(loop_sum) + 1)
    w1 = w2 * (W_MAX + 1)
    obj = {"u": w1, "w": w2}
    obj.update({v: w3 + tie.get(v, 0) for v in loop_sum})
    obj.update({v: w4 for v in const_sum})
    sol = ilp_lexmin(lp, [obj], ints)
    if sol is None:
        return None
    phi = {}
    for S in prog.stmts:
        f = {S.iters[j]: sol[coef(S, j + 1)] for j in range(len(S.iters))}
        f[""] = sol[const(S)]
        phi[S.name] = {v: c for v, c in f.items() if c}
    return phi, int(sol["u"]), int(sol["w"])


def delta_form(phi, e):
    S, T, _, _ = e
    sn = {v: f"s{k}" for k, v in enumerate(S.iters)}
    tn = {v: f"t{k}" for k, v in enumerate(T.iters)}
    return add(rename(phi[T.name], tn), rename(phi[S.name], sn), -1)


def strongly(phi, e):
    """phi_T - phi_S >= 1 on the integer points of P_e. The difference is an
    integer there, so a positive rational minimum is enough."""
    m = min_over(delta_form(phi, e), e[2])
    return m is not None and m > 0


def scc_order(names, edges):
    """Tarjan's algorithm on the statement graph; returns a map from a name
    to the index of its component in topological order."""
    succ = {n: [] for n in names}
    for S, T, _, _ in edges:
        succ[S.name].append(T.name)
    index, low, stack, on, comps = {}, {}, [], set(), []

    def visit(v):
        index[v] = low[v] = len(index)
        stack.append(v)
        on.add(v)
        for w in succ[v]:
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = set()
            while True:
                w = stack.pop()
                on.discard(w)
                comp.add(w)
                if w == v:
                    break
            comps.append(comp)

    for v in names:
        if v not in index:
            visit(v)
    comps.reverse()             # Tarjan finds sinks first
    return {v: k for k, comp in enumerate(comps) for v in comp}


def original_component(prog, p):
    """Place p (from 1) of the original schedule vector, as an affine form
    per statement; 0 for statements whose vector is shorter."""
    out = {}
    for S in prog.stmts:
        if p <= 2 * len(S.iters) + 1:
            out[S.name] = F(**{S.iters[p // 2 - 1]: 1}) if p % 2 == 0 else form({}, S.betas[(p - 1) // 2])
        else:
            out[S.name] = {}
    return out


def pluto(prog):
    """Returns (dims, bands, edges). dims is a list of dicts with keys
    'phi' ({S: form}), 'kind' ('hyperplane', 'scalar', 'original' or
    'complete'), and 'u', 'w' for hyperplanes. bands lists the index lists
    of the bands of hyperplanes."""
    all_edges = dependences(prog)
    E = list(all_edges)  # @line L1
    H = {S.name: [] for S in prog.stmts}
    dims, bands, band = [], [], []

    def close():
        nonlocal E, band
        if band:
            bands.append(band)
            E = [e for e in E if not any(strongly(dims[k]["phi"], e) for k in band)]
        band = []

    while E or any(len(H[S.name]) < len(S.iters) for S in prog.stmts):  # @line L2
        found = None
        if any(len(H[S.name]) < len(S.iters) for S in prog.stmts):
            found = find_hyperplane(prog, E, H)  # @line L3
        if found:
            phi, u, w = found
            for S in prog.stmts:  # @line L4
                if len(H[S.name]) < len(S.iters):
                    H[S.name].append([phi[S.name].get(x, 0) for x in S.iters])
            band.append(len(dims))
            dims.append({"phi": phi, "kind": "hyperplane", "u": u, "w": w})
            continue
        if band:
            close()  # @line L5
            continue
        order = scc_order([S.name for S in prog.stmts], E)
        cross = [e for e in E if order[e[0].name] != order[e[1].name]]
        if cross:  # @line L6
            dims.append({"phi": {S.name: form({}, order[S.name]) for S in prog.stmts}, "kind": "scalar"})
            E = [e for e in E if e not in cross]
        elif E:  # @line L7
            phi = original_component(prog, min(e[3] for e in E))
            dims.append({"phi": phi, "kind": "original"})
            E = [e for e in E if not strongly(phi, e)]
        else:  # @line L8
            phi = {}
            for S in prog.stmts:
                phi[S.name] = {}
                for x in S.iters:
                    rows = H[S.name] + [[int(y == x) for y in S.iters]]
                    if len(H[S.name]) < len(S.iters) and rank(rows) == len(rows):
                        H[S.name].append(rows[-1])
                        phi[S.name] = F(**{x: 1})
                        break
            band.append(len(dims))
            dims.append({"phi": phi, "kind": "complete", "u": 0, "w": 0})
    close()  # @line L9
    return dims, bands, all_edges  # @line L10


def rank(rows):
    m = [[Fraction(x) for x in r] for r in rows]
    rk = 0
    for col in range(len(m[0]) if m else 0):
        piv = next((i for i in range(rk, len(m)) if m[i][col] != 0), None)
        if piv is None:
            continue
        m[rk], m[piv] = m[piv], m[rk]
        for i in range(len(m)):
            if i != rk and m[i][col] != 0:
                k = m[i][col] / m[rk][col]
                m[i] = [x - k * y for x, y in zip(m[i], m[rk])]
        rk += 1
    return rk


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


def time_vector(prog, dims, name, point, env, bands=(), tile=None):
    """The new time of an instance. With a tile size, each band of two or
    more hyperplanes gets tile coordinates floor(phi / tile) in front."""
    S = prog.by_name[name]
    e = dict(env)
    e.update(zip(S.iters, point))
    vals = [evaluate(d["phi"][name], e) for d in dims]
    if tile is None:
        return tuple(vals)
    starts = {b[0]: b for b in bands if len(b) >= 2}
    out = []
    for k, v in enumerate(vals):
        if k in starts:
            out += [floor(vals[j] / tile) for j in starts[k]]
        out.append(v)
    return tuple(out)


def run(prog, env, box, order_key=None, rng=None):
    """Run the instances in the original order, or sorted by order_key with
    ties in a random order."""
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


def show(dims):
    def fmt(f):
        terms = [(f"{c}*{v}" if c != 1 else v) if v else str(c)
                 for v, c in sorted(f.items(), key=lambda t: (t[0] == "", t[0]))]
        return " + ".join(terms).replace("+ -", "- ") or "0"
    names = list(dims[0]["phi"]) if dims else []
    return {n: "(" + ", ".join(fmt(d["phi"][n]) for d in dims) + ")" for n in names}


# ------------------------------------------------------------------ examples

def seidel():
    """for t = 0 to N: for i = 1 to N - 1: A[i] = (A[i-1] + A[i] + A[i+1]) / 3"""
    s = Stmt("S", ["t", "i"], [0, 0, 0], [F(t=1), F(N=1, t=-1), F(i=1, c=-1), F(N=1, i=-1, c=-1)],
             ("A", [F(i=1)]), [("A", [F(i=1, c=-1)]), ("A", [F(i=1)]), ("A", [F(i=1, c=1)])])
    return Program(["N"], [F(N=1, c=-2)], [s])


def stencil():
    """for i = 1 to N: for j = 1 to N: A[i][j] = A[i-1][j] + A[i][j-1]"""
    s = Stmt("S", ["i", "j"], [0, 0, 0], [F(i=1, c=-1), F(N=1, i=-1), F(j=1, c=-1), F(N=1, j=-1)],
             ("A", [F(i=1), F(j=1)]), [("A", [F(i=1, c=-1), F(j=1)]), ("A", [F(i=1), F(j=1, c=-1)])])
    return Program(["N"], [F(N=1, c=-1)], [s])


def producer_consumer():
    """for i = 1 to N: S1: B[i] = A[i];  for i = 1 to N: S2: C[i] = B[i-1] + B[i+1]"""
    s1 = Stmt("S1", ["i"], [0, 0], [F(i=1, c=-1), F(N=1, i=-1)], ("B", [F(i=1)]), [("A", [F(i=1)])])
    s2 = Stmt("S2", ["i"], [1, 0], [F(i=1, c=-1), F(N=1, i=-1)], ("C", [F(i=1)]),
              [("B", [F(i=1, c=-1)]), ("B", [F(i=1, c=1)])])
    return Program(["N"], [F(N=1, c=-1)], [s1, s2])


def matmul():
    """for i, j: S1: C[i][j] = 0; for k: S2: C[i][j] = C[i][j] + A[i][k] * B[k][j]"""
    dom = [F(i=1), F(N=1, i=-1), F(j=1), F(N=1, j=-1)]
    s1 = Stmt("S1", ["i", "j"], [0, 0, 0], dom, ("C", [F(i=1), F(j=1)]), [])
    s2 = Stmt("S2", ["i", "j", "k"], [0, 0, 1, 0], dom + [F(k=1), F(N=1, k=-1)],
              ("C", [F(i=1), F(j=1)]), [("C", [F(i=1), F(j=1)]), ("A", [F(i=1), F(k=1)]), ("B", [F(k=1), F(j=1)])])
    return Program(["N"], [F(N=1)], [s1, s2])


if __name__ == "__main__":
    for name, prog in [("seidel", seidel()), ("stencil", stencil()),
                       ("producer-consumer", producer_consumer()), ("matmul", matmul())]:
        dims, bands, edges = pluto(prog)
        info = [(d["kind"], d.get("u"), d.get("w")) for d in dims]
        print(name, len(edges), "edges", show(dims), "bands", bands, info)
