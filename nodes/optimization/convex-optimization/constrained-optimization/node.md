---
tag: C98PX0
kind: problem
slug: constrained-optimization
name: Constrained optimization
aliases:
- nonlinear programming
- mathematical programming
area: optimization/convex-optimization
level: core
summary: Find the minimum of an objective function over the points that satisfy given equality and inequality constraints.
prereqs: [gradient]
see_also: [convex-optimization-problem, kkt-conditions, lagrange-multiplier, linear-programming-problem, quadratic-programming, mixed-integer-programming, global-optimization, penalty-method]
sources:
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 12, Theory of constrained optimization (local and global solutions, the KKT theorem under LICQ, second-order conditions), and Chapters 15 to 19 (the main algorithms)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 4.1 (optimization problems in standard form, feasibility, optimal value, local optima, equivalent problems)
  - paper: "Panos M. Pardalos and Stephen A. Vavasis, Quadratic programming with one negative eigenvalue is NP-hard, Journal of Global Optimization 1(1), 15 to 22 (1991)"
    locator: the main theorem
  - paper: "Katta G. Murty and Santosh N. Kabadi, Some NP-complete problems in quadratic and nonlinear programming, Mathematical Programming 39, 117 to 129 (1987)"
    locator: the hardness of deciding whether a point is a local minimum
---

Constrained optimization is the problem of finding the minimum of an objective function over the points that satisfy a list of equality and inequality constraints. It contains [linear programming](/linear-programming-problem/), [quadratic programming](/quadratic-programming/), [convex optimization](/convex-optimization-problem/) and [integer programming](/mixed-integer-programming/) as special cases. When the problem is convex it can be solved to any accuracy in polynomial time, under mild conditions on how the data is given. In general it is NP-hard, even with one nonconvex quadratic term, and algorithms find only local solutions or bounds.

## In plain words

You want the best value of some quantity, but not every choice is allowed. A budget must not be exceeded, a part must fit in a box, a sum of fractions must be one. The allowed choices form a region, and you look for the best point inside that region.

Without rules, the best point is where the ground is flat. With rules, the best point can also sit on the edge of the region, pressed against a rule, while the ground still slopes. The rules that press are the ones that matter, and the theory measures how hard each one presses. When the region and the objective are both bowl shaped, every low point you find is the lowest one. Otherwise there can be many valleys, and finding the deepest is hard.

## Definition

We use $n$ for the number of variables, $m$ for the number of inequality constraints and $p$ for the number of equality constraints.

**Input.** An objective $f_0 : \mathbb{R}^n \to \mathbb{R}$, inequality constraint functions $f_1, \ldots, f_m$, equality constraint functions $h_1, \ldots, h_p$, and optionally a set $X \subseteq \mathbb{R}^n$ (for example $\mathbb{Z}^n$ or a box).

**The problem.**

$$\begin{aligned} \text{minimize} \quad & f_0(x) \\ \text{subject to} \quad & f_i(x) \le 0, \quad i = 1, \ldots, m, \\ & h_j(x) = 0, \quad j = 1, \ldots, p, \\ & x \in X. \end{aligned}$$

**Terms.**

- The *feasible set* is $S = \{x \in X : f_i(x) \le 0 \text{ for all } i, \ h_j(x) = 0 \text{ for all } j\}$.
- The *optimal value* is $f^* = \inf_{x \in S} f_0(x)$, with $f^* = +\infty$ if $S = \emptyset$ (infeasible) and $f^* = -\infty$ if $f_0$ is unbounded below on $S$ (unbounded).
- A *global minimum* (an optimal solution) is $x^* \in S$ with $f_0(x^*) = f^*$. A *local minimum* is $x^* \in S$ with $f_0(x^*) \le f_0(x)$ for all $x \in S$ with $\lVert x - x^* \rVert \le r$, for some $r > 0$.
- The constraint $f_i \le 0$ is *active* at $x$ if $f_i(x) = 0$. Equality constraints are always active at a feasible point.
- A maximization problem is the minimization of $-f_0$, and $f_i(x) \ge 0$ is $-f_i(x) \le 0$.

**Output.** One of: an optimal solution $x^*$ with $f^*$; a proof that $S$ is empty; a proof that $f^* = -\infty$; or, when the minimum is not attained, a sequence in $S$ whose values tend to $f^*$. A numerical method gives an approximate solution, for example $x$ with constraint violation at most $\varepsilon$ and $f_0(x) \le f^* + \varepsilon$. A local method gives a point that satisfies first-order conditions, such as the [KKT conditions](/kkt-conditions/), up to a tolerance.

