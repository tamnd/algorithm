---
tag: T4XYGG
kind: technique
slug: residual-error-estimator
name: Residual-based a posteriori error estimator
aliases:
- residual error estimator
area: scientific-computing/finite-element-practice
level: core
summary: Bounds the energy error by element residuals and jumps of the normal flux across faces, all computable from the discrete solution.
prereqs: [weak-formulation, sobolev-space, finite-element-method]
see_also: [zienkiewicz-zhu-estimator, dual-weighted-residual-method, adaptive-finite-element-method, dorfler-marking, afem-optimality-theorem, poisson-equation, galerkin-method, cea-lemma]
sources:
  - paper: doi:10.1137/0715049
    title: Ivo Babuska and Werner C. Rheinboldt, Error estimates for adaptive finite element computations, SIAM Journal on Numerical Analysis 15(4) (1978) 736-754
    locator: the first a posteriori error estimates by local residuals and their use for adaptive refinement
  - book: isbn:9780199679423
    title: Rudiger Verfurth, A Posteriori Error Estimation Techniques for Finite Element Methods, Oxford University Press (2013)
    locator: the chapter on residual estimators for the Poisson equation (reliability, efficiency and data oscillation)
  - book: isbn:9780471294115
    title: Mark Ainsworth and J. Tinsley Oden, A Posteriori Error Estimation in Finite Element Analysis, Wiley (2000)
    locator: the chapter on explicit residual estimators
  - paper: doi:10.1137/07069047X
    title: J. Manuel Cascon, Christian Kreuzer, Ricardo H. Nochetto and Kunibert G. Siebert, Quasi-optimal convergence rate for an adaptive finite element method, SIAM Journal on Numerical Analysis 46(5) (2008) 2524-2550
    locator: the estimator with the weight h_K on the jumps, its reduction under refinement and discrete reliability
---

The residual-based a posteriori error estimator measures the error of a finite element solution by how badly it fails to satisfy the equation. For the Poisson problem $-\Delta u = f$ with continuous piecewise linear elements, the discrete solution $u_h$ leaves two kinds of residual: inside each element, $f + \Delta u_h$ is not zero, and across each interior edge, the normal derivative of $u_h$ jumps, while for the exact solution it is continuous. The estimator adds these up with powers of the mesh size:
$$\eta_K^2 = h_K^2\|f + \Delta u_h\|_{L^2(K)}^2 + \tfrac12\sum_{E \subset \partial K\setminus\partial\Omega}h_E\|[\partial_nu_h]\|_{L^2(E)}^2 .$$
The total $\eta = (\sum_K\eta_K^2)^{1/2}$ is reliable, $|u - u_h|_1 \le C_{\mathrm{rel}}\eta$, and each $\eta_K$ is efficient, a lower bound for the local error up to a constant and a data oscillation term. The constants depend only on the shape regularity of the mesh. This two sided bound is why the estimator is the basis of the convergence theory of the [adaptive finite element method](/adaptive-finite-element-method/).

## In plain words

The exact solution satisfies the equation everywhere, and its slope across element sides is continuous. The computed solution does neither. Inside each element, put the computed solution into the equation and see what is left over. On each side between two elements, see how much the slope jumps. Both numbers are easy to compute from the computed solution alone. Weigh them by the element size, add them up, and you get an estimate of the error. The theory shows that the true error is at most a constant times this estimate, and that a large estimate on an element means a large true error near that element.

## When it applies

- **A Galerkin method for an elliptic problem.** The derivation needs Galerkin orthogonality, $a(u - u_h, v_h) = 0$ for all $v_h$ in the discrete space, and a coercive [weak formulation](/weak-formulation/).
- **A conforming space with local interpolation.** The proof uses a quasi-interpolation operator of Clement or Scott-Zhang type with local error bounds, which exists on shape regular meshes of simplices or quadrilaterals.
- **Data that can be integrated.** The residual $f + \Delta u_h$ must be in $L^2$. Rough $f$ is handled by a projection onto piecewise polynomials, with the difference counted as data oscillation.
- **Other problems.** The same template works for linear elasticity, convection diffusion and Maxwell's equations, with the residual and the flux of each equation. For singularly perturbed problems the constants then depend on the perturbation parameter unless the weights are adapted.

