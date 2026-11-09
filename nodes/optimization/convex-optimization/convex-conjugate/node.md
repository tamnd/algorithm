---
tag: VCH05B
kind: definition
slug: convex-conjugate
name: Convex conjugate
aliases:
- Fenchel conjugate
- Legendre-Fenchel transform
- conjugate function
area: optimization/convex-optimization
level: advanced
summary: The function f*(y) = sup_x (y·x − f(x)). It is always convex and closed, and f** = f exactly when f is closed and convex.
prereqs: [convex-function, subgradient]
see_also: [fenchel-duality, convex-envelope, support-function, convex-hull-trick, strong-convexity, smoothness, lagrangian-duality, proximal-operator]
sources:
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970 (Princeton Landmarks in Mathematics edition, 1997)
    locator: Section 12, Conjugates of convex functions (the conjugacy correspondence and the Fenchel inequality)
  - book: isbn:9783540422051
    title: Jean-Baptiste Hiriart-Urruty and Claude Lemaréchal, Fundamentals of Convex Analysis, Springer, 2001
    locator: Chapter E, Conjugacy in convex analysis (calculus rules, the biconjugate, examples)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 3.3, The conjugate function (examples and basic properties)
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 4, Conjugate functions
  - paper: "Yves Lucet, Faster than the fast Legendre transform, the linear-time Legendre transform, Numerical Algorithms 16, 1997, 171-185"
    locator: computing the discrete Legendre transform in linear time with a convex hull and a merge
---

The convex conjugate of a function $f$ is the function $f^*(y) = \sup_x (y^T x - f(x))$. For each slope $y$, the number $-f^*(y)$ is the largest intercept of an affine function with slope $y$ that lies below $f$. So $f^*$ encodes $f$ by its affine minorants, and the double conjugate $f^{**}$ is the largest closed [convex function](/convex-function/) below $f$. Conjugates turn sums into infimal convolutions, give closed forms for Lagrange dual functions, and are the main tool of [Fenchel duality](/fenchel-duality/).

## Definition

Let $f : \mathbb{R}^n \to \mathbb{R} \cup \{+\infty\}$ be *proper*: $\operatorname{dom} f$ is nonempty. Its *conjugate* is

$$f^*(y) = \sup_{x \in \operatorname{dom} f} \left( y^T x - f(x) \right), \qquad y \in \mathbb{R}^n,$$

with values in $\mathbb{R} \cup \{+\infty\}$. The *biconjugate* is $f^{**} = (f^*)^*$. In one variable with $f$ differentiable and strictly convex, the supremum is attained where $f'(x) = y$, and $f^*$ is the classical Legendre transform $f^*(y) = y\, x(y) - f(x(y))$.

**Theorem 1.** $f^*$ is convex and closed (lower semicontinuous).

*Proof.* For each $x \in \operatorname{dom} f$, the map $y \mapsto y^T x - f(x)$ is affine. The [epigraph](/epigraph/) of a pointwise supremum is the intersection of the epigraphs, and the epigraph of an affine function is a closed half-space. An intersection of closed convex sets is closed and convex. $\square$

**Theorem 2 (Fenchel-Young inequality).** For all $x$ and $y$,

$$f(x) + f^*(y) \ge y^T x,$$

with equality if and only if $y \in \partial f(x)$.

*Proof.* The inequality is the definition of $f^*(y)$ as a supremum, at the point $x$. Equality holds if and only if $x$ attains the supremum, that is, $y^T x - f(x) \ge y^T z - f(z)$ for all $z$. Rearranged, this is $f(z) \ge f(x) + y^T (z - x)$ for all $z$, which is the [subgradient](/subgradient/) inequality. $\square$

**Theorem 3.** $f^{**} \le f$.

*Proof.* By Theorem 2, $y^T x - f^*(y) \le f(x)$ for all $y$. Take the supremum over $y$. $\square$

**Theorem 4 (Fenchel-Moreau).** Let $f$ be proper. Then $f^{**} = f$ if and only if $f$ is convex and closed.

*Proof.* If $f^{**} = f$, then $f$ is a conjugate, so it is convex and closed by Theorem 1.

Conversely, let $f$ be convex and closed, so $\operatorname{epi} f$ is a nonempty closed convex set. We use strict separation of a point from a closed convex set (Lemma 2 on the [separating hyperplane theorem](/separating-hyperplane-theorem/) page). For a point $(x_0, r) \notin \operatorname{epi} f$, it gives $(y, -\beta) \in \mathbb{R}^n \times \mathbb{R}$ and $c$ with

