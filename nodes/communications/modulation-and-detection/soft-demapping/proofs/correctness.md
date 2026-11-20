---
title: SOFT-DEMAP returns the a posteriori LLR of each bit and its extrinsic part
proves: [correctness]
status: full
---

The model is $y = h x + w$ with $h \ne 0$ and $N_0 > 0$ known, $w \sim \mathcal{CN}(0, N_0)$, and $x$ one of the points $a_0, \ldots, a_{M-1}$, $M = 2^m$. The point $a_i$ carries the label $i$ with bits $b_0(i), \ldots, b_{m-1}(i)$. The label bits are independent a priori, with $P(b_k = 0) = p_k \in (0, 1)$ and $L^a_k = \ln\big(p_k/(1 - p_k)\big)$; equal priors are the case $L^a_k = 0$ for all $k$.

**Lemma 1 (the metric).** For each $i$, $d_i$ of line L2 satisfies $d_i = \ln\big(p(y \mid a_i)\, P(x = a_i)\big) + C$, where $C$ does not depend on $i$.

*Proof.* The density of $y$ given $x = a_i$ is $\frac{1}{\pi N_0}\exp(-|y - h a_i|^2/N_0)$, a circularly symmetric complex Gaussian with mean $h a_i$. Since the label map $i \mapsto (b_0(i), \ldots, b_{m-1}(i))$ is a bijection onto $\{0, 1\}^m$ and the bits are independent, $P(x = a_i) = \prod_k P(b_k = b_k(i))$. For one bit, $p_k = e^{L^a_k/2}/(e^{L^a_k/2} + e^{-L^a_k/2})$ and $1 - p_k = e^{-L^a_k/2}/(e^{L^a_k/2} + e^{-L^a_k/2})$, so $P(b_k = b) = e^{(1 - 2b)L^a_k/2}/Z_k$ with $Z_k = e^{L^a_k/2} + e^{-L^a_k/2}$ for both values of $b$. Taking logs,

$$\ln\big(p(y \mid a_i)\,P(x = a_i)\big) = -\frac{|y - h a_i|^2}{N_0} + \sum_k \frac{(1 - 2b_k(i))L^a_k}{2} - \ln(\pi N_0) - \sum_k \ln Z_k,$$

and the last two terms form the constant $-C$. $\square$

**Lemma 2 ($\max^*$).** For real $u, v$, $\max^*(u, v) = \max(u, v) + \ln(1 + e^{-|u - v|}) = \ln(e^u + e^v)$. With the convention $e^{-\infty} = 0$, $\max^*(-\infty, v) = v = \ln(0 + e^v)$.

*Proof.* Let $u \ge v$ without loss of generality. Then $\ln(e^u + e^v) = \ln\big(e^u(1 + e^{v - u})\big) = u + \ln(1 + e^{-|u - v|})$. The second claim is the definition used in line L6 for the first term of each sum. $\square$

**Lemma 3 (the fold).** Fix $k$. After line L6 has run for the points $a_0, \ldots, a_{t-1}$, for $b \in \{0, 1\}$,

$$A_b = \ln \sum_{i < t,\ b_k(i) = b} e^{d_i},$$

with the empty sum giving $-\infty$.

*Proof.* By induction on $t$. For $t = 0$ both sums are empty and line L4 sets $A_0 = A_1 = -\infty$. Step $t \to t + 1$: let $b = b_k(t)$. Line L6 changes only $A_b$, to $\max^*(A_b, d_t)$, which by Lemma 2 and the hypothesis is $\ln\big(\sum_{i < t,\ b_k(i) = b} e^{d_i} + e^{d_t}\big)$, the sum over $i < t + 1$. The other accumulator keeps its value, and its sum gains no term. $\square$

**Theorem.** For every $k$, line L7 returns $L_k = \ln P(b_k = 0 \mid y)/P(b_k = 1 \mid y)$, and line L8 returns $E_k = L_k - L^a_k$, which equals

$$E_k = \ln\frac{\sum_{i:\, b_k(i) = 0} p(y \mid a_i) \prod_{k' \ne k} P(b_{k'} = b_{k'}(i))}{\sum_{i:\, b_k(i) = 1} p(y \mid a_i) \prod_{k' \ne k} P(b_{k'} = b_{k'}(i))},$$

the LLR of bit $k$ computed with the priors of all bits except $k$.

*Proof.* Each label $i$ has $b_k(i) = 0$ or $b_k(i) = 1$, and both values occur, since the labels are all of $\{0, 1\}^m$. So after the loop of line L5 has seen all $M$ points, Lemma 3 gives two nonempty sums, and $A_0, A_1$ are finite. By Lemma 1,

$$A_0 - A_1 = \ln\frac{\sum_{b_k(i) = 0} e^{C} p(y \mid a_i) P(a_i)}{\sum_{b_k(i) = 1} e^{C} p(y \mid a_i) P(a_i)} = \ln\frac{p(y,\ b_k = 0)}{p(y,\ b_k = 1)} = \ln\frac{P(b_k = 0 \mid y)}{P(b_k = 1 \mid y)},$$

where the factor $e^C$ cancels and the last step divides the numerator and the denominator by $p(y) > 0$.

For the extrinsic value, the factor $P(b_k = b_k(i))$ is $p_k$ for every term of the numerator and $1 - p_k$ for every term of the denominator. Taking these factors out of the two sums gives

$$L_k = \ln\frac{p_k}{1 - p_k} + E_k = L^a_k + E_k,$$

with $E_k$ as in the statement. So $L_k - L^a_k = E_k$. $\blacksquare$

**Special cases.** For BPSK with the label 0 on $+1$ and 1 on $-1$, the theorem gives $L = \big(-|y - h|^2 + |y + h|^2\big)/N_0 = 4\,\mathrm{Re}(h^* y)/N_0$, and $E = L - L^a$ does not depend on the prior, since there are no other bits. For Gray QPSK with the points $a = (s_I + j s_Q)/\sqrt{2}$, $s_I, s_Q \in \{\pm 1\}$, the metric is $-|y - h a|^2/N_0 = c + \sqrt{2}\big(s_I\,\mathrm{Re}(h^* y) + s_Q\,\mathrm{Im}(h^* y)\big)/N_0$, where $c$ is the same for all four points. Each sum in the theorem then factors into a term in $s_I$ times a term in $s_Q$; the bit 0 fixes $s_I$, the $s_Q$ factor cancels, and $L_0 = 2\sqrt{2}\,\mathrm{Re}(h^* y)/N_0$. In the same way $L_1 = 2\sqrt{2}\,\mathrm{Im}(h^* y)/N_0$.

**Cost.** Line L2 runs $M$ times, with $m$ extra terms each when there are priors, and line L6 runs $mM$ times. Each is a constant number of arithmetic operations, $\exp$ and $\ln$, so the total is $\Theta(M \log M)$ per symbol, with $\Theta(M)$ extra space for the metrics.
