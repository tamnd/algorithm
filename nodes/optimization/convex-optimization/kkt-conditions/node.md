---
tag: MERSHB
kind: theorem
slug: kkt-conditions
name: Karush-Kuhn-Tucker conditions
aliases:
- KKT conditions
- KKT optimality conditions
- Kuhn-Tucker conditions
area: optimization/convex-optimization
level: core
summary: Feasibility, nonnegative multipliers, complementary slackness and a zero Lagrangian gradient. Necessary for optimality under a constraint qualification, and sufficient for convex problems.
prereqs: [lagrangian-function, slater-condition]
see_also: [lagrange-multiplier, complementary-slackness, farkas-lemma, quadratic-programming, interior-point-method, central-path, constrained-optimization, support-vector-machine]
sources:
  - paper: "William Karush, Minima of functions of several variables with inequalities as side conditions, Master's thesis, Department of Mathematics, University of Chicago, 1939"
    locator: the first statement of the first-order conditions with inequality constraints
  - paper: "Harold W. Kuhn and Albert W. Tucker, Nonlinear programming, in Proceedings of the Second Berkeley Symposium on Mathematical Statistics and Probability, University of California Press, 1951, 481-492"
    locator: the conditions under the Kuhn-Tucker constraint qualification and the saddle-point form for convex problems
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, 2nd edition, Springer, 2006
    locator: Chapter 12, Theorem 12.1 (first-order necessary conditions under LICQ), and Chapter 16 (KKT systems of quadratic programs and active-set methods)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 5.5.3, KKT optimality conditions (necessity under strong duality and sufficiency for convex problems)
---

