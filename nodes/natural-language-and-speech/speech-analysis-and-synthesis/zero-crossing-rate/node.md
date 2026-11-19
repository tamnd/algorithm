---
tag: A1QYXM
kind: definition
slug: zero-crossing-rate
name: Zero-crossing rate
aliases:
- ZCR
- zero-crossing count
area: natural-language-and-speech/speech-analysis-and-synthesis
level: intro
summary: The fraction of adjacent samples in a frame whose signs differ, high for unvoiced fricatives and low for voiced speech.
prereqs: [autocorrelation]
see_also: [voice-activity-detection, rabiner-sambur-endpoint-detection, likelihood-ratio-vad, pitch-detection, source-filter-model, pre-emphasis, short-time-fourier-transform, cross-correlation]
sources:
  - paper: doi:10.1109/PROC.1986.13663
    title: Benjamin Kedem, Spectral analysis and discrimination by zero-crossings, Proceedings of the IEEE 74(11), 1986, 1477 to 1493
    locator: "the cosine formula that links the expected number of zero crossings of a stationary Gaussian sequence to its first autocorrelation, and the higher order crossings"
  - paper: doi:10.1002/j.1538-7305.1975.tb02840.x
    title: L. R. Rabiner and M. R. Sambur, An algorithm for determining the endpoints of isolated utterances, The Bell System Technical Journal 54(2), 1975, 297 to 315
    locator: the zero-crossing count of 10 ms frames and its use to find weak fricatives
  - book: isbn:9780132136037
    title: L. R. Rabiner and R. W. Schafer, Digital Processing of Speech Signals, Prentice Hall, 1978
    locator: "Chapter 4 (time domain processing of speech), the short-time average zero-crossing rate"
---

The zero-crossing rate of a frame of audio is the fraction of pairs of adjacent samples whose signs differ. It is a cheap measure of how much of the energy of the frame lies at high frequencies: hiss such as "s" or "f" crosses zero often, and voiced speech, whose energy is mostly below 1 kHz, crosses rarely. It is a measurement of one frame, not a decision; a [voice activity detector](/voice-activity-detection/) or the [Rabiner-Sambur endpoint detector](/rabiner-sambur-endpoint-detection/) uses it, together with the energy, to decide which frames are speech, and a [likelihood ratio VAD](/likelihood-ratio-vad/) uses a model of the spectrum in its place.

## Definition

Let $x[0], \ldots, x[N-1]$ be one frame with $N \ge 2$, and let $\operatorname{sgn}(v) = +1$ for $v \ge 0$ and $-1$ for $v < 0$, so that 0 counts as positive. The **zero-crossing count** of the frame is

$$Z = \sum_{n=1}^{N-1} \mathbb{1}\bigl[\operatorname{sgn}(x[n]) \ne \operatorname{sgn}(x[n-1])\bigr],$$

and the **zero-crossing rate** is $\mathrm{ZCR} = Z / (N - 1)$, a number between 0 and 1. Some texts divide by $N$ in place of $N - 1$, some report $Z$ itself per frame of fixed length, as Rabiner and Sambur do per 10 ms, and some report crossings per second, $\mathrm{ZCR} \cdot f_s$. Some count a crossing only when the product $x[n]\, x[n-1]$ is negative, so that samples equal to 0 never count. All these variants are proportional to each other for frames of a fixed length, except for the treatment of zeros.

**Facts that follow from the definition.**

- **Gain invariant (theorem).** Multiplying the frame by any $c > 0$ does not change $Z$. Multiplying by $c < 0$ does not change it either when no sample is 0.
- **Sinusoid (theorem, up to the frame edges).** The sampled sinusoid $\cos(2\pi f n / f_s + \varphi)$ with $0 < f < f_s / 2$ changes sign $2 f / f_s$ times per sample on average, so a frame of $N$ samples has about $2 f N / f_s$ crossings.
- **Gaussian noise (theorem).** For a stationary zero-mean Gaussian sequence with normalized first autocorrelation $\rho = r[1] / r[0]$, the probability that two adjacent samples differ in sign is $\arccos(\rho) / \pi$, so the expected ZCR is $\arccos(\rho)/\pi$. This is the cosine formula used by Kedem: $\rho = \cos(\pi\, \mathbb{E}[\mathrm{ZCR}])$.
- **Not offset invariant.** Adding a constant to the frame can change $Z$ a lot. A DC offset larger than the signal makes $Z = 0$.

## Examples and non-examples

- **A short frame.** For $x = (0.5, 0.2, -0.1, -0.4, 0.3, 0.0, -0.2, 0.1)$ the signs are $+, +, -, -, +, +, -, +$, since 0.0 counts as positive. The sign changes between samples 2 and 3, 4 and 5, 6 and 7, and 7 and 8, so $Z = 4$ and $\mathrm{ZCR} = 4/7 = 0.571$.
- **White noise.** Independent zero-mean Gaussian samples have $\rho = 0$ and $\mathrm{ZCR} = \arccos(0)/\pi = 0.5$.
- **Low-pass noise.** A first order autoregressive sequence with $\rho = 0.9$ has an expected ZCR of 0.1436, and one with $\rho = 0.98$ of 0.0638, about 10 crossings in a frame of 160 samples.
- **A tone.** At 16 kHz a 300 Hz tone has a ZCR of $2 \cdot 300 / 16000 = 0.0375$, about 6 crossings per 10 ms frame, and a 4 kHz tone has 0.5.
- **Speech.** Voiced frames have a low ZCR because their energy is mostly below 1 kHz, and unvoiced fricatives have a high one because their energy is mostly above 3 kHz. In the example of the [Rabiner-Sambur endpoint detector](/rabiner-sambur-endpoint-detection/), background frames have about 9 crossings per 160 samples and fricative frames between 62 and 96 (measurement on synthetic signals).
- **Non-example: pitch.** The ZCR of a voiced frame is not twice its fundamental frequency. Strong harmonics, such as a first formant at 700 Hz on a voice at 120 Hz, add crossings between the pitch periods. [Pitch detection](/pitch-detection/) uses the autocorrelation or similar methods.
- **Non-example: frequency of a mixture.** For a sum of tones, the ZCR is not a weighted mean of their frequencies; a small high tone added to a large low one adds no crossings until its amplitude is large enough to make the sum change sign.

## Related definitions

- **Short-time energy.** The energy $\sum_n x[n]^2$, or the sum of magnitudes, of a frame. Together with the ZCR it separates silence, voiced and unvoiced frames in simple detectors.
- **Autocorrelation.** By the cosine formula, the ZCR of a Gaussian sequence determines its normalized first [autocorrelation](/autocorrelation/) and back.
- **Higher order crossings.** Kedem's higher order crossings are the zero-crossing counts of the sequence after it has been differenced $0, 1, 2, \ldots$ times. They describe the spectrum in more detail than the single count.
- **Level-crossing rate.** The rate at which the signal crosses a level $c \ne 0$, or a band of $\pm c$ around 0, which makes the count less sensitive to low-level noise.
- **Spectral centroid.** The mean frequency of the power spectrum, a spectral measure that rises and falls with the ZCR on many signals, but needs an FFT.

## References
