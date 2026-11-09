---
tag: WRH959
kind: definition
slug: proximal-operator
name: Proximal operator
aliases:
- prox operator
- proximal mapping
area: optimization/gradient-methods
level: advanced
summary: Prox_h(x) = argmin_u { h(u) + (1/2)||u - x||^2 }, a generalized projection for nonsmooth terms.
prereqs: [convex-function, subdifferential]
see_also: [proximal-gradient-method, fista, composite-minimization, projected-gradient-descent, proximal-point-method, admm, convex-conjugate, lasso-regression]
sources:
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 6, The proximal operator (existence and uniqueness, the calculus of prox, the second prox theorem, Moreau decomposition)
  - paper: doi:10.1561/2400000003
    title: Neal Parikh and Stephen Boyd, Proximal algorithms, Foundations and Trends in Optimization 1(3), 2014
    locator: Chapter 2 (properties) and Chapter 6 (evaluating proximal operators)
  - paper: doi:10.24033/bsmf.1625
    title: Jean-Jacques Moreau, Proximité et dualité dans un espace hilbertien, Bulletin de la Société Mathématique de France 93, 1965
    locator: pages 273 to 299, the original definition of the proximal map and the decomposition theorem
  - paper: doi:10.1137/050626090
    title: Patrick L. Combettes and Valérie R. Wajs, Signal recovery by proximal forward-backward splitting, Multiscale Modeling and Simulation 4(4), 2005
    locator: Section 2 (proximity operators and their properties)
---

The proximal operator of a [convex function](/convex-function/) $h$ maps a point $x$ to the point $u$ that minimizes $h(u) + \frac{1}{2t}\lVert u - x \rVert_2^2$. It trades a small value of $h$ against a short distance from $x$. For the indicator function of a convex set it is the Euclidean projection onto the set, and for $\lambda \lVert \cdot \rVert_1$ it is soft thresholding. It is the step that lets gradient methods handle nonsmooth terms, as in the [proximal gradient method](/proximal-gradient-method/) and [FISTA](/fista/).

## Definition

Notation: $n$ is the number of variables, $\lVert \cdot \rVert$ is the Euclidean norm on $\mathbb{R}^n$, and $t > 0$ is a step parameter.

Let $h : \mathbb{R}^n \to (-\infty, +\infty]$ be proper (it is not $+\infty$ everywhere), closed (its epigraph is closed, so it is lower semicontinuous) and convex. The **proximal operator** of $h$ with parameter $t$ is

$$\operatorname{prox}_{t h}(x) = \operatorname*{argmin}_{u \in \mathbb{R}^n} \Big\{ h(u) + \frac{1}{2t} \lVert u - x \rVert^2 \Big\}, \qquad x \in \mathbb{R}^n.$$

The value $\operatorname{prox}_h$ is the case $t = 1$. The minimum value of the same problem, as a function of $x$, is the **Moreau envelope** $M_{th}(x) = \min_u \{ h(u) + \frac{1}{2t}\lVert u - x\rVert^2 \}$.

### Basic properties

**Existence and uniqueness.** For each $x$, the minimizer exists and is unique. The function $\phi(u) = h(u) + \frac{1}{2t}\lVert u - x \rVert^2$ is closed, and it is strongly convex with modulus $1/t$, because it is a convex function plus a strongly convex one. A closed proper convex function has an affine minorant $h(u) \ge a^\top u + b$, so $\phi(u) \to +\infty$ as $\lVert u \rVert \to \infty$. Its sublevel sets are therefore closed and bounded, and a lower semicontinuous function attains its minimum on a nonempty compact sublevel set. If $u_1 \ne u_2$ were two minimizers, strong convexity would give $\phi(\frac{u_1 + u_2}{2}) < \frac{1}{2}\phi(u_1) + \frac{1}{2}\phi(u_2) = \min \phi$, which is impossible.

**Subgradient characterization.** For all $x, p \in \mathbb{R}^n$,

