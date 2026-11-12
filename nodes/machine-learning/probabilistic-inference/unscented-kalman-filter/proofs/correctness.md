---
title: The unscented transform matches the first two moments, is exact for linear maps, and gets the mean right to third order
proves: [correctness]
status: full
---

Notation as on the page. The state has dimension $n$, $x \sim \mathcal N(m, P)$ with $P$ positive definite, $\lambda = \alpha^2 (n + \kappa) - n$ and $c = n + \lambda > 0$. Let $L$ satisfy $L L^\top = c P$ (for example the Cholesky factor) and let $\ell_1, \ldots, \ell_n$ be its columns. The sigma points are $X_0 = m$, $X_j = m + \ell_j$ and $X_{n+j} = m - \ell_j$ for $j = 1, \ldots, n$. The weights are $W^m_0 = \lambda / c$, $W^c_0 = \lambda / c + 1 - \alpha^2 + \beta$ and $W^m_i = W^c_i = 1/(2c)$ for $i \ge 1$. The transform of a map $g$ returns
$$\hat\mu = \sum_i W^m_i g(X_i), \qquad \hat S = \sum_i W^c_i (g(X_i) - \hat\mu)(g(X_i) - \hat\mu)^\top, \qquad \hat C = \sum_i W^c_i (X_i - m)(g(X_i) - \hat\mu)^\top.$$
The unscented Kalman filter (UKF) is no more exact than the transform it uses, so the statements below are about the transform, plus the linear case of the filter.

**Lemma 1 (moments of the points).** Let $d_i = X_i - m$. Then $\sum_i W^m_i = 1$, $\sum_i W^m_i d_i = 0$, $\sum_i W^m_i d_i d_i^\top = P$, and every odd moment $\sum_i W^m_i d_i^{\otimes k}$, $k$ odd, is zero. The same holds with $W^c$ in place of $W^m$ for the moments of order $k \ge 1$, because $d_0 = 0$.

*Proof.* $\sum_i W^m_i = \lambda / c + 2n / (2c) = (\lambda + n)/c = 1$. The points come in pairs $m \pm \ell_j$ with equal weights, and $d_0 = 0$, so each odd moment cancels in pairs. For the second moment, $\sum_{i \ge 1} W^m_i d_i d_i^\top = \frac{1}{2c} \sum_j 2 \ell_j \ell_j^\top = \frac1c L L^\top = P$. The weights of $W^c$ differ from those of $W^m$ only at $i = 0$, where $d_0 = 0$. $\square$

**Claim 1 (exact for affine maps).** If $g(x) = A x + b$, then $\hat\mu = A m + b$, $\hat S = A P A^\top$ and $\hat C = P A^\top$, which are the true mean of $g(x)$, its covariance and $\mathrm{Cov}(x, g(x))$.

*Proof.* $g(X_i) = A m + b + A d_i$. By Lemma 1, $\hat\mu = (A m + b) \sum_i W^m_i + A \sum_i W^m_i d_i = A m + b$. So $g(X_i) - \hat\mu = A d_i$, and $\hat S = A (\sum_i W^c_i d_i d_i^\top) A^\top = A P A^\top$ and $\hat C = (\sum_i W^c_i d_i d_i^\top) A^\top = P A^\top$. The true values follow from the linearity of expectation. $\square$

**Claim 2 (the mean is exact for polynomials of degree at most 3).** If each component of $g$ is a polynomial of degree at most $3$, then $\hat\mu = \mathbb E g(x)$. In particular the mean is exact for every quadratic map.

*Proof.* Expand $g$ around $m$: $g(m + d) = g(m) + J d + \frac12 G[d, d] + \frac16 T[d, d, d]$, exactly, where $J$, $G$ and $T$ are the first three derivative tensors at $m$. The transform weights this with $W^m$, and the expectation weights it with the law of $d \sim \mathcal N(0, P)$. Both have total mass $1$, mean $0$, second moment $P$ and zero third moment (Lemma 1, and the symmetry of the Gaussian). The four terms are linear in these moments, so the two results are equal; both are $g(m) + \frac12 \sum_{k,l} G_{\cdot kl} P_{kl}$. $\square$

