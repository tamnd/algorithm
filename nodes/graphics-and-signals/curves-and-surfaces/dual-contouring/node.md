---
tag: B0HXQ1
kind: algorithm
slug: dual-contouring
name: Dual contouring
aliases:
- dual contouring of implicit surfaces
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Isosurface extraction that puts one vertex in each cut cell at the minimizer of a quadratic error built from Hermite data, which keeps sharp edges and corners.
solves: [isosurface-extraction]
model: real-ram
complexity:
  vars: {n: the number of cells of the grid, k: the number of bisection steps per edge}
  time: {worst: Θ(n k), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 2002
  people: [Tao Ju, Frank Losasso, Scott Schaefer, Joe Warren]
  note: Ju, Losasso, Schaefer and Warren contoured Hermite data with one vertex per cell of an octree, placed by a quadratic error function, at SIGGRAPH 2002.
prereqs: [isosurface-extraction, marching-cubes, least-squares-problem]
see_also: [marching-tetrahedra, quadric-error-metrics, pseudoinverse, singular-value-decomposition, octree, signed-distance-function, implicit-surface, polygon-mesh]
sources:
  - paper: doi:10.1145/566654.566586
    title: Tao Ju, Frank Losasso, Scott Schaefer and Joe Warren, Dual contouring of Hermite data, ACM Transactions on Graphics 21(3) (SIGGRAPH 2002), 339 to 346, 2002
    locator: the whole paper (Hermite data, the quadratic error function and its solution near the mass point, the quads dual to the edges with a sign change, the octree simplification)
  - paper: "Leif Kobbelt, Mario Botsch, Ulrich Schwanecke and Hans-Peter Seidel, Feature sensitive surface extraction from volume data, Proceedings of SIGGRAPH 2001, 57 to 66, 2001"
    locator: the whole paper (extended marching cubes, the earlier use of a quadratic error function on Hermite data to place feature points)
  - paper: doi:10.1109/TVCG.2007.1012
    title: Scott Schaefer, Tao Ju and Joe Warren, Manifold dual contouring, IEEE Transactions on Visualization and Computer Graphics 13(3), 610 to 619, 2007
    locator: the whole paper (the non-manifold output of dual contouring and the fix with several vertices per cell)
  - paper: doi:10.1145/37401.37422
    title: William E. Lorensen and Harvey E. Cline, Marching cubes, a high resolution 3D surface construction algorithm, Computer Graphics (SIGGRAPH 87 Proceedings) 21(4), 163 to 169, 1987
    locator: the whole paper (the primal method, with vertices on the edges)
---

Dual contouring builds a mesh of the surface $f = c$ from samples of $f$ on a grid and from Hermite data, the exact crossing point and the surface normal on each grid edge with a sign change. Where [marching cubes](/marching-cubes/) puts vertices on the edges, dual contouring puts one vertex inside each cut cell, at the point that best fits the tangent planes of that cell in the least squares sense. It then joins the four cells around each cut edge by a quadrilateral. Because the vertex fits planes and not only points, it can sit on a sharp edge or corner of the surface, which marching cubes cuts off. The output is closed, but it can be non-manifold where a cell or a face is ambiguous.

## In plain words

Look at each little cube of the grid that the surface passes through. On each cube edge where the value changes from low to high, find the point where the surface crosses the edge, and find which way the surface faces there. That gives a small flat piece of the surface, a tangent plane, at each crossing.

Now put one point in the cube: the point that is as close as possible to all of these planes at once. If the planes meet at a corner, the point lands on that corner. If they meet along a line, it lands on the line, at the spot nearest the middle of the crossings.

Last, each cut edge is surrounded by four cubes. Join their four points by a four-sided face. These faces fit together into a closed surface.

## The problem

The input is a function $f$ and its gradient $\nabla f$, an iso value $c$, and a grid of $(N + 1)^3$ points $o + h(i, j, k)$, $0 \le i, j, k \le N$, with $n = N^3$ cells. A grid point is inside when $f < c$. The output is a [polygon mesh](/polygon-mesh/) of quadrilaterals whose normals point to the outside, an approximation of the [isosurface](/isosurface-extraction/) $\{f = c\}$. The method needs only, for each grid edge with a sign change, its crossing point $p_e$ and the unit normal $n_e$ there; these are the Hermite data. A [signed distance function](/signed-distance-function/) or another implicit model gives them directly. From a scan, they come from the samples and an estimated gradient.

For a cell $C$ with crossings $p_1, \ldots, p_m$ and normals $n_1, \ldots, n_m$ on its edges, the quadratic error function (QEF) is

$$E(x) = \sum_{i=1}^{m} \bigl(n_i \cdot (x - p_i)\bigr)^2 = \lVert A x - b \rVert^2, \qquad A = \begin{pmatrix} n_1^{\mathsf T} \\ \vdots \\ n_m^{\mathsf T} \end{pmatrix},\ b_i = n_i \cdot p_i,$$

the sum of the squared distances from $x$ to the tangent planes. Minimizing it is a [least squares problem](/least-squares-problem/), the same sum of plane quadrics that [quadric error metrics](/quadric-error-metrics/) use for simplification.

## The algorithm

```pseudo id=main
DUAL-CONTOURING(f, ∇f, c, grid)
L1  for each grid edge e = (u, w) whose ends are on different sides of c do
L2      p_e ← the point on e with f(p_e) = c, by bisection
L3      n_e ← ∇f(p_e) / |∇f(p_e)|; add (p_e, n_e) to each of the up to 4 cells that contain e
L4  for each cell C that has Hermite data do
L5      m ← the mean of its points p_i; v_C ← m + A⁺_τ (A^T b − A^T A m)
L6      optionally clamp v_C into C
L7  for each edge e with a sign change that is not on the border of the box do
L8      C_1, C_2, C_3, C_4 ← the 4 cells around e, counterclockwise seen from the + end of e
L9      if the + end of e is inside then reverse the order
L10     append the quad (v_{C_1}, v_{C_2}, v_{C_3}, v_{C_4})
L11 return the vertices v_C and the quads
```

In line L5, $A^{\mathsf T} A$ is a symmetric $3 \times 3$ matrix, and $A^{+}_{\tau}$ is its truncated [pseudoinverse](/pseudoinverse/): with the eigen decomposition $A^{\mathsf T} A = \sum_j \lambda_j e_j e_j^{\mathsf T}$, from the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/) or a [singular value decomposition](/singular-value-decomposition/) of $A$, it is $\sum_{\lambda_j > \tau^2 \lambda_{\max}} \lambda_j^{-1} e_j e_j^{\mathsf T}$. The result is a minimizer of $E$ restricted to the directions with large eigenvalues, and it stays at the mass point $m$ along the other ones. On a flat part, all $n_i$ are nearly equal, one eigenvalue is large, and $v_C$ is the mass point moved along $n$ to the best fitting plane. Along a sharp edge two eigenvalues are large, and $v_C$ lands on the edge line. At a corner all three are large, and $v_C$ is the corner. Line L2 is the [bisection method](/bisection-method/) on the segment $e$; any root finder works, and when $f$ is a linear interpolant of the samples, the crossing has a closed form. The implementation uses $\tau = 0.1$.

