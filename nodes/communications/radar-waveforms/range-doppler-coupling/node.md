---
tag: JFMM3S
kind: concept
slug: range-doppler-coupling
name: Range-Doppler coupling
aliases:
- delay-Doppler coupling
area: communications/radar-waveforms
level: advanced
summary: "A Doppler shift moves the matched filter peak of a frequency modulated pulse in delay, so the measured range depends on the target's speed along a tilted ridge of the ambiguity function."
prereqs: [matched-filter, ambiguity-function, linear-frequency-modulation-pulse]
see_also: [pulse-compression, nonlinear-frequency-modulation, stepped-frequency-waveform, fmcw-radar, range-doppler-processing, costas-array, range-doppler-algorithm, cramer-rao-bound]
sources:
  - paper: doi:10.1002/j.1538-7305.1960.tb03942.x
    title: "J. R. Klauder, A. C. Price, S. Darlington and W. J. Albersheim, The theory and design of chirp radars, Bell System Technical Journal 39(4), 1960"
    locator: "pp. 745 to 808 (the response of the chirp matched filter to a Doppler shifted echo, and the resulting error in range)"
  - book: isbn:9780471473787
    title: "Nadav Levanon and Eli Mozeson, Radar Signals, Wiley, 2004"
    locator: "Chapter 3, Ambiguity Function, and Chapter 4, Basic Radar Signals (the tilted ridge of the linear FM pulse)"
  - book: isbn:9780071798327
    title: "Mark A. Richards, Fundamentals of Radar Signal Processing, second edition, McGraw-Hill, 2014"
    locator: "Chapter 4, Radar Waveforms (range-Doppler coupling of the linear FM waveform)"
---

Range-Doppler coupling is the error in range that a Doppler shift causes for a waveform whose [ambiguity function](/ambiguity-function/) has a tilted ridge. For a [linear frequency modulation pulse](/linear-frequency-modulation-pulse/) of length $T$ and band $B$, a Doppler shift $\nu$ moves the matched filter peak by $-\nu T/B$ in delay, so the target appears at the wrong range but is still detected. The ambiguity function is the whole surface, and [pulse compression](/pulse-compression/) is the processing; the coupling is one feature of the surface, the slope of its ridge. Waveforms with a thumbtack surface, such as a [Costas array](/costas-array/) pulse, have little coupling but less Doppler tolerance.

## In plain words

A chirp radar finds a target by matching the echo to the pulse, which sweeps up in frequency. A moving target shifts the whole echo up or down in frequency. A sweep that is shifted up looks the same as the original sweep sent a little earlier, because the frequency rises with time. So the receiver finds the best match at a slightly wrong time and reports a slightly wrong range. The match is still strong, which is good for detection. The error is in proportion to the speed, so it is often small, and it can be removed if the speed is known. A pair of sweeps, one up and one down, makes errors of opposite sign, and their average gives the true range.

## The idea

**The linear chirp (closed form).** With sweep rate $k = B/T$, the magnitude of the ambiguity function is

$$|\chi(\tau, \nu)| = \Bigl(1 - \frac{|\tau|}{T}\Bigr) \left|\operatorname{sinc}\bigl((\nu + k\tau)(T - |\tau|)\bigr)\right|, \quad |\tau| \le T.$$

The sinc factor is largest on the line $\nu + k\tau = 0$. So for an echo with Doppler shift $\nu$, the output peaks near the delay $\tau = -\nu/k$, and on that line its value is $1 - |\nu|/B$. The delay error and the range error are

$$\Delta\tau = -\frac{\nu T}{B}, \qquad \Delta R = \frac{c\,\Delta\tau}{2} = -\frac{c\,\nu\, T}{2B}.$$

With $\nu = 2 v f_c / c$ for a target that approaches at the speed $v$ and a carrier $f_c$, this is $\Delta R = -v f_c T / B$. For an up-chirp, an approaching target appears closer, and for a down-chirp it appears farther away. The triangle factor $(1 - |\tau|/T)$ pulls the true peak a little toward $\tau = 0$, so the closed form for $\Delta R$ is exact on the ridge and slightly too large for the peak.

