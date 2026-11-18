# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delta-mush/. The authors are listed in prov/118N6H.jsonl.
"""Delta mush (Mancewicz, Derksen, Rijpkema and Wilson 2014).

Precomputation, once in the rest pose:
1. Smooth the rest mesh V into S(V) by K steps of uniform Laplacian
   smoothing with the step lam.
2. At each smoothed vertex build an orthonormal frame F_i (tangent,
   bitangent, normal), and store the delta d_i = F_i^T (v_i - S(V)_i), the
   detail that the smoothing removed, in that frame.

Each frame:
3. Deform the mesh with any skinning, here linear blend skinning: U.
4. Smooth U into S(U) with the same K and lam.
5. Build the frames G_i of S(U) and add back the details:
   u_i' = S(U)_i + G_i d_i.

The frame of vertex i has the normal n_i (the sum of the cross products of
the faces around i, normalized), the tangent t_i (the edge to the first
neighbor of i in the vertex list, with its part along n_i removed,
normalized) and b_i = n_i x t_i. K and lam are tuning values.
"""

from anim import add, cross, dot, normalize, scale, sub

LAM = 0.5
ITERS = 10


def neighbors(n, triangles):
    """Return the sorted neighbor lists of the n vertices of a triangle mesh."""
    nb = [set() for _ in range(n)]
    for a, b, c in triangles:
        nb[a] |= {b, c}
        nb[b] |= {a, c}
        nb[c] |= {a, b}
    return [sorted(s) for s in nb]


def smooth(points, nbrs, lam=LAM, iters=ITERS):
    """K steps of x_i <- x_i + lam (mean of the neighbors - x_i), all at once."""
    x = [tuple(p) for p in points]
    for _ in range(iters):  # @line L8
        new = []
        for i, p in enumerate(x):
            m = (0.0, 0.0, 0.0)
            for k in nbrs[i]:
                m = add(m, x[k])
            m = scale(m, 1.0 / len(nbrs[i]))
            new.append(add(p, scale(sub(m, p), lam)))
        x = new
    return x


def frames(points, triangles, nbrs):
    """Return the frame of each vertex as the columns (t, b, n)."""
    nsum = [(0.0, 0.0, 0.0) for _ in points]
    for a, b, c in triangles:
        fn = cross(sub(points[b], points[a]), sub(points[c], points[a]))
        for v in (a, b, c):
            nsum[v] = add(nsum[v], fn)
    out = []
    for i, p in enumerate(points):
        nrm = normalize(nsum[i])  # @line L9
        e = sub(points[nbrs[i][0]], p)
        t = normalize(sub(e, scale(nrm, dot(e, nrm))))
        out.append((t, cross(nrm, t), nrm))
    return out


def to_local(f, v):
    return (dot(f[0], v), dot(f[1], v), dot(f[2], v))


def to_world(f, d):
    return add(add(scale(f[0], d[0]), scale(f[1], d[1])), scale(f[2], d[2]))


def precompute(rest, triangles, lam=LAM, iters=ITERS):
    """Return (nbrs, deltas) of the rest mesh."""
    nbrs = neighbors(len(rest), triangles)
    s = smooth(rest, nbrs, lam, iters)  # @line L1
    fr = frames(s, triangles, nbrs)
    deltas = [to_local(fr[i], sub(rest[i], s[i])) for i in range(len(rest))]  # @line L2
    return nbrs, deltas


def lbs(vertices, weights, palette):
    """Linear blend skinning with sparse weights (joint, weight)."""
    out = []
    for v, wi in zip(vertices, weights):
        p = (0.0, 0.0, 0.0)
        for j, w in wi:
            m = palette[j]
            q = tuple(m[r][0] * v[0] + m[r][1] * v[1] + m[r][2] * v[2] + m[r][3] for r in range(3))
            p = add(p, scale(q, w))
        out.append(p)
    return out


def delta_mush(rest, triangles, weights, palette, pre=None, lam=LAM, iters=ITERS, deformed=None):
    """Return the delta mush result of one frame.

    deformed: the skinned mesh to correct; if None, linear blend skinning of
    rest with weights and palette is used.
    """
    if pre is None:
        pre = precompute(rest, triangles, lam, iters)
    nbrs, deltas = pre
    u = deformed if deformed is not None else lbs(rest, weights, palette)  # @line L3
    su = smooth(u, nbrs, lam, iters)  # @line L4
    fr = frames(su, triangles, nbrs)  # @line L5
    out = [add(su[i], to_world(fr[i], deltas[i])) for i in range(len(rest))]  # @line L6
    return out  # @line L7
