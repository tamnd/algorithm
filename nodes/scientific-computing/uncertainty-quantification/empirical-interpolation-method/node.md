---
tag: 003ET5
kind: algorithm
slug: empirical-interpolation-method
name: Empirical interpolation method
area: scientific-computing/uncertainty-quantification
level: advanced
summary: Approximates a parametrized nonlinear function by interpolation at greedily chosen points in a basis of its snapshots, so online cost is mesh independent.
model: real-ram
complexity:
  vars: {n: the number of points of the grid that stands for the domain, m: the number of training parameters, M: the number of terms}
  time: {offline: "O(m n M^2 + m M^3)", online: "O(M^2)"}
  space: {extra: "O(m n + M n)"}
properties: {deterministic: true, exact: false, iterative: true, interpolatory: true}
history:
  year: 2004
  people: [Maxime Barrault, Yvon Maday, Ngoc Cuong Nguyen, Anthony T. Patera]
  note: Introduced to make reduced basis methods fast for problems with a coefficient that does not depend on the parameter in an affine way. The general form with magic points followed in 2009.
prereqs: [lagrange-interpolation, lebesgue-constant, reduced-basis-method]
see_also: [discrete-empirical-interpolation-method, weak-greedy-reduced-basis, pod-galerkin-reduced-model, kolmogorov-width, orthogonal-matching-pursuit, operator-inference]
sources:
  - paper: doi:10.1016/j.crma.2004.08.006
    title: Maxime Barrault, Yvon Maday, Ngoc Cuong Nguyen and Anthony T. Patera, An empirical interpolation method, application to efficient reduced-basis discretization of partial differential equations, Comptes Rendus Mathematique 339(9), 2004, 667-672
    locator: the greedy construction of the basis and the interpolation points, and the bound 2^M - 1 of the Lebesgue constant
  - paper: doi:10.3934/cpaa.2009.8.383
    title: Yvon Maday, Ngoc Cuong Nguyen, Anthony T. Patera and George S. H. Pau, A general multipurpose interpolation procedure, the magic points, Communications on Pure and Applied Analysis 8(1), 2009, 383-404
    locator: the magic points for a general family of functions, and the Lebesgue constant of the construction
  - book: isbn:9783319224695
    title: Jan S. Hesthaven, Gianluigi Rozza and Benjamin Stamm, Certified Reduced Basis Methods for Parametrized Partial Differential Equations, SpringerBriefs in Mathematics, Springer, 2016
    locator: Chapter 5, Section 5.2 (the empirical interpolation method)
---

The empirical interpolation method (EIM) replaces a function $g(x; \mu)$ of a space variable and a parameter by a sum $\sum_{j=1}^{M} c_j(\mu)\, q_j(x)$ with fixed basis functions $q_j$. The coefficients come from interpolation: they make the sum equal to $g$ at $M$ points $x_1, \ldots, x_M$, the magic points. A greedy loop over a training set of parameters chooses the basis and the points together. At each step it finds the parameter whose function is worst interpolated, takes its interpolation error as the next basis function, and takes the point where that error is largest as the next point. The online stage then needs only the $M$ values $g(x_i; \mu)$ and a triangular solve of size $M$. In a [reduced basis method](/reduced-basis-method/), this turns a coefficient that is not affine in $\mu$ into an affine sum with $M$ terms, so the online cost no longer depends on the mesh. The [discrete empirical interpolation method](/discrete-empirical-interpolation-method/) is the variant for vectors: it takes a [POD](/pod-galerkin-reduced-model/) basis that is computed first and then chooses only the points, with the same greedy rule. EIM chooses the basis and the points in the same loop, from the functions themselves.

## In plain words

A coefficient such as $1/(x + \mu)$ changes shape with $\mu$. If you store it on the mesh for each new $\mu$, every reduced solve has to touch the whole mesh again. EIM finds a few fixed shapes and a few special points. For a new $\mu$ you evaluate the function at those few points only, and the shapes, weighted to match those values, give the function everywhere. The points are chosen where the current approximation is worst, and the shapes are the errors that the earlier shapes left. So each new shape fixes the largest remaining error, and the points stay well spread.

## The problem

