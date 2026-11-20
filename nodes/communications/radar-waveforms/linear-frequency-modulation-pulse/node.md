---
tag: YAP6B6
kind: definition
slug: linear-frequency-modulation-pulse
name: Linear frequency modulation pulse
aliases:
- LFM pulse
- chirp pulse
- linear chirp
area: communications/radar-waveforms
level: core
summary: "A pulse of constant amplitude whose frequency sweeps linearly over a band B during its length T, which compresses to about 1/B and tolerates Doppler shifts."
prereqs: [analytic-signal, matched-filter, pulse-compression]
see_also: [ambiguity-function, range-doppler-coupling, nonlinear-frequency-modulation, stepped-frequency-waveform, frank-code, fmcw-radar, window-functions, chirp-scaling-algorithm]
sources:
  - paper: doi:10.1002/j.1538-7305.1960.tb03942.x
    title: "J. R. Klauder, A. C. Price, S. Darlington and W. J. Albersheim, The theory and design of chirp radars, Bell System Technical Journal 39(4), 1960"
    locator: "pp. 745 to 808 (the linear FM pulse, its spectrum, its matched filter output and the effect of a Doppler shift)"
  - book: isbn:9780471473787
    title: "Nadav Levanon and Eli Mozeson, Radar Signals, Wiley, 2004"
    locator: "Chapter 4, Basic Radar Signals (the linear FM pulse and its ambiguity function), and Chapter 5, Frequency-Modulated Pulse (weighting and its costs)"
  - book: isbn:9780071798327
    title: "Mark A. Richards, Fundamentals of Radar Signal Processing, second edition, McGraw-Hill, 2014"
    locator: "Chapter 4, Radar Waveforms (the linear FM waveform, its matched filter response and range-Doppler coupling)"
---

A linear frequency modulation (LFM) pulse, or chirp, has a constant amplitude and a frequency that changes at a constant rate $k = B/T$ across its length $T$, so that it sweeps a band $B$. Its [matched filter](/matched-filter/) compresses it to a peak about $1/B$ wide, and a Doppler shift moves the peak in delay but does not destroy it. Among the waveforms for [pulse compression](/pulse-compression/), it differs from [nonlinear frequency modulation](/nonlinear-frequency-modulation/), which sweeps at a changing rate to shape the spectrum, from the [stepped frequency waveform](/stepped-frequency-waveform/), which steps the carrier from one pulse to the next, and from a [phase-coded waveform](/phase-coded-waveform/), which keeps the frequency and changes the phase in steps.

## Definition

**LFM pulse.** For a length $T > 0$ and a sweep rate $k \ne 0$, the complex envelope is

$$u(t) = \frac{1}{\sqrt{T}}\, e^{j\pi k t^2} \quad \text{for } -\tfrac{T}{2} \le t \le \tfrac{T}{2},$$

and $0$ otherwise. The phase is $\pi k t^2$, so the instantaneous frequency is $f(t) = kt$, a straight line from $-kT/2$ to $kT/2$. The swept band is $B = |k| T$. With $k > 0$ it is an up-chirp, and with $k < 0$ a down-chirp. The transmitted signal is $\operatorname{Re}\{u(t)\, e^{j2\pi f_c t}\}$ at the carrier $f_c$. The energy is $E = 1$.

**Time bandwidth product.** $TB$ is the main parameter. For $TB \gg 1$, the spectrum is close to a rectangle of width $B$ with ripples near its edges (Fresnel ripples), and the compression ratio is about $TB$.

**Ambiguity function (closed form).** With the convention $\chi(\tau, \nu) = \int u(t)\,\overline{u(t - \tau)}\, e^{j2\pi\nu t}\, dt$ of the [ambiguity function](/ambiguity-function/) page,

$$|\chi(\tau, \nu)| = \Bigl(1 - \frac{|\tau|}{T}\Bigr) \left|\operatorname{sinc}\bigl((\nu + k\tau)(T - |\tau|)\bigr)\right| \quad \text{for } |\tau| \le T,$$

and $0$ otherwise, with $\operatorname{sinc} x = \sin(\pi x)/(\pi x)$. It is the surface of the rectangular pulse sheared along the line $\nu = -k\tau$.

**Consequences.** All follow from the closed form.

