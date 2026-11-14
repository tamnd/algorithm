---
tag: BWP73E
kind: problem
slug: hole-filling
name: Mesh hole filling
aliases:
- mesh hole closing
area: cad/mesh-processing
level: core
summary: Given a mesh and a loop of its border edges, add a patch of triangles that closes the loop and fits the surface around it, as a step of mesh repair and scan completion.
prereqs: [manifold-mesh, polygon-triangulation]
see_also: [liepa-hole-filling, volumetric-mesh-repair, mesh-repair-problem, min-weight-triangulation, polygon-triangulation-dp, catalan-triangulation-theorem, image-inpainting, implicit-fairing]
sources:
  - paper: doi:10.2312/SGP/SGP03/200-206
    title: Peter Liepa, Filling holes in meshes, Eurographics Symposium on Geometry Processing, 2003, 200 to 206
    locator: the statement of the problem for oriented manifold meshes and its four steps (identify the border, triangulate, refine, fair)
  - paper: doi:10.1016/0167-8396(94)00011-G
    title: Gill Barequet and Micha Sharir, Filling gaps in the boundary of a polyhedron, Computer Aided Geometric Design 12(2), 1995, 207 to 229
    locator: the gaps bounded by edges with one face, and their triangulation of least weight
  - paper: doi:10.1016/S0925-7721(98)00005-4
    title: Gill Barequet, Matthew Dickerson and David Eppstein, On triangulating three-dimensional polygons, Computational Geometry 10(3), 1998, 155 to 170
    locator: the main theorem (deciding whether a polygon in space has a triangulation without self-intersections is NP-complete)
  - paper: doi:10.1145/2431211.2431214
    title: Marco Attene, Marcel Campen and Leif Kobbelt, Polygon mesh repairing, an application perspective, ACM Computing Surveys 45(2), Article 15, 2013
    locator: the parts on holes as a type of defect and on the methods that fill them
---

Mesh hole filling asks for new triangles that close a hole of a surface mesh. The input is an oriented [manifold mesh](/manifold-mesh/) and a loop of its border edges, the edges with only one face, and the output is a patch whose border is that loop, so that after gluing the loop edges have two faces each. Holes come from scanners that cannot see part of an object, from parts that a user deleted, and from CAD exports with missing faces. The true surface in the hole is unknown, so the problem only becomes precise when a measure of quality is fixed, such as the area of the patch, the angles at its seam, or how smooth it is. Without new vertices, a loop of $n$ vertices has as many patches as a convex polygon has [triangulations](/catalan-triangulation-theorem/), the Catalan number $C_{n-2}$. Image inpainting fills missing pixels of a picture; this page fills missing surface of a mesh.

## In plain words

A scanned statue often has holes where the scanner could not look, such as under the chin or inside an ear. Around each hole, a ring of edges belongs to only one triangle. That ring is the edge of the hole.

The task is to sew a patch of new triangles onto that ring, so that the surface is closed again. The patch must join the ring without gaps, face the same way as the rest of the surface, and not cut through itself or through the old surface.

Many patches are possible, and none of them is the true one, because the data is missing. So a method must choose a patch that looks right: small, smooth, and with triangles of the same size as their neighbours.

## Definition

**Input.** A triangle mesh $M$ that is an oriented manifold mesh with border, given as an [indexed face set](/indexed-face-set/) with exact vertex positions. A *border loop* is a cycle $v_0, v_1, \ldots, v_{n-1}$ of border edges, each $\{v_i, v_{i+1}\}$ with indices mod $n$. A *hole* is a border loop that the user, or a rule, marks to be closed. Not every border loop is a hole: the rim of a cup or the outline of a sheet is meant to be there.

**Output.** A patch $P$: a set of triangles, and possibly new vertices with their positions, such that:

