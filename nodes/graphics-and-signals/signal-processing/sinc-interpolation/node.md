---
tag: CYHRAN
kind: algorithm
slug: sinc-interpolation
name: Sinc interpolation
aliases:
- Whittaker-Shannon interpolation
- bandlimited interpolation
- cardinal series interpolation
area: graphics-and-signals/signal-processing
level: core
summary: "Rebuild a band-limited signal between its samples as the sum of x[n] sinc(t/T - n); exact at the samples, and the truncation error of N terms falls like 1/N."
solves: [signal-reconstruction]
model: real-ram
complexity:
  vars: {N: number of samples in the window, M: number of output times}
  time: {worst: Θ(N M), average: Θ(N M), best: Θ(N M)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1915
  people: [Edmund Taylor Whittaker, Vladimir Kotelnikov, Claude Shannon]
  note: Whittaker introduced the cardinal series in 1915; Kotelnikov in 1933 and Shannon in 1949 proved that it rebuilds every band-limited signal from its samples.
prereqs: [sampling-theorem]
see_also: [reconstruction-filter, trigonometric-interpolation, sample-rate-conversion, polyphase-resampling, image-resampling, sinc-quadrature, lebesgue-constant, gibbs-phenomenon]
sources:
  - paper: doi:10.1017/S0370164600017806
    title: Edmund Taylor Whittaker, On the Functions which are Represented by the Expansions of the Interpolation-Theory, Proceedings of the Royal Society of Edinburgh 35, 1915
    locator: pp. 181 to 194 (the cardinal function through equally spaced values)
  - paper: doi:10.1109/JRPROC.1949.232969
    title: Claude E. Shannon, Communication in the Presence of Noise, Proceedings of the IRE 37(1), 1949
    locator: Section II, The Sampling Theorem (the series of sin x / x pulses that rebuilds the signal, pp. 11 to 12)
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 4, Sampling of Continuous-Time Signals (reconstruction of a band-limited signal from its samples with the ideal reconstruction filter, and the ideal discrete-to-continuous converter)
  - paper: doi:10.1109/5.843002
    title: Michael Unser, Sampling, 50 Years After Shannon, Proceedings of the IEEE 88(4), 2000
    locator: pp. 569 to 587 (the sinc series as an orthogonal projection, its slow decay, and spline and other short kernels as replacements)
  - url: https://ccrma.stanford.edu/~jos/resample/
    title: Julius O. Smith III, Digital Audio Resampling Home Page, CCRMA, Stanford University
    locator: the description of bandlimited interpolation with a windowed sinc stored in a table, as used for audio sample-rate conversion
---

Sinc interpolation rebuilds a continuous signal from its samples $x[n] = x(nT)$ as the sum $x(t) = \sum_n x[n]\, \mathrm{sinc}(t/T - n)$, where $\mathrm{sinc}(u) = \sin(\pi u)/(\pi u)$. By the [sampling theorem](/sampling-theorem/) the full series gives the signal exactly when its spectrum lies below half the sampling rate; this is the ideal solution of [signal reconstruction](/signal-reconstruction/). In practice only $N$ samples are available, and the cost is $\Theta(N)$ per output time. The truncated series is still exact at the sample times, but between them it converges slowly: for typical samples, which decay like $1/n$, the error falls only like $1/N$.

## In plain words

Each sample is replaced by a wave shape, the sinc, which has the value one at its own sample time, zero at every other sample time, and small ripples in between. The shapes are scaled by the sample values and added up. At a sample time only one shape is nonzero, so the sum passes exactly through the samples. Between samples every shape adds a little. When the signal has no fast parts, this sum is not just a smooth curve through the points but the true signal. The ripples of each shape fade out slowly, so far samples still matter, and stopping the sum early leaves a noticeable error.

## The problem

Given the sampling period $T > 0$ (the rate is $f_s = 1/T$), samples $x[n_0], \ldots, x[n_0 + N - 1]$ of a signal $x(t)$ taken at the times $nT$, and a time $t$, compute

$$S(t) = \sum_{n = n_0}^{n_0 + N - 1} x[n]\, \mathrm{sinc}\!\left(\frac{t}{T} - n\right).$$

This is the cardinal series with the samples outside the window set to zero. If $x$ has finite energy and its spectrum is zero outside $|f| \le f_s/2$, then $S(t) \to x(t)$ uniformly as the window grows to all of $\mathbb{Z}$, by the sampling theorem. Time is in seconds and frequency in Hz.

## The algorithm

The algorithm evaluates the sum term by term. It handles a time on the sample grid separately, since there the formula has the form $0/0$ in one term.

```pseudo id=main
SINC-INTERPOLATE(x, n0, T, t)        ▷ x[j] is the sample at time (n0 + j) T, for j = 0 .. N − 1
L1  u ← t / T
L2  if u is an integer and n0 ≤ u < n0 + N then return x[u − n0]
L3  s ← 0
L4  for j ← 0 to N − 1 do
L5      v ← u − (n0 + j)
L6      s ← s + x[j] · sin(π v) / (π v)
L7  return s
```

Line L1 puts the time in units of the sample period. At a sample time inside the window, line L2 returns the sample itself: every other term of the series is a multiple of $\sin(\pi k)$ for a nonzero integer $k$, which is zero. Otherwise $v$ is never zero, and lines L4 to L6 add the $N$ terms. At an integer $u$ outside the window every term is zero, and the loop returns $0$ up to rounding.

## Example

Take $T = 1$ and the signal $x(t) = \mathrm{sinc}(t - 1/2)$, a sinc pulse centred halfway between two samples. Its spectrum is $e^{-i\pi f}$ for $|f| < 1/2$ and zero outside, so it is band-limited to the edge of the baseband and has finite energy. Its samples are $x[n] = \mathrm{sinc}(n - 1/2) = (-1)^{n+1}/(\pi(n - 1/2))$:

| $n$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
|---|---|---|---|---|---|---|
| $x[n]$ | $0.1273$ | $-0.2122$ | $0.6366$ | $0.6366$ | $-0.2122$ | $0.1273$ |

They decay only like $1/n$. Evaluate at $t = 1/2$, where $x(1/2) = 1$, with the window $-N \le n \le N$. For $N = 1$ the three terms are $(-0.2122)(-0.2122) + 0.6366 \cdot 0.6366 + 0.6366 \cdot 0.6366 = 0.8556$. Evaluated by the code with more terms:

| $N$ | $S(1/2)$ | error $1 - S(1/2)$ | $N \times$ error |
|---|---|---|---|
| $1$ | $0.855601$ | $0.144399$ | $0.1444$ |
| $10$ | $0.980672$ | $0.019328$ | $0.1933$ |
| $100$ | $0.997984$ | $0.002016$ | $0.2016$ |
| $1000$ | $0.999797$ | $0.000203$ | $0.2025$ |

The last column tends to $2/\pi^2 \approx 0.20264$, the constant that the bound in the next section predicts. At each integer time $t = n$ the truncated series returns $x[n]$ exactly, whatever $N$ is.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). Line L2 and the loop of lines L4 to L6 compute exactly the truncated sum $S(t)$, with no division by zero. As the window grows, $S(t) \to x(t)$ for every band-limited signal of finite energy, uniformly in $t$, by the [sampling theorem](/sampling-theorem/). For a finite window $W$ the error obeys

