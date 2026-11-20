---
tag: 1VXDWM
kind: definition
slug: symbol-error-rate
name: Symbol error rate
aliases:
- SER
- symbol error probability
area: communications/modulation-and-detection
level: intro
summary: The probability that the detector decides a different symbol than the one sent, as a function of the SNR per symbol.
prereqs: [symbol-detection, gaussian-q-function, signal-constellation]
see_also: [bit-error-rate, minimum-distance-detector, union-bound, energy-per-bit-to-noise-density-ratio, gray-labeling, rayleigh-fading-channel, importance-sampling, monte-carlo-integration]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 4.2-3 (a union bound on the probability of error of ML detection) and Sections 4.3-1 to 4.3-3 (the error probabilities of PAM, PSK and QAM)
  - paper: doi:10.1109/MILCOM.1991.258319
    title: John W. Craig, A new, simple and exact result for calculating the probability of error for two-dimensional signal constellations, MILCOM 91 Conference Record, 1991
    locator: pp. 571-575 (exact error probabilities of two-dimensional constellations as integrals over a finite range of angles)
  - book: isbn:9780471649533
    title: Marvin K. Simon and Mohamed-Slim Alouini, Digital Communication over Fading Channels, second edition, Wiley, 2005
    locator: Chapter 4, Alternative Representations of Classical Functions (the integral forms used for error probabilities in AWGN and in fading)
---

The symbol error rate (SER) is the probability that the detector's decision is a different constellation point from the one that was sent. It measures how well a modulation scheme and its detector work at a given signal strength, and it is the quantity that [symbol detection](/symbol-detection/) minimizes. The [bit error rate](/bit-error-rate/) counts wrong bits instead of wrong symbols; the two are linked by the labeling, and with a [Gray labeling](/gray-labeling/) the bit error rate is close to the SER divided by the number of bits per symbol. The formulas on this page are written in terms of $E_s/N_0$, the SNR per symbol.

## Definition

Let $\mathcal{A} = \{a_0, \ldots, a_{M-1}\}$ be a constellation with priors $\pi_i$, sent over a channel, and let $d$ be a decision rule. The **symbol error rate** of $d$ is

$$\mathrm{SER} = \Pr[\hat\imath \ne i] = \sum_i \pi_i \Pr[d(y) \ne i \mid x = a_i].$$

Unless a page says otherwise, the detector is the optimal one for equal priors, which in AWGN is the [minimum distance detector](/minimum-distance-detector/), and the SER is given as a function of $E_s/N_0$. The **measured** SER of a link or a simulation is the fraction $k/n$ of wrong decisions among $n$ symbols; it estimates the probability.

**Closed forms in AWGN.** These hold under these assumptions: complex AWGN $\mathcal{CN}(0, N_0)$, equal priors, a known gain and phase, minimum distance detection, and $\gamma_s = E_s/N_0$. Here $Q$ is the [Gaussian Q-function](/gaussian-q-function/).

| Scheme | SER |
|---|---|
| BPSK | $Q(\sqrt{2\gamma_s})$ |
| QPSK (4-QAM) | $2Q(\sqrt{\gamma_s}) - Q(\sqrt{\gamma_s})^2$ |
| $M$-PAM | $2(1 - 1/M)\, Q\big(\sqrt{6\gamma_s/(M^2-1)}\big)$ |
| square $M$-QAM | $2p - p^2$ with $p = 2(1 - 1/\sqrt{M})\, Q\big(\sqrt{3\gamma_s/(M-1)}\big)$ |
| $M$-PSK, exact | $\frac{1}{\pi}\int_0^{(M-1)\pi/M} \exp\!\big(-\gamma_s \sin^2(\pi/M)/\sin^2\theta\big)\, d\theta$ |
| $M$-PSK, $M \ge 4$, approximate | $2Q\big(\sqrt{2\gamma_s}\,\sin(\pi/M)\big)$ |

The derivations are on the pages for [PAM](/pulse-amplitude-modulation/), [QAM](/quadrature-amplitude-modulation/) and [PSK](/phase-shift-keying/). The PSK integral is Craig's form (Craig 1991).

**Bounds for any constellation.** Write $d_{ik} = |a_i - a_k|$, and assume equal priors and the ML detector in $\mathcal{CN}(0, N_0 I)$ noise.

