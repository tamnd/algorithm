---
title: The number of empty bits has exact mean m(1-1/m)^d, and the estimate inverts it
proves: [correctness]
status: full
---

Let the stream have $d$ distinct items, and let their hash values $h(x_1), \ldots, h(x_d)$ be independent and uniform on $\{0, \ldots, m-1\}$. Let $U$ be the number of bits that are 0 after lines L1 to L4.

**Lemma 1 (the state is a function of the set).** Bit $j$ is 1 exactly when some distinct item has $h(x) = j$. So $U$ does not depend on order or repeats, and the OR of the bitmaps of two streams with the same $h$ and $m$ is the bitmap of their concatenation.

*Proof.* Line L4 only sets bits, and it sets bit $h(x)$ for each item. By induction, after a prefix, bit $j$ is 1 exactly when some item of the prefix hashes to $j$, which is a property of the set of items. For a union, the condition is the OR of the two conditions. $\square$

**Theorem 2 (exact moments).**
$$\mathbb{E}[U] = m\,q_1^d, \qquad \mathrm{Var}(U) = m(m-1)\,q_2^d + m\,q_1^d - m^2 q_1^{2d}, \qquad q_1 = 1 - \tfrac1m,\; q_2 = 1 - \tfrac2m.$$

*Proof.* Let $I_j$ be the [indicator](/indicator-random-variable/) that bit $j$ is 0, so $U = \sum_j I_j$. Bit $j$ is 0 when no item hashes to $j$; each item misses $j$ with probability $q_1$, independently, so $\mathbb{E}[I_j] = q_1^d$, and linearity gives $\mathbb{E}[U] = m q_1^d$. For $j \ne k$, both bits are 0 when every item misses both, which has probability $q_2^d$ for each item in turn, so $\mathbb{E}[I_j I_k] = q_2^d$. Since $I_j^2 = I_j$,
$$\mathbb{E}[U^2] = \sum_j \mathbb{E}[I_j] + \sum_{j \ne k}\mathbb{E}[I_j I_k] = m q_1^d + m(m-1) q_2^d,$$
and $\mathrm{Var}(U) = \mathbb{E}[U^2] - (\mathbb{E}U)^2$. $\square$

**Corollary 3 (limits).** Let $m \to \infty$ with $t = d/m$ fixed. Then $\mathbb{E}[U]/m \to e^{-t}$ and $\mathrm{Var}(U)/m \to e^{-t}\big(1 - (1 + t)e^{-t}\big)$.

*Proof.* $q_1^d = (1 - 1/m)^{tm} \to e^{-t}$, which gives the first limit. For the second, write $\mathrm{Var}(U)/m = (m-1)q_2^d + q_1^d - m q_1^{2d}$. The middle term tends to $e^{-t}$. For the other two, $\ln q_2^d = tm\ln(1 - 2/m) = -2t - 2t/m + O(m^{-2})$ and $\ln q_1^{2d} = 2tm\ln(1 - 1/m) = -2t - t/m + O(m^{-2})$. So $q_2^d = e^{-2t}(1 - 2t/m + O(m^{-2}))$ and $q_1^{2d} = e^{-2t}(1 - t/m + O(m^{-2}))$. Then
$$(m - 1)q_2^d - m q_1^{2d} = e^{-2t}\big(m - 2t - 1 - m + t + O(1/m)\big) \to -(1 + t)e^{-2t}.$$
Adding $e^{-t}$ gives the limit. $\square$

**Lemma 4 (the estimate inverts the mean).** The function $g(u) = m\ln(m/u)$ satisfies $g(m e^{-d/m}) = d$, and $g(m q_1^d) = -dm\ln(1 - 1/m) = d + t/2 + O(t/m)$.

*Proof.* The first identity is direct. For the second, $g(m q_1^d) = -m d \ln q_1 = -md\ln(1 - 1/m) = md(1/m + 1/(2m^2) + O(m^{-3})) = d + d/(2m) + O(d/m^2)$, and $d/(2m) = t/2$. $\square$

**Bias and variance of the estimate (a sketch, not a proof).** Write $U = \mu + \Delta$ with $\mu = \mathbb{E}[U]$. Expand $g(U) = m\ln m - m\ln U$ to second order:
$$g(U) \approx g(\mu) - \frac{m}{\mu}\Delta + \frac{m}{2\mu^2}\Delta^2.$$
Taking expectations, with $\mathbb{E}[\Delta] = 0$ and $\mathbb{E}[\Delta^2] = \mathrm{Var}(U)$, and using Corollary 3,
$$\mathbb{E}[g(U)] - g(\mu) \approx \frac{m\,\mathrm{Var}(U)}{2\mu^2} \approx \frac{m \cdot m e^{-t}(1 - (1+t)e^{-t})}{2 m^2 e^{-2t}} = \frac{e^t - t - 1}{2},$$
$$\mathrm{Var}(g(U)) \approx \frac{m^2}{\mu^2}\mathrm{Var}(U) \approx m\,(e^t - t - 1).$$
With $g(\mu) = d + t/2$ from Lemma 4, the bias is about $(e^t - t - 1)/2 + t/2 = (e^t - 1)/2$. Whang, Vander-Zanden and Taylor (1990) used $\mu \approx m e^{-t}$, for which $g(\mu) = d$ exactly, and so they state the bias as $(e^t - t - 1)/2$. The relative standard error is $\sqrt{m(e^t - t - 1)}/d$ in both cases.

The expansion is not a proof, for two reasons. $g(U)$ is infinite on the event $U = 0$, which has positive probability once $d \ge m$, so the mean of $g(U)$ is infinite and the statements are about the estimate on the event $U > 0$. And the remainder of the expansion must be bounded, which needs a concentration bound for $U$. When $m e^{-t}$ is large, $U$ is concentrated around $\mu$ with fluctuations of order $\sqrt{\mu}$, and the expansion is accurate; this is the regime in which the paper recommends using the method. $\blacksquare$
