---
tag: TCPRM3
kind: definition
slug: root-raised-cosine-filter
name: Root-raised-cosine filter
aliases:
- RRC filter
- square-root raised-cosine filter
area: communications/modulation-and-detection
level: intro
summary: "The filter whose spectrum is the square root of a raised cosine. One at the transmitter and its matched copy at the receiver give a raised cosine overall: no ISI and the best SNR in white noise."
prereqs: [raised-cosine-filter, matched-filter]
see_also: [raised-cosine-filter, matched-filter, pulse-shaping, nyquist-isi-criterion, intersymbol-interference, eye-diagram, offset-qpsk, fir-filter]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 9.2-1 (the split of a raised cosine spectrum into a transmit filter and a matched receive filter, each with the square root of the spectrum)
  - book: isbn:9780521879071
    title: Robert G. Gallager, Principles of Digital Communication, Cambridge University Press, 2008
    locator: Section 6.3.2 (the shifts of a pulse by multiples of T are orthonormal if and only if the folded squared magnitude of its spectrum is T; the square root of a raised cosine as the example)
  - paper: "ETSI EN 302 307, Digital Video Broadcasting (DVB); Second generation framing structure, channel coding and modulation systems for Broadcasting, Interactive Services, News Gathering and other broadband satellite applications (DVB-S2)"
    locator: the clause on baseband shaping (square-root raised cosine with roll-off 0.35, 0.25 or 0.20)
---

The root-raised-cosine (RRC) filter has the square root of a [raised-cosine](/raised-cosine-filter/) spectrum as its frequency response. A link puts one RRC filter at the transmitter and the same filter, which is then the [matched filter](/matched-filter/), at the receiver. The two together form a raised cosine, so the samples at the receiver have no [intersymbol interference](/intersymbol-interference/), and the matched filter gives the best SNR in white noise. A single RRC pulse is not free of ISI; only the pair is.

## Definition

Let $T > 0$ be the symbol period, $\beta \in [0, 1]$ the roll-off factor, and $H(f)$ the raised-cosine spectrum with roll-off $\beta$ (flat at the value $T$ up to $(1 - \beta)/(2T)$, zero above $(1 + \beta)/(2T)$). The **root-raised-cosine filter** is the filter with the real, even, non-negative frequency response

$$G(f) = \sqrt{H(f)}.$$

Its impulse response, the **root-raised-cosine pulse**, is

$$g(t) = \frac{1}{\sqrt{T}} \cdot \frac{\sin\!\big(\pi(1 - \beta)t/T\big) + (4\beta t/T) \cos\!\big(\pi(1 + \beta)t/T\big)}{(\pi t/T)\big(1 - (4\beta t/T)^2\big)}.$$

The formula is $0/0$ at three points, and the values there are the limits:

$$g(0) = \frac{1}{\sqrt{T}}\left(1 - \beta + \frac{4\beta}{\pi}\right), \qquad g\!\left(\pm \frac{T}{4\beta}\right) = \frac{\beta}{\sqrt{2T}}\left[\left(1 + \frac{2}{\pi}\right) \sin\frac{\pi}{4\beta} + \left(1 - \frac{2}{\pi}\right) \cos\frac{\pi}{4\beta}\right].$$

For $\beta = 0$ the pulse is $\mathrm{sinc}(t/T)/\sqrt{T}$, with $\mathrm{sinc}(x) = \sin(\pi x)/(\pi x)$. In discrete time the filter has taps $g(nT/L_s)$ for $|n| \le S L_s$, with $L_s$ samples per symbol and a span of $S$ symbols on each side.

**Properties.**
- *Unit energy.* $\int g^2\, dt = \int H\, df = h(0) = 1$, where $h$ is the raised-cosine pulse.
- *The pair is a raised cosine.* $g$ is real and even, so its matched filter $g(-t)$ is $g$ itself, and $g * g$ has the spectrum $G^2 = H$. So $(g * g)(t) = h(t)$, which is $1$ at $t = 0$ and $0$ at every other multiple of $T$.
- *Orthonormal shifts.* $\int g(t - kT)\, g(t - lT)\, dt = h((k - l)T)$, which is $1$ for $k = l$ and $0$ otherwise. The pulses $g(t - kT)$ are an orthonormal set. In frequency this is the condition $\sum_m |G(f - m/T)|^2 = T$, the [Nyquist criterion](/nyquist-isi-criterion/) applied to $|G|^2$.
- *White noise stays white.* After the receive RRC filter, white noise of density $N_0/2$ sampled at $t = kT$ gives independent samples of variance $N_0/2$, because the correlation of the noise samples at lag $k$ is $(N_0/2)\, h(kT)$.
- *Bandwidth.* The same as the raised cosine: $(1 + \beta)/(2T)$ at baseband, $(1 + \beta)/T$ on a carrier.
- *Decay.* $|g(t)|$ falls like $1/t^2$, more slowly than the raised cosine ($1/|t|^3$). Near the band edge $H$ goes to zero like the square of the distance, so $G$ goes to zero like the distance itself, with a kink at the edge, and a kink costs one order of decay.

