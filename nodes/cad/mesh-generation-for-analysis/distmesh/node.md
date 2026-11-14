---
tag: M30YY9
kind: algorithm
slug: distmesh
name: DistMesh
aliases:
- Persson-Strang mesh generator
area: cad/mesh-generation-for-analysis
level: advanced
summary: Persson and Strang's mesher that treats edges as springs, moves points to force balance, projects them back with a signed distance function and retriangulates.
solves: [mesh-generation]
model: real-ram
complexity:
  vars: {n: the number of points, k: the number of iterations}
  time: {worst: O(k n^2)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2004
  people: [Per-Olof Persson, Gilbert Strang]
  note: Persson and Strang published the method in SIAM Review in 2004, with a MATLAB code of about one page.
prereqs: [signed-distance-function, delaunay-triangulation, bowyer-watson-algorithm]
see_also: [optimal-delaunay-triangulation, centroidal-voronoi-tessellation, lloyds-algorithm, laplacian-smoothing, mesh-sizing-function, advancing-front-mesh-generation, isosurface-stuffing, mesh-quality-measures]
sources:
  - paper: doi:10.1137/S0036144503429121
    title: Per-Olof Persson and Gilbert Strang, A simple mesh generator in MATLAB, SIAM Review 46(2), 2004, 329 to 345
    locator: the truss analogy, the repulsive force law, the scaling factor Fscale, the projection with the signed distance function, the retriangulation test and the stopping test (general locator)
  - paper: doi:10.1093/comjnl/24.2.162
    title: Adrian Bowyer, Computing Dirichlet tessellations, The Computer Journal 24(2), 1981, 162 to 166
    locator: incremental Delaunay construction by removal of the triangles whose circumcircle contains the new point (general locator)
  - paper: doi:10.1093/comjnl/24.2.167
    title: David F. Watson, Computing the n-dimensional Delaunay tessellation with application to Voronoi polytopes, The Computer Journal 24(2), 1981, 167 to 172
    locator: the same insertion method in any dimension (general locator)
---

DistMesh is a mesh generator by Per-Olof Persson and Gilbert Strang. It describes the domain by a [signed distance function](/signed-distance-function/), which is negative inside and positive outside. It treats the edges of a triangle mesh as springs that push their two end points apart, moves the points a small step along the net force, pulls back every point that left the domain onto the boundary, and rebuilds the [Delaunay triangulation](/delaunay-triangulation/) when the points have moved enough. It repeats until the points stop moving. The code is short, the triangles are close to equilateral in practice, and the method works for any shape that has a distance function. There is no proof that the iteration converges, and no proved bound on the angles.

## In plain words

Scatter dots evenly over a box and throw away those outside the shape. Join the dots into triangles. Now think of every edge as a small spring that is a bit too short, so it pushes its two dots apart. The dots spread out until the pushes balance.

The shape acts as a wall. A dot that is pushed through the wall is put back on it. When the dots have moved far enough, join them into triangles again in the best way. When no dot moves more than a tiny amount, stop.

The result is a mesh with triangles close to equilateral and dots spread out evenly along the wall. Nothing proves that the dots settle, so a program sets a limit on the number of steps.

## The problem

The input is a domain $\Omega = \{x : f_d(x) \le 0\}$ given by a function $f_d$ that is the signed distance to the boundary, or close to it, a target edge length $h_0$, a box that contains $\Omega$, and a list of fixed points such as corners. The output is a triangle mesh of a polygon close to $\Omega$, with all vertices in $\Omega$, the fixed points among them, boundary vertices on the boundary, and edges of length close to $h_0$. This page treats a uniform size; the original method also takes a relative size function $h(x)$.

## The algorithm

The parameters are the ones of Persson and Strang: $F_\text{scale} = 1.2$, $\Delta t = 0.2$, $g_\text{eps} = 0.001 h_0$, $t_\text{tol} = 0.1$ and $d_\text{tol} = 0.001$.

```pseudo id=main
DISTMESH(f_d, h0, box, fixed, cap)
L1  p ← the points of an equilateral grid of spacing h0 in the box
L2  keep the points with f_d < g_eps, and put the fixed points first
L3  for it ← 1 to cap do
L4      if some point moved more than t_tol · h0 since the last triangulation then
L5          T ← Delaunay(p); drop the triangles whose centroid has f_d ≥ −g_eps; bars ← the edges of T
L6      ℓ ← the bar lengths; L0 ← F_scale · sqrt(Σ ℓ² / number of bars)
L7      for each bar ij: push i and j apart by max(L0 − ℓ_ij, 0)
L8      p ← p + Δt · F, with no force on the fixed points
L9      for each moved point with f_d(p) > 0: p ← p − f_d(p) ∇f_d(p)
L10     if every interior point moved less than d_tol · h0 then break
L11 T ← Delaunay(p) without the outside triangles
L12 return p, T
```

L6 to L8 are one explicit Euler step of the truss equation $dp/dt = F(p)$; see the [Euler method](/euler-method/). The force of a bar is linear in the compression and zero for a stretched bar, so bars only push. $L_0$ is 20 percent longer than the mean bar, so most bars push, which drives the points out to the boundary. L9 is a projection: for an exact distance function, $\nabla f_d$ is a unit vector and the step lands on the nearest boundary point. The gradient is a forward difference. L5 and L11 use the [Bowyer-Watson algorithm](/bowyer-watson-algorithm/) with exact integer predicates on the points rounded to the grid of step $2^{-24}$; the [in-circle test](/in-circle-test/) decides which triangles to remove.

## Example

Take the unit disk with $f_d(x) = |x| - 1$, $h_0 = 0.2$ and no fixed points. L1 and L2 keep 88 points. The table shows the state after some numbers of iterations. The quality is the mean ratio $4\sqrt3 A / \sum \ell^2$ from the [mesh quality measures](/mesh-quality-measures/), where 1 means equilateral.

| iterations | triangles | smallest mean ratio | points on the circle |
|---|---|---|---|
| 1 | 151 | 0.255 | 1 |
| 2 | 155 | 0.002 | 3 |
| 10 | 149 | 0.555 | 21 |
| 40 | 145 | 0.342 | 29 |
| 90 (stopped by L10) | 143 | 0.815 | 31 |

The worst triangle is not monotone. In the first steps the outer points move to the circle and leave near flat triangles behind, and the retriangulation repairs them later. At the end, the mean of the mean ratio is 0.969, the angles are between $40.6°$ and $96.4°$, and the area of the mesh is 3.1200, just under $\pi$ because the boundary edges are chords.

On the square $[-1,1]^2$ with the four corners fixed and $h_0 = 0.25$, the run stops after 51 iterations with 87 points and 137 triangles. The smallest mean ratio is 0.852, the angles are between $42.0°$ and $91.5°$, and the triangles cover the square exactly, with area 4. With $h_0 = 0.1$ on the disk, it stops after 197 iterations with 362 points, 661 triangles and smallest mean ratio 0.839. These numbers are measured, not proved.

## Correctness

The proof file proves what can be proved. Each call of the Delaunay step gives triangles that are counterclockwise, conforming and have empty circumcircles, exactly, for the rounded points. The core is the classic argument for Bowyer-Watson: the triangles whose circumcircle contains the new point form a region that is connected and star shaped from that point, and the circles through an edge form a pencil, so each new circle lies inside the union of two old empty circles. Dropping the outside triangles keeps a subset, which keeps all three properties. For a convex domain and an exact distance function, every point stays in the domain to rounding, so every triangle does too.

What is not proved is the force iteration. Persson and Strang give no convergence proof, and the run above shows that the worst triangle can get worse for many steps before it gets better. The loop stops because of the iteration cap in L3. The tests check that the output on a disk and on a square is an exact Delaunay mesh with every triangle inside the domain, and that the Delaunay step equals a brute force over all triples on small random sets.

## Complexity

One iteration costs $O(n)$ for the forces and the projection, because a planar triangulation has $O(n)$ edges. A retriangulation costs $O(n \log n)$ with a good Delaunay code; the simple Bowyer-Watson here finds the first triangle by a linear scan, which costs $O(n^2)$ per triangulation. So $k$ iterations cost $O(k n^2)$ here and $O(k n \log n)$ with a fast Delaunay code, and in practice only a small fraction of the iterations retriangulate. The number of iterations $k$ is not bounded by any proof; in the runs above it grew from 90 to 197 when the number of points grew about four times. The space is $O(n)$.

## Properties

- **Simple.** The whole method is a force loop around a Delaunay call. The original MATLAB code has about one page.
- **Implicit geometry.** The domain enters only through $f_d$, so set operations on distance functions, such as minimum for union and maximum for intersection, give new domains at no cost.
- **Exact Delaunay output, proved.** Each triangulation is exactly Delaunay for the returned points.
- **No convergence proof.** The stopping test may never be met; the cap is needed.
- **Good shapes in practice.** The measured smallest mean ratio is above 0.8 on the test domains, but no bound is proved.

## Variants and improvements

- **Size functions.** With a relative size function $h(x)$, each bar uses $L_0 = h(\text{midpoint}) \cdot F_\text{scale} \cdot$ a common scale, and L1 rejects grid points with probability that depends on $h$. A [mesh sizing function](/mesh-sizing-function/) gives $h$.
- **Higher dimensions.** The same loop with a tetrahedral Delaunay code makes tetrahedral meshes. Slivers are common in 3D, because the forces do not see them.
- **Surfaces.** Points can be projected onto the zero set of $f_d$ to mesh an implicit surface.
- **Energy view.** [Optimal Delaunay triangulation](/optimal-delaunay-triangulation/) and the [centroidal Voronoi tessellation](/centroidal-voronoi-tessellation/), computed by [Lloyd's algorithm](/lloyds-algorithm/), move points by the gradient of an energy and come with a proof that the energy goes down. DistMesh has no such energy for its repulsive only forces.

## When to use it

Use it for a quick mesh of a domain that has a simple distance function: disks, rectangles with holes, set operations of such shapes, or a level set from a simulation. It is good for teaching and for small problems, where the short code and the regular triangles matter more than speed. For large meshes, sharp corners that are not given as fixed points, or a need for a proved angle bound, use [Delaunay refinement](/delaunay-refinement/), [advancing front mesh generation](/advancing-front-mesh-generation/) or [isosurface stuffing](/isosurface-stuffing/).

## Pitfalls

- **Corners not fixed.** A corner of the domain that is not in the fixed list is cut off: the points near it are pushed to the two sides, and the mesh rounds the corner.
- **Thin features.** The centroid test can keep a triangle that spans a notch narrower than $h_0$. Only for a convex domain does the test prove that the triangles are inside.
- **Inexact distance.** With an approximate $f_d$, such as the maximum of the distances to the sides of a square near a corner, the projection may not land on the boundary in one step.
- **No convergence.** The stopping test may never be met. Always cap the iterations and check the final mesh.
- **Float predicates.** With float in-circle tests, a retriangulation of nearly cocircular points, as on the initial equilateral grid, can be wrong. Use exact predicates.
- **Wrong scale factor.** With $F_\text{scale} \le 1$, many bars do not push, the points do not reach the boundary, and the boundary triangles get bad.

## Implementations

## History

Per-Olof Persson and Gilbert Strang published DistMesh in SIAM Review in 2004 with a MATLAB code of about one page, as part of Persson's doctoral work on mesh generation with distance functions. The idea of a truss of springs that moves the points of a mesh is older, but the combination of a signed distance function, a repulsive only force law and Delaunay retriangulation in a few lines of code made the method popular for teaching and research. The Delaunay step goes back to the insertion methods that Adrian Bowyer and David Watson published, separately, in 1981.

## References
