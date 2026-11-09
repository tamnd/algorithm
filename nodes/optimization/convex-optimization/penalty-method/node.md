---
tag: 759QSG
kind: technique
slug: penalty-method
name: Penalty method
aliases:
- quadratic penalty method
- exterior penalty method
- exact penalty method
area: optimization/convex-optimization
level: core
summary: Replace constraints with a penalty term added to the objective.
prereqs: [constrained-optimization, gradient-descent]
see_also: [augmented-lagrangian-method, barrier-method, lagrange-multiplier, kkt-conditions, big-m-method, hinge-loss, basis-pursuit, lagrangian-relaxation]
sources:
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 17 (Section 17.1 the quadratic penalty method, its convergence theorems and the ill-conditioning of the Hessian, Section 17.2 nonsmooth and exact penalty functions, Section 17.3 the augmented Lagrangian method)
  - paper: doi:10.1090/S0002-9904-1943-07818-4
    title: Richard Courant, Variational methods for the solution of problems of equilibrium and vibrations, Bulletin of the American Mathematical Society 49(1), 1943
    locator: pages 1 to 23 (the quadratic penalty for a constraint, in the appendix on boundary conditions)
  - book: isbn:9780898712544
    title: Anthony V. Fiacco and Garth P. McCormick, Nonlinear Programming, Sequential Unconstrained Minimization Techniques, SIAM Classics edition, 1990
    locator: Chapter 4 (exterior point unconstrained minimization techniques)
  - paper: doi:10.1287/mnsc.13.5.344
    title: Willard I. Zangwill, Non-linear programming via penalty functions, Management Science 13(5), 1967
    locator: pages 344 to 358 (the exact absolute-value penalty)
  - paper: doi:10.1007/BF01588250
    title: S.-P. Han and O. L. Mangasarian, Exact penalty functions in nonlinear programming, Mathematical Programming 17, 1979
    locator: pages 251 to 269
---

The penalty method solves a constrained problem by a sequence of unconstrained ones. It drops the constraints and adds to the objective a term that is $0$ on the feasible set and positive outside it, multiplied by a weight $\rho$. For the quadratic penalty, each minimizer violates the constraints by $O(1/\rho)$, so the method raises $\rho$ and minimizes again from the last point. As $\rho \to \infty$, the minimizers go to a solution, and the products $\rho\,h(x)$ go to the [Lagrange multipliers](/lagrange-multiplier/). The price is ill-conditioning: the curvature of the penalty grows with $\rho$. The [augmented Lagrangian method](/augmented-lagrangian-method/) and exact penalties are the standard ways to avoid it.

## In plain words

Some problems say "you must stay in this region." The penalty method changes the rule to "you may leave the region, but you pay a fine that grows with the distance." Now there is no rule, only a cost, and any method for problems without rules can find the cheapest point.

With a small fine, the cheapest point is a little outside the region. So the method makes the fine larger and searches again, starting from the last answer. The answers come closer and closer to the region and to the true best point. The size of the fine that the answer still pays tells how much the rule is worth. If the fine gets very large, the cost function becomes very steep, and the search becomes slow and inaccurate.

## When it applies

- The problem is $\min f(x)$ subject to $h(x) = 0$ and $g(x) \le 0$, and you have a good solver for problems without constraints, or with only simple constraints.
- The constraints are hard to project on, so [projected gradient descent](/projected-gradient-descent/) does not apply.
- A small violation of the constraints is acceptable, or you will finish with a few steps of a more exact method.
- For an exact penalty (see Variations), you also have a bound on the size of the Lagrange multipliers.

## The template

```pseudo id=main
PENALTY-METHOD(f, h, g, x, ρ, κ, ε)          ▷ κ > 1: the growth factor of ρ
L1  loop
L2      x ← argmin_x  f(x) + ρ · P(x)          ▷ hole: the inner solver, started at the last x
L3      if ‖h(x)‖ + ‖max(g(x), 0)‖ ≤ ε then return x
L4      ρ ← κ · ρ                              ▷ hole: the schedule of ρ
```