**Existence.** If $S$ is nonempty and compact and $f_0$ is continuous on $S$, a global minimum exists (the Weierstrass extreme value theorem). This holds for example when all $f_i$ and $h_j$ are continuous, $X$ is closed, and one constraint bounds the region. A minimum can fail to exist on an unbounded set: $e^{-x}$ on $x \ge 0$ has $f^* = 0$, and no $x$ attains it.

**Optimality conditions.** At a local minimum where a constraint qualification holds, such as the linear independence of the gradients of the active constraints, there are [Lagrange multipliers](/lagrange-multiplier/) $\lambda \ge 0$ and $\nu$ with

$$\nabla f_0(x^*) + \sum_{i=1}^m \lambda_i \nabla f_i(x^*) + \sum_{j=1}^p \nu_j \nabla h_j(x^*) = 0, \qquad \lambda_i f_i(x^*) = 0.$$

These are the [KKT conditions](/kkt-conditions/), where the page proves them. They are necessary, not sufficient, unless the problem is convex.

## Variants

- **By the form of the functions.** [Linear programming](/linear-programming-problem/) (all functions affine). [Quadratic programming](/quadratic-programming/) (quadratic objective, affine constraints). Quadratically constrained programs. [Convex optimization](/convex-optimization-problem/) ($f_0, \ldots, f_m$ convex, $h_j$ affine), which includes [second-order cone](/second-order-cone-programming/) and [semidefinite programming](/semidefinite-programming/). General nonlinear programming (smooth functions, no convexity).
- **By the set $X$.** Continuous ($X = \mathbb{R}^n$), [integer and mixed-integer programming](/mixed-integer-programming/) ($X$ includes integrality), and box constraints $\ell \le x \le u$.
- **Equality constraints only.** The classical problem of [Lagrange multipliers](/lagrange-multiplier/).
- **Feasibility.** The objective is 0, and the task is to find a point of $S$ or prove that $S$ is empty. For convex constraints this is the [convex feasibility problem](/convex-feasibility-problem/).
- **Local versus global.** Find a local minimum (or a KKT point), or find a global minimum, which is the subject of [global optimization](/global-optimization/).
- **Several objectives.** Minimize a vector of objectives, which leads to Pareto optimality in multi-objective optimization.

## Examples

**A minimum on the boundary.** Minimize $f_0(x) = (x_1 - 1)^2 + (x_2 - 2)^2$ subject to $x_1 + x_2 \le 2$, $x_1 \ge 0$ and $x_2 \ge 0$. The unconstrained minimum $(1, 2)$ has $x_1 + x_2 = 3$, so it is not feasible. The solution is the nearest feasible point, $x^* = (0.5, 1.5)$, with $f^* = 0.5$. Only $x_1 + x_2 \le 2$ is active. Its multiplier $\lambda = 1$ satisfies $\nabla f_0(x^*) + \lambda (1, 1) = (-1, -1) + (1, 1) = 0$. The problem is convex, so this KKT point is the global minimum.

**Several local minima.** Minimize $f_0(x) = x^4 - 3x^2 + x$ subject to $-2 \le x \le 2$. The derivative $4x^3 - 6x + 1$ has three roots:

| point | kind | value |
|---|---|---|
| $x = -2$ | end point | $2$ |
| $x \approx -1.3008$ | local minimum | $\approx -3.5139$ |
| $x \approx 0.1699$ | local maximum | $\approx 0.0841$ |
| $x \approx 1.1309$ | local minimum | $\approx -1.0702$ |
| $x = 2$ | end point | $6$ |

The global minimum is at $x \approx -1.3008$. A descent method started at $x = 1.5$ stops at the local minimum $x \approx 1.1309$, whose value is more than $2.4$ higher. In one variable, the list of critical points and end points settles the question. In many variables there can be exponentially many local minima.

**No multiplier at the minimum.** Minimize $x$ subject to $x^2 \le 0$. The only feasible point, $x = 0$, is optimal. The constraint gradient $2x$ is 0 there, and $1 + \lambda \cdot 0 = 0$ has no solution. The constraint qualification fails, and so do the KKT conditions.

## Known algorithms

