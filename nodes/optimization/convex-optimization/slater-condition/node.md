---
tag: 32VTME
kind: theorem
slug: slater-condition
name: Slater's condition
aliases:
- Slater constraint qualification
- Slater's theorem
- Slater point
area: optimization/convex-optimization
level: core
summary: If a convex problem has a strictly feasible point, then strong duality holds, and the dual optimum is attained whenever the primal optimal value is finite.
prereqs: [lagrangian-duality, separating-hyperplane-theorem]
see_also: [kkt-conditions, convex-optimization-problem, strong-duality, lagrangian-function, fenchel-duality, lp-duality, interior-point-method, lagrange-multiplier]
sources:
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 5.2.3, Strong duality and Slater's constraint qualification, and Section 5.3.2, Proof of strong duality under constraint qualification
  - paper: "Morton Slater, Lagrange multipliers revisited: a contribution to non-linear programming, Cowles Commission Discussion Paper, Mathematics 403, 1950"
    locator: the original strict feasibility condition for convex programs
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970 (Princeton Landmarks in Mathematics edition, 1997)
    locator: Section 28, Ordinary convex programs and Lagrange multipliers (existence of Kuhn-Tucker vectors under a strict feasibility assumption)
---

Slater's condition asks that a convex optimization problem have a strictly feasible point: a point that satisfies every convex inequality constraint with strict inequality and every affine equality constraint. Slater's theorem says that under this condition the [Lagrangian dual](/lagrangian-duality/) has the same optimal value as the primal, and that a dual optimal solution exists when this value is finite. It is the most used constraint qualification in convex optimization, because it makes the [KKT conditions](/kkt-conditions/) necessary for optimality.

## Statement

Consider a convex problem

$$\text{minimize } f_0(x) \quad \text{subject to } f_i(x) \le 0,\ i = 1, \dots, m, \quad Ax = b,$$

where $f_0, \dots, f_m : \mathbb{R}^n \to \mathbb{R} \cup \{+\infty\}$ are convex, $A$ is a $p \times n$ matrix, and $\mathcal{D} = \bigcap_{i=0}^m \operatorname{dom} f_i$. Let $p^*$ be the optimal value and $d^*$ the optimal value of the Lagrange dual problem: maximize $g(\lambda, \nu) = \inf_{x \in \mathcal{D}} \left( f_0(x) + \sum_i \lambda_i f_i(x) + \nu^T (Ax - b) \right)$ subject to $\lambda \ge 0$.

**Slater's condition.** There is $\tilde{x} \in \operatorname{int} \mathcal{D}$ with $f_i(\tilde{x}) < 0$ for $i = 1, \dots, m$ and $A \tilde{x} = b$.

**Theorem (Slater).** Under Slater's condition, $d^* = p^*$. If moreover $p^* > -\infty$, there is a dual feasible $(\lambda^*, \nu^*)$ with $g(\lambda^*, \nu^*) = p^*$.

The theorem also holds with the relative interior $\operatorname{ri} \mathcal{D}$ in place of $\operatorname{int} \mathcal{D}$, and the inequality needs to be strict only for the constraints $f_i$ that are not affine (Boyd, Section 5.2.3; Rockafellar, Section 28). For a problem whose constraints are all affine, feasibility is then enough.

### Examples

- **A disk constraint.** Minimize $(x_1 - 2)^2 + (x_2 - 1)^2$ subject to $x_1^2 + x_2^2 - 1 \le 0$. The point $0$ gives $-1 < 0$, so Slater's condition holds. Strong duality holds, and the multiplier $\lambda^* = \sqrt{5} - 1 \approx 1.2361$ of the [convex optimization problem](/convex-optimization-problem/) example is a dual optimum.
- **A one-variable problem.** Minimize $x^2$ subject to $1 - x \le 0$. The point $x = 2$ gives $-1 < 0$. The dual optimum is $\lambda^* = 2$ with $d^* = p^* = 1$, as on the [Lagrangian duality](/lagrangian-duality/) page.

## In plain words

Strong duality can fail at the edge of what is allowed. If the allowed region is so thin that no point sits strictly inside the inequality rules, then the best prices for the rules may give a bound below the true answer, or the best prices may not exist.

