---
tag: QFYSEB
kind: model
slug: source-filter-model
name: Source-filter model
aliases:
- source-filter model of speech production
- source-filter theory
area: natural-language-and-speech/speech-analysis-and-synthesis
level: intro
summary: Speech as a glottal or noise source passed through a vocal tract filter, so the spectrum splits into an excitation and an envelope.
history:
  year: 1960
  people: [Gunnar Fant, Tsutomu Chiba, Masato Kajiyama]
  note: Chiba and Kajiyama treated the vocal tract as a tube with resonances in 1941, and Fant's Acoustic Theory of Speech Production (1960) gave the full model of a source, a vocal tract transfer function and a radiation term that later speech coding and analysis built on.
prereqs: [linear-time-invariant-system, transfer-function]
see_also: [linear-predictive-coding, levinson-durbin-recursion, cepstrum, formant-estimation, pitch-detection, pre-emphasis, mel-frequency-cepstral-coefficients, perceptual-linear-prediction]
sources:
  - paper: "Gunnar Fant, Acoustic Theory of Speech Production, Mouton, The Hague, 1960"
    title: Gunnar Fant, Acoustic Theory of Speech Production
    locator: the source, the vocal tract transfer function and the radiation as separate factors of the speech spectrum
  - book: isbn:9780132136037
    title: L. R. Rabiner and R. W. Schafer, Digital Processing of Speech Signals, Prentice Hall, 1978
    locator: "Chapter 3 (the digital model of speech production: the excitation, the vocal tract as lossless tubes and an all-pole filter, and the radiation)"
  - book: isbn:9780130226167
    title: Xuedong Huang, Alex Acero and Hsiao-Wuen Hon, Spoken Language Processing, Prentice Hall, 2001
    locator: "Chapter 6 (Speech Signal Representations), the source-filter view behind linear prediction and the cepstrum"
---

The source-filter model describes a speech signal as the output of a linear filter, the vocal tract, driven by a source: a train of glottal pulses for voiced sounds, noise for unvoiced sounds, or both. Because the two parts are assumed independent, the spectrum of a frame is the product of a fine structure set by the source and a smooth envelope set by the filter, and the log spectrum is their sum. It is a physical model of how speech is made; [linear predictive coding](/linear-predictive-coding/) is a method that fits its filter as an all-pole model, and the [cepstrum](/cepstrum/) is a method that separates its two parts.

## The machine

Speech is sampled at $f_s$, here 16 kHz. One frame of 10 to 30 ms is modeled as

$$S(z) = E(z)\, G(z)\, V(z)\, R(z),$$

where each factor is a linear time-invariant system, and the parameters change from frame to frame.

- **Source $E(z)$.** For voiced sounds, an impulse train $e[n] = \sum_k \delta[n - kP]$ with period $P$ samples, so the fundamental frequency is $F_0 = f_s / P$. For unvoiced sounds, white noise. A gain $\sigma$ scales either one. Voiced fricatives such as "z" mix both.
- **Glottal pulse $G(z)$.** Each glottal pulse is a smooth bump, not an impulse. Its spectrum falls by about 12 dB per octave above a few hundred Hz, and it is often modeled by two real poles near $z = 1$ (heuristic).
- **Vocal tract $V(z)$.** For vowels, an all-pole filter $V(z) = 1 / A(z)$ with $A(z) = 1 - \sum_{k=1}^{p} a_k z^{-k}$. Each pair of complex poles at radius $r$ and angle $\theta$ is a formant at $f = \theta f_s / (2\pi)$ with a bandwidth of about $-f_s \ln r / \pi$ Hz. Nasals and some consonants also need zeros.
- **Radiation $R(z)$.** The sound at a distance from the lips is about the derivative of the volume velocity, $R(z) \approx 1 - z^{-1}$, a rise of 6 dB per octave (heuristic).

The model assumes that the source does not depend on the filter, that the tract is linear, and that the parameters are fixed within a frame (quasi-stationarity). Many uses merge $G$, $V$ and $R$ into one all-pole filter $H(z) = \sigma / A(z)$ of order $p$, which gives the classic model of linear prediction, $s[n] = \sum_{k=1}^{p} a_k s[n-k] + \sigma e[n]$.

## What it counts

A frame is described by a few numbers: a voicing decision, $F_0$ for voiced frames, a gain $\sigma$, and the $p$ coefficients of $A(z)$, or equivalently $p/2$ formant frequencies and bandwidths. A common rule of thumb for the order is $p \approx f_s / 1000 + 2$, one pole pair per kHz of bandwidth for the formants plus 2 poles for the glottal and radiation slope (heuristic); this gives $p = 10$ at 8 kHz and $p = 18$ at 16 kHz. With an update every 10 ms, the whole model is a few hundred numbers per second, against 16 000 samples per second for the waveform, which is why vocoders and LPC coders use it.

