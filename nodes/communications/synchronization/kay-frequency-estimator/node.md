---
tag: 9RD1BP
kind: algorithm
slug: kay-frequency-estimator
name: Kay frequency estimator
aliases:
- Kay weighted phase averager
area: communications/synchronization
level: advanced
summary: "Estimates a tone frequency by a weighted average of phase differences of consecutive samples. It reaches the CRB above a threshold SNR; below it, phase wraps cause large errors."
solves: [frequency-offset-estimation]
model: real-ram
complexity:
  vars: {N: the number of samples}
  time: {worst: O(N)}
  space: {extra: O(1)}
properties: {deterministic: true, feedforward: true, range: "|omega| < pi radians per sample", efficient_above_threshold: true}
history:
  year: 1989
  people: [Steven M. Kay]
  note: "Steven Kay published the estimator in 1989. It applies the weights of the best linear unbiased estimator to the phase differences of consecutive samples, which avoids the phase unwrapping that the linear regression of Tretter needs."
prereqs: [frequency-offset-estimation, cramer-rao-bound, gauss-markov-theorem]
see_also: [rife-boorstyn-frequency-estimator, luise-reggiannini-estimator, modified-cramer-rao-bound, linear-prediction, phase-unwrapping, periodogram, carrier-recovery, viterbi-viterbi-phase-estimation]
sources:
  - paper: doi:10.1109/29.45547
    title: "S. Kay, A fast and accurate single frequency estimator, IEEE Transactions on Acoustics, Speech, and Signal Processing 37(12), 1989, pages 1987 to 1990"
    locator: "the weighted phase averager with parabolic weights, its high-SNR variance at the Cramer-Rao bound, and its relation to the linear prediction estimator"
  - book: isbn:9780306457258
    title: "Umberto Mengali and Aldo N. D'Andrea, Synchronization Techniques for Digital Receivers, Plenum Press, 1997"
    locator: "Chapter 3 (carrier frequency recovery with linear modulations, data-aided feedforward estimators)"
  - book: isbn:9780133457117
    title: "Steven M. Kay, Fundamentals of Statistical Signal Processing, Volume I: Estimation Theory, Prentice Hall, 1993"
    locator: "Chapter 3 (the Cramer-Rao lower bound, including the bound for the parameters of a sinusoid)"
---

The Kay frequency estimator finds the frequency $\omega$ of one complex tone in white noise from $N$ samples. It computes the phase difference $\arg(r_{t+1}\overline{r_t})$ of each pair of consecutive samples and takes a weighted average with the parabolic weights $w_t = \frac{6(t+1)(N-1-t)}{N(N^2-1)}$. These weights are the best linear unbiased weights for the correlated noise of the differences, so above a threshold SNR its variance reaches the [Cramer-Rao bound](/cramer-rao-bound/) $\frac{6}{\mathrm{SNR}\,N(N^2-1)}$; in synchronization with known data this is the [modified Cramer-Rao bound](/modified-cramer-rao-bound/). It is one of the estimators for [frequency offset estimation](/frequency-offset-estimation/). The [Rife and Boorstyn estimator](/rife-boorstyn-frequency-estimator/) finds the maximum likelihood frequency at the peak of the [periodogram](/periodogram/) and has a lower threshold, at a higher cost. The [Luise and Reggiannini estimator](/luise-reggiannini-estimator/) uses the angle of a sum of autocorrelations and works down to lower SNR with a smaller range. Kay's estimator covers the full range $|\omega| < \pi$ and costs one angle per sample, but each angle uses only two samples, so its threshold is set by the per-sample SNR and does not drop as $N$ grows.

## In plain words

A pure tone turns by the same angle from each sample to the next, and that angle is the frequency. So the receiver measures the turn between each pair of neighbors and averages the measurements. Noise disturbs each sample, and each disturbance enters two neighboring measurements with opposite signs. A plain average would cancel almost everything except the first and last samples. Giving the middle measurements more weight, along a parabola, uses all samples in the best way. When noise is so strong that a single turn can look like a turn the other way round, the method makes large errors.

## The problem

