# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lipton-tarjan-separator/. The authors are listed in prov/YCV3MB.jsonl.

from collections import deque

Rotation = dict[int, list[int]]


def _components(vertices: list[int], adj: Rotation, removed: set[int]) -> list[list[int]]:
    """Connected components of the graph minus removed, by iterative search."""
    seen = set(removed)
    comps: list[list[int]] = []
    for s in vertices:
        if s in seen:
            continue
        seen.add(s)
        comp = [s]
        stack = [s]
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if w not in seen:
                    seen.add(w)
                    comp.append(w)
                    stack.append(w)
        comps.append(comp)
    return comps


def _check_planar(rot: Rotation) -> None:
    """Raise ValueError unless rot is a planar rotation system of a simple graph."""
    pos: dict[tuple[int, int], int] = {}
    m2 = 0
    for v, around in rot.items():
        if len(set(around)) != len(around) or v in around:
            raise ValueError("the graph must be simple")
        for i, w in enumerate(around):
            pos[(v, w)] = i
            m2 += 1
    for v, w in pos:
        if (w, v) not in pos:
            raise ValueError("the rotation system is not symmetric")
    seen: set[tuple[int, int]] = set()
    faces = 0
    for (u, v) in pos:
        if (u, v) in seen:
            continue
        faces += 1
        d = (u, v)
        while d not in seen:
            seen.add(d)
            a, b = d
            ring = rot[b]
            d = (b, ring[pos[(b, a)] - 1])
    n = len(rot)
    isolated = sum(1 for v in rot if not rot[v])
    c = len(_components(list(rot), rot, set()))
    if n - m2 // 2 + faces + isolated != 2 * c:
        raise ValueError("the rotation system is not planar")


def _group(pieces: list[list[int]], n: int) -> tuple[list[int], list[int]]:
    """Split pieces of at most 2n/3 vertices each into two sides of at most 2n/3."""
    a: list[int] = []
    b: list[int] = []
    big = [p for p in pieces if 3 * len(p) >= n]
    if big:
        a = list(big[0])
        for p in pieces:
            if p is not big[0]:
                b.extend(p)
        return a, b
    for p in pieces:
        if 3 * len(a) < n:
            a.extend(p)
        else:
            b.extend(p)
    return a, b


def _within(cost: int, budget: int) -> bool:
    """True if cost <= 2 * sqrt(budget), in exact integer arithmetic."""
    return cost * cost <= 4 * budget


