---
tag: HPEG9T
kind: definition
slug: offset-qpsk
name: Offset QPSK
aliases:
- OQPSK
- staggered QPSK
area: communications/modulation-and-detection
level: core
summary: "QPSK with the quadrature stream delayed by half a symbol, so the phase never jumps by 180 degrees and the envelope of the filtered signal stays away from zero."
prereqs: [phase-shift-keying, pulse-shaping]
see_also: [phase-shift-keying, pulse-shaping, root-raised-cosine-filter, minimum-shift-keying, peak-to-average-power-ratio, quadrature-amplitude-modulation, differential-phase-shift-keying, continuous-phase-modulation]
sources:
  - paper: doi:10.1109/TCOM.1976.1093392
    title: Steven A. Gronemeyer and Alan L. McBride, MSK and offset QPSK modulation, IEEE Transactions on Communications 24(8), 1976
    locator: pp. 809 to 820 (offset QPSK and MSK as the same structure with a rectangular and a half-sine pulse, their spectra, and their behavior after band limiting and a hard limiter)
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Chapter 3 (digital modulation schemes, including offset QPSK and its relation to MSK)
---

Offset QPSK (OQPSK) is QPSK in which the quadrature component is delayed by half a symbol period against the in-phase component. The two components then never change at the same instant, so the phase of the signal moves by at most $90$ degrees at a time and never by $180$ degrees. After a band-limiting filter, the envelope of QPSK falls close to zero at each $180$ degree step, while the envelope of OQPSK stays well away from zero. This matters when a nonlinear amplifier would otherwise spread the filtered spectrum again. The spectrum and the error rate in white noise are the same as for QPSK.

## Definition

Let $T$ be the symbol period, $g(t)$ a real pulse with unit energy, and let the bits be grouped in pairs $(b_{2k}, b_{2k+1})$. Map them to the levels $a_{I,k} = (1 - 2b_{2k})/\sqrt2$ and $a_{Q,k} = (1 - 2b_{2k+1})/\sqrt2$, so that each symbol has energy $E_s = 1$ and each bit $E_b = 1/2$. The **offset QPSK** signal in complex baseband is

$$s(t) = \sum_k a_{I,k}\, g(t - kT) + j \sum_k a_{Q,k}\, g\!\left(t - kT - \frac{T}{2}\right),$$

where $j$ is the imaginary unit. On a carrier of frequency $f_c$ it is $\mathrm{Re}\{s(t) e^{j2\pi f_c t}\}$. Plain QPSK is the same formula without the delay $T/2$; it is [PSK](/phase-shift-keying/) with $4$ points at the phases $\pi/4 + k\pi/2$.

**Properties.**
- *No 180 degree steps.* With a rectangular pulse of length $T$, the in-phase level can change only at $t = kT$ and the quadrature level only at $t = kT + T/2$. At each instant only one sign flips, which moves the point to a neighbor at $\pm 90$ degrees. In QPSK both signs can flip at once, which moves the point to the opposite side: a $180$ degree step through the origin.
- *The envelope after filtering.* With a smooth pulse, such as a [root-raised-cosine filter](/root-raised-cosine-filter/), a $180$ degree step of QPSK makes the signal pass near $0$. In OQPSK one component is at its peak while the other changes, so the envelope stays away from $0$ and varies less. A smaller range of the envelope means less regrowth of the spectrum in a nonlinear amplifier.
- *Same spectrum.* The two components carry independent data, so the power spectral density is the sum of theirs, and a delay of one component does not change its spectrum. OQPSK has the spectrum of QPSK with the same pulse: $|G(f)|^2/T$ up to a constant.
- *Same error rate.* The receiver applies the [matched filter](/matched-filter/) and samples the in-phase part at $kT$ and the quadrature part at $kT + T/2$, each after the delay of the filters. With a pulse whose matched pair is a Nyquist pulse, each component is a binary decision in white noise, and the bit error rate is $Q(\sqrt{2E_b/N_0})$, as for QPSK, with $Q$ the [Gaussian Q function](/gaussian-q-function/).
- *Constant envelope with a half-sine pulse.* With $g(t) = \sin(\pi t/T)$ on $0 \le t \le T$, the two components satisfy $\sin^2 + \cos^2 = 1$ at every instant, and the signal has a constant amplitude. This is [minimum-shift keying](/minimum-shift-keying/), whose bit period is $T/2$.

