---
tag: BWRZ8V
kind: theorem
slug: representer-theorem
name: Representer theorem
aliases:
- generalized representer theorem
- Kimeldorf-Wahba representer theorem
area: machine-learning/supervised-learning
level: advanced
summary: "For any loss on the training values plus a strictly increasing function of the RKHS norm, every minimizer is a combination of the kernel functions k(x_i, ·)."
prereqs: [kernel-trick]
see_also: [mercer-theorem, kernel-ridge-regression, support-vector-machine, kernel-trick, gaussian-process, logistic-regression, hinge-loss, kernel-pca]
sources:
  - paper: doi:10.1016/0022-247X(71)90184-3
    title: George Kimeldorf and Grace Wahba, Some results on Tchebycheffian spline functions, Journal of Mathematical Analysis and Applications 33(1), 1971
    locator: pp. 82 to 95 (the minimizer of a quadratic loss plus a squared RKHS norm is a combination of kernel functions at the data)
  - paper: doi:10.1007/3-540-44581-1_27
    title: Bernhard Schölkopf, Ralf Herbrich and Alex J. Smola, A generalized representer theorem, COLT 2001, Lecture Notes in Computer Science 2111
    locator: pp. 416 to 426 (Theorem 1, arbitrary loss and a strictly increasing regularizer; the semiparametric version)
  - paper: "Andreas Argyriou, Charles A. Micchelli and Massimiliano Pontil, When is there a representer theorem? Vector versus matrix regularizers, Journal of Machine Learning Research 10, 2009"
    locator: the characterization of the regularizers for which a representer theorem holds for all data
  - book: isbn:9780262194754
    title: Bernhard Schölkopf and Alexander J. Smola, Learning with Kernels, MIT Press, 2002
    locator: Chapter 4 (regularization; the representer theorem)
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Chapter 16 (kernel methods; the representer theorem for the norm in feature space)
---

The representer theorem says that a regularized learning problem over a reproducing kernel Hilbert space, which has infinitely many unknowns, has a solution with only $n$ unknowns. If the objective is any function of the values $f(x_1), \ldots, f(x_n)$ plus a strictly increasing function of the norm $\lVert f \rVert$, then every minimizer has the form $f = \sum_{i=1}^n \alpha_i k(x_i, \cdot)$. This is why the [support vector machine](/support-vector-machine/), [kernel ridge regression](/kernel-ridge-regression/) and kernel logistic regression can be solved with the $n \times n$ Gram matrix. Kimeldorf and Wahba proved it for the squared loss in 1971, and Schölkopf, Herbrich and Smola gave the general form in 2001.

## Statement

Let $k$ be a positive semidefinite kernel on a set $X$, and $\mathcal{H}$ its reproducing kernel Hilbert space: a Hilbert space of functions on $X$ with $k(x, \cdot) \in \mathcal{H}$ and $f(x) = \langle f, k(x, \cdot) \rangle_{\mathcal{H}}$ for all $f \in \mathcal{H}$ and $x \in X$. Let $(x_1, y_1), \ldots, (x_n, y_n)$ be training data with $x_i \in X$. Let

- $c : (X \times \mathbb{R} \times \mathbb{R})^n \to \mathbb{R} \cup \{+\infty\}$ be any function (the loss), with no convexity or continuity required, and
- $g : [0, \infty) \to \mathbb{R}$ be strictly increasing (the regularizer).

**Theorem (Schölkopf, Herbrich and Smola 2001).** Every minimizer $f^\ast \in \mathcal{H}$ of

$$J(f) = c\big((x_1, y_1, f(x_1)), \ldots, (x_n, y_n, f(x_n))\big) + g(\lVert f \rVert_{\mathcal{H}})$$

has the form

$$f^\ast = \sum_{i=1}^{n} \alpha_i\, k(x_i, \cdot) \quad \text{for some } \alpha \in \mathbb{R}^n.$$

If $g$ is only nondecreasing, then some minimizer has this form whenever a minimizer exists.

**The semiparametric version.** Let $\psi_1, \ldots, \psi_M$ be real functions on $X$, such as the constant function for a bias. Then every minimizer $\tilde f = f + h$ with $f \in \mathcal{H}$ and $h \in \operatorname{span}(\psi_p)$ of $c(\ldots, \tilde f(x_i), \ldots) + g(\lVert f \rVert_{\mathcal{H}})$ has $f = \sum_i \alpha_i k(x_i, \cdot)$. The unpenalized part $h$ is free.

