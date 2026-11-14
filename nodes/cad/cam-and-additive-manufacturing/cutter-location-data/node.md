---
tag: 9TA6DF
kind: definition
slug: cutter-location-data
name: Cutter location data
aliases:
- CL data
- cutter location path
area: cad/cam-and-additive-manufacturing
level: core
summary: The sequence of tool reference points and axis directions, offset from the cutter contact points on the part, that a CNC machine follows.
prereqs: [toolpath-planning, offset-surface]
see_also: [inverse-tool-offset, gouge-detection, scallop-height, z-map-model, nc-verification, swept-volume, accessibility-cone, iso-parametric-toolpath]
sources:
  - book: isbn:978-0-412-78020-2
    title: Byoung K. Choi and Robert B. Jerard, Sculptured Surface Machining, Theory and Applications, Kluwer Academic Publishers, 1998
    locator: chapter 5, fundamentals of tool-path generation, the parts on cutter contact and cutter location points and the tool offset for ball, flat and torus cutters
  - title: ISO 3592:2000, Industrial automation systems, Numerical control of machines, NC processor output, File structure and language format
    locator: the CLDATA file that carries cutter location records from the NC processor to the post-processor; it replaces ISO 3592:1978
  - title: ISO 4343:2000, Industrial automation systems, Numerical control of machines, NC processor output, Post processor commands
    locator: the post-processor commands that travel with the cutter location records
---

Cutter location data, or CL data, is the list of tool positions that a CAM system computes for a part: for each step, the position of a reference point on the tool and, for multi-axis machines, the direction of the tool axis. The reference point is usually the tip of the tool on its axis, or the center of a ball end mill. It is not the point where the tool touches the part. That point, the *cutter contact* (CC) point, lies on the part surface, and the CL point is found from it by an offset that depends on the surface normal and the shape of the tool. A post-processor then turns the CL data into the commands of one machine, such as G-code. This is a term of mechanical manufacturing: placement and routing here mean where a cutter goes and how it moves, not the placement and routing of a circuit.

## Definition

A **CL point** is a pair $(c, a)$ of a point $c$ on the tool, the tool reference point, and a unit vector $a$ along the tool axis, pointing from the tip into the spindle. On a three-axis machine $a = (0, 0, 1)$ for every point, and only $c$ is stored. **CL data** is a sequence of CL points, with the feed and the kind of motion between them (straight, circular or rapid). A **CL path** is the curve that the reference point follows.

Given a CC point $p$ on the part with outward unit normal $n$, and the tool axis $a$, write
$$
u = \frac{n - (n \cdot a)\,a}{|n - (n \cdot a)\,a|}
$$
for the unit vector across the axis toward the normal (defined when $n \ne \pm a$). The CL point of the tool tip, on the axis, is then:

| tool | tool tip $c$ |
|---|---|
| ball end mill, radius $r$ | $p + r\,n - r\,a$, with the ball center at $p + r\,n$ |
| flat end mill, radius $R$ | $p + R\,u$ |
| torus (bull-nose) cutter, radius $R$, corner radius $r_c$ | $p + r_c\,n + (R - r_c)\,u - r_c\,a$ |

The torus formula gives the ball formula for $r_c = R$ and the flat formula for $r_c = 0$. A ball end mill does not need $u$, so its offset is defined for every normal. For a flat or torus cutter on a face with $n = a$, every point of the flat bottom touches, and the CL point is chosen by the path.

For a ball end mill, the set of ball centers over a whole surface is the [offset surface](/offset-surface/) at distance $r$, and the CL surface of the tip is that offset moved down by $r$. Where the offset folds, at concave regions with radius smaller than $r$, the offset of a CC point gives a CL point at which the tool cuts into the part: a gouge. Correct CL data keeps the tool out of the part at every point, which is the job of [gouge detection](/gouge-detection/) or of methods that compute the CL surface directly, such as the [inverse tool offset](/inverse-tool-offset/).

## Examples and non-examples

**Examples.**

- **A tool on a slope.** Take the plane $z = \tfrac34 x$, the CC point $p = (4, 0, 3)$, and a vertical axis $a = (0, 0, 1)$. The outward normal is $n = (-\tfrac35, 0, \tfrac45)$, and $u = (-1, 0, 0)$. A ball end mill with $r = 5$ has its center at $(1, 0, 7)$ and its tip at $(1, 0, 2)$. A flat end mill with $R = 5$ has its tip at $(-1, 0, 3)$, so it touches the slope at the uphill edge of its bottom. A torus cutter with $R = 5$ and $r_c = 1$ has its tip at $(-0.6, 0, 2.8)$. Three tools touch the same CC point from three different CL points.
- **A pocket floor.** For a flat end mill on a horizontal floor at depth $z_0$, the CL points of a [contour-parallel](/contour-parallel-toolpath/) or [direction-parallel](/direction-parallel-toolpath/) path are the points of the path at height $z_0$. The offset by the tool radius is already in the path, which runs in the inward offset of the pocket.
- **A five-axis record.** On a five-axis machine each CL record holds six numbers, $(x, y, z)$ of the tip and $(i, j, k)$ of the axis.

**Non-examples.**

- **CC points.** The points where the tool touches the part are on the part surface. They are the input to the CL computation, not CL data. An [iso-parametric](/iso-parametric-toolpath/) path is a CC path until it is offset.
- **G-code.** The program that a machine runs is in the coordinates of its axes. On a five-axis machine the post-processor turns each axis vector into the angles of the rotary axes and moves the linear axes to match. The same CL data gives different G-code on different machines.
- **The swept volume.** The set of points that the tool passes through is the [swept volume](/swept-volume/) of the tool along the CL path. It is used for verification, not sent to the machine.

## Related definitions

- The [offset surface](/offset-surface/) of the part at the ball radius is the surface of ball centers.
- The [scallop height](/scallop-height/) between two passes is measured between their CC points and sets the step between CL paths.
- The [z-map model](/z-map-model/) and other methods of [NC verification](/nc-verification/) simulate the cut of the CL data on the stock.
- An [accessibility cone](/accessibility-cone/) gives the axis directions $a$ at which the tool can reach a CC point without collision.
- The [inverse tool offset](/inverse-tool-offset/) computes the CL surface of a three-axis tool directly on a grid, with no CC points.

## References
