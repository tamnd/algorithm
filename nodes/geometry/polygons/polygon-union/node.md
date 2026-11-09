---
tag: MCDBFV
kind: problem
slug: polygon-union
name: Polygon union
aliases:
- union of polygons
- union of rectangles
- polygon dissolve
area: geometry/polygons
level: core
summary: Compute the boundary or area of the union of a set of polygons.
prereqs: [simple-polygon, polygon-clipping]
see_also: [polygon-clipping, vatti-clipping, area-of-union-of-rectangles, klee-measure-problem, polygon-area, minkowski-sum, segment-tree, sweep-line-technique]
sources:
  - paper: "Klara Kedem, Ron Livne, János Pach and Micha Sharir, On the union of Jordan regions and collision-free translational motion amidst polygonal obstacles, Discrete and Computational Geometry 1(1), 59 to 71 (1986)"
    locator: the bound of at most 6n − 12 boundary intersection points for the union of n pseudo-disks, and its use for Minkowski sums of disjoint convex polygons with a convex robot
  - paper: doi:10.1145/129902.129906
    title: Bala R. Vatti, A generic solution to polygon clipping, Communications of the ACM 35(7), 56 to 63 (1992)
    locator: the sweep that computes the union of many contours with holes and self-intersections in one pass
  - paper: "Michael L. Fredman and Bruce Weide, On the complexity of computing the measure of the union of intervals, Communications of the ACM 21(7), 540 to 544 (1978)"
    locator: the Ω(n log n) lower bound for the length of a union of n intervals in the linear decision tree model
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 8, the geometry of rectangles (the measure, perimeter and contour of a union of rectangles by a sweep with a segment tree)
---

The polygon union problem asks for the region covered by a set of polygons: its boundary, as a set of contours with holes, or only its area or perimeter. For two polygons it is one case of [polygon clipping](/polygon-clipping/). For many polygons the difficulty is the size of the answer: $N$ polygons with $n$ vertices in total can have a union whose boundary has $\Theta(n^2)$ vertices, as a grid of thin rectangles shows, while special families such as pseudo-disks have unions of linear size. The general method is a plane sweep over all edges, as in [Vatti clipping](/vatti-clipping/), that keeps for each strip between edges the number of polygons covering it; for axis-parallel rectangles the [area of union of rectangles](/area-of-union-of-rectangles/) is found in $O(N \log N)$ time with a [segment tree](/segment-tree/), which is optimal.

## In plain words

Drop several paper shapes on a table, so that some overlap. The union is the part of the table that is covered by at least one shape. You may want the outline of that covered part, or only how much table it covers.

Adding the areas of the shapes counts the overlaps twice, so it is too much. Instead, slide a ruler across the table. At each moment, the ruler crosses the shapes in a set of pieces; the covered part of the ruler is where at least one shape is under it. Adding up the covered length as the ruler moves gives the covered area, and recording where the covered part starts and stops gives the outline.

## Definition

**Input.** A set of $N$ polygons $P_1, \ldots, P_N$, each [simple](/simple-polygon/) or with holes, with $n$ vertices in total.

**Output.** One of:

- the **boundary** of $U = P_1 \cup \cdots \cup P_N$, as a set of contours, outer contours counterclockwise and holes clockwise;
- the **area** of $U$;
- the **perimeter** of $U$, the length of its boundary.

**Model.** The [real RAM](/real-ram/). Boundary vertices of $U$ are input vertices or crossing points of two edges, so on integer input the area is rational and can be computed exactly.

**General position.** No three edges pass through one point, and no two edges overlap. With overlapping edges, as when two rectangles share a side, a sweep treats the two copies as one edge with a coverage change of 0 or 2 and drops it from the boundary when the coverage on both sides is positive.

Let $k$ be the number of pairs of edges that cross.

## Variants

