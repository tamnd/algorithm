# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/path-based-scheduling/. The authors are listed in prov/60ZARY.jsonl.

"""Path-based (as fast as possible) scheduling in a simple model.

The control flow graph is a DAG whose nodes are operations, given by a
successor list succ. The entry is one node; the exits are the nodes with no
successor. Every operation has a type kind[v] and a combinational delay
delay[v]. Along a path, the operations between two cuts form one state.
A state may not hold two operations of a type in `limited` (one unit each),
and the delays in one state may add up to at most `period`.

A cut sits on an edge (u, v) of the graph. On a path p = p[0], ..., p[m-1],
cut position t means the edge (p[t], p[t+1]). A constraint on p is an
interval [lo, hi] of positions that must hold at least one cut.
"""

from itertools import combinations


def stab_intervals(intervals) -> list[int]:
    """Fewest positions that hit every interval [lo, hi], by the right end greedy."""
    cuts: list[int] = []
    for lo, hi in sorted(intervals, key=lambda x: (x[1], x[0])):
        if not cuts or cuts[-1] < lo:
            cuts.append(hi)
    return cuts


def all_paths(succ: dict, entry) -> list[list]:
    """Every path from the entry to a node with no successor."""
    out: list[list] = []
    stack = [[entry]]
    while stack:
        p = stack.pop()
        nxt = succ.get(p[-1], [])
        if not nxt:
            out.append(p)
        for w in reversed(nxt):
            stack.append(p + [w])
    return out


def path_constraints(p: list, kind: dict, delay: dict, limited, period) -> list[tuple[int, int]]:
    """The intervals of cut positions on path p that must each hold a cut."""
    m = len(p)
    if any(delay[v] > period for v in p):
        raise ValueError("an operation is longer than the clock period")
    out = set()
    for i in range(m):
        for j in range(i + 1, m):
            if kind[p[i]] in limited and kind[p[i]] == kind[p[j]]:
                out.add((i, j - 1))
        total = 0
        for j in range(i, m):
            total += delay[p[j]]
            if total > period:
                out.add((i, j - 1))
                break
    return sorted(out)


def path_based_schedule(succ: dict, entry, kind: dict, delay: dict, limited, period):
    """Return (cuts, per_path) where cuts is a set of edges and per_path lists
    (path, fewest states of that path alone, states under the shared cuts)."""
    paths = all_paths(succ, entry)                               # @line L1
    rows: set = set()
    alone = []
    for p in paths:                                              # @line L2
        iv = path_constraints(p, kind, delay, limited, period)   # @line L3
        alone.append(1 + len(stab_intervals(iv)))                # @line L4
        for lo, hi in iv:                                        # @line L5
            rows.add(frozenset((p[t], p[t + 1]) for t in range(lo, hi + 1)))
    cuts = greedy_hitting_set(rows)                              # @line L6
    per_path = []
    for p, a in zip(paths, alone):
        on_p = sum((p[t], p[t + 1]) in cuts for t in range(len(p) - 1))
        per_path.append((p, a, 1 + on_p))
    return cuts, per_path                                        # @line L11


def greedy_hitting_set(rows) -> set:
    """Pick edges until every row holds one, each time the edge in most open rows."""
    open_rows = [r for r in rows]
    order: list = []
    while open_rows:                                             # @line L7
        count: dict = {}
        for r in open_rows:
            for e in r:
                count[e] = count.get(e, 0) + 1
        best = max(sorted(count), key=lambda e: count[e])        # @line L8
        order.append(best)                                       # @line L9
        open_rows = [r for r in open_rows if best not in r]
    chosen = set(order)
    for e in reversed(order):                                    # @line L10
        if all(r & (chosen - {e}) for r in rows):
            chosen.discard(e)
    return chosen


def exact_hitting_set(rows) -> set:
    """A smallest set of edges that meets every row, by search over subset sizes."""
    rows = list(rows)
    edges = sorted(set().union(*rows)) if rows else []
    for k in range(len(edges) + 1):
        for pick in combinations(edges, k):
            s = set(pick)
            if all(r & s for r in rows):
                return s
    raise AssertionError("unreachable")


def all_rows(succ: dict, entry, kind: dict, delay: dict, limited, period) -> set:
    rows: set = set()
    for p in all_paths(succ, entry):
        for lo, hi in path_constraints(p, kind, delay, limited, period):
            rows.add(frozenset((p[t], p[t + 1]) for t in range(lo, hi + 1)))
    return rows


def is_valid(succ: dict, entry, kind: dict, delay: dict, limited, period, cuts) -> bool:
    """Check the states of every path directly, without the interval model."""
    for p in all_paths(succ, entry):
        state: list = []
        for t, v in enumerate(p):
            if t > 0 and (p[t - 1], v) in cuts:
                state = []
            state.append(v)
            if sum(delay[x] for x in state) > period:
                return False
            ks = [kind[x] for x in state if kind[x] in limited]
            if len(ks) != len(set(ks)):
                return False
    return True
