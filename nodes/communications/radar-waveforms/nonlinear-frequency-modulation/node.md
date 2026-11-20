---
tag: E39CJW
kind: technique
slug: nonlinear-frequency-modulation
name: Nonlinear frequency modulation
aliases:
- NLFM
- nonlinear FM pulse
area: communications/radar-waveforms
level: advanced
summary: "Shapes the frequency sweep of a pulse so that it spends more time near the center of the band, which gives low range sidelobes with a matched filter and no weighting loss."
prereqs: [matched-filter, window-functions, pulse-compression, linear-frequency-modulation-pulse]
see_also: [ambiguity-function, range-doppler-coupling, mismatched-filter-design, phase-coded-waveform, stepped-frequency-waveform, spectral-leakage, discrete-fourier-transform]
sources:
  - paper: "E. N. Fowle, IEEE Transactions on Information Theory 10(1), 1964, pp. 61 to 67"
    title: The design of FM pulse compression signals
    locator: "the whole paper (the stationary phase relation between the frequency sweep and the power spectrum, and the design of a sweep for a given spectrum and envelope)"
  - paper: doi:10.1002/j.1538-7305.1960.tb03942.x
    title: "J. R. Klauder, A. C. Price, S. Darlington and W. J. Albersheim, The theory and design of chirp radars, Bell System Technical Journal 39(4), 1960"
    locator: "pp. 745 to 808 (the spectrum of a chirp by the principle of stationary phase, and weighting for low sidelobes)"
  - book: isbn:9780471473787
    title: "Nadav Levanon and Eli Mozeson, Radar Signals, Wiley, 2004"
    locator: "Chapter 5, Frequency-Modulated Pulse (nonlinear FM pulses, their design and their ambiguity functions)"
---

Nonlinear frequency modulation (NLFM) shapes the frequency sweep of a pulse of constant amplitude so that the power spectrum has the shape of a window, and so the matched filter output has low range sidelobes without a weighting filter. A [linear frequency modulation pulse](/linear-frequency-modulation-pulse/) has a flat spectrum and sidelobes near $-13$ dB, and lowering them with a [window](/window-functions/) on the receive filter costs about 1 to 2 dB in signal to noise ratio. NLFM puts the window into the transmitted sweep, so the filter stays matched and has no loss, but the waveform is much less tolerant of Doppler shifts than the linear chirp. A [mismatched filter](/mismatched-filter-design/) is the other way to lower sidelobes, at the receiver only.

## In plain words

A radar chirp is a tone that rises in pitch at a steady rate. After compression, its echo gives a sharp peak with bumps beside it that are too high for many uses. You can lower the bumps by weighting the receiver, but then some signal is lost. Instead, you can make the tone rise slowly near the middle of the band and fast near the edges. The pulse then spends more time, and so puts more energy, at the middle frequencies. That has the same effect on the bumps as the weighting, but the receiver still matches the pulse exactly, so no signal is lost. The cost is that a moving target, whose echo is shifted in frequency, brings the bumps back up.

## When it applies

- The transmitter must run saturated at constant amplitude, so amplitude weighting on transmit is not possible.
- The 1 to 2 dB loss of a receive window is too costly, for example in a long range search radar.
- The Doppler shifts are small against $1/T$, or a bank of Doppler matched filters is available, because the low sidelobes hold only near zero Doppler.
- The time bandwidth product is large, at least several tens, so that the stationary phase relation holds well.

## The template

The principle of stationary phase links the sweep and the spectrum (a closed form under the assumption $TB \gg 1$). If the pulse has a constant amplitude and the instantaneous frequency $f(t)$ increases from $-B/2$ to $B/2$, then the energy near frequency $f$ is proportional to the time the sweep spends there:

$$|U(f)|^2 \approx \frac{dt}{df}.$$

1. **Choose the spectrum.** Choose a window $W(f) > 0$ on $-B/2 \le f \le B/2$, for example a Hamming, Taylor or raised cosine shape. The compressed pulse is close to the inverse Fourier transform of $W$, so its sidelobes are about those of the window.
2. **Find the time at each frequency.** $t(f) = T \left( \int_{-B/2}^{f} W(x)\,dx \Big/ \int_{-B/2}^{B/2} W(x)\,dx \right) - T/2$, an increasing function from $-T/2$ to $T/2$.
3. **Invert.** Solve $t(f) = t$ for $f(t)$ by bisection or a table.
4. **Integrate the phase.** $\varphi(t) = 2\pi \int_{-T/2}^{t} f(s)\, ds$, and transmit $u(t) = e^{j\varphi(t)}/\sqrt{T}$.
5. **Check and correct.** Compute the matched filter output and its peak sidelobe. The ripples of the finite pulse raise the sidelobes above those of the window, so the design is often refined, for example with a small amplitude taper at the ends of the pulse or by a numerical search over the parameters of the sweep.

