---
title: MAX-LOG-DEMAP returns the max form, its signs are the MAP bits, and its error is at most ln(M/2)
proves: [correctness]
status: full
---

The model and the notation are those of the page: $y = h x + w$ with $h \ne 0$ and $N_0 > 0$ known, $w \sim \mathcal{CN}(0, N_0)$, the points $a_0, \ldots, a_{M-1}$ with $M = 2^m$, the label bits $b_k(i)$, and the metric $d_i$ of line L2. For a bit $k$ and a value $b$, write $S_k^b = \{i : b_k(i) = b\}$. Since the labels are all of $\{0, 1\}^m$, each $S_k^b$ has exactly $M/2$ elements.

**Lemma 1 (the fold).** Fix $k$. After line L6 has run for the points $a_0, \ldots, a_{t-1}$, $B_b = \max\{d_i : i < t,\ i \in S_k^b\}$ for $b \in \{0, 1\}$, with $\max \emptyset = -\infty$. So line L7 returns $\tilde L_k = \max_{S_k^0} d_i - \max_{S_k^1} d_i$, and both terms are finite.

*Proof.* By induction on $t$. For $t = 0$ line L4 sets both to $-\infty$. Step $t \to t + 1$: with $b = b_k(t)$, line L6 sets $B_b$ to $\max(B_b, d_t)$, the maximum over the enlarged set, and leaves the other value unchanged. After $t = M$ both sets are full, and they are nonempty. $\square$

**Lemma 2 (the distance form).** Without priors, $\tilde L_k = \big(\min_{S_k^1}|y - h a_i|^2 - \min_{S_k^0}|y - h a_i|^2\big)/N_0$. In particular $N_0 \tilde L_k$ does not depend on $N_0$.

*Proof.* Here $d_i = -|y - h a_i|^2/N_0$ with $N_0 > 0$, and $\max_S(-f/N_0) = -\min_S f/N_0$ for any finite set $S$. $\square$

**Lemma 3 (the sandwich).** For a finite set $S$ of $n \ge 1$ indices, $\max_S d_i \le \ln\sum_S e^{d_i} \le \max_S d_i + \ln n$.

*Proof.* Let $D = \max_S d_i$. The sum contains the term $e^D$ and every term is positive, so it is at least $e^D$. Every term is at most $e^D$, so the sum is at most $n e^D$. Take logs. $\square$

**Theorem.** Let $L_k = \ln\sum_{S_k^0} e^{d_i} - \ln\sum_{S_k^1} e^{d_i}$ be the exact LLR of [soft demapping](/soft-demapping/).

1. $|L_k - \tilde L_k| \le \ln(M/2)$ for every $k$.
2. If $i^*$ is a point with the largest $d_i$ (the MAP decision; without priors, the nearest point to $y$ after the gain), then $\tilde L_k \ge 0$ when $b_k(i^*) = 0$ and $\tilde L_k \le 0$ when $b_k(i^*) = 1$. If $i^*$ is the only maximizer, the inequalities are strict, and the hard decisions $[\tilde L_k < 0]$ are the bits of $i^*$.
3. For $M = 2$ and for Gray QPSK, $\tilde L_k = L_k$.

*Proof.* (1) Write $E_b = \ln\sum_{S_k^b} e^{d_i} - \max_{S_k^b} d_i$. By Lemma 3 with $n = M/2$, $0 \le E_b \le \ln(M/2)$. Then $L_k - \tilde L_k = E_0 - E_1$, which lies in $[-\ln(M/2), \ln(M/2)]$.

(2) Let $b = b_k(i^*)$. Then $i^* \in S_k^b$, so $\max_{S_k^b} d_i = d_{i^*}$, and $\max_{S_k^{1-b}} d_i \le d_{i^*}$ because $d_{i^*}$ is the largest of all metrics. So the term for $b$ is at least the term for $1 - b$, which gives the signs. If $i^*$ is the only maximizer, every $i \in S_k^{1-b}$ has $d_i < d_{i^*}$, and since the set is finite the maximum over it is also smaller. Without priors, $d_i$ is largest exactly where $|y - h a_i|^2$ is smallest.

