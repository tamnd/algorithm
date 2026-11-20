---
tag: D1QPK7
kind: concept
slug: digital-modulation
name: Digital modulation
aliases:
- digital modulation scheme
area: communications/modulation-and-detection
level: intro
summary: The mapping of a stream of bits onto a set of analog waveforms that a physical channel can carry.
prereqs: [additive-white-gaussian-noise-channel]
see_also: [signal-space-representation, signal-constellation, symbol-detection, spectral-efficiency, energy-per-bit-to-noise-density-ratio, pulse-shaping, bit-error-rate, shannon-hartley-theorem]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Chapter 3, Digital Modulation Schemes (Section 3.1 on the representation of digitally modulated signals and Section 3.2 on memoryless modulation methods), and Section 4.6, A Comparison of Digital Signaling Methods
  - book: isbn:9780792375487
    title: John R. Barry, Edward A. Lee and David G. Messerschmitt, Digital Communication, third edition, Kluwer Academic Publishers, 2004
    locator: Chapter 5, Pulse-Amplitude Modulation, and Chapter 6, Advanced Modulation
  - book: isbn:9780881335545
    title: John M. Wozencraft and Irwin M. Jacobs, Principles of Communication Engineering, Wiley, 1965 (reissued by Waveland Press, 1990)
    locator: Chapter 4, Optimum receiver principles (signals as vectors, and the receiver for a set of M signals in white Gaussian noise)
---

Digital modulation is the mapping of bits onto waveforms that a physical channel can carry, together with the receiver that maps the received waveform back to bits. This page is the general concept. The [signal space representation](/signal-space-representation/) gives the geometry that turns waveforms into vectors, the [signal constellation](/signal-constellation/) is the finite point set that one scheme uses, and the format pages ([PAM](/pulse-amplitude-modulation/), [PSK](/phase-shift-keying/) and [QAM](/quadrature-amplitude-modulation/)) define particular constellations. The receiver side is the [symbol detection](/symbol-detection/) problem.

## In plain words

A wire, a cable or a radio link carries smooth signals, not bits. To send bits, the sender agrees with the receiver on a small menu of signal shapes, each a short burst of a fixed length. It cuts the bit stream into groups, and for each group it sends the shape that stands for that group. A menu of 16 shapes carries 4 bits per burst.

The receiver gets each burst with noise added and picks the menu item that it most likely was. A larger menu sends more bits per burst, but its items are closer together, so noise causes more mistakes unless the sender uses more power. The whole design of a modulation scheme is a trade between three things: bits per second, the width of the frequency band, and the power needed to keep mistakes rare.

## The idea

**Symbols and waveforms.** A memoryless scheme takes $k = \log_2 M$ bits at a time and sends one of $M$ waveforms $s_0(t), \ldots, s_{M-1}(t)$, each of duration about $T$, the symbol period. The symbol rate is $R_s = 1/T$ and the bit rate is $R_b = R_s \log_2 M$ (before any channel code). Most practical schemes are *linear*: each symbol is a complex number $x$ from a finite set, and the transmitted passband signal is

$$s(t) = \mathrm{Re}\Big\{\sqrt{2} \sum_n x_n\, g(t - nT)\, e^{j 2\pi f_c t}\Big\},$$

with a pulse $g$ of unit energy and a carrier frequency $f_c$. The complex baseband signal is $\sum_n x_n g(t - nT)$, and the factor $\sqrt{2}$ makes the passband energy equal to the baseband energy. Proakis and Salehi write the same signal without the $\sqrt{2}$, so their baseband energies differ from the ones here by a factor of 2. The pulse sets the spectrum (see [pulse shaping](/pulse-shaping/)); the set of possible $x$ is the [signal constellation](/signal-constellation/).

**Kinds of schemes.** The common families differ in what the symbol changes.

- *Amplitude*: [pulse amplitude modulation](/pulse-amplitude-modulation/) uses real symbols on one axis.
- *Phase*: [phase-shift keying](/phase-shift-keying/) puts the symbols on a circle, so every symbol has the same energy.
- *Amplitude and phase*: [quadrature amplitude modulation](/quadrature-amplitude-modulation/) uses a grid in the complex plane, and [amplitude and phase-shift keying](/amplitude-and-phase-shift-keying/) uses rings.
- *Frequency*: [frequency-shift keying](/frequency-shift-keying/) uses $M$ orthogonal tones. It is not linear in the sense above, and its dimension grows with $M$.
- *With memory*: [differential phase-shift keying](/differential-phase-shift-keying/), [minimum-shift keying](/minimum-shift-keying/) and [continuous-phase modulation](/continuous-phase-modulation/) make each waveform depend on earlier symbols, for a constant envelope or for detection without a phase reference.

