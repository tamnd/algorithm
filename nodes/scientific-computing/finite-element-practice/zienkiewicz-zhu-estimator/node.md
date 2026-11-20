---
tag: 4WBQ50
kind: algorithm
slug: zienkiewicz-zhu-estimator
name: Zienkiewicz-Zhu error estimator
aliases:
- ZZ estimator
- superconvergent patch recovery
area: scientific-computing/finite-element-practice
level: core
summary: Recovers a smoother gradient by local least squares fits on patches and uses its difference from the raw gradient as an error estimate.
model: real-ram
complexity:
  vars: {M: the number of triangles}
  time: {average: "Θ(M)"}
  space: {extra: "Θ(M)"}
properties: {deterministic: true, local: true, problem_independent: true, asymptotically_exact_on_superconvergent_meshes: true}
history:
  year: 1987
  people: [Olgierd C. Zienkiewicz, Jian Zhong Zhu]
  note: Zienkiewicz and Zhu proposed the estimator with simple averaging in 1987 and the superconvergent patch recovery in 1992.
prereqs: [finite-element-method, lagrange-finite-element]
see_also: [residual-error-estimator, dual-weighted-residual-method, adaptive-finite-element-method, dorfler-marking, least-squares-problem, normal-equations, finite-element-assembly, poisson-equation]
sources:
  - paper: doi:10.1002/nme.1620240206
    title: O. C. Zienkiewicz and J. Z. Zhu, A simple error estimator and adaptive procedure for practical engineering analysis, International Journal for Numerical Methods in Engineering 24(2) (1987) 337-357
    locator: the estimator with the averaged gradient and the effectivity index
  - paper: doi:10.1002/nme.1620330702
    title: "O. C. Zienkiewicz and J. Z. Zhu, The superconvergent patch recovery and a posteriori error estimates. Part 1: The recovery technique, International Journal for Numerical Methods in Engineering 33(7) (1992) 1331-1364"
    locator: the least squares fit on element patches at the superconvergent points
  - paper: doi:10.1002/nme.1620330703
    title: "O. C. Zienkiewicz and J. Z. Zhu, The superconvergent patch recovery and a posteriori error estimates. Part 2: Error estimates and adaptivity, International Journal for Numerical Methods in Engineering 33(7) (1992) 1365-1382"
    locator: the asymptotic exactness argument and the adaptive examples
  - paper: doi:10.1090/S0025-5718-02-01402-3
    title: "Carsten Carstensen and Soren Bartels, Each averaging technique yields reliable a posteriori error control in FEM on unstructured grids. Part I: Low order conforming, nonconforming, and mixed FEM, Mathematics of Computation 71(239) (2002) 945-969"
    locator: reliability of averaging estimators on general meshes
  - book: isbn:9780471294115
    title: Mark Ainsworth and J. Tinsley Oden, A Posteriori Error Estimation in Finite Element Analysis, Wiley (2000)
    locator: the chapter on recovery based estimators
---

The Zienkiewicz-Zhu (ZZ) estimator measures the error of a finite element solution by how rough its gradient is. A piecewise linear solution $u_h$ has a gradient that jumps from one element to the next, while the gradient of the exact solution is continuous. The estimator builds a continuous gradient $G$ from $u_h$, called the recovered gradient, and uses $\eta_K = \|G - \nabla u_h\|_{L^2(K)}$ as the error indicator of element $K$. The superconvergent patch recovery (SPR) computes $G$ at each vertex by a least squares fit of a linear polynomial to the element gradients of the patch around that vertex. The estimator needs only the mesh and the solution. It does not look at the equation, so one code works for heat flow, elasticity and other problems. When $G$ is much closer to the true gradient than $\nabla u_h$ is, the estimate is asymptotically exact: $\eta$ divided by the true error tends to 1.

## In plain words

The computed solution has a slope that is constant on each triangle and jumps between triangles. The true solution has a smooth slope. So make a smooth slope from the computed one: at each corner, look at the slopes of the triangles around it and fit a plane through them. This gives a slope at every corner, and in between we interpolate linearly. Where the computed slope is far from the smooth slope, the solution is probably bad, and that triangle should be refined. The total difference is the estimate of the error. On good meshes the estimate is almost exactly the true error.

## The problem

**Input.** A conforming triangle mesh of a polygon and the nodal values $U$ of a continuous piecewise linear finite element solution $u_h$.

