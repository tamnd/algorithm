---
tag: K6ED83
kind: definition
slug: signal-constellation
name: Signal constellation
aliases:
- constellation diagram
area: communications/modulation-and-detection
level: intro
summary: The finite set of points in signal space, each a symbol, that a modulation scheme can send, with its labeling by bits.
prereqs: [signal-space-representation]
see_also: [pulse-amplitude-modulation, phase-shift-keying, quadrature-amplitude-modulation, amplitude-and-phase-shift-keying, gray-labeling, minimum-distance-detector, probabilistic-constellation-shaping, lattice]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 3.2, Memoryless Modulation Methods (the signal space diagrams of PAM, PSK and QAM), and Section 4.7, Lattices and Constellations Based on Lattices
  - book: isbn:9780792375487
    title: John R. Barry, Edward A. Lee and David G. Messerschmitt, Digital Communication, third edition, Kluwer Academic Publishers, 2004
    locator: Chapter 5, Pulse-Amplitude Modulation (the alphabet and its constellation), and Chapter 6, Advanced Modulation
  - paper: doi:10.1109/18.720542
    title: G. David Forney Jr. and Gottfried Ungerboeck, Modulation and coding for linear Gaussian channels, IEEE Transactions on Information Theory 44(6), 2384-2415, 1998
    locator: the parts on constellations for the band-limited Gaussian channel, coding gain and shaping gain, including the ultimate shaping gain of 1.53 dB
---

A signal constellation is the finite set of points in [signal space](/signal-space-representation/) that a modulation scheme can send, one point per symbol, together with the map from bit groups to points. [Digital modulation](/digital-modulation/) is the general idea and the signal space representation is the geometry; the constellation is the concrete point set. [PAM](/pulse-amplitude-modulation/), [PSK](/phase-shift-keying/) and [QAM](/quadrature-amplitude-modulation/) are particular constellations, each with its own page.

## Definition

A **signal constellation** is a finite set $\mathcal{A} = \{a_0, \ldots, a_{M-1}\}$ of $M \ge 2$ distinct points in $\mathbb{C}^n$ (or $\mathbb{R}^N$), with a probability $\pi_i$ for each point. Unless a page says otherwise, the points are equally likely, $\pi_i = 1/M$. When $M = 2^k$, a **labeling** is a bijection from the bit strings of length $k$ to the points; the area pages index the points by their label, $a_i$ being the point labeled with the binary form of $i$.

The quantities that describe a constellation are:

- the **average symbol energy** $E_s = \sum_i \pi_i |a_i|^2$, and the **energy per bit** $E_b = E_s / \log_2 M$ before any channel code;
- the **minimum distance** $d_{\min} = \min_{i \ne k} |a_i - a_k|$, and the *normalized* value $d_{\min}^2 / E_s$, which does not change when the constellation is scaled;
- the **average number of nearest neighbors** $\bar N_{\min}$, the mean over $i$ of the number of points at distance $d_{\min}$ from $a_i$;
- the **peak-to-average power ratio** $\max_i |a_i|^2 / E_s$;
- the **dimension**, the number of real dimensions that the points span.

In code on this site, constellations are scaled to $E_s = 1$. With that scale, the [symbol error rate](/symbol-error-rate/) at high SNR depends on the constellation mainly through $d_{\min}^2/E_s$ and $\bar N_{\min}$: it is about $\bar N_{\min}\, Q\big(\sqrt{(d_{\min}^2/E_s)(E_s/N_0)/2}\big)$ in complex AWGN of density $N_0$.

**Two facts about energy.**

1. *Theorem.* Translating the points does not change any distance, and the average energy is smallest when the mean $\bar a = \sum_i \pi_i a_i$ is zero. *Proof:* $\sum_i \pi_i |a_i - c|^2 = \sum_i \pi_i |a_i - \bar a|^2 + |\bar a - c|^2$, which is smallest at $c = \bar a$. $\square$ So a constellation with a nonzero mean wastes the energy $|\bar a|^2$ on a component that carries no information.
2. *Theorem.* A rotation, a reflection or a unitary map of the constellation does not change its distances or its energy. In noise that is circularly symmetric, such as $\mathcal{CN}(0, N_0 I)$, the error rate of the optimal detector is the same for the rotated constellation.