- **Two polygons.** The union case of [polygon clipping](/polygon-clipping/), solved by [Weiler-Atherton](/weiler-atherton-algorithm/), [Greiner-Hormann](/greiner-hormann-algorithm/) or [Vatti](/vatti-clipping/).
- **Axis-parallel rectangles.** The area is the [area of union of rectangles](/area-of-union-of-rectangles/), in $O(N \log N)$ time; the perimeter and the contour are also found by a sweep with a segment tree, in $O(N \log N)$ and $O(N \log N + s)$ time for a contour with $s$ edges.
- **Boxes in $d$ dimensions.** The volume of the union is [Klee's measure problem](/klee-measure-problem/); in one dimension it is the length of a union of intervals.
- **Pseudo-disks and fat objects.** Families whose boundaries cross few times have unions of small size, which makes output-sensitive algorithms fast; see the bounds below.
- **Minkowski sums.** The free space for a translating robot is the complement of the union of the [Minkowski sums](/minkowski-sum/) of the obstacles with the reflected robot.
- **Coverage.** Decide whether the union covers a given region, for example whether $N$ triangles cover a square.

## Examples

All polygons are counterclockwise.

- **Two squares.** $[0,2]^2$ and $[1,3]^2$ overlap in $[1,2]^2$. The union is the octagon $(0,0), (2,0), (2,1), (3,1), (3,3), (1,3), (1,2), (0,2)$ with area $4 + 4 - 1 = 7$ and perimeter 12.
- **A union with a hole.** The U-shape $(0,0), (3,0), (3,3), (2,3), (2,1), (1,1), (1,3), (0,3)$ with area 7 and the strip $[0,3] \times [2,3]$ with area 3 overlap in area 2. Their union is the square $[0,3]^2$ with the hole $[1,2] \times [1,2]$, of area 8: the union of two simple polygons need not be simple.
- **Disjoint pieces.** Adding the square $[4,5] \times [0,1]$ to the two squares above gives a union with two outer contours and area 8.
- **A grid.** Take $g$ rectangles $[0, 2g] \times [2i, 2i + 1]$ and $g$ rectangles $[2j, 2j + 1] \times [0, 2g]$, for $0 \le i, j < g$. Their union is a grid with $(g - 1)^2$ square holes, so its boundary has $\Theta(g^2)$ vertices from $n = 8g$ input vertices.

## Known algorithms

| algorithm | input | time | idea |
| --- | --- | --- | --- |
| repeated two-polygon union | any polygons | depends on intermediate sizes | union with [polygon clipping](/polygon-clipping/) one polygon at a time, or pairwise in a balanced tree |
| plane sweep with winding counts ([Vatti](/vatti-clipping/) and later variants) | any polygons | $O((n + k) \log n)$ for the arrangement of all edges | keep the number of polygons covering each interval of the sweep line; an edge is on the boundary when the count on one side is 0 |
| sweep with a segment tree | axis-parallel rectangles | $O(N \log N)$ for the area | the [area of union of rectangles](/area-of-union-of-rectangles/): the covered length of the sweep line is kept in the tree under insertions and deletions of intervals |
| divide and conquer | pseudo-disks, fat triangles | near-linear | split the set in two, take the two unions recursively, and merge them; fast when unions are small |
| Klee's measure algorithms | boxes in $d$ dimensions | $O(N \log N)$ for $d = 2$, $O(N^{d/2})$ for fixed $d \ge 3$ | see [Klee's measure problem](/klee-measure-problem/) |

The area of the union can also be computed without the boundary, by summing, during the sweep, the covered length times the distance between consecutive events; for polygons with slanted edges the covered part of the sweep line changes linearly between events, so each slab is a union of trapezoids.

## Bounds

- **Worst-case size.** The boundary of the union of polygons with $n$ edges in total has $O(n^2)$ vertices, since each is an input vertex or a crossing of two edges, and the grid example shows $\Omega(n^2)$ even for rectangles. So any algorithm that outputs the boundary needs $\Omega(n^2)$ time in the worst case.
- **Pseudo-disks.** If every two of the polygons have boundaries that cross at most twice, the boundary of the union has at most $6N - 12$ crossing vertices for $N \ge 3$ (Kedem, Livne, Pach and Sharir). Minkowski sums of pairwise disjoint convex polygons with one convex polygon form such a family.
- **Area lower bound.** Computing the length of a union of $N$ intervals takes $\Omega(N \log N)$ time in the linear decision tree model (Fredman and Weide), and in the algebraic decision tree model by Ben-Or's theorem, so the area of a union of rectangles, which contains it as a special case, takes $\Omega(N \log N)$, and the segment-tree sweep is optimal.
- **Coverage.** Deciding whether a union of $N$ triangles covers a given triangle is 3SUM-hard (Gajentaan and Overmars, 1995), so no algorithm much faster than quadratic is expected.

## Reductions

- **Union to clipping.** $P \cup Q$ is a Boolean operation of [polygon clipping](/polygon-clipping/), and the union of $N$ polygons is $N - 1$ of them, at the cost of intermediate results that can be larger than the final one.
- **Area of the union to the boundary.** The [polygon area](/polygon-area/) of the boundary contours, summed with their signs, is the area of the union.
- **Interval union to rectangle union.** Thickening $N$ intervals into rectangles of height 1 turns the union length into a union area, which gives the lower bound above.
- **Free space to union.** Motion planning for a translating polygon reduces to the complement of a union of Minkowski sums, see [configuration space](/configuration-space/).

## Applications

- **GIS.** The dissolve operation merges adjacent parcels or regions with the same attribute into one polygon with holes.
- **Chip layout.** The union of the rectangles on one layer of a circuit gives the actual shapes of metal, used for design rule checks and for extracting connectivity.
- **Robotics.** The forbidden positions of a translating robot form the union of the Minkowski sums of the obstacles with the robot, and the linear bound on their size makes motion planning fast.
- **Coverage problems.** The area covered by sensors, antennas or sprinklers, each modeled by a polygon.
- **Rendering.** Merging overlapping shapes before filling, so that shared parts are not drawn twice.

## References
