---
tag: KRGT01
kind: technique
slug: discrete-multitone
name: Discrete multitone
aliases:
- DMT modulation
area: communications/ofdm-and-multicarrier
level: core
summary: "Baseband OFDM: Hermitian symmetry makes the IFFT output real, and each tone carries as many bits as its measured SNR allows, as on DSL telephone lines."
prereqs: [orthogonal-frequency-division-multiplexing, cyclic-prefix, quadrature-amplitude-modulation, discrete-fourier-transform]
see_also: [bit-loading, snr-gap-approximation, water-filling-power-allocation, chow-cioffi-bingham-algorithm, levin-campello-algorithm, peak-to-average-power-ratio, frequency-domain-equalization, shannon-hartley-theorem]
sources:
  - paper: doi:10.1109/35.54342
    title: "J. A. C. Bingham, Multicarrier modulation for data transmission: an idea whose time has come, IEEE Communications Magazine 28(5), 1990"
    locator: "pages 5 to 14 (multicarrier modulation by the FFT, the loading of bits and power per subchannel, and its use on telephone lines)"
  - paper: doi:10.1109/49.93100
    title: "J. S. Chow, J. C. Tu and J. M. Cioffi, A discrete multitone transceiver system for HDSL applications, IEEE Journal on Selected Areas in Communications 9(6), 1991"
    locator: "pages 895 to 908 (a DMT transceiver for digital subscriber lines)"
  - book: isbn:9780521837163
    title: "Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005"
    locator: "Chapter 12, Multicarrier Modulation"
---

Discrete multitone (DMT) is [OFDM](/orthogonal-frequency-division-multiplexing/) for a real baseband channel such as a telephone pair. Two changes adapt OFDM to it. First, the transmitter fills the upper half of the IFFT input with the complex conjugates of the lower half, $X[N - k] = X[k]^*$, and sets $X[0] = X[N/2] = 0$. This Hermitian symmetry makes the IFFT output real, so it goes straight to a digital to analog converter without a carrier. Second, the channel stays the same for a long time, so the receiver measures the SNR of each tone and tells the transmitter how many bits to put on it: many bits on tones with a high SNR, few or none on tones in a deep notch or under noise. A [cyclic prefix](/cyclic-prefix/) longer than the channel response turns the line into $N/2 - 1$ independent tones, each with one complex gain, as in OFDM. DMT is the modulation of ADSL and VDSL.

## In plain words

A telephone wire carries a real voltage, not the pair of signals that a radio sends on a carrier. DMT still uses the FFT trick of OFDM, but it fills the input so that the mirror half is the conjugate of the first half. Then the imaginary parts cancel, and the output is a plain real signal. The wire is different at every frequency: low frequencies get through well, high ones are weak, and some bands have noise from radios or other lines. Because the wire changes slowly, the modem can measure each tone and then load each tone with just as many bits as it can carry safely. Good tones carry big constellations, bad tones carry small ones, and the worst tones carry nothing.

## When it applies

- The channel is real and at baseband, or the modulation must be real for another reason, such as an optical intensity that cannot be negative or complex.
- The channel is frequency selective, with an impulse response that a cyclic prefix of acceptable length can cover, or that a short time-domain filter can shorten to that length.
- The channel and the noise change slowly against the time it takes to measure the SNR per tone and send the bit table back to the transmitter, as on wires.
- A return path exists for the bit table. Without it, use OFDM with the same constellation on all tones and coding across them.

## The template

Take an even FFT size $N$, a prefix of $N_{cp}$ samples, the measured SNR per tone $\text{SNR}[k]$ at the planned power, and the gap $\Gamma$, the factor by which a practical QAM system with a target error rate falls short of capacity.

```pseudo id=main
DMT-LINK(data, SNR, Γ, N, N_cp)
L1  for k ← 1 to N/2 - 1: b[k] ← ⌊log2(1 + SNR[k] / Γ)⌋
L2  for each symbol: for k ← 1 to N/2 - 1: X[k] ← the next b[k] bits as a point of 2^b[k]-QAM (zero if b[k] = 0)
L3      X[0] ← 0; X[N/2] ← 0; for k ← 1 to N/2 - 1: X[N - k] ← conj(X[k])
L4      x ← IFFT(X), a real vector of N samples
L5      send the last N_cp samples of x and then x
L6  receiver: drop the prefix, Y ← FFT(y), and for k ← 1 to N/2 - 1 decide X[k] from Y[k] / H[k] in 2^b[k]-QAM
```

The holes are the loading rule of line L1 (the gap rule here, or an exact greedy rule), the constellations of line L2 (square and cross QAM, often with a smallest size of 2 bits), the coding before line L2 and the way the receiver gets $H[k]$ in line L6, usually from a known training sequence during startup.

**Why the output of line L4 is real.** With the unitary pair of the OFDM page, $x[n] = \frac{1}{\sqrt N} \sum_k X[k] e^{j 2\pi k n / N}$. Under line L3, the terms $k$ and $N - k$ are complex conjugates of each other, because $e^{j 2\pi (N - k) n / N} = e^{-j 2\pi k n / N}$. So $x[n] = \frac{2}{\sqrt N} \sum_{k=1}^{N/2-1} \operatorname{Re}\left( X[k] e^{j 2\pi k n / N} \right)$, a sum of real cosine waves, one per tone. $X[0]$ and $X[N/2]$ must be real for a real output; DMT sets them to zero, because a telephone line does not pass DC and the tone $N/2$ has no quadrature part.