## Examples and non-examples

**Standard constellations.** All values are for equally likely points; the formulas are on the format pages.

| Constellation | $M$ | $d_{\min}^2 / E_s$ | $\bar N_{\min}$ | peak-to-average |
|---|---|---|---|---|
| BPSK ($\pm 1$) | 2 | 4 | 1 | 1 (0 dB) |
| QPSK | 4 | 2 | 2 | 1 (0 dB) |
| 8-PSK | 8 | 0.5858 | 2 | 1 (0 dB) |
| 16-PSK | 16 | 0.1522 | 2 | 1 (0 dB) |
| 4-PAM | 4 | 0.8 | 1.5 | 1.8 (2.55 dB) |
| 16-QAM | 16 | 0.4 | 3 | 1.8 (2.55 dB) |
| 64-QAM | 64 | 0.0952 | 3.5 | 2.333 (3.68 dB) |

16-QAM and 16-PSK both carry 4 bits per symbol, but 16-QAM has $d_{\min}^2/E_s$ larger by a factor of $0.4/0.1522 = 2.63$, which is 4.2 dB. That is why QAM, not PSK, is used for 16 points and more, unless a constant envelope is needed.

**16-QAM with its labeling.** The raw points (before scaling by $1/\sqrt{10}$) are $\pm 1, \pm 3$ on each axis. The first two bits give the in-phase level and the last two the quadrature level, each by the Gray map $00 \to +3$, $01 \to +1$, $11 \to -1$, $10 \to -3$. So the label 0000 is $3 + 3j$, 0111 is $1 - 1j$ and 1111 is $-1 - 1j$. The raw energy is 10, so the scaled points have $E_s = 1$. The [Gray labeling](/gray-labeling/) page explains why neighbors get labels that differ in one bit.

**Non-uniform probabilities.** In [probabilistic constellation shaping](/probabilistic-constellation-shaping/), the inner points of a QAM grid are sent more often than the outer ones. It is still a constellation; $E_s$ is the weighted mean, and it falls for the same set of points.

**Non-example: points that coincide.** A list with two equal points is not a constellation in this sense, because no receiver can tell those two symbols apart. A labeling of it cannot be decoded without errors even with no noise.

**Non-example: a Gaussian input.** The input that achieves the capacity of the AWGN channel is a continuous Gaussian distribution. It has no finite point set, so it is not a constellation. Large QAM constellations with shaping approach it. At high rates, shaping can save at most the factor $\pi e/6$ in energy over a uniform square grid, which is 1.53 dB; Forney and Ungerboeck call this the ultimate shaping gain.

## Related definitions

- **Signal space.** The constellation is a point set in the [signal space representation](/signal-space-representation/), and the transmitted waveform is $\sum_n x_n g(t - nT)$ with each $x_n \in \mathcal{A}$.
- **Formats.** [Pulse amplitude modulation](/pulse-amplitude-modulation/) uses equally spaced points on a line, [phase-shift keying](/phase-shift-keying/) equally spaced points on a circle, [quadrature amplitude modulation](/quadrature-amplitude-modulation/) a square grid, and [amplitude and phase-shift keying](/amplitude-and-phase-shift-keying/) concentric rings.
- **Labeling.** A [Gray labeling](/gray-labeling/) gives labels that differ in one bit to every pair of nearest neighbors, which keeps the [bit error rate](/bit-error-rate/) close to the symbol error rate divided by $\log_2 M$.
- **Decision regions.** The [minimum distance detector](/minimum-distance-detector/) splits the plane into the Voronoi cells of the points (see [Voronoi diagram](/voronoi-diagram/)).
- **Lattice constellations.** A finite part of a [lattice](/lattice/) inside a bounding region; square QAM is a part of the lattice $\mathbb{Z}^2$, scaled and shifted.

## References
