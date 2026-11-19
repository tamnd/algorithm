---
tag: AJSQPY
kind: definition
slug: mel-scale
name: Mel scale
aliases:
- mel frequency scale
- mel
area: natural-language-and-speech/speech-analysis-and-synthesis
level: intro
summary: "A pitch scale from listener tests. Speech tools use m = 2595 log10(1 + f/700); other mel formulas exist, such as Slaney's and the 1937 table of Stevens, Volkmann and Newman."
prereqs: []
see_also: [mel-filter-bank, mel-frequency-cepstral-coefficients, perceptual-linear-prediction, delta-features, cepstral-mean-normalization, pre-emphasis, rasta-filtering, pitch-detection]
sources:
  - paper: doi:10.1121/1.1915893
    title: S. S. Stevens, J. Volkmann and E. B. Newman, A scale for the measurement of the psychological magnitude pitch, Journal of the Acoustical Society of America 8(3), 1937, 185 to 190
    locator: the listener experiments and the table of pitch in mels against frequency
  - paper: doi:10.1109/TASSP.1980.1163420
    title: S. B. Davis and P. Mermelstein, Comparison of parametric representations for monosyllabic word recognition in continuously spoken sentences, IEEE Transactions on Acoustics, Speech, and Signal Processing 28(4), 1980, 357 to 366
    locator: "Section II.C, footnote 1: the mel scale taken as linear below 1000 Hz and logarithmic above"
  - url: https://github.com/kaldi-asr/kaldi/blob/master/src/feat/mel-computations.h
    title: Kaldi speech recognition toolkit, src/feat/mel-computations.h
    locator: "the functions MelScale, 1127 ln(1 + f/700), and InverseMelScale"
  - url: https://github.com/librosa/librosa/blob/main/librosa/core/convert.py
    title: librosa, librosa/core/convert.py
    locator: "the function hz_to_mel: the Slaney scale by default, and 2595 log10(1 + f/700) when htk is true"
---

The mel scale maps a frequency $f$ in Hz to a perceived pitch $m$ in mels, so that equal steps in mels sound like equal steps in pitch. Speech toolkits use the formula $m = 2595 \log_{10}(1 + f/700)$, but it is a fit, and other mel scales are in use: the scale of Slaney's Auditory Toolbox and librosa, and the original table of Stevens, Volkmann and Newman (1937) from listener tests. The mel scale is only a frequency axis; the [mel filter bank](/mel-filter-bank/) places triangular filters on it, and [MFCC](/mel-frequency-cepstral-coefficients/) and the other speech front ends start from those filters.

## Definition

The **mel scale** used on this site and in most speech toolkits is

$$m(f) = 2595 \log_{10}\Bigl(1 + \frac{f}{700}\Bigr), \qquad f \ge 0,$$

with $f$ in Hz and $m$ in mels. Its inverse is $f(m) = 700\,(10^{m/2595} - 1)$. The function is strictly increasing and concave, $m(0) = 0$, and $m(1000) = 999.99$, so 1000 Hz is very close to 1000 mels.

The constant $2595$ is close to $1127 \ln 10$, so the form $m = 1127 \ln(1 + f/700)$, which Kaldi uses, is the same scale to about 4 significant digits: $2595 / \ln 10 = 1126.994$. At 4000 Hz the two forms give 2146.06 and 2146.08.

The slope is $dm/df = 2595 / ((700 + f) \ln 10)$, which is 1.61 mel per Hz at 0 Hz and 0.66 mel per Hz at 1000 Hz. For $f$ much smaller than 700 Hz, $m$ grows nearly in proportion to $f$; for $f$ much larger, $m$ grows nearly in proportion to $\log f$, so each doubling of the frequency adds nearly the same number of mels. The usual phrase "linear below 1 kHz and logarithmic above" describes this shape only loosely: at 500 Hz the formula is already 25 percent below its tangent line at 0.

The **Slaney scale**, from Slaney's Auditory Toolbox and the default of librosa, is a different function with a different unit:

$$m_S(f) = \begin{cases} f / f_{sp} & f < 1000 \\ 15 + \ln(f / 1000) / s & f \ge 1000 \end{cases}, \qquad f_{sp} = \tfrac{200}{3}, \quad s = \tfrac{\ln 6.4}{27}.$$

It is exactly linear below 1 kHz, where 1 kHz is 15 units, and exactly logarithmic above.

The **original mel scale** is the table of Stevens, Volkmann and Newman (1937). Listeners adjusted one pure tone until it sounded half as high, or twice as high, as another, and the scale was built from these judgments, with a 1000 Hz tone set at 1000 mels. The formulas above are fits to this shape and its later revisions, not the table itself.

## Examples and non-examples

| $f$ (Hz) | 100 | 250 | 500 | 700 | 1000 | 2000 | 4000 | 8000 |
|---|---|---|---|---|---|---|---|---|
| $2595 \log_{10}(1 + f/700)$ | 150.49 | 344.16 | 607.45 | 781.17 | 999.99 | 1521.36 | 2146.06 | 2840.02 |
| Slaney $m_S(f)$ | 1.5 | 3.75 | 7.5 | 10.5 | 15 | 25.08 | 35.16 | 45.25 |
| Slaney, scaled so 1000 Hz is 1000 | 100 | 250 | 500 | 700 | 1000 | 1672.1 | 2344.3 | 3016.4 |

- **Equal steps.** A [mel filter bank](/mel-filter-bank/) with 26 filters from 0 to 8000 Hz has its 28 edges every $2840.02 / 27 = 105.19$ mels, which gives edges 68.5 Hz apart at the bottom and 775 Hz apart at the top.
- **Two scales, different numbers.** Even after scaling the Slaney scale so that 1000 Hz is 1000, the two scales differ: 4000 Hz is 2146.06 on one and 2344.3 on the other. Filters built on the two scales are not the same.
- **Non-example: the octave scale.** A musical scale of semitones, $12 \log_2(f / f_0)$, is logarithmic at all frequencies. On the mel scale, the octave from 100 to 200 Hz spans 133 mels, and the octave from 2000 to 4000 Hz spans 625 mels.
- **Non-example: fundamental frequency.** The mel scale describes the pitch of pure tones as a function of their frequency. It does not say what pitch a complex sound such as a voiced vowel has; that is the task of [pitch detection](/pitch-detection/).

## Related definitions

- **Mel filter bank.** Triangular filters whose edges are equally spaced in mels; see [mel filter bank](/mel-filter-bank/).
- **Mel-frequency cepstral coefficients.** The cosine transform of the log energies of those filters; see [MFCC](/mel-frequency-cepstral-coefficients/).
- **Bark scale.** A scale of critical bands, about 24 Bark over the range of hearing. [Perceptual linear prediction](/perceptual-linear-prediction/) uses the form $6 \operatorname{asinh}(f / 600)$. It has a shape similar to the mel scale, with one Bark near 100 Hz wide at low frequencies.
- **ERB rate.** A scale based on the equivalent rectangular bandwidth of the auditory filters, used by gammatone filter banks. It also grows nearly linearly at low frequencies and logarithmically at high ones.
- **Other mel formulas.** Older work used $m = (1000 / \log_{10} 2) \log_{10}(1 + f / 1000)$, which is exactly 1000 at 1000 Hz, and Davis and Mermelstein took the scale as linear below 1000 Hz and logarithmic above.

## References