(3) For $M = 2$, $M/2 = 1$ and the bound of part 1 is $0$. For Gray QPSK, the points are $a = (s_I + j s_Q)/\sqrt{2}$ with $s_I, s_Q \in \{\pm 1\}$, the bit 0 fixes $s_I$ and the bit 1 fixes $s_Q$. Expanding the square, $-|y - h a|^2/N_0 = c + \alpha s_I + \beta s_Q$ with $c$ the same for all points, $\alpha = \sqrt{2}\,\mathrm{Re}(h^* y)/N_0$ and $\beta = \sqrt{2}\,\mathrm{Im}(h^* y)/N_0$; with priors, each bit adds $\pm L^a_k/2$, which keeps this form. For the bit 0, both $\ln\sum$ and $\max$ over $S_0^b$ equal the term in $s_I$ plus the same function of $\beta$ (a log-sum-exp in one case and a max in the other), and that function cancels in the difference. So $L_0 = \tilde L_0 = 2\alpha$ plus the prior, and in the same way $L_1 = \tilde L_1$. $\blacksquare$

**Proposition (per-axis form for Gray square QAM).** Let the points be $a = (c_I + j c_Q)/s$ with $s = \sqrt{2(M - 1)/3}$, where $(c_I, c_Q)$ runs over all pairs of raw levels $\{\pm 1, \pm 3, \ldots, \pm(\sqrt{M} - 1)\}$ and the label is the Gray label of $c_I$ followed by that of $c_Q$. Put $z = y/h$, $u = s\,\mathrm{Re}\,z$, $v = s\,\mathrm{Im}\,z$. Without priors, for an in-phase bit $k$,

$$\tilde L_k = \frac{|h|^2}{s^2 N_0}\Big(\min_{c_I:\, b_k = 1}(u - c_I)^2 - \min_{c_I:\, b_k = 0}(u - c_I)^2\Big),$$

and the same holds for a quadrature bit with $v$ and $c_Q$.

*Proof.* $y - h a = h(z - a)$, so $|y - h a|^2 = |h|^2|z - a|^2 = (|h|^2/s^2)\big((u - c_I)^2 + (v - c_Q)^2\big)$. An in-phase bit depends only on $c_I$, and the set of points is the full product of the levels, so

$$\min_{S_k^b}|y - h a|^2 = \frac{|h|^2}{s^2}\Big(\min_{c_I:\, b_k = b}(u - c_I)^2 + \min_{c_Q}(v - c_Q)^2\Big).$$

The second term is the same for $b = 0$ and $b = 1$ and cancels in Lemma 2. $\square$

**Corollary (16-QAM).** With the in-phase levels $+3, +1, -1, -3$ labeled $00, 01, 11, 10$, the first bit is $0$ on $\{+3, +1\}$ and the second bit is $0$ on $\{+3, -3\}$. For $u \ge 0$, the nearest level with the first bit $1$ is $-1$, and the nearest with the first bit $0$ is $+1$ if $u \le 2$ and $+3$ if $u > 2$. So the bracket is $(u + 1)^2 - (u - 1)^2 = 4u$ or $(u + 1)^2 - (u - 3)^2 = 8(u - 1)$. For the second bit and $u \ge 0$, the nearest levels are $+1$ (bit $1$) and $+3$ (bit $0$), and the bracket is $(u - 1)^2 - (u - 3)^2 = 4(u - 2)$. For $u < 0$ the same follows by the symmetry $u \mapsto -u$, which swaps $+c$ and $-c$; it changes the sign of the first bracket and keeps the second. With $s^2 = 10$ this is the closed form on the page. $\square$

**Cost.** Line L2 runs $M$ times, with $m$ extra terms each when there are priors, and line L6 runs $mM$ times, each a constant number of operations. The total is $\Theta(M \log M)$ per symbol with $\Theta(M)$ extra space. The per-axis form scans $\sqrt{M}$ levels for each of the $m$ bits, $\Theta(\sqrt{M}\log M)$.
