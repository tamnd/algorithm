---
tag: N8KZKA
kind: algorithm
slug: welch-method
name: Welch's method
aliases:
- Welch periodogram
- averaged modified periodogram
area: graphics-and-signals/signal-processing
level: core
summary: "Estimate a power spectral density by cutting the record into overlapping windowed segments and averaging their periodograms. The variance falls about as 1/K, the resolution as 1/M."
solves: [spectral-estimation]
model: real-ram
complexity:
  vars: {N: the number of samples, M: the segment length, D: the hop between segment starts, K: the number of segments, L: the FFT length (at least M)}
  time: {worst: Θ(K L log L), average: Θ(K L log L), best: Θ(K L log L)}
  space: {extra: Θ(L)}
properties: {deterministic: true, nonparametric: true, consistent: true, streaming: true}
history:
  year: 1967
  people: [Peter D. Welch]
  note: Welch proposed averaging FFT periodograms of overlapping windowed segments in 1967, extending the segment averaging that Bartlett introduced in 1948.
prereqs: [periodogram, window-functions]
see_also: [spectral-estimation, power-spectral-density, wiener-khinchin-theorem, short-time-fourier-transform, spectral-leakage, burg-method, fast-fourier-transform, overlap-add-method]
sources:
  - paper: doi:10.1109/TAU.1967.1161901
    title: Peter D. Welch, The use of fast Fourier transform for the estimation of power spectra, a method based on time averaging over short, modified periodograms, IEEE Transactions on Audio and Electroacoustics 15(2), 1967
    locator: pp. 70 to 73 (the averaged modified periodogram, its mean as a window-smoothed spectrum, and its variance with overlapping segments)
  - paper: doi:10.1038/161686a0
    title: M. S. Bartlett, Smoothing periodograms from time-series with continuous spectra, Nature 161(4096), 1948
    locator: pp. 686 to 687 (averaging the periodograms of nonoverlapping segments to reduce the variance)
  - book: isbn:9780131139565
    title: Petre Stoica and Randolph L. Moses, Spectral Analysis of Signals, Pearson Prentice Hall, 2005
    locator: Section 2.7.1 (Bartlett's method) and Section 2.7.2 (Welch's method, with 50 percent overlap recommended)
  - paper: doi:10.1109/PROC.1978.10837
    title: Fredric J. Harris, On the use of windows for harmonic analysis with the discrete Fourier transform, Proceedings of the IEEE 66(1), 1978
    locator: pp. 51 to 83 (the overlap correlation of each window at 50 and 75 percent overlap, in the table of window figures of merit)
---

Welch's method estimates the [power spectral density](/power-spectral-density/) of a stationary signal by cutting the record into $K$ segments of length $M$ that start every $D$ samples, multiplying each by a window, computing the [periodogram](/periodogram/) of each, and averaging. A single periodogram has a variance as large as the square of its mean, however long the record. Averaging $K$ of them divides the variance by about $K$, at the price of the resolution of a segment, about $2\pi/M$ radians per sample in place of $2\pi/N$. Bartlett's method is the case of no overlap and no window. With a Hann window and 50 percent overlap it is the default spectrum estimator of most software, and the standard nonparametric answer to [spectral estimation](/spectral-estimation/).

## In plain words

One periodogram of a noisy record is jagged, and a longer record does not make it smoother. So cut the record into many short pieces, compute the jagged picture of each piece, and average the pictures. The jags are random and partly cancel; the true shape stays. With 30 pieces the wobble is about five times smaller. The price is detail: each piece is short, so two close tones that a long record could separate now blur into one. Overlapping the pieces by half gives you almost twice as many pieces from the same record.

## The problem

Given a record $x[0], \dots, x[N-1]$ of a zero-mean wide-sense stationary process sampled at the rate $f_s$, estimate its power spectral density $S(\omega)$, $\omega$ in radians per sample, on the grid $\omega_b = 2\pi b / L$, which is $b f_s / L$ Hz. The [spectral estimation](/spectral-estimation/) page states the problem and its other solutions.

## The algorithm

The parameters are the segment length $M \le N$, the hop $1 \le D \le M$ (the overlap is $M - D$ samples), a window $w[0], \dots, w[M-1]$ and the FFT length $L \ge M$, a power of two.

```pseudo id=main
WELCH(x[0 .. N − 1], M, D, w[0 .. M − 1], L)     ▷ 1 ≤ M ≤ N, 1 ≤ D ≤ M, L ≥ M
L1  K ← ⌊(N − M) / D⌋ + 1                         ▷ number of full segments
L2  U ← (1/M) · Σ_{t<M} w[t]²                     ▷ window power
L3  for b ← 0 to L − 1 do S[b] ← 0
L4  for i ← 0 to K − 1 do
L5      a ← (w[t] · x[iD + t] for t < M, then L − M zeros)
L6      A ← FFT_L(a)
L7      for b ← 0 to L − 1 do S[b] ← S[b] + |A[b]|² / (M·U)
L8  for b ← 0 to L − 1 do S[b] ← S[b] / K
L9  return S
```

