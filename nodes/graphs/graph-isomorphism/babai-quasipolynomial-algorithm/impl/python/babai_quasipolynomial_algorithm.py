# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/babai-quasipolynomial-algorithm/. The authors are listed in prov/E8W04N.jsonl.
"""A model of the framework of Babai's graph isomorphism algorithm.

Babai's algorithm (2015) solves string isomorphism, and through it graph
isomorphism, in quasipolynomial time. Its outer structure is Luks's
recursion: split along orbits, and for a transitive group along a system of
maximal blocks. The only case where Luks's recursion is too slow is when the
group induced on the blocks is a giant, the alternating or symmetric group
on the m blocks, with m large. Babai's new tools (local certificates,
aggregation of certificates, and the split-or-Johnson routine) handle that
case. They are not implemented here.

This module implements the framework exactly: the canonical first step
(color refinement on both graphs together), Luks's recursion, and a
polynomial-time test that detects the giant case and records it. In the
giant case it falls back to running over all cosets, so the answer is exact
but the time is exponential there; outside the giant case the recursion is
the same as in the paper.

A permutation of {0, ..., n-1} is a tuple p, with p[i] the image of i.
Products apply the left factor first: mul(p, q)[i] = q[p[i]].
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


def is_giant(image_gens: list[Perm], m: int) -> bool:
    """Whether the group generated on m points contains the alternating group.

    Uses the order from Schreier-Sims, which is polynomial: |H| >= m!/2.
    """
    if m <= 2:
        return False
    full = 1
    for i in range(2, m + 1):
        full *= i
    return 2 * Group(image_gens, m).order() >= full


def string_isomorphism(gens: list[Perm], n: int, window: list[int], x: list[int], y: list[int],
                       stats: dict[str, int] | None = None, threshold: int = 4) -> Coset | None:
    """All g in <gens> with x[d] == y[g[d]] on the window, as (generators of A, tau), or None.

    The window must be invariant under the group. stats, if given, counts the
    transitive cases by kind: "small" (Luks's recursion applies) and "giant"
    (the bottleneck that Babai's algorithm handles with new tools; here the
    fallback runs over all cosets). Giants on at most `threshold` blocks are
    counted as small, since their size is bounded.
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
        a_gens, tau = gens, e
        for orb in orbs:
            res = string_isomorphism(a_gens, n, orb, x, _shift(y, tau), stats, threshold)
            if res is None:
                return None
            a_gens, g = res
            tau = mul(g, tau)
        return a_gens, tau
    # @line L3
    system = maximal_blocks(gens, window)
    where = {p: i for i, b in enumerate(system) for p in b}
    images = [tuple(where[g[b[0]]] for b in system) for g in gens]
    # @line L4
    giant = len(system) > threshold and is_giant(images, len(system))
    if stats is not None:
        key = "giant" if giant else "small"
        stats[key] = stats.get(key, 0) + 1
    # @line L5
    reps = _block_action(gens, system)
    schreier = [mul(mul(t, g), inverse(reps[mul(img, gi)]))
                for img, t in reps.items() for g, gi in zip(gens, images)]
    kernel = Group(schreier, n).strong_gens()
    # @line L6
    found: list[Perm] = []
    a_gens: list[Perm] = []
    for t in reps.values():
        res = string_isomorphism(kernel, n, window, x, _shift(y, t), stats, threshold)
        if res is not None:
            a_gens = res[0]
            found.append(mul(res[1], t))
    # @line L7
    if not found:
        return None
    t1_inv = inverse(found[0])
    return Group(a_gens + [mul(t, t1_inv) for t in found[1:]], n).strong_gens(), found[0]


def joint_color_refinement(n: int, e1: list[tuple[int, int]], e2: list[tuple[int, int]],
                           c1: list[int], c2: list[int]) -> tuple[list[int], list[int]] | None:
    """Color refinement run on both graphs with shared color names.

    Returns the stable colors of both graphs, or None if the color counts differ
    in some round, which proves that the graphs are not isomorphic.
    """
    adj = [[] for _ in range(2 * n)]
    for u, v in e1:
        adj[u].append(v)
        adj[v].append(u)
    for u, v in e2:
        adj[n + u].append(n + v)
        adj[n + v].append(n + u)
    col = list(c1) + list(c2)
    while True:
        sig = [(col[v], tuple(sorted(col[w] for w in adj[v]))) for v in range(2 * n)]
        names = {s: i for i, s in enumerate(sorted(set(sig)))}
        new = [names[s] for s in sig]
        if sorted(new[:n]) != sorted(new[n:]):
            return None
        if len(names) == len(set(col)):
            return new[:n], new[n:]
        col = new


def graph_isomorphism(n: int, e1: list[tuple[int, int]], e2: list[tuple[int, int]],
                      c1: list[int] | None = None, c2: list[int] | None = None,
                      stats: dict[str, int] | None = None) -> tuple[list[int], int] | None:
    """An isomorphism of two vertex-colored simple undirected graphs, and the
    number of automorphisms of the first; or None.

    Step 1 refines colors canonically on both graphs. Step 2 renames the
    second graph so that equal colors sit on the same vertices. Step 3 solves
    string isomorphism for the product of the symmetric groups on the color
    classes, acting on vertex pairs.
    """
    c1 = list(c1) if c1 is not None else [0] * n
    c2 = list(c2) if c2 is not None else [0] * n
    if len(e1) != len(e2):
        return None
    ref = joint_color_refinement(n, e1, e2, c1, c2)
    if ref is None:
        return None
    col1, col2 = ref
    # rename the second graph: the k-th vertex of color c in H becomes the k-th of color c in G
    slots: dict[int, list[int]] = {}
    for v in range(n):
        slots.setdefault(col1[v], []).append(v)
    rename = [0] * n
    used: dict[int, int] = {}
    for v in range(n):
        c = col2[v]
        rename[v] = slots[c][used.get(c, 0)]
        used[c] = used.get(c, 0) + 1
    e2r = [(rename[u], rename[v]) for u, v in e2]
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
    for cls in slots.values():
        for a, b in zip(cls, cls[1:]):
            vp = list(range(n))
            vp[a], vp[b] = b, a
            gens.append(lift(vp))
    s1 = {tuple(sorted(e)) for e in e1}
    s2 = {tuple(sorted(e)) for e in e2r}
    x = [0] * n + [1 if p in s1 else 0 for p in pairs]
    y = [0] * n + [1 if p in s2 else 0 for p in pairs]
    if not pairs:
        return list(range(n)), 1
    res = string_isomorphism(gens, size, list(range(n, size)), x, y, stats)
    if res is None:
        return None
    a_gens, tau = res
    back = [0] * n
    for v in range(n):
        back[rename[v]] = v
    return [back[tau[v]] for v in range(n)], Group(a_gens, size).order()
