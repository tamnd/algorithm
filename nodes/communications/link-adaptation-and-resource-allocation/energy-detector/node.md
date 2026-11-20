---
tag: T2T7RR
kind: algorithm
slug: energy-detector
name: Energy detector
aliases:
- radiometer
- Urkowitz energy detector
area: communications/link-adaptation-and-resource-allocation
level: core
summary: Declares a signal present when the energy of the received samples over a window exceeds a threshold set by the noise level.
solves: [spectrum-sensing]
model: real-ram
complexity:
  vars: {N: the number of samples}
  time: {worst: O(N)}
  space: {extra: O(1)}
properties: {deterministic: true, needs_noise_power: true, needs_signal_knowledge: false, exact_false_alarm_rate: true}
history:
  year: 1967
  people: [Harry Urkowitz]
  note: "Urkowitz analyzed the energy of a band-limited record of length T and bandwidth W as a chi-square variable with about 2TW degrees of freedom, central under noise and noncentral with a signal, and gave the detection curves of the radiometer."
prereqs: [neyman-pearson-lemma, signal-detection]
see_also: [spectrum-sensing, cyclostationary-feature-detection, matched-filter, likelihood-ratio-test, cfar-detection, neyman-pearson-lemma, central-limit-theorem, periodogram]
sources:
  - paper: doi:10.1109/PROC.1967.5573
    title: "Harry Urkowitz, Energy detection of unknown deterministic signals, Proceedings of the IEEE 55(4), 1967, pages 523 to 531"
    locator: "the energy of a band-limited record as a sum of about 2TW squared samples, its central and noncentral chi-square laws, and the curves of detection probability against SNR"
  - paper: doi:10.1109/JSTSP.2007.914879
    title: "Rahul Tandra and Anant Sahai, SNR walls for signal detection, IEEE Journal of Selected Topics in Signal Processing 2(1), 2008, pages 4 to 17"
    locator: "the sample count of the radiometer that grows like 1 over SNR squared, the noise uncertainty model with factor rho, and the SNR wall rho - 1/rho"
  - book: isbn:9780135041352
    title: "Steven M. Kay, Fundamentals of Statistical Signal Processing, Volume II: Detection Theory, Prentice Hall, 1998"
    locator: "Chapter 5 (detection of random signals: the energy detector for a white Gaussian signal and its chi-square performance) and Chapter 7 (the generalized likelihood ratio test for an unknown deterministic signal)"
---

The energy detector, or radiometer, decides whether a band holds a signal by adding the energy of $N$ received samples and comparing the sum with a threshold. It needs no knowledge of the signal: not its waveform, its modulation or its timing, only the noise power $\sigma^2$, which sets the threshold. With complex Gaussian noise, the normalized energy $T = \sum_n |y[n]|^2 / \sigma^2$ has a gamma law under noise only, so the threshold for a target false alarm rate can be computed exactly. The detector is the [likelihood ratio test](/likelihood-ratio-test/) for a white Gaussian signal of any power, and the generalized likelihood ratio test for a fully unknown signal. It is the standard first test for [spectrum sensing](/spectrum-sensing/). Its two weak points are that the number of samples grows like $1/\mathrm{SNR}^2$, against $1/\mathrm{SNR}$ for a [matched filter](/matched-filter/), and that an error in $\sigma^2$ shifts the threshold, which creates an SNR wall below which no number of samples is enough.

## In plain words

To find out whether someone is sending in a radio band, the receiver listens for a short time and adds up how much energy it picked up. If there is only noise, the total is close to a known value. If someone is sending, the total is larger. The receiver compares the total with a limit chosen so that noise alone passes it only rarely, for example once in twenty tries. Above the limit, it says a signal is present. The method needs no idea of what the signal looks like. But it must know how strong the noise is. If it gets the noise level a little wrong, very weak signals can never be told apart from noise, however long it listens.

## The problem

The receiver has $N$ complex baseband samples. Under $H_0$, $y[n] = w[n]$ with $w[n]$ independent $\mathcal{CN}(0, \sigma^2)$ and $\sigma^2$ known. Under $H_1$, $y[n] = s[n] + w[n]$, where nothing is known about $s$ except that it is independent of the noise. The SNR is the signal power per sample over $\sigma^2$. For a target false alarm rate $P_{fa} \in (0, 1)$, decide between $H_0$ and $H_1$ with $\Pr[\text{decide } H_1 \mid H_0] = P_{fa}$ exactly, and report the detection probability $P_d$ for the signals of interest.

## The algorithm

