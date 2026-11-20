---
tag: M5567E
kind: model
slug: rician-fading-channel
name: Rician fading channel
aliases:
- Rician fading
- Rice fading
area: communications/fading-channels
level: core
summary: "The flat fading channel whose gain is a fixed line-of-sight part plus circular Gaussian scatter, with K the power ratio of the two: K = 0 is Rayleigh, large K is nearly AWGN."
prereqs: [rayleigh-fading-channel, moment-generating-function]
see_also: [rayleigh-fading-channel, nakagami-m-fading-channel, outage-probability, multipath-fading, method-of-moments, moment-generating-function, bit-error-rate, diversity-order]
sources:
  - paper: doi:10.1002/j.1538-7305.1945.tb00453.x
    title: S. O. Rice, Mathematical analysis of random noise, Bell System Technical Journal 24(1), 1945
    locator: pp. 46 to 156 (the continuation of the 1944 paper; it includes the statistics of a sine wave plus Gaussian noise, whose envelope has the Rice distribution)
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Section 2.4.2 (Rayleigh and Rician fading)
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 3.2.2 (envelope and power distributions) and Section 6.3.3 (the moment generating function approach to the average error probability)
  - book: isbn:9780130422323
    title: Theodore S. Rappaport, Wireless Communications, Principles and Practice, second edition, Prentice Hall, 2002
    locator: Section 5.6.2 (the Ricean fading distribution)
  - paper: doi:10.1109/4234.769521
    title: L. J. Greenstein, D. G. Michelson and V. Erceg, Moment-method estimation of the Ricean K-factor, IEEE Communications Letters 3(6), 1999
    locator: pp. 175 to 176 (the estimate of K from the mean and the variance of the received power)
---

The Rician fading channel is the flat fading channel $y = h x + w$ in which the gain $h$ is a fixed line-of-sight part plus a circular Gaussian scattered part. The ratio of the power of the fixed part to the power of the scattered part is the Rician factor $K$. With $K = 0$ the model is the [Rayleigh fading channel](/rayleigh-fading-channel/), and as $K$ grows it tends to the [AWGN channel](/additive-white-gaussian-noise-channel/). The envelope $|h|$ has the Rice distribution, which Rice derived for a sine wave plus Gaussian noise.

## The machine

One symbol $x$ with energy $E_s$ is sent per channel use, and

$$y = h x + w, \qquad h = \sqrt{\frac{K \Omega}{K+1}}\, e^{j\theta} + \sqrt{\frac{\Omega}{K+1}}\, g, \qquad g \sim \mathcal{CN}(0, 1), \quad w \sim \mathcal{CN}(0, N_0).$$

The parameters are the mean power $\Omega = \mathbb{E}|h|^2$, the factor $K \ge 0$ and the phase $\theta$ of the line-of-sight part. $g$ and $w$ are independent. The line-of-sight part has power $K\Omega/(K+1)$ and the scattered part has power $\Omega/(K+1)$. The envelope $R = |h|$ has the Rice density

$$p(r) = \frac{2 (K+1) r}{\Omega} \exp\left(-K - \frac{(K+1) r^2}{\Omega}\right) I_0\left(2 r \sqrt{\frac{K (K+1)}{\Omega}}\right), \qquad r \ge 0,$$

where $I_0$ is the modified Bessel function of the first kind and order 0. The density does not depend on $\theta$. As before, $\gamma = |h|^2 E_s / N_0$ and $\bar\gamma = \Omega E_s / N_0$.

The same choices as for Rayleigh fading complete the model: block, fast or time-correlated variation of the scattered part $g$, and CSIR for coherent detection, with no CSIT. In a time-correlated model, the line-of-sight part also turns at its own Doppler shift when the receiver moves.

**Where $K$ comes from.** $K$ is a fitted parameter. It is large when a clear direct path exists, for example near the transmitter or in a fixed link, and it falls toward 0 when obstacles block the direct path.

## What it counts

The model predicts the distribution of $\gamma$ and so the fade probabilities, the error rates and the outage. With $\Omega = 1$:

| | $\Pr[\lvert h\rvert^2 < 0.1]$ | $\Pr[\lvert h\rvert^2 < 0.01]$ |
|---|---|---|
| $K = 0$ (Rayleigh) | 0.0952 | 0.00995 |
| $K = 1$ | 0.0733 | 0.00736 |
| $K = 10$ | $7.39 \cdot 10^{-4}$ | $7.79 \cdot 10^{-6}$ |

**Error rate of BPSK** with coherent detection. The moment generating function of $\gamma$ is

$$M_\gamma(s) = \mathbb{E}[e^{s\gamma}] = \frac{1 + K}{1 + K - s\bar\gamma} \exp\left(\frac{K s \bar\gamma}{1 + K - s\bar\gamma}\right), \qquad s < \frac{1+K}{\bar\gamma},$$

and Craig's form $Q(x) = \frac{1}{\pi} \int_0^{\pi/2} \exp\left(-\frac{x^2}{2 \sin^2\phi}\right) d\phi$ for $x \ge 0$ turns the average of $Q(\sqrt{2\gamma})$ into one finite integral (Goldsmith, Section 6.3.3):

$$\bar P_b = \frac{1}{\pi} \int_0^{\pi/2} M_\gamma\left(-\frac{1}{\sin^2\phi}\right) d\phi .$$

