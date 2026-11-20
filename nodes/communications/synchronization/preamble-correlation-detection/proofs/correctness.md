---
title: The normalized correlation lies in [0, 1], equals 1 exactly on a scaled copy of the preamble, and has the false alarm probability (1 - lambda)^(L - 1) on white Gaussian noise
proves: [correctness]
status: full
---

The input is a sequence of complex symbols $y_0, y_1, \ldots$ and a known preamble $s = (s_0, \ldots, s_{L-1})$ with $E_s = \sum_i|s_i|^2 > 0$ and $L \ge 2$. For a start $n$, write $\mathbf{y}_n = (y_n, \ldots, y_{n+L-1})$. Line L4 computes $c(n) = \sum_i\overline{s_i}\,y_{n+i} = \langle s, \mathbf{y}_n\rangle$, lines L1 and L3 keep $E(n) = \|\mathbf{y}_n\|^2$, and line L5 forms $\rho(n) = |c(n)|^2/(E_s E(n))$, or $0$ when $E(n) = 0$. Lines L6 to L10 return the largest $\rho$ among the $L$ starts that begin at the first $n$ with $\rho(n) \ge \lambda$.

**Lemma 1 (running energy).** After line L3 at step $n$, the variable holds $E(n)$.

*Proof.* By induction on $n$. Line L1 sets it to $E(0)$. If it holds $E(n - 1)$, line L3 adds $|y_{n+L-1}|^2$ and removes $|y_{n-1}|^2$, which turns the sum over $n - 1, \ldots, n + L - 2$ into the sum over $n, \ldots, n + L - 1$. $\square$

In floating point the running sum gathers rounding error over a long stream; the implementation offers a direct recomputation to reset it, and the tests compare both to $10^{-9}$ over 300 symbols.

**Theorem 1 (range and equality).** $0 \le \rho(n) \le 1$, and $\rho(n) = 1$ if and only if $\mathbf{y}_n = h\,s$ for some complex $h \ne 0$. In that case $c(n)/E_s = h$.

*Proof.* By the Cauchy-Schwarz inequality, $|\langle s, \mathbf{y}_n\rangle|^2 \le \|s\|^2\|\mathbf{y}_n\|^2$, with equality if and only if the two vectors are linearly dependent. If $\mathbf{y}_n = hs$, then $c(n) = h\|s\|^2 = hE_s$. $\square$

**Theorem 2 (invariance).** For every complex $h \ne 0$, replacing $y$ by $hy$ does not change any $\rho(n)$.

*Proof.* $|c(n)|^2$ and $E(n)$ are both multiplied by $|h|^2$. $\square$

So the detector needs no estimate of the gain, the carrier phase or the noise level, and its threshold $\lambda$ is a fixed number.

**Theorem 3 (false alarm probability).** If the $y_i$ in a window are independent $\mathcal{CN}(0, \sigma^2)$, then $\rho(n)$ has the Beta$(1, L - 1)$ distribution for every $\sigma^2 > 0$, and
$$P(\rho(n) \ge \lambda) = (1 - \lambda)^{L-1}, \qquad 0 \le \lambda \le 1.$$

*Proof.* Let $U$ be a unitary matrix whose first row is $s^H/\|s\|$. Then $\mathbf{w} = U\mathbf{y}_n$ has independent $\mathcal{CN}(0, \sigma^2)$ entries, because the distribution of a white circular Gaussian vector does not change under a unitary map. Also $c(n) = \|s\|\,w_1$ and $E(n) = \|\mathbf{w}\|^2$, so $\rho(n) = |w_1|^2/\sum_i|w_i|^2$. The values $|w_i|^2$ are independent and exponential with mean $\sigma^2$, which is Gamma$(1, \sigma^2)$. For independent $G_1 \sim$ Gamma$(1)$ and $G_2 = \sum_{i \ge 2}|w_i|^2 \sim$ Gamma$(L - 1)$ with the same scale, $G_1/(G_1 + G_2)$ is Beta$(1, L - 1)$, and the scale cancels. The tail of Beta$(1, L - 1)$ is $\int_\lambda^1 (L - 1)(1 - r)^{L-2}dr = (1 - \lambda)^{L-1}$. $\square$

**Corollary 1 (threshold).** For a target false alarm probability $P_{fa}$ per start, $\lambda = 1 - P_{fa}^{1/(L-1)}$. For a stream with $K$ starts of noise, the union bound gives at most $K P_{fa}$ for the probability of any false alarm.

**Theorem 4 (correct detection without noise).** If $y$ holds $hs$ at start $n_0$ and no start $n < n_0$ has $\rho(n) \ge \lambda$, and every $n \ne n_0$ in $[n_0 - L + 1, n_0 + L - 1]$ has $\rho(n) < 1$, then the detector returns $n_0$, $\rho = 1$ and the gain $h$.

*Proof.* The scan of lines L6 and L7 stops at the first $n_1 \le n_0$ with $\rho(n_1) \ge \lambda$, since $\rho(n_0) = 1 \ge \lambda$ by Theorem 1. Then $n_0 \in [n_1, n_1 + L - 1]$, and line L8 picks the maximum over that range, which is the unique start with $\rho = 1$. Theorem 1 gives the gain. $\square$

The false alarm formula is a theorem for white circular Gaussian noise. On data symbols instead of noise it does not hold, because data symbols can match part of the preamble; that rate depends on the data and the preamble. The tests check Theorem 3 with 5000 windows of noise whose variance changes from window to window, and Theorem 4 with a gain of $0.5e^{j0.7}$.
