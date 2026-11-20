---
title: The L-pulse MTI canceller is the filter (1 - z^-1)^(L-1) in slow time, with response (2 |sin(pi f)|)^(L-1), blind speeds n lambda PRF / 2 and the stated improvement factor
proves: [correctness]
status: full
---

The notation is that of the page. $X[p][r]$ is the complex sample of pulse $p = 0, \dots, P-1$ at range bin $r = 0, \dots, M-1$. The canceller has $L \ge 1$ pulses and the weights $w[i] = (-1)^i \binom{L-1}{i}$, $i = 0, \dots, L-1$ (line L1). For $p = L-1, \dots, P-1$ and every $r$, lines L2 to L4 compute

$$y[p][r] = \sum_{i=0}^{L-1} w[i]\, X[p-i][r].$$

The implementation stores this value in output row $p - L + 1$. Write $f = f_d / \mathrm{PRF}$ for the Doppler frequency normalized by the pulse repetition frequency.

**Lemma 1 (the weights).** $\sum_{i} w[i] z^{-i} = (1 - z^{-1})^{L-1}$ for every complex $z \ne 0$.

*Proof.* This is the binomial theorem: $(1 - z^{-1})^{L-1} = \sum_{i=0}^{L-1} \binom{L-1}{i} (-z^{-1})^i$. $\square$

So the canceller is the FIR filter with transfer function $(1 - z^{-1})^{L-1}$: the two-pulse canceller $X[p] - X[p-1]$ applied $L - 1$ times in a row. Each output is the $(L-1)$-th backward difference of the slow-time sequence of one range bin.

**Theorem 1 (the output).** The canceller returns exactly the values $y[p][r]$ above, for all $p$ with $L - 1 \le p \le P - 1$ and all $r$, and no row when $P < L$.

*Proof.* Line L2 runs over $p = L-1, \dots, P-1$, line L3 over every $r$, and line L4 forms the sum of the definition, which reads only the rows $p - L + 1, \dots, p$, all inside $0, \dots, P-1$. When $P < L$ the range of line L2 is empty. $\square$

**Theorem 2 (the Doppler response).** If $X[p][r] = c\, e^{j 2\pi f p}$ for one range bin $r$, then $y[p][r] = c\, e^{j 2\pi f p} H(f)$ with

$$H(f) = \sum_{i} w[i] e^{-j 2\pi f i} = \left(1 - e^{-j 2\pi f}\right)^{L-1}, \qquad |H(f)| = \left(2\, |\sin(\pi f)|\right)^{L-1}.$$

*Proof.* $y[p][r] = \sum_i w[i]\, c\, e^{j 2\pi f (p - i)} = c\, e^{j 2\pi f p} \sum_i w[i] e^{-j 2\pi f i}$, and Lemma 1 with $z = e^{j 2\pi f}$ gives the product form. Next, $1 - e^{-j 2\pi f} = e^{-j\pi f}(e^{j\pi f} - e^{-j\pi f}) = 2j\, e^{-j\pi f} \sin(\pi f)$, whose magnitude is $2|\sin(\pi f)|$. $\square$

**Corollary 1 (blind speeds).** For $L \ge 2$, $H(f) = 0$ exactly when $f$ is an integer. A target of radial speed $v$ has $f_d = 2v/\lambda$, so the canceller output is zero for every pulse exactly at the blind speeds $v_n = n \lambda\, \mathrm{PRF} / 2$, $n = 0, \pm 1, \pm 2, \dots$. The largest gain, $2^{L-1}$, is at the half-integer values of $f$.

*Proof.* $\sin(\pi f) = 0$ exactly for integer $f$, and $f = 2v / (\lambda\, \mathrm{PRF}) = n$ gives $v = n\lambda\, \mathrm{PRF}/2$. $|\sin(\pi f)| = 1$ exactly at the half integers. $\square$

**Theorem 3 (polynomial clutter).** If, for one range bin, $X[p][r] = q(p)$ for a polynomial $q$ of degree at most $L - 2$, then $y[p][r] = 0$ for all $p$.

*Proof.* Let $\Delta$ be the backward difference, $(\Delta u)[p] = u[p] - u[p-1]$. If $u[p] = q(p)$ with $q$ of degree $d \ge 1$ and leading coefficient $a$, then $q(p) - q(p-1)$ has degree $d - 1$, because the terms $a p^d$ cancel and the next term is $a d\, p^{d-1}$. A constant gives 0. So $L - 1$ differences of a polynomial of degree at most $L - 2$ give 0, and by Lemma 1, $y = \Delta^{L-1} X$ in each range bin. $\square$

Stationary clutter of constant amplitude is the case of degree 0, which every canceller with $L \ge 2$ removes exactly.

**Theorem 4 (the improvement factor).** Let the clutter of one range bin be a wide-sense stationary sequence with power $\sigma_c^2$ and normalized autocorrelation $\rho_k = E[c[p]\, \overline{c[p-k]}]/\sigma_c^2$, real and with $\rho_0 = 1$. Let the target be $e^{j 2\pi f p}$ with $f$ uniform on $[0, 1)$. With real weights, the ratio of the output signal to clutter ratio to the input signal to clutter ratio, averaged over the target Doppler, is

$$I = \frac{\sum_i w[i]^2}{\sum_{i}\sum_{m} w[i]\, w[m]\, \rho_{|i-m|}}.$$

For $L = 2$, $I = 1/(1 - \rho_1)$. For $L = 3$, $I = 6/(6 - 8\rho_1 + 2\rho_2)$.

*Proof.* The output clutter power is $E|\sum_i w[i] c[p-i]|^2 = \sum_i \sum_m w[i] w[m] E[c[p-i]\overline{c[p-m]}] = \sigma_c^2 \sum_{i,m} w[i] w[m] \rho_{|i-m|}$, because $\rho_{-k} = \overline{\rho_k} = \rho_k$ for a real $\rho$. The input clutter power is $\sigma_c^2$. By Theorem 2 the target power gain at Doppler $f$ is $|H(f)|^2$, and

$$\int_0^1 |H(f)|^2\, df = \sum_i \sum_m w[i] w[m] \int_0^1 e^{-j 2\pi f (i - m)}\, df = \sum_i w[i]^2,$$

because the integral is 1 for $i = m$ and 0 otherwise. The input target power is 1. Divide the two ratios to get $I$. For $L = 2$ the weights are $(1, -1)$, the numerator is 2 and the denominator is $2 - 2\rho_1$. For $L = 3$ the weights are $(1, -2, 1)$, the numerator is 6 and the denominator is $6 + 2(-2\rho_1 - 2\rho_1 + \rho_2) = 6 - 8\rho_1 + 2\rho_2$. $\blacksquare$