The Karush-Kuhn-Tucker (KKT) conditions are the first-order optimality conditions of a [constrained optimization](/constrained-optimization/) problem with inequality and equality constraints. They extend the method of [Lagrange multipliers](/lagrange-multiplier/) to inequalities: the gradient of the [Lagrangian](/lagrangian-function/) vanishes, the multipliers of the inequalities are nonnegative, and a multiplier is zero when its constraint is slack. For convex problems they are sufficient for optimality, and they are also necessary under [Slater's condition](/slater-condition/). For general smooth problems they are necessary at a local minimum under a constraint qualification such as linear independence of the active gradients.

## Statement

Consider the problem

$$\text{minimize } f_0(x) \quad \text{subject to } f_i(x) \le 0,\ i = 1, \dots, m, \quad h_j(x) = 0,\ j = 1, \dots, p,$$

where all functions are defined and differentiable on an open set $\mathcal{D} \subseteq \mathbb{R}^n$. The Lagrangian is $L(x, \lambda, \nu) = f_0(x) + \sum_i \lambda_i f_i(x) + \sum_j \nu_j h_j(x)$. A triple $(x^*, \lambda^*, \nu^*)$ with $x^* \in \mathcal{D}$ satisfies the *KKT conditions* if

1. *primal feasibility:* $f_i(x^*) \le 0$ for all $i$ and $h_j(x^*) = 0$ for all $j$,
2. *dual feasibility:* $\lambda_i^* \ge 0$ for all $i$,
3. *complementary slackness:* $\lambda_i^* f_i(x^*) = 0$ for all $i$,
4. *stationarity:* $\nabla f_0(x^*) + \sum_{i=1}^m \lambda_i^* \nabla f_i(x^*) + \sum_{j=1}^p \nu_j^* \nabla h_j(x^*) = 0$.

The constraint $i$ is *active* at $x^*$ if $f_i(x^*) = 0$. Let $I(x^*)$ be the set of active indices. By condition 3, $\lambda_i^* = 0$ for $i \notin I(x^*)$.

**Theorem 1 (sufficiency for convex problems).** Let $f_0, \dots, f_m$ be convex and $h_1, \dots, h_p$ affine. If $(x^*, \lambda^*, \nu^*)$ satisfies the KKT conditions, then $x^*$ is optimal, $(\lambda^*, \nu^*)$ is optimal for the Lagrange dual problem, and the duality gap is zero.

**Theorem 2 (necessity under Slater's condition).** Let the problem be convex as in Theorem 1, with $\mathcal{D}$ open, and assume Slater's condition: some $\tilde{x} \in \mathcal{D}$ has $f_i(\tilde{x}) < 0$ for all $i$ and $h_j(\tilde{x}) = 0$ for all $j$. If $x^*$ is optimal, then there are $\lambda^*, \nu^*$ such that $(x^*, \lambda^*, \nu^*)$ satisfies the KKT conditions.

**Theorem 3 (necessity under LICQ).** Let all functions be continuously differentiable near $x^*$, and let $x^*$ be a local minimum. Assume the *linear independence constraint qualification* (LICQ): the vectors $\nabla f_i(x^*)$ for $i \in I(x^*)$ and $\nabla h_j(x^*)$ for $j = 1, \dots, p$ are linearly independent. Then there are unique $\lambda^*, \nu^*$ such that $(x^*, \lambda^*, \nu^*)$ satisfies the KKT conditions.

### Example

Minimize $(x_1 - 1)^2 + (x_2 - 2)^2$ subject to $x_1 + x_2 - 2 \le 0$, $-x_1 \le 0$ and $-x_2 \le 0$. At $x^* = (\frac{1}{2}, \frac{3}{2})$ only the first constraint is active. Stationarity asks $(2 x_1^* - 2, 2 x_2^* - 4) + \lambda_1 (1, 1) = (-1, -1) + \lambda_1 (1, 1) = 0$, so $\lambda^* = (1, 0, 0)$. All four conditions hold, the problem is convex, and Theorem 1 shows that $x^*$ is optimal, with value $\frac{1}{2}$. The implementation in this page's folder finds this point from the KKT system, as described under Consequences.

## In plain words

At the best point of a problem with rules, no small move can both obey the rules and improve the result. The KKT conditions write this down as a balance of forces. The pull of the objective toward a better value is held back by pushes from the rules that are tight at that point. Each push has a strength, and a push can only point outward from the allowed region. A rule that is not tight does not push at all.

For bowl-shaped problems, any point where such a balance exists is the best point. For other problems, the balance is a test that every best point passes, as long as the rules are not degenerate at that point.

## Proof

**Proof of Theorem 1.** Fix $(\lambda^*, \nu^*)$. Since $\lambda^* \ge 0$, the function $x \mapsto L(x, \lambda^*, \nu^*)$ is a nonnegative combination of convex functions plus affine functions, so it is convex. By stationarity its gradient is 0 at $x^*$, so by the first-order condition for convex functions, $x^*$ minimizes it over $\mathcal{D}$. Hence

$$g(\lambda^*, \nu^*) = L(x^*, \lambda^*, \nu^*) = f_0(x^*) + \sum_i \lambda_i^* f_i(x^*) + \sum_j \nu_j^* h_j(x^*) = f_0(x^*),$$

by complementary slackness and primal feasibility. For each feasible $x$, weak duality gives $f_0(x) \ge g(\lambda^*, \nu^*) = f_0(x^*)$. So $x^*$ is optimal, and $(\lambda^*, \nu^*)$ is dual optimal with zero gap. $\square$

**Proof of Theorem 2.** The optimal value $p^* = f_0(x^*)$ is finite. By [Slater's theorem](/slater-condition/) there is a dual feasible $(\lambda^*, \nu^*)$ with $g(\lambda^*, \nu^*) = p^*$. Then

$$f_0(x^*) = g(\lambda^*, \nu^*) \le L(x^*, \lambda^*, \nu^*) = f_0(x^*) + \sum_i \lambda_i^* f_i(x^*) \le f_0(x^*).$$

So both inequalities are equalities. The second one gives $\sum_i \lambda_i^* f_i(x^*) = 0$, a sum of terms that are each at most 0, so each term is 0: complementary slackness. The first one says that $x^*$ minimizes $L(\cdot, \lambda^*, \nu^*)$ over the open set $\mathcal{D}$, so its gradient vanishes at $x^*$: stationarity. Primal and dual feasibility hold by assumption. $\square$

**Proof of Theorem 3.** Write $a_0 = \nabla f_0(x^*)$, $a_i = \nabla f_i(x^*)$ and $c_j = \nabla h_j(x^*)$.

*Step 1: no improving direction.* We show that there is no $d$ with

$$a_0^T d < 0, \qquad a_i^T d \le 0 \ (i \in I(x^*)), \qquad c_j^T d = 0 \ (j = 1, \dots, p). \tag{1}$$

Suppose $d$ satisfies (1). By LICQ the linear system $a_i^T w = -1$ for $i \in I(x^*)$ and $c_j^T w = 0$ for all $j$ has a solution $w$, because its coefficient rows are linearly independent. For small $\varepsilon > 0$, the direction $d_\varepsilon = d + \varepsilon w$ satisfies $a_0^T d_\varepsilon < 0$, $a_i^T d_\varepsilon \le -\varepsilon < 0$ for active $i$, and $c_j^T d_\varepsilon = 0$.

Let $H$ be the $p \times n$ matrix with rows $c_j^T$. It has full row rank. Consider the equation $h(x^* + t d_\varepsilon + H^T y) = 0$ in the unknown $y \in \mathbb{R}^p$, for $t$ near 0. At $(t, y) = (0, 0)$ it holds, and its Jacobian in $y$ is $H H^T$, which is invertible. By the implicit function theorem there is a continuously differentiable $y(t)$ with $y(0) = 0$ that solves it for small $\lvert t \rvert$. Differentiating at $t = 0$ gives $H d_\varepsilon + H H^T y'(0) = 0$, so $y'(0) = 0$. (If $p = 0$, take $y \equiv 0$.) The curve $x(t) = x^* + t d_\varepsilon + H^T y(t)$ has $x(0) = x^*$ and $x'(0) = d_\varepsilon$.

For small $t > 0$:

- $h_j(x(t)) = 0$ for all $j$, by construction,
- $f_i(x(t)) = t\, a_i^T d_\varepsilon + o(t) < 0$ for active $i$,
- $f_i(x(t)) < 0$ for inactive $i$, by continuity, since $f_i(x^*) < 0$,
- $f_0(x(t)) = f_0(x^*) + t\, a_0^T d_\varepsilon + o(t) < f_0(x^*)$.

So $x(t)$ is feasible, arbitrarily close to $x^*$, and better than $x^*$. This contradicts local optimality. Hence (1) has no solution.

*Step 2: Farkas' lemma.* Consider the cone $K$ generated by the vectors $a_i$ ($i \in I(x^*)$), $c_j$ and $-c_j$ ($j = 1, \dots, p$). By [Farkas' lemma](/farkas-lemma/), either $-a_0 \in K$, or there is $d$ with $a_i^T d \le 0$, $c_j^T d \le 0$, $-c_j^T d \le 0$ and $-a_0^T d > 0$. The second alternative is a solution of (1), which Step 1 excludes. So $-a_0 = \sum_{i \in I(x^*)} \lambda_i^* a_i + \sum_j (\alpha_j - \beta_j) c_j$ with $\lambda_i^*, \alpha_j, \beta_j \ge 0$. Put $\nu_j^* = \alpha_j - \beta_j$ and $\lambda_i^* = 0$ for inactive $i$. This gives stationarity, dual feasibility and complementary slackness, and primal feasibility holds because $x^*$ is feasible.

*Step 3: uniqueness.* If two multiplier vectors satisfy stationarity, their difference gives a linear combination of the active $a_i$ and the $c_j$ equal to 0. By LICQ it is the zero combination. $\blacksquare$

## Consequences

**Solving small quadratic programs from the KKT system.** For a strictly convex [quadratic program](/quadratic-programming/), minimize $\frac{1}{2} x^T Q x + c^T x$ subject to $Ax \le b$ with $Q$ positive definite, the KKT conditions are necessary and sufficient, since the constraints are affine. If the set $S$ of active constraints at the optimum were known, the conditions would reduce to the linear system

$$\begin{pmatrix} Q & A_S^T \\ A_S & 0 \end{pmatrix} \begin{pmatrix} x \\ \lambda_S \end{pmatrix} = \begin{pmatrix} -c \\ b_S \end{pmatrix}.$$

The implementation in `impl/python/kkt_conditions.py` uses this:

1. For each set $S$ of at most $n$ constraints, in order of size, solve the system above exactly with rational arithmetic. Skip $S$ if the matrix is singular.
2. Reject $S$ if some $\lambda_S$ is negative or if $x$ violates a constraint $a_k^T x \le b_k$.
3. Otherwise return $x$ and the multipliers, with $\lambda_k = 0$ for $k \notin S$. By Theorem 1, $x$ is optimal.
4. If no $S$ passes, the problem is infeasible.

At an optimum, the conic form of [Carathéodory's theorem](/caratheodory-theorem/) writes $-(Qx^* + c)$ with a linearly independent set of active rows. For that set the matrix is nonsingular, so step 1 reaches it and the search is complete. The search costs $O(m^n)$ linear solves, so it is a reference method for small problems. Active-set methods move between neighboring sets $S$ instead, and [interior-point methods](/interior-point-method/) avoid the choice of $S$. On the example above, $S = \emptyset$ gives $x = (1, 2)$, which violates $x_1 + x_2 \le 2$. Then $S = \{1\}$ gives $2x_1 + \lambda_1 = 2$, $2x_2 + \lambda_1 = 4$ and $x_1 + x_2 = 2$, with solution $x = (\frac{1}{2}, \frac{3}{2})$ and $\lambda_1 = 1$, which passes step 2. The tests compare the solver with Hildreth's dual coordinate ascent in floating point, to a tolerance of $10^{-6}$, on random instances with up to 3 variables and 5 constraints, and check that no random feasible point has a smaller objective value.

**Other consequences.**

- **Interior-point methods.** Replacing complementary slackness by $\lambda_i f_i(x) = -1/t$ gives the [central path](/central-path/). Primal-dual [interior-point methods](/interior-point-method/) apply Newton's method to these perturbed KKT equations.
- **Sensitivity.** The multipliers are the derivatives of the optimal value with respect to the constraint levels, as explained on the [Lagrange multiplier](/lagrange-multiplier/) page.
- **Support vectors.** In the [support vector machine](/support-vector-machine/), complementary slackness says that only the training points on or inside the margin have nonzero multipliers.
- **Linear programming.** For a linear program, the KKT conditions are primal feasibility, dual feasibility and [complementary slackness](/complementary-slackness/), which is the LP optimality criterion.

## Tightness

- **A constraint qualification is needed for necessity.** Minimize $x$ subject to $x^2 \le 0$. The only feasible point, $x^* = 0$, is optimal. Stationarity asks $1 + 2\lambda x^* = 1 = 0$, which fails for every $\lambda$. Here LICQ fails, because $\nabla(x^2) = 0$ at 0, and Slater's condition fails, because $x^2 < 0$ has no solution.
- **Convexity is needed for sufficiency.** Minimize $-x^2$ subject to $x - 1 \le 0$ and $-x - 1 \le 0$. The point $x = 0$ with $\lambda = (0, 0)$ satisfies the KKT conditions, but it is a global maximum: $f_0(0) = 0 > -1 = f_0(\pm 1)$.
- **Without LICQ the multipliers need not be unique.** Minimize $x$ subject to $-x \le 0$ and $-2x \le 0$. At $x^* = 0$ every $\lambda \ge 0$ with $\lambda_1 + 2\lambda_2 = 1$ works. The problem is convex and has a Slater point, so Theorem 2 still gives existence.
- **Theorem 3 gives a necessary condition only.** The point $x = 0$ of the second example passes it, as does every local maximum in the interior of the feasible set. Second-order conditions on the Hessian of the Lagrangian separate minima from other KKT points.

## History

William Karush stated the conditions in his 1939 master's thesis at the University of Chicago. Fritz John gave a version with a multiplier on the objective in 1948, which needs no constraint qualification. Harold Kuhn and Albert Tucker published the conditions in 1951, together with the saddle-point form for convex problems, and the name Kuhn-Tucker conditions was used until Karush's priority became widely known. Kuhn and Tucker's constraint qualification was later replaced in most texts by LICQ, by Slater's condition, and by the Mangasarian-Fromovitz condition.

## References
