---
tag: 41P41Y
kind: definition
slug: strong-convexity
name: Strong convexity
aliases:
- mu-strong convexity
- strongly convex function
area: optimization/convex-optimization
level: core
summary: Convexity with a quadratic lower bound of curvature μ > 0. A μ-strongly convex function has a unique minimizer, and the gap to it grows at least like (μ/2)‖x − x*‖².
prereqs: [convex-function]
see_also: [smoothness, condition-number-of-an-optimization-problem, linear-convergence-strongly-convex, polyak-lojasiewicz-condition, ridge-regression, convex-conjugate, gradient-descent, positive-definite-matrix]
sources:
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, 2nd edition, Springer, 2018
    locator: Section 2.1.3, Strongly convex functions (equivalent conditions and the class of smooth strongly convex functions)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 9.1.2, Strong convexity and implications
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 5, Smoothness and strong convexity (equivalent characterizations, the conjugate correspondence between strong convexity and smoothness)
---

A function is strongly convex with parameter $\mu > 0$ if it stays convex after a quadratic bowl of curvature $\mu$ is taken away from it. Equivalently, it lies above each of its tangent planes by at least $\frac{\mu}{2}$ times the squared distance. This gives a unique minimizer, a quadratic growth of the gap to it, and a lower bound on the gradient norm, and these three facts make [gradient descent](/gradient-descent/) converge at a linear rate. Together with [smoothness](/smoothness/) of constant $L_f$, the ratio $\kappa = L_f / \mu$ is the [condition number](/condition-number-of-an-optimization-problem/) that sets the speed of first-order methods.

## Definition

Let $f : \mathbb{R}^n \to \mathbb{R} \cup \{+\infty\}$ and $\mu > 0$. The function $f$ is *$\mu$-strongly convex* if

$$h(x) = f(x) - \frac{\mu}{2} \lVert x \rVert^2$$

is convex. Here $\lVert \cdot \rVert$ is the Euclidean norm. The constant $\mu$ is the *modulus* of strong convexity. A strongly convex function is strictly convex, and a strictly convex function need not be strongly convex.

### Equivalent conditions

**Theorem 1.** Each of the following is equivalent to $\mu$-strong convexity. Conditions (b) and (d) assume that $f$ is differentiable on $\mathbb{R}^n$, and (c) assumes that $f$ is twice continuously differentiable on $\mathbb{R}^n$.

- (a) $f(\theta x + (1 - \theta) y) \le \theta f(x) + (1 - \theta) f(y) - \frac{\mu}{2} \theta (1 - \theta) \lVert x - y \rVert^2$ for all $x, y$ and $\theta \in [0, 1]$.
- (b) $f(y) \ge f(x) + \nabla f(x)^T (y - x) + \frac{\mu}{2} \lVert y - x \rVert^2$ for all $x, y$.
- (c) $\nabla^2 f(x) \succeq \mu I$ for all $x$.
- (d) $(\nabla f(x) - \nabla f(y))^T (x - y) \ge \mu \lVert x - y \rVert^2$ for all $x, y$.

*Proof.* Each condition is the matching condition for convexity of $h$, rewritten in terms of $f$.

- (a) Expand the squares to get the identity $\lVert \theta x + (1 - \theta) y \rVert^2 = \theta \lVert x \rVert^2 + (1 - \theta) \lVert y \rVert^2 - \theta (1 - \theta) \lVert x - y \rVert^2$. Multiply it by $\frac{\mu}{2}$ and subtract it from the inequality of (a). The result is the convexity inequality for $h$.
- (b) $\nabla h(x) = \nabla f(x) - \mu x$. The first-order condition $h(y) \ge h(x) + \nabla h(x)^T (y - x)$ becomes $f(y) \ge f(x) + \nabla f(x)^T (y - x) + \frac{\mu}{2} (\lVert y \rVert^2 - \lVert x \rVert^2 - 2 x^T (y - x))$, and the last bracket equals $\lVert y - x \rVert^2$. The first-order condition characterizes convexity of a differentiable function, as on the [convex function](/convex-function/) page.
- (c) $\nabla^2 h = \nabla^2 f - \mu I$, and $h$ is convex if and only if $\nabla^2 h \succeq 0$.
- (d) $(\nabla h(x) - \nabla h(y))^T (x - y) = (\nabla f(x) - \nabla f(y))^T (x - y) - \mu \lVert x - y \rVert^2$. A differentiable function is convex if and only if its gradient is monotone: add the first-order inequalities at $x$ and at $y$ for one direction, and for the other direction, apply monotonicity to $\phi(t) = h(x + t(y - x))$, whose derivative is then nondecreasing. $\square$

