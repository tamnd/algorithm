---
tag: QN6KW8
kind: theorem
slug: radar-range-equation
name: Radar range equation
aliases:
- radar equation
area: communications/radar-waveforms
level: intro
summary: "Gives the SNR of one echo, Pt G^2 lambda^2 sigma / ((4 pi)^3 R^4 k T0 B F L), for a monostatic radar and a point target in free space. The SNR falls as the fourth power of range."
prereqs: [free-space-path-loss]
see_also: [albersheim-equation, swerling-target-models, matched-filter, pulse-compression, cfar-detection, additive-white-gaussian-noise-channel, fmcw-radar, energy-per-bit-to-noise-density-ratio]
sources:
  - book: isbn:9780072881387
    title: "Merrill I. Skolnik, Introduction to Radar Systems, third edition, McGraw-Hill, 2001"
    locator: "Chapter 2, The Radar Equation (the simple form, the receiver noise, the radar cross section and the losses)"
  - book: isbn:9780071444743
    title: "Mark A. Richards, Fundamentals of Radar Signal Processing, McGraw-Hill, 2005"
    locator: "Chapter 2, Section 2.2.1 (the radar range equation and the signal to noise ratio of a single pulse)"
---

The radar range equation gives the signal to noise ratio (SNR) of the echo of one pulse from a point target. For a monostatic radar in free space,

$$\mathrm{SNR} = \frac{P_t G^2 \lambda^2 \sigma}{(4\pi)^3 R^4\, k T_0 B F L}.$$

The power spreads over a sphere on the way out and again on the way back, so the SNR falls as $1/R^4$: twice the range costs 12.04 dB. The equation is not a theorem in the mathematical sense. It is a physical model, a closed form under stated assumptions, and it is the start of every radar design: with the SNR that a detector needs, from the [Albersheim equation](/albersheim-equation/) or the [Swerling models](/swerling-target-models/), it gives the largest range at which the radar can detect a target.

## Statement

**Assumptions.** One antenna transmits and receives (monostatic). The target is in the far field of the antenna, and the path is free space, with no multipath, no atmospheric loss beyond what $L$ includes, and no obstacles. The target is a point scatterer with radar cross section $\sigma$. The receiver noise is thermal, white over the band, at the reference temperature $T_0 = 290$ K, raised by the noise figure $F$. The echo is filtered by a filter of noise bandwidth $B$, and the signal power is measured at its output.

**Quantities.** $P_t$ is the peak transmit power in W, $G$ the antenna gain (the same on transmit and receive, a ratio, not in dB), $\lambda$ the wavelength in m, $\sigma$ the radar cross section in m², $R$ the range in m, $k = 1.380649 \times 10^{-23}$ J/K the Boltzmann constant, $B$ the noise bandwidth in Hz, $F \ge 1$ the noise figure and $L \ge 1$ the product of all the other losses.

**Claim.** The received echo power is

$$P_r = \frac{P_t G^2 \lambda^2 \sigma}{(4\pi)^3 R^4 L},$$

the noise power is $P_n = k T_0 B F$, and the SNR is their ratio, as in the equation above.

In decibels, $\mathrm{SNR} = P_t + 2G + 2\lambda + \sigma - 32.98 - 4R + 203.98 - B - F - L$, with each quantity in dB of its unit: $10\log_{10}(4\pi)^3 = 32.98$ and $10\log_{10}(k T_0) = -203.98$ dBW/Hz.

## In plain words

The transmitter puts out power. The antenna sends more of it in one direction, by its gain. On the way to the target, the power spreads over a sphere, so the power per square meter falls as the square of the range. The target catches some of it, and the radar cross section says how much it sends back as if it were an isotropic source. On the way back, the power spreads over a sphere again, and the antenna catches the part that falls on its effective area. That is the echo power. The receiver adds its own noise, which grows with the bandwidth and the noise figure. The ratio of the two is the SNR.

## Proof

The proof builds the received power step by step from the assumptions.

**Step 1: the power density at the target.** An isotropic antenna that radiates $P_t$ spreads it evenly over a sphere of area $4\pi R^2$ in free space, by conservation of energy. An antenna of gain $G$ puts $G$ times the isotropic density in the direction of the target, by the definition of gain. So the power density at the target is

$$S_t = \frac{P_t G}{4\pi R^2}\ \text{W/m}^2.$$

**Step 2: the definition of $\sigma$.** The radar cross section is defined so that the target reflects the power $\sigma S_t$ and that this power, radiated isotropically, gives the same density back at the radar as the real target. So the density of the echo at the radar is

$$S_r = \frac{\sigma S_t}{4\pi R^2} = \frac{P_t G \sigma}{(4\pi)^2 R^4}.$$