## Relation to other models

- **Linear prediction.** [Linear predictive coding](/linear-predictive-coding/) estimates $a_k$ and $\sigma$ from a frame by solving the normal equations with the [Levinson-Durbin recursion](/levinson-durbin-recursion/). It assumes the merged all-pole filter and no explicit glottal pulse; see also [linear prediction](/linear-prediction/).
- **Lossless tube model.** A tract made of $p$ short tubes of equal length with different areas, lossless and closed at the glottis, has an all-pole transfer function whose reflection coefficients come from the area ratios. This is the physical reading of the reflection coefficients of the Levinson recursion.
- **Homomorphic model.** Taking the log of $|S| = |E|\,|H|$ turns the product into a sum, and the [cepstrum](/cepstrum/) of the sum places the envelope at low quefrencies and the pitch at the quefrency $P$.
- **Front ends.** The [mel filter bank](/mel-filter-bank/), [MFCC](/mel-frequency-cepstral-coefficients/) and [perceptual linear prediction](/perceptual-linear-prediction/) all try to keep $|H|$ and discard $|E|$: wide filters average over the harmonics, and a short cepstrum keeps only the envelope. [Pre-emphasis](/pre-emphasis/) undoes part of the spectral slope of $G R$ before analysis.
- **Neural vocoders.** Modern speech synthesis often drops the explicit split, but some neural vocoders still drive a learned filter with a pulse and noise source.

## Known results in the model

**Harmonics sample the envelope (theorem).** If $e$ is a periodic impulse train with period $P$, the output $s = h * e$ is periodic with period $P$, and its spectrum is made of lines at the harmonics $k F_0$ with amplitudes proportional to $|H(e^{j 2\pi k F_0 / f_s})|$. So a voiced spectrum is the envelope seen only at multiples of $F_0$. For $H$ with one formant at 1000 Hz and a bandwidth of 80 Hz at 16 kHz ($r = 0.98441$, $a_1 = 1.81896$, $a_2 = -0.96907$), a source at $F_0 = 100$ Hz gives harmonics at 900, 1000 and 1100 Hz with levels $-8.2$, 0 and $-9.0$ dB relative to the peak, and the harmonic at 2000 Hz is at $-31.2$ dB. A source at $F_0 = 300$ Hz misses the peak: its harmonics near the formant are at 900 and 1200 Hz, at $-8.2$ and $-14.9$ dB, which is why formants are hard to measure in high voices.

**Linear prediction is exact on an all-pole output (theorem).** If $s$ is the impulse response of $\sigma / A(z)$ with $A$ of order $p$ and all zeros inside the unit circle, then its autocorrelation over all time satisfies $r[i] = \sum_{k=1}^{p} a_k r[|i - k|]$ for $i \ge 1$, the Yule-Walker equations, and $r[0] - \sum_k a_k r[k] = \sigma^2$. So the Levinson-Durbin recursion of order $p$ on $r$ returns $a$ and $\sigma^2$ exactly. For the one-formant filter above, the recursion on the autocorrelation of 20 000 samples of the impulse response returns $a_1 = 1.81896$, $a_2 = -0.96907$ and an error of 1.0000. On a short windowed frame of a voiced signal the equations hold only approximately, and the estimate is biased toward the nearest harmonic (measurement).

**Resonances of a uniform tube (theorem, for the ideal tube).** A lossless uniform tube of length $L$, closed at the glottis and open at the lips, resonates at $f_k = (2k - 1) c / (4L)$. With $L = 17.5$ cm and $c = 350$ m/s this is 500, 1500, 2500 Hz and so on, the formants of a neutral vowel. A shorter tract moves every formant up by the same factor, which is one reason formants of children are higher than those of adults.

**Separation in the cepstrum (theorem, with a heuristic condition).** For a minimum phase $H$ with poles $z_i$, the complex cepstrum of $h$ is $\hat h[m] = \sum_i z_i^m / m$ for $m \ge 1$, whose size is at most $p \max_i |z_i|^m / m$. The cepstrum of a periodic impulse train is nonzero only at multiples of $P$. So when the envelope part has decayed well before $m = P$, a low-time lifter separates the two. At $F_0 = 100$ Hz and 16 kHz, $P = 160$ samples, and an envelope with pole radii up to 0.98 has terms of size at most $p \cdot 0.98^{160} / 160 \approx 2.5 \times 10^{-4}\, p$ there.

**Spectral slope (measurement).** The glottal fall of about 12 dB per octave and the radiation rise of 6 dB per octave leave voiced speech with a fall of about 6 dB per octave above a few hundred Hz. Pre-emphasis with $1 - 0.97 z^{-1}$ undoes most of it.

## References