Let $\Omega_h = \{x^{(1)}, \ldots, x^{(n)}\}$ be a grid of points that stands for the domain, for example the quadrature points of a finite element mesh, and let $\|v\|_\infty = \max_{x \in \Omega_h} |v(x)|$. A function $g(x; \mu)$ can be evaluated for $x \in \Omega_h$ and $\mu$ in a parameter set $\mathcal{P}$. A training set $\Xi \subset \mathcal{P}$ has $m$ points. The input is $g$, $\Omega_h$, $\Xi$, a tolerance $\varepsilon_{tol}$ and a largest size $M_{max}$. The output is $M$ parameters $\mu_j$, points $x_j \in \Omega_h$ and functions $q_j$ on $\Omega_h$, such that the interpolant

$$I_M g(\cdot; \mu) = \sum_{j=1}^{M} c_j(\mu)\, q_j, \qquad \sum_{j=1}^{M} q_j(x_i)\, c_j(\mu) = g(x_i; \mu) \quad (i = 1, \ldots, M),$$

has $\max_{\mu \in \Xi} \|g(\cdot; \mu) - I_M g(\cdot; \mu)\|_\infty \le \varepsilon_{tol}$, or $M = M_{max}$. The matrix $B_{ij} = q_j(x_i)$ of the interpolation system must be invertible, and the method makes it lower triangular with a unit diagonal.

## The algorithm

```pseudo id=main
EIM(g, Ω_h, Ξ, ε_tol, M_max)
L1  M ← 0; r_μ ← g(·; μ) on Ω_h for each μ in Ξ               ▷ I_0 g = 0
L2  e(μ) ← max over Ω_h of |r_μ| for each μ in Ξ
L3  μ* ← the μ in Ξ with the largest e(μ)
L4  if e(μ*) ≤ ε_tol or M = M_max then
L5      return μ_1..μ_M, x_1..x_M, q_1..q_M, B
L6  M ← M + 1; μ_M ← μ*; r ← r_μ*                             ▷ the worst residual
L7  x_M ← the point of Ω_h with the largest |r(x)|
L8  q_M ← r / r(x_M)
L9  B_Mj ← q_j(x_M) for j = 1..M; B_iM ← 0 for i < M            ▷ B_MM = 1
L10 r_μ ← g(·; μ) - I_M g(·; μ) for each μ in Ξ, with B c = (g(x_i; μ))_i; go to L2
```

Line L1 starts with the empty interpolant, so the first residuals are the functions. Lines L2 and L3 find the worst interpolated training function in the max norm. Line L6 takes its residual $r = g(\cdot; \mu_M) - I_{M-1} g(\cdot; \mu_M)$. Line L7 chooses the new point where this residual is largest, and line L8 scales it to the value 1 there. The residual is 0 at the earlier points $x_1, \ldots, x_{M-1}$, because $I_{M-1}$ interpolates there. So $q_M(x_i) = 0$ for $i < M$, and line L9 only adds a row to $B$. Line L10 computes the new interpolants by forward substitution. The online stage for a new $\mu$ is the last part of line L10 for one function: evaluate $g(x_i; \mu)$ for $i \le M$, solve $B c = (g(x_i; \mu))_i$ in $O(M^2)$, and use $c(\mu)$ as the affine coefficients.

## Example

**By hand.** Take the grid $\{0, 1/2, 1\}$, $g(x; \mu) = 1 + \mu x^2$ and $\Xi = \{1, 3\}$. The functions are $(1, 1.25, 2)$ and $(1, 1.75, 4)$. Their max norms are 2 and 4, so $\mu_1 = 3$, $x_1 = 1$ and $q_1 = (0.25, 0.4375, 1)$. The interpolant of $g(\cdot; 1)$ is $2 q_1 = (0.5, 0.875, 2)$, so the residual is $(0.5, 0.375, 0)$, with its largest value $0.5$ at $x = 0$. Then $\mu_2 = 1$, $x_2 = 0$, $q_2 = (1, 0.75, 0)$ and

$$B = \begin{pmatrix} q_1(1) & q_2(1) \\ q_1(0) & q_2(0) \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ 0.25 & 1 \end{pmatrix} .$$

