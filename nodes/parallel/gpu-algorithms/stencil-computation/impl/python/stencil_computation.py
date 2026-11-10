# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stencil-computation/. The authors are listed in prov/WF3821.jsonl.
"""Star stencils on a 2D grid: a direct loop, a tiled kernel with halo cells in
shared memory, and temporal blocking with overlapped tiles, on a small SIMT-style
simulator that counts global loads and stores.

A star stencil of radius r reads the centre and the r nearest cells in each of
the four directions (4r + 1 points; r = 1 is the 5-point stencil).  The cells on
the border of width r keep their values (a fixed boundary).  The update is a
function f of the list of the 4r + 1 values, centre first.

Each thread block owns a T x T tile of outputs.  It loads its tile and the halo
into shared memory (a Python dict), waits at a barrier, and computes from shared
memory.  The CUDA kernel on the page is not run by these tests.
"""
from fractions import Fraction


def star_offsets(r):
    offs = [(0, 0)]
    for d in range(1, r + 1):
        offs += [(-d, 0), (d, 0), (0, -d), (0, d)]
    return offs


def jacobi_average(vals):
    """The 5-point Jacobi update for the Laplace equation: the mean of the four neighbours."""
    return Fraction(sum(vals[1:]), len(vals) - 1)


def step_direct(u, r, f):
    """One sweep with a plain double loop. Returns (new grid, global loads)."""
    h, w = len(u), len(u[0]) if u else 0
    offs = star_offsets(r)
    v = [row[:] for row in u]
    loads = 0
    for i in range(r, h - r):
        for j in range(r, w - r):
            v[i][j] = f([u[i + di][j + dj] for di, dj in offs])
            loads += len(offs)
    return v, loads


def _interior(i, j, h, w, r):
    return r <= i < h - r and r <= j < w - r


def step_tiled(u, r, f, t, halo="star"):
    """One sweep with T x T output tiles and a halo of width r in shared memory.

    halo="star" loads only the cells a star stencil reads (no corners); halo="box"
    loads the whole (T + 2r) x (T + 2r) square.  Returns (grid, stats).
    """
    h, w = len(u), len(u[0]) if u else 0
    offs = star_offsets(r)
    v = [row[:] for row in u]
    st = {"global_loads": 0, "global_stores": 0, "outputs": 0, "blocks": 0}
    for bi in range(r, h - r, t):
        for bj in range(r, w - r, t):
            st["blocks"] += 1
            outs = [(i, j) for i in range(bi, min(bi + t, h - r)) for j in range(bj, min(bj + t, w - r))]
            need = set()
            if halo == "box":
                need = {(i, j) for i in range(bi - r, min(bi + t, h - r) + r)
                        for j in range(bj - r, min(bj + t, w - r) + r)}
            else:
                need = {(i + di, j + dj) for i, j in outs for di, dj in offs}
            shared = {c: u[c[0]][c[1]] for c in need}          # phase 1: cooperative load
            st["global_loads"] += len(need)
            # __syncthreads()
            for i, j in outs:                                   # phase 2: compute from shared memory
                v[i][j] = f([shared[(i + di, j + dj)] for di, dj in offs])
            st["global_stores"] += len(outs)
            st["outputs"] += len(outs)
    return v, st


def halo_loads(t, r, halo="star", dims=2):
    """Global loads of one full tile: T^2 + 4rT (star) or (T + 2r)^2 (box); in 3D T^3 + 6rT^2 or (T + 2r)^3."""
    if dims == 2:
        return t * t + 4 * r * t if halo == "star" else (t + 2 * r) ** 2
    if dims == 3:
        return t ** 3 + 6 * r * t * t if halo == "star" else (t + 2 * r) ** 3
    raise ValueError(dims)


def steps_temporal(u, r, f, t, s):
    """s sweeps with overlapped temporal blocking: each block loads its tile with a
    halo of width r*s once, runs s sweeps in shared memory, and stores its T x T
    outputs.  Cells near the edge of the loaded region go stale; the tile stays valid.
    Returns (grid after s sweeps, global loads)."""
    h, w = len(u), len(u[0]) if u else 0
    offs = star_offsets(r)
    v = [row[:] for row in u]
    loads = 0
    g = r * s
    for bi in range(r, h - r, t):
        for bj in range(r, w - r, t):
            i0, i1 = max(0, bi - g), min(h, min(bi + t, h - r) + g)
            j0, j1 = max(0, bj - g), min(w, min(bj + t, w - r) + g)
            cur = {(i, j): u[i][j] for i in range(i0, i1) for j in range(j0, j1)}
            loads += len(cur)
            for _ in range(s):
                nxt = {}
                for (i, j), x in cur.items():
                    if not _interior(i, j, h, w, r):
                        nxt[(i, j)] = x                         # fixed boundary
                    elif all((i + di, j + dj) in cur for di, dj in offs):
                        nxt[(i, j)] = f([cur[(i + di, j + dj)] for di, dj in offs])
                cur = nxt                                       # stale cells drop out
            for i in range(bi, min(bi + t, h - r)):
                for j in range(bj, min(bj + t, w - r)):
                    v[i][j] = cur[(i, j)]
    return v, loads
