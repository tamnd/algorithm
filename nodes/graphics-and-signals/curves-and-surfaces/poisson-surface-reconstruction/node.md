---
tag: 6BENWT
kind: algorithm
slug: poisson-surface-reconstruction
name: Poisson surface reconstruction
aliases:
- Poisson reconstruction
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Reconstructs a closed surface from oriented points by solving a Poisson equation for a smoothed indicator function of the solid, then extracting one of its level sets.
solves: [surface-reconstruction]
model: real-ram
complexity:
  vars: {n: the number of points, m: the number of grid nodes per axis}
  time: {worst: O(n + m^4), average: O(n + m^4), best: Θ(n + m^3)}
  space: {extra: Θ(n + m^3)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 2006
  people: [Michael Kazhdan, Matthew Bolitho, Hugues Hoppe]
  note: Kazhdan, Bolitho and Hoppe presented the method at the Eurographics Symposium on Geometry Processing in 2006; Kazhdan and Hoppe added screening in 2013.
prereqs: [surface-reconstruction, poisson-equation, galerkin-method, octree]
see_also: [ball-pivoting-algorithm, marching-cubes, marching-tetrahedra, conjugate-gradient-method, multigrid-method, b-spline, implicit-surface, finite-element-method]
sources:
  - paper: "Michael Kazhdan, Matthew Bolitho and Hugues Hoppe, Poisson surface reconstruction, Proceedings of the Fourth Eurographics Symposium on Geometry Processing (SGP 2006), 61 to 70, 2006"
    locator: the whole paper (the indicator function and its gradient, the vector field from the samples, the octree and the B-spline basis, the solver, the iso value, non-uniform samples)
  - paper: doi:10.1145/2487228.2487237
    title: Michael Kazhdan and Hugues Hoppe, Screened Poisson surface reconstruction, ACM Transactions on Graphics 32(3), article 29, 2013
    locator: the whole paper (the screening term that pulls the surface to the points, and the solver that is linear in the number of points)
  - paper: doi:10.1145/142920.134011
    title: Hugues Hoppe, Tony DeRose, Tom Duchamp, John McDonald and Werner Stuetzle, Surface reconstruction from unorganized points, Computer Graphics (SIGGRAPH 92 Proceedings) 26(2), 71 to 78, 1992
    locator: the whole paper (an earlier implicit method with a signed distance from tangent planes, and the estimation and orientation of normals)
---

Poisson surface reconstruction turns a set of points with outward normals into a closed surface. It does not connect the points. Instead, it looks for the indicator function $\chi$ of the solid, which is 1 inside and 0 outside: the gradient of $\chi$ is zero away from the surface and points inward across it, so the inward normals of the samples are a picture of $\nabla \chi$. The method finds the function whose gradient is closest to that vector field, which means solving a [Poisson equation](/poisson-equation/) $\Delta \chi = \nabla \cdot V$, and returns a level set of $\chi$. Since the whole solid is fitted at once, the result is closed and smooth, noise is averaged out, and holes in the data are filled.

## In plain words

Imagine that each sample point is a small arrow on the surface that points out of the object. We want a function on all of space that is high inside the object and low outside. Such a function rises when you walk from outside to inside, and the arrows tell us in which direction that rise happens.

So spread the arrows out a little, so that they form a smooth flow, and ask: which function rises most like this flow? There is one best answer, and it comes from solving one large linear system on a grid. The surface is the place where this function is halfway between its inside and its outside values. Gaps in the data are bridged, because the function is defined everywhere.

## The problem

The input is $n$ points $s_1, \ldots, s_n$ that sample the boundary $\partial M$ of a solid $M$, with outward unit normals $\nu_1, \ldots, \nu_n$, and a grid resolution. The output is a closed [polygon mesh](/polygon-mesh/) that approximates $\partial M$. This is [surface reconstruction](/surface-reconstruction/) by an [implicit surface](/implicit-surface/): the mesh is a level set of a function.

The method rests on one identity. If $\tilde\chi = \chi_M * F$ is the indicator function smoothed by a filter $F$, then by the divergence theorem

$$\nabla \tilde\chi(q) = -\int_{\partial M} F(q - p)\, \nu(p)\, dp,$$

and the integral can be estimated from the samples as $V(q) = -\sum_s F(q - s)\, \nu_s\, |P_s|$, where $|P_s|$ is the area of the surface near $s$. A vector field $V$ that comes from noisy data is not in general a gradient, so the method asks for the $\chi$ that minimizes $\int \lVert \nabla \chi - V \rVert^2$, whose Euler-Lagrange equation is the Poisson equation $\Delta \chi = \nabla \cdot V$.

## The algorithm

This page describes the method on a uniform grid of $m^3$ nodes with trilinear hat functions $\varphi_o$, the version that the implementation uses. The paper uses an adaptive [octree](/octree/) of depth $D$, with a quadratic [B-spline](/b-spline/) basis on each node, refined only near the samples.

```pseudo id=main
POISSON-RECONSTRUCTION(s, ν, D)
L1  grid ← m = 2^D + 1 nodes per axis on a cube around the points with a margin, spacing h
L2  for each sample s: add -ν_s φ_o(s) to V_o for the 8 nodes o of the cell of s
L3  b_o ← ∫ V · ∇φ_o for every interior node o, where V = Σ_o V_o φ_o
L4  solve L x = b with L_{o o'} = ∫ ∇φ_o · ∇φ_{o'} by conjugate gradients, x = 0 on the border
L5  γ ← the mean of χ(s) over the samples, where χ = Σ_o x_o φ_o
L6  extract the level set {χ = γ}, with χ > γ inside, by marching tetrahedra
L7  return the mesh
```

Line L4 is the [Galerkin method](/galerkin-method/) for the Poisson equation: $\chi = \sum_o x_o \varphi_o$ minimizes $\int \lVert \nabla \chi - V \rVert^2$ over the span of the interior $\varphi_o$ exactly when $\int \nabla \chi \cdot \nabla \varphi_{o'} = \int V \cdot \nabla \varphi_{o'}$ for every interior $o'$. Both integrals are products of the 1D integrals of hat functions on spacing $h$: $\int \varphi_i \varphi_j = h \cdot \{\tfrac23, \tfrac16\}$, $\int \varphi_i' \varphi_j' = \tfrac1h \{2, -1\}$ and $\int \varphi_i \varphi_j' = \pm\tfrac12$, for $|i - j| = 0, 1$. So $L$ is the 27-point stencil $h (K \otimes M \otimes M + M \otimes K \otimes M + M \otimes M \otimes K)$, symmetric and positive definite on the interior nodes, and the [conjugate gradient method](/conjugate-gradient-method/) applies without forming it. Line L5 is the paper's choice of iso value: the samples lie on the surface, so $\chi$ should take one value on them, and their mean is a robust estimate of it. Line L6 can be any [isosurface extraction](/isosurface-extraction/) method; the paper uses [marching cubes](/marching-cubes/) on the octree, and the implementation uses [marching tetrahedra](/marching-tetrahedra/), which guarantees a closed manifold.

## Example

Take 800 points on the unit sphere (a Fibonacci spiral), with their radial normals, and $D = 4$, so $m = 17$ and $h = 0.187$ on a cube of side 3. Conjugate gradients reach a relative residual of $10^{-10}$ in 34 steps. The values of $\chi$ at the samples lie between 0.176 and 0.206, and their mean is $\gamma = 0.189$. Along the positive $x$ axis:

| $x$ | 0 | 0.5 | 0.8 | 0.9 | 1.0 | 1.1 | 1.2 | 1.4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\chi(x, 0, 0)$ | 0.418 | 0.418 | 0.385 | 0.311 | 0.206 | 0.085 | 0.031 | $-0.003$ |

The function is flat inside, flat near 0 outside, and falls across the sphere, where it crosses $\gamma$ at about $x = 1.015$; the inside value is not 1 because the samples are not weighted by area. The mesh has 1586 vertices and 3168 triangles, it is a closed manifold with Euler characteristic 2, every vertex is within 0.044 of the unit sphere, and its volume is 4.198, against $4\pi/3 = 4.189$. When the cap $z > 0.7$ is removed from the input, the output is still a closed sphere: the solid is filled across the hole.

## Correctness

**Claim.** (1) The vector $x$ of line L4 is the unique minimizer of $\int \lVert \nabla \chi - V \rVert^2$ over the functions $\chi = \sum_o x_o \varphi_o$ that are zero on the border of the grid, and conjugate gradients converge to it. (2) If $\gamma > 0$, the output of line L6 is a closed, oriented 2-manifold, the exact level set $\{\chi = \gamma\}$ of the piecewise linear interpolant of the values of $\chi$ at the nodes on the tetrahedra of the grid.

Part (1) is the Galerkin argument: the energy is a convex quadratic in $x$, with Hessian $2L$, and $L$ is positive definite because $\int \lVert \nabla \chi \rVert^2 > 0$ for every non-zero $\chi$ that is zero on the border. Part (2) follows from the correctness of marching tetrahedra, because the border values are $0 < \gamma$, which is outside. The full proof is in [the correctness proof](proofs/correctness.md). What is not guaranteed is that the surface is close to the sampled surface. The output is always closed, even where the input has a real boundary, and for noisy, sparse or wrongly oriented samples it can have the wrong shape or topology; there is no worst case bound on the quality.

## Complexity

The model is the [real RAM](/real-ram/).

- **Time.** Lines L2 and L5 cost $O(n)$. Lines L3 and L6, and each step of conjugate gradients, cost $O(m^3)$. The condition number of $L$ grows like $m^2$, so conjugate gradients need $O(m)$ steps for a fixed relative error, for $O(m^4)$ in all. A [multigrid method](/multigrid-method/) solves the system in $O(m^3)$.
- **Space.** $\Theta(m^3)$ for the grid vectors, and $O(n)$ for the input.
- **Octree.** In the paper the octree is refined to depth $D$ only near the samples, so the number of nodes grows like the area of the surface, about $4^D$ instead of $8^D$. The screened version of 2013 has a solver whose time is linear in the number of points.

## Properties

- **Closed output.** The output is the level set of a function on a box that is zero on the border, so it is always closed. This fills holes, and it also closes surfaces that should stay open, such as a scan of a face.
- **Smooth and robust to noise.** The solution of a global least squares problem averages the noise in the normals and the positions.
- **Normals needed.** The method needs consistently oriented normals. If some normals point inward, the solution has the wrong sign there.
- **Over-smoothing.** The surface does not go through the points. Fine details below the grid spacing are lost, and thin parts can vanish. The screened version adds a term that pulls $\chi$ to $\gamma$ at the samples.
- **Scale of $\chi$.** Without the area weights, the inside value depends on the sampling density, but the level set at the mean sample value does not change much, because the scale cancels.

## Variants and improvements

- **Octree and B-splines.** The original method uses an adaptive octree with a quadratic B-spline basis (the box filter convolved with itself three times) on each node, splats each sample with trilinear weights onto the nodes at the depth of its local sampling density, and weighs the samples by an estimate of that density.
- **Screened Poisson.** Kazhdan and Hoppe add $\alpha \sum_s (\chi(s) - \gamma)^2$ to the energy, which gives a screened Poisson equation, a surface that stays closer to the points, and Dirichlet or Neumann conditions at the border of the box.
- **Multigrid solvers.** Solve from coarse to fine depths, with the coarse solution as the start of the next depth.
- **Streaming and parallel.** Out of core solvers that stream the octree one slice at a time handle scans that do not fit in memory.
- **Other implicit methods.** Hoppe et al. (1992) used the signed distance to the tangent plane of the nearest sample; radial basis functions fit an interpolating implicit function.

## When to use it

Use Poisson reconstruction for scans with noise, uneven density and small holes, when you want a closed, smooth surface and have oriented normals. Use the screened version for sharper detail. Use [ball pivoting](/ball-pivoting-algorithm/) when the mesh must go through the input points or when the data is clean and dense, and trim the Poisson output by sample density when the scanned surface has a real boundary.

## Pitfalls

- **Normals with the wrong sign.** Splatting $+\nu_s$ in line L2 gives $\chi$ low inside and high outside, and line L6 then treats the outside as the inside. Splat $-\nu_s$ (the gradient of the indicator points inward), or splat $+\nu_s$ and extract with $\chi < \gamma$ inside.
- **No border condition.** Solving $L x = b$ over all nodes, without fixing $x = 0$ on the border in line L4, gives a singular system, because adding a constant to $\chi$ does not change $\nabla \chi$. Fix the border values, or fix the mean.
- **A fixed iso value.** Using $\gamma = 1/2$ instead of the mean over the samples in line L5 gives an empty or wrong surface, because the scale of $\chi$ depends on the sampling density and the filter.
- **Too fine a grid.** A grid much finer than the sampling makes $V$ a set of isolated spikes, and the level set breaks into bubbles around the samples. Choose $h$ larger than the typical distance between samples, or splat at a coarser depth where the samples are sparse.
- **Trusting the hole filling.** The filled parts of the surface are smooth guesses, not data. Mark or trim them if the result is used for measurement.

## Implementations

## History

Kazhdan, Bolitho and Hoppe introduced the method at the Symposium on Geometry Processing in 2006. It built on Kazhdan's earlier work with Fourier methods for the same problem, and on the implicit reconstruction of Hoppe, DeRose, Duchamp, McDonald and Stuetzle from 1992. It became one of the most used reconstruction methods for scanned data. Kazhdan and Hoppe published the screened version in 2013, with the points as soft constraints and a faster solver.

## References