- *Union bound* (a theorem): $\mathrm{SER} \le \frac{1}{M}\sum_i \sum_{k \ne i} Q\big(d_{ik}/\sqrt{2N_0}\big)$, from the [union bound](/union-bound/) over the pairwise error events.
- *Lower bound* (a theorem): $\mathrm{SER} \ge \frac{1}{M}\sum_i Q\big(d_i/\sqrt{2N_0}\big)$, where $d_i$ is the distance from $a_i$ to its nearest neighbor.
- *Nearest neighbor approximation* (a heuristic that is accurate at high SNR): $\mathrm{SER} \approx \bar N_{\min}\, Q\big(d_{\min}/\sqrt{2N_0}\big)$.

The proofs are on the [symbol detection](/symbol-detection/) page. At high SNR the SER falls like $\exp(-d_{\min}^2/(4N_0))$, so the normalized minimum distance $d_{\min}^2/E_s$ sets the slope of the SER curve, and $\bar N_{\min}$ shifts it a little.

**Estimating the SER by simulation.** Simulating $n$ symbols with $k$ errors gives the estimate $k/n$. A confidence interval for the true value is the Wilson score interval

$$\frac{k + z^2/2 \pm z\sqrt{k(n-k)/n + z^2/4}}{n + z^2},$$

with $z = 3.29$ for a two-sided level of 99.9%. The relative width of the interval is about $2z/\sqrt{k}$, so the number of errors, not the number of symbols, sets the accuracy; about 100 errors give an interval of roughly $\pm 33\%$, and $n$ must be about $100/\mathrm{SER}$. For very small SER, [importance sampling](/importance-sampling/) lowers the number of samples.

## Examples and non-examples

**QPSK at $E_s/N_0 = 10$ dB.** The exact SER is $1.5648 \times 10^{-3}$. The union bound gives $2Q(\sqrt{10}) + Q(\sqrt{20}) = 1.5693 \times 10^{-3}$, the nearest neighbor approximation $2Q(\sqrt{10}) = 1.5654 \times 10^{-3}$, and the lower bound $Q(\sqrt{10}) = 7.827 \times 10^{-4}$.

**16-QAM at $E_s/N_0 = 15$ dB.** The exact SER is $0.017782$, the nearest neighbor approximation $3Q(\sqrt{0.4 \cdot 10^{1.5}/2}) = 0.017862$, and the union bound $0.018285$. A simulation of $n = 20000$ symbols with the seed 5 in the tests of the [minimum distance detector](/minimum-distance-detector/) gives 358 errors, the estimate $0.0179$, and the Wilson interval $[0.01507, 0.02126]$ with $z = 3.29$, which contains the exact value.

**More values.**

| $E_s/N_0$ | 4-PAM | 8-PSK | 16-QAM | 16-PSK | 64-QAM |
|---|---|---|---|---|---|
| 10 dB | 0.03413 | 0.08700 | 0.22203 | 0.38295 | 0.6738 |
| 15 dB | $2.818 \times 10^{-4}$ | $2.3395 \times 10^{-3}$ | 0.017782 | 0.12078 | 0.34762 |
| 20 dB | $1.905 \times 10^{-10}$ | $6.234 \times 10^{-8}$ | $1.1616 \times 10^{-5}$ | $5.7980 \times 10^{-3}$ | 0.050270 |

**Non-example: SER on a fading channel.** On a [Rayleigh fading channel](/rayleigh-fading-channel/) the gain changes from symbol to symbol, and the SER is the average of the AWGN formula over the distribution of the gain. For BPSK with average $E_s/N_0 = 10$ dB, the average is $\tfrac{1}{2}\big(1 - \sqrt{10/11}\big) = 0.02327$, while the AWGN value at 10 dB is $3.87 \times 10^{-6}$. The table above does not apply there.

**Non-example: the bit error rate.** One symbol error in 16-QAM may change one bit or up to four. The SER counts it once; the [bit error rate](/bit-error-rate/) counts the wrong bits.

## Related definitions

- **Bit error rate.** $\mathrm{SER}/\log_2 M \le P_b \le \mathrm{SER}$ for any labeling, and $P_b \approx \mathrm{SER}/\log_2 M$ for a Gray labeling at high SNR; see [bit error rate](/bit-error-rate/) and [Gray labeling](/gray-labeling/).
- **SNR per bit.** To compare schemes with different $M$, the SER is often plotted against $E_b/N_0 = E_s/(N_0 \log_2 M)$; see [energy per bit to noise density ratio](/energy-per-bit-to-noise-density-ratio/).
- **Frame and block error rates.** With a channel code, a frame is in error if any of its decoded bits is wrong; the frame error rate is the usual measure of coded links.
- **Monte Carlo estimation.** A simulated SER is a [Monte Carlo](/monte-carlo-integration/) estimate of an integral over the noise.

## References
