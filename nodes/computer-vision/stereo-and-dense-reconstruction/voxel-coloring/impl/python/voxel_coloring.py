# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/voxel-coloring/. The authors are listed in prov/1NZA21.jsonl.

"""Voxel coloring (Seitz and Dyer) in a layered model.

The grid has nx * ny * nz unit voxels; voxel (i, j, k) is the cube
[i, i+1] x [j, j+1] x [k, k+1]. All camera centers lie below the plane z = 0
and every pixel ray goes up (its direction has a positive z part), so no scene
point is inside the convex hull of the camera centers and z orders the voxels
by visibility. The ray of a pixel meets layer k at the voxel that contains its
point on the plane z = k + 0.5, or at no voxel. A camera is (K, R, t) with
X_c = R X + t. Pixel values are gray numbers, or None for a background pixel.
"""

import math


def inverse_intrinsics(K):
    """K^-1 for K = [[fx, s, cx], [0, fy, cy], [0, 0, 1]]."""
    fx, s, cx = K[0]
    fy, cy = K[1][1], K[1][2]
    return [[1.0 / fx, -s / (fx * fy), (s * cy - cx * fy) / (fx * fy)],
            [0.0, 1.0 / fy, -cy / fy],
            [0.0, 0.0, 1.0]]


def layer_cells(cam, u, v, dims):
    """The voxel of each layer k that the ray of pixel (u, v) meets, or None."""
    K, R, t = cam
    Ki = inverse_intrinsics(K)
    m = [Ki[r][0] * u + Ki[r][1] * v + Ki[r][2] for r in range(3)]
    d = [sum(R[r][c] * m[r] for r in range(3)) for c in range(3)]
    C = [-sum(R[r][c] * t[r] for r in range(3)) for c in range(3)]
    if C[2] >= 0.0 or d[2] <= 0.0:
        raise ValueError("cameras must lie below z = 0 and look up")
    cells = []
    for k in range(dims[2]):
        s = (k + 0.5 - C[2]) / d[2]
        i, j = int(math.floor(C[0] + s * d[0])), int(math.floor(C[1] + s * d[1]))
        cells.append((i, j, k) if 0 <= i < dims[0] and 0 <= j < dims[1] else None)
    return cells


def build_rays(cams, width, height, dims):
    """rays[c][v * width + u] is the list of layer voxels of pixel (u, v) of camera c."""
    return [[layer_cells(cam, float(u), float(v), dims)
             for v in range(height) for u in range(width)] for cam in cams]


def render(rays, scene):
    """Images of a voxel scene {voxel: gray value}: the value of the first voxel on each ray, else None."""
    images = []
    for lists in rays:
        img = []
        for cells in lists:
            val = None
            for c in cells:
                if c is not None and c in scene:
                    val = scene[c]
                    break
            img.append(val)
        images.append(img)
    return images


def consistent(values, tau):
    """The monotone test: no background pixel, and max - min <= tau."""
    if any(x is None for x in values):
        return False
    return not values or max(values) - min(values) <= tau


def voxel_color(rays, images, nz, tau):
    """One pass over the layers, nearest first. Returns (scene, ok): scene maps
    each colored voxel to the mean of its pixels, and ok tells whether every
    non-background pixel was explained (if not, no consistent scene exists)."""
    scene = {}  # @line L1
    marked = [[False] * len(img) for img in images]
    for k in range(nz):  # @line L2
        footprint = {}
        for c, lists in enumerate(rays):  # @line L3
            for p, cells in enumerate(lists):
                if not marked[c][p] and cells[k] is not None:
                    footprint.setdefault(cells[k], []).append((c, p))  # @line L4
        new = []
        for v, pixels in footprint.items():
            values = [images[c][p] for c, p in pixels]
            if consistent(values, tau):  # @line L5
                scene[v] = sum(values) / len(values)
                new.extend(pixels)
        for c, p in new:  # @line L6
            marked[c][p] = True
    ok = all(marked[c][p] or val is None
             for c, img in enumerate(images) for p, val in enumerate(img))
    return scene, ok  # @line L7


def owners(rays, shape):
    """The owner of each pixel in a set of voxels: the first voxel of its ray in the set."""
    out = []
    for lists in rays:
        row = []
        for cells in lists:
            o = None
            for c in cells:
                if c is not None and c in shape:
                    o = c
                    break
            row.append(o)
        out.append(row)
    return out


def is_consistent_scene(shape, rays, images, tau):
    """Every voxel passes the test on the pixels it owns, and every non-background pixel has an owner."""
    own = owners(rays, shape)
    groups = {}
    for c, row in enumerate(own):
        for p, o in enumerate(row):
            if o is None:
                if images[c][p] is not None:
                    return False
            else:
                groups.setdefault(o, []).append(images[c][p])
    return all(consistent(vals, tau) for vals in groups.values())


def closest_consistent_scene_brute_force(volume, rays, images, tau):
    """S-bar of Seitz and Dyer: for each pixel, the nearest voxel that owns it in some consistent scene."""
    cells = sorted(volume)
    best = {}
    for mask in range(1 << len(cells)):
        shape = {cells[i] for i in range(len(cells)) if mask >> i & 1}
        if not is_consistent_scene(shape, rays, images, tau):
            continue
        for c, row in enumerate(owners(rays, shape)):
            for p, o in enumerate(row):
                if o is not None and ((c, p) not in best or o[2] < best[(c, p)][2]):
                    best[(c, p)] = o
    return set(best.values())
