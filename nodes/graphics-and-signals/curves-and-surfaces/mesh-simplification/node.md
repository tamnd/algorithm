---
tag: R4Q6NE
kind: problem
slug: mesh-simplification
name: Mesh simplification
aliases:
- polygon mesh decimation
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Given a triangle mesh and a target size or error bound, build a mesh with fewer faces that stays close to it, usually in Hausdorff distance. Finding the smallest one is NP-hard.
prereqs: [polygon-mesh, hausdorff-distance]
see_also: [quadric-error-metrics, curve-simplification, polygon-simplification, surface-reconstruction, isosurface-extraction, subdivision-surface, np-hard, set-cover]
sources:
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, A K Peters, 2010
    locator: Chapter 7, Simplification and Approximation, from page 111 (vertex clustering, incremental decimation, shape approximation and out-of-core methods)
  - paper: doi:10.1145/142920.134010
    title: William J. Schroeder, Jonathan A. Zarge and William E. Lorensen, Decimation of triangle meshes, Computer Graphics (SIGGRAPH 92 Proceedings) 26(2), 65 to 70, 1992
    locator: the whole paper (vertex removal by a distance or angle test, and the filling of the hole)
  - paper: doi:10.1145/258734.258849
    title: Michael Garland and Paul S. Heckbert, Surface simplification using quadric error metrics, Proceedings of SIGGRAPH 97, 209 to 216, 1997
    locator: the whole paper (pair contraction ordered by a quadric error, and the comparison with earlier methods)
  - paper: "Pankaj K. Agarwal and Subhash Suri, Surface approximation and geometric partitions, SIAM Journal on Computing 27(4), 1016 to 1035, 1998"
    locator: the NP-hardness of the minimum size approximation of a terrain within a given error, and the algorithm with O(c log c) vertices
---

Mesh simplification is the problem of replacing a [polygon mesh](/polygon-mesh/) by one with far fewer faces that has nearly the same shape. Scanners, [surface reconstruction](/surface-reconstruction/) and [isosurface extraction](/isosurface-extraction/) give meshes with millions of triangles, many more than a display or a simulation needs. The goal is either a target number of faces with the smallest error, or a given error bound with the fewest faces; the error is usually measured by the [Hausdorff distance](/hausdorff-distance/) between the two surfaces. Finding the smallest mesh within a given error is NP-hard even for terrains. The methods in use are greedy and local, such as edge collapse ordered by [quadric error metrics](/quadric-error-metrics/), and they have no worst case guarantee on how close their result is to the best possible one. Their quality is measured by experiment.

## In plain words

You have a model made of a million small triangles, and you want one made of ten thousand that looks almost the same. Flat parts need only a few big triangles. Curved parts and sharp edges need more.

The usual method is to make the mesh smaller one small step at a time. A step joins the two ends of one edge into one point, and the triangles next to that edge go away. Before each step, you compute how much the surface would move, and you always do the step that moves it least. You stop at the target size.

This is fast and gives good models. But each step only looks at a small part of the mesh, so nothing proves that the result is the best one of that size.

## Definition

**Input.** A triangle mesh $M$ with $n$ vertices, usually a 2-manifold, and either a target number $k$ of faces (or vertices) or an error bound $\varepsilon > 0$. Some inputs also have attributes at the vertices, such as colors, normals and texture coordinates.

**Output.** A triangle mesh $M'$ such that one of these holds:

