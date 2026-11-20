---
tag: JNJ2KK
kind: definition
slug: minimum-shift-keying
name: Minimum-shift keying
aliases:
- MSK
area: communications/modulation-and-detection
level: core
summary: Binary CPM with rectangular frequency pulses and modulation index 1/2, the smallest tone spacing that keeps the two tones orthogonal for a coherent receiver.
prereqs: [continuous-phase-modulation, frequency-shift-keying, offset-qpsk]
see_also: [gaussian-minimum-shift-keying, offset-qpsk, laurent-decomposition, continuous-phase-modulation, frequency-shift-keying, power-spectral-density, phase-shift-keying, differential-phase-shift-keying]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Chapter 3 (minimum-shift keying as continuous-phase FSK with h = 1/2, its representation as offset QPSK with half-sine pulses, and its power spectrum)
  - book: isbn:9780306421952
    title: John B. Anderson, Tor Aulin and Carl-Erik Sundberg, Digital Phase Modulation, Plenum Press, 1986
    locator: the treatment of full-response CPM with rectangular pulses, of which MSK is the case h = 1/2
  - paper: doi:10.1109/TCOM.1986.1096504
    title: Pierre A. Laurent, Exact and approximate construction of digital phase modulations by superposition of amplitude modulated pulses (AMP), IEEE Transactions on Communications 34(2), 150-160, 1986
    locator: the binary CPM decomposition, whose single pulse for MSK is the half-sine pulse of length 2T
---

Minimum-shift keying (MSK) is binary [continuous phase modulation](/continuous-phase-modulation/) with a rectangular frequency pulse of one symbol and modulation index $h = 1/2$. Each bit turns the carrier phase by $+\pi/2$ or $-\pi/2$ along a straight line, so the signal is a tone at $f_c + 1/(4T)$ or $f_c - 1/(4T)$ with no phase jump. The tone spacing $1/(2T)$ is the smallest that keeps two [FSK](/frequency-shift-keying/) tones orthogonal for a coherent receiver, which gives the name. The same signal is [offset QPSK](/offset-qpsk/) with half-sine pulses, so MSK is both a constant-envelope CPM and a linear modulation. [Gaussian MSK](/gaussian-minimum-shift-keying/) smooths its frequency pulse to narrow the spectrum.

## Definition

Let $T$ be the bit period, $E_b$ the energy per bit and $a_n \in \{+1, -1\}$ the data. The **MSK signal** in complex baseband is $s(t) = \sqrt{E_b/T}\, e^{j\phi(t)}$, where $j$ is the imaginary unit and

$$\phi(t) = \frac{\pi}{2}\sum_{i < n} a_i + \frac{\pi}{2}\, a_n\, \frac{t - nT}{T}, \qquad nT \le t < (n + 1)T.$$

This is CPM with $M = 2$, $L = 1$, $g(t) = 1/(2T)$ on $[0, T]$ and $h = 1/2$. The instantaneous frequency is $a_n/(4T)$, so the two tones are $1/(2T)$ apart. At the bit boundaries the phase is a multiple of $\pi/2$, and the phase trellis has the four states $0, \pi/2, \pi, 3\pi/2$.

**MSK as offset QPSK.** Let $p(t) = \sin(\pi t/(2T))$ for $0 \le t \le 2T$ and $0$ otherwise, the half-sine pulse of length $2T$. Put $A_n = \sum_{i \le n} a_i$, with the first symbol at $i = 0$. Then, exactly,

$$e^{j\phi(t)} = \sum_{n} j^{A_n}\, p(t - nT).$$

The exponent $A_n$ is odd for even $n$ and even for odd $n$, so the weights $j^{A_n}$ are imaginary and real in turn. Each pulse lasts $2T$ and the real and imaginary pulses are offset by $T$, which is offset QPSK with half-sine pulses at a rate of one symbol each $2T$ on each axis. If we write $j^{A_n} = j^{n+1} d_n$ with $d_n \in \{+1, -1\}$, then $d_n = d_{n-1}\, a_n$: the OQPSK symbols are a differential encoding of the MSK bits. This identity is the one-pulse case of the [Laurent decomposition](/laurent-decomposition/). The envelope is constant because at each instant one real and one imaginary half-sine overlap, and $\sin^2 + \cos^2 = 1$.

