---
tag: 3S4YA7
kind: definition
slug: pulse-amplitude-modulation
name: Pulse amplitude modulation
aliases:
- M-PAM
- amplitude-shift keying
- ASK
area: communications/modulation-and-detection
level: intro
summary: A modulation that sends one of M equally spaced amplitudes of a fixed pulse in each symbol period.
prereqs: [signal-constellation]
see_also: [quadrature-amplitude-modulation, phase-shift-keying, gray-labeling, minimum-distance-detector, symbol-error-rate, bit-error-rate, pulse-shaping, nyquist-isi-criterion]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 3.2-1, Pulse Amplitude Modulation (PAM), and Section 4.3-1, Optimal Detection and Error Probability for ASK or PAM Signaling
  - book: isbn:9780792375487
    title: John R. Barry, Edward A. Lee and David G. Messerschmitt, Digital Communication, third edition, Kluwer Academic Publishers, 2004
    locator: Chapter 5, Pulse-Amplitude Modulation (baseband PAM, passband PAM and performance analysis in AWGN)
  - paper: doi:10.1109/TCOMM.2002.800818
    title: Kyongkuk Cho and Dongweon Yoon, On the general BER expression of one- and two-dimensional amplitude modulations, IEEE Transactions on Communications 50(7), 1074-1080, 2002
    locator: the exact bit error probability of Gray-coded M-PAM in AWGN
---

Pulse amplitude modulation (PAM) sends, in each symbol period, one fixed pulse scaled by one of $M$ equally spaced real amplitudes. Its [signal constellation](/signal-constellation/) is a set of points on a line, so it uses one real dimension per symbol. On a carrier it is also called amplitude-shift keying. [Quadrature amplitude modulation](/quadrature-amplitude-modulation/) uses two PAM signals on the in-phase and quadrature carriers, and [phase-shift keying](/phase-shift-keying/) changes the phase instead of the amplitude.

## Definition

**$M$-PAM.** Let $M = 2^k$. The *raw* amplitudes are $c_m = M - 1 - 2m$ for $m = 0, \ldots, M - 1$, that is $\pm 1, \pm 3, \ldots, \pm(M-1)$, with spacing 2. The point with the label $g(m)$ is

$$a_{g(m)} = \sqrt{\frac{3 E_s}{M^2 - 1}}\; c_m,$$

where $g(m) = m \oplus \lfloor m/2 \rfloor$ is the binary reflected Gray code (see [Gray labeling](/gray-labeling/)), so neighboring amplitudes have labels that differ in one bit. The baseband signal is $s(t) = \sum_n x_n\, g_{\mathrm{p}}(t - nT)$ with $x_n \in \{a_0, \ldots, a_{M-1}\}$ and a pulse $g_{\mathrm{p}}$ of unit energy. On a carrier, the same real symbols multiply $\sqrt{2}\cos(2\pi f_c t)$.

**Energy.** *Theorem.* With equally likely points, the raw average energy is $\frac{1}{M}\sum_m c_m^2 = (M^2 - 1)/3$, so the scale factor above gives the average energy $E_s$. *Proof.* $\sum_{m=0}^{M-1} (M - 1 - 2m)^2 = \sum_{j} (2j - M + 1)^2$, and with $\sum j = M(M-1)/2$ and $\sum j^2 = (M-1)M(2M-1)/6$ this is $M(M^2-1)/3$. $\square$ For example 4-PAM has raw energy 5 and 8-PAM has 21.

**Distances.** The minimum distance is the spacing, so $d_{\min}^2/E_s = 12/(M^2 - 1)$. The two outer points have one neighbor each and the $M - 2$ inner points have two, so $\bar N_{\min} = 2(M-1)/M$. The peak-to-average power ratio is $3(M-1)/(M+1)$.

**Error rates.** In the complex AWGN model $y = x + w$ with $w \sim \mathcal{CN}(0, N_0)$, the imaginary part carries no information, and the real part has noise variance $N_0/2$. A closed form under these assumptions (equal priors, minimum distance detection): an inner point is in error when the noise passes either half-spacing, an outer point when it passes one, so