$$y^T x - \beta t \le c < y^T x_0 - \beta r \quad \text{for all } (x, t) \in \operatorname{epi} f. \tag{1}$$

Since $t$ can increase without bound, $\beta \ge 0$.

*Step 1: $f^*$ is proper.* Take $x_1 \in \operatorname{dom} f$ and the point $(x_1, f(x_1) - 1) \notin \operatorname{epi} f$. If $\beta = 0$ in (1), then $y^T x_1 \le c < y^T x_1$, which is impossible. So $\beta > 0$. Dividing by $\beta$ gives $y_0$ with $y_0^T x - f(x) \le c / \beta$ for all $x \in \operatorname{dom} f$, so $f^*(y_0) < \infty$.

*Step 2: $f^{**} \ge f$.* Suppose $f^{**}(x_0) < r < f(x_0)$ for some $x_0$ and $r$. Then $(x_0, r) \notin \operatorname{epi} f$; take (1) for this point.

- If $\beta > 0$, scale to $\beta = 1$. Then $y^T x - f(x) \le c$ on $\operatorname{dom} f$, so $f^*(y) \le c < y^T x_0 - r$, and $f^{**}(x_0) \ge y^T x_0 - f^*(y) > r$, a contradiction.
- If $\beta = 0$, then $y^T x \le c < y^T x_0$ for all $x \in \operatorname{dom} f$. With $y_0$ from Step 1 and $\mu > 0$, for $x \in \operatorname{dom} f$: $(y_0 + \mu y)^T x - f(x) \le f^*(y_0) + \mu c$. So $f^*(y_0 + \mu y) \le f^*(y_0) + \mu c$, and $f^{**}(x_0) \ge (y_0 + \mu y)^T x_0 - f^*(y_0) - \mu c = y_0^T x_0 - f^*(y_0) + \mu (y^T x_0 - c)$. This tends to $+\infty$ as $\mu \to \infty$, which contradicts $f^{**}(x_0) < r$.

So $f^{**} \ge f$, and with Theorem 3, $f^{**} = f$. $\square$

For any proper $f$ that has an affine minorant, the same argument applied to the closed convex hull of $f$ shows that $f^{**}$ is the largest closed convex function below $f$, the closed [convex envelope](/convex-envelope/).

### Calculus rules

Each rule follows by a change of variables in the supremum.

| Function | Conjugate |
|---|---|
| $\alpha f(x)$, $\alpha > 0$ | $\alpha f^*(y / \alpha)$ |
| $f(x - a)$ | $f^*(y) + a^T y$ |
| $f(x) + a^T x + b$ | $f^*(y - a) - b$ |
| $f(Ax)$, $A$ invertible | $f^*(A^{-T} y)$ |
| $f_1(x_1) + f_2(x_2)$ (separable) | $f_1^*(y_1) + f_2^*(y_2)$ |
| infimal convolution $\inf_z (f_1(z) + f_2(x - z))$ | $f_1^* + f_2^*$ |

### Computing the conjugate of a sampled function

In one variable, given samples $(x_i, f_i)$ for $i = 1, \dots, n$ and slopes $s_1, \dots, s_k$, the *discrete Legendre transform* is $f^*(s_j) = \max_i (s_j x_i - f_i)$. Brute force costs $O(nk)$. The implementation in `impl/python/convex_conjugate.py` follows Lucet's method:

1. Sort the samples by $x$ and compute their lower convex hull with a monotone chain. A sample above the hull never attains the maximum, because a hull vertex beats it for every slope.
2. Sort the slopes. Walk along the hull with one pointer: for slope $s$, advance while the next hull edge has a slope below $s$. The vertex reached maximizes $s x - f$, since $s x - f$ increases along an edge exactly when the edge slope is below $s$, and the edge slopes increase along the hull.
3. Output $s x - f$ at that vertex for each slope.

After sorting, both passes are linear, so the cost is $O(n \log n + k \log k)$, and $O(n + k)$ for sorted input. With rational inputs the arithmetic is exact. The tests compare the result with the brute-force maximum on random rational inputs, and check the Fenchel-Young inequality and $f^{**} \le f$, with equality at the hull vertices. The same queries, a maximum of linear functions at many points, are the [convex hull trick](/convex-hull-trick/).

## Examples and non-examples