The span of $q_1$ and $q_2$ is the span of $1$ and $x^2$, so the residuals are now 0 and the loop stops with $M = 2$. For the new parameter $\mu = 2$ the online stage uses the values $g(1; 2) = 3$ and $g(0; 2) = 1$: $c_1 = 3$ and $c_2 = 1 - 0.25 \cdot 3 = 0.25$, and $3 q_1 + 0.25 q_2 = (1, 1.5, 3) = 1 + 2x^2$ on the grid.

**A singular family.** Take $g(x; \mu) = 1/(x + \mu)$ on $201$ equispaced points of $[0, 1]$, with the $51$ training values $\mu = 0.05 + 0.019 i$, $i = 0, \ldots, 50$, and $\varepsilon_{tol} = 10^{-8}$. The table is a measurement from the test file. The column $\varepsilon_M$ is the largest max-norm error over $\Xi$ after $M$ terms.

| $M$ | $\mu_M$ | $x_M$ | $\varepsilon_M$ |
|---|---|---|---|
| 0 | | | 20.0 |
| 1 | 0.050 | 0.000 | 1.802 |
| 2 | 0.126 | 0.080 | 0.3554 |
| 3 | 0.544 | 0.505 | $9.890 \times 10^{-2}$ |
| 5 | 1.000 | 1.000 | $5.700 \times 10^{-3}$ |
| 8 | 0.354 | 0.315 | $6.565 \times 10^{-6}$ |
| 11 | 0.107 | 0.125 | $6.958 \times 10^{-9}$ |

The loop stops at $M = 11$. The first parameter is the one with the largest function, $\mu = 0.05$, and its peak at $x = 0$ is the first point. The points gather near $x = 0$, where the functions change fastest: 0, 0.005, 0.02, 0.045, 0.08 and 0.125 are among the eleven. The second row of $B$ is $q_1(x_2) = (1/0.13)/(1/0.05) = 0.3846$. The Lebesgue constant is 1.00, 1.12, 1.63, 2.68, 3.87 and 3.53 for $M = 1, 2, 3, 5, 8, 11$, far below the bound $2^M - 1$, which is 2047 for $M = 11$. On a 101, 401 or 801 point grid the loop also stops at $M = 11$. On 400 test parameters between the training points, the largest error is $3.6 \times 10^{-5}$ for $M = 8$ and $5.7 \times 10^{-7}$ for $M = 11$, so the training set is too coarse near $\mu = 0.05$; see the pitfalls.

## Correctness

The proof file shows, in exact arithmetic, that the loop is well defined and stops, and that the interpolant has the bounds of a good interpolation scheme.

1. Each chosen residual is not 0, so line L8 does not divide by 0, and $q_M(x_i) = 0$ for $i < M$ and $q_M(x_M) = 1$. So $B$ is lower triangular with a unit diagonal and is invertible. Also $\|q_j\|_\infty = 1$.
2. $I_M$ interpolates: $I_M g(x_i; \mu) = g(x_i; \mu)$. It reproduces the span: $I_M v = v$ for $v \in \operatorname{span}\{q_1, \ldots, q_M\}$, and this span is the span of $g(\cdot; \mu_1), \ldots, g(\cdot; \mu_M)$.
3. With the Lagrange functions $\ell_j$ of the points ($\ell_j(x_i) = \delta_{ij}$, $\ell_j$ in the span) and the Lebesgue constant $\Lambda_M = \max_{\Omega_h} \sum_j |\ell_j(x)|$, every $g$ satisfies

$$\|g - I_M g\|_\infty \le (1 + \Lambda_M) \min_{v \in \operatorname{span}\{q_j\}} \|g - v\|_\infty, \qquad \Lambda_M \le 2^M - 1 .$$

4. On the finite set $\Xi$, the loop stops after at most $m$ steps, and if it stops by the tolerance, the error is at most $\varepsilon_{tol}$ at every $\mu \in \Xi$.

The bound $2^M - 1$ is a worst case. In practice the [Lebesgue constant](/lebesgue-constant/) grows slowly, as in the example. Compare it with the Lebesgue constant of [Lagrange interpolation](/lagrange-interpolation/) at fixed nodes: there the space is fixed and only the points are chosen; here both are adapted to the family.

## Complexity