The input is $r_t = A e^{j(\omega t + \phi)} + w_t$, $t = 0, \ldots, N - 1$, where the amplitude $A > 0$, the phase $\phi$ and the frequency $\omega \in (-\pi, \pi)$ in radians per sample are unknown, and $w_t \sim \mathcal{CN}(0, N_0)$ is white, $\mathrm{SNR} = A^2/N_0$. In a receiver, $r_t$ is the received signal with the data removed: the known pilot symbols divided out, or, for M-PSK, the Mth power taken, which multiplies the frequency by $M$. Output $\hat\omega$.

## The algorithm

```pseudo id=main
KAY(r[0..N-1])
L1  w[t] <- 6 (t + 1) (N - 1 - t) / (N (N^2 - 1)) for t = 0..N-2
L2  omega <- 0
L3  for t <- 0 to N - 2 do
L4      d <- arg(r[t+1] * conj(r[t]))            ▷ phase difference in (-pi, pi]
L5      omega <- omega + w[t] * d
L6  return omega
```

Line L4 takes the angle of the product, not the difference of two angles, so no phase unwrapping is needed as long as each single difference stays in $(-\pi, \pi]$. Line L1 gives a parabola that is largest in the middle. The weights sum to 1; the frequency in cycles per sample is $\hat\omega/(2\pi)$.

## Example

$N = 6$, $\omega = 0.4$, $\phi = 0$, $\mathrm{SNR} = 10$ dB (noise seed 8). The weights are $0.1429, 0.2286, 0.2571, 0.2286, 0.1429$.

| $t$ | $r_t$ | $d_t$ (line L4) | $w_t d_t$ |
|---|---|---|---|
| 0 | $1.083 + 0.566j$ | $0.0193$ | $0.0028$ |
| 1 | $1.166 + 0.638j$ | $0.2611$ | $0.0597$ |
| 2 | $0.842 + 0.803j$ | $0.3030$ | $0.0779$ |
| 3 | $0.516 + 0.931j$ | $0.7311$ | $0.1671$ |
| 4 | $-0.185 + 0.807j$ | $0.3693$ | $0.0528$ |

The last sample is $r_5 = -0.666 + 0.985j$. The estimate is $\hat\omega = 0.3602$, an error of $-0.040$. The bound is $6/(10 \cdot 6 \cdot 35) = 0.002857$, a standard deviation of $0.053$, so this error is typical. The single differences range from $0.02$ to $0.73$, which shows how noisy each one is.

With $N = 32$ and 500 random tones per point (seed 1, $\omega$ uniform in $[-0.5, 0.5]$), the mean square error over the CRB was (measurements):

| SNR | 0 dB | 3 dB | 5 dB | 7 dB | 10 dB | 15 dB | 20 dB |
|---|---|---|---|---|---|---|---|
| MSE/CRB | $185$ | $45$ | $18$ | $5.1$ | $0.99$ | $0.95$ | $0.94$ |

Above about 10 dB the estimator is at the bound; between 5 and 10 dB it leaves it fast. At $N = 32$ and 10 dB the bound is $1.833 \times 10^{-5}$ rad$^2$. A ratio slightly below 1 is sampling error of the measurement, not a violation of the bound.

## Correctness

**Claim.** The weights sum to 1, so without noise $\hat\omega = \omega$ exactly for $|\omega| < \pi$ (theorem). In the high-SNR model, where the phase noise of each sample is $u_t \sim \mathcal{N}(0, \frac{1}{2\,\mathrm{SNR}})$ and no difference wraps, the differences are $d_t = \omega + u_{t+1} - u_t$ with tridiagonal covariance, the weights are the best linear unbiased weights, and the variance is the CRB $\frac{6}{\mathrm{SNR}\,N(N^2-1)}$ (a closed form under assumptions).

**Key steps.** $\sum_{s=1}^{N-1} s(N-s) = N(N^2-1)/6$. For the covariance $C = \operatorname{tridiag}(-1, 2, -1)$, $Cw$ is the negative second difference of $s(N-s)$, which is the constant $2$ times the scale, so $w \propto C^{-1}\mathbf 1$, the generalized least squares weights of the [Gauss-Markov theorem](/gauss-markov-theorem/). Then $\operatorname{var}\hat\omega = \sigma^2 w^\top C w = \frac{12\sigma^2}{N(N^2-1)}$. The tests check the weights against a direct solution of $C x = \mathbf 1$.

