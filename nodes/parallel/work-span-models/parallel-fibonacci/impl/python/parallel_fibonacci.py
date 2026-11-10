# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-fibonacci/. The authors are listed in prov/SX5BQA.jsonl.

"""P-FIB, the multithreaded Fibonacci program of CLRS, with its work and span.

The cost model is the strand model of CLRS (third edition, Section 27.1):
a call P-FIB(n) with n <= 1 is one strand. A call with n >= 2 is three
strands: A runs up to the spawn, B runs from the spawn up to the call of
P-FIB(n - 2), and C runs after the sync. A spawns the child P-FIB(n - 1)
and continues with B; B calls P-FIB(n - 2); C waits for both. Each strand
costs one unit.

p_fib(n) runs the program as its serial elision (the spawn becomes a call)
and returns (F(n), work, span), composed by the series and parallel rules.
pfib_dag(n) builds the DAG of strands, so that a test can check the rules.
cost(n) gives the work and span from the recurrences in O(n) steps.
The recursion depth of p_fib and pfib_dag is n, so use n below about 900.
"""


def p_fib(n: int) -> tuple[int, int, int]:
    """Return (F(n), work, span) of P-FIB(n)."""
    if n <= 1:  # @line L1
        return n, 1, 1
    x, wx, sx = p_fib(n - 1)  # @line L2  the spawned child: it runs in parallel with strand B
    y, wy, sy = p_fib(n - 2)  # @line L3  called from strand B
    # @line L4  sync: strand C starts after the child and after the call
    work = 3 + wx + wy
    span = max(1 + sx + 1,      # A, then the child, then C
               1 + 1 + sy + 1)  # A, B, then the call, then C
    return x + y, work, span  # @line L5


def pfib_dag(n: int) -> list[list[int]]:
    """Return succ, the strand DAG of P-FIB(n). Node 0 is the first strand."""
    succ: list[list[int]] = []

    def new() -> int:
        succ.append([])
        return len(succ) - 1

    def build(k: int) -> tuple[int, int]:
        if k <= 1:
            s = new()
            return s, s
        a, b = new(), new()
        succ[a].append(b)                # continuation edge A -> B
        c1, c2 = build(k - 1)
        succ[a].append(c1)               # spawn edge A -> child
        d1, d2 = build(k - 2)
        succ[b].append(d1)               # call edge B -> P-FIB(k - 2)
        c = new()
        succ[c2].append(c)               # return edge of the child
        succ[d2].append(c)               # return edge of the call
        return a, c

    build(n)
    return succ


def dag_work_span(succ: list[list[int]]) -> tuple[int, int]:
    """Work (nodes) and span (nodes on a longest path) of a DAG."""
    n = len(succ)
    indeg = [0] * n
    for vs in succ:
        for v in vs:
            indeg[v] += 1
    longest = [1] * n
    ready = [u for u in range(n) if indeg[u] == 0]
    while ready:
        u = ready.pop()
        for v in succ[u]:
            longest[v] = max(longest[v], longest[u] + 1)
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
    return n, max(longest, default=0)


def cost(n: int) -> tuple[int, int]:
    """Work and span of P-FIB(n) from the recurrences, without running it."""
    w = [1, 1]
    s = [1, 1]
    for k in range(2, n + 1):
        w.append(w[k - 1] + w[k - 2] + 3)
        s.append(max(s[k - 1] + 2, s[k - 2] + 3))
    return w[n], s[n]


def fib(n: int) -> int:
    """F(n) by iteration, the reference value."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
