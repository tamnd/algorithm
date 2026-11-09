# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-sat-algorithm/. The authors are listed in prov/7XSPN7.jsonl.

"""The linear-time 2-SAT algorithm of Aspvall, Plass and Tarjan (1979).

A formula is a list of clauses in DIMACS style: a clause is a list of nonzero
ints, where v > 0 is the variable v and -v is its negation. Each clause has at
most two literals. The variables are 1 .. n.
"""


def vertex(lit: int) -> int:
    """The vertex of a literal: 2(v - 1) for v and 2(v - 1) + 1 for -v."""
    return 2 * (abs(lit) - 1) + (1 if lit < 0 else 0)


def tarjan_components(adj: list[list[int]]) -> list[int]:
    """Number the strongly connected components of a directed graph.

    The components get the numbers 0, 1, 2, ... in the order in which
    Tarjan's algorithm finishes them. This is a reverse topological order:
    for each arc u -> w, comp[u] >= comp[w]. Iterative, Theta(V + E) time.
    """
    n = len(adj)
    index = [-1] * n
    low = [0] * n
    on_stack = [False] * n
    comp = [-1] * n
    stack: list[int] = []
    counter = 0
    ncomp = 0
    for s in range(n):
        if index[s] != -1:
            continue
        index[s] = low[s] = counter
        counter += 1
        stack.append(s)
        on_stack[s] = True
        work = [(s, 0)]
        while work:
            v, i = work[-1]
            if i < len(adj[v]):
                work[-1] = (v, i + 1)
                w = adj[v][i]
                if index[w] == -1:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on_stack[w] = True
                    work.append((w, 0))
                elif on_stack[w]:
                    low[v] = min(low[v], index[w])
                continue
            work.pop()
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
            if low[v] == index[v]:
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    comp[w] = ncomp
                    if w == v:
                        break
                ncomp += 1
    return comp


def two_sat_algorithm(n: int, clauses: list[list[int]]) -> list[bool] | None:
    """Decide a 2-CNF formula over the variables 1 .. n.

    Precondition: each clause has at most two literals, each in 1 .. n in
    absolute value. Returns a model as a list x of n booleans, where x[v - 1]
    is the value of the variable v, or None when the formula is
    unsatisfiable. Time and space Theta(n + m) for m clauses.
    """
    if any(len(c) == 0 for c in clauses):  # @line L1
        return None
    adj: list[list[int]] = [[] for _ in range(2 * n)]  # @line L2
    for c in clauses:  # @line L3
        a = c[0]
        b = c[1] if len(c) == 2 else c[0]  # a unit clause (a) is (a or a)
        adj[vertex(-a)].append(vertex(b))  # @line L4
        adj[vertex(-b)].append(vertex(a))
    comp = tarjan_components(adj)  # @line L5
    for v in range(1, n + 1):  # @line L6
        if comp[vertex(v)] == comp[vertex(-v)]:
            return None  # @line L7
    # v is true when the component of v is finished before the one of -v
    x = [comp[vertex(v)] < comp[vertex(-v)] for v in range(1, n + 1)]  # @line L8
    return x  # @line L9
