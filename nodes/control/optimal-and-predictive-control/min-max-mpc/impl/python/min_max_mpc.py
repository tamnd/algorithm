# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/min-max-mpc/. The authors are listed in prov/SE9461.jsonl.

"""Min-max MPC with 1-norm costs, by one linear program on a scenario tree.

The plant is x_(k+1) = A x_k + B u_k + w_k with w_k in the convex hull of the
given vertices. The cost of a horizon is

    sum_(k < N) (|Q x_k|_1 + |R u_k|_1) + |P x_N|_1,

with the constraints |x_k|_i <= x_max_i, |u_k|_j <= u_max_j and F x_N <= f.
The tree has one branch per vertex at each step. In the feedback form each
node has its own control (the control may depend on the past disturbances);
in the open-loop form all nodes at the same depth share one control.

Matrices are lists of rows and vectors flat lists. The LP solver is a dense
two-phase simplex method with Bland's rule.
"""

from fractions import Fraction

__all__ = ["lp_min", "min_max_mpc", "closed_loop", "path_cost"]


def _pivot(T, obj, r, c):
    """Pivot on T[r][c]; obj is the reduced cost row and is updated too."""
    p = T[r][c]
    if isinstance(p, int):
        p = Fraction(p)  # int / int would give a float
    prow = [v / p for v in T[r]]
    T[r] = prow
    nzj = [j for j, v in enumerate(prow) if v != 0]
    for row in T + [obj]:
        if row is not prow and row[c] != 0:
            f = row[c]
            for j in nzj:
                row[j] -= f * prow[j]


def _simplex(T, obj, basis, tol, limit):
    """Bland's rule on columns below limit. Returns False if the objective is unbounded below."""
    while True:
        enter = next((j for j in range(limit) if obj[j] < -tol), None)
        if enter is None:
            return True
        leave, best = None, None
        for i, row in enumerate(T):
            if row[enter] > tol:
                ratio = row[-1] / row[enter]
                if best is None or ratio < best - tol or (abs(ratio - best) <= tol and basis[i] < basis[leave]):
                    leave, best = i, ratio
        if leave is None:
            return False
        _pivot(T, obj, leave, enter)
        basis[leave] = enter


def lp_min(c, G, g, E=(), e=(), nonneg=(), tol=1e-9):
    """Minimize c . z subject to G z <= g and E z = e.

    The variables in nonneg are >= 0, the others are free. Returns (value, z),
    or None if the LP is infeasible. Raises ValueError if it is unbounded.
    """
    n = len(c)
    nonneg = set(nonneg)
    free = [j for j in range(n) if j not in nonneg]
    # Columns: z_j (or its positive part), the negative parts of the free variables, slacks, artificials.
    neg_col = {j: n + i for i, j in enumerate(free)}
    nz = n + len(free)
    ns = len(G)
    rows = [(a, b, True) for a, b in zip(G, g)] + [(a, b, False) for a, b in zip(E, e)]
    need_art = [i for i, (a, b, ineq) in enumerate(rows) if b < 0 or not ineq]
    art_col = {i: nz + ns + k for k, i in enumerate(need_art)}
    ncol = nz + ns + len(need_art)
    T, basis = [], []
    for i, (a, b, ineq) in enumerate(rows):
        row = [0] * (ncol + 1)
        for j in range(n):
            row[j] = a[j]
            if j in neg_col:
                row[neg_col[j]] = -a[j]
        if ineq:
            row[nz + i] = 1
        row[-1] = b
        if b < 0:
            row = [-v for v in row]
        if i in art_col:
            row[art_col[i]] = 1
        T.append(row)
        basis.append(art_col.get(i, nz + i))
    if need_art:
        # Phase 1: minimize the sum of the artificial variables.
        obj = [0] * (ncol + 1)
        for i in need_art:
            for j in range(ncol + 1):
                if j < nz + ns or j == ncol:
                    obj[j] -= T[i][j]
        _simplex(T, obj, basis, tol, ncol)
        if -obj[-1] > tol * max(1, len(need_art)):
            return None
        keep = []
        for i in range(len(T)):
            if basis[i] >= nz + ns:
                j = next((j for j in range(nz + ns) if abs(T[i][j]) > tol), None)
                if j is None:
                    continue  # a redundant equation
                _pivot(T, obj, i, j)
                basis[i] = j
            keep.append(i)
        T = [T[i][:nz + ns] + [T[i][-1]] for i in keep]
        basis = [basis[i] for i in keep]
    else:
        T = [row[:nz + ns] + [row[-1]] for row in T]
    cost = list(c) + [-c[j] for j in free] + [0] * ns
    obj = cost + [0]
    for i, j in enumerate(basis):
        if cost[j] != 0:
            f = cost[j]
            obj = [o - f * t for o, t in zip(obj, T[i])]
    if not _simplex(T, obj, basis, tol, nz + ns):
        raise ValueError("the LP is unbounded")
    val = [0] * (nz + ns)
    for i, j in enumerate(basis):
        val[j] = T[i][-1]
    z = [val[j] - (val[neg_col[j]] if j in neg_col else 0) for j in range(n)]
    return sum(ci * zi for ci, zi in zip(c, z)), z


