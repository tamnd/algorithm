---
tag: JQY36Z
kind: algorithm
slug: isogeometric-boundary-element-method
name: Isogeometric boundary element method
aliases:
- IGABEM
area: cad/cad-cae-integration
level: research
summary: Uses the spline basis of the CAD boundary for boundary integral equations, so only the surface needs a parameterization, as Politis and then Simpson and coauthors showed.
solves: [poisson-equation]
model: real-ram
complexity:
  vars: {n: number of boundary unknowns, g: Gauss points per element}
  time: {worst: "O(n^2 g + n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2009
  people: [Costas Politis, Alexandros I. Ginnis, Panagiotis D. Kaklis, Robert N. Simpson, Stéphane P. A. Bordas, Jon Trevelyan, Timon Rabczuk]
  note: Politis, Ginnis, Kaklis, Belibassakis and Feurer used the NURBS basis of the boundary for a 2D potential flow BEM in 2009, and Simpson, Bordas, Trevelyan and Rabczuk gave a 2D elastostatic IGABEM in 2012.
prereqs: [isogeometric-analysis, nurbs, collocation-method]
see_also: [isogeometric-collocation, boehm-knot-insertion, gauss-legendre-quadrature, trimmed-isogeometric-analysis, volumetric-spline-parameterization, condition-number, galerkin-method, finite-element-method]
sources:
  - paper: doi:10.1016/j.cma.2011.08.008
    title: R. N. Simpson, S. P. A. Bordas, J. Trevelyan and T. Rabczuk, A two-dimensional isogeometric boundary element method for elastostatic analysis, Computer Methods in Applied Mechanics and Engineering 209-212, 2012, 87 to 100
    locator: the whole paper (the NURBS basis of the boundary for both the geometry and the fields, collocation at the Greville abscissae, the singular integrals and the comparison with Lagrange BEM)
  - paper: doi:10.1145/1629255.1629302
    title: C. Politis, A. I. Ginnis, P. D. Kaklis, K. Belibassakis and C. Feurer, An isogeometric BEM for exterior potential-flow problems in the plane, 2009 SIAM/ACM Joint Conference on Geometric and Physical Modeling, 2009, 349 to 354
    locator: the whole paper, the first use of the NURBS basis of the boundary in a BEM
  - paper: doi:10.1016/j.cma.2004.10.008
    title: T. J. R. Hughes, J. A. Cottrell and Y. Bazilevs, Isogeometric analysis, CAD, finite elements, NURBS, exact geometry and mesh refinement, Computer Methods in Applied Mechanics and Engineering 194(39-41), 2005, 4135 to 4195
    locator: the isogeometric idea of one basis for geometry and analysis, and the NURBS circle
  - paper: doi:10.1007/s11831-017-9220-9
    title: B. Marussig and T. J. R. Hughes, A review of trimming in isogeometric analysis, challenges, data exchange and simulation aspects, Archives of Computational Methods in Engineering 25(4), 2018, 1059 to 1127
    locator: the part on boundary methods, which need only the boundary representation of a trimmed CAD model
---

The isogeometric boundary element method (IGABEM) solves a linear partial differential equation by an integral equation on the boundary of the domain, and it uses the [NURBS](/nurbs/) basis of the CAD boundary both for the geometry and for the unknown fields. A CAD solid is stored by its boundary, so the method needs no volume mesh and no [volumetric spline parameterization](/volumetric-spline-parameterization/), which is the hard step of volume [isogeometric analysis](/isogeometric-analysis/). Politis and coauthors (2009) used it for 2D potential flow, and Simpson, Bordas, Trevelyan and Rabczuk (2012) for 2D elasticity. No page of this site covers the boundary element method itself, so this page defines what it needs, for the 2D Laplace equation, with collocation at the Greville abscissae as in [isogeometric collocation](/isogeometric-collocation/).

## In plain words

For some equations, such as steady heat flow without sources, the values inside a region follow from the values and the fluxes on its border. A classic formula, built from the field of a point source, ties the two together. So you can solve for the unknown border data only, and the problem lives on a curve instead of on a whole area.

To solve the border problem, you need a way to describe functions on the border. The CAD model already describes the border with smooth spline pieces. The method uses those same pieces for the unknown data, so the shape is exact and no mesh has to be made. You ask the border formula to hold at one point per unknown, get a full linear system, and solve it. The values inside then follow from the same formula.

## The problem

Let $\Omega \subset \mathbb{R}^2$ be a bounded domain with a smooth boundary $\Gamma$ and outward normal $n$. Given $g$ on $\Gamma$, find $u$ with

$$ \Delta u = 0 \text{ in } \Omega, \qquad u = g \text{ on } \Gamma, $$

that is, the [Poisson equation](/poisson-equation/) with zero source. The unknown of the boundary method is the flux $q = \partial u / \partial n$ on $\Gamma$.

**The boundary integral equation.** The fundamental solution of the 2D Laplace equation and its normal derivative at $y$ are

$$ u^*(x, y) = -\frac{1}{2\pi} \ln |y - x|, \qquad q^*(x, y) = \frac{\partial u^*}{\partial n_y} = -\frac{1}{2\pi} \frac{(y - x) \cdot n_y}{|y - x|^2}. $$

Green's second identity, applied on $\Omega$ minus a small disc around $x$, gives for a harmonic $u$ and an interior point $x$ the representation formula $u(x) = \int_\Gamma u^* q \, ds - \int_\Gamma q^* u \, ds$. As $x$ moves to a smooth point of $\Gamma$, the second integral jumps by half the value, and

$$ \tfrac12 u(x) + \int_\Gamma q^*(x, y) \, u(y) \, ds_y = \int_\Gamma u^*(x, y) \, q(y) \, ds_y \qquad (x \in \Gamma). $$

The right side is the *single layer* operator $V q$, with a weak singularity $\ln |y - x|$. On a smooth boundary $q^*$ is bounded, because $(y - x) \cdot n_y$ is of order $|y - x|^2$.

**The isogeometric discretization.** $\Gamma$ is a closed NURBS curve $C(t) = \sum_j R_j(t) P_j$, $t \in [0, 1]$, of degree $p$, counterclockwise, with an open knot vector and $P_0 = P_n$. The functions $R_0$ and $R_n$ are merged into one, which gives $n$ functions that are continuous around the closed curve and sum to 1. Both fields use this basis, $u_h = \sum_j R_j u_j$ and $q_h = \sum_j R_j q_j$. The collocation points are $x_i = C(\tau_i)$, $i = 1, \ldots, n$, for the Greville abscissae $\tau_i$ without the last one, which gives the same point as the first.

## The algorithm

```pseudo id=main
IGABEM-DIRICHLET(C, g)                                ▷ C: closed NURBS curve, g: boundary values
L1  n ← number of control points − 1                  ▷ first and last basis functions merged
L2  τ_i ← Greville abscissae of the knots, the last dropped; x_i ← C(τ_i)
L3  for i = 1 to n, for each element e = [t_a, t_b] of C do
L4      if τ_i ∈ e: split e at τ_i; graded Gauss rule t = τ_i ± d w^m for u*, plain Gauss on each part for q*
L5      else: the same g-point Gauss rule on e for both kernels
L6      for each rule point t with weight ω: add u*(x_i, C(t)) R_j(t) |C'(t)| ω to G[i, j] and the same with q* to H[i, j]
L7  H[i, j] ← H[i, j] + ½ R_j(τ_i)                     ▷ the free term
L8  solve Σ_j R_j(τ_i) u_j = g(x_i) for the coefficients u of the data
L9  solve G q = H u and return q
```

Line L4 handles the log singularity of $u^*$. On each side of $\tau_i$, of length $d$, the substitution $t = \tau_i \pm d \, w^m$ with $w \in [0, 1]$ turns $\ln |t - \tau_i|$ into $m \ln w + \ln d$ and multiplies it by $m d \, w^{m-1}$, which is bounded and smooth enough for Gauss rules in $w$. The code uses $m = 4$ and 16 points. The element test checks both $\tau_i$ and $\tau_i + 1$, because the collocation point at $t = 0$ also ends the last element at $t = 1$. Line L8 takes the Dirichlet data into the basis by interpolation at the same points, so that $H u$ is the left side of the integral equation. For a Neumann problem, $q$ is given and lines L8 and L9 change roles. For mixed data the columns of known and unknown values are swapped.

**Geometry refinement.** The basis is refined by knot insertion with [Boehm's algorithm](/boehm-knot-insertion/) applied to the homogeneous control points $(w_j P_j, w_j)$, which leaves the curve exactly unchanged.

## Example

**The circle.** Take the circle of radius $R = 2$ as the exact quadratic NURBS with 9 control points, the knots $(0, 0, 0, \tfrac14, \tfrac14, \tfrac12, \tfrac12, \tfrac34, \tfrac34, 1, 1, 1)$ and the weights $1, \tfrac{\sqrt2}{2}, 1, \ldots$. On the circle, $(y - x) \cdot n_y = |y - x|^2 / (2R)$, so $q^* = -1/(4\pi R)$ is constant, and $\int_\Gamma q^* \, ds = -\tfrac12$.

- **Constant data.** For $u = 1$, each row of $H u$ is $\tfrac12 - \tfrac12 = 0$, so $q_h = 0$. The code returns $|q_j| < 10^{-7}$.
- **Data in the space.** For $u = x + 2y$, the flux is $q = (x + 2y)/R$. Both are NURBS of the basis, because $x$ and $y$ are. The code returns the exact control values of $q$ to about $7 \times 10^{-9}$, the error of the quadrature.
- **A smooth solution not in the space.** For $u = x^2 - y^2 = R^2 \cos 2\theta$, the flux is $q = 2R \cos 2\theta = 4 \cos 2\theta$. Uniform knot insertion gives:

| elements | unknowns $n$ | max error of $q_h$ | error of $u$ at $(0.5, 0.3)$ |
|---|---|---|---|
| 4 | 8 | $5.3 \times 10^{-1}$ | $1.5 \times 10^{-2}$ |
| 8 | 12 | $6.4 \times 10^{-2}$ | $2.5 \times 10^{-4}$ |
| 16 | 20 | $1.5 \times 10^{-2}$ | $9.2 \times 10^{-5}$ |
| 32 | 36 | $1.7 \times 10^{-3}$ | $5.5 \times 10^{-6}$ |
| 64 | 68 | $2.1 \times 10^{-4}$ | $3.4 \times 10^{-7}$ |

From 16 to 64 elements the flux error falls by about 8 per halving of the element size, an observed order 3, and the interior error by about 16, an observed order 4. These are measurements on this problem. The interior value comes from the representation formula with $u_h$ and $q_h$, which smooths the boundary error.

**An ellipse.** The same circle scaled by $(1, 0.75)$ is an ellipse, still an exact NURBS with the same weights. There $q^*$ is not constant, and for $u = x^2 - y^2 + \tfrac12 xy + x$ the flux error falls from $2.4 \times 10^{-2}$ to $2.7 \times 10^{-3}$ when the elements go from 16 to 32.

## Correctness

Three things are proved on the proof page. First, the integral equation holds for the exact solution, and on the circle the operators are diagonal in Fourier modes: $V 1 = -R \ln R$ and $V e^{ik\theta} = \frac{R}{2|k|} e^{ik\theta}$ for $k \ne 0$. So the single layer operator of a circle is invertible if and only if $R \ne 1$. Second, the discrete system is consistent: if the exact $u$ and $q$ are both in the spline space, they satisfy the collocation equations exactly, so if the matrices of lines L8 and L9 are non-singular, the method returns them. This is what the test with $u = x + 2y$ checks. Third, $u = 1$ gives $q_h = 0$ for every closed smooth curve, from $\int_\Gamma q^* \, ds = -\tfrac12$.

The non-singularity of the discrete matrix $G$ and the convergence order are not proved here. The table measures them.

## Complexity

In the [real RAM](/real-ram/) model, with $n$ unknowns, about $n$ elements and $g$ Gauss points per element:

- **Assembly.** Each pair (collocation point, element) costs $g$ kernel evaluations, each adding to $p + 1$ entries. The regular rules do not depend on the point, so the curve is evaluated once per element. The total is $O(n^2 g p)$, with two extra graded rules per row. The code evaluates full basis rows, an extra factor $n$ in that step, which is fine for the tests.
- **Solve.** $G$ is dense and not symmetric, so [Gaussian elimination](/gaussian-elimination/) costs $O(n^3)$ time and the matrices $O(n^2)$ space.

A 3D problem has $n$ unknowns on a surface, against about $n^{3/2}$ for a volume mesh of the same resolution, but the dense matrix makes plain BEM cost $O(n^2)$ memory. Large problems use fast methods, such as the fast multipole method or hierarchical matrices, which reduce this to nearly $O(n)$.

## Properties

- **Exact geometry and boundary only.** The analysis uses the CAD boundary without change. A trimmed CAD solid also only needs its boundary, see [trimmed isogeometric analysis](/trimmed-isogeometric-analysis/).
- **Dense, non-symmetric matrix.** Every point sees every element.
- **Exterior problems** (unbounded domains) need no truncation, because the fundamental solution has the right behavior at infinity.
- **Singular integrals.** The diagonal blocks need special rules, and their accuracy limits the whole method.
- **Linear, constant coefficient equations only.** The method needs a fundamental solution.

## Variants and improvements

- **Galerkin BEM.** Test the integral equation against the basis instead of collocating. The matrix of $V$ is then symmetric, and positive definite when the logarithmic capacity of $\Gamma$ is below 1 (for a circle, $R < 1$), at the cost of double integrals.
- **Other equations.** Elastostatics (Simpson and coauthors 2012), Helmholtz for acoustics, and Stokes flow, each with its fundamental solution.
- **T-spline and trimmed boundaries.** 3D IGABEM works directly on T-spline surfaces and on trimmed NURBS surfaces.
- **Fast methods.** Fast multipole methods and hierarchical matrices compress the dense blocks.

## When to use it

Use it for linear problems with a known fundamental solution when the model comes from CAD and a volume mesh is costly: exterior acoustics and potential flow, electrostatics, and elasticity of solids when only the boundary is of interest. Use volume isogeometric or finite element analysis for nonlinear materials, variable coefficients and volume sources, which need a volume integral.

## Pitfalls

- **The degenerate scale.** In 2D, $V$ is not invertible when the logarithmic capacity of $\Gamma$ is 1, and for a circle that means $R = 1$: then $V 1 = -R \ln R = 0$. The test with $R = 1$ shows that the constant vector is in the kernel of the discrete $G$ to $10^{-9}$. Scale the geometry, or add the condition $\int_\Gamma q \, ds = 0$ with an extra unknown.
- **Singular quadrature.** Plain Gauss on the element that holds the collocation point converges slowly on $\ln |t - \tau_i|$. Use a graded rule, subtraction of the singularity, or a special log rule.
- **Points at corners.** At a corner the free term is not $\tfrac12$ but the inner angle over $2\pi$, and the normal jumps. Do not collocate at corners with the smooth formula, or move the point inside an element.
- **The seam of a closed curve.** The parameter $t = 0$ and $t = 1$ are the same point. Merge the two basis functions and treat the singular element on both sides.
- **Nearly singular integrals.** Interior points close to the boundary need refined rules, as in line L4.

## Implementations

## History

Boundary integral equations for potential problems go back to the nineteenth century, and the boundary element method as a numerical method developed from the 1960s. Politis, Ginnis, Kaklis, Belibassakis and Feurer (2009) used the NURBS basis of the boundary curve for a 2D exterior potential flow BEM. Simpson, Bordas, Trevelyan and Rabczuk (2012) gave a 2D IGABEM for elastostatics with collocation at the Greville abscissae, and later work extended the idea to 3D with T-splines and to trimmed surfaces. Marussig and Hughes (2018) list boundary methods among the ways to analyze trimmed CAD models without a volume parameterization.

## References