## Example

Take the cube $[1.3, 6.4]^3$, given by $f(x) = \max_t |x_t - 3.85| - 2.55$ and $c = 0$, on the grid of integer points $0, \ldots, 8$ with $h = 1$. The normal on a face is the unit vector along the axis of that face. Two cells:

| cell | edges with a sign change | crossings $p_i$ | normals $n_i$ | $A^{\mathsf T} A$ | mass point $m$ | $v_C$ |
| --- | --- | --- | --- | --- | --- | --- |
| $[1,2]^3$ | the 3 edges at $(2,2,2)$ | $(1.3, 2, 2)$, $(2, 1.3, 2)$, $(2, 2, 1.3)$ | $-e_x$, $-e_y$, $-e_z$ | $I$ | $(1.77, 1.77, 1.77)$ | $(1.3, 1.3, 1.3)$ |
| $[1,2] \times [3,4] \times [1,2]$ | 2 edges along $x$, 2 along $z$ | $(1.3, 3, 2)$, $(1.3, 4, 2)$, $(2, 3, 1.3)$, $(2, 4, 1.3)$ | $-e_x$, $-e_x$, $-e_z$, $-e_z$ | $\operatorname{diag}(2, 0, 2)$ | $(1.65, 3.5, 1.65)$ | $(1.3, 3.5, 1.3)$ |

