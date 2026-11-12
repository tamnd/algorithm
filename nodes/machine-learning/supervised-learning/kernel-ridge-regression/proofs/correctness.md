---
title: Kernel ridge regression returns the unique minimizer of the penalized squared error
proves: [correctness]
status: full
---

We use the pseudocode of the page. Let $k$ be a positive semidefinite kernel with reproducing kernel Hilbert space $\mathcal{H}$, let $\lambda > 0$, and let

$$J(f) = \sum_{i=1}^n (f(x_i) - y_i)^2 + \lambda \lVert f \rVert_{\mathcal{H}}^2, \qquad f \in \mathcal{H}.$$

**Lemma 1.** The matrix $A = K + \lambda I$ of line L2 is symmetric positive definite, so lines L3 to L5 compute $\alpha = A^{-1} y$.

*Proof.* $K$ is symmetric, and $c^\top K c = \lVert \sum_i c_i k(x_i, \cdot) \rVert_{\mathcal{H}}^2 \ge 0$ for every $c \in \mathbb{R}^n$. So $c^\top A c \ge \lambda \lVert c \rVert^2 > 0$ for $c \ne 0$. A symmetric positive definite matrix has a Cholesky factor $L$ with a positive diagonal, so the triangular systems of lines L4 and L5 have unique solutions, and $L L^\top \alpha = L u = y$. $\square$

**Lemma 2.** $J$ has at most one minimizer.

*Proof.* The map $f \mapsto (f(x_i))_i$ is linear, so the first term of $J$ is convex in $f$. The term $\lambda \lVert f \rVert^2$ is strictly convex, because for $f \ne g$ and $0 < t < 1$, $\lVert t f + (1 - t) g \rVert^2 = t \lVert f \rVert^2 + (1 - t) \lVert g \rVert^2 - t(1 - t) \lVert f - g \rVert^2$. So $J$ is strictly convex, and two different minimizers $f, g$ would give $J((f + g)/2) < J(f)$. $\square$

**Lemma 3.** Let $\hat f = \sum_i \alpha_i k(x_i, \cdot)$ with $\alpha = (K + \lambda I)^{-1} y$. Then $J(\hat f) \le J(f)$ for every $f \in \mathcal{H}$.

*Proof.* Let $V = \operatorname{span}\{k(x_i, \cdot)\}$ and split $f = f_\parallel + f_\perp$ with $f_\parallel \in V$ and $f_\perp \perp V$. By the reproducing property $f(x_i) = f_\parallel(x_i)$, and $\lVert f \rVert^2 \ge \lVert f_\parallel \rVert^2$, so $J(f) \ge J(f_\parallel)$. This is the argument of the [representer theorem](/representer-theorem/). So it suffices to compare $\hat f$ with $g = \sum_i \beta_i k(x_i, \cdot) \in V$. For such $g$, the values are $K\beta$ and $\lVert g \rVert^2 = \beta^\top K \beta$, so

$$J(g) = q(\beta) = \lVert K\beta - y \rVert^2 + \lambda \beta^\top K \beta.$$

The function $q$ is a convex quadratic, since its Hessian $2(K^2 + \lambda K) = 2K(K + \lambda I)$ is positive semidefinite: $K$ and $K + \lambda I$ commute and are both positive semidefinite. Its gradient is

$$\nabla q(\beta) = 2K(K\beta - y) + 2\lambda K \beta = 2K\big((K + \lambda I)\beta - y\big),$$

which is 0 at $\beta = \alpha$. A convex differentiable function is minimal where its gradient is 0, so $q(\alpha) \le q(\beta)$ for every $\beta$. $\square$

**Theorem.** KRR-FIT returns $\alpha$ such that $\hat f = \sum_i \alpha_i k(x_i, \cdot)$ is the unique minimizer of $J$ over $\mathcal{H}$, and KRR-PREDICT returns $\hat f(x)$.

*Proof.* Lemma 1 shows that lines L1 to L6 return $\alpha = (K + \lambda I)^{-1} y$. Lemma 3 shows that $\hat f$ is a minimizer, and Lemma 2 that it is the only one. Line L7 evaluates $\hat f(x) = \sum_i \alpha_i k(x_i, x)$. $\blacksquare$

**Remark.** The minimizing function is unique, but $\alpha$ need not be unique as a representation when $K$ is singular. The algorithm returns the particular $\alpha = (K + \lambda I)^{-1} y$, which also satisfies $y - K\alpha = \lambda \alpha$.
