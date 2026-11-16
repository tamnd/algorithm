# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/octree-occupancy-map/. The authors are listed in prov/34SSST.jsonl.

"""A 3D occupancy map in an octree of log odds, with clamping and pruning.

This follows the design of OctoMap (Hornung et al. 2013). The map covers a
cube of 2^D voxels on each side. A voxel has the integer key (kx, ky, kz),
each in [0, 2^D), and covers the half-open cube of side res whose lowest
corner is origin + res * key. A node at depth d covers a block of
2^(D - d) voxels on each side; the root has depth 0 and the voxels depth D.

A voxel that no update has reached is unknown: no node holds it. A leaf
above depth D is a pruned node: all voxels of its block are known and have
its value. An inner node holds the maximum of the values of its children.
The prior occupancy probability of a voxel is 0.5, so its prior log odds
is 0.
"""

import math

import robest


class _Node:
    __slots__ = ("value", "children")

    def __init__(self, value, inner):
        self.value = value
        self.children = [None] * 8 if inner else None


class OctreeOccupancyMap:
    """An octree of depth D over the voxel keys [0, 2^D)^3.

    l_occ and l_free are the log odds of the inverse sensor model for a
    voxel with an end point and for a voxel that a beam passes through.
    l_min and l_max clamp every voxel value. The defaults are the values
    of Hornung et al. (2013): 0.85, -0.4, -2 and 3.5, the log odds of about
    0.7, 0.4, 0.12 and 0.97. Use None for a bound to switch it off.
    """

    def __init__(self, depth, res=1.0, origin=(0.0, 0.0, 0.0),
                 l_occ=0.85, l_free=-0.4, l_min=-2.0, l_max=3.5):
        if depth < 1 or res <= 0:
            raise ValueError("the depth must be at least 1 and res positive")
        self.depth = int(depth)
        self.size = 1 << self.depth
        self.res = float(res)
        self.origin = tuple(float(v) for v in origin)
        self.l_occ, self.l_free = float(l_occ), float(l_free)
        self.l_min = -math.inf if l_min is None else float(l_min)
        self.l_max = math.inf if l_max is None else float(l_max)
        if not self.l_min <= 0.0 <= self.l_max:
            raise ValueError("the clamping bounds must contain the prior log odds 0")
        self.root = _Node(None, inner=True)

    # ------------------------------------------------------------ invariant

    def check_invariant(self):
        """Raise AssertionError unless the tree is a valid, fully pruned octree."""
        root = self.root
        if root.children is not None and all(c is None for c in root.children):
            assert root.value is None  # the empty map
            return
        self._check(root, 0)

    def _check(self, n, d):
        if n.children is None:
            assert d <= self.depth
            assert self.l_min <= n.value <= self.l_max
            return
        assert d < self.depth and len(n.children) == 8
        kids = [c for c in n.children if c is not None]
        assert kids, "an inner node below the root has no children"
        for c in kids:
            self._check(c, d + 1)
        assert n.value == max(c.value for c in kids)
        same = len(kids) == 8 and all(c.children is None for c in kids)
        assert not (same and all(c.value == kids[0].value for c in kids)), "a node can be pruned"

    # ------------------------------------------------------------ keys

    def key_of(self, point):
        """Return the integer key of the voxel that holds point; it may lie outside the map."""
        return tuple(math.floor((p - o) / self.res) for p, o in zip(point, self.origin))

    def inside(self, key):
        return all(0 <= k < self.size for k in key)

    def key(self, point):
        """Return the key of the voxel that holds point, or None outside the map."""
        k = self.key_of(point)
        return k if self.inside(k) else None

    def _child_index(self, key, d):
        """The child of a node of depth d that holds the voxel key: one bit per axis."""
        b = self.depth - 1 - d
        return ((key[0] >> b) & 1) | (((key[1] >> b) & 1) << 1) | (((key[2] >> b) & 1) << 2)

    # ------------------------------------------------------------ update and search

    def update(self, key, l_meas):
        """Add the log odds l_meas to the voxel key, clamp it, and prune on the way up."""
        if not self.inside(key):
            raise ValueError("the key is outside the map")
        n = self.root  # @line L1
        path = []
        for d in range(self.depth):  # @line L2
            if n.children is None:  # @line L3
                n.children = [_Node(n.value, inner=False) for _ in range(8)]
            c = self._child_index(key, d)  # @line L4
            if n.children[c] is None:  # @line L5
                leaf = d == self.depth - 1
                n.children[c] = _Node(0.0 if leaf else None, inner=not leaf)
            path.append(n)  # @line L6
            n = n.children[c]
        n.value = min(self.l_max, max(self.l_min, n.value + l_meas))  # @line L7
        while path:  # @line L8
            q = path.pop()  # @line L9
            kids = q.children
            first = kids[0]
            if (first is not None and first.children is None
                    and all(c is not None and c.children is None and c.value == first.value
                            for c in kids)):  # @line L10
                q.value = first.value
                q.children = None
            else:  # @line L11
                q.value = max(c.value for c in kids if c is not None)

    def search(self, key, depth=None):
        """Return the log odds of the node of the given depth that holds key, or None if unknown.

        With depth = D (the default) this is the value of the voxel. With a
        smaller depth it is the value of the block of that depth: the
        maximum over the known voxels of the block.
        """
        d_q = self.depth if depth is None else depth
        n = self.root  # @line L12
        d = 0
        while d < d_q and n.children is not None:  # @line L13
            n = n.children[self._child_index(key, d)]  # @line L14
            d += 1
            if n is None:  # @line L15
                return None
        return n.value  # @line L16

    def probability(self, key, depth=None):
        """Return the occupancy probability of search(key, depth), or None if unknown."""
        v = self.search(key, depth)
        return None if v is None else robest.prob_from_logodds(v)

    # ------------------------------------------------------------ rays and scans

    def voxels_on_segment(self, a, b):
        """Return the keys of the voxels that the segment from a to b crosses, in order.

        This is the 3D traversal of Amanatides and Woo (1987) on the infinite
        lattice of voxels. It takes |kb - ka| steps per axis, and each step
        moves to a voxel that shares a face with the last one.
        """
        k = list(self.key_of(a))
        kb = self.key_of(b)
        step, t_max, t_delta = [0] * 3, [math.inf] * 3, [math.inf] * 3
        for ax in range(3):
            dv = b[ax] - a[ax]
            if dv != 0:
                step[ax] = 1 if dv > 0 else -1
                edge = self.origin[ax] + (k[ax] + (1 if dv > 0 else 0)) * self.res
                t_max[ax] = (edge - a[ax]) / dv
                t_delta[ax] = self.res / abs(dv)
        out = [tuple(k)]
        for _ in range(sum(abs(kb[ax] - k[ax]) for ax in range(3))):
            ax = min((t_max[i], i) for i in range(3) if k[i] != kb[i])[1]
            k[ax] += step[ax]
            t_max[ax] += t_delta[ax]
            out.append(tuple(k))
        return out

    def insert_scan(self, sensor, points):
        """Insert one scan: beams from sensor to each end point, all of them hits.

        Every voxel is updated at most once per scan. A voxel that holds an
        end point gets l_occ, even if another beam of the scan passes
        through it. Voxels outside the map are skipped.
        """
        free, occupied = set(), set()  # @line L17
        for z in points:  # @line L18
            cells = self.voxels_on_segment(sensor, z)  # @line L19
            free.update(cells[:-1])  # @line L20
            occupied.add(cells[-1])
        for k in sorted(free - occupied):  # @line L21
            if self.inside(k):
                self.update(k, self.l_free)
        for k in sorted(occupied):  # @line L22
            if self.inside(k):
                self.update(k, self.l_occ)

    # ------------------------------------------------------------ inspection

    def num_nodes(self):
        """Return the number of nodes, the root included."""
        count, stack = 0, [self.root]
        while stack:
            n = stack.pop()
            count += 1
            if n.children is not None:
                stack.extend(c for c in n.children if c is not None)
        return count

    def leaves(self):
        """Return a list of (key of the lowest voxel, side in voxels, value) for each leaf."""
        out = []
        stack = [(self.root, 0, (0, 0, 0))]
        while stack:
            n, d, low = stack.pop()
            if n.children is None:
                out.append((low, 1 << (self.depth - d), n.value))
                continue
            half = 1 << (self.depth - d - 1)
            for c, child in enumerate(n.children):
                if child is not None:
                    off = (low[0] + (c & 1) * half, low[1] + ((c >> 1) & 1) * half,
                           low[2] + ((c >> 2) & 1) * half)
                    stack.append((child, d + 1, off))
        return sorted(out)
