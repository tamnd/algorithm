# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/occupancy-grid-mapping/. The authors are listed in prov/NBXJ4P.jsonl.

"""Occupancy grid mapping with known poses (Thrun, Burgard and Fox 2005, Tables 9.1 and 9.2).

The grid has W by H square cells of side res. Cell (i, j) has its center at
(ox + (i + 0.5) res, oy + (j + 0.5) res); the map is a list of W columns of
H log odds values, l[i][j]. A pose is (x, y, theta) in meters and radians.
A scan is a list of beams (z, bearing): the range z in meters, at most
z_max, and the bearing of the beam in the robot frame in radians.
"""

import math

import robest


class Grid:
    """The geometry of a grid: origin (ox, oy), cell side res, W by H cells."""

    def __init__(self, ox, oy, res, width, height):
        self.ox, self.oy, self.res = float(ox), float(oy), float(res)
        self.width, self.height = int(width), int(height)

    def center(self, i, j):
        return (self.ox + (i + 0.5) * self.res, self.oy + (j + 0.5) * self.res)

    def cells_within(self, x, y, radius):
        """Yield the cells whose center can be within radius of (x, y)."""
        i0 = max(0, int(math.floor((x - radius - self.ox) / self.res)))
        i1 = min(self.width - 1, int(math.floor((x + radius - self.ox) / self.res)))
        j0 = max(0, int(math.floor((y - radius - self.oy) / self.res)))
        j1 = min(self.height - 1, int(math.floor((y + radius - self.oy) / self.res)))
        for i in range(i0, i1 + 1):
            for j in range(j0, j1 + 1):
                yield i, j


class InverseRangeSensorModel:
    """The inverse range sensor model of Table 9.2, with its parameters.

    alpha is the thickness of obstacles and beta the width of a beam.
    The log odds l_occ and l_free are rules of thumb, not derived values.
    """

    def __init__(self, z_max, alpha, beta, p_occ=0.7, p_free=0.4, p_prior=0.5):
        self.z_max, self.alpha, self.beta = z_max, alpha, beta
        self.l_occ = robest.logodds(p_occ)
        self.l_free = robest.logodds(p_free)
        self.l0 = robest.logodds(p_prior)

    def __call__(self, center, pose, scan):
        xi, yi = center
        x, y, theta = pose
        r = math.hypot(xi - x, yi - y)  # @line L7
        phi = math.atan2(yi - y, xi - x) - theta
        k = min(range(len(scan)), key=lambda j: abs(robest.wrap_angle(phi - scan[j][1])))  # @line L8
        zk, bk = scan[k]
        dphi = abs(robest.wrap_angle(phi - bk))
        if r > min(self.z_max, zk + self.alpha / 2) or dphi > self.beta / 2:  # @line L9
            return self.l0
        if zk < self.z_max and abs(r - zk) < self.alpha / 2:  # @line L10
            return self.l_occ
        if r <= zk:  # @line L11
            return self.l_free
        return self.l0  # @line L12


def occupancy_grid_mapping(l, grid, pose, scan, ism):
    """Return the log odds map after one scan taken at a known pose.

    l is updated in place and returned. Only the cells within reach of the
    sensor are visited; for the others the inverse model returns l0, so the
    update would leave them unchanged.
    """
    reach = ism.z_max + ism.alpha
    for i, j in grid.cells_within(pose[0], pose[1], reach):  # @line L1
        center = grid.center(i, j)  # @line L6
        v = ism(center, pose, scan)
        if v != ism.l0:  # @line L2
            l[i][j] += v - ism.l0  # @line L3
        # else the cell is outside the perceptual field and keeps its value  # @line L4
    return l  # @line L5


def new_map(grid, ism):
    """Return a map with every cell at the prior log odds l0."""
    return [[ism.l0] * grid.height for _ in range(grid.width)]


def probabilities(l):
    """Return the map of occupancy probabilities of a log odds map."""
    return [[robest.prob_from_logodds(v) for v in col] for col in l]
