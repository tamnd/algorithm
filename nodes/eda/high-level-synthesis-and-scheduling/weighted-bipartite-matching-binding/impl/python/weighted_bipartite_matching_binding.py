# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-bipartite-matching-binding/. The authors are listed in prov/6HS42N.jsonl.

"""Register binding step by step through weighted bipartite matching.

A value is a tuple (birth, death, src, dst): it is held in a register in the
steps birth, ..., death (a closed interval), it is written by the unit src,
and it is read by the set dst of unit input ports. A register collects the
sources and the ports of all its values. The cost of a binding is the number
of connections: the sum over registers of |sources| + |ports|.

At each birth step, the new values are matched to the free registers, plus
fresh registers when there are too few free ones. The weight of a pair (v, r)
counts the connections that v needs and r already has. Each step takes a
matching of the largest weight that places every new value.
"""

Value = tuple[int, int, int, frozenset]


def hungarian_max(weight: list[list[int]]) -> list[int]:
    """Columns for each row of a matching that places every row and has the largest total weight.

    weight has n rows and m >= n columns. This is the O(n^2 m) Hungarian method with
    potentials, run on the costs top - weight.
    """
    n = len(weight)
    if n == 0:
        return []
    m = len(weight[0])
    top = max(max(row) for row in weight)
    inf = float("inf")
    u = [0] * (n + 1)
    v = [0] * (m + 1)
    p = [0] * (m + 1)
    way = [0] * (m + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [inf] * (m + 1)
        used = [False] * (m + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = inf
            j1 = 0
            for j in range(1, m + 1):
                if not used[j]:
                    cur = (top - weight[i0 - 1][j - 1]) - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(m + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    col = [0] * n
    for j in range(1, m + 1):
        if p[j]:
            col[p[j] - 1] = j - 1
    return col


def pair_weight(value: Value, srcs: set, ports: set) -> int:
    """Connections that value needs and the register with these sources and ports already has."""
    return (1 if value[2] in srcs else 0) + len(value[3] & ports)


def matching_bind(values: list[Value], trace: list | None = None) -> list[int]:
    """The register of each value, by one weighted bipartite matching per birth step.

    When trace is a list, each step appends (step, new values, candidate registers,
    weight matrix, chosen columns) to it.
    """
    reg_src: list[set] = []                                      # @line L1
    reg_dst: list[set] = []
    reg_end: list[int] = []
    where = [-1] * len(values)
    for t in sorted({b for b, _, _, _ in values}):               # @line L2
        new = [k for k, val in enumerate(values) if val[0] == t]  # @line L3
        free = [r for r in range(len(reg_end)) if reg_end[r] < t]  # @line L4
        for _ in range(max(0, len(new) - len(free))):            # @line L5
            reg_src.append(set())
            reg_dst.append(set())
            reg_end.append(-1)
            free.append(len(reg_end) - 1)
        w = [[pair_weight(values[k], reg_src[r], reg_dst[r]) for r in free]
             for k in new]                                       # @line L6
        col = hungarian_max(w)                                   # @line L7
        if trace is not None:
            trace.append((t, list(new), list(free), w, list(col)))
        for a, k in enumerate(new):                              # @line L8
            r = free[col[a]]
            where[k] = r
            reg_src[r].add(values[k][2])
            reg_dst[r] |= values[k][3]
            reg_end[r] = values[k][1]
    return where                                                 # @line L9


def connections(values: list[Value], where: list[int]) -> int:
    """Sum over registers of the number of distinct sources and of distinct ports."""
    srcs: dict[int, set] = {}
    ports: dict[int, set] = {}
    for val, r in zip(values, where):
        srcs.setdefault(r, set()).add(val[2])
        ports.setdefault(r, set()).update(val[3])
    return sum(len(srcs[r]) + len(ports[r]) for r in srcs)


def is_valid(values: list[Value], where: list[int]) -> bool:
    """True when no two values in one register are live in a common step."""
    for a in range(len(values)):
        for b in range(a + 1, len(values)):
            if where[a] == where[b]:
                if not (values[a][1] < values[b][0] or values[b][1] < values[a][0]):
                    return False
    return True


def max_live(values: list[Value]) -> int:
    """The largest number of values live in one step."""
    if not values:
        return 0
    return max(sum(1 for b, e, _, _ in values if b <= t <= e) for t in {b for b, _, _, _ in values})