**Reduction to $n$ unknowns.** With $f = \sum_j \alpha_j k(x_j, \cdot)$ and the Gram matrix $K_{ij} = k(x_i, x_j)$, the values are $f(x_i) = (K\alpha)_i$ and the norm is $\lVert f \rVert^2 = \alpha^\top K \alpha$. So the problem becomes

$$\min_{\alpha \in \mathbb{R}^n} \; c\big(\ldots, (x_i, y_i, (K\alpha)_i), \ldots\big) + g\big(\sqrt{\alpha^\top K \alpha}\big).$$

The theorem does not claim that a minimizer exists. For a convex, lower semicontinuous loss and $g(t) = \lambda t^2$ with $\lambda > 0$, one exists because the reduced problem is coercive in the directions that change $f$.

## In plain words

The space of candidate functions is huge, often infinite dimensional. But the training data only sees each function through its values at the $n$ training points. Split a function into a part built from the $n$ kernel functions $k(x_i, \cdot)$ and a part orthogonal to them. The orthogonal part is zero at every training point, so it does not change the fit. It only makes the function larger. If the penalty strictly prefers smaller functions, the orthogonal part must be zero at the best solution. So the best solution is a combination of $n$ kernel functions, with $n$ coefficients to find.

## Proof

Let $V = \operatorname{span}\{k(x_1, \cdot), \ldots, k(x_n, \cdot)\}$. It is a finite dimensional, hence closed, subspace of $\mathcal{H}$. Every $f \in \mathcal{H}$ has a unique orthogonal decomposition

$$f = f_\parallel + f_\perp, \qquad f_\parallel \in V, \quad f_\perp \perp V.$$

**The loss depends only on $f_\parallel$.** By the reproducing property, for each $i$,

$$f(x_i) = \langle f, k(x_i, \cdot) \rangle = \langle f_\parallel, k(x_i, \cdot) \rangle + \langle f_\perp, k(x_i, \cdot) \rangle = f_\parallel(x_i) + 0,$$

since $k(x_i, \cdot) \in V$ and $f_\perp \perp V$. So the loss term of $J$ has the same value at $f$ and at $f_\parallel$.

**The regularizer prefers $f_\parallel$.** By Pythagoras, $\lVert f \rVert^2 = \lVert f_\parallel \rVert^2 + \lVert f_\perp \rVert^2$. If $f_\perp \ne 0$, then $\lVert f_\parallel \rVert < \lVert f \rVert$, and since $g$ is strictly increasing, $g(\lVert f_\parallel \rVert) < g(\lVert f \rVert)$.

**Conclusion.** If $f^\ast$ is a minimizer and $f^\ast_\perp \ne 0$, then $J(f^\ast_\parallel) < J(f^\ast)$, which is impossible. So $f^\ast_\perp = 0$ and $f^\ast \in V$. If $g$ is only nondecreasing, the same argument gives $J(f^\ast_\parallel) \le J(f^\ast)$, so the projection $f^\ast_\parallel \in V$ of any minimizer is also a minimizer.

**The semiparametric version.** Apply the same split to the $\mathcal{H}$ part $f$ of $\tilde f = f + h$. The values $\tilde f(x_i) = f_\parallel(x_i) + h(x_i)$ do not depend on $f_\perp$, and the regularizer depends on $f$ alone, so again $f_\perp = 0$ at every minimizer. $\blacksquare$

## Consequences