$$p = \operatorname{prox}_{th}(x) \iff \frac{x - p}{t} \in \partial h(p).$$

The point $p$ minimizes the convex function $\phi$ exactly when $0 \in \partial \phi(p)$. The quadratic term is differentiable and finite everywhere, so the sum rule for the [subdifferential](/subdifferential/) holds and $\partial\phi(p) = \partial h(p) + (p - x)/t$.

**Firm nonexpansiveness.** For all $x, y$, with $p = \operatorname{prox}_{th}(x)$ and $q = \operatorname{prox}_{th}(y)$,

$$\lVert p - q \rVert^2 \le \langle p - q, x - y \rangle, \qquad \text{so} \qquad \lVert p - q \rVert \le \lVert x - y \rVert.$$

By the characterization, $(x - p)/t \in \partial h(p)$ and $(y - q)/t \in \partial h(q)$. The subdifferential of a convex function is monotone: $\langle g_1 - g_2, p - q\rangle \ge 0$ for $g_1 \in \partial h(p)$ and $g_2 \in \partial h(q)$. With these two subgradients, $\langle (x - y) - (p - q), p - q \rangle \ge 0$, which is the first inequality. The Cauchy-Schwarz bound $\langle p - q, x - y\rangle \le \lVert p - q\rVert \lVert x - y\rVert$ gives the second one.

**Fixed points are minimizers.** $x = \operatorname{prox}_{th}(x)$ holds if and only if $0 \in \partial h(x)$, that is, if and only if $x$ minimizes $h$. This is the characterization with $p = x$.

**Moreau decomposition.** With the [convex conjugate](/convex-conjugate/) $h^*$, each $x$ splits as $x = \operatorname{prox}_{h}(x) + \operatorname{prox}_{h^*}(x)$. With a parameter, $x = \operatorname{prox}_{th}(x) + t\operatorname{prox}_{h^*/t}(x/t)$. The proof uses $g \in \partial h(p) \iff p \in \partial h^*(g)$ (Beck, Chapter 6). So a prox of $h$ gives a prox of $h^*$ at no extra cost.

**The envelope is smooth.** $M_{th}$ is convex and differentiable, with $\nabla M_{th}(x) = (x - \operatorname{prox}_{th}(x))/t$. By firm nonexpansiveness, this gradient is $1/t$-Lipschitz. $M_{th}$ has the same minimizers and the same minimum value as $h$. So the prox step $x \mapsto \operatorname{prox}_{th}(x) = x - t\nabla M_{th}(x)$ is a gradient step on a smooth version of $h$.

## Examples and non-examples

**Zero function.** For $h = 0$, $\operatorname{prox}_{th}(x) = x$.

**Linear function.** For $h(u) = a^\top u$, the minimizer of $a^\top u + \frac{1}{2t}\lVert u - x\rVert^2$ is $x - t a$: the prox is one gradient step.

**Indicator of a convex set.** Let $C$ be a nonempty closed [convex set](/convex-set/), and let $h = \iota_C$, with $\iota_C(u) = 0$ for $u \in C$ and $+\infty$ otherwise. Then $\operatorname{prox}_{t\iota_C}(x) = \Pi_C(x)$, the nearest point of $C$ to $x$, for every $t > 0$. For the box $[0,1]^3$ and $x = (1.7, -0.3, 0.4)$, the prox clips each coordinate: $(1, 0, 0.4)$. For the unit ball and $x = (3, 4)$, it scales $x$ to length 1: $(0.6, 0.8)$. This makes [projected gradient descent](/projected-gradient-descent/) a special case of the proximal gradient method.

**The $\ell_1$ norm: soft thresholding.** For $h = \lambda \lVert \cdot \rVert_1$ with $\lambda > 0$, the problem splits into one problem for each coordinate, and

