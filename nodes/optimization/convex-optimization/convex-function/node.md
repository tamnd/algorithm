---
tag: SBRWJ2
kind: definition
slug: convex-function
name: Convex function
aliases:
- convexity of functions
- convex map
area: optimization/convex-optimization
level: intro
summary: A function whose chord between any two points lies on or above its graph, so that its epigraph is a convex set.
prereqs: [convex-set, gradient]
see_also: [epigraph, strong-convexity, quasiconvex-function, subgradient, convex-conjugate, jensens-inequality, convex-optimization-problem, positive-definite-matrix]
sources:
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 3.1 (definition, extended-value extension, first-order and second-order conditions, examples, epigraph) and Section 3.2 (operations that preserve convexity)
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970 (Princeton Landmarks in Mathematics edition, 1997)
    locator: Section 4, Convex functions (the epigraph definition with values in the extended reals, and the second-derivative tests)
  - book: isbn:9783540422051
    title: Jean-Baptiste Hiriart-Urruty and Claude Lemaréchal, Fundamentals of Convex Analysis, Springer, 2001
    locator: Chapter B, Convex functions (Section B.1 definitions and examples, Section B.2 functional operations, Section B.4 first-order and second-order differentiation)
---

A convex function is a function $f$ such that the chord between any two points of its graph lies on or above the graph. Equivalently, its [epigraph](/epigraph/), the set of points on or above the graph, is a [convex set](/convex-set/). Convex functions are the objectives of a [convex optimization problem](/convex-optimization-problem/), where each local minimum is a global minimum. This is the main reason why convexity separates the optimization problems that are solved reliably from the ones that are not.

## Definition

We write $n$ for the number of variables and use the extended real line $\overline{\mathbb{R}} = \mathbb{R} \cup \{+\infty\}$. For $f : \mathbb{R}^n \to \overline{\mathbb{R}}$, the *effective domain* is $\operatorname{dom} f = \{x : f(x) < +\infty\}$.

**Definition.** The function $f : \mathbb{R}^n \to \overline{\mathbb{R}}$ is *convex* if $\operatorname{dom} f$ is a convex set and for all $x, y \in \operatorname{dom} f$ and all $\theta \in [0, 1]$,

$$f(\theta x + (1 - \theta) y) \le \theta f(x) + (1 - \theta) f(y).$$

A function defined only on a convex set $D \subseteq \mathbb{R}^n$ is convex if it meets the same inequality on $D$. Set $f = +\infty$ outside $D$ to get the extended-value form, and the two definitions agree. With the rule $\theta \cdot (+\infty) = +\infty$ for $\theta > 0$, the inequality then holds for all $x, y \in \mathbb{R}^n$ and all $\theta \in (0, 1)$.

- $f$ is *strictly convex* if the inequality is strict for all $x \ne y$ in $\operatorname{dom} f$ and all $\theta \in (0, 1)$.
- $f$ is *concave* if $-f$ is convex. An affine function $a^T x + b$ is both convex and concave.
- $f$ is *proper* if $\operatorname{dom} f \neq \emptyset$ and $f$ never takes the value $-\infty$. All functions on this page are proper.

### The epigraph test

The epigraph is $\operatorname{epi} f = \{(x, t) \in \mathbb{R}^n \times \mathbb{R} : f(x) \le t\}$. The function $f$ is convex if and only if $\operatorname{epi} f$ is a convex set. The proof is on the [epigraph](/epigraph/) page. This form explains why the pointwise maximum of convex functions is convex: its epigraph is the intersection of their epigraphs.

### The first-order test

**Theorem.** Let $\operatorname{dom} f$ be open and convex, and let $f$ be differentiable on it. Then $f$ is convex if and only if

$$f(y) \ge f(x) + \nabla f(x)^T (y - x) \quad \text{for all } x, y \in \operatorname{dom} f.$$

*Proof.* Assume that $f$ is convex. For $t \in (0, 1]$, the definition with $\theta = 1 - t$ gives $f(x + t(y - x)) \le f(x) + t (f(y) - f(x))$. So $\frac{f(x + t(y - x)) - f(x)}{t} \le f(y) - f(x)$. As $t \to 0^+$, the left side tends to the directional derivative $\nabla f(x)^T (y - x)$, which gives the inequality.

Conversely, assume the inequality. Fix $x, y$ and $\theta$, and let $z = \theta x + (1 - \theta) y$, which is in $\operatorname{dom} f$. The inequality at $z$ gives $f(x) \ge f(z) + \nabla f(z)^T (x - z)$ and $f(y) \ge f(z) + \nabla f(z)^T (y - z)$. Multiply the first by $\theta$ and the second by $1 - \theta$, and add. Since $\theta (x - z) + (1 - \theta)(y - z) = 0$, the result is $\theta f(x) + (1 - \theta) f(y) \ge f(z)$. $\square$

