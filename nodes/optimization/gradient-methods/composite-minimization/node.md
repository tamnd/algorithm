---
tag: R33W76
kind: problem
slug: composite-minimization
name: Composite minimization
aliases:
- smooth plus nonsmooth minimization
- regularized minimization
- composite convex optimization
area: optimization/gradient-methods
level: advanced
summary: Minimize a smooth function plus a simple nonsmooth regularizer, such as the l1 norm.
prereqs: [proximal-operator, smoothness, convex-function]
see_also: [proximal-gradient-method, fista, constrained-smooth-minimization, lasso-regression, admm, coordinate-descent, first-order-lower-bound, total-variation-denoising]
sources:
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 10, The proximal gradient method (the model, the gradient mapping, the rates of the proximal gradient method and of FISTA)
  - paper: doi:10.1007/s10107-012-0629-5
    title: Yurii Nesterov, Gradient methods for minimizing composite functions, Mathematical Programming 140(1), 2013
    locator: Section 2 (the composite problem and the composite gradient mapping) and Section 4 (the accelerated method)
  - paper: doi:10.1561/2400000003
    title: Neal Parikh and Stephen Boyd, Proximal algorithms, Foundations and Trends in Optimization 1(3), 2014
    locator: Chapter 4 (proximal algorithms) and Chapter 6 (evaluating proximal operators, including norms and matrix functions)
  - paper: doi:10.1007/s10107-004-0552-5
    title: Yurii Nesterov, Smooth minimization of non-smooth functions, Mathematical Programming 103(1), 2005
    locator: pages 127 to 152, the smoothing technique and its O(1/ε) bound
  - paper: doi:10.1111/j.2517-6161.1996.tb02080.x
    title: Robert Tibshirani, Regression shrinkage and selection via the lasso, Journal of the Royal Statistical Society Series B 58(1), 1996
    locator: pages 267 to 288, the l1-penalized least squares problem
---

Composite minimization is the problem of minimizing $F(x) = f(x) + h(x)$, where $f$ is convex and smooth and $h$ is convex, possibly nonsmooth, and simple in the sense that its [proximal operator](/proximal-operator/) is cheap. The $\ell_1$-penalized least squares problem ([lasso](/lasso-regression/)) is the standard example. The structure matters: a method that uses $\nabla f$ and the prox of $h$ reaches the rates of smooth optimization, $O(1/k)$ and $O(1/k^2)$, while a method that sees $F$ only as a nonsmooth function is limited to $O(1/\sqrt{k})$.

## In plain words

Many objectives are a sum of two terms. The first term measures how badly the solution fits the data. It is smooth: it has a slope everywhere. The second term encodes a wish about the solution, for example "few nonzero entries" or "stay inside this box". It often has corners or jumps.

Composite minimization is the task of making this sum as small as possible. Methods for it treat the two terms in different ways. They follow the slope of the smooth term, and they handle the second term by an exact small subproblem that has a closed form. This way the corners do not slow the method down.

## Definition

Notation: $n$ is the number of variables, $x^*$ is a minimizer, $F^* = F(x^*)$, $L_f$ and $\mu$ are the smoothness and strong convexity constants of $f$, $\kappa = L_f/\mu$, $R = \lVert x_0 - x^*\rVert$ for a start point $x_0$, and $\varepsilon$ is the target accuracy.

**Input.** A function $f : \mathbb{R}^n \to \mathbb{R}$ that is convex and differentiable with an $L_f$-Lipschitz gradient ([smoothness](/smoothness/)), given by an oracle for $f$ and $\nabla f$. A function $h : \mathbb{R}^n \to (-\infty, +\infty]$ that is proper, closed and convex, given by an oracle for $\operatorname{prox}_{th}$ for each $t > 0$. A start point $x_0$ and an accuracy $\varepsilon > 0$.

**Output.** A point $x$ with $F(x) - F^* \le \varepsilon$, where $F = f + h$ and $F^* = \inf F$, under the promise that $F$ has a minimizer.

