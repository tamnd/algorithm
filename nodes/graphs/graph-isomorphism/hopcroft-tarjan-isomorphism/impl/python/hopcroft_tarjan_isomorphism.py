# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hopcroft-tarjan-isomorphism/. The authors are listed in prov/NBDRZ3.jsonl.
"""Isomorphism of triconnected planar graphs by refining darts, after Hopcroft and Tarjan.

A planar map is given by a rotation system: rot[v] lists the neighbors of v
in clockwise order around v. Graphs are simple, undirected and connected.
A dart is an ordered pair (u, v) with uv an edge. Two permutations act on
darts: sigma turns a dart around its tail, sigma(u, v) = (u, next neighbor
after v in rot[u]), and alpha reverses it, alpha(u, v) = (v, u).

By Whitney's theorem a 3-connected planar graph has one embedding up to
mirror image, so two such graphs are isomorphic exactly when their maps are
isomorphic, possibly after reversing every rotation of one of them. Map
isomorphism is a bijection of darts that commutes with sigma and alpha.
The test refines a partition of the darts of both maps with Hopcroft's
"smaller half" rule, then individualizes one pair of darts at a time.
"""

Rotation = list[list[int]]


class _Maps:
    """The darts of two maps as one set, with sigma, its inverse and alpha."""

    def __init__(self, r1: Rotation, r2: Rotation) -> None:
        self.tail: list[int] = []
        self.side: list[int] = []
        index: dict[tuple[int, int, int], int] = {}
        for s, rot in enumerate((r1, r2)):
            for u, nbrs in enumerate(rot):
                for v in nbrs:
                    index[(s, u, v)] = len(self.tail)
                    self.tail.append(u)
                    self.side.append(s)
        n = len(self.tail)
        self.sigma = [0] * n
        self.alpha = [0] * n
        for s, rot in enumerate((r1, r2)):
            for u, nbrs in enumerate(rot):
                for i, v in enumerate(nbrs):
                    d = index[(s, u, v)]
                    self.sigma[d] = index[(s, u, nbrs[(i + 1) % len(nbrs)])]
                    self.alpha[d] = index[(s, v, u)]
        self.sigma_inv = [0] * n
        for d in range(n):
            self.sigma_inv[self.sigma[d]] = d

    def labels(self) -> list[tuple[int, int]]:
        """(degree of the tail, length of the face to the left) for each dart."""
        n = len(self.tail)
        deg = [0] * n
        face = [0] * n
        for d in range(n):
            k, e = 1, self.sigma[d]
            while e != d:
                k, e = k + 1, self.sigma[e]
            deg[d] = k
        seen = [False] * n
        for d in range(n):
            if seen[d]:
                continue
            cyc, e = [], d
            while not seen[e]:
                seen[e] = True
                cyc.append(e)
                e = self.sigma[self.alpha[e]]
            for e in cyc:
                face[e] = len(cyc)
        return list(zip(deg, face))


def refine(maps: _Maps, block_of: list[int], blocks: list[list[int]], queue: list[int]) -> None:
    """Coarsest refinement stable under sigma and alpha, in place.

    A partition is stable when the preimage of every block under sigma and
    under alpha is a union of blocks. Splitters come from the queue; after
    a split, the smaller piece is queued, or both if the block was queued.
    Cost: O(N log N) for N darts.
    """
    queued = [False] * len(blocks)
    for b in queue:
        queued[b] = True
    while queue:
        s = queue.pop()
        queued[s] = False
        splitter = list(blocks[s])
        for inverse in (maps.sigma_inv, maps.alpha):
            pre: dict[int, list[int]] = {}
            for d in splitter:
                p = inverse[d]
                pre.setdefault(block_of[p], []).append(p)
            for b, part in pre.items():
                if len(part) == len(blocks[b]):
                    continue
                mark = set(part)
                rest = [d for d in blocks[b] if d not in mark]
                blocks[b] = rest
                nb = len(blocks)
                blocks.append(part)
                queued.append(False)
                for d in part:
                    block_of[d] = nb
                if queued[b]:
                    queue.append(nb)
                    queued[nb] = True
                else:
                    small = nb if len(part) <= len(rest) else b
                    queue.append(small)
                    queued[small] = True


def map_isomorphism(r1: Rotation, r2: Rotation) -> list[int] | None:
    """A vertex bijection that maps the map r1 onto the map r2, or None.

    Both maps must be connected. Cost: O(N log N) for the first refinement
    plus O(N log N) per trial, at most N trials, for N darts.
    """
    if len(r1) != len(r2):
        return None
    if sorted(len(x) for x in r1) != sorted(len(x) for x in r2):
        return None
    maps = _Maps(r1, r2)
    total = len(maps.tail)
    if total == 0:
        return [0] * len(r1) if len(r1) <= 1 else None
    # @line L1
    lab = maps.labels()
    keys = sorted(set(lab))
    blocks: list[list[int]] = [[] for _ in keys]
    pos = {k: i for i, k in enumerate(keys)}
    block_of = [0] * total
    for d in range(total):
        block_of[d] = pos[lab[d]]
        blocks[block_of[d]].append(d)
    # @line L2
    refine(maps, block_of, blocks, list(range(len(blocks))))
    # @line L3
    for b in blocks:
        if 2 * sum(maps.side[d] for d in b) != len(b):
            return None
    # @line L4
    b0 = min((b for b in blocks if b), key=len)
    x = next(d for d in b0 if maps.side[d] == 0)
    # @line L5
    for y in [d for d in b0 if maps.side[d] == 1]:
        bo = list(block_of)
        bl = [list(b) for b in blocks]
        k = bo[x]
        bl[k] = [d for d in bl[k] if d != x and d != y]
        bl.append([x, y])
        bo[x] = bo[y] = len(bl) - 1
        # @line L6
        refine(maps, bo, bl, [len(bl) - 1])
        # @line L7
        if all(len(b) == 2 and maps.side[b[0]] != maps.side[b[1]] for b in bl if b):
            phi = [0] * len(r1)
            for b in bl:
                if b:
                    a, c = sorted(b, key=lambda d: maps.side[d])
                    phi[maps.tail[a]] = maps.tail[c]
            return phi
    # @line L8
    return None


def mirror(rot: Rotation) -> Rotation:
    """The mirror image: every rotation reversed. Cost O(n + m)."""
    return [list(reversed(x)) for x in rot]


def triconnected_planar_isomorphism(r1: Rotation, r2: Rotation) -> list[int] | None:
    """An isomorphism of two 3-connected planar graphs given by planar
    rotation systems, or None. Cost: that of two calls of map_isomorphism.
    """
    phi = map_isomorphism(r1, r2)
    return phi if phi is not None else map_isomorphism(r1, mirror(r2))