In the first cell the three planes $x = 1.3$, $y = 1.3$, $z = 1.3$ meet at the corner of the box, and the vertex is that corner. Marching cubes would put one triangle through the three crossings and cut the corner off. In the second cell the eigenvalue along $y$ is 0, so the vertex keeps the $y$ of the mass point and sits on the box edge. The whole mesh has all 8 corners, 4 vertices on each of the 12 box edges, every vertex on the box surface, Euler characteristic 2, and the exact volume $5.1^3$ when the quads are split into triangles.

## Correctness

**Claim.** (1) Each $v_C$ minimizes $E$ over the affine set $m + \operatorname{span}\{e_j : \lambda_j > \tau^2 \lambda_{\max}\}$, so it is an exact minimizer of $E$ when no eigenvalue is truncated, and an exact point of every tangent plane when the planes have a common point and no eigenvalue is truncated. (2) If every border sample is outside, the quads form a closed oriented surface: each mesh edge is used by the quads equally often in the two directions. It is the boundary of the union of the cubes of side $h$ centered at the inside grid points, with the corners moved to the vertices $v_C$. Each mesh edge is in 2 quads, or in 4 when the grid face across it has all four corners alternating in sign.

Part (1) is the normal equations $A^{\mathsf T} A x = A^{\mathsf T} b$ solved on an eigenbasis. Part (2) holds because the quad of an edge is the face between the dual cube of its inside end and that of its outside end. The full proof is in [the correctness proof](proofs/correctness.md). Dual contouring gives no guarantee that the mesh is a manifold, that it has the topology of $\{f = c\}$, or that it does not intersect itself: a vertex placed by the QEF can fall outside its cell and fold a quad over its neighbor.

## Complexity

The model is the [real RAM](/real-ram/), with an evaluation of $f$ or $\nabla f$ as one step.

- **Time.** Line L1 evaluates $f$ at the $(N + 1)^3$ grid points. Each cut edge costs $k$ evaluations in line L2, and line L5 costs $O(1)$ per cell: a $3 \times 3$ eigen problem with a bounded number of rotations, and at most 12 data points. The total is $\Theta(n)$ plus $k$ times the number of cut edges, so $\Theta(n k)$ in the worst case and $\Theta(n)$ when the crossings have a closed form.
- **Space.** $\Theta(n)$ for the samples, and $\Theta(V + F)$ for the output. The mesh has one vertex per cut cell and one quad per cut edge, which are about equal in number for a closed surface. Marching cubes has one vertex per cut edge and about two triangles per vertex, so the two methods give about the same number of triangles; for the sphere of radius 3.3 with $h = 1$ in the tests, dual contouring gives 224 vertices and 222 quads.
- **Octree.** On an [octree](/octree/) with $s$ leaves, the cost is $O(s)$ instead of $O(n)$. Ju et al. also collapse octree cells whose combined QEF has a small residual, which simplifies flat regions while keeping features.

## Properties

