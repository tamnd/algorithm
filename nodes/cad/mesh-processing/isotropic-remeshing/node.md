---
tag: 0E9HMJ
kind: algorithm
slug: isotropic-remeshing
name: Isotropic remeshing
aliases:
- incremental remeshing
- Botsch-Kobbelt remeshing
area: cad/mesh-processing
level: core
summary: Makes a mesh with nearly equal edges and good angles by repeating edge splits, collapses, flips toward valence six and tangential smoothing.
model: real-ram
complexity:
  vars: {n: the largest number of vertices during the run, k: the number of rounds}
  time: {worst: O(k n² log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2004
  people: [Mario Botsch, Leif Kobbelt]
  note: Botsch and Kobbelt reduced remeshing to a short loop of four local operators with the thresholds 4/3 and 4/5 of the target length, in their work on remeshing for multiresolution modeling.
prereqs: [polygon-mesh, manifold-mesh, edge-flip, laplacian-smoothing]
see_also: [delaunay-refinement, mesh-simplification, quadric-error-metrics, lawson-flip-algorithm, ruppert-algorithm, taubin-smoothing, doubly-connected-edge-list, metro-mesh-comparison]
sources:
  - paper: doi:10.2312/SGP/SGP04/189-196
    title: Mario Botsch and Leif Kobbelt, A remeshing approach to multiresolution modeling, Eurographics Symposium on Geometry Processing (SGP), 2004, 189 to 196
    locator: the remeshing loop of splits, collapses, flips and tangential relaxation, with the thresholds 4/3 and 4/5 of the target edge length
  - paper: doi:10.1090/S0025-5718-1975-0375068-5
    title: Ivo G. Rosenberg and Frank Stenger, A lower bound on the angles of triangles constructed by bisecting the longest side, Mathematics of Computation 29(130), 1975, 390 to 395
    locator: the theorem that repeated longest-side bisection keeps every angle at least half the smallest angle of the first triangle
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 6, Remeshing (incremental isotropic remeshing and the local operators)
---

Isotropic remeshing turns a triangle mesh with triangles of all sizes and shapes into one whose edges are all close to a target length $L$ and whose triangles are close to equilateral, while the surface stays the same up to a small error. It repeats a short loop of four local steps. It splits every edge longer than $\frac{4}{3}L$ and collapses every edge shorter than $\frac{4}{5}L$. It flips edges so that the valences move toward 6. Then it moves each vertex toward the centroid of its neighbours, inside its tangent plane, and projects it back onto the input surface. Each step only changes a few triangles at a time, so the method is simple to write on a [half-edge structure](/doubly-connected-edge-list/), and a few rounds are enough.

## In plain words

A scanned or converted mesh often has long thin triangles next to tiny ones. Many later steps, such as smoothing, simulation or computing distances, work badly on such triangles. Remeshing replaces them by triangles of one size and a nice shape, on the same surface.

The method keeps a goal length in mind and repeats four simple fixes. If an edge is too long, cut it in the middle. If an edge is too short, shrink it to a point, which merges its two ends. If a corner has too many or too few edges around it, turn an edge in a four-sided patch the other way, so that the corners move toward six edges each. Finally, nudge every corner toward the middle of its neighbours, but only along the surface, and put it back on the surface. After a few rounds, all edges are about the goal length.

## The problem

The input is a manifold triangle mesh, a target edge length $L > 0$, a number of rounds $k$, and optionally a projection onto a reference surface, usually the input mesh itself. The output is a manifold triangle mesh with the same topology, the same border curve, edge lengths mostly in $[\frac{4}{5}L, \frac{4}{3}L]$, angles near $60°$ and valences near 6 (4 on the border). This is a quality goal, not an optimization with a unique answer. The page proves what each step keeps and measures the final quality.

## The algorithm

The *valence excess* of a set of vertices is $\sum_v |\operatorname{val}(v) - t(v)|$ with $t(v) = 6$ for an inner vertex and $4$ for a border vertex.

```pseudo id=main
ISOTROPIC-REMESH(mesh, L, k, project)
L1  for r ← 1 to k do
L2      while the longest edge uv has |uv| > 4L/3 do split uv at its midpoint
L3      for each edge uv with |uv| < 4L/5 do collapse uv to its midpoint if it is safe
L4      while some inner edge uv has a legal flip that lowers the valence excess of its four vertices do flip uv
L5      for each inner vertex v do x_v ← project(x_v + (I − n_v n_vᵀ)(c_v − x_v))
L6  return the mesh
```

**Split** (line L2). The edge $uv$ with faces $(u, v, c)$ and $(v, u, d)$ gets a new vertex $m$ at its midpoint, and the faces become $(u, m, c)$, $(m, v, c)$, $(v, m, d)$, $(m, u, d)$. A border edge has one face and gets two. The code always splits the longest edge, from a priority queue.

**Collapse** (line L3). Vertex $v$ is merged into $u$ at the midpoint, and the two faces of $uv$ vanish. The code allows it only if the collapse is *safe*. Neither $u$ nor $v$ may be a border vertex. The *link condition* must hold: the common neighbours of $u$ and $v$ are exactly $c$ and $d$. Both $c$ and $d$ must have valence at least 4. No edge at the new vertex may be longer than $\frac{4}{3}L$. No remaining face may turn its normal by $90°$ or more.

**Flip** (line L4). The faces $(u, v, c)$ and $(v, u, d)$ become $(u, d, c)$ and $(d, v, c)$, as in an [edge flip](/edge-flip/). A flip is *legal* if $uv$ is not a border edge, $cd$ is not already an edge, $u$ and $v$ have valence at least 4, and neither new face folds over the old pair. It is made only if it lowers the valence excess of $u, v, c, d$, where $u, v$ lose one edge and $c, d$ gain one.

**Relaxation** (line L5). $c_v$ is the centroid of the neighbours of $v$ and $n_v$ the unit normal, the normalized sum of the face normals. The move is the tangential part of the [Laplacian smoothing](/laplacian-smoothing/) step with factor 1, so the vertices spread evenly without shrinking the shape, and the projection puts them back on the surface.

## Example

**The split phase on a square.** Take the unit square as two triangles, cut by the diagonal from $(0, 0)$ to $(1, 1)$, with $L = \frac{1}{2}$, so the split threshold is $\frac{2}{3}$. The longest edge is the diagonal, $\sqrt{2}$. Splitting it at $(\frac{1}{2}, \frac{1}{2})$ gives four triangles, with four sides of length 1 and four half-diagonals of length $\frac{\sqrt{2}}{2} \approx 0.707$. The sides are now the longest. Each is split at its midpoint, which adds a spoke of length $\frac{1}{2}$ to the center. Then the half-diagonals, $0.707 > \frac{2}{3}$, are the longest, and each is split, for example at $(\frac{1}{4}, \frac{1}{4})$, with new edges of length $\frac{\sqrt{2}}{4} \approx 0.354$. After these 9 splits the mesh has 13 vertices and 16 faces, and every edge has length $\frac{1}{2}$ or $\frac{\sqrt{2}}{4}$. The tests check these counts.

**A noisy sphere.** Take the icosphere with 162 vertices, move each vertex by up to $0.025$ in each coordinate and put it back on the unit sphere. Then remesh with $L = 0.15$, half the input edge length, for 5 rounds, with projection onto the sphere. The measured result has 619 vertices, a mean edge length of $1.021L$, $99.5$ percent of the edges in $[\frac{4}{5}L, \frac{4}{3}L]$, 563 of the 619 vertices of valence 6, and a smallest angle of $41°$, against $44°$ in the noisy input at twice the edge length. The Euler characteristic stays 2.

**A rectangle of thin triangles.** An $8 \times 4$ rectangle cut into 32 triangles of size $4 \times \frac{1}{2}$ has a smallest angle of $7.1°$. Five rounds with $L = \frac{1}{2}$ give 164 vertices, 102 of the 116 inner vertices of valence 6, and a measured smallest angle of $27.4°$. The area stays exactly $32$, the corners stay, and every border edge lies on a side of the rectangle.

## Correctness

These are proved in the correctness file:

- **The split loop stops, and then every edge is at most $\frac{4}{3}L$.** The loop splits the longest edge, which is the longest edge of both its faces, so every split is a longest-side bisection. By the theorem of Rosenberg and Stenger, every triangle made in this way has all its angles at least half the smallest angle of the input. So a triangle with an edge longer than $\frac{4}{3}L$ has area at least a fixed amount, and a counting argument bounds the number of splits.
- **Splits keep the surface.** A midpoint lies on the old edge, so the new faces cover exactly the old ones, with the same area.
- **The collapse loop stops and keeps the bound.** Each collapse removes a vertex. The guard keeps every edge at most $\frac{4}{3}L$.
- **The flip loop stops at a local optimum.** Each flip lowers the integer valence excess of the whole mesh by at least 1. When it stops, no legal flip lowers the excess, which the tests check by a scan of all edges.
- **The mesh stays a manifold with the same topology.** Splits and flips keep a manifold with the same Euler characteristic. A collapse under the link condition, away from the border, also keeps the manifold and the Euler characteristic. The tests recompute the topology from scratch after random operations.
- **The border stays.** No border vertex moves, no border edge is collapsed or flipped, and a split of a border edge puts the new vertex on that edge.

The upper bound $\frac{4}{3}L$ holds after line L3, but flips and relaxation can create longer edges. Edges shorter than $\frac{4}{5}L$ can remain where a collapse is not safe. So the final length distribution, the angles and the valences are only measured, as in the examples.

## Complexity

With a half-edge structure, or the edge and face maps of the code, each local operator costs $O(d)$ time for the valences $d$ involved, which is $O(1)$ on a mesh of bounded valence. Assume bounded valence. In one round, line L2 makes at most $n$ splits, each with a priority queue operation of $O(\log n)$, and line L5 takes $O(n)$ time plus the cost of the projection. Lines L3 and L4 sweep the sorted edge list, $O(n \log n)$ per sweep, until a sweep changes nothing. Every sweep but the last makes a collapse or a flip, and the proofs bound these by $n$ collapses and by the valence excess, which is $O(n)$, flips. This gives the worst case $O(k n^2 \log n)$. In the measured runs the loops end after a few sweeps, so a round costs about $O(n \log n)$ in practice. Projection onto the input mesh needs a spatial search structure, about $O(\log n)$ per query. In practice $k = 5$ to $10$ rounds are used. The extra space is $\Theta(n)$.

## Properties

- **Local and simple.** Four operators and two thresholds.
- **The thresholds fit together.** $\frac{4}{3}L$ and $\frac{4}{5}L$ are chosen so that splitting an edge just above $\frac{4}{3}L$ gives halves above $\frac{2}{3}L$, and the guard of line L3 keeps a collapse from making an edge longer than the split threshold, so no collapse is undone by a split. The converse does not hold: the halves of an edge shorter than $\frac{8}{5}L$ are shorter than $\frac{4}{5}L$, so a collapse can still undo a split.
- **Uniform, not adaptive.** All edges aim at one length. Fine details smaller than $L$ are lost, and flat regions get as many triangles as curved ones.
- **Topology is kept.** The Euler characteristic, the number of border loops and the orientation stay.
- **Not exact.** The midpoints, normals and projections use floating point.

## Variants and improvements

- **Adaptive remeshing.** Make $L$ depend on the position, smaller where the curvature is high, so that the error stays the same with fewer triangles.
- **Feature edges.** Mark sharp edges and corners, and never collapse or flip across them. Relax feature vertices only along the feature curve.
- **Area-weighted relaxation.** Use the centroid of the neighbours weighted by the areas of their faces, which spreads the vertices according to the area.
- **Delaunay flips.** Flip toward the intrinsic Delaunay condition, the angles opposite each edge summing to at most $\pi$, as in the [Lawson flip algorithm](/lawson-flip-algorithm/), instead of toward valence 6.
- **Quadric collapses.** For coarsening only, collapse by the [quadric error metric](/quadric-error-metrics/) of [mesh simplification](/mesh-simplification/), which keeps the shape better than midpoint collapses.
- **Global methods.** Centroidal Voronoi tessellations and parameterization-based remeshers optimize the vertex positions as a whole, at a higher cost.

## When to use it

Use it to clean a mesh before simulation, smoothing, parameterization or geodesic computations, all of which need well-shaped triangles, and to bring a scanned or converted mesh to a known resolution. Several mesh libraries include it. For planar domains with guaranteed angle bounds, use [Delaunay refinement](/delaunay-refinement/), such as [Ruppert's algorithm](/ruppert-algorithm/). To reduce the triangle count while keeping the shape, use [mesh simplification](/mesh-simplification/). To measure how far the result is from the input, use [Metro](/metro-mesh-comparison/).

## Pitfalls

- **No projection.** Without line L5's projection, the tangential moves still drift off a curved surface, and the shape slowly changes.
- **Unsafe collapses.** A collapse without the link condition can glue two sheets together, or make a vertex whose star is not a disk.
- **Collapsing into long edges.** Without the $\frac{4}{3}L$ guard, a collapse can make edges that the next round splits again, and the loop does not settle.
- **Moving the border.** Relaxing border vertices like inner ones pulls the border inward.
- **Features.** Sharp edges are rounded unless they are marked and kept.
- **A target too large.** If $L$ is larger than the size of a thin part, collapses close it up or the link condition blocks them, and the mesh stays poor there.

## Implementations

## History

Remeshing by local operators grew out of the mesh optimization work of the 1990s, which used splits, collapses and swaps to fit a mesh to data. Surazhsky and Gotsman described explicit remeshing by local operators in 2003. In 2004 Botsch and Kobbelt, in a paper on multiresolution modeling, reduced the method to a loop of four steps with the thresholds $\frac{4}{3}L$ and $\frac{4}{5}L$, and this simple form became the standard one in teaching and in libraries. The termination of the split step rests on the 1975 theorem of Rosenberg and Stenger on the angles of longest-side bisection.

## References
