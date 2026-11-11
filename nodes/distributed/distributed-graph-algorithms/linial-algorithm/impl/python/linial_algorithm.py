# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linial-algorithm/. The authors are listed in prov/RAK95W.jsonl.

"""Linial's colour reduction with polynomial cover-free families, simulated round by round in the LOCAL model.

A colour x < q^(d+1) names the polynomial p_x over GF(q) whose coefficients
are the base-q digits of x, and the set S_x = {(a, p_x(a))} of q points. Two
such sets share at most d points, so when q > Delta * d no set is covered by
Delta others. In one round each node reads its neighbours' colours and takes
the least point of its own set that no neighbour's set contains. Then one
colour class per round moves into {0, ..., Delta}.

Precondition: adj is an undirected simple graph with maximum degree at most
Delta; the identifiers are distinct integers in [0, N), and every node knows
N and Delta.
Cost: O(log* N) rounds to reach O(Delta^2) colours, then at most that many
rounds to reach Delta + 1 colours. A message holds one colour.
"""


def is_prime(q: int) -> bool:
    """Trial division; q is small here."""
    if q < 2:
        return False
    i = 2
    while i * i <= q:
        if q % i == 0:
            return False
        i += 1
    return True


def root_ceil(m: int, k: int) -> int:
    """The least integer r >= 1 with r ** k >= m."""
    lo, hi = 1, 1
    while hi**k < m:
        hi *= 2
    while lo < hi:  # binary search for the least r with r ** k >= m
        mid = (lo + hi) // 2
        if mid**k >= m:
            hi = mid
        else:
            lo = mid + 1
    return lo


def choose(m: int, delta: int) -> tuple[int, int]:
    """Return (q, d) with q prime, q > delta * d and q^(d+1) >= m, with q as small as possible."""
    best: tuple[int, int] | None = None
    for d in range(max(2, m.bit_length()), 0, -1):
        q = max(2, delta * d + 1, root_ceil(m, d + 1))
        if best is not None and q >= best[0]:
            continue
        while not is_prime(q) or q ** (d + 1) < m:
            q += 1
        if best is None or q < best[0]:
            best = (q, d)
    assert best is not None
    return best


def schedule(N: int, delta: int) -> list[tuple[int, int, int]]:
    """The list of (m, q, d) for the reduction steps, starting from m = N colours."""
    out = []
    m = N
    while True:
        q, d = choose(m, delta)
        if q * q >= m:
            return out
        out.append((m, q, d))
        m = q * q


def point_set(x: int, q: int, d: int) -> set[int]:
    """The set S_x, with the point (a, y) encoded as a * q + y."""
    coeffs = [(x // q**j) % q for j in range(d + 1)]
    out = set()
    for a in range(q):
        y = 0
        for cf in reversed(coeffs):
            y = (y * a + cf) % q
        out.add(a * q + y)
    return out


def linial_step(c: list[int], adj: list[list[int]], q: int, d: int) -> list[int]:
    """One round: every node takes the least point of its set that no neighbour's set holds."""
    new = []
    for v in range(len(adj)):
        blocked: set[int] = set()
        for u in adj[v]:
            blocked |= point_set(c[u], q, d)  # @line L5
        free = point_set(c[v], q, d) - blocked  # @line L4 L5
        new.append(min(free))  # @line L6
    return new


def linial_coloring(
    adj: list[list[int]], ids: list[int], N: int, delta: int, history: list[list[int]] | None = None
) -> tuple[list[int], int]:
    """Return (a proper colouring with colours in [0, delta], rounds)."""
    n = len(adj)
    c = list(ids)  # @line L1
    rounds = 0
    m = N
    for _, q, d in schedule(N, delta):  # @line L2
        rounds += 1  # @line L3
        c = linial_step(c, adj, q, d)
        m = q * q  # @line L7
        if history is not None:
            history.append(list(c))
    for x in range(m - 1, delta, -1):  # @line L8
        rounds += 1
        old = list(c)
        for v in range(n):
            if old[v] == x:
                used = {old[u] for u in adj[v]}
                c[v] = min(set(range(delta + 1)) - used)  # @line L9
    return c, rounds  # @line L10