- **[Kernel ridge regression](/kernel-ridge-regression/).** With $c = \sum_i (f(x_i) - y_i)^2$ and $g(t) = \lambda t^2$, the reduced problem is $\lVert K\alpha - y \rVert^2 + \lambda \alpha^\top K \alpha$, minimized by $\alpha = (K + \lambda I)^{-1} y$. This is the case of Kimeldorf and Wahba, where it also explains why smoothing splines are piecewise polynomials with knots at the data.
- **The [support vector machine](/support-vector-machine/).** With the [hinge loss](/hinge-loss/) $\sum_i \max(0, 1 - y_i \tilde f(x_i))$, $g(t) = \tfrac12 t^2$ and an unpenalized bias, $\tilde f = \sum_i \alpha_i k(x_i, \cdot) + b$. The KKT conditions add that $\alpha_i \ne 0$ only for the support vectors.
- **Kernel logistic regression.** With the logistic loss, every $\alpha_i$ is usually nonzero, so the solution is not sparse.
- **The [kernel trick](/kernel-trick/) is justified.** Each such method needs only $K$ to train and $k(x_i, x)$ to predict, never the feature map.
- **The cost.** Training works with $n$ unknowns and an $n \times n$ matrix; prediction costs $n$ kernel evaluations, or one per nonzero $\alpha_i$.
- **Gaussian processes.** The posterior mean of a [Gaussian process](/gaussian-process/) with covariance $k$ and noise variance $\sigma^2$ is the kernel ridge solution with $\lambda = \sigma^2$, so it also lies in $V$.

**A numerical check.** Take the kernel $(x \cdot z + 1)^2$ on $\mathbb{R}^2$, whose explicit feature map has 6 coordinates, and 4 training points, so $V$ is a proper subspace of $\mathbb{R}^6$. Minimize the regularized logistic loss $\sum_i \log(1 + e^{-y_i w \cdot \varphi(x_i)}) + 0.2 \lVert w \rVert^2$ over all of $\mathbb{R}^6$ by gradient descent, from a random start (seed 1971) at distance more than 0.1 from $V$. After 4000 steps the distance from $w$ to $V$ is below $10^{-8}$. Ridge regression solved in $\mathbb{R}^6$ by the normal equations gives the same $w$ as $\sum_i \alpha_i \varphi(x_i)$ with $\alpha = (K + \lambda I)^{-1} y$, to within $10^{-9}$.

## Tightness

- **Strictness of $g$.** With $g \equiv 0$ and the squared loss, take 3 training points in the 6 dimensional feature space above. An interpolant in $V$ has loss 0. Adding any nonzero $v \perp V$ gives another interpolant with loss 0, which is not in $V$. So only "some minimizer" can be claimed when $g$ is not strictly increasing.
- **The norm must be the Hilbert norm.** With an $\ell_1$ penalty on the weights, the theorem fails. For the linear kernel on $\mathbb{R}^2$ and one point $x_1 = (1, 1)$ with $y_1 = 1$, the problem $\min_w (w \cdot x_1 - 1)^2 + \lambda \lVert w \rVert_1$ with $0 < \lambda < 2$ is minimized by every $w \ge 0$ with $w_1 + w_2 = 1 - \lambda/2$. One of them is $w = (1 - \lambda/2, 0)$, which is not a multiple of $x_1$.
- **The regularizer must depend only on the norm, in a sense.** Argyriou, Micchelli and Pontil (2009) showed that, for a differentiable regularizer $\Omega$, a representer theorem holds for all data sets if and only if $\Omega(f) = h(\lVert f \rVert)$ for a nondecreasing $h$.
- **Point evaluations must be continuous.** The proof uses $f(x_i) = \langle f, k(x_i, \cdot) \rangle$. In a Hilbert space such as $L^2$, where point values are not defined, there is no such theorem.
- **Existence is a separate question.** Let $g(t) = t$, and let the loss be 0 if $f(x_1) > 0$ and 1 otherwise, with $k(x_1, x_1) > 0$. Then $f = \epsilon\, k(x_1, \cdot)$ gives $J = \epsilon \sqrt{k(x_1, x_1)}$ for every $\epsilon > 0$, so $\inf J = 0$, but $J(f) > 0$ for every $f$. No minimizer exists, and the theorem says nothing. The loss here is not lower semicontinuous.

## History

Kimeldorf and Wahba (1970, 1971) proved that the minimizer of a squared error plus a squared RKHS norm is a combination of kernel functions at the data, linking smoothing splines with Bayesian estimation. Cox and O'Sullivan (1990) and Wahba's 1990 monograph extended it to other losses. Schölkopf, Herbrich and Smola (2001) gave the general form for an arbitrary loss and a strictly increasing function of the norm, with a semiparametric part. Argyriou, Micchelli and Pontil (2009) characterized the regularizers that allow a representer theorem.

## References
