---
title: Correctness of iterative shrinkage-thresholding
proves: [correctness]
status: full
---

We prove that the fixed points of the iteration are exactly the minimizers of $F(x) = \tfrac12\|Ax - y\|_2^2 + \lambda\|x\|_1$, that the objective gap after $k$ steps is at most $L\|x_0 - x^*\|^2/(2k)$, that the iterates converge to a minimizer, and that under strict complementarity the zero entries and the signs are found in finitely many steps, after which convergence is linear.

## Setup

Let $A \in \mathbb R^{m \times n}$, $y \in \mathbb R^m$, $\lambda > 0$ and $L \ge \lambda_{\max}(A^{\mathsf T}A)$. Write $f(x) = \tfrac12\|Ax - y\|^2$, so $\nabla f(x) = A^{\mathsf T}(Ax - y)$, and $c(x) = -\nabla f(x) = A^{\mathsf T}(y - Ax)$. One pass of lines L3 to L5 is the map

$$T(x) = S_{\lambda/L}\big(x + c(x)/L\big),$$

and $x_{k+1} = T(x_k)$. Let $F^*$ be the minimum of $F$; it exists because $F$ is continuous and $F(x) \ge \lambda\|x\|_1$ tends to infinity with $\|x\|$.

## Lemma 1 (soft thresholding as a subgradient condition)

For $t \ge 0$ and real $v$, $p = S_t(v)$ if and only if $v - p \in t\,\partial|p|$, where $\partial|p| = \{\operatorname{sign} p\}$ for $p \ne 0$ and $\partial|0| = [-1, 1]$.

*Proof.* If $|v| \le t$, then $p = 0$ and $v - p = v \in [-t, t]$. If $v > t$, then $p = v - t > 0$ and $v - p = t$. The case $v < -t$ is symmetric. So $S_t(v)$ satisfies the condition. It is the only solution, since the condition says that $p$ minimizes the strictly convex function $\tfrac12(u - v)^2 + t|u|$. $\square$

Applied entry by entry with $t = \lambda/L$ and $v = x + c(x)/L$, Lemma 1 says that $x^+ = T(x)$ is characterized by

$$L(x - x^+) - \nabla f(x) \in \lambda\,\partial\|x^+\|_1. \tag{1}$$

## Theorem 1 (fixed points are the minimizers)

For every $L > 0$, $T(x) = x$ if and only if $x$ minimizes $F$.

*Proof.* By (1) with $x^+ = x$, $T(x) = x$ exactly when $-\nabla f(x) \in \lambda\,\partial\|x\|_1$, that is, $0 \in \nabla f(x) + \lambda\,\partial\|x\|_1 = \partial F(x)$. Entry by entry this reads $c_j(x) = \lambda\operatorname{sign} x_j$ when $x_j \ne 0$ and $|c_j(x)| \le \lambda$ when $x_j = 0$. Since $F$ is convex, $0 \in \partial F(x)$ is the same as $x$ being a minimizer. The value of $L$ does not appear in the condition. $\square$

**Corollary (the zero threshold).** $0$ minimizes $F$ if and only if $\|A^{\mathsf T}y\|_\infty \le \lambda$, because $c(0) = A^{\mathsf T}y$. In that case $T(0) = 0$, so the run from $x_0 = 0$ stays at $0$.

## Lemma 2 (one step)

Let $x^+ = T(x)$. For every $z \in \mathbb R^n$,

$$F(x^+) \le F(z) + \frac L2\big(\|x - z\|^2 - \|x^+ - z\|^2\big).$$

*Proof.* Write $g = \nabla f(x)$. Since $f$ is quadratic,

$$f(x^+) = f(x) + \langle g, x^+ - x\rangle + \tfrac12\|A(x^+ - x)\|^2 \le f(x) + \langle g, x^+ - x\rangle + \tfrac L2\|x^+ - x\|^2,$$

because $\|Ad\|^2 \le \lambda_{\max}(A^{\mathsf T}A)\|d\|^2 \le L\|d\|^2$. Also $f(z) \ge f(x) + \langle g, z - x\rangle$ by convexity. By (1), $w = L(x - x^+) - g$ is a subgradient of $\|\cdot\|_1$ at $x^+$ times $\lambda$, so $\lambda\|z\|_1 \ge \lambda\|x^+\|_1 + \langle w, z - x^+\rangle$. Adding the three inequalities, the terms with $g$ cancel:

$$F(x^+) \le F(z) + \tfrac L2\|x^+ - x\|^2 + L\langle x - x^+, x^+ - z\rangle.$$

The identity $\|x - z\|^2 = \|x - x^+\|^2 + \|x^+ - z\|^2 + 2\langle x - x^+, x^+ - z\rangle$ turns the last two terms into $\tfrac L2(\|x - z\|^2 - \|x^+ - z\|^2)$. $\square$

## Theorem 2 (monotone decrease and the gap bound)

