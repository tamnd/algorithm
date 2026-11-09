---
tag: 54MPPW
kind: algorithm
slug: bfgs
name: BFGS method
aliases:
- Broyden-Fletcher-Goldfarb-Shanno method
- BFGS
- BFGS update
area: optimization/gradient-methods
level: advanced
summary: "Quasi-Newton method: step along -H_k∇f(x_k), then update H by a rank-two formula so that H_(k+1) y_k = s_k. It keeps H positive definite under Wolfe steps; the local rate is superlinear."
solves: [unconstrained-smooth-minimization]
model: real-ram
complexity:
  vars: {n: the number of variables, k: the number of iterations, m: the largest number of trial steps in one line search}
  time: {worst: O(k (n^2 + m n))}
  space: {extra: O(n^2)}
  gradients: {quadratic_exact_steps: O(n), step: O(m)}
properties: {deterministic: true, iterative: true, descent_method: true, first_order: true, finite_termination_on_quadratics: true}
history:
  year: 1970
  people: [Charles G. Broyden, Roger Fletcher, Donald Goldfarb, David F. Shanno]
  note: Broyden, Fletcher, Goldfarb and Shanno each published the update in 1970, by different arguments.
prereqs: [quasi-newton-method, wolfe-conditions, positive-definite-matrix]
see_also: [limited-memory-bfgs, quasi-newton-method, nonlinear-conjugate-gradient, wolfe-conditions, broyden-method, newton-method-for-systems, sherman-morrison-formula, cholesky-decomposition]
sources:
  - paper: doi:10.1093/imamat/6.1.76
    title: Charles G. Broyden, The convergence of a class of double-rank minimization algorithms 1. General considerations, IMA Journal of Applied Mathematics 6(1), 1970
    locator: pages 76 to 90
  - paper: doi:10.1093/comjnl/13.3.317
    title: Roger Fletcher, A new approach to variable metric algorithms, The Computer Journal 13(3), 1970
    locator: pages 317 to 322
  - paper: doi:10.1090/S0025-5718-1970-0258249-6
    title: Donald Goldfarb, A family of variable-metric methods derived by variational means, Mathematics of Computation 24(109), 1970
    locator: pages 23 to 26
  - paper: doi:10.1090/S0025-5718-1970-0274029-X
    title: David F. Shanno, Conditioning of quasi-Newton methods for function minimization, Mathematics of Computation 24(111), 1970
    locator: pages 647 to 656
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Section 6.1, The BFGS method, and Section 6.4, Convergence analysis (global convergence on uniformly convex functions and the superlinear rate)
  - paper: doi:10.1090/S0025-5718-1974-0343581-1
    title: John E. Dennis Jr. and Jorge J. Moré, A characterization of superlinear convergence and its application to quasi-Newton methods, Mathematics of Computation 28(126), 1974
    locator: pages 549 to 560
  - paper: doi:10.1137/0726042
    title: Richard H. Byrd and Jorge Nocedal, A tool for the analysis of quasi-Newton methods with application to unconstrained minimization, SIAM Journal on Numerical Analysis 26(3), 1989
    locator: pages 727 to 739
  - paper: doi:10.1137/0724077
    title: Richard H. Byrd, Jorge Nocedal and Ya-Xiang Yuan, Global convergence of a class of quasi-Newton methods on convex problems, SIAM Journal on Numerical Analysis 24(5), 1987
    locator: pages 1171 to 1190
  - paper: doi:10.1137/S1052623401383455
    title: Yu-Hong Dai, Convergence properties of the BFGS algorithm, SIAM Journal on Optimization 13(3), 2002
    locator: pages 693 to 701 (a nonconvex example on which BFGS with a Wolfe line search does not converge)
  - paper: doi:10.1007/s10107-003-0421-7
    title: Walter F. Mascarenhas, The BFGS method with exact line searches fails for non-convex objective functions, Mathematical Programming 99(1), 2004
    locator: pages 49 to 61
---

BFGS is the standard [quasi-Newton method](/quasi-newton-method/) for smooth unconstrained minimization. It keeps a symmetric positive definite matrix $H_k$ that approximates the inverse Hessian, steps along $d_k = -H_k\nabla f(x_k)$ with a [Wolfe](/wolfe-conditions/) line search that tries $\alpha = 1$ first, and then updates
$$H_{k+1} = (I - \rho_ks_ky_k^\top)H_k(I - \rho_ky_ks_k^\top) + \rho_ks_ks_k^\top, \qquad \rho_k = \frac{1}{y_k^\top s_k},$$
with $s_k = x_{k+1} - x_k$ and $y_k = \nabla f(x_{k+1}) - \nabla f(x_k)$. The update satisfies the secant equation $H_{k+1}y_k = s_k$, costs $O(n^2)$, and keeps $H$ positive definite whenever $y_k^\top s_k > 0$, which the Wolfe conditions ensure. On a strictly convex quadratic with exact line searches it stops after at most $n$ steps with $H_n = A^{-1}$. Near a minimizer with a positive definite and Lipschitz continuous Hessian it converges superlinearly.

