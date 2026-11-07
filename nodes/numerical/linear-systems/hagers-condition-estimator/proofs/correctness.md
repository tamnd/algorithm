---
title: Correctness of Hager's estimator
proves: [correctness, termination]
status: full
---

Exact arithmetic. $f(x) = \|B x\|_1$, $\operatorname{sign}(0) = 1$, and for a point $x$ with $y = B x$, $\xi = \operatorname{sign}(y)$ and $z = B^T \xi$.

**Lemma 1 (subgradient).** For every $w$, $f(w) \ge z^T w$, and $f(x) = z^T x$.

*Proof.* $|\xi_i| = 1$, so $f(w) = \sum_i |(B w)_i| \ge \sum_i \xi_i (B w)_i = \xi^T B w = z^T w$. At $w = x$, $\xi_i y_i = |y_i|$, so equality holds. $\square$

**Theorem 2 (lower bound).** Every value assigned to $\gamma$ equals $\|B v\|_1 / \|v\|_1$ for some $v \ne 0$, hence $\gamma \le \|B\|_1$.

*Proof.* The vectors $x$ used in line L3 are $e/n$ and $e_j$, of 1-norm $1$, so $\gamma = \|B x\|_1$ is of this form. In line L10, $\|b\|_1 = \sum_{i=0}^{n-1}(1 + i/(n - 1)) = n + n/2 = 3n/2$, so $2\|B b\|_1/(3n) = \|B b\|_1 / \|b\|_1$. Finally $\|B v\|_1 \le \|B\|_1 \|v\|_1$. $\square$

**Lemma 3 (the maximum is at a vertex).** $\max_{\|w\|_1 \le 1} f(w) = \max_j f(e_j) = \|B\|_1$.

*Proof.* $f$ is convex (a norm composed with a linear map), and every $w$ with $\|w\|_1 \le 1$ is a convex combination of the points $\pm e_j$ (and $0$): $w = \sum_j |w_j| \operatorname{sign}(w_j) e_j + (1 - \|w\|_1) \cdot 0$. So $f(w) \le \max_j f(\pm e_j) = \max_j \|B e_j\|_1$, the largest column sum. $\square$

**Theorem 4 (strict ascent).** If $\|z\|_\infty > z^T x$ and $j$ is chosen in line L7, then $f(e_j) > f(x)$.

*Proof.* By Lemma 1 with $w = \operatorname{sign}(z_j) e_j$, $f(e_j) = f(w) \ge |z_j| = \|z\|_\infty > z^T x = f(x)$. $\square$

**Theorem 5 (local maximum, Hager).** If $\|z\|_\infty \le z^T x$, $\|x\|_1 = 1$, and $y = B x$ has no zero entry, then there is a neighbourhood $N$ of $x$ such that $f(w) \le f(x)$ for all $w \in N$ with $\|w\|_1 \le 1$.

*Proof.* By continuity there is a neighbourhood $N$ on which $\operatorname{sign}(B w) = \xi$, and there $f(w) = \xi^T B w = z^T w \le \|z\|_\infty \|w\|_1 \le \|z\|_\infty \le z^T x = f(x)$. $\square$

**Theorem 6 (termination).** Hager's form stops after at most $n + 1$ iterations, and Higham's after at most $t$.

*Proof.* Higham's loop has the explicit bound $t$. In Hager's form, from the second iteration on $x$ is some $e_j$. If the test of line L8 fails at iteration $k$, Theorem 4 gives $f(x_{k+1}) > f(x_k)$, so the values $f(x_2) < f(x_3) < \cdots$ are strictly increasing and the vertices $x_2, x_3, \ldots$ are distinct. There are $n$ unit vectors, so at most $n$ iterations follow the first. $\square$

**Remark (failure of the stopping test at the start).** For $B = I - (1 - \delta) e e^T/n$ with $0 < \delta < 1$, $B e = \delta e$, so with $x = e/n$, $y = \delta e/n$, $\xi = e$, $z = B^T e = \delta e$ and $\|z\|_\infty = \delta = z^T x$. Hager's form stops with $\gamma = \delta$, while $\|B\|_1 = 1 - (1 - \delta)/n + (n - 1)(1 - \delta)/n \ge 2(n-1)(1 - \delta)/n$. So no positive lower bound on $\gamma / \|B\|_1$ holds. $\blacksquare$
