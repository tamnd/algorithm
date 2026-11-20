---
tag: YCPTMX
kind: model
slug: rayleigh-fading-channel
name: Rayleigh fading channel
aliases:
- Rayleigh fading
area: communications/fading-channels
level: intro
summary: "The flat fading channel y = hx + w with h circular complex Gaussian: the envelope is Rayleigh, the power is exponential, and BPSK errors fall only as 1/(4 mean SNR)."
prereqs: [multipath-fading, gaussian-q-function]
see_also: [rician-fading-channel, nakagami-m-fading-channel, outage-probability, clarke-model, maximal-ratio-combining, diversity-order, ergodic-capacity, bit-error-rate]
sources:
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Section 2.4.2 (Rayleigh and Rician fading), Section 3.1.2 (coherent detection in a Rayleigh fading channel) and Section 5.4.5 (capacity of the fast fading channel)
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 3.2.2 (envelope and power distributions) and Section 6.3.2 (average probability of error in fading)
  - book: isbn:9780130422323
    title: Theodore S. Rappaport, Wireless Communications, Principles and Practice, second edition, Prentice Hall, 2002
    locator: Section 5.6.1 (the Rayleigh fading distribution)
  - paper: doi:10.1002/j.1538-7305.1968.tb00069.x
    title: R. H. Clarke, A statistical theory of mobile-radio reception, Bell System Technical Journal 47(6), 1968
    locator: pp. 957 to 1000 (the Gaussian field and the Rayleigh envelope at a moving receiver in a field of scattered waves)
---

The Rayleigh fading channel is the flat fading channel $y = h x + w$ in which the gain $h$ is a circularly symmetric complex Gaussian variable. It models [multipath fading](/multipath-fading/) with many scattered paths and no dominant one. The envelope $|h|$ then has the Rayleigh distribution, and the power $|h|^2$ is exponential, so deep fades are common. It is the base case for the analysis of fading, diversity and the capacity of wireless links.

## The machine

One complex symbol $x$ with energy $E_s = \mathbb{E}|x|^2$ is sent per channel use, and the receiver gets

$$y = h x + w, \qquad h \sim \mathcal{CN}(0, \Omega), \qquad w \sim \mathcal{CN}(0, N_0),$$

with $h$ and $w$ independent. Write $h = h_I + j h_Q$ with $h_I$ and $h_Q$ independent and $\mathcal{N}(0, \Omega/2)$. Then:

- the envelope $R = |h|$ has the Rayleigh density $p(r) = \frac{2r}{\Omega} e^{-r^2/\Omega}$ for $r \ge 0$;
- the power $|h|^2$ is exponential with mean $\Omega$;
- the phase $\arg h$ is uniform on $[0, 2\pi)$ and independent of $|h|$.

The instantaneous SNR is $\gamma = |h|^2 E_s / N_0$ and the mean SNR is $\bar\gamma = \Omega E_s / N_0$. The density of $\gamma$ is $p(\gamma) = \frac{1}{\bar\gamma} e^{-\gamma/\bar\gamma}$ for $\gamma \ge 0$.

The model needs two more choices:

- **Time behavior.** In *block fading*, $h$ stays constant over a block and is independent from block to block. In *fast fading*, a new independent $h$ is drawn for each symbol. In *time-correlated fading*, $h(t)$ is a Gaussian process; with scatterers in all directions around a mobile, Clarke's model gives the autocorrelation $\Omega J_0(2 \pi f_D \tau)$, where $f_D$ is the largest Doppler shift (see the [Clarke model](/clarke-model/)).
- **Channel knowledge.** Coherent detection assumes CSIR: the receiver knows $h$, for example from [channel estimation](/channel-estimation/). The transmitter does not know $h$ (no CSIT) unless the page says so.

**Why Gaussian.** The gain is a sum of many paths with independent, uniform phases. By the [central limit theorem](/central-limit-theorem/) the sum is close to circular Gaussian. This is an approximation; measurements fit it well in dense scattering without a line-of-sight path (Rappaport, Section 5.6.1).

