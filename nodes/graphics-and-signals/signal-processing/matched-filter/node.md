---
tag: 3Q26KM
kind: algorithm
slug: matched-filter
name: Matched filter
aliases:
- correlation receiver
area: graphics-and-signals/signal-processing
level: core
summary: "Filter the data with the time-reversed conjugate of a known pulse, which maximizes the output signal to noise ratio in white noise, and compare the output with a threshold."
solves: [signal-detection]
model: real-ram
complexity:
  vars: {N: the length of the pulse, M: the length of the record}
  time: {worst: Θ(M N), average: Θ(M N), best: Θ(M N)}
  space: {extra: Θ(M)}
properties: {deterministic: true, linear: true, optimal_snr: true, most_powerful_gaussian: true}
history:
  year: 1943
  people: [Dwight O. North]
  note: North derived the filter that maximizes the peak signal to noise ratio of a radar pulse in a 1943 RCA report, reprinted in the Proceedings of the IEEE in 1963.
prereqs: [cross-correlation, fir-filter]
see_also: [signal-detection, cross-correlation, normalized-cross-correlation, template-matching, wiener-filter, overlap-save-method, additive-white-gaussian-noise-channel, roc-auc]
sources:
  - paper: doi:10.1109/PROC.1963.2383
    title: Dwight O. North, An analysis of the factors which determine signal/noise discrimination in pulsed-carrier systems, Proceedings of the IEEE 51(7), 1963 (reprint of RCA Laboratories report PTR-6C, 1943)
    locator: pp. 1016 to 1027 (the filter that maximizes the ratio of peak signal to noise, with the transfer function proportional to the conjugate spectrum of the pulse)
  - paper: doi:10.1109/TIT.1960.1057571
    title: George L. Turin, An introduction to matched filters, IRE Transactions on Information Theory 6(3), 1960
    locator: pp. 311 to 329 (the derivation by the Schwarz inequality, the correlation receiver, colored noise and the likelihood ratio view)
  - book: isbn:9780135041352
    title: Steven M. Kay, Fundamentals of Statistical Signal Processing, Volume II, Detection Theory, Prentice Hall, 1998
    locator: Chapter 4, Deterministic Signals (Section 4.3, matched filters, with the detection performance, and Section 4.4, generalized matched filters for colored noise)
---

The matched filter detects a known pulse $s[0], \dots, s[N-1]$ in noise. It filters the data with the impulse response $h[n] = \overline{s[N-1-n]}$, the pulse reversed in time and conjugated, which is the same as computing the [cross-correlation](/cross-correlation/) of the data with the pulse. It then compares the output with a threshold. Among all linear filters, this one gives the largest ratio of signal power to noise power at the output sample where the pulse ends, if the noise is white. The ratio there is $E/\sigma^2$, the pulse energy over the noise variance, whatever the shape of the pulse. For Gaussian noise, the threshold test on its output is also the most powerful test of [signal detection](/signal-detection/) at a given false alarm rate. It is the receiver of radar, sonar and digital communication, and is also called the correlation receiver. For images, the normalized score that tolerates changes of brightness is [normalized cross-correlation](/normalized-cross-correlation/).

## In plain words

You know the exact shape of the pulse you are looking for, and the noise is random. Slide a copy of the pulse along the data, and at each position multiply sample by sample and add. Where the pulse really is, all the products add up in step and give a large number. The noise products have random signs and partly cancel. No other set of weights makes the pulse stand out more against the noise. Declare the pulse present where the sum is above a threshold, which you choose from the rate of false alarms you accept.

## The problem

The data are $x[0], \dots, x[M-1]$ with either $x[n] = w[n]$ (noise only) or $x[n] = s[n - t] + w[n]$ for an unknown start time $t$, where $s$ is known and $w$ is white noise of variance $\sigma^2$. Find a linear filter whose output at the end of the pulse has the largest signal to noise ratio, and decide for each $t$ whether the pulse is present, with the probability of a false alarm at each $t$ equal to a given $P_{FA}$. The detection problem itself, with its other models, is on the [signal detection](/signal-detection/) page.

## The algorithm

For real data and real Gaussian noise:

```pseudo id=main
MATCHED-FILTER-DETECT(x[0 .. M − 1], s[0 .. N − 1], σ², P_FA)
L1  h[n] ← conj(s[N − 1 − n]),  n = 0, …, N − 1
L2  y[n] ← Σ_{k=0}^{N−1} h[k]·x[n − k],  n = 0, …, M − 1      ▷ x = 0 before 0
L3  γ ← sqrt(σ² · E) · Q⁻¹(P_FA),  E = Σ |s[n]|²
L4  for n ← N − 1 to M − 1 do
L5      if y[n] > γ then report a pulse starting at n − N + 1
L6  return the reported start times
```

