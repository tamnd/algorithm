---
tag: XYTR6D
kind: algorithm
slug: cyclostationary-feature-detection
name: Cyclostationary feature detection
aliases:
- cyclic spectrum detection
area: communications/link-adaptation-and-resource-allocation
level: advanced
summary: Detects a modulated signal from peaks of its spectral correlation at cyclic frequencies, which noise does not have.
solves: [spectrum-sensing]
model: real-ram
complexity:
  vars: {N: the number of samples}
  time: {worst: O(N), scan: O(N log N)}
  space: {extra: O(1), scan: O(N)}
properties: {deterministic: true, needs_noise_power: false, needs_cycle_frequency: true, asymptotic_false_alarm_rate: true}
history:
  year: 1988
  people: [William A. Gardner]
  note: "Gardner set out feature detection by the spectral correlation of cyclostationary signals as a framework for signal interception. Dandawate and Giannakis (1994) gave asymptotic chi-square tests for the presence of cyclostationarity."
prereqs: [autocorrelation, discrete-fourier-transform, energy-detector]
see_also: [spectrum-sensing, energy-detector, autocorrelation, power-spectral-density, phase-shift-keying, cyclic-prefix, carrier-recovery, fast-fourier-transform]
sources:
  - paper: doi:10.1109/26.3769
    title: "William A. Gardner, Signal interception: a unifying theoretical framework for feature detection, IEEE Transactions on Communications 36(8), 1988, pages 897 to 906"
    locator: "the cyclic autocorrelation and the spectral correlation density, and detectors that measure them at the cycle frequencies of the signal"
  - paper: doi:10.1109/79.81007
    title: "William A. Gardner, Exploitation of spectral redundancy in cyclostationary signals, IEEE Signal Processing Magazine 8(2), 1991, pages 14 to 36"
    locator: "the cycle frequencies of common modulations, among them the conjugate feature at twice the carrier of BPSK, and the tolerance of feature detectors to noise and interference"
  - paper: doi:10.1109/78.317857
    title: "Amod V. Dandawate and Georgios B. Giannakis, Statistical tests for presence of cyclostationarity, IEEE Transactions on Signal Processing 42(9), 1994, pages 2355 to 2369"
    locator: "the estimate of the cyclic correlation, its asymptotic normal law, and the chi-square test for a nonzero cyclic correlation at a given cycle frequency"
---

Cyclostationary feature detection decides whether a band holds a modulated signal by looking for a correlation that only the signal has. A modulated signal repeats its statistics with the carrier, the symbol rate or the block length: its cyclic autocorrelation $R^\alpha(\tau)$ is not zero at certain cycle frequencies $\alpha$, while for stationary noise it is zero at every $\alpha \ne 0$. The detector estimates $R^\alpha(\tau)$ from $N$ samples at a cycle frequency of the signal it looks for, normalizes it by the measured power, and compares the result with a threshold. The statistic does not change when the samples are scaled, so the test needs no noise power, and an error in the noise power does not give it the SNR wall of the [energy detector](/energy-detector/). It also tells signals apart: a BPSK signal has a feature at twice its carrier that QPSK and noise lack. The price is that the cycle frequency must be known or searched, and with exact noise power it needs about $1.6$ to $2.1$ times the samples of the energy detector.

## In plain words

Noise has no pattern in time. A radio signal has one: its symbols come at a fixed rate on a fixed carrier, so some products of its samples keep the same phase from sample to sample. The detector multiplies the samples in the way that brings out this pattern, turns them back by the expected phase step, and adds them up. For noise, the terms point in random directions and the sum stays small. For the signal, the terms line up and the sum grows. The detector divides by the measured power, so a louder or quieter receiver gives the same answer. It must know, or search for, the rate of the pattern it looks for.

## The problem

The receiver has $N$ complex baseband samples $y[0], \ldots, y[N-1]$. Under $H_0$, they are white circular complex Gaussian noise of unknown power $\sigma^2$. Under $H_1$, they hold a signal plus that noise, and the signal is cyclostationary: for a known cycle frequency $\alpha \ne 0$ and lag $\tau$, its conjugate cyclic autocorrelation
$$R^\alpha(\tau) = \lim_{M \to \infty} \frac{1}{M}\sum_{n < M} \mathbb E\big[y[n + \tau]\, y[n]\big] e^{-j 2\pi \alpha n}$$
is not zero. The non-conjugate form uses $y[n]^*$ in place of $y[n]$. For a target false alarm rate $P_{fa}$, decide between $H_0$ and $H_1$ without knowing $\sigma^2$.

## The algorithm

