---
tag: K4A34E
kind: concept
slug: lagrange-multiplier
name: Lagrange multiplier
aliases:
- dual variable
- method of Lagrange multipliers
area: optimization/convex-optimization
level: intro
summary: A number attached to a constraint. It is the weight of the constraint gradient at a solution, and it measures how fast the optimal value changes when the constraint moves.
prereqs: [gradient]
see_also: [lagrangian-function, kkt-conditions, lagrangian-duality, shadow-price, constrained-optimization, complementary-slackness, lp-sensitivity-analysis]
sources:
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 12, Theory of constrained optimization (Section 12.1 examples with one equality and one inequality constraint, Theorem 12.1 first-order necessary conditions, and the section on Lagrange multipliers and sensitivity)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 5.1 (the Lagrangian and the multipliers), Section 5.5.3 (KKT conditions) and Section 5.6 (perturbation and sensitivity analysis)
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970 (Princeton Landmarks in Mathematics edition, 1997)
    locator: Section 28, Ordinary convex programs and Lagrange multipliers
---

A Lagrange multiplier is a number attached to one constraint of an optimization problem. At a solution that meets a mild regularity condition, the gradient of the objective is a linear combination of the gradients of the constraints, and the coefficients of this combination are the multipliers. Each multiplier also measures the price of its constraint: how fast the optimal value changes when the constraint is relaxed. The multipliers are the variables of the dual problem in [Lagrangian duality](/lagrangian-duality/), and in a linear program they are the [shadow prices](/shadow-price/).

## In plain words

You walk on a hill and must stay on a fixed path. You want the lowest point of the path. At that point, the path is level in the direction you walk: the downhill direction of the hill points straight across the path, not along it. So the downhill direction is a multiple of the direction that leaves the path. That multiple is the Lagrange multiplier.

The multiplier also tells you a price. If someone moves the path a little, the lowest height changes, and the multiplier says by how much for each unit of movement. A large multiplier means the constraint costs a lot. A zero multiplier means the constraint does not matter at the solution.

## The idea

We use $n$ for the number of variables. For equality constraints we use $p$ of them, $h_j(x) = 0$ for $j = 1, \ldots, p$, and for inequality constraints $m$ of them, $f_i(x) \le 0$. We write $h = (h_1, \ldots, h_p)$ and $Dh(x)$ for its $p \times n$ Jacobian, whose rows are $\nabla h_j(x)^T$.

### The equality case

**Theorem (Lagrange multiplier rule).** Let $f_0$ and $h_1, \ldots, h_p$ be continuously differentiable near $x^*$. Let $x^*$ be a local minimum of $f_0$ on $\{x : h(x) = 0\}$, and let the gradients $\nabla h_1(x^*), \ldots, \nabla h_p(x^*)$ be linearly independent. Then there is a unique $\nu^* \in \mathbb{R}^p$ with

$$\nabla f_0(x^*) + \sum_{j=1}^{p} \nu_j^* \nabla h_j(x^*) = 0.$$

*Proof.* Write $M = Dh(x^*)$. It has full row rank $p$, so $M M^T$ is invertible.