| $\bar\gamma$ | $K = 0$ | $K = 1$ | $K = 10$ |
|---|---|---|---|
| 10 dB | 0.0233 | 0.0182 | $7.01 \cdot 10^{-4}$ |
| 20 dB | $2.48 \cdot 10^{-3}$ | $1.84 \cdot 10^{-3}$ | $2.51 \cdot 10^{-6}$ |

A strong direct path gains a lot. At 20 dB, $K = 10$ gives an error rate about 1000 times lower than Rayleigh.

## Relation to other models

- **Rayleigh** is the case $K = 0$.
- **AWGN** is the limit $K \to \infty$ with $\Omega$ fixed: the scattered part vanishes and $|h|^2 = \Omega$.
- **Nakagami.** The [Nakagami-m channel](/nakagami-m-fading-channel/) with $m = (K+1)^2/(2K+1)$ has the same mean and variance of $|h|^2$. This match is only an approximation and is poor in the deep tail; see item 4 below.
- **Diversity.** For any finite $K$ the fade probability is linear in $x$ for small $x$, so the [diversity order](/diversity-order/) of one Rician branch is still 1. A large $K$ moves the curve down but does not change the final slope.
- **Physical origin.** In [multipath fading](/multipath-fading/) with one dominant path and many weak scattered paths, the central limit theorem applies to the scattered part only.

## Known results in the model

1. **Mean and variance of the power (a closed form).** Write $h = \mu + \sigma g$ with $|\mu|^2 = K\Omega/(K+1)$ and $\sigma^2 = \Omega/(K+1)$. Then $\mathbb{E}|h|^2 = |\mu|^2 + \sigma^2 = \Omega$ and $\mathrm{Var}(|h|^2) = \sigma^4 + 2 |\mu|^2 \sigma^2 = \Omega^2 \frac{2K+1}{(K+1)^2}$. The ratio $\mathrm{Var}(|h|^2)/\Omega^2 = (2K+1)/(K+1)^2$ is the *amount of fading*: 1 for Rayleigh, 0.174 for $K = 10$, and 0 without fading.
2. **The moment generating function (a closed form).** Let $u = \mathrm{Re}(\mu + \sigma g)$, a real Gaussian with mean $a$ and variance $\sigma^2/2$. For $s < 1/\sigma^2$, completing the square gives $\mathbb{E}[e^{s u^2}] = (1 - s\sigma^2)^{-1/2} \exp\left(\frac{s a^2}{1 - s\sigma^2}\right)$. The real and imaginary parts are independent, so $\mathbb{E}[e^{s|h|^2}] = (1 - s\sigma^2)^{-1} \exp\left(\frac{s |\mu|^2}{1 - s\sigma^2}\right)$. Scale by $E_s/N_0$ to get $M_\gamma$ above. With $K = 0$ it is $1/(1 - s\bar\gamma)$, the Rayleigh case.
3. **Estimating $K$ from moments.** Let $G = \mathrm{Var}(R^2)/(\mathbb{E}R^2)^2$, measured from samples of the received power. Put $u = K/(K+1)$. By item 1, $1 - G = 1 - \frac{2K+1}{(K+1)^2} = \frac{K^2}{(K+1)^2} = u^2$, so $u = \sqrt{1 - G}$ and
   $$\hat K = \frac{\sqrt{1 - G}}{1 - \sqrt{1 - G}} .$$
   This is the [method of moments](/method-of-moments/) estimate of Greenstein, Michelson and Erceg 1999. Example: $K = 3$ gives $G = 7/16 = 0.4375$, and the formula returns 3.
4. **The tail, and the Nakagami match.** For small $x$, $\Pr[|h|^2 < x \Omega] \approx (1+K) e^{-K} x$, because the density of $|h|^2/\Omega$ at 0 is $(1+K)e^{-K}$. For $K = 10$ the matched Nakagami parameter is $m = 121/21 = 5.76$, and the Nakagami tail falls as $x^{5.76}$. At $x = 0.1$ the Rician value is $7.39 \cdot 10^{-4}$ and the Nakagami value is $5.55 \cdot 10^{-5}$; at $x = 0.01$ they are $7.79 \cdot 10^{-6}$ and $1.50 \cdot 10^{-10}$. Outage and high-SNR error rates need the true Rician tail.
5. **Construction for simulation.** For $K = 10$ and $\Omega = 1$, the line-of-sight amplitude is $\sqrt{10/11} = 0.953$ and the scattered part has variance $1/11$. Draw $g$ with two independent Gaussians of variance $1/2$ each.

### Pitfalls

- **Two definitions of $K$.** $K$ is a power ratio. Some texts give it in dB, and some write the Rice density with the line-of-sight amplitude $s$ and the scatter variance $\sigma^2$ per real dimension, so that $K = s^2/(2\sigma^2)$. Check which one a table uses.
- **Fixed $\Omega$.** Comparing $K$ values at a fixed $\bar\gamma$ moves power from the scatter to the direct path. Comparing at a fixed scattered power changes $\bar\gamma$ too.
- **Moment fits in the tail.** A Nakagami fit with the same two moments gives tail probabilities that are orders of magnitude too small at large $K$ (item 4).
- **The estimate of $K$.** $\hat K$ from item 3 needs many independent samples. With few samples, $G$ is noisy: a sample value $G > 1$ has no real estimate (set $\hat K = 0$), and a small $G$ gives a very large $\hat K$.

## References
