---
title: The Laguerre recurrence gives the Gauss-Laguerre rule, the log-weight computation is exact up to rounding, and the rule has degree 2n-1 with an error bound on the half-line
proves: [correctness, error]
status: full
---

We use the notation of the page: $w(x) = x^a e^{-x}$ on $(0, \infty)$ with $a > -1$, monic orthogonal polynomials $\pi_k$ with $\pi_{k+1} = (x - \alpha_k)\pi_k - \beta_k\pi_{k-1}$, $\beta_0 = \int w$, and $n \ge 1$.

## Claim 1: the weight is admissible, and $\beta_0$

$w$ is positive and continuous on $(0, \infty)$. Its moments are $\int_0^\infty x^{k+a}e^{-x}\,dx = \Gamma(k + a + 1)$, finite because $k + a > -1$. So the hypotheses of the [Gauss quadrature theorem](/gauss-quadrature-theorem/) hold, and $\beta_0 = \Gamma(a + 1)$, which line L2 keeps as $\log\Gamma(a + 1)$.

## Claim 2: the recurrence coefficients

The generalized Laguerre polynomials $L_k = L_k^{(a)}$ are orthogonal for $w$, have leading coefficient $(-1)^k/k!$, and satisfy (Szegő, *Orthogonal Polynomials*, Section 5.1)

$$(k + 1)L_{k+1} = (2k + a + 1 - x)L_k - (k + a)L_{k-1}, \qquad k \ge 1,$$

with $L_0 = 1$, $L_1 = 1 + a - x$. The monic polynomials are $\pi_k = (-1)^k k!\, L_k$. Multiplying the recurrence by $(-1)^{k+1}k!$,

$$\pi_{k+1} = (x - (2k + a + 1))\,(-1)^k k!\,L_k + (-1)^k k!\,(k + a)\,L_{k-1} = (x - (2k + a + 1))\,\pi_k - k(k + a)\,\pi_{k-1},$$

because $(-1)^k k!\,L_{k-1} = -k\,\pi_{k-1}$. Also $\pi_1 = x - (a + 1)$. By uniqueness of the monic recurrence, $\alpha_k = 2k + a + 1$ and $\beta_k = k(k + a) > 0$ for $k \ge 1$, which is line L2.

## Claim 3: the eigen-computation returns the Gauss rule

The characteristic polynomial of the Jacobi matrix $J_n$ of line L3 is $\pi_n$, so its eigenvalues are the Gauss nodes; Sturm-count bisection finds them in increasing order (line L4). For an eigenvalue $x_j$ the eigenvector with $v_0 = 1$ has components $v_k = \sqrt{\beta_0}\,p_k(x_j)$, with $p_k$ the orthonormal polynomials, because both follow the same recurrence. The rows of the orthogonal eigenvector matrix $V$ are orthonormal, so with $\mu_j = \beta_0/\|v^{(j)}\|^2$,

$$\sum_j \mu_j\,p_k(x_j)\,p_l(x_j) = (VV^T)_{kl} = \delta_{kl} \qquad (k, l < n).$$

Hence the rule $(x_j, \mu_j)$ is exact on all polynomials of degree at most $2n - 2$, in particular on the Lagrange basis polynomials, and $\mu_j$ is the Gauss weight; this is the [Golub-Welsch](/golub-welsch-algorithm/) theorem. In line L5 the recurrence is linear and homogeneous; whenever $|v_k| > 10^{100}$ the code multiplies $v_k$ and $v_{k-1}$ by $10^{-100}$, the stored squares by $10^{-200}$, and adds $100\log 10$ to a running scale. The result is the true $\|v^{(j)}\|^2$ times a known power of $10^{-200}$, so $\log\mu_j = \log\beta_0 - \log\|v^{(j)}\|^2$ is computed without overflow even when $\mu_j$ itself is below the underflow threshold.

## Claim 4: degree, positivity, and the error bound

By the Gauss quadrature theorem the rule is exact for every polynomial of degree at most $2n - 1$, is not exact for $\pi_n^2$, has simple nodes in $(0, \infty)$, and has positive weights. Moreover $\|\pi_n\|^2 = \beta_0\beta_1\cdots\beta_n = \Gamma(a + 1)\prod_{k=1}^n k(k + a) = n!\,\Gamma(n + a + 1)$.

Let $f \in C^{2n}[0, \infty)$ with $|f^{(2n)}| \le M$ and $\int |f|\,w < \infty$. Let $h$ be the Hermite interpolant of degree at most $2n - 1$ matching $f$ and $f'$ at the $n$ nodes. Then

$$f(x) - h(x) = f[x_1, x_1, \ldots, x_n, x_n, x]\,\pi_n(x)^2,$$

and the divided difference is $f^{(2n)}(\eta_x)/(2n)!$ for some $\eta_x \in (0, \infty)$, so it is bounded by $M/(2n)!$. Since $Q_n(f) = Q_n(h) = I(h)$,

$$|E_n(f)| = \Bigl|\int_0^\infty (f - h)\,w\Bigr| \le \frac{M}{(2n)!}\int_0^\infty \pi_n^2\,w = \frac{M\,n!\,\Gamma(n + a + 1)}{(2n)!}.$$

If in addition $f^{(2n)} \ge 0$ on $(0, \infty)$, the integrand $(f - h)w$ is nonnegative and $E_n(f) \ge 0$. For $f = x^{2n}$ the divided difference is identically $1$, so $E_n(x^{2n}) = n!\,\Gamma(n + a + 1)$ exactly; the test file checks this against the computed rule. $\blacksquare$
