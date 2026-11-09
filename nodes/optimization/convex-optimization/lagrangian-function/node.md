---
tag: 5KV4QF
kind: definition
slug: lagrangian-function
name: Lagrangian function
aliases:
- Lagrangian
- Lagrange function
area: optimization/convex-optimization
level: core
summary: The objective plus a weighted sum of the constraint functions, L(x, λ, ν) = f0(x) + Σ λi fi(x) + Σ νj hj(x), with the Lagrange multipliers as weights.
prereqs: [constrained-optimization, lagrange-multiplier]
see_also: [lagrangian-duality, kkt-conditions, slater-condition, dual-linear-program, lagrangian-relaxation, augmented-lagrangian-method, minimax-theorem, dual-ascent]
sources:
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 5.1, The Lagrange dual function, and Section 5.4, Saddle-point interpretation
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970 (Princeton Landmarks in Mathematics edition, 1997)
    locator: Section 28, Ordinary convex programs and Lagrange multipliers (Kuhn-Tucker vectors and saddle points of the Lagrangian)
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, 2nd edition, Springer, 2006
    locator: Chapter 12, Theory of constrained optimization (the Lagrangian function and the first-order conditions)
---

The Lagrangian function of a [constrained optimization](/constrained-optimization/) problem adds to the objective each constraint function times a [Lagrange multiplier](/lagrange-multiplier/). Minimizing it over the variables, for fixed multipliers, gives the dual function, which is concave and bounds the optimal value from below. The [KKT conditions](/kkt-conditions/) say that its gradient in the variables vanishes at an optimum, and [Lagrangian duality](/lagrangian-duality/) is the study of its maximin and minimax values.

## Definition

Consider the problem in standard form, with $n$ variables, $m$ inequality constraints and $p$ equality constraints:

$$\text{minimize } f_0(x) \quad \text{subject to } f_i(x) \le 0,\ i = 1, \dots, m, \quad h_j(x) = 0,\ j = 1, \dots, p.$$

Let $\mathcal{D}$ be the set of points where all the $f_i$ and $h_j$ are defined, and let $p^*$ be the optimal value. The *Lagrangian* is the function $L : \mathcal{D} \times \mathbb{R}^m \times \mathbb{R}^p \to \mathbb{R}$,

$$L(x, \lambda, \nu) = f_0(x) + \sum_{i=1}^m \lambda_i f_i(x) + \sum_{j=1}^p \nu_j h_j(x).$$

The vectors $\lambda$ and $\nu$ are the *multipliers*, or *dual variables*. Only $\lambda \ge 0$ is of interest for the inequality constraints. The *Lagrange dual function* is

$$g(\lambda, \nu) = \inf_{x \in \mathcal{D}} L(x, \lambda, \nu),$$

with the value $-\infty$ when $L$ is unbounded below in $x$.

The Lagrangian depends on how the constraints are written, not only on the feasible set. For example, $x \le 0$ and $x^3 \le 0$ describe the same set, but they give different Lagrangians and different multipliers.

### Basic properties

**Theorem 1 (concavity).** $g$ is concave on $\mathbb{R}^m \times \mathbb{R}^p$, even when the problem is not convex.

*Proof.* For each fixed $x$, the map $(\lambda, \nu) \mapsto L(x, \lambda, \nu)$ is affine. $g$ is the pointwise infimum of this family of affine maps, and the hypograph of an infimum of affine maps is an intersection of closed half-spaces, so it is convex. $\square$

**Theorem 2 (lower bound).** If $\lambda \ge 0$, then $g(\lambda, \nu) \le p^*$.

*Proof.* Let $\tilde{x}$ be feasible. Then $\lambda_i f_i(\tilde{x}) \le 0$ and $\nu_j h_j(\tilde{x}) = 0$, so $L(\tilde{x}, \lambda, \nu) \le f_0(\tilde{x})$. Hence $g(\lambda, \nu) \le L(\tilde{x}, \lambda, \nu) \le f_0(\tilde{x})$. Take the infimum over feasible $\tilde{x}$. $\square$

**Theorem 3 (the primal as a minimax).** For $x \in \mathcal{D}$,

$$\sup_{\lambda \ge 0,\, \nu} L(x, \lambda, \nu) = \begin{cases} f_0(x) & \text{if } x \text{ is feasible}, \\ +\infty & \text{otherwise}. \end{cases}$$

So $p^* = \inf_x \sup_{\lambda \ge 0, \nu} L$, and the dual optimal value is $d^* = \sup_{\lambda \ge 0, \nu} \inf_x L$.

*Proof.* If $x$ is feasible, each term $\lambda_i f_i(x)$ is at most 0 and is 0 at $\lambda = 0$, and each $\nu_j h_j(x)$ is 0. If $f_i(x) > 0$ for some $i$, let $\lambda_i \to \infty$. If $h_j(x) \ne 0$, let $\nu_j = t\, h_j(x)$ with $t \to \infty$. $\square$

The inequality $d^* \le p^*$ is then the max-min inequality $\sup_y \inf_x \le \inf_x \sup_y$, which holds for any function. This is weak duality.

**Theorem 4 (saddle points).** Suppose $x^* \in \mathcal{D}$, $\lambda^* \ge 0$ and $\nu^*$ satisfy

$$L(x^*, \lambda, \nu) \le L(x^*, \lambda^*, \nu^*) \le L(x, \lambda^*, \nu^*) \quad \text{for all } x \in \mathcal{D},\ \lambda \ge 0,\ \nu.$$

