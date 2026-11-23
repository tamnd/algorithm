---
title: Randomized response is epsilon-LDP and its estimate is unbiased
proves: [correctness]
status: full
---

Fix a rational number $e^{\varepsilon} \ge 1$ and let $p = e^{\varepsilon}/(1 + e^{\varepsilon}) = a/q$ in lowest terms (line L1). Write $R(v)$ for the output of RANDOMIZED-RESPONSE on the bit $v$.

**Lemma 1 (the coin).** Line L2 gives $\Pr[c = 1] = p$.

*Proof.* The integer is uniform on the $q$ values $\{0, \ldots, q - 1\}$, and exactly $a$ of them are below $a$, because $0 \le a \le q$. So $\Pr[c = 1] = a/q = p$. $\square$

**Lemma 2 (the pmf of one report).** For $v, r \in \{0, 1\}$, $\Pr[R(v) = r] = p$ if $r = v$ and $1 - p$ if $r \ne v$.

*Proof.* Line L3 returns $v$ when $c = 1$, and line L4 returns $1 - v$ when $c = 0$. The claim follows from Lemma 1. $\square$

**Theorem 1 (privacy).** $R$ is $\varepsilon$-LDP. The vector $(R(v_1), \ldots, R(v_n))$, with independent coins, is $\varepsilon$-DP under replace neighbors, and no smaller $\varepsilon$ holds for it when $n \ge 1$.

*Proof.* By Lemma 2, for all $v, v', r$, the ratio $\Pr[R(v) = r] / \Pr[R(v') = r]$ is 1 if $v = v'$, and otherwise it is $p/(1-p)$ or $(1-p)/p$. Since $p/(1-p) = e^{\varepsilon}$ and $(1-p)/p = e^{-\varepsilon}$, the ratio is at most $e^{\varepsilon}$. This is $\varepsilon$-LDP.

Let $v$ and $v'$ be two vectors of length $n$ that differ only at position $j$. The coins are independent, so for every vector of reports $r$,

$$\frac{\Pr[R(v) = r]}{\Pr[R(v') = r]} = \prod_{i=1}^{n} \frac{\Pr[R(v_i) = r_i]}{\Pr[R(v'_i) = r_i]} = \frac{\Pr[R(v_j) = r_j]}{\Pr[R(v'_j) = r_j]} \le e^{\varepsilon}.$$

For a set $S$ of vectors, sum the inequality $\Pr[R(v) = r] \le e^{\varepsilon} \Pr[R(v') = r]$ over $r \in S$. The ratio equals $e^{\varepsilon}$ when $r_j = v_j$, so no smaller $\varepsilon$ holds. $\square$

**Theorem 2 (the estimate).** Let $\pi = \frac1n \sum_i v_i$ and $\hat\pi$ the output of ESTIMATE on the reports, with $\varepsilon > 0$. Then $\mathbb E[\hat\pi] = \pi$ and $\mathrm{Var}[\hat\pi] = p(1-p)/(n(2p-1)^2)$.

*Proof.* Let $r_i = R(v_i)$. By Lemma 2, $r_i$ is an indicator variable with $\Pr[r_i = 1] = p v_i + (1-p)(1 - v_i) = (2p - 1) v_i + (1 - p)$. By linearity of expectation, $\lambda$ of line L5 has

$$\mathbb E[\lambda] = \frac1n \sum_{i} \big((2p - 1) v_i + (1 - p)\big) = (2p - 1)\pi + (1 - p).$$

Since $\varepsilon > 0$, $p > 1/2$ and $2p - 1 > 0$. Line L6 is $\hat\pi = (\lambda - (1-p))/(2p-1)$, an affine map of $\lambda$, so $\mathbb E[\hat\pi] = ((2p-1)\pi + (1-p) - (1-p))/(2p-1) = \pi$.

For the variance, $\Pr[r_i = 1]$ is $p$ if $v_i = 1$ and $1 - p$ if $v_i = 0$. In both cases $\mathrm{Var}[r_i] = p(1-p)$. The $r_i$ are independent, so $\mathrm{Var}[\lambda] = \frac{1}{n^2} \cdot n\,p(1-p) = p(1-p)/n$. The affine map divides the variance by $(2p-1)^2$, which gives the claim. $\square$

Theorem 1 gives the privacy of each report and of the vector of reports. Theorem 2 shows that the collector's estimate is unbiased, with the stated variance, for every fixed dataset. $\blacksquare$