## What it counts

The model predicts the distribution of the received SNR, and from it the error rates, the outage and the capacity that a link sees on average over the fades.

**Fade probability.** $\Pr[\gamma < x] = 1 - e^{-x/\bar\gamma}$. The power is 10 dB or more below its mean with probability $1 - e^{-0.1} = 0.0952$, and 20 dB or more below with probability $0.00995$. For small $x$ the probability is close to $x / \bar\gamma$: each 10 dB of extra margin divides it by only 10.

**Error rate of BPSK** with coherent detection and CSIR:

$$\bar P_b = \tfrac12 \left(1 - \sqrt{\frac{\bar\gamma}{1 + \bar\gamma}}\right) \approx \frac{1}{4 \bar\gamma} \quad \text{for large } \bar\gamma .$$

| $\bar\gamma$ | 0 dB | 10 dB | 20 dB | 30 dB | 40 dB |
|---|---|---|---|---|---|
| Rayleigh $\bar P_b$ | 0.146 | 0.0233 | $2.48 \cdot 10^{-3}$ | $2.50 \cdot 10^{-4}$ | $2.50 \cdot 10^{-5}$ |
| $1/(4\bar\gamma)$ | 0.25 | 0.025 | $2.5 \cdot 10^{-3}$ | $2.5 \cdot 10^{-4}$ | $2.5 \cdot 10^{-5}$ |

The [AWGN channel](/additive-white-gaussian-noise-channel/) at 10 dB gives $Q(\sqrt{20}) = 3.87 \cdot 10^{-6}$. To reach $\bar P_b = 10^{-3}$ the Rayleigh channel needs 23.97 dB against 6.79 dB without fading; for $10^{-5}$ it needs 43.98 dB against 9.59 dB.

**Ergodic capacity** with CSIR and fast fading, in bit per channel use:

$$C = \mathbb{E}[\log_2(1 + \gamma)] = \log_2(e)\, e^{1/\bar\gamma} E_1(1/\bar\gamma),$$

where $E_1(z) = \int_z^\infty e^{-t}/t\, dt$. It is 0.860 at 0 dB, 2.907 at 10 dB and 5.884 at 20 dB, against 1, 3.459 and 6.658 for AWGN at the same SNR.

**Outage.** For a fixed rate $R$ in block fading, the [outage probability](/outage-probability/) is $\Pr[\log_2(1 + \gamma) < R] = 1 - e^{-(2^R - 1)/\bar\gamma}$: 0.0952 for $R = 1$ at 10 dB.

## Relation to other models

- **AWGN.** With $h$ fixed and known, the channel is the [AWGN channel](/additive-white-gaussian-noise-channel/) with SNR $\gamma$. Rayleigh fading averages AWGN results over an exponential $\gamma$.
- **Rician.** The [Rician fading channel](/rician-fading-channel/) adds a fixed line-of-sight part to $h$. Rician with $K = 0$ is Rayleigh.
- **Nakagami.** The [Nakagami-m channel](/nakagami-m-fading-channel/) with $m = 1$ is Rayleigh. Smaller $m$ is worse, larger $m$ is better.
- **Diversity.** The sum of $L$ independent exponential powers, as in [maximal ratio combining](/maximal-ratio-combining/), has a Gamma distribution, which is Nakagami with $m = L$.
- **Frequency-selective.** Each tap of a [tapped delay line model](/tapped-delay-line-channel-model/) is often an independent Rayleigh gain, and each subcarrier of [OFDM](/orthogonal-frequency-division-multiplexing/) then sees Rayleigh fading.
- **Composite.** With [log-normal shadowing](/log-normal-shadowing/) on $\Omega$ the model becomes a composite of shadowing and fading.
- **Bursts.** A two-state approximation of a Rayleigh channel with errors in the fades is the [Gilbert-Elliott channel](/gilbert-elliott-channel/).

## Known results in the model