- **Sharp features.** Edges and corners of the surface are reproduced where the Hermite data sees them, without a feature detection step.
- **Closed, not always manifold.** The quads always close up, but at an ambiguous face four quads share an edge, and at an ambiguous cell one vertex joins two sheets. A coarse grid on a smooth torus already shows this: in the tests, with $h = 1$, the top circle of a tube of radius 2 lies 0.05 above a grid plane, the inside grid points on that plane form a thin, staircase band, and 12 edges are in 4 quads. With $h = 1/2$ the mesh is a manifold.
- **Quads.** The output is a quad mesh, which suits subdivision and texture work. A quad is not planar in general; splitting it into two triangles needs a choice of diagonal.
- **Vertices off the cell.** Without clamping, a vertex can lie outside its cell when the planes are nearly parallel and the truncation threshold is too low, or when the data is noisy. With clamping it stays in the cell but can leave the feature.
- **One vertex per cell.** A cell that is cut by two separate pieces of surface still gets one vertex, which joins them.

## Variants and improvements

- **Surface nets.** Ignore the normals and put $v_C$ at the mass point (or relax it), which gives smooth meshes without features; this is the surface nets method of Gibson (1998).
- **Extended marching cubes.** Kobbelt et al. (2001) place an extra vertex, from a similar QEF, inside cells that contain a feature, and keep the primal vertices of [marching cubes](/marching-cubes/).
- **Octree simplification.** Sum the QEF matrices $A^{\mathsf T} A$, $A^{\mathsf T} b$ and $b^{\mathsf T} b$ of the children and collapse when the error of the combined vertex is small, as in [quadric error metrics](/quadric-error-metrics/).
- **Manifold dual contouring.** Schaefer, Ju and Warren (2007) put one vertex per surface component of a cell, chosen by the marching cubes cases, and simplify only where the topology stays the same; the output is then a manifold.
- **Robust QEF.** Store the QEF in the QR form of $A$, which avoids forming $A^{\mathsf T} A$ and loses less precision, or regularize toward the mass point by adding a small multiple of $\lVert x - m \rVert^2$.

## When to use it

Use dual contouring when the surface has sharp edges and corners and you have, or can compute, normals: CAD models, constructive solid geometry on signed distance functions, and voxel game worlds that are edited by the user. Use it on octrees for adaptive meshes. Use [marching cubes](/marching-cubes/) when the data is scanned, without reliable normals, or when the output must be a manifold with no further work; use the manifold variant when you need both.

## Pitfalls

- **Inverting the full matrix.** Solving $A^{\mathsf T} A x = A^{\mathsf T} b$ with a plain inverse on a flat or nearly flat cell gives a huge, meaningless $x$, because $A^{\mathsf T} A$ is singular or nearly so. Line L5 solves relative to the mass point with the truncated pseudoinverse; the wrong form is $x = (A^{\mathsf T} A)^{-1} A^{\mathsf T} b$.
- **Truncating relative to zero.** A truncation threshold that is not relative to the largest eigenvalue (or that is too small) keeps the noise directions of nearly parallel normals and throws the vertex far out of its cell. Use a relative threshold as in line L5, and clamp in line L6 if the vertex must stay in the cell.
- **Unnormalized gradients.** Using $\nabla f$ without normalizing it in line L3 gives more weight to planes where $|\nabla f|$ is large, and the vertex moves away from the features. Normalize every normal.
- **Wrong quad orientation.** Taking the 4 cells in the same order for every edge, without line L9, gives half the quads the wrong normal. Reverse the order when the inside end of the edge is the + end.
- **Assuming a manifold.** Code that builds a half-edge structure from the quads fails at the edges that are in 4 quads. Check for them, refine the grid, or use manifold dual contouring.

## Implementations

## History

Kobbelt, Botsch, Schwanecke and Seidel used Hermite data and a quadratic error function to place feature vertices in their extended marching cubes of 2001. Ju, Losasso, Schaefer and Warren made the method dual in 2002: one vertex per cell, quads dual to the cut edges, and simplification on an octree by summing the QEFs, which works without detecting the features first. Schaefer, Ju and Warren fixed the non-manifold cases in 2007 with manifold dual contouring. The dual structure of the mesh goes back to the cuberille methods of the late 1970s, which output the faces of the voxels themselves.

## References
