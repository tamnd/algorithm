---
tag: X217KT
kind: problem
slug: convex-optimization-problem
name: Convex optimization problem
aliases:
- convex program
- convex optimization
area: optimization/convex-optimization
level: core
summary: Minimize a convex function over a convex set given by convex inequalities and affine equations. Each local minimum is global, and the problem is tractable under mild oracle assumptions.
prereqs: [convex-function, convex-set, constrained-optimization]
see_also: [kkt-conditions, lagrangian-duality, slater-condition, interior-point-method, ellipsoid-method, linear-programming-problem, quadratic-programming, semidefinite-programming]
sources:
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 4.2 (convex optimization, local and global optima, the optimality criterion for differentiable objectives), Sections 4.3 to 4.7 (LP, QP, SOCP, GP, conic and vector problems) and Section 11.5 (the complexity of barrier methods)
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, second edition, Springer, 2018
    locator: Chapter 3 (nonsmooth convex optimization, lower complexity bounds and the subgradient and ellipsoid methods) and Chapter 5 (polynomial-time interior-point methods with self-concordant barriers)
  - paper: doi:10.1561/2200000050
    title: Sébastien Bubeck, Convex Optimization, Algorithms and Complexity, Foundations and Trends in Machine Learning 8(3-4), 2015
    locator: Section 2.2 (the ellipsoid method and its rate) and Section 3.5 (lower bounds for black-box methods)
  - paper: doi:10.1007/s10107-011-0499-2
    title: Amir Ali Ahmadi, Alex Olshevsky, Pablo A. Parrilo and John N. Tsitsiklis, NP-hardness of deciding convexity of quartic polynomials and related problems, Mathematical Programming 137, 2013
    locator: the main theorem (deciding convexity of a quartic polynomial is strongly NP-hard)
  - paper: "Etienne de Klerk and Dmitrii V. Pasechnik, Approximation of the stability number of a graph via copositive programming, SIAM Journal on Optimization 12(4), 875 to 892 (2002)"
    locator: the copositive formulation of the stability number
---

