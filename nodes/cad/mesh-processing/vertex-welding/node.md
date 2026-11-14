---
tag: 09QVC4
kind: technique
slug: vertex-welding
name: Vertex welding
aliases:
- vertex merging
- duplicate vertex removal
area: cad/mesh-processing
level: intro
summary: Merges vertices that lie within a tolerance of each other, usually with a grid or a k-d tree, so faces that should share edges become connected.
prereqs: [indexed-face-set, uniform-grid, disjoint-set]
see_also: [fixed-radius-near-neighbors, spatial-hashing, kd-tree, mesh-repair-problem, manifold-mesh, hole-filling, consistent-mesh-orientation, mesh-simplification]
sources:
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 12, Geometrical Robustness, Section 12.1, Vertex Welding (the choice of the tolerance, and welding with a grid of cells)
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 8, Model Repair (gaps and duplicate elements in polygon soups)
  - paper: doi:10.1145/2431211.2431214
    title: Marco Attene, Marcel Campen and Leif Kobbelt, Polygon mesh repairing, an application perspective, ACM Computing Surveys 45(2), Article 15, 2013
    locator: the parts on polygon soups, duplicate elements and small gaps
---

Vertex welding merges the vertices of a mesh that lie within a tolerance $\varepsilon$ of each other into one vertex, and rewrites the faces with the new indices. It turns a triangle soup, where each face has its own copy of each corner, into an [indexed face set](/indexed-face-set/) in which neighbouring faces share their vertices and edges. The technique has three parts: a spatial search for close pairs, usually a [uniform grid](/uniform-grid/) with cells of side $\varepsilon$ or a [k-d tree](/kd-tree/), a rule that joins close vertices into classes, usually with a [disjoint-set](/disjoint-set/) structure, and a clean-up that removes the faces that collapse. It is the first step of most [mesh repair](/mesh-repair-problem/) pipelines, because STL files and many exporters write meshes without shared vertices.

## In plain words

A model often arrives as loose tiles, each with its own copy of its corners. Two tiles that should touch have corners at almost the same place, but the computer sees two different points, so it thinks there is a crack between the tiles.

Welding fixes this. Pick a small distance. Any two corners closer than that distance become one corner, and every tile that used either of them now uses the merged one. Then the tiles share their sides again.

To find the close pairs fast, drop each corner into a box of a grid whose boxes are as wide as the distance. Close corners are always in the same box or in boxes that touch, so each corner only needs to look at its own box and its neighbours.

## When it applies

- The input is a polygon soup or a mesh with duplicate vertices: STL files, exports from CAD tools that write each face alone, meshes merged from parts, and the output of [marching cubes](/marching-cubes/) when each cell writes its own vertices.
- The duplicates are closer to each other than to any vertex they should not merge with. There must be a gap between the size of the errors and the size of the smallest real feature. The tolerance goes into that gap.
- The positions of the copies are nearly equal because they come from the same computation or from rounding. If the copies are far apart because of real gaps between parts, welding is the wrong tool, and [hole filling](/hole-filling/) or snapping of borders applies.

## The template

The input is $n$ points $p_0, \ldots, p_{n-1}$, a list of faces over them, and a tolerance $\varepsilon > 0$. Two points are *close* when $|p_i - p_j| \le \varepsilon$. The welded vertices are the classes of the transitive closure of this relation, that is, the connected components of the graph with an edge between each close pair.

```pseudo id=main
WELD(P, F, ε)
L1  for each point i: cell[i] ← (⌊x_i/ε⌋, ⌊y_i/ε⌋, ⌊z_i/ε⌋); add i to the list G[cell[i]]
L2  U ← a disjoint-set structure with the classes {0}, ..., {n − 1}
L3  for each point i, each of the 27 cells c with each coordinate of c − cell[i] in {−1, 0, 1}, each j > i in G[c] do
L4      if |p_i − p_j|² ≤ ε² then UNION(U, i, j)
L5  give each class a new index, and the position of its smallest point
L6  replace each vertex of each face by the new index of its class, and remove consecutive repeats
L7  drop each face that has fewer than 3 vertices or a repeated vertex
L8  return the new points, the new faces, and the edges of the new faces that have 3 or more faces
```

**Why the grid finds every close pair.** If $|x_i - x_j| \le \varepsilon$, then $|x_i/\varepsilon - x_j/\varepsilon| \le 1$, so the floors differ by at most 1. The same holds for $y$ and $z$. So each close pair lies in one cell or in two cells that touch, and line L3 looks at it. The test of line L4 compares squared distances, so with integer or rational coordinates it is exact and needs no square root.

**Why the result is the transitive closure.** Lines L3 and L4 call UNION on every close pair, and only on close pairs. The classes of the disjoint-set structure are then exactly the connected components of the graph of close pairs.

