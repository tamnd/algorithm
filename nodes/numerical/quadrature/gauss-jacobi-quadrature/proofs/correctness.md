---
title: The Jacobi recurrence coefficients are correct, the eigen-computation returns the Gauss-Jacobi rule, and the rule has degree 2n-1 with a definite error term
proves: [correctness, error]
status: full
---

We use the notation of the page: $w(x) = (1 - x)^a (1 + x)^b$ on $(-1, 1)$ with $a, b > -1$, monic orthogonal polynomials $\pi_k$ with $\pi_{k+1} = (x - \alpha_k)\pi_k - \beta_k \pi_{k-1}$, $\beta_0 = \int w$, and $n \ge 1$.

## Claim 1: the weight is admissible, and $\beta_0$

$w$ is positive and continuous on $(-1, 1)$. Near $x = 1$ it behaves like $(1 - x)^a$ with $a > -1$, near $x = -1$ like $(1 + x)^b$ with $b > -1$, so all moments $\int x^k w$ are finite. Hence $w$ satisfies the hypotheses of the [Gauss quadrature theorem](/gauss-quadrature-theorem/). Substituting $x = 2t - 1$,

$$\beta_0 = \int_{-1}^1 (1 - x)^a (1 + x)^b\,dx = 2^{a+b+1}\int_0^1 (1 - t)^a t^b\,dt = 2^{a+b+1}\,\frac{\Gamma(a+1)\Gamma(b+1)}{\Gamma(a+b+2)},$$

which line L2 evaluates with `lgamma` to avoid overflow.

## Claim 2: $\alpha_0$ and $\beta_1$

Under the substitution, $w/\beta_0$ is the density of $x = 2t - 1$ where $t$ has the Beta$(b + 1, a + 1)$ distribution, whose mean is $\frac{b+1}{a+b+2}$ and variance $\frac{(a+1)(b+1)}{(a+b+2)^2(a+b+3)}$. Since $\pi_1 = x - \alpha_0$ is orthogonal to $1$, $\alpha_0$ is the mean of $x$: $\alpha_0 = \frac{2(b+1)}{a+b+2} - 1 = \frac{b - a}{a + b + 2}$. And $\beta_1 = \|\pi_1\|^2/\|\pi_0\|^2$ is the variance of $x$, four times that of $t$: $\beta_1 = \frac{4(a+1)(b+1)}{(a+b+2)^2(a+b+3)}$. Both match line L2 for every $a, b > -1$, including $a + b = 0$ and $a + b = -1$, where the general formulas below have a removable $0/0$.

## Claim 3: $\alpha_k$ for $k \ge 1$ and $\beta_k$ for $k \ge 2$

We use the classical three-term recurrence of the Jacobi polynomials $P_m = P_m^{(a,b)}$ (Szegő, *Orthogonal Polynomials*, equation (4.5.1)), valid for $m \ge 2$: with $s = 2m + a + b$,

$$2m(m + a + b)(s - 2)\,P_m = (s - 1)\bigl(s(s - 2)x + a^2 - b^2\bigr)P_{m-1} - 2(m + a - 1)(m + b - 1)\,s\,P_{m-2}.$$

For $m \ge 2$ all of $m + a + b$, $s - 1$, $s - 2$ are positive, so we can write $P_m = (A_m x + B_m)P_{m-1} - C_m P_{m-2}$ with

$$A_m = \frac{(s-1)s}{2m(m+a+b)},\quad B_m = \frac{(s-1)(a^2 - b^2)}{2m(m+a+b)(s-2)},\quad C_m = \frac{(m+a-1)(m+b-1)s}{m(m+a+b)(s-2)}.$$

The leading coefficients satisfy $k_m = A_m k_{m-1}$. Dividing by $k_m$, the monic $\pi_m = P_m/k_m$ satisfy $\pi_m = (x + B_m/A_m)\pi_{m-1} - \frac{C_m}{A_m A_{m-1}}\pi_{m-2}$, valid for $m \ge 3$ (so that $A_{m-1}$ comes from the same formula) and, for the $\alpha$ part, for $m \ge 2$. By uniqueness of the monic recurrence, with $k = m - 1$:

$$\alpha_k = -\frac{B_{k+1}}{A_{k+1}} = \frac{b^2 - a^2}{(2k + a + b)(2k + a + b + 2)} \quad (k \ge 1),$$

$$\beta_k = \frac{C_{k+1}}{A_{k+1}A_k} = \frac{4k(k + a)(k + b)(k + a + b)}{(2k + a + b)^2(2k + a + b + 1)(2k + a + b - 1)} \quad (k \ge 2).$$

The second follows by substituting $A_{k+1}, A_k, C_{k+1}$ with $s = 2k + a + b + 2$ and cancelling the factors $s$, $k + 1$ and $k + 1 + a + b$. These are the formulas of line L2. All $\beta_k$ are positive, so line L3 has real off-diagonal entries $\sqrt{\beta_k}$.

## Claim 4: the eigen-computation returns the Gauss rule

The characteristic polynomial of the Jacobi matrix $J_n$ of line L3 is $\pi_n$ (expand along the last row), so its eigenvalues are the zeros of $\pi_n$, which are the Gauss nodes; Sturm-count bisection finds them in increasing order (line L4), as on the [Gaussian quadrature](/gaussian-quadrature/) page. For each eigenvalue $x_j$, the eigenvector with $v_0 = 1$ has $v_k = \sqrt{\beta_0}\,p_k(x_j)$, where $p_k$ are the orthonormal polynomials, because both follow the same recurrence. With $V$ the orthogonal matrix of unit eigenvectors and $\mu_j = \beta_0 / \|v^{(j)}\|^2$,

$$\sum_j \mu_j\, p_k(x_j)\,p_l(x_j) = (VV^T)_{kl} = \delta_{kl} \qquad (k, l < n),$$

so the rule $(x_j, \mu_j)$ integrates all polynomials of degree at most $2n - 2$ exactly, in particular the Lagrange basis polynomials, and $\mu_j$ is the Gauss weight $\lambda_j$ (this is the [Golub-Welsch](/golub-welsch-algorithm/) theorem). Line L5 multiplies $v$ and $v_{k-1}$ by $10^{-100}$ whenever $|v|$ exceeds $10^{100}$ and the stored squares by $10^{-200}$, keeping the total scale in a separate logarithm. The recurrence is linear and homogeneous, so the rescaled vector is a multiple of the true one and $\log \mu_j$ is unchanged; only the overflow is avoided.

## Claim 5: degree, positivity and the error term

By the Gauss quadrature theorem, the rule is exact for all polynomials of degree at most $2n - 1$, not for $\pi_n^2$, the nodes are simple and lie in $(-1, 1)$, and the weights are positive. For $f \in C^{2n}[-1, 1]$, Hermite interpolation of $f$ at the doubled nodes gives

$$E_n(f) = \frac{f^{(2n)}(\xi)}{(2n)!}\int_{-1}^1 \pi_n(x)^2\, w(x)\,dx, \qquad \xi \in (-1, 1),$$

and $\|\pi_n\|^2 = \beta_0\beta_1\cdots\beta_n$, because $\|\pi_{k+1}\|^2 = \beta_{k+1}\|\pi_k\|^2$. The test file checks this product against the closed form $\frac{2^{2n+a+b+1}\, n!\,\Gamma(n+a+1)\Gamma(n+b+1)\Gamma(n+a+b+1)}{(2n+a+b+1)\,\Gamma(2n+a+b+1)^2}$ and checks $E_n((1 + x)^{2n}) = \|\pi_n\|^2$ against the computed rule. $\blacksquare$