**The holes.** The penalty is $P(x) = \tfrac12\|h(x)\|^2 + \tfrac12\|\max(g(x), 0)\|^2$ for the quadratic penalty. It is $0$ exactly on the feasible set, it is differentiable when $h$ and $g$ are, and it is convex when $h$ is affine and each $g_i$ is convex. Line L2 is any unconstrained method: [gradient descent](/gradient-descent/), [Newton's method](/newton-method-for-systems/) or [conjugate gradients](/conjugate-gradient-method/). Line L4 is usually $\kappa = 10$. The estimate $y = \rho\,h(x)$ of the multipliers comes for free at line L2.

**The analysis.** Let $f^*$ be the optimal value and $Q_\rho(x) = f(x) + \rho P(x)$.

1. *Lower bound.* For each $\rho$, $\min Q_\rho \le f^*$, because $Q_\rho = f$ on the feasible set. The value $\min Q_\rho$ is nondecreasing in $\rho$.
2. *Limit points are optimal.* Let $x_k$ be a global minimizer of $Q_{\rho_k}$, with $\rho_k \to \infty$, let $f$ be bounded below by $f_{\mathrm{low}}$, and let $x^*$ be optimal. Then $f(x_k) + \rho_k P(x_k) \le f(x^*) = f^*$, so $P(x_k) \le (f^* - f_{\mathrm{low}})/\rho_k \to 0$, and $f(x_k) \le f^*$. If $\bar{x}$ is a limit point of $(x_k)$ and $f$, $h$, $g$ are continuous, then $P(\bar{x}) = 0$, so $\bar{x}$ is feasible, and $f(\bar{x}) \le f^*$, so $\bar{x}$ is optimal.
3. *The violation is $O(1/\rho)$ with a certificate.* Take a convex $f$, linear constraints $Ax = b$, and a multiplier $y^*$, so that $f(x) + y^{*\top}(Ax - b) \ge f^*$ for all $x$. Let $r = Ax_\rho - b$. From fact 1, $f(x_\rho) + \tfrac{\rho}{2}\|r\|^2 \le f^*$. With the multiplier inequality this gives $-y^{*\top} r + \tfrac{\rho}{2}\|r\|^2 \le 0$, so $\|r\| \le 2\|y^*\|/\rho$. Also, the optimality condition $\nabla f(x_\rho) + \rho A^\top r = 0$ says that $x_\rho$ minimizes the [Lagrangian](/lagrangian-function/) $f(x) + y^\top(Ax - b)$ for $y = \rho r$. So by [weak duality](/lagrangian-duality/)

$$f(x_\rho) + \rho\|r\|^2 \le f^* \quad\text{and}\quad f(x_\rho) \le f^*,$$

a lower bound that the method can compute, so the gap to $f^*$ is known up to the violation.

### A worked example

Minimize $\tfrac12 x^2$ subject to $x = 1$. The solution is $x^* = 1$ with $f^* = \tfrac12$, and the multiplier is $y^* = -1$ (from $x + y = 0$). The penalized function is $\tfrac12 x^2 + \tfrac{\rho}{2}(x - 1)^2$, and its minimizer solves $x + \rho(x - 1) = 0$:

| $\rho$ | $x_\rho = \rho/(1 + \rho)$ | violation $1/(1 + \rho)$ | $y = \rho(x_\rho - 1)$ | lower bound $f(x_\rho) + \rho r^2$ |
|---|---|---|---|---|
| 1 | 0.5 | 0.5 | -0.5 | 0.375 |
| 10 | 0.909091 | 0.0909091 | -0.909091 | 0.495868 |
| 100 | 0.990099 | 0.00990099 | -0.990099 | 0.499951 |
| 1000 | 0.999001 | 0.000999001 | -0.999001 | 0.4999995 |

The lower bound is exactly $\tfrac12(1 - 1/(1 + \rho)^2)$. The violation is about $|y^*|/\rho$, half of the proved bound. The second derivative of the penalized function is $1 + \rho$, so its condition grows with $\rho$; in $n$ variables, the Hessian $\nabla^2 f + \rho A^\top A$ has $m$ eigenvalues of size about $\rho$ and the others of size about the curvature of $f$, and gradient methods slow down by the same factor.

## Classic examples

- **The [augmented Lagrangian method](/augmented-lagrangian-method/).** Add the term $y^\top h(x)$ with the estimate $y$, and update $y \leftarrow y + \rho\,h(x)$. The violation then goes to $0$ with a fixed $\rho$, so the ill-conditioning goes away.
- **Soft-margin [support vector machines](/support-vector-machine/).** The constraints $y_i(w^\top x_i + b) \ge 1$ of the hard-margin problem are replaced by the [hinge loss](/hinge-loss/) $C\sum_i \max(0, 1 - y_i(w^\top x_i + b))$, an exact $\ell_1$ penalty with weight $C$.
- **[Basis pursuit](/basis-pursuit/) and the lasso.** The quadratic penalty of $\min\|x\|_1$ subject to $Ax = b$ is $\min\|x\|_1 + \tfrac{\rho}{2}\|Ax - b\|^2$, basis pursuit denoising, which is the [lasso](/lasso-regression/) with $\lambda = 1/\rho$.
- **The [big-M method](/big-m-method/) for LP.** An artificial variable in each row gets the cost $M$, a linear exact penalty on the violation of the row. For a large enough $M$ the optimum has all artificial variables at $0$.
- **[Tikhonov regularization](/tikhonov-regularization/).** The quadratic penalty of a soft constraint $Lx = 0$ on a least-squares problem.
- **[Lagrangian relaxation](/lagrangian-relaxation/).** A linear penalty $y^\top h(x)$ with a fixed price $y$. When $y$ is an optimal multiplier of a convex problem, each solution minimizes the relaxed function, but the relaxed function can have other minimizers that are not feasible.

## Variations

- **Exact $\ell_1$ penalty.** $f(x) + \rho\big(\sum_i|h_i(x)| + \sum_j\max(0, g_j(x))\big)$. For a convex problem with a multiplier vector $\lambda^*$, each solution of the constrained problem minimizes this function as soon as $\rho \ge \|\lambda^*\|_\infty$ (Zangwill, 1967; Han and Mangasarian, 1979). In the example, $\tfrac12 x^2 + \rho|x - 1|$ has its minimum at $x = 1$ exactly when $\rho \ge 1 = |y^*|$. The price is a nonsmooth function.
- **Barrier methods.** The [barrier method](/barrier-method/) adds a term that is infinite outside the feasible set and decreases its weight. It stays strictly feasible, while the penalty method approaches from outside.
- **Moreau envelope view.** The quadratic penalty of the constraint $x \in C$ is $\tfrac{\rho}{2}\operatorname{dist}(x, C)^2$, the Moreau envelope of the indicator of $C$, a smooth function with gradient $\rho(x - \Pi_C(x))$.
- **Penalty continuation in first-order methods.** Increase $\rho$ slowly while taking only a few gradient steps per value. This is common in imaging and sparse recovery.

## Pitfalls

- **Ill-conditioning.** The Hessian of $Q_\rho$ has eigenvalues of order $\rho$. With $\rho = 10^8$, [gradient descent](/gradient-descent/) needs about $10^8$ times more steps, and Newton's method loses about 8 digits in its linear solve. Increase $\rho$ step by step, use warm starts, and prefer the augmented Lagrangian method when high accuracy is needed.
- **Infeasible answers.** The quadratic penalty never gives an exactly feasible point. A user who needs exact feasibility must project, or use an exact penalty, a barrier or a multiplier method.
- **Local minimizers.** Fact 2 is about global minimizers of $Q_\rho$. For a nonconvex problem, an inner solver can stop at a local minimizer of $Q_\rho$ that is far from the feasible set.
- **Too small exact penalty weight.** If $\rho < \|\lambda^*\|_\infty$, the exact penalty function has its minimum at an infeasible point, and it can be unbounded below.

## Exercises

1. Minimize $x^3$ subject to $x \ge 1$. The solution is $x^* = 1$. Show that the quadratic penalty function $x^3 + \tfrac{\rho}{2}\max(0, 1 - x)^2$ is unbounded below for every $\rho$. Which assumption of fact 2 fails?
2. For $\min \tfrac12\|x\|^2$ subject to $a^\top x = 1$, find $x_\rho$ and $\rho\,(a^\top x_\rho - 1)$ in closed form, and show that the second converges to the multiplier.

## References
