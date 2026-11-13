---
tag: 3S9P1H
kind: theorem
slug: parsevals-theorem
name: Parseval's theorem for the DTFT
aliases:
- Parseval's identity
- Plancherel theorem
area: graphics-and-signals/signal-processing
level: core
summary: "For a square-summable sequence, the sum of |x[n]|^2 equals (1/2π) times the integral of |X(e^(iω))|^2 over one period of its DTFT."
prereqs: [discrete-time-fourier-transform, parseval-theorem]
see_also: [time-frequency-uncertainty, sampling-theorem, power-spectral-density, wiener-khinchin-theorem, periodogram, fir-filter, gibbs-phenomenon, unitary-operator]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 2 (the table of Fourier transform theorems, where Parseval's theorem for sequences is listed with the convolution and modulation theorems)
  - book: isbn:9780691113845
    title: Elias M. Stein and Rami Shakarchi, Fourier Analysis, An Introduction, Princeton University Press, 2003
    locator: Chapter 3, Convergence of Fourier Series (mean-square convergence and Parseval's identity), and Chapter 5 (the Fourier transform on the real line and the Plancherel formula)
  - paper: doi:10.1007/BF03014877
    title: Michel Plancherel, Contribution à l'étude de la représentation d'une fonction arbitraire par des intégrales définies, Rendiconti del Circolo Matematico di Palermo 30, 1910
    locator: pp. 289 to 335 (the energy identity for Fourier integrals of square-integrable functions)
  - url: https://en.wikipedia.org/wiki/Parseval%27s_theorem
    title: Parseval's theorem, Wikipedia
    locator: the sections Statement of Parseval's theorem and Notation used in physics and engineering (the DTFT form with the factor 1/(2π)) and History (Parseval's memoir of 1799)
---

Parseval's theorem for the [discrete-time Fourier transform](/discrete-time-fourier-transform/) says that a sequence $x[n]$ and its transform $X(e^{i\omega})$ have the same energy: $\sum_n |x[n]|^2 = \frac{1}{2\pi}\int_{-\pi}^{\pi} |X(e^{i\omega})|^2\, d\omega$. The same holds for inner products, so the transform is, up to the factor $1/(2\pi)$, a unitary map from square-summable sequences onto square-integrable functions on one period. This page is the DTFT form for infinite sequences and a continuous frequency; the finite form, $\sum_k |X_k|^2 = N\sum_n |x[n]|^2$ for the DFT, is on the page [Parseval's theorem for the DFT](/parseval-theorem/). The two forms are cases of one statement, and the Plancherel theorem is the same statement for the Fourier transform on the real line.

## Statement

**Notation.** $\ell^2$ is the space of sequences $x : \mathbb{Z} \to \mathbb{C}$ with $\|x\|^2 = \sum_n |x[n]|^2 < \infty$, and $L^2 = L^2[-\pi, \pi]$ the space of functions with $\int_{-\pi}^{\pi} |X(\omega)|^2 d\omega < \infty$. The frequency $\omega$ is in radians per sample. The DTFT of $x \in \ell^2$ is the mean-square limit of the partial sums $X_N(e^{i\omega}) = \sum_{|n| \le N} x[n] e^{-i\omega n}$.

**Theorem (Parseval).** For $x, y \in \ell^2$ with DTFTs $X$ and $Y$,

$$\sum_{n=-\infty}^{\infty} x[n]\, \overline{y[n]} = \frac{1}{2\pi}\int_{-\pi}^{\pi} X(e^{i\omega})\, \overline{Y(e^{i\omega})}\, d\omega, \qquad \sum_{n=-\infty}^{\infty} |x[n]|^2 = \frac{1}{2\pi}\int_{-\pi}^{\pi} |X(e^{i\omega})|^2\, d\omega.$$

Moreover every $X \in L^2$ is the DTFT of exactly one $x \in \ell^2$, namely $x[n] = \frac{1}{2\pi}\int_{-\pi}^{\pi} X(e^{i\omega}) e^{i\omega n} d\omega$. So $x \mapsto X/\sqrt{2\pi}$ is a unitary map of $\ell^2$ onto $L^2$.

