# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-quadtree/. The authors are listed in prov/HXZGKW.jsonl.

from bisect import bisect_left, bisect_right
from typing import Iterable

Pixel = tuple[int, int]
Block = tuple[int, int]  # (Morton code of the lower left pixel, level)


def morton(x: int, y: int, depth: int) -> int:
    """Interleave the bits of x and y: bit i of x goes to bit 2i, bit i of y to bit 2i+1."""
    z = 0
    for i in range(depth):
        z |= ((x >> i) & 1) << (2 * i)
        z |= ((y >> i) & 1) << (2 * i + 1)
    return z


def demorton(z: int, depth: int) -> Pixel:
    """The inverse of morton."""
    x = y = 0
    for i in range(depth):
        x |= ((z >> (2 * i)) & 1) << i
        y |= ((z >> (2 * i + 1)) & 1) << i
    return x, y


class LinearQuadtree:
    """The black pixels of a 2^depth by 2^depth binary image, as a sorted list of blocks.

    A block (c, l) is the aligned square of side 2^l whose pixels have the Morton
    codes c to c + 4^l - 1. Invariant: c is a multiple of 4^l, the blocks are
    disjoint and sorted by code, and no four sibling blocks of one level are all
    present (they would form their parent). So the list is the set of black
    leaves of the region quadtree of the image, and it is unique.
    """

    def __init__(self, depth: int) -> None:
        if depth < 0:
            raise ValueError("need depth >= 0")
        self.depth = depth
        self.codes: list[int] = []
        self.levels: list[int] = []

    @classmethod
    def from_pixels(cls, depth: int, pixels: Iterable[Pixel]) -> "LinearQuadtree":
        """Build from a set of black pixels with one sort and one stack pass. O(n log n)."""
        t = cls(depth)
        zs = sorted({morton(*t._norm(p), depth) for p in pixels})
        stack: list[Block] = []
        for z in zs:  # @line L1
            stack.append((z, 0))  # @line L2
            while len(stack) >= 4:  # @line L3
                c, l = stack[-4]
                step = 1 << (2 * l)
                if c % (step << 2) != 0 or any(stack[-4 + k] != (c + k * step, l) for k in range(1, 4)):  # @line L4
                    break
                del stack[-4:]  # @line L5
                stack.append((c, l + 1))  # @line L6
        t.codes = [c for c, _ in stack]
        t.levels = [l for _, l in stack]
        return t

    def __len__(self) -> int:
        return len(self.codes)

    def _norm(self, p: Pixel) -> Pixel:
        x, y = int(p[0]), int(p[1])
        if not (0 <= x < (1 << self.depth) and 0 <= y < (1 << self.depth)):
            raise ValueError("the pixel is outside the image")
        return x, y

    def _locate(self, z: int) -> int:
        """Index of the block that holds the code z, or -1."""
        i = bisect_right(self.codes, z) - 1  # @line L7
        if i >= 0 and z < self.codes[i] + (1 << (2 * self.levels[i])):  # @line L8
            return i
        return -1  # @line L9

    def locate(self, p: Pixel) -> tuple[int, int, int] | None:
        """The block (x, y, side) that holds the pixel p, or None if p is white. O(log n)."""
        i = self._locate(morton(*self._norm(p), self.depth))
        if i < 0:
            return None
        x, y = demorton(self.codes[i], self.depth)
        return x, y, 1 << self.levels[i]

    def __contains__(self, p: Pixel) -> bool:
        return self._locate(morton(*self._norm(p), self.depth)) >= 0

    def _has(self, c: int, l: int) -> bool:
        i = bisect_left(self.codes, c)
        return i < len(self.codes) and self.codes[i] == c and self.levels[i] == l

    def _add(self, c: int, l: int) -> None:
        i = bisect_left(self.codes, c)
        self.codes.insert(i, c)
        self.levels.insert(i, l)

    def _remove(self, c: int) -> None:
        i = bisect_left(self.codes, c)
        del self.codes[i]
        del self.levels[i]

    def insert(self, p: Pixel) -> bool:
        """Make the pixel p black. Returns False if it was black. O(depth) list updates."""
        z = morton(*self._norm(p), self.depth)
        if self._locate(z) >= 0:  # @line L10
            return False
        c, l = z, 0
        self._add(c, l)  # @line L11
        while l < self.depth:
            step = 1 << (2 * l)
            parent = c - c % (step << 2)
            if not all(self._has(parent + k * step, l) for k in range(4)):  # @line L12
                break
            for k in range(4):  # @line L13
                self._remove(parent + k * step)
            c, l = parent, l + 1
            self._add(c, l)
        return True

    def delete(self, p: Pixel) -> bool:
        """Make the pixel p white. Returns False if it was white. O(depth) list updates."""
        z = morton(*self._norm(p), self.depth)
        i = self._locate(z)  # @line L14
        if i < 0:
            return False
        l = self.levels[i]
        self._remove(self.codes[i])  # @line L15
        for j in range(l - 1, -1, -1):  # @line L16
            step = 1 << (2 * j)
            base = z - z % (step << 2)
            for k in range(4):  # @line L17
                if base + k * step != z - z % step:
                    self._add(base + k * step, j)
        return True

    def blocks_in_cell(self, x: int, y: int, level: int) -> list[tuple[int, int, int]]:
        """The black blocks inside the aligned cell of side 2^level at (x, y), clipped to it.

        The blocks inside a cell form one run of the sorted list, found by two
        binary searches. A block that covers the whole cell is returned as the cell.
        """
        if level < 0 or level > self.depth or x % (1 << level) or y % (1 << level):
            raise ValueError("need an aligned cell inside the image")
        lo = morton(*self._norm((x, y)), self.depth)
        hi = lo + (1 << (2 * level))
        i = self._locate(lo)
        if i >= 0 and self.levels[i] >= level:
            return [(x, y, 1 << level)]
        out = []
        for j in range(bisect_left(self.codes, lo), bisect_left(self.codes, hi)):
            bx, by = demorton(self.codes[j], self.depth)
            out.append((bx, by, 1 << self.levels[j]))
        return out

    def blocks(self) -> list[tuple[int, int, int]]:
        """All blocks as (x, y, side), in Morton order."""
        return [(*demorton(c, self.depth), 1 << l) for c, l in zip(self.codes, self.levels)]

    def area(self) -> int:
        """The number of black pixels."""
        return sum(1 << (2 * l) for l in self.levels)

    def pixels(self) -> list[Pixel]:
        out = []
        for c, l in zip(self.codes, self.levels):
            for z in range(c, c + (1 << (2 * l))):
                out.append(demorton(z, self.depth))
        return out

    def check_invariant(self) -> None:
        full = 1 << (2 * self.depth)
        assert len(self.codes) == len(self.levels)
        end = 0
        for c, l in zip(self.codes, self.levels):
            assert 0 <= l <= self.depth, "level out of range"
            assert c % (1 << (2 * l)) == 0, "block not aligned"
            assert c >= end, "blocks overlap or are out of order"
            end = c + (1 << (2 * l))
            assert end <= full, "block outside the image"
        for c, l in zip(self.codes, self.levels):
            if l < self.depth:
                step = 1 << (2 * l)
                parent = c - c % (step << 2)
                assert not all(self._has(parent + k * step, l) for k in range(4)), "four siblings not merged"