def _cycle_separator(comp: list[int], rot: Rotation, level: dict[int, int], parent: dict[int, int],
                     l0: int, l2: int, root_q: int) -> list[int]:
    """Lines L7 to L12: the vertices of M on a balanced fundamental cycle."""
    in_m = {v for v in comp if l0 < level[v] < l2}  # @line L7: H is M plus the levels <= l0 contracted into x
    in_r = {v for v in comp if level[v] <= l0}
    ids: dict[int, int] = {}
    names: list[int | None] = []
    if l0 >= 0:
        ids[-1] = 0  # the contracted root x has no name in G
        names.append(None)
    for v in comp:
        if v in in_m:
            ids[v] = len(names)
            names.append(v)
    hrot: list[list[int]] = [[] for _ in names]
    if l0 >= 0:
        x = 0
        kept: dict[int, int] = {}  # vertex of M -> vertex of R whose edge is kept
        stack = [(root_q, 0, len(rot[root_q]))]  # Euler tour of the BFS tree inside R
        while stack:
            v, start, count = stack.pop()
            ring = rot[v]
            while count > 0:
                w = ring[start % len(ring)]
                start += 1
                count -= 1
                if w in in_r and parent.get(w) == v:
                    stack.append((v, start, count))
                    i = ring_index(rot, w, v)
                    stack.append((w, i + 1, len(rot[w]) - 1))
                    break
                if w in in_m and w not in kept:
                    kept[w] = v
                    hrot[x].append(ids[w])
        for v in comp:
            if v in in_m:
                out = hrot[ids[v]]
                for w in rot[v]:
                    if w in in_m:
                        out.append(ids[w])
                    elif w in in_r and kept.get(v) == w:
                        out.append(x)
        root = x
    else:
        for v in comp:
            if v in in_m:
                hrot[ids[v]] = [ids[w] for w in rot[v] if w in in_m]
        root = ids[root_q]
    h = len(names)
    # Darts of H: dart 2e and 2e + 1 are the two directions of edge e.
    tail: list[int] = []
    head: list[int] = []
    dart_of: dict[tuple[int, int], int] = {}
    for a in range(h):
        for b in hrot[a]:
            if (a, b) not in dart_of:
                dart_of[(a, b)] = len(tail)
                tail.append(a)
                head.append(b)
                dart_of[(b, a)] = len(tail)
                tail.append(b)
                head.append(a)
    drot = [[dart_of[(a, b)] for b in hrot[a]] for a in range(h)]
    nh = len(tail)  # @line L8: put a new vertex in every face of H, joined to each corner
    pos = [0] * nh
    for a in range(h):
        for i, d in enumerate(drot[a]):
            pos[d] = i
    hface = [-1] * nh
    face_darts: list[list[int]] = []
    for d0 in range(nh):
        if hface[d0] >= 0:
            continue
        walk = []
        d = d0
        while hface[d] < 0:
            hface[d] = len(face_darts)
            walk.append(d)
            b = head[d]
            ring = drot[b]
            d = ring[pos[d ^ 1] - 1]
        face_darts.append(walk)
    total = h + len(face_darts)
    spoke: list[int] = [0] * nh  # the dart from tail(d) to the new vertex of face(d)
    new_rot: list[list[int]] = [[] for _ in range(total)]
    for d in range(nh):
        c = h + hface[d]
        spoke[d] = len(tail)
        tail.append(tail[d])
        head.append(c)
        tail.append(c)
        head.append(tail[d])
    for a in range(h):
        for d in drot[a]:
            new_rot[a].append(d)
            new_rot[a].append(spoke[d])
    for f, walk in enumerate(face_darts):
        new_rot[h + f] = [spoke[d] ^ 1 for d in walk]
    nd = len(tail)
    tparent = [-1] * total  # @line L9: the tree T, inherited from the search; weights 1 on M
    tdart = [-1] * total  # the dart from a vertex to its parent
    for v in comp:
        if v in in_m:
            p = parent[v]
            pv = 0 if (l0 >= 0 and level[v] == l0 + 1) else ids[p]
            tparent[ids[v]] = pv
            tdart[ids[v]] = dart_of[(ids[v], pv)]
    for f, walk in enumerate(face_darts):
        c = h + f
        tparent[c] = tail[walk[0]]
        tdart[c] = spoke[walk[0]] ^ 1
    weight = [0] * total
    for a in range(h):
        if names[a] is not None:
            weight[a] = 1
    wtotal = sum(weight)
    in_tree = [False] * nd
    for v in range(total):
        if tdart[v] >= 0:
            in_tree[tdart[v]] = True
            in_tree[tdart[v] ^ 1] = True
    order = [root]  # vertices of T in breadth-first order
    children: list[list[int]] = [[] for _ in range(total)]
    for v in range(total):
        if tparent[v] >= 0:
            children[tparent[v]].append(v)
    for v in order:
        order.extend(children[v])
    depth = [0] * total
    pre = [0] * total  # weight of the tree path from v up to the root
    for v in order:
        if v != root:
            depth[v] = depth[tparent[v]] + 1
            pre[v] = pre[tparent[v]] + weight[v]
        else:
            pre[v] = weight[v]
    up = [[tparent[v] if tparent[v] >= 0 else v for v in range(total)]]
    while (1 << len(up)) <= max(depth) + 1:
        last = up[-1]
        up.append([last[last[v]] for v in range(total)])

    def lca(u: int, v: int) -> int:
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        j = 0
        while diff:
            if diff & 1:
                u = up[j][u]
            diff >>= 1
            j += 1
        if u == v:
            return u
        for j in range(len(up) - 1, -1, -1):
            if up[j][u] != up[j][v]:
                u, v = up[j][u], up[j][v]
        return tparent[u]

    # Faces of the triangulation: every face is a triangle.
    tpos = [0] * nd
    for a in range(total):
        for i, d in enumerate(new_rot[a]):
            tpos[d] = i
    face = [-1] * nd
    nf = 0
    for d0 in range(nd):
        if face[d0] >= 0:
            continue
        d = d0
        while face[d] < 0:
            face[d] = nf
            ring = new_rot[head[d]]
            d = ring[tpos[d ^ 1] - 1]
        nf += 1
    dual: list[list[int]] = [[] for _ in range(nf)]
    for d in range(0, nd, 2):
        if not in_tree[d]:
            dual[face[d]].append(d)
            dual[face[d ^ 1]].append(d ^ 1)
    owner_w = [0] * nf  # @line L10: the dual tree of non-tree edges, with subtree sums
    for v in range(total):
        od = tdart[v] if tdart[v] >= 0 else new_rot[v][0]
        owner_w[face[od]] += weight[v]
    fparent_dart = [-1] * nf  # the dart whose left face is the child face
    tin = [0] * nf
    tout = [0] * nf
    sub_w = owner_w[:]
    sub_n = [1] * nf
    clock = 0
    visited = [False] * nf
    visited[0] = True
    stack2: list[tuple[int, int]] = [(0, 0)]
    tin[0] = clock
    clock += 1
    while stack2:
        f, i = stack2.pop()
        if i < len(dual[f]):
            stack2.append((f, i + 1))
            d = dual[f][i]
            g = face[d ^ 1]
            if not visited[g]:
                visited[g] = True
                fparent_dart[g] = d ^ 1
                tin[g] = clock
                clock += 1
                stack2.append((g, 0))
        else:
            tout[f] = clock
            if f != 0:
                p = face[fparent_dart[f] ^ 1]
                sub_w[p] += sub_w[f]
                sub_n[p] += sub_n[f]
    best = -1  # @line L11: weights inside and on each cycle; the candidate with fewest faces
    best_size = nf + 1
    best_inside = 0
    for g in range(1, nf):
        d = fparent_dart[g]  # the inside face g lies on the left of d = (u, v)
        u, v = tail[d], head[d]
        z = lca(u, v)
        on_cycle = pre[u] + pre[v] - 2 * pre[z] + weight[z]
        oz = tdart[z] if tdart[z] >= 0 else new_rot[z][0]
        fz = face[oz]
        z_inside = tin[g] <= tin[fz] < tout[g]
        owners_on_cycle = pre[v] - pre[z] + (weight[z] if z_inside else 0)
        inside = sub_w[g] - owners_on_cycle
        if 3 * (inside + on_cycle) >= wtotal and sub_n[g] < best_size:
            best, best_size, best_inside = g, sub_n[g], inside
    assert 3 * best_inside <= 2 * wtotal  # the lemma of the separator theorem
    d = fparent_dart[best]
    u, v = tail[d], head[d]
    z = lca(u, v)
    cycle = [z]  # @line L12: the vertices of G on the cycle
    for s in (u, v):
        while s != z:
            cycle.append(s)
            s = tparent[s]
    return [names[a] for a in cycle if a < h and names[a] is not None]


