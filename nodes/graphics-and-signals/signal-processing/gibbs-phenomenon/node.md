---
tag: NNCRSC
kind: concept
slug: gibbs-phenomenon
name: Gibbs phenomenon
aliases:
- Gibbs ringing
- Gibbs overshoot
area: graphics-and-signals/signal-processing
level: core
summary: "Near a jump, the partial sums of a Fourier series overshoot by about 8.95% of the jump on each side, and the overshoot does not shrink as more terms are added."
prereqs: [discrete-time-fourier-transform]
see_also: [window-functions, spectral-leakage, fir-filter, digital-filter-design, sinc-interpolation, reconstruction-filter, parsevals-theorem, runge-phenomenon]
sources:
  - paper: doi:10.1038/059200b0
    title: J. Willard Gibbs, Fourier's Series, Nature 59, 1898
    locator: p. 200, letter of 29 December 1898 (the limit of the graphs of the partial sums of a sawtooth series)
  - paper: doi:10.1038/059606a0
    title: J. Willard Gibbs, Fourier's Series, Nature 59, 1899
    locator: p. 606, letter of 27 April 1899 (the correction that gives the size of the overshoot, the integral of sin u / u from 0 to π)
  - paper: "Henry Wilbraham, On a certain periodic function, The Cambridge and Dublin Mathematical Journal 3, 1848"
    locator: pp. 198 to 201 (the overshoot of the partial sums of a square-wave series, computed half a century before Gibbs)
  - paper: doi:10.2307/1967238
    title: Maxime Bôcher, Introduction to the Theory of Fourier's Series, Annals of Mathematics (2) 7(3), 1906
    locator: the section on the Gibbs phenomenon, where the name is introduced and the overshoot is proved for general jumps (page range of the section not confirmed)
  - paper: doi:10.1007/BF00330404
    title: Edwin Hewitt and Robert E. Hewitt, The Gibbs-Wilbraham phenomenon, an episode in Fourier analysis, Archive for History of Exact Sciences 21(2), 1979
    locator: pp. 129 to 160 (the history from Wilbraham to Gibbs and Bôcher, and the proofs)
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 7, Filter Design Techniques (design of FIR filters by windowing, where truncation of the ideal response shows the Gibbs phenomenon)
---

The Gibbs phenomenon is the overshoot of the partial sums of a Fourier series next to a jump discontinuity. Near a jump of size $J$, the sum of the first terms rises past the function by about $0.0895\,J$ on each side, then ripples. Adding more terms moves the overshoot closer to the jump and makes it narrower, but its height tends to the fixed constant $\left(\frac{1}{\pi}\mathrm{Si}(\pi) - \frac12\right) J \approx 0.0895\,J$, where $\mathrm{Si}$ is the sine integral; it never goes away. The same effect appears whenever a sharp edge in time or frequency is approximated by truncating its spectrum: in FIR filters designed by truncation, in [sinc interpolation](/sinc-interpolation/) of a step, and as ringing near edges in images.

## In plain words

A sharp step can be built from smooth waves by adding many of them. With a few waves the step looks rounded. With more waves it gets steeper, as expected. But just beside the step the sum always rises a bit too high, then wobbles, before it settles down. Adding more waves squeezes this bump closer to the step and makes it thinner. It does not make the bump lower. The bump stays at about nine parts in a hundred of the step's height. So a sum of smooth waves can match a step well on average but never everywhere.

## The idea

**The square wave.** Let $f(t) = \mathrm{sign}(\sin t)$, which is $1$ on $(0, \pi)$ and $-1$ on $(-\pi, 0)$, with jumps of size $J = 2$ at multiples of $\pi$. Its Fourier series is $\frac{4}{\pi}\sum_{k \ge 1} \frac{\sin((2k-1)t)}{2k-1}$. Let $S_m$ be the sum of the first $m$ terms.

**Where the peak is.** Differentiating term by term and summing the cosines,

$$S_m'(t) = \frac{4}{\pi}\sum_{k=1}^{m} \cos((2k-1)t) = \frac{2}{\pi}\,\frac{\sin(2mt)}{\sin t}.$$

