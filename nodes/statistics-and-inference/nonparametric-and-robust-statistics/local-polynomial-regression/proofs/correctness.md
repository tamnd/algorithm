---
title: A local polynomial fit of degree p reproduces polynomials of degree p exactly, and the local linear fit has a boundary bias of order h squared
proves: [correctness]
status: full
---

**Setting.** The data are pairs $(x_1, y_1), \ldots, (x_n, y_n)$. Fix a point $x$, a kernel $K \ge 0$, a bandwidth $h > 0$, optional robustness weights $\delta_i \ge 0$ and a degree $p \ge 0$. Line L1 sets $w_i = \delta_i K((x_i - x)/h)$, and with $d_i = x_i - x$ the fit minimizes
$$Q(\beta) = \sum_{i=1}^n w_i \Big(y_i - \sum_{k=0}^p \beta_k d_i^k\Big)^2 .$$
Line L2 forms the normal equations $S\beta = t$, with $S_{jk} = \sum_i w_i d_i^{j+k}$ and $t_j = \sum_i w_i d_i^j y_i$ for $0 \le j, k \le p$, and line L3 solves them and returns $\hat m(x) = \beta_0$.

## Part 1. The normal equations

**Lemma 1.** $S$ is positive definite if and only if at least $p + 1$ distinct values $x_i$ have $w_i > 0$. Then $Q$ has exactly one minimizer, the solution of $S\beta = t$.

*Proof.* For a vector $v$, $v^\top S v = \sum_i w_i \big(\sum_k v_k d_i^k\big)^2 = \sum_i w_i\,q_v(d_i)^2$, where $q_v$ is the polynomial with coefficients $v$. This is 0 if and only if $q_v$ vanishes at every $d_i$ with $w_i > 0$. A nonzero polynomial of degree at most $p$ has at most $p$ roots, so with $p + 1$ distinct such $d_i$ only $v = 0$ gives 0. With $p$ or fewer, a nonzero $q_v$ with those roots exists. $Q$ is a quadratic in $\beta$ with Hessian $2S$ and gradient $2(S\beta - t)$, so a positive definite $S$ gives one minimizer, where the gradient is 0. $\square$

When $S$ is singular, the code returns "undefined". The test file skips such cases.

## Part 2. Exact reproduction

**Theorem 2 (polynomials of degree p are reproduced).** Let $S$ be positive definite. If $y_i = q(x_i)$ for a polynomial $q$ of degree at most $p$, then $\hat m(x) = q(x)$, and more generally $\beta_k = q^{(k)}(x)/k!$ for every $k$.

*Proof.* Taylor's formula is exact for a polynomial of degree at most $p$: $q(x_i) = \sum_{k=0}^p \frac{q^{(k)}(x)}{k!}\,d_i^k$. So the vector $\beta^\circ$ with $\beta^\circ_k = q^{(k)}(x)/k!$ makes every residual 0 and $Q(\beta^\circ) = 0$. Since $Q \ge 0$, $\beta^\circ$ is a minimizer, and by Lemma 1 it is the only one. Line L3 returns $\beta^\circ_0 = q(x)$. $\square$

**Corollary 3 (the local linear fit reproduces a line).** With $p = 1$ and at least two distinct $x_i$ with positive weight, a line $y_i = a + bx_i$ gives $\hat m(x) = a + bx$ exactly, at every $x$: in the interior of the data, at its ends, and outside it. The local constant fit ($p = 0$) reproduces only constants.

The test file checks Theorem 2 in exact rational arithmetic for degrees 1, 2 and 3, at random points that include points at the edge of and outside the data, and checks $\beta_1 = q'(x)$.

**Corollary 4 (equivalent kernel).** $\hat m(x) = \sum_i \ell_i(x)\,y_i$ with weights $\ell_i(x) = w_i\,(e_0^\top S^{-1})(1, d_i, \ldots, d_i^p)^\top$ that satisfy
$$\sum_i \ell_i(x) = 1, \qquad \sum_i \ell_i(x)\,d_i^k = 0 \quad (1 \le k \le p).$$

*Proof.* $\beta = S^{-1}t$ and $t$ is linear in $y$, which gives the formula. Apply Theorem 2 to $q(t) = (t - x)^k$: then $y_i = d_i^k$ and $\hat m(x) = q(x)$, which is 1 for $k = 0$ and 0 for $k \ge 1$. $\square$

For $p = 1$, solving the 2 by 2 system gives the closed form
$$\hat m(x) = \frac{\sum_i w_i\,(S_2 - S_1 d_i)\,y_i}{S_0 S_2 - S_1^2}, \qquad S_k = \sum_i w_i d_i^k,$$
and the test compares the general solver with it, exactly. With $p = 0$, $\hat m(x) = \sum_i w_i y_i / \sum_i w_i$, the Nadaraya-Watson estimator; the test checks this too.

## Part 3. Bias at the boundary

