---
tag: 6F02H1
kind: algorithm
slug: implicit-fairing
name: Implicit fairing
aliases:
- mean curvature flow smoothing
- Desbrun fairing
area: cad/mesh-processing
level: advanced
summary: Desbrun, Meyer, Schröder and Barr's smoothing by backward Euler steps of mean curvature flow with the cotangent Laplacian, stable for large time steps.
model: real-ram
complexity:
  vars: {n: the number of vertices, K: the number of steps, s: the number of solver iterations per step}
  time: {worst: Θ(K s n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1999
  people: [Mathieu Desbrun, Mark Meyer, Peter Schröder, Alan H. Barr]
  note: They replaced the explicit Laplacian steps of earlier smoothing by one implicit step of a linear system, and the uniform weights by the cotangent weights of mean curvature flow.
prereqs: [cotangent-laplacian, laplacian-smoothing, backward-euler-method, conjugate-gradient-method]
see_also: [taubin-smoothing, heat-equation, finite-element-method, cholesky-decomposition, discrete-gaussian-curvature, surface-curvature, liepa-hole-filling, heat-method]
sources:
  - paper: doi:10.1145/311535.311576
    title: Mathieu Desbrun, Mark Meyer, Peter Schröder and Alan H. Barr, Implicit fairing of irregular meshes using diffusion and curvature flow, Proceedings of SIGGRAPH 99, 1999, 317 to 324
    locator: the implicit integration of the diffusion equation, the curvature normal from the cotangent formula, the volume correction, and the comparison with explicit steps
  - paper: doi:10.1007/978-3-662-05105-4_2
    title: Mark Meyer, Mathieu Desbrun, Peter Schröder and Alan H. Barr, Discrete differential-geometry operators for triangulated 2-manifolds, in Visualization and Mathematics III, Springer, 2003, 35 to 57
    locator: the mean curvature normal as the cotangent Laplacian of the positions, with the vertex areas
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 4, Smoothing (implicit smoothing with the symmetric system of mass and stiffness matrices)
---

Implicit fairing smooths a mesh by taking backward Euler steps of mean curvature flow. Each step solves the sparse linear system

$$(M + \Delta t\, C)\, x^{\text{new}} = M\, x^{\text{old}}$$

for each coordinate, where $C = -L$ is the stiffness matrix of the [cotangent Laplacian](/cotangent-laplacian/) and $M$ the diagonal matrix of vertex areas, both taken at the old positions. A [Laplacian smoothing](/laplacian-smoothing/) step is the explicit form of the same flow and is stable only for small steps. The implicit step is stable for every $\Delta t > 0$, so one step can do the work of many. With the cotangent weights, the motion follows the mean curvature normal $-2Hn$. A flat region does not move, even on an irregular mesh. Each step costs one solve with a symmetric positive definite matrix, by [conjugate gradients](/conjugate-gradient-method/) or a sparse [Cholesky factorization](/cholesky-decomposition/).

## In plain words

Plain smoothing moves each corner a small step toward its neighbours. If the step is too large, corners overshoot, swing back and forth, and the mesh blows up. So many small steps are needed, and a smooth result takes a long time.

Implicit fairing asks a different question: where should every corner be, so that one step back from there leads to where the corners are now? All corners are found at once, by solving one system of equations. The answer is never wild, even for a very large step, because a large step just means more smoothing.

The weights come from the angles of the triangles, not only from who is next to whom. On a flat part of the mesh the corners already balance, so they stay where they are, even if the triangles have very different shapes. On a curved part they move inward along the bend.

## The problem

The input is a triangle mesh with positions $x_1, \ldots, x_n$, a time step $\Delta t > 0$, a number of steps $K$, and a set $F$ of fixed vertices, by default the border. The output is new positions with the same connectivity, after $K$ steps of the discrete flow $M\dot x = -Cx$ on the free vertices, with the fixed vertices as boundary data. Larger $\Delta t K$ means more smoothing. There is no single target: the user picks the amount.

## The algorithm

Let $w_{ij} = \frac{1}{2}(\cot\alpha_{ij} + \cot\beta_{ij})$ be the cotangent weights, $C_{ij} = -w_{ij}$ for an edge $ij$, $C_{ii} = \sum_j w_{ij}$, and $M_{ii}$ one third of the area of the faces at $i$. $R$ is the set of free vertices.

```pseudo id=main
IMPLICIT-FAIR(x[1 .. n], faces, Δt, K, F)
L1  F ← the border vertices if not given; R ← the other vertices
L2  for k ← 1 to K do
L3      C, M ← the stiffness and mass matrices at the current x
L4      A ← (M + Δt C) restricted to the rows and columns of R
L5      for each coordinate: b ← M_R x_R − Δt C_RF x_F; solve A y = b
L6      x_R ← y
L7      optionally scale x about its centroid so that the volume is the starting volume
    return x
```

$A$ is symmetric. It is positive definite because $C$ is positive semidefinite, being the matrix of the Dirichlet energy $\frac{1}{2}x^\top C x$, and $M$ is positive. So [conjugate gradients](/conjugate-gradient-method/) applies, and the code uses it, started from the old positions.

With *uniform* weights, $C = D - A_{\text{adj}}$ is the [graph Laplacian](/laplacian-matrix/) and $M = D$ the valences. The step is then $(I + \Delta t\, G)x^{\text{new}} = x^{\text{old}}$ with $G = I - D^{-1}A_{\text{adj}}$, the implicit form of Laplacian smoothing. The code offers both, and a dense exact solver for tests.

## Example

**The octahedron, uniform weights.** The octahedron with vertices $(\pm 1, 0, 0)$, $(0, \pm 1, 0)$, $(0, 0, \pm 1)$ has four neighbours per vertex, summing to 0, so $Gx = x$ for each coordinate. The step is $(1 + \Delta t)x^{\text{new}} = x$, so $x^{\text{new}} = x / (1 + \Delta t)$, exactly. With $\Delta t = 3$, the octahedron shrinks to $\frac{1}{4}$ of its size. The explicit step with the same $\Delta t$ gives $x + 3(0 - x) = -2x$: it turns the octahedron inside out and doubles it, and repeating it blows up.

**The octahedron, cotangent weights.** Every angle is $60°$, so $w_{ij} = \cot 60° = \frac{1}{\sqrt{3}}$, and $(Cx)_i = \frac{1}{\sqrt{3}}(4x_i - 0) = \frac{4}{\sqrt{3}}x_i$. Each face has area $\frac{\sqrt{3}}{2}$, so $M_{ii} = \frac{4}{3} \cdot \frac{\sqrt{3}}{2} = \frac{2}{\sqrt{3}}$. The step is $(\frac{2}{\sqrt{3}} + \frac{4\Delta t}{\sqrt{3}})x^{\text{new}} = \frac{2}{\sqrt{3}}x$, so $x^{\text{new}} = x / (1 + 2\Delta t)$. After a first step to size $s$, the areas are $s^2$ times larger and the weights the same, so the second step multiplies by $s^2 / (s^2 + 2\Delta t)$. This matches the smooth flow of a sphere of radius $r$, which moves inward with speed $2/r$, so that $r^2$ falls by $4$ per unit time.

**A sphere.** On the icosphere with 162 vertices, one step with $\Delta t = 0.01$, $1$ and $10$ gives measured radii within 1 percent of $1/(1 + 2\Delta t)$, that is $0.980$, $0.333$ and $0.0476$. With the volume correction of line L7, the volume stays at its start value. On the same sphere with 10 percent radial noise, one corrected step with $\Delta t = 0.001$, $0.003$ and $0.01$ lowers the measured relative spread of the radii from $0.0285$ to $0.0275$, $0.0257$ and $0.0215$.

## Correctness

These are proved in the correctness file:

- **The step solves the system.** Lines L4 to L6 give the unique $x_R$ with $(M + \Delta t C)x = Mx^{\text{old}}$ on the free rows, with $x_F$ fixed. The matrix is symmetric positive definite, so the solution exists, is unique, and conjugate gradients converge to it. The tests compare conjugate gradients with dense Gaussian elimination.
- **It is the backward Euler step.** The system is $M\frac{x^{\text{new}} - x^{\text{old}}}{\Delta t} = -Cx^{\text{new}}$, the backward Euler step of $M\dot x = -Cx$ with the matrices frozen at the start of the step.
- **Unconditional stability.** For fixed $C$ and $M$, the step does not increase the energy norm $x^\top M x$, and each eigenmode of $M^{-1}C$ with eigenvalue $k$ is multiplied by $\frac{1}{1 + \Delta t k} \in (0, 1]$, for every $\Delta t > 0$. The explicit step multiplies it by $1 - \Delta t k$, which is less than $-1$ when $\Delta t > 2/k$.
- **A maximum principle.** If all weights are nonnegative, as with uniform weights or on a Delaunay mesh, each new position is a convex combination of the old positions and the fixed positions. With uniform weights and no fixed vertex, $\sum_i d_i x_i$ is also kept. The tests check both exactly.
- **Flat regions stay.** With cotangent weights, $(Cx)_i = 0$ at each inner vertex of a planar mesh, so a planar mesh with a fixed border is a fixed point for every $\Delta t$. The uniform weights move it inside the plane.

The tests also check the cotangent matrix against the Hessian of the Dirichlet energy, computed triangle by triangle. How much noise a step removes, and how close the sphere is to the smooth flow, is measured, not proved.

## Complexity

Building $C$ and $M$ takes $O(n)$ time, because a manifold mesh has $O(n)$ faces. The matrix has at most $7n$ nonzero entries, and one product with it costs $O(n)$. Conjugate gradients need $s$ iterations per coordinate, so one step costs $\Theta(sn)$, and $K$ steps $\Theta(Ksn)$ on the [real RAM](/real-ram/). The number $s$ depends on the condition number of $M + \Delta t C$, about $1 + \Delta t\, k_{\max}$, and grows like $\sqrt{\Delta t}/h$ for edge length $h$. A sparse Cholesky factorization costs more once, about $O(n^{1.5})$ time for a planar-like mesh with nested dissection, and then $O(n \log n)$ per solve, but it must be redone when $C$ and $M$ change. The extra space is $\Theta(n)$ for conjugate gradients.

## Properties

- **Stable for any step.** Large $\Delta t$ gives strong smoothing, never a blow-up.
- **Geometric.** With cotangent weights, the result depends on the shape, not on the mesh. Flat regions do not move, and on a curved region the motion is along the normal, with speed proportional to the mean curvature.
- **Still shrinks.** Mean curvature flow decreases the area of every closed surface, and a sphere shrinks to a point in finite time. So the volume correction of line L7 is part of the method in practice.
- **Not exact.** The cotangent weights need square roots, and the solver is iterative. With uniform weights and rational input, the dense solver gives exact results.
- **Semi-implicit.** The matrices are taken at the old positions, so the step is linear. The true implicit step of the nonlinear flow would need Newton iterations.

## Variants and improvements

- **Uniform weights.** The implicit form of [Laplacian smoothing](/laplacian-smoothing/), cheaper, but with tangential drift.
- **Normalized operator.** Desbrun et al. divided the cotangent sum by the area of the one-ring, which gives a nonsymmetric matrix. They solved it with a preconditioned biconjugate gradient method. The symmetric form $M + \Delta t C$ used here is the later standard.
- **Fixed matrices.** Compute $C$ and $M$ once and factor $M + \Delta t C$ once. All steps then reuse the factor. This is the heat equation on the first mesh, not mean curvature flow, but it is often good enough.
- **Higher order.** Replace $C$ by $CM^{-1}C$, the bi-Laplacian, for smoother results with tangent continuity at a fixed border, as used for [hole filling](/hole-filling/) and fairing patches.
- **Conformalized flow.** Keep the stiffness matrix of the first mesh and update only the mass matrix. Kazhdan, Solomon and Ben-Chen (2012) showed that this avoids the singularities that mean curvature flow forms on some shapes.
- **Anisotropic diffusion.** Lower the weights across sharp features, so that creases are kept.

## When to use it

Use it to remove noise from a mesh with irregular triangles, where the uniform weights would drift, and when strong smoothing is wanted in few steps. It also fairs the patch of a filled hole inside a fixed border. For a quick, cheap cleanup with no solver, use [Taubin smoothing](/taubin-smoothing/). The same matrices $M$ and $C$, in one heat step, give the first solve of the [heat method](/heat-method/) for geodesic distance.

## Pitfalls

- **Degenerate triangles.** A triangle with an angle near $0$ or $180°$ has a huge cotangent and makes the system badly conditioned. Remesh first, or clamp the weights.
- **Negative weights.** With obtuse triangles, some $w_{ij} < 0$. The system is still positive definite, but the maximum principle fails, and a new position can leave the convex hull of the old ones.
- **Shrinking to a point.** Without the volume correction, a closed mesh shrinks, and with a large enough $\Delta t$ it shrinks almost to a point in one step, as for the sphere above.
- **Forgetting the mass matrix.** Solving $(I + \Delta t C)x^{\text{new}} = x$ makes the smoothing depend on the size of the triangles, and a refined region moves faster.
- **Singularities.** Mean curvature flow pinches thin necks, as on a dumbbell, and the mesh degenerates there.
- **A free border.** Without fixed vertices, the border of an open mesh shrinks inward along the surface.

## Implementations

## History

Diffusion-based mesh smoothing goes back to [Laplacian smoothing](/laplacian-smoothing/) and to Taubin's 1995 signal processing view of it. In 1999 Desbrun, Meyer, Schröder and Barr made two changes. First, they took implicit steps of the diffusion, by solving a sparse linear system, and so allowed large time steps. Second, they replaced the uniform weights by the cotangent formula for the mean curvature normal, which goes back to Pinkall and Polthier (1993), so that the flow depends on the geometry and not on the sampling. They also rescaled the mesh after each step to keep its volume. The method became the standard reference for mesh fairing, and the symmetric form with mass and stiffness matrices became common through the later finite element view of the cotangent Laplacian.

## References
