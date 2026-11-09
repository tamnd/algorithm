---
tag: AJV6AP
kind: algorithm
slug: limited-memory-bfgs
name: Limited-memory BFGS
aliases:
- L-BFGS
- LBFGS
- limited-memory quasi-Newton method
area: optimization/gradient-methods
level: advanced
summary: BFGS that keeps only the last m pairs (s, y) and applies the inverse Hessian approximation to the gradient by a two-loop recursion in O(mn) time and O(mn) memory, for problems with many variables.
solves: [unconstrained-smooth-minimization]
model: real-ram
complexity:
  vars: {n: the number of variables, k: the number of iterations, m: the number of stored pairs, t: the largest number of trial steps in one line search}
  time: {worst: O(k (m n + t n))}
  space: {extra: O(m n)}
  gradients: {quadratic_exact_steps: O(n), step: O(t)}
properties: {deterministic: true, iterative: true, descent_method: true, first_order: true, finite_termination_on_quadratics: true}
history:
  year: 1980
  people: [Jorge Nocedal, Dong C. Liu]
  note: Nocedal gave the limited-storage BFGS update and the two-loop recursion in 1980. Liu and Nocedal analyzed the method and compared it with other large-scale methods in 1989.
prereqs: [bfgs, quasi-newton-method, wolfe-conditions]
see_also: [bfgs, quasi-newton-method, nonlinear-conjugate-gradient, wolfe-conditions, gradient-descent, conjugate-gradient-method, logistic-regression, unconstrained-smooth-minimization]
sources:
  - paper: doi:10.1090/S0025-5718-1980-0572855-7
    title: Jorge Nocedal, Updating quasi-Newton matrices with limited storage, Mathematics of Computation 35(151), 1980
    locator: pages 773 to 782
  - paper: doi:10.1007/BF01589116
    title: Dong C. Liu and Jorge Nocedal, On the limited memory BFGS method for large scale optimization, Mathematical Programming 45, 1989
    locator: pages 503 to 528 (the scaling of the initial matrix, numerical comparisons, and R-linear convergence on uniformly convex functions)
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Section 7.2, Limited-memory quasi-Newton methods (the two-loop recursion and the L-BFGS algorithm)
  - paper: doi:10.1137/0916069
    title: Richard H. Byrd, Peihuang Lu, Jorge Nocedal and Ciyou Zhu, A limited memory algorithm for bound constrained optimization, SIAM Journal on Scientific Computing 16(5), 1995
    locator: pages 1190 to 1208
  - paper: doi:10.1145/279232.279236
    title: Ciyou Zhu, Richard H. Byrd, Peihuang Lu and Jorge Nocedal, Algorithm 778, L-BFGS-B, Fortran subroutines for large-scale bound-constrained optimization, ACM Transactions on Mathematical Software 23(4), 1997
    locator: pages 550 to 560
---

Limited-memory BFGS (L-BFGS) is the form of [BFGS](/bfgs/) for problems with many variables. Dense BFGS stores an $n \times n$ matrix $H_k$. L-BFGS stores only the last $m$ pairs $s_i = x_{i+1} - x_i$, $y_i = \nabla f(x_{i+1}) - \nabla f(x_i)$, typically with $m$ between $3$ and $20$. At each step it defines $H_k$ as the result of $m$ BFGS updates applied to the scaled identity $\gamma_kI$, $\gamma_k = s_{k-1}^\top y_{k-1}/y_{k-1}^\top y_{k-1}$, and computes $H_k\nabla f(x_k)$ by the *two-loop recursion* in $O(mn)$ time without forming the matrix. With a [Wolfe](/wolfe-conditions/) line search, $H_k$ is positive definite, so every direction goes downhill. On a strictly convex quadratic with exact line searches, L-BFGS with any $m \ge 1$ produces the iterates of the linear [conjugate gradient method](/conjugate-gradient-method/). On uniformly convex functions it converges R-linearly (Liu and Nocedal).

## In plain words

BFGS learns the curvature of the function from the steps it has taken, but it keeps everything it learned in a large square table. With a million variables, the table has a million times a million numbers, which does not fit in memory.