The tangent plane at each point is a global under-estimator. So if $\nabla f(x) = 0$, then $f(y) \ge f(x)$ for all $y$, and $x$ is a global minimum.

### The second-order test

**Theorem.** Let $\operatorname{dom} f$ be open and convex, and let $f$ be twice differentiable on it. Then $f$ is convex if and only if the Hessian $\nabla^2 f(x)$ is positive semidefinite for each $x \in \operatorname{dom} f$.

*Proof.* The definition only involves segments, so $f$ is convex if and only if each restriction $\varphi(t) = f(x + t v)$ to a line is convex on the open interval where it is finite. Here $\varphi''(t) = v^T \nabla^2 f(x + t v) v$. So it is enough to show that a twice differentiable $\varphi$ on an open interval is convex if and only if $\varphi'' \ge 0$.

If $\varphi'' \ge 0$, then $\varphi'$ is nondecreasing. Take $t, s$ in the interval. By the mean value theorem, $\varphi(s) - \varphi(t) = \varphi'(r)(s - t)$ for some $r$ between $t$ and $s$. If $s > t$, then $\varphi'(r) \ge \varphi'(t)$. If $s < t$, then $\varphi'(r) \le \varphi'(t)$ and $s - t < 0$. In both cases $\varphi(s) \ge \varphi(t) + \varphi'(t)(s - t)$, and the first-order test gives convexity.

If $\varphi$ is convex, the first-order test at $t$ and at $s$ gives $\varphi(s) \ge \varphi(t) + \varphi'(t)(s - t)$ and $\varphi(t) \ge \varphi(s) + \varphi'(s)(t - s)$. The sum is $(\varphi'(s) - \varphi'(t))(s - t) \ge 0$. So $\varphi'$ is nondecreasing and $\varphi'' \ge 0$. $\square$

A positive definite Hessian at each point implies strict convexity, but the converse is false: $x^4$ is strictly convex and its second derivative is 0 at 0.

### Local minima are global

**Theorem.** Let $f$ be convex and let $x$ be a local minimum of $f$. Then $x$ is a global minimum.

*Proof.* Assume that $f(y) < f(x)$ for some $y$. For $t \in (0, 1]$, the point $x + t(y - x)$ has $f(x + t (y - x)) \le (1 - t) f(x) + t f(y) < f(x)$. These points are as close to $x$ as we like when $t$ is small, so $x$ is not a local minimum. $\square$

A strictly convex function has at most one minimum: if $x \ne y$ were both minima with value $f^*$, the midpoint would have value less than $f^*$.

## Examples and non-examples

**Convex functions of one variable** (each by the second-order test on its domain):

| function | domain | second derivative |
|---|---|---|
| $ax + b$ | $\mathbb{R}$ | $0$ |
| $x^2$, $x^4$ | $\mathbb{R}$ | $2$, $12 x^2$ |
| $e^{ax}$ | $\mathbb{R}$ | $a^2 e^{ax}$ |
| $-\log x$ | $x > 0$ | $1/x^2$ |
| $x \log x$ | $x > 0$ | $1/x$ |
| $x^p$ with $p \ge 1$ | $x \ge 0$ | $p(p-1)x^{p-2}$ |
| $\lvert x \rvert$ | $\mathbb{R}$ | not differentiable at 0, convex by the triangle inequality |

**Convex functions of several variables.**

- Each norm $\lVert x \rVert$. The triangle inequality and homogeneity give $\lVert \theta x + (1-\theta) y \rVert \le \theta \lVert x \rVert + (1 - \theta) \lVert y \rVert$.
- The quadratic $f(x) = \frac{1}{2} x^T Q x + c^T x$ with $Q$ symmetric and positive semidefinite, because $\nabla^2 f = Q$. With $Q = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$, whose eigenvalues are 1 and 3, $f$ is convex. With $Q = \begin{pmatrix} 1 & 2 \\ 2 & 1 \end{pmatrix}$, whose eigenvalues are $-1$ and 3, it is not.
- The maximum of affine functions $\max_i (a_i^T x + b_i)$, as a pointwise maximum.
- Log-sum-exp $\log \sum_{i=1}^n e^{x_i}$. Its Hessian is $\operatorname{diag}(p) - p p^T$ with $p_i = e^{x_i} / \sum_j e^{x_j}$, and $v^T(\operatorname{diag}(p) - p p^T) v = \sum_i p_i v_i^2 - (\sum_i p_i v_i)^2 \ge 0$ by the Cauchy-Schwarz inequality.
- The largest eigenvalue $\lambda_{\max}(X) = \max_{\lVert v \rVert = 1} v^T X v$ of a symmetric matrix, as a maximum of linear functions of $X$.

