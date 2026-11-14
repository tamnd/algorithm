---
tag: FWX0HA
kind: technique
slug: anisotropic-mesh-adaptation
name: Metric-based anisotropic mesh adaptation
aliases:
- Riemannian metric mesh adaptation
- continuous mesh framework
area: cad/mesh-generation-for-analysis
level: advanced
summary: Builds a metric tensor field from the Hessian of the solution and makes a mesh whose elements are unit and regular in it, so elements stretch along features.
prereqs: [finite-element-method, piecewise-linear-interpolation, mesh-sizing-function]
see_also: [jacobi-eigenvalue-algorithm, boundary-layer-mesh-generation, delaunay-refinement, advancing-front-mesh-generation, optimization-based-mesh-smoothing, mesh-quality-measures, parametric-surface-meshing, edge-flip]
sources:
  - paper: doi:10.1137/090754078
    title: Adrien Loseille and Frédéric Alauzet, Continuous mesh framework part I, well-posed continuous interpolation error, SIAM Journal on Numerical Analysis 49(1), 2011, 38 to 60
    locator: the duality between unit meshes and Riemannian metric fields, the complexity of a metric, and the interpolation error of a continuous mesh (general locator)
  - paper: doi:10.1137/10078654X
    title: Adrien Loseille and Frédéric Alauzet, Continuous mesh framework part II, validations and applications, SIAM Journal on Numerical Analysis 49(1), 2011, 61 to 86
    locator: the optimal metric in the L^p norm for a given complexity and the adaptation loop (general locator)
  - book: isbn:978-1-84821-029-5
    title: Pascal Jean Frey and Paul-Louis George, Mesh Generation, Application to Finite Elements, 2nd edition, ISTE and Wiley, 2008
    locator: the chapters on metrics, anisotropic meshing and mesh adaptation (general locator)
---

Metric-based anisotropic mesh adaptation makes a mesh whose elements are long in the directions where the solution changes slowly and short where it changes fast. It describes the wanted size and shape at every point by a metric tensor, a symmetric positive definite matrix $M(x)$, and then asks for a mesh in which every edge has length close to 1 when measured with $M$. A mesh that is unit in this sense is a mesh of near equilateral triangles in a deformed space; in the real plane its triangles are stretched as $M$ says. The metric usually comes from the Hessian of the computed solution, because the error of linear interpolation is controlled by second derivatives. Solve, build the metric, remesh, and repeat. For the same accuracy, a solution with a strongly directional feature needs far fewer elements than with an isotropic mesh; the example below shows a factor of 10 for a simple quadratic.

## In plain words

A mesh puts small tiles where the answer of a computation changes fast. If the answer changes fast in one direction only, as across a shock wave, square tiles waste effort along the other direction. Long thin tiles, lying along the shock, do the same job with far fewer tiles.

The method stores, at each point, a rule for measuring length that says how long a tile edge may be in each direction. Then it builds a mesh in which every edge has length about 1 by that rule. Short in one direction and long in another is then automatic.

The rule comes from the curvature of the answer: strong bending in a direction asks for short edges in that direction. So the loop is: solve, measure the bending, build the rule, remesh, and solve again.

## When it applies

- The solution is a scalar field, or a few fields, on a 2D or 3D domain, computed on a simplicial mesh with a linear or low order method, for example the [finite element method](/finite-element-method/).
- The solution has strongly directional features: shocks, boundary and shear layers, contact lines, or fronts.
- The mesh generator can work with a variable metric: it can measure edge lengths in a metric and change the mesh locally by edge splits, edge collapses, edge flips and vertex moves.
- It does not help much for a smooth, isotropic solution, where an isotropic [mesh sizing function](/mesh-sizing-function/) does the same.

**The metric and the length of an edge.** A metric field gives each point a symmetric positive definite matrix $M(x)$. In a constant metric, the length of an edge vector $e$ is $\ell_M(e) = \sqrt{e^T M e}$. For a varying metric, it is the integral of $\sqrt{e^T M(a + s e)\,e}$ over $s \in [0, 1]$, which is computed by a few quadrature points. If $M = R\,\mathrm{diag}(\lambda_1, \lambda_2)\,R^T$ with orthogonal $R$, the unit ball of $M$ is an ellipse with axes along the columns of $R$ and half lengths $h_i = 1/\sqrt{\lambda_i}$. These $h_i$ are the wanted edge lengths in the two directions. A mesh is unit for $M$ if every edge has $\ell_M$ in $[1/\sqrt2, \sqrt2]$ and every element is close to equilateral when measured with $M$.

**Why the Hessian.** For a quadratic function $f$ with Hessian $H$, the error of linear interpolation at the midpoint of an edge $e$ is exactly $\frac18 e^T H e$, since $\frac12(f(a) + f(a + e)) - f(a + \frac{e}{2}) = \frac18 e^T H e$. With $M = |H|/(8\varepsilon)$, where $|H|$ has the absolute values of the eigenvalues of $H$, the midpoint error on an edge of a convex function is $\varepsilon\,\ell_M(e)^2$, so it is $\varepsilon$ on a unit edge. Different authors use different constants in front of $|H|$, from different error norms; the structure is the same.

## The template

```pseudo id=main
ADAPT(domain, solver, ε, N_max)
L1  T ← an initial mesh
L2  repeat
L3      u ← the solution of the problem on T
L4      H(v) ← a recovered Hessian of u at each vertex v
L5      M(v) ← R |Λ| R^T / (8ε), where H(v) = R Λ R^T, with eigenvalues clipped to [1/h_max², 1/h_min²]
L6      limit the growth of M from vertex to vertex (gradation)
L7      repeat
L8          split every edge with ℓ_M > √2, collapse every edge with ℓ_M < 1/√2
L9          flip edges and move vertices to make the elements regular in M
L10     until no edge changes
L11 until the error estimate stops falling or the mesh has N_max vertices
```