Line L2 is an [FIR filter](/fir-filter/), and $y[n] = \sum_k \overline{s[k]}\, x[n - N + 1 + k]$ is the cross-correlation of $x$ with $s$ at lag $n - N + 1$. Line L3 uses $Q(u) = \Pr(Z > u) = \tfrac12\operatorname{erfc}(u/\sqrt2)$ for a standard normal $Z$. The implementation inverts $Q$ by bisection. For complex data with circular noise of total variance $\sigma^2$, compare $\operatorname{Re} y[n]$ with $\sqrt{\sigma^2E/2}\,Q^{-1}(P_{FA})$ when the phase is known, or $|y[n]|^2$ with $\sigma^2 E \ln(1/P_{FA})$ when it is not.

## Example

Take the pulse $s = (1, 2, 2, -1)$, with $E = 10$, so $h = (-1, 2, 2, 1)$. Put it into a record of 8 samples starting at $t = 2$, without noise: $x = (0, 0, 1, 2, 2, -1, 0, 0)$. Line L2 gives:

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $y[n]$ | 0 | 0 | $-1$ | 0 | 4 | 10 | 4 | 0 |

The peak $y[5] = E = 10$ is at the end of the pulse, $n = t + N - 1$. The other values are the [autocorrelation](/autocorrelation/) of $s$ at lags $\pm1, \pm2, \pm3$: $4, 0, -1$. With $\sigma^2 = 1$ and $P_{FA} = 10^{-3}$, line L3 gives $Q^{-1}(10^{-3}) = 3.0902$ and $\gamma = \sqrt{10} \cdot 3.0902 = 9.772$. Only $y[5]$ crosses, and the detector reports $t = 2$. The output signal to noise ratio is $E/\sigma^2 = 10$ (10.0 dB). A plain average over 4 samples, $h = (1, 1, 1, 1)$, gives $(\sum s)^2/(4\sigma^2) = 4$ (6.0 dB), and $h = (1, 0, 0, 0)$ gives $1$. With noise, the detector finds this pulse with probability $P_D = Q(3.0902 - \sqrt{10}) = 0.529$. With a threshold close to zero, the side lobes $y[4] = y[6] = 4$ also cross and the detector reports $t = 1, 2, 3$, which is why a practical detector keeps only local maxima.

## Correctness

At the end of a pulse that starts at $t$, the output is $y = \sum_k h[k]\,s[N-1-k] + \sum_k h[k]\,w[t+N-1-k]$. The noise part has variance $\sigma^2\sum_k |h[k]|^2$ because the noise is white. By the Cauchy-Schwarz inequality, $|\sum_k h[k]\,s[N-1-k]|^2 \le E\sum_k |h[k]|^2$, so the output signal to noise ratio is at most $E/\sigma^2$, with equality exactly when $h$ is a multiple of the filter of line L1. For Gaussian noise, the output is normal with mean $0$ or $E$ and variance $\sigma^2 E$. So the threshold of line L3 gives the false alarm probability $P_{FA}$ and the detection probability $P_D = Q(Q^{-1}(P_{FA}) - \sqrt{E/\sigma^2})$. The log likelihood ratio of the two hypotheses is $(y - E/2)/\sigma^2$, increasing in $y$, so by the Neyman-Pearson lemma no test with the same false alarm probability detects more often. The full proof is below.

## Complexity

**Time.** Line L2 costs $N$ multiplies per output sample, $\Theta(MN)$ for the record. With the FFT and the [overlap-save method](/overlap-save-method/) it costs $O(M \log N)$, which is the better choice for pulses longer than a few dozen samples. Lines L4 and L5 cost $\Theta(M)$, and line L3 is one evaluation of $Q^{-1}$.

**Space.** $\Theta(M)$ for the output as implemented, or $\Theta(N)$ for a streaming filter that tests each output as it is produced.

## Properties

