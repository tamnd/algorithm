---
title: The numerical accountant computes the composed delta, and the two grids bracket it
proves: [correctness]
status: full
---

We work in the real RAM, where arithmetic on reals and $e^x$ are exact. Write $g_\varepsilon(s) = (1 - e^{\varepsilon - s})_+$ for $s \in \mathbb R$ and $g_\varepsilon(+\infty) = 1$. For each $\varepsilon$, $g_\varepsilon$ takes values in $[0, 1]$ and does not decrease on $\mathbb R \cup \{+\infty\}$.

Let $P$ and $Q$ be distributions on a countable set $O$ (the argument for densities is the same with integrals in place of sums). The privacy loss of $o$ with $P(o) > 0$ is $L(o) = \ln(P(o)/Q(o))$, which is $+\infty$ when $Q(o) = 0$. The PLD of $(P, Q)$ is the law of $L(o)$ for $o \sim P$, a probability measure on $\mathbb R \cup \{+\infty\}$. For $\varepsilon \ge 0$ let $\delta_{P,Q}(\varepsilon) = \sup_{S \subseteq O}(P(S) - e^{\varepsilon}Q(S))$.

**Lemma 1 (delta as an expectation).** $\delta_{P,Q}(\varepsilon) = E_{o \sim P}[g_\varepsilon(L(o))]$.

*Proof.* For each $S$, $P(S) - e^{\varepsilon}Q(S) = \sum_{o \in S}(P(o) - e^{\varepsilon}Q(o))$, and this is largest for $S^* = \{o : P(o) > e^{\varepsilon}Q(o)\}$, where it equals $\sum_o (P(o) - e^{\varepsilon}Q(o))_+$. A point with $P(o) = 0$ adds nothing. For $P(o) > 0$, $(P(o) - e^{\varepsilon}Q(o))_+ = P(o)(1 - e^{\varepsilon}Q(o)/P(o))_+ = P(o)\,g_\varepsilon(L(o))$, also when $Q(o) = 0$, where both sides are $P(o)$. Summing gives the claim. $\square$

**Lemma 2 (composition adds losses).** Let $(P_i, Q_i)$ for $i = 1, \ldots, k$ be pairs with PLDs $\lambda_1, \ldots, \lambda_k$. The PLD of $(P_1 \times \cdots \times P_k, Q_1 \times \cdots \times Q_k)$ is the law of $L_1 + \cdots + L_k$ with independent $L_i \sim \lambda_i$, where a sum with an infinite term is $+\infty$.

*Proof.* For $o = (o_1, \ldots, o_k)$ with $\prod_i P_i(o_i) > 0$,
$$\ln\frac{\prod_i P_i(o_i)}{\prod_i Q_i(o_i)} = \sum_i \ln\frac{P_i(o_i)}{Q_i(o_i)},$$
and both sides are $+\infty$ exactly when some $Q_i(o_i) = 0$. Under the product law $o_1, \ldots, o_k$ are independent with $o_i \sim P_i$, so the terms are independent with laws $\lambda_i$. $\square$

So for $k$ copies of one pair with PLD $\lambda$, Lemmas 1 and 2 give $\delta_k(\varepsilon) = E[g_\varepsilon(L_1 + \cdots + L_k)]$ with $L_i$ independent draws from $\lambda$.

**Lemma 3 (lines L1 to L5 compute the k-fold convolution).** Let $\omega$ be a grid PLD with finite masses $\omega_0, \ldots, \omega_{n-1}$ at $(l + j)h$ and mass $\omega_\infty$ at $+\infty$, and let $S$ be the sum of $k$ independent draws from $\omega$. Then lines L1 to L5 return the law of $S$: mass $\omega'_j$ at $(kl + j)h$ for $0 \le j \le k(n-1)$, and $\omega'_\infty$ at $+\infty$.

*Proof.* The finite part. Let $c = \omega^{*k}$ be the $k$-fold linear convolution of the vector $(\omega_0, \ldots, \omega_{n-1})$. Its entry $c_j$ is the sum of $\omega_{j_1}\cdots\omega_{j_k}$ over all tuples with $j_1 + \cdots + j_k = j$, which is the probability that all $k$ draws are finite and $S = (kl + j)h$, because $\sum_i (l + j_i)h = (kl + j)h$. The entries with $j > k(n-1)$ are zero. Let $a$ be $\omega$ padded with zeros to length $N$, and let $\circledast$ be cyclic convolution modulo $N$. By the convolution theorem for the discrete Fourier transform, the transform of $a^{\circledast k}$ is the pointwise $k$-th power of the transform of $a$, so lines L2 to L4 return $a^{\circledast k}$. An entry of $a^{\circledast k}$ at index $r$ is the sum of $c_j$ over $j \equiv r \pmod N$. Every nonzero $c_j$ has $0 \le j \le k(n-1) < N$ by line L1, so each residue class holds at most one such $j$, and $a^{\circledast k}$ equals $c$ padded with zeros. Line L4 keeps the first $k(n-1)+1$ entries, which are $c$. The offset is $kl$.

The infinite part. $S = +\infty$ exactly when at least one draw is $+\infty$, which has probability $1 - (1 - \omega_\infty)^k$ by independence. This is line L5. $\square$

Line L6 computes $\omega'_\infty + \sum_j \omega'_j\,g_\varepsilon((kl + j)h)$, where the terms with $(kl + j)h \le \varepsilon$ are zero. By Lemma 3 this is $E[g_\varepsilon(S)]$, and line L7 returns it.