L-BFGS keeps only the last few steps and the change of slope over each of them. When it needs a new direction, it replays these few updates on a simple starting guess of the curvature. The replay works directly on the slope vector, in two passes over the stored steps, so the large table never exists. The old information is forgotten, but the recent steps usually hold most of what is useful near the current point.

## The problem

The input is a continuously differentiable function $f : \mathbb{R}^n \to \mathbb{R}$, given by routines for $f$ and $\nabla f$, a start $x_0$, the memory $m \ge 1$, an iteration limit $K$ and a gradient tolerance $\varepsilon$. The output is a point $x_k$ with $\|\nabla f(x_k)\| \le \varepsilon$, or the last point reached. This is [unconstrained smooth minimization](/unconstrained-smooth-minimization/) with $n$ large, from thousands to millions of variables. All arithmetic is in floating point.

## The algorithm

```pseudo id=main
L-BFGS(f, ∇f, x₀, m, K, ε)
L1  x ← x₀; g ← ∇f(x); P ← empty list of pairs
L2  for k = 0, 1, …, K − 1 while ‖g‖ > ε do
L3      d ← −TWO-LOOP(g, P)
L4      α ← a step along d that satisfies the strong Wolfe conditions, trying α = 1 first
L5      s ← α d; x ← x + s; g⁺ ← ∇f(x); y ← g⁺ − g
L6      if yᵀs > 0 then append (s, y) to P; if P has more than m pairs, remove the oldest
L7      g ← g⁺
L8  return x

TWO-LOOP(q, P = (s₁, y₁), …, (s_ℓ, y_ℓ), oldest first)
L9   for i = ℓ, ℓ − 1, …, 1 do ρᵢ ← 1/(yᵢᵀsᵢ); aᵢ ← ρᵢ sᵢᵀq; q ← q − aᵢ yᵢ
L10  r ← γ q, with γ = s_ℓᵀy_ℓ / y_ℓᵀy_ℓ, or γ = 1 if ℓ = 0
L11  for i = 1, 2, …, ℓ do b ← ρᵢ yᵢᵀr; r ← r + (aᵢ − b) sᵢ
L12  return r
```

Lines L1 to L8 are the outer loop of [BFGS](/bfgs/) with the matrix replaced by the list $P$. Line L4 is a strong Wolfe line search by bracketing and zoom (Nocedal and Wright, Algorithms 3.5 and 3.6), with $c_1 = 10^{-4}$, $c_2 = 0.9$ and a limit of $100$ trial points; if the limit is reached, the method stops. Line L6 stores a pair only when $y^\top s > 0$, which every Wolfe step gives; this keeps $H_k$ positive definite. The two-loop recursion of lines L9 to L12 returns $H q$, where $H$ is obtained from $\gamma I$ by the BFGS updates with the stored pairs, oldest first. The first loop goes from the newest pair to the oldest and the second loop goes back. Each pass over a pair costs two inner products and one vector update, so one call costs $4\ell n$ multiplications plus $n$ for the scaling.

## Example

**The two-loop recursion.** Take $n = 2$, the pairs $(s_1, y_1) = ((1, 0), (2, 1))$ and $(s_2, y_2) = ((0, 1), (1, 4))$, and $q = (1, 1)$. Then $\rho_1 = \frac12$ and $\rho_2 = \frac14$.

| line | step | result |
|---|---|---|
| L9, $i = 2$ | $a_2 = \frac14s_2^\top q = \frac14$ | $q = (1, 1) - \frac14(1, 4) = (\frac34, 0)$ |
| L9, $i = 1$ | $a_1 = \frac12s_1^\top q = \frac38$ | $q = (\frac34, 0) - \frac38(2, 1) = (0, -\frac38)$ |
| L10 | $\gamma = \frac{4}{17}$ | $r = (0, -\frac{3}{34})$ |
| L11, $i = 1$ | $b = \frac12y_1^\top r = -\frac{3}{68}$ | $r = r + (\frac38 + \frac{3}{68})s_1 = (\frac{57}{136}, -\frac{3}{34})$ |
| L11, $i = 2$ | $b = \frac14y_2^\top r = \frac{9}{544}$ | $r = r + (\frac14 - \frac{9}{544})s_2 = (\frac{57}{136}, \frac{79}{544})$ |