1. *Each direction in the null space of $M$ is the velocity of a feasible curve.* Fix $d$ with $M d = 0$. Define $F(t, u) = h(x^* + t d + M^T u)$ for $t \in \mathbb{R}$ and $u \in \mathbb{R}^p$. Then $F(0, 0) = h(x^*) = 0$ and the Jacobian of $F$ in $u$ at $(0, 0)$ is $M M^T$, which is invertible. By the implicit function theorem there is $\delta > 0$ and a continuously differentiable $u : (-\delta, \delta) \to \mathbb{R}^p$ with $u(0) = 0$ and $F(t, u(t)) = 0$. The derivative of $F(t, u(t)) = 0$ at $t = 0$ is $M (d + M^T u'(0)) = 0$. Since $M d = 0$, this gives $M M^T u'(0) = 0$, so $u'(0) = 0$. The curve $x(t) = x^* + t d + M^T u(t)$ is feasible, starts at $x^*$, and has $x'(0) = d$.
2. *The objective is stationary along each such curve.* The function $t \mapsto f_0(x(t))$ has a local minimum at $t = 0$, so its derivative there is 0: $\nabla f_0(x^*)^T d = 0$.
3. *The gradient lies in the row space of $M$.* Step 2 holds for each $d$ in the null space of $M$. So $\nabla f_0(x^*)$ is orthogonal to the null space of $M$, and therefore lies in the row space of $M$: $\nabla f_0(x^*) = -M^T \nu^*$ for some $\nu^*$. The rows of $M$ are independent, so $\nu^*$ is unique. $\square$

The condition on the gradients is the *linear independence constraint qualification* (LICQ). It cannot be dropped. Minimize $f_0(x) = x$ subject to $h(x) = x^2 = 0$. The only feasible point is $x^* = 0$, so it is the minimum. But $\nabla h(0) = 0$ and $\nabla f_0(0) = 1$, so no $\nu$ gives $1 + \nu \cdot 0 = 0$.

The rule is a necessary condition. It finds all candidate points, which can include maxima and saddle points.

### The Lagrangian view

With the [Lagrangian function](/lagrangian-function/) $L(x, \nu) = f_0(x) + \sum_j \nu_j h_j(x)$, the rule reads $\nabla_x L(x^*, \nu^*) = 0$, and feasibility reads $\nabla_\nu L(x^*, \nu^*) = h(x^*) = 0$. So the candidates are the stationary points of $L$ in all $n + p$ variables. This gives $n + p$ equations for $n + p$ unknowns.

### Inequality constraints

For constraints $f_i(x) \le 0$, the multipliers $\lambda_i$ have a sign and a switch: $\lambda_i \ge 0$, and $\lambda_i f_i(x^*) = 0$, so a constraint that is not tight has multiplier 0. These are the [KKT conditions](/kkt-conditions/). The sign comes from the direction of the constraint: making $f_i(x) \le 0$ looser can only lower the optimal value. The switch is [complementary slackness](/complementary-slackness/).

### The multiplier as a price

Consider the perturbed problem with constraints $f_i(x) \le u_i$ and $h_j(x) = v_j$, and let $p^*(u, v)$ be its optimal value.

**Theorem (global sensitivity).** Assume that $f_0, \ldots, f_m$ are convex, that each $h_j$ is affine, and that $\lambda^* \ge 0$ and $\nu^*$ are dual optimal with zero duality gap, so $p^*(0, 0) = g(\lambda^*, \nu^*)$ where $g$ is the Lagrange dual function. Then for all $u, v$,

$$p^*(u, v) \ge p^*(0, 0) - \lambda^{*T} u - \nu^{*T} v.$$

If $p^*$ is differentiable at $(0, 0)$, then $\lambda_i^* = -\partial p^* / \partial u_i$ and $\nu_j^* = -\partial p^* / \partial v_j$ there.

*Proof.* Let $x$ be feasible for the perturbed problem. By the definition of $g$ as an infimum of the Lagrangian,

$$p^*(0,0) = g(\lambda^*, \nu^*) \le f_0(x) + \sum_i \lambda_i^* f_i(x) + \sum_j \nu_j^* h_j(x) \le f_0(x) + \lambda^{*T} u + \nu^{*T} v,$$

where the last step uses $\lambda^* \ge 0$, $f_i(x) \le u_i$ and $h_j(x) = v_j$. Take the infimum over such $x$. For the derivative, put $u = t e_i$ and $v = 0$. The inequality gives $(p^*(t e_i, 0) - p^*(0,0))/t \ge -\lambda_i^*$ for $t > 0$, and $\le -\lambda_i^*$ for $t < 0$. Both one-sided limits equal $\partial p^* / \partial u_i$, so it equals $-\lambda_i^*$. The same argument works for $v_j$. $\square$

The convexity of the problem is used only through the zero duality gap. When the gap is zero, a constraint with a large multiplier is one that the optimal value is sensitive to. The inequality is global, not only to first order: tightening a constraint with a large $\lambda_i^*$ raises the optimal value by at least $\lambda_i^* \lvert u_i \rvert$.

## Examples

**A circle and a line.** Minimize $x_1^2 + x_2^2$ subject to $x_1 + 2x_2 = b$. With $L = x_1^2 + x_2^2 + \nu(x_1 + 2x_2 - b)$, stationarity gives $2x_1 + \nu = 0$ and $2x_2 + 2\nu = 0$, so $x_1 = -\nu/2$ and $x_2 = -\nu$. The constraint gives $-\frac52 \nu = b$, so $\nu^* = -\frac{2b}{5}$ and $x^* = (\frac{b}{5}, \frac{2b}{5})$, with $p^*(b) = \frac{b^2}{5}$. For $b = 5$: $x^* = (1, 2)$, $\nu^* = -2$ and $p^* = 5$. The constraint is $h(x) = x_1 + 2x_2 - 5 = v$, that is $b = 5 + v$, so $\frac{dp^*}{dv} = \frac{2b}{5} = 2 = -\nu^*$. For $b = 5.1$ the exact value is $p^* = 5.202$, and the first-order estimate $5 + 2 \cdot 0.1 = 5.2$ is below it, as the global sensitivity bound says.

**Two candidates, one minimum.** Minimize $x_1$ on the unit circle $x_1^2 + x_2^2 = 1$. The rule gives $1 + 2\nu x_1 = 0$ and $2 \nu x_2 = 0$. The first equation forces $\nu \ne 0$, so $x_2 = 0$ and $x_1 = \pm 1$, with $\nu = \mp \frac12$. The point $(-1, 0)$ is the minimum and $(1, 0)$ is the maximum. The rule finds both, and a comparison of values picks the minimum.

**An inequality with a positive multiplier.** Minimize $x^2$ subject to $1 - x \le 0$. The solution is $x^* = 1$. The KKT condition $2x - \lambda = 0$ gives $\lambda^* = 2$. The perturbed problem $1 - x \le u$ has $p^*(u) = (1 - u)^2$ for $u \le 1$, and $\frac{dp^*}{du}(0) = -2 = -\lambda^*$.

**A slack inequality.** Minimize $x^2$ subject to $x - 3 \le 0$. The solution $x^* = 0$ does not touch the constraint, so $\lambda^* = 0$, and moving the constraint a little does not change $p^* = 0$.

**Linear programming.** For the LP "minimize $c^T x$ subject to $Ax = b$, $x \ge 0$", the multipliers of $Ax = b$ are the variables $y$ of the [dual linear program](/dual-linear-program/). When the optimal basis does not change, $p^*(b) = b^T y^*$ is linear in $b$, and $y_i^*$ is the [shadow price](/shadow-price/) of row $i$. With the sign convention of the dual LP, $y = -\nu$.

## Where it is used

- **Optimality conditions.** The rule above and its extension to inequalities, the [KKT conditions](/kkt-conditions/), are the first-order conditions of nonlinear programming. They are the equations that Newton-type methods such as sequential quadratic programming and [interior-point methods](/interior-point-method/) solve.
- **Duality.** The multipliers are the variables of the dual problem in [Lagrangian duality](/lagrangian-duality/). Methods such as [dual ascent](/dual-ascent/), [dual decomposition](/dual-decomposition/), the [augmented Lagrangian method](/augmented-lagrangian-method/) and [ADMM](/admm/) update them directly.
- **Sensitivity analysis and economics.** A multiplier is a marginal value: the price of a unit of a scarce resource, the value of one more unit of budget, or in an LP the [shadow price](/shadow-price/) of [LP sensitivity analysis](/lp-sensitivity-analysis/).
- **Lagrangian relaxation.** In combinatorial optimization, hard constraints are moved into the objective with fixed multipliers to get bounds. See [Lagrangian relaxation](/lagrangian-relaxation/).
- **Physics and statistics.** Constrained equilibria, maximum entropy distributions (a multiplier for each moment constraint gives the exponential family) and constrained least squares are all derived with multipliers.

## References