Slater's condition rules this out: if one point satisfies every curved rule with room to spare, then the best price bound equals the true answer, and a best set of prices exists. The condition is easy to check, because one such point is enough.

## Proof

We may assume $p^* > -\infty$: otherwise $d^* \le p^* = -\infty$ by weak duality. Since $\tilde{x}$ is feasible, $p^* < +\infty$, so $p^*$ is finite. We may also assume that $A$ has full row rank: the system $Ax = b$ has the solution $\tilde{x}$, so the rows of $[A\ b]$ that are linear combinations of other rows can be removed without changing the feasible set, and a dual solution of the reduced problem extends by zeros. If $p = 0$, ignore $A$ in what follows.

**Step 1: two convex sets.** Let

$$\mathcal{A} = \{ (u, v, t) \in \mathbb{R}^m \times \mathbb{R}^p \times \mathbb{R} : \exists x \in \mathcal{D},\ f_i(x) \le u_i\ (i = 1, \dots, m),\ Ax - b = v,\ f_0(x) \le t \},$$

$$\mathcal{B} = \{ (0, 0, s) : s < p^* \}.$$

$\mathcal{A}$ is convex: if $x$ and $x'$ witness $(u, v, t)$ and $(u', v', t')$, then $\theta x + (1 - \theta) x' \in \mathcal{D}$ witnesses the convex combination, by convexity of each $f_i$ and of $\mathcal{D}$, and linearity of $Ax - b$. $\mathcal{B}$ is convex. They are disjoint: a point $(0, 0, s) \in \mathcal{A}$ would come from a feasible $x$ with $f_0(x) \le s < p^*$.

**Step 2: separation.** By the [separating hyperplane theorem](/separating-hyperplane-theorem/), there are $(\tilde{\lambda}, \tilde{\nu}, \mu) \ne 0$ and $\alpha$ with

$$\tilde{\lambda}^T u + \tilde{\nu}^T v + \mu t \ge \alpha \ \text{ on } \mathcal{A}, \qquad \mu s \le \alpha \ \text{ for all } s < p^*.$$

The coordinates $u_i$ and $t$ of a point of $\mathcal{A}$ can be increased without bound and stay in $\mathcal{A}$. If $\tilde{\lambda}_i < 0$ or $\mu < 0$, the left side would tend to $-\infty$. So $\tilde{\lambda} \ge 0$ and $\mu \ge 0$. The second inequality gives $\mu p^* \le \alpha$. With $(f_1(x), \dots, f_m(x), Ax - b, f_0(x)) \in \mathcal{A}$ for $x \in \mathcal{D}$, we get

$$\sum_{i=1}^m \tilde{\lambda}_i f_i(x) + \tilde{\nu}^T (Ax - b) + \mu f_0(x) \ge \mu p^* \quad \text{for all } x \in \mathcal{D}. \tag{1}$$

**Step 3: $\mu > 0$.** Suppose $\mu = 0$. Then (1) at $x = \tilde{x}$ gives $\sum_i \tilde{\lambda}_i f_i(\tilde{x}) \ge 0$. Each $f_i(\tilde{x}) < 0$ and $\tilde{\lambda}_i \ge 0$, so $\tilde{\lambda} = 0$. Since $(\tilde{\lambda}, \tilde{\nu}, \mu) \ne 0$, $\tilde{\nu} \ne 0$, and (1) reads $\tilde{\nu}^T (Ax - b) \ge 0$ on $\mathcal{D}$. Because $\tilde{x} \in \operatorname{int} \mathcal{D}$, the point $\tilde{x} + \varepsilon d$ lies in $\mathcal{D}$ for each $d$ and small $\varepsilon > 0$, and it gives $\varepsilon\, \tilde{\nu}^T A d \ge 0$. With $d$ and $-d$ this forces $A^T \tilde{\nu} = 0$, which contradicts the full row rank of $A$. So $\mu > 0$.

**Step 4: the dual solution.** Divide (1) by $\mu$ and put $\lambda^* = \tilde{\lambda} / \mu \ge 0$ and $\nu^* = \tilde{\nu} / \mu$. Then $L(x, \lambda^*, \nu^*) \ge p^*$ for all $x \in \mathcal{D}$, so $g(\lambda^*, \nu^*) \ge p^*$. Weak duality gives $g(\lambda^*, \nu^*) \le d^* \le p^*$. Hence $d^* = p^* = g(\lambda^*, \nu^*)$. $\blacksquare$