L4 recovers second derivatives from a piecewise linear $u$, for example by a least squares fit of a quadratic on the vertex neighbours, or by applying a recovered gradient twice. L5 takes the eigenvalues, which for a symmetric $2 \times 2$ or $3 \times 3$ matrix can be done by the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/), and the clipping keeps the sizes finite where $H$ vanishes. L8 to L9 are the local remeshing operators. A metric aware [Delaunay](/delaunay-refinement/) or [advancing front](/advancing-front-mesh-generation/) mesher can replace L7 to L10 by a new mesh.

**The continuous mesh view.** Loseille and Alauzet treat a metric field as a continuous mesh. Its complexity $\mathcal{C}(M) = \int_\Omega \sqrt{\det M(x)}\,dx$ is the continuous counterpart of the number of vertices, and a unit mesh has about that many vertices, up to a fixed factor. For the interpolation error in the $L^p$ norm, at a fixed complexity $N$, they derive the optimal metric

$$M_{L^p}(x) = D_{L^p}\,\det\bigl(|H(x)|\bigr)^{-\frac{1}{2p + d}}\,|H(x)|,$$

in dimension $d$, where the constant $D_{L^p}$ makes the complexity equal to $N$. The factor with the determinant moves resolution from places where the Hessian is large in every direction to places where it is large in only one. As $p \to \infty$ the formula tends to a multiple of $|H|$, the choice of L5.

## Classic examples

**A stretched quadratic.** Let $f(x, y) = x^2 + 100 y^2$ on the unit square and $\varepsilon = 1/100$. The Hessian is $\mathrm{diag}(2, 200)$, so $M = \mathrm{diag}(25, 2500)$ everywhere, and the wanted edge lengths are $h_x = 0.2$ and $h_y = 0.02$. The edge $(0.2, 0)$ and the edge $(0, 0.02)$ are unit, and both have midpoint error exactly $1/100$. The edge $(0.3, 0.01)$ has $\ell_M = \sqrt{2.25 + 0.25} = \sqrt{2.5} \approx 1.58 > \sqrt2$, so L8 splits it, and its midpoint error is $1/40 = \varepsilon \cdot 2.5$, as the formula says. An equilateral triangle with unit sides in $M$ has real area $\frac{\sqrt3}{4}/\sqrt{\det M}$, so about $\frac{4}{\sqrt3}\sqrt{25 \cdot 2500} \approx 577$ triangles cover the square. An isotropic mesh with the same error needs $h = 0.02$ in every direction and about $5774$ triangles, 10 times more, which is $\sqrt{\lambda_{\max} / \lambda_{\min}}$.

**Shocks in compressible flow.** For an inviscid supersonic flow, the Mach number or the density changes sharply across shocks. An adapted mesh puts long thin triangles along each shock, and a few adaptation loops capture the shocks to a width of a few cells.

**Boundary layers.** Near a wall in a viscous flow, the velocity Hessian is large in the wall normal direction. Metric adaptation then gives stretched elements along the wall, the same kind of mesh that [boundary layer mesh generation](/boundary-layer-mesh-generation/) builds directly from the geometry.

**Surfaces.** Meshing a curved surface in its parameter plane is a metric problem: the first fundamental form is the metric. See [surface meshing in parametric space](/parametric-surface-meshing/).

## Variations

- **Metric intersection.** For several fields, or a field and a geometric size, take at each point the largest metric whose unit ball is inside both unit balls. It is computed by a simultaneous reduction of the two matrices, a generalised eigenvalue problem.
- **Gradation.** Limit how fast the sizes can change between neighbours, by shrinking each metric so that it is not much larger than its neighbours' metrics carried along the edge. Without it, the elements change size too fast and get bad shapes.
- **Goal oriented metrics.** Weight the Hessian by the solution of an adjoint problem, so that the mesh reduces the error in a chosen output, such as the drag, instead of the interpolation error.
- **Time dependent problems.** Build one metric for a window of time steps, by intersecting the metrics of the steps, so that the mesh does not have to change at every step.
- **Higher order.** For elements of degree $k$, the error depends on derivatives of order $k + 1$, and the metric comes from those.

## Pitfalls

- **Noisy Hessian.** Second derivatives recovered from a piecewise linear field are noisy, and the noise shows up as random stretching. Smooth or fit over a larger patch.
- **Zero eigenvalues.** Where the solution is linear, the Hessian has a zero eigenvalue and the wanted length is infinite. Always clip the eigenvalues.
- **Wrong sign.** Use $|H|$, with the absolute values of the eigenvalues. $H$ itself is not positive definite where the solution has a saddle.
- **No gradation.** Sharp jumps of the metric make the mesher fail or give bad elements at the jump.
- **Unit is not enough.** A mesh can have all edge lengths near 1 in $M$ and still contain flat elements in $M$. Also measure the element quality in $M$.
- **Solver limits.** Highly stretched elements can make the linear systems ill conditioned and can break the [maximum angle condition](/maximum-angle-condition/). Check that the solver handles them.

## Exercises

- Show that $\frac12(f(a) + f(a + e)) - f(a + \frac{e}{2}) = \frac18 e^T H e$ for every quadratic $f$ with Hessian $H$, and conclude that the midpoint error of a convex quadratic is $\varepsilon\,\ell_M(e)^2$ for $M = H/(8\varepsilon)$.
- For $M = \mathrm{diag}(\lambda_1, \lambda_2)$, show that the real area of a triangle that is equilateral with unit sides in $M$ is $\frac{\sqrt3}{4}(\lambda_1\lambda_2)^{-1/2}$, and use it to count the triangles of a unit mesh of a domain of area $A$.

## References
