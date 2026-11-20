---
tag: WNH512
kind: technique
slug: fmcw-radar
name: FMCW radar processing
aliases:
- frequency-modulated continuous-wave radar
- dechirp processing
area: communications/radar-waveforms
level: core
summary: "Mixes the echo of a continuous linear chirp with the transmitted chirp, so that range becomes the beat frequency 2 R B / (c T_c), found by an FFT. A second FFT over the chirps gives the speed."
prereqs: [linear-frequency-modulation-pulse, fast-fourier-transform]
see_also: [range-doppler-processing, pulse-compression, stepped-frequency-waveform, range-doppler-coupling, ordered-statistic-cfar, integrated-sensing-and-communication, window-functions, radar-range-equation]
sources:
  - paper: doi:10.1049/ip-f-2.1992.0048
    title: Linear FMCW radar techniques
    locator: "A. G. Stove, IEE Proceedings F (Radar and Signal Processing) 139(5), 1992, pp. 343 to 350 (the beat frequency, the range resolution, the linearity of the sweep and the leakage from the transmitter)"
  - book: isbn:9780071444743
    title: "Mark A. Richards, Fundamentals of Radar Signal Processing, McGraw-Hill, 2005"
    locator: "Chapter 4, Section 4.6.5 (stretch processing of a linear FM pulse, which uses the same mixing step on a pulsed waveform)"
---

An FMCW radar transmits a continuous linear chirp: its frequency rises by the bandwidth $B$ over the chirp time $T_c$, then starts again. The echo of a target at range $R$ is the same chirp delayed by $\tau = 2R/c$. A mixer multiplies the echo by the conjugate of the chirp that is being sent at that moment, and the result is a tone at the beat frequency $f_b = (B/T_c)\tau = 2RB/(cT_c)$. So the range becomes a frequency, and an [FFT](/fast-fourier-transform/) of the mixer output finds every target at once. A second FFT across many chirps gives the Doppler shift, as in [range-Doppler processing](/range-doppler-processing/). The receiver needs a sample rate set by the largest beat frequency, not by $B$: a few MHz in place of hundreds. This is one reason why most automotive radars use FMCW.

## In plain words

Send a tone whose pitch rises at a steady rate. When the echo comes back, the transmitter has already moved to a higher pitch. The difference between the pitch you send now and the pitch you hear now is the same during the whole chirp, and it is larger for a farther target. Mix the two and you get a tone at exactly that difference. Take an FFT of the mixed signal and each target is a peak, at a frequency proportional to its range. Repeat the chirp many times. A moving target shifts the phase of its tone a little from chirp to chirp, so a second FFT across the chirps gives the speed.

## When it applies

- The radar can transmit and receive at the same time, with enough isolation between the two antennas or channels, because the transmitter never stops.
- The ranges of interest are short or medium, up to a few hundred meters for cars or a few kilometers for altimeters, so the largest beat frequency stays within a low sample rate.
- The chirp is linear in frequency, or can be corrected to be. A nonlinear sweep turns each beat tone into a chirp of its own and smears the range peak.
- The target moves little during one chirp. Then the Doppler shift adds a small constant offset to the beat frequency, and the phase change across chirps carries the speed.

## The template

The input is the transmitted chirp of slope $K = B/T_c$, the number of chirps $M$, the sample rate $f_s$ of the mixer output, and $N_s = f_s T_c$ samples per chirp. The holes are the mixer (analog or digital, real or complex), the window, the detector and the conversion of bin indices to range and speed.

```pseudo id=main
FMCW-PROCESS(echo, chirp, M, N_s, f_s, window, detector)
L1  for m <- 0 to M - 1
L2      b[m][n] <- echo of chirp m at sample n times conj(chirp at sample n)    ▷ the mixer: beat signal
L3      b[m] <- window(b[m])
L4      X[m][.] <- FFT(b[m])                                                    ▷ range FFT: bin k is f_b = k f_s / N_s
L5  for each range bin k: Y[.][k] <- FFT over m of X[m][k]                      ▷ Doppler FFT across chirps
L6  peaks <- detector(|Y|^2)                                                    ▷ for example a CFAR
L7  for each peak (d, k): R <- k (f_s / N_s) c T_c / (2B);  v <- f_D lambda / 2 with f_D = d / (M T_c)
```

**Why the mixer gives a tone.** The chirp is $s(t) = e^{j\pi K t^2}$ for $0 \le t < T_c$. The echo is $a\, s(t - \tau)$. Then

$$a\, s(t - \tau)\, \overline{s(t)} = a\, e^{j\pi K (t - \tau)^2 - j\pi K t^2} = a\, e^{-j 2\pi K\tau t}\, e^{j\pi K\tau^2},$$

a tone at the frequency $-K\tau$, whose size is $K\tau = 2RB/(cT_c)$, with a constant phase $\pi K \tau^2$, the residual video phase. The tone holds for $\tau \le t < T_c$, so the part of each chirp in which the echo of the farthest target has not arrived yet is discarded or ignored.