1. **Size given.** $M'$ has at most $k$ faces, and the error $d(M, M')$ is as small as possible.
2. **Error given.** $d(M, M') \le \varepsilon$, and $M'$ has as few faces as possible.

**Error measures.** The usual measure is the Hausdorff distance
$$d_H(M, M') = \max\Big(\max_{x \in M} \min_{y \in M'} \lVert x - y \rVert,\ \max_{y \in M'} \min_{x \in M} \lVert x - y \rVert\Big).$$
The two one-sided terms differ, and methods that measure only the distance from the old vertices to the new surface can miss the error in the other direction. A mean squared distance is also used. For terrains, the vertical distance between two height functions is a simpler measure. Methods often optimize a cheaper proxy, such as the sum of squared distances to the planes of the original faces in [quadric error metrics](/quadric-error-metrics/), which is not the Hausdorff distance.

**Topology.** Most applications ask that $M'$ have the same topology as $M$: it is still a 2-manifold, with the same genus and the same number of border loops, so the Euler characteristic $\chi = V - E + F$ does not change. Other applications allow the genus to drop, which removes small holes and handles, or allow separate parts to merge.

## Variants

- **Topology preserving or not.** Edge collapse with a link test keeps the topology; vertex clustering and pair contraction of vertices that are close but not joined by an edge can change it.
- **Attributes.** The error includes the change in colors, normals and texture coordinates, and seams in the texture must stay in place.
- **Progressive meshes.** The sequence of collapses is stored, so that the inverse steps, vertex splits, rebuild any size between the coarse mesh and the original. This allows transmission of a coarse mesh first.
- **View dependent detail.** The size is chosen per region from the distance to the viewer and the screen error, and changes each frame.
- **Discrete levels of detail.** A small number of meshes at fixed sizes, such as one half, one quarter and one eighth of the faces, switched by distance.
- **Out of core.** The mesh does not fit in memory, so the method must read it in one or few passes, as vertex clustering on a [uniform grid](/uniform-grid/) can.
- **Shape approximation.** The output faces are large planar regions fitted to the surface, rather than triangles from collapses.
- **Curves.** The same problem one dimension lower is [curve simplification](/curve-simplification/), and for closed curves [polygon simplification](/polygon-simplification/).

## Examples

**One edge collapse.** In a closed triangle mesh, collapsing an inner edge $\{u, v\}$ to one vertex removes the vertex $v$, the edge $\{u, v\}$, the two triangles on it, and two more edges that merge with others: $V$ drops by 1, $E$ by 3 and $F$ by 2, so $\chi$ does not change. The step is safe only if the link test holds, that is, the vertices joined to both $u$ and $v$ are exactly the two opposite vertices of the two triangles. If a third vertex is joined to both, the collapse makes two triangles with the same three vertices, or an edge in more than two faces.

**A flat grid.** A square divided into a $k \times k$ grid of squares, each split into 2 triangles, has $V = (k + 1)^2$, $F = 2 k^2$ and $\chi = 1$, a disk. All of it is in one plane, so the error of any collapse that keeps the corners and moves vertices along the plane is 0, and the mesh simplifies to 2 triangles on the 4 corners: $4 - 5 + 2 = 1$.

**A cube.** A cube with each face split into a $4 \times 4$ grid of squares and each square into 2 triangles has $V = 98$, $E = 288$, $F = 192$ and $\chi = 2$. Quadric error metrics reduces it to the 12 triangles of the plain cube, $8 - 18 + 12 = 2$, with zero error and the vertices at the 8 corners; the page of that method tests this case.

**How small can it get.** If the topology is kept and the output is a triangulation in which two triangles share at most one edge, then $E \le V (V - 1) / 2$. A closed mesh of genus $g$ has $E = 3V - 6 + 6g$, so
$$V \ge \frac{7 + \sqrt{1 + 48 g}}{2}.$$
For a sphere this gives 4, the tetrahedron, and for a torus 7, which the 7-vertex torus with 14 triangles attains. No topology preserving method can go below these sizes, whatever the error.

## Known algorithms

- **Vertex decimation.** Schroeder, Zarge and Lorensen, 1992: remove a vertex whose distance to the average plane of its neighbors, or whose edge angle, is under a threshold, and triangulate the hole. Repeat in passes.
- **Vertex clustering.** Put a grid over the mesh, merge all vertices in each cell into one, and drop the triangles that become degenerate. It takes one pass and $O(n)$ time, handles any input, and changes the topology. Each vertex moves by at most the cell diagonal, but the face count is hard to control. An [octree](/octree/) gives an adaptive version.
- **Edge collapse with [quadric error metrics](/quadric-error-metrics/).** Garland and Heckbert, 1997: give each vertex a $4 \times 4$ matrix that sums the squared distances to the planes of its faces, collapse the edge whose merged quadric has the smallest minimum, and keep the candidates in a [priority queue](/priority-queue/). With a link test it keeps the topology.
- **Mesh optimization and progressive meshes.** Hoppe and coauthors minimize an energy of distance and size over collapses, swaps and splits, and store the collapse sequence for progressive transmission.
- **Shape approximation.** Partition the faces into regions that are each near a plane, then build one polygon per region.
- **Approximation for terrains.** Agarwal and Suri give a polynomial time method for terrains that uses at most $O(c \log c)$ vertices, where $c$ is the size of the best approximation within the error bound, by a reduction to a geometric covering problem, a special [set cover](/set-cover/).

## Bounds

**Hardness.** Agarwal and Suri proved that the decision version, whether a terrain can be approximated within a vertical error $\varepsilon$ with at most $k$ vertices, is NP-complete. So the optimal problems above are [NP-hard](/np-hard/) already for height functions, and unless P = NP there is no polynomial time exact method.

**No guarantee for greedy methods.** The methods in use, vertex decimation, vertex clustering and edge collapse by quadric error, are [greedy](/greedy-algorithm/): each step is the best local step, and steps are not undone. There is no proof that their result is within any factor of the optimal size for a given error, or of the optimal error for a given size. Also, the quadric cost is a proxy, and the true Hausdorff error of the result can be larger than the sum of the costs suggests. In practice, they give good results, and the error is measured after the run.

**Time.** Any method must read the input, so $\Omega(n)$ time is needed. Vertex clustering takes $O(n)$. Edge collapse with a binary heap takes $O(n \log n)$ when the vertex degrees stay bounded during the run, with $O(\log n)$ per heap update and $O(1)$ local work per collapse. The terrain approximation of Agarwal and Suri is polynomial but of high degree, $O(n^8)$, and is of theoretical interest.

## Reductions

- **Analog of curve simplification.** One dimension lower, the problem is [curve simplification](/curve-simplification/). There the smallest subchain within a given error is a shortest path in a graph of the allowed shortcuts, so it is found in polynomial time. For surfaces no such order of the vertices exists, and the problem becomes NP-hard.
- **To set cover.** For terrains, choosing triangles that each fit the points under them within $\varepsilon$, and that together cover the domain, is a covering problem, which gives the $O(c \log c)$ bound above.
- **To a priority queue of local operations.** The greedy methods are a loop over a [priority queue](/priority-queue/) of candidate collapses or removals, updated in the neighborhood of each step, often with [lazy deletion](/lazy-deletion/) of old entries.
- **Inverse of refinement.** A [subdivision surface](/subdivision-surface/) goes from coarse to fine; simplification goes from fine to coarse, and a progressive mesh stores both directions.

## Applications

- **Real time rendering and games.** Several levels of detail of each model, chosen by distance, keep the number of triangles per frame low.
- **Transmission and streaming.** Progressive meshes send a coarse model first and refine it as data arrives.
- **Scanning and reconstruction.** Reconstructed and extracted surfaces are reduced to a size that tools can edit and store.
- **Simulation.** A coarse mesh for collision detection or for a finite element solve where the fine detail is not needed.
- **3D printing and CAD.** Smaller files with a known bound on the deviation from the design.

## References
