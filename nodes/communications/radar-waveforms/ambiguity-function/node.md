---
tag: FTBGX6
kind: definition
slug: ambiguity-function
name: Ambiguity function
aliases:
- Woodward ambiguity function
- radar ambiguity function
area: communications/radar-waveforms
level: core
summary: "The matched filter response of a waveform as a function of delay and Doppler mismatch, which shows its resolution and sidelobes."
prereqs: [autocorrelation, cross-correlation, matched-filter]
see_also: [pulse-compression, range-doppler-coupling, linear-frequency-modulation-pulse, costas-array, time-frequency-uncertainty, short-time-fourier-transform, range-doppler-processing, parsevals-theorem]
sources:
  - book: "P. M. Woodward, Probability and Information Theory, with Applications to Radar, Pergamon Press, London, 1953"
    title: "Probability and Information Theory, with Applications to Radar"
    locator: "Chapter 7, The Transmitted Radar Signal (Section 7.1, Accuracy, Resolution and Signal Ambiguity, and Section 7.2, Ambiguity in Range and Velocity)"
  - paper: doi:10.1109/TIT.1956.1056805
    title: "W. McC. Siebert, A radar detection philosophy, IRE Transactions on Information Theory 2(3), 1956"
    locator: "pp. 204 to 221 (the ambiguity function as the output of the matched filter, and the volume property, which Siebert calls the radar uncertainty principle)"
  - book: isbn:9780471473787
    title: "Nadav Levanon and Eli Mozeson, Radar Signals, Wiley, 2004"
    locator: "Chapter 3, Ambiguity Function (definition, properties and the volume), and Chapter 4, Basic Radar Signals (the rectangular pulse and the chirp)"
---

The ambiguity function of a radar waveform is the output of its [matched filter](/matched-filter/) when the echo has a delay and a Doppler shift that differ from the ones the filter assumes. Its magnitude, a surface over the delay and Doppler plane, shows at once the range resolution, the Doppler resolution, the sidelobes and the [coupling of range and Doppler](/range-doppler-coupling/) of the waveform. The zero Doppler cut is the [autocorrelation](/autocorrelation/) of the waveform, which is what [pulse compression](/pulse-compression/) gives for a target that does not move. The ambiguity function is a property of one waveform, and its total volume is fixed by the energy, so a waveform design can only move the volume around.

## Definition

**Notation.** The waveform is a complex envelope $u(t)$ with finite energy $E = \int |u(t)|^2\, dt$. The delay $\tau$ is in seconds, the Doppler shift $\nu$ in Hz, and a bar is the complex conjugate. The imaginary unit is $j$.

**Ambiguity function.**

$$\chi(\tau, \nu) = \int_{-\infty}^{\infty} u(t)\, \overline{u(t - \tau)}\, e^{j 2\pi \nu t}\, dt.$$

The echo of a point target at zero delay with Doppler shift $\nu$ is $u(t)\, e^{j2\pi\nu t}$. The filter matched to $u$ correlates its input with $u(t - \tau)$ at the output delay $\tau$, so $\chi(\tau, \nu)$ is the output of the matched filter at the delay $\tau$ for that echo. For an echo at delay $\tau_0$, the output at $\tau_0 + \tau$ has the same magnitude. Most plots show $|\chi(\tau, \nu)|$, often divided by $E$.

**Sign convention.** Levanon and Mozeson, and many other texts, write $\overline{u(t + \tau)}$ in place of $\overline{u(t - \tau)}$. This replaces $\tau$ with $-\tau$: their plot is the mirror image of this one in the delay axis. Some authors use $|\chi|^2$ and call it the ambiguity function. Check the convention before comparing the slope of a ridge with another source.

**Discrete form.** For samples $u[0], \dots, u[N-1]$, $A[k, l] = \sum_n u[n]\, \overline{u[n - k]}\, e^{j2\pi l n / N}$ for the lags $k = -(N-1), \dots, N-1$ and the Doppler bins $l = 0, \dots, N-1$, with $u[n] = 0$ outside the record.

