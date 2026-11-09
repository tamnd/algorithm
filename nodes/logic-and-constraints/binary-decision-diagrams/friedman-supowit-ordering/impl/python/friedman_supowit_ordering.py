# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/friedman-supowit-ordering/. The authors are listed in prov/T03ZRT.jsonl.

"""The Friedman-Supowit dynamic program for an optimal OBDD variable order.

The input is the truth table of f: table[a] is f(x) for the assignment a with
x_i = bit i of a, for the variables x_0, ..., x_{n-1} (x_{i+1} of the page is
x_i here). The values can be any hashable objects, so multi-terminal tables
work as well. An order is a list of the variables from the top level to the
bottom level. The size of an OBDD counts the inner nodes and the sinks.

The program builds the order from the bottom. For a set J of bottom variables
it keeps the table T_J, which maps each assignment of the other variables to
an id of the subfunction on J. Equal subfunctions get equal ids. The number of
nodes of x when x sits directly above J is the number of distinct pairs
(T_J[b, x=0], T_J[b, x=1]) with two different ids, and it does not depend on
the order inside J.

Cost: O(n 3^n) dictionary operations and O(3^n / n^(1/2)) entries of memory
for two adjacent layers. Precondition: len(table) == 2^n.
"""

from itertools import permutations
from typing import Hashable


def level_cost(t: dict[int, int], x: int) -> int:
    """The number of x-nodes when x sits directly above the set of t."""
    bit = 1 << x
    seen = set()
    for b, p in t.items():
        if b & bit == 0:
            q = t[b | bit]
            if p != q:
                seen.add((p, q))
    return len(seen)


def lift(t: dict[int, int], x: int, fresh: list[int]) -> dict[int, int]:
    """The table of J + {x} from the table of J. fresh[0] is the next free id."""
    bit = 1 << x
    ids: dict[tuple[int, int], int] = {}
    out: dict[int, int] = {}
    for b, p in t.items():
        if b & bit == 0:
            q = t[b | bit]
            if p == q:
                out[b] = p
            else:
                key = (p, q)
                if key not in ids:
                    ids[key] = fresh[0]
                    fresh[0] += 1
                out[b] = ids[key]
    return out


def friedman_supowit(table: list[Hashable], n: int, maximize: bool = False) -> tuple[int, list[int]]:
    """Return (size, order) of an OBDD of minimum size over all n! orders.

    With maximize=True, return the maximum size and an order that gives it.
    """
    assert len(table) == 1 << n
    values: dict[Hashable, int] = {}
    t0: dict[int, int] = {}
    for a, v in enumerate(table):
        t0[a] = values.setdefault(v, len(values))
    fresh = [len(values)]
    full = (1 << n) - 1
    tables: dict[int, dict[int, int]] = {0: t0}  # @line L1
    cost: dict[int, int] = {0: 0}  # @line L2
    choice: dict[int, int] = {}
    for k in range(n):  # @line L3
        new_tables: dict[int, dict[int, int]] = {}
        for J in tables:  # @line L4
            for x in range(n):  # @line L5
                if J >> x & 1:
                    continue
                K = J | 1 << x
                c = cost[J] + level_cost(tables[J], x)  # @line L6
                old = cost.get(K)
                if old is None or (c > old if maximize else c < old):  # @line L7
                    cost[K] = c
                    choice[K] = x
                if x == (K & -K).bit_length() - 1:  # @line L8
                    new_tables[K] = lift(tables[J], x, fresh)
        for J in tables:
            del cost[J]
        tables = new_tables  # @line L9
    order: list[int] = []
    K = full
    while K:  # @line L10
        x = choice[K]
        order.append(x)
        K &= ~(1 << x)
    return cost[full] + len(values), order  # @line L11


def obdd_size(table: list[Hashable], n: int, order: list[int]) -> int:
    """The size of the reduced OBDD of the table under the order, by counting
    the distinct subfunctions that depend on the variable of each level."""
    assert sorted(order) == list(range(n))
    total = len(set(table))
    for k, x in enumerate(order):
        rest = order[k + 1:]
        subs = set()
        for top in range(1 << k):
            fixed = 0
            for j in range(k):
                if top >> j & 1:
                    fixed |= 1 << order[j]
            lo = []
            hi = []
            for low in range(1 << len(rest)):
                a = fixed
                for j, y in enumerate(rest):
                    if low >> j & 1:
                        a |= 1 << y
                lo.append(table[a])
                hi.append(table[a | 1 << x])
            if lo != hi:
                subs.add((tuple(lo), tuple(hi)))
        total += len(subs)
    return total


def brute_force(table: list[Hashable], n: int) -> tuple[int, int]:
    """The minimum and the maximum OBDD size over all n! orders."""
    sizes = [obdd_size(table, n, list(p)) for p in permutations(range(n))]
    return min(sizes), max(sizes)