### Consequences for minimization

In this section $f$ is $\mu$-strongly convex and finite on $\mathbb{R}^n$.

**Theorem 2 (unique minimizer).** $f$ has exactly one minimizer $x^*$.

*Proof.* $h$ is convex and finite, so it has a [subgradient](/subgradient/) $g$ at 0, and $f(y) = h(y) + \frac{\mu}{2} \lVert y \rVert^2 \ge h(0) + g^T y + \frac{\mu}{2} \lVert y \rVert^2$. The right side tends to $+\infty$ as $\lVert y \rVert \to \infty$, so the sublevel set $\{f \le f(0)\}$ is bounded. It is closed, because a finite convex function is continuous. By the Weierstrass theorem, $f$ attains its minimum on it. If $x \ne y$ are two minimizers with value $f^*$, then (a) with $\theta = \frac{1}{2}$ gives $f(\frac{x + y}{2}) \le f^* - \frac{\mu}{8} \lVert x - y \rVert^2 < f^*$, a contradiction. $\square$

**Theorem 3.** Let $f$ also be differentiable, and let $x^*$ be its minimizer, with value $f^*$. For all $x$:

1. *Quadratic growth:* $f(x) - f^* \ge \frac{\mu}{2} \lVert x - x^* \rVert^2$.
2. *Gradient domination:* $\lVert \nabla f(x) \rVert^2 \ge 2 \mu (f(x) - f^*)$.
3. *Distance bound:* $\lVert x - x^* \rVert \le \lVert \nabla f(x) \rVert / \mu$.

*Proof.*

1. Apply (b) at $x^*$, where $\nabla f(x^*) = 0$.
2. By (b), for each $y$, $f(y) \ge f(x) + \nabla f(x)^T (y - x) + \frac{\mu}{2} \lVert y - x \rVert^2$. The right side is a convex quadratic in $y$, minimized at $y = x - \nabla f(x) / \mu$ with value $f(x) - \lVert \nabla f(x) \rVert^2 / (2\mu)$. So $f^* = \min_y f(y) \ge f(x) - \lVert \nabla f(x) \rVert^2 / (2 \mu)$.
3. By (d) with $y = x^*$ and the Cauchy-Schwarz inequality, $\mu \lVert x - x^* \rVert^2 \le \nabla f(x)^T (x - x^*) \le \lVert \nabla f(x) \rVert \lVert x - x^* \rVert$. $\square$

Part 2 is the [Polyak-Łojasiewicz condition](/polyak-lojasiewicz-condition/). With an $L_f$-smooth $f$, the [gradient descent](/gradient-descent/) step $x^+ = x - \nabla f(x) / L_f$ gives $f(x^+) \le f(x) - \lVert \nabla f(x) \rVert^2 / (2 L_f)$, and part 2 turns this into $f(x^+) - f^* \le (1 - \mu / L_f)(f(x) - f^*)$. This is the [linear convergence](/linear-convergence-strongly-convex/) of gradient descent at the rate $1 - 1/\kappa$.

**Duality with smoothness.** A closed proper convex $f$ is $\mu$-strongly convex if and only if its [convex conjugate](/convex-conjugate/) $f^*$ is finite and differentiable everywhere with a $\frac{1}{\mu}$-Lipschitz gradient. This correspondence is proved in Beck, Chapter 5. For $f = \frac{\mu}{2} \lVert x \rVert^2$ the conjugate is $\frac{1}{2\mu} \lVert y \rVert^2$.

## Examples and non-examples