## Consequences

- **KKT conditions are necessary.** If Slater's condition holds and $x^*$ is optimal, then there are multipliers $(\lambda^*, \nu^*)$ such that $(x^*, \lambda^*, \nu^*)$ satisfies the [KKT conditions](/kkt-conditions/). This follows from the theorem and the argument for strong duality on the [Lagrangian duality](/lagrangian-duality/) page.
- **Saddle points.** The optimal $x^*$ and $(\lambda^*, \nu^*)$ form a saddle point of the [Lagrangian](/lagrangian-function/).
- **Bounded multipliers.** For an optimal dual solution, $L(\tilde{x}, \lambda^*, \nu^*) \ge g(\lambda^*, \nu^*) = p^*$ and $A\tilde{x} = b$ give $\sum_i \lambda_i^* (-f_i(\tilde{x})) \le f_0(\tilde{x}) - p^*$. So $\sum_i \lambda_i^* \le \frac{f_0(\tilde{x}) - p^*}{\min_i (-f_i(\tilde{x}))}$. Methods that search for the multipliers can restrict the search to this bounded set.
- **Sensitivity.** The dual optimum gives the global lower bound $p^*(u, v) \ge p^* - \lambda^{*T} u - \nu^{*T} v$ on the perturbed optimal value.
- **Interior-point methods.** [Interior-point methods](/interior-point-method/) need a strictly feasible start, or a phase that finds one. Slater's condition is the statement that such a start exists.

## Tightness

- **A positive duality gap without a Slater point.** Minimize $e^{-x}$ subject to $x^2 / y \le 0$, over $\mathcal{D} = \{(x, y) : y > 0\}$. The constraint function is convex on $\mathcal{D}$. The feasible points have $x = 0$, so $p^* = 1$. No point has $x^2 / y < 0$. For each $\lambda \ge 0$, take $y = x^3$: then $L = e^{-x} + \lambda / x \to 0$ as $x \to \infty$, and $L > 0$, so $g(\lambda) = 0$. With $\lambda = 1$ the values of $L$ are about $1.368$, $0.207$ and $0.050$ at $x = 1, 5, 20$. So $d^* = 0 < p^* = 1$.
- **Strong duality without dual attainment.** Minimize $x$ subject to $x^2 \le 0$. The only feasible point is 0, so $p^* = 0$, and there is no strictly feasible point. The dual function is $g(\lambda) = \inf_x (x + \lambda x^2) = -\frac{1}{4\lambda}$ for $\lambda > 0$ and $-\infty$ at $\lambda = 0$. So $d^* = \sup_\lambda g = 0 = p^*$, but no $\lambda$ attains it. The KKT condition $1 + 2\lambda x = 0$ has no solution at $x = 0$.
- **Convexity is needed.** Minimize $-x$ subject to $2x - 3 \le 0$ and $x \in \mathcal{D} = \{0, 1, 2\}$. The point $x = 0$ is strictly feasible, but $\mathcal{D}$ is not convex. Here $p^* = -1$ and $d^* = -\frac{3}{2}$, as computed on the [Lagrangian duality](/lagrangian-duality/) page.
- **Slater's condition is sufficient, not necessary.** Linear programs need no strictly feasible point: if the primal is feasible and $p^*$ is finite, then strong duality holds with dual attainment, by [Farkas' lemma](/farkas-lemma/). The problem of minimizing $x$ subject to $-x \le 0$ and $x \le 0$ has no strictly feasible point, but its dual has the optimum $\lambda = (1, 0)$ with $d^* = 0 = p^*$.

## History

Morton Slater introduced the condition in a 1950 Cowles Commission discussion paper on Lagrange multipliers for nonlinear programming. The paper of Kuhn and Tucker (1951) used a different constraint qualification. Slater's condition became the standard assumption of convex duality theory, and Rockafellar's Convex Analysis (1970) gives the relative interior form. The proof by separation of the sets $\mathcal{A}$ and $\mathcal{B}$ is the one in Boyd and Vandenberghe.

## References
