---
tag: S69GHG
kind: algorithm
slug: ball-pivoting-algorithm
name: Ball-pivoting algorithm
aliases:
- ball pivoting
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Reconstructs a triangle mesh from an oriented point cloud by rolling a ball of fixed radius over the points; each triangle is one where the ball touches three points and holds none.
solves: [surface-reconstruction]
model: real-ram
complexity:
  vars: {n: the number of points, d: the largest number of points within distance 2ρ of a point}
  time: {worst: O(n d^3), best: Θ(n)}
  space: {extra: O(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1999
  people: [Fausto Bernardini, Joshua Mittleman, Holly Rushmeier, Cláudio Silva, Gabriel Taubin]
  note: Bernardini and his coauthors at IBM built triangle meshes from large laser scans by pivoting a ball around the edges of a growing front, in IEEE Transactions on Visualization and Computer Graphics.
prereqs: [surface-reconstruction, alpha-shape, delaunay-triangulation]
see_also: [poisson-surface-reconstruction, uniform-grid, fixed-radius-near-neighbors, polygon-mesh, mesh-simplification, convex-hull]
sources:
  - paper: doi:10.1109/2945.817351
    title: Fausto Bernardini, Joshua Mittleman, Holly Rushmeier, Cláudio Silva and Gabriel Taubin, The ball-pivoting algorithm for surface reconstruction, IEEE Transactions on Visualization and Computer Graphics 5(4), 349 to 359, 1999
    locator: the whole paper (the seed triangle, the front of edges with its join and glue operations, the pivot, the relation to alpha shapes and the sampling conditions, several radii)
---

The ball-pivoting algorithm builds a triangle mesh through a set of points that sample a surface, with a normal at each point. It imagines a ball of a fixed radius $\rho$ that rests on the points from the outside. When the ball touches three points and contains no other, those three points form a triangle. The ball then rolls, or pivots, over each edge of the triangle, keeping contact with the two end points, until it touches a new point; that makes the next triangle. The output triangles all come from empty balls, so they are a subset of the [alpha shape](/alpha-shape/) of the points for $\alpha = \rho$, and the method is fast and needs little memory, but holes stay open where the sampling is sparser than the ball.

## In plain words

Think of the points as nails in a surface, with a ball rolling over their heads. Put the ball down so that it sits on three nails and touches no other. Those three nails become a triangle.

Now roll the ball over one side of the triangle, as if that side were a hinge. The ball keeps touching the two nails of the hinge, and it swings until it hits a third nail. That nail and the hinge make a new triangle. Keep a list of the sides that the ball has not rolled over yet, and roll over each one.

When the ball swings off into empty space, the side is the edge of a hole or of the surface. When no side is left, put the ball down at a new place and start again.

## The problem

The input is a set of $n$ points $p_1, \ldots, p_n$ in space with outward unit normals $\nu_1, \ldots, \nu_n$, and a radius $\rho > 0$. The output is a set of triangles on the points, a [polygon mesh](/polygon-mesh/) that approximates the sampled surface; this is [surface reconstruction](/surface-reconstruction/) by interpolation. For three points $a, b, c$ with normal $N = (p_b - p_a) \times (p_c - p_a)$, let $B(a, b, c)$ be the ball of radius $\rho$ through them whose center is on the side of $N$; it exists when the circumradius $R$ of the triangle is at most $\rho$, and its center is the circumcenter plus $\sqrt{\rho^2 - R^2}\, N / |N|$. A triangle $(a, b, c)$ is valid when $B(a, b, c)$ has no point of the input strictly inside and $N \cdot \nu_v > 0$ for its three vertices.

## The algorithm

The front is the set of directed edges $(i, j)$ that belong to one output triangle $(i, j, o)$ so far, with the triangle on the left; the ball of $(i, j, o)$ sits on it.

```pseudo id=main
BALL-PIVOTING(p, ν, ρ)
L1  while a seed triangle exists do
L2      take an unused point a and points b, c within 2ρ of it, nearest first (b and c unused or on the front)
L3      if (a, b, c) is valid then add it; put its edges in the front
L4      if no point gives a valid seed then stop
L5      while the front has an edge (i, j) with triangle (i, j, o) do
L6          pivot the ball B(i, j, o) about the axis from p_i to p_j
L7          for each point k within 2ρ of the midpoint of i and j do
L8              θ_k ← the rotation angle from the center of B(i, j, o) to the center of B(j, i, k)
L9          k ← the point with the least θ_k; if k is unused or on the front, and the edges (i, k) and (k, j) are not in the mesh
L10         then add the triangle (j, i, k) if it is valid, and glue: remove each edge whose reverse is in the front
L11         else leave (i, j) in the front as a boundary edge
L12 return the triangles
```

The center of every ball through $p_i$ and $p_j$ lies on a circle around the edge: in the plane through the midpoint $m$ that is perpendicular to the edge, at distance $\sqrt{\rho^2 - |p_j - p_i|^2 / 4}$ from $m$. In line L8 the angle is measured in the right hand sense about $u = (p_j - p_i) / |p_j - p_i|$, which turns the ball away from the triangle $(i, j, o)$: with $a = c_0 - m$ and $b = c_k - m$, $\theta_k = \operatorname{atan2}(u \cdot (a \times b), a \cdot b)$ taken in $[0, 2\pi)$. As the ball turns from $c_0$ to the first $c_k$, it stays empty, so the first point hit has an empty ball. Points within $2\rho$ of $m$ are found with a [uniform grid](/uniform-grid/) of cell size $2\rho$, a [fixed radius near neighbor](/fixed-radius-near-neighbors/) query. Line L10 is the join of the paper when $k$ is new, and the glue when an edge of the new triangle meets its reverse in the front.

## Example

Take six points in the plane $z = 0$, all with normal $(0, 0, 1)$: $p_0 = (0, 0)$, $p_1 = (2, 0)$, $p_2 = (1, 1.5)$, $p_3 = (3, 1.2)$, $p_4 = (1.2, -1.4)$, $p_5 = (6, 0)$, and $\rho = 1.2$. The front is shown after each step; $R$ is the circumradius of the new triangle.

| step | action | result | front after it |
| --- | --- | --- | --- |
| 1 | seed at $p_0$: the nearest pair $p_2, p_4$ has $R > \rho$, the next pair $p_2, p_1$ is valid | triangle $(0, 1, 2)$, $R = 1.083$ | $(0,1)$, $(1,2)$, $(2,0)$ |
| 2 | pivot about $(2, 0)$ | no point: the ball swings to empty space | the same, $(2,0)$ stays as a boundary edge |
| 3 | pivot about $(1, 2)$ | hits $p_3$: triangle $(2, 1, 3)$, $R = 1.055$ | $(0,1)$, $(1,3)$, $(3,2)$, $(2,0)$ |
| 4 | pivot about $(3, 2)$, then $(1, 3)$ | no point for either | the same |
| 5 | pivot about $(0, 1)$ | hits $p_4$: triangle $(1, 0, 4)$, $R = 1.062$ | $(0,4)$, $(4,1)$, $(1,3)$, $(3,2)$, $(2,0)$ |
| 6 | pivot about $(4, 1)$, then $(0, 4)$ | no point for either | the same |
| 7 | look for a new seed | $p_5$ is more than $2\rho$ from every point | stop |

The result is 3 triangles, and the front is the boundary loop $0, 4, 1, 3, 2$. For points on a plane, the ball above a triangle is empty exactly when the circumcircle is, so the valid triangles are the [Delaunay](/delaunay-triangulation/) triangles with $R \le \rho$; here they are the 3 found. The triangle $(1, 4, 3)$ is not in the output: its three points are almost on a line, and its circumradius is far more than $\rho$. With $\rho = 1$ the output is empty, because every triangle has $R > 1$.

## Correctness

**Claim.** (1) Every output triangle $(a, b, c)$ has an empty ball $B(a, b, c)$ of radius $\rho$ on the side of its normal, so it is a face of the alpha complex for $\alpha = \rho$; it is oriented so that its normal agrees with the normals of its vertices. (2) Each directed edge is in at most one triangle, so each undirected edge is in at most two, and two triangles that share an edge have opposite directions on it. (3) The algorithm stops.

Part (1) is the test in lines L3 and L10. Part (2) is the check of line L9 and the glue of line L10. For (3), each pivot either adds a triangle, which uses a new directed edge, or leaves its edge alone for good. The full proof is in [the correctness proof](proofs/correctness.md). These are all the guarantees that hold for every input. Bernardini et al. also show that if the sampling is dense enough for $\rho$ on a smooth surface, with conditions on the curvature, the output is homeomorphic to the surface; real scans do not meet these conditions everywhere, and on them there is no worst case bound on the quality of the result.

## Complexity

The model is the [real RAM](/real-ram/), with a hash table for the grid cells.

- **Time.** A pivot reads the points within $2\rho$ of the edge midpoint, at most $O(d)$ of them, and the emptiness test of the chosen ball is another $O(d)$. There are $O(n d)$ triangles and edges in the worst case. A seed test at one point tries $O(d^2)$ pairs with an $O(d)$ emptiness test each. A point that fails as a seed fails again later, because the set of allowed partners only shrinks, so the seed scan moves through the points once. The total is $O(n d^3)$. For a scan of a surface with bounded density, $d = O(1)$, and the time is $O(n)$.
- **Space.** $O(n)$ for the grid, the front and the output, with $d = O(1)$. The paper processes scans that do not fit in memory by loading only the slices of the grid near the front.

## Properties

- **Interpolating.** The vertices are the input points; nothing is moved, which keeps details but also keeps the noise.
- **Subset of the alpha shape.** The output is a subset of the triangles of the alpha complex for $\alpha = \rho$; for points on a plane, it is a subset of the Delaunay triangles of circumradius at most $\rho$.
- **Holes.** Where the gap between points is larger than about $2\rho$, the ball falls through and the hole stays open. Where it is smaller than the noise, the ball can make extra layers.
- **One radius.** A single $\rho$ cannot fit both dense and sparse areas. The paper runs several passes with growing radii; each pass pivots the ball of the larger radius about the edges of the current front.
- **Order dependence.** Ties and the choice of seed decide the result when the input is degenerate, for example when four points lie on one ball.

## Variants and improvements

- **Several radii.** Run with $\rho_1 < \rho_2 < \cdots$, keeping the mesh and the front from one pass to the next, to fill larger holes in sparse regions.
- **Out of core.** Load the slices of the grid near the front only, as in the paper, for scans of hundreds of millions of points.
- **Parallel.** Grow fronts from several seeds in separate regions of space and merge them at the borders.
- **Other interpolating methods.** The crust and the cocone of Amenta and her coauthors select triangles from the [Delaunay triangulation](/delaunay-triangulation/) with guarantees for good samples. Approximating methods such as [Poisson surface reconstruction](/poisson-surface-reconstruction/) fit a smooth, closed surface and fill holes.

## When to use it

Use ball pivoting for dense, fairly uniform scans when the mesh must go through the input points, when the data is too big for a global method, or when you need a fast first mesh. Use [Poisson surface reconstruction](/poisson-surface-reconstruction/) when the data is noisy or has holes and you want a closed surface. Follow either one with [mesh simplification](/mesh-simplification/) if the mesh is too large.

## Pitfalls

- **Pivoting the wrong way.** Measuring the angle of line L8 about $-u$ turns the ball into the triangle that it came from, and it finds the third vertex $o$ again or a point under the surface. Turn in the right hand sense about $p_j - p_i$ when the triangle is on the left of the edge $(i, j)$.
- **Ball on the wrong side.** Taking the center of $B(j, i, k)$ on the side of $-N$ in line L8 puts the ball inside the surface, and the triangles do not match the normals. Put the center on the side of the triangle normal and check it against the point normals.
- **Joining an inner point.** Adding a triangle at a point $k$ that is used but has no edge in the front, in line L9, makes a non-manifold vertex. Only use $k$ if it is new or on the front, and leave the edge as a boundary edge otherwise.
- **Seeds only from fresh points.** Requiring all three seed points to be unused in line L2 misses parts of the surface that touch the mesh only at one vertex. Only the first point must be unused; the other two may be on the front.
- **Radius without normals.** Running without consistent normals, or with $\rho$ smaller than half the distance between neighbors, gives an empty or a heavily broken mesh. Estimate and orient the normals first, and choose $\rho$ from the typical spacing.

## Implementations

## History

Bernardini, Mittleman, Rushmeier, Silva and Taubin presented the method in 1999, at IBM, for the meshes of large laser scans of sculptures and other objects. They related it to the alpha shapes of Edelsbrunner and Mücke, of which the output is a subset, and gave it a front-based, out of core structure. The idea of a sphere that rolls over the points is also close to the way molecular surfaces are traced with a probe sphere.

## References
