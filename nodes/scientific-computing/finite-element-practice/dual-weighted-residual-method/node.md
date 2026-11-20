---
tag: WE0842
kind: technique
slug: dual-weighted-residual-method
name: Dual weighted residual method
aliases:
- DWR method
- goal-oriented error estimation
area: scientific-computing/finite-element-practice
level: advanced
summary: Estimates the error in a quantity of interest by weighting local residuals with the solution of an adjoint problem.
prereqs: [residual-error-estimator, galerkin-method]
see_also: [adjoint-state-method, adjoint-model, adaptive-finite-element-method, zienkiewicz-zhu-estimator, dorfler-marking, lagrange-multiplier, finite-element-method, poisson-equation]
sources:
  - paper: doi:10.1017/S0962492901000010
    title: Roland Becker and Rolf Rannacher, An optimal control approach to a posteriori error estimation in finite element methods, Acta Numerica 10 (2001) 1-102
    locator: the error representation by the dual solution, the weighted indicators and the nonlinear case with the Lagrangian
  - paper: doi:10.1017/S096249290200003X
    title: "Michael B. Giles and Endre Suli, Adjoint methods for PDEs: a posteriori error analysis and postprocessing by duality, Acta Numerica 11 (2002) 145-236"
    locator: the adjoint error correction of output functionals and its superconvergence
---

The dual weighted residual (DWR) method estimates the error in one number computed from a finite element solution, such as the drag on a body, the mean stress in a region or the value at a point. The number is a functional $J(u)$ of the solution. The method solves an adjoint problem, also called the dual problem, whose solution $z$ measures how much a residual at each place changes $J$. Then the error is the residual of $u_h$ tested with $z - I_hz$, where $I_hz$ is the interpolant of $z$:
$$J(u) - J(u_h) = \sum_K\Big[(f + \Delta u_h, z - I_hz)_K - \tfrac12([\partial_nu_h], z - I_hz)_{\partial K}\Big].$$
For a linear problem and a linear functional this identity is exact. In practice $z$ is replaced by a more accurate discrete approximation, and the terms of the sum are the local indicators. They mark the elements that matter for $J$, which can be far from the elements where the energy error is large.

## In plain words

Often you do not care about the error everywhere, only about one result, like a force or an average. The DWR method finds out how sensitive that result is to errors at each place in the domain. It does this by solving one extra problem, the adjoint problem, which has the same operator turned around and the goal as its source. Its solution is large where errors matter for the goal and small where they do not. Multiply the usual residuals by this sensitivity, and you get an estimate of the error in the result, element by element. Refine where the product is large.

## When it applies

- **A Galerkin method and a goal.** The problem is $a(u, v) = (f, v)$ for all $v$, the Galerkin solution satisfies Galerkin orthogonality, and the quantity of interest is a functional $J$. For a linear $J$, the dual problem is $a(v, z) = J(v)$ for all $v$.
- **A dual problem that can be solved.** The adjoint problem must be well posed and solvable to higher accuracy than the primal one, by a higher degree, a finer mesh or a recovery from $z_h$.
- **Nonlinear problems and nonlinear goals.** With the Lagrangian $L(u, z) = J(u) + (f, z) - a(u; z)$, the error in $J$ is half the primal residual weighted by the dual error plus half the dual residual weighted by the primal error, up to a remainder of third order. This is the optimal control view of Becker and Rannacher.
- **Time dependent problems.** The dual problem runs backward in time. It needs the primal solution at all times, which costs memory or recomputation.

## The template

```pseudo id=main
DWR-ADAPT(mesh, f, J, tol)
L1  repeat
L2      u_h <- the Galerkin solution on the mesh
L3      z_h <- an approximation of the dual solution, a(v, z) = J(v), of higher accuracy than the space of u_h
L4      for each element K do
L5          eta_K <- (f + Laplacian(u_h), z_h - I_h z_h)_K - (1/2) (jump of normal derivative of u_h, z_h - I_h z_h) on the boundary of K
L6      if |sum of eta_K| < tol then return J(u_h) and the estimate
L7      mark by |eta_K|, for example with Dorfler marking, and refine
```

**Why the identity holds.** Let $e = u - u_h$. For a linear $J$ and the dual solution $z$, $J(e) = a(e, z)$. Galerkin orthogonality gives $a(e, z) = a(e, z - v_h)$ for every $v_h$ in the discrete space, in particular $v_h = I_hz$. Then $a(e, z - I_hz)$ is the residual of $u_h$ tested with $z - I_hz$, and integration by parts on each element gives the sum above. No constant and no inequality enters, so the identity is exact.

**The computable estimate.** The identity needs the exact $z$. Replacing it by $z_h$ from the same space as $u_h$ gives 0, by Galerkin orthogonality. So $z$ must be approximated in a richer way: by elements of one higher degree, by a solve on a finer mesh, or by a patch-wise higher order interpolation of $z_h$. The sum of the signed indicators then estimates $J(e)$, and often it can be added to $J(u_h)$ as a correction.

## Classic examples