```pseudo id=main
CYCLIC-FEATURE-DETECT(y[0..N-1], α, τ, P_fa)
L1  λ ← -ln P_fa
L2  R ← 0; M ← N - τ
L3  for n ← 0 to M - 1 do R ← R + y[n + τ] y[n] e^{-j2παn}
L4  P ← (1/N) Σ_n |y[n]|²
L5  R ← R / M
L6  T ← M |R|² / (c P²), with c = 2 if τ = 0 and c = 1 otherwise
L7  if T > λ then return "signal present"
L8  return "noise only"
```

For the non-conjugate form, line L3 uses $y[n]^*$ and needs $\tau \ge 1$, and $c = 1$. When the carrier, and so $\alpha$, is unknown, compute $R$ at all $\alpha = k/M$ by one DFT of the products $y[n + \tau]\,y[n]$ and compare the largest $T$ with $\lambda = -\ln\big(1 - (1 - P_{fa})^{1/M}\big)$, the threshold on the largest of $M$ independent unit exponentials.

**Cycle frequencies of common signals.** A BPSK signal $\sqrt S\, a[n] e^{j(2\pi f_c n + \phi)}$ with $a[n] = \pm 1$ has $y[n]^2 = S e^{j2\phi} e^{j 2\pi (2 f_c) n}$ without noise, so the conjugate feature at $\tau = 0$ is at $\alpha = 2 f_c$ with $|R| = S$. This is the same line at twice the carrier that a squaring loop for [carrier recovery](/carrier-recovery/) uses. QPSK has no conjugate feature at $\tau = 0$, because the square of a QPSK symbol is $\pm j$ with mean zero. An OFDM signal with a [cyclic prefix](/cyclic-prefix/) of $D$ samples on blocks of $L$ has a non-conjugate feature at lag $\tau = L$ and cycle frequencies $k/(L + D)$, because each prefix sample repeats a sample $L$ positions later.

## Example

**Without noise.** Take eight BPSK samples $y[n] = a[n] e^{j\pi n/4}$, with carrier $f_c = 1/8$ and symbols $a = (-1, 1, 1, -1, 1, 1, -1, 1)$. At $\alpha = 2f_c = 1/4$ and $\tau = 0$, each term of line L3 is $a[n]^2 e^{j\pi n/2} e^{-j\pi n/2} = 1$, so $R = 1$, $P = 1$ and $T = 8 \cdot 1/(2 \cdot 1) = 4$. For $P_{fa} = 0.05$, $\lambda = -\ln 0.05 = 2.996$, and the detector declares a signal. At the wrong cycle frequency $\alpha = 1/8$, the terms are $e^{j2\pi n/8}$, which add to zero over eight samples, and $T = 0$.

**With noise.** For BPSK at $\alpha = 2 f_c$ and large $N$, $T$ is about $k\,|Z|^2$ with $Z$ complex Gaussian of unit variance and mean $\sqrt\mu$, where $\mu = N\gamma^2/(4\gamma + 2)$, $k = (2\gamma + 1)/(1 + \gamma)^2$ and $\gamma$ is the SNR. The table gives $P_d$ for $P_{fa} = 0.05$, next to the energy detector with the exact noise power:

| SNR | $N = 64$ | $N = 256$ | $N = 1024$ | energy detector, $N = 64$ / $256$ / $1024$ |
|---|---|---|---|---|
| $0$ dB | 0.973 | 1.000 | 1.000 | 1.000 / 1.000 / 1.000 |
| $-5$ dB | 0.378 | 0.945 | 1.000 | 0.731 / 0.997 / 1.000 |
| $-10$ dB | 0.091 | 0.235 | 0.744 | 0.199 / 0.463 / 0.921 |

For $P_{fa} = 0.1$ and $P_d = 0.9$, the cyclic test needs $179$, $1{,}263$ and $11{,}127$ samples at $-5$, $-10$ and $-15$ dB, against $85$, $721$ and $6{,}775$ for the energy detector. Both grow like $1/\mathrm{SNR}^2$. But if the noise power is only known within $1$ dB, the energy detector cannot reach any SNR below $-3.3$ dB, while the cyclic test is not changed at all.

## Correctness

**Claim.** Under $H_0$, as $N \to \infty$, $T$ tends in law to a unit exponential, so $\Pr[T > -\ln P_{fa}] \to P_{fa}$, for every noise power. Under $H_1$ with $R^\alpha(\tau) \ne 0$, $T$ grows like $N$, and $P_d \to 1$.

