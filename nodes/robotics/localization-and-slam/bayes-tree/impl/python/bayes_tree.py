# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayes-tree/. The authors are listed in prov/XZ2CJC.jsonl.

"""The Bayes tree of a linear Gaussian factor graph (Kaess et al.).

A linear factor is the cost 1/2 || sum_k A_k x_k - b ||^2 on a few vector
variables x_k. Eliminating the variables in an order turns the factor graph
into a Bayes net: one Gaussian conditional per variable,

    R x_v + sum over the parents s of S_s x_s = d,

with R upper triangular. These are the block rows of the square root
information matrix. The Bayes tree groups the conditionals into cliques:
a clique has frontal variables F (in elimination order) and separator
variables S, and each separator lies in the variables of the parent clique.

Operations:
  eliminate(factors, order)    the conditionals, by variable elimination
  BayesTree.build(factors)     eliminate, then group the conditionals
  tree.solve()                 back substitution from the roots down
  tree.update(new_factors)     add factors: remove the top of the tree above
                               the touched variables, turn its conditionals
                               back into factors, add the new factors,
                               eliminate them again, and put the untouched
                               subtrees (the orphans) back.
"""

import math

# ------------------------------------------------------------ dense helpers


def tr(a):
    return [list(r) for r in zip(*a)]


def mm(a, b):
    bt = tr(b)
    return [[sum(x * y for x, y in zip(r, c)) for c in bt] for r in a]


def mv(a, x):
    return [sum(p * q for p, q in zip(r, x)) for r in a]


def upper_cholesky(a):
    """Upper triangular R with R^T R = a; ValueError if a is not positive definite."""
    n = len(a)
    r = [[0.0] * n for _ in range(n)]
    for i in range(n):
        s = a[i][i] - sum(r[k][i] ** 2 for k in range(i))
        if s <= 1e-12 * max(1.0, abs(a[i][i])):
            raise ValueError("the information block is not positive definite")
        r[i][i] = math.sqrt(s)
        for j in range(i + 1, n):
            r[i][j] = (a[i][j] - sum(r[k][i] * r[k][j] for k in range(i))) / r[i][i]
    return r


def forward(r, b):
    """Solve R^T y = b."""
    y = [0.0] * len(r)
    for i in range(len(r)):
        y[i] = (b[i] - sum(r[k][i] * y[k] for k in range(i))) / r[i][i]
    return y


def backward(r, b):
    """Solve R x = b."""
    n = len(r)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(r[i][k] * x[k] for k in range(i + 1, n))) / r[i][i]
    return x


# ------------------------------------------------------------------ factors


class LinearFactor:
    """1/2 || sum_k A_k x_k - b ||^2, with blocks = {key: A_k}."""

    def __init__(self, blocks, b):
        self.keys = list(blocks)
        self.blocks = {k: [list(row) for row in a] for k, a in blocks.items()}
        self.b = list(b)


class InfoFactor:
    """1/2 x^T Lambda x - eta^T x, with the blocks lam[(u, w)] and eta[u]."""

    def __init__(self, keys, lam, eta):
        self.keys = list(keys)
        self.lam = lam
        self.eta = eta


def to_info(f):
    if isinstance(f, InfoFactor):
        return f
    lam, eta = {}, {}
    for u in f.keys:
        aut = tr(f.blocks[u])
        eta[u] = mv(aut, f.b)
        for w in f.keys:
            lam[(u, w)] = mm(aut, f.blocks[w])
    return InfoFactor(f.keys, lam, eta)


def _accumulate(dst, key, blk):
    if key not in dst:
        dst[key] = [list(r) if isinstance(r, list) else r for r in blk]
        return
    cur = dst[key]
    for i in range(len(cur)):
        if isinstance(cur[i], list):
            for j in range(len(cur[i])):
                cur[i][j] += blk[i][j]
        else:
            cur[i] += blk[i]


def product(factors, pos):
    lam, eta = {}, {}
    keys = set()
    for f in factors:
        f = to_info(f)
        keys |= set(f.keys)
        for kw, blk in f.lam.items():
            _accumulate(lam, kw, blk)
        for k, vec in f.eta.items():
            _accumulate(eta, k, vec)
    return InfoFactor(sorted(keys, key=pos.get), lam, eta)


class Conditional:
    """R x_v + sum over the parents s of S[s] x_s = d."""

    def __init__(self, var, parents, r, s, d):
        self.var = var
        self.parents = list(parents)
        self.r = r
        self.s = s
        self.d = d

    def solve(self, values):
        rhs = list(self.d)
        for p in self.parents:
            rhs = [a - b for a, b in zip(rhs, mv(self.s[p], values[p]))]
        return backward(self.r, rhs)

    def as_factor(self):
        """The conditional read as the factor 1/2 ||R x_v + sum S_s x_s - d||^2."""
        blocks = {self.var: self.r}
        blocks.update(self.s)
        return LinearFactor(blocks, self.d)