## Complexity

$N - 1$ complex products, $N - 1$ angles and $O(N)$ additions: $O(N)$ time in the [real RAM](/real-ram/), with $O(1)$ extra space if the weights are computed on the fly. There is no FFT and no search, which is the main gain over the maximum likelihood periodogram peak.

## Properties

- **Efficient above threshold.** The variance equals the CRB in the high-SNR model, and the measurements at 10 dB and above match it.
- **Threshold set by the per-sample SNR.** Each difference has noise of standard deviation about $1/\sqrt{\mathrm{SNR}}$, whatever $N$ is. A wrap of a single difference adds an error of about $2\pi w_t$. So the threshold does not fall as $N$ grows, unlike the periodogram peak, whose threshold depends on $N\cdot\mathrm{SNR}$ (a rule).
- **Full range.** It estimates any $|\omega| < \pi$, but near $\pm\pi$ the differences wrap more often, so the threshold rises.
- **Unbiased in the model.** In the high-SNR model the estimate is unbiased; with wraps it is pulled toward zero for large $|\omega|$.
- **Not robust to fading.** It assumes a constant amplitude. Deep fades make some differences pure noise.

## Variants and improvements

- **Unweighted mean.** Equal weights give $\frac{1}{N-1}\sum_t d_t$, which, without wraps, is $(\arg r_{N-1} - \arg r_0)/(N-1)$ and uses only two samples: its variance is about $N/6$ times the bound. The tests show it.
- **Linear regression on the unwrapped phase.** Tretter's estimator fits a line to $\arg r_t$ after unwrapping. It has the same high-SNR variance, but needs a correct [phase unwrapping](/phase-unwrapping/).
- **Smoothed or lagged differences.** Averaging $r_{t+1}\overline{r_t}$ over a few terms before the angle, or using differences at lag $m > 1$, lowers the threshold and narrows the range; the [Luise and Reggiannini estimator](/luise-reggiannini-estimator/) and the estimator of Fitz are built this way.
- **Data removal.** For pilots, divide out the known symbols first; for M-PSK, apply Kay to $r_t^M$ and divide by $M$, which reduces the range to $|\omega| < \pi/M$.
- **Relation to linear prediction.** The angle of a one-step prediction coefficient is a related estimator. Kay used the relation between the two to explain why the linear prediction estimator does not reach the bound even at high SNR.

## When to use it

Use Kay's estimator for a fast frequency estimate at moderate to high SNR, for example 10 dB or more per sample for a few tens of samples, when the range must be wide and an FFT is too costly. For low SNR or long blocks, use the periodogram peak or a correlation estimator.

## Pitfalls

- **Running it below threshold.** At 5 dB with $N = 32$ the error was 18 times the bound in the measurement. More samples do not help, because the threshold depends on the per-sample SNR.
- **Leaving the data in.** Modulated symbols turn the phase from sample to sample. Remove them first, by pilots or a power.
- **Large frequencies after an Mth power.** After $r^M$, the frequency is $M\omega$, and it must stay in $(-\pi, \pi)$.
- **Mixing units.** The output is in radians per sample. Divide by $2\pi T$ for hertz.
- **Comparing with the wrong bound.** The CRB $\frac{6}{\mathrm{SNR}\,N(N^2-1)}$ is for unknown phase and amplitude in complex noise. Do not compare with a bound for a known phase or for real signals.

## Implementations

## History

Before Kay, Steven Tretter showed in 1985 that, at high SNR, the phase of a noisy tone is a line plus white Gaussian noise, so linear regression on the unwrapped phase reaches the Cramer-Rao bound, but unwrapping fails easily. Steven Kay published his estimator in 1989 in the IEEE Transactions on Acoustics, Speech, and Signal Processing. He used phase differences, which need no unwrapping, and the weights of the best linear unbiased estimator for their correlated noise, and he explained with the same analysis why the linear prediction estimator does not reach the bound. The estimator is used in burst modem frequency recovery and in measurement instruments, and its threshold behavior led to many variants with smoothed differences.

## References
