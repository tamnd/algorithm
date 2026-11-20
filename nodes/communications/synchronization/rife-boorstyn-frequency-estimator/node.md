---
tag: 749SAD
kind: algorithm
slug: rife-boorstyn-frequency-estimator
name: Rife and Boorstyn frequency estimator
aliases:
- ML single-tone frequency estimation
- periodogram peak frequency estimator
area: communications/synchronization
level: advanced
summary: Finds the maximum likelihood frequency of a tone in noise as the peak of the periodogram, refined by a local search.
solves: [frequency-offset-estimation]
model: real-ram
complexity:
  vars: {N: the number of samples, I: "the number of golden-section steps (about the log of 1/(N times the tolerance))"}
  time: {worst: O(N log N + N I)}
  space: {extra: O(N)}
properties: {deterministic: true, feedforward: true, maximum_likelihood: true, range: "|omega| < pi radians per sample"}
history:
  year: 1974
  people: [David C. Rife, Robert R. Boorstyn]
  note: "David Rife and Robert Boorstyn derived the Cramer-Rao bounds and the maximum likelihood estimator for one tone in discrete-time noise in 1974, and proposed to compute it with an FFT search followed by a fine search. They also analyzed the threshold effect."
prereqs: [frequency-offset-estimation, periodogram, fast-fourier-transform, maximum-likelihood-estimation]
see_also: [kay-frequency-estimator, luise-reggiannini-estimator, cramer-rao-bound, modified-cramer-rao-bound, golden-section-search, discrete-fourier-transform, music-algorithm, esprit]
sources:
  - paper: doi:10.1109/TIT.1974.1055282
    title: "D. C. Rife and R. R. Boorstyn, Single-tone parameter estimation from discrete-time observations, IEEE Transactions on Information Theory 20(5), 1974, pages 591 to 598"
    locator: "the Cramer-Rao bounds for amplitude, phase and frequency, the maximum likelihood estimator as the periodogram peak, the coarse FFT and fine search, and the threshold analysis"
  - book: isbn:9780306457258
    title: "Umberto Mengali and Aldo N. D'Andrea, Synchronization Techniques for Digital Receivers, Plenum Press, 1997"
    locator: "Chapter 3 (carrier frequency recovery with linear modulations, the maximum likelihood data-aided estimator)"
  - book: isbn:9780133457117
    title: "Steven M. Kay, Fundamentals of Statistical Signal Processing, Volume I: Estimation Theory, Prentice Hall, 1993"
    locator: "Chapter 7 (maximum likelihood estimation)"
---

The Rife and Boorstyn estimator finds the frequency of one complex tone in white Gaussian noise by maximum likelihood. With the amplitude and the phase unknown, the likelihood is largest where the [periodogram](/periodogram/) $P(\omega) = \frac1N\bigl|\sum_t r_t e^{-j\omega t}\bigr|^2$ is largest. So the estimator computes a zero-padded [FFT](/fast-fourier-transform/) for a coarse search, then refines the best grid point by a local search, here a [golden-section search](/golden-section-search/). It differs from the plain periodogram, which is a spectral estimate on a fixed grid: the refinement removes the grid error, which at high SNR would otherwise be far larger than the noise error. It is the reference method for [frequency offset estimation](/frequency-offset-estimation/). Above a threshold its variance reaches the [Cramer-Rao bound](/cramer-rao-bound/) $\frac{6}{\mathrm{SNR}\,N(N^2-1)}$, which with known data is the [modified Cramer-Rao bound](/modified-cramer-rao-bound/), and its threshold is the lowest of the common estimators, because it depends on $N \cdot \mathrm{SNR}$. The [Kay estimator](/kay-frequency-estimator/) and the [Luise and Reggiannini estimator](/luise-reggiannini-estimator/) cost less but have higher thresholds or smaller ranges.

## In plain words

The receiver tries many candidate frequencies. For each one, it turns the samples back by that frequency and adds them up. At the right frequency all samples point the same way, and the sum is long. At a wrong frequency they point in different directions and the sum is short. A fast transform checks a fine grid of candidates at once. The receiver then searches near the best candidate, step by step, until the sum is as long as it can be. When the noise is very strong, a random candidate far from the right one can give a longer sum, and the answer is then completely wrong.

