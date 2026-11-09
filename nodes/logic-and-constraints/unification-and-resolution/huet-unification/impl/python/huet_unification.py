# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/huet-unification/. The authors are listed in prov/XZKWT3.jsonl.
"""Huet's almost-linear first-order unification on a term DAG with union-find.

A term is a variable, written as a string, or a tuple (f, t1, ..., tn) for a
function symbol f applied to n terms; a constant is (c,). The two input terms
are stored as one DAG in which equal subterms share a node.
"""


class TermDag:
    def __init__(self):
        self.label = []  # a variable name, or (symbol, arity)
        self.kids = []
        self.ids = {}

    def node(self, t):
        if isinstance(t, str):
            key = ("var", t)
            kids = ()
            label = t
        else:
            kids = tuple(self.node(a) for a in t[1:])
            key = (t[0], kids)
            label = (t[0], len(kids))
        if key not in self.ids:
            self.ids[key] = len(self.label)
            self.label.append(label)
            self.kids.append(kids)
        return self.ids[key]

    def is_fun(self, n):
        return not isinstance(self.label[n], str)


def unify(s, t):
    """A most general unifier of s and t as a dict from variables to terms, or None."""
    dag = TermDag()
    u0, v0 = dag.node(s), dag.node(t)
    n = len(dag.label)
    parent = list(range(n))  # @line L1
    rank = [0] * n
    schema = list(range(n))

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def union(x, y, sch):
        if rank[x] < rank[y]:
            x, y = y, x
        parent[y] = x
        if rank[x] == rank[y]:
            rank[x] += 1
        schema[x] = sch

    stack = [(u0, v0)]  # @line L2
    while stack:  # @line L3
        u, v = stack.pop()  # @line L4
        u, v = find(u), find(v)  # @line L5
        if u == v:
            continue  # @line L6
        a, b = schema[u], schema[v]  # @line L7
        if dag.is_fun(a) and dag.is_fun(b):  # @line L8
            if dag.label[a] != dag.label[b]:
                return None  # @line L9
            union(u, v, a)  # @line L10
            stack.extend(zip(dag.kids[a], dag.kids[b]))  # @line L11
        else:
            union(u, v, a if dag.is_fun(a) else b)  # @line L12

    # L13: the graph of classes, with an edge from the class of each schema to the classes of its children.
    succ = {}
    for x in range(n):
        r = find(x)
        if r not in succ:
            sch = schema[r]
            succ[r] = [find(c) for c in dag.kids[sch]] if dag.is_fun(sch) else []  # @line L13
    color = dict.fromkeys(succ, 0)
    for root in succ:  # @line L14
        if color[root]:
            continue
        color[root] = 1
        work = [(root, iter(succ[root]))]
        while work:
            x, it = work[-1]
            y = next(it, None)
            if y is None:
                color[x] = 2
                work.pop()
            elif color[y] == 1:
                return None  # @line L15
            elif color[y] == 0:
                color[y] = 1
                work.append((y, iter(succ[y])))

    memo = {}

    def read(r):
        if r not in memo:
            sch = schema[r]
            if dag.is_fun(sch):
                memo[r] = (dag.label[sch][0],) + tuple(read(find(c)) for c in dag.kids[sch])
            else:
                memo[r] = dag.label[sch]
        return memo[r]

    sigma = {}
    for x in range(n):
        if not dag.is_fun(x):
            value = read(find(x))  # @line L16
            if value != dag.label[x]:
                sigma[dag.label[x]] = value
    return sigma