def min_max_mpc(A, B, x0, N, vertices, Q, R, P, x_max, u_max, F, f, feedback=True, tol=1e-9):
    """Solve the min-max problem from x0. Returns (value, u0, tree) or None if infeasible.

    tree maps each node (a tuple of vertex indices, the past disturbances) to
    its state, and each inner node to ("u", control).
    """
    n, m = len(A), len(B[0])
    var = []  # names of the LP variables, for reading the answer

    def new(name):
        var.append(name)
        return len(var) - 1

    # @line L1
    nodes = [()]
    for k in range(N):
        nodes += [p + (i,) for p in nodes if len(p) == k for i in range(len(vertices))]
    inner = [p for p in nodes if len(p) < N]
    # @line L2
    if feedback:
        u_idx = {p: [new(("u", p, j)) for j in range(m)] for p in inner}
    else:
        shared = {k: [new(("u", k, j)) for j in range(m)] for k in range(N)}
        u_idx = {p: shared[len(p)] for p in inner}
    x_idx = {p: [new(("x", p, i)) for i in range(n)] for p in nodes if p}
    t = new("t")
    nonneg = [t]
    G, g, E, e = [], [], [], []

    def row(coef):
        r = [0] * len(var)
        for j, v in coef.items():
            r[j] = r[j] + v
        return r

    # @line L3
    for p in nodes:
        if not p:
            continue
        q, w = p[:-1], vertices[p[-1]]
        for i in range(n):
            coef = {x_idx[p][i]: 1}
            const = w[i]
            for j in range(n):
                if q:
                    coef[x_idx[q][j]] = coef.get(x_idx[q][j], 0) - A[i][j]
                else:
                    const += A[i][j] * x0[j]
            for j in range(m):
                coef[u_idx[q][j]] = coef.get(u_idx[q][j], 0) - B[i][j]
            E.append(coef)
            e.append(const)
    # Epigraph variables for the stage and terminal costs.
    s_idx = {}
    for p in nodes:
        Wt = P if len(p) == N else Q
        s_idx[p] = []
        for r_ in range(len(Wt)):
            s = new(("s", p, r_))
            nonneg.append(s)
            s_idx[p].append(s)
    r_vars = {}
    for p in inner:
        key = p if feedback else len(p)
        if key not in r_vars:
            r_vars[key] = []
            for r_ in range(len(R)):
                s = new(("r", key, r_))
                nonneg.append(s)
                r_vars[key].append(s)
    # Now every variable exists; build the rows.
    E = [row(cf) for cf in E]
    # @line L4
    for p in nodes:
        if p:
            for i in range(n):
                G.append(row({x_idx[p][i]: 1}))
                g.append(x_max[i])
                G.append(row({x_idx[p][i]: -1}))
                g.append(x_max[i])
        elif any(abs(x0[i]) > x_max[i] for i in range(n)):
            return None
        if len(p) == N:
            for fr, fb in zip(F, f):
                if p:
                    G.append(row({x_idx[p][i]: fr[i] for i in range(n)}))
                    g.append(fb)
                elif sum(a * b for a, b in zip(fr, x0)) > fb:
                    return None
    for p in inner:
        for j in range(m):
            G.append(row({u_idx[p][j]: 1}))
            g.append(u_max[j])
            G.append(row({u_idx[p][j]: -1}))
            g.append(u_max[j])
    # @line L5
    for p in nodes:
        Wt = P if len(p) == N else Q
        for r_, wr in enumerate(Wt):
            for sg in (1, -1):
                coef = {s_idx[p][r_]: -1}
                const = 0
                for i in range(n):
                    if p:
                        coef[x_idx[p][i]] = coef.get(x_idx[p][i], 0) + sg * wr[i]
                    else:
                        const += sg * wr[i] * x0[i]
                G.append(row(coef))
                g.append(-const)
    for p in inner:
        key = p if feedback else len(p)
        for r_, rr in enumerate(R):
            for sg in (1, -1):
                coef = {r_vars[key][r_]: -1}
                for j in range(m):
                    coef[u_idx[p][j]] = coef.get(u_idx[p][j], 0) + sg * rr[j]
                G.append(row(coef))
                g.append(0)
    for leaf in [p for p in nodes if len(p) == N]:
        coef = {t: -1}
        for k in range(N + 1):
            p = leaf[:k]
            for s in s_idx[p]:
                coef[s] = coef.get(s, 0) + 1
            if k < N:
                for s in r_vars[p if feedback else k]:
                    coef[s] = coef.get(s, 0) + 1
        G.append(row(coef))
        g.append(0)
    c = [0] * len(var)
    c[t] = 1
    # @line L6
    sol = lp_min(c, G, g, E, e, nonneg, tol)
    if sol is None:
        return None
    val, z = sol
    tree = {(): list(x0)}
    for p in nodes:
        if p:
            tree[p] = [z[j] for j in x_idx[p]]
    for p in inner:
        tree[("u",) + p] = [z[j] for j in u_idx[p]]
    # @line L7
    return val, [z[j] for j in u_idx[()]], tree


