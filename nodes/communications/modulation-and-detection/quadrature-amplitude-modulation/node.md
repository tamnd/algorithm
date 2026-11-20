---
tag: 8ZFTA8
kind: definition
slug: quadrature-amplitude-modulation
name: Quadrature amplitude modulation
aliases:
- QAM
- M-QAM
area: communications/modulation-and-detection
level: intro
summary: A modulation that sends a point of a two-dimensional grid by changing the amplitudes of an in-phase and a quadrature carrier.
prereqs: [pulse-amplitude-modulation, signal-constellation]
see_also: [phase-shift-keying, amplitude-and-phase-shift-keying, gray-labeling, minimum-distance-detector, symbol-error-rate, bit-error-rate, probabilistic-constellation-shaping, adaptive-modulation]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 3.2-3, Quadrature Amplitude Modulation, and Section 4.3-3, Optimal Detection and Error Probability for QAM Signaling
  - book: isbn:9780792375487
    title: John R. Barry, Edward A. Lee and David G. Messerschmitt, Digital Communication, third edition, Kluwer Academic Publishers, 2004
    locator: Chapter 5, Pulse-Amplitude Modulation (passband PAM with complex symbols, which includes QAM), and Chapter 6, Advanced Modulation
  - paper: doi:10.1109/TCOMM.2002.800818
    title: Kyongkuk Cho and Dongweon Yoon, On the general BER expression of one- and two-dimensional amplitude modulations, IEEE Transactions on Communications 50(7), 1074-1080, 2002
    locator: the exact bit error probability of Gray-coded square and rectangular QAM in AWGN
---

Quadrature amplitude modulation (QAM) sends, in each symbol period, two [PAM](/pulse-amplitude-modulation/) amplitudes at once: one on a cosine carrier and one on a sine carrier of the same frequency. The two carriers are orthogonal, so the receiver can separate them, and the [signal constellation](/signal-constellation/) is a grid of points in the complex plane. It changes both amplitude and phase, unlike [phase-shift keying](/phase-shift-keying/), which keeps the amplitude fixed; at 16 points and more it needs less energy than PSK for the same error rate.

## Definition

**Square $M$-QAM.** Let $M = 4^k$ and $L = \sqrt{M}$. With the raw PAM amplitudes $c_m = L - 1 - 2m$ for $m = 0, \ldots, L - 1$ and the Gray code $g(m) = m \oplus \lfloor m/2 \rfloor$, the point with the label $i = g(m_I)\, L + g(m_Q)$ is

$$a_i = \sqrt{\frac{3 E_s}{2(M - 1)}}\; \big(c_{m_I} + j\, c_{m_Q}\big).$$

So the first $k$ bits of the label choose the in-phase level and the last $k$ bits choose the quadrature level, each by the Gray code of $L$-PAM. Two points at the minimum distance differ in one level on one axis, so their labels differ in one bit: this is a [Gray labeling](/gray-labeling/). The passband signal is

$$s(t) = \sqrt{2}\, g_{\mathrm{p}}(t)\big(\mathrm{Re}\,a\, \cos(2\pi f_c t) - \mathrm{Im}\,a\, \sin(2\pi f_c t)\big) = \mathrm{Re}\{\sqrt{2}\, a\, g_{\mathrm{p}}(t)\, e^{j 2\pi f_c t}\}.$$

**Energy.** Each axis is $L$-PAM with raw energy $(L^2 - 1)/3$, so the raw energy of the grid is $2(M-1)/3$: 2 for 4-QAM, 10 for 16-QAM and 42 for 64-QAM. The scale factor above makes the average energy $E_s$.

**Distances.** $d_{\min}^2/E_s = 6/(M - 1)$: 0.4 for 16-QAM, 0.0952 for 64-QAM. The average number of nearest neighbors is $4(1 - 1/L)$: 3 for 16-QAM and 3.5 for 64-QAM. The corner points have the largest energy, and the peak-to-average power ratio is $3(L-1)/(L+1)$: 1.8 (2.55 dB) for 16-QAM and 2.333 (3.68 dB) for 64-QAM.

**Error rates.** A closed form, in terms of $E_s/N_0$, under these assumptions: complex AWGN $\mathcal{CN}(0, N_0)$, equal priors and minimum distance detection. The noise on the two axes is independent with variance $N_0/2$, so each axis is an $L$-PAM decision with error probability