**Output.** An indicator $\eta_K \ge 0$ for each triangle $K$ and the total $\eta = (\sum_K\eta_K^2)^{1/2}$, which estimates the energy error $\|\nabla u - \nabla u_h\|_{L^2(\Omega)}$.

## The algorithm

ZZ-ESTIMATE is the estimator. SPR-RECOVER is the recovery of the 1992 paper. The averaging recovery of the 1987 paper replaces lines L6 to L10 by the area weighted mean of the element gradients around each vertex.

```pseudo id=main
ZZ-ESTIMATE(mesh, U)
L1  G <- SPR-RECOVER(mesh, U)                      ▷ one vector per vertex
L2  for each triangle K do
L3      s <- (|K| / 3) * sum over the edge midpoints m of |G(m) - grad u_h on K|^2
L4      eta_K <- sqrt(s)
L5  return (eta_K for all K), sqrt(sum of eta_K^2)

SPR-RECOVER(mesh, U)
L6  for each interior vertex v do
L7      fit p(x) = a + b x + c y to the gradients of the triangles at v, at their centroids, by least squares (one fit per component)
L8      G(v) <- p(v)
L9      for each boundary vertex w of the patch of v do add p(w) to the sum at w
L10 for each boundary vertex w do G(w) <- the mean of the sums at w
L11 return G
```

At line L3, $G(m)$ is the mean of $G$ at the two ends of the edge, because $G$ is linear on the edge. The rule is exact, because the integrand is a quadratic polynomial on $K$.

## Example

**One dimension, by hand.** Take $-u'' = -2$ on $(0, 1)$ with $u(0) = 0$ and $u(1) = 1$, so $u = x^2$. With 4 elements of size $h = \tfrac14$, the linear finite element solution matches $u$ at the nodes, so its slope on an element is $2$ times the midpoint.

| Element | Slope of $u_h$ | $G$ at the left end | $G$ at the right end | $\eta_K^2$ | True $\|u' - u_h'\|_K^2$ |
|---|---|---|---|---|---|
| $[0, \tfrac14]$ | $\tfrac14$ | 0 | $\tfrac12$ | $\tfrac{1}{192}$ | $\tfrac{1}{192}$ |
| $[\tfrac14, \tfrac12]$ | $\tfrac34$ | $\tfrac12$ | 1 | $\tfrac{1}{192}$ | $\tfrac{1}{192}$ |
| $[\tfrac12, \tfrac34]$ | $\tfrac54$ | 1 | $\tfrac32$ | $\tfrac{1}{192}$ | $\tfrac{1}{192}$ |
| $[\tfrac34, 1]$ | $\tfrac74$ | $\tfrac32$ | 2 | $\tfrac{1}{192}$ | $\tfrac{1}{192}$ |

At the interior node $\tfrac14$, the patch has the slopes $\tfrac14$ and $\tfrac34$ at the midpoints $\tfrac18$ and $\tfrac38$. The line through them is $2x$, so $G(\tfrac14) = \tfrac12$, and its value at the boundary node 0 is 0. The same happens at every node, so $G = 2x = u'$ exactly. On each element $G - u_h'$ is $2(x - x_m)$ with $x_m$ the midpoint, and $\int_K 4(x - x_m)^2\,dx = h^3/3 = \tfrac{1}{192}$. So $\eta^2 = \tfrac{4}{192} = \tfrac{1}{48}$, equal to the true error, and the effectivity is exactly 1.

**Two dimensions, measured.** The reference code solves $-\Delta u = 2\pi^2\sin(\pi x)\sin(\pi y)$ on the unit square with $u = 0$ on the boundary, on uniform meshes of $2m^2$ triangles, and compares the estimate with the exact energy error.

| $m$ | Triangles | Error $e$ | $\eta$ (SPR) | $\eta / e$ (SPR) | $\eta$ (averaging) | $\eta / e$ (averaging) |
|---|---|---|---|---|---|---|
| 4 | 32 | 0.8386 | 0.8337 | 0.9943 | 0.8213 | 0.9794 |
| 8 | 128 | 0.4318 | 0.4340 | 1.0052 | 0.4394 | 1.0176 |
| 16 | 512 | 0.2175 | 0.2184 | 1.0038 | 0.2200 | 1.0115 |
| 32 | 2048 | 0.1090 | 0.1091 | 1.0013 | 0.1096 | 1.0055 |

