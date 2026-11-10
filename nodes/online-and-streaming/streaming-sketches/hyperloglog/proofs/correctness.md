---
title: HyperLogLog merges exactly, its registers have an exact law, and its range corrections invert exact means
proves: [correctness]
status: full
---

This page proves the parts of HyperLogLog that hold exactly: the state and the merge, the law of the registers in the Poisson model, the series for the mean of $2^{-M[j]}$, and the formulas behind the two range corrections. The asymptotic mean and standard error of Theorem 1 of Flajolet, Fusy, Gandouet and Meunier (2007) are cited at the end, not proved.

Let the stream have $d$ distinct items, let $h$ map items to 32-bit integers, and let $m = 2^b$. For an item, $j$ is the first $b$ bits of $h(x)$ and $w$ the other $W = 32 - b$ bits. $\rho(w)$ is the position of the leftmost 1 of $w$, counted from 1, with $\rho(0) = W + 1$.

**Lemma 1 (state and merge).** After lines L1 to L5, $M[j]$ is the maximum of $\rho(w_x)$ over the distinct items $x$ with bucket $j$, or 0 if there are none. So the state depends only on the set of distinct items, and the register by register maximum of the states of two streams, with the same $h$ and $b$, is the state of their concatenation.

*Proof.* Line L5 replaces $M[j]$ by $\max(M[j], \rho(w_x))$, and $(j, w_x)$ is a function of $x$. By induction over the stream, after each prefix $M[j]$ is the maximum over the items of the prefix in bucket $j$, which depends only on the set of those items. For the concatenation the set is the union, and a maximum over a union is the maximum of the two maxima. $\square$

From here on the hash values of the distinct items are independent and uniform 32-bit strings. As on the [LogLog](/loglog-counting/) proof page, $j$ and $w$ of an item are then independent and uniform, and $\Pr[\rho(w) > r] = 2^{-r}$ for $0 \le r \le W$.

**Lemma 2 (law of the registers).** If the number of distinct items is Poisson with mean $\lambda$, the registers are independent, and with $\mu = \lambda/m$,
$$\Pr[M[j] \le r] = \exp(-\mu 2^{-r}) \quad (0 \le r \le W), \qquad \Pr[M[j] = 0] = e^{-\mu}.$$

*Proof.* This is Theorem 4 of the LogLog proof page, since the state and the update are the same. Each item falls into bucket $j$ and has $\rho > r$ with probability $2^{-r}/m$, independently, so by Poisson splitting these counts are independent over $j$ and Poisson with mean $\mu 2^{-r}$. $M[j] \le r$ exactly when the count is 0. $\square$

**Theorem 3 (the mean of $2^{-M}$).** In the model of Lemma 2, ignoring the cut at $r = W + 1$,
$$\mathbb{E}\big[2^{-M[j]}\big] = e^{-\mu} + \sum_{r \ge 1} 2^{-r}\big(e^{-\mu 2^{-r}} - e^{-\mu 2^{-r+1}}\big).$$

*Proof.* By Lemma 2, $\Pr[M[j] = r] = \Pr[M[j] \le r] - \Pr[M[j] \le r - 1] = e^{-\mu 2^{-r}} - e^{-\mu 2^{-r+1}}$ for $r \ge 1$, and $\Pr[M[j] = 0] = e^{-\mu}$. Sum $2^{-r}\Pr[M[j] = r]$ over $r$. $\square$

The function $\mu\,\mathbb{E}[2^{-M[j]}]$ is, for large $\mu$, equal to $1/(2\ln 2) \approx 0.72135$ up to a periodic term in $\log_2\mu$ of very small amplitude (this asymptotic step is cited). Since the registers are independent with the same law, $\frac1m\sum_j 2^{-M[j]}$ concentrates near $\mathbb{E}[2^{-M[j]}] \approx \alpha_\infty/\mu$, and so the raw estimate of line L6, $\alpha_m m^2/\sum_j 2^{-M[j]} = \alpha_m m \big/ \big(\frac1m\sum_j 2^{-M[j]}\big)$, is near $\alpha_m m \mu/\alpha_\infty \approx \lambda$. This explains the form of line L6 and the limit $\alpha_\infty = 1/(2\ln 2)$; the precise constants $\alpha_m$ for finite $m$ are from the paper.

**Theorem 4 (small range).** Let $V$ be the number of registers equal to 0.

1. For a fixed number $d$ of distinct items, $\mathbb{E}[V] = m(1 - 1/m)^d$.
2. In the model of Lemma 2, $\mathbb{E}[V] = m e^{-\lambda/m}$, and solving $V = m e^{-\lambda/m}$ for $\lambda$ gives $\lambda = m\ln(m/V)$, the small range estimate of line L7.

*Proof.* A register is 0 exactly when no distinct item falls into its bucket. For fixed $d$, each item misses a fixed bucket with probability $1 - 1/m$, independently, so a register is 0 with probability $(1 - 1/m)^d$, and linearity of expectation over the $m$ registers gives part 1. In the Poisson model, a register is 0 with probability $e^{-\mu}$ by Lemma 2, which gives part 2. $\square$

This is the estimator of [linear counting](/linear-counting/) with the $m$ registers as the $m$ bits of its bitmap; its bias and variance are proved on that page.

**Theorem 5 (large range).** Let $D$ be the number of distinct values among the 32-bit hash values of $d$ distinct items. Then $\mathbb{E}[D] = 2^{32}\big(1 - (1 - 2^{-32})^d\big)$. If $D$ is replaced by $E$ and $(1 - 2^{-32})^d$ by $e^{-d/2^{32}}$, solving for $d$ gives $d = -2^{32}\ln(1 - E/2^{32})$, the large range estimate of line L7.

*Proof.* A fixed 32-bit value is hit by no item with probability $(1 - 2^{-32})^d$, so it is among the hash values with probability $1 - (1 - 2^{-32})^d$, and linearity of expectation over the $2^{32}$ values gives $\mathbb{E}[D]$. The sketch sees only the hash values, so in the middle range the raw estimate $E$ estimates $D$, not $d$. Setting $E = 2^{32}(1 - e^{-d/2^{32}})$ and solving gives the formula. $\square$

**What is cited and what is empirical.** For a fully random hash, Flajolet, Fusy, Gandouet and Meunier prove (Theorem 1) that $\mathbb{E}[E]/d \to 1 + \delta_1(d)$ with $|\delta_1| < 5 \cdot 10^{-5}$ for $m \ge 16$, and that the relative standard error tends to $\beta_m/\sqrt m$ up to a similar small term, with $\beta_\infty = \sqrt{3\ln 2 - 1}$. This analysis uses the Poisson model and a depoissonization step, and it is not reproduced here. The thresholds $\tfrac52 m$ and $2^{32}/30$ of line L7, and the accuracy of the corrected estimate near those thresholds, are empirical: they come from the simulations of Section 4 of the paper. $\blacksquare$
