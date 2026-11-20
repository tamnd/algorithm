---
tag: QN0P95
kind: definition
slug: raised-cosine-filter
name: Raised-cosine filter
aliases:
- raised-cosine pulse
area: communications/modulation-and-detection
level: intro
summary: "A Nyquist pulse whose spectrum is flat in the middle and falls off as half a cosine period. The roll-off beta sets the excess bandwidth, from 0 (a sinc) to 1 (twice the minimum)."
prereqs: [nyquist-isi-criterion]
see_also: [root-raised-cosine-filter, pulse-shaping, eye-diagram, intersymbol-interference, spectral-efficiency, fir-filter, sinc-interpolation, matched-filter]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 9.2-1 (the raised cosine spectrum, its pulse in time, the roll-off factor and the split of the spectrum between the transmit and the receive filter)
  - book: isbn:9780521879071
    title: Robert G. Gallager, Principles of Digital Communication, Cambridge University Press, 2008
    locator: Section 6.3.1 (band-edge symmetry and the raised cosine pulse as its standard example)
---

The raised-cosine filter is the pulse $h(t)$ whose spectrum is flat up to $(1 - \beta)/(2T)$ and then falls to zero at $(1 + \beta)/(2T)$ along half a period of a cosine raised above zero. Its folded spectrum is flat, so by the [Nyquist ISI criterion](/nyquist-isi-criterion/) it is zero at every nonzero multiple of the symbol period $T$ and causes no [intersymbol interference](/intersymbol-interference/). The roll-off factor $\beta \in [0, 1]$ trades bandwidth for a faster decay in time. In practice the raised cosine is the overall response of a link, split into two [root-raised-cosine filters](/root-raised-cosine-filter/), one at the transmitter and one at the receiver.

## Definition

Let $T > 0$ be the symbol period and $\beta \in [0, 1]$ the roll-off factor, and let $\mathrm{sinc}(x) = \sin(\pi x)/(\pi x)$ with $\mathrm{sinc}(0) = 1$. The **raised-cosine spectrum** is

$$H(f) = \begin{cases} T, & |f| \le \dfrac{1 - \beta}{2T}, \\[2mm] \dfrac{T}{2}\left[1 + \cos\!\left(\dfrac{\pi T}{\beta}\left(|f| - \dfrac{1 - \beta}{2T}\right)\right)\right], & \dfrac{1 - \beta}{2T} < |f| \le \dfrac{1 + \beta}{2T}, \\[2mm] 0, & |f| > \dfrac{1 + \beta}{2T}, \end{cases}$$

and the **raised-cosine pulse** is its inverse Fourier transform,

$$h(t) = \mathrm{sinc}\!\left(\frac{t}{T}\right) \frac{\cos(\pi \beta t / T)}{1 - (2 \beta t / T)^2}.$$

At $t = \pm T/(2\beta)$ the fraction is $0/0$; the limit, and the value of $h$ there, is $(\pi/4)\, \mathrm{sinc}(1/(2\beta))$. For $\beta = 0$ the pulse is $\mathrm{sinc}(t/T)$. A **raised-cosine filter** is a linear filter with impulse response $h(t)$, or in discrete time an [FIR filter](/fir-filter/) with taps $h(nT/L_s)$ for $|n| \le S L_s$, where $L_s$ is the number of samples per symbol and $S$ the span in symbols on each side.

**Why the formula in time.** $H$ is the convolution of the rectangle $T\,\mathbf{1}\{|f| < 1/(2T)\}$ with the half-cosine bump $Q(f) = (\pi T / (2\beta)) \cos(\pi T f/\beta)$ on $|f| \le \beta/(2T)$, which has area $1$. Convolving with a bump of area $1$ keeps the flat part at $T$ and turns each edge of the rectangle into the integral of the bump, which is the raised cosine edge. In time, convolution becomes a product: the rectangle gives $\mathrm{sinc}(t/T)$, and the bump gives $\int Q(f) e^{j 2\pi f t} df = \cos(\pi\beta t/T)/(1 - (2\beta t/T)^2)$.

**Properties.**
- *No ISI.* $h(0) = 1$ and $h(kT) = 0$ for every integer $k \ne 0$, because the factor $\mathrm{sinc}(t/T)$ is zero there. (At $kT = \pm T/(2\beta)$, which happens for $\beta = 1/2$ at $k = \pm 1$, the value $(\pi/4)\,\mathrm{sinc}(k)$ is $0$ too.) In frequency: the edge satisfies $H(1/(2T) - x) + H(1/(2T) + x) = T$ for $0 \le x \le \beta/(2T)$, since $\cos(\pi/2 - y) + \cos(\pi/2 + y) = 0$, so the fold is the constant $T$.
- *Bandwidth.* The spectrum is zero for $|f| > (1 + \beta)/(2T)$. The baseband bandwidth is $(1 + \beta)/(2T)$; the bandwidth of the passband signal on a carrier is twice that, $(1 + \beta)/T$. The excess bandwidth over the Nyquist minimum $1/(2T)$ is the fraction $\beta$.
- *Decay.* For $\beta > 0$ and large $|t|$, $|h(t)| \le T^3/(\pi\, |t|\,(4\beta^2 t^2 - T^2))$, which falls like $1/|t|^3$. The sinc ($\beta = 0$) falls only like $1/|t|$.
- *Energy.* By Parseval, $\int h^2\, dt = \int H^2\, df = T(1 - \beta/4)$.