## Classic examples

**A Hamming spectrum (measurement).** Take $W(f) = 0.54 + 0.46\cos(2\pi f/B)$ and follow the template with 4 samples per $1/B$. The peak sidelobe of the matched filter output is:

| $TB$ | Doppler $\nu T$ | NLFM peak sidelobe | LFM peak sidelobe |
|---|---|---|---|
| 50 | 0 | $-27.33$ dB | $-13.55$ dB |
| 100 | 0 | $-31.81$ dB | $-13.49$ dB |
| 50 | 1 | $-15.67$ dB | |
| 100 | 1 | $-15.71$ dB | |
| 100 | 2 | $-10.02$ dB | |
| 100 | 5 | $-4.46$ dB | $-13.14$ dB |

At zero Doppler the NLFM pulse gains 14 to 18 dB over the linear chirp, with no loss, and the gain grows with $TB$ because the stationary phase relation becomes more exact. The Hamming window on a linear chirp would reach about $-42.7$ dB at large $TB$, at a loss of 1.34 dB. A Doppler shift of only $1/T$ brings the NLFM sidelobes up to about $-15.7$ dB, while the linear chirp keeps its sidelobes up to large shifts.

**Hybrid sweeps.** A common design is a linear sweep in the middle of the pulse with faster, nonlinear sweeps at both ends, which adds the extra bandwidth at the edges where a Hamming or Taylor spectrum has little energy.

**Tangent FM.** The sweep $f(t) \propto \tan(\beta t)$ for $|t| \le T/2$ is a closed form family. It is close to linear for small $\beta$ and moves time to the center of the band as $\beta$ grows.

## Variations

- **NLFM and a small receive weight.** A mild NLFM sweep with a light weighting filter shares the work and keeps both the loss and the Doppler sensitivity small.
- **NLFM and a mismatched filter.** A [mismatched filter](/mismatched-filter-design/) designed for the NLFM pulse removes the residual sidelobes caused by the ripples of the finite pulse.
- **Phase codes from NLFM.** Sampling the phase $\varphi(t)$ of an NLFM pulse at the chip rate gives a polyphase code, a [phase-coded waveform](/phase-coded-waveform/) with similar sidelobes near zero Doppler, which is easy to generate digitally.
- **Pulse trains.** In a coherent train of pulses, the sidelobes that rise with Doppler can be lowered by changing the sweep from one pulse to the next, so that they do not add up in the same place.

## Pitfalls

- **Doppler sensitivity.** The low sidelobes hold only near zero Doppler. In the example, a shift of $1/T$, which is 100 kHz for a 10 µs pulse, raises them by 12 to 16 dB. Check the [ambiguity function](/ambiguity-function/) over the expected Doppler range, not only the zero Doppler cut.
- **Small time bandwidth product.** The stationary phase relation is an approximation. For $TB$ of a few tens the measured sidelobes are well above those of the window, $-27$ dB instead of about $-43$ dB in the example with $TB = 50$.
- **Hardware distortion.** A nonlinear sweep is harder to generate and to keep exact than a linear one. Small phase errors raise the sidelobes that the design was meant to lower.
- **Range-Doppler coupling that changes with the frequency.** The coupling of a linear chirp is one constant shift. For NLFM the slope of the sweep changes, so a Doppler shift both moves and smears the peak, see [range-Doppler coupling](/range-doppler-coupling/).
- **Window values close to zero.** A window that goes to zero at the band edges asks for an infinite sweep rate there. Use a window with a small pedestal, such as Hamming with 0.08 at the edges.

## Exercises

1. For $W(f) = 1$ on $-B/2 \le f \le B/2$, show that the template gives the linear chirp.
2. For the Hamming spectrum, write $t(f)$ in closed form and find the sweep rate $df/dt$ at the center and at the edges of the band, as a ratio to $B/T$.
3. Explain from the stationary phase relation why NLFM has no loss in signal to noise ratio, while the same window on the receive filter of a linear chirp does.
4. Compute the matched filter output of a Hamming NLFM pulse with $TB = 200$ and compare its peak sidelobe with the values in the table.
5. Show that a Doppler shift $\nu$ moves the point of stationary phase for the frequency $f$ by an amount that depends on $df/dt$ at $f$, and explain why this smears the peak.

## References
