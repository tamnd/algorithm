# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/holistic-twig-join/. The authors are listed in prov/JKP2FG.jsonl.

"""TwigStack, the holistic twig join of Bruno, Koudas and Srivastava (2002).

A document is an ordered tree of elements. Each element has the region code
(start, end, level) from one depth-first walk: start is the counter on entry,
end the counter on exit and level the depth. Element u is an ancestor of v when
u.start < v.start and v.end < u.end, and the parent of v when it is also one
level higher.

A twig is a tree of query nodes. Node q has a tag and, if it is not the root,
an axis to its parent: "//" (ancestor-descendant) or "/" (parent-child). A
match maps every query node to an element with its tag so that each edge holds.
Two query nodes may map to the same element when that is allowed by the edges.

For every query node q, the stream T_q lists the elements with the tag of q in
order of start. TwigStack keeps one stack S_q per query node; the entries of a
stack form a chain of nested elements, and each entry points to the top of the
parent stack at the time of its push. It outputs the path solutions of every
root-to-leaf path and then joins them on the shared query nodes.
"""

from collections import namedtuple

Elem = namedtuple("Elem", "start end level tag")
INF = float("inf")


def encode(tags: list, parent: list) -> list:
    """Region codes for a document given by tags[i] and parent[i] (-1 for the root, children in order of i)."""
    kids = [[] for _ in tags]
    roots = []
    for i, p in enumerate(parent):
        (roots if p < 0 else kids[p]).append(i)
    out = [None] * len(tags)
    clock = 0
    stack = [(r, 0, False) for r in reversed(roots)]
    start = {}
    while stack:
        v, lev, done = stack.pop()
        if done:
            out[v] = Elem(start[v], clock, lev, tags[v])
            clock += 1
            continue
        start[v] = clock
        clock += 1
        stack.append((v, lev, True))
        stack.extend((c, lev + 1, False) for c in reversed(kids[v]))
    return out


def is_ancestor(u: Elem, v: Elem) -> bool:
    return u.start < v.start and v.end < u.end


def holds(axis: str, u: Elem, v: Elem) -> bool:
    """The edge test: v is a descendant ("//") or a child ("/") of u."""
    return is_ancestor(u, v) and (axis == "//" or v.level == u.level + 1)


class Twig:
    """Query nodes 0..k-1; node 0 is the root. nodes[q] = (tag, parent, axis)."""

    def __init__(self, nodes: list) -> None:
        self.tag = [t for t, _, _ in nodes]
        self.parent = [p for _, p, _ in nodes]
        self.axis = [a for _, _, a in nodes]
        self.kids = [[] for _ in nodes]
        for q, p in enumerate(self.parent):
            if q:
                assert 0 <= p < q, "list a parent before its children"
                self.kids[p].append(q)
        self.leaves = [q for q in range(len(nodes)) if not self.kids[q]]

    def path(self, q: int) -> list:
        out = [q]
        while self.parent[out[-1]] >= 0:
            out.append(self.parent[out[-1]])
        return out[::-1]

    def subtree_leaves(self, q: int) -> list:
        return [l for l in self.leaves if q in self.path(l)]


def twig_stack(twig: Twig, elems: list):
    """Return (matches, stats). A match is a tuple with one element per query node.

    stats holds "path_solutions" (a dict from leaf to its list of path
    solutions, each a tuple of elements along the root-to-leaf path) and "steps",
    one (query node, element, action) per element taken from a stream: "push"
    (line L5), "skip" (line L7) or "drop" (line L12, inside getNext).
    """
    k = len(twig.tag)
    stream = [sorted((e for e in elems if e.tag == twig.tag[q]), key=lambda e: e.start) for q in range(k)]
    pos = [0] * k
    stacks = [[] for _ in range(k)]  # entries (element, index of the top of the parent stack or -1)
    leaves_below = [twig.subtree_leaves(q) for q in range(k)]
    paths = {l: [] for l in twig.leaves}
    steps = []
    stats = {"path_solutions": paths, "steps": steps}

    eof = lambda q: pos[q] >= len(stream[q])
    next_l = lambda q: INF if eof(q) else stream[q][pos[q]].start
    next_r = lambda q: INF if eof(q) else stream[q][pos[q]].end
    ended = lambda q: all(eof(l) for l in leaves_below[q])

    def clean_stack(q: int, act_l) -> None:
        s = stacks[q]
        while s and s[-1][0].end < act_l:
            s.pop()

    def get_next(q: int) -> int:
        if not twig.kids[q]:
            return q  # @line L9
        live = [c for c in twig.kids[q] if not ended(c)]
        for c in live:
            n = get_next(c)
            if n != c:
                return n  # @line L10
        n_min = min(live, key=next_l)
        far = max(INF if ended(c) else next_l(c) for c in twig.kids[q])  # @line L11
        while next_r(q) < far:
            steps.append((q, stream[q][pos[q]], "drop"))
            pos[q] += 1  # @line L12
        return q if next_l(q) < next_l(n_min) else n_min  # @line L13

    def show_solutions(leaf: int) -> None:
        path = twig.path(leaf)
        out = paths[leaf]

        def up(i: int, top: int, suffix: tuple) -> None:
            q = path[i]
            for j in range(min(top, len(stacks[q]) - 1) + 1):
                e, ptr = stacks[q][j]
                child = suffix[0] if suffix else None
                if child is not None and not holds(twig.axis[path[i + 1]], e, child):
                    continue
                if i == 0:
                    out.append((e,) + suffix)
                else:
                    up(i - 1, ptr, (e,) + suffix)

        e, ptr = stacks[leaf][-1]
        if len(path) == 1:
            out.append((e,))
        else:
            up(len(path) - 2, ptr, (e,))

    root = 0
    while not ended(root):  # @line L1
        q = get_next(root)  # @line L2
        p = twig.parent[q]
        if q != root:
            clean_stack(p, next_l(q))  # @line L3
        if q == root or stacks[p]:  # @line L4
            clean_stack(q, next_l(q))
            stacks[q].append((stream[q][pos[q]], len(stacks[p]) - 1 if p >= 0 else -1))
            steps.append((q, stream[q][pos[q]], "push"))
            pos[q] += 1  # @line L5
            if not twig.kids[q]:
                show_solutions(q)
                stacks[q].pop()  # @line L6
        else:
            steps.append((q, stream[q][pos[q]], "skip"))
            pos[q] += 1  # @line L7
    return merge(twig, paths), stats  # @line L8


def merge(twig: Twig, paths: dict) -> list:
    """Join the path solutions of all leaves on their shared query nodes, one leaf at a time."""
    k = len(twig.tag)
    acc = None
    for leaf in twig.leaves:
        path = twig.path(leaf)
        rows = [dict(zip(path, sol)) for sol in paths[leaf]]
        if acc is None:
            acc = rows
            continue
        common = [q for q in path if q in acc[0]] if acc else []
        index = {}
        for r in rows:
            index.setdefault(tuple(r[q] for q in common), []).append(r)
        acc = [{**a, **r} for a in acc for r in index.get(tuple(a[q] for q in common), [])]
    return sorted(tuple(m[q] for q in range(k)) for m in (acc or []))


def useless(twig: Twig, paths: dict, matches: list) -> int:
    """The number of path solutions that are not part of any match."""
    count = 0
    for leaf in twig.leaves:
        path = twig.path(leaf)
        used = {tuple(m[q] for q in path) for m in matches}
        count += sum(1 for sol in paths[leaf] if sol not in used)
    return count
