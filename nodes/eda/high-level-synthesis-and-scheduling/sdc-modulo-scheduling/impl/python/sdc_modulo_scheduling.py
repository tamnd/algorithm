# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sdc-modulo-scheduling/. The authors are listed in prov/6XQDH6.jsonl.

"""SDC-based modulo scheduling of one loop body, in a simplified form.

Operations are 0 .. n-1 with a latency lat[v] >= 0 and a type kind[v].
An edge (u, v, dist) says that v in iteration i + dist uses the result of
u in iteration i: s[v] + II * dist >= s[u] + lat[u]. Edges with dist == 0
must form a graph with no cycle. Units are pipelined: an operation of type
k that starts at step t uses one unit of type k in the slot t mod II of the
modulo reservation table, and limits[k] units exist in each slot.

Every timing rule is a difference constraint s[v] - s[u] >= w, kept as
(u, v, w). A fixed start is a lower and an upper bound on one variable.
"""

from typing import Optional


def least_solution(n: int, cons, low: list[int], high: list[Optional[int]]) -> Optional[list[int]]:
    """Least s >= low with every row, if it also meets s <= high; else None."""
    s = list(low)
    for _ in range(n + 1):
        changed = False
        for (u, v, w) in cons:
            if s[u] + w > s[v]:
                s[v] = s[u] + w
                changed = True
        if not changed:
            break
    else:
        return None
    if any(h is not None and s[v] > h for v, h in enumerate(high)):
        return None
    return s


def dependence_rows(edges, lat: list[int], ii: int):
    return [(u, v, lat[u] - ii * dist) for (u, v, dist) in edges]


def res_mii(kind: list, limits: dict) -> int:
    count: dict = {}
    for k in kind:
        count[k] = count.get(k, 0) + 1
    return max([1] + [-(-count[k] // c) for k, c in limits.items() if k in count])


def rec_mii(n: int, edges, lat: list[int]) -> int:
    """The least II >= 1 for which the dependence rows have no positive cycle."""
    bound = 1 + sum(lat)
    for ii in range(1, bound + 1):
        if least_solution(n, dependence_rows(edges, lat, ii), [0] * n, [None] * n) is not None:
            return ii
    raise ValueError("a cycle of edges with distance 0")


def sdc_modulo_schedule(n, edges, lat, kind, limits, max_ii=None):
    """Return (II, starts) for the least II this heuristic reaches."""
    ii = max(res_mii(kind, limits), rec_mii(n, edges, lat))     # @line L1
    cap = max_ii if max_ii is not None else ii + n * (1 + max(lat, default=0)) + n
    while ii <= cap:                                             # @line L2
        s = try_ii(n, edges, lat, kind, limits, ii)
        if s is not None:
            return ii, s
        ii += 1                                                  # @line L13
    return None


def try_ii(n, edges, lat, kind, limits, ii) -> Optional[list[int]]:
    cons = dependence_rows(edges, lat, ii)                       # @line L3
    low, high = [0] * n, [None] * n
    asap = least_solution(n, cons, low, high)                    # @line L4
    if asap is None:
        return None
    mrt: dict = {}                                               # @line L5
    todo = sorted((v for v in range(n) if kind[v] in limits), key=lambda v: (asap[v], v))  # @line L6
    for v in todo:                                               # @line L7
        cur = least_solution(n, cons, low, high)
        placed = False
        for t in range(cur[v], cur[v] + ii):                     # @line L8
            slot = (kind[v], t % ii)
            if mrt.get(slot, 0) >= limits[kind[v]]:              # @line L9
                continue
            low2, high2 = list(low), list(high)
            low2[v], high2[v] = t, t
            if least_solution(n, cons, low2, high2) is not None:  # @line L10
                low, high = low2, high2
                mrt[slot] = mrt.get(slot, 0) + 1                 # @line L11
                placed = True
                break
        if not placed:
            return None                                          # @line L12
    return least_solution(n, cons, low, high)                    # @line L14


def is_valid(n, edges, lat, kind, limits, ii, s) -> bool:
    if len(s) != n or any(x < 0 for x in s):
        return False
    if any(s[v] + ii * dist < s[u] + lat[u] for (u, v, dist) in edges):
        return False
    use: dict = {}
    for v in range(n):
        if kind[v] in limits:
            key = (kind[v], s[v] % ii)
            use[key] = use.get(key, 0) + 1
            if use[key] > limits[kind[v]]:
                return False
    return True


def exact_min_ii(n, edges, lat, kind, limits, max_ii):
    """The least II with a valid modulo schedule, by search over all residues.

    For residues r, write s = r + II * q. The rows s[v] - s[u] >= w become
    q[v] - q[u] >= ceil((w - r[v] + r[u]) / II), again difference constraints.
    """
    lo = max(res_mii(kind, limits), rec_mii(n, edges, lat))
    for ii in range(lo, max_ii + 1):
        if exact_schedule(n, edges, lat, kind, limits, ii) is not None:
            return ii
    return None


def exact_schedule(n, edges, lat, kind, limits, ii) -> Optional[list[int]]:
    """A valid modulo schedule for this II, or None, by search over all residue vectors."""
    cons = dependence_rows(edges, lat, ii)
    for r in _residues(n, kind, limits, ii):
        rows = [(u, v, -(-(w - r[v] + r[u]) // ii)) for (u, v, w) in cons]
        q = least_solution(n, rows, [0] * n, [None] * n)
        if q is not None:
            return [r[v] + ii * q[v] for v in range(n)]
    return None


def _residues(n, kind, limits, ii):
    """All residue vectors whose limited operations fit the modulo reservation table."""
    use: dict = {}
    acc: list[int] = []

    def rec(v):
        if v == n:
            yield list(acc)
            return
        for x in range(ii):
            key = (kind[v], x)
            if kind[v] in limits and use.get(key, 0) >= limits[kind[v]]:
                continue
            use[key] = use.get(key, 0) + 1
            acc.append(x)
            yield from rec(v + 1)
            acc.pop()
            use[key] -= 1

    yield from rec(0)