So the critical points in $(0, \pi)$ are $t = j\pi/(2m)$, $j = 1, \ldots, 2m - 1$, alternately maxima and minima. The first maximum is at $t_m = \pi/(2m)$, which moves toward the jump at the rate $1/m$.

**How high it is.** Since $S_m(0) = 0$,

$$S_m(t_m) = \int_0^{\pi/(2m)} \frac{2}{\pi}\,\frac{\sin(2mt)}{\sin t}\,dt = \frac{2}{\pi}\int_0^{\pi} \frac{\sin u}{2m \sin(u/(2m))}\,du \;\longrightarrow\; \frac{2}{\pi}\int_0^{\pi}\frac{\sin u}{u}\,du = \frac{2}{\pi}\,\mathrm{Si}(\pi),$$

after the substitution $u = 2mt$. The limit is allowed by dominated convergence, since $2m\sin(u/(2m)) \ge 2u/\pi$ on $[0, \pi]$. With $\mathrm{Si}(\pi) = 1.8519370520$, the limit is $1.1789797$: the overshoot above $1$ is $0.1789797$, which is $0.0894899$ of the jump $J = 2$. The successive lobes have alternating signs and decreasing areas, so the first maximum is the largest value of $S_m$.

**Any jump.** Let $g$ be $2\pi$ periodic and piecewise continuously differentiable, with a jump $J = g(t_0^+) - g(t_0^-)$ at $t_0$. Then $g - \frac{J}{2}f(t - t_0)$ is continuous and piecewise smooth near $t_0$, and its Fourier series converges uniformly there. So the partial sums of $g$ behave near $t_0$ like those of $\frac{J}{2}f$: they overshoot by $\frac{J}{2}\cdot 0.1789797 = 0.0894899\,J$ on each side, at a distance of order $1/m$ from the jump.

