---
title: Local quadratic convergence and termination of the Durand-Kerner method
proves: [correctness, termination, convergence-rate]
status: full
---

Let $p(z) = a_0 \prod_{k=1}^{n}(z - x_k)$ with $a_0 \ne 0$ and $n \ge 2$. For distinct points $z_1, \dots, z_n$ the Weierstrass correction is $W_i = p(z_i)/(a_0 \prod_{j \ne i}(z_i - z_j))$ and the total step is $z_i' = z_i - W_i$. Write $e_i = z_i - x_i$ and $\varepsilon = \max_i |e_i|$. Line numbers refer to the pseudocode on the main page. We work in exact arithmetic except in Theorem 4.

**Lemma 1 (error formula).** If the $z_i$ are distinct, then for each $i$
$$e_i' = -e_i\left(\prod_{j \ne i}\left(1 + \frac{e_j}{z_i - z_j}\right) - 1\right).$$

*Proof.* $p(z_i)/a_0 = (z_i - x_i)\prod_{j \ne i}(z_i - x_j)$ and $z_i - x_j = (z_i - z_j) + e_j$. Dividing by $\prod_{j \ne i}(z_i - z_j)$ gives $W_i = e_i \prod_{j \ne i}(1 + e_j/(z_i - z_j))$, and $e_i' = e_i - W_i$. $\square$

**Theorem 2 (local quadratic convergence).** Suppose the roots are simple with $\sigma = \min_{i \ne j}|x_i - x_j| > 0$, and $\varepsilon \le \sigma/(4n)$. Then the $z_i$ are distinct, and
$$\varepsilon' = \max_i |e_i'| \le \frac{3.3\,(n - 1)}{\sigma}\,\varepsilon^2 \le 0.83\,\varepsilon .$$
So the condition $\varepsilon \le \sigma/(4n)$ is kept, the errors tend to 0, and the order is at least 2 with $C = 3.3(n - 1)/\sigma$.

*Proof.* For $j \ne i$, $|z_i - z_j| \ge |x_i - x_j| - 2\varepsilon \ge \sigma - \sigma/(2n) \ge \sigma/2 > 0$, so the points are distinct and $t_j = e_j/(z_i - z_j)$ satisfies $|t_j| \le 2\varepsilon/\sigma \le 1/(2n)$. For complex $t_j$ with $|t_j| \le \tau$,
$$\Big|\prod_{j \ne i}(1 + t_j) - 1\Big| \le (1 + \tau)^{n-1} - 1 \le (n - 1)\tau(1 + \tau)^{n-2},$$
the first step by expanding the product and bounding each term by its modulus, the second by the mean value theorem. With $\tau = 2\varepsilon/\sigma \le 1/(2n)$, $(1 + \tau)^{n-2} \le e^{(n-2)/(2n)} < e^{1/2} < 1.65$. Lemma 1 gives $|e_i'| \le \varepsilon \cdot (n - 1)(2\varepsilon/\sigma) \cdot 1.65 = 3.3(n - 1)\varepsilon^2/\sigma$. Finally $3.3(n - 1)\varepsilon/\sigma \le 3.3(n - 1)/(4n) < 0.83$. $\square$

**Remark (multiple roots).** If $x_i = x_j$ for some $i \ne j$, then $\sigma = 0$ and Theorem 2 says nothing. Lemma 1 still holds: for a root of multiplicity $m$ approached by $m$ approximations at distances of the same order, the factors $1 + e_j/(z_i - z_j)$ do not tend to 1, so the error does not square. For a symmetric cluster $z_l = x^* + \rho\,\omega^l$, $\omega = e^{2\pi i/m}$, with the other approximations exact, $\prod_{l=1}^{m-1}(\rho - \rho\omega^l) = m\rho^{m-1}$, so $W_0 = \frac{\rho}{m}(1 + O(\rho))$ and the new error is $\frac{m - 1}{m}\rho + O(\rho^2)$. This explains the ratio close to $(m - 1)/m$ seen on the main page; that the cluster becomes symmetric is observed, not proved.

**Lemma 3 (sum of the roots).** For distinct $z_1, \dots, z_n$, $\sum_i W_i = \sum_i z_i + a_1/a_0$. So after a total step with no frozen index, $\sum_i z_i' = -a_1/a_0 = \sum_k x_k$.

*Proof.* Let $q(z) = \prod_j(z - z_j)$ and $r = p/a_0 - q$, a polynomial of degree at most $n - 1$ whose coefficient of $z^{n-1}$ is $a_1/a_0 + \sum_j z_j$. Lagrange interpolation at the $n$ nodes $z_i$ is exact for $r$, and its leading coefficient is $\sum_i r(z_i)/q'(z_i) = \sum_i p(z_i)/(a_0 \prod_{j \ne i}(z_i - z_j)) = \sum_i W_i$, since $q(z_i) = 0$. $\square$

**Theorem 4 (termination and the stopping rule).** The loop of L2 runs at most $K$ sweeps, and each index is frozen at most once, so the procedure always stops after at most $Kn$ evaluations of $p$. When an index is frozen at L4, the computed residual satisfies $|\hat p(z_i)| \le \beta_i$ where $\beta_i = 4u\mu_i$ is the running bound of Horner's rule.

*Proof.* The loops are bounded by $K$ and $n$, and an active index costs one evaluation per sweep. The residual claim is the test of L4. That $4u\mu$ bounds the rounding error of complex Horner evaluation to first order follows the running error analysis of Higham, Section 5.1, with the factor 4 covering the error of a complex multiply and add. In this case $z_i$ is an exact root of a polynomial whose coefficients differ from the $a_k$ by relative perturbations of order $nu$; this backward error statement is all that the residual test gives, and the forward error is then bounded by the [condition number](/root-conditioning/) of the root times that perturbation. $\square$

Global convergence is not claimed. Reinke, Schleicher and Stoll (2023) exhibited polynomials with open sets of starting vectors that never converge, so no proof can cover every start.