**In other units.** With the frequency $\nu = \omega/(2\pi)$ in cycles per sample the identity reads $\sum_n |x[n]|^2 = \int_{-1/2}^{1/2} |X(e^{2\pi i\nu})|^2\, d\nu$, with no constant. The factor depends on the unit of frequency and not on the signal.

**The Plancherel theorem.** For the Fourier transform $\hat x(f) = \int x(t) e^{-2\pi i f t} dt$ on the real line, the analogous identity is $\int |x(t)|^2 dt = \int |\hat x(f)|^2 df$. The integral defining $\hat x$ converges only for $x \in L^1$; Plancherel showed in 1910 that the map extends from $L^1 \cap L^2$ to a unitary map of $L^2(\mathbb{R})$ onto itself. Names vary: many texts say *Parseval* for Fourier series and sequences and *Plancherel* for the real line, and others use either name for both. The three settings, the DFT on $\mathbb{Z}_N$, the DTFT on $\mathbb{Z}$ and the transform on $\mathbb{R}$, are cases of the Plancherel theorem for locally compact abelian groups.

## In plain words

A signal has a total energy. One way to measure it is to add up the squared size of every sample. The other way is to split the signal into pure tones and add up the squared strength of every tone. Parseval's theorem says that the two totals are always equal. No energy is made or lost when one changes from the list of samples to the list of tones. So an engineer can measure the power of noise, the error of a filter or the distance between two signals in whichever view is easier, and the answer does not change.

## Proof

**Step 1: finite sequences.** Let $x$ and $y$ be zero outside $|n| \le N$. Then $X$ and $Y$ are trigonometric polynomials, and

$$\frac{1}{2\pi}\int_{-\pi}^{\pi} X \overline{Y}\, d\omega = \sum_{|m| \le N} \sum_{|n| \le N} x[m]\, \overline{y[n]}\, \frac{1}{2\pi}\int_{-\pi}^{\pi} e^{-i\omega(m - n)}\, d\omega = \sum_{|n| \le N} x[n] \overline{y[n]},$$

because the last integral is $1$ for $m = n$ and $0$ for each other pair of integers. This is a finite sum, so the exchange needs no justification.

**Step 2: the forward map on $\ell^2$.** For $x \in \ell^2$ and $M < N$, Step 1 applied to $x$ restricted to $M < |n| \le N$ gives $\frac{1}{2\pi}\|X_N - X_M\|_{L^2}^2 = \sum_{M < |n| \le N} |x[n]|^2$, which tends to $0$. So $(X_N)$ is a Cauchy sequence in $L^2$. Since $L^2$ is complete (the Riesz-Fischer theorem), it has a limit $X$, and this limit is the DTFT. The inner product is continuous in $L^2$, so

$$\frac{1}{2\pi}\int X \overline{Y}\, d\omega = \lim_{N \to \infty} \frac{1}{2\pi}\int X_N \overline{Y_N}\, d\omega = \lim_{N \to \infty} \sum_{|n| \le N} x[n] \overline{y[n]} = \sum_n x[n]\overline{y[n]}.$$

Taking $y = x$ gives the energy identity. The same continuity shows that $\frac{1}{2\pi}\int X e^{i\omega n} d\omega = x[n]$, which is the inverse formula.

**Step 3: the map is onto.** Let $X \in L^2$ and set $c_n = \frac{1}{2\pi}\int X e^{i\omega n} d\omega$. The functions $e^{-i\omega n}$ are orthonormal for the inner product $\frac{1}{2\pi}\int u \bar v$, so Bessel's inequality gives $\sum |c_n|^2 \le \frac{1}{2\pi}\int |X|^2 < \infty$, and $c \in \ell^2$. By Step 2, $c$ has a DTFT $C$ with the same coefficients as $X$, so $D = X - C$ has all coefficients zero. The trigonometric polynomials are dense in $L^2$: continuous periodic functions are dense, and by Fejér's theorem each one is a uniform limit of the Cesàro means of its Fourier series. A function orthogonal to a dense set is zero, so $D = 0$ and $X = C$. Uniqueness of $x$ follows from the inverse formula. $\blacksquare$

