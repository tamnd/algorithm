# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/occupancy-grid-map/. The authors are listed in prov/MJFAZ4.jsonl.

"""A 2D occupancy grid map that stores log odds, with optional clamping.

The grid has W by H square cells of side res. Cell (i, j) covers the
half-open square [ox + i res, ox + (i + 1) res) x [oy + j res, oy + (j + 1) res).
The log odds are kept in one flat list in row-major order, at index j W + i.
"""

import math

import robest


class OccupancyGridMap:
    """A grid of log odds values l = log(p / (1 - p)), one per cell.

    p_prior is the prior occupancy probability of every cell. If p_min and
    p_max are given, every update clamps the log odds to
    [logodds(p_min), logodds(p_max)].
    """

    def __init__(self, ox, oy, res, width, height, p_prior=0.5, p_min=None, p_max=None):
        if res <= 0 or width <= 0 or height <= 0:
            raise ValueError("the grid must have a positive size")
        self.ox, self.oy, self.res = float(ox), float(oy), float(res)
        self.width, self.height = int(width), int(height)
        self.l0 = robest.logodds(p_prior)
        self.l_min = robest.logodds(p_min) if p_min is not None else -math.inf
        self.l_max = robest.logodds(p_max) if p_max is not None else math.inf
        if not self.l_min <= self.l0 <= self.l_max:
            raise ValueError("the prior must lie between the clamping bounds")
        self.l = [self.l0] * (self.width * self.height)

    def check_invariant(self):
        """Raise AssertionError unless there is one value per cell, inside the bounds."""
        assert len(self.l) == self.width * self.height
        assert all(self.l_min <= v <= self.l_max for v in self.l)

    # ------------------------------------------------------------ geometry

    def cell_of(self, x, y):
        """Return the integer indices (i, j) of the cell that holds (x, y).

        The indices may lie outside the grid; use inside() to check them.
        """
        i = math.floor((x - self.ox) / self.res)  # @line L1
        j = math.floor((y - self.oy) / self.res)
        return i, j

    def inside(self, i, j):
        return 0 <= i < self.width and 0 <= j < self.height  # @line L2

    def index(self, x, y):
        """Return the cell (i, j) that holds the point (x, y), or None outside the grid."""
        i, j = self.cell_of(x, y)
        return (i, j) if self.inside(i, j) else None

    def center(self, i, j):
        return (self.ox + (i + 0.5) * self.res, self.oy + (j + 0.5) * self.res)

    # ------------------------------------------------------------ values

    def log_odds(self, i, j):
        return self.l[j * self.width + i]

    def probability(self, i, j):
        return robest.prob_from_logodds(self.l[j * self.width + i])  # @line L5

    def update(self, i, j, l_meas):
        """Add the log odds l_meas of one inverse model value to cell (i, j)."""
        k = j * self.width + i  # @line L3
        v = self.l[k] + l_meas - self.l0  # @line L4
        self.l[k] = min(self.l_max, max(self.l_min, v))

    # ------------------------------------------------------------ rays

    def cells_on_segment(self, a, b):
        """Return the cells that the segment from a to b crosses, in order.

        This is the traversal of Amanatides and Woo (1987) on the infinite
        lattice of cells: it starts in the cell of a, ends in the cell of b,
        and each step moves to a cell that shares an edge with the last one.
        """
        ax, ay = a
        bx, by = b
        i, j = self.cell_of(ax, ay)  # @line L6
        ib, jb = self.cell_of(bx, by)
        dx, dy = bx - ax, by - ay
        step_i = 1 if dx > 0 else -1
        step_j = 1 if dy > 0 else -1
        if dx != 0:  # @line L7
            edge = self.ox + (i + (1 if dx > 0 else 0)) * self.res
            t_max_i, t_delta_i = (edge - ax) / dx, self.res / abs(dx)
        else:
            t_max_i, t_delta_i = math.inf, math.inf
        if dy != 0:
            edge = self.oy + (j + (1 if dy > 0 else 0)) * self.res
            t_max_j, t_delta_j = (edge - ay) / dy, self.res / abs(dy)
        else:
            t_max_j, t_delta_j = math.inf, math.inf
        cells = [(i, j)]  # @line L8
        for _ in range(abs(ib - i) + abs(jb - j)):  # @line L9
            if j == jb or (i != ib and t_max_i < t_max_j):  # @line L10
                i += step_i
                t_max_i += t_delta_i
            else:  # @line L11
                j += step_j
                t_max_j += t_delta_j
            cells.append((i, j))  # @line L12
        return cells

    def insert_ray(self, a, b, hit, l_occ=None, l_free=None):
        """Update the cells of one beam from the sensor at a to the end point b.

        The cells before the end cell get l_free. The end cell gets l_occ if
        hit is true (the beam stopped at an obstacle) and l_free if not (a
        max range reading). Cells outside the grid are skipped. The default
        values are the log odds of 0.7 and 0.4, which are rules of thumb.
        """
        if l_occ is None:
            l_occ = robest.logodds(0.7)
        if l_free is None:
            l_free = robest.logodds(0.4)
        cells = self.cells_on_segment(a, b)
        for i, j in cells[:-1]:  # @line L13
            if self.inside(i, j):
                self.update(i, j, l_free)
        i, j = cells[-1]
        if self.inside(i, j):  # @line L14
            self.update(i, j, l_occ if hit else l_free)