$$p = 2\left(1 - \frac{1}{L}\right) Q\!\left(\sqrt{\frac{3}{M - 1}\cdot\frac{E_s}{N_0}}\right),$$

and a symbol is correct only if both axes are: $\mathrm{SER} = 1 - (1 - p)^2 = 2p - p^2$. The exact bit error rate of the Gray labeling is a finite sum of $Q$ terms (Cho and Yoon 2002); at high SNR it is close to $\mathrm{SER}/\log_2 M$.

**Detection.** Since the grid is a product of two PAM sets and the distance splits into the two axes, the [minimum distance detector](/minimum-distance-detector/) slices the real and imaginary parts of $y/h$ independently, in $O(1)$ time.

**Non-square QAM.** For $M = 2^{2k+1}$ (8, 32, 128), there is no square grid. *Rectangular* QAM uses an $L_1 \times L_2$ grid; *cross* QAM removes the corners of a larger square to lower the energy. Cross constellations do not have a perfect Gray labeling; the [Gray labeling](/gray-labeling/) page discusses this.

## Examples and non-examples

**16-QAM labels.** In raw units (divide by $\sqrt{10}$ for $E_s = 1$), with the label written as in-phase bits then quadrature bits:

| | Q bits 00 ($+3$) | 01 ($+1$) | 11 ($-1$) | 10 ($-3$) |
|---|---|---|---|---|
| **I bits 00 ($+3$)** | 0000 | 0001 | 0011 | 0010 |
| **01 ($+1$)** | 0100 | 0101 | 0111 | 0110 |
| **11 ($-1$)** | 1100 | 1101 | 1111 | 1110 |
| **10 ($-3$)** | 1000 | 1001 | 1011 | 1010 |

For example 0000 is $3 + 3j$, 0111 is $1 - 1j$ and 1010 is $-3 - 3j$.

**A decision.** For $y = 0.5 - 0.2j$ with $h = 1$ and $E_s = 1$, the raw value is $\sqrt{10}\,y = 1.5811 - 0.6325j$. The nearest odd integers are $1$ and $-1$, so the decision is $1 - 1j$, with the label 0111. The squared distance to its point $(1 - j)/\sqrt{10}$ is 0.0473; the next nearest points, with the labels 0011 and 0101, are at 0.2148 and 0.3003.

**Error rates.** 16-QAM has $\mathrm{SER} = 0.22203$ at $E_s/N_0 = 10$ dB, $0.017782$ at 15 dB and $1.1616 \times 10^{-5}$ at 20 dB. 64-QAM has $0.34762$ at 15 dB and $0.050270$ at 20 dB. At $E_b/N_0 = 10$ dB, which is $E_s/N_0 = 16.02$ dB for 16-QAM, the exact Gray bit error rate is $1.7542 \times 10^{-3}$ and $\mathrm{SER}/4 = 1.7511 \times 10^{-3}$.

**4-QAM is QPSK.** With $M = 4$ the grid is $(\pm 1 \pm j)/\sqrt{2}$, the same points as QPSK with the offset $\pi/4$. Its labeling here (in-phase bit, then quadrature bit) differs from the labeling around the circle on the [PSK](/phase-shift-keying/) page.

**Uses.** QAM is the main modulation of high-rate links with a good SNR: Wi-Fi and cellular systems use QAM on [OFDM](/orthogonal-frequency-division-multiplexing/) subcarriers, from 16 points up to 1024 or 4096, and choose the order by [adaptive modulation](/adaptive-modulation/). Cable modems, microwave links and coherent optical links also use large QAM.

**Non-example: APSK.** Points on concentric circles, as in [APSK](/amplitude-and-phase-shift-keying/), also change both amplitude and phase, but they are not a grid, and the detector cannot slice the two axes separately.

## Related definitions

- **PAM.** Each axis of square QAM is an $L$-PAM signal; see [pulse amplitude modulation](/pulse-amplitude-modulation/).
- **Lattice view.** Square QAM is a finite, shifted part of the lattice $\mathbb{Z}^2$; see [lattice](/lattice/) and [signal constellation](/signal-constellation/).
- **Shaping.** [Probabilistic constellation shaping](/probabilistic-constellation-shaping/) sends the inner points of a large QAM grid more often to save energy.
- **Coded modulation.** [Bit-interleaved coded modulation](/bit-interleaved-coded-modulation/) and [trellis-coded modulation](/trellis-coded-modulation/) combine QAM with a channel code; the bits come out of the detector through [soft demapping](/soft-demapping/).

## References
