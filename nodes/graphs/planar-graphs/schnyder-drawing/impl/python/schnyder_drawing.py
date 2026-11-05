# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schnyder-drawing/. The authors are listed in prov/EKZ3MZ.jsonl.

Rotation = dict[int, list[int]]


def _faces(rot: Rotation) -> list[list[int]]:
    """Face walks; the dart after (a, b) is (b, w) with w just before a in rot[b]."""
    pos = {(v, w): i for v, around in rot.items() for i, w in enumerate(around)}
    seen: set[tuple[int, int]] = set()
    out: list[list[int]] = []
    for dart in pos:
        if dart in seen:
            continue
        walk = []
        d = dart
        while d not in seen:
            seen.add(d)
            walk.append(d[0])
            a, b = d
            d = (b, rot[b][pos[(b, a)] - 1])
        out.append(walk)
    return out


def _components(rot: Rotation) -> list[list[int]]:
    seen: set[int] = set()
    comps = []
    for s in rot:
        if s in seen:
            continue
        seen.add(s)
        comp, stack = [s], [s]
        while stack:
            u = stack.pop()
            for w in rot[u]:
                if w not in seen:
                    seen.add(w)
                    comp.append(w)
                    stack.append(w)
        comps.append(comp)
    return comps


def _check_planar(rot: Rotation) -> None:
    """Raise ValueError unless rot is a planar rotation system of a simple graph."""
    m2 = 0
    for v, around in rot.items():
        if len(set(around)) != len(around) or v in around:
            raise ValueError("the graph must be simple")
        for w in around:
            if w not in rot or v not in rot[w]:
                raise ValueError("the rotation system is not symmetric")
        m2 += len(around)
    isolated = sum(1 for v in rot if not rot[v])
    if len(rot) - m2 // 2 + len(_faces(rot)) + isolated != 2 * len(_components(rot)):
        raise ValueError("the rotation system is not planar")


def _edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def _blocks(rot: Rotation) -> dict[tuple[int, int], int]:
    """Label every edge with its biconnected component, by iterative DFS."""
    disc: dict[int, int] = {}
    low: dict[int, int] = {}
    label: dict[tuple[int, int], int] = {}
    count = 0
    for s in rot:
        if s in disc:
            continue
        disc[s] = low[s] = len(disc)
        stack = [(s, -1, iter(rot[s]))]
        edges: list[tuple[int, int]] = []
        while stack:
            v, p, it = stack[-1]
            descended = False
            for w in it:
                if w == p:
                    continue
                if w not in disc:
                    edges.append(_edge(v, w))
                    disc[w] = low[w] = len(disc)
                    stack.append((w, v, iter(rot[w])))
                    descended = True
                    break
                if disc[w] < disc[v]:
                    edges.append(_edge(v, w))
                    low[v] = min(low[v], disc[w])
            if descended:
                continue
            stack.pop()
            if stack:
                u = stack[-1][0]
                low[u] = min(low[u], low[v])
                if low[v] >= disc[u]:
                    while True:
                        e = edges.pop()
                        label[e] = count
                        if e == _edge(u, v):
                            break
                    count += 1
    return label


