---
tag: 6S1Y6B
kind: algorithm
slug: periodogram
name: Periodogram
aliases:
- raw periodogram
area: graphics-and-signals/signal-processing
level: core
summary: "Estimate the power spectral density of a record as |DFT|^2 / N on a grid of frequencies. Fast and simple, but its variance does not shrink as the record grows."
solves: [spectral-estimation]
model: real-ram
complexity:
  vars: {N: the number of samples in the record, L: the number of frequency bins (at least N)}
  time: {worst: Θ(L log L), average: Θ(L log L), best: Θ(L log L)}
  space: {extra: Θ(L)}
properties: {deterministic: true, nonparametric: true, consistent: false, asymptotically_unbiased: true}
history:
  year: 1898
  people: [Arthur Schuster]
  note: Schuster introduced the periodogram in 1898 to search for hidden periodicities in meteorological and magnetic records.
prereqs: [power-spectral-density, discrete-fourier-transform, fast-fourier-transform]
see_also: [welch-method, wiener-khinchin-theorem, window-functions, spectral-leakage, burg-method, music-algorithm, short-time-fourier-transform, autocorrelation]
sources:
  - paper: doi:10.1029/TM003i001p00013
    title: Arthur Schuster, On the investigation of hidden periodicities with application to a supposed 26 day period of meteorological phenomena, Terrestrial Magnetism 3(1), 1898
    locator: pp. 13 to 41 (the squared Fourier sums of a record as a test for a period)
  - book: isbn:9780131139565
    title: Petre Stoica and Randolph L. Moses, Spectral Analysis of Signals, Pearson Prentice Hall, 2005
    locator: Section 2.2 (the periodogram and the correlogram and their equality), Section 2.4 (bias, the Fejér window, resolution, and the variance that does not decay), and Section 4.9.3 (the periodogram as a detector of sinusoids)
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 10.5 (Fourier analysis of stationary random signals, the periodogram, its mean and variance, and the use of the DFT to compute it)
  - paper: doi:10.1109/PROC.1978.10837
    title: Fredric J. Harris, On the use of windows for harmonic analysis with the discrete Fourier transform, Proceedings of the IEEE 66(1), 1978
    locator: pp. 51 to 83 (leakage, the windowed periodogram and the tables of window figures of merit)
---

The periodogram estimates the [power spectral density](/power-spectral-density/) of a stationary signal from one record of $N$ samples. It takes the DFT of the record, squares the magnitude of each bin and divides by $N$: $P(\omega_m) = \frac{1}{N}|X(\omega_m)|^2$. With the [FFT](/fast-fourier-transform/) it costs $O(L \log L)$ operations for $L$ bins, and its mean tends to the true spectrum. But it is not consistent. On white Gaussian noise each bin is an exponential random variable whose standard deviation equals its mean, for every $N$, so a longer record gives more bins and not less noise. It is the base case of [spectral estimation](/spectral-estimation/), and the [Welch method](/welch-method/) averages it to reduce the variance.

## In plain words

Split a recording into pure tones with the Fourier transform, and look at the strength of each tone, squared. That is the periodogram. A loud hum shows up as a tall spike at its frequency. The problem is noise. For random noise the picture is a jagged comb, and recording for longer does not smooth it: you get more teeth, each as jagged as before. So the periodogram is good for finding strong tones and poor for measuring the smooth shape of a noise spectrum. To smooth it you must average, which costs resolution.

## The problem

Given a record $x[0], \dots, x[N-1]$ of a zero-mean wide-sense stationary process with sampling rate $f_s$, estimate its power spectral density $S(\omega)$, with $\omega$ in radians per sample, on the grid $\omega_m = 2\pi m / L$, $m = 0, \dots, L-1$. Bin $m$ is the frequency $m f_s / L$ Hz, read as $(m - L) f_s/L$ for $m \ge L/2$. The general problem and the other estimators are on the [spectral estimation](/spectral-estimation/) page.

## The algorithm

The input is the record, a grid size $L \ge N$ and an optional window $w[0], \dots, w[N-1]$; the rectangular window $w[n] = 1$ gives the raw periodogram.

```pseudo id=main
PERIODOGRAM(x[0 .. N − 1], L, w[0 .. N − 1])     ▷ L ≥ N; w = 1 for the raw periodogram
L1  N ← length of x; require L ≥ N
L2  U ← (1/N) · Σ_{n<N} w[n]²                    ▷ window power; U = 1 for w = 1
L3  a ← (w[0]x[0], …, w[N−1]x[N−1], 0, …, 0)     ▷ zero padding to length L
L4  A ← DFT_L(a)                                 ▷ an FFT when L is a power of two
L5  for m ← 0 to L − 1 do P[m] ← |A[m]|² / (N·U)
L6  return P                                     ▷ P[m] estimates S(2πm/L)
```