**Key steps.** Under $H_0$, the terms $u_n = y[n + \tau] y[n] e^{-j2\pi\alpha n}$ have mean zero, since circular noise has $\mathbb E[w^2] = 0$ and distinct samples are independent. They are uncorrelated with each other, and $\mathbb E|u_n|^2 = c\sigma^4$: for $\tau = 0$, $\mathbb E|w|^4 = 2\sigma^4$, and for $\tau \ge 1$, the two factors are independent. They are also circular. The sequence is $\tau$-dependent, so the [central limit theorem](/central-limit-theorem/) for $m$-dependent sequences gives $\sum_n u_n / \sqrt{M c\sigma^4} \to \mathcal{CN}(0, 1)$, whose squared magnitude is a unit exponential. The [law of large numbers](/law-of-large-numbers/) gives $P \to \sigma^2$, and so $T = |\sum_n u_n|^2/(M c P^2)$ has the same limit. Under $H_1$, $R \to R^\alpha(\tau) \ne 0$ and $P$ tends to the total power, so $T/M$ tends to a positive constant. Scaling $y$ by any $a \ne 0$ multiplies $|R|^2$ and $P^2$ by $|a|^4$, so $T$ does not depend on the noise power. The full proof is in the proofs folder.

## Complexity

In the [real RAM](/real-ram/), one cycle frequency and one lag take $O(N)$ time: lines L3 and L4 each pass over the samples once, and the rotation $e^{-j2\pi\alpha n}$ is updated by one multiplication per sample. The extra space is $O(1)$. A scan over all $M$ cycle frequencies $k/M$ is one DFT of the products, $O(N \log N)$ with the [FFT](/fast-fourier-transform/); the reference code uses the direct $O(N^2)$ DFT. A full spectral correlation map over many cycle frequencies and many lags or frequency bins costs much more, which is why practical detectors test a few known features.

## Properties

- **No noise power needed.** $T$ is invariant to scaling of the samples, so the threshold holds for any white noise level, and an error in the noise power gives no SNR wall.
- **Asymptotic false alarm rate.** The rate tends to $P_{fa}$ as $N$ grows. At finite $N$, $T \le N^2/(cM)$ by the Cauchy-Schwarz inequality, so its far tail is lighter than the exponential law. In simulations with $64$ and $128$ samples, the scan over all bins had a false alarm rate below its target of $0.1$.
- **Selective.** It reacts only to signals with a feature at the tested $(\alpha, \tau)$, so it can tell BPSK from QPSK, or a primary user from other users of the band with different symbol rates or carriers.
- **Slower than the energy detector with exact noise power.** The sample count also grows like $1/\mathrm{SNR}^2$, with a constant about $1.6$ to $2.1$ times larger in the cases above.

## Variants and improvements

- **Several lags and frequencies.** Dandawate and Giannakis test a vector of cyclic correlations at several lags with an estimated covariance; the statistic is asymptotically chi-square with twice the number of lags as degrees of freedom.
- **Spectral correlation.** Estimate the spectral correlation density $S^\alpha(f)$, the Fourier transform of $R^\alpha(\tau)$ in $\tau$, by the FFT accumulation method or the strip spectral correlation analyzer, and look for peaks off the line $\alpha = 0$.
- **Non-conjugate features.** For signals without conjugate features, such as QPSK or OFDM, use the non-conjugate form at the symbol rate, which needs pulse shaping with excess bandwidth, or at the block rate of a cyclic prefix.
- **Pilot and preamble features.** Some standards add a feature on purpose, for example a repeated pilot pattern, so that a detector can find the signal at low SNR.
- **Two-stage sensing.** Use the energy detector to find candidate bands, then a feature detector to confirm and classify them.

## When to use it

Use it when the noise power is uncertain or drifts, when the signal of interest has a known feature, or when the detector must separate the signal from other signals in the same band. For a single wideband scan with a well calibrated noise floor, the energy detector is simpler and needs fewer samples. When a full known preamble is present, a [matched filter](/matched-filter/) needs fewer samples than both.

## Pitfalls

- **Cycle frequency errors.** An error $\delta$ in $\alpha$ makes the terms rotate by $2\pi\delta$ per sample, and the sum cancels once $N\delta$ is about $1$. A carrier offset of the receiver moves the conjugate feature of BPSK by twice the offset. Search a small range of $\alpha$, with the scan threshold.
- **Colored noise and interference with features.** The threshold assumes white noise. Spurs, narrowband interferers and adjacent signals can have features at the same $\alpha$.
- **Wrong form.** QPSK and most higher-order signals have no conjugate feature at $\tau = 0$; a test for one will not see them.
- **Small samples.** The exponential law is a large-$N$ result. Check the rate by simulation for the $N$ and $P_{fa}$ in use, especially for small $P_{fa}$.

## Implementations

## History

The theory of cyclostationary signals in communications grew from the work of Gardner and others in the 1970s and 1980s, who showed that modulated signals have spectral correlation at cycle frequencies tied to the carrier and the symbol rate. Gardner (1988) set out feature detection for signal interception, and his 1991 survey listed the features of common modulations. Dandawate and Giannakis (1994) gave asymptotic chi-square tests for the presence of cyclostationarity. With cognitive radio in the 2000s, feature detection became the main alternative to energy detection for spectrum sensing at low SNR.

## References