def path_cost(A, B, x0, us, ws, Q, R, P):
    """Cost of the input sequence us under the disturbance sequence ws."""
    x = list(x0)
    J = 0
    for u, w in zip(us, ws):
        J += sum(abs(sum(q * xi for q, xi in zip(row, x))) for row in Q)
        J += sum(abs(sum(r * ui for r, ui in zip(row, u))) for row in R)
        x = [sum(a * xi for a, xi in zip(Ar, x)) + sum(b * ui for b, ui in zip(Br, u)) + wi
             for Ar, Br, wi in zip(A, B, w)]
    return J + sum(abs(sum(p * xi for p, xi in zip(row, x))) for row in P), x


def closed_loop(A, B, x0, N, vertices, Q, R, P, x_max, u_max, F, f, disturbances, feedback=True):
    """Receding horizon: apply the first control of each min-max problem. Returns (xs, us, values)."""
    x = list(x0)
    xs, us, vals = [list(x)], [], []
    for w in disturbances:  # @line L8
        sol = min_max_mpc(A, B, x, N, vertices, Q, R, P, x_max, u_max, F, f, feedback)
        if sol is None:
            raise RuntimeError("the min-max problem became infeasible")
        val, u, _ = sol
        x = [sum(a * xi for a, xi in zip(Ar, x)) + sum(b * ui for b, ui in zip(Br, u)) + wi
             for Ar, Br, wi in zip(A, B, w)]
        xs.append(x)
        us.append(u)
        vals.append(val)
    return xs, us, vals