1. **Border.** The border of $P$ is the loop, and the union $M \cup P$ is a manifold mesh in which the edges of the loop are inner edges.
2. **Orientation.** Each edge of the loop is used by $P$ in the direction opposite to its face in $M$, so the orientation of $M$ extends to $P$. The outward normal follows the right-hand rule on both sides of the seam.
3. **Topology.** In the usual form, $P$ is a disk. Then filling a hole lowers the number of border loops $b$ by 1, and by $\chi = V - E + F = 2 - 2g - b$ the Euler characteristic of the mesh goes up by 1.
4. **Embedding.** $P$ does not intersect itself, and it meets $M$ only along the loop. This is [mesh self-intersection](/mesh-self-intersection/) freedom of $M \cup P$.

**Objective.** A weight to make small. Common ones are the total area of $P$, the largest dihedral angle between two neighbouring triangles of $P$ or across the seam, and a fairness energy of the positions of the new vertices, which measures bending. Some forms also ask that the triangles of $P$ have about the same edge length as the triangles of $M$ near the loop.

**The combinatorial form.** If $P$ may use only the loop vertices, it is a triangulation of the loop: $n - 2$ triangles over the loop vertices whose edges are the $n$ loop edges and $n - 3$ diagonals that do not cross in the order of the loop. These patches are in one-to-one correspondence with the triangulations of a convex $n$-gon, so there are $C_{n-2}$ of them, for example 2 for $n = 4$, 14 for $n = 6$ and 132 for $n = 8$.

**Degeneracies are part of the input.** A loop can pass a vertex twice when two holes touch at one vertex, three loop vertices can be collinear, and a loop can be flat, which makes many patches tie on area. A hole can contain an island, a part of the mesh with its own border loop, and then the patch is not a disk.

## Variants

- **With or without new vertices.** The combinatorial form keeps only the loop vertices. The usual form adds vertices inside the patch, so that its triangles match the size of the triangles around the hole.
- **Order of smoothness.** The patch may only close the hole (a joint of order 0), or it may also match the normals at the seam (order 1), or the curvature (order 2). The order picks the fairness energy: membrane, thin plate, or a higher one.
- **Holes with islands.** The missing region contains a part of the surface. The patch must join two or more loops, and its topology is no longer a disk.
- **All holes at once.** For a watertight result in one step, as for 3D printing, all border loops are closed together, sometimes by a volumetric method that rebuilds the whole surface near the holes.
- **Gaps between parts.** In CAD data, a hole is often a thin slot between two parts that should touch. Barequet and Sharir treat these gaps, which are long and narrow, and closing them by moving vertices is a different task from filling a large hole.
- **Holes with context.** In scan completion, the patch may copy shape detail from other parts of the model, or from a database of models.

## Examples

**A hole in a plane.** Remove the two triangles of a square from a flat grid mesh. The loop has $n = 4$ vertices, and the $C_2 = 2$ patches are the two diagonals of the square. Both are flat, with the same area, and both fill the hole exactly. The weight has a tie, and a rule must break it.

**A skew loop.** Take the loop $p_0 = (0, 0, 0)$, $p_1 = (1, 0, 0)$, $p_2 = (1, 1, 0)$, $p_3 = (0, 1, 1)$. The two patches give the areas:

| diagonal | triangles | areas | total |
|---|---|---|---|
| $\{0, 2\}$ | $(0, 1, 2)$, $(0, 2, 3)$ | $1/2$, $\sqrt{3}/2$ | $\approx 1.366$ |
| $\{1, 3\}$ | $(0, 1, 3)$, $(1, 2, 3)$ | $\sqrt{2}/2$, $\sqrt{2}/2$ | $\approx 1.414$ |

The diagonal $\{0, 2\}$ gives the smaller area. Each area is half the length of the [cross product](/cross-product/) of two edge vectors, for example $(1, 1, 0) \times (0, 1, 1) = (1, -1, 1)$ for the triangle $(0, 2, 3)$.

**An open box.** A cube of 12 triangles with the 2 triangles of one face removed has one loop of 4 vertices. It has $V = 8$, $E = 17$ (the 18 edges of the cube less the diagonal of the removed face) and $F = 10$, so $\chi = 8 - 17 + 10 = 1$, a disk. Both patches close it to a cube surface with $\chi = 2$.

**A knotted loop.** If the loop is knotted in space, such as a trefoil, no embedded disk has it as its border, with or without new vertices. Every embedded patch must then have genus at least 1. This is why the definition must allow failure, or a patch that is not a disk.

