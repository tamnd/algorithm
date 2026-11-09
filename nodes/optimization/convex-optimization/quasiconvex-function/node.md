---
tag: 2TD6T2
kind: definition
slug: quasiconvex-function
name: Quasiconvex function
aliases:
- quasi-convex function
- quasiconcave function
- quasilinear function
area: optimization/convex-optimization
level: advanced
summary: A function whose sublevel sets are all convex. Equivalently, its value on a segment never exceeds the larger of the values at the end points.
prereqs: [convex-function]
see_also: [convex-set, convex-feasibility-problem, convex-optimization-problem, unimodal-function, fractional-programming, ternary-search, bisection-method, geometric-programming]
sources:
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 3.4, Quasiconvex functions, and Section 4.2.5, Quasiconvex optimization (the bisection method)
  - paper: "Kenneth J. Arrow and Alain C. Enthoven, Quasi-concave programming, Econometrica 29(4), 1961, 779-800"
    locator: optimality conditions for maximizing a quasiconcave function under quasiconvex constraints
---

A quasiconvex function is a function whose sublevel sets $\{x : f(x) \le \alpha\}$ are all [convex sets](/convex-set/). Every [convex function](/convex-function/) is quasiconvex, but so are many nonconvex ones, such as $\lceil x \rceil$, $\log x$, and ratios of an affine function to a positive affine function. A quasiconvex function can have local minima that are not global, but it can still be minimized by bisection on its value, with a [convex feasibility problem](/convex-feasibility-problem/) at each step.

## Definition

Let $f : \mathbb{R}^n \to \mathbb{R} \cup \{+\infty\}$ have a convex domain. For $\alpha \in \mathbb{R}$, the *$\alpha$-sublevel set* is $S_\alpha = \{x \in \operatorname{dom} f : f(x) \le \alpha\}$.

- $f$ is *quasiconvex* if $S_\alpha$ is convex for every $\alpha$.
- $f$ is *quasiconcave* if $-f$ is quasiconvex, that is, if every superlevel set $\{x : f(x) \ge \alpha\}$ is convex.
- $f$ is *quasilinear* if it is both.

### The max inequality

**Theorem 1.** $f$ is quasiconvex if and only if, for all $x, y \in \operatorname{dom} f$ and $\theta \in [0, 1]$,

$$f(\theta x + (1 - \theta) y) \le \max(f(x), f(y)).$$

*Proof.* Assume the sublevel sets are convex, and let $\alpha = \max(f(x), f(y))$. Then $x, y \in S_\alpha$, so $\theta x + (1 - \theta) y \in S_\alpha$, which is the inequality. Conversely, assume the inequality, and let $x, y \in S_\alpha$. Then $f(\theta x + (1 - \theta) y) \le \max(f(x), f(y)) \le \alpha$, so $S_\alpha$ is convex. $\square$

The max inequality is weaker than the convexity inequality $f(\theta x + (1 - \theta) y) \le \theta f(x) + (1 - \theta) f(y)$, because the right side of that one is at most $\max(f(x), f(y))$. So every convex function is quasiconvex.

In one variable, Theorem 1 says that $f$ is quasiconvex if and only if there are no $a < b < c$ with $f(b) > \max(f(a), f(c))$. A continuous function on an interval is quasiconvex exactly when it is nonincreasing, nondecreasing, or nonincreasing up to some point and nondecreasing after it. These are the [unimodal functions](/unimodal-function/) with a minimum, and [ternary search](/ternary-search/) minimizes them.

### A first-order condition

**Theorem 2.** Let $f$ be quasiconvex and differentiable on an open convex set. If $f(y) \le f(x)$, then $\nabla f(x)^T (y - x) \le 0$.

*Proof.* For $t \in [0, 1]$, Theorem 1 gives $f(x + t(y - x)) \le \max(f(x), f(y)) = f(x)$. So the function $t \mapsto f(x + t(y - x))$ has its maximum over $[0, 1]$ at $t = 0$, and its right derivative there, $\nabla f(x)^T (y - x)$, is at most 0. $\square$

The converse also holds: a differentiable function with this property is quasiconvex (Boyd and Vandenberghe, Section 3.4). The condition says that $\nabla f(x)$, when nonzero, is the normal of a [supporting hyperplane](/supporting-hyperplane-theorem/) of the sublevel set $S_{f(x)}$ at $x$. Unlike for convex functions, $\nabla f(x) = 0$ does not imply that $x$ is a minimum: $f(x) = x^3$ is quasiconvex with $f'(0) = 0$.

### Operations that keep quasiconvexity

- **Maximum.** If $f_1, \dots, f_k$ are quasiconvex, so is $\max_i f_i$: its sublevel set $S_\alpha$ is $\bigcap_i \{f_i \le \alpha\}$, an intersection of convex sets. The same holds for a supremum over any family.
- **Nondecreasing transformation.** If $f$ is quasiconvex and $g : \mathbb{R} \to \mathbb{R}$ is nondecreasing, then $g \circ f$ is quasiconvex. Its sublevel set $\{x : g(f(x)) \le \alpha\}$ equals $\{x : f(x) \in J\}$, where $J = \{s : g(s) \le \alpha\}$ is an interval that is unbounded below, so the set is a sublevel set of $f$ or a union of a nested family of them, which is convex.
- **Affine composition.** $x \mapsto f(Ax + b)$ is quasiconvex, since its sublevel sets are preimages of convex sets under an affine map.
- **Sums are not kept.** The sum of two quasiconvex functions need not be quasiconvex; see the examples.

