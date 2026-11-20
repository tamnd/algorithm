---
title: The two-dimensional Wiener weights give the smallest mean squared error of all linear estimates from the chosen pilots
proves: [correctness]
status: full
---

Notation. $H(n, k)$ is the channel on OFDM symbol $n$ and subcarrier $k$, a zero-mean random field with the correlation $r(\Delta n, \Delta k) = E[H(n + \Delta n, k + \Delta k)\, H(n, k)^*]$, the same for every $(n, k)$ (wide-sense stationary), so $r(-\Delta n, -\Delta k) = r(\Delta n, \Delta k)^*$. The pilots chosen for a target $t$ are at the positions $p_1, \ldots, p_K$ and give the values $y_i = H(p_i) + e_i$, where the errors $e_i$ have zero mean, the variance $\sigma^2$, and are independent of each other and of the channel. Vectors are columns, $b^H$ is the conjugate transpose and $r_0 = r(0, 0)$. For weights $b \in \mathbb{C}^K$, the linear estimate is $b^H y = \sum_i b_i^* y_i$.

**Lemma 1 (the moments).** $E[y y^H] = R + \sigma^2 I$ with $R[i, j] = r(p_i - p_j)$, and $E[y\, H(t)^*] = c$ with $c[i] = r(p_i - t)$.

*Proof.* $E[y_i y_j^*] = E[H(p_i) H(p_j)^*] + E[e_i e_j^*]$, because the cross terms vanish by independence and zero mean. The first term is $r(p_i - p_j)$ by stationarity and the second is $\sigma^2$ if $i = j$ and $0$ otherwise. Similarly $E[y_i H(t)^*] = E[H(p_i) H(t)^*] = r(p_i - t)$. $\square$

**Lemma 2 (the error of any weights).** For every $b$,

$$E\left|H(t) - b^H y\right|^2 = r_0 - 2 \operatorname{Re}(b^H c) + b^H (R + \sigma^2 I)\, b.$$

*Proof.* Expand $E[(H(t) - b^H y)(H(t) - b^H y)^*] = E|H(t)|^2 - b^H E[y H(t)^*] - E[H(t) y^H] b + b^H E[y y^H] b$, and use Lemma 1 with $E[H(t) y^H] = c^H$, so that the two middle terms add up to $2 \operatorname{Re}(b^H c)$. $\square$

**Theorem (the Wiener weights are optimal).** Let $Q = R + \sigma^2 I$ with $\sigma^2 > 0$. Then $Q$ is Hermitian positive definite, the weights $w = Q^{-1} c$ of lines L2 to L5 minimize the error of Lemma 2 over all $b \in \mathbb{C}^K$, the minimum is unique, and

$$E\left|H(t) - w^H y\right|^2 = r_0 - c^H Q^{-1} c.$$

Line L6 returns $w^H y$.

*Proof.* $R$ is a covariance matrix, so $u^H R u = E|\sum_i u_i^* H(p_i)|^2 \ge 0$, and adding $\sigma^2 I$ makes $Q$ positive definite. Lines L2 and L3 build $Q$, line L4 builds $c$ and line L5 solves $Q w = c$. Completing the square in Lemma 2,

$$r_0 - 2 \operatorname{Re}(b^H c) + b^H Q b = r_0 - c^H Q^{-1} c + (b - w)^H Q\, (b - w),$$

which can be checked by expanding the last term with $Q w = c$ and $w^H Q w = c^H Q^{-1} c$. The last term is positive unless $b = w$, because $Q$ is positive definite. Line L6 computes $\sum_i w_i^* y_i = w^H y$. $\square$

**Corollary 1 (more pilots never hurt).** If the pilot set $S$ is contained in the pilot set $S'$, the Wiener error from $S'$ is at most that from $S$.

*Proof.* Any weights on $S$ are weights on $S'$ with zeros on $S' \setminus S$, and they give the same error, so the minimum over $S'$ is not larger. $\square$

**Corollary 2 (a clean pilot is kept).** If $t$ is a pilot position $p_i$ and $\sigma^2 \to 0$, the error tends to 0 and the estimate tends to $y_i$.

*Proof.* The weights $b = e_i$ (one on pilot $i$, zero elsewhere) give the error $\sigma^2$ by Lemma 2, because $c[i] = r_0 = Q[i, i] - \sigma^2$. The Wiener error is at most this, so it tends to 0. $\square$

**The Gaussian case.** If the channel and the errors are jointly circular complex Gaussian, the conditional mean $E[H(t) \mid y]$ is linear in $y$, so the Wiener estimate is also the minimum mean squared error estimate among all functions of the chosen pilot values. This is a theorem of Gaussian estimation. For other distributions it is the best linear estimate only.

**Mismatch (a remark).** If the receiver uses a correlation $\tilde r$ or a noise variance $\tilde\sigma^2$ that differ from the true ones, the weights are $\tilde w = \tilde Q^{-1} \tilde c$, and the true error is Lemma 2 evaluated at $b = \tilde w$ with the true $R$, $c$ and $\sigma^2$. By the theorem, it is at least the optimal error, and the difference is $(\tilde w - w)^H Q (\tilde w - w)$.
