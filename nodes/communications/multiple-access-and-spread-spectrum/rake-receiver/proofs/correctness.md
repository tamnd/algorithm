---
title: The rake output is the matched filter to the received pulse, and its weights maximize the output SNR
proves: [correctness]
status: full
---

The model is one symbol $b$ of a direct-sequence signal with a cyclic prefix. The code is $c \in \mathbb{C}^N$ with $\|c\|^2 = 1$. Write $T^d c$ for the code delayed by $d$ chips cyclically, $(T^d c)[n] = c[(n - d) \bmod N]$. The channel has $L$ paths with distinct delays $d_1, \ldots, d_L$ and known gains $h_1, \ldots, h_L$. The received block is

$$r = \sqrt{E_s}\, b\, g + w, \qquad g = \sum_{l=1}^{L} h_l\, T^{d_l} c, \qquad w \sim \mathcal{CN}(0, N_0 I_N).$$

The finger outputs are $z_l = \langle T^{d_l} c, r \rangle = \sum_n \overline{c[(n - d_l) \bmod N]}\, r[n]$, and the rake returns $y = \sum_l \overline{h_l}\, z_l$ (lines L1 to L5). Let $R$ be the $L \times L$ matrix with $R_{lm} = \langle T^{d_l} c, T^{d_m} c \rangle$, the periodic autocorrelation of the code at the shift $d_m - d_l$. It is Hermitian and positive semidefinite, with $R_{ll} = 1$. We assume that it is positive definite, which holds when the shifted codes are linearly independent; for an m-sequence, $R = (1 + 1/N) I - (1/N) \mathbf{1}\mathbf{1}^T$, whose eigenvalues are $1 + 1/N$ and $(1 + 1/N) - L/N > 0$ for $L \le N$.

**Lemma 1 (the loop computes the defined sum).** After the loop, $y = \sum_l \overline{h_l} z_l$.

*Proof.* L1 sets $y = 0$. The loop visits each finger once (L2). At finger $l$, L3 computes $z_l$ by its definition and L4 adds $\overline{h_l} z_l$. By induction on the number of fingers visited, after $k$ fingers $y$ is the sum over those $k$ fingers. After all $L$, it is the full sum, which L5 returns. $\square$

**Lemma 2 (matched filter).** $y = \langle g, r \rangle$.

*Proof.* The inner product $\langle u, v \rangle = \sum_n \overline{u[n]}\, v[n]$ is conjugate-linear in $u$. So
$$\langle g, r \rangle = \Big\langle \sum_l h_l T^{d_l} c, \ r \Big\rangle = \sum_l \overline{h_l}\, \langle T^{d_l} c, r \rangle = \sum_l \overline{h_l}\, z_l = y. \quad \square$$

**Lemma 3 (the statistic is sufficient).** Given $r$, the likelihood of a symbol value $b$ depends on $r$ only through $\langle g, r \rangle$. For BPSK with $b \in \{+1, -1\}$ and equal priors, the maximum likelihood decision is the sign of $\operatorname{Re} y$.

*Proof.* The density of $r$ given $b$ is $(\pi N_0)^{-N} \exp(-\|r - \sqrt{E_s} b g\|^2 / N_0)$. Expand the norm:
$$\|r - \sqrt{E_s} b g\|^2 = \|r\|^2 - 2\sqrt{E_s}\, \operatorname{Re}\big(\overline{b}\, \langle g, r\rangle\big) + E_s |b|^2 \|g\|^2.$$
The first term does not depend on $b$, and the others depend on $r$ only through $\langle g, r\rangle = y$. For $b = \pm 1$, $|b|^2 = 1$, so the likelihood is larger for $b = +1$ exactly when $\operatorname{Re} y > 0$. $\square$

**Lemma 4 (output statistics).** $\|g\|^2 = h^H R h$, and $y = \sqrt{E_s}\, b\, \|g\|^2 + v$ with $v \sim \mathcal{CN}(0, N_0 \|g\|^2)$. For BPSK, the error probability of the decision in Lemma 3 is
$$P_b = Q\Big(\sqrt{2 E_s\, h^H R h / N_0}\Big).$$

*Proof.* $\|g\|^2 = \sum_{l,m} \overline{h_l} h_m \langle T^{d_l} c, T^{d_m} c\rangle = h^H R h$. By Lemma 2, $y = \sqrt{E_s} b \langle g, g\rangle + \langle g, w\rangle$. The term $v = \langle g, w \rangle$ is a fixed linear combination of independent $\mathcal{CN}(0, N_0)$ samples, so it is circularly symmetric Gaussian with variance $N_0 \|g\|^2$; its real part has variance $N_0 \|g\|^2 / 2$. Given $b = +1$, an error occurs when $\operatorname{Re} v < -\sqrt{E_s} \|g\|^2$, with probability $Q\big(\sqrt{E_s} \|g\|^2 / \sqrt{N_0 \|g\|^2/2}\big) = Q\big(\sqrt{2 E_s \|g\|^2 / N_0}\big)$. The case $b = -1$ is symmetric. $\square$

**Lemma 5 (maximal ratio weights are best).** For any nonzero weights $a \in \mathbb{C}^L$, the combiner $y_a = \sum_l \overline{a_l} z_l$ has output SNR
$$\mathrm{SNR}(a) = \frac{E_s\, |a^H R h|^2}{N_0\, a^H R a} \;\le\; \frac{E_s\, h^H R h}{N_0},$$
with equality if and only if $a$ is a nonzero multiple of $h$.

*Proof.* The vector of finger outputs is $z = \sqrt{E_s} b R h + u$, where $u_l = \langle T^{d_l} c, w\rangle$ has covariance $E[u u^H] = N_0 R$. So $y_a = a^H z$ has signal part $\sqrt{E_s} b\, a^H R h$ and noise variance $N_0\, a^H R a$, which gives the formula for $\mathrm{SNR}(a)$. Since $R$ is positive definite, $\langle a, h \rangle_R = a^H R h$ is an inner product, and the Cauchy-Schwarz inequality gives $|a^H R h|^2 \le (a^H R a)(h^H R h)$, with equality exactly when $a$ and $h$ are parallel. Dividing by $a^H R a > 0$ gives the bound. $\square$

**Theorem.** The rake receiver returns $y = \langle g, r\rangle$, the output of the filter matched to the received pulse. The sign of $\operatorname{Re} y$ is the maximum likelihood BPSK decision, with error probability $Q(\sqrt{2 E_s h^H R h / N_0})$, and no other choice of finger weights gives a larger output SNR. When the shifted codes are orthogonal ($R = I$), $h^H R h = \sum_l |h_l|^2$, the SNR of maximal ratio combining over $L$ independent branches.

*Proof.* Lemmas 1 to 5. $\square$

**Cost.** Each finger computes one correlation of $N$ products (L3) and one multiply-add (L4). The total is $\Theta(L N)$ operations per symbol and $\Theta(1)$ space beyond the input.