## Known algorithms

| method | guarantee | time |
|---|---|---|
| exhaustive search over all triangulations of the loop | optimal for any weight in the combinatorial form | $\Theta(C_{n-2})$, about $4^n$ |
| dynamic program over the loop ([polygon triangulation DP](/polygon-triangulation-dp/)), Barequet and Sharir | optimal in the combinatorial form for a weight that is a sum over triangles; embedding not guaranteed | $O(n^3)$ time, $O(n^2)$ space |
| [Liepa hole filling](/liepa-hole-filling/): the dynamic program with the largest dihedral angle and the area, then refinement and fairing | the triangulation step is a heuristic for its weight, which is not monotone; the refinement and the fairing are heuristics, judged by measurement | $O(n^3)$ for the triangulation, and the cost of a sparse solve for the fairing |
| advancing front: add triangles at the sharpest angle of the loop until it closes | none; measured | about linear in the size of the patch |
| [volumetric mesh repair](/volumetric-mesh-repair/): rebuild the surface from a grid of inside and outside signs | a closed surface; the shape in the hole is a guess | linear in the number of grid cells |
| [surface reconstruction](/surface-reconstruction/) from the vertices, for example [Poisson surface reconstruction](/poisson-surface-reconstruction/) | a watertight surface; the whole model moves a little | a sparse solve on an octree |

All methods in the table choose a patch for a weight or a rule that they fix. None of them can recover a missing surface that the data does not show, so results beyond the stated weights are measured, on scans with holes cut into known surfaces.

## Bounds

- **Count.** The combinatorial form has exactly $C_{n-2} = \frac{1}{n-1}\binom{2n-4}{n-2}$ patches, so exhaustive search is exponential.
- **Optimal triangulation.** For a weight that is a sum or a maximum over the triangles, the best triangulation of the loop takes $O(n^3)$ time and $O(n^2)$ space. This is proved, by the same argument as for polygons in the plane. For a lexicographic pair of a maximum and a sum, one pass of the program with the pair can miss the optimum; a first pass finds the least maximum $w^*$, and a second pass minimizes the sum over the triangles whose first part is at most $w^*$, within the same bounds.
- **Embedding is hard.** Barequet, Dickerson and Eppstein proved that deciding whether a polygon in space has a triangulation, with its own vertices, that does not intersect itself is NP-complete. So the dynamic program cannot also promise an embedded patch in polynomial time, unless P = NP, and the optimal embedded patch is at least as hard.
- **Topology.** A loop bounds an embedded disk in space, if the rest of the mesh is ignored, if and only if it is not knotted. With an island or a knotted loop, no disk patch exists.

## Reductions

- **To optimal polygon triangulation.** The combinatorial form with a weight that adds up over triangles is the [optimal polygon triangulation](/optimal-polygon-triangulation/) problem on the abstract convex polygon $v_0, \ldots, v_{n-1}$, with the weight of each triangle given by the positions in space.
- **Not the plane problem.** It differs from the [minimum weight triangulation](/min-weight-triangulation/) of a point set in the plane, which is NP-hard. Here the loop fixes the order of the vertices, and that order makes the dynamic program possible.
- **From triangulability.** The NP-complete problem of Barequet, Dickerson and Eppstein is the special case with the embedding constraint and no objective.
- **Into mesh repair.** Hole filling is one step of [mesh repair](/mesh-repair-problem/), after the vertices are welded and the faces are oriented.

## Applications

- **Scan completion.** Range scans and photogrammetry leave holes where the sensor had no view. Filling them gives a closed model for display and measurement.
- **3D printing.** Slicing needs a closed surface. Each hole makes the inside of a layer unclear.
- **CAD data exchange.** Gaps between faces after a translation between file formats give holes and slots in the mesh.
- **Editing.** After a user cuts away a part of a mesh, the cut is filled to make the surface closed again.
- **Cultural heritage.** Scans of broken statues and sherds get patches that are marked as added, so that the restored shape and the measured shape stay apart.

## References