def triangulate(rot: Rotation) -> Rotation:
    """Add edges to a planar rotation system until every face is a triangle.

    Needs at least 3 vertices. Returns a new rotation system; the input is
    not changed. The original edges keep their cyclic order.
    """
    rot = {v: list(around) for v, around in rot.items()}
    adj = {v: set(around) for v, around in rot.items()}

    def add(u: int, w: int) -> None:
        adj[u].add(w)
        adj[w].add(u)

    comps = _components(rot)
    root = comps[0][0]
    for comp in comps[1:]:  # join the components at arbitrary corners
        r = comp[0]
        rot[root].append(r)
        rot[r].append(root)
        add(root, r)
    label = _blocks(rot)
    parent = list(range(max(label.values(), default=-1) + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for v in list(rot):  # remove cut vertices: join consecutive neighbours from different blocks
        ring = rot[v]
        d = len(ring)
        for i in range(d if d > 1 else 0):
            a, b = ring[i], ring[(i + 1) % d]
            x, y = find(label[_edge(v, a)]), find(label[_edge(v, b)])
            if x != y:
                rot[a].insert(rot[a].index(v), b)
                rot[b].insert(rot[b].index(v) + 1, a)
                add(a, b)
                parent[x] = y
                label[_edge(a, b)] = y
    for work in _faces(rot):  # every face is now a cycle; cut off triangles
        while len(work) > 3:
            v0, v1, v2, v3 = work[0], work[1], work[2], work[3]
            if v2 not in adj[v0]:
                rot[v0].insert(rot[v0].index(v1) + 1, v2)
                rot[v2].insert(rot[v2].index(v3) + 1, v0)
                add(v0, v2)
                work = [v0] + work[2:]
            else:  # then v1 and v3 are not adjacent, by planarity
                v4 = work[4 % len(work)]
                rot[v1].insert(rot[v1].index(v2) + 1, v3)
                rot[v3].insert(rot[v3].index(v4) + 1, v1)
                add(v1, v3)
                work = work[:2] + work[3:]
    return rot


def schnyder_wood(rot: Rotation, outer: tuple[int, int, int]) -> list[dict[int, int]]:
    """The three parent maps of a Schnyder wood of a plane triangulation.

    outer = (a1, a2, a3) lists the outer face counterclockwise, so that
    (a1, a3, a2) is a face walk of rot. The result [p1, p2, p3] gives, for
    each inner vertex v, its parent pi[v] in the tree rooted at ai.
    Raises ValueError if rot is not a triangulation with this face.
    """
    a1, a2, a3 = outer
    if a1 not in rot[a3] or a2 not in rot[a3] or rot[a3][(rot[a3].index(a2) + 1) % len(rot[a3])] != a1:
        raise ValueError("outer is not a face")
    on_path = {v: 0 for v in rot}  # 0 inside, 1 on the outer path, 2 removed
    for a in outer:
        on_path[a] = 1
    nxt = {a1: a3, a3: a2}
    prv = {a3: a1, a2: a3}
    chords = {v: 0 for v in rot}
    chords[a1] = chords[a2] = 1  # the edge a1 a2
    p1: dict[int, int] = {}
    p2: dict[int, int] = {}
    p3: dict[int, int] = {}
    stack = [a3]
    removed = 0
    while stack:  # @line L3
        z = stack.pop()
        if on_path[z] != 1 or chords[z] != 0 or z == a1 or z == a2:
            continue
        p, q = prv[z], nxt[z]
        ring = rot[z]
        d = len(ring)
        j = (ring.index(p) + 1) % d
        mids = []
        while ring[j] != q:  # the neighbours of z below the path, from p to q
            mids.append(ring[j])
            j = (j + 1) % d
        on_path[z] = 2
        removed += 1
        if z != a3:
            p1[z], p2[z] = p, q  # @line L4
        for m in mids:
            p3[m] = z
        seq = [p] + mids + [q]
        for x, y in zip(seq, seq[1:]):
            nxt[x], prv[y] = y, x
        for m in mids:
            on_path[m] = 1
        if not mids:  # the edge p q was a chord and is now on the path
            for x in (p, q):
                chords[x] -= 1
                if chords[x] == 0:
                    stack.append(x)
        index = {m: i for i, m in enumerate(mids)}
        for i, m in enumerate(mids):
            for u in rot[m]:
                if on_path[u] != 1 or u == prv[m] or u == nxt[m] or index.get(u, len(mids)) < i:
                    continue
                chords[m] += 1
                chords[u] += 1
        stack.extend(m for m in mids if chords[m] == 0)
    if removed != len(rot) - 2:
        raise ValueError("the rotation system is not a triangulation")
    return [p1, p2, p3]


def schnyder_drawing(rot: Rotation, outer: tuple[int, int, int] | None = None) -> dict[int, tuple[int, int]]:
    """Straight-line planar drawing on the (n-2) x (n-2) grid, for n >= 3.

    rot[v] lists the neighbours of v counterclockwise and must be a planar
    rotation system of a simple graph. If it is not a triangulation, edges
    are added first. outer, a face (a1, a2, a3) of the triangulation listed
    counterclockwise, becomes the outer face; by default the face that
    contains the first dart. The drawing realizes the rotation system.
    a1, a2, a3 go to (n-2, 1), (0, n-2), (1, 0).
    Returns integer coordinates in 0..n-2. Raises ValueError if rot is not
    a planar rotation system.
    """
    _check_planar(rot)
    n = len(rot)
    if n <= 2:
        return {v: (i, 0) for i, v in enumerate(rot)}
    tri = rot  # @line L1
    if 2 * sum(len(a) for a in rot.values()) != 2 * (6 * n - 12) or any(len(f) != 3 for f in _faces(rot)):
        tri = triangulate(rot)
    if outer is None:
        v = next(iter(tri))  # @line L2
        w = tri[v][0]
        outer = (v, tri[w][tri[w].index(v) - 1], w)
    parents = schnyder_wood(tri, outer)
    inner = [v for v in tri if v not in outer]
    size = []  # @line L5
    for i in range(3):
        children: dict[int, list[int]] = {v: [] for v in tri}
        for v in inner:
            children[parents[i][v]].append(v)
        order = [outer[i]]
        for v in order:
            order.extend(children[v])
        d = {v: 1 for v in order}
        for v in reversed(order[1:]):
            d[parents[i][v]] += d[v]
        size.append((d, order))
    length = []  # @line L6
    tail = {}
    for j in range(3):
        d, order = size[j]
        ln = {outer[j]: 1}
        s = {(i, outer[j]): 0 for i in range(3)}
        for v in order[1:]:
            ln[v] = ln[parents[j][v]] + 1
            for i in range(3):
                s[(i, v)] = s[(i, parents[j][v])] + size[i][0][v] - 1
        length.append(ln)
        tail[j] = s
    pos: dict[int, tuple[int, int]] = {}
    for v in inner:  # @line L7
        c = []
        for i in range(3):
            a, b = (i + 1) % 3, (i + 2) % 3
            region = length[a][v] + length[b][v] - 1 + tail[a][(i, v)] + tail[b][(i, v)] - (size[i][0][v] - 1)
            c.append(region - length[b][v])
        pos[v] = (c[0], c[1])
    a1, a2, a3 = outer  # @line L8
    pos[a1], pos[a2], pos[a3] = (n - 2, 1), (0, n - 2), (1, 0)
    return pos  # @line L9
