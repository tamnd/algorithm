# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shock-propagation/. The authors are listed in prov/P1VHW8.jsonl.

"""Shock propagation for stacks (Guendelman, Bridson and Fedkiw 2003, Section 8).

The model of this file is small on purpose: 2D axis-aligned boxes that only
translate, y up, gravity (0, -g), and contacts with the normal (0, 1) from
the lower body B to the upper body A. A contact is resolved by a plastic
impulse when it approaches, as in the contact processing of the paper with
a restitution of zero.

The graph part (contact graph, strongly connected components by two depth
first searches, levels) works on any directed graph.
"""


# ------------------------------------------------------------------ graph part


def strongly_connected_components(n, edges):
    """Return the components of the digraph on 0..n-1, in a topological order of the condensation.

    Two depth-first searches: one on the graph for the finishing order, one on
    the reversed graph in the reverse finishing order."""
    adj = [[] for _ in range(n)]
    radj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        radj[v].append(u)
    seen, order = [False] * n, []
    for s in range(n):
        if seen[s]:
            continue
        seen[s] = True
        stack = [(s, iter(adj[s]))]
        while stack:
            u, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                stack.pop()
                order.append(u)
            elif not seen[nxt]:
                seen[nxt] = True
                stack.append((nxt, iter(adj[nxt])))
    comp = [-1] * n
    comps = []
    for s in reversed(order):
        if comp[s] != -1:
            continue
        cid = len(comps)
        comp[s] = cid
        members, stack = [], [s]
        while stack:
            u = stack.pop()
            members.append(u)
            for w in radj[u]:
                if comp[w] == -1:
                    comp[w] = cid
                    stack.append(w)
        comps.append(sorted(members))
    return comps, comp


def levels(n, edges):
    """Level of each node: 0 for a component that no edge enters, else 1 + the largest level of a predecessor."""
    comps, comp = strongly_connected_components(n, edges)  # @line L2
    preds = [set() for _ in comps]
    for u, v in edges:
        if comp[u] != comp[v]:
            preds[comp[v]].add(comp[u])
    clevel = [0] * len(comps)
    for c in range(len(comps)):  # @line L3
        clevel[c] = 1 + max(clevel[p] for p in preds[c]) if preds[c] else 0  # @line L3
    return [clevel[comp[u]] for u in range(n)], comp


# ------------------------------------------------------------------ bodies and contacts


class Box:
    """An axis-aligned box: center (x, y), half sizes (hx, hy), mass m (None: static), velocity (vx, vy)."""

    def __init__(self, x, y, hx, hy, m=None, vx=0, vy=0):
        self.x, self.y, self.hx, self.hy = x, y, hx, hy
        self.inv_m = 0 if m is None else 1 / m
        self.m = m
        self.vx, self.vy = vx, vy

    @property
    def static(self):
        return self.m is None


def overlap_x(a, b):
    return min(a.x + a.hx, b.x + b.hx) - max(a.x - a.hx, b.x - b.hx)


def boxes_overlap(a, b, dy_a=0):
    """Strict overlap of a (moved by dy_a) and b."""
    oy = min(a.y + dy_a + a.hy, b.y + b.hy) - max(a.y + dy_a - a.hy, b.y - b.hy)
    return overlap_x(a, b) > 0 and oy > 0


def contact_graph(boxes, g, dtau):
    """Edge j -> i when box i, moved down by its fall under gravity in time dtau, overlaps box j."""
    drop = g * dtau * dtau / 2
    edges = []
    for i, bi in enumerate(boxes):  # @line L1
        if bi.static:
            continue
        for j, bj in enumerate(boxes):
            if j != i and boxes_overlap(bi, bj, -drop):  # @line L1
                edges.append((j, i))  # @line L1
    return edges


def find_contacts(boxes, slop):
    """Contacts (A, B): A rests on B, with a horizontal overlap and a vertical gap of at most slop."""
    out = []
    for a, A in enumerate(boxes):
        for b, B in enumerate(boxes):
            if a == b or A.y <= B.y or overlap_x(A, B) <= 0:
                continue
            gap = (A.y - A.hy) - (B.y + B.hy)
            if gap <= slop and not (A.static and B.static):
                out.append((a, b))
    return out


def resolve(boxes, inv_m, contact):
    """A plastic impulse along (0, 1) on the upper body if the contact approaches. Return the impulse."""
    a, b = contact
    A, B = boxes[a], boxes[b]
    v_rel = A.vy - B.vy
    k = inv_m[a] + inv_m[b]
    if v_rel >= 0 or k == 0:
        return 0
    j = -v_rel / k
    A.vy += inv_m[a] * j
    B.vy -= inv_m[b] * j
    return j


def solve_velocities(boxes, contacts, level, sweeps, iters, shock=True):
    """Contact propagation sweeps from the lowest level up, then one shock propagation sweep."""
    inv_m = [bx.inv_m for bx in boxes]
    by_level = {}
    for c in contacts:
        by_level.setdefault(max(level[c[0]], level[c[1]]), []).append(c)
    order = sorted(by_level)
    for _ in range(sweeps):  # @line L4
        for lv in order:  # @line L5
            for _ in range(iters):  # @line L6
                for c in by_level[lv]:  # @line L6
                    resolve(boxes, inv_m, c)  # @line L6
    if not shock:
        return
    for lv in range(max(level) + 1):  # @line L7
        for _ in range(iters):  # @line L8
            for c in by_level.get(lv, []):  # @line L8
                resolve(boxes, inv_m, c)  # @line L8
        for u, bx in enumerate(boxes):  # @line L9
            if level[u] == lv:  # @line L9
                inv_m[u] = 0  # @line L9
    # the infinite masses live only in the local list inv_m, so the boxes keep their masses


def step(boxes, dt, g, sweeps, iters, shock=True, slop=1e-9):
    """One time step: gravity, contact graph and levels, velocity solve, then positions (symplectic Euler)."""
    for bx in boxes:
        if not bx.static:
            bx.vy -= g * dt
    edges = contact_graph(boxes, g, dt)
    level, _ = levels(len(boxes), edges)
    contacts = find_contacts(boxes, slop)
    solve_velocities(boxes, contacts, level, sweeps, iters, shock)
    for bx in boxes:
        if not bx.static:
            bx.x += bx.vx * dt
            bx.y += bx.vy * dt
    return level, contacts


def penetration(boxes, contacts):
    return max([0] + [(boxes[b].y + boxes[b].hy) - (boxes[a].y - boxes[a].hy) for a, b in contacts])


def stack(n, m=1, size=0.5, gap=0):
    """The ground (static) and n boxes of mass m and side 2*size, stacked with the given gap."""
    boxes = [Box(0, -1, 10, 1)]
    for k in range(n):
        boxes.append(Box(0, size + k * (2 * size + gap), size, size, m))
    return boxes