$$|x(t) - S(t)| \le \Big(\sum_{n \notin W} |x[n]|^2\Big)^{1/2} \Big(\sum_{n \notin W} \mathrm{sinc}^2(t/T - n)\Big)^{1/2} \le \Big(\sum_{n \notin W} |x[n]|^2\Big)^{1/2},$$

because $\sum_{n \in \mathbb{Z}} \mathrm{sinc}^2(u - n) = 1$ for every real $u$. If $|x[n]| \le C/|n|$ and $W = \{-N, \ldots, N\}$, both factors are of order $N^{-1/2}$ for a fixed $t$, so the error is $O(1/N)$. For the example above the bound is asymptotically equal to the measured error, $2/(\pi^2 N)$ at $t = 1/2$.

## Complexity

Lines L4 to L6 run $N$ times, with one sine and one division each, so one output time costs $\Theta(N)$ and $M$ output times cost $\Theta(NM)$. The extra space is $\Theta(1)$. The cost does not depend on the values, so worst, average and best cases are equal.

When the output times are equally spaced with a step that is a rational multiple of $T$, the computation is a discrete convolution with a fixed set of sinc values and can be done with the [FFT](/fast-fourier-transform/) in $O((N + M)\log(N + M))$ time. The variant with one sine per output time (below) removes the sine from the loop. A windowed kernel of $K$ taps cuts the cost to $\Theta(KM)$, at the price of a small, controlled error.

## Properties