Line L1 counts the segments that fit; samples after the last full segment are dropped, so choose $N - M$ divisible by $D$ or pad. Line L5 takes segment $i$ and applies the window, and lines L6 and L7 add its modified periodogram. The factor $1/(MU)$ makes each segment periodogram have mean $\sigma^2$ on white noise of variance $\sigma^2$, for any window. Line L8 turns the sum into an average. The loop of line L4 needs only one segment in memory at a time, so the method runs on a stream: keep a running sum and a count.

**Bartlett's method** is $D = M$ with the rectangular window $w = 1$: disjoint segments and plain periodograms.

## Example

Take $y = (2, 1, 0, -1, 1, 3, -2, 0)$, $N = 8$, $M = 4$, $D = 2$, the rectangular window and $L = 4$, so $K = \lfloor 4/2 \rfloor + 1 = 3$. The bins are $\omega = 0, \pi/2, \pi, -\pi/2$. The implementation computes the same values, and a brute force over the defining sums agrees.

| segment $i$ | samples $y[2i .. 2i+3]$ | DFT $A[0], A[1], A[2], A[3]$ | periodogram $|A[b]|^2/4$ |
|---|---|---|---|
| 0 | $2, 1, 0, -1$ | $2,\ 2 - 2i,\ 2,\ 2 + 2i$ | $1,\ 2,\ 1,\ 2$ |
| 1 | $0, -1, 1, 3$ | $3,\ -1 + 4i,\ -1,\ -1 - 4i$ | $9/4,\ 17/4,\ 1/4,\ 17/4$ |
| 2 | $1, 3, -2, 0$ | $2,\ 3 - 3i,\ -4,\ 3 + 3i$ | $1,\ 9/2,\ 4,\ 9/2$ |
| average | | | $17/12,\ 43/12,\ 7/4,\ 43/12$ |

The three segment estimates of bin 2 range from $1/4$ to $4$; the average is $7/4$. On real noise this spread is what averaging reduces.

## Correctness

The loop of line L4 keeps the invariant that, before iteration $i$, $S[b]$ is the sum of the modified periodograms of segments $0$ to $i - 1$ at bin $b$. So line L8 returns their average. Each segment of a WSS process has the same law, so the mean of the estimate is the mean of one segment periodogram: the true spectrum smoothed by the kernel $|W(\omega)|^2/(MU)$ of the window, with a main lobe of width about $4\pi/M$ for the rectangle and $8\pi/M$ for the Hann window. For Bartlett's method on real white Gaussian noise of variance $\sigma^2$, at bins $0 < b < M/2$ with $L = M$, the segment periodograms are independent exponentials, so $\operatorname{Var}\hat S = \sigma^4/K$ exactly. With overlap, for circular complex Gaussian white noise, $\operatorname{Var}\hat S = \frac{\sigma^4}{K}\left(1 + 2\sum_{j \ge 1}(1 - j/K)\rho_j\right)$ with the overlap correlations $\rho_j$ of the window. The full proof is below.

## Complexity

**Time.** Line L2 is $M$ multiplies. Each iteration of line L4 does $M$ multiplies in line L5, $\frac{L}{2}\log_2 L$ complex multiplies in line L6 and $L$ squared magnitudes in line L7. So the total is $\Theta(K L \log L)$ in the real-RAM model. With $L = M$ and $D = M/2$, $K \approx 2N/M$ and the cost is $\Theta(N \log M)$: about $\log_2 M + 2$ complex multiplies per input sample. Bartlett's method ($D = M$) costs half as much.

**Space.** One padded segment, its transform and the $L$ running sums: $\Theta(L)$. The record itself can be read as a stream.

## Properties

- **Consistent.** With $M$ fixed and $N \to \infty$, $K \to \infty$ and the variance goes to $0$, but the mean stays the smoothed spectrum. If also $M \to \infty$ with $M/N \to 0$, the bias goes to $0$ too, and the estimate converges to $S(\omega)$ at each $\omega$ where $S$ is continuous.
- **The trade-off.** Resolution is about $2\pi/M$ (times a window factor), and the variance is about $S^2/K_{\mathrm{eff}}$. For a fixed $N$, a larger $M$ means fewer segments, so the two cannot both improve. Their product is fixed by $N$.
- **Overlap.** For the Hann window, $\sum_t w[t]\,w[t + M/2] / \sum_t w[t]^2 = 1/6$ at 50 percent overlap, so $\rho_1 = 1/36$ and the extra variance is small, while $K$ almost doubles. Harris lists this overlap correlation as 16.7 percent. At 75 percent overlap the correlation is larger and the gain from the extra segments is small.
- **Unbiased on white noise.** The normalization by $U$ gives mean exactly $\sigma^2$ for every window.