**Resolution.** The tone lasts about $T_c$, so the FFT resolves frequencies $1/T_c$ apart, which is the range step $(1/T_c)\, cT_c/(2B) = c/(2B)$. The range resolution depends only on the bandwidth, as for a pulse with [pulse compression](/pulse-compression/).

**The largest range.** With complex samples at rate $f_s$, the beat frequency must be below $f_s$, so $R_{\max} = f_s c T_c/(2B)$. With real samples it is half of that.

**Speed.** A target at speed $v$ adds the phase $2\pi f_D T_c$ per chirp, with $f_D = 2v/\lambda$. The FFT of line L5 resolves $\Delta v = \lambda/(2 M T_c)$, and the speed is unambiguous within $\pm\lambda/(4T_c)$.

**Check values.** $B = 300$ MHz and $T_c = 50$ μs give the slope $K = 6$ MHz/μs. A target at 50 m gives $f_b = 2.0014$ MHz, and one at 100 m gives 4.0028 MHz. The range resolution is $c/(2B) = 0.4997$ m. With complex sampling at $f_s = 10$ MHz, $R_{\max} = 249.8$ m; with real sampling, 124.9 m. At 77 GHz ($\lambda = 3.893$ mm), a target at 20 m/s has $f_D = 10.27$ kHz. With $M = 128$ chirps, the speed resolution is 0.304 m/s, and the unambiguous speed is $\pm 19.47$ m/s. The residual video phase at 100 m is $\pi K \tau^2 = 8.39$ rad, the same for every chirp.

## Classic examples

- **Automotive radar.** Radars at 77 GHz send fast chirps of tens of microseconds, take the range FFT and the Doppler FFT of the [range-Doppler processing](/range-doppler-processing/) template, and detect with [ordered-statistic CFAR](/ordered-statistic-cfar/) or cell-averaging CFAR. Several receive antennas add a third FFT, over angle.
- **Stretch processing of a pulsed chirp.** A wideband [linear FM pulse](/linear-frequency-modulation-pulse/) can be mixed with a delayed copy of itself in the same way, which turns a short window of ranges into low frequencies. This is the same step in a pulsed radar, with a reference chirp at a chosen range.
- **Radar altimeters and level gauges.** An altimeter measures the height of an aircraft, and a level gauge measures the height of a liquid in a tank, both as the beat frequency of a single strong target.
- **Compared with stepped frequency.** A [stepped-frequency waveform](/stepped-frequency-waveform/) covers the same bandwidth in discrete steps and gets the range profile by an inverse DFT over the steps. FMCW sweeps continuously and gets it by an FFT over time.

## Variations

- **Triangular sweep.** An up-chirp followed by a down-chirp. The Doppler shift adds to the beat frequency of one and subtracts from the other, so the sum and the difference of the two beat frequencies give range and speed for one target. With many targets, the pairing of the peaks is ambiguous.
- **Fast chirps (chirp sequence).** Many short chirps, with the speed from the second FFT, as in the template. The Doppler shift within a chirp is then a small range offset.
- **Real and complex mixers.** A real mixer is cheaper but folds negative frequencies onto positive ones, which halves the usable range and adds images of the leakage.
- **MIMO FMCW.** Several transmitters in time, Doppler or code division give a virtual array for angle estimation.
- **Joint use with communications.** A chirp can carry data in its phase or its start frequency, one of the forms of [integrated sensing and communication](/integrated-sensing-and-communication/).

## Pitfalls

- **The range-Doppler coupling of line L7.** The Doppler shift moves the beat frequency by $f_D$, which looks like a range offset of $f_D c T_c/(2B)$. At 77 GHz and 20 m/s, with $T_c = 50$ μs and $B = 300$ MHz, the offset is 0.257 m, half a range bin. With slower chirps it grows in proportion to $T_c$. See [range-Doppler coupling](/range-doppler-coupling/).
- **A nonlinear sweep in line L2.** If the frequency of the oscillator does not rise linearly, the beat signal of a target is not a pure tone, and the range peak spreads, more at long range. Correct the sweep, or resample the beat signal on a corrected time axis.
- **Leakage from the transmitter.** The transmitter couples into the receiver at zero delay and gives a strong low frequency beat. Without a high-pass filter before line L4, its sidelobes mask close targets.
- **A sample rate too low for line L4.** A target beyond $R_{\max}$ folds into a wrong range bin, and with a real mixer it also folds from negative frequencies. Use an anti-alias filter that cuts off at the largest wanted beat frequency.
- **Too many chirps for a moving target.** If a target moves more than one range bin, $c/(2B)$, during the $M$ chirps, its energy spreads over several range bins in line L5. At 0.5 m bins and 20 m/s, that happens after 25 ms.

## References