## The template

```pseudo id=main
RESIDUAL-ESTIMATE(mesh, u_h, f)
L1  for each element K do
L2      r_K <- f + Laplacian(u_h) on K                    ▷ for P1 elements, Laplacian(u_h) = 0
L3      eta_K^2 <- h_K^2 * ||r_K||^2 on K
L4  for each interior edge E between K and K' do
L5      J_E <- the jump of grad(u_h) . n across E
L6      add (1/2) h_E ||J_E||^2 on E to eta_K^2 and to eta_K'^2
L7  return the eta_K and eta = sqrt(sum of eta_K^2)
```

**Why it is reliable.** Let $e = u - u_h$. For every $v \in H^1_0(\Omega)$, integrate by parts on each element:
$$a(e, v) = (f, v) - \sum_K(\nabla u_h, \nabla v)_K = \sum_K(f + \Delta u_h, v)_K - \sum_E([\partial_nu_h], v)_E .$$
Galerkin orthogonality allows us to replace $v$ by $v - I_hv$, where $I_h$ is a quasi-interpolant into the finite element space. Its local bounds are $\|v - I_hv\|_K \le Ch_K|v|_{1,\omega_K}$ and $\|v - I_hv\|_E \le Ch_E^{1/2}|v|_{1,\omega_E}$, on the patches $\omega$ of neighbor elements. Apply the Cauchy-Schwarz inequality to each term, and use that each element is in a bounded number of patches:
$$a(e, v) \le C\Big(\sum_K\eta_K^2\Big)^{1/2}|v|_1 .$$
Take $v = e$. Then $|e|_1^2 \le C\eta|e|_1$, so $|e|_1 \le C_{\mathrm{rel}}\eta$.

**Why it is efficient.** Verfurth's bubble function method gives the lower bound. Multiply the element residual by the cubic bubble $b_K$ of $K$, which is zero on $\partial K$, and test the error equation with $v = r_Kb_K$; the jumps drop out, and norm equivalences on polynomial spaces give $h_K\|r_K\|_K \le C(|e|_{1,K} + h_K\|f - f_K\|_K)$, where $f_K$ is the mean of $f$ on $K$. An edge bubble gives the same bound for the jump terms on the two elements next to the edge. Together, $\eta_K \le C_{\mathrm{eff}}(|e|_{1,\omega_K} + \mathrm{osc}_K)$.

## Classic examples

**One dimension, by hand.** Take $-u'' = 1$ on $(0, 1)$ with $u(0) = u(1) = 0$, so $u = x(1 - x)/2$, and two elements of size $h = \tfrac12$. The P1 solution matches $u$ at the node: $u_h(\tfrac12) = \tfrac18$. Its slopes are $\tfrac14$ and $-\tfrac14$.

| Quantity | Value |
|---|---|
| Element residual $r_K = f + u_h''$ | 1 on each element |
| $h_K^2\|r_K\|_K^2$ | $\tfrac14\cdot\tfrac12 = \tfrac18$ on each element |
| Jump of $u_h'$ at $x = \tfrac12$ | $-\tfrac14 - \tfrac14 = -\tfrac12$ |
| Jump term $\tfrac12 h\,|J|^2$ for each element | $\tfrac12\cdot\tfrac12\cdot\tfrac14 = \tfrac1{16}$ |
| $\eta_K^2$ | $\tfrac18 + \tfrac1{16} = \tfrac3{16}$ |
| $\eta$ | $\sqrt{3/8} \approx 0.612$ |
| True error $|u - u_h|_1 = \sqrt{|u|_1^2 - |u_h|_1^2} = \sqrt{\tfrac1{12} - \tfrac1{16}}$ | $\sqrt{1/48} \approx 0.144$ |

The effectivity $\eta/|e|_1 = \sqrt{18} \approx 4.24$ is typical: the estimator has the right size and the right behavior, up to a constant that is not 1.

