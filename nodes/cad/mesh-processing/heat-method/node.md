---
tag: MWDDTN
kind: algorithm
slug: heat-method
name: Heat method
aliases:
- heat method for geodesics
area: cad/mesh-processing
level: research
summary: Crane, Weischedel and Wardetzky's geodesic distance by a short heat flow, normalizing its gradient and solving a Poisson equation, with two sparse linear solves.
solves: [discrete-geodesic-problem]
model: real-ram
complexity:
  vars: {n: the number of vertices, s: the number of solver iterations}
  time: {worst: Θ(s n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2013
  people: [Keenan Crane, Clarisse Weischedel, Max Wardetzky]
  note: They turned Varadhan's link between heat flow and distance into a method with two sparse linear solves, using the direction of the heat gradient and not its size.
prereqs: [cotangent-laplacian, heat-equation, poisson-equation, discrete-geodesic-problem]
see_also: [mmp-geodesic-algorithm, fast-marching-method, eikonal-equation, implicit-fairing, dijkstra, cholesky-decomposition, conjugate-gradient-method, backward-euler-method]
sources:
  - paper: doi:10.1145/2516971.2516977
    title: Keenan Crane, Clarisse Weischedel and Max Wardetzky, Geodesics in heat, a new approach to computing distance based on heat flow, ACM Transactions on Graphics 32(5), 2013, article 152
    locator: the three steps of the method, the choice t = h^2, the discrete gradient and divergence on triangle meshes, and the boundary conditions
  - paper: doi:10.1002/cpa.3160200210
    title: S. R. S. Varadhan, On the behavior of the fundamental solution of the heat equation with variable coefficients, Communications on Pure and Applied Mathematics 20(2), 1967, 431 to 455
    locator: the limit of -4t log k(t, x, y) as t goes to 0, which is the square of the Riemannian distance
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 3, Differential geometry (the cotangent Laplacian, the lumped mass matrix and the gradient of a linear function on a triangle)
---

The heat method computes an approximate geodesic distance from a set of source vertices to every vertex of a triangle mesh, with two sparse linear solves and one pass over the faces. It lets heat flow from the sources for a short time $t$. The heat $u$ itself is a poor guide to distance, but its gradient points away from the sources. So the method keeps only the direction, $X = -\nabla u/|\nabla u|$, a field of unit vectors along which distance grows at rate 1. Then it finds the function $\varphi$ whose gradient is closest to $X$, by solving a Poisson equation. Both matrices are built from the [cotangent Laplacian](/cotangent-laplacian/), do not depend on the source, and can be factored once. Then each new source costs two back-substitutions. This is a solution method for the [discrete geodesic problem](/discrete-geodesic-problem/). It is not exact, and its error shrinks as the mesh is refined.

## In plain words

Touch the surface at one point with something hot and wait a moment. The heat spreads out. Close to the point it is hot, farther away it is cooler. The heat does not tell you the distance well, because it fades in a complicated way. But the direction in which it gets cooler always points straight away from the hot point.

So the method warms the surface for a moment, notes on each triangle only the direction in which it gets cooler, and throws away how fast. That gives arrows of length one that point away from the start. A distance is a function that grows by exactly one per unit step along such arrows. The last step finds the function whose slope best matches the arrows, which is one more system of equations. Its values are the distances.

## The problem

The input is a connected triangle mesh with positions $x_1, \ldots, x_n$, a nonempty set $S$ of source vertices, and a time $t > 0$, by default $t = h^2$ for the mean edge length $h$. The output is a value $\varphi_i$ at each vertex that approximates the geodesic distance from vertex $i$ to $S$ on the surface, with $\min_{s \in S}\varphi_s = 0$. Exact distances are the task of the [MMP algorithm](/mmp-geodesic-algorithm/). The heat method trades exactness for two linear solves.

## The algorithm

Let $C = -L$ be the cotangent stiffness matrix, $M$ the lumped mass matrix (one third of the face areas at each vertex), and $\delta$ the vector with 1 at the sources and 0 elsewhere. On a face with area $A_f$, unit normal $N$, and the edge $e_i$ opposite vertex $i$ taken in the order of the face, the gradient of the linear interpolant of $u$ is $\nabla u = \frac{1}{2A_f}\sum_i u_i\, (N \times e_i)$. For a vector $X_f$ on each face, the integrated divergence at vertex $i$ is

$$(\nabla \cdot X)_i = \frac{1}{2}\sum_{f \ni i}\big(\cot\theta_1\,(e_1 \cdot X_f) + \cot\theta_2\,(e_2 \cdot X_f)\big),$$

where $e_1$, $e_2$ are the two edges of $f$ out of $i$ and $\theta_1$, $\theta_2$ the angles of $f$ opposite them.

```pseudo id=main
HEAT-METHOD(x[1 .. n], faces, S, t)
L1  t ← h² for the mean edge length h, if not given
L2  C, M ← the cotangent stiffness and the lumped mass matrices
L3  solve (M + t C) u = δ_S                         ▷ one backward Euler step of heat flow
L4  for each face f do X_f ← −∇u / |∇u|              ▷ the unit direction away from S
L5  b_i ← (∇ · X)_i for each vertex i
L6  solve C φ = −b with φ_s = 0 for one source s     ▷ the Poisson equation
L7  φ ← φ − min over s ∈ S of φ_s
    return φ
```

Line L3 is one [backward Euler](/backward-euler-method/) step of the [heat equation](/heat-equation/) $\dot u = \Delta u$ from the initial heat $\delta_S$. The matrix $M + tC$ is symmetric positive definite. Line L6 is the weak form of the [Poisson equation](/poisson-equation/) $\Delta\varphi = \nabla \cdot X$. The matrix $C$ has the constants in its kernel, so one value is fixed. The code solves both systems by [conjugate gradients](/conjugate-gradient-method/), or by a dense solver for tests.

## Example

**A flat square.** Take the unit square as an $8 \times 8$ grid of right triangles, with the diagonals from $(i, j)$ to $(i + 1, j + 1)$, and the source at the corner $(0, 0)$. On a flat convex region the geodesic distance is the straight-line distance. The table lists measured values of the heat method and of [Dijkstra's algorithm](/dijkstra/) on the edge graph.

| point | exact | heat method | edge Dijkstra |
|---|---|---|---|
| $(1/2, 1/2)$ | $0.7071$ | $0.7246$ | $0.7071$ |
| $(1, 1/4)$ | $1.0308$ | $0.9836$ | $1.1036$ |
| $(1, 1/2)$ | $1.1180$ | $1.0856$ | $1.2071$ |
| $(1, 1)$ | $1.4142$ | $1.4276$ | $1.4142$ |
| $(1, 0)$ | $1$ | $0.9286$ | $1$ |

Edge paths are exact along the grid lines and the diagonals, and too long in every other direction, $1.2071 = \frac{\sqrt{2}}{2} + \frac{1}{2}$ instead of $\frac{\sqrt{5}}{2}$ at $(1, \frac{1}{2})$, and no refinement removes this. The heat method errs in both directions but has the smaller mean error, $0.021$ against $0.036$. Its largest errors are on the border, as at $(1, 0)$, where the free (Neumann) boundary condition of the heat flow bends the gradient. On the $4 \times 4$, $8 \times 8$ and $16 \times 16$ grids the measured mean error is $0.033$, $0.021$ and $0.014$.

**A sphere.** On the icosphere with 42, 162 and 642 vertices on the unit sphere, the measured mean error against the great-circle distance is $0.096$, $0.045$ and $0.023$. It halves with each refinement, so it is about proportional to the edge length. At the antipode of the source of the 162-vertex sphere the method gives $3.045$ against $\pi$.

## Correctness

The method is an approximation. These parts are proved in the correctness file:

- **Both systems have unique solutions.** $M + tC$ is symmetric positive definite. $C$ restricted to the vertices other than one pinned vertex is positive definite on a connected mesh.
- **The Poisson step inverts the gradient.** If $X$ is the gradient of a piecewise linear function $\varphi^0$, then line L5 gives $b = -C\varphi^0$, and lines L6 and L7 return $\varphi^0$ up to a constant. So the only errors come from $X$ not being a gradient field of unit length. The tests check this identity on random functions.
- **Least squares.** In general, line L6 returns the piecewise linear $\varphi$ that minimizes $\int |\nabla\varphi - X|^2\,dA$.
- **Why it works in the limit.** For a smooth surface, Varadhan's formula says that the heat kernel satisfies $-4t\log k_t(x, y) \to d(x, y)^2$ as $t \to 0$. So for small $t$, $\nabla u$ is nearly parallel to $-\nabla d$, and $X$ is nearly $\nabla d$, which has unit length. Crane, Weischedel and Wardetzky analyse the error when the mesh is refined with $t = mh^2$. This page does not prove convergence on meshes and gives no proved rate.

The errors of the examples are measured, not proved.

## Complexity

Building $C$, $M$, the gradients and the divergence takes $O(n)$ time. The two solves dominate. With [conjugate gradients](/conjugate-gradient-method/) each takes $s$ iterations of $O(n)$ work, so $\Theta(sn)$ in total on the [real RAM](/real-ram/), with $s$ of order $\sqrt{n}$ for a well-shaped mesh. With a sparse [Cholesky factorization](/cholesky-decomposition/), the two factorizations cost about $O(n^{1.5})$ time once, by nested dissection, and each new source set then costs two back-substitutions, about $O(n \log n)$. This reuse is the main practical gain: the factors depend only on the mesh. The extra space is $\Theta(n)$ for conjugate gradients, more for the factors.

## Properties

- **Approximate.** The error is not bounded by a constant times the true distance on a fixed mesh. It goes to 0 under refinement, at about first order in $h$ in the measured examples.
- **Smooth output.** The result has no sharp crease at the cut locus, where two shortest paths meet, because the heat flow smooths it. A larger $t$ smooths more.
- **Any set of sources.** A point, a curve of vertices, or a region, at the same cost.
- **Not monotone.** Nothing forces $\varphi \ge 0$ or the triangle inequality. Small negative values near a source can occur.
- **Works on other domains.** The same three steps apply to point clouds, polygon meshes and grids, wherever a Laplacian, a gradient and a divergence exist.

## Variants and improvements

- **Boundary conditions.** On a mesh with a border, Crane et al. suggest the mean of the heat solutions with zero Neumann and zero Dirichlet conditions, which reduces the error near the border seen in the flat example.
- **The time step.** $t = mh^2$ with $m = 1$ is the default. A larger $m$ gives a smoother result, and a smaller $m$ follows the true distance more closely until the mesh is too coarse to resolve the heat.
- **Intrinsic Delaunay meshes.** Computing $C$ on an intrinsic Delaunay triangulation of the same surface keeps the weights nonnegative and improves accuracy on poor meshes.
- **Exact methods.** The [MMP algorithm](/mmp-geodesic-algorithm/) and its successors compute exact distances, at a cost of $O(n^2 \log n)$ in the worst case.
- **Fast marching.** The [fast marching method](/fast-marching-method/) solves the [eikonal equation](/eikonal-equation/) $|\nabla d| = 1$ directly, in $O(n \log n)$ time, with first-order error and an extra step on obtuse triangles.

## When to use it

Use it when many distance queries are made on one fixed mesh, because the factorizations are reused, and when a smooth, approximate distance is enough, as for texture placement, sampling, mesh segmentation or the descriptors of shape analysis. Use the [MMP algorithm](/mmp-geodesic-algorithm/) when exact distances or exact shortest paths are needed, and [Dijkstra](/dijkstra/) on the edge graph only for a fast upper bound.

## Pitfalls

- **The sign of the Laplacian.** With $L = -C$, the Poisson equation is $L\varphi = \nabla \cdot X$, that is $C\varphi = -\nabla \cdot X$. With the wrong sign, the result is minus the distance, and the shift of line L7 hides the error until the values are compared.
- **Forgetting to normalize.** Solving the Poisson equation with $-\nabla u$ itself, not its direction, gives a smooth function that is not a distance.
- **A $t$ too small for the mesh.** If $t \ll h^2$, the heat does not reach past the first ring of the source, $\nabla u$ is near 0 elsewhere, and the directions are noise from rounding.
- **Degenerate and obtuse triangles.** They give huge or negative cotangents and a poorly conditioned system. Remesh, or use an intrinsic Delaunay triangulation.
- **Disconnected meshes.** The heat never reaches another part, and $C$ has one constant per part in its kernel. Run the method on each part.
- **The border.** Near a border the error is larger, as in the example.

## Implementations

## History

Varadhan proved in 1967 that the heat kernel on a Riemannian manifold determines the distance: $-4t \log k_t(x, y)$ tends to $d(x, y)^2$ as $t \to 0$. Using the formula directly on a mesh needs a very small $t$ and is sensitive to error, because $\log u$ is taken of tiny values. In 2013 Crane, Weischedel and Wardetzky observed that only the direction of $\nabla u$ is needed. That direction is already accurate for $t$ of the order of $h^2$, and a Poisson solve recovers the distance from it. They called the method the heat method, showed its convergence under refinement, and applied it to triangle meshes, polygon meshes and point clouds.

## References
