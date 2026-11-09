---
tag: AJX07P
kind: definition
slug: ear
name: Ear of a polygon
aliases:
- Ear vertex
- polygon ear
area: geometry/triangulations
level: intro
summary: A vertex whose two neighbours form a diagonal lying inside the polygon.
prereqs: [simple-polygon, orientation-test]
see_also: [two-ears-theorem, ear-clipping, polygon-triangulation, triangulation-dual-tree, convex-polygon, art-gallery-theorem]
sources:
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Section 1.2, Triangulation, Theory (diagonals, ears and Meisters' two ears theorem) and Section 1.6 (the ear test in code)
  - paper: "Gary H. Meisters, Polygons have ears, American Mathematical Monthly 82(6), 648 to 651 (1975)"
    locator: the definition of an ear and the two ears theorem
  - paper: "Godfried T. Toussaint, Anthropomorphic polygons, American Mathematical Monthly 98(1), 31 to 35 (1991)"
    locator: ears and mouths, and polygons with exactly two ears
---

An ear of a [simple polygon](/simple-polygon/) is a vertex $v$ such that the segment joining the two neighbors of $v$ is a diagonal: it lies inside the polygon and touches the boundary only at its two end points. Cutting along that diagonal removes a triangle and leaves a simple polygon with one vertex fewer. Ears are the basis of the [two ears theorem](/two-ears-theorem/) and of [ear clipping](/ear-clipping/).

## Definition

Let $P$ be a simple polygon with vertices $v_0, \ldots, v_{n-1}$ in counterclockwise order, indices mod $n$, and $n \ge 4$. A **diagonal** of $P$ is a segment $v_i v_j$ between two vertices whose relative interior (the segment without its end points) lies in the interior of $P$. The vertex $v_i$ is an **ear** of $P$ if $v_{i-1} v_{i+1}$ is a diagonal. The triangle $v_{i-1} v_i v_{i+1}$ is then the **ear triangle**, and $v_i$ is its tip.

Two ears are **non-overlapping** if their ear triangles have disjoint interiors.

An equivalent test uses only the [orientation test](/orientation-test/). The vertex $v_i$ is an ear if and only if

$$\mathrm{orient}(v_{i-1}, v_i, v_{i+1}) > 0 \quad\text{and no vertex } v_k,\ k \notin \{i-1, i, i+1\}, \text{ lies in the closed triangle } v_{i-1} v_i v_{i+1}.$$

The proof of this equivalence is Lemma 1 of the [ear clipping correctness proof](/ear-clipping/). For a clockwise polygon, reverse the sign of the first condition.

Conventions:

- A triangle ($n = 3$) has no diagonal, so by this definition it has no ears. Some authors call all three of its vertices ears; this page does not.
- An ear tip is a *strictly* convex vertex: its interior angle is less than $\pi$. A vertex with an angle of exactly $\pi$ is never an ear.
- A **mouth** (Toussaint) is a reflex vertex $v_i$ whose segment $v_{i-1} v_{i+1}$ lies outside $P$ except for its end points.

## Examples and non-examples

Take the notched rectangle $v_0 = (0,0)$, $v_1 = (6,0)$, $v_2 = (6,4)$, $v_3 = (4,4)$, $v_4 = (3,1)$, $v_5 = (2,4)$, $v_6 = (0,4)$, in counterclockwise order.

| vertex | $\mathrm{orient}(v_{i-1}, v_i, v_{i+1})$ | vertices in the closed triangle | ear? |
|---|---|---|---|
| $v_0 = (0,0)$ | 24 | $v_4$ | no |
| $v_1 = (6,0)$ | 24 | $v_4$ | no |
| $v_2 = (6,4)$ | 8 | none | yes |
| $v_3 = (4,4)$ | 6 | none | yes |
| $v_4 = (3,1)$ | $-6$ | (reflex) | no |
| $v_5 = (2,4)$ | 6 | none | yes |
| $v_6 = (0,4)$ | 8 | none | yes |

- **Convex but not an ear.** The corners $v_0$ and $v_1$ are convex, but the segment from $v_6$ to $v_1$ passes above the reflex vertex $v_4$ and leaves the polygon. So convexity alone is not enough.
- **Reflex vertex.** $v_4$ is not an ear, and it is a mouth: the segment from $v_3$ to $v_5$ runs along the top through the notch, outside the polygon.
- **Convex polygon.** In a convex polygon with $n \ge 4$ vertices and no three collinear, every vertex is an ear.
- **A vertex on the cut.** In the polygon $(0,0), (1,0), (2,0), (1,2)$, the apex $(1,2)$ is convex and no vertex lies inside its triangle, but $(1,0)$ lies on the segment from $(2,0)$ to $(0,0)$. So the apex is not an ear. The ears are $(0,0)$ and $(2,0)$.
- **Exactly two ears.** A polygon can have only two ears; Toussaint calls such polygons anthropomorphic. A long zigzag strip whose triangulation is a path has two ears, one at each end.

## Related definitions

- [Simple polygon](/simple-polygon/): the polygons on which ears are defined.
- [Two ears theorem](/two-ears-theorem/): every simple polygon with $n \ge 4$ vertices has at least two non-overlapping ears.
- [Ear clipping](/ear-clipping/): triangulation by removing ears one at a time.
- [Dual tree of a triangulation](/triangulation-dual-tree/): the ears of a triangulation are the leaves of its dual tree.
- [Polygon triangulation](/polygon-triangulation/): a partition of a polygon into triangles by diagonals.
- [Convex polygon](/convex-polygon/): a polygon in which every strictly convex vertex is an ear.

## References