**The DFT form as a special case.** If $x$ is zero outside $0 \le n < N$, then $|X|^2 = \sum_{|d| < N} r[d] e^{-i\omega d}$ with $r[d] = \sum_n x[n + d]\overline{x[n]}$. The mean of $e^{-i\omega d}$ over the $N$ points $\omega_k = 2\pi k/N$ is $1$ if $N$ divides $d$ and $0$ otherwise, and the only multiple of $N$ with $|d| < N$ is $0$. So $\frac{1}{N}\sum_k |X(e^{i\omega_k})|^2 = r[0] = \frac{1}{2\pi}\int |X|^2 d\omega$: the $N$ DFT values integrate $|X|^2$ exactly, and the DTFT form becomes the [DFT form](/parseval-theorem/).

## Consequences

**A worked case.** For $x = (1, 2, 0, -1)$ at $n = 0, \ldots, 3$, the autocorrelation is $r[0] = 6$, $r[\pm 1] = 2$, $r[\pm 2] = -2$, $r[\pm 3] = -1$, so $|X(e^{i\omega})|^2 = 6 + 4\cos\omega - 4\cos 2\omega - 2\cos 3\omega$. Its mean over a period is $6$, the energy. The mean over $4$ or more equally spaced frequencies is also $6$. The mean over only $2$ points is $\frac{1}{2}(|X(e^{i0})|^2 + |X(e^{i\pi})|^2) = \frac{1}{2}(4 + 0) = 2$. This is $r[0] + r[2] + r[-2]$, the energy of the folded block $(1 + 0, 2 - 1)$, because sampling in frequency [aliases](/aliasing/) in time.

**Energy of an infinite sequence.** For $x[n] = a^n$, $n \ge 0$, with $|a| < 1$, $|X|^2 = 1/(1 - 2a\cos\omega + a^2)$. Parseval gives $\frac{1}{2\pi}\int_{-\pi}^{\pi} \frac{d\omega}{1 - 2a\cos\omega + a^2} = \frac{1}{1 - a^2}$, a classical integral obtained here from a geometric series. For $a = 1/2$ both sides are $4/3$.

**The ideal low-pass filter.** The inverse DTFT of the indicator of $|\omega| < \omega_c$ is $h[n] = \sin(\omega_c n)/(\pi n)$. Parseval gives $\sum_n h[n]^2 = \omega_c/\pi$, although $\sum_n |h[n]|$ diverges. The tail beyond $|n| = N$ is at most $2/(\pi^2 N)$, so the energy of the truncated filter converges like $1/N$.

**The Basel sum.** $X(e^{i\omega}) = \omega$ on $(-\pi, \pi)$ has $x[0] = 0$ and $|x[n]| = 1/|n|$ for $n \ne 0$. Parseval gives $\sum_{n \ne 0} 1/n^2 = \frac{1}{2\pi}\int_{-\pi}^{\pi}\omega^2 d\omega = \pi^2/3$, so $\sum_{n \ge 1} 1/n^2 = \pi^2/6$.

**Filter output energy and noise.** If $y = h * x$, then $Y = HX$ and $\sum|y[n]|^2 = \frac{1}{2\pi}\int |H|^2|X|^2 d\omega$. For white noise of variance $\sigma^2$ at the input of a stable filter, the output variance is $\sigma^2 \sum |h[n]|^2 = \frac{\sigma^2}{2\pi}\int |H|^2 d\omega$, the noise gain of the [frequency response](/frequency-response/).