### Computing the pulse

The function below returns the pulse, with the limit at the two singular points. The filter taps are its values at $t = nT/L_s$.

```pseudo id=main
RC-PULSE(t, β, T)                       ▷ the raised-cosine pulse h(t)
L1  u ← t / T
L2  if β > 0 and |2βu| = 1 then
L3      return (π/4) · sinc(1 / (2β))   ▷ the limit at t = ±T/(2β)
L4  return sinc(u) · cos(πβu) / (1 - (2βu)²)

RC-TAPS(β, L_s, S)                      ▷ T = 1, L_s samples per symbol, S symbols on each side
L5  return [RC-PULSE(n / L_s, β, 1) for n = -S·L_s, ..., S·L_s]
```

The implementation also gives $H(f)$. Its tests check the values on this page, the zeros at $kT$ for several $\beta$, the flat fold, the energy $T(1 - \beta/4)$ in time and in frequency, and the continuity at $t = \pm T/(2\beta)$.

## Examples and non-examples

**Check values.** For $\beta = 0.5$ and $T = 1$: $h(0.5) = \mathrm{sinc}(0.5) \cos(\pi/4)/(1 - 0.25) = (2/\pi)(0.70711)/0.75 = 0.60021$, $h(1) = 0$, and $h(1.5) = -0.12004$. For $\beta = 0.25$: $h(0.5) = 0.62737$ and $h(1.5) = -0.18562$. The baseband bandwidth for $\beta = 0.25$ and $T = 1$ is $1.25/2 = 0.625$ Hz.

**The fold at one frequency.** For $\beta = 0.5$ and $T = 1$, the edge runs from $0.25$ to $0.75$. At $f = 0.4$, $H(0.4) = \tfrac12[1 + \cos(0.3\pi)] = 0.79389$, and its partner $H(0.4 - 1) = H(0.6) = \tfrac12[1 + \cos(0.7\pi)] = 0.20611$. The sum is $1 = T$.

**Full roll-off.** For $\beta = 1$ the pulse is $\mathrm{sinc}(t/T)\cos(\pi t/T)/(1 - 4t^2/T^2) = \mathrm{sinc}(2t/T)/(1 - 4t^2/T^2)$. Besides the zeros at $kT$, it is zero at $\pm 3T/2, \pm 5T/2, \ldots$, and $h(\pm T/2) = 1/2$. Zero crossings halfway between the symbols make the timing easy to track, at the cost of twice the minimum bandwidth.

**Decay in numbers.** The largest $|h(t)|$ over $10T \le t \le 11T$ is $0.0303$ for $\beta = 0$, $4.79 \times 10^{-4}$ for $\beta = 0.25$, and $2.21 \times 10^{-4}$ for $\beta = 0.5$. A filter truncated to $8$ symbols on each side loses little for $\beta \ge 0.25$, and much for the sinc.

**Bandwidth of a link.** QPSK at $1$ million symbols per second with $\beta = 0.25$ occupies $1.25$ MHz around the carrier and carries $2$ Mbit/s, a [spectral efficiency](/spectral-efficiency/) of $2/1.25 = 1.6$ bits/s/Hz.

**Non-example: one root-raised-cosine filter.** The [root-raised-cosine filter](/root-raised-cosine-filter/) has the spectrum $\sqrt{H(f)}$. Its folded spectrum is not flat on the edge, so a single RRC pulse has ISI: for $\beta = 0.5$, its value at $t = T$ is $-0.0934$ times its peak. Only the cascade of two RRC filters is a raised cosine.

**Non-example: a raised cosine in time.** The pulse $\tfrac12(1 - \cos(2\pi t/(LT)))$ on $0 \le t \le LT$, the frequency pulse of LRC [continuous-phase modulation](/continuous-phase-modulation/), is a raised cosine in time. It is a different object with the same name, and it is not a Nyquist pulse.

**Non-example: a Gaussian pulse.** The Gaussian filter of [Gaussian minimum-shift keying](/gaussian-minimum-shift-keying/) is never zero, so it has ISI at every symbol instant; GMSK accepts this for a compact spectrum.

## Related definitions

- [Nyquist ISI criterion](/nyquist-isi-criterion/): the theorem that makes any pulse with a flat fold free of ISI; the raised cosine is its standard example.
- [Root-raised-cosine filter](/root-raised-cosine-filter/): the square root of $H$, used at both ends of a link with a [matched filter](/matched-filter/).
- [Pulse shaping](/pulse-shaping/): the choice of the transmit pulse, where the raised cosine is the usual target.
- [Eye diagram](/eye-diagram/): shows how the eye of a raised-cosine link opens wider in time as $\beta$ grows.
- [Sinc interpolation](/sinc-interpolation/): the case $\beta = 0$, the ideal low-pass kernel.
- [Spectral efficiency](/spectral-efficiency/): the factor $1/(1 + \beta)$ that the excess bandwidth costs.

## References