### The modulator and the receiver

```pseudo id=main
OQPSK-MODULATE(b_0, ..., b_{2N-1}, g, L_s)   ▷ L_s even, g the taps of the pulse at L_s per T
L1  a_I[k] ← (1 - 2 b_{2k})/√2,  a_Q[k] ← (1 - 2 b_{2k+1})/√2
L2  s ← Σ_k a_I[k] · g shifted by k·L_s samples
L3  s ← s + j · Σ_k a_Q[k] · g shifted by k·L_s + L_s/2 samples   ▷ the offset of T/2
L4  return s

OQPSK-RECEIVE(r, g, L_s, N)
L5  z ← r filtered with the time-reversed taps of g; D ← len(g) - 1
L6  b̂_{2k} ← [Re z[k·L_s + D] < 0]
L7  b̂_{2k+1} ← [Im z[k·L_s + L_s/2 + D] < 0]   ▷ the quadrature part, half a symbol later
L8  phase step between the middles of two half-symbol intervals: arg(s[m′] · conj(s[m]))
```

The tests build both signals with a rectangular pulse and with an RRC pulse at $L_s = 8$, check that OQPSK has only steps of $0$ and $\pm 90$ degrees while QPSK also has steps of $180$ degrees, check the envelope numbers below, and recover the bits through the matched filter.

## Examples and non-examples

**A sequence by hand.** Take the bit pairs $00, 11, 10$. The levels (times $\sqrt2$) are $I = +1, -1, -1$ and $Q = +1, -1, +1$. In QPSK the point goes from $(+,+)$ to $(-,-)$ at $t = T$: a $180$ degree step. In OQPSK, at $t = T$ only $I$ changes, to $(-,+)$, a $90$ degree step; at $t = 3T/2$ the $Q$ part changes, to $(-,-)$, another $90$ degree step. At $t = 2T$ the $I$ part stays at $-1$, and at $t = 5T/2$ the $Q$ part changes to $+1$: one more step of $90$ degrees.

**Envelope with RRC pulses.** With $\beta = 0.5$, $L_s = 8$, filters of $8$ symbols on each side, and $1500$ random symbols (seed $7$ in the tests), the envelope of QPSK ranges from $0.0016$ to $1.46$ times its rms value, and the envelope of OQPSK from $0.57$ to $1.40$ times its rms value. The peaks hardly change; the deep dips of QPSK are gone.

**Where it is used.** The 2.4 GHz physical layer of IEEE 802.15.4 sends OQPSK with half-sine pulses, which is MSK in another form. The reverse link of IS-95 CDMA used OQPSK so that the handset amplifier could run close to saturation.

**Non-example: pi/4-QPSK.** This scheme alternates between two QPSK constellations rotated by $45$ degrees, so that every step is $\pm 45$ or $\pm 135$ degrees. It also avoids the step through the origin, but both components change at the same instants and there is no offset in time. It is often detected differentially, as in [differential phase-shift keying](/differential-phase-shift-keying/).

**Non-example: offset 16-QAM.** Delaying the quadrature part of 16-QAM by $T/2$ (offset QAM) keeps the data rate, but the levels of each component still pass near zero, so the gain in envelope is smaller. It is used in filter-bank multicarrier systems for reasons of orthogonality, not for the envelope.

## Related definitions

- [Phase-shift keying](/phase-shift-keying/) and [QAM](/quadrature-amplitude-modulation/): QPSK is 4-PSK and 4-QAM; OQPSK is the same constellation with staggered timing.
- [Minimum-shift keying](/minimum-shift-keying/): OQPSK with a half-sine pulse of length $T$, two bit periods, a form of [continuous-phase modulation](/continuous-phase-modulation/) with a constant envelope.
- [Pulse shaping](/pulse-shaping/) and the [root-raised-cosine filter](/root-raised-cosine-filter/): the usual pulse; the offset does not change the matched filter.
- [Peak-to-average power ratio](/peak-to-average-power-ratio/): the measure of the envelope that OQPSK improves at the low end.

## References