- **Interpolating.** $S(nT) = x[n]$ for every $n$ in the window, for any samples.
- **Linear and shift-invariant on the grid.** $S$ depends linearly on the samples, and shifting the samples by $k$ shifts $S$ by $kT$.
- **Exact for band-limited signals.** With all samples, the output is the unique signal of finite energy with spectrum in $[-f_s/2, f_s/2]$ that has the given samples; it is the orthogonal projection of $x$ onto that space.
- **Not local and not causal.** Every output depends on every sample, including future ones, and the influence of a sample at distance $d$ falls only like $1/d$.
- **Ringing.** At a jump in the samples the series overshoots and ripples on both sides, because it is the ideal low-pass filter in disguise; the size of the overshoot is the subject of [reconstruction filter](/reconstruction-filter/) and of the [Gibbs phenomenon](/gibbs-phenomenon/).
- **Slow convergence.** For samples of order $1/n$ the truncation error is of order $1/N$. For bounded samples that do not decay, the output can grow like $\frac{2}{\pi}(\ln N + \gamma + 2\ln 2)$ at $t = T/2$, where $\gamma$ is Euler's constant: with all signs chosen to match those of $\mathrm{sinc}(1/2 - n)$, the values for $N = 100, 1000, 10000$ agree with this formula to within $0.01$.

## Variants and improvements

- **One sine per output.** Since $\sin(\pi(u - n)) = (-1)^n \sin(\pi u)$, the sum equals $\frac{\sin(\pi u)}{\pi}\sum_n \frac{(-1)^n x[n]}{u - n}$. This needs one sine and $N$ divisions per output; to keep $\sin(\pi u)$ accurate for large $u$, reduce $u$ modulo $2$ first.
- **Windowed sinc.** Multiplying the sinc by a window of finite length, such as the Lanczos, Kaiser or Blackman window, gives a kernel of $K$ taps with a fast-decaying error. The kernels and their trade-offs are on [reconstruction filter](/reconstruction-filter/) and [window functions](/window-functions/).
- **Oversampled kernels.** When $f_s$ is above twice the band, any kernel whose spectrum is flat on the band and zero above $f_s - B$ also reconstructs exactly, and smooth such kernels decay faster than any power of $t$ (see the [sampling theorem](/sampling-theorem/)).
- **Periodic signals.** For $N$ samples of a periodic band-limited signal, the infinite sum folds into a finite one with the periodic sinc (Dirichlet) kernel, and is computed exactly by [trigonometric interpolation](/trigonometric-interpolation/), for example by zero padding the DFT.
- **Resampling tables.** Audio [sample-rate conversion](/sample-rate-conversion/) stores a long windowed sinc at a fine step and interpolates in the table, and [polyphase resampling](/polyphase-resampling/) organizes the same products as a bank of short filters.
- **Images.** In two dimensions the separable kernel $\mathrm{sinc}(x)\,\mathrm{sinc}(y)$ rebuilds a band-limited image; [image resampling](/image-resampling/) uses windowed versions of it.
- **Numerical analysis.** Sinc expansions also approximate analytic functions on the real line, with errors that fall like $e^{-c\sqrt N}$ for suitable functions; [sinc quadrature](/sinc-quadrature/) is the integration rule of this theory.

## When to use it

Use the exact series as a reference, for offline work where accuracy matters more than speed, and when the signal is known to be band-limited with a margin, so that a long windowed sinc gives errors near rounding level. Use a windowed sinc with a few dozen taps for high-quality audio resampling. Do not use it for real-time work with short latency, since it is not causal, or for images with sharp edges, where the ringing is visible; shorter kernels, splines or the methods on [signal reconstruction](/signal-reconstruction/) are better there.

## Pitfalls

- **The point $u = 0$.** $\sin(\pi v)/(\pi v)$ is $0/0$ at the sample times; test for an integer $u$ before the loop, as line L2 does, or define $\mathrm{sinc}(0) = 1$.
- **Two sinc conventions.** Signal processing uses $\sin(\pi u)/(\pi u)$; mathematics often uses $\sin(u)/u$. Mixing them stretches the kernel by $\pi$.
- **End effects.** Samples outside the window are treated as zero, so near the ends of a finite record the output pulls toward zero. Extend the record, or use a window long enough that the ends are far from the times of interest.
- **Slow convergence.** Doubling the number of terms only halves the error for typical signals. Plan for a windowed kernel instead of a longer plain sum.
- **Signals that are not band-limited.** If the signal had energy above $f_s/2$ before sampling, that energy has [aliased](/aliasing/) into the band, and the series rebuilds the aliased signal, not the original.
- **Accuracy of the sine.** For a large $u$ the argument $\pi v$ loses no accuracy, but the one-sine variant does unless $u$ is reduced first.

## Implementations

## History

E. T. Whittaker introduced the series in 1915 under the name *cardinal function*, as the interpolant of equally spaced values that has no rapidly oscillating part, and his son J. M. Whittaker studied its convergence in the following years. Vladimir Kotelnikov in 1933 and Claude Shannon in 1949 proved that the series rebuilds every band-limited signal from samples at twice the band, which made it the ideal reconstruction of communication engineering. Because the series converges slowly, practical systems soon replaced it by windowed and oversampled kernels; digital audio resampling with a stored windowed sinc became standard in the 1980s.

## References