| $f(x)$ | $\operatorname{dom} f$ | $f^*(y)$ |
|---|---|---|
| $\frac{1}{2} x^2$ | $\mathbb{R}$ | $\frac{1}{2} y^2$ |
| $\frac{1}{2} x^T Q x$, $Q \succ 0$ | $\mathbb{R}^n$ | $\frac{1}{2} y^T Q^{-1} y$ |
| $e^x$ | $\mathbb{R}$ | $y \log y - y$ for $y > 0$, $0$ at $y = 0$, $+\infty$ for $y < 0$ |
| $-\log x$ | $x > 0$ | $-1 - \log(-y)$ for $y < 0$, $+\infty$ otherwise |
| $x \log x$ | $x \ge 0$ | $e^{y - 1}$ |
| $\lvert x \rvert$ | $\mathbb{R}$ | $0$ on $[-1, 1]$, $+\infty$ outside |
| $\max(0, x)$ | $\mathbb{R}$ | $0$ on $[0, 1]$, $+\infty$ outside |
| a norm $\lVert x \rVert$ | $\mathbb{R}^n$ | indicator of the dual unit ball $\{\lVert y \rVert_* \le 1\}$ |
| indicator $I_C$ of a set $C$ | $C$ | [support function](/support-function/) $\sigma_C(y) = \sup_{x \in C} y^T x$ |
| $a^T x + b$ | $\mathbb{R}^n$ | $-b$ at $y = a$, $+\infty$ otherwise |

- **A worked case.** For $f(x) = \frac{1}{2} x^2$, the supremum of $yx - \frac{1}{2} x^2$ is at $x = y$, with value $\frac{1}{2} y^2$. So $f^* = f$, and $\frac{1}{2} \lVert x \rVert^2$ is the only function on $\mathbb{R}^n$ equal to its own conjugate.
- **The discrete transform of a sampled square.** Sample $f(x) = x^2$ at $x = -2, -1, 0, 1, 2$. The exact conjugate is $f^*(s) = s^2 / 4$. The discrete one is never larger, because it maximizes over fewer points:

  | $s$ | $-3$ | $-1$ | $0$ | $1/2$ | $1$ | $3$ | $4$ | $5$ |
  |---|---|---|---|---|---|---|---|---|
  | discrete | $2$ | $0$ | $0$ | $0$ | $0$ | $2$ | $4$ | $6$ |
  | $s^2/4$ | $9/4$ | $1/4$ | $0$ | $1/16$ | $1/4$ | $9/4$ | $4$ | $25/4$ |

  They agree at $s = 0$ and $s = 4$, where the exact maximizer $x = s/2$ is a sample. For $\lvert s \rvert > 4$ the discrete conjugate grows linearly, as the conjugate of a function that is $+\infty$ outside $[-2, 2]$ must.
- **A nonconvex function.** For the double well $f(x) = \min((x - 1)^2, (x + 1)^2)$, $f^*(y) = \frac{y^2}{4} + \lvert y \rvert$, and $f^{**}$ is 0 on $[-1, 1]$ and equals $f$ outside. So $f^{**} \ne f$, as Theorem 4 predicts for a nonconvex $f$. See the [convex envelope](/convex-envelope/) page.
- **A convex function that is not closed.** Let $f = 0$ on $(0, 1]$ and $f(0) = 1$, with $+\infty$ elsewhere. It is convex but not lower semicontinuous at 0. Here $f^*(y) = \max(y, 0)$, and $f^{**}$ is the indicator of $[0, 1]$, which differs from $f$ at 0.
- **Smoothness and strong convexity.** A closed convex $f$ is [$\mu$-strongly convex](/strong-convexity/) if and only if $f^*$ is differentiable with a $\frac{1}{\mu}$-Lipschitz gradient. In the table, $\frac{1}{2} x^T Q x$ is $\lambda_{\min}(Q)$-strongly convex, and its conjugate has gradient $Q^{-1} y$ with Lipschitz constant $1 / \lambda_{\min}(Q)$.

## Related definitions

- The [convex envelope](/convex-envelope/) of $f$ is its largest convex minorant. Its closure is $f^{**}$.
- The [support function](/support-function/) of a set is the conjugate of its indicator.
- [Fenchel duality](/fenchel-duality/) pairs $\inf_x (f(x) + g(Ax))$ with $\sup_y (-f^*(A^T y) - g^*(-y))$.
- The Lagrange dual function of a problem with linear constraints is $g(\lambda, \nu) = -b^T \lambda - d^T \nu - f_0^*(-A^T \lambda - C^T \nu)$; see [Lagrangian duality](/lagrangian-duality/).
- *Moreau's decomposition* says $x = \operatorname{prox}_f(x) + \operatorname{prox}_{f^*}(x)$ for closed convex $f$, linking the conjugate to the [proximal operator](/proximal-operator/).

## References
