# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cole-vishkin/. The authors are listed in prov/PCJE4Q.jsonl.

"""Cole-Vishkin colour reduction (deterministic coin tossing), simulated round by round in the LOCAL model.

On an oriented ring every node knows its successor. On a rooted tree every
node knows its parent. One round is one synchronous step: every node reads the
colours of its neighbours from before the round, and then all nodes change
their colours at the same time.

Precondition: the identifiers are distinct integers in [0, N), and every node
knows N. succ describes one directed cycle with at least 3 nodes; parent
describes a rooted forest, with parent[v] == -1 at a root.
Cost: steps(N) + 3 rounds on a ring and steps(N) + 6 rounds on a forest, with
steps(N) <= log* N. Each node does O(log N) work in a round and each message
holds one colour of O(log N) bits.
"""


def lg_ceil(b: int) -> int:
    """Return the ceiling of log2(b) for b >= 1."""
    return (b - 1).bit_length()


def cv_value(c: int, d: int) -> int:
    """New colour of a node with colour c whose successor (or parent) has colour d != c."""
    x = c ^ d
    i = (x & -x).bit_length() - 1  # the lowest bit where c and d differ
    return 2 * i + ((c >> i) & 1)


def steps(N: int) -> int:
    """Number of reduction steps that take the colour range from N down to at most 6."""
    b, t = N, 0
    while b > 6:
        b = 2 * lg_ceil(b)
        t += 1
    return t


def log_star(N: int) -> int:
    """The least k such that N <= tower(k), where tower(0) = 1 and tower(k + 1) = 2 ** tower(k)."""
    k, t = 0, 1
    while N > t:
        t = 2**t
        k += 1
    return k


def cole_vishkin_ring(
    succ: list[int], ids: list[int], N: int, history: list[list[int]] | None = None
) -> tuple[list[int], int]:
    """Return (colours in {0, 1, 2}, rounds) for the oriented ring given by succ."""
    n = len(succ)
    pred = [0] * n
    for v in range(n):
        pred[succ[v]] = v
    c = list(ids)  # @line L1
    b = N
    rounds = 0
    while b > 6:  # @line L2
        rounds += 1
        seen = [c[succ[v]] for v in range(n)]  # @line L3
        c = [cv_value(c[v], seen[v]) for v in range(n)]  # @line L4 L5
        b = 2 * lg_ceil(b)  # @line L6
        if history is not None:
            history.append(list(c))
    for x in (5, 4, 3):  # @line L7
        rounds += 1
        old = list(c)
        for v in range(n):
            if old[v] == x:
                c[v] = min({0, 1, 2} - {old[pred[v]], old[succ[v]]})  # @line L8
        if history is not None:
            history.append(list(c))
    return c, rounds  # @line L9


def cole_vishkin_tree(parent: list[int], ids: list[int], N: int) -> tuple[list[int], int]:
    """Return (colours in {0, 1, 2}, rounds) for the rooted forest given by parent.

    A root acts as if its parent had its own colour with bit 0 flipped. The
    reduction from 6 to 3 colours does a shift-down before each colour class,
    as in Goldberg, Plotkin and Shannon (1988).
    """
    n = len(parent)
    children: list[list[int]] = [[] for _ in range(n)]
    for v in range(n):
        if parent[v] >= 0:
            children[parent[v]].append(v)
    c = list(ids)
    b = N
    rounds = 0
    while b > 6:
        rounds += 1
        seen = [c[parent[v]] if parent[v] >= 0 else c[v] ^ 1 for v in range(n)]
        c = [cv_value(c[v], seen[v]) for v in range(n)]
        b = 2 * lg_ceil(b)
    for x in (5, 4, 3):
        rounds += 1  # shift-down: take the parent's colour; a root takes a new colour
        old = list(c)
        for v in range(n):
            c[v] = old[parent[v]] if parent[v] >= 0 else min({0, 1, 2} - {old[v]})
        rounds += 1  # recolour the class x
        old = list(c)
        for v in range(n):
            if old[v] == x:
                used = {old[u] for u in children[v]}
                if parent[v] >= 0:
                    used.add(old[parent[v]])
                c[v] = min({0, 1, 2} - used)
    return c, rounds