**Why the receiver can use only half the tones.** The channel taps are real, so $H[N - k] = H[k]^*$, and without noise $Y[N - k] = Y[k]^*$. The upper half repeats the lower half, and the receiver decides from $k = 1, \ldots, N/2 - 1$ only.

## Classic examples

**A small symbol.** Take $N = 8$, $X[1] = 1 + j$, $X[2] = 3 - j$ and $X[3] = -1 + j$. Line L3 sets $X[7] = 1 - j$, $X[6] = 3 + j$, $X[5] = -1 - j$ and $X[0] = X[4] = 0$. Line L4 gives $x = (2.1213, 0.7071, -2.1213, -2.7071, 2.1213, 0.7071, -2.1213, 1.2929)$, with imaginary parts below $4 \times 10^{-15}$, the rounding of floating point arithmetic. The energy is $28$ in both domains: $2(|1 + j|^2 + |3 - j|^2 + |-1 + j|^2) = 28$.

**Bit loading by the gap.** With $\Gamma = 9.8$ dB, the gap often used for uncoded QAM at a symbol error rate of $10^{-7}$, tones with an SNR of 40, 30, 20, 10 and 3 dB get $\log_2(1 + \text{SNR}/\Gamma) = 10.03$, $6.72$, $3.52$, $1.03$ and $0.27$ bits, so line L1 loads 10, 6, 3, 1 and 0 bits. The tone at 3 dB carries nothing, and the five tones carry 20 bits per DMT symbol.

**ADSL.** ADSL uses 256 tones spaced 4.3125 kHz apart, an IFFT of 512 points at 2.208 MHz downstream and a prefix of 32 samples, so a DMT symbol takes 544 samples and the rate is $2.208\ \text{MHz} / 544 = 4058.8$ symbols per second. One symbol in 69 is a synchronization symbol, which leaves exactly 4000 data symbols per second. A tone carries up to 15 bits. The lowest tones are left empty for the analog telephone service on the same pair.

**VDSL2.** VDSL2 keeps the tone spacing of 4.3125 kHz in most profiles and uses thousands of tones up to tens of MHz on short lines.

## Variations

- **Exact loading.** The gap rule of line L1 rounds down each tone separately and wastes power. Greedy algorithms add one bit at a time where it costs the least power, and give the best integer table for a power or a rate target.
- **Power shaping.** Water filling puts more power on good tones. On DSL the gain over flat power is small because spectral masks limit the power per tone, so loading of bits matters more than loading of power.
- **Time-domain equalizer.** When the line response is longer than the prefix, a short FIR filter before the FFT shortens the response to fit the prefix. Early DMT modems used this instead of a longer prefix.
- **Bit swapping.** During operation, the receiver moves bits from tones whose SNR has dropped to tones with margin, without stopping the link.
- **Optical DMT.** Intensity-modulated optical links use the same Hermitian symmetry and add a DC bias or clip the negative samples, because light intensity cannot be negative.
- **Zipper and frequency-division duplexing.** Upstream and downstream use separate sets of tones, so one IFFT size serves both directions with no analog filters between them.

## Pitfalls

- **Forgetting the conjugate.** If line L3 sets $X[N - k] = X[k]$ instead of $X[k]^*$, the output is complex, and taking its real part throws away half of each tone and mixes it with its mirror.
- **Using the wrong index for the mirror.** The mirror of $k$ is $N - k$, not $N - 1 - k$. An off-by-one mirror also makes the output complex.
- **Non-real DC or middle tone.** $X[0]$ and $X[N/2]$ must be real; a complex value there makes the output complex. DMT leaves them empty.
- **A stale bit table.** A loading computed during startup fails when crosstalk from a new line or radio noise raises the noise on some tones later. Keep a margin, and swap bits when the SNR changes.
- **Loading at the SNR without the gap.** Using $\log_2(1 + \text{SNR})$ in line L1 loads more bits than QAM can carry at the target error rate; the error rate on every tone is then far too high.
- **Peaks.** A DMT symbol is a sum of many cosines and has a high peak to average power ratio, which needs a linear line driver and converters with enough range.

## Exercises

1. Show that $X[N - k] = X[k]^*$ for $k = 1, \ldots, N/2 - 1$, with real $X[0]$ and $X[N/2]$, is necessary and sufficient for a real IFFT output.
2. For $N = 8$ with only $X[1] = 1$ nonzero apart from its mirror, compute $x$ and show that it is a sampled cosine with amplitude $2/\sqrt 8$.
3. Tones have the SNRs 35, 28, 21, 14 and 7 dB. Compute the loading of line L1 with $\Gamma = 9.8$ dB and the number of bits per DMT symbol.
4. Show that a real channel has $H[N - k] = H[k]^*$, and that the receiver loses nothing by discarding the upper half of the FFT output.
5. Check from the ADSL numbers that 32 prefix samples at 2.208 MHz cover a response of about 14.5 µs, and compute the fraction of the rate the prefix costs.

## References