## The problem

The input is $r_t = A e^{j(\omega_0 t + \phi)} + w_t$, $t = 0, \ldots, N - 1$, with unknown $A > 0$, $\phi$ and $\omega_0 \in [-\pi, \pi)$, in radians per sample, and $w_t \sim \mathcal{CN}(0, N_0)$ white, $\mathrm{SNR} = A^2/N_0$. In a receiver, $r_t$ is the signal with the known pilot symbols removed. Output the maximum likelihood estimate $\hat\omega$.

## The algorithm

```pseudo id=main
RIFE-BOORSTYN(r[0..N-1], K, tol)              ▷ K >= 4N, a power of two
L1  X <- FFT of r padded with zeros to K points
L2  i* <- the index i with the largest |X[i]|
L3  a <- 2 pi (i* - 1) / K; b <- 2 pi (i* + 1) / K
L4  omega <- golden-section maximizer of P(w) = |sum_t r[t] exp(-j w t)|^2 / N on [a, b], to tol
L5  return omega reduced to [-pi, pi)
```

Line L1 evaluates $X(\omega)$ on the grid $2\pi i/K$. Zero padding to $K \ge 4N$ makes the grid fine enough that the best grid point is in the main lobe of the signal peak. Line L4 evaluates $P$ directly, $O(N)$ per point, about 50 times for a tolerance of $10^{-10}$. Any local search that keeps a bracket works here.

## Example

$N = 8$, $\omega_0 = 1.0$, $\phi = 0.5$, $\mathrm{SNR} = 10$ dB (noise seed 9), $K = 32$. The grid spacing is $2\pi/32 = 0.196$. Line L1 gives these periodogram values near the peak:

| $i$ | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|
| $2\pi i/32$ | $0.589$ | $0.785$ | $0.982$ | $1.178$ | $1.374$ |
| $P$ | $3.162$ | $6.348$ | $7.971$ | $6.759$ | $3.736$ |

Line L2 picks $i^\ast = 5$, and line L3 gives $[0.785, 1.178]$. The golden-section search ends at $\hat\omega = 0.99644$, where $P = 7.980$. The error is $-0.0036$. The grid point alone would have had the error $-0.018$. The bound is a standard deviation of $\sqrt{6/(10 \cdot 8 \cdot 63)} = 0.0345$.

With $N = 32$, 400 random tones per point with $\omega_0$ uniform in $[-3, 3]$ (seed 2), the mean square error over the CRB was (measurements). An outlier is an error larger than $2\pi/N$. The last row uses the grid point of line L2 alone, with $K = 4N = 128$:

| SNR | $-6$ dB | $-3$ dB | 0 dB | 3 dB | 5 dB | 10 dB |
|---|---|---|---|---|---|---|
| MSE/CRB, RB | $481$ | $4.97$ | $1.14$ | $1.10$ | $1.08$ | $1.05$ |
| outliers in 400 | $48$ | $2$ | $0$ | $0$ | $0$ | $0$ |
| MSE/CRB, grid only | $478$ | $5.7$ | $2.2$ | $3.7$ | $4.8$ | $12.1$ |

The threshold is between $-6$ and $-3$ dB for $N = 32$, that is $N \cdot \mathrm{SNR}$ between 9 dB and 12 dB. Above it, the estimate is at the bound. Without the fine search, the grid error dominates and the ratio grows with the SNR.

## Correctness

**Claim.** Minimizing $\sum_t |r_t - b e^{j\omega t}|^2$ over the complex amplitude $b$ leaves $\sum_t |r_t|^2 - N P(\omega)$, so the ML frequency is the maximizer of $P$ (theorem). Without noise, the algorithm returns $\omega_0$ to within the tolerance (theorem). In noise it returns the global maximizer whenever the global peak is within one grid step of the best grid point and $P$ is unimodal there (theorem); that this holds above threshold is a rule, and that the variance there approaches the CRB is a closed form under assumptions.

