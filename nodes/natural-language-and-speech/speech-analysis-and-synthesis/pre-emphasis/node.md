---
tag: KX275F
kind: technique
slug: pre-emphasis
name: Pre-emphasis
aliases:
- pre-emphasis filter
- preemphasis
area: natural-language-and-speech/speech-analysis-and-synthesis
level: intro
summary: Filter speech by y[n] = x[n] - a x[n-1] with a near 0.97, which boosts high frequencies before spectral analysis.
prereqs: [fir-filter, source-filter-model]
see_also: [mel-filter-bank, mel-frequency-cepstral-coefficients, linear-predictive-coding, perceptual-linear-prediction, frequency-response, rasta-filtering, delta-features, cepstral-mean-normalization]
sources:
  - paper: "Steve Young et al., The HTK Book (for HTK version 3.4), Cambridge University Engineering Department, 2006"
    title: The HTK Book, version 3.4
    locator: "Chapter Speech Input/Output, the pre-emphasis of each frame with the coefficient PREEMCOEF"
  - url: https://github.com/kaldi-asr/kaldi/blob/master/src/feat/feature-window.cc
    title: Kaldi speech recognition toolkit, src/feat/feature-window.cc
    locator: "the function Preemphasize, and its place in ProcessWindow after the removal of the DC offset and before the window"
---

Pre-emphasis passes speech through the one-zero filter $y[n] = x[n] - \alpha x[n-1]$ with $\alpha$ near 0.97 before the frames are analyzed, which raises the high frequencies by up to 36 dB relative to the low ones. It works along the samples of the waveform, once, before framing or inside each frame; [RASTA filtering](/rasta-filtering/) and [delta features](/delta-features/) are filters along the frames of a feature sequence, and the equal loudness curve of [perceptual linear prediction](/perceptual-linear-prediction/) does a similar job on the spectrum and replaces it there. It is the usual first step of [MFCC](/mel-frequency-cepstral-coefficients/) and of [linear predictive coding](/linear-predictive-coding/).

## In plain words

In voiced speech the low frequencies are much stronger than the high ones, because the vocal folds produce smooth pulses. The high frequencies still carry useful detail, such as the upper formants and the hiss of consonants, but an analysis that looks at the whole spectrum is dominated by the strong low part. Pre-emphasis evens this out. From each sample it subtracts almost all of the previous sample. Slow changes, which are the low frequencies, nearly cancel, and fast changes, which are the high frequencies, stay. The result sounds thin and bright, but the spectrum is flatter, and the later steps see all frequencies more equally.

## When it applies

- The signal is voiced speech or a similar source, whose spectrum falls by about 6 dB per octave above a few hundred Hz, as the [source-filter model](/source-filter-model/) explains (measurement).
- The next step fits or compares whole spectra: [linear predictive coding](/linear-predictive-coding/), where a steep slope makes the autocorrelation matrix close to singular and the high formants poorly fitted, and [MFCC](/mel-frequency-cepstral-coefficients/), where the high bands would otherwise have very small energies.
- The features must match a model trained with the same filter. HTK and Kaldi recipes usually apply it with 0.97; many neural front ends on log mel energies leave it out, because the network can learn the weighting.

## The template

1. Choose $\alpha$, usually 0.95 to 0.97; this page and the area use $\alpha = 0.97$.
2. Compute $y[n] = x[n] - \alpha x[n - 1]$ for $n \ge 1$. For the first sample, take $y[0] = x[0]$, or treat $x[-1] = x[0]$ so that $y[0] = (1 - \alpha) x[0]$.
3. Either filter the whole signal once and then cut frames, or cut frames first and filter each frame on its own; Kaldi does the second, after it removes the mean of the frame.
4. Apply the window, the FFT and the rest of the front end to $y$.

**Frequency response (theorem).** The filter is $H(z) = 1 - \alpha z^{-1}$, an [FIR filter](/fir-filter/) with one zero at $z = \alpha$. On the unit circle, $|H(e^{j\omega})|^2 = 1 + \alpha^2 - 2\alpha\cos\omega$, which grows from $(1 - \alpha)^2$ at $\omega = 0$ to $(1 + \alpha)^2$ at $\omega = \pi$. At $f_s = 16$ kHz and $\alpha = 0.97$:

| $f$ (Hz) | 0 | 76 | 100 | 250 | 500 | 1000 | 2000 | 4000 | 8000 |
|---|---|---|---|---|---|---|---|---|---|
| $\lvert H \rvert$ | 0.030 | 0.042 | 0.049 | 0.101 | 0.195 | 0.386 | 0.754 | 1.393 | 1.970 |
| dB | $-30.46$ | $-27.54$ | $-26.21$ | $-19.90$ | $-14.18$ | $-8.28$ | $-2.45$ | $+2.88$ | $+5.89$ |