$$\mathrm{SER} = 2\left(1 - \frac{1}{M}\right) Q\!\left(\sqrt{\frac{6}{M^2 - 1} \cdot \frac{E_s}{N_0}}\right),$$

in terms of $E_s/N_0$, with $Q$ the [Gaussian Q-function](/gaussian-q-function/). For the Gray labeling, the exact [bit error rate](/bit-error-rate/) is a short sum of $Q$ terms (Cho and Yoon 2002); at high SNR it is close to $\mathrm{SER}/\log_2 M$.

**Detection.** The [minimum distance detector](/minimum-distance-detector/) for PAM is a slicer: scale $\mathrm{Re}(y/h)$ back to raw amplitudes, round to the nearest odd integer, and clamp to $\pm(M-1)$. It takes $O(1)$ time.

**Bandwidth.** One real dimension per symbol. At baseband, $R_s$ real symbols per second need at least $R_s/2$ Hz (the [Nyquist ISI criterion](/nyquist-isi-criterion/)). On a carrier with two sidebands, PAM needs at least $R_s$ Hz but uses only the in-phase dimension. Square QAM with $M^2$ points sends two PAM symbols in the same bandwidth, which is why passband systems use QAM rather than PAM.

## Examples and non-examples

**4-PAM labels.** The raw amplitudes and labels are

| label | 00 | 01 | 11 | 10 |
|---|---|---|---|---|
| raw amplitude | $+3$ | $+1$ | $-1$ | $-3$ |

and the unit-energy points are these divided by $\sqrt{5}$.

**4-PAM at $E_s/N_0 = 15$ dB.** The argument of $Q$ is $a = \sqrt{0.4 \cdot 10^{1.5}} = 3.5566$, so $\mathrm{SER} = 1.5\, Q(3.5566) = 2.818 \times 10^{-4}$. Counting the bit errors of each crossing exactly gives the Gray bit error rate $\tfrac{1}{4}\big(3Q(a) + 2Q(3a) - Q(5a)\big) = 1.4090 \times 10^{-4}$, which equals $\mathrm{SER}/2$ to the digits shown. With the natural binary labels $00, 01, 10, 11$ in order, the middle crossing changes both bits, and the bit error rate is $1.8787 \times 10^{-4}$, larger by the factor 4/3.

**2-PAM is BPSK.** With $M = 2$, the points are $\pm\sqrt{E_s}$, $d_{\min}^2/E_s = 4$, and $\mathrm{SER} = Q(\sqrt{2E_s/N_0})$.

**Uses.** Four-level PAM is used on wired links where a carrier is not needed: high-speed Ethernet over copper and fiber, and memory and backplane links. The ATSC digital television standard uses 8 levels with vestigial sideband filtering.

**Non-example: on-off keying.** The levels $\{0, A\}$ are equally spaced, but their mean is $A/2$, not zero. Then $E_s = A^2/2$, $d_{\min}^2/E_s = 2$, and the scheme needs 3 dB more energy than 2-PAM for the same distance, because the mean $A/2$ carries no information (see [signal constellation](/signal-constellation/)). It is still used where the receiver detects only energy, as with direct detection in optical links.

**Non-example: pulse position and pulse width modulation.** These change when the pulse occurs or how long it lasts, not its amplitude, so they are not PAM.

## Related definitions

- **QAM.** Square $M^2$-QAM is two independent $M$-PAM signals on the in-phase and quadrature axes; see [quadrature amplitude modulation](/quadrature-amplitude-modulation/).
- **Constellation quantities.** $E_s$, $d_{\min}$ and $\bar N_{\min}$ are defined on the [signal constellation](/signal-constellation/) page.
- **Pulse.** The pulse $g_{\mathrm{p}}$ sets the spectrum; a [raised cosine](/raised-cosine-filter/) pulse avoids [intersymbol interference](/intersymbol-interference/); see [pulse shaping](/pulse-shaping/).
- **Error measures.** [Symbol error rate](/symbol-error-rate/) and [bit error rate](/bit-error-rate/).

## References