**Properties.** The first four are theorems. The proofs use only the Cauchy-Schwarz inequality, a change of variable and [Parseval's theorem](/parsevals-theorem/).

1. **Peak at the origin.** $|\chi(\tau, \nu)| \le \chi(0, 0) = E$, by the Cauchy-Schwarz inequality applied to $u(t)\,e^{j2\pi\nu t}$ and $u(t - \tau)$.
2. **Volume.** $\int\!\!\int |\chi(\tau, \nu)|^2\, d\tau\, d\nu = E^2 = |\chi(0,0)|^2$. For a fixed $\tau$, $\chi(\tau, \cdot)$ is the Fourier transform of $u(t)\overline{u(t-\tau)}$, so by Parseval's theorem $\int |\chi(\tau, \nu)|^2 d\nu = \int |u(t)|^2 |u(t-\tau)|^2 dt$. Integrating over $\tau$ gives $E \cdot E$. In discrete form, $\sum_k \sum_l |A[k,l]|^2 = N E^2$.
3. **Symmetry.** $\chi(-\tau, -\nu) = e^{j2\pi\nu\tau}\, \overline{\chi(\tau, \nu)}$, so $|\chi(-\tau, -\nu)| = |\chi(\tau, \nu)|$. Substitute $t' = t + \tau$ in the integral.
4. **Chirp shear.** If $u_2(t) = u(t)\, e^{j\pi k t^2}$, then $|\chi_2(\tau, \nu)| = |\chi(\tau, \nu + k\tau)|$. A linear frequency modulation tilts the surface without changing its volume.
5. **Cuts.** The zero Doppler cut $\chi(\tau, 0) = \int u(t + \tau)\, \overline{u(t)}\, dt$ is the autocorrelation of $u$ at the lag $\tau$. The zero delay cut $\chi(0, \nu) = \int |u(t)|^2 e^{j2\pi\nu t} dt$ depends only on the magnitude of $u$, so phase or frequency modulation cannot change the Doppler resolution.

## Examples and non-examples

**Rectangular pulse (closed form).** For $u(t) = 1/\sqrt{T}$ on $0 \le t \le T$, so that $E = 1$,

$$|\chi(\tau, \nu)| = \Bigl(1 - \frac{|\tau|}{T}\Bigr) \left|\operatorname{sinc}\bigl(\nu (T - |\tau|)\bigr)\right| \quad \text{for } |\tau| \le T,$$

and $0$ otherwise, with $\operatorname{sinc} x = \sin(\pi x)/(\pi x)$. The zero Doppler cut is a triangle of half width $T$, and the zero delay cut is a sinc with its first null at $\nu = 1/T$. At $\tau = 0$ and $\nu = 1/(2T)$ the value is $2/\pi = 0.6366$. The first Doppler sidelobe is at $-13.26$ dB. A pulse of $T = 10\ \mu$s resolves about 1.5 km in range and 100 kHz in Doppler.

**Linear FM pulse (closed form).** For the [linear frequency modulation pulse](/linear-frequency-modulation-pulse/) $u(t) = (1/\sqrt{T})\, e^{j\pi k t^2}$ on $0 \le t \le T$, with $k = B/T$, the chirp shear gives

$$|\chi(\tau, \nu)| = \Bigl(1 - \frac{|\tau|}{T}\Bigr) \left|\operatorname{sinc}\bigl((\nu + k\tau)(T - |\tau|)\bigr)\right| \quad \text{for } |\tau| \le T.$$

With $T = 10\ \mu$s and $B = 5$ MHz, the time bandwidth product is $TB = 50$. The first null of the zero Doppler cut is at $\tau = 204$ ns, close to $1/B = 200$ ns, a range resolution near $c/(2B) = 29.98$ m. The peak lies on the ridge $\tau = -\nu/k$: a Doppler shift of 10 kHz moves it by $-20$ ns, or $3.0$ m closer, and lowers it only to $0.998$.

**Barker code of length 13 (zero Doppler cut).** The [Barker code](/barker-code/) of 13 chips has the autocorrelation $13, 0, 1, 0, 1, \dots$, so the zero Doppler cut has a peak of 13 and sidelobes of magnitude 1, at $-22.28$ dB. Away from zero Doppler the sidelobes rise, because the code is not Doppler tolerant.

**Costas waveform.** A frequency hopping pulse that follows a [Costas array](/costas-array/) has a surface close to a thumbtack: one narrow peak, and sidelobes that are low and spread over the plane.

**Non-example: the ideal thumbtack.** No waveform has $|\chi| = E$ at the origin and $0$ everywhere else. By the volume property, a surface that is $0$ almost everywhere has volume $0$, not $E^2$. A narrow central peak always comes with volume somewhere else, in a ridge, in sidelobes or in a pedestal. This is the radar form of the [time-frequency uncertainty](/time-frequency-uncertainty/) principle.

**Non-example: the cross-ambiguity function.** $\int x(t)\, \overline{u(t-\tau)}\, e^{j2\pi\nu t} dt$ for a received signal $x$ that is not $u$ is the output of a bank of Doppler shifted matched filters. It is what a receiver computes, but it is not a property of the waveform, and the volume and symmetry properties do not hold for it.

**Non-example: the autocorrelation alone.** The autocorrelation is only the zero Doppler cut. An up-chirp and a down-chirp of the same length and bandwidth have autocorrelations of the same magnitude, but their ambiguity functions have ridges of opposite slope.

## Related definitions

- **Matched filter.** The [matched filter](/matched-filter/) maximizes the signal to noise ratio for a known echo. The ambiguity function describes its output when the echo is not exactly the one it is matched to.
- **Pulse compression.** [Pulse compression](/pulse-compression/) is the use of the matched filter on a long coded pulse. Its range sidelobes are the zero Doppler cut of the ambiguity function.
- **Range-Doppler coupling.** A ridge that is not parallel to an axis means that delay and Doppler cannot be told apart along it. [Range-Doppler coupling](/range-doppler-coupling/) is the error in range that results.
- **Short-time Fourier transform.** For a fixed $\tau$, $\chi(\tau, \cdot)$ is a Fourier transform of a lag product, and the cross-ambiguity function of $x$ with $u$ is a [short-time Fourier transform](/short-time-fourier-transform/) of $x$ with the window $u$, up to the sign of the frequency. The Wigner distribution of $u$ is the two-dimensional Fourier transform of $\chi$, up to the conventions of the transform.
- **Range-Doppler map.** A [range-Doppler processing](/range-doppler-processing/) chain computes a sampled cross-ambiguity function over a coherent train of pulses. The ambiguity function of the train predicts its sidelobes and its ambiguities in range and in Doppler.

## References