In the [real RAM](/real-ram/) model, line L1 costs $m n$ evaluations of $g$. In step $M$, line L10 solves a triangular system of size $M$ for each training function, $O(m M^2)$, and forms the interpolants on the grid, $O(m n M)$. Lines L2, L3 and L7 cost $O(m n)$. The sum over $M$ steps is $O(m n M^2 + m M^3)$. Since $I_M g = I_{M-1} g + r(x_M)\, q_M$ for the residual $r$ of $g$, an implementation can update each residual by one term, $r_\mu \leftarrow r_\mu - r_\mu(x_M)\, q_M$, at a cost of $O(m n)$ per step and $O(m n M)$ in total. The implementation here solves again for simplicity. The online stage costs $M$ evaluations of $g$ and $O(M^2)$ for the solve, with no dependence on $n$. Memory is $O(m n)$ for the training functions and $O(M n)$ for the basis.

## Properties

- **Interpolatory.** The approximation is exact at the magic points, and exact for the training functions that were chosen.
- **Triangular.** $B$ is lower triangular with a unit diagonal, so the online solve is a forward substitution and is always possible.
- **Online cost independent of the mesh.** Only $M$ values of $g$ are needed.
- **Adapted points.** The points move to where the family changes fastest, without any knowledge of the formula of $g$.
- **Quasi-optimal up to $1 + \Lambda_M$.** The error is within the factor $1 + \Lambda_M$ of the best max-norm approximation in the same space.
- **No certified bound.** The error away from the training set is not bounded by the method.

## Variants and improvements

- **DEIM.** The [discrete empirical interpolation method](/discrete-empirical-interpolation-method/) takes the basis from the POD of snapshots and chooses only the points by the same rule. It is the usual choice for the nonlinear term of a POD-Galerkin model.
- **Generalized EIM.** Replace the point values by linear functionals, such as local averages or sensor responses, so the method works for functions in $L^2$ and for measured data.
- **Error estimate with one more point.** Use $|g(x_{M+1}; \mu) - I_M g(x_{M+1}; \mu)|$ as an estimate of the error. It is cheap, but it is a bound only under an assumption on the next term.
- **Discrete versions on the quadrature points.** In a finite element code the grid is the set of quadrature points, and the online assembly evaluates $g$ only in the elements that contain the magic points.
- **Nonlinear operators.** The same construction applies to $g(x; u(\mu))$, where $g$ depends on the solution, inside a Newton loop.

## When to use it

Use EIM inside a reduced basis or POD model when a coefficient, a source term or a nonlinear term depends on the parameter in a way that is not affine, and when the family of functions is smooth in the parameter, so that a few terms are enough. It needs point evaluations of $g$ and nothing else. Do not use it when the family has a slowly decaying [Kolmogorov width](/kolmogorov-width/), for example a moving front or a moving peak, because then $M$ becomes large. When the basis must come from data that is given as vectors, use DEIM.

## Pitfalls

- **A coarse training set.** The error is controlled only at the training parameters. In the example, the error between the training points is 80 times the training error at $M = 11$. Refine $\Xi$ where $g$ changes fast, or check on a test set.
- **The stopping tolerance near rounding.** When the residual is near the rounding level, line L8 divides by a tiny number and the new basis function is noise. Stop with a tolerance well above $\varepsilon_{mach} \max \|g\|_\infty$.
- **Using the Euclidean norm in line L2 but the max in line L7.** Both are valid, but the bound with $\Lambda_M$ is for the max norm. Keep the norms consistent with the claims.
- **Forgetting that the error adds to the model error.** In a reduced basis method with EIM, the error bound of the reduced model must account for the interpolation error, or it is no longer a bound.
- **Evaluating $g$ on the whole mesh online.** The gain is lost if the online stage forms $g$ on all of $\Omega_h$ and then samples it. Only the $M$ values are needed.

## Implementations

## History

Barrault, Maday, Nguyen and Patera introduced the empirical interpolation method in 2004, to keep the offline-online split of reduced basis methods for coefficients that are not affine in the parameter. Their note gives the greedy construction and the bound $2^M - 1$ of the Lebesgue constant. Maday, Nguyen, Patera and Pau presented the construction in 2009 as a general interpolation procedure, with the name magic points. Chaturantabut and Sorensen gave the discrete version DEIM in 2010.

## References