Then $x^*$ is optimal for the primal problem, $(\lambda^*, \nu^*)$ is optimal for the dual problem, $p^* = d^*$, and $\lambda_i^* f_i(x^*) = 0$ for each $i$.

*Proof.* The left inequality says that $L(x^*, \cdot, \cdot)$ is maximized at $(\lambda^*, \nu^*)$. Its supremum is finite, so by Theorem 3, $x^*$ is feasible, and the supremum is $f_0(x^*)$. Hence $L(x^*, \lambda^*, \nu^*) = f_0(x^*)$, which gives $\sum_i \lambda_i^* f_i(x^*) = 0$. Each term is at most 0, so each term is 0. The right inequality says $g(\lambda^*, \nu^*) = L(x^*, \lambda^*, \nu^*) = f_0(x^*)$. By Theorem 2, $f_0(x^*) = g(\lambda^*, \nu^*) \le d^* \le p^* \le f_0(x^*)$, so all are equal. $\square$

The converse holds for convex problems under [Slater's condition](/slater-condition/): an optimal $x^*$ and an optimal dual pair form a saddle point. Without convexity a saddle point can fail to exist; see the integer example on the [Lagrangian duality](/lagrangian-duality/) page.

## Examples and non-examples

- **A one-variable problem.** Minimize $x^2$ subject to $1 - x \le 0$, so $p^* = 1$ at $x^* = 1$. The Lagrangian is $L(x, \lambda) = x^2 + \lambda (1 - x)$. For fixed $\lambda$ it is minimized at $x = \lambda / 2$, so $g(\lambda) = \lambda - \lambda^2 / 4$. At $\lambda = 0, 1, 2, 3, 4$ the values are $0, \frac{3}{4}, 1, \frac{3}{4}, 0$, all at most $p^* = 1$. The maximum is $g(2) = 1 = p^*$. The point $(x^*, \lambda^*) = (1, 2)$ is a saddle point: $L(1, \lambda) = 1$ for every $\lambda$, and $L(x, 2) = (x - 1)^2 + 1 \ge 1$.
- **Least norm.** Minimize $x^T x$ subject to $Ax = b$. Here $L(x, \nu) = x^T x + \nu^T (Ax - b)$. Setting $\nabla_x L = 2x + A^T \nu = 0$ gives $x = -A^T \nu / 2$ and $g(\nu) = -\frac{1}{4} \nu^T A A^T \nu - b^T \nu$. For $A = (1\ 2)$ and $b = 5$: $g(\nu) = -\frac{5}{4} \nu^2 - 5 \nu$, with values $\frac{15}{4}, 5, \frac{15}{4}$ at $\nu = -3, -2, -1$. The maximum is $g(-2) = 5$, and $x = (1, 2)$ gives $p^* = 5$.
- **Linear programming.** Minimize $c^T x$ subject to $Ax = b$, $x \ge 0$. With multipliers $\lambda$ for $-x \le 0$ and $\nu$ for $Ax - b = 0$, $L = (c - \lambda + A^T \nu)^T x - b^T \nu$. A linear function of $x$ is bounded below only if it is constant, so $g(\lambda, \nu) = -b^T \nu$ if $c - \lambda + A^T \nu = 0$ and $-\infty$ otherwise. Eliminating $\lambda \ge 0$ gives the [dual linear program](/dual-linear-program/): maximize $-b^T \nu$ subject to $A^T \nu + c \ge 0$. For $c = (1, 2)$, $A = (1\ 1)$ and $b = 1$, the primal optimum is $1$ at $x = (1, 0)$, and the dual constraint $\nu \ge -1$ gives the dual optimum $1$ at $\nu = -1$.
- **The representation matters.** Minimize $x$ over $x \in \mathbb{R}$ subject to $x \ge 0$, so $p^* = 0$. Written as $-x \le 0$, the Lagrangian is $(1 - \lambda) x$, so $g(\lambda) = 0$ for $\lambda = 1$ and $-\infty$ otherwise, and $d^* = 0 = p^*$. Written as $-x^3 \le 0$, the Lagrangian is $x - \lambda x^3$, which is unbounded below for each $\lambda \ge 0$, so $g \equiv -\infty$ and $d^* = -\infty$. The feasible set is the same, but the second form has no multiplier.
- **Non-example: a negative multiplier for an inequality.** Minimize $x^2$ subject to $x - 1 \le 0$, so $p^* = 0$ at $x = 0$. The dual function is $g(\lambda) = -\frac{\lambda^2}{4} - \lambda$. At $\lambda = -1$ it is $\frac{3}{4} > p^*$, so Theorem 2 fails without the sign condition $\lambda \ge 0$.

## Related definitions

- The [Lagrange multiplier](/lagrange-multiplier/) is a component of $(\lambda, \nu)$. At an optimum it measures the sensitivity of $p^*$ to the constraint.
- The *dual problem* is to maximize $g(\lambda, \nu)$ subject to $\lambda \ge 0$. It is a convex problem for any primal; see [Lagrangian duality](/lagrangian-duality/).
- The *augmented Lagrangian* adds $\frac{\rho}{2} \sum_j h_j(x)^2$ to $L$. It is the basis of the [augmented Lagrangian method](/augmented-lagrangian-method/) and of [ADMM](/admm/).
- [Lagrangian relaxation](/lagrangian-relaxation/) in integer programming moves hard constraints into $L$ and maximizes $g$ to get bounds.
- The *Hessian of the Lagrangian*, $\nabla_{xx}^2 L$, enters the second-order optimality conditions and Newton-type methods for constrained problems.

## References