A convex optimization problem asks for the minimum of a [convex function](/convex-function/) over a [convex set](/convex-set/) that is given by convex inequality constraints and affine equality constraints. In such a problem each local minimum is a global minimum, the set of solutions is convex, and simple first-order conditions certify optimality. [Lagrangian duality](/lagrangian-duality/) gives lower bounds that are tight under [Slater's condition](/slater-condition/). Under mild assumptions on how the problem is given, it can be solved to accuracy $\varepsilon$ in time polynomial in the size and in $\log(1/\varepsilon)$. Linear, convex quadratic, second-order cone and semidefinite programs are special cases.

## In plain words

Think of a valley shaped like a bowl, and a fenced field that has no dents or holes in its boundary. You want the lowest point of the valley inside the field. Because the valley is a bowl and the field has no dents, you can always walk downhill toward the answer without being trapped. If you stand at a point where no allowed direction goes down, you are at the lowest point of the whole field, not only of a nearby dip.

This is why bowl-shaped problems are the ones that computers solve reliably. A method only needs to keep going down and stop when it cannot. A certificate from the other side, a lower bound from duality, tells you how far from the best you can still be.

## Definition

We use $n$ for the number of variables, $m$ for the number of inequality constraints and $p$ for the number of equality constraints.

**Input.** Convex functions $f_0, f_1, \ldots, f_m : \mathbb{R}^n \to \mathbb{R} \cup \{+\infty\}$, a matrix $A \in \mathbb{R}^{p \times n}$ and a vector $b \in \mathbb{R}^p$.

**The problem (standard form).**

$$\begin{aligned} \text{minimize} \quad & f_0(x) \\ \text{subject to} \quad & f_i(x) \le 0, \quad i = 1, \ldots, m, \\ & Ax = b. \end{aligned}$$

The domain is $D = \bigcap_{i=0}^m \operatorname{dom} f_i$. The feasible set $S = \{x \in D : f_i(x) \le 0, \ Ax = b\}$ is convex: each sublevel set $\{f_i \le 0\}$ of a convex function is convex, $\{Ax = b\}$ is affine, and an intersection of convex sets is convex. The optimal value is $f^* = \inf_{x \in S} f_0(x)$, as in [constrained optimization](/constrained-optimization/).

An equality constraint $h(x) = 0$ is allowed only when $h$ is affine. With $h(x) = x_1^2 + x_2^2 - 1$, the feasible set is a circle, which is not convex.

**Output.** An $\varepsilon$-solution: a point $x \in S$ (or within $\varepsilon$ of $S$) with $f_0(x) - f^* \le \varepsilon$, together with a certificate when one is available, usually a dual point $(\lambda, \nu)$ whose dual value is within $\varepsilon$ of $f_0(x)$. Exact solutions are in general not finite objects: the solution of the example below involves $\sqrt{5}$.

### The basic theorems

**Theorem 1 (local minima are global).** Let $x^*$ be a local minimum of a convex problem. Then $x^*$ is a global minimum.

*Proof.* Assume that some $y \in S$ has $f_0(y) < f_0(x^*)$. For $t \in (0, 1]$, the point $z_t = x^* + t(y - x^*)$ is in $S$, because $S$ is convex. By the convexity of $f_0$, $f_0(z_t) \le (1 - t) f_0(x^*) + t f_0(y) < f_0(x^*)$. As $t \to 0$, the points $z_t$ come arbitrarily close to $x^*$, so $x^*$ is not a local minimum. $\square$

**Theorem 2 (the solution set).** The set of optimal solutions is convex. If $f_0$ is strictly convex on $S$, there is at most one optimal solution.

*Proof.* The solution set is $S \cap \{x : f_0(x) \le f^*\}$, an intersection of two convex sets. If $x \ne y$ were both optimal and $f_0$ strictly convex, the midpoint would be feasible with value less than $f^*$. $\square$

**Theorem 3 (first-order optimality).** Let $f_0$ be convex and differentiable on an open set that contains $S$. Then $x \in S$ is optimal if and only if

$$\nabla f_0(x)^T (y - x) \ge 0 \quad \text{for all } y \in S.$$

*Proof.* If the condition holds, the first-order test for convex functions gives $f_0(y) \ge f_0(x) + \nabla f_0(x)^T (y - x) \ge f_0(x)$ for each $y \in S$. Conversely, assume that $\nabla f_0(x)^T (y - x) < 0$ for some $y \in S$. The function $\varphi(t) = f_0(x + t(y - x))$ has $\varphi'(0) = \nabla f_0(x)^T(y - x) < 0$, so $\varphi(t) < \varphi(0)$ for small $t > 0$. The points $x + t(y - x)$ are in $S$ by convexity, so $x$ is not optimal. $\square$

Geometrically, $-\nabla f_0(x)$ defines a [supporting hyperplane](/supporting-hyperplane-theorem/) of $S$ at $x$, unless it is 0. Special cases: with no constraints, the condition is $\nabla f_0(x) = 0$. With only $Ax = b$, it is $\nabla f_0(x) = A^T \nu$ for some $\nu$. On the orthant $x \ge 0$, it is $\nabla f_0(x) \ge 0$ and $x_i \, (\nabla f_0(x))_i = 0$ for each $i$. For nondifferentiable $f_0$, the condition becomes $0 \in \partial f_0(x) + N_S(x)$, with the [subdifferential](/subdifferential/) and the normal cone of $S$. With constraint functions and a constraint qualification, it becomes the [KKT conditions](/kkt-conditions/).

## Variants

- **[Linear programming](/linear-programming-problem/):** all functions affine.
- **Convex [quadratic programming](/quadratic-programming/):** $f_0(x) = \frac12 x^T Q x + c^T x$ with $Q$ positive semidefinite, affine constraints.
- **[Second-order cone programming](/second-order-cone-programming/):** constraints $\lVert A_i x + b_i \rVert_2 \le c_i^T x + d_i$. It contains convex quadratically constrained programs.
- **[Semidefinite programming](/semidefinite-programming/):** a linear matrix inequality $F_0 + \sum_k x_k F_k \succeq 0$. It contains LP and SOCP.
- **[Geometric programming](/geometric-programming/):** not convex as written, but convex after the change of variables $x_k = e^{y_k}$ and a logarithm of the functions.
- **Conic form:** minimize $c^T x$ subject to $Ax = b$, $x \in K$ for a closed convex cone $K$. Each convex problem can be written in this form.
- **Unconstrained and composite problems:** minimize $f(x)$, or $f(x) + h(x)$ with $f$ smooth and $h$ simple, as in the [lasso](/lasso-regression/).
- **Feasibility:** $f_0 = 0$. This is the [convex feasibility problem](/convex-feasibility-problem/).
- **Quasiconvex problems:** $f_0$ [quasiconvex](/quasiconvex-function/). Local minima need not be global, but bisection on the level reduces the problem to a sequence of convex feasibility problems.

## Examples

**Projection on a disk.** Minimize $f_0(x) = (x_1 - 2)^2 + (x_2 - 1)^2$ subject to $x_1^2 + x_2^2 - 1 \le 0$. Both functions are convex. The unconstrained minimum $a = (2, 1)$ has $\lVert a \rVert = \sqrt{5} > 1$, so the constraint is active. The KKT condition $2(x - a) + 2\lambda x = 0$ gives $x = a / (1 + \lambda)$, and $\lVert x \rVert = 1$ gives $\lambda^* = \sqrt{5} - 1 \approx 1.2361 \ge 0$. So

$$x^* = \frac{a}{\sqrt 5} \approx (0.8944, 0.4472), \qquad f^* = (\sqrt5 - 1)^2 = 6 - 2\sqrt5 \approx 1.5279.$$

Theorem 3 confirms it: $\nabla f_0(x^*) = -2\lambda^* x^*$, so $\nabla f_0(x^*)^T(y - x^*) = 2\lambda^*(1 - x^{*T} y) \ge 0$ for each $y$ in the disk, by the Cauchy-Schwarz inequality.

**Least squares and its relatives.** Minimize $\lVert Ax - b \rVert_2^2$, with no constraints. The condition $\nabla f_0 = 0$ gives the normal equations $A^T A x = A^T b$. Adding $\lambda \lVert x \rVert_1$ gives the lasso, which is still convex but not differentiable.

**Same set, convex or not.** Minimize $x_1 + x_2$ subject to $x_1^2 + x_2^2 \le 1$ is convex, with solution $-\frac{1}{\sqrt2}(1, 1)$. Maximize the same objective over the same disk is also convex (it is minimizing a linear function). But maximize $x_1^2 + x_2^2$ over a square is not convex: the objective is maximized, and each of the four corners is a local maximum.

**A convex problem written in a nonconvex way.** The constraint $x_1 x_2 \ge 1$ with $x_1, x_2 > 0$ is not of the form "convex function $\le 0$" as written, since $1 - x_1 x_2$ is not convex. But the same set is $\{-\log x_1 - \log x_2 \le 0\}$, and $-\log x_1 - \log x_2$ is convex. Convexity is a property of the set and the function, not of the formula. Modeling tools check a sufficient rule set (disciplined convex programming) on the formula.

## Known algorithms

- **[Interior-point methods](/interior-point-method/)** and the [barrier method](/barrier-method/): Newton steps along the [central path](/central-path/). The method of choice for small and medium LP, SOCP and SDP.
- **The [ellipsoid method](/ellipsoid-method/)** and other [cutting-plane methods](/cutting-plane-method/): need only a separation oracle. They give the theoretical polynomial bounds.
- **First-order methods:** [gradient descent](/gradient-descent/), [projected gradient descent](/projected-gradient-descent/), the [proximal gradient method](/proximal-gradient-method/), [FISTA](/fista/), [mirror descent](/mirror-descent/) and the subgradient method. One cheap step per iteration, used for large problems.
- **Splitting and dual methods:** [ADMM](/admm/), [dual ascent](/dual-ascent/), [dual decomposition](/dual-decomposition/), the [augmented Lagrangian method](/augmented-lagrangian-method/).
- **Nonsmooth methods:** the [bundle method](/bundle-method/) and the [proximal point method](/proximal-point-method/).
- **Special structure:** the [simplex method](/simplex-method/) for LP, active-set methods for QP.

## Bounds

All bounds count oracle calls or arithmetic steps to reach $f_0(x) - f^* \le \varepsilon$.

- **Ellipsoid method (proved, worst case).** Assume that $S$ lies in a ball of radius $R$, contains a ball of radius $r$, and that $f_0$ varies by at most $V$ on $S$. Then the ellipsoid method reaches accuracy $\varepsilon$ after $O(n^2 \log(R V / (r \varepsilon)))$ iterations, each with one separation or subgradient oracle call and $O(n^2)$ arithmetic. The bound is polynomial in $n$ and $\log(1/\varepsilon)$.
- **Interior-point methods (proved, worst case).** For a problem in conic form with a self-concordant barrier of parameter $\vartheta$, a path-following method needs $O(\sqrt{\vartheta} \log(\vartheta / \varepsilon))$ Newton steps, after a suitable start. For LP with $m$ inequality constraints, $\vartheta = m$. Each Newton step solves one linear system.
- **First-order lower bounds (proved).** For convex $f_0$ with subgradients bounded by $G$ on a ball of radius $R$, each method that only uses subgradients needs $\Omega(G^2 R^2 / \varepsilon^2)$ calls when $n$ is large enough, and for $L_f$-smooth $f_0$ it needs $\Omega(\sqrt{L_f R^2 / \varepsilon})$ calls. These match the subgradient method and [Nesterov's accelerated method](/nesterov-accelerated-gradient/) up to constants. See [first-order lower bounds](/first-order-lower-bound/).
- **Convexity is not enough.** Polynomial time needs efficient oracles. Linear optimization over the cone of copositive matrices is a convex problem, and it can express NP-hard problems such as the stability number of a graph. Deciding whether a quartic polynomial is convex is strongly NP-hard (Ahmadi, Olshevsky, Parrilo and Tsitsiklis 2013). So a formula cannot always be checked for convexity.
- **Exactness.** An LP with rational data has a rational optimal vertex of polynomial size. A general convex problem does not: the example below has an irrational solution, and the convex constraints $x_1 \ge 2$ and $x_k^2 - x_{k+1} \le 0$ for $k = 1, \ldots, n-1$ force $x_n \ge 2^{2^{n-1}}$, a number with exponentially many digits. So the bounds are about $\varepsilon$-solutions, not exact ones.

## Reductions

- **Epigraph form.** Each convex problem is equivalent to one with a linear objective: minimize $t$ subject to $f_0(x) - t \le 0$. See [epigraph](/epigraph/).
- **To conic form.** Each convex problem can be written as minimizing $c^T x$ over an affine slice of a closed convex cone, which is the input of conic interior-point solvers.
- **Optimization to feasibility.** Bisection on $t$ in "is $\{x \in S : f_0(x) \le t\}$ nonempty?" reduces optimization to $O(\log(V/\varepsilon))$ [convex feasibility problems](/convex-feasibility-problem/).
- **Dual problem.** The [Lagrangian dual](/lagrangian-duality/) is again a convex problem. Under [Slater's condition](/slater-condition/) it has the same value, and solving either side gives a certificate for the other.
- **Phase I.** Finding a strictly feasible start for a barrier method is itself a convex problem: minimize $s$ subject to $f_i(x) \le s$, $Ax = b$.

## Applications

- Statistics and machine learning: least squares, [ridge regression](/ridge-regression/), the [lasso](/lasso-regression/), [logistic regression](/logistic-regression/), [support vector machines](/support-vector-machine/) and [maximum likelihood estimation](/maximum-likelihood-estimation/) in exponential families.
- Finance: mean-variance [portfolio optimization](/portfolio-optimization/).
- Control and signal processing: model predictive control, filter design, compressed sensing.
- Geometry: the [minimum enclosing ball](/minimum-enclosing-ball/), the [minimum volume enclosing ellipsoid](/minimum-volume-enclosing-ellipsoid/) and the [geometric median](/geometric-median/).
- Combinatorial optimization: [convex relaxations](/convex-relaxation/), such as the [LP relaxation](/lp-relaxation/) and semidefinite relaxations of max cut, give bounds and rounding schemes.

## References
