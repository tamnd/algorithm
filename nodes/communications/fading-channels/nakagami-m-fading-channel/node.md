---
tag: 2B42MX
kind: model
slug: nakagami-m-fading-channel
name: Nakagami-m fading channel
aliases:
- Nakagami fading
area: communications/fading-channels
level: core
summary: "The flat fading channel whose power gain is Gamma distributed with shape m >= 1/2: m = 1 is Rayleigh, m = 1/2 is worse, and large m is close to no fading."
prereqs: [rayleigh-fading-channel, moment-generating-function]
see_also: [rayleigh-fading-channel, rician-fading-channel, maximal-ratio-combining, diversity-order, outage-probability, method-of-moments, bit-error-rate, moment-generating-function]
sources:
  - paper: "M. Nakagami, The m-distribution, a general formula of intensity distribution of rapid fading, in W. C. Hoffman (editor), Statistical Methods in Radio Wave Propagation, Pergamon Press, Oxford, 1960, pages 3 to 36"
    title: The m-distribution, a general formula of intensity distribution of rapid fading
    locator: pp. 3 to 36 (the m-distribution of the fading amplitude, its parameter m, and its fit to measured fading)
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 3.2.2 (envelope and power distributions, including the Nakagami distribution), Section 6.3.2 (average probability of error) and Section 6.3.3 (the moment generating function approach)
---

The Nakagami-m fading channel is the flat fading channel $y = h x + w$ in which the power gain $|h|^2$ has a Gamma distribution with shape $m \ge 1/2$. The one parameter $m$ sets the depth of the fades: $m = 1$ gives the [Rayleigh fading channel](/rayleigh-fading-channel/), $m = 1/2$ gives deeper fades than Rayleigh, and $m \to \infty$ gives no fading. Nakagami proposed the distribution in 1960 as a fit to measured fading. It is popular because many results have closed forms, and with integer $m$ it is also the exact SNR after combining $m$ Rayleigh branches.

## The machine

$$y = h x + w, \qquad |h|^2 \sim \mathrm{Gamma}\left(m, \frac{\Omega}{m}\right), \qquad w \sim \mathcal{CN}(0, N_0),$$

with shape $m \ge 1/2$ and scale $\Omega/m$, so that $\mathbb{E}|h|^2 = \Omega$. The density of the power and of the envelope $R = |h|$ are

$$p_{|h|^2}(x) = \frac{m^m x^{m-1}}{\Gamma(m)\, \Omega^m} e^{-m x / \Omega}, \qquad p_R(r) = \frac{2 m^m r^{2m-1}}{\Gamma(m)\, \Omega^m} e^{-m r^2/\Omega}, \qquad x, r \ge 0 .$$

The parameter is the inverse of the amount of fading: $m = \Omega^2 / \mathrm{Var}(|h|^2)$. The model gives only the distribution of $|h|$. For coherent detection with CSIR the phase of $h$ does not matter; a simulation that needs a phase usually takes it uniform and independent of $|h|$.

The SNR $\gamma = |h|^2 E_s / N_0$ is $\mathrm{Gamma}(m, \bar\gamma/m)$ with mean $\bar\gamma = \Omega E_s / N_0$. As for Rayleigh fading, the model also needs a time behavior (block, fast or time-correlated) and a statement of channel knowledge; the results below are for CSIR and no CSIT.

**Special cases.**

- $m = 1/2$: $|h|$ is the absolute value of a real Gaussian variable (one-sided Gaussian). This is the worst case the model allows.
- $m = 1$: Rayleigh fading.
- integer $m$: $|h|^2$ has the distribution of the sum of $m$ independent exponential powers with mean $\Omega/m$ each.
- $m \to \infty$: $|h|^2 \to \Omega$, the [AWGN channel](/additive-white-gaussian-noise-channel/).

**Status.** The Gamma law is a fit to measurements, not a result of a physical theory, except for integer $m$ in the combining case.

## What it counts

**Fade probability.** $\Pr[\gamma < x] = P(m, m x/\bar\gamma)$, where $P(a, z) = \frac{1}{\Gamma(a)} \int_0^z t^{a-1} e^{-t} dt$ is the regularized lower incomplete Gamma function. For small $x$ it is close to $\frac{(m x/\bar\gamma)^m}{\Gamma(m+1)}$.

| | $m = 1/2$ | $m = 1$ | $m = 2$ | $m = 4$ |
|---|---|---|---|---|
| $\Pr[\gamma < 0.1\bar\gamma]$ | 0.248 | 0.0952 | 0.0175 | $7.76 \cdot 10^{-4}$ |
| $\Pr[\gamma < 0.01\bar\gamma]$ | 0.0797 | 0.00995 | $1.97 \cdot 10^{-4}$ | $1.03 \cdot 10^{-7}$ |

**Error rate of BPSK** with coherent detection. The moment generating function of $\gamma$ is $M_\gamma(s) = (1 - s\bar\gamma/m)^{-m}$ for $s < m/\bar\gamma$, and Craig's form of the [Q function](/gaussian-q-function/) gives $\bar P_b = \frac{1}{\pi} \int_0^{\pi/2} (1 + \frac{\bar\gamma}{m \sin^2\phi})^{-m} d\phi$ (Goldsmith, Section 6.3.3). For integer $m$, with $\mu = \sqrt{\frac{\bar\gamma/m}{1 + \bar\gamma/m}}$,