## In plain words

Newton's method needs the curvature of the function, which is often not available. BFGS starts with a plain guess of the curvature and improves it after every step. Each step shows how much the slope changed over the distance walked, and that is a measurement of the curvature along the step. BFGS changes its guess so that it agrees with this measurement and changes it as little as it can in the other directions.

The guess always describes a bowl that opens upward, so the direction it gives always goes downhill. After enough steps the guess is close to the true curvature along the path, and the steps become almost as good as Newton's steps, but each one costs much less.

## The problem

The input is a continuously differentiable function $f : \mathbb{R}^n \to \mathbb{R}$, given by routines for $f$ and $\nabla f$, a start $x_0$, an optional symmetric positive definite $H_0$, an iteration limit $K$ and a gradient tolerance $\varepsilon$. The output is a point $x_k$ with $\|\nabla f(x_k)\| \le \varepsilon$, or the last point reached. This is [unconstrained smooth minimization](/unconstrained-smooth-minimization/); for nonconvex $f$ the method looks for a stationary point. All arithmetic is in floating point.

## The algorithm

```pseudo id=main
BFGS(f, ∇f, x₀, H₀, K, ε)
L1  x ← x₀; g ← ∇f(x); H ← H₀, or I if no H₀ is given
L2  for k = 0, 1, …, K − 1 while ‖g‖ > ε do
L3      d ← −H g
L4      α ← a step along d that satisfies the strong Wolfe conditions, trying α = 1 first
L5      s ← α d; x ← x + s; g⁺ ← ∇f(x); y ← g⁺ − g
L6      if k = 0 and no H₀ is given then H ← (yᵀs / yᵀy) I
L7      if yᵀs > 0 then ρ ← 1/(yᵀs); H ← (I − ρ s yᵀ) H (I − ρ y sᵀ) + ρ s sᵀ
L8      g ← g⁺
L9  return x
```

Line L3 is the quasi-Newton direction; it goes downhill because $H$ is positive definite. Line L4 is a strong Wolfe line search by bracketing and zoom (Nocedal and Wright, Algorithms 3.5 and 3.6) with $c_1 = 10^{-4}$ and $c_2 = 0.9$; if it fails within $100$ trial points, the method stops. Line L6 rescales the start matrix after the first step so that its size matches the curvature $y^\top s/y^\top y$ along that step; this changes only the later directions. Line L7 is the update. With $v = Hy$ it expands to
$$H^+ = H - \rho(sv^\top + vs^\top) + (\rho^2y^\top v + \rho)ss^\top,$$
which takes $O(n^2)$ operations. The test $y^\top s > 0$ always passes after a Wolfe step; it guards against rounding and against callers that pass their own steps.

## Example

Take $f(x) = \frac12(x_1^2 + 10x_2^2)$, so $A = \operatorname{diag}(1, 10)$, and $x_0 = (10, 1)$, $H_0 = I$:

| $k$ | $x_k$ | $\alpha_k$ | $H_k$ |
|---|---|---|---|
| 0 | $(10, 1)$ | $2/11$ | $I$ |
| 1 | $(8.1818, -0.8182)$ | $1$ | $\begin{pmatrix} 0.2709 & 0.0729 \\ 0.0729 & 0.0927 \end{pmatrix}$ |
| 2 | $(6.5617, -0.6562)$ | $1$ | $\begin{pmatrix} 1 & 0 \\ 0 & 0.1 \end{pmatrix} = A^{-1}$ |
| 3 | $(0, 0)$ | | |

The first direction is $-g_0 = (-10, -10)$; the trial $\alpha = 1$ fails the Armijo test, and the quadratic interpolation of the zoom phase lands on the exact minimizer $2/11$ along the line. The second step accepts $\alpha = 1$ at once, because the curvature condition holds with $c_2 = 0.9$. After two updates $H_2 = A^{-1}$ exactly, so the third direction is the Newton step and lands on the minimizer. The reason: the first step is exact, so $s_1^\top As_0 = -\alpha_1g_1^\top H_1y_0 = -\alpha_1g_1^\top s_0 = 0$, and then $H_2$ satisfies both $H_2y_0 = s_0$ and $H_2y_1 = s_1$, which fixes $H_2 = A^{-1}$ in two dimensions. With exact steps at every iteration the method stops after two steps.