- **Linear programs.** The [simplex method](/simplex-method/), the [ellipsoid method](/ellipsoid-method/) and [interior-point methods](/interior-point-method/).
- **Projection methods.** When projection on $S$ is cheap (a box, a ball, a simplex), [projected gradient descent](/projected-gradient-descent/) and the [proximal gradient method](/proximal-gradient-method/) treat the constraint by projection.
- **Penalty and barrier methods.** The [penalty method](/penalty-method/) adds a growing cost for violation. The [barrier method](/barrier-method/) adds a cost that becomes infinite at the boundary and follows the [central path](/central-path/). Both solve a sequence of unconstrained problems.
- **Multiplier methods.** The [augmented Lagrangian method](/augmented-lagrangian-method/) and [ADMM](/admm/) update the [Lagrange multipliers](/lagrange-multiplier/) between unconstrained steps. [Dual ascent](/dual-ascent/) and [dual decomposition](/dual-decomposition/) work on the dual problem.
- **Newton-type methods on the KKT system.** Active-set methods for [quadratic programming](/quadratic-programming/), sequential quadratic programming, and primal-dual [interior-point methods](/interior-point-method/) solve the KKT equations with Newton steps.
- **Nonsmooth convex problems.** The [cutting-plane method](/cutting-plane-method/) and the [bundle method](/bundle-method/).
- **Integer constraints.** Branch and bound and [branch and cut](/branch-and-cut/) on top of an [LP relaxation](/lp-relaxation/).

## Bounds

- **Convex problems.** With a separation oracle for the feasible set and a subgradient oracle for the objective, the [ellipsoid method](/ellipsoid-method/) reaches accuracy $\varepsilon$ in a number of oracle calls polynomial in $n$ and $\log(1/\varepsilon)$, given bounds on the size of the feasible set. Interior-point methods with a self-concordant barrier of parameter $\vartheta$ need $O(\sqrt{\vartheta} \log(1/\varepsilon))$ Newton steps. The details are on the [convex optimization problem](/convex-optimization-problem/) page.
- **First-order lower bounds.** For methods that use only gradients or subgradients, there are lower bounds on the number of oracle calls in terms of $\varepsilon$, which hold in high dimension. See [first-order lower bounds](/first-order-lower-bound/).
- **Nonconvex quadratic programs.** Minimizing a quadratic function over a polytope is NP-hard, even when the Hessian has only one negative eigenvalue (Pardalos and Vavasis 1991).
- **Local optimality.** Deciding whether a given feasible point is a local minimum of a quadratic program is NP-hard (Murty and Kabadi 1987). So even the local question has no efficient general algorithm.
- **Integer programs.** Integer linear programming is [NP-hard](/np-hard/). For a fixed number of variables, it is polynomial by [Lenstra's algorithm](/lenstra-algorithm/).

## Reductions

- **To an unconstrained problem.** Add the indicator function $I_S$ (0 on $S$, $+\infty$ off $S$): minimize $f_0 + I_S$. This exact form is nonsmooth. Penalty and barrier methods replace $I_S$ by finite approximations.
- **Epigraph form.** Minimize $t$ subject to $f_0(x) \le t$ and the old constraints. The objective becomes linear. See [epigraph](/epigraph/).
- **Equality to inequality.** $h(x) = 0$ is $h(x) \le 0$ and $-h(x) \le 0$. This keeps convexity only when $h$ is affine, and it breaks constraint qualifications such as Slater's.
- **Inequality to equality.** $f_i(x) \le 0$ is $f_i(x) + s_i = 0$ with a slack variable $s_i \ge 0$, as in the [slack form](/lp-slack-form/) of an LP.
- **Integrality to a nonconvex constraint.** $x_i \in \{0, 1\}$ is $x_i(1 - x_i) = 0$. So continuous constrained optimization contains 0/1 integer programming, and is NP-hard in general.

## Applications

- Engineering design: minimize weight or cost subject to strength, size and safety limits.
- Resource allocation and economics: maximize utility under budgets, with prices given by the multipliers.
- Machine learning: [support vector machines](/support-vector-machine/), constrained regression such as the constrained form of the [lasso](/lasso-regression/), and fairness or norm constraints on models.
- Finance: [portfolio optimization](/portfolio-optimization/) under budget and risk constraints.
- Control: model predictive control solves a constrained problem at each time step.
- Operations research: scheduling, routing and production planning, often with integer variables.

## References
