# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isolation-levels/. The authors are listed in prov/VCE808.jsonl.

"""Classify a history by the phenomena of Berenson et al. (1995) and the
dependency-graph phenomena of Adya (1999).

A history is a list of operations:
  ("r", t, x)        T_t reads item x (the last write of x before it)
  ("r", t, x, j)     T_t reads the version of x written by T_j (0: initial)
  ("rp", t, P)       T_t reads the predicate P, given as a frozenset of items
  ("w", t, x)        T_t writes x (an insert is a write of a new item)
  ("c", t), ("a", t) commit, abort
Transactions are numbered from 1.
"""

from itertools import product

LEVELS = [  # Berenson et al., the broad (preventative) reading of ANSI
    ("SERIALIZABLE", {"P0", "P1", "P2", "P3"}),
    ("REPEATABLE READ", {"P0", "P1", "P2"}),
    ("READ COMMITTED", {"P0", "P1"}),
    ("READ UNCOMMITTED", {"P0"}),
]
PL = [  # Adya, Liskov and O'Neil
    ("PL-3", {"G0", "G1a", "G1b", "G1c", "G2-item", "G2"}),
    ("PL-2.99", {"G0", "G1a", "G1b", "G1c", "G2-item"}),
    ("PL-2", {"G0", "G1a", "G1b", "G1c"}),
    ("PL-1", {"G0"}),
]


def _ends(h):
    end, out = {}, {}
    for i, op in enumerate(h):
        if op[0] in "ca" and op[1] not in end:
            end[op[1]], out[op[1]] = i, op[0]
    return end, out


def berenson(h) -> set[str]:
    """The phenomena P0 to P4 and the anomalies A1, A2, A3, A5A and A5B."""
    end, out = _ends(h)
    n = len(h)
    e = lambda t: end.get(t, n)  # noqa: E731
    found = set()
    ix = list(enumerate(h))
    rs = [(i, o[1], o[2]) for i, o in ix if o[0] == "r"]
    ws = [(i, o[1], o[2]) for i, o in ix if o[0] == "w"]
    ps = [(i, o[1], o[2]) for i, o in ix if o[0] == "rp"]
    for (i, t1, x), (j, t2, y) in product(ws, ws):
        if x == y and t1 != t2 and i < j < e(t1):
            found.add("P0")
    for (i, t1, x), (j, t2, y) in product(ws, rs):
        if x == y and t1 != t2 and i < j < e(t1):
            found.add("P1")
            if out.get(t1) == "a" and out.get(t2) == "c":
                found.add("A1")
    for (i, t1, x), (j, t2, y) in product(rs, ws):
        if x == y and t1 != t2 and i < j < e(t1):
            found.add("P2")
            if any(l > e(t2) and t == t1 and z == x for l, t, z in rs) and out.get(t2) == "c" and out.get(t1) == "c":
                found.add("A2")
            if any(l > j and t == t1 and z == x for l, t, z in ws) and out.get(t1) == "c":
                found.add("P4")
    for (i, t1, p), (j, t2, y) in product(ps, ws):
        if y in p and t1 != t2 and i < j < e(t1):
            found.add("P3")
            if any(l > e(t2) and t == t1 and q == p for l, t, q in ps) and out.get(t2) == "c" and out.get(t1) == "c":
                found.add("A3")
    for (i, t1, x), (j, t2, x2) in product(rs, ws):  # A5A read skew
        if x2 != x or t1 == t2 or j < i or out.get(t2) != "c":
            continue
        for (k, t, y) in ws:
            if t == t2 and y != x and k < e(t2):
                if any(l > e(t2) and u == t1 and z == y for l, u, z in rs) and t1 in out:
                    found.add("A5A")
    for (i, t1, x), (j, t2, y) in product(rs, rs):  # A5B write skew
        if t1 == t2 or x == y or out.get(t1) != "c" or out.get(t2) != "c":
            continue
        first = min(e(t1), e(t2))
        w1 = [k for k, t, z in ws if t == t1 and z == y and j < k < first]
        w2 = [k for k, t, z in ws if t == t2 and z == x and i < k < first]
        if w1 and w2 and i < first and j < first:
            found.add("A5B")
    return found


