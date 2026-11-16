# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/space-carving/. The authors are listed in prov/TB513P.jsonl.

"""Space carving (Kutulakos and Seitz) on a voxel grid.

The grid has nx * ny * nz unit voxels; voxel (i, j, k) is the cube
[i, i+1] x [j, j+1] x [k, k+1] in world coordinates. A camera is (K, R, t):
a world point X maps to X_c = R X + t, and the pixel (u, v) is the center of
the pixel in column u and row v. Each pixel ray is reduced to the ordered list
of voxels that it crosses (a 3D DDA, Amanatides and Woo). A voxel owns a pixel
in the shape V if it is the first voxel of V on the ray of that pixel. Pixel
values are gray numbers, or None for a background pixel.
"""

import math

INF = float("inf")


def inverse_intrinsics(K):
    """K^-1 for K = [[fx, s, cx], [0, fy, cy], [0, 0, 1]]."""
    fx, s, cx = K[0]
    fy, cy = K[1][1], K[1][2]
    return [[1.0 / fx, -s / (fx * fy), (s * cy - cx * fy) / (fx * fy)],
            [0.0, 1.0 / fy, -cy / fy],
            [0.0, 0.0, 1.0]]


def pixel_ray(cam, u, v):
    """Center C = -R^T t and direction R^T K^-1 (u, v, 1) of the ray of pixel (u, v)."""
    K, R, t = cam
    Ki = inverse_intrinsics(K)
    m = [Ki[r][0] * u + Ki[r][1] * v + Ki[r][2] for r in range(3)]
    d = [sum(R[r][c] * m[r] for r in range(3)) for c in range(3)]
    C = [-sum(R[r][c] * t[r] for r in range(3)) for c in range(3)]
    return C, d


def traverse(origin, d, dims):
    """The voxels that the ray origin + s d (s >= 0) crosses, in order (3D DDA)."""
    t0, t1 = 0.0, INF
    for a in range(3):
        if abs(d[a]) < 1e-15:
            if not 0.0 <= origin[a] <= dims[a]:
                return []
        else:
            ta, tb = -origin[a] / d[a], (dims[a] - origin[a]) / d[a]
            if ta > tb:
                ta, tb = tb, ta
            t0, t1 = max(t0, ta), min(t1, tb)
    if t0 >= t1:
        return []
    p = [origin[a] + d[a] * t0 for a in range(3)]
    cell = [min(max(int(math.floor(p[a])), 0), dims[a] - 1) for a in range(3)]
    step, tmax, tdelta = [0] * 3, [INF] * 3, [INF] * 3
    for a in range(3):
        if d[a] > 0:
            step[a], tmax[a], tdelta[a] = 1, (cell[a] + 1 - origin[a]) / d[a], 1.0 / d[a]
        elif d[a] < 0:
            step[a], tmax[a], tdelta[a] = -1, (cell[a] - origin[a]) / d[a], -1.0 / d[a]
    cells = []
    while True:
        cells.append(tuple(cell))
        a = min(range(3), key=lambda b: tmax[b])
        if tmax[a] >= t1:
            return cells
        cell[a] += step[a]
        if not 0 <= cell[a] < dims[a]:
            return cells
        tmax[a] += tdelta[a]


def build_rays(cams, width, height, dims):
    """The voxel list of every pixel of every camera: rays[c][v * width + u]."""
    rays = []
    for cam in cams:
        lists = []
        for v in range(height):
            for u in range(width):
                C, d = pixel_ray(cam, float(u), float(v))
                lists.append(traverse(C, d, dims))
        rays.append(lists)
    return rays


def first_in(cells, shape):
    """The first voxel of the list that is in the shape, or None."""
    for c in cells:
        if c in shape:
            return c
    return None


def render(rays, scene):
    """Images of a voxel scene {voxel: gray value}: the value of the first voxel on each ray, else None."""
    images = []
    for lists in rays:
        img = []
        for cells in lists:
            c = first_in(cells, scene)
            img.append(None if c is None else scene[c])
        images.append(img)
    return images


def owned_values(rays, images, shape):
    """For each voxel of the shape, the values of the pixels it owns (None for background)."""
    owned = {}
    for lists, img in zip(rays, images):
        for cells, val in zip(lists, img):
            c = first_in(cells, shape)
            if c is not None:
                owned.setdefault(c, []).append(val)
    return owned


def consistent(values, tau):
    """The monotone test: no background pixel, and max - min <= tau."""
    if any(x is None for x in values):
        return False
    return not values or max(values) - min(values) <= tau


def covers(rays, images, shape):
    """True if every non-background pixel is owned by a voxel of the shape."""
    for lists, img in zip(rays, images):
        for cells, val in zip(lists, img):
            if val is not None and first_in(cells, shape) is None:
                return False
    return True


def space_carve(volume, rays, images, tau):
    """Carve the voxels that are not photo-consistent until none is left.

    volume: an iterable of voxels that contains the scene. Returns
    (shape, rounds, ok), where ok tells whether the result explains every
    non-background pixel (if not, no photo-consistent shape lies in the volume).
    """
    shape = set(volume)  # @line L1
    rounds = 0
    while True:  # @line L2
        rounds += 1
        owned = owned_values(rays, images, shape)  # @line L3
        bad = {c for c, vals in owned.items() if not consistent(vals, tau)}  # @line L4
        if not bad:  # @line L5
            break
        shape -= bad  # @line L6
    return shape, rounds, covers(rays, images, shape)  # @line L7


def is_photo_consistent(shape, rays, images, tau):
    """A shape is photo-consistent if each voxel passes the test on the pixels it owns
    and every non-background pixel is owned by some voxel."""
    owned = owned_values(rays, images, shape)
    return all(consistent(v, tau) for v in owned.values()) and covers(rays, images, shape)


def photo_hull_brute_force(volume, rays, images, tau):
    """The union of all photo-consistent subsets of a small volume (2^n subsets)."""
    cells = sorted(volume)
    hull = set()
    for mask in range(1 << len(cells)):
        shape = {cells[i] for i in range(len(cells)) if mask >> i & 1}
        if is_photo_consistent(shape, rays, images, tau):
            hull |= shape
    return hull
