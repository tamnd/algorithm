---
tag: 7TFCV8
kind: definition
slug: subgradient
name: Subgradient
aliases:
- subgradient vector
area: optimization/convex-optimization
level: core
summary: A vector g with f(y) ≥ f(x) + g·(y − x) for all y, so that the affine function through (x, f(x)) with slope g lies below f.
prereqs: [convex-function]
see_also: [subdifferential, supporting-hyperplane-theorem, epigraph, gradient, proximal-operator, bundle-method, cutting-plane-method, polyak-step-size]
sources:
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970 (Princeton Landmarks in Mathematics edition, 1997)
    locator: Section 23, The subdifferential of a convex function (definition, existence at interior points, relation to the gradient)
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 3, Subgradients, and Chapter 8, Primal and dual projected subgradient methods
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, 2nd edition, Springer, 2018
    locator: Chapter 3, Nonsmooth convex optimization (subgradients, the subgradient method and its lower complexity bounds)
  - paper: doi:10.1561/2200000050
    title: "Sébastien Bubeck, Convex Optimization: Algorithms and Complexity, Foundations and Trends in Machine Learning 8(3-4), 2015"
    locator: Section 3.1, Projected subgradient descent for Lipschitz functions
---

A subgradient of a [convex function](/convex-function/) $f$ at a point $x$ is a vector $g$ such that the affine function $f(x) + g^T (y - x)$ lies below $f$ everywhere. It replaces the [gradient](/gradient/) at points where $f$ has a kink, such as $|x|$ at 0. Subgradients exist at each interior point of the domain, by the [supporting hyperplane theorem](/supporting-hyperplane-theorem/), and the set of all of them is the [subdifferential](/subdifferential/). They are the information that nonsmooth methods such as the subgradient method, the [bundle method](/bundle-method/) and the [cutting-plane method](/cutting-plane-method/) use.

## Definition

Let $f : \mathbb{R}^n \to \mathbb{R} \cup \{+\infty\}$ and $x \in \operatorname{dom} f$. A vector $g \in \mathbb{R}^n$ is a *subgradient* of $f$ at $x$ if

$$f(y) \ge f(x) + g^T (y - x) \quad \text{for all } y \in \mathbb{R}^n.$$

This is the *subgradient inequality*. In terms of the [epigraph](/epigraph/), $g$ is a subgradient at $x$ exactly when the vector $(g, -1)$ defines a non-vertical supporting hyperplane of $\operatorname{epi} f$ at $(x, f(x))$: $(g, -1)^T (y, t) \le (g, -1)^T (x, f(x))$ for all $(y, t) \in \operatorname{epi} f$. The function $f$ is *subdifferentiable* at $x$ if it has at least one subgradient there. The set of all subgradients at $x$ is the subdifferential $\partial f(x)$.

The definition makes sense for any $f$, but it is useful for convex $f$. If $f$ has a subgradient at each point of a convex set, then $f$ is convex on that set, since it is the pointwise maximum of affine functions there.

### Existence

**Theorem 1.** If $f$ is convex and $x \in \operatorname{int} \operatorname{dom} f$, then $\partial f(x)$ is nonempty.

*Proof.* This is the first consequence on the [supporting hyperplane theorem](/supporting-hyperplane-theorem/) page: a supporting hyperplane of $\operatorname{epi} f$ at $(x, f(x))$ exists, and it is not vertical because $x$ is interior to $\operatorname{dom} f$. $\square$

### Relation to the gradient

**Theorem 2.** Let $f$ be convex and differentiable at $x \in \operatorname{int} \operatorname{dom} f$. Then $\partial f(x) = \{\nabla f(x)\}$.

*Proof.* The first-order condition on the [convex function](/convex-function/) page gives $f(y) \ge f(x) + \nabla f(x)^T (y - x)$, so $\nabla f(x) \in \partial f(x)$. Let $g \in \partial f(x)$ and $d \in \mathbb{R}^n$. For $t > 0$, $f(x + t d) - f(x) \ge t\, g^T d$. Divide by $t$ and let $t \to 0^+$: $\nabla f(x)^T d \ge g^T d$. Take $d = g - \nabla f(x)$: $0 \ge \lVert g - \nabla f(x) \rVert^2$, so $g = \nabla f(x)$. $\square$

### Optimality