On the Rosenbrock function $100(x_2 - x_1^2)^2 + (1 - x_1)^2$ from $(-1.2, 1)$, the implementation reaches $\|\nabla f\| \le 10^{-6}$ after $36$ steps and $61$ values of $f$ in the line searches. With tolerance $10^{-8}$ it takes $37$ steps, $27$ of them with $\alpha = 1$, and the last distances to the minimizer $(1, 1)$ are $4.2 \cdot 10^{-2}$, $1.4 \cdot 10^{-2}$, $3.1 \cdot 10^{-3}$, $3.7 \cdot 10^{-4}$, $4.4 \cdot 10^{-5}$, $6.7 \cdot 10^{-6}$, $1.8 \cdot 10^{-7}$ and $2.3 \cdot 10^{-12}$. The ratio of successive errors falls toward $0$, which is the superlinear rate. For comparison, the PR+ [nonlinear conjugate gradient](/nonlinear-conjugate-gradient/) method needs $19$ steps but $153$ values of $f$, and steepest descent with a strong Wolfe search needs $381$ steps, both to $10^{-6}$.

## Correctness

Let $g_k = \nabla f(x_k)$. The proofs of claims 1 to 4 are in the correctness proof of this page.

1. **Secant equation and symmetry.** If $y^\top s > 0$, the update gives a symmetric $H^+$ with $H^+y = s$.
2. **Positive definiteness.** If $H$ is symmetric positive definite and $y^\top s > 0$, then $H^+$ is symmetric positive definite. With Wolfe steps, $y_k^\top s_k \ge (1 - c_2)\alpha_k|g_k^\top d_k| > 0$, so every $H_k$ is positive definite, every $d_k$ is a descent direction, $f$ decreases at every step, and the method stops after at most $K$ iterations.
3. **Quadratic termination.** Let $f(x) = \frac12x^\top Ax - b^\top x$ with $A$ symmetric positive definite, and let every step be exact. Then the steps are $A$-conjugate, $H_{k+1}y_j = s_j$ for all $j \le k$, $g_k = 0$ for some $k \le n$, and if $n$ steps are taken, $H_n = A^{-1}$.
4. **Same as conjugate gradient.** Under the conditions of claim 3 with $H_0 = I$ and no rescaling, the iterates are those of the linear [conjugate gradient method](/conjugate-gradient-method/).

The following two theorems are proved in the cited sources; this page states them with their assumptions.

- **Global convergence on uniformly convex functions** (Powell, 1976; Nocedal and Wright, Section 6.4). Let $f$ be twice continuously differentiable, let the level set $\Omega = \{x : f(x) \le f(x_0)\}$ be convex, and let there be constants $0 < m \le M$ with $m\|z\|^2 \le z^\top\nabla^2f(x)z \le M\|z\|^2$ for all $x \in \Omega$ and all $z$. Let $H_0$ be symmetric positive definite and let every step satisfy the Wolfe conditions. Then $x_k$ converges to the unique minimizer $x^*$. Byrd and Nocedal showed that the convergence is R-linear, so $\sum_k\|x_k - x^*\| < \infty$.
- **Superlinear rate** (Nocedal and Wright, Section 6.4, after Dennis and Moré). Let $f$ be twice continuously differentiable, let $x_k \to x^*$ with $\nabla^2f(x^*)$ positive definite, let $\nabla^2f$ be Lipschitz continuous near $x^*$, and let $\sum_k\|x_k - x^*\| < \infty$. Then the BFGS matrices satisfy the Dennis-Moré condition $\|(H_k^{-1} - \nabla^2f(x^*))s_k\|/\|s_k\| \to 0$, the line search with $c_1 < \frac12$ eventually accepts $\alpha_k = 1$, and $\|x_{k+1} - x^*\| = o(\|x_k - x^*\|)$.

For nonconvex functions there is no such guarantee. Dai (2002) built a smooth example on which BFGS with a Wolfe line search does not reach a stationary point, and Mascarenhas (2004) did the same for exact line searches.

## Complexity

One iteration costs $O(n^2)$ for the product $Hg$ and the update, plus a line search with $m$ trial points at $O(n)$ each and $m$ values of $f$ and $\nabla f$. So $k$ iterations cost $O(k(n^2 + mn))$ arithmetic. The matrix $H$ needs $n^2$ numbers, so the extra space is $O(n^2)$. Near the solution the line search usually accepts $\alpha = 1$ at the first trial, so $m = 1$ there. Newton's method costs $O(n^3)$ per iteration for the solve, plus the Hessian.