**Spectrum.** For independent equally likely bits, the power spectral density of the complex envelope is proportional to

$$S(f) \propto \left(\frac{\cos(2\pi f T)}{1 - 16 f^2 T^2}\right)^2.$$

The first null is at $|f| = 3/(4T)$, the main lobe holds $99.5\%$ of the power, and the side lobes fall as $f^{-4}$. Offset QPSK and QPSK with rectangular pulses have their first null at $|f| = 1/(2T)$, but their side lobes fall only as $f^{-2}$.

**Coherent detection.** A receiver that knows the carrier phase filters each axis with the half-sine pulse over $2T$ and decides $d_n$ from the sign. The two axes do not interfere. Each symbol $d_n$ has the energy $(E_b/T)\int_0^{2T}\sin^2(\pi t/(2T))\, dt = E_b$ and the two values are antipodal, so $P(d_n \text{ wrong}) = Q(\sqrt{2E_b/N_0})$, the value of BPSK. If the data is the MSK bits $a_n = d_n d_{n-1}$, each wrong $d_n$ spoils two bits and $P_b = 2p(1 - p)$ with $p = Q(\sqrt{2E_b/N_0})$. Transmitters that want the BPSK error rate on the data precode it, so that $d_n$ is the data bit.

## Examples and non-examples

**A short phase path.** The bits $+1, -1, -1, +1$ take the phase from $0$ to $\pi/2$, back to $0$, to $-\pi/2$ and back to $0$, each time along a line. With $T = 1\ \mu$s the tones are at $f_c \pm 250$ kHz.

**The weights of the OQPSK form.** For the same bits, $A_0, A_1, A_2, A_3 = 1, 0, -1, 0$, so the weights $j^{A_n}$ are $j, 1, -j, 1$: imaginary, real, imaginary, real. The OQPSK symbols are $d_n = j^{A_n - n - 1} = 1, -1, 1, 1$, and indeed $d_n d_{n-1}$ gives back $-1, -1, 1$ for $n = 1, 2, 3$.

**Bandwidth in numbers.** For MSK, $99\%$ of the power lies in $|f| \le 0.59/T$, a total width of $1.18/T$. QPSK with rectangular pulses at the same bit rate needs a total width of about $10.3/T$ for $99\%$, because of its slow side lobes, although its main lobe is narrower.

**Non-example: binary FSK with $h = 1/2$ and phase jumps.** If each tone comes from a separate oscillator, the tones are still orthogonal for a coherent receiver, but the phase jumps at the bit boundaries. The signal is not MSK and its spectrum falls as $f^{-2}$.

**Non-example: QPSK with half-sine pulses and no offset.** Without the offset of $T$, both axes change sign at the same instants, the envelope goes to zero there, and the signal is not constant-envelope.

## Related definitions

- [Continuous phase modulation](/continuous-phase-modulation/): the family; MSK is its case $M = 2$, 1REC, $h = 1/2$.
- [Offset QPSK](/offset-qpsk/): MSK is OQPSK with half-sine pulses and differentially encoded data.
- [Gaussian minimum-shift keying](/gaussian-minimum-shift-keying/): MSK with a Gaussian-filtered frequency pulse, used in GSM.
- [Frequency-shift keying](/frequency-shift-keying/): MSK is binary FSK at the smallest coherent spacing, with continuous phase.
- [Laurent decomposition](/laurent-decomposition/): for MSK it has exactly one pulse, the half-sine.
- [Differential phase-shift keying](/differential-phase-shift-keying/): another place where data is carried by phase changes; MSK bits are the products of consecutive OQPSK symbols.

## References
