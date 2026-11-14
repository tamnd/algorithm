# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/steensgaard-analysis/. The authors are listed in prov/EFB787.jsonl.
"""Steensgaard's unification-based points-to analysis.

steensgaard(stmts) takes statements in the four forms of ptsgen and returns
a dict from each variable to the set of variables it may point to. The
locations are split into classes kept in a union-find forest. Each class
has at most one target class, pt, or none (bottom). A copy p = q is a
conditional join: if q has no target yet, p is put on the pending list of
q, and the join waits until q gets a target. Joining two classes also joins
their targets. All the work goes through one queue of operations, so the
code has no recursion.

classes(stmts) returns the classes of the program variables and the target
class of each, for display.
"""

from collections import deque

import ptsgen


def _solve(stmts):
    names = ptsgen.variables(stmts)
    parent = {}
    rank = {}
    pt = {}  # target class of a root, or None for bottom
    pending = {}  # roots waiting for this root to get a target
    ops = deque()

    def make(key):
        parent[key] = key
        rank[key] = 0
        pt[key] = None
        pending[key] = []
        return key

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def set_target(c, t):
        pt[c] = t  # @line L19
        for d in pending[c]:
            ops.append(("assign", d, c))  # @line L20
        pending[c] = []

    def deref(c):
        """The target class of c; a fresh class if c has none."""
        c = find(c)
        if pt[c] is None:
            set_target(c, make(("fresh", len(parent))))  # @line L10
        return find(pt[c])  # @line L11

    def assign(cx, cy):
        """The targets of cx must include those of cy."""
        cx, cy = find(cx), find(cy)
        if cx == cy:
            return
        if pt[cy] is None:
            pending[cy].append(cx)  # @line L12
        elif pt[cx] is None:
            set_target(cx, pt[cy])  # @line L13
        else:
            ops.append(("join", pt[cx], pt[cy]))  # @line L14

    def join(c1, c2):
        c1, c2 = find(c1), find(c2)
        if c1 == c2:
            return
        t1, t2, p1, p2 = pt[c1], pt[c2], pending[c1], pending[c2]
        if rank[c1] < rank[c2]:
            c1, c2 = c2, c1
        parent[c2] = c1  # @line L15
        if rank[c1] == rank[c2]:
            rank[c1] += 1
        c = c1
        pt[c], pending[c] = None, []
        if t1 is None and t2 is None:  # @line L16
            # Append the shorter list to the longer one; a linked list
            # would do this in O(1).
            longer, shorter = (p1, p2) if len(p1) >= len(p2) else (p2, p1)
            longer.extend(shorter)
            pending[c] = longer
        elif t1 is None or t2 is None:  # @line L17
            set_target(c, t1 if t1 is not None else t2)
            for d in p1 if t1 is None else p2:
                ops.append(("assign", d, c))
        else:
            pt[c] = t1  # @line L18
            ops.append(("join", t1, t2))

    for v in names:
        make(v)  # @line L1
    for kind, x, y in stmts:  # @line L2
        if kind == "addr":
            cx = find(x)
            if pt[cx] is None:
                set_target(cx, find(y))  # @line L3
            else:
                ops.append(("join", pt[cx], y))  # @line L4
        elif kind == "copy":
            assign(x, y)  # @line L5
        elif kind == "load":
            assign(x, deref(y))  # @line L6
        else:
            assign(deref(x), y)  # @line L7
        while ops:  # @line L8
            op, a, b = ops.popleft()
            if op == "assign":
                assign(a, b)
            else:
                join(a, b)
    return names, find, pt


def steensgaard(stmts):
    names, find, pt = _solve(stmts)
    members = {}
    for a in names:
        members.setdefault(find(a), set()).add(a)
    pts = {}
    for v in names:
        t = pt[find(v)]
        pts[v] = set() if t is None else set(members.get(find(t), ()))  # @line L9
    return pts


def classes(stmts):
    """The classes of the program variables, each a sorted list, and a dict
    from the index of each class to the index of its target class, if the
    target holds a program variable."""
    names, find, pt = _solve(stmts)
    by_root = {}
    for v in names:
        by_root.setdefault(find(v), []).append(v)
    roots = sorted(by_root, key=lambda r: sorted(by_root[r]))
    groups = [sorted(by_root[r]) for r in roots]
    index = {r: i for i, r in enumerate(roots)}
    target = {}
    for r in roots:
        t = pt[r]
        if t is not None and find(t) in index:
            target[index[r]] = index[find(t)]
    return groups, target


def points_to(text):
    return steensgaard(ptsgen.parse(text))