def dsg(h):
    """Adya's direct serialization graph on the committed transactions.
    Returns (edges, aborted_reads, intermediate_reads); edges is a set of
    (ti, tj, kind) with kind in ww, wr, rw, rw-pred."""
    end, out = _ends(h)
    committed = {t for t, o in out.items() if o == "c"}
    last_write: dict[tuple[int, str], int] = {}
    for i, op in enumerate(h):
        if op[0] == "w":
            last_write[(op[1], op[2])] = i
    order: dict[str, list[int]] = {}  # version order of x: committed writers
    for (t, x), i in sorted(last_write.items(), key=lambda kv: kv[1]):
        if t in committed:
            order.setdefault(x, []).append(t)
    edges, g1a, g1b = set(), False, False

    def nxt(x, j):  # the writer of the version after T_j's (j = 0: initial)
        vs = order.get(x, [])
        k = vs.index(j) + 1 if j in vs else 0
        return vs[k] if k < len(vs) else None

    for x, vs in order.items():
        for a, b in zip(vs, vs[1:]):
            edges.add((a, b, "ww"))
    cur: dict[str, int] = {}
    for i, op in enumerate(h):
        k = op[0]
        if k == "w":
            cur[op[2]] = op[1]
        elif k == "r":
            t, x = op[1], op[2]
            j = op[3] if len(op) > 3 else cur.get(x, 0)
            if t not in committed or j == t:
                continue
            if j and j not in committed:
                g1a = True
                continue
            if j and last_write[(j, x)] > i and len(op) == 3:
                g1b = True  # T_j writes x again later: an intermediate version
            if j:
                edges.add((j, t, "wr"))
            n = nxt(x, j)
            if n is not None and n != t:
                edges.add((t, n, "rw"))
        elif k == "rp":
            t, p = op[1], op[2]
            if t not in committed:
                continue
            for y in p:
                j = cur.get(y, 0)
                if j and j != t and j in committed:
                    edges.add((j, t, "wr"))  # a predicate read dependency
                n = nxt(y, j) if j == 0 or j in committed else None
                if n is not None and n != t:
                    edges.add((t, n, "rw-pred"))
    return edges, g1a, g1b


def _reach(edges, kinds, a, b) -> bool:
    adj: dict[int, list[int]] = {}
    for u, v, k in edges:
        if k in kinds:
            adj.setdefault(u, []).append(v)
    seen, stack = set(), [a]
    while stack:
        u = stack.pop()
        if u == b:
            return True
        if u not in seen:
            seen.add(u)
            stack.extend(adj.get(u, []))
    return False


def adya(h) -> set[str]:
    """The phenomena G0, G1a, G1b, G1c, G2-item and G2."""
    edges, g1a, g1b = dsg(h)
    found = set()
    if g1a:
        found.add("G1a")
    if g1b:
        found.add("G1b")
    item = {"ww", "wr", "rw"}
    allk = item | {"rw-pred"}
    for u, v, k in edges:
        if k == "ww" and _reach(edges, {"ww"}, v, u):
            found.add("G0")
        if k in ("ww", "wr") and _reach(edges, {"ww", "wr"}, v, u):
            found.add("G1c")
        if k == "rw" and _reach(edges, item, v, u):
            found.add("G2-item")
        if k in ("rw", "rw-pred") and _reach(edges, allk, v, u):
            found.add("G2")
    return found


def ansi_level(h) -> str:
    """The strongest level of Berenson et al. that the history satisfies."""
    found = berenson(h)
    for name, banned in LEVELS:
        if not banned & found:
            return name
    return "NONE"


def adya_level(h) -> str:
    found = adya(h)
    for name, banned in PL:
        if not banned & found:
            return name
    return "NONE"