- **Zero Doppler cut.** $|\chi(\tau, 0)| = (1 - |\tau|/T)\,|\operatorname{sinc}(k\tau(T - |\tau|))|$. For $TB \gg 1$ its 3 dB width is close to $0.886/B$ and its first null close to $1/B$, which gives the range resolution $c/(2B)$. Its first sidelobe tends to $-13.26$ dB, the first sidelobe of the sinc, as $TB$ grows.
- **Ridge.** At $\tau = -\nu/k$ the sinc is 1 and $|\chi| = 1 - |\nu|/B$. A Doppler shift $\nu$ moves the peak by $-\nu/k = -\nu T/B$ in delay and lowers it only by the factor $1 - |\nu|/B$. This is the Doppler tolerance of the chirp and the source of its [range-Doppler coupling](/range-doppler-coupling/).
- **Sign of the error.** For an up-chirp and an approaching target ($\nu > 0$), the peak comes early and the target appears closer. A down-chirp gives the opposite error. Texts that use $\overline{u(t + \tau)}$ in the definition, such as Levanon and Mozeson, show the ridge with the opposite slope in their delay axis, but the physical error is the same.

## Examples and non-examples

**A chirp with $TB = 50$.** $T = 10\ \mu$s and $B = 5$ MHz, so $k = 5 \times 10^{11}$ Hz/s. From the closed form:

| Quantity | Value |
|---|---|
| range resolution $c/(2B)$ | 29.98 m |
| first null of the zero Doppler cut | 204.2 ns (against $1/B = 200$ ns) |
| 3 dB width of the zero Doppler cut | 176.8 ns (against $0.886/B = 177.2$ ns) |
| highest sidelobe of the zero Doppler cut | $-13.52$ dB |
| shift of the peak for $\nu = 10$ kHz | $-20$ ns, or 3.0 m closer, with the peak at 0.998 |
| shift for a target approaching at 300 m/s at $f_c = 10$ GHz ($\nu = 20.0$ kHz) | about 6 m closer |

The plain pulse of 10 µs resolves $cT/2 = 1499$ m, so the chirp is 50 times finer at the same energy.

**With weighting.** The sidelobes of $-13.5$ dB are too high for many radars. A Hamming weight on the matched filter lowers them to about $-42.7$ dB in the large $TB$ approximation, at a cost of 1.34 dB in signal to noise ratio and a main lobe 1.47 times wider at the 3 dB points (closed forms from the transform of the window). See [window functions](/window-functions/).

**Non-example: FMCW.** An [FMCW radar](/fmcw-radar/) uses linear sweeps, but it transmits continuously and usually processes the echo by mixing it with the transmitted sweep (stretch processing), not by a matched filter on a pulse.

**Non-example: nonlinear FM.** A sweep whose frequency is not a straight line in time, for example one that is faster near the center of the band, is [nonlinear frequency modulation](/nonlinear-frequency-modulation/). It is designed for low sidelobes without weighting, and it is less tolerant of Doppler.

**Non-example: the Frank code.** A [Frank code](/frank-code/) changes the phase in steps that follow a staircase approximation of a chirp. It is a phase-coded waveform with a constant carrier inside each chip, not an LFM pulse, although its ambiguity function has a similar ridge.

**Non-example: a stepped frequency train.** A [stepped frequency waveform](/stepped-frequency-waveform/) sweeps the band in steps over many pulses, each pulse at one frequency. The sweep is linear in pulse number, but no single pulse is a chirp.

## Related definitions

- **Ambiguity function.** The [ambiguity function](/ambiguity-function/) of the chirp is a ridge along $\nu = -k\tau$, which is why the chirp is Doppler tolerant.
- **Range-Doppler coupling.** The shift $-\nu/k$ of the peak is [range-Doppler coupling](/range-doppler-coupling/). It can be corrected when the Doppler shift is known, or cancelled with a pair of up- and down-chirps.
- **Pulse compression.** The chirp is the most common waveform of [pulse compression](/pulse-compression/).
- **Chirp scaling.** In synthetic aperture radar, the [chirp scaling algorithm](/chirp-scaling-algorithm/) uses the quadratic phase of chirps in range and azimuth to focus an image without interpolation.
- **Analytic signal.** The complex envelope $u$ is the baseband form of the [analytic signal](/analytic-signal/) of the transmitted real chirp.

## References
