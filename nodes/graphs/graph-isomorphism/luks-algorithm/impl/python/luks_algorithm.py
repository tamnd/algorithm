# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/luks-algorithm/. The authors are listed in prov/QX3WY0.jsonl.
"""Luks's divide and conquer for string isomorphism under a permutation group.

A permutation of {0, ..., n-1} is a tuple p, with p[i] the image of i.
Products apply the left factor first: mul(p, q)[i] = q[p[i]].

Given generators of a group G, a G-invariant window W and two strings
x, y (lists of colors indexed by points), string_isomorphism returns the set

    Iso = { g in G : x[d] == y[g[d]] for every d in W }

as a pair (generators of A, t) meaning Iso = { a t : a in A }, where
A = Aut(x) inside G restricted to W, or None when the set is empty.
The recursion follows Luks (1982): split an intransitive window into orbits
(the chain rule), and split a transitive one along a system of maximal blocks,
running over the cosets of the kernel of the action on the blocks.

As an application, colored_graph_isomorphism tests isomorphism of two
vertex-colored simple undirected graphs with the same color classes; with
classes of size at most b the group lies in Luks's class Gamma_b.
"""

Perm = tuple[int, ...]
Coset = tuple[list[Perm], Perm]


def identity(n: int) -> Perm:
    return tuple(range(n))


def mul(p: Perm, q: Perm) -> Perm:
    return tuple(q[i] for i in p)


def inverse(p: Perm) -> Perm:
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def _transversal(base_point: int, gens: list[Perm], n: int) -> dict[int, Perm]:
    """For each point of the orbit of base_point, a group element sending base_point there."""
    trans = {base_point: identity(n)}
    queue = [base_point]
    for p in queue:
        for g in gens:
            q = g[p]
            if q not in trans:
                trans[q] = mul(trans[p], g)
                queue.append(q)
    return trans


class Group:
    """A permutation group with a base and strong generating set (Schreier-Sims)."""

    def __init__(self, gens: list[Perm], n: int) -> None:
        self.n = n
        e = identity(n)
        self.gens = list(dict.fromkeys(g for g in gens if g != e))
        self.base: list[int] = []
        self.levels: list[list[Perm]] = []
        self.trans: list[dict[int, Perm]] = []
        for g in self.gens:
            self._add(g)

    def _sift(self, g: Perm, start: int) -> tuple[Perm, int]:
        for i in range(start, len(self.base)):
            t = self.trans[i].get(g[self.base[i]])
            if t is None:
                return g, i
            g = mul(g, inverse(t))
        return g, len(self.base)

    def _add(self, g: Perm) -> None:
        """Add g and restore the strong generating property (iterative Schreier-Sims)."""
        e = identity(self.n)
        g, level = self._sift(g, 0)
        if g == e:
            return
        todo = [(g, level)]
        while todo:
            h, level = todo.pop()
            h, level = self._sift(h, level)
            if h == e:
                continue
            if level == len(self.base):
                self.base.append(next(i for i in range(self.n) if h[i] != i))
                self.levels.append([])
                self.trans.append({})
            for j in range(level + 1):
                self.levels[j].append(h)
            for j in range(level, -1, -1):
                self.trans[j] = _transversal(self.base[j], self.levels[j], self.n)
            # Schreier generators of every level touched must sift through.
            for j in range(level, -1, -1):
                fresh = False
                for p, u in list(self.trans[j].items()):
                    for s in self.levels[j]:
                        w = mul(mul(u, s), inverse(self.trans[j][s[p]]))
                        r, lv = self._sift(w, j + 1)
                        if r != e:
                            todo.append((r, lv))
                            fresh = True
                if fresh:
                    break

    def order(self) -> int:
        out = 1
        for t in self.trans:
            out *= len(t)
        return out

    def contains(self, g: Perm) -> bool:
        return self._sift(g, 0)[0] == identity(self.n)

    def strong_gens(self) -> list[Perm]:
        return list(self.levels[0]) if self.levels else []


def orbits(gens: list[Perm], window: list[int]) -> list[list[int]]:
    seen: set[int] = set()
    out = []
    for p in window:
        if p in seen:
            continue
        seen.add(p)
        orb = [p]
        for q in orb:
            for g in gens:
                if g[q] not in seen:
                    seen.add(g[q])
                    orb.append(g[q])
        out.append(sorted(orb))
    return out


def _min_block(gens: list[Perm], window: list[int], seeds: list[int]) -> list[list[int]]:
    """The finest block system in which all seeds lie in one block (Atkinson)."""
    parent = {p: p for p in window}

    def find(p: int) -> int:
        while parent[p] != p:
            parent[p] = parent[parent[p]]
            p = parent[p]
        return p

    pairs = [(seeds[0], s) for s in seeds[1:]]
    while pairs:
        a, b = pairs.pop()
        ra, rb = find(a), find(b)
        if ra == rb:
            continue
        parent[rb] = ra
        for g in gens:
            pairs.append((g[a], g[b]))
    classes: dict[int, list[int]] = {}
    for p in window:
        classes.setdefault(find(p), []).append(p)
    return sorted(classes.values())