**Measured variance.** On real white Gaussian noise of variance 1, with seeds 6000 to 6199 (one record per seed), the sample variance of the estimate at $\omega = \pi/2$ was:

| $N$ | Welch, $M = 64$, $D = 32$, Hann: $K$, variance, formula | Bartlett, $M = 64$: $K$, variance, $1/K$ | raw periodogram |
|---|---|---|---|
| 256 | 7, 0.115, 0.150 | 4, 0.237, 0.250 | 1.227 |
| 1024 | 31, 0.0296, 0.0340 | 16, 0.0548, 0.0625 | 0.888 |
| 4096 | 127, 0.0069, 0.0083 | 64, 0.0148, 0.0156 | not computed |

The Welch and Bartlett variances fall by about 4 each time $N$ grows by 4; the raw periodogram stays near $1$. The standard error of a variance from 200 records is about 10 percent of its value, and these three Welch rows share their seeds, so their errors are correlated. A rerun at $N = 256$ with 2000 records (seeds 20000 to 21999) gave $0.1555$ against the formula $0.1497$.

## Variants and improvements

- **Bartlett's method.** $D = M$, rectangular window: the variance is exactly $\sigma^4/K$ on white Gaussian noise, and no work is spent on overlaps.
- **Window and overlap choices.** Hann with 50 percent overlap is the common default; a window with lower side lobes (Blackman-Harris, Kaiser) helps when the dynamic range is large, and needs more overlap to use all the data. See [window functions](/window-functions/).
- **Median averaging.** Replacing the mean in line L8 by a median, with a bias correction, resists bursts and transients in some segments.
- **Cross spectra and coherence.** Replacing $|A_i|^2$ by $A_i\overline{B_i}$ for two signals estimates the cross power spectral density; dividing by the two auto spectra gives the coherence, which is $1$ for every single segment and becomes meaningful only after averaging.
- **The spectrogram.** Keeping the segment periodograms instead of averaging them is the [short-time Fourier transform](/short-time-fourier-transform/) magnitude, a time-frequency picture of a nonstationary signal.
- **Multitaper and Blackman-Tukey.** Multitaper averages over orthogonal tapers of the full record instead of over segments; Blackman-Tukey smooths in frequency through a lag window. Both reach a similar trade-off between variance and resolution.

## When to use it

Use Welch's method to measure the level and shape of a broadband spectrum, a noise floor, or a transfer function and coherence, when the record is long compared with the resolution you need. It is fast, streams, and has a known variance. When the record is short and the signal is a few close tones, it cannot resolve them; a parametric method such as the [Burg method](/burg-method/) or a subspace method such as [MUSIC](/music-algorithm/) can do better if its model holds. When the signal changes over the record, look at the segments separately (a spectrogram) instead of averaging them.

## Pitfalls

- **Dropping $U$ in line L7.** Without it, a Hann-windowed estimate is too low by $U = 3/8$, about $-4.3$ dB. Divide by $M \cdot U$ for a density; for the power of a sinusoid read off a peak, the right normalization is by $(\sum_t w[t])^2$ instead.
- **Using $N$ instead of $M$ in line L7.** Each segment periodogram is normalized by its own length. Dividing by $N$ makes the level depend on $K$.
- **Counting the segments wrongly in line L1.** $K$ is $\lfloor (N - M)/D \rfloor + 1$, not $N/D$. Taking $N/D$ segments reads past the end of the record or averages a short last segment with a different normalization.
- **Expecting a large overlap to keep reducing the variance.** Past about 50 percent for Hann, successive segment periodograms are strongly correlated, and the effective number of segments grows much more slowly than $K$, while the work grows as $K$.
- **Not removing the mean.** A constant offset puts a spike at bin 0 in every segment, and the window leaks it into the low bins.

## Implementations

## History

M. S. Bartlett showed in 1948 that splitting a record into nonoverlapping pieces and averaging their periodograms gives a spectrum estimate with a variance that falls with the number of pieces. In the decade before the FFT, Blackman and Tukey's lag-window method was the practical standard, because it worked from a short autocorrelation. Peter Welch's paper of 1967 combined Bartlett's averaging with data windows, overlapping segments and the new FFT, and computed the variance of the result; the FFT made the direct approach cheaper than the autocorrelation route.

## References