**Why it happens.** The instantaneous frequency of the chirp is $f(t) = kt$. A Doppler shift $\nu$ turns it into $kt + \nu = k(t + \nu/k)$, which is the same sweep shifted in time by $-\nu/k$. The matched filter cannot tell a shift in frequency from a shift in time along this line. The volume of the ambiguity function is fixed, so the narrow peak in delay is paid for by this long ridge in the delay and Doppler plane.

**Other waveforms.** The coupling is the slope of the ridge, $d\tau/d\nu$ along the ridge, and it depends on how the waveform links time and frequency.

- A pulse of constant frequency, or a binary [phase-coded waveform](/phase-coded-waveform/) such as a [Barker code](/barker-code/), has no tilted ridge. A Doppler shift lowers the peak and raises the sidelobes, but does not move the peak.
- A polyphase code such as the [Frank code](/frank-code/) follows a staircase approximation of a chirp, and has a tilted ridge and a coupling like the chirp it approximates.
- A [nonlinear frequency modulation](/nonlinear-frequency-modulation/) sweep has a local slope that changes across the band, so a Doppler shift both moves and smears the peak.
- A [stepped frequency waveform](/stepped-frequency-waveform/) has the same coupling between pulses: radial motion $v$ during the train moves the synthetic range profile by $f_0 v T_r / \Delta f$, where $T_r$ is the pulse interval and $\Delta f$ the frequency step.
- A frequency hopping pulse that follows a [Costas array](/costas-array/) has a thumbtack surface and almost no coupling.

## Examples

**A chirp at X band.** $T = 10\ \mu$s, $B = 5$ MHz, $f_c = 10$ GHz and a target that approaches at $v = 300$ m/s, so $\nu = 2vf_c/c = 20.0$ kHz. The closed form gives $\Delta R = -v f_c T/B = -6.0$ m on the ridge. A direct search of the closed form for the largest output finds the peak 5.8 m closer than the target, with a value of 0.996. The range resolution is $c/(2B) = 29.98$ m, so the error is a fifth of a range cell.

**A smaller shift.** For $\nu = 10$ kHz with the same chirp, the ridge is at $-20$ ns, which is 3.0 m, and the value there is $1 - 10^4/(5 \times 10^6) = 0.998$.

**An up and down pair.** Send an up-chirp and a down-chirp of the same $T$ and $B$. For the target above, the up-chirp measures about $R - 6$ m and the down-chirp $R + 6$ m. The mean of the two is the range $R$, and half the difference, divided by $f_c T / B$, gives the speed. The same idea separates range and Doppler in a triangular sweep of an [FMCW radar](/fmcw-radar/), where the beat frequency of each sweep contains both.

**Stepped frequency.** With $f_0 = 10$ GHz, $\Delta f = 1$ MHz, $N = 64$ steps, a pulse interval of $T_r = 100\ \mu$s and a radial speed of 30 m/s, the profile moves by $f_0 v T_r/\Delta f = 30$ m, which is 12.8 cells of $c/(2N\Delta f) = 2.342$ m. A term in $n^2$ in the phase also smears the peak.

## Where it is used

- **Correction in a tracker.** When a tracker knows the radial speed, it subtracts $\Delta R$ from the measured range. A search radar that uses one chirp accepts the error, which is small against the resolution for slow targets.
- **Doppler tolerant detection.** Because the peak survives on the ridge, a single chirp matched filter detects targets over a wide range of speeds, which saves a bank of Doppler filters. This is why the chirp is the usual waveform for search.
- **Measuring range and speed together.** Pairs of up and down chirps, or triangular FMCW sweeps, turn the coupling into a measurement of speed.
- **Range-Doppler maps.** In [range-Doppler processing](/range-doppler-processing/) over a coherent train, the coupling of each pulse adds a small range shift that grows with the Doppler bin, which a correction can remove.
- **Imaging.** In synthetic aperture radar, the coupling of the range chirp with the Doppler of the azimuth signal is one of the terms that the [range-Doppler algorithm](/range-doppler-algorithm/) must correct.
- **Joint estimation.** The tilt of the ambiguity peak sets the correlation of the errors of range and Doppler estimates, and so the joint [Cramér-Rao bound](/cramer-rao-bound/) of the two.

## References
