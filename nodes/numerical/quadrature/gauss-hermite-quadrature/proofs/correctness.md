---
title: The Hermite recurrence gives the Gauss-Hermite rule, the symmetrized log-weight computation is correct, and the rule has degree 2n-1 with an error bound on the real line
proves: [correctness, error]
status: full
---

We use the notation of the page: $w(x) = e^{-x^2}$ on $(-\infty, \infty)$, monic orthogonal polynomials $\pi_k$ with $\pi_{k+1} = (x - \alpha_k)\pi_k - \beta_k\pi_{k-1}$, $\beta_0 = \int w$, and $n \ge 1$.

## Claim 1: the weight is admissible, and the coefficients

$w$ is positive and continuous, and its moments $\int x^k e^{-x^2}dx$ are $0$ for odd $k$ and $\Gamma(\frac{k+1}{2})$ for even $k$, all finite. So the hypotheses of the [Gauss quadrature theorem](/gauss-quadrature-theorem/) hold, and $\beta_0 = \Gamma(\frac12) = \sqrt\pi$.

The physicists' Hermite polynomials $H_k$ are orthogonal for $w$, have leading coefficient $2^k$, and satisfy $H_{k+1} = 2xH_k - 2kH_{k-1}$ with $H_0 = 1$, $H_1 = 2x$ (Szegő, *Orthogonal Polynomials*, Section 5.5). Dividing by $2^{k+1}$, the monic $\pi_k = H_k/2^k$ satisfy

$$\pi_{k+1} = x\,\pi_k - \frac{2k}{4}\,\pi_{k-1} = x\,\pi_k - \frac{k}{2}\,\pi_{k-1}.$$

By uniqueness of the monic recurrence, $\alpha_k = 0$ and $\beta_k = \frac{k}{2} > 0$, which is line L2.

## Claim 2: the eigen-computation returns the Gauss rule

The characteristic polynomial of the Jacobi matrix $J_n$ of line L3 is $\pi_n$, so its eigenvalues are the Gauss nodes; Sturm-count bisection finds them in increasing order (line L4). For an eigenvalue $x_j$, the eigenvector with $v_0 = 1$ has components $v_k = \sqrt{\beta_0}\,p_k(x_j)$, with $p_k$ the orthonormal polynomials, because both follow the same recurrence. The rows of the orthogonal eigenvector matrix $V$ are orthonormal, so with $\mu_j = \beta_0/\|v^{(j)}\|^2$,

$$\sum_j \mu_j\,p_k(x_j)\,p_l(x_j) = (VV^T)_{kl} = \delta_{kl} \qquad (k, l < n).$$

Hence the rule $(x_j, \mu_j)$ is exact on all polynomials of degree at most $2n - 2$, in particular on the Lagrange basis polynomials of its nodes, and $\mu_j$ is the Gauss weight (the [Golub-Welsch](/golub-welsch-algorithm/) theorem). Line L5 rescales $v$ by $10^{-100}$ whenever $|v| > 10^{100}$, the stored squares by $10^{-200}$, and records the scale in a logarithm. The recurrence is linear and homogeneous, so the log weight $\log\beta_0 - \log\|v^{(j)}\|^2$ is unchanged by the rescaling, and it is finite even when $\mu_j$ underflows.

## Claim 3: the symmetrization

Since $\alpha_k = 0$, induction on the recurrence gives $\pi_k(-x) = (-1)^k\pi_k(x)$. So the zeros of $\pi_n$ are symmetric about $0$, and $0$ is a zero when $n$ is odd. The weights satisfy $\lambda(-x_j) = \lambda(x_j)$, because $\lambda_j = 1/\sum_{k<n} p_k(x_j)^2$ (the Christoffel formula, equivalent to the eigenvector formula of Claim 2) and $p_k(-x)^2 = p_k(x)^2$. Line L6 replaces each computed pair of nodes $(\hat x_j, \hat x_{n+1-j})$ by $\pm\frac12(\hat x_{n+1-j} - \hat x_j)$ and the pair of log weights by their mean, and sets the middle node to $0$ when $n$ is odd. If $|\hat x_j - x_j| \le \epsilon$ and $|\hat x_{n+1-j} - x_{n+1-j}| \le \epsilon$, then with $x_{n+1-j} = -x_j$ the average differs from the exact node by at most $\epsilon$; the same holds for the log weights. So line L6 never increases the error bound, and it makes the computed rule exactly symmetric, so odd integrands integrate to exactly $0$.

## Claim 4: degree, positivity, and the error bound

By the Gauss quadrature theorem the rule is exact for every polynomial of degree at most $2n - 1$, is not exact for $\pi_n^2$, has simple real nodes, and has positive weights. Moreover $\|\pi_n\|^2 = \beta_0\beta_1\cdots\beta_n = \sqrt\pi\,\prod_{k=1}^n \frac{k}{2} = \frac{\sqrt\pi\,n!}{2^n}$.

Let $f \in C^{2n}(\mathbb R)$ with $|f^{(2n)}| \le M$ and $\int |f|\,w < \infty$. Let $h$ be the Hermite interpolant of degree at most $2n - 1$ matching $f$ and $f'$ at the $n$ nodes. Then $f(x) - h(x) = f[x_1, x_1, \ldots, x_n, x_n, x]\,\pi_n(x)^2$, and the divided difference is $f^{(2n)}(\eta_x)/(2n)!$ for some real $\eta_x$, so it is bounded by $M/(2n)!$. Since $Q_n(f) = Q_n(h) = I(h)$,

$$|E_n(f)| = \Bigl|\int_{-\infty}^\infty (f - h)\,w\Bigr| \le \frac{M}{(2n)!}\int_{-\infty}^\infty \pi_n^2\,w = \frac{\sqrt\pi\,n!}{2^n\,(2n)!}\,M.$$

If $f^{(2n)} \ge 0$ everywhere, the integrand $(f - h)w$ is nonnegative and $E_n(f) \ge 0$. For $f = x^{2n}$ the divided difference is identically $1$ and $E_n(x^{2n}) = \frac{\sqrt\pi\,n!}{2^n}$ exactly; the test file checks this against the computed rule. $\blacksquare$
