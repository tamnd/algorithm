---
tag: YM1D2Z
kind: algorithm
slug: reduced-basis-method
name: Reduced basis method
area: scientific-computing/uncertainty-quantification
level: advanced
summary: For PDEs with parameters, builds a basis from solutions at a few chosen parameters, solves new cases by Galerkin projection, and certifies each answer with an a posteriori error bound.
model: real-ram
complexity:
  vars: {n: "the number of finite element unknowns, with banded matrices in 1D", r: the size of the reduced basis, Q: the number of affine terms}
  time: {offline: "O(Q^2 r^2 n)", online: "O(Q r^2 + r^3 + Q^2 r^2)"}
  space: {extra: "O(Q r n + Q^2 r^2)"}
properties: {deterministic: true, exact: false, iterative: false, certified: true}
history:
  year: 2002
  people: [Christophe Prud'homme, Dimitrios V. Rovas, Karen Veroy, Yvon Maday, Anthony T. Patera, Gabriel Turinici]
  note: Reduced bases from a few solutions were used in structural mechanics around 1980. The offline-online split with an a posteriori error bound is from the work of Patera and coworkers from 2002.
prereqs: [galerkin-method, finite-element-method, lax-milgram-theorem, gram-schmidt-process]
see_also: [weak-greedy-reduced-basis, pod-galerkin-reduced-model, empirical-interpolation-method, kolmogorov-width, cea-lemma, weak-formulation, multifidelity-monte-carlo, forward-uncertainty-propagation]
sources:
  - paper: doi:10.1115/1.1448332
    title: Christophe Prud'homme, Dimitrios V. Rovas, Karen Veroy, Luc Machiels, Yvon Maday, Anthony T. Patera and Gabriel Turinici, Reliable real-time solution of parametrized partial differential equations, reduced-basis output bound methods, Journal of Fluids Engineering 124(1), 2002, 70-80
    locator: the affine parameter dependence, the offline-online computation and the output bounds
  - paper: doi:10.1007/s11831-008-9019-9
    title: Gianluigi Rozza, D. B. Phuong Huynh and Anthony T. Patera, Reduced basis approximation and a posteriori error estimation for affinely parametrized elliptic coercive partial differential equations, Archives of Computational Methods in Engineering 15(3), 2008, 229-275
    locator: the affine decomposition, the offline-online computation of the dual norm of the residual, and the error bounds with a lower bound of the coercivity constant (including the min-theta bound)
  - book: isbn:9783319224695
    title: Jan S. Hesthaven, Gianluigi Rozza and Benjamin Stamm, Certified Reduced Basis Methods for Parametrized Partial Differential Equations, SpringerBriefs in Mathematics, Springer, 2016
    locator: Chapter 3 (reduced basis methods, offline and online) and Chapter 4 (certified error control)
  - book: isbn:9783319154305
    title: Alfio Quarteroni, Andrea Manzoni and Federico Negri, Reduced Basis Methods for Partial Differential Equations, An Introduction, UNITEXT 92, Springer, 2016
    locator: Chapter 3 (basic principles and properties of reduced basis methods)
---

The reduced basis method solves a parametrized PDE fast and many times, for example for a sweep of a material coefficient or for the samples of a Monte Carlo study. It solves the full finite element problem, the truth, at a few parameter values $\mu_1, \ldots, \mu_r$. The span of these solutions is the reduced space. For a new $\mu$ it finds the [Galerkin](/galerkin-method/) approximation in this space, which is a linear system of size $r$. It also returns a bound $\Delta(\mu)$ that is at least the true error, computed from the residual and a lower bound of the coercivity constant. If the matrix depends on $\mu$ in an affine way, all the work that involves the $n$ unknowns of the mesh is done once, in the offline stage. Each online query then costs a number of operations that does not depend on $n$. The [POD-Galerkin reduced-order model](/pod-galerkin-reduced-model/) uses the same projection, but takes its basis from time snapshots of one run and has no certified bound. The [weak greedy algorithm](/weak-greedy-reduced-basis/) chooses the parameters $\mu_j$ with the bound $\Delta$, and the [Kolmogorov width](/kolmogorov-width/) of the solution set says how small $r$ can be. The [empirical interpolation method](/empirical-interpolation-method/) makes a non-affine problem affine.

## In plain words

You must solve the same PDE for a thousand values of a parameter. Each solve on a fine mesh takes time. But the solutions for different parameters look alike, so a few of them, added with the right weights, describe the rest well. The reduced basis method solves the fine problem for a few parameters, keeps those solutions as building blocks, and finds the best weights for each new parameter from a tiny system.

The method also tells you how much to trust each answer. It puts the cheap answer back into the fine equation and measures how much is left over, the residual. A small residual means a small error, and a stability constant turns one into a bound on the other. With some care, both the weights and the bound come out of small precomputed tables, so a query does not touch the fine mesh.

## The problem

Let $X$ be a finite element space of dimension $n$ with an inner product $(u, v)_X = u^T X v$, where $X$ is now also its symmetric positive definite matrix. For each parameter $\mu$ in a set $\mathcal{P}$, a bilinear form $a(\cdot, \cdot; \mu)$ and a load $F$ define the truth solution $u(\mu) \in X$ by

$$a(u(\mu), v; \mu) = F(v) \quad \text{for all } v \in X .$$

The form is coercive and continuous in the $X$ norm, with constants $\alpha(\mu) > 0$ and $\gamma(\mu)$, so by the [Lax-Milgram theorem](/lax-milgram-theorem/) $u(\mu)$ exists and is unique. The form is affine: $a(u, v; \mu) = \sum_{q=1}^{Q} \theta_q(\mu)\, a_q(u, v)$, with matrices $A_q$ that do not depend on $\mu$. A lower bound $\alpha_{LB}(\mu)$ with $0 < \alpha_{LB}(\mu) \le \alpha(\mu)$ is known and cheap to evaluate.

Given sample parameters $\mu_1, \ldots, \mu_r$ with linearly independent truth solutions and a query $\mu$, the output is the reduced solution $u_r(\mu) \in X_r = \operatorname{span}\{u(\mu_1), \ldots, u(\mu_r)\}$ with $a(u_r, v; \mu) = F(v)$ for all $v \in X_r$, and a bound $\Delta(\mu) \ge \|u(\mu) - u_r(\mu)\|_X$.

**The model problem** of the example and the tests is $-u'' + \mu u = 1$ on $(0, 1)$ with $u(0) = u(1) = 0$ and $\mu \in [1, 100]$, in P1 [finite elements](/finite-element-method/) on a uniform mesh with $n$ interior nodes and $h = 1/(n+1)$. Then $A(\mu) = K + \mu M$ with the stiffness matrix $K$ and the mass matrix $M$, so $Q = 2$, $\theta_1 = 1$ and $\theta_2 = \mu$. The inner product is $X = K + \bar{\mu} M$ with $\bar{\mu} = 10$. Since $v^T A(\mu) v = v^T K v + \mu\, v^T M v \ge \min(1, \mu/\bar{\mu})\, v^T X v$, the min-theta bound $\alpha_{LB}(\mu) = \min(1, \mu/\bar{\mu})$ is a valid lower bound, and in the same way $\gamma(\mu) \le \max(1, \mu/\bar{\mu})$. The exact solution is $u(x) = \mu^{-1}\big(1 - \cosh(\sqrt{\mu}(x - 1/2)) / \cosh(\sqrt{\mu}/2)\big)$.

## The algorithm

```pseudo id=main
REDUCED-BASIS(A_1..A_Q, F, X, μ_1..μ_r; query μ)
    ▷ offline stage, once
L1  solve A(μ_j) u_j = F for j = 1..r                                 ▷ r truth solves
L2  Z ← [z_1 ... z_r], an X-orthonormal basis of span{u_1..u_r} by Gram-Schmidt
L3  A_q^r ← Z^T A_q Z for q = 1..Q;  F_r ← Z^T F
L4  e_F ← X^(-1) F;  e_qj ← X^(-1) A_q z_j;  store G_FF = F^T e_F, g_qj = F^T e_qj, G_qp,ij = (A_q z_i)^T e_pj
    ▷ online stage, for each query μ
L5  solve (Σ_q θ_q(μ) A_q^r) c = F_r
L6  ρ² ← G_FF - 2 Σ_q θ_q Σ_j c_j g_qj + Σ_q Σ_p θ_q θ_p Σ_i Σ_j c_i c_j G_qp,ij
L7  Δ ← sqrt(max(ρ², 0)) / α_LB(μ)
L8  return u_r = Z c, Δ, the output s_r = F_r^T c and its bound Δ_s = ρ² / α_LB(μ)
```

Line L1 is the only place where the truth problem is solved, $r$ times. Line L2 orthonormalizes the snapshots in the $X$ inner product; the implementation runs Gram-Schmidt twice per vector and stops with an error if the snapshots are dependent. Line L3 projects each affine term once. Line L4 computes the Riesz representers of $F$ and of each $A_q z_j$, that is the solutions of $X e = F$ and $X e = A_q z_j$, and stores their inner products. These $1 + Q r$ solves with $X$ and the tables are the price of the bound. Line L5 assembles the $r$ by $r$ matrix from $Q$ small matrices. Line L6 expands $\rho^2 = R^T X^{-1} R$ for the residual vector $R = F - A(\mu) Z c$, by the affine sum, so it uses only the tables. Line L7 divides by the stability lower bound. The compliance output $s(\mu) = F(u(\mu))$ in line L8 has its own bound. Lines L5 to L8 cost a number of operations that depends on $r$ and $Q$, not on $n$, except for the lift $Z c$, which a user who wants only $s_r$ can skip.

## Example

The mesh has $n = 99$ interior nodes ($h = 0.01$), the samples are $\mu_j = 1, 10, 100$, so $r = 3$, and $\bar{\mu} = 10$. At $\mu = 10$ the truth value at $x = 1/2$ is $0.0605253$; the exact value is $0.0605229$, so the finite element error is $2.4 \times 10^{-6}$. The reduced basis method approximates the truth, not the exact solution. The table gives the online results (a measurement, from the test file).

| $\mu$ | $\alpha_{LB}$ | $\gamma / \alpha_{LB}$ | $\|u - u_r\|_X$ | $\Delta$ | $\Delta / \|u - u_r\|_X$ | $s_r$ | $s - s_r$ |
|---|---|---|---|---|---|---|---|
| 2 | 0.2 | 5 | $7.528 \times 10^{-6}$ | $3.690 \times 10^{-5}$ | 4.90 | 0.0694652 | $5.6 \times 10^{-11}$ |
| 3 | 0.3 | 3.33 | $1.184 \times 10^{-5}$ | $3.878 \times 10^{-5}$ | 3.28 | 0.0641482 | $1.4 \times 10^{-10}$ |
| 10 | 1 | 1 | $5.4 \times 10^{-15}$ | $5.3 \times 10^{-9}$ | | 0.0418882 | $1.1 \times 10^{-15}$ |
| 30 | 1 | 3 | $7.795 \times 10^{-5}$ | $8.157 \times 10^{-5}$ | 1.05 | 0.0212615 | $6.4 \times 10^{-9}$ |
| 60 | 1 | 6 | $9.115 \times 10^{-5}$ | $1.012 \times 10^{-4}$ | 1.11 | 0.0123660 | $9.2 \times 10^{-9}$ |

In each row the bound is above the error, and the effectivity $\Delta / \|u - u_r\|_X$ is below $\gamma / \alpha_{LB}$, as the correctness section proves. You can check the second and third columns by hand: at $\mu = 3$, $\alpha_{LB} = \min(1, 3/10) = 0.3$ and $\gamma \le \max(1, 0.3) = 1$. The effectivity grows as $\mu$ falls below $\bar{\mu}$, because the min-theta bound is then pessimistic: for the smoothest mode $v = \sin(\pi x)$, the ratio $a(v, v; \mu) / \|v\|_X^2$ is close to $(\pi^2 + \mu)/(\pi^2 + \bar{\mu})$, which is 0.60 at $\mu = 2$, not 0.2. At the sample $\mu = 10$, the reduced solution is the truth up to rounding, but $\Delta$ is $5.3 \times 10^{-9}$, not $10^{-15}$: see the pitfalls. The output error $s - s_r$ is positive and about the square of the error, as the compliance lemma says. At $\mu = 30$, the error is $2.49 \times 10^{-3}$ with the two samples $1, 100$, $7.79 \times 10^{-5}$ with $1, 10, 100$, and $8.90 \times 10^{-7}$ with $1, 4, 20, 100$.

## Correctness

The proof file shows four facts, for a symmetric or non-symmetric coercive form. First, the reduced problem of line L5 has a unique solution, because $a$ is coercive on the subspace $X_r$. Second, with $e = u - u_r$ and the Riesz representer $\hat{e}$ of the residual ($X \hat{e} = R$),

$$\|e\|_X \le \frac{\|\hat{e}\|_X}{\alpha(\mu)} \le \frac{\|\hat{e}\|_X}{\alpha_{LB}(\mu)} = \Delta(\mu), \qquad \frac{\Delta(\mu)}{\|e\|_X} \le \frac{\gamma(\mu)}{\alpha_{LB}(\mu)} .$$

So the bound is reliable, and it is never worse than the error by more than a factor that does not depend on $r$ or $n$. Third, the quantity $\rho^2$ of line L6 is exactly $\|\hat{e}\|_X^2$. Fourth, for a symmetric form and the compliance output, $0 \le s - s_r = a(e, e; \mu) \le \rho^2 / \alpha_{LB}(\mu)$. The proof also shows that $u_r(\mu_j) = u(\mu_j)$ at each sample. For a symmetric form, $u_r$ is the best approximation of $u$ in $X_r$ in the energy norm of $\mu$, by [Cea's lemma](/cea-lemma/).

## Complexity

In the [real RAM](/real-ram/) model, the offline stage costs $r$ truth solves in line L1 and $1 + Q r$ solves with $X$ in line L4. For a 1D problem with tridiagonal matrices each solve costs $O(n)$; the implementation uses dense Gaussian elimination for simplicity. Lines L2 to L4 also cost $O(n r^2)$ for Gram-Schmidt and $O(Q^2 r^2 n)$ for the tables, with sparse $A_q$ and $X$. The online stage costs $O(Q r^2)$ to assemble the reduced matrix, $O(r^3)$ to solve it and $O(Q^2 r^2)$ for line L6, with no dependence on $n$. The tables need $O(Q^2 r^2)$ memory and the representers $O(Q r n)$ during the offline stage. The method pays off when the number of queries times the cost of a truth solve is much larger than the offline cost.

## Properties

- **Certified.** Each answer comes with a bound that is proved to hold, if $\alpha_{LB}$ is a true lower bound and the arithmetic is exact.
- **Effective.** The bound overestimates by at most $\gamma / \alpha_{LB}$, independent of $r$ and $n$.
- **Interpolatory.** At the sample parameters, the reduced solution equals the truth.
- **Online cost independent of $n$.** This needs the affine form. Without it, line L5 must assemble $A(\mu)$ on the mesh at each query.
- **Approximates the truth.** The bound is on the distance to the finite element solution, not to the solution of the PDE. The discretization error is separate.
- **Intrusive.** Lines L3 and L4 need the matrices $A_q$ of the finite element code.

## Variants and improvements

- **Greedy sampling.** The [weak greedy algorithm](/weak-greedy-reduced-basis/) chooses $\mu_{j+1}$ where $\Delta$ is largest over a training set, so the basis is built with $r$ truth solves only.
- **POD sampling.** Take many snapshots and keep their leading POD modes, as in the [POD-Galerkin model](/pod-galerkin-reduced-model/). This costs more truth solves but needs no error bound.
- **Successive constraint method.** When no simple formula like min-theta gives $\alpha_{LB}$, a small linear program per query gives a lower bound from the coercivity constants at a few parameters.
- **Non-affine problems.** The [empirical interpolation method](/empirical-interpolation-method/) replaces a non-affine coefficient by an affine sum with $Q$ terms, at the cost of an extra error.
- **Time-dependent and non-coercive problems.** Parabolic problems use a POD-greedy method in time and parameter. Non-coercive problems such as Helmholtz use the inf-sup constant in place of $\alpha$.
- **Primal-dual outputs.** For an output other than the compliance, a dual problem gives an output bound that is the product of the primal and dual residuals.

## When to use it

Use the reduced basis method when a parametrized elliptic or parabolic PDE must be solved many times, in a real-time or many-query setting such as optimization, control, [forward uncertainty propagation](/forward-uncertainty-propagation/) or Bayesian inversion, and when the solution set has a small [Kolmogorov width](/kolmogorov-width/), that is when a few solutions describe all of them. Smooth dependence on a few parameters is the good case. Do not use it when the parameter moves a shock or a front, when there are tens of parameters with no structure, or when you need only a few solves. If you cannot change the solver, use a non-intrusive model such as [operator inference](/operator-inference/) or a [Gaussian process](/gaussian-process/) emulator, with no certified bound.

## Pitfalls

- **A lower bound that is not a lower bound.** If line L7 uses an estimate of $\alpha(\mu)$ that is too large, for example the value at a nearby parameter, the bound can fall below the true error. The min-theta bound holds here because all $\theta_q$ and all $a_q$ are positive; it fails for a form with a term of either sign.
- **The square root floor.** Line L6 forms $\rho^2$ as a difference of numbers of size $\|F\|^2$. Rounding errors of size $\varepsilon_{mach} \|F\|_{X'}^2$ give $\rho \approx \sqrt{\varepsilon_{mach}} \|F\|_{X'}$ even when the error is 0. In the example, $\Delta = 5.3 \times 10^{-9}$ at a sample point. Tolerances in a greedy loop must be well above this floor, or the residual must be computed in a stable way.
- **Clipping a negative value.** Line L7 takes $\max(\rho^2, 0)$. A negative $\rho^2$ means rounding, not a negative error; do not take the absolute value of a large negative number, which is a sign of a bug in the tables.
- **The wrong inner product.** The bound is in the norm of $X$. If line L2 orthonormalizes in the Euclidean product but line L4 uses $X$, the tables do not match the norm of the bound. Use the same $X$ in both lines.
- **Affine terms done online.** If line L5 assembles $A(\mu)$ on the mesh and then projects it, the online cost is $O(n r)$ per query or more, and the method is no faster than a good truth solver for small $n$.
- **Dependent snapshots.** Two samples that are equal or very close make Gram-Schmidt in line L2 divide by a tiny norm. The implementation raises an error; a greedy choice avoids the problem in practice because the bound at a sample is near zero.

## Implementations

## History

Reduced bases built from a few solutions were used in nonlinear structural analysis around 1980, by Almroth, Stern and Brogan and by Noor and Peters, to follow a load path. The modern method, with a global basis over the parameter domain, a rigorous a posteriori error bound and the offline-online split for affine problems, comes from Patera, Maday and their coworkers. Prud'homme, Rovas, Veroy, Machiels, Maday, Patera and Turinici published the output bound method in 2002. Rozza, Huynh and Patera wrote the standard review of the coercive case in 2008, with the min-theta and successive constraint lower bounds. The books of Hesthaven, Rozza and Stamm and of Quarteroni, Manzoni and Negri appeared in 2015 and 2016.

## References
