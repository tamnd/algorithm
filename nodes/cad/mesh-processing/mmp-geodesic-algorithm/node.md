---
tag: 14F19Q
kind: algorithm
slug: mmp-geodesic-algorithm
name: Mitchell-Mount-Papadimitriou algorithm
aliases:
- MMP algorithm
- continuous Dijkstra
area: cad/mesh-processing
level: advanced
summary: Computes exact geodesic distances from a source on a polyhedral surface by propagating intervals of edges with one unfolding each, in O(n^2 log n) time.
solves: [discrete-geodesic-problem]
model: real-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n² log n)}
  space: {extra: O(n²)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1987
  people: [Joseph S. B. Mitchell, David M. Mount, Christos H. Papadimitriou]
  note: They gave the first polynomial exact method for shortest paths on a general polyhedral surface, by sweeping a distance front over the edges in the order of Dijkstra's algorithm.
prereqs: [discrete-geodesic-problem, dijkstra, polygon-mesh]
see_also: [heat-method, fast-marching-method, euclidean-shortest-path, visibility-graph, discrete-gaussian-curvature, priority-queue, eikonal-equation, single-source-shortest-paths]
sources:
  - paper: doi:10.1137/0216045
    title: Joseph S. B. Mitchell, David M. Mount and Christos H. Papadimitriou, The discrete geodesic problem, SIAM Journal on Computing 16(4), 1987, 647 to 668
    locator: the structure of shortest paths (straight in each face, through vertices only at saddle or border vertices), intervals of optimality on edges, and the O(n^2 log n) time and O(n^2) space bounds
  - paper: doi:10.1145/1073204.1073228
    title: Vitaly Surazhsky, Tatiana Surazhsky, Danil Kirsanov, Steven J. Gortler and Hugues Hoppe, Fast exact and approximate geodesics on meshes, ACM Transactions on Graphics 24(3) (SIGGRAPH 2005), 553 to 560
    locator: the window data (interval, pseudo-source position, distance to the pseudo-source), the propagation across a face, the trimming of overlapping windows, and the measured running times
  - paper: "Jindong Chen and Yijie Han, Shortest paths on a polyhedron, Proceedings of the 6th ACM Symposium on Computational Geometry, 1990, 360 to 369; journal version in International Journal of Computational Geometry and Applications 6(2), 1996, 127 to 144"
    title: Jindong Chen and Yijie Han, Shortest paths on a polyhedron
    locator: the O(n^2) time and O(n) space method that keeps one tree of unfoldings and prunes it with the "one angle one split" rule
  - paper: doi:10.1137/0215014
    title: Micha Sharir and Amir Schorr, On shortest paths in polyhedral spaces, SIAM Journal on Computing 15(1), 1986, 193 to 215
    locator: the first algorithm for shortest paths on the surface of a convex polytope
  - paper: doi:10.1007/s00454-007-9031-0
    title: Yevgeny Schreiber and Micha Sharir, An optimal-time algorithm for shortest paths on a convex polytope in three dimensions, Discrete and Computational Geometry 39, 2008
    locator: the O(n log n) time algorithm for convex polytopes (general locator, the pages were not checked)
---

The Mitchell-Mount-Papadimitriou algorithm, or MMP, computes exact shortest path distances on the surface of a triangle mesh. Paths may cross faces anywhere, not only along edges, so the answer is the true geodesic distance of the polyhedral surface and not a graph distance. The method keeps, on each edge, a set of *windows*. A window is an interval of the edge where the shortest paths all come straight from one point, a *pseudo-source*, in one flat unfolding of the faces they cross. Windows are taken in order of distance from a [priority queue](/priority-queue/), as in [Dijkstra's algorithm](/dijkstra/), and each one is pushed across the next face and cut at the two other edges. Vertices where shortest paths can bend start new windows. MMP runs in $O(n^2 \log n)$ time, and it is the reference against which approximate methods such as the [heat method](/heat-method/) and the [fast marching method](/fast-marching-method/) are measured.

## In plain words

Think of an ant walking on the surface of a box. It can walk straight across a side, and when it reaches an edge it keeps going straight on the next side, as if the two sides were unfolded flat. The shortest walk to a far corner may cross several sides, and it is a straight line on the right unfolding.

The method spreads out from the start like a ripple. On each edge it keeps pieces where the ripple arrives straight from one known point. It always grows the nearest piece first. When a piece crosses a triangle, it splits where the triangle's far corner is, and when two pieces from different directions land on the same part of an edge, only the nearer one is kept. At corners where a walk can bend, such as the inner corner of an L-shaped room, the ripple restarts from the corner.

## The problem

The input is a triangle mesh that is a connected manifold, possibly with border, and one or more source vertices. The surface is the union of the flat triangles. The length of a path on the surface is its Euclidean length, and the geodesic distance $d(v)$ is the length of a shortest path from the nearest source to $v$. The output is $d(v)$ for every vertex $v$. This is the [discrete geodesic problem](/discrete-geodesic-problem/).

Two facts about shortest paths drive the method. Inside a face a shortest path is a straight segment, and across an edge it continues straight in the unfolding of the two faces. A shortest path passes through a vertex $v$ only if $v$ is on the border, or the angles of the faces at $v$ sum to at least $2\pi$ (MMP call the case above $2\pi$ a saddle vertex, and its curvature $2\pi - \sum$ is negative, see [discrete Gaussian curvature](/discrete-gaussian-curvature/)). At a vertex with angle sum below $2\pi$ a shortest path never bends.

## The algorithm

A window $w$ lives on an edge $pq$ and looks into one face $h$ of that edge. In the frame where $p = (0, 0)$, $q = (|pq|, 0)$ and the third vertex of $h$ has $y > 0$, it holds an interval $[b_0, b_1]$ of the edge, a pseudo-source $s = (s_x, s_y)$ with $s_y < 0$, and the distance $\sigma$ from the source to $s$. On the interval the window claims the distance $\sigma + |(x, 0) - s|$. Its key is the smallest such value. A vertex is a *pseudo-source vertex* if it is a source, a border vertex, or has angle sum at least $2\pi$.

```pseudo id=main
MMP(mesh, sources)
L1  d(v) ← ∞ for all v; d(s) ← 0 and push the vertex event s for each source s
L2  while the queue is not empty do pop the event with the smallest key
L3      if it is a vertex event at a pseudo-source vertex v with key d(v) then for each face (v, a, b) put the window [0, |ab|] with pseudo-source v and σ = d(v) on the edge ab, looking into the face beyond it
L4      if it is a window w on edge pq into face h with third vertex r then unfold r into the frame; if r lies in the cone from s through w then d(r) ← min(d(r), σ + |r − s|); cut the cone at the edges pr and rq
L5      for each new window on an edge e: lower d at the end points it covers, trim it and the windows already on e so that each point keeps only the windows with the smallest value, and push the pieces that remain; push a vertex event whenever some d(v) drops
L6  return d
```

**Cutting the cone** (line L4). The rays from $s$ through $(b_0, 0)$ and $(b_1, 0)$ bound a cone. The ray from $s$ through the third vertex $r$ meets the edge at $x = g_r$. Rays through $[b_0, \min(b_1, g_r)]$ leave the face through $pr$, and rays through $[\max(b_0, g_r), b_1]$ leave through $rq$. Each part becomes a window on its edge, with $s$ written in the frame of that edge and the next face, and the same $\sigma$.

**Trimming** (line L5). Two windows on one edge give two distance functions $\sigma_1 + |x - s_1|$ and $\sigma_2 + |x - s_2|$. They are equal where a hyperbola meets the edge, at most two points, which a quadratic equation gives. Between these points one window is better, and the worse one loses that part. Windows on the two sides of an edge are compared too, because the distance on the edge is the same from both sides.

## Example

**The unit cube.** Take the cube $[0, 1]^3$ as 12 triangles, with the source at the corner $(0, 0, 0)$. The source is a pseudo-source vertex, so line L3 puts a window on the far edge of each of its 6 faces. One of them lies on the edge from $(1, 0, 0)$ to $(1, 1, 0)$ of the bottom face and looks into the side $x = 1$. Unfolding that side into the plane of the bottom puts the far corner $(1, 1, 1)$ at $(2, 1, 0)$, inside the cone from the source, so line L4 gives $d = \sqrt{2^2 + 1^2} = \sqrt{5} \approx 2.236$. A path along edges needs at least $1 + \sqrt{2} \approx 2.414$. The whole run makes 14 windows.

**A box.** On the box $1 \times 2 \times 3$, the three ways to unfold two sides between opposite corners give $\sqrt{(1 + 2)^2 + 3^2} = \sqrt{18}$, $\sqrt{(1 + 3)^2 + 2^2} = \sqrt{20}$ and $\sqrt{(2 + 3)^2 + 1^2} = \sqrt{26}$. MMP returns $\sqrt{18} \approx 4.243$, and the edge graph gives $4.606$.

**An L-shaped floor.** On the flat region $[0, 2]^2$ without the square $(1, 2] \times (1, 2]$, with the source at $(2, 0)$, the vertices $(1, \frac{3}{2})$, $(1, 2)$ and $(\frac{1}{2}, 2)$ cannot be seen in a straight line. The reflex corner $(1, 1)$ is a border vertex, so it becomes a pseudo-source with $\sigma = \sqrt{2}$, and the distance to $(\frac{1}{2}, 2)$ is $\sqrt{2} + \sqrt{\frac{5}{4}}$. The tests check every vertex against the exact visibility test.

## Correctness

The correctness file proves three things in exact arithmetic. *Soundness*: every value that the method assigns is the length of a real path on the surface, because a window only holds rays that stay inside the unfolded faces they cross. *Completeness*: for every vertex, the window chain of one shortest path survives all trimming, because a window is only cut where another one is strictly better, and a shortest path cannot be beaten at any point it crosses. *Order*: as in Dijkstra's algorithm, keys never decrease along a chain, so when a vertex event is taken, its distance is final, and the windows it starts use the right $\sigma$. Together these give $d(v)$ equal to the geodesic distance for every vertex. The algorithm stops because each window is pushed across a face once and, by the analysis of Mitchell, Mount and Papadimitriou, only finitely many windows are made.

The code uses floating point, with a relative tolerance of $10^{-10}$ in the cone and trimming tests. The tests compare it with an exhaustive search over unfoldings on convex polyhedra, with exact visibility on the L-shape, with the Euclidean distance on flat grids, and with Steiner-point graph distances on rough terrains, which are upper bounds.

## Complexity

Mitchell, Mount and Papadimitriou show that each edge carries $O(n)$ intervals of optimality, so there are $O(n^2)$ windows in all. Each is pushed and taken once, at $O(\log n)$ for the queue, which gives $O(n^2 \log n)$ time and $O(n^2)$ space. These bounds are cited, not proved here, and the implementation does not keep their data structures. Surazhsky and coauthors measured running times close to $O(n^{1.5} \log n)$ on typical models. On random terrains of 81, 169 and 289 vertices, this implementation makes 451, 1019 and 1839 windows, which is about $6n$.

## Properties

- **Exact.** The answer is the true distance of the polyhedral surface, not of a graph, and it does not depend on how the faces are cut.
- **Single source per run.** Several sources are handled by starting from all of them, which gives the distance to the nearest one.
- **Full field.** The windows describe the distance at every point of every edge, and so inside every face, not only at the vertices.
- **Paths too.** Following the pseudo-sources back gives the shortest paths.
- **Order matters only for the pseudo-sources.** Trimming is safe in any order, but a pseudo-source vertex must start its windows with its final distance.

## Variants and improvements

- **Chen and Han (1990).** A tree of unfoldings pruned by the rule that each vertex angle keeps at most one child that splits, in $O(n^2)$ time and $O(n)$ space, with no priority queue.
- **Surazhsky, Surazhsky, Kirsanov, Gortler and Hoppe (2005).** The window form used here, a fast practical implementation of MMP, and an approximate version that merges nearby windows with a bounded error.
- **Convex polytopes.** Sharir and Schorr gave the first method for convex surfaces, and Schreiber and Sharir reached the optimal $O(n \log n)$ time on them.
- **Approximations.** Steiner points on the edges with graph search, the [fast marching method](/fast-marching-method/), and the [heat method](/heat-method/) are faster, with errors that shrink as the mesh is refined.
- **Planar obstacles.** The [Euclidean shortest path](/euclidean-shortest-path/) among polygons is the flat case, where the [visibility graph](/visibility-graph/) also works.

## When to use it

Use MMP when exact distances matter, for example to measure the error of an approximate method, for geodesic Voronoi diagrams, or for paths that must be truly shortest on a coarse mesh. On meshes with millions of vertices, or when many sources and repeated queries are needed, the heat method or fast marching is often faster, at the cost of a small error.

## Pitfalls

- **Lost crossing points.** When two windows have the same $\sigma$, the quadratic for their crossing has a double root, which rounding can turn into no root. Then a whole piece is given to the wrong window and a distance is too large. The code solves the linear equation in that case, and the symmetry test $d(a, b) = d(b, a)$ catches the error.
- **Missing pseudo-sources.** Forgetting border vertices or saddle vertices loses every path that bends there, as at the corner of the L-shape.
- **Starting a pseudo-source too early.** If a vertex starts its windows before its distance is final, the wrong $\sigma$ spreads. The priority queue prevents this.
- **Grazing rays.** When the pseudo-source lies on the line of an edge, the rays only touch that edge, and the new window has no width. Skip it, the neighbouring windows cover the same points.
- **Memory.** The $O(n^2)$ windows can be too many on large meshes.

## Implementations

## History

Sharir and Schorr solved the problem on convex polytopes in 1986. In 1987 Mitchell, Mount and Papadimitriou gave the first polynomial method for general polyhedral surfaces, sweeping intervals of optimality over the edges in Dijkstra order, in $O(n^2 \log n)$ time. Chen and Han lowered the time to $O(n^2)$ and the space to $O(n)$ in 1990. For many years both methods were thought too complex to implement, until Surazhsky and coauthors showed in 2005 that the window form of MMP is simple and fast in practice. Schreiber and Sharir later reached $O(n \log n)$ for convex polytopes.

## References