def ring_index(rot: Rotation, v: int, w: int) -> int:
    return rot[v].index(w)


def lipton_tarjan_separator(rot: Rotation) -> tuple[list[int], list[int], list[int]]:
    """Return (A, B, S) for a planar graph given by a planar rotation system.

    rot[v] lists the neighbours of v in counterclockwise order. The result is
    a partition of the vertices with no edge between A and B, len(A) and
    len(B) at most 2n/3, and len(S) at most 2 * sqrt(2) * sqrt(n).
    Raises ValueError if rot is not a planar rotation system of a simple graph.
    """
    _check_planar(rot)
    vertices = list(rot)
    n = len(vertices)
    if n == 0:
        return [], [], []
    comps = _components(vertices, rot, set())
    comp = max(comps, key=len)
    sep: list[int] = []
    if 3 * len(comp) > 2 * n:  # @line L1
        nk = len(comp)
        q = comp[0]
        level = {q: 0}  # @line L2
        parent: dict[int, int] = {}
        levels: list[list[int]] = [[q]]
        queue = deque([q])
        while queue:
            u = queue.popleft()
            for w in rot[u]:
                if w not in level:
                    level[w] = level[u] + 1
                    parent[w] = u
                    if level[w] == len(levels):
                        levels.append([])
                    levels[level[w]].append(w)
                    queue.append(w)
        r = len(levels) - 1
        size = [len(lv) for lv in levels]

        def lsize(i: int) -> int:
            return size[i] if 0 <= i <= r else 0

        count = 0
        l1 = 0
        while 2 * (count + size[l1]) < nk:
            count += size[l1]
            l1 += 1
        k = count + size[l1]
        if size[l1] * size[l1] <= 8 * nk:  # @line L3
            sep = list(levels[l1])
        else:
            l0 = l1  # @line L4
            while not _within(lsize(l0) + 2 * (l1 - l0), k):
                l0 -= 1
            l2 = l1 + 1  # @line L5
            while not _within(lsize(l2) + 2 * (l2 - l1 - 1), nk - k):
                l2 += 1
            sep = [v for i in (l0, l2) if 0 <= i <= r for v in levels[i]]  # @line L6
            m_size = sum(lsize(i) for i in range(l0 + 1, l2))
            if 3 * m_size > 2 * nk:
                sep += _cycle_separator(comp, rot, level, parent, l0, l2, q)
    pieces = _components(vertices, rot, set(sep))  # @line L13
    a, b = _group(pieces, n)
    return sorted(a), sorted(b), sorted(sep)  # @line L14