**Optimality.** A point $x^*$ minimizes $F$ if and only if $0 \in \nabla f(x^*) + \partial h(x^*)$. By the characterization of the prox, this holds if and only if, for some (and then for every) $t > 0$,

$$x^* = \operatorname{prox}_{th}\big(x^* - t\nabla f(x^*)\big).$$

The **gradient mapping** $G_t(x) = \frac{1}{t}\big(x - \operatorname{prox}_{th}(x - t\nabla f(x))\big)$ is therefore zero exactly at the minimizers. For $h = 0$ it is $\nabla f(x)$. Its norm is the usual measure of progress when $f$ is not convex.

## Variants

- **Strongly convex.** $f$ is $\mu$-strongly convex. Then the minimizer is unique and linear rates are possible.
- **Constrained smooth minimization.** $h = \iota_C$, the indicator of a closed convex set $C$. This is [constrained smooth minimization](/constrained-smooth-minimization/), and the prox is the projection onto $C$.
- **Nonconvex smooth part.** $f$ is smooth but not convex, and $h$ is convex. The goal becomes a point with $\lVert G_t(x)\rVert \le \varepsilon$.
- **Finite sums.** $f = \frac{1}{N}\sum_{i=1}^N f_i$. Stochastic and variance-reduced methods apply ([finite-sum minimization](/finite-sum-minimization/)).
- **Composition with a linear map.** $F(x) = f(x) + h(Ax)$, where the prox of $h$ is cheap but the prox of $h \circ A$ is not, as in total variation. Splitting methods such as [ADMM](/admm/) handle this form.

## Examples

**One variable.** Let $f(x) = \frac{1}{2}(x - 3)^2$ and $h(x) = \lambda\lvert x\rvert$. The optimality condition $3 - x \in \lambda\,\partial\lvert x\rvert$ gives $x^* = 3 - \lambda$ for $\lambda < 3$ and $x^* = 0$ for $\lambda \ge 3$. For $\lambda = 2$, $x^* = 1$ and $F^* = 2 + 2 = 4$. For $\lambda = 4$, $x^* = 0$ and $F^* = 4.5$. The kink of $h$ at $0$ holds the solution at exactly zero for every $\lambda \ge 3$.

**Lasso.** $f(x) = \frac{1}{2}\lVert Ax - b\rVert^2$ and $h(x) = \lambda\lVert x\rVert_1$. Here $L_f = \lambda_{\max}(A^\top A)$ and the prox is soft thresholding. A worked run is on the [proximal gradient method](/proximal-gradient-method/) page.

**Nonnegative least squares.** $f(x) = \frac{1}{2}\lVert Ax - b\rVert^2$ and $h = \iota_{\{x \ge 0\}}$. The prox sets each negative entry to zero.

**Elastic net.** $h(x) = \lambda_1\lVert x\rVert_1 + \frac{\lambda_2}{2}\lVert x\rVert^2$. The prox is soft thresholding by $t\lambda_1$ followed by division by $1 + t\lambda_2$.

**Sparse logistic regression.** $f$ is the average [logistic loss](/logistic-loss/), with $L_f \le \lambda_{\max}(X^\top X)/(4N)$ for a data matrix $X$ with $N$ rows, and $h = \lambda\lVert\cdot\rVert_1$.

**Low-rank matrix recovery.** The variable is a matrix, $f$ is a squared error on observed entries, and $h$ is $\lambda$ times the nuclear norm (the sum of singular values). The prox soft-thresholds the singular values, so one prox costs one singular value decomposition.

**Non-example.** $h(x) = \lambda\lVert Dx\rVert_1$ with a general matrix $D$, such as the differences of neighboring pixels. The function is convex, but its prox has no closed form in general. The problem is still composite in the wider sense of the last variant, but the prox oracle of the definition is not available.

## Known algorithms