**A global average, by hand.** Take $-u'' = 1$ on $(0, 1)$ with $u(0) = u(1) = 0$, so $u = x(1-x)/2$, two P1 elements of size $\tfrac12$, and $J(v) = \int_0^1v$. Then $J(u) = \tfrac1{12}$ and $u_h$ is the hat function with height $\tfrac18$, so $J(u_h) = \tfrac1{16}$ and the error is $\tfrac1{48}$. The dual problem is $-z'' = 1$, so $z = u$. In 1D the jumps meet $z - I_hz$ only at the nodes, where it is 0, and the residual is $f + u_h'' = 1$. Each element gives $\eta_K = \int_K(z - I_hz) = \tfrac1{96}$, and the sum $\tfrac1{48}$ is exactly the error.

**A local average.** Keep the same $u_h$ and take $J(v) = \int_0^{1/2}v$. Now $J(u) = \tfrac1{24}$ and $J(u_h) = \tfrac1{32}$, so the error is $\tfrac1{96}$. The dual problem is $-z'' = \chi_{(0, 1/2)}$, with
$$z = \begin{cases} -\tfrac{x^2}2 + \tfrac{3x}8, & 0 \le x \le \tfrac12, \\ \tfrac{1 - x}8, & \tfrac12 \le x \le 1.\end{cases}$$
The interpolant is $I_hz = x/8$ on the left element and $z$ itself on the right one. So $z - I_hz = x(\tfrac12 - x)/2$ on the left, with integral $\tfrac1{96}$, and $z - I_hz = 0$ on the right.

| Element | Residual | $\int_K(z - I_hz)$ | $\eta_K$ | Energy indicator $\eta_K^2$ |
|---|---|---|---|---|
| $[0, \tfrac12]$ | 1 | $\tfrac1{96}$ | $\tfrac1{96}$ | $\tfrac3{16}$ |
| $[\tfrac12, 1]$ | 1 | 0 | 0 | $\tfrac3{16}$ |

The sum of the DWR indicators is $\tfrac1{96}$, the exact error. The [residual estimator](/residual-error-estimator/) has the same value on both elements, so it would refine both, while the DWR method sees that the error on the right element does not change $J$ at all.

**Drag and lift.** In computational fluid dynamics, the drag coefficient is a boundary integral of the stress. DWR meshes for it refine near the body and in the parts of the flow upstream that influence the drag. In the flow examples of Becker and Rannacher, such meshes reach a given accuracy in the drag with fewer cells than meshes adapted for the energy error.

**Point values.** For $J(v) = v(x_0)$, the dual solution is the Green's function at $x_0$. It is singular in 2D and 3D, so in practice $J$ is replaced by a mean over a small ball around $x_0$.

## Variations

- **Higher order dual.** Solve the dual problem with elements of degree $k + 1$ on the same mesh. This is robust but costs more than the primal solve.
- **Recovered dual.** Solve the dual problem in the same space and use a higher order patch interpolation of $z_h$ as the weight. It is cheaper and works well on structured meshes.
- **Error correction.** The adjoint correction $J(u_h) + \sum_K\eta_K$ is often much more accurate than $J(u_h)$. Giles and Suli show that its error is of the order of the product of the primal and the dual errors, so the order of convergence of the output can double.
- **Multiple goals.** Combine several functionals into one by weights and signs, and solve one dual problem for the combination.
- **Effectivity and signs.** The signed sum can be small by cancellation even when the local terms are large. Use $\sum_K|\eta_K|$ for marking and the signed sum as the estimate of the error.

## Pitfalls

- **Using $z_h$ from the same space.** The weight $z_h - I_hz_h$ is then 0, or nearly so, and the estimate is 0 by Galerkin orthogonality. The dual must be approximated with more accuracy.
- **No guaranteed bound.** The estimate is not an upper bound in general. With an approximate dual solution, it is only asymptotically exact as the mesh is refined.
- **Cancellation.** Positive and negative local contributions can cancel, so a small estimate of $J(e)$ does not mean the local errors are small. Mark with absolute values.
- **Irregular goals.** A goal with a singular dual solution, such as a point value or a line integral in 3D, makes the weights large near the singular set and the estimate less reliable.
- **Cost and memory.** The dual problem doubles the work at least. For time dependent and nonlinear problems the backward dual solve needs the stored primal solution, which can dominate the memory.

## Exercises

1. Show that for a symmetric bilinear form and $J(v) = (f, v)$, the dual solution is $z = u$, and $J(u) - J(u_h) = |u - u_h|_a^2$. *Answer:* $a(v, z) = (f, v) = a(u, v)$, so $z = u$. Then $J(e) = a(e, u) = a(e, e) + a(e, u_h) = a(e, e)$ by Galerkin orthogonality.
2. In the local example, compute $\int_0^{1/2}(z - I_hz)$ by hand. *Answer:* $\tfrac12\int_0^{1/2}(\tfrac x2 - x^2) = \tfrac12(\tfrac1{16} - \tfrac1{24}) = \tfrac1{96}$.
3. Why is the error representation exact in 1D without the jump terms? *Answer:* the jump terms are tested with $z - I_hz$ at the nodes, and the nodal interpolant matches $z$ there.

## References
