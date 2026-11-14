# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sdf-static-scheduling/. The authors are listed in prov/XS6G6S.jsonl.

"""Static scheduling of a synchronous dataflow graph (Lee and Messerschmitt).

Actors are 0, ..., n - 1. An edge is (src, dst, prod, cons, delay): each
firing of src puts prod tokens on it, each firing of dst takes cons tokens
from it, and it holds delay tokens at the start. The graph must be
connected (as an undirected graph).
"""

from collections import deque
from fractions import Fraction
from math import gcd, lcm


def topology_matrix(n, edges):
    """Gamma with one row per edge: +prod in the src column, -cons in the dst column."""
    rows = []
    for s, d, p, c, _ in edges:
        row = [0] * n
        row[s] += p
        row[d] -= c
        rows.append(row)
    return rows


def repetition_vector(n, edges):
    """The least positive integer q with Gamma q = 0, or None if none exists.

    Fix q_0 = 1, give every actor reached along an edge the rate that the
    balance equation of that edge forces, then check every edge.
    """
    adj = [[] for _ in range(n)]
    for s, d, p, c, _ in edges:
        if p <= 0 or c <= 0:
            raise ValueError("rates must be positive")
        adj[s].append((d, Fraction(p, c)))
        adj[d].append((s, Fraction(c, p)))
    q = [None] * n
    q[0] = Fraction(1)
    stack = [0]
    while stack:
        a = stack.pop()
        for b, f in adj[a]:
            if q[b] is None:
                q[b] = q[a] * f  # @line L1
                stack.append(b)
    if any(x is None for x in q):
        raise ValueError("the graph is not connected")
    if any(q[s] * p != q[d] * c for s, d, p, c, _ in edges):  # @line L2
        return None
    m = lcm(*(x.denominator for x in q))  # @line L3
    ints = [int(x * m) for x in q]
    g = 0
    for x in ints:
        g = gcd(g, x)
    return [x // g for x in ints]


def schedule(n, edges):
    """Return (q, firing sequence) for one period, or (q, None) on deadlock.

    q is None when the balance equations have no positive solution. The
    simulation fires any actor that has enough tokens on every input edge
    and has fired fewer than q times. A FIFO worklist holds actors to look
    at again; an actor is put back when a firing adds tokens to one of its
    input edges.
    """
    q = repetition_vector(n, edges)
    if q is None:
        return None, None
    ins = [[] for _ in range(n)]
    outs = [[] for _ in range(n)]
    for i, (s, d, p, c, _) in enumerate(edges):
        outs[s].append(i)
        ins[d].append(i)
    tokens = [e[4] for e in edges]  # @line L4
    count = [0] * n
    seq = []
    work = deque(range(n))
    queued = [True] * n
    while work:  # @line L5
        a = work.popleft()  # @line L6
        queued[a] = False
        if count[a] == q[a] or any(tokens[i] < edges[i][3] for i in ins[a]):  # @line L7
            continue
        for i in ins[a]:  # @line L8
            tokens[i] -= edges[i][3]
        for i in outs[a]:
            tokens[i] += edges[i][2]
        count[a] += 1  # @line L9
        seq.append(a)
        for b in [a] + [edges[i][1] for i in outs[a]]:  # @line L10
            if not queued[b]:
                queued[b] = True
                work.append(b)
    if count != q:  # @line L11
        return q, None
    return q, seq


def buffer_sizes(edges, seq):
    """The largest token count of each edge while seq runs."""
    tokens = [e[4] for e in edges]
    peak = list(tokens)
    for a in seq:
        for i, (s, d, p, c, _) in enumerate(edges):
            if d == a:
                tokens[i] -= c
        for i, (s, d, p, c, _) in enumerate(edges):
            if s == a:
                tokens[i] += p
                peak[i] = max(peak[i], tokens[i])
    return peak