1. **The Rayleigh envelope (a theorem).** $h_I$ and $h_Q$ have the joint density $\frac{1}{\pi \Omega} e^{-(x^2 + y^2)/\Omega}$. In polar coordinates $x = r \cos\theta$, $y = r \sin\theta$ with Jacobian $r$, the joint density is $\frac{r}{\pi \Omega} e^{-r^2/\Omega}$. It does not depend on $\theta$, so $\theta$ is uniform and independent of $r$, and integrating over $\theta$ gives $\frac{2r}{\Omega} e^{-r^2/\Omega}$. The substitution $u = r^2$ gives the exponential density of $|h|^2$. Moments: $\mathbb{E}|h| = \frac{\sqrt{\pi \Omega}}{2} = 0.886 \sqrt{\Omega}$, $\mathbb{E}|h|^2 = \Omega$, and the median of $|h|^2$ is $\Omega \ln 2$, which is 1.59 dB below the mean.
2. **The BPSK error rate (a closed form under CSIR and coherent detection).** Given $\gamma$, the error probability is $Q(\sqrt{2\gamma})$, so $\bar P_b = \int_0^\infty Q(\sqrt{2g}) \frac{1}{\bar\gamma} e^{-g/\bar\gamma} dg$. Integrate by parts with $\frac{d}{dg} Q(\sqrt{2g}) = -\frac{e^{-g}}{2 \sqrt{\pi g}}$:
   $$\bar P_b = \tfrac12 - \frac{1}{2\sqrt{\pi}} \int_0^\infty g^{-1/2} e^{-g (1 + 1/\bar\gamma)} dg = \tfrac12 - \frac{1}{2\sqrt{\pi}} \cdot \frac{\sqrt{\pi}}{\sqrt{1 + 1/\bar\gamma}},$$
   which is the formula above. For large $\bar\gamma$, $\sqrt{\bar\gamma/(1+\bar\gamma)} \approx 1 - \frac{1}{2\bar\gamma}$, so $\bar P_b \approx \frac{1}{4\bar\gamma}$. The error rate falls as $\bar\gamma^{-1}$: the [diversity order](/diversity-order/) is 1.
3. **Errors come from fades.** At high SNR, an error is likely only when $\gamma$ is below about 1, and $\Pr[\gamma < 1] \approx 1/\bar\gamma$. That event, not the Gaussian tail of the noise, sets the slope (Tse and Viswanath, Section 3.1.2).
4. **Diversity.** With $L$ independent branches of mean SNR $\bar\gamma$ each and maximal ratio combining, $\bar P_b \approx \binom{2L-1}{L} (4\bar\gamma)^{-L}$ at high SNR. Two branches at 10 dB each give $\bar P_b = 1.60 \cdot 10^{-3}$, against 0.0233 for one branch.
5. **Ergodic capacity (a closed form under CSIR).** For $X$ exponential with mean 1, integration by parts gives $\mathbb{E}[\ln(1 + \bar\gamma X)] = \int_0^\infty \frac{e^{-x}}{x + 1/\bar\gamma} dx = e^{1/\bar\gamma} E_1(1/\bar\gamma)$. By [Jensen's inequality](/jensens-inequality/), $C \le \log_2(1 + \bar\gamma)$: with CSIR only, fading always lowers the ergodic capacity at the same mean SNR. At high SNR the loss tends to $\gamma_E \log_2 e = 0.83$ bit, where $\gamma_E = 0.5772$ is the Euler constant.

### Pitfalls

- **Mean SNR and SNR.** Every formula uses the mean $\bar\gamma$. Results quoted against the instantaneous $\gamma$ are AWGN results.
- **Envelope and power.** $\Omega$ is the mean of $|h|^2$, not of $|h|$. Some texts write the Rayleigh density with $\sigma^2 = \Omega/2$, the variance of each real part.
- **Independent samples.** Drawing a new $h$ per symbol models ideal interleaving. A slow channel stays in a fade for many symbols, and the code then sees bursts of errors.
- **No line of sight.** With a strong direct path the fades are far less deep. A Rayleigh model then overstates the error rate; use the [Rician](/rician-fading-channel/) model.

## References