**A guaranteed bound in 1D.** In one dimension the nodal interpolant $I_hv$ is exact at the nodes, so the jump terms drop out of the error equation, and $\|v - I_hv\|_K \le (h_K/\pi)|v|_{1,K}$ gives $|e|_1 \le \tfrac1\pi(\sum_Kh_K^2\|r_K\|_K^2)^{1/2}$ with no unknown constant. For the example this bound is $\tfrac1\pi\cdot\tfrac12 \approx 0.159 \ge 0.144$. On a uniform mesh of size $h$ for the same problem, the true error is $h/\sqrt{12} \approx 0.289h$ and the bound is $h/\pi \approx 0.318h$, so the effectivity of this bound is 1.10 for every $h$.

**The L-shaped domain.** The [AFEM](/adaptive-finite-element-method/) reference code uses this estimator with the weight $h_K = |K|^{1/2}$ on both terms. On the L-shaped domain with a corner singularity, its effectivity stays between 2.66 and 3.67 over all adaptive steps, while the error falls from the uniform rate $N^{-1/3}$ to the optimal rate $N^{-1/2}$. The constant changes little, which is what the marking needs.

## Variations

- **Weights.** The proofs of [AFEM optimality](/afem-optimality-theorem/) use $h_K = |K|^{1/d}$ in both terms. This weight shrinks by a fixed factor at every bisection, which the estimator reduction step needs. The edge length $h_E$ gives an equivalent estimator on shape regular meshes.
- **Higher degree.** For P$k$ elements the element residual includes $\Delta u_h$, which is no longer zero, and the weights stay $h_K^2$ and $h_E$. The constants then depend on $k$. For hp methods, weights $h_K^2/p_K^2$ and $h_E/p_E$ give bounds that are robust in $p$ up to a small loss.
- **Estimators with explicit constants.** Equilibrated flux estimators, such as those of Prager-Synge type, give guaranteed upper bounds with constant 1, at the price of local solves.
- **Implicit estimators.** Solving small local problems on elements or patches with the residual as data gives estimators with better effectivity, as in the Bank-Weiser method.
- **Goal oriented estimators.** The [dual weighted residual method](/dual-weighted-residual-method/) weights the same residuals with the solution of an adjoint problem, to estimate the error in one output quantity.

## Pitfalls

- **Unknown constants.** The constant $C_{\mathrm{rel}}$ is not computed by the method. The estimator is a good indicator for refinement, but $\eta$ itself is not a guaranteed bound in 2D or 3D. Use an equilibrated estimator when you need a certified bound.
- **Missing the jump term.** For P1 elements in 2D the element residual alone is not reliable: the jumps carry most of the error. Leaving them out gives an estimator that does not converge to zero at the right rate.
- **Oscillation of f.** If $f$ varies on a scale smaller than the mesh, the efficiency bound has the extra term $\mathrm{osc}_K$, and the estimate can be far from the error on coarse meshes. Integrate $f$ accurately and watch the oscillation.
- **Anisotropic meshes.** On long thin elements the constants grow with the aspect ratio, unless the estimator is built for anisotropic meshes.
- **Boundary conditions.** For Neumann boundary parts, add the jump between the computed flux and the given flux on the boundary edges. Forgetting this hides the error near the Neumann boundary.

## Exercises

1. For P1 elements in 1D on a uniform mesh for $-u'' = 1$, show that the jump of $u_h'$ at each interior node is $-h$. *Answer:* $u_h$ interpolates $u = x(1-x)/2$ at the nodes, so the slope on $[x_{i-1}, x_i]$ is $u'(x_{i-1/2}) = \tfrac12 - x_{i-1/2}$, and two neighbor slopes differ by $h$.
2. Derive the 1D bound $|e|_1 \le \tfrac1\pi(\sum_Kh_K^2\|r_K\|_K^2)^{1/2}$. *Answer:* $|e|_1^2 = a(e, e - I_he) = \sum_K(r_K, e - I_he)_K$, because $e - I_he$ is zero at the nodes. Then use the Poincare inequality $\|w\|_K \le (h_K/\pi)\|w'\|_K$ for $w$ that is zero at both ends of $K$, and the Cauchy-Schwarz inequality.
3. Why does the element residual vanish for P1 elements and $f = 0$, while the error does not? *Answer:* $\Delta u_h = 0$ on each element, so only the jumps carry the information, which is why the jump term cannot be left out.

## References
