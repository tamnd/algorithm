---
title: Maximal ratio combining gives the largest output SNR of any linear combiner, equal to the sum of the branch SNRs, and keeps all information about the symbol
proves: [correctness]
status: full
---

Branch $l = 1, \ldots, L$ receives $y_l = h_l x + w_l$, with $E|x|^2 = E_s$ and $w_l \sim CN(0, N_{0,l})$ independent of each other and of $x$, and $N_{0,l} > 0$. The gains $h_l$ are known and not all zero. Write $\gamma_l = |h_l|^2 E_s/N_{0,l}$ and $g = \sum_l |h_l|^2 / N_{0,l} > 0$.

**Lemma 1 (SNR of a linear combiner).** For weights $c = (c_1, \ldots, c_L) \ne 0$, $z = \sum_l c_l^* y_l = (\sum_l c_l^* h_l)\, x + \sum_l c_l^* w_l$, and the ratio of signal energy to noise variance is

$$\mathrm{SNR}(c) = \frac{E_s \left|\sum_l c_l^* h_l\right|^2}{\sum_l |c_l|^2 N_{0,l}}.$$

*Proof.* The noise term $\sum_l c_l^* w_l$ is a sum of independent zero-mean terms, so its variance is $\sum_l |c_l|^2 E|w_l|^2 = \sum_l |c_l|^2 N_{0,l}$, which is positive because $c \ne 0$. The signal term has energy $|\sum_l c_l^* h_l|^2 E_s$. $\square$

**Theorem 1 (MRC is the best linear combiner).** $\mathrm{SNR}(c) \le \sum_l \gamma_l$ for every $c \ne 0$, with equality if and only if $c_l = a\, h_l/N_{0,l}$ for all $l$, for some complex $a \ne 0$.

*Proof.* Let $u_l = c_l \sqrt{N_{0,l}}$ and $v_l = h_l / \sqrt{N_{0,l}}$. Then $\sum_l c_l^* h_l = \sum_l u_l^* v_l$, and the Cauchy-Schwarz inequality gives $|\sum_l u_l^* v_l|^2 \le \sum_l |u_l|^2 \sum_l |v_l|^2 = \sum_l |c_l|^2 N_{0,l} \cdot g$. Divide by $\sum_l |c_l|^2 N_{0,l}$ and multiply by $E_s$: $\mathrm{SNR}(c) \le E_s g = \sum_l \gamma_l$. Equality in Cauchy-Schwarz holds if and only if $u = a v$ for a scalar $a$ (with $u \ne 0$, so $a \ne 0$), which is $c_l\sqrt{N_{0,l}} = a\, h_l/\sqrt{N_{0,l}}$, that is $c_l = a\, h_l / N_{0,l}$. $\square$

**Corollary (the output of the algorithm).** With $c_l = h_l/N_{0,l}$ as in line L1, line L2 gives $z = g x + n'$ with $n' = \sum_l (h_l^*/N_{0,l}) w_l$ of variance $\sum_l |h_l|^2/N_{0,l} = g$. So $z/g = x + n$ with $n \sim CN(0, 1/g)$, and the output SNR is $E_s g = \sum_l \gamma_l$. With no noise, $z/g = x$ exactly.

*Proof.* $\sum_l (h_l^*/N_{0,l}) h_l = g$, and Lemma 1 with $c_l = h_l / N_{0,l}$ gives the variance $\sum_l |h_l|^2 N_{0,l}/N_{0,l}^2 = g$. A sum of independent circular Gaussian variables is circular Gaussian. $\square$

**Theorem 2 (no loss of information).** Given $h$ and the $N_{0,l}$, $z$ is a sufficient statistic for $x$. So for any finite set of symbols with any prior, the maximum likelihood (or maximum a posteriori) decision from $z/g$ in Gaussian noise of variance $1/g$ is the same as the decision from all of $y_1, \ldots, y_L$.

*Proof.* The likelihood is $p(y \mid x) = \prod_l \frac{1}{\pi N_{0,l}} \exp(-|y_l - h_l x|^2 / N_{0,l})$. Expand the exponent: $\sum_l |y_l - h_l x|^2/N_{0,l} = \sum_l |y_l|^2/N_{0,l} - 2\operatorname{Re}(x^* z) + g|x|^2$, with $z = \sum_l h_l^* y_l / N_{0,l}$. The first term does not depend on $x$, and the rest depends on $y$ only through $z$. By the factorization theorem, $z$ is sufficient. The same expansion with one observation $z/g = x + n$, $n \sim CN(0, 1/g)$, gives the exponent $g|z/g - x|^2 = |z|^2/g - 2\operatorname{Re}(x^* z) + g|x|^2$, which differs from the one above by a term free of $x$, so both give the same ranking of the candidates $x$. $\square$

**Remark (Rayleigh branches).** If the $h_l$ are independent $CN(0, \Omega)$ and all $N_{0,l} = N_0$, the $\gamma_l$ are independent exponential with mean $\bar\gamma = \Omega E_s/N_0$, so $\gamma = \sum_l \gamma_l$ has the gamma distribution with shape $L$ and scale $\bar\gamma$. Its distribution function is $1 - e^{-x/\bar\gamma}\sum_{k=0}^{L-1}(x/\bar\gamma)^k/k!$, which is the outage formula of the page, and its moment generating function $E e^{-s\gamma} = (1 + s\bar\gamma)^{-L}$ with Craig's form of the Q function, $Q(\sqrt{2\gamma}) = \frac1\pi\int_0^{\pi/2} e^{-\gamma/\sin^2\theta}\, d\theta$, gives the BPSK error rate $P_b = \frac1\pi\int_0^{\pi/2}(1 + \bar\gamma/\sin^2\theta)^{-L} d\theta$. The test file checks that this integral equals the closed form with $\mu$ within a relative error of $10^{-9}$.