**The channel model.** On the [AWGN channel](/additive-white-gaussian-noise-channel/), the receiver sees $y = h x + w$ per symbol after a matched filter, with $w \sim \mathcal{CN}(0, N_0)$. The average symbol energy is $E_s = \mathbb{E}|x|^2$ and the energy per information bit is $E_b = E_s / \log_2 M$ for an uncoded scheme. The [signal space representation](/signal-space-representation/) shows why this discrete model loses nothing in white Gaussian noise.

**The three costs.** A scheme is judged by:

1. *Spectral efficiency* $\eta = R_b / B$ in bit/s/Hz, where $B$ is the occupied bandwidth. For a linear scheme with a raised cosine pulse of roll-off $\beta$, $B = (1 + \beta) R_s$ in passband, so $\eta = \log_2 M / (1 + \beta)$ (see [spectral efficiency](/spectral-efficiency/)).
2. *Power efficiency*: the [$E_b/N_0$](/energy-per-bit-to-noise-density-ratio/) needed for a target [bit error rate](/bit-error-rate/).
3. *Complexity and robustness*: the cost of the detector, and the tolerance to phase noise, to amplifier nonlinearity and to fading.

The [Shannon-Hartley theorem](/shannon-hartley-theorem/) bounds the first two together: reliable transmission at spectral efficiency $\eta$ needs $E_b/N_0 \ge (2^\eta - 1)/\eta$. As $\eta \to 0$ the bound falls to $\ln 2$, which is $-1.59$ dB.

**Bandwidth-limited and power-limited schemes.** Raising $M$ in PAM, PSK or QAM raises $\eta$ but needs more $E_b/N_0$, because the points move closer together for the same energy per bit. Raising $M$ in orthogonal FSK lowers the $E_b/N_0$ needed but uses more bandwidth. Proakis and Salehi treat the first group as band-limited signaling and the second as power-limited signaling (Sections 4.3 and 4.4).

## Examples

**Bit rate and bandwidth.** 16-QAM at $R_s = 1$ Msymbol/s carries $R_b = 4$ Mbit/s. With a raised cosine pulse of roll-off $\beta = 0.25$, the passband bandwidth is $1.25$ MHz, so $\eta = 3.2$ bit/s/Hz.

**The cost of more bits per symbol.** The table gives the $E_b/N_0$ that uncoded Gray-labeled schemes need for $P_b = 10^{-5}$ in AWGN, computed from the exact symbol error rate with $P_b \approx \mathrm{SER}/\log_2 M$. The last column is the Shannon bound $(2^\eta - 1)/\eta$ at the ideal spectral efficiency $\eta = \log_2 M$ (with $\beta = 0$).

| Scheme | bits per symbol | $E_b/N_0$ for $P_b = 10^{-5}$ | Shannon bound at $\eta = \log_2 M$ |
|---|---|---|---|
| BPSK | 1 | 9.59 dB | 0 dB |
| QPSK | 2 | 9.59 dB | 1.76 dB |
| 8-PSK | 3 | 12.97 dB | 3.68 dB |
| 16-QAM | 4 | 13.44 dB | 5.74 dB |
| 16-PSK | 4 | 17.44 dB | 5.74 dB |
| 64-QAM | 6 | 17.79 dB | 10.21 dB |

QPSK carries twice the bits of BPSK in the same bandwidth at the same $E_b/N_0$, because it uses the second (quadrature) dimension. Beyond 4 points every doubling of $M$ costs power. QAM needs about 4 dB less than PSK at 16 points, because its points fill the plane better. The gap of 7 to 8 dB to the Shannon bound is what channel codes recover.

**Non-example.** Analog frequency modulation of a voice signal maps a continuous message onto a waveform. There is no finite symbol set and no symbol decision, so it is analog modulation, not digital modulation.

## Where it is used

Every digital link uses a modulation scheme. Wi-Fi, 4G and 5G cellular systems and cable modems use QAM on [OFDM](/orthogonal-frequency-division-multiplexing/) subcarriers and change the order of the constellation with the channel quality, which is [adaptive modulation](/adaptive-modulation/). Satellite links use PSK and APSK because their amplifiers work best near a constant envelope. GSM and Bluetooth use frequency and continuous-phase schemes for the same reason. Coherent optical links use QPSK and QAM on two polarizations. Modern systems combine the constellation with a channel code, as in [bit-interleaved coded modulation](/bit-interleaved-coded-modulation/) and [trellis-coded modulation](/trellis-coded-modulation/).

## References
