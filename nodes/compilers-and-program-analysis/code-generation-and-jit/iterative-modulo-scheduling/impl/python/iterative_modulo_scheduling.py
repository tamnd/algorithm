# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-modulo-scheduling/. The authors are listed in prov/PJN90C.jsonl.
"""Iterative modulo scheduling (Rau 1994) of the body of a loop.

A loop body is given by
- n: the number of operations, numbered 0 .. n-1;
- res[v]: the reservation table of operation v, a list of pairs
  (resource, offset): v holds one unit of the resource in cycle
  t(v) + offset of its iteration;
- edges: a list of (u, v, delay, distance): operation v of iteration
  i + distance starts at least delay cycles after operation u of
  iteration i starts;
- machine: a dict from each resource to its number of units.

A modulo schedule for an initiation interval II gives each operation a
start t(v) >= 0 such that every edge has
t(v) + II * distance >= t(u) + delay, and for each resource r and slot k
in 0 .. II-1, at most machine[r] uses of r fall in cycles congruent to k
modulo II. Iteration i then starts at cycle i * II.

Precondition: offsets >= 0, distances >= 0, every resource of a table is
in machine with at least one unit, and the edges of distance 0 form no
cycle (check_loop raises ValueError otherwise).

modulo_schedule returns (II, t, MII) with MII = max(1, ResMII, RecMII).
The result is always a legal modulo schedule and II >= MII. It is a
heuristic: II may be larger than the least possible one.

Cost: with e edges, D the sum of the positive delays and w the longest
reservation table, RecMII takes O(n^3 log D) by binary search with
Floyd-Warshall. One attempt at a given II takes O(n e) for the heights
and O(budget (n + e + II w)) for the steps, budget = budget_ratio * n.
"""

NEG = float("-inf")