- **Best signal to noise ratio.** Measured in exact rational arithmetic over 500 random pulses of lengths 1 to 8 and 500 random filters, with random noise variances (seed 5101), every filter gave an output signal to noise ratio of at most $E/\sigma^2$. Equality held exactly when the filter was proportional to the matched filter. For the pulse of the example and 500 random Gaussian filters (seed 5104), the mean ratio was $2.51$ against the optimum $10$, the largest was $9.94$, and only $3.6\%$ came within 1 dB of the optimum.
- **Shape does not matter, energy does.** The best ratio is $E/\sigma^2$ for every pulse of energy $E$. A long pulse of low power performs as well as a short strong one, which is the basis of pulse compression in radar.
- **False alarm rate as designed.** For a pulse of 16 samples with $E = 4$, $\sigma^2 = 1$ and $P_{FA} = 0.01$, over 20000 noise records (seed 5103), the measured false alarm rate was $0.00875$, which is $1.8$ binomial standard deviations ($0.0007$) from $0.01$. The detection rate with the pulse present was $0.3765$, against $P_D = 0.3721$ from the formula, with a standard deviation of $0.0034$.
- **Most powerful for Gaussian noise.** For a known pulse in white Gaussian noise, the threshold test on the matched filter output maximizes $P_D$ at the given $P_{FA}$.
- **Linear and time invariant.** The filter is an FIR filter, so it can run on a stream and its output for a delayed pulse is delayed by the same amount, which turns detection into the estimation of the arrival time.

## Variants and improvements

- **Colored noise.** For noise with covariance $C$, the best weights are $C^{-1}s$, which is whitening followed by the filter matched to the whitened pulse. Measured in exact arithmetic over 300 random positive definite matrices (seed 5102), the weights $C^{-1}s$ gave the ratio $s^T C^{-1} s$ and no random weights did better.
- **Unknown phase or amplitude.** For a carrier of unknown phase, compare the magnitude $|y|$ with a threshold (the envelope or quadrature detector). For an unknown amplitude, the generalized likelihood ratio test gives the same filter with a normalized statistic.
- **Pulse compression.** Radars send long chirps or coded pulses with low power and compress them with the matched filter into a sharp peak, which gives the range resolution of a short pulse with the energy of a long one.
- **Filter banks.** For a pulse with unknown Doppler shift or one of several known shapes, run one matched filter per hypothesis. A bank matched to $M$ symbols is the optimal receiver of $M$-ary communication over the [additive white Gaussian noise channel](/additive-white-gaussian-noise-channel/).
- **Normalized correlation.** If the gain of the signal is unknown and changes, divide by the local energy of the data. For images this is [normalized cross-correlation](/normalized-cross-correlation/), used in [template matching](/template-matching/).

## When to use it

Use the matched filter whenever the waveform you are looking for is known and the noise is close to white, or can be whitened: radar and sonar echoes, symbols in digital receivers, synchronization words, seismic and gravitational wave templates, and spikes in neural recordings. It is the first stage of most detectors, followed by a threshold and peak picking. If the noise is not white and its spectrum is unknown, estimate it first. If the signal is random rather than known, the right detector is an energy or estimator-correlator detector, not a matched filter. If the goal is to recover the waveform rather than to detect it, use a [Wiener filter](/wiener-filter/).

## Pitfalls

- **Forgetting the time reversal or the conjugate in line L1.** Without the reversal, line L2 computes a convolution with $s$, which does not peak at the pulse. Without the conjugate, a complex pulse is not matched and the peak can vanish.
- **A threshold from the wrong noise level in line L3.** $\gamma$ scales with $\sigma$, so an error of 1 dB in the noise power changes the false alarm rate by a large factor at small $P_{FA}$. Estimate $\sigma^2$ from the data, as CFAR detectors do.
- **Counting every sample above the threshold in line L5.** The side lobes of the pulse's autocorrelation also cross a low threshold, as in the example. Keep local maxima, or use a pulse with low side lobes.
- **Many tests, one false alarm rate.** Line L5 runs $M - N + 1$ tests, and each has false alarm probability $P_{FA}$, so a long record has about $(M - N + 1)P_{FA}$ false alarms. Choose $P_{FA}$ per test from the rate per record you accept.
- **Mismatch.** A Doppler shift, a delay that is not a whole number of samples, or a distorted channel lowers the peak. A pulse whose energy is spread over a long time is more sensitive to a frequency shift.

## Implementations

## History

Dwight O. North of RCA Laboratories derived the filter that maximizes the peak signal to noise ratio of a radar pulse in a classified report of 1943. He showed that, in white noise, its transfer function is the complex conjugate of the pulse spectrum times a delay. The report was reprinted in the Proceedings of the IEEE in 1963. Van Vleck and Middleton reached the same result independently at Harvard during the war and published it in 1946. After the war, the connection with statistical hypothesis testing (the likelihood ratio, Woodward's ambiguity function and the work of Middleton) made the matched filter the standard optimal receiver. George Turin's 1960 tutorial summarized the theory, and pulse compression radars, spread spectrum communications and modern template searches in gravitational wave astronomy are built on it.

## References