def eliminate_variable(joint, v):
    rest = [k for k in joint.keys if k != v]
    r = upper_cholesky(joint.lam[(v, v)])
    s = {}
    for k in rest:
        blk = joint.lam.get((v, k))
        if blk is None:
            blk = [[0.0] * len(joint.eta[k]) for _ in range(len(r))]
        s[k] = tr([forward(r, col) for col in tr(blk)])
    d = forward(r, joint.eta[v])
    lam, eta = {}, {}
    for a in rest:
        sat = tr(s[a])
        eta[a] = [x - y for x, y in zip(joint.eta[a], mv(sat, d))]
        for b in rest:
            corr = mm(sat, s[b])
            base = joint.lam.get((a, b))
            if base is None:
                lam[(a, b)] = [[-x for x in row] for row in corr]
            else:
                lam[(a, b)] = [[x - y for x, y in zip(r1, r2)] for r1, r2 in zip(base, corr)]
    return Conditional(v, rest, r, s, d), InfoFactor(rest, lam, eta)


def eliminate(factors, order):
    """Variable elimination in the given order; return the conditionals in that order."""
    pos = {v: i for i, v in enumerate(order)}
    pool = {v: [] for v in order}
    for f in factors:
        pool[min(f.keys, key=pos.get)].append(f)
    conds = []
    for v in order:  # @line L1
        group = pool.pop(v)  # @line L2
        cond, rest = eliminate_variable(product(group, pos), v)  # @line L3
        conds.append(cond)
        if rest.keys:
            pool[min(rest.keys, key=pos.get)].append(rest)  # @line L4
    return conds


def min_degree_order(variables, factors, last=()):
    """Minimum degree on the variables; the variables in last go after the others."""
    last = set(last)
    nb = {v: set() for v in variables}
    for f in factors:
        for u in f.keys:
            nb[u] |= set(f.keys) - {u}
    order = []
    for group in ([v for v in variables if v not in last], [v for v in variables if v in last]):
        left = set(group)
        while left:
            u = min(left, key=lambda v: (len(nb[v]), repr(v)))
            left.discard(u)
            around = nb.pop(u)
            for a in around:
                nb[a].discard(u)
                nb[a] |= around - {a}
            order.append(u)
    return order


# --------------------------------------------------------------- the tree


class Clique:
    def __init__(self, frontals, sep, parent):
        self.frontals = frontals  # in elimination order
        self.sep = sep
        self.parent = parent
        self.children = []
        self.conds = {}

    def variables(self):
        return set(self.frontals) | set(self.sep)


class BayesTree:
    def __init__(self):
        self.roots = []
        self.clique_of = {}

    @classmethod
    def build(cls, factors, order=None):
        tree = cls()
        variables = sorted({k for f in factors for k in f.keys}, key=repr)
        if order is None:
            order = min_degree_order(variables, factors)
        conds = eliminate(factors, order)
        _, roots, clique_of = group_into_cliques(conds, {v: i for i, v in enumerate(order)})
        tree.roots, tree.clique_of = roots, clique_of
        return tree

    def cliques(self):
        out, stack = [], list(self.roots)
        while stack:
            c = stack.pop()
            out.append(c)
            stack.extend(c.children)
        return out

    def solve(self):
        values = {}
        stack = list(self.roots)
        while stack:  # @line L10
            c = stack.pop()
            for v in reversed(c.frontals):
                values[v] = c.conds[v].solve(values)  # @line L11
            stack.extend(c.children)
        return values

    def update(self, new_factors):
        """Add linear factors; return (removed cliques, new cliques)."""
        new_keys = {k for f in new_factors for k in f.keys}
        top = set()
        for v in new_keys & set(self.clique_of):  # @line L12
            c = self.clique_of[v]
            while c is not None and c not in top:
                top.add(c)
                c = c.parent
        orphans = [ch for c in top for ch in c.children if ch not in top]  # @line L13
        group = [cond.as_factor() for c in top for cond in c.conds.values()]  # @line L14
        group += list(new_factors)
        variables = sorted({v for c in top for v in c.frontals} | (new_keys - set(self.clique_of)), key=repr)
        order = min_degree_order(variables, group, last=new_keys)
        conds = eliminate(group, order)  # @line L15
        pos = {v: i for i, v in enumerate(order)}
        made, roots, clique_of = group_into_cliques(conds, pos)
        for o in orphans:  # @line L16
            p = clique_of[min(o.sep, key=pos.get)]
            o.parent = p
            p.children.append(o)
        self.roots = [r for r in self.roots if r not in top] + roots
        self.clique_of.update(clique_of)
        return len(top), len(made)


def group_into_cliques(conds, pos):
    """Return (cliques, roots, map from a variable to its clique)."""
    clique_of, made, roots = {}, [], []
    for cond in reversed(conds):  # @line L5
        v = cond.var
        if not cond.parents:
            c = Clique([v], [], None)  # @line L6
            made.append(c)
            roots.append(c)
        else:
            p = clique_of[min(cond.parents, key=pos.get)]  # @line L7
            if p.variables() == set(cond.parents):
                p.frontals.insert(0, v)  # @line L8
                c = p
            else:
                c = Clique([v], list(cond.parents), p)  # @line L9
                p.children.append(c)
                made.append(c)
        c.conds[v] = cond
        clique_of[v] = c
    return made, roots, clique_of