### Minimization by bisection

For minimizing a quasiconvex $f_0$ subject to convex constraints, write each sublevel set as $\{x : \phi_t(x) \le 0\}$ with $\phi_t$ convex. For example, for $f_0 = p / q$ with $p$ convex and nonnegative and $q$ concave and positive, take $\phi_t = p - t q$. Then $p^* \le t$ if and only if the convex feasibility problem

$$\phi_t(x) \le 0, \quad f_i(x) \le 0, \quad Ax = b$$

has a solution. Given $\ell \le p^* \le u$, bisection on $t$ halves the interval $[\ell, u]$ with each feasibility test, so $\lceil \log_2((u - \ell)/\varepsilon) \rceil$ tests give $p^*$ to within $\varepsilon$.

## Examples and non-examples

- **Ceiling.** $\lceil x \rceil$ is quasilinear: its sublevel sets are the half-lines $(-\infty, k]$ for integers $k$. It is not continuous, and it is not convex.
- **Logarithm.** $\log x$ on $(0, \infty)$ is nondecreasing, so it is quasilinear, but it is concave and not convex.
- **Square root of the absolute value.** $\sqrt{\lvert x \rvert}$ is quasiconvex, since its sublevel sets are intervals $[-\alpha^2, \alpha^2]$. It is not convex, since its value at $\frac{1}{2}$ is $0.707$, above the chord value $\frac{1}{2}$ between 0 and 1.
- **Product.** $f(x) = x_1 x_2$ on $\mathbb{R}^2_+$ is quasiconcave: for $\alpha > 0$ the superlevel set $\{x_1 x_2 \ge \alpha\}$ is the region above a branch of a hyperbola, which is convex. At the midpoint of $(1, 0)$ and $(0, 1)$ its value is $\frac{1}{4} \ge \min(0, 0)$, as quasiconcavity requires. It is not concave, since along the diagonal $f(t, t) = t^2$ is strictly convex. Utility functions in economics are often assumed quasiconcave in this way.
- **Linear-fractional functions.** $f(x) = (a^T x + b)/(c^T x + d)$ on $\{c^T x + d > 0\}$ is quasilinear: $\{f \le t\} = \{a^T x + b \le t(c^T x + d)\}$ is a half-space intersected with the domain, and the same holds for $\{f \ge t\}$. This is the basis of linear [fractional programming](/fractional-programming/).
- **A bisection run.** Minimize $f(x) = (\lVert x \rVert^2 + 1)/(x_1 + x_2)$ over $x_1 + x_2 > 0$. The test "$p^* \le t$" asks whether $\lVert x \rVert^2 + 1 - t(x_1 + x_2) \le 0$ for some $x$. The minimum of the left side, at $x = (t/2, t/2)$, is $1 - t^2/2$, so the test passes exactly when $t^2 \ge 2$. Starting from $[0, 4]$, the tests at $t = 2, 1, 1.5, 1.25, 1.375, 1.4375$ are feasible, infeasible, feasible, infeasible, infeasible, feasible, which leaves $[1.375, 1.4375]$. The optimum is $\sqrt{2} \approx 1.4142$, at $x = (1/\sqrt{2}, 1/\sqrt{2})$. This $f$ happens to be convex as well, but the method uses only the convexity of the sets $\{\phi_t \le 0\}$.
- **Non-example: a sum.** $x^3$ and $-3x$ are both monotone, hence quasilinear, but $f(x) = x^3 - 3x$ is not quasiconvex. Its sublevel set $\{f \le 0\} = (-\infty, -\sqrt{3}] \cup [0, \sqrt{3}]$ is not an interval. Also $f(-1) = 2 > \max(f(-2), f(1)) = -2$, which violates Theorem 1.
- **A local minimum that is not global.** $f(x) = \min(\max(x, 0), 1)$ is nondecreasing, hence quasiconvex. Each $x > 1$ is a local minimum with value 1, since $f = 1$ near $x$, but the global minimum is 0. A convex function has no such points.

## Related definitions

- A *strictly quasiconvex* function satisfies $f(\theta x + (1 - \theta) y) < \max(f(x), f(y))$ for $f(x) \ne f(y)$ and $\theta \in (0, 1)$. For such functions each local minimum is global.
- A *pseudoconvex* function is differentiable and satisfies $\nabla f(x)^T (y - x) \ge 0 \Rightarrow f(y) \ge f(x)$. For it, $\nabla f(x) = 0$ implies a global minimum. Convex implies pseudoconvex, which implies quasiconvex.
- A function is *log-convex* if $\log f$ is convex. Log-convex functions are convex, and log-concave functions are quasiconcave. [Geometric programming](/geometric-programming/) uses a related change of variables.
- [Unimodal functions](/unimodal-function/) are the one-variable case.

## References