| Method | Assumption | Rate after $k$ iterations |
|---|---|---|
| [Proximal gradient method](/proximal-gradient-method/) | convex | $F(x_k) - F^* \le L_f R^2/(2k)$ |
| Proximal gradient method | $\mu$-strongly convex | $\lVert x_k - x^*\rVert^2 \le (1 - 1/\kappa)^k R^2$ |
| [FISTA](/fista/) | convex | $F(x_k) - F^* \le 2L_f R^2/(k+1)^2$ |
| Accelerated proximal gradient with $\mu$ known | $\mu$-strongly convex | error factor $(1 - 1/\sqrt{\kappa})^k$ |
| [Coordinate descent](/coordinate-descent/) | $h$ separable | as gradient methods, with coordinate constants |
| [ADMM](/admm/) | convex | $O(1/k)$ in an ergodic sense |
| Subgradient method | $F$ is $G$-Lipschitz | $O(GR/\sqrt{k})$, ignores the structure |

Each iteration of the first four rows costs one gradient of $f$ and one prox of $h$. With $h$ a box or $\ell_1$ norm, an interior point method can also solve the problem as a quadratic program, at a higher cost for each iteration but with $O(\log(1/\varepsilon))$ iterations.

## Bounds

- **Upper.** FISTA needs $O(\sqrt{L_f R^2/\varepsilon})$ iterations. In the strongly convex case, accelerated methods need $O(\sqrt{\kappa}\log(1/\varepsilon))$.
- **Lower.** The case $h = 0$ is smooth convex minimization, so the [first-order lower bound](/first-order-lower-bound/) of Nemirovski and Yudin and of Nesterov applies: for $k \le (n-1)/2$, some $f$ forces $F(x_k) - F^* \ge \frac{3L_f R^2}{32(k+1)^2}$ for every method whose iterates lie in the span of the past gradients. So FISTA is optimal up to a constant factor.
- **Without the structure.** If $F$ is only known to be convex and $G$-Lipschitz, the best rate for first-order methods is $\Theta(GR/\sqrt{k})$ in high dimension. The composite structure is what removes this barrier.

## Reductions

- **Constrained to composite.** Minimizing a smooth $f$ over a convex set $C$ is the case $h = \iota_C$.
- **Composite to smooth, by smoothing.** If $h$ is $G$-Lipschitz, its Moreau envelope $M_{sh}$ is $(1/s)$-smooth and $0 \le h - M_{sh} \le sG^2/2$. The first inequality holds because $u = x$ is a candidate in the definition of $M_{sh}(x)$. For the second, with $p = \operatorname{prox}_{sh}(x)$, $h(x) - M_{sh}(x) = h(x) - h(p) - \frac{1}{2s}\lVert x - p\rVert^2 \le G\lVert x - p\rVert - \frac{1}{2s}\lVert x - p\rVert^2 \le sG^2/2$. With $s$ of order $\varepsilon/G^2$, an accelerated method on $f + M_{sh}$ needs $O(1/\varepsilon)$ iterations (Nesterov 2005). This is worse than FISTA on the composite form, and better than the $O(1/\varepsilon^2)$ of the subgradient method.
- **Lasso to a quadratic program.** Write $x = x^+ - x^-$ with $x^+, x^- \ge 0$. Then $\lambda\lVert x\rVert_1$ becomes the linear term $\lambda\mathbf{1}^\top(x^+ + x^-)$, and the lasso is a [quadratic program](/quadratic-programming/) in $2n$ variables.
- **The prox step is a composite problem.** Computing $\operatorname{prox}_{th}(y)$ is itself the case $f(u) = \frac{1}{2t}\lVert u - y\rVert^2$.

## Applications

- Sparse regression and [compressed sensing](/compressed-sensing/), with the $\ell_1$ norm.
- Image denoising and deblurring, with total variation ([total variation denoising](/total-variation-denoising/)) or with wavelet sparsity.
- Matrix completion and recommender systems, with the nuclear norm.
- Regularized classifiers, such as $\ell_1$-penalized [logistic regression](/logistic-regression/).
- Problems with simple constraints: boxes, the probability simplex, balls, nonnegativity, as in [portfolio optimization](/portfolio-optimization/).

## References