| claim | value |
|---|---|
| time per iteration | $O(n^2 + mn)$ plus $m$ values of $f$ and $\nabla f$ |
| extra space | $O(n^2)$ |
| iterations on a quadratic with exact steps | at most $n$ |
| local rate | superlinear, under the assumptions above |

## Properties

- **Positive definite.** $H_k$ stays symmetric positive definite under Wolfe steps, so every direction goes downhill.
- **Invariant under linear changes of variables, with care.** If $x = Tz$ and $H_0$ is replaced by $T^{-1}H_0T^{-\top}$, the iterates in $z$ are the images of the iterates in $x$. With $H_0 = I$ in both coordinate systems this fails, so the method depends on the scaling through $H_0$.
- **Least change.** The BFGS $H^+$ is the symmetric matrix with $H^+y = s$ that is closest to $H$ in a weighted Frobenius norm whose weight is any matrix $W$ with $Ws = y$ (Nocedal and Wright, Section 6.1).
- **Self-correcting.** If $H$ has wrong curvature along some direction, later updates correct it within a few steps when the line search is a Wolfe search; this is the main practical advantage over DFP.
- **No second derivatives.** It needs only $f$ and $\nabla f$.

## Variants and improvements

- **Direct form with a Cholesky factor.** Update $B = H^{-1}$ by $B^+ = B - \frac{Bss^\top B}{s^\top Bs} + \frac{yy^\top}{y^\top s}$, keep its [Cholesky factor](/cholesky-decomposition/) and update the factor in $O(n^2)$. The inverse and direct forms are related by the [Sherman-Morrison formula](/sherman-morrison-formula/).
- **Limited memory.** [L-BFGS](/limited-memory-bfgs/) stores only the last few pairs $(s, y)$ and costs $O(mn)$ per step.
- **Damped BFGS.** For constrained problems, where $y^\top s$ can be negative, Powell's damping replaces $y$ by $\theta y + (1 - \theta)Bs$ with $\theta$ chosen so that $s^\top y \ge 0.2\,s^\top Bs$.
- **Bound constraints.** L-BFGS-B handles bounds $l \le x \le u$ with a projected search.
- **The Broyden class and DFP.** BFGS is one member of a one-parameter family of updates; see [quasi-Newton method](/quasi-newton-method/).

## When to use it

Use BFGS for smooth problems with up to a few thousand variables when the gradient is available and the Hessian is not, or is too expensive. It is the default method of many libraries for this case. For larger $n$, use [L-BFGS](/limited-memory-bfgs/). If the Hessian is cheap and the problem is small, Newton's method with a line search needs fewer iterations. For a quadratic objective, use the linear [conjugate gradient method](/conjugate-gradient-method/) or a [Cholesky](/cholesky-decomposition/) solve.

## Pitfalls

- **Backtracking without the curvature condition.** Then $y^\top s$ can be negative, and $H$ loses positive definiteness. Use a Wolfe search, or skip the update when $y^\top s \le 10^{-8}\|s\|\|y\|$.
- **A line search that does not try α = 1.** The superlinear rate needs unit steps near the solution.
- **Poor scaling of H₀.** With $H_0 = I$ the first step can be far too long or too short; rescale with $y^\top s/y^\top y$, as line L6 does.
- **Memory.** The matrix needs $8n^2$ bytes; for $n = 10^5$ that is $80$ gigabytes.
- **Nonconvex functions.** The method can fail to converge (Dai, 2002; Mascarenhas, 2004), and near a saddle point the update may never see negative curvature.
- **Noisy gradients.** Errors in $\nabla f$ make $y$ inaccurate for short steps and can make $H$ ill conditioned.

## Implementations

The Python module has the method in inverse form with a strong Wolfe line search, the $O(n^2)$ update as a separate function, and an option to pass a step rule, such as the exact step on a quadratic, in place of the line search. It returns the iterates and, for each step, the step length, the direction, the gradient and the matrix $H$. SciPy's `minimize(method="BFGS")` and the `optim` function of R with `method = "BFGS"` are widely used implementations.

## History

Davidon proposed the first quasi-Newton method in a 1959 report, and Fletcher and Powell published it in 1963 in the form now called DFP. In 1970 Broyden, Fletcher, Goldfarb and Shanno each derived the BFGS update in separate papers and by different arguments; Goldfarb's derivation was variational, a least-change argument. Powell proved global convergence on convex functions with inexact line searches in 1976, Dennis and Moré gave the characterization of superlinear convergence in 1974, and Byrd, Nocedal and Yuan extended the convex theory to the Broyden class in 1987. Dai in 2002 and Mascarenhas in 2004 showed that convergence can fail on nonconvex functions.

## References
