---
title: The Mueller and Muller detector has the S-curve g(1 - Delta) - g(1 + Delta), it has no self-noise at lock for a Nyquist pulse, and its loop variance is 32 xi times the MCRB at high SNR
proves: [correctness]
status: full
---

Times are in symbol periods, $T = 1$. After carrier phase correction, the matched filter output is $y(t) = \sum_m a_m g(t - m - \tau) + v(t)$. The overall pulse $g$ is real and even, the data are independent with $E a_m = 0$ and $E|a_m|^2 = 1$, and the noise $v$ is independent of the data, stationary, with zero mean and autocorrelation $E[v(t)\overline{v(s)}] = N_0\,g(t - s)$, as at the output of a matched filter. Line L3 takes the strobe $y_k = y(k + \tau_k)$, line L4 gives the symbol $\hat a_k$ (a decision, or a known symbol), and line L6 forms
$$e_k = \operatorname{Re}\bigl\{\overline{\hat a_{k-1}}\,y_k - \overline{\hat a_k}\,y_{k-1}\bigr\}.$$
Write $\Delta = \tau - \tau_k$, and take $\tau_k = \tau_{k-1}$ while the mean is taken.

**Theorem 1 (S-curve with correct symbols).** If $\hat a_k = a_k$ for all $k$, then $E[e_k] = g(1 - \Delta) - g(1 + \Delta)$.

*Proof.* $y_k = \sum_m a_m g(k - m - \Delta) + v_k$. Since the data are independent with mean zero and $E|a|^2 = 1$, $E[\overline{a_{k-1}}\,y_k] = g(k - (k - 1) - \Delta) = g(1 - \Delta)$, and $E[\overline{a_k}\,y_{k-1}] = g(-1 - \Delta) = g(1 + \Delta)$ because $g$ is even. The noise is independent of the data and has mean zero. $\square$

So the S-curve is odd in $\Delta$ and zero at $\Delta = 0$. Its slope there is $K_D = -2g'(1)$. For the raised cosine pulse with roll-off $\beta$, $g'(1) = -\cos(\pi\beta)/(1 - 4\beta^2)$, so $K_D = 2\cos(\pi\beta)/(1 - 4\beta^2)$, with the limit $\pi/2$ at $\beta = \frac12$. $K_D > 0$ for $0 \le \beta < 1$, so $\Delta = 0$ is a stable point of the loop of lines L7 and L8 with $K_p > 0$.

**Lemma 1 (no self-noise at lock).** If $g$ satisfies the Nyquist condition $g(m) = \delta_m$, $\Delta = 0$, there is no noise and the symbols are correct, then $e_k = 0$ for every data sequence.

*Proof.* At $\Delta = 0$, $y_k = \sum_m a_m g(k - m) = a_k$. Then $e_k = \operatorname{Re}\{\overline{a_{k-1}}a_k - \overline{a_k}a_{k-1}\} = \operatorname{Re}\{2j\operatorname{Im}(\overline{a_{k-1}}a_k)\} = 0$. $\square$

So $\tau_k = \tau$ is an exact fixed point of the loop for random data, not only for a special pattern. This is the main difference from the early-late gate and the Gardner detector, which have self-noise.

**Lemma 2 (noise at lock).** At $\Delta = 0$ with correct symbols from a PSK constellation ($|a| = 1$), the detector output is $e_k = \operatorname{Re}\{\overline{a_{k-1}}v_k - \overline{a_k}v_{k-1}\}$. The samples $v_k$ are white $\mathcal{CN}(0, N_0)$, $E[e_k^2] = N_0$, and $E[e_k e_{k+1}] = 0$ averaged over the data. So the noise of the detector has the spectral density $S(0) = N_0$.

*Proof.* The first claim is Lemma 1 plus the noise. $E[v_k\overline{v_{k'}}] = N_0 g(k - k') = N_0\delta_{k-k'}$, so the samples are white. For a complex $z$ with independent parts of variance $\sigma^2/2$, $E[(\operatorname{Re}\{\overline{a}z\})^2] = |a|^2\sigma^2/2$. The two terms of $e_k$ use different noise samples, so $E[e_k^2] = \frac{N_0}{2} + \frac{N_0}{2} = N_0$. The pair $e_k, e_{k+1}$ shares only $v_k$, and its covariance is $-\frac{N_0}{2}\operatorname{Re}\{\overline{a_{k-1}}a_{k+1}\}$, whose mean over the independent data is zero. Pairs further apart share no noise sample. $\square$

**Theorem 2 (loop variance).** In the linear model of a first-order loop with noise bandwidth $B_L T$, correct symbols and PSK data, the variance of $\tau_k$ is $\sigma_\tau^2 = 2B_LT\,N_0/K_D^2$. In units of the loop form of the MCRB, $B_LT/(4\pi^2\xi\,\mathrm{SNR})$ with $\mathrm{SNR} = 1/N_0$,
$$\frac{\sigma_\tau^2}{\mathrm{MCRB}} = \frac{8\pi^2\xi}{K_D^2}.$$
For $\beta = \frac12$, $K_D = \pi/2$ and $\xi = 0.0951727$, the ratio is $32\xi = 3.0455$.

*Proof.* The linear model of the [phase-locked loop](/phase-locked-loop/) gives the variance $2B_LT\,S(0)/K_D^2$ for a detector with slope $K_D$ and white noise of density $S(0)$. Lemma 2 gives $S(0) = N_0$. Divide by the bound. $\square$

The variance is a closed form under assumptions: the linear model, correct decisions, and white noise at the detector output. It holds at high SNR; at low SNR wrong decisions add errors and bend the S-curve. The tests measure ratios of $2.76$ to $3.62$ at 10 dB over three seeds, against $3.05$. The detector is not phase invariant: it needs the carrier phase, since the symbol $\hat a_k$ and the strobe $y_k$ are compared directly.