The error halves when $h$ halves, and the effectivity tends to 1. With the interior nodes moved at random by up to $h/4$ in each direction, the effectivity at $m = 16$ and $m = 32$ was still within 1 percent of 1 for SPR in this test, but no theorem covers such meshes.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). Line L3 integrates a quadratic polynomial with a rule that is exact for quadratics, so $\eta_K$ is exactly $\|G - \nabla u_h\|_{L^2(K)}$. A least squares fit of data that come from a linear polynomial returns that polynomial when the points are not on one line. So if $u_h$ is linear on the whole domain, the recovery returns its gradient and every indicator is 0. The main fact is one line of algebra: by the triangle inequality, $|\eta - e| \le \|\nabla u - G\|$. If the recovered gradient superconverges, that is $\|\nabla u - G\| / e \to 0$, then $\eta / e \to 1$.

## Complexity

For $M$ triangles of a mesh with bounded vertex degree, each step is local. Collecting the element gradients is $\Theta(M)$, each vertex solves a $3 \times 3$ least squares system in $O(1)$ time, and lines L2 to L4 are $\Theta(M)$. So the total is $\Theta(M)$ time and $\Theta(M)$ memory. This is much cheaper than the solve that produced $u_h$.

## Properties

- **No equation needed.** The estimator uses only $u_h$, so it is the same code for any second order problem. This is why many engineering codes use it.
- **Asymptotically exact under superconvergence.** If $\|\nabla u - G\| = o(e)$, then $\eta / e \to 1$. For linear triangles and smooth $u$, this is known on uniform and almost uniform meshes.
- **Reliable up to constants on general meshes.** Carstensen and Bartels proved that every averaging estimator bounds the error from above and below up to constants and higher order terms, on unstructured meshes.
- **Local.** The indicator $\eta_K$ depends only on $u_h$ in the patches of the vertices of $K$.
- **Exact for linear solutions.** If $u_h$ is linear, all indicators are 0.

## Variants and improvements

- **Simple averaging.** The 1987 form takes the area weighted mean of the element gradients at each vertex. It is simpler than SPR and gives similar results on good meshes, as the table shows.
- **Higher order elements.** For degree $p$, SPR fits a polynomial of degree $p$ to the gradients at the Gauss points of the patch elements.
- **Stress recovery.** In elasticity the same fit is applied to the stress components, which is the original engineering use.
- **Polynomial preserving recovery.** Zhang and Naga fit the nodal values of $u_h$ instead of the gradients, which gives superconvergence on a wider class of meshes.
- **Equilibrated recoveries.** Some methods recover a flux that also satisfies the balance law. These estimators give guaranteed upper bounds with explicit constants, which ZZ does not.

## When to use it

Use ZZ when you need a cheap, robust indicator for refinement and you do not want to code element residuals and jumps for each new equation. It is a good choice for engineering problems with smooth solutions on good meshes. Use the [residual estimator](/residual-error-estimator/) when a proof of convergence of the adaptive loop is needed, because the convergence theory of [AFEM](/adaptive-finite-element-method/) is built on it. Use the [dual weighted residual method](/dual-weighted-residual-method/) when you need the error in one output quantity, not in the energy norm.

## Pitfalls

- **Exactness needs superconvergence.** Near a singularity or on a mesh with a bad structure, the recovered gradient is not much better than $\nabla u_h$, and the effectivity can be far from 1. The estimator then still marks the right region in most cases, but the number $\eta$ is not a guaranteed bound.
- **Boundary vertices.** A fit centered at a boundary vertex uses a one sided patch and is less accurate. SPR uses the fits of the interior patches nearby, as at lines L9 and L10.
- **Collinear centroids.** A patch with fewer than 3 triangles, or with centroids on one line, gives a singular least squares system. The code then uses the averaged value.
- **Scaling.** Center the coordinates at the vertex before the fit, as the code does, or the normal equations become badly conditioned on small elements.
- **Data oscillation.** The estimator does not see the right side $f$, so it misses error caused by a rough $f$ on a coarse mesh.

## Implementations

## History

Olgierd Zienkiewicz and Jian Zhong Zhu published the estimator in 1987. It came from engineering practice: stress values averaged at the nodes were known to be more accurate than the raw element stresses, and the difference was a natural measure of the error. In 1992 they gave the superconvergent patch recovery, which fits a polynomial to the values at the points where the finite element gradient is most accurate, and they showed the effectivity tends to 1 in many tests. The method spread quickly in commercial codes. Mathematical analysis followed: superconvergence results for the recovered gradient on structured meshes, and in 2002 the proof by Carsten Carstensen and Soren Bartels that averaging gives a reliable estimate on any mesh.

## References