$F(x_{k+1}) \le F(x_k)$ for every $k$, and for every minimizer $x^*$ and every $k \ge 1$,

$$F(x_k) - F^* \le \frac{L\|x_0 - x^*\|^2}{2k}.$$

*Proof.* Lemma 2 with $z = x_k$ gives $F(x_{k+1}) \le F(x_k) - \tfrac L2\|x_{k+1} - x_k\|^2 \le F(x_k)$. Lemma 2 with $z = x^*$ gives

$$F(x_{i+1}) - F^* \le \tfrac L2\big(\|x_i - x^*\|^2 - \|x_{i+1} - x^*\|^2\big).$$

Summing over $i = 0, \ldots, k - 1$, the right side telescopes to at most $\tfrac L2\|x_0 - x^*\|^2$. The left side is a sum of $k$ terms, and by the first part the smallest is the last one, $F(x_k) - F^*$. So $k(F(x_k) - F^*) \le \tfrac L2\|x_0 - x^*\|^2$. $\square$

The inequality with $z = x^*$ also shows $\|x_{i+1} - x^*\| \le \|x_i - x^*\|$, since its left side is nonnegative. We use this below.

## Theorem 3 (the iterates converge)

The sequence $x_k$ converges to a minimizer of $F$.

*Proof.* Fix a minimizer $x^*$. The distances $\|x_k - x^*\|$ do not grow, so the sequence is bounded and has a convergent subsequence $x_{k_i} \to \bar x$. By Theorem 2, $F(x_k) \to F^*$, and $F$ is continuous, so $F(\bar x) = F^*$ and $\bar x$ is a minimizer. Apply the distance property to the minimizer $\bar x$: $\|x_k - \bar x\|$ does not grow, and it tends to $0$ along the subsequence, so it tends to $0$. $\square$

## Theorem 4 (finite identification and the local rate)

Let $x^*$ be the limit and $c^* = c(x^*)$. Let $Z = \{j : x^*_j = 0\}$ and $S$ be the rest, and assume strict complementarity: $|c^*_j| < \lambda$ for all $j \in Z$. Then there is a $K$ such that for all $k \ge K$, $x_{k,j} = 0$ for $j \in Z$ and $\operatorname{sign} x_{k,j} = \operatorname{sign} x^*_j$ for $j \in S$. From then on,

$$x_{k+1,S} - x^*_S = \Big(I - \tfrac1L A_S^{\mathsf T}A_S\Big)(x_{k,S} - x^*_S),$$

so if $A_S$ has full column rank, the error falls by at least the factor $1 - \mu_{\min}/L < 1$ per step, where $\mu_{\min}$ is the smallest eigenvalue of $A_S^{\mathsf T}A_S$.

*Proof.* The map $x \mapsto x + c(x)/L$ is continuous, so $v_k = x_k + c(x_k)/L \to x^* + c^*/L$. For $j \in Z$, the limit of $v_{k,j}$ is $c^*_j/L$, which lies in the open interval $(-\lambda/L, \lambda/L)$, so $|v_{k,j}| < \lambda/L$ and $x_{k+1,j} = 0$ for all large $k$. For $j \in S$, $x_{k,j} \to x^*_j \ne 0$, so $x_{k,j}$ has the sign $\sigma_j$ of $x^*_j$ for all large $k$, and so does $x_{k+1,j}$. Take $K$ past all these finitely many thresholds.

For $k \ge K$, the zero entries do not enter $Ax_k$, and for $j \in S$, line L5 subtracts $\sigma_j\lambda/L$. So

$$x_{k+1,S} = x_{k,S} + \tfrac1L\big(A_S^{\mathsf T}(y - A_S x_{k,S}) - \lambda\sigma_S\big).$$

The fixed point $x^*$ satisfies the same equation, by Theorem 1, and subtracting gives the stated recursion. The matrix $I - A_S^{\mathsf T}A_S/L$ is symmetric with eigenvalues $1 - \mu/L$ for the eigenvalues $\mu$ of $A_S^{\mathsf T}A_S$. These lie in $[0, L]$, so the eigenvalues of the matrix lie in $[0, 1 - \mu_{\min}/L]$, and its norm is $1 - \mu_{\min}/L$. $\square$

## Remark (penalty to zero)

If $y = Az$ for some $z$, let $x_\lambda$ minimize $F$ for the penalty $\lambda$, and let $\hat x$ solve basis pursuit, $\min\|x\|_1$ subject to $Ax = y$. Then $F(x_\lambda) \le F(\hat x) = \lambda\|\hat x\|_1$ gives $\|x_\lambda\|_1 \le \|\hat x\|_1$ and $\tfrac12\|Ax_\lambda - y\|^2 \le \lambda\|\hat x\|_1$. So the $x_\lambda$ are bounded, and every limit point $\bar x$ as $\lambda \to 0$ has $A\bar x = y$ and $\|\bar x\|_1 \le \|\hat x\|_1$, so it solves basis pursuit.
