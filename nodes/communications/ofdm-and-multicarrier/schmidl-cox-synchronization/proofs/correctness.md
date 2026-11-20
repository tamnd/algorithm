---
title: "The Schmidl-Cox metric is 1 on the ISI-free starts, its angle gives the fractional offset, and the second symbol gives the even integer part"
proves: [correctness]
status: full
---

Notation. $N$ is even, and the half length is $N/2$. The unitary DFT pair is the one of the OFDM page, $x = F^H X$ with $F[k, n] = e^{-j 2\pi k n / N} / \sqrt N$, and $j$ is the imaginary unit. The channel has $L$ taps, the prefix has $N_{cp} \ge L - 1$ samples, and the carrier frequency offset is $\varepsilon$ subcarrier spacings, so the receiver sees

$$r[i] = e^{j 2\pi \varepsilon i / N}\, (h * s)[i] + w[i],$$

with $s$ the sent samples and $w[i]$ independent $\mathcal{CN}(0, N_0)$. The first training symbol $X_1$ is zero on the odd subcarriers, and the second, $X_2$, is nonzero on the even ones; $v[k] = X_2[k] / X_1[k]$ for even $k$. Lines L1 to L4 compute

$$P(d) = \sum_{m=0}^{N/2-1} r[d + m]^*\, r[d + m + N/2], \qquad R(d) = \sum_{m=0}^{N/2-1} |r[d + m + N/2]|^2, \qquad M(d) = \frac{|P(d)|^2}{R(d)^2}.$$

**Lemma 1 (two equal halves).** If $X_1[k] = 0$ for every odd $k$, then $x_1[n + N/2] = x_1[n]$ for $n = 0, \ldots, N/2 - 1$.

*Proof.* $x_1[n + N/2] = \frac{1}{\sqrt N} \sum_k X_1[k]\, e^{j 2\pi k n / N} e^{j\pi k}$, and $e^{j\pi k} = 1$ for every even $k$, while the odd terms are zero. $\square$

**Lemma 2 (the recursion).** Lines L2 and L3 give the sums above for every $d \ge 1$ if they start from the direct sums at $d = 0$.

*Proof.* Going from $d - 1$ to $d$, the sum for $P$ loses the term $m = 0$ of $d - 1$, which is $r[d - 1]^* r[d - 1 + N/2]$, and gains the term $m = N/2 - 1$ of $d$, which is $r[d - 1 + N/2]^* r[d - 1 + N]$. The same holds for $R$ with $|r[d - 1 + N/2]|^2$ and $|r[d - 1 + N]|^2$. $\square$

**Lemma 3 (the plateau).** Without noise, let the first training symbol start (with its prefix) at sample $t$, so its body starts at $t + N_{cp}$. For every $d$ with $t + L - 1 \le d \le t + N_{cp}$, $P(d) = e^{j\pi\varepsilon} R(d)$, so $M(d) = 1$ and $\angle P(d) = \pi \varepsilon$ modulo $2\pi$, if $R(d) > 0$. There are $N_{cp} - L + 2$ such $d$.

*Proof.* Let $c = h * s$. For $t + L - 1 \le i \le t + N_{cp} + N - 1$, the sample $c[i]$ only uses sent samples of the first training symbol, and as in Lemma 1 of the OFDM page it equals the circular convolution of $h$ and $x_1$ at index $i - t - N_{cp}$ modulo $N$. A circular convolution with a sequence of period $N/2$ (Lemma 1) has period $N/2$, so $c[i + N/2] = c[i]$ whenever both $i$ and $i + N/2$ are in this range. For $d$ in the stated range and $0 \le m < N/2$, the indices $d + m$ and $d + m + N/2$ are both in it. Then $r[d + m + N/2] = e^{j\pi\varepsilon}\, r[d + m]$, because the offset factor advances by $e^{j 2\pi \varepsilon (N/2)/N}$. Substituting gives $P(d) = e^{j\pi\varepsilon} \sum_m |r[d + m]|^2$, and the same relation gives $\sum_m |r[d + m]|^2 = R(d)$. The count is $(t + N_{cp}) - (t + L - 1) + 1$. $\square$

**Remark (M can pass 1 elsewhere).** By the Cauchy-Schwarz inequality, $|P(d)|^2 \le R_1(d) R(d)$ with $R_1(d) = \sum_m |r[d + m]|^2$, the energy of the first half. So $M(d) \le R_1(d) / R(d)$, which is 1 on the plateau but can be larger than 1 next to it, where the two halves have different energies. The global maximum of $M$ is then not on the plateau. This is why the implementation offers the middle of the 90 percent plateau as the timing estimate.

**Lemma 4 (the fractional part).** If $d$ is on the plateau, line L6 returns $\varepsilon_f = \angle P(d) / \pi \in (-1, 1]$, and $\varepsilon - \varepsilon_f = 2g$ for an integer $g$.

