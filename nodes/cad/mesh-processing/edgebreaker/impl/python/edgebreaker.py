# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/edgebreaker/. The authors are listed in prov/5F4MY3.jsonl.

"""Edgebreaker connectivity compression for closed triangle meshes of genus 0 (after Rossignac 1999).

A mesh is a list of faces, each a tuple of three vertex ids, oriented by the
right-hand rule. The encoder walks the triangles from a first triangle and
writes one symbol for each other triangle:

    C  the tip vertex is new;
    L  the tip is the vertex just before the gate on the boundary loop;
    R  the tip is the vertex just after the gate;
    E  both: the triangle closes the loop;
    S  the tip is elsewhere on the loop, which splits in two.

The decoder rebuilds the faces, with the vertices numbered in the order in
which the encoder met them. The code C = 0, S = 100, R = 101, L = 110,
E = 111 gives exactly 2T - 1 bits for T triangles on a closed genus 0 mesh.
"""

CODE = {"C": "0", "S": "100", "R": "101", "L": "110", "E": "111"}
DECODE = {v: k for k, v in CODE.items()}


def nxt(c):
    return c - c % 3 + (c + 1) % 3


def prv(c):
    return c - c % 3 + (c + 2) % 3


def corner_table(faces):
    """The corner table: V[c] is the vertex of corner c, O[c] the opposite corner (or -1)."""
    v = [x for tri in faces for x in tri]
    facing = {}
    for c in range(len(v)):
        e = (v[nxt(c)], v[prv(c)])
        if e in facing:
            raise ValueError("directed edge %r used twice" % (e,))
        facing[e] = c
    o = [facing.get((v[prv(c)], v[nxt(c)]), -1) for c in range(len(v))]
    return v, o


def encode(faces, start=0):
    """(symbols, vertex order, triangle order) for a closed connected genus 0 mesh, starting at face start."""
    if any(len(set(tri)) != 3 for tri in faces):
        raise ValueError("a face repeats a vertex")
    v, o = corner_table(faces)
    t = len(faces)
    if -1 in o:
        raise ValueError("the mesh has a boundary")
    nverts = len({x for tri in faces for x in tri})
    if nverts - 3 * t // 2 + t != 2:
        raise ValueError("V - E + F is not 2: the mesh is not a sphere")
    seen_v, seen_t = set(), [False] * t
    c0 = 3 * start
    order = [v[c0], v[c0 + 1], v[c0 + 2]]  # @line L1
    seen_v.update(order)
    seen_t[start] = True
    tri_order = [start]
    symbols = []
    stack = [o[c0 + 2]]  # the triangle across the edge from v[c0] to v[c0 + 1]
    while stack:
        c = stack.pop()
        while True:
            # c is the corner at the tip x of the new triangle (b, a, x); the gate is a -> b.
            if seen_t[c // 3]:
                raise ValueError("the mesh is not a manifold sphere")  # never on a valid input
            seen_t[c // 3] = True
            tri_order.append(c // 3)
            left = seen_t[o[nxt(c)] // 3]  # the triangle across the edge a x
            right = seen_t[o[prv(c)] // 3]  # the triangle across the edge x b
            if v[c] not in seen_v:  # @line L2
                symbols.append("C")
                seen_v.add(v[c])
                order.append(v[c])
                c = o[prv(c)]
            elif left and right:  # @line L3
                symbols.append("E")
                break
            elif left:  # @line L4
                symbols.append("L")
                c = o[prv(c)]
            elif right:  # @line L5
                symbols.append("R")
                c = o[nxt(c)]
            else:  # @line L6
                symbols.append("S")
                stack.append(o[nxt(c)])
                c = o[prv(c)]
    if not all(seen_t):
        raise ValueError("the mesh is not connected")
    return "".join(symbols), order, tri_order


def right_loop_lengths(symbols):
    """For each S at position i, the length of the loop of its right branch (symbols i+1 to its E)."""
    count = {s: [0] for s in "CLRSE"}
    for s in symbols:
        for k in count:
            count[k].append(count[k][-1] + (s == k))
    # Let D(j) = #E - #S in symbols[0..j]. The right branch of the S at i ends at the
    # first E at j > i with D(j) = D(i) + 1. Nested S symbols have smaller targets, so
    # the open S with the smallest target is on top of the stack.
    out = {}
    stack = []  # (target, i) for each S whose right branch is open
    d = 0
    for j, s in enumerate(symbols):
        if s == "S":
            d -= 1
            stack.append((d + 1, j))
        elif s == "E":
            d += 1
            if stack and stack[-1][0] == d:
                i = stack.pop()[1]
                n = {k: count[k][j + 1] - count[k][i + 1] for k in count}
                out[i] = 3 + 2 * n["S"] - n["C"] + n["L"] + n["R"]
    if d != 1 or stack:
        raise ValueError("the numbers of S and E symbols do not match")
    return out


def decode(symbols):
    """The faces, with vertex ids 0, 1, 2, ... in the order of the encoder, in the encoder's triangle order."""
    lengths = right_loop_lengths(symbols)  # @line L7
    faces = [(0, 1, 2)]
    vert = [0, 1, 2]  # loop nodes: their vertex, next and previous node
    nx = [1, 2, 0]
    pv = [2, 0, 1]
    nverts = 3
    gate = 0  # the gate is the loop edge from node gate to node nx[gate]
    stack = []
    for i, s in enumerate(symbols):
        if gate is None:
            raise ValueError("symbols after the last loop was closed")
        g, h = gate, nx[gate]
        a, b = vert[g], vert[h]
        if s == "C":  # @line L8
            x = nverts
            nverts += 1
            vert.append(x)
            nx.append(h)
            pv.append(g)
            nx[g] = pv[h] = len(vert) - 1
            gate = len(vert) - 1
        elif s == "L":  # @line L9
            p = pv[g]
            x = vert[p]
            nx[p], pv[h] = h, p
            gate = p
        elif s == "R":  # @line L10
            q = nx[h]
            x = vert[q]
            nx[g], pv[q] = q, g
        elif s == "E":  # @line L11
            x = vert[pv[g]]
            if nx[h] != pv[g]:
                raise ValueError("E on a loop that is not a triangle")
            gate = stack.pop() if stack else None
        elif s == "S":  # @line L12
            k = h
            for _ in range(lengths[i] - 1):
                k = nx[k]
            x = vert[k]
            # Right loop: a new node for x, then h ... pv[k]. Left loop: g, k, ...
            vert.append(x)
            nx.append(h)
            pv.append(pv[k])
            nx[pv[k]] = len(vert) - 1
            pv[h] = len(vert) - 1
            nx[g], pv[k] = k, g
            stack.append(g)  # @line L13
            gate = len(vert) - 1
        else:
            raise ValueError("unknown symbol %r" % (s,))
        faces.append((b, a, x))  # @line L14
    if gate is not None:
        raise ValueError("the symbols end before every loop is closed")
    return faces  # @line L15


def to_bits(symbols):
    return "".join(CODE[s] for s in symbols)


def from_bits(bits):
    out, word = [], ""
    for ch in bits:
        word += ch
        if word in DECODE:
            out.append(DECODE[word])
            word = ""
    if word:
        raise ValueError("trailing bits")
    return "".join(out)
