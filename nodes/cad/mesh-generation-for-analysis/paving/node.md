---
tag: AS3MCY
kind: algorithm
slug: paving
name: Paving
aliases:
- Blacker-Stephenson paving
area: cad/mesh-generation-for-analysis
level: core
summary: Blacker and Stephenson's all-quadrilateral mesher that lays rows of quads inward from the boundary and closes the front where rows meet, with good boundary elements.
solves: [mesh-generation]
model: real-ram
complexity:
  vars: {n: the number of front nodes}
  time: {worst: O(n^2)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1991
  people: [Ted D. Blacker, Michael B. Stephenson]
  note: Blacker and Stephenson published paving in 1991, from work at Sandia National Laboratories, as an automatic all-quadrilateral mesher for arbitrary planar regions.
prereqs: [advancing-front-mesh-generation, shoelace-formula, orientation-test]
see_also: [q-morph, blossom-quad, boundary-layer-mesh-generation, structured-grid-generation, laplacian-smoothing, mesh-quality-measures, parametric-surface-meshing, finite-element-method]
sources:
  - paper: doi:10.1002/nme.1620320410
    title: Ted D. Blacker and Michael B. Stephenson, Paving, a new approach to automated quadrilateral mesh generation, International Journal for Numerical Methods in Engineering 32(4), 1991, 811 to 847
    locator: the row by row advance of the front, the classification of front nodes, seaming, row adjustment, intersection of fronts, closure, and smoothing (general locator)
---

Paving is a method that fills a planar region with quadrilaterals only. It starts at the boundary and lays a row of quads along it, then a row along the new inner boundary, and so on, so the mesh grows inward like the rows of stones on a path. Each row follows the shape of the boundary, so the quads near the boundary are well shaped and aligned with it, which is where a finite element solution often needs the most accuracy. Where rows from different sides meet, paving joins the fronts by seaming and closes small remaining holes with fixed patterns, then smooths the mesh. Ted Blacker and Michael Stephenson published it in 1991. There is no proof that paving always succeeds, and no bound on the quality of its quads. This page implements and proves one core step: laying one row.

## In plain words

Picture laying tiles on the floor of an odd shaped room. Lay a row of tiles along every wall first, so the edge of the room looks neat. Then lay a second row along the inside edge of the first row, and so on, moving toward the middle.

At a corner of the room, one tile bends the row around the corner. Along a wall, each tile is about as tall as it is wide. In the middle, rows from opposite walls meet, and the last gaps need special care. Tiles with four sides can only fill a closed loop that has an even number of sides, so the method counts the sides first. The middle is where most bad tiles end up, so the method nudges the tile corners at the end to even them out.

## The problem

The input is a planar region bounded by closed polygons, with nodes on the boundary that have an even total number of edges. The output is a conforming mesh of the region by convex quadrilaterals, using the given boundary nodes, with quads near the boundary that are close to squares and aligned with it. The core step solves a smaller problem: given a closed front, a simple counterclockwise polygon around the empty region, return one row of valid quads along it and the new, smaller front, or report that no row of this kind fits.

## The algorithm

The full method repeats the core step and adds operations for the places where the step fails. The core step classifies each front node by its interior angle. A row end is a sharp corner, which turns the row around; it gets no new node, and one quad covers both of its edges. A row side is a node along a straight or gently curved part; it gets a new node inside the front. This code uses a row end below $135°$ and a row side up to $240°$; these thresholds are parameters of the code, not values from the paper. Paving has more node types, row corners and row reversals, for reflex nodes.

```pseudo id=main
PAVE-ROW(front x_0..x_{n−1})
L1  classify each node as a row end or a row side by its interior angle; fail on other nodes
L2  for each row end c: q_c ← x_{c−1} + x_{c+1} − x_c, the new node of both neighbours
L3  for each other row side i: y_i ← the point inside at distance h_i from both edge lines at x_i, h_i ← mean length of the two edges
L4  make one quad (x_{c−1}, x_c, x_{c+1}, q_c) per row end and one quad (x_i, x_{i+1}, y_{i+1}, y_i) per other edge
L5  the new front ← the new nodes in front order, each q_c once
L6  if some quad is not strictly convex and counterclockwise then fail
L7  if the new front is not simple or not counterclockwise then fail
L8  return the quads and the new front
```

L6 and L7 use exact [orientation tests](/orientation-test/) on the float coordinates, converted to fractions without rounding. The full method runs PAVE-ROW until the front is small, and between rows it smooths the nodes, adds or removes nodes to keep the quads close to square (row adjustment), joins front nodes across sharp angles and narrow gaps (seaming), detects fronts that cross each other and splits them, and closes the last small fronts with fixed patterns.

## Example

Take the square $[0,4]^2$ with 16 boundary nodes at unit spacing. The four corners have interior angle $90°$ and are row ends; the other 12 nodes are row sides, with $h = 1$ and new nodes one unit inside. The corner $(0,0)$ gives the quad $(0,1), (0,0), (1,0), (1,1)$ in front order. The row has 12 unit squares, exactly the outer ring of the $4 \times 4$ grid, and the new front is the square $[1,3]^2$ with 8 nodes. A second row fails: on that small square, the row ends are only 2 nodes apart, so their quads would share an edge. A closure rule fills it with 4 squares.

For the rectangle $[0,6] \times [0,3]$, the row has 14 quads and leaves the strip $[1,5] \times [1,2]$ with 10 nodes, which is one row of 4 quads that closure must fill. For a round front of 16 nodes on a circle of radius 3, every node is a row side, since the interior angle is $157.5°$. The edges have length $1.1705$, the new nodes lie on a circle of radius $1.8065$, the area inside the front falls from $27.553$ to $9.991$, and a second row succeeds as well.

| front | quads in the row | nodes of the new front | next row |
|---|---|---|---|
| square $[0,4]^2$ | 12 | 8 | fails: row ends too close |
| rectangle $6 \times 3$ | 14 | 10 | fails: row ends too close |
| square $[0,7]^2$ | 24 | 20 | succeeds, 16 quads |
| circle, 16 nodes | 16 | 16 | succeeds |

## Correctness

The proof file has two results. The first is the parity rule: in any quad mesh, each quad has 4 edge sides, interior edges have two and boundary edges one, so $4Q = 2E_\text{int} + E_\text{bnd}$ and the boundary has an even number of edges. Paving therefore makes the boundary count even before it starts. The row step keeps the parity: each row end removes its own node and merges two new nodes, so the new front has $n - 2e$ nodes for $e$ row ends.

The second result is that an accepted row is a valid mesh of the band between the two fronts. The boundaries of the quads add up to the old front minus the new front, because each radial edge appears in two neighbouring quads with opposite directions. So the winding numbers add up the same way. If every quad is strictly convex and both fronts are simple and counterclockwise, each point of the band lies in exactly one quad, and the areas add up exactly. The code tests every hypothesis exactly, so it never returns an invalid row.

What is not proved: that a row exists, that paving as a whole closes every front, and any bound on the quality of the quads. These are measured, case by case.

## Complexity

The row step costs $O(n)$ for the classification, the new nodes and the quads, and $O(n^2)$ for the exact test that the new front is simple. A sweep line or a grid of buckets brings the test down for typical fronts. Paving as a whole meshes a region with $N$ quads in a number of rows that is about the ratio of the region width to the element size. The intersection tests between fronts dominate in practice, and implementations use spatial search structures for them.

## Properties

- **All quads.** The output has no triangles, when closure succeeds.
- **Boundary aligned.** The rows follow the boundary, so the quads near it are close to squares and aligned with it.
- **Parity.** Every front must have an even number of edges, a hard rule for any all-quad mesh.
- **No guarantee.** No bound on angles or on success is proved; the irregular nodes collect where the fronts meet.
- **Row step proved.** An accepted row is a valid mesh of its band, with exact checks.

## Variants and improvements

- **Plastering.** Blacker and Meyers extended the idea to 3D, filling a volume with hexahedra layer by layer. Closing the fronts is much harder in 3D, and plastering is not robust in general.
- **Q-Morph.** Owen and coauthors run the same kind of advancing front of quads over an existing triangle mesh, which makes the closure and the intersection tests easier; see [Q-Morph](/q-morph/).
- **Blossom-Quad.** An indirect method that pairs the triangles of a triangle mesh into quads by a perfect matching; see [Blossom-Quad](/blossom-quad/).
- **Surface paving.** Paving on a CAD face runs in the parameter plane with the surface metric; see [surface meshing in parametric space](/parametric-surface-meshing/).
- **Size fields.** The row height can follow a size field instead of the local edge length, for graded meshes.

## When to use it

Use paving when an all-quad mesh is needed on a planar region or a CAD face, with good elements along the boundary, for example for structural analysis with the [finite element method](/finite-element-method/), where boundary stresses matter. For a simple region that maps to a rectangle, a [structured grid](/structured-grid-generation/) is better. For large meshes or complex regions, an indirect method such as Q-Morph or Blossom-Quad is often more robust, because the triangle mesh already solves the hard global problem.

## Pitfalls

- **Odd boundary count.** A front with an odd number of edges cannot be meshed by quads at all. Fix the count before meshing.
- **Colliding rows.** Rows from opposite sides of a narrow region cross. Test the new front for self intersection, as in L7, and seam or split the front.
- **Sharp corners.** Without row ends at sharp corners, the row quads there fold. Classify the nodes.
- **Poor interior.** The irregular nodes all end up where the fronts meet, often with poor quads. Smooth the mesh, and accept that the interior is worse than the boundary.
- **Float tests.** Front intersection with float tests can miss a touch and leave overlapping quads. Use exact tests.

## Implementations

## History

Ted Blacker and Michael Stephenson published paving in the International Journal for Numerical Methods in Engineering in 1991, from work at Sandia National Laboratories, where it went into the CUBIT mesh generation toolkit. Before paving, all-quad meshes of general regions were mostly made by splitting the region into four-sided blocks by hand and meshing each block with a structured grid, or by splitting triangles into quads. Paving was among the first methods to produce well shaped all-quad meshes of arbitrary planar regions automatically. Plastering, its 3D extension to hexahedra, followed in the early 1990s, and Q-Morph moved the advancing front of quads onto a triangle mesh in 1999.

## References