### Computing the pulse

```pseudo id=main
RRC-PULSE(t, β, T)                       ▷ unit energy
L1  u ← t / T
L2  if u = 0 then return (1 - β + 4β/π) / √T
L3  if β > 0 and |4βu| = 1 then return (β/√(2T)) · ((1 + 2/π) sin(π/(4β)) + (1 - 2/π) cos(π/(4β)))
L4  return (sin(π(1 - β)u) + 4βu · cos(π(1 + β)u)) / (√T · πu · (1 - (4βu)²))

RRC-TAPS(β, L_s, S)                      ▷ T = 1, L_s samples per symbol, S symbols on each side
L5  g ← [RRC-PULSE(n / L_s, β, 1) for n = -S·L_s, ..., S·L_s]
L6  return g / √(Σ g[n]²)                ▷ the truncated taps, scaled to unit energy

PAIR-AT-SYMBOLS(g, L_s)                  ▷ the transmit filter g, then the matched filter g
L7  r ← g convolved with g               ▷ g is even, so this is the correlation
L8  c ← the index of the center of r
L9  return [r[c + k·L_s] for every k with c + k·L_s inside r]
```

The tests check the values below, the unit energy, the limits at the three special points, that the convolution of two RRC pulses equals the raised cosine, and that the truncated pair has small ISI while one RRC alone does not.

## Examples and non-examples

**Check values.** For $T = 1$ (values of $\sqrt{T}\, g$):

| $\beta$ | $g(0)$ | $g(T/(4\beta))$ | $g(T)$ | $g(2T)$ |
|---|---|---|---|---|
| 0.25 | 1.06831 | $-0.06424$ (here $T/(4\beta) = T$) | $-0.06424$ | 0.05305 |
| 0.5 | 1.13662 | 0.57863 | $-0.10610$ | 0.04244 |

For example, $g(T)$ for $\beta = 0.5$ is $[\sin(\pi/2) + 2\cos(3\pi/2)]/[\pi(1 - 4)] = 1/(-3\pi) = -0.10610$, and $g(0) = 0.5 + 2/\pi = 1.13662$. Two common roll-offs: for $\beta = 0.35$ (DVB-S) the peak is $1.09563$, and for $\beta = 0.22$ (UMTS) it is $1.06011$.

**Non-example: one RRC pulse sampled alone.** Sampled at $t = kT$, a single RRC pulse has ISI. For $\beta = 0.5$ the sample at $t = T$ is $-0.0934$ times the peak, and for $\beta = 0.25$ it is $-0.0601$ times the peak. A receiver that samples the transmit RRC pulse without the matched RRC filter sees this ISI, and the [eye diagram](/eye-diagram/) at the transmitter output looks partly closed. This is expected: the eye opens after the receive filter.

**The truncated pair.** With $L_s = 8$ samples per symbol and a span of $8$ symbols on each side, the two RRC filters are $129$ taps each. Scaled so that the center of the pair is $1$, the largest sample of the pair at a nonzero multiple of $T$ is $5.43 \times 10^{-4}$ for $\beta = 0.25$ and $1.81 \times 10^{-4}$ for $\beta = 0.5$: residual ISI below $10^{-3}$, caused only by the truncation.

**Mismatched pair.** A transmit RRC with $\beta = 0.25$ and a receive RRC with $\beta = 0.35$ do not multiply to a Nyquist spectrum. The product $\sqrt{H_{0.25} H_{0.35}}$ is not band-edge symmetric, so the pair has ISI. Both ends must agree on $\beta$.

## Related definitions

- [Raised-cosine filter](/raised-cosine-filter/): the overall response of the pair, a Nyquist pulse.
- [Matched filter](/matched-filter/): the receive RRC is the matched filter of the transmit RRC, so it maximizes the SNR at the sampling instant.
- [Nyquist ISI criterion](/nyquist-isi-criterion/): the RRC pulse satisfies it in the form for orthonormal shifts, $\sum_m |G(f - m/T)|^2 = T$.
- [Pulse shaping](/pulse-shaping/): the RRC is the default transmit pulse of most single-carrier links.
- [Offset QPSK](/offset-qpsk/): uses the same pulse with the quadrature branch delayed by $T/2$.
- [FIR filter](/fir-filter/): the RRC is built as a truncated FIR filter with $L_s$ samples per symbol.

## References
