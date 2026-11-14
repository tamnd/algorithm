---
tag: 5S30QB
kind: algorithm
slug: volumetric-mesh-repair
name: Volumetric mesh repair
aliases:
- Ju polygon repair
area: cad/mesh-processing
level: advanced
summary: Ju's repair that scan-converts a polygon soup into an octree grid, fixes the signs of the grid points by parity, and contours a closed surface that separates inside from outside.
solves: [mesh-repair-problem]
model: real-ram
complexity:
  vars: {s: the number of input polygons or segments, k: the number of crossings of the input with grid edges, g: the number of grid cells, b: the number of odd cells before patching}
  time: {worst: O(s + k + b·g)}
  space: {extra: Θ(g + k)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2004
  people: [Tao Ju]
  note: Ju presented the method at SIGGRAPH 2004 and released it as the program PolyMender.
prereqs: [mesh-repair-problem, marching-cubes, octree]
see_also: [dual-contouring, marching-squares, simulation-of-simplicity, generalized-winding-number, hole-filling, liepa-hole-filling, poisson-surface-reconstruction, point-in-polygon]
sources:
  - paper: doi:10.1145/1015706.1015815
    title: Tao Ju, Robust repair of polygonal models, ACM Transactions on Graphics 23(3), 2004, 888 to 895 (SIGGRAPH 2004)
    locator: the four steps (scan conversion of the polygons into an octree with the parity of each cell edge, patching of the boundary cycles of the dual surface, sign generation, and contouring)
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 8, Model Repair (volumetric repair, and its comparison with surface-based repair)
  - paper: doi:10.1145/2431211.2431214
    title: Marco Attene, Marcel Campen and Leif Kobbelt, Polygon mesh repairing, an application perspective, ACM Computing Surveys 45(2), Article 15, 2013
    locator: the global, volumetric methods of repair and their effect on the input geometry
---

Volumetric mesh repair, as Tao Ju gave it in 2004, turns a polygon soup into a closed surface. The soup can have gaps, holes, overlaps, double faces, dangling pieces and self-intersections. The method does not try to fix the polygons one by one. It puts a grid around them, an [octree](/octree/) in 3D, and marks each grid edge that crosses the polygons an odd number of times. In a closed model, the marked edges are exactly the edges between an inside and an outside grid point. A defect leaves cells where the marks are not consistent, and the method changes a small set of marks there, so that the inside and outside become defined. A search then gives each grid point a sign, and [marching cubes](/marching-cubes/) or [dual contouring](/dual-contouring/) contours a surface between the signs. The result is a closed surface that separates inside from outside, for every input. The code on this page is the same method in the plane, on a square grid, where every step can be tested exactly. The method solves the [mesh repair problem](/mesh-repair-problem/) for the condition of a closed, oriented surface, at the cost of a resampled surface everywhere.

## In plain words

Lay a fine net of points over the broken model. Each short line of the net either crosses the model's skin an odd number of times or not. If the skin were whole, the odd lines would be exactly the lines that go from inside to outside, and you could colour every net point as inside or outside without a contradiction.

A gap in the skin breaks this. Around the gap, a small square of the net has an odd number of odd lines, which no colouring can explain. Such squares come in pairs. Join each pair by the shortest chain of squares and flip the lines along the chain: this paints in a bit of skin across the gap.

Now colour the points by walking out from a corner that is surely outside. Finally, draw the new skin between inside and outside points. It is always closed.

## The problem

The input is a list of polygons in space, with no promise about their connections: a polygon soup, as read from an STL file. The output is a closed, oriented surface that is near the input where the input is good, and that bounds a solid: every point off the surface is inside or outside, and the inside is on the side of the [right-hand rule](/consistent-mesh-orientation/) normals. The problem statement and the other conditions of a valid mesh are on the [mesh repair problem](/mesh-repair-problem/) page.

In the plane, the input is a list of segments, and the output is a set of closed polygons that do not cross, with the inside on the left of each segment.

## The algorithm

The grid has cell size $h$ and a margin of one cell around the input. In the plane, the grid points sit at $(X_i + \varepsilon, Y_j + \varepsilon^2)$ for a symbolic $\varepsilon > 0$, in the manner of [simulation of simplicity](/simulation-of-simplicity/), so no grid point lies on a segment and each crossing of a segment with the grid lines falls on exactly one grid edge.

```pseudo id=main
VOLUMETRIC-REPAIR(S, h)
L1  G ← a grid of cell size h around S, with a margin of one cell
L2  for each segment of S, for each grid edge e that it crosses: toggle mark(e)
L3  B ← the cells with an odd number of marked edges
L4  while B is not empty: take c ∈ B, and find by breadth-first search over the cells the nearest d ∈ B \ {c}
L5      toggle mark(e) for each edge e between two consecutive cells of the path from c to d; remove c and d from B
L6  sign(corner) ← outside; by breadth-first search over the grid edges, sign(w) ← sign(v) xor mark(vw)
L7  for each cell: join the midpoints of its marked edges by marching squares, with the inside on the left
L8  return the segments of line L7
```

**In 3D.** Ju's method has the same four steps on an octree. Line L2 scan-converts each polygon into the cells it meets, and stores the parity of the crossings on each cell edge, refining the octree only near the polygons. The marked edges define a *dual surface*: one quad for each marked edge, made of the four cells around it. For a closed input, this dual surface is closed. A defect leaves *boundary cycles*: loops of cell faces on the border of the dual surface, at the grid faces with an odd number of marked edges. Lines L4 and L5 become the patching step, which finds a small patch of the dual grid for each boundary cycle and toggles the edges under the patch. Line L6 is the same [flood fill](/flood-fill/) over the grid points. Line L7 is [marching cubes](/marching-cubes/) on the signs, or [dual contouring](/dual-contouring/), which also uses the crossing points and the polygon normals stored in line L2 to keep sharp edges.

**The predicate and its failure.** Line L2 is a crossing test of a segment with a grid edge, which is two [orientation tests](/orientation-test/) in the plane, and a segment-triangle test in 3D. With floating point coordinates, a segment that passes very near a grid point is a sign test of a nearly zero value, and [catastrophic cancellation](/catastrophic-cancellation/) can give it the wrong sign. Then the crossing is put on two edges, or on none. This is not a small error: the cell next to that grid point gets an odd number of marked edges, so line L4 sees a gap where the input has none, and patches it, or it pairs this cell with a real gap far away and cuts a strip through the model. The fix is to make the test exact. The code uses rational coordinates and the symbolic perturbation above, so each crossing falls on exactly one edge, and the tests check the result against an exact crossing test of every segment with every perturbed grid edge.

## Example

The input is three sides of the square $[1, 4] \times [1, 4]$, with $h = 1$: the segments $(1, 1) \to (4, 1)$, $(4, 1) \to (4, 4)$ and $(1, 4) \to (1, 1)$. The top side is missing.

1. **Grid.** Line L1 makes the grid $[0, 5] \times [0, 5]$ with 25 cells. The grid point $(i, j)$ sits at $(i + \varepsilon, j + \varepsilon^2)$.
2. **Scan conversion.** The bottom side crosses the vertical edges at $x = 1 + \varepsilon$, $2 + \varepsilon$ and $3 + \varepsilon$ just below $y = 1 + \varepsilon^2$, the right side crosses three horizontal edges at $x = 4$, and the left side three at $x = 1$. So 9 edges are marked.
3. **Odd cells.** Each cell is even except the two cells at the free ends: the cell $(0, 3)$, with the corner $(1, 4)$, and the cell $(3, 3)$, with the corner $(4, 4)$. Each has one marked edge.
4. **Patching.** The shortest path of cells from $(0, 3)$ to $(3, 3)$ runs along the row $y \in [3, 4]$. Line L5 toggles its three vertical edges at $x = 3, 2, 1$, which closes the gap one cell below the missing side. Now 12 edges are marked, and every cell is even.
5. **Signs.** The search from the corner $(0, 0)$ gives the inside to the 9 grid points $(i, j)$ with $1 \le i, j \le 3$.
6. **Contour.** Marching squares gives 12 segments through the midpoints of the 12 marked edges, for example from $(0.5, 1)$ to $(1, 0.5)$ in the corner cell, with the inside point $(1, 1)$ on its left, which make one closed polygon around the 9 inside points.

The result is a closed curve, but the closing is not where the missing side was: it follows the grid one cell lower, because the grid point $(i, 4)$ is outside of the three given sides. With a smaller $h$, the closing moves closer to the line $y = 4$.

## Correctness

The proofs below are for the method in the plane, which the code follows. The 3D method rests on the same parity arguments, and Ju's paper argues them there.

- **Each crossing falls on one edge.** Under the perturbation, no grid point lies on a segment, and each crossing is assigned to exactly one edge. Because of the margin, no outer edge is marked.
- **Odd cells come in pairs, and patching makes every cell even.** Each marked edge lies on two cells, so the number of odd cells is even. Toggling the edges along a path of cells changes the parity of its two end cells only.
- **The signs exist, and they are unique up to complement.** If every cell is even, every cycle of the grid crosses an even number of marked edges, since the cell boundaries generate the cycles. So the signs from the search are consistent on every edge, and the corner fixes them. The outer ring is outside.
- **A closed input keeps its inside.** If every end point of the segments has even degree, as for any set of closed polygons, there are no odd cells, and each grid point gets its [even-odd](/point-in-polygon/) value with respect to the input. So on good input, the method changes nothing but the sampling.
- **The output is closed and separates the signs.** Each output vertex starts one segment and ends one, two segments meet only at shared end points, and the even-odd value of the output at each grid point is its sign.

The tests check each of these by brute force: the scan conversion against an exact test of all segment and edge pairs, the signs against even-odd ray casting, and the uniqueness against all $2^{16}$ sign vectors of a small grid. What is not proved is how good the patch is. The shortest path is one choice among many, and the patch it gives is a guess at the missing surface, as in any [hole filling](/hole-filling/).

## Complexity

With a walk along each segment through the cells it meets, line L2 takes $O(s + k)$ time, where $k$ is the number of crossings. Each search of line L4 takes $O(g)$ time in the worst case, and there are $b / 2$ of them, so patching takes $O(b \cdot g)$. In practice the pairs are close, and each search stops after a few cells. Lines L6 and L7 take $\Theta(g)$ time. The marks and signs take $\Theta(g)$ space. The code scans every grid line for each segment, which costs $O(s \cdot (n_x + n_y))$ for an $n_x \times n_y$ grid, simpler and enough for the tests.

In 3D, an octree that is fine only near the polygons keeps $g$ near the surface area of the model divided by $h^2$, in place of the volume divided by $h^3$. This is what makes the method practical for large scans.

## Properties

- **Always closed.** For every input, the output is a closed surface that separates inside from outside. This holds by construction, for any defects.
- **Not always a manifold.** The guarantee is a closed, separating surface. Whether it is also a manifold depends on the contouring: marching squares with a fixed rule for the saddle cells gives disjoint closed curves, as the code shows, but in 3D a cell that touches the surface in several pieces can give a non-manifold vertex or edge with plain dual contouring.
- **Resamples everything.** The output is a new surface at the resolution $h$. Thin parts below about $h$ can vanish or merge, small features are lost, and the polygons of the input are not kept.
- **Robust to the defects of the input.** Overlaps cancel in pairs, since two copies of a polygon toggle the same marks twice, and dangling pieces only add odd cells that patching pairs.
- **Deterministic.** Ties in the searches follow a fixed order of the neighbours.
- **Not exact geometry.** The signs are exact under the perturbation, but the output is an approximation of the input surface at the resolution $h$.

## Variants and improvements

- **Dual contouring with Hermite data.** Storing the crossing points and normals on the marked edges lets [dual contouring](/dual-contouring/) place the output vertices on the sharp edges and corners of a CAD model.
- **Signs from a winding number.** In place of parity patching, the sign of each grid point can come from the [generalized winding number](/generalized-winding-number/) of the soup, which is robust to gaps and gives a smooth inside measure. Thresholding it, then contouring, is another volumetric repair.
- **Reconstruction from points.** [Poisson surface reconstruction](/poisson-surface-reconstruction/) ignores the connections altogether and fits an indicator function to points with normals. It gives a watertight surface too, but it needs good normals.
- **Different patch choices.** Ju chooses small patches for the boundary cycles, and the code takes shortest paths. Any set of paths that pairs the odd cells makes the signs consistent, so other rules give other closings of a large gap, with the same guarantee.
- **Space carving and distance fields.** A [signed distance function](/signed-distance-function/) computed from the soup, with a sign from ray casting or visibility, is the older form of volumetric repair. It fails when the soup has large gaps, because the sign is then not defined.

## When to use it

Use it when the input is badly broken and a closed solid is required: for 3D printing, for [slicing for additive manufacturing](/slicing-for-additive-manufacturing/), for finite element meshing, or for collision tests. It handles any soup, including models where surface-based repair gives up. Do not use it when the input polygons must be kept, when the model has features thinner than the cell size you can afford, or when there is only one small hole in a good mesh: then a surface-based method such as [Liepa hole filling](/liepa-hole-filling/) keeps the rest of the mesh as it is.

## Pitfalls

- **Cell size too coarse.** Thin walls and narrow gaps close up, and small handles vanish. Pick $h$ below the thinnest part that must survive.
- **Cell size too fine.** A gap wider than a few cells needs a patch that is large in the grid, and the patching can choose a closing that a human would not. Fix large gaps before, or use a coarser grid there.
- **Floating point scan conversion.** A crossing near a grid point that is counted twice or not at all makes a false odd cell, which patching then joins to another odd cell. Use an exact or perturbed crossing test.
- **Open sheets.** A single open sheet, such as a terrain or a facade, is all boundary. The method closes it into a thin slab or cuts it off along the grid, which is seldom the wanted result.
- **Nested shells.** Two shells, one inside the other, give a hollow solid by parity. This is right for a thick-walled part, but wrong if the inner shell was a duplicate by mistake.
- **Measuring the change.** The output differs from the input everywhere. Measure the difference, for example with the [Hausdorff distance](/hausdorff-distance/) or a [Metro comparison](/metro-mesh-comparison/), before trusting it.

## Implementations

## History

Volumetric methods for repairing scans and models used signed distance fields and space carving in the 1990s, but they needed a well-defined inside, which a broken model does not have. In 2004 Tao Ju observed that the parity of the crossings on each grid edge is defined for any soup, and that its defects show up as boundary cycles that can be patched on the grid. His program PolyMender made the method widely used for repairing models for printing and simulation. Later work, such as the generalized winding number, gave other ways to define the inside of a broken model.

## References