The gain is 3 dB above its DC value near $f = -f_s \ln\alpha / (2\pi) = 78$ Hz, rises by close to 6 dB per octave from a few hundred Hz to a few kHz, crosses 1 at $f = \frac{f_s}{2\pi} \arccos(\alpha / 2) = 2711$ Hz, and ends at $+5.89$ dB at 8 kHz. The total range from 0 Hz to 8 kHz is 36.35 dB.

**Inverse (theorem).** The de-emphasis filter $1 / (1 - \alpha z^{-1})$, that is $x[n] = y[n] + \alpha x[n - 1]$, undoes it exactly when the same initial value is used. It is stable because $|\alpha| < 1$.

## Classic examples

**A short signal.** For $x = (1, 2, 3, 2)$ and $y[0] = x[0]$, the output is $y = (1, 1.03, 1.06, -0.91)$. De-emphasis gives back $1$, $1.03 + 0.97 = 2$, $1.06 + 1.94 = 3$ and $-0.91 + 2.91 = 2$.

**A DC offset.** A constant $x[n] = c$ gives $y[n] = 0.03\, c$ after the first sample, so pre-emphasis also removes 97 percent of a DC offset.

**Two tones.** At 16 kHz, a tone at 100 Hz comes out with 0.049 times its amplitude and a tone at 4000 Hz with 1.393 times, so their power ratio changes by $20 \log_{10}(1.393 / 0.049) = 29.1$ dB.

**Before linear prediction.** On a voiced frame at 16 kHz, the normalized autocorrelation $r[1] / r[0]$ of the raw signal is close to 1, because neighbouring samples are nearly equal, and the Toeplitz matrix is then nearly singular. After pre-emphasis the ratio is smaller, and the all-pole fit spends its poles on the formants and not on the overall slope.

## Variations

- **Other coefficients.** Values from 0.9 to 1.0 are in use. With $\alpha = 1$ the filter is the first difference, which removes DC completely.
- **Adaptive pre-emphasis.** Take $\alpha = r[1] / r[0]$ for each frame, the first order predictor of the frame, so that the slope is removed as far as one zero can remove it.
- **In the spectrum.** Multiply the power spectrum by $|H(e^{j\omega})|^2$ after the FFT. This is the same as the time domain filter on each frame up to the edge effects of the window.
- **Equal loudness weighting.** [Perceptual linear prediction](/perceptual-linear-prediction/) weights the critical band spectrum by an equal loudness curve, which boosts the middle frequencies, and does not use pre-emphasis.
- **De-emphasis in synthesis.** LPC coders and vocoders analyze pre-emphasized speech and apply the inverse filter to the synthesized output.

## Pitfalls

- **Mismatched front ends.** Features computed with and without pre-emphasis, or with different $\alpha$, differ in every cepstral coefficient. Train and test with the same setting.
- **Applied twice.** A pipeline that pre-emphasizes the waveform and then calls a toolkit that does it again gets a second order high-pass with a range of over 70 dB.
- **Signal or frame.** Filtering the whole signal and filtering each frame differ at the first sample of every frame. The difference is small, but bit-exact comparisons fail.
- **Noise at high frequencies.** The filter raises the noise above about 2.7 kHz along with the speech. For noisy or band-limited audio, such as telephone speech, a smaller $\alpha$ or none may be better.
- **Sample rate.** The filter is defined per sample, so its corner frequency scales with $f_s$: at 8 kHz the same $\alpha$ gives a crossing of 1 at 1355 Hz.

## Exercises

1. Derive $|H(e^{j\omega})|^2 = 1 + \alpha^2 - 2\alpha\cos\omega$ and find the frequency where the gain is 1.
2. Show that a sinusoid $\cos(\omega n)$ comes out as $|H| \cos(\omega n + \varphi)$ and find the phase $\varphi$ as a function of $\alpha$ and $\omega$.
3. For a signal with autocorrelation $r[0] = 1$, $r[1] = \rho$, find the energy of the pre-emphasized signal, and the $\alpha$ that minimizes it.
4. Write the de-emphasis recursion and prove that it inverts pre-emphasis when both use $x[-1] = 0$.
5. Find the total gain range from 0 Hz to $f_s / 2$ in dB for $\alpha = 0.9$, 0.95 and 0.97.

## References
