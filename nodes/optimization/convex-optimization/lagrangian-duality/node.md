---
tag: KKEB0A
kind: concept
slug: lagrangian-duality
name: Lagrangian duality
aliases:
- dual problem
- duality
- Lagrange duality
area: optimization/convex-optimization
level: core
summary: Pair a minimization problem with the concave problem of maximizing its Lagrange dual function. The dual optimum is a lower bound, and for convex problems under Slater's condition it is exact.
prereqs: [lagrangian-function]
see_also: [slater-condition, kkt-conditions, fenchel-duality, lp-duality, weak-duality, strong-duality, lagrangian-relaxation, dual-decomposition]
sources:
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Chapter 5, Duality (Section 5.2 the dual problem, Section 5.3 geometric interpretation, Section 5.6 perturbation and sensitivity)
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, 2nd edition, Springer, 2006
    locator: Chapter 12, Theory of constrained optimization (the section on duality)
  - paper: "Arthur M. Geoffrion, Lagrangean relaxation for integer programming, Mathematical Programming Study 2, 1974, 82-114"
    locator: the Lagrangian dual of an integer program equals the linear relaxation over the convex hull of the integer points
---

Lagrangian duality pairs a [constrained optimization](/constrained-optimization/) problem, the primal, with a second problem, the dual: maximize the dual function $g(\lambda, \nu) = \inf_x L(x, \lambda, \nu)$ of the [Lagrangian](/lagrangian-function/) over $\lambda \ge 0$. The dual is a convex problem for any primal, and its optimal value $d^*$ is a lower bound on the primal optimal value $p^*$. For convex problems that satisfy [Slater's condition](/slater-condition/) the two values are equal, and the dual solution gives the multipliers of the [KKT conditions](/kkt-conditions/). [LP duality](/lp-duality/) is the special case of linear programs.

## In plain words

Instead of forcing a solution to obey the rules, let it break them and charge a price for each unit of violation. For any choice of prices, the cheapest result of this relaxed game can be no worse than the best result that obeys the rules. So each set of prices gives a guaranteed bound.

The dual problem looks for the prices that make this bound as high as possible. For problems with a bowl shape and room inside the rules, the best bound meets the true answer, and the best prices tell how much each rule costs. For other problems, such as choices among whole numbers, a gap can remain.

## The idea

### The dual problem

For the primal problem

$$\text{minimize } f_0(x) \quad \text{subject to } f_i(x) \le 0,\ i = 1, \dots, m, \quad h_j(x) = 0,\ j = 1, \dots, p,$$

with Lagrangian $L(x, \lambda, \nu) = f_0(x) + \sum_i \lambda_i f_i(x) + \sum_j \nu_j h_j(x)$, the *Lagrange dual problem* is

$$\text{maximize } g(\lambda, \nu) \quad \text{subject to } \lambda \ge 0.$$

Its optimal value is $d^*$. The objective $g$ is concave, as the infimum of affine functions of $(\lambda, \nu)$, so the dual is a convex problem even when the primal is not. A pair $(\lambda, \nu)$ with $\lambda \ge 0$ and $g(\lambda, \nu) > -\infty$ is *dual feasible*.

### Weak duality

**Theorem (weak duality).** $d^* \le p^*$, for any problem.

*Proof.* Let $\lambda \ge 0$ and let $x$ be feasible. Then $g(\lambda, \nu) \le L(x, \lambda, \nu) = f_0(x) + \sum_i \lambda_i f_i(x) \le f_0(x)$, because each $\lambda_i f_i(x) \le 0$ and each $h_j(x) = 0$. Take the supremum over dual feasible pairs on the left and the infimum over feasible $x$ on the right. $\square$

The difference $p^* - d^*$ is the *duality gap*. For a feasible $x$ and a dual feasible $(\lambda, \nu)$, the gap $f_0(x) - g(\lambda, \nu)$ bounds the suboptimality of $x$: $f_0(x) - p^* \le f_0(x) - g(\lambda, \nu)$. If this gap is 0, then $x$ is optimal, and the dual pair is a certificate of that. Primal-dual methods, such as [interior-point methods](/interior-point-method/), stop when the gap is below the accuracy $\varepsilon$.

### Strong duality

*Strong duality* means $d^* = p^*$. It does not hold in general. It holds:

- for [linear programs](/lp-duality/) whenever the primal or the dual is feasible,
- for convex problems, where the $f_i$ are convex and the $h_j$ are affine, if there is a strictly feasible point, which is [Slater's condition](/slater-condition/). Then the dual optimum is also attained when $p^*$ is finite,
- for some nonconvex problems, such as a quadratic objective with one quadratic constraint (the S-lemma, Boyd Appendix B).

Under strong duality with $x^*$ primal optimal and $(\lambda^*, \nu^*)$ dual optimal, $f_0(x^*) = g(\lambda^*, \nu^*) \le L(x^*, \lambda^*, \nu^*) \le f_0(x^*)$. So both inequalities are equalities: $x^*$ minimizes $L(\cdot, \lambda^*, \nu^*)$, and $\lambda_i^* f_i(x^*) = 0$ for each $i$. These are the [KKT conditions](/kkt-conditions/), including [complementary slackness](/complementary-slackness/).

### The geometric view

For one inequality constraint and no equalities, let $\mathcal{G} = \{(f_1(x), f_0(x)) : x \in \mathcal{D}\} \subseteq \mathbb{R}^2$. Then $p^* = \inf\{t : (u, t) \in \mathcal{G}, u \le 0\}$, and

$$g(\lambda) = \inf\{ t + \lambda u : (u, t) \in \mathcal{G} \}.$$

The line $t + \lambda u = g(\lambda)$ touches $\mathcal{G}$ from below, and it meets the axis $u = 0$ at height $g(\lambda)$. The dual problem tilts this line to raise that height as far as possible. The best height is the value at $u = 0$ of the lower convex hull of $\mathcal{G} + (\mathbb{R}_+ \times \mathbb{R}_+)$. If this set is convex, as it is for convex problems, the height can reach $p^*$. If the lower boundary has a dent at $u = 0$, a gap remains. The proof of strong duality under Slater's condition makes this precise with the [separating hyperplane theorem](/separating-hyperplane-theorem/).

### Sensitivity

Let $p^*(u, v)$ be the optimal value when the constraints are changed to $f_i(x) \le u_i$ and $h_j(x) = v_j$. Under strong duality with dual optimum $(\lambda^*, \nu^*)$, for all $(u, v)$:

$$p^*(u, v) \ge p^*(0, 0) - \lambda^{*T} u - \nu^{*T} v.$$

*Proof.* For $x$ feasible for the changed problem, $p^*(0, 0) = g(\lambda^*, \nu^*) \le f_0(x) + \sum_i \lambda_i^* f_i(x) + \sum_j \nu_j^* h_j(x) \le f_0(x) + \lambda^{*T} u + \nu^{*T} v$. Take the infimum over such $x$. $\square$

So a large $\lambda_i^*$ means that tightening constraint $i$ raises the optimal value by a lot. This is the [Lagrange multiplier](/lagrange-multiplier/) as a price, and the [shadow price](/shadow-price/) in linear programming.

### Duality through conjugates

For linear constraints the dual function has a closed form through the [convex conjugate](/convex-conjugate/) $f_0^*(y) = \sup_x (y^T x - f_0(x))$. For the problem of minimizing $f_0(x)$ subject to $Ax \le b$ and $Cx = d$,

$$g(\lambda, \nu) = -b^T \lambda - d^T \nu - f_0^*(-A^T \lambda - C^T \nu).$$

This is the link to [Fenchel duality](/fenchel-duality/), which treats the primal as a sum of two convex functions.

## Examples

**A one-variable convex problem.** Minimize $x^2$ subject to $1 - x \le 0$. The dual function is $g(\lambda) = \lambda - \lambda^2 / 4$, as computed on the [Lagrangian function](/lagrangian-function/) page. The dual problem is to maximize it over $\lambda \ge 0$. The maximum is at $\lambda^* = 2$ with $d^* = 1 = p^*$. Slater's condition holds, since $x = 2$ is strictly feasible. Tightening the constraint to $1 - x \le u$ gives $p^*(u) = (1 - u)^2$ for $u \le 1$, and the bound $p^*(u) \ge 1 - 2u$ is its tangent line at $u = 0$.

**An integer problem with a duality gap.** Minimize $-x$ subject to $2x - 3 \le 0$ and $x \in \{0, 1, 2\}$. The feasible points are 0 and 1, so $p^* = -1$. The Lagrangian is $-x + \lambda (2x - 3)$, and

$$g(\lambda) = \min(-3\lambda,\ -1 - \lambda,\ -2 + \lambda).$$

| $\lambda$ | 0 | 1/4 | 1/2 | 3/4 | 1 |
|---|---|---|---|---|---|
| $g(\lambda)$ | $-2$ | $-7/4$ | $-3/2$ | $-9/4$ | $-3$ |

The maximum is $d^* = -3/2$ at $\lambda^* = 1/2$, where the last two terms are equal. The duality gap is $\frac{1}{2}$. In the geometric view, $\mathcal{G} = \{(-3, 0), (-1, -1), (1, -2)\}$, and the segment between the last two points crosses $u = 0$ at height $-3/2$. The dual value $-3/2$ equals the optimum of the linear relaxation, minimize $-x$ subject to $2x \le 3$ and $0 \le x \le 2$. This is a general fact for integer programs: the Lagrangian dual equals the linear relaxation over the convex hull of the integer points that are kept in the inner problem (Geoffrion, 1974).

**Linear programming.** For minimize $c^T x$ subject to $Ax = b$, $x \ge 0$, the dual function is $-b^T \nu$ on $\{A^T \nu + c \ge 0\}$ and $-\infty$ elsewhere, so the Lagrangian dual is the [dual linear program](/dual-linear-program/). Strong duality for LP needs no Slater point: it follows from [Farkas' lemma](/farkas-lemma/).

**A least-norm problem.** Minimize $x^T x$ subject to $Ax = b$, with $A$ of full row rank. The dual is to maximize $-\frac{1}{4} \nu^T A A^T \nu - b^T \nu$, which is unconstrained. Its maximizer is $\nu^* = -2 (A A^T)^{-1} b$, and $d^* = b^T (A A^T)^{-1} b = p^*$.

## Where it is used

- **Optimality certificates and stopping rules.** A dual feasible point with a small gap proves near-optimality. [Interior-point methods](/interior-point-method/) track the gap along the [central path](/central-path/).
- **Decomposition.** When the Lagrangian separates over blocks of variables, the dual function is computed block by block. [Dual ascent](/dual-ascent/) and [dual decomposition](/dual-decomposition/) maximize $g$ by (sub)gradient steps.
- **Integer programming bounds.** [Lagrangian relaxation](/lagrangian-relaxation/) moves the hard constraints into the objective, and the dual value bounds the integer optimum in branch and bound.
- **Machine learning.** The dual of the [support vector machine](/support-vector-machine/) depends on the data only through inner products, which allows kernels.
- **Game theory.** The [minimax theorem](/minimax-theorem/) for [zero-sum games](/zero-sum-game/) is LP duality for the two players' linear programs.
- **Economics and engineering.** Dual variables are prices: of resources in linear programs, of bandwidth in network utility maximization, and of power in resource allocation.

## References