*Proof.* By Lemma 3, $\angle P(d) = \pi\varepsilon - 2\pi g$ for the integer $g$ that puts the angle in $(-\pi, \pi]$. Divide by $\pi$. $\square$

**Lemma 5 (the even integer part).** After line L7 removes $\varepsilon_f$, the remaining offset is the even integer $2g$. Let $Y_1$ and $Y_2$ be the DFTs of line L8 taken at plateau starts, without noise. Define

$$B(g') = \frac{\left| \sum_{k \text{ even}} \left( Y_1[k + 2g']\, v[k] \right)^* Y_2[k + 2g'] \right|^2}{2 \left( \sum_{k \text{ even}} |Y_2[k]|^2 \right)^2},$$

with indices modulo $N$, where the training symbols satisfy $|X_1[k]|^2 = 2$ on the even subcarriers and $|X_2[k]| = 1$. Then $B(g') \le 1/2$ for every $g'$, and $B(g) = 1/2$ for the true $g$.

*Proof.* An integer offset $2g$ multiplies sample $n$ of each window by $e^{j 2\pi (2g) n / N}$ times a constant phase, so it shifts the DFT: $Y_i[k + 2g] = e^{j\theta_i}\, G[k]\, X_i[k]$, where $G[k]$ is the channel gain with the phase ramp of the window start, the same for both symbols because both windows start at the same position in their symbols, and $\theta_1$, $\theta_2$ are constants. Hence for the true $g$,

$$\left( Y_1[k + 2g]\, v[k] \right)^* Y_2[k + 2g] = e^{j(\theta_2 - \theta_1)}\, |G[k]|^2\, X_1[k]^* v[k]^* X_2[k] = e^{j(\theta_2 - \theta_1)}\, |G[k]|^2 |X_2[k]|^2,$$

because $X_1 v = X_2$. All terms have the same phase, so the numerator is $(\sum_{k \text{ even}} |G[k]|^2)^2$, and the denominator is $2 (\sum_{k \text{ even}} |G[k]|^2)^2$, because the even subcarriers are closed under a shift by $2g$ and $|Y_2[k + 2g]| = |G[k]|$. So $B(g) = 1/2$. For any $g'$, the Cauchy-Schwarz inequality bounds the numerator by $\sum_{k \text{ even}} |Y_1[k + 2g'] v[k]|^2 \cdot \sum_{k \text{ even}} |Y_2[k + 2g']|^2$. Here $|v[k]|^2 = 1/2$, and $|Y_1[k']|^2 = 2 |Y_2[k']|^2$ on the even $k'$ (both are $|G|^2$ times $2$ or $1$ at the same position), so each factor equals $\sum_{k \text{ even}} |Y_2[k]|^2$ after the shift. So $B(g') \le 1/2$. $\square$

Equality at a wrong $g'$ needs $Y_1[k + 2g'] v[k]$ to be proportional to $Y_2[k + 2g']$ on all even $k$, which a random code $v$ avoids with high probability. Line L9 searches $|g'| \le g_{\max}$, so the true $g$ must be in that range.

**Theorem (noise-free correctness).** Without noise, with $N_{cp} \ge L - 1$, a timing estimate $\hat d$ on the plateau, $|g| \le g_{\max}$ and no tie in line L9, line L10 returns $\hat d$ and $\varepsilon_f + 2\hat g = \varepsilon$ exactly.

*Proof.* Lemmas 3 to 5. $\blacksquare$

**Variance of the fractional estimate (a closed form at high SNR).** At a plateau start, let $s_m$ be the noise-free samples of the first half, $E = \sum_m |s_m|^2$, and write the noise of the two halves as $n_m$ and $n'_m$, all independent $\mathcal{CN}(0, N_0)$. Then

$$e^{-j\pi\varepsilon} P = E + \sum_m s_m^* n'_m e^{-j\pi\varepsilon} + \sum_m n_m^* s_m + \sum_m n_m^* n'_m e^{-j\pi\varepsilon} = E + Z.$$

The three noise sums are uncorrelated with zero mean. The first two have variance $E N_0$ each and the third $(N/2) N_0^2$. For a small $Z$, $\angle(E + Z) \approx \operatorname{Im}(Z) / E$, and $\operatorname{Im}(Z)$ has half the variance of $Z$, so

$$\operatorname{var}(\pi \varepsilon_f) \approx \frac{2 E N_0 + (N/2) N_0^2}{2 E^2}.$$

With the mean sample energy $E_s$ and $\text{SNR} = E_s / N_0$ per sample, $E = (N/2) E_s$, and

$$\operatorname{var}(\varepsilon_f) \approx \frac{1}{\pi^2 (N/2)\, \text{SNR}} \left( 1 + \frac{1}{2\,\text{SNR}} \right).$$

For $N = 64$ at 10 dB this is $3.3245 \times 10^{-4}$, and the tests measure it within 15 percent. At a high SNR the leading term $1/(\pi^2 (N/2)\, \text{SNR})$ dominates; the factor $1 + 1/(2\,\text{SNR})$ comes from the noise-times-noise term.