For a general smooth $g$ the same argument shows that $\hat\mu$ and $\mathbb E g(x)$ agree in all Taylor terms of order at most $3$ and can differ from order $4$ on. The extended Kalman filter, which uses $g(m)$, misses the second-order term $\frac12 \mathrm{tr}(G P)$. If the points also match the fourth moments, the agreement goes further: in one dimension $\sum_i W^m_i d_i^4 = 2 \cdot \frac{1}{2c} (c P)^2 = c P^2$, which equals the Gaussian value $3 P^2$ exactly when $c = 3$. That is the reason for the default $\kappa = 3 - n$, which gives $c = 3$ when $\alpha = 1$; in one dimension the mean is then exact for polynomials of degree at most $5$.

**Claim 3 (the variance of a square).** Let $n = 1$ and $g(x) = x^2$. Then $\hat\mu = m^2 + P$, which is exact, and
$$\hat S = 4 m^2 P + (\alpha^2 \kappa + \beta) P^2,$$
while the true variance is $4 m^2 P + 2 P^2$. So the transform gives the exact variance if and only if $\alpha^2 \kappa + \beta = 2$, for example with $\alpha = 1$, $\beta = 0$, $\kappa = 2$, or with $\kappa = 0$ and $\beta = 2$ for every $\alpha$.

*Proof.* The points are $m$ and $m \pm s$ with $s = \sqrt{cP}$. The images are $m^2$ and $m^2 \pm 2 m s + c P$. Then $\hat\mu = W^m_0 m^2 + \frac{1}{c}(m^2 + cP) = m^2 + P$ because $W^m_0 + 1/c = 1$. The deviations are $-P$ at the centre and $\pm 2 m s + (c - 1) P$ at the outer points. So
$$\hat S = W^c_0 P^2 + \frac{1}{2c}\Bigl[2 \cdot 4 m^2 c P + 2 (c-1)^2 P^2\Bigr] = 4 m^2 P + \Bigl(W^c_0 + \frac{(c-1)^2}{c}\Bigr) P^2.$$
With $W^c_0 = 1 - 1/c + 1 - \alpha^2 + \beta$, the coefficient is $2 - \frac1c - \alpha^2 + \beta + c - 2 + \frac1c = c - \alpha^2 + \beta$, and $c = \alpha^2(1 + \kappa)$ gives $\alpha^2 \kappa + \beta$. The true variance is $\mathbb E x^4 - (\mathbb E x^2)^2 = (m^4 + 6 m^2 P + 3P^2) - (m^2 + P)^2 = 4 m^2 P + 2 P^2$. $\square$

The term $\beta$ adds weight to the centre point in the covariance only, and corrects the fourth-moment error of the points without changing the mean. For a Gaussian prior $\beta = 2$ is the best choice in this sense.

**Claim 4 (the UKF is the Kalman filter on linear models).** If $f(x) = A x$ and $h(x) = H x$, the UKF returns the Kalman filter means and covariances at every step, which are the exact filtering moments.

*Proof.* By Claim 1, line L3 gives $m^- = A m$ and $P^- = A P A^\top + Q$. Line L4, applied to the new points from $(m^-, P^-)$, gives $\hat\mu = H m^-$, $S = H P^- H^\top + R$ and $C = P^- H^\top$. Then $K = C S^{-1} = P^- H^\top S^{-1}$, and line L6 is the Kalman update. By induction on $t$ the outputs agree with the Kalman filter, which is exact for this model. $\square$

**Cost.** Each transform needs one Cholesky factorization, $O(n^3)$, the $2n + 1$ function evaluations, and the weighted sums, $O(n k^2 + n^2 k)$ for an output of dimension $k$. The update adds an $m \times m$ solve. A filter step costs $O(n^3 + n^2 m + n m^2 + m^3)$ plus $2(2n + 1)$ function evaluations.