def maximal_blocks(gens: list[Perm], window: list[int]) -> list[list[int]]:
    """A block system of a transitive group on which it acts primitively."""
    alpha = window[0]
    system = [[p] for p in window]
    block = [alpha]
    for beta in window:
        if beta in block:
            continue
        cand = _min_block(gens, window, block + [beta])
        if len(cand) > 1:
            system = cand
            block = next(b for b in cand if alpha in b)
    return system


def _block_action(gens: list[Perm], system: list[list[int]]) -> dict[Perm, Perm]:
    """The image group on the blocks, each image with one preimage in G."""
    where = {p: i for i, b in enumerate(system) for p in b}
    images = [tuple(where[g[b[0]]] for b in system) for g in gens]
    k = len(system)
    n = len(gens[0]) if gens else len(where)
    reps = {identity(k): identity(n)}
    queue = [identity(k)]
    for img in queue:
        for g, gi in zip(gens, images):
            nxt = mul(img, gi)
            if nxt not in reps:
                reps[nxt] = mul(reps[img], g)
                queue.append(nxt)
    return reps


def _shift(y: list[int], t: Perm) -> list[int]:
    """The string y composed with t: position d gets y[t[d]]."""
    return [y[t[d]] for d in range(len(y))]


def string_isomorphism(gens: list[Perm], n: int, window: list[int], x: list[int], y: list[int]) -> Coset | None:
    """All g in <gens> with x[d] == y[g[d]] on the window, as a coset, or None.

    The window must be invariant under the group. Recursion depth is at most
    about 2 log2 of the window size, since blocks at least halve.
    """
    e = identity(n)
    gens = Group(gens, n).strong_gens()
    # @line L1
    if len(window) == 1:
        d = window[0]
        return (gens, e) if x[d] == y[d] else None
    orbs = orbits(gens, window)
    # @line L2
    if len(orbs) > 1:
        # @line L3
        a_gens, tau = gens, e
        # @line L4
        for orb in orbs:
            res = string_isomorphism(a_gens, n, orb, x, _shift(y, tau))
            if res is None:
                return None
            a_gens, g = res
            tau = mul(g, tau)
        # @line L5
        return a_gens, tau
    # @line L6
    system = maximal_blocks(gens, window)
    reps = _block_action(gens, system)
    where = {p: i for i, b in enumerate(system) for p in b}
    images = [tuple(where[g[b[0]]] for b in system) for g in gens]
    schreier = [mul(mul(t, g), inverse(reps[mul(img, gi)]))
                for img, t in reps.items() for g, gi in zip(gens, images)]
    kernel = Group(schreier, n).strong_gens()
    # @line L7
    found: list[Perm] = []
    a_gens: list[Perm] = []
    for t in reps.values():
        res = string_isomorphism(kernel, n, window, x, _shift(y, t))
        if res is not None:
            a_gens = res[0]
            found.append(mul(res[1], t))
    # @line L8
    if not found:
        return None
    # @line L9
    t1_inv = inverse(found[0])
    return Group(a_gens + [mul(t, t1_inv) for t in found[1:]], n).strong_gens(), found[0]


def colored_graph_isomorphism(n: int, e1: list[tuple[int, int]], e2: list[tuple[int, int]],
                              colors: list[int]) -> tuple[list[int], int] | None:
    """An isomorphism of two graphs on vertices 0..n-1 that keeps every vertex color,
    and the number of color-preserving automorphisms of the first; or None.

    The group is the product of the symmetric groups on the color classes,
    acting on vertices and on vertex pairs; the window is the set of pairs.
    """
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    pid = {p: n + i for i, p in enumerate(pairs)}
    size = n + len(pairs)

    def lift(vp: list[int]) -> Perm:
        out = list(vp) + [0] * len(pairs)
        for (u, v), i in pid.items():
            a, b = vp[u], vp[v]
            out[i] = pid[(a, b) if a < b else (b, a)]
        return tuple(out)

    gens = []
    classes: dict[int, list[int]] = {}
    for v in range(n):
        classes.setdefault(colors[v], []).append(v)
    for cls in classes.values():
        for a, b in zip(cls, cls[1:]):
            vp = list(range(n))
            vp[a], vp[b] = b, a
            gens.append(lift(vp))
    s1 = {tuple(sorted(e)) for e in e1}
    s2 = {tuple(sorted(e)) for e in e2}
    x = [0] * size
    y = [0] * size
    for p, i in pid.items():
        x[i] = 1 if p in s1 else 0
        y[i] = 1 if p in s2 else 0
    window = list(range(n, size))
    if not window:
        return list(range(n)), 1
    res = string_isomorphism(gens, size, window, x, y)
    if res is None:
        return None
    a_gens, tau = res
    auts = Group(a_gens, size).order()
    return list(tau[:n]), auts
