---
title: The Moose estimate is exact without noise and is the maximum likelihood estimate for two repeated symbols in white noise
proves: [correctness]
status: full
---

Notation. $N$ is the DFT size, $j$ the imaginary unit, and $F$ the unitary DFT, $F[k, n] = e^{-j 2\pi k n / N} / \sqrt N$. The transmitter sends one block $x$ of $N$ samples twice; the second copy starts $N + G$ samples after the first. The channel has $L$ taps, and the first copy is preceded by at least $L - 1$ samples that repeat its tail, as a cyclic prefix does. If $G = 0$, the second copy is preceded by the end of the first copy, which is its own tail; if $G > 0$, each copy has its own prefix of $G \ge L - 1$ samples. The receiver sees $r[i] = e^{j 2\pi\varepsilon i / N} (h * s)[i] + w[i]$ with the offset $\varepsilon$ in subcarrier spacings and $w[i]$ independent $\mathcal{CN}(0, N_0)$. The windows are $y_1 = r[t, \ldots, t + N - 1]$ and $y_2 = r[t + N + G, \ldots, t + 2N + G - 1]$, where $t$ is the start of the first copy. Lines L1 to L3 compute $Y_i = F y_i$, $C = \sum_k Y_1[k]^* Y_2[k]$ and $\hat\varepsilon = \angle C \cdot N / (2\pi (N + G))$. Let $\phi = 2\pi\varepsilon (N + G) / N$.

**Lemma 1 (the two windows differ by one phase).** Without noise, $y_2[n] = e^{j\phi}\, y_1[n]$ for $n = 0, \ldots, N - 1$.

*Proof.* Let $c = h * s$. The sample $c[t + n]$ uses $s[t + n - l]$ for $l = 0, \ldots, L - 1$, and $c[t + N + G + n]$ uses $s[t + N + G + n - l]$. For $n - l \ge 0$ both are $x[n - l]$. For $n - l < 0$, the first is a prefix sample, $x[N + n - l]$, and the second is either the tail of the first copy ($G = 0$) or a sample of the second prefix ($G > 0$), which is also $x[N + n - l]$, because $l \le L - 1$ is not longer than the part that repeats the tail. So $c[t + N + G + n] = c[t + n]$, and the offset factors differ by $e^{j 2\pi\varepsilon (N + G) / N} = e^{j\phi}$. $\square$

**Lemma 2 (time or frequency domain).** $C = \sum_k Y_1[k]^* Y_2[k] = \sum_n y_1[n]^* y_2[n]$, and $Y_2 = e^{j\phi} Y_1$ without noise.

*Proof.* The first is the Plancherel identity for the unitary $F$, $\langle F y_1, F y_2 \rangle = \langle y_1, y_2 \rangle$. The second is the linearity of $F$ applied to Lemma 1. $\square$

The inter-carrier interference that the offset causes inside each window is the same in both windows up to the factor $e^{j\phi}$, so it does not disturb the relation $Y_2 = e^{j\phi} Y_1$.

**Theorem 1 (exact without noise).** If $y_1 \ne 0$ and $|\varepsilon| < N / (2(N + G))$, the algorithm returns $\varepsilon$ exactly.

*Proof.* By Lemma 2, $C = e^{j\phi} \sum_k |Y_1[k]|^2$ with a positive sum, so $\angle C = \phi$ modulo $2\pi$. The bound on $\varepsilon$ gives $|\phi| < \pi$, so the principal angle is $\phi$ itself, and line L3 returns $\phi N / (2\pi (N + G)) = \varepsilon$. $\square$

**Theorem 2 (maximum likelihood).** Model the windows as $Y_1 = S + W_1$ and $Y_2 = e^{j\phi} S + W_2$, with $S \in \mathbb{C}^N$ unknown and $W_1$, $W_2$ independent white Gaussian noise. The joint maximum likelihood estimate of $(S, \phi)$ has $\hat\phi = \angle C$, so $\hat\varepsilon$ of line L3 is the maximum likelihood estimate of $\varepsilon$ in the range of Theorem 1.

*Proof.* The unitary $F$ keeps white Gaussian noise white with the same variance, so the model in the frequency domain follows from Lemma 2. The log-likelihood is a constant minus $\frac{1}{N_0} \sum_k \left( |Y_1[k] - S[k]|^2 + |Y_2[k] - e^{j\phi} S[k]|^2 \right)$. For a fixed $\phi$, each term is smallest at $S[k] = \frac12 (Y_1[k] + e^{-j\phi} Y_2[k])$, the midpoint of $Y_1[k]$ and $e^{-j\phi} Y_2[k]$, and the smallest value is $\frac12 |Y_1[k] - e^{-j\phi} Y_2[k]|^2$. Expanding,

$$\sum_k \frac12 \left| Y_1[k] - e^{-j\phi} Y_2[k] \right|^2 = \frac12 \sum_k \left( |Y_1[k]|^2 + |Y_2[k]|^2 \right) - \operatorname{Re}\left( e^{-j\phi} C \right).$$

Only the last term depends on $\phi$, so the estimate maximizes $\operatorname{Re}(e^{-j\phi} C) = |C| \cos(\angle C - \phi)$, which gives $\hat\phi = \angle C$. The map from $\phi$ to $\varepsilon$ is one to one on the range, so the estimate of $\varepsilon$ is also the maximum likelihood estimate. $\square$

**The variance (a closed form at high SNR).** Let $E = \sum_n |y_1[n]|^2$ without noise, so $e^{-j\phi} C = E + Z$ with three uncorrelated zero-mean noise sums of variances $E N_0$, $E N_0$ and $N N_0^2$. Linearizing the angle, $\hat\phi - \phi \approx \operatorname{Im}(Z) / E$, and $\operatorname{Im}(Z)$ has half the variance of $Z$, so

$$\operatorname{var}(\hat\phi) \approx \frac{2 E N_0 + N N_0^2}{2 E^2}, \qquad \operatorname{var}(\hat\varepsilon) \approx \left( \frac{N}{2\pi (N + G)} \right)^2 \frac{N_0}{E} \left( 1 + \frac{N N_0}{2E} \right).$$

With $E = N E_s$, $\text{SNR} = E_s / N_0$ and $G = 0$, this is $\frac{1}{4\pi^2 N\, \text{SNR}} (1 + \frac{1}{2\,\text{SNR}})$, which is $1.6623 \times 10^{-4}$ for $N = 16$ at 10 dB. The tests measure it within 15 percent.
