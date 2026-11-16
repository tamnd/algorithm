# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isam2/. The authors are listed in prov/32NTDV.jsonl.

"""iSAM2 (Kaess et al. 2012) on a planar pose graph.

The variables are poses (x, y, theta). The nonlinear factors are a prior on
one pose and "between" factors that measure the pose j in the frame of i.
The noise is Gaussian with diagonal standard deviations. A pose is updated
by adding a step to (x, y, theta) and wrapping the angle.

iSAM2 keeps:
  theta   the linearization point of each variable,
  delta   the current solution of the linear system at theta,
  a Bayes tree of cliques. Each clique has frontal variables, separator
          variables, one Gaussian conditional per frontal variable, and the
          cached factor on its separator that its elimination passed up.
The estimate is theta + delta.

UPDATE(new factors, new variables) does:
  1. fluid relinearization: the variables J with |delta_j| >= beta move
     their linearization point to theta_j + delta_j;
  2. it removes the top of the tree: the cliques that contain a variable of
     J, or a variable of a new factor as a frontal variable, and all their
     ancestors. The children of the top that are not in it are the orphans;
  3. it eliminates the factors whose variables all lie in the top, linearized
     at theta, together with the cached factors of the orphans, in a
     minimum degree order with the variables of the new factors last;
  4. it builds new cliques from the conditionals and puts each orphan back
     under the clique of the first eliminated variable of its separator;
  5. it updates delta from the root down. A clique is solved if it is new,
     or if a separator variable changed by more than alpha (the wildfire
     threshold). alpha = 0 updates every clique whose input changed.

A Gaussian factor is kept in information form: the matrix blocks
lam[(u, w)] and the vector blocks eta[u] of 1/2 x^T Lambda x - eta^T x.
Eliminating a variable v uses a Cholesky factor R of lam[(v, v)] and gives
the conditional R x_v + sum_s S_s x_s = d, which is one block row of the
square root information matrix, and a new factor on the other variables.
"""

import math

# ------------------------------------------------------------ small dense algebra


def wrap(a):
    return (a + math.pi) % (2.0 * math.pi) - math.pi


def transpose(a):
    return [list(r) for r in zip(*a)]


def mul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(r, c)) for c in bt] for r in a]


def mat_vec(a, x):
    return [sum(p * q for p, q in zip(r, x)) for r in a]


def chol_upper(a):
    """Return the upper triangular R with R^T R = a."""
    n = len(a)
    r = [[0.0] * n for _ in range(n)]
    for i in range(n):
        s = a[i][i] - sum(r[k][i] ** 2 for k in range(i))
        if s <= 0.0:
            raise ValueError("the information block is not positive definite")
        r[i][i] = math.sqrt(s)
        for j in range(i + 1, n):
            r[i][j] = (a[i][j] - sum(r[k][i] * r[k][j] for k in range(i))) / r[i][i]
    return r


def solve_rt(r, b):
    """Solve R^T y = b for a vector b, with R upper triangular."""
    n = len(r)
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(r[k][i] * y[k] for k in range(i))) / r[i][i]
    return y


def solve_r(r, b):
    """Solve R x = b for a vector b, with R upper triangular."""
    n = len(r)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(r[i][k] * x[k] for k in range(i + 1, n))) / r[i][i]
    return x


def solve_rt_mat(r, b):
    """Solve R^T Y = B column by column."""
    cols = [solve_rt(r, c) for c in transpose(b)]
    return transpose(cols)


# ------------------------------------------------------------------ factors


class Prior:
    def __init__(self, key, mean, sigmas):
        self.keys = [key]
        self.z = list(mean)
        self.sigmas = list(sigmas)

    def error_and_jacobians(self, theta):
        x = theta[self.keys[0]]
        e = [x[0] - self.z[0], x[1] - self.z[1], wrap(x[2] - self.z[2])]
        return e, [[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]]


class Between:
    def __init__(self, i, j, z, sigmas):
        self.keys = [i, j]
        self.z = list(z)
        self.sigmas = list(sigmas)

    def error_and_jacobians(self, theta):
        a, b = theta[self.keys[0]], theta[self.keys[1]]
        c, s = math.cos(a[2]), math.sin(a[2])
        dx, dy = b[0] - a[0], b[1] - a[1]
        e = [c * dx + s * dy - self.z[0], -s * dx + c * dy - self.z[1], wrap(b[2] - a[2] - self.z[2])]
        ja = [[-c, -s, -s * dx + c * dy], [s, -c, -c * dx - s * dy], [0.0, 0.0, -1.0]]
        jb = [[c, s, 0.0], [-s, c, 0.0], [0.0, 0.0, 1.0]]
        return e, [ja, jb]