```pseudo id=main
ENERGY-DETECTOR(y[0..N-1], σ², P_fa)
L1  λ ← the root of e^{-λ} Σ_{k<N} λ^k / k! = P_fa
L2  T ← 0
L3  for n ← 0 to N - 1 do T ← T + |y[n]|²
L4  T ← T / σ²
L5  if T > λ then return "signal present"
L6  return "noise only"
```

Line L1 depends only on $N$ and $P_{fa}$, so it is computed once and stored. The left side decreases in $\lambda$, from $1$ at $\lambda = 0$ to $0$, so bisection finds the root. For large $N$, the [central limit theorem](/central-limit-theorem/) gives $\lambda \approx N + \sqrt N\, Q^{-1}(P_{fa})$.

## Example

Take $N = 16$ samples and $P_{fa} = 0.05$. Line L1 gives $\lambda = 23.097$: under noise only, $T$ has mean $16$ and standard deviation $4$, and the threshold is $1.77$ standard deviations above the mean.

| SNR | $P_d$, Gaussian signal | $P_d$, QPSK signal |
|---|---|---|
| $-5$ dB | 0.3235 | 0.3213 |
| $0$ dB | 0.8752 | 0.9104 |
| $5$ dB | 0.9998 | 1.0000 |

With $N = 64$ the threshold is $77.70$, and at $-5$ dB the detection probabilities rise to $0.724$ and $0.731$. A signal of constant power (QPSK) is a little easier to detect than a Gaussian one of the same mean power at medium SNR, because its energy does not fluctuate.

**Samples for a target.** For $P_{fa} = 0.1$ and $P_d = 0.9$ with a Gaussian signal, the normal approximation $N \approx \big(Q^{-1}(P_{fa}) - (1 + \mathrm{SNR}) Q^{-1}(P_d)\big)^2 / \mathrm{SNR}^2$ gives $89$, $725$, $6{,}779$ and $66{,}354$ samples at $-5$, $-10$, $-15$ and $-20$ dB. With the exact threshold, these sample counts give $P_d$ between $0.900$ and $0.904$.

**The SNR wall.** Suppose the true noise power is only known to lie in $[\sigma^2/\rho, \rho\sigma^2]$, with $\rho = 10^{x/10}$ for an uncertainty of $x$ dB. To keep $P_{fa}$ for every noise level, the threshold must assume $\rho\sigma^2$. A signal of power $P$ in the smallest noise $\sigma^2/\rho$ gives $\mathbb E[T]$ above this only if $P > (\rho - 1/\rho)\sigma^2$. For $x = 1$ dB the wall is $\rho - 1/\rho = 0.465$, or $-3.3$ dB. With $N = 10^5$ samples and $P_{fa} = 0.1$, a Gaussian signal at $-4$ dB, just below the wall, is detected with probability below $10^{-6}$ in the smallest noise, while at $-2.5$ dB it is detected with probability above $0.999999$.

## Correctness

**Claim.** Under $H_0$, $T$ has the $\mathrm{Gamma}(N, 1)$ law, $\Pr[T > \lambda] = e^{-\lambda} \sum_{k < N} \lambda^k / k!$, and so the detector has false alarm rate exactly $P_{fa}$. With a complex Gaussian signal of SNR $\gamma$, white and independent of the noise, $P_d = \Pr[\mathrm{Gamma}(N, 1) > \lambda / (1 + \gamma)]$. With a fixed signal of total energy $\mu \sigma^2$, $P_d = \sum_{j \ge 0} e^{-\mu} \frac{\mu^j}{j!} \Pr[\mathrm{Gamma}(N + j, 1) > \lambda]$.

**Key steps.** For $w \sim \mathcal{CN}(0, \sigma^2)$, $|w|^2 / \sigma^2$ is half a chi-square with $2$ degrees of freedom, which is a unit exponential. The sum of $N$ independent unit exponentials is $\mathrm{Gamma}(N, 1)$: it is the time of the $N$-th event of a Poisson process of rate $1$, so it exceeds $\lambda$ exactly when fewer than $N$ events fall in $[0, \lambda]$, which has probability $e^{-\lambda} \sum_{k < N} \lambda^k / k!$. The tail is continuous and strictly decreasing, so the root of line L1 gives the exact rate. With a Gaussian signal, $y[n] \sim \mathcal{CN}(0, (1 + \gamma)\sigma^2)$, and the same argument applies to $T / (1 + \gamma)$. With a fixed signal, $2T$ is a noncentral chi-square with $2N$ degrees of freedom and noncentrality $2\mu$, whose law is a Poisson mixture of central ones. The full proof is in the proofs folder.