The dense BFGS recursion from $\frac{4}{17}I$ with the same two pairs gives $H = \begin{pmatrix} 19/34 & -19/136 \\ -19/136 & 155/544 \end{pmatrix}$, and $Hq = (\frac{57}{136}, \frac{79}{544})$, the same vector. The secant equation holds for the newest pair: the recursion maps $y_2 = (1, 4)$ to $s_2 = (0, 1)$. For the older pair it does not: $y_1 = (2, 1)$ maps to about $(0.978, 0.006)$, not to $s_1 = (1, 0)$, because the later update changes $H$ along $y_1$.

**Runs.** On the Rosenbrock function from $(-1.2, 1)$ with tolerance $\|\nabla f\| \le 10^{-6}$, the implementation needs:

| memory $m$ | steps | values of $f$ in line searches |
|---|---|---|
| 1 | 45 | 106 |
| 3 | 40 | 75 |
| 5 | 39 | 68 |
| 10 | 37 | 64 |

Dense BFGS needs $36$ steps and $61$ values on the same problem. On the extended Rosenbrock function in $n = 100$ variables (50 independent copies of the two-variable function), from a fixed random start near $(-1.2, 1, -1.2, 1, \dots)$, the implementation needs $139$ steps with $m = 1$, $239$ with $m = 5$ and $145$ with $m = 20$. So on this problem more memory does not always mean fewer steps. These counts describe these runs only.

## Correctness

The proofs are in the correctness proof of this page.

1. **The two-loop recursion is exact.** TWO-LOOP$(q, P)$ returns $Hq$, where $H_0 = \gamma I$ and $H_i = V_i^\top H_{i-1}V_i + \rho_is_is_i^\top$ with $V_i = I - \rho_iy_is_i^\top$, for $i = 1, \dots, \ell$, and $H = H_\ell$.
2. **Positive definiteness, secant equation and descent.** If every stored pair has $y_i^\top s_i > 0$, then $\gamma > 0$, $H$ is symmetric positive definite, $Hy_\ell = s_\ell$, and $d_k = -H\nabla f(x_k)$ is a descent direction. With Wolfe steps every pair is stored, $f$ decreases at every step, and the method stops after at most $K$ iterations.
3. **Quadratics with exact steps.** For $f(x) = \frac12x^\top Ax - b^\top x$ with $A$ symmetric positive definite and exact line searches, every $d_k$ is a positive multiple of the linear conjugate gradient direction, for every $m \ge 1$. So the iterates are those of linear conjugate gradient, and $\nabla f(x_k) = 0$ for some $k \le n$ in exact arithmetic.

The convergence theorem is proved by Liu and Nocedal; this page states it with its assumptions. Let $f$ be twice continuously differentiable, let the level set $\Omega = \{x : f(x) \le f(x_0)\}$ be convex, and let there be constants $0 < \mu \le M$ with $\mu\|z\|^2 \le z^\top\nabla^2f(x)z \le M\|z\|^2$ for all $x \in \Omega$ and all $z$. Let the steps satisfy the Wolfe conditions and let the starting matrices of the recursion, here $\gamma_kI$, have norms and inverse norms bounded by a constant. Then $x_k$ converges to the unique minimizer $x^*$, and there is $r \in [0, 1)$ with $f(x_k) - f(x^*) \le r^k(f(x_0) - f(x^*))$. With $\gamma_k = s^\top y/y^\top y$ the bound holds, because $y = \bar{A}s$ for the average Hessian $\bar{A}$ along the step, so $1/M \le \gamma_k \le 1/\mu$. There is no superlinear rate in general, since the matrices keep only $m$ directions of curvature.

## Complexity

A call of TWO-LOOP with $\ell \le m$ pairs costs $4\ell n + n$ multiplications. One iteration adds $O(n)$ for the pair update and a line search with $t$ trial points, each costing $O(n)$ plus one value of $f$ and $\nabla f$. So $k$ iterations cost $O(k(mn + tn))$ arithmetic, against $O(k(n^2 + tn))$ for dense BFGS. The memory is $2m$ vectors of length $n$, $O(mn)$. Near the solution the unit step usually passes the first trial, so $t = 1$ there.

