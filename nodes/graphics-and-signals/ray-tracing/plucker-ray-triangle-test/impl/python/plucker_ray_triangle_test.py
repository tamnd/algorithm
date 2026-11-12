# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plucker-ray-triangle-test/. The authors are listed in prov/C4PQD6.jsonl.

"""Entry point named after the slug. The code lives in plucker_ray_triangle.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from plucker_ray_triangle import cross, dot, plucker_intersect, plucker_line, ray_line, side, sub

__all__ = ["cross", "dot", "plucker_intersect", "plucker_line", "ray_line", "side", "sub"]
