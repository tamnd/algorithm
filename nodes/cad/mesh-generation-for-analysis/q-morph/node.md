---
tag: D6Y61V
kind: algorithm
slug: q-morph
name: Q-Morph
aliases:
- Owen Q-Morph
area: cad/mesh-generation-for-analysis
level: advanced
summary: Owen's quadrilateral mesher that converts a triangle mesh by an advancing front of quads that merge triangles and recover edges, giving all-quad meshes.
solves: [mesh-generation]
model: real-ram
complexity:
  vars: {n: the number of triangles, f: the number of flips in the recovery of the top edge}
  time: {worst: O(f n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1999
  people: [Steven J. Owen, Matthew L. Staten, Scott A. Canann, Sunil Saigal]
  note: Owen, Staten, Canann and Saigal published Q-Morph in 1999 as an indirect advancing front quad mesher that works on top of an existing triangle mesh.
prereqs: [advancing-front-mesh-generation, edge-flip, depth-first-search]
see_also: [paving, blossom-quad, lawson-flip-algorithm, constrained-delaunay-triangulation, laplacian-smoothing, mesh-quality-measures, delaunay-triangulation, finite-element-method]
sources:
  - paper: doi:10.1002/(SICI)1097-0207(19990330)44:9<1317::AID-NME532>3.0.CO;2-N
    title: Steven J. Owen, Matthew L. Staten, Scott A. Canann and Sunil Saigal, Q-Morph, an indirect approach to advancing front quad meshing, International Journal for Numerical Methods in Engineering 44(9), 1999, 1317 to 1340
    locator: the front edge states, side edge definition, top edge recovery, quad formation, smoothing and seaming (general locator)
---

Q-Morph is a method that turns a triangle mesh into a mesh of quadrilaterals. It works like [paving](/paving/): a front moves inward from the boundary, and each step puts a new quad on one front edge. The difference is that Q-Morph does not place new nodes in empty space. It starts from a valid triangle mesh, picks two existing edges as the sides of the new quad, makes the top edge appear in the mesh by flipping triangle edges, and then merges all triangles inside the quad into it. Because the triangle mesh always covers the rest of the region, Q-Morph never has to test whether two fronts cross, which is the hardest part of paving. Steven Owen and his coauthors published it in 1999. It gives quads aligned with the boundary, but there is no proof that it always closes the front and no bound on the quality of the quads. This page implements and proves one core step.

## In plain words

Start with a floor that is fully covered by triangular tiles. You want square tiles instead. Begin at a wall. Take one tile edge on the wall, and look for the two tile edges that go away from the wall at its ends, as straight as you can find. Join their far ends with a new line, moving tile edges around until that line is a tile edge too. Now the triangles between the wall and the new line make one four sided tile, so glue them together.

Do this along the whole wall, then along the new line of four sided tiles, and so on. The floor is always fully covered, partly by four sided tiles and partly by triangles, so the work never leaves a gap. At the end, the corners of the new tiles are nudged to make them more even.

## The problem

The input is a conforming triangle mesh of a planar region whose boundary has an even number of edges. The output is a conforming mesh of the same region by convex quads, aligned with the boundary. The core step solves a smaller problem: given a conforming triangle mesh with exact coordinates and an edge $a \to b$ with a triangle on its left, return a strictly convex quad $(a, b, d, c)$ and the triangles that remain after the triangles inside the quad are removed, so that the quad and the remaining triangles form a conforming mesh of the same region; or report that the step fails.

## The algorithm

The full method keeps a front of edges, starting with the boundary edges of the triangle mesh. Each front edge has a state that records whether the neighbouring front edges at its ends make sharp corners. At a sharp corner, the neighbouring front edge itself becomes a side of the quad. Otherwise, the side is the mesh edge at that end that is closest to the ideal direction, the bisector of the front angle. If no edge is close, Q-Morph swaps an edge or splits one to make a better side. This code uses only the second rule, with the inward normal of $ab$ as the ideal direction, which is the bisector when the front is straight.

```pseudo id=main
QMORPH-STEP(T, a → b)
L1  c ← the neighbour of a for which the edge ac is closest in angle to the inward normal of ab
L2  d ← the neighbour of b for which the edge bd is closest in angle to the inward normal of ab
L3  if c = d then fail
L4  if the quad (a, b, d, c) is not strictly convex and counterclockwise then fail
L5  if a vertex lies on the segment cd then fail; X ← the edges of T that cross cd
L6  while X is not empty: flip an edge of X whose two triangles form a convex quad, first one whose new edge does not cross cd; update X
L7  S ← the triangles reached from the triangle left of ab without crossing the four sides of the quad
L8  if the area of S is not the area of the quad then fail
L9  remove the triangles of S from T, with the vertices inside the quad
L10 return the quad (a, b, d, c)
```

All tests use exact [orientation tests](/orientation-test/). L5 and L6 are the recovery of the top edge by [edge flips](/edge-flip/). The search in L7 is a [depth first search](/depth-first-search/) over the triangles. After the step, the full method adds the new quad to the front: $ab$ leaves the front, and the sides and the top edge join it where they are not shared with an earlier quad. Between rows, it smooths the nodes, and at the end it closes small loops of the front with fixed patterns.

## Example

Take the points $a = (0, 0)$, $b = (2, 0)$, $c = (-\tfrac12, 2)$, $d = (\tfrac52, 2)$, $p = (1, \tfrac32)$ and $e = (1, 3)$, with the five triangles $abp$, $apc$, $bdp$, $cpe$ and $pde$. The front edge is $ab$, and its inward normal points up. At $a$, the edge to $p$ is $33.7°$ from the normal and the edge to $c$ is $14.0°$, so the side is $ac$. At $b$, the side is $bd$ for the same reason. The quad $(a, b, d, c)$ is a trapezoid with area 5, strictly convex.

The top edge $cd$ is not in the mesh: the segment $y = 2$ crosses the edge $pe$. The triangles $cpe$ and $pde$ form a convex quad, so one flip replaces $pe$ by $cd$, with the triangles $cpd$ and $dec$. The search starts at $abp$ and reaches $apc$, $bdp$ and $cpd$ without crossing the quad sides. The four triangles have areas $1.5$, $1.375$, $1.375$ and $0.75$, which add up to 5, the area of the quad. They are removed, together with the inner vertex $p$, and the mesh is now the quad $(a, b, d, c)$ and the triangle $dec$. The quad has angles of $104.0°$ at $a$ and $b$ and $76.0°$ at $c$ and $d$.

On random meshes of jittered grids, scrambled by 300 random flips, 97 of 128 steps on boundary edges succeeded, and 44 of them needed between 1 and 5 flips to recover the top edge.

## Correctness

The proof file shows two results. The first is the parity rule: each quad has 4 edge sides, so $4Q = 2E_\text{int} + E_\text{bnd}$, and a region can have an all-quad mesh only if its boundary has an even number of edges. Q-Morph needs the same parity on every front loop.

The second is that an accepted step gives a conforming mesh. Each flip keeps a conforming mesh of the same region. The flips touch only edges that cross the open segment $cd$, so the three sides $ab$, $bd$ and $ca$ survive, and after recovery all four sides of the quad are mesh edges. A triangle cannot cross a mesh edge, so each triangle is inside the quad or outside it. The search reaches only triangles inside, and the area check proves that they cover the quad. Replacing them by the quad keeps every other directed edge, so the result is conforming, with the same boundary and the same area. The tests check the area exactly, the conformity, the presence of the top edge, and that the merged triangles are exactly those whose centroid is inside the quad.

Not proved: that a flippable crossing edge always exists during recovery (the code reports a failure if not, and this never happened in the tests), that Q-Morph closes every front, and any bound on the angles of the quads.

## Complexity

In this simple code, each flip rebuilds the edge map, so recovery costs $O(f n)$ for $f$ flips, and the search costs $O(n)$. With an adjacency structure, a flip costs $O(1)$, and the step costs $O(f + k)$ for $k$ triangles inside the quad, plus the cost to find the crossing edges along $cd$. Each flip removes at most one crossing edge, so $f$ is at least the number of edges that cross $cd$. Q-Morph as a whole makes about one quad for every two triangles, and the local work per quad is small, so the total cost is close to linear in the number of triangles in practice.

## Properties

- **Indirect.** Q-Morph needs a triangle mesh first, but any valid triangle mesh will do, often a [Delaunay triangulation](/delaunay-triangulation/).
- **Always covered.** The region is covered by quads and triangles after every step, so there are no front crossing tests.
- **Boundary aligned.** The rows of quads follow the boundary, as in paving.
- **Parity.** The boundary must have an even number of edges for an all-quad result.
- **No guarantee.** No bound on angles and no proof of success are known; quality depends on side edge choice and smoothing.
- **Step proved.** An accepted step is a conforming mesh, with exact checks.

## Variants and improvements

- **Side edge swaps and splits.** When no mesh edge is close to the ideal direction, Q-Morph swaps an edge or splits one, which this code does not do.
- **Smoothing.** Q-Morph smooths the new quad nodes and the nearby triangle nodes as the front moves; see [Laplacian smoothing](/laplacian-smoothing/).
- **Blossom-Quad.** Pairs the triangles into quads all at once by a minimum cost perfect matching, instead of a front; see [Blossom-Quad](/blossom-quad/).
- **Hex meshing.** Owen and Saigal extended the idea to hexahedra over a tetrahedral mesh (H-Morph), which is harder to make robust.
- **Constrained recovery.** The top edge recovery is the same operation as edge insertion in a [constrained Delaunay triangulation](/constrained-delaunay-triangulation/).

## When to use it

Use Q-Morph when you need an all-quad mesh of a planar region or a CAD face with quads aligned with the boundary, and a good triangle mesher is already available. It is often more robust than direct paving, because the triangle mesh solves the global problem of covering the region. If boundary alignment is less important than speed and global quality, Blossom-Quad is an alternative. For a region that maps to a rectangle, a structured grid is better than both.

## Pitfalls

- **Odd boundary count.** A front loop with an odd number of edges cannot end with quads only. Fix the count first, or accept one triangle.
- **Lost side edges.** Recovery must never flip a side of the quad. Flip only edges that cross the open segment $cd$; the sides share an end with it or lie opposite it.
- **Vertex on the top edge.** If a vertex lies on $cd$, no flips can make $cd$ an edge. Test for it before the flips.
- **Holes.** If the quad covers a hole of the region, the search fills only part of it. Compare the areas, as in L8.
- **Float tests.** Crossing tests in floats can miss a touch and leave a crossed edge. Use exact tests.
- **Poor quads.** The closest mesh edge can still be far from the ideal direction. Swap or split, and smooth.

## Implementations

## History

Steven Owen, Matthew Staten, Scott Canann and Sunil Saigal published Q-Morph in the International Journal for Numerical Methods in Engineering in 1999. Paving, published in 1991, made good all-quad meshes, but its tests for crossing fronts were slow and fragile. Earlier indirect methods merged pairs of triangles into quads and split the rest, which gave poor alignment with the boundary. Q-Morph joined the two ideas: it moves a paving front over a triangle mesh, so the front never needs to test for crossings. It is still a standard reference method for indirect quad meshing.

## References
