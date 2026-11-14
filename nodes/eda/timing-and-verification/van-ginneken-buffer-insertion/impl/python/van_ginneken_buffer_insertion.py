# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/van-ginneken-buffer-insertion/. The authors are listed in prov/98230Y.jsonl.
"""Van Ginneken's buffer insertion on an RC interconnect tree with Elmore delay.

The tree has nodes 0 to n - 1. Node 0 is the source, driven by a gate with
resistance driver_r and intrinsic delay driver_d. Every other node v has a
parent parent[v] and a wire to it with resistance wire_r[v] and capacitance
wire_c[v] (pi model: half of the capacitance at each end). The leaves are the
sinks: sinks[v] = (load capacitance, required time). A buffer of type b is a
triple (input capacitance, output resistance, intrinsic delay) and may go at
any node in positions. A buffer at v drives the subtree of v.

All arithmetic is exact when the inputs are Fractions or integers.
"""

import heapq
from fractions import Fraction


def prune(cands):
    """Drop dominated pairs from a list sorted by load. A pair (c, q, s) is
    dominated when another pair has a load no larger and a required time no
    smaller. The result has strictly increasing load and required time."""
    out = []
    for c, q, s in cands:
        if out and q <= out[-1][1]:
            continue
        if out and c == out[-1][0]:
            out[-1] = (c, q, s)
        else:
            out.append((c, q, s))
    return out


def add_wire(cands, r, c):
    """Move every pair up through a wire of resistance r and capacitance c."""
    moved = [(load + c, q - r * (Fraction(c) / 2 + load), s) for load, q, s in cands]
    return prune(moved)


def add_buffers(cands, buffers, v):
    """Add, for each buffer type, the pair of a buffer at node v."""
    new = []
    for b, (cb, rb, db) in enumerate(buffers):
        best = None
        for load, q, s in cands:
            t = q - db - rb * load
            if best is None or t > best[0]:
                best = (t, s)
        new.append((cb, best[0], ("buf", v, b, best[1])))
    key = lambda p: (p[0], -p[1])
    return prune(list(heapq.merge(cands, sorted(new, key=key), key=key)))  # @line L10


def merge(a, b):
    """Join the lists of two branches that meet at one node (two pointers)."""
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        ca, qa, sa = a[i]
        cb, qb, sb = b[j]
        out.append((ca + cb, min(qa, qb), ("join", sa, sb)))
        if qa < qb:
            i += 1
        elif qb < qa:
            j += 1
        else:
            i += 1
            j += 1
    return prune(out)


def placement(s, out):
    """Collect the buffers of a solution record into the dict out."""
    stack = [s]
    while stack:
        s = stack.pop()
        if s is None:
            continue
        if s[0] == "buf":
            out[s[1]] = s[2]
            stack.append(s[3])
        else:
            stack.append(s[1])
            stack.append(s[2])
    return out


def van_ginneken(parent, wire_r, wire_c, sinks, positions, buffers, driver_r, driver_d):
    """Return (best slack at the source, {node: buffer type}) and the size of
    the largest candidate list seen."""
    n = len(parent)
    children = [[] for _ in range(n)]
    for v in range(1, n):
        children[parent[v]].append(v)
    order, stack = [], [0]
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(children[v])
    lists = [None] * n
    largest = 0
    for v in reversed(order):  # @line L1
        if not children[v]:
            if v not in sinks:
                raise ValueError("every leaf must be a sink")
            cap, req = sinks[v]
            cur = [(cap, req, None)]  # @line L2
        else:  # @line L3
            if v in sinks:
                raise ValueError("a sink must be a leaf")
            cur = None  # @line L4
            for u in children[v]:  # @line L5
                up = add_wire(lists[u], wire_r[u], wire_c[u])  # @line L6
                lists[u] = None
                cur = up if cur is None else merge(cur, up)  # @line L7
            if v in positions and v != 0:  # @line L8
                cur = add_buffers(cur, buffers, v)  # @line L9
        largest = max(largest, len(cur))
        lists[v] = cur
    best = None
    for load, q, s in lists[0]:  # @line L11
        slack = q - driver_d - driver_r * load
        if best is None or slack > best[0]:
            best = (slack, s)
    return best[0], placement(best[1], {}), largest