$$\bar P_b = \left(\frac{1 - \mu}{2}\right)^m \sum_{k=0}^{m-1} \binom{m-1+k}{k} \left(\frac{1 + \mu}{2}\right)^k \approx \binom{2m-1}{m} \left(\frac{4\bar\gamma}{m}\right)^{-m} .$$

| $\bar\gamma$ | $m = 1/2$ | $m = 1$ | $m = 2$ | $m = 4$ |
|---|---|---|---|---|
| 10 dB | 0.0700 | 0.0233 | $5.53 \cdot 10^{-3}$ | $1.04 \cdot 10^{-3}$ |
| 20 dB | 0.0225 | $2.48 \cdot 10^{-3}$ | $7.26 \cdot 10^{-5}$ | $3.04 \cdot 10^{-7}$ |

At 10 dB the high-SNR form gives 0.0075 for $m = 2$ and 0.0035 for $m = 4$, so it is loose there. At 20 dB it gives $7.5 \cdot 10^{-5}$ for $m = 2$, close to the exact value. With $m = 1/2$ the error rate falls only as $\bar\gamma^{-1/2}$: 10 dB more mean SNR divides it by about 3.

**Outage.** At the rate $R = 1$ bit per channel use and $\bar\gamma = 10$ dB, the [outage probability](/outage-probability/) is $\Pr[\gamma < 1] = P(2, 0.2) = 1 - 1.2 e^{-0.2} = 0.0175$ for $m = 2$, against 0.0952 for Rayleigh.

## Relation to other models

- **Rayleigh** is $m = 1$.
- **Rician.** Matching the mean and the variance of $|h|^2$ gives $m = (K+1)^2/(2K+1)$ and back $K = u/(1-u)$ with $u = \sqrt{1 - 1/m}$, for $m \ge 1$. The match is an approximation and is poor in the deep tail: a Rician channel has a fade probability linear in $x$, and the matched Nakagami channel has one of order $x^m$. For $K = 10$ ($m = 5.76$), $\Pr[|h|^2 < 0.01\Omega]$ is $7.79 \cdot 10^{-6}$ for Rician and $1.50 \cdot 10^{-10}$ for Nakagami. See the [Rician page](/rician-fading-channel/).
- **Maximal ratio combining.** With $L$ independent Rayleigh branches of mean $\bar\gamma_0$ each, the combined SNR is $\mathrm{Gamma}(L, \bar\gamma_0)$: Nakagami with $m = L$ and $\bar\gamma = L \bar\gamma_0$. Two branches at 10 dB each give $\bar P_b = 1.60 \cdot 10^{-3}$, the $m = 2$ formula at $\bar\gamma = 20$. See [maximal ratio combining](/maximal-ratio-combining/).
- **Diversity order.** The fade probability falls as $\bar\gamma^{-m}$, so a Nakagami channel has [diversity order](/diversity-order/) $m$, which need not be an integer.

## Known results in the model

1. **The moment generating function (a closed form).** For $X \sim \mathrm{Gamma}(m, \theta)$ and $s < 1/\theta$, $\mathbb{E}[e^{sX}] = \frac{1}{\Gamma(m)\theta^m} \int_0^\infty x^{m-1} e^{-x(1/\theta - s)} dx = \frac{(1/\theta - s)^{-m}}{\theta^m} = (1 - s\theta)^{-m}$. With $\theta = \bar\gamma/m$ this is $M_\gamma$ above.
2. **Sums of exponentials (a theorem).** If $X_1, \ldots, X_L$ are independent and exponential with mean $\theta$, each has $\mathbb{E}[e^{sX_i}] = (1 - s\theta)^{-1}$, so the sum has $(1 - s\theta)^{-L}$, which is the moment generating function of $\mathrm{Gamma}(L, \theta)$. A moment generating function that is finite near 0 fixes the distribution, so the sum is $\mathrm{Gamma}(L, \theta)$.
3. **Moments of the envelope.** $\mathbb{E}[R^k] = \frac{\Gamma(m + k/2)}{\Gamma(m)} \left(\frac{\Omega}{m}\right)^{k/2}$, from the Gamma density with the substitution $x = r^2$. For $m = 2$ and $\Omega = 1$, $\mathbb{E}R = 0.940$, against 0.886 for Rayleigh.
4. **Estimating $m$.** The [method of moments](/method-of-moments/) gives $\hat m = \hat\Omega^2 / \widehat{\mathrm{Var}}(R^2)$ from samples of the power. A value below $1/2$ means that the data do not fit the model.
5. **The high-SNR error rate.** For small $x$, the Gamma CDF is $\frac{(mx/\bar\gamma)^m}{\Gamma(m+1)}(1 + O(x))$, so $\Pr[\gamma < 1]$ and the error rates fall as $\bar\gamma^{-m}$. This is the reason that $m$ acts as a diversity order.

### Pitfalls

- **Matching moments is not matching tails.** Two channels with the same $\Omega$ and the same variance of $|h|^2$ can differ by orders of magnitude in outage at low rates (the Rician comparison above).
- **The range of $m$.** The density is defined for $m > 0$, but Nakagami's model and most closed forms require $m \ge 1/2$. Some results, such as the sum formula for BPSK, need an integer $m$.
- **The Gamma parameters.** Some libraries use the rate $m/\Omega$ instead of the scale $\Omega/m$. Python's `random.gammavariate(alpha, beta)` takes the shape and the scale, so $|h|^2$ is `gammavariate(m, Omega / m)`.
- **No phase model.** The Nakagami law says nothing about the phase or about the correlation in time. A simulator must add both.

## References
