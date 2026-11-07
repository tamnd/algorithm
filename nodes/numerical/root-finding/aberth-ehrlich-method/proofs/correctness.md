---
title: Local cubic convergence, termination and the multiple-root rate of the Aberth-Ehrlich method
proves: [correctness, termination, convergence-rate]
status: full
---

Let $p(z) = a_0 \prod_{k=1}^{n}(z - x_k)$ with $a_0 \ne 0$ and $n \ge 2$. For distinct points $z_1, \dots, z_n$ with $p(z_i) \ne 0$, the total step is $z_i' = z_i - 1/(p'(z_i)/p(z_i) - S_i^z)$ with $S_i^z = \sum_{j \ne i} 1/(z_i - z_j)$, which equals $z_i - p/(p' - pS_i^z)$ at $z_i$. Write $e_i = z_i - x_i$ and $\varepsilon = \max_i |e_i|$. Line numbers refer to the pseudocode on the main page. We work in exact arithmetic except in Theorem 4.

**Lemma 1 (error formula).** If $z_i \ne x_k$ for all $k$ and the $z_j$ are distinct, put
$$S_i = \sum_{j \ne i}\left(\frac{1}{z_i - x_j} - \frac{1}{z_i - z_j}\right) = -\sum_{j \ne i}\frac{e_j}{(z_i - x_j)(z_i - z_j)} .$$
Then, if $1 + e_i S_i \ne 0$, $e_i' = e_i^2 S_i/(1 + e_i S_i)$.

*Proof.* $p'(z_i)/p(z_i) = \sum_k 1/(z_i - x_k) = 1/e_i + \sum_{j \ne i} 1/(z_i - x_j)$, so $p'/p - S_i^z = 1/e_i + S_i$. The second form of $S_i$ follows from $1/(z_i - x_j) - 1/(z_i - z_j) = ((z_i - z_j) - (z_i - x_j))/((z_i - x_j)(z_i - z_j))$ and $x_j - z_j = -e_j$. Then $e_i' = e_i - 1/(1/e_i + S_i) = e_i - e_i/(1 + e_iS_i) = e_i^2S_i/(1 + e_iS_i)$. $\square$

If $z_i = x_i$ exactly, then $p(z_i) = 0$, L4 freezes $z_i$, and its error stays 0.

**Theorem 2 (local cubic convergence).** Suppose the roots are simple with $\sigma = \min_{i \ne j}|x_i - x_j| > 0$ and $\varepsilon \le \sigma/(4n)$. Then the $z_j$ are distinct, no $z_i$ equals a root $x_j$ with $j \ne i$, the step is defined, and
$$\varepsilon' \le \frac{3.2\,(n - 1)}{\sigma^2}\,\varepsilon^3 \le \frac{\varepsilon}{5n}.$$
So the condition is kept, and the method converges with order at least 3 and $C = 3.2(n - 1)/\sigma^2$.

*Proof.* For $j \ne i$: $|z_i - x_j| \ge \sigma - \varepsilon \ge \frac34\sigma$ and $|z_i - z_j| \ge \sigma - 2\varepsilon \ge \frac12\sigma$, both positive. So $|S_i| \le (n - 1)\varepsilon \cdot \frac{8}{3\sigma^2}$ and $|e_iS_i| \le \frac{8(n - 1)}{3}\frac{\varepsilon^2}{\sigma^2} \le \frac{8(n - 1)}{3 \cdot 16 n^2} < \frac{1}{6n} \le \frac16$. Hence $1 + e_iS_i \ne 0$, the denominator $p' - pS_i^z = p(1/e_i + S_i)$ is nonzero, and by Lemma 1
$$|e_i'| \le \frac{\varepsilon^2 \cdot \frac{8(n - 1)\varepsilon}{3\sigma^2}}{1 - \frac16} = \frac{3.2(n - 1)\varepsilon^3}{\sigma^2}.$$
Finally $3.2(n - 1)\varepsilon^2/\sigma^2 \le 3.2(n - 1)/(16n^2) < 1/(5n)$. $\square$

**Theorem 3 (symmetric cluster at a multiple root).** Let $x^*$ be a root of multiplicity $m \ge 2$, $p(z) = (z - x^*)^m h(z)$ with $h(x^*) \ne 0$, and let $m$ of the approximations be $z_j = x^* + \rho\,\omega^j$, $j = 0, \dots, m - 1$, with $\omega = e^{2\pi i/m}$ and $\rho \ne 0$ small. Then, as $\rho \to 0$ with the other approximations fixed away from $x^*$, each of these takes the step to $z_j' = x^* + \frac{m - 1}{m + 1}\rho\,\omega^j + O(\rho^2)$.

*Proof.* Take $j = 0$ by symmetry, so $z_0 - x^* = \rho$. Then $p'/p = m/\rho + O(1)$. The other cluster points give $\sum_{l = 1}^{m-1} 1/(\rho - \rho\omega^l) = \frac{1}{\rho}\sum_{l=1}^{m-1}\frac{1}{1 - \omega^l} = \frac{m - 1}{2\rho}$, by the identity $\sum_{l=1}^{m-1} 1/(1 - \omega^l) = (m - 1)/2$ (pair $l$ with $m - l$: $\frac{1}{1 - w} + \frac{1}{1 - \bar w} = 1$ for $|w| = 1$, $w \ne 1$). The approximations away from $x^*$ contribute $O(1)$. So $p'/p - S^z = \frac{m + 1}{2\rho} + O(1)$ and the step is $\frac{2\rho}{m + 1}(1 + O(\rho))$, which gives $z_0' - x^* = \rho - \frac{2\rho}{m + 1} + O(\rho^2) = \frac{m - 1}{m + 1}\rho + O(\rho^2)$. $\square$

For $m = 3$ the factor is $1/2$, which is the ratio observed on $(z - 1)^3(z + 2)$ on the main page. The same computation for the Durand-Kerner correction gives $(m - 1)/m$. That the cluster becomes symmetric is observed, not proved.

**Theorem 4 (termination and the stopping rule).** The loop of L2 runs at most $K$ sweeps and each index is frozen at most once, so at most $Kn$ evaluations of $p$ (and as many of $p'$) are made. A root frozen at L4 has computed residual at most the running bound $\beta_i = 4u\mu_i$ of Horner's rule, so it is the exact root of a polynomial whose coefficients differ from the given ones by relative amounts of order $nu$, to first order (Higham, Section 5.1). Its forward error is then bounded by the [condition number](/root-conditioning/) of the root times that perturbation, and nothing better is claimed.

*Proof.* The loops are bounded, and an active index costs one evaluation of $p$ and $p'$ per sweep. The residual claim is the test of L4, and the backward reading is the running error analysis of Horner's rule. $\square$

Global convergence from the circle start of L1 is not claimed.
