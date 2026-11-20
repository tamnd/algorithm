---
tag: E7RJE7
kind: definition
slug: stepped-frequency-waveform
name: Stepped frequency waveform
aliases:
- stepped frequency pulse train
- synthetic wideband waveform
area: communications/radar-waveforms
level: advanced
summary: "A train of N narrowband pulses whose carriers step by delta f, combined by an inverse DFT into a range profile with the resolution c / (2 N delta f) of the whole band."
prereqs: [discrete-fourier-transform, pulse-compression, sampling-theorem]
see_also: [linear-frequency-modulation-pulse, range-doppler-coupling, costas-array, window-functions, inverse-fft, fmcw-radar, synthetic-aperture-radar, orthogonal-frequency-division-multiplexing]
sources:
  - book: isbn:9780890067277
    title: "Donald R. Wehner, High-Resolution Radar, second edition, Artech House, 1994"
    locator: "the chapter on synthetic range profiles from stepped frequency waveforms (the inverse DFT, range ambiguity and the effect of target motion)"
  - book: isbn:9780471473787
    title: "Nadav Levanon and Eli Mozeson, Radar Signals, Wiley, 2004"
    locator: "Chapter 9, Coherent Train of Diverse Pulses (trains whose pulses change frequency from one pulse to the next)"
  - book: isbn:9780071798327
    title: "Mark A. Richards, Fundamentals of Radar Signal Processing, second edition, McGraw-Hill, 2014"
    locator: "Chapter 4, Radar Waveforms (stepped frequency waveforms and the synthetic range profile)"
---

A stepped frequency waveform is a train of $N$ narrowband pulses whose carrier frequencies are $f_0, f_0 + \Delta f, \dots, f_0 + (N - 1)\Delta f$. The receiver keeps one complex sample per pulse at a fixed range gate, and an inverse [DFT](/discrete-fourier-transform/) of the $N$ samples gives a range profile with the resolution $c/(2N\Delta f)$ of the whole band $N\Delta f$, inside a window of $c/(2\Delta f)$. A [linear frequency modulation pulse](/linear-frequency-modulation-pulse/) sweeps the band inside one pulse and needs a receiver as wide as the band, while the stepped waveform needs only the bandwidth of one pulse but takes $N$ pulses and is sensitive to motion during the train. A [phase-coded waveform](/phase-coded-waveform/) also gets its band inside one pulse, from the chip rate.

## Definition

**Waveform.** Pulse $n = 0, \dots, N-1$ is sent at the time $n T_r$, where $T_r$ is the pulse repetition interval, with the carrier $f_n = f_0 + n\Delta f$. Each pulse has a length $\tau_p$ and a bandwidth of about $1/\tau_p$, much smaller than the total band $N\Delta f$.

**Samples.** For a point target at the range $R$ that does not move, the receiver mixes each echo down with its own carrier and samples it at a range gate that contains $R$. The sample is

$$x[n] = A\, e^{-j 4\pi f_n R/c} = A\, e^{-j4\pi f_0 R/c}\, e^{-j 2\pi n\, (2\Delta f R/c)},$$

a complex tone in $n$ whose frequency $2\Delta f R/c$ cycles per pulse is proportional to the range.

**Synthetic range profile.** The inverse DFT

$$p[k] = \frac{1}{N} \sum_{n=0}^{N-1} x[n]\, e^{j2\pi nk/N}, \qquad k = 0, \dots, N-1,$$

has a peak at the bin $k = (2N\Delta f R/c) \bmod N$. So:

- **Resolution (closed form).** One bin is $\Delta R = c/(2N\Delta f)$, the resolution of a band $N\Delta f$.
- **Unambiguous window (closed form).** The profile repeats every $N$ bins, which is $R_u = c/(2\Delta f)$ in range. Targets farther apart than $R_u$ fold onto each other.
- **Gate condition (rule).** The range gate of one pulse spans about $c\tau_p/2$. To keep all targets of the gate inside one window, choose $c\tau_p/2 \le c/(2\Delta f)$, that is, $\Delta f \le 1/\tau_p$.
- **Sidelobes.** With uniform weights the profile of one target is a Dirichlet kernel, with the highest sidelobe near $-13.3$ dB for large $N$. A [window](/window-functions/) on the samples lowers it at the cost of a wider peak.

**Motion (closed form).** For a target with a radial speed $v$, $R = R_0 + v\, nT_r$, and the phase gains the term $-4\pi f_0 v n T_r/c$, which is linear in $n$, and a term $-4\pi\Delta f v T_r n^2/c$. The linear term moves the profile by $f_0 v T_r/\Delta f$ in range. The quadratic term spreads the peak over several bins. This is the [range-Doppler coupling](/range-doppler-coupling/) of the waveform.

## Examples and non-examples

**A profile of 64 steps.** $N = 64$ and $\Delta f = 1$ MHz give a band of 64 MHz, a resolution of $c/(2N\Delta f) = 2.342$ m and a window of $c/(2\Delta f) = 149.9$ m. Each pulse needs a receiver of only about 1 MHz.

- A target at $R = 30$ m gives the tone frequency $2N\Delta f R/c = 12.81$ bins. The profile peaks at bin 13 with 0.941 of the full value, a loss from the target lying between two bins.
- A target at $R = 1000$ m gives $426.96$ bins, which folds to bin $42.96$: the profile shows it at 100.6 m, which is $1000 \bmod 149.9$.
- With $f_0 = 10$ GHz, $T_r = 100\ \mu$s and a speed of 30 m/s, the profile moves by $f_0 v T_r/\Delta f = 30$ m, which is 12.8 bins. One profile takes $N T_r = 6.4$ ms.

**Stepped chirps.** Each pulse can itself be a chirp of band $\Delta f$ or more, compressed first. The steps then join the bands of the chirps into a wider band. This is common in imaging radars.

**Non-example: frequency agility.** A radar that changes its carrier at random from pulse to pulse to avoid jamming does not form a profile. The samples are not combined coherently across the band.

**Non-example: an LFM pulse.** A chirp also sweeps a band linearly, but inside one pulse. It needs a wide receiver, and it has no folding of range at $c/(2\Delta f)$.

**Non-example: a Costas pulse.** A [Costas array](/costas-array/) hops through frequencies inside one pulse in a permuted order, to get a thumbtack ambiguity function. The stepped waveform steps between pulses in a linear order, which gives the coupling described above.

## Related definitions

- **DFT.** The profile is the inverse DFT of the samples, computed with an [inverse FFT](/inverse-fft/) in $O(N \log N)$.
- **FMCW radar.** An [FMCW radar](/fmcw-radar/) also turns range into a tone, by mixing a linear sweep with its echo, and finds the range with a DFT. Its sweep is continuous, not stepped.
- **OFDM.** The samples $x[n]$ are the response of the channel at $N$ equally spaced frequencies, as on the subcarriers of [OFDM](/orthogonal-frequency-division-multiplexing/), and the profile is the impulse response of the channel.
- **Synthetic aperture radar.** Stepped frequency trains give fine range resolution in some [synthetic aperture radar](/synthetic-aperture-radar/) and inverse synthetic aperture systems, where the profile is combined with cross range processing.

## References