**Step 3: the effective aperture.** An antenna of gain $G$ at wavelength $\lambda$ has the effective area $A_e = G\lambda^2/(4\pi)$, and it delivers the power $S_r A_e$ from an incident plane wave. The plane wave holds because the target is in the far field. With the losses $L$,

$$P_r = \frac{S_r A_e}{L} = \frac{P_t G \sigma}{(4\pi)^2 R^4} \cdot \frac{G \lambda^2}{4\pi} \cdot \frac{1}{L} = \frac{P_t G^2 \lambda^2 \sigma}{(4\pi)^3 R^4 L}.$$

**Step 4: the noise.** Thermal noise at temperature $T_0$ has the one-sided density $k T_0$ W/Hz at the input. The noise figure $F$ is defined as the ratio of the output noise of the real receiver to that of an ideal receiver with the same gain, so referred to the input the density is $k T_0 F$. A filter of noise bandwidth $B$ passes $P_n = k T_0 B F$.

**Step 5: the ratio.** $\mathrm{SNR} = P_r / P_n$, which is the stated equation.

The relation $A_e = G\lambda^2/(4\pi)$ of Step 3 is taken as known here. It follows from reciprocity and a thermodynamic argument, and it is the same relation that gives the [free-space path loss](/free-space-path-loss/) of a one-way link. $\blacksquare$

## Consequences

**A worked example.** Take $P_t = 100$ kW, $G = 35$ dB, a frequency of 10 GHz ($\lambda = 0.02998$ m), $\sigma = 1$ m², $R = 50$ km, $B = 1$ MHz, $F = 3$ dB and $L = 6$ dB.

| quantity | value |
|---|---|
| power density at the target, $P_t G/(4\pi R^2)$ | 0.010066 W/m² |
| effective aperture, $G\lambda^2/(4\pi)$ | 0.2262 m² |
| echo power $P_r$ | $1.82 \times 10^{-14}$ W |
| noise power $k T_0 B F$ | $7.99 \times 10^{-15}$ W, that is $-110.98$ dBm |
| SNR | 2.279, that is 3.58 dB |

In decibels: $50 + 70 - 30.46 + 0 - 32.98 - 187.96 + 203.98 - 60 - 3 - 6 = 3.58$ dB.

**The maximum range.** Solve for $R$ with the smallest SNR that the detector needs:

$$R_{\max} = \left( \frac{P_t G^2 \lambda^2 \sigma}{(4\pi)^3 k T_0 B F L\, \mathrm{SNR}_{\min}} \right)^{1/4}.$$

In the example, an SNR of 13 dB is reached at $R_{\max} = 29.07$ km. To double the range, the radar needs 12.04 dB more: 16 times the power, or 4 times the antenna gain.

**Pulse compression and integration.** With a [matched filter](/matched-filter/), $B$ is about $1/\tau$ for a pulse of length $\tau$, so $P_t / B$ is close to the energy $P_t \tau$ of the pulse. A long coded pulse with [pulse compression](/pulse-compression/) gets the SNR of its energy and the range resolution $c/(2B)$ of its bandwidth: 149.9 m for $B = 1$ MHz. Coherent integration of $n$ pulses multiplies the SNR by $n$.

**The radar cross section is not fixed.** Real targets fluctuate with aspect, and the [Swerling models](/swerling-target-models/) give the distribution of $\sigma$. The equation then gives the mean SNR.

**Unambiguous range.** The equation does not include the pulse repetition frequency, but the range is unambiguous only up to $c/(2\,\mathrm{PRF})$: 149.9 km at 1 kHz.

## Tightness

The equation is exact under its assumptions, in the sense that each step is an identity or a definition: Steps 1 and 2 are energy conservation and the definition of $\sigma$, and Steps 3 and 4 use the definitions of $A_e$ and $F$. It stops holding when an assumption fails.

- **Multipath.** Over a flat ground or sea, the direct and reflected paths interfere. The echo then varies between 0 and 16 times the free space value, and at low angles it falls as $1/R^8$ instead of $1/R^4$.
- **Near field.** Close to a large antenna or target, the wave is not plane, and neither $G$ nor $\sigma$ has its far field value.
- **Clutter and jamming.** In clutter the limit is the signal to clutter ratio, which falls more slowly with range, often as $1/R^3$ for surface clutter. Jamming adds a noise power that the equation does not include.
- **Bistatic radar.** With separate transmit and receive antennas, $R^4$ becomes $R_t^2 R_r^2$ and the two gains differ.
- **Atmosphere.** Rain and gas absorb power, which grows with frequency and range and is put in $L$ only as a rough figure.

## History

The radar equation took its form in the radar work of the Second World War, and it has been in every radar textbook since. Skolnik's textbook treats it at length in Chapter 2, with the many losses that a real system has, and Richards gives the form for the SNR of a single pulse that signal processing uses.

## References
