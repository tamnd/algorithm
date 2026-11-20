---
tag: S02STG
kind: theorem
slug: nyquist-isi-criterion
name: Nyquist ISI criterion
aliases:
- Nyquist zero-ISI criterion
- Nyquist first criterion
area: communications/modulation-and-detection
level: intro
summary: "A pulse is zero at every nonzero multiple of T if and only if its spectrum, folded at multiples of 1/T, is the constant T. The narrowest such pulse is the sinc, of bandwidth 1/(2T)."
prereqs: [intersymbol-interference, sampling-theorem]
see_also: [raised-cosine-filter, root-raised-cosine-filter, pulse-shaping, eye-diagram, partial-response-signaling, faster-than-nyquist-signaling, matched-filter, nyquist-rate]
sources:
  - paper: doi:10.1109/T-AIEE.1928.5055024
    title: Harry Nyquist, Certain Topics in Telegraph Transmission Theory, Transactions of the AIEE 47(2), 1928
    locator: pp. 617 to 644 (the conditions on the shaping of a telegraph channel under which the signal elements do not interfere at the sampling instants)
  - book: isbn:9780521879071
    title: Robert G. Gallager, Principles of Digital Communication, Cambridge University Press, 2008
    locator: Section 6.3 (the Nyquist criterion, Theorem 6.3.1, band-edge symmetry in Section 6.3.1, and orthonormal shifts of a pulse in Section 6.3.2)
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 9.2-1 (design of band-limited signals for no intersymbol interference, the Nyquist criterion and the raised cosine spectrum)
---

The Nyquist ISI criterion says when a pulse $p(t)$, sent once every $T$ seconds, causes no [intersymbol interference](/intersymbol-interference/) at the sampling instants $kT$: exactly when the copies of its spectrum shifted by multiples of $1/T$ add up to a constant. It is the frequency-domain test behind every pulse of [pulse shaping](/pulse-shaping/), among them the [raised-cosine filter](/raised-cosine-filter/). A direct consequence is the smallest bandwidth of a pulse with no intersymbol interference, $1/(2T)$, which only the sinc pulse reaches. Applied to the pulse after a [matched filter](/matched-filter/), the same test says when the shifted transmit pulses are orthonormal, which is the reason for the [root-raised-cosine filter](/root-raised-cosine-filter/).

## Statement

**Notation.** Time $t$ is in seconds and frequency $f$ in Hz. The Fourier transform is $P(f) = \int p(t) e^{-j 2\pi f t} dt$, with $j$ the imaginary unit. $T > 0$ is the symbol period, and $\mathrm{sinc}(x) = \sin(\pi x)/(\pi x)$ with $\mathrm{sinc}(0) = 1$. The *folded spectrum* of $P$ for the period $T$ is

$$P_{\mathrm{fold}}(f) = \sum_{m = -\infty}^{\infty} P\!\left(f - \frac{m}{T}\right),$$

a function of period $1/T$. A pulse is a *Nyquist pulse* for $T$ if $p(0) = 1$ and $p(kT) = 0$ for every integer $k \ne 0$.

**Theorem (Nyquist ISI criterion).** Let $P$ be integrable, $\int |P(f)| df < \infty$, and let $p(t) = \int P(f) e^{j 2\pi f t} df$. Then $p$ is a Nyquist pulse for $T$ if and only if

$$P_{\mathrm{fold}}(f) = T \quad \text{for almost every } f.$$

**Corollary (minimum bandwidth).** Under the same hypothesis, let $P(f) = 0$ for $|f| > W$. If $p$ is a Nyquist pulse for $T$, then $W \ge 1/(2T)$. If $W = 1/(2T)$, then $P(f) = T$ for almost every $|f| < 1/(2T)$, so $p(t) = \mathrm{sinc}(t/T)$.

In a PAM link the received samples are $y_k = \sum_i a_i p((k - i)T) + w_k$, where $p$ is the whole response from the symbols to the sampler (transmit filter, channel and receive filter). The theorem says that $y_k = a_k + w_k$ for every symbol sequence $(a_i)$ exactly when the folded spectrum of that whole response is flat.

## In plain words

A transmitter sends one pulse for each symbol, one pulse every symbol period. The receiver reads the signal once per period, at the center of each pulse. If every pulse is zero at the centers of all the other pulses, then each reading holds only its own symbol. The criterion turns this condition on time samples into a condition on the spectrum. Cut the spectrum of the pulse into slices one symbol rate wide, stack the slices on top of each other, and add them. If the sum is flat, the pulse does not leak into its neighbors. If the sum has a dip or a bump anywhere, it leaks. A pulse whose spectrum is narrower than half the symbol rate leaves gaps in the stack, so it always leaks.