- **A quadratic.** $f(x) = \frac{1}{2} x^T Q x$ with $Q = \begin{pmatrix} 3 & 1 \\ 1 & 2 \end{pmatrix}$ has $\nabla^2 f = Q$. The eigenvalues of $Q$ are $\frac{5 \mp \sqrt{5}}{2}$, so $f$ is $\mu$-strongly convex with $\mu \approx 1.381966$ and $L_f$-smooth with $L_f \approx 3.618034$, and $\kappa = \frac{3 + \sqrt{5}}{2} \approx 2.618034$. The minimizer is $x^* = 0$ with $f^* = 0$. At $x = (1, -2)$: $\nabla f(x) = Qx = (1, -3)$, $f(x) = 3.5$, and $\lVert \nabla f(x) \rVert^2 = 10$. The three bounds of Theorem 3 read $3.5 \ge \frac{\mu}{2} \cdot 5 \approx 3.455$, $3.5 \le 10 / (2\mu) \approx 3.618$, and $\lVert x \rVert = \sqrt{5} \approx 2.236 \le \sqrt{10} / \mu \approx 2.288$. From this point, 20 steps of gradient descent with step $1/L_f$ reduce $f$ by a factor of at most $0.382$ per step, within the bound $1 - 1/\kappa \approx 0.618$.
- **Any positive definite quadratic.** $\frac{1}{2} x^T Q x + c^T x$ with $Q$ [positive definite](/positive-definite-matrix/) is $\lambda_{\min}(Q)$-strongly convex.
- **Ridge regression.** $f(w) = \frac{1}{2} \lVert X w - y \rVert^2 + \frac{\lambda}{2} \lVert w \rVert^2$ has Hessian $X^T X + \lambda I \succeq \lambda I$, so it is $\lambda$-strongly convex for each data matrix $X$. Adding a squared-norm penalty to a convex loss makes it strongly convex, which is one reason for [ridge regression](/ridge-regression/).
- **A nonsmooth example.** $f(x) = \lvert x \rvert + \frac{1}{2} x^2$ is 1-strongly convex, since $f - \frac{1}{2} x^2 = \lvert x \rvert$ is convex. Theorem 2 applies, with minimizer 0.
- **Non-example: $x^4$.** It is strictly convex, but $f''(0) = 0$, so (c) fails for every $\mu > 0$ near 0. Gradient descent on it converges at a sublinear rate near 0. On $[1, \infty)$ it satisfies $f'' \ge 12$.
- **Non-example: $e^x$.** $f''(x) = e^x \to 0$ as $x \to -\infty$, and $f$ has no minimizer, so Theorem 2 fails.
- **Non-example: the logistic loss.** $\log(1 + e^{-x})$ has $f''(x) = \sigma(x)(1 - \sigma(x)) \to 0$ as $\lvert x \rvert \to \infty$, where $\sigma$ is the logistic function. Unregularized [logistic regression](/logistic-regression/) on separable data has no minimizer. With an added $\frac{\lambda}{2} \lVert w \rVert^2$ the objective is $\lambda$-strongly convex.
- **Non-example: $\lvert x \rvert$.** $\lvert x \rvert - \frac{\mu}{2} x^2$ is concave on $(0, \infty)$ and not linear there, so it is not convex for any $\mu > 0$.

## Related definitions

- [Smoothness](/smoothness/) is the upper bound $f(y) \le f(x) + \nabla f(x)^T (y - x) + \frac{L_f}{2} \lVert y - x \rVert^2$. Strong convexity is the matching lower bound.
- The [Polyak-Łojasiewicz condition](/polyak-lojasiewicz-condition/) keeps only part 2 of Theorem 3. It holds for some nonconvex functions and still gives linear convergence.
- Strong convexity with respect to a general norm replaces $\lVert \cdot \rVert$ in (a) or (b). The negative entropy is 1-strongly convex with respect to $\lVert \cdot \rVert_1$ on the probability simplex, and [mirror descent](/mirror-descent/) uses this through the [Bregman divergence](/bregman-divergence/).
- A function is *strictly convex* if the inequality of convexity is strict for $x \ne y$ and $\theta \in (0, 1)$. This is weaker than strong convexity.

## References