**Mean square versus maximum.** By [Parseval's theorem](/parsevals-theorem/), the mean square error $\frac{1}{2\pi}\int |f - S_m|^2 dt = \frac{8}{\pi^2}\sum_{k > m}\frac{1}{(2k-1)^2}$ tends to $0$. So $S_m \to f$ in mean square, and also pointwise away from the jump, but not uniformly: $\sup_t |f(t) - S_m(t)|$ tends to $1$ (near the jump itself the sum passes through $0$ while $f = \pm 1$), and the overshoot keeps a fixed height while its width shrinks. The partial sum is the best approximation in mean square among trigonometric polynomials of its degree, and that best fit pays for its small energy error with a fixed maximum error.

**Why it happens.** $S_m = f * D_m$, the [convolution](/convolution/) of $f$ with the Dirichlet kernel, the [DTFT](/discrete-time-fourier-transform/) of a box. The Dirichlet kernel has negative side lobes, so near a jump the average gives weight to the wrong side and swings past the level. Any truncation of a spectrum by a sharp cut is multiplication by a box, which is convolution with a kernel of this kind on the other side.

**The cure: smooth the cut.** Replacing the sharp truncation by weights that go smoothly to zero removes or reduces the overshoot.

- *Fejér means.* The averages of $S_0, \ldots, S_{M-1}$ weight the harmonic $k$ by $1 - k/M$. Their kernel, the Fejér kernel, is nonnegative with integral $1$, so the result always lies between the smallest and largest values of $f$: no overshoot at all. The price is a wider transition, of order $1/M$ with a gentler slope.
- *Lanczos sigma factors* multiply the $k$-th harmonic by $\mathrm{sinc}(k/m)$, which reduces the overshoot to a small fraction of its size.
- *Windows.* In filter design the same idea is the choice of a [window function](/window-functions/) in place of plain truncation: the Hann, Hamming, Blackman and Kaiser windows trade a wider transition band for a much smaller ripple.

**The sampled version.** The DTFT of the ideal low-pass filter $h[n] = \sin(\omega_c n)/(\pi n)$ has a jump of size $1$ at $\omega_c$. Truncating $h$ to $|n| \le N$ is a partial Fourier sum in $\omega$, so the response overshoots by about $0.0895$ next to the cutoff, for every $N$. This is the ripple of FIR filters designed by plain truncation.

## Examples

**Partial sums of the square wave, measured.** The peak $S_m(\pi/(2m))$, evaluated directly from the sum, and the overshoot as a fraction of the jump $2$:

| $m$ (odd harmonics) | peak location $\pi/(2m)$ | peak value | overshoot / jump |
|---|---|---|---|
| $5$ | $0.31416$ | $1.1823282$ | $0.0911641$ |
| $50$ | $0.031416$ | $1.1790131$ | $0.0895065$ |
| $500$ | $0.0031416$ | $1.1789801$ | $0.0894900$ |
| limit | $0$ | $1.1789797$ | $0.0894899$ |

The limit uses $\mathrm{Si}(\pi)$ from its power series, which agrees with Simpson's rule on $4000$ intervals to $10^{-11}$. A search over a grid of $40m$ points in $(0, \pi/2]$ never finds a value above $S_m(\pi/(2m))$. The distance from the limit falls like $1/m^2$ (about $0.042/m^2$), always from above, so the overshoot never drops below $8.95\%$.

**The energy error vanishes anyway.** For $m = 5$, $20$ and $80$, the mean square error is $0.04039$, $0.01013$ and $0.00253$, decreasing like $1/m$, while the peak stays above $1.1789$ in each case. The value from Parseval's tail sum agrees with Simpson's rule on the error to $10^{-5}$.

**Fejér means.** With the weights $1 - k/M$, $M = 2m$, the largest value of the mean on a fine grid of $(0, \pi)$ is $0.93573$ for $m = 5$ and $0.99363$ for $m = 50$: the mean approaches $1$ from below and never overshoots.

**A truncated low-pass filter.** For the cutoff $\omega_c = \pi/2$, truncated to $|n| \le N$, the largest value of the response just inside the passband, searched at a step of $5 \times 10^{-5}$ rad, is $1.08991$ at $\omega_c - 0.1571$ for $N = 20$ and $1.08949$ at $\omega_c - 0.0157$ for $N = 200$. The peak sits about $\pi/N$ from the cutoff, and its height approaches $1.0895$, the same constant as for the square wave.

**Images.** Band-limiting an image with a sharp edge, as in sinc resampling or strong compression of high frequencies, produces bright and dark halos parallel to the edge, called ringing; the kernels that limit it are compared on [reconstruction filter](/reconstruction-filter/).

## Where it is used

- **FIR filter design.** The window method of [FIR filter](/fir-filter/) design starts from the truncated ideal response and fights its Gibbs ripple with [window functions](/window-functions/); [digital filter design](/digital-filter-design/) by optimal (equiripple) methods controls the ripple directly.
- **Spectral analysis.** The side lobes of the rectangular window that cause [spectral leakage](/spectral-leakage/) are the same Dirichlet kernel lobes, seen in frequency.
- **Spectral methods for differential equations.** Fourier and Chebyshev methods applied to solutions with shocks show Gibbs oscillations; filtering of the coefficients and reconstruction methods that use the location of the jump recover high accuracy away from it.
- **Signal and image reconstruction.** Ringing near edges in band-limited [sinc interpolation](/sinc-interpolation/), in MRI images reconstructed from truncated frequency data, and in heavily compressed images.
- **Approximation theory.** The phenomenon shows the gap between convergence in mean square and uniform convergence, as the [Runge phenomenon](/runge-phenomenon/) shows a similar gap for polynomial interpolation.

**History.** Henry Wilbraham described and computed the overshoot in 1848, but his paper was forgotten. In 1898 Albert Michelson's mechanical harmonic analyzer showed the overshoot for a square wave, and the question of what the partial sums converge to was argued in letters to Nature. J. Willard Gibbs's first letter, of December 1898, described the limit of the graphs for a sawtooth series without giving the size; his second letter, of April 1899, corrected it and gave the overshoot in terms of $\int_0^\pi \frac{\sin u}{u}du$. Maxime Bôcher gave a general analysis in 1906 and named it after Gibbs; the name Gibbs-Wilbraham phenomenon is also used.

## References