## Proof

**Step 1: the samples are integrals of the folded spectrum.** Let $I = [-1/(2T), 1/(2T))$. The intervals $I + m/T$, $m \in \mathbb{Z}$, cover the real line without overlap. For every integer $k$,

$$p(kT) = \int P(f) e^{j 2\pi f k T} df = \sum_{m} \int_I P\!\left(f - \frac{m}{T}\right) e^{j 2\pi (f - m/T) k T} df = \int_I P_{\mathrm{fold}}(f)\, e^{j 2\pi f k T} df .$$

The last step uses $e^{-j 2\pi m k} = 1$ and exchanges the sum and the integral. The exchange is valid because $\sum_m \int_I |P(f - m/T)| df = \int |P(f)| df < \infty$, so the series of $P(f - m/T)$ converges absolutely for almost every $f$ in $I$, $P_{\mathrm{fold}}$ is integrable on $I$, and the dominated convergence theorem applies.

**Step 2: the samples are the Fourier coefficients of the fold.** The functions $e^{j 2\pi f k T}$, $k \in \mathbb{Z}$, form the Fourier basis on $I$, an interval of length $1/T$. Step 1 says that the Fourier coefficient of $P_{\mathrm{fold}}$ with index $k$ is $T\, p(-kT)$:

$$T \int_I P_{\mathrm{fold}}(f)\, e^{-j 2\pi f k T} df = T\, p(-kT).$$

**Step 3: if the fold is flat.** If $P_{\mathrm{fold}} = T$ almost everywhere on $I$, Step 1 gives $p(kT) = T \int_I e^{j 2\pi f k T} df$. This is $T \cdot (1/T) = 1$ for $k = 0$. For $k \ne 0$ it is $T\,[e^{j 2\pi f k T}/(j 2\pi k T)]$ between $f = -1/(2T)$ and $f = 1/(2T)$, which is $(e^{j\pi k} - e^{-j\pi k})/(j 2\pi k) = \sin(\pi k)/(\pi k) = 0$. So $p$ is a Nyquist pulse.

**Step 4: if the pulse is a Nyquist pulse.** If $p(0) = 1$ and $p(kT) = 0$ for $k \ne 0$, Step 2 says that the integrable function $P_{\mathrm{fold}} - T$ has all its Fourier coefficients on $I$ equal to $0$: the coefficient with index $0$ is $T p(0) - T = 0$, and the others are $T p(-kT) - 0 = 0$. An integrable function on an interval whose Fourier coefficients are all zero is zero almost everywhere (uniqueness of Fourier coefficients in $L^1$). So $P_{\mathrm{fold}} = T$ almost everywhere.

**Step 5: the corollary.** Let $P = 0$ outside $[-W, W]$ with $W < 1/(2T)$. Take $f$ with $W < f < 1/(2T)$. The term $m = 0$ of the fold is $P(f) = 0$ because $f > W$. For $m \ne 0$, the point $f - m/T$ has absolute value at least $1/T - f > 1/(2T) > W$, so that term is $0$ too. Hence $P_{\mathrm{fold}} = 0 \ne T$ on the interval $(W, 1/(2T))$, which has positive length, and by Step 4 the pulse is not a Nyquist pulse. If $W = 1/(2T)$, the same count shows that for $|f| < 1/(2T)$ only the term $m = 0$ can be nonzero, so the criterion reads $P(f) = T$ there. The inverse transform of $T$ on $(-1/(2T), 1/(2T))$ is $\mathrm{sinc}(t/T)$. $\blacksquare$

## Consequences

**Raised cosine and other band-edge symmetric pulses.** If $P$ is real, equals $T$ for $|f| \le (1 - \beta)/(2T)$, is $0$ for $|f| \ge (1 + \beta)/(2T)$, and satisfies $P(1/(2T) - x) + P(1/(2T) + x) = T$ for $0 \le x \le \beta/(2T)$ (odd symmetry about the band edge), then the fold is $T$ and the pulse has no intersymbol interference. The [raised-cosine filter](/raised-cosine-filter/) is the standard example, with a cosine roll-off. The parameter $\beta \in [0, 1]$ is the roll-off factor, and the bandwidth is $(1 + \beta)/(2T)$ in baseband.