Line L3 applies the window and pads the record with zeros. Padding does not add information: it samples the same function $\frac{1}{NU}|\sum_n w[n]x[n]e^{-i\omega n}|^2$ on a finer grid. Line L4 is one DFT. Line L5 squares each bin. The factor $1/(NU)$ makes the mean of the estimate equal to $\sigma^2$ on white noise of variance $\sigma^2$, for every window, so windowed and raw periodograms have the same scale. With a window other than the rectangle the result is called the *modified periodogram*.

## Example

Take the square wave $x = (1, 1, 1, 1, -1, -1, -1, -1)$, $N = 8$, the raw periodogram and $L = 8$ and $L = 16$. The implementation on this page produces these values; the closed forms come from $X(\omega) = (1 - e^{-4i\omega})\sum_{n<4} e^{-i\omega n}$.

| bin $m$ ($L = 8$) | $\omega_m$ | $P[m]$ | value |
|---|---|---|---|
| 0 | 0 | $0$ | 0 |
| 1 | $\pi/4$ | $2 + \sqrt{2}$ | 3.4142 |
| 2 | $\pi/2$ | $0$ | 0 |
| 3 | $3\pi/4$ | $2 - \sqrt{2}$ | 0.5858 |
| 4 | $\pi$ | $0$ | 0 |
| 5, 6, 7 | $-3\pi/4, -\pi/2, -\pi/4$ | mirror of bins 3, 2, 1 | 0.5858, 0, 3.4142 |