def whitened_error(f, theta):
    e, _ = f.error_and_jacobians(theta)
    return sum((v / s) ** 2 for v, s in zip(e, f.sigmas))


class GaussianFactor:
    """1/2 x^T Lambda x - eta^T x on the variables keys."""

    def __init__(self, keys, lam, eta):
        self.keys = list(keys)
        self.lam = lam
        self.eta = eta


def linearize(f, theta):
    """Return the Gaussian factor of f at theta, in the step delta."""
    e, js = f.error_and_jacobians(theta)
    e = [v / s for v, s in zip(e, f.sigmas)]
    js = [[[v / s for v in row] for row, s in zip(j, f.sigmas)] for j in js]
    lam, eta = {}, {}
    for u, ju in zip(f.keys, js):
        jut = transpose(ju)
        eta[u] = [-v for v in mat_vec(jut, e)]
        for w, jw in zip(f.keys, js):
            lam[(u, w)] = mul(jut, jw)
    return GaussianFactor(f.keys, lam, eta)


def _add_to(dst, src):
    for i in range(len(dst)):
        if isinstance(dst[i], list):
            for k in range(len(dst[i])):
                dst[i][k] += src[i][k]
        else:
            dst[i] += src[i]


def combine(factors, pos):
    keys = sorted({k for f in factors for k in f.keys}, key=pos.get)
    lam, eta = {}, {}
    for f in factors:
        for kw, blk in f.lam.items():
            if kw in lam:
                _add_to(lam[kw], blk)
            else:
                lam[kw] = [list(r) for r in blk]
        for k, vec in f.eta.items():
            if k in eta:
                _add_to(eta[k], vec)
            else:
                eta[k] = list(vec)
    return GaussianFactor(keys, lam, eta)


class Conditional:
    """R x_v + sum over the parents s of S[s] x_s = d."""

    def __init__(self, var, parents, r, s, d):
        self.var = var
        self.parents = parents
        self.r = r
        self.s = s
        self.d = d

    def solve(self, values):
        rhs = list(self.d)
        for p in self.parents:
            sx = mat_vec(self.s[p], values[p])
            rhs = [a - b for a, b in zip(rhs, sx)]
        return solve_r(self.r, rhs)


def eliminate_one(joint, v):
    """Return (conditional on v, the new factor on the other variables)."""
    rest = [k for k in joint.keys if k != v]
    r = chol_upper(joint.lam[(v, v)])
    n = len(r)
    s = {}
    for k in rest:
        blk = joint.lam.get((v, k))
        s[k] = solve_rt_mat(r, blk) if blk is not None else [[0.0] * len(joint.eta[k]) for _ in range(n)]
    d = solve_rt(r, joint.eta.get(v, [0.0] * n))
    lam, eta = {}, {}
    for a in rest:
        sat = transpose(s[a])
        e = joint.eta.get(a, [0.0] * len(sat))
        eta[a] = [x - y for x, y in zip(e, mat_vec(sat, d))]
        for b in rest:
            base = joint.lam.get((a, b))
            corr = mul(sat, s[b])
            if base is None:
                lam[(a, b)] = [[-x for x in row] for row in corr]
            else:
                lam[(a, b)] = [[x - y for x, y in zip(r1, r2)] for r1, r2 in zip(base, corr)]
    return Conditional(v, rest, r, s, d), GaussianFactor(rest, lam, eta)


def eliminate(factors, order):
    """Variable elimination; return the conditionals in order and the produced factors."""
    pos = {v: i for i, v in enumerate(order)}
    buckets = {v: [] for v in order}
    for f in factors:
        buckets[min(f.keys, key=pos.get)].append(f)
    conds, produced = [], {}
    for v in order:
        joint = combine(buckets[v], pos)
        cond, newf = eliminate_one(joint, v)
        conds.append(cond)
        produced[v] = newf
        if newf.keys:
            buckets[min(newf.keys, key=pos.get)].append(newf)
    return conds, produced


# --------------------------------------------------------------- the Bayes tree


class Clique:
    def __init__(self, frontals, sep, parent):
        self.frontals = frontals  # in elimination order
        self.sep = sep
        self.parent = parent
        self.children = []
        self.conds = {}
        self.cached = None  # the factor on sep from the elimination of this clique


def build_cliques(conds, produced, pos):
    """Return (new cliques, new roots, map from a variable to its clique)."""
    clique_of, cliques, roots = {}, [], []
    for cond in reversed(conds):
        v = cond.var
        if not cond.parents:
            c = Clique([v], [], None)
            cliques.append(c)
            roots.append(c)
        else:
            first = min(cond.parents, key=pos.get)
            p = clique_of[first]
            if set(p.frontals) | set(p.sep) == set(cond.parents):
                p.frontals.insert(0, v)  # merge: v is eliminated before the others
                c = p
            else:
                c = Clique([v], list(cond.parents), p)
                p.children.append(c)
                cliques.append(c)
        c.conds[v] = cond
        clique_of[v] = c
    for c in cliques:
        c.cached = produced[c.frontals[-1]]
    return cliques, roots, clique_of


