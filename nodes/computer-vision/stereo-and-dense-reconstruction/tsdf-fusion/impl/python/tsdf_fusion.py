# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tsdf-fusion/. The authors are listed in prov/AYN2F8.jsonl.

"""Fusion of depth maps into a truncated signed distance field (TSDF).

The volume is a grid of nx * ny * nz voxels of size h. The center of voxel
(i, j, k) is origin + h (i + 1/2, j + 1/2, k + 1/2). Each voxel keeps a fused
value D in [-1, 1] and a weight W; W = 0 means that no camera has seen it.
A camera is (K, R, t) with X_c = R X + t, and a depth map gives the depth Z of
the surface for each pixel (u, v) as depth[v][u], or None where it has no
reading. The signed distance of a voxel is the projective distance
depth - Z_c along the line of sight: positive in front of the surface,
negative behind it.
"""


class Volume:
    def __init__(self, dims, origin, h):
        self.dims, self.origin, self.h = tuple(dims), tuple(origin), float(h)
        n = dims[0] * dims[1] * dims[2]
        self.D = [0.0] * n
        self.W = [0.0] * n

    def index(self, i, j, k):
        return i + self.dims[0] * (j + self.dims[1] * k)

    def center(self, i, j, k):
        return [self.origin[0] + self.h * (i + 0.5),
                self.origin[1] + self.h * (j + 0.5),
                self.origin[2] + self.h * (k + 0.5)]


def integrate(vol, depth, cam, mu, weight=1.0):
    """Fuse one depth map into the volume with the running weighted average."""
    K, R, t = cam
    height, width = len(depth), len(depth[0])
    nx, ny, nz = vol.dims
    for k in range(nz):  # @line L1
        for j in range(ny):
            for i in range(nx):
                X = vol.center(i, j, k)
                Xc = [R[r][0] * X[0] + R[r][1] * X[1] + R[r][2] * X[2] + t[r] for r in range(3)]  # @line L2
                if Xc[2] <= 0.0:
                    continue
                x, y = Xc[0] / Xc[2], Xc[1] / Xc[2]
                u = int(round(K[0][0] * x + K[0][1] * y + K[0][2]))  # @line L3
                v = int(round(K[1][1] * y + K[1][2]))
                if not (0 <= u < width and 0 <= v < height) or depth[v][u] is None:
                    continue
                eta = depth[v][u] - Xc[2]  # @line L4
                if eta < -mu:  # @line L5
                    continue
                f = min(1.0, eta / mu)  # @line L6
                n = vol.index(i, j, k)
                vol.D[n] = (vol.W[n] * vol.D[n] + weight * f) / (vol.W[n] + weight)  # @line L7
                vol.W[n] += weight


def zero_crossings(vol, axis=2):
    """Surface points where D changes sign between two seen neighbors along one axis,
    placed by linear interpolation. Marching cubes builds a mesh from the same data."""
    nx, ny, nz = vol.dims
    step = [0, 0, 0]
    step[axis] = 1
    points = []
    for k in range(nz - step[2]):
        for j in range(ny - step[1]):
            for i in range(nx - step[0]):
                a = vol.index(i, j, k)
                b = vol.index(i + step[0], j + step[1], k + step[2])
                if vol.W[a] == 0.0 or vol.W[b] == 0.0:
                    continue
                da, db = vol.D[a], vol.D[b]
                if (da > 0.0) == (db > 0.0) or da == db:
                    continue
                s = da / (da - db)
                pa = vol.center(i, j, k)
                pb = vol.center(i + step[0], j + step[1], k + step[2])
                points.append([pa[c] + s * (pb[c] - pa[c]) for c in range(3)])
    return points


def batch_average(values_and_weights):
    """The weighted mean that the running average must equal."""
    sw = sum(w for _, w in values_and_weights)
    return sum(f * w for f, w in values_and_weights) / sw, sw
