---
title: The matched filter maximizes the output signal to noise ratio, and its threshold test has the stated false alarm and detection probabilities
proves: [correctness]
status: full
---

The notation is that of the page. The pulse is $s[0], \dots, s[N-1]$, not all zero, with energy $E = \sum_n |s[n]|^2$. The noise $w$ is white with variance $\sigma^2 > 0$: $\mathbb{E}[w[n]] = 0$ and $\mathbb{E}[w[n]\overline{w[k]}] = \sigma^2$ if $n = k$ and $0$ otherwise. A filter $h[0], \dots, h[N-1]$, not all zero, is applied as in line L2, $y[n] = \sum_k h[k]\,x[n-k]$.

**Lemma 1 (output at the end of the pulse).** If $x[n] = s[n - t] + w[n]$ for a pulse starting at $t$, then $y[t + N - 1] = \sum_k h[k]\, s[N-1-k] + \sum_k h[k]\, w[t + N - 1 - k]$. The first term is the signal part $g(h)$. The second has mean $0$ and variance $\sigma^2 \sum_k |h[k]|^2$.

*Proof.* Substitute $x$ into line L2 at $n = t + N - 1$. The noise term is a fixed linear combination of distinct noise samples, so its variance is $\sum_k |h[k]|^2 \sigma^2$ by whiteness. $\square$

**Theorem 1 (maximum output signal to noise ratio).** For every nonzero $h$,

$$\mathrm{SNR}(h) = \frac{|g(h)|^2}{\sigma^2 \sum_k |h[k]|^2} \le \frac{E}{\sigma^2},$$

with equality if and only if $h[k] = c\,\overline{s[N-1-k]}$ for some constant $c \ne 0$, the filter of line L1.

*Proof.* By the Cauchy-Schwarz inequality, $|g(h)|^2 = |\sum_k h[k]\, s[N-1-k]|^2 \le \sum_k |h[k]|^2 \sum_k |s[N-1-k]|^2 = E\sum_k|h[k]|^2$. Dividing by $\sigma^2 \sum_k |h[k]|^2$ gives the bound. Equality in Cauchy-Schwarz holds exactly when the vectors $(h[k])$ and $(\overline{s[N-1-k]})$ are proportional. For $h[k] = c\,\overline{s[N-1-k]}$, $g(h) = c\sum_k |s[N-1-k]|^2 = cE$ and $\sum_k|h[k]|^2 = |c|^2 E$, so $\mathrm{SNR} = |c|^2E^2/(\sigma^2|c|^2E) = E/\sigma^2$. $\square$

The bound uses only the second moments of the noise, so Theorem 1 holds for any white noise, Gaussian or not.

**Theorem 2 (the threshold test).** Let the data be real, the noise real Gaussian, and the test at start time $t$ be $T = y[t + N - 1] > \gamma$ with $\gamma = \sigma\sqrt{E}\,Q^{-1}(P_{FA})$ as in line L3, where $Q(u) = \Pr(Z > u)$ for a standard normal $Z$. Then the probability of a false alarm, $T > \gamma$ when $x = w$, is $P_{FA}$, and the probability of detection, $T > \gamma$ when $x[n] = s[n - t] + w[n]$, is $P_D = Q(Q^{-1}(P_{FA}) - \sqrt{E/\sigma^2})$.

*Proof.* With $h$ from line L1 and $c = 1$, $T = \sum_n s[n]\, x[t + n]$. Under the noise alone, $T = \sum_n s[n]\, w[t+n]$ is a linear combination of independent normal variables, so it is normal with mean $0$ and variance $\sigma^2 E$, and $\Pr(T > \gamma) = Q(\gamma/(\sigma\sqrt E)) = Q(Q^{-1}(P_{FA})) = P_{FA}$. With the pulse, $T = E + \sum_n s[n]w[t+n]$ is normal with mean $E$ and variance $\sigma^2 E$, so $\Pr(T > \gamma) = Q((\gamma - E)/(\sigma\sqrt E)) = Q(Q^{-1}(P_{FA}) - \sqrt{E}/\sigma)$. $\square$

**Theorem 3 (the test is most powerful).** For a known pulse in real white Gaussian noise, among all tests of "noise only" against "pulse at $t$" with false alarm probability at most $P_{FA}$, the test of Theorem 2 has the largest probability of detection.

*Proof.* Let $v = (x[t], \dots, x[t+N-1])$. The two densities are $p_0(v) \propto \exp(-\|v\|^2/(2\sigma^2))$ and $p_1(v) \propto \exp(-\|v - s\|^2/(2\sigma^2))$, so the log likelihood ratio is $\ln(p_1/p_0) = (2\langle s, v\rangle - E)/(2\sigma^2) = (T - E/2)/\sigma^2$, an increasing function of $T$. By the Neyman-Pearson lemma, proved on the signal detection page, the most powerful test at level $P_{FA}$ rejects the noise hypothesis when the likelihood ratio exceeds a constant, which is the same as $T > \gamma$ for the $\gamma$ that gives level $P_{FA}$. Because $T$ has a continuous distribution, no randomization is needed and Theorem 2 gives the level. $\blacksquare$

**Line L5.** Lines L4 and L5 apply the test of Theorem 2 at every start time $t$ from $0$ to $M - N$. Each test has false alarm probability $P_{FA}$; the tests are not independent, because neighboring outputs share noise samples, so the expected number of false alarms in a record is $(M - N + 1)P_{FA}$ but their count is not binomial.
