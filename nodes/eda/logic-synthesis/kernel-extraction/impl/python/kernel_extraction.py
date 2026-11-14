# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-extraction/. The authors are listed in prov/6VFGF9.jsonl.

"""Kernel extraction by rectangles of the kernel-cube matrix.

A literal is 2 * v + c for the variable v and c = 1 for the complement, a
cube is a frozenset of literals, and an SOP is a frozenset of cubes. A
network maps each node variable to its SOP over the primary inputs and the
other node variables, with no cycle.

KERNELS(F) lists the pairs (cokernel, kernel) of F by the recursion of
Brayton and McMullen. EXTRACT builds the kernel-cube matrix of all nodes,
grows a rectangle greedily from each row, and if the best one saves
literals it makes the sum of its column cubes a new node and rewrites the
rows to use it. It repeats until no rectangle found has positive value.
"""

from typing import Optional

Cube = frozenset
Sop = frozenset
Network = dict


def common_cube(f: Sop) -> Cube:
    """The largest cube that divides every cube of f (f must be nonempty)."""
    return frozenset.intersection(*f)


def divide_by_cube(f: Sop, c: Cube) -> Sop:
    """The algebraic quotient f / c."""
    return frozenset(x - c for x in f if c <= x)


def is_cube_free(f: Sop) -> bool:
    """True if f has two or more cubes and no literal common to all of them."""
    return len(f) >= 2 and not common_cube(f)


def literals(f: Sop) -> int:
    return sum(len(c) for c in f)


def kernels(f: Sop) -> list:
    """All pairs (cokernel, kernel) of f, each once."""
    if len(f) < 2:
        return []
    order = sorted({l for c in f for l in c})
    index = {l: i for i, l in enumerate(order)}
    out: list = []

    def rec(g: Sop, cok: Cube, j: int) -> None:
        for i in range(j, len(order)):  # @line L1
            l = order[i]
            s = [x for x in g if l in x]
            if len(s) < 2:  # @line L2
                continue
            c = frozenset.intersection(*s)  # @line L3
            if any(index[k] < i for k in c):  # @line L4
                continue
            rec(divide_by_cube(g, c), cok | c, i + 1)  # @line L5
        out.append((cok, g))  # @line L6

    c0 = common_cube(f)
    rec(divide_by_cube(f, c0), c0, 0)
    return out


def kernel_cube_matrix(net: Network) -> tuple:
    """Rows (node, cokernel, kernel) and the sorted list of distinct kernel cubes."""
    rows = []
    for v in sorted(net):
        for cok, ker in kernels(net[v]):
            rows.append((v, cok, ker))
    cols = sorted({c for _, _, ker in rows for c in ker}, key=lambda c: sorted(c))
    return rows, cols


def value(rows: list, chosen: list, cubes: list) -> int:
    """Literals saved by extracting the rectangle chosen x cubes."""
    covered = {(rows[r][0], rows[r][1] | c) for r in chosen for c in cubes}
    gain = sum(len(x) for _, x in covered)
    cost = sum(len(rows[r][1]) + 1 for r in chosen) + sum(len(c) for c in cubes)
    return gain - cost


def best_rectangle(rows: list) -> tuple:
    """Greedy row growth from every seed row; returns (value, rows, cubes)."""
    best: tuple = (0, [], [])
    for seed in range(len(rows)):
        chosen = [seed]
        cubes = set(rows[seed][2])
        cur = value(rows, chosen, list(cubes))
        while True:
            pick: Optional[tuple] = None
            for s in range(len(rows)):
                if s in chosen:
                    continue
                common = cubes & rows[s][2]
                if len(common) < 2:
                    continue
                val = value(rows, chosen + [s], list(common))
                if val > cur and (pick is None or val > pick[0]):
                    pick = (val, s, common)
            if pick is None:
                break
            cur, s, cubes = pick[0], pick[1], set(pick[2])
            chosen.append(s)
        if cur > best[0]:
            best = (cur, list(chosen), sorted(cubes, key=lambda c: sorted(c)))
    return best


def extract(net: Network, first_new: int) -> tuple:
    """Run extraction to the end. Returns the new network and the list of values."""
    net = dict(net)
    log = []
    x = first_new
    while True:
        rows, _ = kernel_cube_matrix(net)  # @line L7
        val, chosen, cubes = best_rectangle(rows)  # @line L8
        if val <= 0:  # @line L9
            return net, log
        net[x] = frozenset(cubes)  # @line L10
        for r in chosen:  # @line L11
            v, cok, _ = rows[r]
            removed = {cok | c for c in cubes}
            net[v] = (net[v] - removed) | {cok | {2 * x}}  # @line L12
        log.append(val)
        x += 1


def network_literals(net: Network) -> int:
    return sum(literals(f) for f in net.values())


def evaluate(net: Network, point: dict) -> dict:
    """Values of all nodes at a point that maps each primary input to 0 or 1."""
    val = dict(point)

    def get(v: int) -> int:
        if v not in val:
            val[v] = 0
            for c in net[v]:
                if all(get(l >> 1) ^ (l & 1) for l in c):
                    val[v] = 1
                    break
        return val[v]

    for v in net:
        get(v)
    return val