Take the equally spaced design $x_i = i/N$, $i = 0, \ldots, N$, no robustness weights, a kernel $K$ that is symmetric, vanishes outside $[-1, 1]$ and has bounded variation, and the end point $x = 0$. Let $\mu_k^+ = \int_0^1 u^k K(u)\,du$. The weights depend only on the design, so $\mathbb{E}\,\hat m(0) = \sum_i \ell_i(0)\,m(x_i)$.

**Theorem 5 (local linear boundary bias of order $h^2$).** Let $m$ have a bounded second derivative that is continuous at 0. As $h \to 0$ and $Nh \to \infty$,
$$\mathbb{E}\,\hat m(0) - m(0) = \frac{h^2}{2}\,m''(0)\,\frac{(\mu_2^+)^2 - \mu_1^+\mu_3^+}{\mu_0^+\mu_2^+ - (\mu_1^+)^2} + o(h^2).$$

*Proof.* By Corollary 4 with $p = 1$, the constant and linear parts of $m$ cancel exactly:
$$\sum_i \ell_i(0)\,m(x_i) - m(0) = \sum_i \ell_i(0)\big(m(x_i) - m(0) - m'(0)\,x_i\big) = \sum_i \ell_i(0)\Big(\tfrac12 m''(0)\,x_i^2 + \rho_i x_i^2\Big),$$
where by Taylor's theorem $|\rho_i| \le \frac12\sup_{0 \le t \le h}|m''(t) - m''(0)| \to 0$, since only $x_i \le h$ have weight. From the closed form, $\sum_i \ell_i(0)\,x_i^2 = (S_2^2 - S_1 S_3)/(S_0 S_2 - S_1^2)$, and
$$\sum_i |\ell_i(0)|\,x_i^2 \le h^2 \sum_i |\ell_i(0)| \le h^2\,\frac{S_0 S_2 + S_1^2}{S_0 S_2 - S_1^2},$$
because $|S_2 - S_1 x_i| \le S_2 + S_1 x_i$ and $\sum_i w_i x_i = S_1$. Write $x_i = h\cdot i\delta$ with $\delta = 1/(Nh)$. Then $S_k = N h^{k+1}\,(\mu_k^+ + O(\delta))$ by the same Riemann sum bound as for the Nadaraya-Watson estimator, applied to $u^k K(u)$. So
$$\frac{S_2^2 - S_1 S_3}{S_0 S_2 - S_1^2} = h^2\,\frac{(\mu_2^+)^2 - \mu_1^+\mu_3^+ + O(\delta)}{\mu_0^+\mu_2^+ - (\mu_1^+)^2 + O(\delta)},$$
and the ratio $(S_0S_2 + S_1^2)/(S_0S_2 - S_1^2)$ stays bounded. The denominator $\mu_0^+\mu_2^+ - (\mu_1^+)^2$ is positive by the Cauchy-Schwarz inequality, which is strict because $K$ is not concentrated at one point. So the first term gives the stated main term, and the $\rho_i$ terms are $o(h^2)$. $\square$

For the Epanechnikov kernel, $\mu_0^+ = \frac12$, $\mu_1^+ = \frac3{16}$, $\mu_2^+ = \frac1{10}$ and $\mu_3^+ = \frac1{16}$, so the factor is $\big(\frac1{100} - \frac3{256}\big)/\big(\frac1{20} - \frac9{256}\big) = -\frac{11}{95}$. For $m(x) = x^2$ the remainder is 0, and the test measures the ratio of the bias to $h^2$: $-0.11287$ for $N = 1000$, $h = 0.1$ and $-0.11433$ for $N = 4000$, $h = 0.05$, against the limit $-11/95 = -0.11579$. Compare the Nadaraya-Watson estimator, whose boundary bias is $\frac38 h\,m'(0)$ for the same kernel: order $h$, not $h^2$.

In the interior, at a design point $x$ with $h \le x \le 1 - h$, the design is symmetric around $x$, so $S_1 = S_3 = 0$ and the local linear fit equals the local constant fit there; the bias is $\frac{h^2}{2}\mu_2\,m''(x) + o(h^2)$ by the same argument.

## What is cited, not proved

For a random design with density $f$, the local linear fit has interior bias $\frac{h^2}{2}\mu_2 m''(x)$ with no design bias term, variance $\sigma^2(x)R(K)/(nhf(x))$, the same bias order at the boundary, and it is the best linear smoother in a minimax sense (Fan 1992, 1993; Fan and Gijbels 1996, Chapter 3). For odd $p - \nu$, where $\nu$ is the order of the derivative estimated, the bias has the same order in the interior and at the boundary. These are cited, not proved here. The robustness iterations of LOWESS have no general convergence theorem; their effect on the example and in the tests is measured.

## Cost

Line L1 costs $O(n)$. Line L2 costs $O(np)$ for the $2p + 1$ power sums and line L3 costs $O(p^3)$. So one point costs $O(np + p^3)$, and the fitted values at all $n$ data points cost $O(n^2 p + np^3)$, or $O(n(k p + p^3))$ when only the $k$ nearest neighbours have weight and the data are sorted. LOWESS repeats this $1 + t$ times for $t$ robustness iterations.