| claim | value |
|---|---|
| time of TWO-LOOP | $4mn + n$ multiplications |
| time per iteration | $O(mn + tn)$ plus $t$ values of $f$ and $\nabla f$ |
| extra space | $O(mn)$ |
| iterations on a quadratic with exact steps | at most $n$ |

## Properties

- **Linear memory.** $O(mn)$ numbers, so it scales to millions of variables.
- **Descent method.** $H_k$ is positive definite under Wolfe steps, so every direction goes downhill and $f$ decreases.
- **Self-scaling.** The factor $\gamma_k$ sets the length of the step to the curvature along the last step, so $\alpha = 1$ is usually accepted.
- **No matrix ever formed.** The method needs only inner products and vector updates, which suit parallel and distributed computation.
- **Only the newest pair is interpolated.** $H_ky_{k-1} = s_{k-1}$ holds, but older pairs need not satisfy their secant equations, except in special cases such as quadratics with exact steps.

## Variants and improvements

- **L-BFGS-B.** Bounds $l \le x \le u$, handled by a projected gradient search for the Cauchy point and a subspace minimization (Byrd, Lu, Nocedal and Zhu; Zhu, Byrd, Lu and Nocedal).
- **Compact representation.** Write $H_k = \gamma I + WMW^\top$ with $W$ of size $n \times 2m$ and $M$ of size $2m \times 2m$. This form suits trust-region methods and constraints.
- **OWL-QN.** A variant for objectives with an $\ell_1$ term, used for sparse logistic regression.
- **Stochastic L-BFGS.** Pairs built from mini-batch gradients, for [stochastic gradient descent](/stochastic-gradient-descent/) settings. The noise in $y$ needs extra care, such as larger batches for the pairs.
- **Other memories.** Limited-memory forms of other quasi-Newton updates exist, but BFGS is the standard.

## When to use it

Use L-BFGS for smooth problems with many variables when only gradients are available: maximum likelihood estimation such as [logistic regression](/logistic-regression/), conditional random fields, variational problems from physics and engineering, and image reconstruction. It is often the first method to try for a smooth deterministic problem with $n$ above a few thousand. For small $n$, dense [BFGS](/bfgs/) can take fewer steps. With noisy mini-batch gradients, first-order methods such as [Adam](/adam/) are more common. For nonsmooth terms, use [proximal methods](/proximal-gradient-method/) or OWL-QN.

## Pitfalls

- **Armijo backtracking only.** Without the curvature condition, $y^\top s$ can be negative. The implementation then skips the pair, and too many skipped pairs reduce the method to scaled gradient descent. Use a Wolfe search.
- **Too much memory.** Beyond about $20$ pairs the cost per step grows with little gain, and old pairs from far away can hurt more than help.
- **No scaling.** With $\gamma = 1$ in place of $s^\top y/y^\top y$, the first trial step is often far from acceptable, and the line search costs more.
- **Changing the function.** If $f$ changes between iterations, as with mini-batch sampling, the pairs mix information from different functions, and $y^\top s$ can be negative or misleading.
- **Reading the matrix.** The approximate inverse Hessian is not stored. If it is needed, for example for error estimates, form $Hq$ by the recursion for the needed vectors $q$, and remember that it is a rough approximation.

## Implementations

The Python module has the two-loop recursion as a separate function, the method with a strong Wolfe line search, and an option to pass a step rule, such as the exact step on a quadratic, in place of the line search. It returns the iterates and, for each step, the step length, the direction, the gradient and the stored pairs. SciPy's `minimize(method="L-BFGS-B")` wraps the Fortran code L-BFGS-B, and `torch.optim.LBFGS` in PyTorch is a widely used implementation.

## History

Nocedal published the limited-storage BFGS update in 1980, with the recursion that applies the update to a vector without forming the matrix. Liu and Nocedal studied the method in 1989: they tested several choices of the starting matrix, among them the scaling $\gamma_k = s^\top y/y^\top y$, compared the method with other methods for large problems, and proved R-linear convergence on uniformly convex functions. Byrd, Lu, Nocedal and Zhu extended it to bound constraints in 1995, and the Fortran code L-BFGS-B, published in 1997, became one of the most used optimization codes.

## References
