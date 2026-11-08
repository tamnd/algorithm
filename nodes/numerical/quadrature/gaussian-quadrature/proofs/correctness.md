---
title: Sturm bisection on the Jacobi matrix finds the Gauss nodes, and the Christoffel formula gives the Gauss weights
proves: [correctness, termination]
status: full
---

We use the notation of the page. The weight $w$ satisfies the hypotheses of the [Gauss quadrature theorem](/gauss-quadrature-theorem/), $\pi_k$ are its monic orthogonal polynomials, and

$$\pi_{k+1}(x) = (x - \alpha_k)\pi_k(x) - \beta_k \pi_{k-1}(x), \qquad \pi_0 = 1,\ \pi_{-1} = 0,\ \beta_0 = \int_a^b w,$$

with $\beta_k = \langle \pi_k, \pi_k \rangle / \langle \pi_{k-1}, \pi_{k-1} \rangle > 0$ for $k \ge 1$. The orthonormal polynomials are $p_k = \pi_k / \sqrt{\beta_0 \beta_1 \cdots \beta_k}$; they satisfy $p_0 = 1/\sqrt{\beta_0}$ and $\sqrt{\beta_{k+1}}\, p_{k+1} = (x - \alpha_k) p_k - \sqrt{\beta_k}\, p_{k-1}$, which is the recurrence of line L9. $J_n$ is the symmetric tridiagonal matrix with diagonal $\alpha_0, \ldots, \alpha_{n-1}$ and off-diagonal $\sqrt{\beta_1}, \ldots, \sqrt{\beta_{n-1}}$.

The statements are in exact arithmetic unless floating point is named.

## Claim 1: the eigenvalues of $J_n$ are the Gauss nodes

Let $D_k(x) = \det(x I - J_k)$, with $J_k$ the leading $k \times k$ block of $J_n$. Expanding along the last row gives $D_{k+1} = (x - \alpha_k) D_k - \beta_k D_{k-1}$, with $D_0 = 1$ and $D_1 = x - \alpha_0$. This is the recurrence of $\pi_k$ with the same start, so $D_n = \pi_n$. The Gauss nodes are the zeros of $\pi_n$ (part 1 of the theorem), so they are the eigenvalues of $J_n$. They are real and distinct: $J_n$ is real symmetric, and an unreduced tridiagonal matrix (all off-diagonal entries nonzero) has simple eigenvalues, since $J_n - \lambda I$ with its first row and last column removed is triangular with a nonzero diagonal, so it has rank at least $n - 1$.

## Claim 2: COUNT(x) is the number of nodes below x

Fix $x$ that is not an eigenvalue of any leading block $J_k$. Gaussian elimination without pivoting on $J_n - xI$ gives $J_n - xI = L D L^T$ with $L$ unit lower bidiagonal and $D = \operatorname{diag}(d_0, \ldots, d_{n-1})$, where

$$d_0 = \alpha_0 - x, \qquad d_k = (\alpha_k - x) - \frac{\beta_k}{d_{k-1}}.$$

This is the loop of `sturm_count`. Indeed $d_k = \det(J_{k+1} - xI)/\det(J_k - xI)$, which is never $0$ under the assumption on $x$. By Sylvester's law of inertia, $D$ and $J_n - xI$ have the same number of negative entries and eigenvalues, so the number of negative $d_k$ is the number of eigenvalues of $J_n$ below $x$. When some $d_k = 0$, the code replaces it by $-10^{-300}$; this is the count for an $x$ that is moved by an amount below any floating-point resolution, and the count is a nondecreasing step function of $x$ in exact arithmetic either way. In floating point the computed count is the exact count for a matrix whose entries differ from those of $J_n$ by a small multiple of the unit roundoff (Kahan's analysis of the Sturm count; see [the Sturm sequence count](/sturm-sequence-eigenvalue-count/)), so each node is found with an absolute error of order $u\,\|J_n\|$.

## Claim 3: bisection brackets the j-th node and stops

Let $x_0 < \cdots < x_{n-1}$ be the nodes. Line L2 sets $[lo, hi]$ to the Gershgorin interval, widened slightly; every eigenvalue lies inside it, so $\mathrm{COUNT}(lo) = 0$ and $\mathrm{COUNT}(hi) = n$.

*Invariant.* In the loop for index $j$: $\mathrm{COUNT}(l) \le j$ and $\mathrm{COUNT}(r) \ge j + 1$. Then fewer than $j + 1$ nodes lie below $l$ and at least $j + 1$ lie below $r$, so $l \le x_j < r$.

*Initialization.* For $j = 0$, $l = lo$ and $r = hi$. For $j \ge 1$, the code starts at $l = \max(lo, x_{j-1}')$ with $x_{j-1}'$ the computed previous node. In exact arithmetic $x_{j-1}' = x_{j-1} < x_j$, so $\mathrm{COUNT}(l) \le j$.

*Maintenance.* Line L7 sets $r \leftarrow m$ when $\mathrm{COUNT}(m) \ge j + 1$ and $l \leftarrow m$ otherwise, which keeps both halves of the invariant.

*Termination.* Each pass halves $r - l$. The loop stops when $r - l \le 4u\max(|l|, |r|)$ or $r - l \le u^2 (hi - lo)$, or when the midpoint is no longer strictly inside. Starting from the width $hi - lo$, the second test alone stops it after at most $\lceil \log_2 u^{-2} \rceil + 1 = 107$ passes. So each node costs at most 107 counts.

## Claim 4: the Christoffel formula gives the Gauss weights

Let $\lambda_0, \ldots, \lambda_{n-1}$ be the Gauss weights and let $P$ be the $n \times n$ matrix with $P_{kj} = p_k(x_j)$. For $k, m < n$, the product $p_k p_m$ has degree at most $2n - 2$, so the Gauss rule integrates it exactly (part 2 of the theorem):

$$\sum_j \lambda_j\, p_k(x_j)\, p_m(x_j) = \langle p_k, p_m \rangle = \delta_{km}.$$

In matrix form $P \Lambda P^T = I$ with $\Lambda = \operatorname{diag}(\lambda_j)$. So $P$ is invertible, $P^T = \Lambda^{-1} P^{-1}$, and $P^T P = \Lambda^{-1}$. The diagonal entry $j$ reads $\sum_{k<n} p_k(x_j)^2 = 1/\lambda_j$, which is line L10. All terms are squares and $p_0^2 = 1/\beta_0 > 0$, so the sum is positive and the weight is well defined.

## Conclusion

By Claims 1 to 3 the loop of line L3 returns the $n$ zeros of $\pi_n$ in increasing order, and by Claim 4 line L10 returns their Gauss weights. By the Gauss quadrature theorem the returned rule has degree of precision $2n - 1$ for $w$. $\blacksquare$
