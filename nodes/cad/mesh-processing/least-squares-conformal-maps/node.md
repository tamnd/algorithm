---
tag: 67C616
kind: algorithm
slug: least-squares-conformal-maps
name: Least squares conformal maps
aliases:
- LSCM
area: cad/mesh-processing
level: advanced
summary: Levy and coauthors' parameterization that minimises the violation of the Cauchy-Riemann equations over the triangles by one linear least squares solve, with free boundary.
solves: [mesh-parameterization]
model: real-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n^3), nested_dissection: O(n^(3/2))}
  space: {extra: O(n^2), nested_dissection: O(n log n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2002
  people: [Bruno Lévy, Sylvain Petitjean, Nicolas Ray, Jérôme Maillot]
  note: Lévy and coauthors gave LSCM in 2002 as part of a method for texture atlases. In the same year Desbrun, Meyer and Alliez gave an energy that gives the same map.
prereqs: [mesh-parameterization, least-squares-problem, normal-equations]
see_also: [tutte-embedding, angle-based-flattening, cotangent-laplacian, floater-mean-value-coordinates, cholesky-decomposition, conjugate-gradient-method, texture-mapping, mesh-segmentation]
sources:
  - paper: doi:10.1145/566654.566590
    title: Bruno Lévy, Sylvain Petitjean, Nicolas Ray and Jérôme Maillot, Least squares conformal maps for automatic texture atlas generation, ACM Transactions on Graphics 21(3), 2002, 362 to 371
    locator: the discrete Cauchy-Riemann energy per triangle, the two pinned vertices, the free boundary, and the segmentation into charts
  - paper: doi:10.1111/1467-8659.00580
    title: Mathieu Desbrun, Mark Meyer and Pierre Alliez, Intrinsic parameterizations of surface meshes, Computer Graphics Forum 21(3), 2002, 209 to 218
    locator: the discrete conformal energy as the Dirichlet energy minus the area, and its natural boundary conditions
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 5, Parametrization (conformal maps with free boundary)
  - paper: doi:10.1561/0600000011
    title: Alla Sheffer, Emil Praun and Kenneth Rose, Mesh parameterization methods and their applications, Foundations and Trends in Computer Graphics and Vision 2(2), 2006, 105 to 171
    locator: the section on conformal methods, which compares LSCM, discrete conformal parameterization and angle-based flattening
---

Least squares conformal maps, LSCM, flatten a triangle mesh with the topology of a disk into the plane by one linear least squares solve. A map is *conformal* if it keeps angles, and for a map of the plane that is the same as the Cauchy-Riemann equations. A piecewise linear map cannot satisfy them on every triangle of a curved mesh, so LSCM minimizes the sum over the triangles of the squared violation, weighted by the area. Two pinned vertices remove the similarities of the plane, which have energy zero, and the boundary is free. The energy equals twice the Dirichlet energy minus twice the area of the image, so the method is the same as the discrete conformal parameterization of Desbrun, Meyer and Alliez. It solves the [mesh parameterization](/mesh-parameterization/) problem with much less distortion than a [Tutte embedding](/tutte-embedding/), but it does not guarantee that the map is one to one.

## In plain words

Draw a small circle on each triangle of the surface. A good flat map turns each circle into a circle, perhaps bigger or smaller, but not into an ellipse. Then the shape of every small part stays the same, and only its size changes.

On a curved surface this is not possible everywhere. LSCM measures for each triangle how far its circle is from a circle in the flat map, and adds up these errors. The flat map with the smallest total is what it returns.

Two points of the map are nailed down first. Without them, the whole map could turn, move or shrink to a point at no cost. The rest of the edge is free, so the outline of the flat map comes out of the shape itself.

## The problem

The input is a triangle mesh $M$ whose triangles all have positive area and whose dual graph (triangles, joined when they share an edge) is connected. Its faces are oriented so that the outward normal follows the right-hand rule. The input also gives two distinct vertices $p$ and $q$ with target points in the plane. The output is a point $U_v = u_v + i v_v \in \mathbb{C}$ for each vertex, and each triangle is mapped linearly. The goal is the map that minimizes the conformal energy below, with $U_p$ and $U_q$ fixed. The map should have every triangle counterclockwise, but LSCM does not guarantee this.

## The algorithm

Each triangle $T$ gets a *frame*: corner points $q_0, q_1, q_2 \in \mathbb{C}$ of a triangle in the plane that is congruent to $T$ and has the same orientation, with area $A_T > 0$. For a triangle in 3D, put $q_0 = 0$, $q_1 = \lVert x_1 - x_0 \rVert$ on the real axis, and $q_2$ in the upper half-plane. Write $\varepsilon_j = q_{j+2} - q_{j+1}$, with indices mod 3. The linear map of the frame to the images $U_{v_j}$ has $\partial_{\bar z} f = i s_T / (4 A_T)$ with

$$s_T = \sum_{j=0}^{2} \varepsilon_j\, U_{v_j},$$

and the Cauchy-Riemann equations hold on $T$ exactly when $s_T = 0$. The energy is

$$E(U) = \sum_T \frac{|s_T|^2}{4 A_T} = \sum_T A_T \big((u_x - v_y)^2 + (u_y + v_x)^2\big).$$

Each $s_T$ is a complex linear form, so it gives two real rows, the real part and the imaginary part. With the pinned values moved to the right side, $E$ is a weighted [least squares problem](/least-squares-problem/) in the $2(n - 2)$ free real unknowns, and the [normal equations](/normal-equations/) give its minimum.

```pseudo id=main
LSCM(M, pins)
L1  for each triangle T of M do (q_0, q_1, q_2), A_T ← FRAME(T)
L2      w_T ← 1 / (4 A_T)
L3      for each of the two real rows ρ of s_T = Σ_j ε_j U_{v_j} do
L4          split ρ into ρ_free, on the free unknowns, and the value c of the pinned terms
L5          N ← N + w_T ρ_freeᵀ ρ_free;  r ← r − w_T c ρ_freeᵀ
L6  solve N x = r
L7  return U, with the pinned values and x
```

$N$ is symmetric and positive semidefinite, and positive definite when the pins fix the map, see the correctness section. Then [Cholesky decomposition](/cholesky-decomposition/) or the [conjugate gradient method](/conjugate-gradient-method/) solves it. Each row has nonzero entries only for the vertices of one triangle, so $N$ has the sparsity of the mesh graph with $2 \times 2$ blocks.

**Degenerate cases.** A triangle with zero area has no frame and is rejected. With fewer than two pins, or two pins on the same point, the similarities that fix the pins have energy zero, and $N$ is singular. A mesh whose dual graph is not connected needs two pins on each part. Two pins also give a singular $N$ when some *development* of the mesh, a map that is a rotation and translation on each triangle, takes both pins to the same point, see the pitfalls. The code raises an error when the elimination finds a zero pivot.

## Example

Take the pyramid with base corners $x_0 = (-1, -1, 0)$, $x_1 = (1, -1, 0)$, $x_2 = (1, 1, 0)$, $x_3 = (-1, 1, 0)$, apex $x_4 = (0, 0, 1)$, and the four side triangles $(0, 1, 4)$, $(1, 2, 4)$, $(2, 3, 4)$, $(3, 0, 4)$. Pin $U_0 = (0, 0)$ and $U_2 = (2, 2)$. The angle at the apex in each triangle is $\arccos(1/3) \approx 70.53°$, so the angles at the apex add up to $282.1°$, not $360°$. No flat map keeps all angles, and the minimum energy is not zero.

| step | value |
|---|---|
| L1, triangle $(0, 1, 4)$ | frame $q = (0, 2, 1 + i\sqrt2)$, $A_T = \sqrt2$, and the same for the other three |
| L2 | $w_T = 1 / (4\sqrt2)$ |
| L3 | $\varepsilon = (-1 + i\sqrt2,\ -1 - i\sqrt2,\ 2)$, so $s_T = (-1 + i\sqrt2) U_0 - (1 + i\sqrt2) U_1 + 2 U_4$ |
| L6 | $U_4 = (1, 1)$, $U_1 = (1 + \tfrac{2\sqrt2}{3}, 1 - \tfrac{2\sqrt2}{3})$, $U_3 = (1 - \tfrac{2\sqrt2}{3}, 1 + \tfrac{2\sqrt2}{3})$ |
| energy | $E = \sqrt2/3 \approx 0.471$, $E_D = 17\sqrt2/6$, image area $8\sqrt2/3$, and $E = 2E_D - 2 \cdot 8\sqrt2/3$ |

The image is a rhombus with the diagonals $U_0 U_2$, of length $2\sqrt2$, and $U_1 U_3$, of length $8/3$, and the four triangles are counterclockwise. The total surface area is $4\sqrt2$, so the pins also fix the scale: the image area is $2/3$ of it.

If the mesh is planar, the energy can be zero. A planar grid with rational coordinates and two pins at distinct points maps exactly to the similarity of the plane that takes the pins to their targets, with $E = 0$. The code of this page checks this in exact rational arithmetic.

**When the arithmetic is floating point.** For a mesh in 3D the frames need square roots, so the solve is in floating point. For the planar grid above, given as points in 3D, the computed map differs from the exact similarity by a relative error of $3 \times 10^{-14}$ on a $4 \times 4$ grid and $7 \times 10^{-13}$ on an $8 \times 8$ grid, with dense elimination on the normal equations. The normal equations square the [condition number](/condition-number/) of the least squares rows, and the subtractions in the elimination lose digits by [catastrophic cancellation](/catastrophic-cancellation/). A QR factorization of the rows, or conjugate gradients on the sparse system, loses fewer digits. Whether a triangle of the result is flipped is the sign of ORIENT2D, the [orientation test](/orientation-test/), on the computed points. Evaluate it exactly, for example with [exact predicates](/shewchuk-expansion-sum/) or with the floats converted to rationals, as the tests of this page do; a sign from a float evaluation of a tiny triangle is not reliable. This is the [robustness problem](/geometric-robustness-problem/) of geometry.

## Correctness

On a triangle, $\partial_{\bar z} f = i s_T / (4 A_T)$, so the term of $T$ is $4 A_T |\partial_{\bar z} f|^2$. It is zero exactly when the linear map is $z \mapsto a z + b$, a similarity that keeps the orientation. Expanding the squares gives $E = 2 E_D - 2 \mathcal{A}$, the Dirichlet energy minus the signed area of the image, twice. $E$ is a sum of squares, so the normal equations give a minimum, which is unique when the only map with $E = 0$ and both pins at 0 is zero. A map with $E = 0$ is a similarity on each triangle, the scale factor is the same across each edge, so it is a development times one constant. So the minimizer is unique exactly when no development takes the two pins to the same point. A planar mesh is its own development, so it is reproduced up to a similarity. The full proof is below.

## Complexity

For $n$ vertices the system has $2(n - 2)$ unknowns, and $N$ has about $7n$ nonzero $2 \times 2$ blocks, one for each vertex and each edge. Building it takes $O(n)$ time, one pass over the triangles. Dense Gaussian elimination, as in the code of this page, takes $O(n^3)$ time and $O(n^2)$ space. The sparsity graph is the mesh graph, which is planar for a disk, so a sparse Cholesky factorization with [nested dissection](/nested-dissection/) takes $O(n^{3/2})$ time and $O(n \log n)$ space. In practice conjugate gradients with a good start, or a multigrid solver, is used for large meshes.

## Properties

- **Free boundary.** Only two vertices are fixed, and the shape of the boundary comes from the minimization. The natural boundary condition says that the map is conformal on the boundary triangles as far as possible.
- **Linear.** One sparse symmetric positive definite solve, with no iteration and no initial guess.
- **Invariant.** A similarity of the targets gives the same similarity of the result. A rigid motion or a uniform scaling of the 3D mesh does not change the result, because $E$ does not change when all frames are scaled by the same factor.
- **Reproduction.** A planar mesh is mapped to a similar copy of itself.
- **Not injective in general.** Triangles can fold, and distant parts of the boundary can overlap.
- **Area not controlled.** Conformal maps of curved surfaces change the scale, and regions of high curvature, such as the tip of a cone, can shrink strongly.

## Variants and improvements

- **Discrete conformal parameterization (Desbrun, Meyer and Alliez 2002).** Minimizes $E_D - \mathcal{A}$, which is $E / 2$, and writes $E_D$ with the [cotangent Laplacian](/cotangent-laplacian/). With the same pins it gives the same map.
- **Spectral conformal parameterization.** Mullen and coauthors (2008) replace the pins by a constraint on the boundary and take an eigenvector of a generalized eigenvalue problem. The result does not depend on the choice of pins.
- **Angle-based flattening.** [ABF](/angle-based-flattening/) optimizes the angles of the flat triangles directly. It is nonlinear but gives lower angle distortion and fewer flips, and a result of ABF is often used where LSCM fails.
- **Cone singularities and boundary control.** Later methods put the curvature at a few cone points or let the user fix the boundary shape or its curvature, which reduces the area distortion of a pure conformal map.
- **Solvers.** For large meshes, sparse direct factorizations, preconditioned conjugate gradients and multigrid solvers replace the dense elimination of the code of this page. How much faster they are depends on the mesh and the solver; the page does not measure it.

## When to use it

Use it for texture atlases and other maps where angles matter more than areas, after a [mesh segmentation](/mesh-segmentation/) into charts that are close to developable. The map is fast and has a free boundary, so it suits interactive unwrapping of many small charts. Check every triangle of the result with an exact orientation test, and cut or split a chart that folds. If injectivity is required, use a [Tutte embedding](/tutte-embedding/) or a method with barriers against flips. If angle distortion is the main concern on strongly curved charts, use angle-based flattening.

## Pitfalls

- **Pins that a development maps to one point.** A common statement is that two pinned vertices make the minimizer unique. That is true when the mesh has no development, for example when some inner vertex has an angle sum that is not a multiple of $2\pi$, or when the pins are two vertices of one triangle. It is false in general. A planar strip that winds once and a half around a square overlaps itself, and two vertices at the same position of the plane, one on each layer, give a singular system. The code of this page tests this case.
- **Folds.** Take six triangles around a flat centre, with the rim vertices on the unit circle at heights $+2$ and $-2$ in turn. The angles at the centre add up to $806.6°$, and LSCM with the pins at vertices 0 and 3 gives two triangles with ORIENT2D $-0.033$. Nothing in the method prevents this.
- **Pins close together.** Two pins at adjacent vertices fix the scale and rotation by one short edge, and the far end of a large chart can come out badly scaled. Pins far apart, such as the two ends of the longest path of the boundary, give a better map.
- **Wrong orientation.** A frame that is mirrored, because a face is oriented the wrong way, makes the term of that triangle measure an orientation-reversing map, and the result folds at that face.
- **Closed or high-genus meshes.** The energy is defined, but the result is meaningless unless the mesh is first cut into a disk.

## Implementations

## History

Bruno Lévy, Sylvain Petitjean, Nicolas Ray and Jérôme Maillot presented LSCM at SIGGRAPH 2002, in a paper on automatic texture atlases that also segments the surface into charts and packs them. In the same year Mathieu Desbrun, Mark Meyer and Pierre Alliez derived discrete conformal parameterization from the Dirichlet energy and the area, and showed with natural boundary conditions how to free the boundary. The two energies are the same up to a factor of 2. LSCM became one of the standard unwrapping methods in modelling software, and is still the usual first choice for fast conformal charts.

## References