def check_loop(n, res, edges, machine):
    if len(res) != n:
        raise ValueError("one reservation table per operation")
    for v in range(n):
        for r, off in res[v]:
            if machine.get(r, 0) < 1 or off < 0:
                raise ValueError("bad reservation (%r, %r) of operation %d" % (r, off, v))
    succ = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v, delay, dist in edges:
        if not (0 <= u < n and 0 <= v < n) or dist < 0:
            raise ValueError("bad edge %r" % ((u, v, delay, dist),))
        if dist == 0:
            succ[u].append(v)
            indeg[v] += 1
    stack = [v for v in range(n) if indeg[v] == 0]
    seen = 0
    while stack:
        u = stack.pop()
        seen += 1
        for v in succ[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                stack.append(v)
    if seen != n:
        raise ValueError("the edges of distance 0 form a cycle")


def res_mii(n, res, machine):
    """max over resources r of ceil(uses of r / units of r)."""
    uses = {}
    for v in range(n):
        for r, _ in res[v]:
            uses[r] = uses.get(r, 0) + 1
    return max([-(-u // machine[r]) for r, u in uses.items()], default=0)


def min_dist(n, edges, ii):
    """M[i][j]: the largest sum of delay - ii * distance over the walks from
    i to j with at least one edge that Floyd-Warshall builds; -inf if there
    is none. Some M[i][i] > 0 exactly when some cycle has a positive sum."""
    m = [[NEG] * n for _ in range(n)]
    for u, v, delay, dist in edges:
        m[u][v] = max(m[u][v], delay - ii * dist)
    for k in range(n):
        mk = m[k]
        for i in range(n):
            a = m[i][k]
            if a == NEG:
                continue
            mi = m[i]
            for j in range(n):
                if a + mk[j] > mi[j]:
                    mi[j] = a + mk[j]
    return m


def has_positive_cycle(n, edges, ii):
    m = min_dist(n, edges, ii)
    return any(m[i][i] > 0 for i in range(n))


def rec_mii(n, edges):
    """The least II >= 0 such that no cycle has delay(C) > II * distance(C),
    that is max(0, max over cycles C of ceil(delay(C) / distance(C)))."""
    lo, hi = 0, sum(max(e[2], 0) for e in edges)
    while lo < hi:
        mid = (lo + hi) // 2
        if has_positive_cycle(n, edges, mid):
            lo = mid + 1
        else:
            hi = mid
    return lo


def height_r(n, edges, ii):
    """HeightR(v): the longest sum of delay - ii * distance over paths from v,
    at least 0. Bellman-Ford rounds; there is no positive cycle."""
    h = [0] * n
    for _ in range(n):
        changed = False
        for u, v, delay, dist in edges:
            x = h[v] + delay - ii * dist
            if x > h[u]:
                h[u] = x
                changed = True
        if not changed:
            break
    return h


def _slots(v, s, res, ii):
    need = {}
    for r, off in res[v]:
        key = (r, (s + off) % ii)
        need[key] = need.get(key, 0) + 1
    return need


def _fits(v, s, mrt, res, machine, ii):
    return all(len(mrt.get(key, ())) + c <= machine[key[0]] for key, c in _slots(v, s, res, ii).items())


def iterative_schedule(n, res, edges, machine, ii, budget, log=None):
    """One attempt at II. Returns (t, mrt) or None. mrt maps (resource,
    slot) to the list of operations that use it, once per use. If log is a
    list, each step appends (op, estart, slot, displaced ops)."""
    if not all(_fits(v, 0, {}, res, machine, ii) for v in range(n)):
        return None
    h = height_r(n, edges, ii)  # @line L4
    preds = [[] for _ in range(n)]
    succs = [[] for _ in range(n)]
    for u, v, delay, dist in edges:
        if u != v:
            preds[v].append((u, delay - ii * dist))
            succs[u].append((v, delay - ii * dist))
    t, prev, mrt = {}, {}, {}

    def unschedule(w):
        for key, c in _slots(w, t[w], res, ii).items():
            for _ in range(c):
                mrt[key].remove(w)
        del t[w]

    while len(t) < n and budget > 0:  # @line L5
        v = max((w for w in range(n) if w not in t), key=lambda w: (h[w], -w))  # @line L6
        estart = max([0] + [t[p] + wt for p, wt in preds[v] if p in t])  # @line L7
        s = next((x for x in range(estart, estart + ii) if _fits(v, x, mrt, res, machine, ii)), None)  # @line L8
        out = []
        if s is None:
            s = estart if v not in prev or estart > prev[v] else prev[v] + 1  # @line L9
            for key, c in _slots(v, s, res, ii).items():
                while len(mrt.get(key, ())) + c > machine[key[0]]:
                    out.append(mrt[key][0])
                    unschedule(mrt[key][0])  # @line L10
        for w, wt in succs[v]:
            if w in t and t[w] < s + wt:
                out.append(w)
                unschedule(w)  # @line L11
        t[v] = s  # @line L12
        prev[v] = s
        for key, c in _slots(v, s, res, ii).items():
            mrt.setdefault(key, []).extend([v] * c)
        budget -= 1
        if log is not None:
            log.append((v, estart, s, out))
    if len(t) < n:
        return None
    return t, mrt  # @line L13


def modulo_schedule(n, res, edges, machine, budget_ratio=3, max_ii=None, log=None):
    """Returns (II, t, MII). Tries II = MII, MII + 1, ... up to max_ii and
    raises RuntimeError if every attempt runs out of budget."""
    check_loop(n, res, edges, machine)
    mii = max(1, res_mii(n, res, machine), rec_mii(n, edges))  # @line L1
    if max_ii is None:
        max_ii = mii + sum(max(e[2], 0) for e in edges) + sum(len(r) for r in res) + n
    for ii in range(mii, max_ii + 1):  # @line L2
        if log is not None:
            log.append(("II", ii))
        got = iterative_schedule(n, res, edges, machine, ii, budget_ratio * n, log)
        if got is not None:
            return ii, got[0], mii  # @line L3
    raise RuntimeError("no schedule up to II = %d" % max_ii)


def stages(t, ii):
    """stage(v) = t(v) div II, and the number of stages SC."""
    st = {v: s // ii for v, s in t.items()}
    return st, 1 + max(st.values(), default=0)
