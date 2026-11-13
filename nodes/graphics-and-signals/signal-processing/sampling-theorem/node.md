---
tag: JHNYYV
kind: theorem
slug: sampling-theorem
name: Nyquist-Shannon sampling theorem
aliases:
- Shannon sampling theorem
- Whittaker-Shannon theorem
- Kotelnikov theorem
- cardinal series theorem
area: graphics-and-signals/signal-processing
level: core
summary: "A signal with no frequencies at or above B Hz is fixed by its samples at any rate fs > 2B and equals the sinc series built from them; at fs = 2B a sine at B is lost."
prereqs: [aliasing]
see_also: [nyquist-rate, sinc-interpolation, signal-reconstruction, parsevals-theorem, antialiasing, reconstruction-filter, digital-image, compressed-sensing]
sources:
  - paper: doi:10.1109/JRPROC.1949.232969
    title: Claude E. Shannon, Communication in the Presence of Noise, Proceedings of the IRE 37(1), 1949
    locator: Section II, The Sampling Theorem, Theorem 1 and its proof by the Fourier series of the spectrum (pp. 11 to 12)
  - paper: doi:10.1017/S0370164600017806
    title: Edmund Taylor Whittaker, On the Functions which are Represented by the Expansions of the Interpolation-Theory, Proceedings of the Royal Society of Edinburgh 35, 1915
    locator: pp. 181 to 194 (the cardinal function, the sum of sinc functions through equally spaced values)
  - paper: doi:10.1109/T-AIEE.1928.5055024
    title: Harry Nyquist, Certain Topics in Telegraph Transmission Theory, Transactions of the AIEE 47(2), 1928
    locator: pp. 617 to 644 (the number of independent signal elements per second that a channel of a given bandwidth can carry)
  - paper: "Vladimir A. Kotelnikov, On the transmission capacity of the ether and of wire in electrocommunications, in Materials for the First All-Union Conference on Questions of Communications, Izdatelstvo Upravleniya Svyazi RKKA, Moscow, 1933; English translation in J. J. Benedetto and P. J. S. G. Ferreira (editors), Modern Sampling Theory, Birkhäuser, 2001"
    locator: the whole report (the theorem that a function with spectrum in a band of width W is fixed by its values at intervals 1/(2W)); no page locator confirmed
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 4, Sampling of Continuous-Time Signals (periodic sampling, the frequency-domain representation of sampling, and the reconstruction of a band-limited signal from its samples)
  - paper: doi:10.1109/5.843002
    title: Michael Unser, Sampling, 50 Years After Shannon, Proceedings of the IEEE 88(4), 2000
    locator: pp. 569 to 587 (Shannon's theorem as an orthogonal projection, its limits, and the modern variants)
---

The sampling theorem says that a signal whose spectrum is zero at all frequencies $|f| \ge B$ is determined completely by its values at the instants $n/f_s$, for any sampling rate $f_s > 2B$, and that it is rebuilt from them by the series $x(t) = \sum_n x(n/f_s)\,\mathrm{sinc}(f_s t - n)$. Below the rate $2B$ different signals share the same samples, which is [aliasing](/aliasing/). At exactly $f_s = 2B$ the theorem still holds for signals of finite energy, but it fails for a sinusoid at the band edge: $\sin(2\pi B t)$ sampled at $2B$ gives only zeros. The theorem is due in different forms to Whittaker (1915), Kotelnikov (1933) and Shannon (1949), and Nyquist's 1928 work on telegraphy gave the rate its name.

## Statement

**Notation.** Time $t$ is in seconds and frequency $f$ in Hz. The Fourier transform is $X(f) = \int_{-\infty}^{\infty} x(t) e^{-2\pi i f t} dt$, extended to $x \in L^2(\mathbb{R})$ by the Plancherel theorem (see [Parseval's theorem](/parsevals-theorem/)). The sampling rate is $f_s$ samples per second, the sampling period is $T = 1/f_s$, and $\mathrm{sinc}(u) = \sin(\pi u)/(\pi u)$ with $\mathrm{sinc}(0) = 1$. A signal is *band-limited to* $B$ if $X(f) = 0$ for almost every $|f| \ge B$.

**Theorem (sampling theorem).** Let $x \in L^2(\mathbb{R})$ be band-limited to $B > 0$, and let $f_s > 2B$. Then $x$ is a continuous function, $\sum_n |x(nT)|^2 < \infty$, and

$$x(t) = \sum_{n=-\infty}^{\infty} x(nT)\, \mathrm{sinc}\!\left(\frac{t - nT}{T}\right) \qquad \text{for every real } t,$$

with the series converging uniformly on $\mathbb{R}$. In particular, two such signals with the same samples are equal.

**The boundary case.** The proof below only uses that $X$ vanishes outside the closed interval $[-f_s/2, f_s/2]$. So for signals of finite energy the conclusion also holds at $f_s = 2B$; this is the form in Shannon's paper, with samples spaced $1/(2W)$ for a band of $W$ Hz. The strict inequality is needed as soon as the signal can carry a spectral line at the band edge, which finite energy excludes but real measurements do not:

- $\sin(2\pi B t)$ has the samples $\sin(\pi n) = 0$ at $f_s = 2B$, the same as the zero signal;
- $\cos(2\pi B t + \varphi)$ has the samples $(-1)^n \cos\varphi$, the same as $\cos\varphi \cos(2\pi B t)$.

A rule that is safe for every signal with spectrum in $(-B, B)$, including sums of sinusoids, is therefore the strict one, $f_s > 2B$, and this is the form most texts give.

**Signals made of tones.** Let $x(t) = \sum_{k=1}^{K} a_k e^{2\pi i f_k t}$ with distinct frequencies in $(-f_s/2, f_s/2)$ that are known. Then the samples $x(nT)$, $n = 0, \ldots, K-1$, determine every $a_k$. A real tone at $|f| < f_s/2$ is a pair of such terms, so a sum of real sinusoids below $f_s/2$ is fixed by its samples.

## In plain words

Think of a signal that cannot wiggle faster than some top speed. If you look at it often enough, there is no room between two looks for any surprise. The theorem gives the exact rule: look more than twice per cycle of the fastest wiggle. Then the looks fix the whole signal, and a standard recipe rebuilds it between the looks. If you look less often, a fast wiggle can hide between the looks and pass for a slow one. If you look exactly twice per cycle, you may always land on the moments where the fastest wave crosses zero, and then you miss it.

## Proof

Assume $X = 0$ almost everywhere outside $I = [-f_s/2, f_s/2]$; this covers $f_s > 2B$ and the finite-energy case $f_s = 2B$.

**Step 1: the samples are Fourier coefficients of the spectrum.** $X$ is in $L^2(I)$, hence in $L^1(I)$ since $I$ is bounded, and $x(t) = \int_I X(f) e^{2\pi i f t} df$ for every $t$. So $x$ is continuous. Expand $X$ on $I$ in the Fourier series of period $f_s$:

$$X(f) = \sum_n c_n e^{-2\pi i n f T}, \qquad c_n = \frac{1}{f_s}\int_I X(f) e^{2\pi i n f T} df = T\, x(nT),$$

with convergence in $L^2(I)$. By [Parseval's theorem](/parsevals-theorem/) for Fourier series, $\sum_n |c_n|^2 = \frac{1}{f_s}\int_I |X|^2 df$, so $\sum_n |x(nT)|^2 = f_s \int |X|^2 df = f_s \int |x|^2 dt < \infty$.

**Step 2: the series.** Let $X_N = \sum_{|n| \le N} c_n e^{-2\pi i n f T}$ on $I$. Since $\int_I e^{2\pi i f (t - nT)} df = f_s\, \mathrm{sinc}(f_s(t - nT))$,

$$\int_I X_N(f) e^{2\pi i f t} df = \sum_{|n| \le N} T\, x(nT)\, f_s\, \mathrm{sinc}\!\left(\frac{t - nT}{T}\right) = \sum_{|n| \le N} x(nT)\, \mathrm{sinc}\!\left(\frac{t - nT}{T}\right).$$

**Step 3: uniform convergence.** For every $t$, by the Cauchy-Schwarz inequality,

$$\left| x(t) - \sum_{|n| \le N} x(nT)\, \mathrm{sinc}\!\left(\frac{t - nT}{T}\right) \right| = \left| \int_I (X - X_N)(f)\, e^{2\pi i f t} df \right| \le \sqrt{f_s}\; \|X - X_N\|_{L^2(I)}.$$

The right side does not depend on $t$ and tends to $0$, so the series converges to $x$ uniformly.

**Step 4: uniqueness.** If two such signals have the same samples, their difference has all $c_n = 0$. The exponentials $e^{-2\pi i n f T}$ are complete in $L^2(I)$, so the spectrum of the difference is $0$, and by Plancherel the difference is $0$.

**Step 5: tones.** For $x(t) = \sum_k a_k e^{2\pi i f_k t}$ the samples are $x(nT) = \sum_k a_k z_k^n$ with $z_k = e^{2\pi i f_k T}$. The map $f \mapsto e^{2\pi i f T}$ is one to one on $[-f_s/2, f_s/2)$, so distinct $f_k$ in the open band give distinct $z_k$. The $K \times K$ matrix $(z_k^n)$ for $n = 0, \ldots, K - 1$ is a Vandermonde matrix with determinant $\prod_{j < k}(z_k - z_j) \ne 0$, so for known $f_k$ the first $K$ samples fix the $a_k$. At $f_s = 2B$ the frequencies $\pm B$ both map to $z = -1$, the determinant is $0$, and the two terms $e^{\pm 2\pi i B t}$ cannot be separated; that is the failure of $\sin(2\pi B t) = (e^{2\pi i Bt} - e^{-2\pi i Bt})/(2i)$. $\blacksquare$

## Consequences

**The samples carry the energy.** Step 1 gives $\int |x(t)|^2 dt = T \sum_n |x(nT)|^2$. For $x(t) = \mathrm{sinc}^2(t)$, whose spectrum is the triangle $\max(0, 1 - |f|)$ with $B = 1$, sampled at $f_s = 2$: the samples are $1$ at $n = 0$, $0$ at the other even $n$, and $4/(\pi^2 n^2)$ at odd $n$. Then $T\sum_n x(nT)^2 = \frac{1}{2}(1 + \frac{32}{\pi^4}\cdot\frac{\pi^4}{96}) = \frac{2}{3}$, which is $\int \mathrm{sinc}^4 dt$. The direct sum over $|n| \le 2000$ gives $0.66666666666$, within $4 \times 10^{-12}$ of $2/3$.

**Processing in discrete time.** For a band-limited input sampled above $2B$, the [DTFT](/discrete-time-fourier-transform/) of the samples equals $f_s X(f)$ on the baseband, with $\omega = 2\pi f/f_s$. So a digital filter $H(e^{i\omega})$ between an ideal sampler and an ideal reconstructor acts as the analog filter $H(e^{2\pi i f/f_s})$ for $|f| < f_s/2$. This is the basis of digital audio, software radio and every DSP system with converters.

**Oversampling buys short kernels.** The sinc series converges slowly: its terms decay only like $1/n$, and for general samples the truncation error falls like $1/N$ (see [sinc interpolation](/sinc-interpolation/)). When $f_s > 2B$, any kernel $g$ whose spectrum is $1$ on $[-B, B]$ and $0$ for $|f| \ge f_s - B$ also works, $x(t) = \sum_n x(nT)\, T g(t - nT)$, and $g$ can be smooth in frequency and hence fast-decaying in time. This is the practical reason for sampling somewhat above $2B$, for example audio at $44.1$ kHz for a band of $20$ kHz.

**Reconstruction in practice.** Real systems replace the sinc by a hold circuit, a spline or a finite kernel; the trade-offs are on [signal reconstruction](/signal-reconstruction/) and, for images, on [reconstruction filter](/reconstruction-filter/). The required rate $2B$ is the [Nyquist rate](/nyquist-rate/), and images inherit the same rule on their pixel grid ([digital image](/digital-image/)).

**Beyond band limits.** Signals that are sparse in some basis can be recovered from fewer samples than the Nyquist rate of their band by [compressed sensing](/compressed-sensing/); this does not contradict the theorem, which assumes nothing but the band.

## Tightness

**Below $2B$ the theorem fails.** The signal $\mathrm{sinc}^2(t)$ has $B = 1$. Sampled at $f_s = 1$, its samples are $1$ at $n = 0$ and $0$ elsewhere, exactly the samples of $\mathrm{sinc}(t)$, which has $B = 1/2$. The cardinal series returns $\mathrm{sinc}(t)$: at $t = 1/2$ it gives $2/\pi \approx 0.6366$, while the signal is $4/\pi^2 \approx 0.4053$. For every $f_s < 2B$ a similar pair exists: add to $x$ the signal with spectrum $W(f) - W(f + f_s)$, for any nonzero $W \in L^2$ that is zero outside $(f_s/2, B)$; this signal is band-limited to $B$, and the shifted copies of its spectrum cancel, so all its samples are zero. For tones, $e^{2\pi i f t}$ and $e^{2\pi i (f - f_s) t}$ with $f_s/2 < f < B$ have equal samples.

**At $2B$ it fails for line spectra.** As in the statement, $\sin(2\pi Bt)$ at $f_s = 2B$ has the phase $n/2$ cycles at sample $n$, which is $0$ or $1/2$ exactly, so every sample is zero and the cardinal series returns $0$ at $t = 1/(4B)$, where the signal is $1$. Just above the edge the information returns: at $f_s = 2.2B$ the samples are nonzero, and the Vandermonde system of Step 5 recovers the two complex amplitudes $\mp i/2$ of the sine.

**The constant 2 cannot be lowered.** The Paley-Wiener space of signals band-limited to $B$ has $2B$ degrees of freedom per second: H. J. Landau proved in 1967 that any sampling set from which all such signals can be stably recovered has a lower density of at least $2B$ points per second, even when the points are not equally spaced.

**No signal of finite duration is band-limited.** An $L^2$ signal band-limited to $B$ extends to an entire function of $t$, so it cannot vanish on an interval unless it is zero. Every real recording is therefore only approximately band-limited, and the residual spectrum above $f_s/2$ aliases; the anti-aliasing filter of [aliasing](/aliasing/) controls how much.

**Uniform convergence needs finite energy or oversampling.** For the bounded signal $\cos(2\pi B' t)$ with $B' < f_s/2$, the samples do not decay, and the plain sinc series converges only conditionally, in symmetric partial sums; with the faster kernels of oversampling it converges absolutely.

**A finite-energy signal at exactly $2B$.** For $\mathrm{sinc}^2(t)$ at $f_s = 2B = 2$, where the triangle spectrum is $0$ at the edge, the series reconstructs the signal. Truncated to $|n| \le N$, the largest error on a grid of $201$ points in $[-2.5, 2.5]$ was measured at $1.55 \times 10^{-6}$ for $N = 50$, $1.94 \times 10^{-7}$ for $N = 100$ and $2.42 \times 10^{-8}$ for $N = 200$. The error falls like $1/N^3$ here because the samples decay like $1/n^2$.

## History

E. T. Whittaker studied in 1915 which functions are determined by their values at equally spaced points, and introduced the *cardinal function* $\sum_n x(nT)\, \mathrm{sinc}((t - nT)/T)$ as the smoothest interpolant, the one free of high-frequency components. Harry Nyquist showed in 1928 that a telegraph channel of bandwidth $W$ can carry at most $2W$ independent pulses per second, the counting argument behind the rate $2W$; he did not state the reconstruction theorem. Vladimir Kotelnikov stated and proved the theorem for communication engineering in a 1933 report to a Soviet conference on communications, which remained little known outside the Soviet Union for decades. Claude Shannon gave the statement and the Fourier-series proof in his 1949 paper, called $1/(2W)$ the Nyquist interval, and wrote that the fact was common knowledge in the communication art. Other early versions are due to K. Ogura (1920) and H. Raabe (1939). The name varies with the country and the field: Shannon, Nyquist-Shannon, Whittaker-Shannon, WKS and Kotelnikov theorem all refer to the same result.

## References
