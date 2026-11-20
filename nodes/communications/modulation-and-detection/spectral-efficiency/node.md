---
tag: EBH976
kind: definition
slug: spectral-efficiency
name: Spectral efficiency
aliases:
- bandwidth efficiency
area: communications/modulation-and-detection
level: intro
summary: "The information bit rate per hertz of bandwidth, in bits/s/Hz. With Eb/N0 it places a scheme on the power and bandwidth plane, where capacity needs Eb/N0 of at least (2^eta - 1)/eta."
prereqs: [shannon-hartley-theorem]
see_also: [shannon-hartley-theorem, energy-per-bit-to-noise-density-ratio, raised-cosine-filter, pulse-shaping, quadrature-amplitude-modulation, frequency-shift-keying, adaptive-modulation, faster-than-nyquist-signaling]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 4.6 (a comparison of digital signaling methods, with the bandwidth efficiency R/W plotted against the SNR per bit and the capacity bound)
  - paper: doi:10.1002/j.1538-7305.1948.tb00917.x
    title: C. E. Shannon, A mathematical theory of communication (continued), Bell System Technical Journal 27(4), 1948
    locator: Part IV, the continuous channel (the capacity of a band-limited channel with white Gaussian noise, from which the bound on the energy per bit follows)
---

Spectral efficiency is the rate of information bits that a scheme carries per hertz of the bandwidth it occupies, measured in bits per second per hertz. It tells how well a scheme uses the band, as [energy per bit](/energy-per-bit-to-noise-density-ratio/) tells how well it uses the power. The [Shannon-Hartley theorem](/shannon-hartley-theorem/) ties the two: a spectral efficiency $\eta$ needs $E_b/N_0 \ge (2^\eta - 1)/\eta$, and no scheme of any efficiency works below $\ln 2$, or $-1.59$ dB.

## Definition

Let a scheme send information bits at the rate $R$ (bits per second) in a band of width $B$ (hertz). Its **spectral efficiency** is

$$\eta = \frac{R}{B} \quad \text{bits/s/Hz}.$$

$R$ counts information bits, after the channel code: parity bits do not count. The value of $\eta$ depends on what $B$ means, so a statement of $\eta$ must say how $B$ is measured. Common choices are the band where the spectrum is not zero (exact for pulses with a band limit, such as the [raised cosine](/raised-cosine-filter/)), the width that holds $99\%$ of the power, and the null-to-null width of the main lobe.

**Linear modulation with Nyquist pulses.** A scheme with $M$ points per symbol, a code of rate $r$, symbol period $T$ and a raised-cosine or root-raised-cosine pulse of roll-off $\beta$ has $R = r\log_2 M / T$. On a carrier the band is $B = (1 + \beta)/T$, so

$$\eta = \frac{r \log_2 M}{1 + \beta}.$$

At baseband (real PAM) the band is $(1 + \beta)/(2T)$, and $\eta = 2 r\log_2 M/(1 + \beta)$. The largest value with no ISI is reached at $\beta = 0$, the sinc pulse of the [Nyquist ISI criterion](/nyquist-isi-criterion/).

**The power and bandwidth plane.** With $E_b$ the energy per information bit and $N_0$ the one-sided noise density, the signal power is $S = E_b R$ and the SNR in the band is

$$\frac{S}{N_0 B} = \eta\, \frac{E_b}{N_0}.$$

The Shannon-Hartley theorem says reliable transmission needs $R \le B\log_2(1 + S/(N_0 B))$, that is $\eta \le \log_2(1 + \eta E_b/N_0)$, or

$$\frac{E_b}{N_0} \ge \frac{2^\eta - 1}{\eta}.$$

Each scheme is a point on the plane with $E_b/N_0$ on one axis and $\eta$ on the other; the curve above bounds the region that any scheme can reach.

## Examples and non-examples

**The bound in numbers.**

| $\eta$ (bits/s/Hz) | $(2^\eta - 1)/\eta$ | in dB |
|---|---|---|
| 0.5 | 0.828 | $-0.82$ |
| 1 | 1 | 0 |
| 2 | 1.5 | 1.76 |
| 4 | 3.75 | 5.74 |
| 6 | 10.5 | 10.21 |
| 8 | 31.9 | 15.03 |

As $\eta \to 0$ the bound falls to $\ln 2 = 0.693$, which is $-1.59$ dB. Above about $\eta = 2$ the bound grows by about $3$ dB for each added bit/s/Hz, since $2^\eta$ doubles.

**QPSK with roll-off 0.25.** $M = 4$, no code, $\beta = 0.25$: $\eta = 2/1.25 = 1.6$ bits/s/Hz. At $1$ million symbols per second the signal fills $1.25$ MHz and carries $2$ Mbit/s.

**Coded 64-QAM.** $M = 64$, code rate $3/4$, $\beta = 0.2$: $\eta = 0.75 \cdot 6/1.2 = 3.75$ bits/s/Hz.

**Distance from the bound.** Uncoded BPSK and QPSK need $E_b/N_0 = 9.59$ dB for a bit error rate of $10^{-5}$. With sinc pulses, QPSK has $\eta = 2$, where the bound is $1.76$ dB: a gap of $7.8$ dB. Uncoded 16-QAM with Gray labels has $P_b \approx \tfrac34 Q\big(\sqrt{0.8\, E_b/N_0}\big)$, which reaches $10^{-5}$ at $13.43$ dB, at $\eta = 4$, where the bound is $5.74$ dB: a gap of $7.7$ dB. Channel codes close most of these gaps.

**Orthogonal FSK goes the other way.** $M$-ary [frequency-shift keying](/frequency-shift-keying/) with tones spaced by $1/T$ needs about $M/T$ hertz for $\log_2 M$ bits per symbol, so $\eta \approx \log_2 M / M$: $0.5$ for $M = 4$ and $0.25$ for $M = 16$. It moves to the left of the plane: less bandwidth efficiency, less $E_b/N_0$ needed.

**Faster than Nyquist.** [Faster-than-Nyquist signaling](/faster-than-nyquist-signaling/) with binary sinc pulses sent every $0.802T$ raises $\eta$ by the factor $1/0.802 = 1.25$, at the same band.

**Non-example: symbols per hertz.** The symbol rate per hertz, in baud per hertz, is not the spectral efficiency: 64-QAM and BPSK at the same symbol rate have the same baud per hertz and very different $\eta$.

**Non-example: bits per second per hertz per cell.** Cellular systems report the rate per hertz summed over the users of one cell, or per unit of area. These are system measures that include the reuse of the band, not the spectral efficiency of one link.

## Related definitions

- [Shannon-Hartley theorem](/shannon-hartley-theorem/): the capacity $B\log_2(1 + S/N)$, which gives the bound on $E_b/N_0$ for each $\eta$.
- [Energy per bit to noise density ratio](/energy-per-bit-to-noise-density-ratio/): the other axis of the plane; the SNR in the band is $\eta E_b/N_0$.
- [Raised-cosine filter](/raised-cosine-filter/) and [pulse shaping](/pulse-shaping/): set the factor $1/(1 + \beta)$.
- [Quadrature amplitude modulation](/quadrature-amplitude-modulation/): the usual way to raise $\eta$ in a fixed band.
- [Adaptive modulation](/adaptive-modulation/): chooses $M$ and the code rate, and so $\eta$, from the measured SNR.

## References
