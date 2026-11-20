---
tag: XNM34K
kind: definition
slug: phase-shift-keying
name: Phase-shift keying
aliases:
- PSK
- BPSK
- QPSK
- M-PSK
area: communications/modulation-and-detection
level: intro
summary: A modulation that sends one of M equally spaced phases of a carrier of fixed amplitude in each symbol period.
prereqs: [signal-constellation]
see_also: [quadrature-amplitude-modulation, pulse-amplitude-modulation, differential-phase-shift-keying, offset-qpsk, amplitude-and-phase-shift-keying, gray-labeling, symbol-error-rate, minimum-distance-detector]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 3.2-2, Phase Modulation, and Section 4.3-2, Optimal Detection and Error Probability for PSK Signaling
  - paper: doi:10.1109/MILCOM.1991.258319
    title: John W. Craig, A new, simple and exact result for calculating the probability of error for two-dimensional signal constellations, MILCOM 91 Conference Record, 1991
    locator: pp. 571-575 (the exact symbol error probability of M-PSK as a single integral over a finite range)
  - book: isbn:9780471649533
    title: Marvin K. Simon and Mohamed-Slim Alouini, Digital Communication over Fading Channels, second edition, Wiley, 2005
    locator: Chapter 4, Alternative Representations of Classical Functions (the integral forms behind the M-PSK error probability)
---

Phase-shift keying (PSK) sends, in each symbol period, a carrier of fixed amplitude with one of $M$ equally spaced phases. Its [signal constellation](/signal-constellation/) is $M$ points on a circle, so every symbol has the same energy, which suits amplifiers that work best at a constant power. [Pulse amplitude modulation](/pulse-amplitude-modulation/) changes the amplitude instead, and [quadrature amplitude modulation](/quadrature-amplitude-modulation/) changes both; the two coincide with PSK only at four points, where QPSK is 4-QAM.

## Definition

**$M$-PSK.** Let $M = 2^k$ and fix an offset phase $\phi_0$. The point with the label $g(m)$ is

$$a_{g(m)} = \sqrt{E_s}\, e^{j(2\pi m/M + \phi_0)}, \qquad m = 0, \ldots, M - 1,$$

where $g(m) = m \oplus \lfloor m/2 \rfloor$ is the binary reflected Gray code, so the labels change by one bit from each point to the next around the circle, including from $m = M - 1$ back to $m = 0$ (see [Gray labeling](/gray-labeling/)). The passband signal is $\mathrm{Re}\{\sqrt{2}\, a\, g_{\mathrm{p}}(t) e^{j2\pi f_c t}\}$, a carrier of phase $2\pi m/M + \phi_0$.

- **BPSK** is $M = 2$ with $\phi_0 = 0$: the points $\pm\sqrt{E_s}$. It is also 2-PAM.
- **QPSK** is $M = 4$. With $\phi_0 = \pi/4$ its points are $\sqrt{E_s}(\pm 1 \pm j)/\sqrt{2}$, the same points as 4-QAM.

**The two Gray labelings of QPSK.** This page labels the points by $g(m)$ around the circle, so with $\phi_0 = \pi/4$ the labels 00, 01, 11, 10 sit at 45, 135, 225 and 315 degrees. The QAM page labels by the in-phase bit and then the quadrature bit, which puts 01 at 315 degrees and 10 at 135 degrees. Both are Gray labelings and have the same bit error rate in AWGN, but a transmitter and a receiver that use different ones will swap two of the four labels.

**Distances.** Neighbors on the circle are at the distance $d_{\min} = 2\sqrt{E_s}\sin(\pi/M)$, so $d_{\min}^2/E_s = 4\sin^2(\pi/M)$. Each point has two nearest neighbors for $M \ge 3$ and one for $M = 2$. The peak-to-average power ratio of the points is 1.

**Error rates.** These are closed forms in terms of $E_s/N_0$, under these assumptions: complex AWGN $\mathcal{CN}(0, N_0)$, equal priors, a known carrier phase and minimum distance detection.

- BPSK: $\mathrm{SER} = Q(\sqrt{2E_s/N_0})$.
- QPSK: $\mathrm{SER} = 2Q(\sqrt{E_s/N_0}) - Q(\sqrt{E_s/N_0})^2$, since the two axes are independent BPSK decisions.
- $M$-PSK, exact (Craig 1991):