**Lemma 4 (monotone coupling).** Let $L_1, \ldots, L_k$ and $L'_1, \ldots, L'_k$ be random variables on $\mathbb R \cup \{+\infty\}$, each family independent, with a coupling such that $L_i \le L'_i$ for each $i$. Then $E[g_\varepsilon(\sum_i L_i)] \le E[g_\varepsilon(\sum_i L'_i)]$.

*Proof.* Under the coupling, $\sum_i L_i \le \sum_i L'_i$ pointwise, with the rule that a sum with an infinite term is $+\infty$. Since $g_\varepsilon$ does not decrease, the inequality holds pointwise, and so for expectations. To couple $k$ pairs with independence across $i$, couple each pair $(L_i, L'_i)$ on its own and take the product of the $k$ couplings. $\square$

**Lemma 5 (dropping mass).** Let $\nu$ be a measure on $\mathbb R \cup \{+\infty\}$ with total mass at most 1, and let $\nu \le \lambda$ setwise, where $\lambda$ is a probability measure. Define $E_\nu^{(k)} = \int g_\varepsilon(s_1 + \cdots + s_k)\,d\nu(s_1)\cdots d\nu(s_k)$. Then $E_\nu^{(k)} \le E_\lambda^{(k)}$.

*Proof.* The integrand is non-negative, and $\nu^{\otimes k} \le \lambda^{\otimes k}$ setwise, because $\lambda - \nu$ is a non-negative measure and the product of the two expands into $\nu^{\otimes k}$ plus non-negative cross terms. $\square$

Lines L1 to L6 apply unchanged to a sub-probability grid: Lemma 3 holds with "law" replaced by the measure $\nu^{*k}$, since its proof only uses the multinomial expansion. With $\omega_\infty = 0$, line L5 gives 0.

**Theorem.** Let $\lambda$ be the PLD of $(P, Q)$ and $\delta_k$ the $\delta$ curve of $(P^{\otimes k}, Q^{\otimes k})$. Let $\omega^\uparrow$ and $\omega^\downarrow$ be the pessimistic and optimistic discretizations of $\lambda$ on a grid of step $h$ with cells indexed by $i_{\mathrm{lo}} \le i \le i_{\mathrm{hi}}$. Then for every $\varepsilon \ge 0$,
$$\text{NUMERICAL-ACCOUNTANT}(\omega^\downarrow, k, \varepsilon) \le \delta_k(\varepsilon) \le \text{NUMERICAL-ACCOUNTANT}(\omega^\uparrow, k, \varepsilon).$$

*Proof.* By Lemmas 1 and 2, $\delta_k(\varepsilon) = E[g_\varepsilon(L_1 + \cdots + L_k)]$ with $L_i$ independent draws from $\lambda$. By Lemma 3 and line L6, the accountant on a grid returns the same expression with draws from the grid PLD.

Upper bound. Define the map $u$ on $\mathbb R \cup \{+\infty\}$ by $u(s) = i_{\mathrm{lo}}h$ for $s \le (i_{\mathrm{lo}} - 1)h$, $u(s) = ih$ for $s \in ((i-1)h, ih]$ with $i_{\mathrm{lo}} \le i \le i_{\mathrm{hi}}$, and $u(s) = +\infty$ for $s > i_{\mathrm{hi}}h$, including $s = +\infty$. Then $u(s) \ge s$ for every $s$, and $u(L)$ for $L \sim \lambda$ has law $\omega^\uparrow$ by its definition. Couple $L'_i = u(L_i)$. Lemma 4 gives $\delta_k(\varepsilon) \le E[g_\varepsilon(\sum_i u(L_i))]$, which is the accountant on $\omega^\uparrow$.

Lower bound. Let $A = ((i_{\mathrm{lo}} - 1)h, i_{\mathrm{hi}}h]$ and let $\nu$ be $\lambda$ restricted to $A$, so $\nu \le \lambda$. By Lemma 5, $E_\nu^{(k)} \le E_\lambda^{(k)} = \delta_k(\varepsilon)$. Define $d(s) = (i-1)h$ for $s \in ((i-1)h, ih]$, so $d(s) \le s$ on $A$, and the image of $\nu$ under $d$ is $\omega^\downarrow$. The coupling argument of Lemma 4 applies to the finite measure $\nu$ after normalizing it, with the same factor $\nu(A)^k$ on both sides, and gives $E[g_\varepsilon(\sum_i d(L_i))] \le E_\nu^{(k)}$ under $\nu$. The left side is the accountant on $\omega^\downarrow$. If $\nu(A) = 0$, the accountant returns 0 and the bound is trivial.

Both bounds hold for every $\varepsilon \ge 0$. Since the curves do not increase in $\varepsilon$, bisection on the pessimistic curve returns an $\varepsilon$ whose true $\delta_k$ is at most the target.

The theorem is about independent copies of one pair. For the Gaussian mechanism with $\mu = \Delta/\sigma$, the pair $(N(\mu, 1), N(0, 1))$ is the worst case over neighbors, and the composition theorem of Gaussian differential privacy (Dong, Roth and Su) says that $k$ adaptive $\mu$-GDP steps are $\sqrt k\mu$-GDP, which is the curve of $k$ independent copies of that pair. So for the Gaussian mechanism the same bracket holds for adaptive composition. $\blacksquare$
