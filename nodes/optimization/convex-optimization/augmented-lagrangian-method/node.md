---
tag: 27GRBM
kind: algorithm
slug: augmented-lagrangian-method
name: Augmented Lagrangian method
aliases:
- method of multipliers
- ALM
- Powell-Hestenes-Rockafellar method
area: optimization/convex-optimization
level: advanced
summary: Dual ascent with a quadratic penalty added to the Lagrangian for better convergence.
solves: [quadratic-programming]
model: real-ram
complexity:
  vars: {k: the number of iterations, m: the number of equality constraints, n: the number of variables, s: the cost of one minimization of the augmented Lagrangian}
  time: {worst: O(k (s + m n))}
  space: {extra: O(m + n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1969
  people: [Magnus Hestenes, Michael J. D. Powell, R. Tyrrell Rockafellar, Dimitri Bertsekas]
  note: Hestenes and Powell proposed the method independently in 1969. Rockafellar extended it to inequality constraints in 1973 and showed in 1976 that it is the proximal point method on the dual. Bertsekas wrote the standard book on it in 1982.
prereqs: [penalty-method, dual-ascent, lagrangian-function]
see_also: [admm, proximal-point-method, dual-decomposition, lagrangian-duality, kkt-conditions, barrier-method, quadratic-programming, basis-pursuit]
sources:
  - paper: doi:10.1007/BF00927673
    title: Magnus R. Hestenes, Multiplier and gradient methods, Journal of Optimization Theory and Applications 4(5), 1969
    locator: pages 303 to 320
  - paper: doi:10.1287/moor.1.2.97
    title: R. Tyrrell Rockafellar, Augmented Lagrangians and applications of the proximal point algorithm in convex programming, Mathematics of Operations Research 1(2), 1976
    locator: pages 97 to 116 (the method of multipliers as the proximal point algorithm on the dual, and its convergence)
  - paper: doi:10.1007/BF00934777
    title: R. Tyrrell Rockafellar, The multiplier method of Hestenes and Powell applied to convex programming, Journal of Optimization Theory and Applications 12(6), 1973
    locator: pages 555 to 562 (inequality constraints and the update y <- max(0, y + rho g(x)))
  - book: isbn:9781886529045
    title: Dimitri P. Bertsekas, Constrained Optimization and Lagrange Multiplier Methods, Athena Scientific, 1996 (first published 1982)
    locator: Chapter 2 (the method of multipliers for equality constrained problems, its convergence and rate), Chapter 3 (inequality constraints)
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Section 17.3 (the augmented Lagrangian method, equality constraints, exactness for a finite rho), Section 17.4 (practical augmented Lagrangian methods, bound constraints, LANCELOT)
  - paper: doi:10.1561/2200000016
    title: Stephen Boyd, Neal Parikh, Eric Chu, Borja Peleato and Jonathan Eckstein, Distributed optimization and statistical learning via the alternating direction method of multipliers, Foundations and Trends in Machine Learning 3(1), 2011
    locator: Section 2.3 (the method of multipliers, and why the step rho in the dual update makes each iterate dual feasible)
  - paper: doi:10.1137/0728030
    title: Andrew R. Conn, Nicholas I. M. Gould and Philippe L. Toint, A globally convergent augmented Lagrangian algorithm for optimization with general constraints and simple bounds, SIAM Journal on Numerical Analysis 28(2), 1991
    locator: pages 545 to 572
---

The augmented Lagrangian method, also called the method of multipliers, solves $\min f(x)$ subject to $Ax = b$ by alternating two steps. It minimizes the augmented Lagrangian $f(x) + y^\top(Ax - b) + \tfrac{\rho}{2}\|Ax - b\|^2$ over $x$, and then it updates the multiplier estimate by $y \leftarrow y + \rho(Ax - b)$. It combines the [penalty method](/penalty-method/) with [dual ascent](/dual-ascent/). Unlike the penalty method, it reaches feasibility with a fixed $\rho$, so the subproblems stay well conditioned. Unlike dual ascent, it needs no strict convexity and no step-size rule. Rockafellar showed that the multiplier sequence is exactly the [proximal point method](/proximal-point-method/) on the dual problem, which gives the bound $d^* - d(y_k) \le \|y_0 - y^*\|^2/(2\rho k)$ for each convex $f$.

## In plain words

The penalty method charges a fine for breaking a rule, and it must make the fine very large to make the answer obey the rule. The augmented Lagrangian method adds a second charge: a price for each rule, which it learns as it goes.

It keeps a moderate fine. After each search it looks at how much each rule is broken, and it raises or lowers that rule's price in proportion. When the prices are right, the cheapest point obeys every rule, even though the fine stays moderate. The learned prices are also useful on their own: they say how much the best value would change if a rule were relaxed a little. At each step the method also knows an exact lower bound on the best value, so it can tell how close it is.

## The problem

Minimize a closed, proper, convex $f: \mathbb{R}^n \to \mathbb{R} \cup \{+\infty\}$ subject to $Ax = b$, with $A \in \mathbb{R}^{m \times n}$. The [Lagrangian](/lagrangian-function/) is $L(x, y) = f(x) + y^\top(Ax - b)$, and the dual function is $d(y) = \inf_x L(x, y)$. We assume that a primal solution $x^*$ and a dual solution $y^*$ exist with $f(x^*) = d(y^*)$, and that each subproblem of line L2 has a minimizer. The input is $f$ (through a solver for line L2), $A$, $b$, a start $y_0$, the penalty $\rho > 0$ and a tolerance $\varepsilon$. The output is $x$ and $y$ with $\|Ax - b\| \le \varepsilon$.

## The algorithm

```pseudo id=main
METHOD-OF-MULTIPLIERS(f, A, b, y, ρ, ε)
L1  repeat
L2      x ← argmin_x  f(x) + yᵀ(Ax − b) + (ρ/2)‖Ax − b‖²
L3      r ← Ax − b
L4      y ← y + ρ r                       ▷ now x also minimizes f(x) + yᵀ(Ax − b)
L5  until ‖r‖ ≤ ε
L6  return x, y
```

The step size of line L4 is exactly $\rho$, the penalty weight of line L2. This choice makes the optimality condition of line L2, $0 \in \partial f(x) + A^\top(y + \rho r)$, the optimality condition of the plain Lagrangian at the new $y$. So after line L4 the method knows the dual value $d(y) = f(x) + y^\top r$ exactly, and the duality gap is $f(x) - d(y) = -y^\top r$.

For a convex quadratic $f(x) = \tfrac12 x^\top Qx + c^\top x$, line L2 is the linear system $(Q + \rho A^\top A)x = -c - A^\top y + \rho A^\top b$. The matrix does not change, so one Cholesky factorization serves all steps. It is positive definite when $Q$ is positive definite on the null space of $A$, even if $Q$ itself is singular.

## Example

Minimize $\tfrac12 x^2$ subject to $x = 1$, with $\rho = 1$ and $y_0 = 0$. The answer is $x^* = 1$, $y^* = -1$, $f^* = \tfrac12$. Line L2 solves $x + y + (x - 1) = 0$, so $x = (1 - y)/2$, and line L4 gives $y^+ + 1 = (y + 1)/2$. In exact arithmetic,

| $k$ | $x_k$ | $r_k$ | $y_k$ | $f(x_k)$ | $d(y_k) = f(x_k) + y_k r_k$ |
|---|---|---|---|---|---|
| 1 | 1/2 | -1/2 | -1/2 | 1/8 | 3/8 |
| 2 | 3/4 | -1/4 | -3/4 | 9/32 | 15/32 |
| 3 | 7/8 | -1/8 | -7/8 | 49/128 | 63/128 |
| $k$ | $1 - 2^{-k}$ | $-2^{-k}$ | $-1 + 2^{-k}$ | $\tfrac12(1 - 2^{-k})^2$ | $\tfrac12(1 - 4^{-k})$ |

The violation halves at each step with $\rho = 1$ fixed. The [penalty method](/penalty-method/) needs $\rho \approx 2^k$ for the same violation. The dual values $d(y_k)$ rise to $f^* = \tfrac12$ from below and certify the primal values. The proved bound $d^* - d(y_k) \le 1/(2k)$ holds with a large margin, because this problem is strongly convex and the true rate is linear.

## Correctness

Two facts carry the proof. First, after line L4 the point $x$ minimizes the plain Lagrangian at the new $y$, so $-r$ is a subgradient of $-d$ at $y$. Second, the update $y^+ = y + \rho r$ then reads $0 \in \partial(-d)(y^+) + (y^+ - y)/\rho$, which is the definition of $y^+ = \operatorname{prox}_{\rho(-d)}(y)$. So the multipliers follow the [proximal point method](/proximal-point-method/) on $-d$, and its theory gives the dual rate and the decrease of $\|y_k - y^*\|$. The residual is $r_k = (y_k - y_{k-1})/\rho$, and the steps of a proximal point method do not grow and have squared lengths with a finite sum, which gives the residual rate. The full proof is below.

## Complexity

**Iterations.** Under the assumptions of the problem statement, for each $k \ge 1$:

$$d^* - d(y_k) \le \frac{\|y_0 - y^*\|^2}{2\rho k}, \qquad \|Ax_k - b\| \le \frac{\|y_0 - y^*\|}{\rho\sqrt{k}},$$

$$-\|y^*\|\,\|Ax_k - b\| \le f(x_k) - f^* \le -y_k^\top(Ax_k - b).$$

The bounds hold for each $\rho > 0$ and improve as $\rho$ grows, at the price of harder subproblems. The rate is sublinear in general. If $f$ is a strongly convex quadratic, the dual is a strongly concave quadratic, and $y_k$ converges linearly: the error is multiplied by at most $1/(1 + \rho\sigma_{\min})$ at each step, where $\sigma_{\min}$ is the smallest eigenvalue of $AQ^{-1}A^\top$. In the example $\sigma_{\min} = 1$, which gives the factor $\tfrac12$. For smooth nonconvex problems with second-order sufficient conditions, the rate is linear with a factor that goes to $0$ as $\rho \to \infty$ (Bertsekas, 1982).

**One iteration.** One minimization of $L_\rho(\cdot, y)$, plus $O(mn)$ for the residual and the update. For a quadratic $f$, one solve with a factored matrix, $O(n^2)$ per step after an $O(n^3)$ factorization. The extra space is $O(m + n)$ plus the factorization.

## Properties

- **Exact with a finite $\rho$.** Feasibility comes from the multipliers, not from $\rho \to \infty$, so the condition number of the subproblems stays bounded.
- **Dual feasible after each step.** After line L4, $x$ minimizes the Lagrangian at $y$, so $d(y)$ is known and the gap $-y^\top r$ is a stopping test.
- **Monotone in the dual.** $d(y_k)$ increases, $\|y_k - y^*\|$ does not increase, and $\|r_k\|$ does not increase.
- **No strict convexity needed.** The term $\tfrac{\rho}{2}\|Ax - b\|^2$ makes the subproblem solvable in many cases where the plain Lagrangian has no minimizer, for example for linear objectives.
- **Not separable.** The term $\|Ax - b\|^2$ couples the blocks of $x$, so the method does not split like [dual decomposition](/dual-decomposition/). [ADMM](/admm/) restores the splitting.

## Variants and improvements

- **Inequality constraints.** For $g(x) \le 0$, use the update $y \leftarrow \max(0, y + \rho\,g(x))$ and the augmented term $\tfrac{1}{2\rho}\big(\|\max(0, y + \rho g(x))\|^2 - \|y\|^2\big)$ (Rockafellar, 1973). This is the Powell-Hestenes-Rockafellar form.
- **Increasing $\rho$.** Practical codes such as LANCELOT increase $\rho$ when the violation does not fall fast enough, and solve the subproblems only approximately, with a tolerance that shrinks.
- **Bound constraints in the subproblem.** Keep simple bounds $l \le x \le u$ in line L2 and put only the general constraints in the augmented Lagrangian (Conn, Gould and Toint, 1991).
- **[ADMM](/admm/).** For $f(x) + g(z)$ subject to $Ax + Bz = c$, replace the joint minimization of line L2 by one pass of minimization over $x$ and then over $z$.
- **Inexact and linearized versions.** Replace line L2 by one proximal gradient step on $L_\rho$. This gives the linearized augmented Lagrangian and primal-dual methods such as that of Chambolle and Pock.

## When to use it

Use the augmented Lagrangian method for equality-constrained problems when each subproblem is easy, for example when $f$ is quadratic or has a cheap [proximal map](/proximal-operator/) after adding $\|Ax - b\|^2$, and when you need accurate feasibility. It is the method behind [basis pursuit](/basis-pursuit/) solvers, nonlinear programming codes such as LANCELOT, and many PDE-constrained solvers. If the variables split into blocks that should be handled separately, use [ADMM](/admm/) or [dual decomposition](/dual-decomposition/). If the problem is small and very high accuracy is needed, an [interior-point method](/interior-point-method/) is often faster.

## Pitfalls

- **A dual step other than $\rho$.** With a step $\alpha \ne \rho$ in line L4, the new $x$ no longer minimizes the Lagrangian at the new $y$, the dual value is no longer known, and for $\alpha > 2\rho$ the method can diverge.
- **Stopping on the residual alone.** A small $\|r\|$ with a large $\|y\|$ can still hide a large gap. Also check $|y^\top r|$, or the change of $x$.
- **Too small $\rho$.** The rates scale like $1/\rho$, so a tiny $\rho$ is slow. Too large a $\rho$ makes line L2 ill-conditioned, as in the penalty method. Values that make $\rho\|A\|^2$ comparable to the curvature of $f$ are a common start.
- **Inexact subproblems.** If line L2 is solved only roughly, the multiplier update can go in the wrong direction. Tighten the inner tolerance as the outer iterations go on.
- **Nonconvex $f$.** Then $d$ is not the right model, the dual bound fails, and the method converges only locally, to a point that satisfies the [KKT conditions](/kkt-conditions/), and only when $\rho$ is large enough.

## Implementations

## History

Hestenes (1969) and Powell (1969) proposed the method independently, Hestenes as the "method of multipliers" and Powell with a shifted penalty $\tfrac{\rho}{2}\|h(x) + \theta\|^2$, which is the same method with $y = \rho\theta$. Rockafellar extended it to inequality constraints in 1973, and in 1976 he showed that it is the proximal point algorithm applied to the dual, which gave a convergence theory for every convex problem. Bertsekas collected the theory in his 1982 book. In the 1990s Conn, Gould and Toint built the LANCELOT code on it. Since about 2010, the method and its splitting form [ADMM](/admm/) have been widely used for large problems in signal processing and machine learning.

## References