def constrained_min_degree(variables, factors, last):
    """A minimum degree order of the variables; the variables in last go last."""
    adj = {v: set() for v in variables}
    for f in factors:
        for u in f.keys:
            adj[u] |= set(f.keys) - {u}
    order = []
    for group in ([v for v in variables if v not in last], [v for v in variables if v in last]):
        left = set(group)
        while left:
            u = min(left, key=lambda v: (len(adj[v]), repr(v)))
            left.discard(u)
            nb = adj.pop(u)
            for a in nb:
                adj[a].discard(u)
                adj[a] |= nb - {a}
            order.append(u)
    return order


class ISAM2:
    def __init__(self, beta=0.1, alpha=0.0):
        self.beta = beta  # relinearization threshold
        self.alpha = alpha  # wildfire threshold of the partial back substitution
        self.theta = {}
        self.delta = {}
        self.factors = []
        self.lin = []  # the linearized factors, at the current theta
        self.roots = []
        self.clique_of = {}
        self.last_stats = {}

    def cliques(self):
        out, stack = [], list(self.roots)
        while stack:
            c = stack.pop()
            out.append(c)
            stack.extend(c.children)
        return out

    def estimate(self):
        return {v: [a + b for a, b in zip(self.theta[v], self.delta[v])] for v in self.theta}

    def update(self, new_factors=(), new_values=None):
        new_values = new_values or {}
        for v, x in new_values.items():
            self.theta[v] = list(x)
            self.delta[v] = [0.0] * len(x)
        relin = {v for v in self.clique_of if max(abs(a) for a in self.delta[v]) >= self.beta}  # @line L1
        for v in relin:
            self.theta[v] = [a + b for a, b in zip(self.theta[v], self.delta[v])]  # @line L2
            self.theta[v][2] = wrap(self.theta[v][2])
            self.delta[v] = [0.0] * len(self.delta[v])
        new_keys = {k for f in new_factors for k in f.keys}
        marked = set()
        for c in self.cliques():  # @line L3
            if (set(c.frontals) | set(c.sep)) & relin or set(c.frontals) & new_keys:
                while c is not None and c not in marked:
                    marked.add(c)  # @line L4
                    c = c.parent
        top_vars = {v for c in marked for v in c.frontals} | (set(new_values) - set(self.clique_of))
        top_vars |= new_keys - set(self.clique_of)
        orphans = [ch for c in marked for ch in c.children if ch not in marked]  # @line L5
        for f in new_factors:
            self.factors.append(f)
            self.lin.append(None)
        n_relin = 0
        top_factors = []
        for i, f in enumerate(self.factors):
            if set(f.keys) <= top_vars:  # @line L6
                if self.lin[i] is None or set(f.keys) & relin:
                    self.lin[i] = linearize(f, self.theta)
                    n_relin += 1
                top_factors.append(self.lin[i])
        cached = [o.cached for o in orphans]  # @line L7
        variables = sorted(top_vars, key=repr)
        order = constrained_min_degree(variables, top_factors + cached, new_keys)  # @line L8
        conds, produced = eliminate(top_factors + cached, order)  # @line L9
        pos = {v: i for i, v in enumerate(order)}
        new_cliques, new_roots, cl = build_cliques(conds, produced, pos)  # @line L10
        for o in orphans:  # @line L11
            p = cl[min(o.sep, key=pos.get)]
            o.parent = p
            p.children.append(o)
        self.roots = [r for r in self.roots if r not in marked] + new_roots
        self.clique_of.update(cl)
        visited = self._solve(set(new_cliques))  # @line L12
        self.last_stats = {
            "relinearized_variables": len(relin),
            "relinearized_factors": n_relin,
            "eliminated_cliques": len(new_cliques),
            "total_cliques": len(self.cliques()),
            "solved_cliques": visited,
        }
        return self.estimate()

    def _solve(self, dirty):
        """Partial back substitution from the roots down (wildfire)."""
        visited = 0
        stack = list(self.roots)
        changed = set()
        while stack:
            c = stack.pop()
            if c not in dirty and not (set(c.sep) & changed):
                continue  # @line L13
            visited += 1
            for v in reversed(c.frontals):
                new = c.conds[v].solve(self.delta)  # @line L14
                if max(abs(a - b) for a, b in zip(new, self.delta[v])) > self.alpha:
                    changed.add(v)  # @line L15
                self.delta[v] = new
            stack.extend(c.children)
        return visited
