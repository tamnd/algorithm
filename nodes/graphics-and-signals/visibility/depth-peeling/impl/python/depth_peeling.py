# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/depth-peeling/. The authors are listed in prov/0TEAXT.jsonl.

"""Depth peeling (Mammen 1989, Everitt 2001) on screen-space triangles.

Each pass renders the whole scene with two depth tests: the fragment must be
behind the layer peeled in the pass before, and nearer than every other such
fragment in this pass. Pass m therefore keeps, at each pixel, the m-th nearest
fragment. The layers are then blended front to back.

A triangle is ((x0, y0, z0), (x1, y1, z1), (x2, y2, z2)) in pixel units, x to
the right, y down, pixel centers at (i + 1/2, j + 1/2), smaller z nearer.
With tie_break=False the peel compares depth only, as the hardware form does,
and of several fragments with equal depth at a pixel only one survives. With
tie_break=True the key is (depth, triangle index), which peels them all.
"""

from fractions import Fraction
from math import ceil, floor

HALF = Fraction(1, 2)


def _edge(ax, ay, bx, by, px, py):
    return (bx - ax) * (py - ay) - (by - ay) * (px - ax)


def _top_left(ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    return dy < 0 or (dy == 0 and dx > 0)


def fragments(tri, width, height):
    """Yield (i, j, z) for each covered pixel center (top-left rule)."""
    (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = tri
    area = _edge(x0, y0, x1, y1, x2, y2)
    if area == 0:
        return
    if area < 0:
        x1, y1, z1, x2, y2, z2 = x2, y2, z2, x1, y1, z1
        area = -area
    edges = ((x1, y1, x2, y2), (x2, y2, x0, y0), (x0, y0, x1, y1))
    tl = [_top_left(*e) for e in edges]
    for j in range(max(0, ceil(min(y0, y1, y2) - HALF)), min(height - 1, floor(max(y0, y1, y2) - HALF)) + 1):
        for i in range(max(0, ceil(min(x0, x1, x2) - HALF)), min(width - 1, floor(max(x0, x1, x2) - HALF)) + 1):
            w = [_edge(*e, i + HALF, j + HALF) for e in edges]
            if all(w[k] > 0 or (w[k] == 0 and tl[k]) for k in range(3)):
                yield i, j, (w[0] * z0 + w[1] * z1 + w[2] * z2) / Fraction(area)


def peel_layers(width, height, triangles, max_layers=None, tie_break=False):
    """Return the list of layers. Layer m is a grid whose entry is the index of
    the triangle seen at that pixel in layer m, or None."""
    frags = [list(fragments(t, width, height)) for t in triangles]
    near, far = (float("-inf"),), (float("inf"),)
    prev = [[near] * width for _ in range(height)]  # @line L1: no layer peeled yet
    layers = []
    while max_layers is None or len(layers) < max_layers:  # @line L2
        # The depth buffer of this pass is cleared to far. A pixel that gets no
        # fragment keeps far, so in later passes nothing passes the peel there.
        best = [[far] * width for _ in range(height)]  # @line L3
        layer = [[None] * width for _ in range(height)]
        written = 0
        for k, fl in enumerate(frags):  # @line L4: one pass over the scene
            for i, j, z in fl:
                key = (z, k) if tie_break else (z,)
                if not key > prev[j][i]:  # @line L5: the peel test
                    continue
                if key < best[j][i]:  # @line L6: the usual depth test
                    if best[j][i] == far:
                        written += 1
                    best[j][i] = key  # @line L7
                    layer[j][i] = k
        if written == 0:  # @line L8: an occlusion query that counts zero
            break
        layers.append(layer)  # @line L9
        prev = best  # @line L10
    return layers


def composite(layers, colors, alphas, background):
    """Blend the layers front to back with the under operator."""
    height, width = len(background), len(background[0])
    out = []
    for j in range(height):
        row = []
        for i in range(width):
            acc = [Fraction(0)] * len(background[j][i])
            trans = Fraction(1)  # @line L11
            for layer in layers:  # @line L12
                k = layer[j][i]
                if k is None:
                    continue
                a = Fraction(alphas[k])
                for c in range(len(acc)):
                    acc[c] += trans * a * colors[k][c]  # @line L13
                trans *= 1 - a
            for c in range(len(acc)):
                acc[c] += trans * background[j][i][c]  # @line L14
            row.append(tuple(acc))
        out.append(row)
    return out