**Truncation is the least-squares FIR design.** Let $H_d$ be a desired response with coefficients $h_d \in \ell^2$, and let $h$ be any filter supported on $|n| \le N$. Parseval gives $\frac{1}{2\pi}\int |H_d - H|^2 d\omega = \sum_{|n| \le N} |h_d[n] - h[n]|^2 + \sum_{|n| > N} |h_d[n]|^2$, which is smallest for $h = h_d$ on $|n| \le N$. So plain truncation of the ideal response, the rectangular window, is optimal in mean square for each length. It is not optimal in the maximum error: at a jump of $H_d$ it keeps the overshoot of the [Gibbs phenomenon](/gibbs-phenomenon/), and the [window functions](/window-functions/) of the [FIR filter](/fir-filter/) design trade mean-square error for smaller ripple.

**Power spectra.** The function $|X(e^{i\omega})|^2/(2\pi)$ is an energy density over frequency, and $r[d]$ is its inverse DTFT. For random signals the same pair is the [power spectral density](/power-spectral-density/) and the autocorrelation, linked by the [Wiener-Khinchin theorem](/wiener-khinchin-theorem/), and the [periodogram](/periodogram/) estimates the density from $|X|^2$ at DFT frequencies.

**Sampled signals.** If $x_c$ has finite energy and its spectrum is zero outside $|f| < f_s/2$, the [sampling theorem](/sampling-theorem/) writes it as a series of shifted sinc functions, and these are orthogonal with $\int \mathrm{sinc}^2((t - nT)/T)\, dt = T$. With the Plancherel theorem this gives $\int |x_c(t)|^2 dt = T\sum_n |x_c(nT)|^2$: the samples carry the energy of the signal.

**Uncertainty.** The [time-frequency uncertainty principle](/time-frequency-uncertainty/) uses the Plancherel identity twice, once for the signal and once for its derivative, to turn a frequency spread into an integral over time.

## Tightness

**The identity is exact.** Parseval's theorem is an equality, so there is no constant to improve. What can fail are its hypotheses and its extensions.

**Square summability is needed.** For $x \notin \ell^2$ the left side is infinite, and no function in $L^2$ has $x$ as its coefficients, by Bessel's inequality. The constant sequence and the unit step have only generalized transforms (trains of impulses), and $|X|^2$ is then not defined.

**Only the exponent 2 works.** The other $\ell^p$ norms are not kept. For $x = (1, 1)$, $|X|^2 = 2 + 2\cos\omega$, so $\sum |x[n]|^4 = 2$ while $\frac{1}{2\pi}\int |X|^4 d\omega = \frac{1}{2\pi}\int (2 + 2\cos\omega)^2 d\omega = 6$. For $1 \le p \le 2$ only the Hausdorff-Young inequality $\|X\|_{L^{p'}} \le \|x\|_{\ell^p}$, with $1/p + 1/p' = 1$ and the normalized measure $d\omega/(2\pi)$, remains.

**Too few frequency samples.** A finite set of $M$ frequency samples gives the exact energy of a sequence of length $L$ only when $M \ge L$. For $M < L$ the mean of $|X(e^{2\pi ik/M})|^2$ is $\sum_{d \equiv 0 \pmod M} r[d]$, the energy of the sequence folded modulo $M$, which can be larger or smaller than the true energy. In the worked case above, $M = 2$ gives $2$ instead of $6$.

**Pointwise information is lost.** Two transforms that differ on a set of measure zero have the same coefficients, so Parseval determines $X$ only almost everywhere. For the ideal low-pass filter, the value of $H$ at $\pm\omega_c$ is not determined by $h$.

## History

Marc-Antoine Parseval stated the identity for trigonometric series in a memoir presented to the Paris Académie des Sciences in 1799, as a formal manipulation without a convergence proof. The complete theory for square-integrable functions came with Lebesgue integration: in 1907 Frigyes Riesz and Ernst Fischer proved that $\ell^2$ and $L^2$ correspond one to one through Fourier coefficients. Michel Plancherel proved the version for the Fourier integral on the real line in 1910, which is why the continuous form carries his name. In signal processing the theorem entered as the energy relation between a sequence and its spectrum, and textbooks of discrete-time signal processing list it with the convolution and modulation theorems of the DTFT.

## References
