---
tag: CQ85FC
kind: algorithm
slug: optimal-delaunay-triangulation
name: Optimal Delaunay triangulation
aliases:
- ODT smoothing
- variational tetrahedral meshing
area: cad/mesh-generation-for-analysis
level: research
summary: Chen and Xu's mesh that minimises the interpolation error of |x|^2, optimised by moving vertices and retriangulating, used by Alliez and coauthors for tetrahedra.
solves: [mesh-generation]
model: real-ram
complexity:
  vars: {n: the number of vertices, k: the number of sweeps}
  time: {worst: O(k n^2)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 2004
  people: [Long Chen, Jinchao Xu, Pierre Alliez, David Cohen-Steiner, Mariette Yvinec, Mathieu Desbrun]
  note: Chen and Xu defined optimal Delaunay triangulations in 2004 and proved that for fixed vertices the Delaunay triangulation minimises the error. Alliez, Cohen-Steiner, Yvinec and Desbrun used the energy to make tetrahedral meshes in 2005.
prereqs: [delaunay-triangulation, paraboloid-lifting-map, lawson-flip-algorithm]
see_also: [centroidal-voronoi-tessellation, lloyds-algorithm, laplacian-smoothing, optimization-based-mesh-smoothing, distmesh, mesh-quality-measures, sliver-exudation, tetrahedral-delaunay-refinement]
sources:
  - paper: url:https://www.math.uci.edu/~chenlong/Papers/Chen.L;Holst.M2010.pdf
    title: Long Chen and Michael Holst, Efficient mesh optimization schemes based on optimal Delaunay triangulations, Computer Methods in Applied Mechanics and Engineering 200(9-12), 2011, 967 to 984
    locator: the ODT energy, the optimality of the Delaunay triangulation for fixed vertices, and the local vertex update as the area-weighted mean of circumcentres (general locator)
  - paper: doi:10.1145/1073204.1073238
    title: Pierre Alliez, David Cohen-Steiner, Mariette Yvinec and Mathieu Desbrun, Variational tetrahedral meshing, ACM Transactions on Graphics 24(3), 2005, 617 to 625
    locator: the ODT energy in 3D, the alternation of vertex moves and Delaunay retriangulation, and the treatment of boundary vertices (general locator)
  - book: isbn:978-1-58488-730-0
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan R. Shewchuk, Delaunay Mesh Generation, CRC Press, 2012
    locator: chapter 2 (the Delaunay lemma, the lifting map and Lawson's flip algorithm)
---

An optimal Delaunay triangulation (ODT) is a triangle or tetrahedral mesh that makes the interpolation error of the function $f(x) = |x|^2$ as small as possible. Long Chen and Jinchao Xu introduced it in 2004. For fixed vertices, the best mesh is the [Delaunay triangulation](/delaunay-triangulation/), which is a theorem. The method then alternates two steps: move each free vertex to the point that minimises the error over its star, and restore the Delaunay property by edge flips. Each step lowers the error, which is proved. The meshes that result are well graded and have good shapes in practice, but no angle bound is proved, and the shapes are only measured.

## In plain words

Put a bowl shaped surface over the domain. Lift every mesh vertex up onto the bowl, and join the lifted points by flat triangles. The flat triangles sit above the bowl, and the volume of the gap between them and the bowl is the error of the mesh.

For a fixed set of points, the best way to join them is the Delaunay way, because it gives the lowest roof. The method then moves one point at a time to the place that makes the gap under its own small fan as small as possible, then rebuilds the Delaunay joins, and repeats. The gap never grows. Big gaps come from long edges, so the method spreads the points out evenly, and the triangles become near equilateral. A program measures their shape at the end.

## The problem

The input is a convex polygon $\Omega$ with corners in counterclockwise order, a set of fixed points on its sides, and a set of free points inside. The output is a triangulation of $\Omega$ with the same fixed points and moved free points. The goal is a small value of

$$E(T) = \int_\Omega (f_{I,T} - f)\,dx, \qquad f(x) = |x|^2,$$

where $f_{I,T}$ is the [piecewise linear interpolation](/piecewise-linear-interpolation/) of $f$ on $T$. On a triangle with area $|\tau|$ and edge lengths $\ell_1, \ell_2, \ell_3$, the error is $\frac{|\tau|}{12}(\ell_1^2 + \ell_2^2 + \ell_3^2)$, so $E$ is small when the triangles are small where they are many and when their edges are short for their area. The minimum over all positions is a global problem with many local minima; the method finds a local one.

## The algorithm

ORIENT2D is the [orientation test](/orientation-test/) and INCIRCLE is the [in-circle test](/in-circle-test/), both exact on Fractions. For a free vertex $x$, its star is the set of triangles $(x, a, b)$ that contain it, and its link is the polygon of the edges $ab$.

```pseudo id=main
ODT-SMOOTH(Ω, fixed, free, k)
L1  T ← a Delaunay triangulation of the corners of Ω, fixed and free   ▷ insert, then flip
L2  for sweep ← 1 to k do
L3      for each free vertex x do
L4          y* ← (1 / |Ω_x|) Σ over star triangles τ of |τ| · circumcentre(τ)
L5          for t ← 1, 1/2, 1/4, ..., 2^−29 do
L6              y ← x + t (y* − x), rounded to the grid of step 2^−20
L7              if ORIENT2D(y, a, b) > 0 for every link edge ab and Φ(y) < Φ(x) then
L8                  move x to y; break
L9      while some interior edge ij with triangles ija and jib has INCIRCLE(i, j, a, b) > 0 do
L10         flip ij to ab
L11 return T
```

Here $\Phi(y) = \sum_\tau |\tau(y)|\,(|y|^2 + |a_\tau|^2 + |b_\tau|^2)$ over the star triangles $(y, a_\tau, b_\tau)$ with signed areas. It is three times the part of $E$ that depends on the free vertex. L4 is the exact minimiser of $\Phi$ for the current star; the proof shows that it is the area-weighted mean of the circumcentres. L5 to L8 backtrack toward it: the target can lie outside the kernel of the star, where a triangle would fold over, and the grid rounding can also spoil the decrease, so both are tested exactly before a move. L9 and L10 are [Lawson's flip algorithm](/lawson-flip-algorithm/). Points on the sides of $\Omega$ never move.

## Example

Take the square $[0,4]^2$ with no fixed side points and free points $(1,1)$, $(3, \frac12)$ and $(\frac52, 3)$. L1 gives a Delaunay triangulation with 8 triangles and $E = 763/24 \approx 31.79$. These 7 points have 18 triangulations, found by a search of the [flip graph](/flip-graph/). Their energies run from $763/24$ for the Delaunay one, through $769/24$ for the next best, up to $47$, as Theorem 1 of the proof says.

| step | vertex | target $y^*$ | new position | $E$ after |
|---|---|---|---|---|
| 0 | | | | 31.792 |
| 1 | $(1, 1)$ | $(0.9331, 1.7641)$ | $(0.9331, 1.7641)$ | 30.051 |
| 2 | $(3, 0.5)$ | $(2.9054, 1.0384)$ | $(2.9054, 1.0384)$ | 29.075 |
| 3 | $(2.5, 3)$ | $(2.1980, 3.2504)$ | $(2.1980, 3.2504)$ | 28.675 |
| flips | | | none needed | 28.675 |

Each target is in the kernel of its star, so $t = 1$ is accepted. The next sweeps give $E = 28.422$, $28.384$, $28.380$, $28.379$, and after 8 sweeps $E = 28.379005$; the points have settled near $(0.650, 1.918)$, $(2.732, 1.268)$ and $(2.082, 3.350)$. The smallest mean ratio, from the [mesh quality measures](/mesh-quality-measures/), rose from 0.261 to 0.362. Three free points in a square cannot make good triangles, so the gain is small.

On the square $[0,8]^2$ with 28 fixed points at unit spacing on the sides and 20 random free points, 20 sweeps lower $E$ from 70.47 to 39.41, raise the smallest angle from $7.3°$ to $29.1°$ and the smallest mean ratio from 0.217 to 0.718. These are measurements.

## Correctness

The full proofs are in the proof file; here is the outline. By the [paraboloid lifting map](/paraboloid-lifting-map/), the interpolant $f_{I,T}$ is the roof made of the lifted triangles, and a point lies inside a circumcircle exactly when its lift lies below the plane of the lifted triangle. Every roof lies on or above the lower convex envelope $g$ of the lifted points, and the Delaunay roof is equal to $g$. So among all triangulations of a fixed vertex set, the Delaunay ones minimise $E$, and only they do. Applied to four points in convex position, the same fact shows that each Lawson flip lowers $E$ strictly, so the flip loop of L9 stops, and it stops at a Delaunay triangulation.

For the vertex move, the signed areas of the star triangles add up to the area of the link polygon for every position $y$. So $\Phi(y) = |\Omega_x|\,|y - y^*|^2 + c$, a convex quadratic with minimum at $y^*$. On the segment from $x$ to $y^*$, $\Phi$ falls by $|\Omega_x|\,t(2 - t)\,|x - y^*|^2$, and points near $x$ are in the open kernel of the star. The code accepts a rounded point only after exact tests, so $E$ never increases.

What is proved is that $E$ goes down and the result is a valid Delaunay triangulation. What is not proved is a bound on angles or a global minimum. With only the four corners of $[0,8]^2$ on the boundary and 20 free points, $E$ fell from 202.5 to 82.3 while the smallest angle fell from $3.0°$ to about $6 \cdot 10^{-6}$ degrees: the free points crowded the two long sides.

## Complexity

One vertex move costs $O(d)$ per trial for a vertex of degree $d$, and there are at most 30 trials, so the moves of one sweep cost $O(n)$ in total with an adjacency structure. Lawson's flip loop can need $\Theta(n^2)$ flips in the worst case, so a sweep costs $O(n^2)$ and $k$ sweeps $O(k n^2)$. In practice the vertices move little after the first sweeps and only a few flips are needed, so a sweep costs close to $O(n)$. The simple implementation here scans the triangle list for each star and restarts the flip search after each flip, which costs more but keeps the code short. The space is $O(n)$. In exact arithmetic the coordinates would grow in size at each move; rounding to a dyadic grid, followed by an exact test, keeps them small.

## Properties

- **Optimal connectivity, proved.** For fixed vertices, the Delaunay triangulation is the exact minimiser of $E$.
- **Monotone, proved.** $E$ never increases from one step to the next.
- **Shape not guaranteed.** Shapes improve in practice, but no angle bound follows from the energy.
- **Exact.** Every orientation and in-circle decision uses exact arithmetic; floats only propose the next position.
- **Isotropic and uniform.** The energy favours equal sizes. A density weight gives a graded mesh.

## Variants and improvements

- **Global solve.** Chen and Holst minimise the energy over all free vertices together with a sparse linear solve in each step, which converges faster than vertex by vertex sweeps.
- **Tetrahedra.** Alliez, Cohen-Steiner, Yvinec and Desbrun use the 3D energy, in which each vertex moves to the volume-weighted mean of the circumcentres of its tetrahedra, then retriangulate with a 3D Delaunay code. The result has few bad tetrahedra in practice, but slivers can remain, because a sliver has a small circumradius-to-edge ratio and a small error. Slivers pass a radius-edge bound, so they are removed by other means, for example [sliver exudation](/sliver-exudation/).
- **Centroidal Voronoi tessellation.** A [centroidal Voronoi tessellation](/centroidal-voronoi-tessellation/), computed by [Lloyd's algorithm](/lloyds-algorithm/), moves each point to the centroid of its Voronoi cell instead. Both energies favour well spaced points; ODT works on the triangles and CVT on the cells.
- **Boundary vertices.** Moving boundary points along the boundary, with a correction to the target, reduces the crowding near long boundary edges.

## When to use it

Use it to improve a mesh made by [Delaunay refinement](/delaunay-refinement/) or another generator, when the vertex set can change but the boundary is fixed, and when an isotropic mesh with near equilateral elements is the goal. It gives better shapes than [Laplacian smoothing](/laplacian-smoothing/), because it also changes the connectivity. When the worst element matters most, follow it with [optimization-based mesh smoothing](/optimization-based-mesh-smoothing/), which raises the smallest quality directly. Do not use it when a proved angle bound is needed, or for an anisotropic mesh, where the energy must use a metric.

## Pitfalls

- **Coarse boundary.** If the boundary has few points, free points crowd its long edges and the triangles there become flat. Sample the boundary at the target size first.
- **Target outside the star.** The target $y^*$ can lie outside the kernel of the star. Moving there without a test makes an inverted triangle. Backtrack and test.
- **No retriangulation.** Moving the vertices without the flips is not ODT. The flip step is the half of the method that has a proof of optimality.
- **Inexact in-circle.** With float predicates the flip loop can cycle on nearly cocircular points. Use exact predicates.
- **Slivers in 3D.** The 3D energy does not remove slivers on its own.

## Implementations

## History

Long Chen and Jinchao Xu introduced optimal Delaunay triangulations in 2004, in a paper in the Journal of Computational Mathematics, with the proof that for fixed vertices the Delaunay triangulation is optimal for the function $|x|^2$, and Chen used the energy for mesh smoothing in the same year. Alliez, Cohen-Steiner, Yvinec and Desbrun applied it to tetrahedral meshing in 2005, under the name variational tetrahedral meshing. Chen and Holst gave faster local and global schemes in 2011.

## References