**Theorem 3 (Fermat's rule).** For any $f$, a point $x^*$ is a global minimum of $f$ if and only if $0 \in \partial f(x^*)$.

*Proof.* With $g = 0$, the subgradient inequality reads $f(y) \ge f(x^*)$ for all $y$. $\square$

The proof is one line, but it has two consequences. First, for convex $f$ it is the nonsmooth form of the condition $\nabla f(x^*) = 0$. Second, a constrained problem $\min_{x \in C} f(x)$ becomes $\min f + I_C$ with the indicator $I_C$ of $C$, and the rule then gives the optimality conditions in terms of the normal cone of $C$, as on the [subdifferential](/subdifferential/) page.

### The subgradient method

The subgradient method for $\min f$ steps $x_{k+1} = x_k - t_k g_k$ with $g_k \in \partial f(x_k)$. A subgradient step need not decrease $f$ (see the examples), so the method keeps the best value $f_{\text{best}, K} = \min_{k < K} f(x_k)$.

**Theorem 4.** Let $f$ be convex on $\mathbb{R}^n$ with a minimizer $x^*$. Assume $\lVert g_k \rVert \le G$ for all $k$ and $\lVert x_0 - x^* \rVert \le R$. With the constant step $t = R / (G \sqrt{K})$,

$$f_{\text{best}, K} - f(x^*) \le \frac{R G}{\sqrt{K}}.$$

*Proof.* By the subgradient inequality at $x_k$ with $y = x^*$, $g_k^T (x_k - x^*) \ge f(x_k) - f(x^*)$. So

$$\lVert x_{k+1} - x^* \rVert^2 = \lVert x_k - x^* \rVert^2 - 2 t\, g_k^T (x_k - x^*) + t^2 \lVert g_k \rVert^2 \le \lVert x_k - x^* \rVert^2 - 2 t \,(f(x_k) - f(x^*)) + t^2 G^2.$$

Sum over $k = 0, \dots, K - 1$ and drop $\lVert x_K - x^* \rVert^2 \ge 0$: $2 t \sum_k (f(x_k) - f(x^*)) \le R^2 + K t^2 G^2$. The minimum is at most the mean, so $f_{\text{best}, K} - f(x^*) \le \frac{R^2 + K t^2 G^2}{2 K t}$. With $t = R / (G\sqrt{K})$ the right side is $\frac{2R^2}{2 R \sqrt{K} / G} = \frac{RG}{\sqrt{K}}$. $\square$

To reach accuracy $\varepsilon$ the method needs $K = R^2 G^2 / \varepsilon^2$ steps. This is the best possible order for methods that see only values and subgradients, when $K \le n$: see the [first-order lower bound](/first-order-lower-bound/). The [Polyak step size](/polyak-step-size/) gives the same bound without knowing $R$ and $K$ in advance, if $f(x^*)$ is known.

## Examples and non-examples

| Function | Point | Subgradients |
|---|---|---|
| $\lvert x \rvert$ on $\mathbb{R}$ | $x = 0$ | each $g \in [-1, 1]$ |
| $\lvert x \rvert$ | $x \ne 0$ | only $\operatorname{sign}(x)$ |
| $\lVert x \rVert_2$ on $\mathbb{R}^n$ | $x = 0$ | each $g$ with $\lVert g \rVert_2 \le 1$ |
| $\max(x_1, x_2)$ | $x_1 = x_2$ | each $(\theta, 1 - \theta)$ with $\theta \in [0, 1]$ |
| $x^2$ | any $x$ | only $2x$ |
| $\max_i (a_i^T x + b_i)$ | any $x$ | each convex combination of the $a_i$ with $a_i^T x + b_i$ maximal |

- **A subgradient step is not a descent step.** Let $f(x) = \lvert x_1 \rvert + 2 \lvert x_2 \rvert$ and $x = (1, 0)$, so $f(x) = 1$. The vector $g = (1, 2)$ is a subgradient, since $f(y) \ge \lvert y_1 \rvert + 2 y_2 \ge y_1 + 2 y_2 = 1 + g^T (y - x)$. The step $x - t g = (1 - t, -2t)$ gives $f = (1 - t) + 4t = 1 + 3t$ for $t \in (0, 1]$: $f = 1.3$ at $t = 0.1$ and $f = 2.5$ at $t = 0.5$. The subgradient $(1, 0)$ at the same point does give descent. The distance to the minimizer 0 still decreases for small $t$: it goes from $1$ to $\sqrt{(1-t)^2 + 4t^2}$, which is less than 1 for $t < 0.4$. Theorem 4 rests on this distance decrease, not on a decrease of $f$.
- **The method on this function.** From $x_0 = (1, 1)$ we have $R = \sqrt{2}$, and each subgradient has norm at most $G = \sqrt{5}$. With $K = 100$ and $t = R / (G \sqrt{K}) \approx 0.0632$, the best value after 100 steps is about $0.0358$, below the bound $RG/\sqrt{K} = \sqrt{10}/10 \approx 0.316$. With $K = 10000$ the best value is about $0.0070$ and the bound is $0.0316$.
- **Non-example: a concave kink.** $f(x) = -\lvert x \rvert$ has no subgradient at 0: the inequality $-\lvert y \rvert \ge g y$ fails for $y$ of the sign of $g$, or for any $y \ne 0$ if $g = 0$.
- **Non-example: a vertical tangent at the boundary.** $f(x) = -\sqrt{x}$ for $x \ge 0$ and $+\infty$ for $x < 0$ is convex, but it has no subgradient at 0. The inequality $-\sqrt{y} \ge g y$ fails for small $y > 0$ for every $g$. So Theorem 1 needs $x$ in the interior of the domain.
- **Non-example: a nonconvex function with a gradient.** $f(x) = x^3$ has $f'(1) = 3$, but $3$ is not a subgradient at 1: at $y = -3$ the line $1 + 3(y - 1)$ has the value $-11$, which is above $y^3 = -27$. No other $g$ works either, since a subgradient of a function differentiable at 1 must equal $f'(1)$, by the argument of Theorem 2.

## Related definitions

- The [subdifferential](/subdifferential/) $\partial f(x)$ is the set of all subgradients. It is closed and convex, and it has its own calculus rules.
- An *$\varepsilon$-subgradient* satisfies $f(y) \ge f(x) + g^T (y - x) - \varepsilon$ for all $y$. [Bundle methods](/bundle-method/) use it.
- The [proximal operator](/proximal-operator/) is characterized by $x - \operatorname{prox}_f(x) \in \partial f(\operatorname{prox}_f(x))$. It turns a subgradient condition into a well-defined step.
- For the [convex conjugate](/convex-conjugate/) of a closed convex $f$, $g \in \partial f(x)$ if and only if $x \in \partial f^*(g)$, and then $f(x) + f^*(g) = g^T x$.
- For nonconvex locally Lipschitz functions, the Clarke generalized gradient plays the role of the subdifferential.

## References