**Orthonormal shifts and the matched filter.** Let $p$ have finite energy and let $g(t) = \int p(s)\, p^*(s - t)\, ds$ be the pulse after the matched filter $p^*(-t)$. Then $g(kT) = \langle p(\cdot), p(\cdot - kT) \rangle$ and $G(f) = |P(f)|^2$. Apply the theorem to $g$: the shifts $p(t - kT)$, $k \in \mathbb{Z}$, are orthonormal if and only if $\sum_m |P(f - m/T)|^2 = T$ almost everywhere. This is why a link splits a raised cosine spectrum into two square roots, one at each end: the [root-raised-cosine filter](/root-raised-cosine-filter/). The matched filter output then has no intersymbol interference, and its noise samples are independent with variance $N_0$, where $N_0$ is the one-sided noise power spectral density.

**Design freedom above the minimum.** Above $1/(2T)$ the criterion leaves room. The excess bandwidth buys a pulse that decays faster in time, so it is less sensitive to timing errors (see [eye diagram](/eye-diagram/)) and easier to truncate to a finite filter. [Partial-response signaling](/partial-response-signaling/) reaches the bandwidth $1/(2T)$ in another way: it keeps a known amount of intersymbol interference. [Faster-than-Nyquist signaling](/faster-than-nyquist-signaling/) breaks the criterion on purpose.

**The criterion is about samples only.** The fold of the whole response must be flat. A flat fold at the transmitter alone gives no guarantee after a channel with a frequency response $C(f)$, because the whole response is $P(f) C(f)$. Restoring the flat fold is the task of [channel equalization](/channel-equalization/).

## Tightness

**A pulse narrower than $1/(2T)$.** Let $T = 1$ and $P(f) = 1$ for $|f| < 0.4$ and $0$ elsewhere, so $W = 0.4 < 1/2$. Then $p(t) = 0.8\, \mathrm{sinc}(0.8 t)$, and $p(1) = \sin(0.8\pi)/\pi = 0.18710$, not $0$. The fold is $0$ on $0.4 < |f| < 0.5$, as Step 5 says.

**A trapezoid passes.** Let $T = 1$ and let $P$ be the trapezoid that is $1$ for $|f| \le 0.25$, falls linearly to $0$ at $|f| = 0.75$, and is $0$ beyond. Its roll-off factor is $\beta = 0.5$. At $f = 0.4$ the fold is $P(0.4) + P(-0.6) = 0.7 + 0.3 = 1$, and the same sum holds at every $f$. The pulse is $p(t) = \mathrm{sinc}(t)\, \mathrm{sinc}(0.5 t)$, the product of the two transforms of the rectangles whose convolution is the trapezoid. It is $0$ at every nonzero integer because the first factor is, and $p(0.5) = \mathrm{sinc}(0.5)\, \mathrm{sinc}(0.25) = 0.57316$.

**The sinc is the only pulse at the minimum.** At $W = 1/(2T)$ the corollary forces $P = T$ on the open band, so no other pulse of that bandwidth is a Nyquist pulse. The sinc decays only like $1/|t|$, and the sum $\sum_k |\mathrm{sinc}(k + \delta)|$ diverges for every timing offset $\delta$ that is not an integer. So a long random symbol sequence can close the eye of a sinc pulse at any timing error; the [eye diagram](/eye-diagram/) page gives the numbers.

**The hypothesis on $P$.** The proof needs the fold to exist as an integrable function. Integrability of $P$ is a convenient sufficient condition; Gallager states the theorem for $P$ of finite energy that decays faster than $1/|f|^{1 + \epsilon}$, and with the fold taken as a limit in mean square.

## History

Harry Nyquist studied telegraph transmission in his 1928 paper and gave conditions on the shaping of the channel under which the signal elements do not interfere at the instants where the receiver reads them. The odd symmetry of the roll-off about the frequency $1/(2T)$ is the band-edge symmetry above, and the minimum bandwidth $1/(2T)$ for $1/T$ independent pulses per second is the same count that later gave the [Nyquist rate](/nyquist-rate/) of the [sampling theorem](/sampling-theorem/) its name. Engineers call the zero-ISI condition Nyquist's first criterion; the same paper also treats the shape of the pulse between the sampling instants, which this page does not cover. The modern form with the folded spectrum is in the textbooks of Proakis and Salehi and of Gallager.

## References