**Cost.** Line L1 takes $O(n)$ expected time with a [hash table](/hash-table/) of the cells, as in [spatial hashing](/spatial-hashing/). Line L3 tests the pairs in neighbouring cells. When each cell holds $O(1)$ points, this is $O(n)$ tests, and the disjoint-set operations add a factor of the inverse Ackermann function. In the worst case, when all points are in a few cells, it is $\Theta(n^2)$ tests, which is also the number of close pairs then. Lines L5 to L8 take time linear in the size of the mesh. This is a [fixed-radius near neighbour](/fixed-radius-near-neighbors/) search followed by [connected components](/connected-components/).

## Classic examples

**A triangle soup of a square.** Two triangles of a unit square, written as a soup with 6 points: $p_0 = (0, 0, 0)$, $p_1 = (1, 0, 0)$, $p_2 = (1, 1, 0)$ for the first triangle, and $p_3 = (10^{-4}, 0, 0)$, $p_4 = (1, 1 + 10^{-4}, 0)$, $p_5 = (0, 1, 0)$ for the second. The copies $p_3$ and $p_4$ have small errors. With $\varepsilon = 10^{-3}$:

| point | cell | close to | class |
|---|---|---|---|
| $p_0$ | $(0, 0, 0)$ | $p_3$ | 0 |
| $p_1$ | $(1000, 0, 0)$ | none | 1 |
| $p_2$ | $(1000, 1000, 0)$ | $p_4$ | 2 |
| $p_3$ | $(0, 0, 0)$ | $p_0$ | 0 |
| $p_4$ | $(1000, 1000, 0)$ | $p_2$ | 2 |
| $p_5$ | $(0, 1000, 0)$ | none | 3 |

The faces $(0, 1, 2)$ and $(3, 4, 5)$ become $(0, 1, 2)$ and $(0, 2, 3)$. They now share the diagonal $\{0, 2\}$, the mesh has 4 vertices, 5 edges and 2 faces, and its Euler characteristic is $4 - 5 + 2 = 1$, a disk. Before welding it was $6 - 6 + 2 = 2$, two separate triangles.

**A cube from an STL file.** An STL cube has 12 triangles and 36 corner points, with each corner of the cube written 3 to 6 times, by the triangles that touch it. Welding with any $\varepsilon$ smaller than the edge length gives the 8 vertices of the cube and a closed [manifold mesh](/manifold-mesh/).

**Marching cubes.** A simple implementation of [marching cubes](/marching-cubes/) writes the vertices of each cell on its own, so each vertex on a grid edge is written by up to four cells. Here the copies are computed by the same formula from the same two samples and are equal, so welding with $\varepsilon = 0$ (exact equality, with a hash map of the positions) is enough.

## Variations

- **Exact welding.** With $\varepsilon = 0$, merge only equal positions, with a hash map from positions to indices. It cannot chain and cannot merge two different points, but it misses copies that differ by rounding.
- **Snap to a grid.** Round each position to the grid of step $\varepsilon$ and merge equal results. This is fast and simple, but two points just across a cell border are not merged however close they are, and two points up to $\varepsilon\sqrt{3}$ apart in one cell are merged.
- **Weld to a kept vertex.** Take the points one at a time. If a point is within $\varepsilon$ of a vertex that is already kept, snap it to that vertex. If not, keep it as a new vertex. Ericson describes welding in this incremental form. A point is never merged with a point that was only close to a snapped point. This avoids chaining, but the result depends on the order of the input.
- **The mean position.** Give each class the mean of its points in place of the first one. The mesh moves less on average, but every face near a merge moves a little.
- **Border welding.** Merge only vertices on border edges, and only with vertices on other borders. This closes cracks between parts and leaves the inside of each part alone.
- **A k-d tree.** For points with very different densities, a [k-d tree](/kd-tree/) gives the close pairs without the choice of a cell size.

## Pitfalls

- **Chaining.** Closeness is not transitive, but the classes are. Points $0, 0.9\varepsilon, 1.8\varepsilon, \ldots$ along a line all merge into one vertex, though the first and the last are far apart. A dense part of the mesh with edges shorter than $\varepsilon$ collapses into one point. Check the diameter of each class, or use a rule that does not chain.
- **A tolerance that is too large.** Thin parts, small holes and short edges vanish. Faces collapse to edges or points, and line L7 drops them. Two sheets that are close but should stay apart become one, and edges with three or more faces appear. The edges of line L8 show where.
- **A tolerance that is too small.** Copies that differ by more than $\varepsilon$ stay apart, and the mesh keeps cracks. A relative tolerance, a small multiple of the size of the model times the machine epsilon, is a common start.
- **Non-manifold results.** Welding can join two parts that only touch, at a vertex or along an edge. The result is not a [manifold mesh](/manifold-mesh/), even if each part was one.
- **Flipped faces.** Welding does not fix the orientation. After welding, faces that were oriented one by one may disagree along their new shared edges. Run [consistent mesh orientation](/consistent-mesh-orientation/) next.
- **Floating point distances.** The test $|p_i - p_j|^2 \le \varepsilon^2$ in floating point can be wrong near the threshold. This only moves the threshold by a rounding error, which is harmless when there is a real gap between the error size and the feature size, and decides nothing when there is not.

## References
