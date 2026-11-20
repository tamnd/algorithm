# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/verlet-neighbor-list/. The authors are listed in prov/NKWXRA.jsonl.

import math

Point = list[float]


def minimum_image_dist2(a: Point, b: Point, box: float) -> float:
    """Squared distance from a to the nearest periodic image of b in a cubic box of side box."""
    s = 0.0
    for x, y in zip(a, b):
        d = x - y
        d -= box * round(d / box)
        s += d * d
    return s


class VerletList:
    """A Verlet neighbor list with cutoff rc and skin in a periodic cubic box.

    The list holds the pairs i < j closer than rc + skin at the last build.
    rule is "two" (rebuild when the two largest displacements since the build
    add up to more than the skin) or "half" (rebuild when one displacement is
    more than half the skin). Both are safe; "half" rebuilds at least as often.
    """

    def __init__(self, positions: list[Point], box: float, rc: float, skin: float, rule: str = "two") -> None:
        if rc + skin > box / 2:
            raise ValueError("rc + skin must be at most half the box")
        if rule not in ("two", "half"):
            raise ValueError("rule must be 'two' or 'half'")
        self.box, self.rc, self.skin, self.rule = box, rc, skin, rule
        self.builds = 0
        self.build(positions)

    def build(self, positions: list[Point]) -> None:
        """Store every pair i < j closer than rc + skin, and the positions at this build. O(N^2)."""
        rl2 = (self.rc + self.skin) ** 2  # @line L1
        n = len(positions)
        self.neighbors: list[tuple[int, int]] = []
        for i in range(n):  # @line L2
            for j in range(i + 1, n):  # @line L2
                if minimum_image_dist2(positions[i], positions[j], self.box) < rl2:  # @line L3
                    self.neighbors.append((i, j))  # @line L3
        self.reference = [list(r) for r in positions]  # @line L4
        self.builds += 1

    def displacements(self, positions: list[Point]) -> list[float]:
        """The minimum image distance of each atom from its position at the last build."""
        return [math.sqrt(minimum_image_dist2(r, r0, self.box)) for r, r0 in zip(positions, self.reference)]

    def needs_rebuild(self, positions: list[Point]) -> bool:
        d = self.displacements(positions)  # @line L5
        if self.rule == "half":
            return max(d, default=0.0) > self.skin / 2
        top = sorted(d, reverse=True)[:2] + [0.0, 0.0]  # @line L6
        return top[0] + top[1] > self.skin  # @line L6

    def pairs(self, positions: list[Point]) -> list[tuple[int, int]]:
        """The pairs i < j closer than rc at these positions, rebuilding the list first if needed."""
        if self.needs_rebuild(positions):  # @line L7
            self.build(positions)  # @line L7
        rc2 = self.rc * self.rc
        out = []
        for i, j in self.neighbors:  # @line L8
            if minimum_image_dist2(positions[i], positions[j], self.box) < rc2:  # @line L9
                out.append((i, j))  # @line L9
        return out
