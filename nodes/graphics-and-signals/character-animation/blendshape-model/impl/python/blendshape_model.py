# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blendshape-model/. The authors are listed in prov/ENWK12.jsonl.
"""The blendshape model in the delta form.

A mesh is a list of vertex tuples. The neutral mesh is b_0 and the targets
are b_1, ..., b_K, all with the same vertex count and order. The model is

    v = b_0 + sum_k w_k (b_k - b_0).

The deltas d_k = b_k - b_0 are computed once. Most rigs keep each w_k in
[0, 1]; that bound is a convention of the rig, not part of the model, so
the clamp is an option here.
"""


def deltas(b0, targets):
    """Return the delta meshes d_k = b_k - b_0, stored sparsely.

    Each delta is a dict {vertex index: offset tuple}, without the vertices
    that the target does not move.
    """
    out = []
    for bk in targets:  # @line L1
        d = {}
        for i, (p, q) in enumerate(zip(b0, bk)):
            off = tuple(y - x for x, y in zip(p, q))
            if any(c != 0 for c in off):
                d[i] = off
        out.append(d)
    return out


def evaluate(b0, ds, w, clamp=False):
    """Return the mesh b_0 + sum_k w_k d_k for sparse deltas ds."""
    if len(ds) != len(w):
        raise ValueError("one weight per target is needed")
    v = [list(p) for p in b0]  # @line L2
    for d, wk in zip(ds, w):  # @line L3
        if clamp:
            wk = min(1.0, max(0.0, wk))
        if wk == 0:
            continue
        for i, off in d.items():  # @line L4
            vi = v[i]
            for c in range(len(vi)):
                vi[c] += wk * off[c]
    return [tuple(p) for p in v]  # @line L5


def evaluate_whole(b0, targets, w):
    """Return the whole-face form w_0 b_0 + sum_k w_k b_k with w_0 = 1 - sum_k w_k.

    This is the same mesh as the delta form; it is here for the tests.
    """
    w0 = 1 - sum(w)
    out = []
    for i, p in enumerate(b0):
        q = [w0 * x for x in p]
        for bk, wk in zip(targets, w):
            for c in range(len(q)):
                q[c] += wk * bk[i][c]
        out.append(tuple(q))
    return out