$$\mathrm{SER} = \frac{1}{\pi}\int_0^{(M-1)\pi/M} \exp\!\left(-\frac{E_s}{N_0} \cdot \frac{\sin^2(\pi/M)}{\sin^2\theta}\right) d\theta.$$

- $M$-PSK, approximation for $M \ge 4$: $\mathrm{SER} \approx 2Q\big(\sqrt{2E_s/N_0}\,\sin(\pi/M)\big)$. It is an upper bound by the [union bound](/union-bound/) over the two half-planes that bound each decision region, and it is tight at high SNR.

**Detection.** The [minimum distance detector](/minimum-distance-detector/) for PSK compares phases only: it takes the angle of $y/h$, subtracts $\phi_0$ and rounds to the nearest multiple of $2\pi/M$. It takes $O(1)$ time and does not need $E_s$ or $N_0$.

## Examples and non-examples

**8-PSK labels.** With $\phi_0 = 0$, the labels around the circle are

| angle | 0° | 45° | 90° | 135° | 180° | 225° | 270° | 315° |
|---|---|---|---|---|---|---|---|---|
| label | 000 | 001 | 011 | 010 | 110 | 111 | 101 | 100 |

Its minimum distance at $E_s = 1$ is $2\sin(\pi/8) = 0.76537$.

**Error rates.** At $E_s/N_0 = 10$ dB, QPSK has $\mathrm{SER} = 1.5648 \times 10^{-3}$, and the approximation $2Q(\sqrt{10})$ gives $1.5654 \times 10^{-3}$. At $E_s/N_0 = 15$ dB, 8-PSK has $\mathrm{SER} = 2.3395 \times 10^{-3}$; the exact integral and the approximation agree to all the digits shown. 16-PSK has $\mathrm{SER} = 0.38295$ at 10 dB and $5.7980 \times 10^{-3}$ at 20 dB.

**PSK against QAM at 16 points.** 16-PSK has $d_{\min}^2/E_s = 0.1522$ and 16-QAM has $0.4$, so 16-PSK needs 4.2 dB more energy for the same minimum distance. Above 8 points, systems use PSK only when a constant envelope matters more than power, for example on satellite amplifiers driven near saturation; they often prefer [APSK](/amplitude-and-phase-shift-keying/), which uses a few rings.

**BPSK error rate in $E_b/N_0$.** BPSK carries one bit per symbol, so $E_b = E_s$ and the bit error rate is $Q(\sqrt{2E_b/N_0})$: 0.078650 at 0 dB and $3.8721 \times 10^{-6}$ at 10 dB. QPSK with a Gray labeling has the same bit error rate as BPSK at the same $E_b/N_0$, because it is two BPSK signals in quadrature.

**Uses.** BPSK and QPSK are the low-rate modes of Wi-Fi and cellular systems and the modulation of satellite navigation signals. QPSK and 8-PSK are used on satellite links.

**Non-example: differential PSK.** [Differential phase-shift keying](/differential-phase-shift-keying/) uses the same points, but the bits choose the *change* of phase from one symbol to the next, and the receiver compares two received symbols without a phase reference. Its error rate is different: about 3 dB worse than coherent PSK at high SNR for $M \ge 4$, and less for $M = 2$.

**Non-example: frequency-shift keying.** [FSK](/frequency-shift-keying/) also keeps a constant envelope, but it changes the frequency, and its $M$ signals are orthogonal, not points on a circle in two dimensions.

## Related definitions

- **Offset and rotated QPSK.** [Offset QPSK](/offset-qpsk/) delays the quadrature bits by half a symbol, so the phase never jumps by 180 degrees, which lowers envelope variations after filtering. [Minimum-shift keying](/minimum-shift-keying/) is a form of offset QPSK with half-sine pulses.
- **APSK.** [Amplitude and phase-shift keying](/amplitude-and-phase-shift-keying/) puts PSK rings of several radii together.
- **Constellation quantities and errors.** [Signal constellation](/signal-constellation/), [symbol error rate](/symbol-error-rate/) and [bit error rate](/bit-error-rate/).

## References