$$\operatorname{prox}_{t\lambda\lVert\cdot\rVert_1}(x)_i = \operatorname{sign}(x_i)\max(\lvert x_i\rvert - t\lambda, 0).$$

To check one coordinate, use the characterization: $p_i$ must satisfy $(x_i - p_i)/t \in \lambda\,\partial\lvert p_i\rvert$. If $\lvert x_i\rvert \le t\lambda$, then $p_i = 0$ works, because $\partial\lvert 0\rvert = [-1, 1]$. If $x_i > t\lambda$, then $p_i = x_i - t\lambda > 0$ works, because $\partial\lvert p_i\rvert = \{1\}$. The case $x_i < -t\lambda$ is the mirror image. With $t\lambda = 1$ and $x = (3, -0.5, 1.2)$, the prox is $(2, 0, 0.2)$. Small entries become exactly zero, which is why the $\ell_1$ term gives sparse solutions in [lasso regression](/lasso-regression/).

**Squared norm.** For $h = \frac{\lambda}{2}\lVert\cdot\rVert^2$, the prox is $x/(1 + t\lambda)$: it shrinks the point toward the origin.

**Moreau envelope of the absolute value.** For $h(u) = \lvert u\rvert$ on $\mathbb{R}$ and $t = 1$, the envelope is the Huber function: $M_h(x) = x^2/2$ for $\lvert x\rvert \le 1$ and $\lvert x\rvert - 1/2$ otherwise. At $x = 3$ it is $2.5$, and at $x = 0.4$ it is $0.08$.

**Non-example: a function that is not closed.** Let $h = \iota_{(0,1)}$, the indicator of an open interval. It is convex and proper, but not closed. At $x = 2$, the values of $h(u) + \frac{1}{2}(u - 2)^2$ on $(0, 1)$ approach $1/2$ as $u \to 1$, but no $u$ in $(0,1)$ attains it. So the prox does not exist at $x = 2$.

**Non-example: a nonconvex function.** Let $h(u) = \lambda \cdot [u \ne 0]$ on $\mathbb{R}$, the $\ell_0$ penalty. Then the minimizers of $h(u) + \frac{1}{2t}(u - x)^2$ are $u = x$ when $\lvert x\rvert > \sqrt{2t\lambda}$ and $u = 0$ when $\lvert x\rvert < \sqrt{2t\lambda}$: this is hard thresholding. At $\lvert x\rvert = \sqrt{2t\lambda}$, both $0$ and $x$ are minimizers, so the "prox" is a set with two points. With $t = 1$ and $\lambda = 0.5$, this happens at $\lvert x\rvert = 1$. The map is also not nonexpansive: it jumps from $0$ to about $1$ as $x$ crosses $1$.

## Related definitions

- **Projection.** The prox of an indicator function, as above. The obtuse-angle property of the projection, $\langle x - \Pi_C(x), z - \Pi_C(x)\rangle \le 0$ for all $z \in C$, is the characterization with $\partial\iota_C(p)$ equal to the normal cone of $C$ at $p$.
- **[Proximal point method](/proximal-point-method/).** The iteration $x_{k+1} = \operatorname{prox}_{t h}(x_k)$. By the envelope property, it is gradient descent with step $t$ on $M_{th}$.
- **[Proximal gradient method](/proximal-gradient-method/).** For $f + h$ with $f$ smooth, it alternates a gradient step on $f$ and a prox step on $h$. See [composite minimization](/composite-minimization/).
- **Resolvent.** In monotone operator theory, $\operatorname{prox}_{th} = (I + t\,\partial h)^{-1}$, the resolvent of the subdifferential. This is the characterization written as an operator.
- **Bregman proximal map.** Replace $\frac{1}{2}\lVert u - x\rVert^2$ by a [Bregman divergence](/bregman-divergence/) $D_\psi(u, x)$. This gives the step of [mirror descent](/mirror-descent/).
- **[ADMM](/admm/).** Each ADMM step evaluates two proximal operators, one for each part of the objective.

## References
