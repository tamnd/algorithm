# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stencil-buffer/. The authors are listed in prov/A59S6S.jsonl.

"""A software stencil buffer with the OpenGL test and update rules, and a
stencil then cover path fill that uses it.

Each pixel holds an unsigned integer of `bits` bits. A fragment at pixel (i, j)
first goes through the stencil test (ref & mask) FUNC (stored & mask). Then one
of three operations updates the stored value: sfail when the stencil test
fails, dpfail when the stencil test passes and the depth test fails, dppass
when both pass. The write mask selects the bits that the update may change.
Pixel centers are at (i + 1/2, j + 1/2), and y grows downward.
"""

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]

FUNCS = {
    "NEVER": lambda r, s: False,
    "LESS": lambda r, s: r < s,
    "LEQUAL": lambda r, s: r <= s,
    "GREATER": lambda r, s: r > s,
    "GEQUAL": lambda r, s: r >= s,
    "EQUAL": lambda r, s: r == s,
    "NOTEQUAL": lambda r, s: r != s,
    "ALWAYS": lambda r, s: True,
}
OPS = ("KEEP", "ZERO", "REPLACE", "INCR", "INCR_WRAP", "DECR", "DECR_WRAP", "INVERT")


class StencilBuffer:
    def __init__(self, width: int, height: int, bits: int = 8):
        if bits < 1:
            raise ValueError("a stencil buffer needs at least one bit")
        self.width, self.height, self.bits = width, height, bits
        self.max = (1 << bits) - 1
        self.values = [[0] * width for _ in range(height)]
        self.func, self.ref, self.mask = "ALWAYS", 0, self.max  # the initial OpenGL state
        self.ops = {True: ("KEEP", "KEEP", "KEEP"), False: ("KEEP", "KEEP", "KEEP")}  # front, back
        self.write_mask = self.max

    def clear(self, value: int = 0) -> None:
        v = value & self.max
        self.values = [[v] * self.width for _ in range(self.height)]

    def set_func(self, func: str, ref: int, mask: int) -> None:
        if func not in FUNCS:
            raise ValueError(f"unknown stencil function {func}")
        self.func, self.ref, self.mask = func, min(max(ref, 0), self.max), mask & self.max  # ref is clamped

    def set_op(self, sfail: str, dpfail: str, dppass: str, face: str = "FRONT_AND_BACK") -> None:
        for op in (sfail, dpfail, dppass):
            if op not in OPS:
                raise ValueError(f"unknown stencil operation {op}")
        if face in ("FRONT", "FRONT_AND_BACK"):
            self.ops[True] = (sfail, dpfail, dppass)
        if face in ("BACK", "FRONT_AND_BACK"):
            self.ops[False] = (sfail, dpfail, dppass)

    def test(self, i: int, j: int) -> bool:
        return FUNCS[self.func](self.ref & self.mask, self.values[j][i] & self.mask)  # @line L1

    def _apply(self, op: str, s: int) -> int:
        if op == "KEEP":
            return s
        if op == "ZERO":
            return 0
        if op == "REPLACE":
            return self.ref
        if op == "INCR":
            return min(s + 1, self.max)  # saturates
        if op == "INCR_WRAP":
            return (s + 1) & self.max
        if op == "DECR":
            return max(s - 1, 0)  # saturates
        if op == "DECR_WRAP":
            return (s - 1) & self.max
        return ~s & self.max  # INVERT

    def fragment(self, i: int, j: int, front: bool = True, depth_pass: bool = True) -> bool:
        """Run one fragment through the stencil stage. Return True when it passes the stencil and depth tests."""
        passed = self.test(i, j)
        sfail, dpfail, dppass = self.ops[front]
        op = sfail if not passed else (dppass if depth_pass else dpfail)  # @line L2
        s = self.values[j][i]
        new = self._apply(op, s)
        self.values[j][i] = (s & ~self.write_mask & self.max) | (new & self.write_mask)  # @line L3
        return passed and depth_pass


def _orient(a: Point, b: Point, c: Point) -> Number:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def triangle_pixels(a: Point, b: Point, c: Point, width: int, height: int) -> list[tuple[int, int]]:
    """Pixels whose center, moved by (e, e^2) for an infinitesimal e > 0, is inside the triangle.

    This is the top-left rule: a pixel on an edge shared by two triangles goes to exactly one of them.
    A triangle with zero area covers no pixel.
    """
    area = _orient(a, b, c)
    if area == 0:
        return []
    if area < 0:
        b, c = c, b
    edges = ((a, b), (b, c), (c, a))
    out = []
    for j in range(height):
        py = Fraction(2 * j + 1, 2)
        for i in range(width):
            px = Fraction(2 * i + 1, 2)
            ok = True
            for p, q in edges:
                e = (q[0] - p[0]) * (py - p[1]) - (q[1] - p[1]) * (px - p[0])
                ax, by = -(q[1] - p[1]), q[0] - p[0]  # the change of e along x and along y
                if not (e > 0 or (e == 0 and (ax > 0 or (ax == 0 and by > 0)))):
                    ok = False
                    break
            if ok:
                out.append((i, j))
    return out


def fill_path(rings: Sequence[Sequence[Point]], width: int, height: int, rule: str = "nonzero", bits: int = 8,
              saturate: bool = False) -> tuple[set[tuple[int, int]], StencilBuffer]:
    """Stencil then cover. Return the covered pixels and the stencil buffer after the stencil pass.

    saturate=True uses INCR and DECR in place of the wrapping operations, to show why they give wrong counts.
    """
    sb = StencilBuffer(width, height, bits)
    sb.set_func("ALWAYS", 0, sb.max)  # @line L4
    if rule == "nonzero":
        sb.set_op("KEEP", "KEEP", "INCR" if saturate else "INCR_WRAP", "FRONT")
        sb.set_op("KEEP", "KEEP", "DECR" if saturate else "DECR_WRAP", "BACK")
        cover_mask = sb.max
    elif rule == "evenodd":
        sb.set_op("KEEP", "KEEP", "INVERT")
        sb.write_mask = 1  # only bit 0 holds the parity
        cover_mask = 1
    else:
        raise ValueError("rule must be 'nonzero' or 'evenodd'")
    for ring in rings:
        for k in range(1, len(ring) - 1):  # @line L5
            a, b, c = ring[0], ring[k], ring[k + 1]
            front = _orient(a, b, c) > 0
            for i, j in triangle_pixels(a, b, c, width, height):  # @line L6
                sb.fragment(i, j, front)
    after_stencil = [row[:] for row in sb.values]
    sb.set_func("NOTEQUAL", 0, cover_mask)  # @line L7
    sb.write_mask = sb.max
    sb.set_op("ZERO", "ZERO", "ZERO")  # cover resets the buffer for the next path
    covered = set()
    for j in range(height):  # @line L8
        for i in range(width):
            if sb.fragment(i, j):
                covered.add((i, j))
    sb.values = after_stencil
    return covered, sb
