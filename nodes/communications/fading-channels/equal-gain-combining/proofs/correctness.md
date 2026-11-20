---
title: Equal gain combining gives an unbiased estimate with output SNR E_s (sum |h_l|)^2 / (L N0), between the mean and the sum of the branch SNRs
proves: [correctness]
status: full
---

Branch $l = 1, \ldots, L$ receives $y_l = h_l x + w_l$ with $E|x|^2 = E_s$ and $w_l \sim CN(0, N_0)$, independent of each other and of $x$. The gains are known and not all zero. Write $\gamma_l = |h_l|^2 E_s/N_0$ and $a = \sum_l |h_l| > 0$. Line L1 sets $c_l = h_l/|h_l|$ for $h_l \ne 0$ and $c_l = 0$ for $h_l = 0$.

**Lemma 1 (one branch).** $c_l^* y_l = |h_l|\, x + c_l^* w_l$, and $c_l^* w_l \sim CN(0, N_0)$ for $h_l \ne 0$.

*Proof.* $c_l^* h_l = \overline{h_l} h_l/|h_l| = |h_l|$. Multiplying a circular Gaussian variable by a number of modulus 1 does not change its distribution. For $h_l = 0$ the term is 0, and $|h_l| = 0$ as well. $\square$

**Theorem 1 (the output).** Let $L'$ be the number of branches with $h_l \ne 0$. Then $z/a = x + n$ with $n \sim CN(0, L' N_0/a^2)$, so the output SNR is $\gamma_{\mathrm{EGC}} = E_s a^2/(L' N_0)$. With all gains nonzero, $L' = L$.

*Proof.* By Lemma 1, $z = \sum_l c_l^* y_l = a x + \sum_l c_l^* w_l$. The noise terms are independent, each $CN(0, N_0)$ for the $L'$ nonzero branches and 0 for the others, so their sum is $CN(0, L' N_0)$. Divide by $a$. $\square$

The reference code sets $c_l = 0$ for a zero gain, as in the theorem; the page states the formula with $L$, the case in which every branch has a nonzero gain, which happens with probability 1 in Rayleigh fading. If a receiver adds a branch with a zero gain but a fixed unit weight, its noise is still added, and the formula with $L$ holds.

**Theorem 2 (the bounds).** With all gains nonzero, $\frac1L \sum_l \gamma_l \le \gamma_{\mathrm{EGC}} \le \sum_l \gamma_l$. The right side is an equality if and only if all $|h_l|$ are equal.

*Proof.* By the Cauchy-Schwarz inequality for the vectors $(1, \ldots, 1)$ and $(|h_1|, \ldots, |h_L|)$, $a^2 = (\sum_l |h_l|)^2 \le L \sum_l |h_l|^2$, with equality if and only if the second vector is constant. Multiply by $E_s/(L N_0)$. For the left side, $a^2 = \sum_l |h_l|^2 + \sum_{l \ne k} |h_l||h_k| \ge \sum_l |h_l|^2$, because all terms are nonnegative. $\square$

The left bound is reached in the limit where one gain carries all the power: with $h = (1, 0)$ and a unit weight on the second branch, $\gamma_{\mathrm{EGC}} = \frac12 E_s/N_0$, half of the best single branch. So EGC can be worse than selection combining.

**Theorem 3 (the mean in Rayleigh fading).** If the $h_l$ are independent $CN(0, \Omega)$ and $\bar\gamma = \Omega E_s/N_0$, then $E[\gamma_{\mathrm{EGC}}] = \bar\gamma\,(1 + (L-1)\pi/4)$.

*Proof.* The amplitude $r = |h_l|$ has the Rayleigh density $(2r/\Omega)e^{-r^2/\Omega}$, with $E r^2 = \Omega$ and $E r = \int_0^\infty (2r^2/\Omega) e^{-r^2/\Omega}\, dr = \sqrt{\pi\Omega}/2$. Then $E a^2 = \sum_l E|h_l|^2 + \sum_{l \ne k} E|h_l|\, E|h_k| = L\Omega + L(L-1)\pi\Omega/4$, by independence. Multiply by $E_s/(L N_0)$. $\square$

**Remark (the error rate for two branches).** For $L = 2$, BPSK and independent Rayleigh branches, $P_b = E[Q(a\sqrt{2E_s/(2N_0)})] = E[Q(a\sqrt{\bar\gamma/\Omega})]$ by Theorem 1, an integral over the two amplitudes. The page gives its closed form $\frac12(1 - \sqrt{\bar\gamma(\bar\gamma+2)}/(\bar\gamma+1))$. That closed form is not proved here: the test file compares it with a direct two-dimensional Simpson integral of this expectation in polar coordinates and finds agreement within a relative error of $10^{-5}$ at 0, 5 and 10 dB, and a simulation with a Wilson interval at 5 dB.
