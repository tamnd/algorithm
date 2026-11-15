# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polyhedral-scanning/. The authors are listed in prov/19214B.jsonl.
"""Polyhedral scanning: loop nests that visit the integer points of a union
of polyhedra in lexicographic order.

Each statement S has a domain D_S and an affine schedule theta_S. Its
points in the scanning space are (theta_S(i), i, 0...), one dimension per
schedule entry and per loop counter, padded with zeros to a common length.
Visiting the union of these sets in lexicographic order runs the program in
schedule order.

At level k the generator projects every polyhedron on the first k + 1
dimensions by Fourier-Motzkin elimination, separates the projections into
disjoint pieces (the Quillere-Rajopadhye-Wilde method), sorts the pieces
along dimension k, and makes one loop per piece whose bounds are the
constraints of the piece on that dimension. Inside each loop it recurses on
the statements of the piece.

A constraint is a list of integers (a_0, ..., a_{v-1}, c) over the dimensions
and then the parameters, and means a . x + c >= 0. An exact simplex method
on integer rows decides emptiness and implication.
"""

from fractions import Fraction
from math import gcd, lcm


# ------------------------------------------------------- exact simplex method

def _reduce(row):
    g = gcd(*row)
    return [x // g for x in row] if g > 1 else row


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
    """Maximize c.x subject to A x = b and x >= 0, with integer data, in
    exact arithmetic. Returns the optimal x as Fractions, None if the system
    is infeasible; raises ValueError if the problem is unbounded."""
    m, n = len(A), len(c)
    rows, basis = [], []
    for i in range(m):
        row = list(A[i]) + [b[i]]
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
    obj = list(c) + [0] * m + [0]
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


def _standard(rows, nv, obj):
    """{x free : rows} as A z = b, z >= 0, with x = p - q and one slack per row."""
    m = len(rows)
    A, b = [], []
    for i, r in enumerate(rows):
        line = []
        for j in range(nv):
            line += [r[j], -r[j]]
        slack = [0] * m
        slack[i] = -1
        A.append(line + slack)
        b.append(-r[-1])
    c = []
    for j in range(nv):
        c += [-obj[j], obj[j]]
    return c + [0] * m, A, b


def feasible(rows, nv):
    """Does {x in Q^nv : rows} have a point?"""
    if any(not any(r[:-1]) and r[-1] < 0 for r in rows):
        return False
    rows = [r for r in rows if any(r[:-1])]
    if not rows:
        return True
    c, A, b = _standard(rows, nv, [0] * nv)
    return lp_max(c, A, b) is not None


def implied(rows, g, nv):
    """Does every rational point of the nonempty set {rows} satisfy g >= 0?"""
    if not any(g[:-1]):
        return g[-1] >= 0
    c, A, b = _standard(rows, nv, g)
    try:
        x = lp_max(c, A, b)
    except ValueError:
        return False
    if x is None:
        return True
    return sum(g[j] * (x[2 * j] - x[2 * j + 1]) for j in range(nv)) + g[-1] >= 0


# ------------------------------------------------- constraints and projection

def norm(row):
    """Divide by the gcd of the coefficients and round the constant down.
    The integer points stay the same."""
    g = gcd(*row[:-1])
    if g <= 1:
        return list(row)
    return [x // g for x in row[:-1]] + [row[-1] // g]


def clean(rows):
    """Normalize, drop trivial rows, keep the tightest row per direction."""
    best = {}
    for r in rows:
        r = norm(r)
        if not any(r[:-1]):
            if r[-1] < 0:
                return [r]
            continue
        key = tuple(r[:-1])
        if key not in best or r[-1] < best[key]:
            best[key] = r[-1]
    return [list(k) + [c] for k, c in best.items()]


def negate(g):
    """The integer complement of g >= 0, that is g <= -1."""
    return [-x for x in g[:-1]] + [-g[-1] - 1]


def eliminate(rows, j):
    """Fourier-Motzkin elimination of variable j. With an equality on the
    variable, substitution is enough."""
    for r in rows:
        if r[j] > 0 and [-x for x in r] in rows:
            a = r[j]
            return clean([[a * x - s[j] * y for x, y in zip(s, r)] if s[j] else s
                          for s in rows if s is not r and s != [-x for x in r]])
    pos = [r for r in rows if r[j] > 0]
    neg = [r for r in rows if r[j] < 0]
    out = [r for r in rows if r[j] == 0]
    for p in pos:
        for q in neg:
            a, b = p[j], -q[j]
            out.append([b * x + a * y for x, y in zip(p, q)])
    return clean(out)


def prune(rows, nv):
    """Remove the rows that the others imply."""
    rows = clean(rows)
    if len(rows) == 1 and not any(rows[0][:-1]):
        return rows
    k = 0
    while k < len(rows):
        rest = rows[:k] + rows[k + 1:]
        if rest and implied(rest, rows[k], nv):
            rows = rest
        else:
            k += 1
    return rows


def project(rows, keep, n, nv):
    """The shadow of {rows} on the first `keep` dimensions (and the
    parameters), by eliminating the dimensions n - 1, ..., keep."""
    for j in range(n - 1, keep - 1, -1):
        rows = eliminate(rows, j)
        if len(rows) > 3 * nv:
            rows = prune(rows, nv)
    return rows


# ------------------------------------------------------------- separation

def difference(P, Q, nv):
    """P minus Q as disjoint pieces: P, q_1 >= 0, ..., q_{t-1} >= 0, q_t <= -1."""
    out, acc = [], list(P)
    for q in Q:
        piece = acc + [negate(q)]
        if feasible(piece, nv):
            out.append(clean(piece))
        acc = acc + [q]
        if not feasible(acc, nv):
            break
    return out


def separate(polys, nv):
    """Disjoint pieces that cover the union of the polyhedra, each with the
    set of polyhedra that contain it."""
    pieces = []
    for rows, lab in polys:
        new, rest = [], [rows]
        for prow, plab in pieces:
            both = clean(prow + rows)
            if feasible(both, nv):
                new.append((both, plab | lab))
            new += [(d, plab) for d in difference(prow, rows, nv)]
            rest = [r2 for r in rest for r2 in difference(r, prow, nv)]
        new += [(r, lab) for r in rest]
        pieces = new
    return pieces


def _pair(A, B, k, nv):
    """A and B in one space of nv + 1 variables: B's dimension k moves to
    the new variable nv, the other dimensions and the parameters are shared."""
    a = [r[:-1] + [0, r[-1]] for r in A]
    b = []
    for r in B:
        s = r[:-1] + [r[k], r[-1]]
        s[k] = 0
        b.append(s)
    return a + b


def sort_pieces(pieces, k, nv):
    """An order of the pieces such that two pieces that exist for the same
    outer values come with the smaller x_k first, or None."""
    m = len(pieces)
    after = [set() for _ in range(m)]
    indeg = [0] * m
    for x in range(m):
        for y in range(x + 1, m):
            both = _pair(pieces[x][0], pieces[y][0], k, nv)
            if not feasible(both, nv + 1):
                continue                     # never at the same outer values
            ge = [0] * (nv + 2)
            ge[k], ge[nv] = 1, -1            # x_k(A) - x_k(B) >= 0
            if not feasible(both + [ge], nv + 1):
                after[x].add(y)
                indeg[y] += 1
            elif not feasible(both + [[-v for v in ge]], nv + 1):
                after[y].add(x)
                indeg[x] += 1
            else:
                return None
    out, ready = [], [x for x in range(m) if indeg[x] == 0]
    while ready:
        x = min(ready)
        ready.remove(x)
        out.append(x)
        for y in after[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                ready.append(y)
    return [pieces[x] for x in out] if len(out) == m else None


# --------------------------------------------------------- code generation

class Scop:
    """Statements with domains and schedules. Each statement is a dict with
    'name', 'iters', 'domain' (affine dicts >= 0 over iters and params) and
    'schedule' (a list of affine dicts). Affine dicts map names to integers;
    the key "" is the constant."""

    def __init__(self, params, context, stmts):
        self.params, self.context, self.stmts = params, context, stmts
        self.m = max(len(s["schedule"]) for s in stmts)
        self.d = max(len(s["iters"]) for s in stmts)
        self.dims = [f"t{k + 1}" for k in range(self.m)] + [f"i{k + 1}" for k in range(self.d)]
        self.names = self.dims + params
        self.n, self.nv = len(self.dims), len(self.names)

    def row(self, aff, rename=None):
        rename = rename or {}
        r = [0] * (self.nv + 1)
        for v, c in aff.items():
            if v == "":
                r[-1] += c
            else:
                r[self.names.index(rename.get(v, v))] += c
        return r

    def context_rows(self):
        return [self.row(c) for c in self.context]

    def polyhedron(self, s):
        """The points (theta(i), i, 0...) of statement s in the scanning space."""
        S = self.stmts[s]
        ren = {x: f"i{k + 1}" for k, x in enumerate(S["iters"])}
        rows = [self.row(c, ren) for c in S["domain"]] + self.context_rows()
        sched = S["schedule"] + [{}] * (self.m - len(S["schedule"]))
        for k, th in enumerate(sched):
            r = self.row(th, ren)
            r[k] -= 1                        # theta_k(i) - t_k = 0
            rows += [r, [-x for x in r]]
        for k in range(len(S["iters"]), self.d):
            r = [0] * (self.nv + 1)
            r[self.m + k] = 1                # i_k = 0 below the statement's depth
            rows += [r, [-x for x in r]]
        return clean(rows)


def scan(scop):
    """The loop nest for the scop: a list of nodes for codegen at level 0."""
    polys = [(scop.polyhedron(s), frozenset([s])) for s in range(len(scop.stmts))]
    ctx = prune(scop.context_rows(), scop.nv) if scop.context else []
    return codegen(polys, 0, ctx, scop.n, scop.nv)


def codegen(polys, k, ctx, n, nv):
    projs = []
    for rows, lab in polys:
        q = prune(project(rows, k + 1, n, nv), nv)  # @line L1
        if feasible(q, nv):
            projs.append((q, lab))
    pieces = separate(projs, nv)  # @line L2
    order = sort_pieces(pieces, k, nv)  # @line L3
    parts = []
    for rows, lab in (order if order is not None else pieces):  # @line L5
        guards = [r for r in rows if r[k] == 0 and not implied(ctx, r, nv)] if ctx else \
            [r for r in rows if r[k] == 0]  # @line L6
        bounds = prune([r for r in rows if r[k] != 0] + ctx, nv)
        bounds = [r for r in bounds if r[k] != 0]  # @line L7
        if k == n - 1:
            body = [{"exec": sorted(lab)}]  # @line L8
        else:
            inner = [(clean(prow + rows), plab) for prow, plab in polys if plab <= lab]
            body = codegen(inner, k + 1, prune(ctx + rows, nv), n, nv)  # @line L9
        parts.append({"k": k, "guards": guards, "bounds": bounds, "body": body})  # @line L10
    if order is None and len(parts) > 1:
        return [{"k": k, "union": parts}]  # @line L4
    return parts


# ------------------------------------------------------------- execution

def _rest(r, k, vals):
    return sum(r[v] * vals[v] for v in range(len(vals)) if v != k and r[v]) + r[-1]


def _range(node, vals):
    """The range of x_k in a loop node, or None if a guard fails."""
    k = node["k"]
    if any(_rest(g, k, vals) < 0 for g in node["guards"]):
        return None
    lo, hi = None, None
    for r in node["bounds"]:
        a, rest = r[k], _rest(r, k, vals)
        if a > 0:
            b = -(rest // a)                 # ceil(-rest / a)
            lo = b if lo is None else max(lo, b)
        else:
            b = rest // (-a)                 # floor(rest / -a)
            hi = b if hi is None else min(hi, b)
    if lo is None or hi is None:
        raise ValueError("unbounded loop")
    return lo, hi


def execute(ast, scop, env, visit):
    """Run the loop nest: visit(s, point) for each statement instance, where
    point is the vector of all scanning dimensions."""
    vals = [0] * scop.n + [env[p] for p in scop.params]

    def run(nodes):
        for node in nodes:
            if "exec" in node:
                for s in node["exec"]:
                    visit(s, tuple(vals[:scop.n]))
                continue
            k = node["k"]
            if "union" in node:
                ranges = [_range(p, vals) for p in node["union"]]
                live = [(p, r) for p, r in zip(node["union"], ranges) if r]
                if not live:
                    continue
                for x in range(min(r[0] for _, r in live), max(r[1] for _, r in live) + 1):
                    vals[k] = x
                    for p, r in live:
                        if r[0] <= x <= r[1]:
                            run(p["body"])
                            vals[k] = x
                continue
            r = _range(node, vals)
            if r is None:
                continue
            for x in range(r[0], r[1] + 1):
                vals[k] = x
                run(node["body"])
                vals[k] = x
            vals[k] = 0

    run(ast)


def instance_of(scop, s, point):
    """The iteration vector of statement s at a scanning point."""
    return point[scop.m:scop.m + len(scop.stmts[s]["iters"])]


# ------------------------------------------------------------- printing

def _expr(coefs, names):
    terms = []
    for v, c in zip(names, coefs[:-1]):
        if c:
            terms.append((c, v))
    out = ""
    for c, v in terms:
        t = v if abs(c) == 1 else f"{abs(c)}*{v}"
        out += (" - " if c < 0 else " + ") + t if out else ("-" if c < 0 else "") + t
    if coefs[-1] or not out:
        c = coefs[-1]
        out += f" {'-' if c < 0 else '+'} {abs(c)}" if out else str(c)
    return out


def _bound(r, k, names):
    a = r[k]
    rest = [x for x in r]
    rest[k] = 0
    if a > 0:
        e = _expr([-x for x in rest], names)
        return e if a == 1 else f"ceil(({e}) / {a})"
    e = _expr(rest, names)
    return e if a == -1 else f"floor(({e}) / {-a})"


def show(ast, scop, depth=0):
    """The loop nest as text."""
    names, pad, lines = scop.names, "  " * depth, []
    for node in ast:
        if "exec" in node:
            for s in node["exec"]:
                S = scop.stmts[s]
                args = ", ".join(scop.dims[scop.m + j] for j in range(len(S["iters"])))
                lines.append(f"{pad}{S['name']}({args})")
            continue
        if "union" in node:
            k = node["k"]
            lines.append(f"{pad}for {names[k]} in the union of:")
            for p in node["union"]:
                lines += show([p], scop, depth + 1)
            continue
        k, inner = node["k"], depth
        if node["guards"]:
            conds = " and ".join(f"{_expr(g, names)} >= 0" for g in node["guards"])
            lines.append(f"{pad}if {conds}:")
            inner += 1
        lo = [_bound(r, k, names) for r in node["bounds"] if r[k] > 0]
        hi = [_bound(r, k, names) for r in node["bounds"] if r[k] < 0]
        ipad = "  " * inner
        if len(lo) == 1 and lo == hi:
            lines.append(f"{ipad}{names[k]} = {lo[0]}")
            inner -= 1
        else:
            lo_s = lo[0] if len(lo) == 1 else f"max({', '.join(lo)})"
            hi_s = hi[0] if len(hi) == 1 else f"min({', '.join(hi)})"
            lines.append(f"{ipad}for {names[k]} = {lo_s} to {hi_s}:")
        lines += show(node["body"], scop, inner + 1)
    return lines


# ------------------------------------------------------------- examples

def triangle(schedule="ij"):
    """for i = 0 to N: for j = 0 to i: S(i, j), scanned in (i, j) or (j, i)."""
    sched = [{"i": 1}, {"j": 1}] if schedule == "ij" else [{"j": 1}, {"i": 1}]
    S = {"name": "S", "iters": ["i", "j"],
         "domain": [{"i": 1}, {"N": 1, "i": -1}, {"j": 1}, {"i": 1, "j": -1}],
         "schedule": sched}
    return Scop(["N"], [{"N": 1}], [S])


def two_ranges():
    """S1 on 0 <= i <= N and S2 on 2 <= i <= N + 2, fused: (i, 0) and (i, 1)."""
    S1 = {"name": "S1", "iters": ["i"], "domain": [{"i": 1}, {"N": 1, "i": -1}],
          "schedule": [{"i": 1}, {}]}
    S2 = {"name": "S2", "iters": ["i"], "domain": [{"i": 1, "": -2}, {"N": 1, "i": -1, "": 2}],
          "schedule": [{"i": 1}, {"": 1}]}
    return Scop(["N"], [{"N": 1}], [S1, S2])


def skewed_stencil():
    """for t = 0 to N: for i = 1 to N: S(t, i), with the schedule (t, t + i)."""
    S = {"name": "S", "iters": ["t", "i"],
         "domain": [{"t": 1}, {"N": 1, "t": -1}, {"i": 1, "": -1}, {"N": 1, "i": -1}],
         "schedule": [{"t": 1}, {"t": 1, "i": 1}]}
    return Scop(["N"], [{"N": 1}], [S])


if __name__ == "__main__":
    for title, scop in [("triangle, (i, j)", triangle("ij")), ("triangle, (j, i)", triangle("ji")),
                        ("two ranges, fused", two_ranges()), ("skewed stencil", skewed_stencil())]:
        print(f"-- {title}")
        print("\n".join(show(scan(scop), scop)))