The even bins are zero because a square wave of period 8 has only odd harmonics. The mean of the eight values is $8/8 = 1$, which is the sample power $\frac{1}{8}\sum x[n]^2$, as [Parseval's theorem](/parsevals-theorem/) requires. With $L = 16$ the even bins repeat the $L = 8$ values and the odd bins show the curve between them: bin 1, at $\omega = \pi/8$, is $1/(8\sin^2(\pi/16)) \approx 3.2843$, and bins 3, 5 and 7 are $0.4050$, $0.1808$ and $0.1299$. The record has only 8 samples, so the main lobe has width $4\pi/8$ whatever $L$ is.

## Correctness

Line L4 computes $A[m] = \sum_{n<N} w[n]x[n] e^{-i\omega_m n}$ because the padded samples are zero, so line L5 returns the defined estimate at each bin. The statistical claims are proved in the proof file. For a WSS process with the rectangular window, $\mathbb{E}\,P(\omega) = \sum_{|k|<N}(1 - |k|/N)\, r[k]\, e^{-i\omega k}$, which tends to $S(\omega)$ when $\sum |r[k]| < \infty$ (the [Wiener-Khinchin theorem](/wiener-khinchin-theorem/)). For white Gaussian noise of variance $\sigma^2$, at each bin $0 < m < N/2$ with $L = N$, $P[m]/\sigma^2$ has the exponential law with mean 1, so $\operatorname{Var} P[m] = \sigma^4$ for every $N$, and distinct bins are independent. At $m = 0$ and $m = N/2$ the variance is $2\sigma^4$.

## Complexity

**Time.** Line L2 is $N$ multiplies and L3 is $N$ more. Line L4 with a radix-2 FFT is $\frac{L}{2}\log_2 L$ complex multiplies; line L5 is $L$ squared magnitudes. So the total is $\Theta(L \log L)$ in the real-RAM model, since $L \ge N$. A direct DFT of a length that is not a power of two costs $\Theta(L^2)$, which the implementation uses as its fallback; Bluestein's method restores $O(L \log L)$ for any $L$. Per bin, the FFT path costs about $\frac{1}{2}\log_2 L + 1$ complex multiplies.

**Space.** The padded array and its transform: $\Theta(L)$ numbers.

**A single bin.** When only a few frequencies are wanted, the direct sum (or the Goertzel recursion) costs $N$ multiplies per bin, which is cheaper than an FFT for fewer than about $\log_2 L$ bins.

## Properties

- **Unbiased in the limit, biased at finite $N$.** The mean is the true spectrum convolved with the Fejér kernel $F_N(\omega) = \frac{1}{N}\sin^2(N\omega/2)/\sin^2(\omega/2)$. Peaks are smeared over a main lobe of width $4\pi/N$, and power leaks into side lobes that fall only like $1/\omega^2$; see [spectral leakage](/spectral-leakage/).
- **Resolution.** Two tones closer than about $2\pi/N$ radians per sample, that is $f_s/N$ Hz, merge into one peak. Zero padding (a larger $L$) does not change this.
- **Not consistent.** The variance at an interior bin is $S(\omega)^2$ for Gaussian white noise. Measured: for $\sigma = 1$, one record per seed, seeds 5000 to 5299, the sample variance of $P$ at bin $N/4$ was $0.800$, $1.168$ and $0.933$ for $N = 64$, $256$ and $1024$, with means $0.911$, $1.008$ and $1.055$. The theory says $1$ and $1$ for each $N$, and the standard error of a variance from 300 exponential values is about $0.16$. A consistent estimator with variance proportional to $1/N$ would have dropped by the factor 16.
- **Exponential law.** Over 2000 records with $N = 32$ (seed 4404), $P$ at bin 5 exceeded $\sigma^2 = 1$ in a fraction $0.360$ of the records, against $e^{-1} \approx 0.368$.
- **Scale.** The mean of $P$ over the full grid of $L \ge N$ bins is $\frac{1}{N}\sum |x[n]|^2$, exactly.
- **Equals the correlogram.** $P(\omega) = \sum_{|k|<N} \hat r[k] e^{-i\omega k}$ with the biased sample [autocorrelation](/autocorrelation/) $\hat r$; the two are one estimator computed two ways.

## Variants and improvements

- **Modified periodogram.** A taper $w$ (Hann, Hamming, Blackman, Kaiser; see [window functions](/window-functions/)) lowers the side lobes at the cost of a wider main lobe. Measured on a cosine at $8.5$ cycles per 64 samples, the leakage 12 bins away from the peak, relative to the peak bin, was $-23.5$ dB with the rectangle and $-71.9$ dB with the periodic Hann window.
- **Bartlett and Welch.** Split the record into $K$ segments, compute a modified periodogram of each and average. The variance drops by about $K$ and the resolution falls to that of one segment. This is the [Welch method](/welch-method/).
- **Blackman-Tukey.** Multiply the biased autocorrelation by a lag window before the transform. This smooths the periodogram in frequency and is the dual of segment averaging.
- **Multitaper.** Average periodograms of the full record computed with several orthogonal tapers (the Slepian sequences), which reduces the variance without cutting the record.
- **Lomb-Scargle.** A least-squares fit of a sinusoid at each frequency, for samples at uneven times.
- **Parametric and subspace methods.** The [Burg method](/burg-method/) fits an AR model, and [MUSIC](/music-algorithm/) and [ESPRIT](/esprit/) estimate the frequencies of a few tones. Both can resolve tones closer than $2\pi/N$ when their models hold.

## When to use it

Use the raw periodogram to find strong narrowband tones in a record, to see the shape of a spectrum at a glance, or as the inner step of a better estimator. Its peaks are at the right places, and its cost is one FFT. Use a taper when a weak tone may hide near a strong one. Do not use one raw periodogram to measure the level of a noise floor or a smooth spectrum: average segments (Welch), smooth across frequency, or use multitapers. For a few closely spaced tones in noise with a short record, a model-based method can resolve what the periodogram cannot.

## Pitfalls

- **Dividing by the wrong constant.** Line L5 divides by $N \cdot U$. Dividing by $L$ (the padded length) makes zero padding change the level of the spectrum, and dropping $U$ makes a Hann-windowed estimate too low by the factor $U = 3/8$.
- **Reading the noise as structure.** A single bin of white noise exceeds $3$ times its mean with probability $e^{-3} \approx 0.05$. A 1024-point periodogram of real noise has 511 independent interior bins, so about 25 of them are such peaks. Line L6 returns a random curve; compare a peak against this exponential law before calling it a tone.
- **Thinking that padding adds resolution.** Line L3 can pad to any $L$, but the main lobe width stays $4\pi/N$. Only a longer record narrows it.
- **Forgetting the mean.** A nonzero mean puts a large spike at bin 0 that leaks into its neighbours. Subtract the sample mean before line L3.
- **Mixing one-sided and two-sided scales.** For a real signal the bins $m$ and $L - m$ are equal. A one-sided plot on $[0, f_s/2]$ doubles every bin except $0$ and $L/2$; state which form a plot uses.

## Implementations

## History

Arthur Schuster introduced the periodogram in 1898 to test whether meteorological records contained a 26-day period; Stoica and Moses credit the name to his work of 1900. The method was used through the first half of the twentieth century to search for hidden periods, with disappointing results on noisy data, because the erratic behaviour that claim 3 describes was not understood. Maurice Bartlett showed in 1948 that averaging periodograms of segments reduces the variance, and Blackman and Tukey based spectrum analysis on lag-windowed autocorrelations in the 1950s. After the FFT of Cooley and Tukey in 1965, Welch returned in 1967 to averaging periodograms directly, which made the FFT-based periodogram the standard first step of spectral analysis.

## References