**Non-examples.**

- $f(x_1, x_2) = x_1 x_2$. Take $x = (1, 0)$ and $y = (0, 1)$. Then $f(x) = f(y) = 0$, but at the midpoint $f(\frac12, \frac12) = \frac14 > 0$. The Hessian $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ has eigenvalues $\pm 1$.
- $x^3$ on $\mathbb{R}$: the second derivative $6x$ is negative for $x < 0$. On $[0, \infty)$ it is convex, so the domain matters.
- $\sqrt{\lvert x \rvert}$: $f(0) = 0$, $f(\pm 1) = 1$ and $f(\frac12) \approx 0.707 > \frac12 = \frac12 f(0) + \frac12 f(1)$.
- The function that is 0 at 0 and 1 elsewhere is not convex: with $x = 0$ and $y = 2$, the midpoint value is $f(1) = 1$, but the chord value is $\frac12 (0 + 1) = \frac12$.
- A function with a convex domain and convex sublevel sets need not be convex. The function $\log x$ on $x > 0$ has convex sublevel sets but it is concave. Such functions are [quasiconvex](/quasiconvex-function/).

**Operations that keep convexity.** Let $f, f_1, f_2$ be convex.

1. *Nonnegative sums:* $\alpha_1 f_1 + \alpha_2 f_2$ with $\alpha_1, \alpha_2 \ge 0$. Add the two defining inequalities.
2. *Affine change of variable:* $g(x) = f(Ax + b)$. The map $x \mapsto Ax + b$ sends $\theta x + (1-\theta) y$ to $\theta(Ax + b) + (1 - \theta)(Ay + b)$.
3. *Pointwise supremum:* $g(x) = \sup_{\alpha} f_\alpha(x)$ for any family of convex $f_\alpha$, because $\operatorname{epi} g = \bigcap_\alpha \operatorname{epi} f_\alpha$.
4. *Composition:* $g(x) = h(f(x))$ with $h : \mathbb{R} \to \mathbb{R}$ convex and nondecreasing. Then $h(f(\theta x + (1-\theta)y)) \le h(\theta f(x) + (1-\theta) f(y)) \le \theta h(f(x)) + (1 - \theta) h(f(y))$. The first step needs the monotonicity of $h$. Without it, the rule fails: $h(u) = -u$ with $f(x) = x^2$ gives $-x^2$.
5. *Partial minimization:* if $F(x, y)$ is jointly convex, then $g(x) = \inf_y F(x, y)$ is convex when it is never $-\infty$. For example, the distance $\operatorname{dist}(x, C) = \inf_{y \in C} \lVert x - y \rVert$ to a convex set $C$ is convex.

A product or a minimum of convex functions is in general not convex: $x$ and $x^2$ are convex but their product $x^3$ is not, and $\min(x^2, (x-2)^2)$ has the value 1 at $x = 1$, which is above the chord value 0 between $x = 0$ and $x = 2$.

## Related definitions

- [Convex set](/convex-set/): a set that contains the segment between any two of its points. The sublevel sets $\{x : f(x) \le \alpha\}$ of a convex function are convex sets.
- [Epigraph](/epigraph/): the set on or above the graph. It turns statements about convex functions into statements about convex sets.
- [Strong convexity](/strong-convexity/): $f - \frac{\mu}{2} \lVert x \rVert^2$ is convex for some $\mu > 0$. It gives a unique minimum and linear rates for [gradient descent](/gradient-descent/).
- [Quasiconvex function](/quasiconvex-function/): only the sublevel sets must be convex.
- [Subgradient](/subgradient/): a slope $g$ with $f(y) \ge f(x) + g^T (y - x)$ for all $y$. It replaces the gradient in the first-order test when $f$ is not differentiable.
- [Convex conjugate](/convex-conjugate/) and [convex envelope](/convex-envelope/): the dual description of $f$ by its affine minorants, and the largest convex function below a given function.
- [Jensen's inequality](/jensens-inequality/): $f(\mathbb{E}[X]) \le \mathbb{E}[f(X)]$, the definition extended to any probability distribution.
- [Smoothness](/smoothness/): a Lipschitz bound on the gradient, the upper counterpart of strong convexity.

## References