**Key steps.** Without noise, $P(\omega) = \frac{A^2}{N} D(\omega - \omega_0)^2$, where $D(x) = \frac{\sin(Nx/2)}{\sin(x/2)}$ is the Dirichlet kernel. $|D|$ decreases on $[0, 2\pi/N]$, and it is at most $N/2$ outside the main lobe. With $K \ge 4N$, the nearest grid point has $|D| > 0.97N$, so it is the best one, and the bracket of line L3 stays within $\frac{3\pi}{4N}$ of $\omega_0$, inside the main lobe, where $P$ is unimodal.

## Complexity

The FFT costs $O(K\log K) = O(N\log N)$ for $K = O(N)$. The golden-section search needs $O(\log\frac{1}{N\,\mathrm{tol}})$ evaluations of $P$, each $O(N)$. Space is $O(N)$ for the padded FFT. This is more than the $O(N)$ of the Kay and Luise and Reggiannini estimators, but small in absolute terms.

## Properties

- **Maximum likelihood.** It is the ML estimator for one tone in white Gaussian noise, and it is asymptotically efficient.
- **Lowest threshold.** The threshold depends on $N \cdot \mathrm{SNR}$, so long blocks work at a low per-sample SNR. In the measurement with $N = 32$, it is at the bound from 0 dB, where the Kay estimator is 185 times above it.
- **Full range.** It covers $|\omega| < \pi$, with no reduction of range.
- **Outliers below threshold.** Below threshold, the errors are not larger Gaussian errors but jumps to a random frequency: 48 of 400 trials at $-6$ dB.
- **One tone only.** Several tones or a strong interferer shift the peak or create a false one.

## Variants and improvements

- **Interpolation instead of search.** Fit a parabola, or use the formulas of Quinn, Jacobsen or Macleod, to the three largest FFT values. This is $O(1)$ after the FFT and close to the bound for moderate SNR.
- **Newton or secant refinement.** Find the zero of $P'(\omega)$ near the grid peak, which converges faster than golden-section search when the start is close.
- **Iterated or recursive search.** Repeat a smaller FFT on a narrower band, or use a dichotomous search between two bins.
- **Data removal for M-PSK.** Apply the estimator to $r_t^M$, then divide by $M$, which cuts the range to $|\omega| < \pi/M$ and adds squaring loss.
- **Several tones.** For more than one tone, subspace methods such as [MUSIC](/music-algorithm/) and [ESPRIT](/esprit/) resolve tones that are closer than $2\pi/N$.

## When to use it

Use it when the SNR per sample is low, the block is long, and the full range is needed: initial acquisition of a carrier offset from a preamble, Doppler estimation, or measurement of a tone frequency. At moderate SNR, if cost matters, use the Kay or Luise and Reggiannini estimator.

## Pitfalls

- **No zero padding.** With $K = N$, the best grid point can be in a side lobe or on the wrong side of the peak at bin edges. Pad to at least $4N$ before the local search.
- **Searching from the grid peak only.** Without the fine search, the error is the grid error, up to half a grid step, which at high SNR is far above the bound: 12 times at 10 dB in the measurement.
- **Wrong bracket.** A bracket wider than the main lobe can hold two local maxima, and the golden-section search may end on the wrong one.
- **Data left in the signal.** Modulated symbols spread the tone over the band. Remove them first.
- **Expecting Gaussian errors below threshold.** Below threshold, the mean square error is dominated by a few outliers. Report the outlier rate as well as the MSE.

## Implementations

## History

David Rife and Robert Boorstyn, at Bell Laboratories and New York University, published the estimator in the IEEE Transactions on Information Theory in 1974. They derived the Cramer-Rao bounds for the amplitude, the phase and the frequency of one complex tone in discrete-time white noise, showed that the ML frequency is the periodogram peak, proposed to compute it with a coarse FFT search and a fine search, and analyzed the threshold where outliers start. In 1976 they extended the work to several tones. Their bound and their estimator became the reference for all later fast frequency estimators, such as those of Kay in 1989 and of Luise and Reggiannini in 1995.

## References