**Optimality.** For a Gaussian signal with covariance $\gamma\sigma^2 I$, the log-likelihood ratio is $\frac{\gamma}{(1 + \gamma)\sigma^2} \sum_n |y[n]|^2$ plus a constant, increasing in $T$ for every $\gamma > 0$. By the [Neyman-Pearson lemma](/neyman-pearson-lemma/), the energy detector is the most powerful test at its $P_{fa}$, uniformly in $\gamma$.

## Complexity

In the [real RAM](/real-ram/), lines L2 to L5 take $N$ squared magnitudes and additions: $O(N)$ time and $O(1)$ extra space, and the statistic can be updated as samples arrive. The threshold of line L1 takes $O(N)$ per evaluation of the tail, or $O(\sqrt N)$ if the sum starts at its largest term, times about $50$ steps of bisection, once for each pair $(N, P_{fa})$. In hardware, the energy of a band is often computed from FFT bins, as a sum of [periodogram](/periodogram/) values, at $O(N \log N)$ for all subbands at once.

## Properties

- **Blind.** It needs no knowledge of the signal: modulation, bandwidth inside the band, timing and carrier phase can all be unknown.
- **Exact false alarm rate.** With known $\sigma^2$ and white Gaussian noise, the threshold gives $P_{fa}$ exactly for every $N$.
- **Optimal for Gaussian signals.** It is the most powerful test for a white Gaussian signal of any power, and the generalized likelihood ratio test for an unknown deterministic signal.
- **Slow at low SNR.** For fixed $P_{fa}$ and $P_d$, the number of samples grows like $1/\mathrm{SNR}^2$, because the signal shifts the mean of $T$ by $N\,\mathrm{SNR}$ while its standard deviation is $\sqrt N$.
- **Not robust to noise power errors.** An error of a factor $\rho$ in $\sigma^2$ creates the SNR wall $\rho - 1/\rho$.

## Variants and improvements

- **Real-valued samples.** For $N$ real samples with noise $\mathcal N(0, \sigma^2)$, $T$ is chi-square with $N$ degrees of freedom; Urkowitz's model of a record of time $T_0$ and bandwidth $W$ has about $2 T_0 W$ degrees of freedom.
- **Estimated noise power.** Estimate $\sigma^2$ from a band known to be empty, or from reference cells as in [CFAR detection](/cfar-detection/); the threshold then follows an F law, and the SNR wall moves with the quality of the estimate.
- **Frequency-domain energy.** Sum the periodogram over the bins of a subband to test many subbands at once, or weight the bins by the expected signal spectrum, which brings the test closer to the [likelihood ratio test](/likelihood-ratio-test/) for a colored signal.
- **Two-stage sensing.** Use the energy detector to find candidate bands quickly, then a [cyclostationary feature detector](/cyclostationary-feature-detection/) or a matched filter on those bands.
- **Fading and diversity.** Average $P_d$ over the fading law, or combine the energies of several antennas or sensors; combining the energies of $L$ sensors is an energy detector with $L N$ samples.

## When to use it

Use it when nothing reliable is known about the signal and the noise power is well calibrated, for example for listen-before-talk in unlicensed bands, for a first scan of wide bands, or when the SNR is moderate. When a pilot or preamble is known, a matched filter needs far fewer samples. When the noise power is uncertain and the SNR is low, use a test that does not depend on it, such as a cyclostationary or eigenvalue test.

## Pitfalls

- **Wrong noise power.** A noise estimate that is $1$ dB too low raises $P_{fa}$ far above its target; one that is too high hides weak signals. Calibrate $\sigma^2$ often, as it drifts with temperature and gain.
- **Colored noise and interference.** The threshold assumes white Gaussian noise; spurs, adjacent-channel leakage and impulsive interference all look like signal.
- **Long records do not fix everything.** Below the SNR wall, more samples do not help, and the time variation of the noise limits how long a record is useful.
- **Signals that only occupy part of the band or the record.** A narrow or bursty signal adds little to the total energy; split the band or the record into pieces and test each.
- **Real versus complex samples.** The threshold for complex samples uses $\mathrm{Gamma}(N, 1)$; for real samples it uses chi-square with $N$ degrees of freedom. Mixing the two gives the wrong $P_{fa}$.

## Implementations

## History

Urkowitz (1967) gave the first detailed analysis of the energy detector for an unknown deterministic signal in band-limited white Gaussian noise. He used the sampling theorem to write the energy of a record of length $T_0$ and bandwidth $W$ as a sum of about $2 T_0 W$ squared samples, with a central chi-square law under noise and a noncentral one with a signal, and gave the curves of $P_d$ against SNR. The radiometer itself was older, from radio astronomy and radar. With cognitive radio in the 2000s it became the standard sensing test, and Tandra and Sahai (2008) showed that noise uncertainty gives it an SNR wall.

## References
