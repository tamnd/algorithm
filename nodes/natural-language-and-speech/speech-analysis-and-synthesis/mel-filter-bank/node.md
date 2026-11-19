---
tag: 3Y1ZJS
kind: algorithm
slug: mel-filter-bank
name: Mel filter bank
aliases:
- mel filterbank
- log-mel spectrogram
- triangular mel filter bank
area: natural-language-and-speech/speech-analysis-and-synthesis
level: core
summary: Weight the power spectrum of each frame by triangular filters spaced evenly on the mel scale and take logs of the band energies.
solves: [automatic-speech-recognition]
model: real-ram
complexity:
  vars: {N: the FFT length, M: the number of filters, W: the frame length}
  time: {worst: O(W + N log N + M N)}
  space: {extra: O(M N)}
properties: {deterministic: true, online: true, in_place: false, exact: true}
history:
  year: 1980
  people: [Steven Davis, Paul Mermelstein]
  note: Davis and Mermelstein used 20 triangular filters, spaced linearly below 1 kHz and logarithmically above, as the first stage of their mel-frequency cepstrum, and showed that it beat the other representations they compared for word recognition.
prereqs: [mel-scale, short-time-fourier-transform, window-functions]
see_also: [mel-frequency-cepstral-coefficients, filter-bank, perceptual-linear-prediction, pre-emphasis, specaugment, automatic-speech-recognition, cepstral-mean-normalization, spectral-leakage]
sources:
  - paper: doi:10.1109/TASSP.1980.1163420
    title: S. B. Davis and P. Mermelstein, Comparison of parametric representations for monosyllabic word recognition in continuously spoken sentences, IEEE Transactions on Acoustics, Speech, and Signal Processing 28(4), 1980, 357 to 366
    locator: "Section II.C (Parametric Representations): the 20 triangular filters of Fig. 1, Eq. (1), and footnote 1 (linear spacing below 1000 Hz and logarithmic spacing above)"
  - paper: "Steve Young et al., The HTK Book (for HTK version 3.4), Cambridge University Engineering Department, 2006"
    title: The HTK Book, version 3.4
    locator: "Chapter Speech Input/Output, section Filterbank Analysis (triangular filters equally spaced on the mel scale, applied to the magnitude spectrum)"
  - book: isbn:9780130226167
    title: Xuedong Huang, Alex Acero and Hsiao-Wuen Hon, Spoken Language Processing, Prentice Hall, 2001
    locator: "Chapter 6 (Speech Signal Representations), section Perceptually Motivated Representations"
  - paper: doi:10.1121/1.1915893
    title: S. S. Stevens, J. Volkmann and E. B. Newman, A scale for the measurement of the psychological magnitude pitch, Journal of the Acoustical Society of America 8(3), 1937, 185 to 190
    locator: the listener experiments behind the mel scale
---

A mel filter bank turns the power spectrum of a short frame of audio into a few dozen band energies. Each band is a triangle in frequency, the triangle edges are equally spaced on the [mel scale](/mel-scale/), and the log of each energy is the output. The [mel scale](/mel-scale/) page defines the frequency axis only; this page builds the filters on it and applies them. The [MFCC](/mel-frequency-cepstral-coefficients/) of a frame are the discrete cosine transform of these log energies, and a general [filter bank](/filter-bank/) of signal processing splits a signal into subband signals that can be put back together, which this analysis does not try to do.

## In plain words

The ear hears small changes in pitch at low frequencies but only large changes at high frequencies. A mel filter bank copies this. It puts many narrow bands at the low end of the spectrum and fewer, wider bands at the high end. Each band adds up the energy of the spectrum inside it, with the most weight at its middle and less weight toward its edges. Neighbouring bands overlap by half, so no part of the spectrum between the first and the last band center is lost. Then each sum is replaced by its logarithm, because loudness is heard on a log scale and because a fixed gain then becomes an added constant. The result is a short list of numbers per frame, for example 40, instead of hundreds of spectrum values.

## The problem

Given a frame of $W$ samples at a sample rate of $f_s$ Hz, a window, an FFT length $N \ge W$, a number of filters $M$ and a frequency range $0 \le f_{lo} < f_{hi} \le f_s / 2$, compute $M$ log band energies. The power spectrum is $P[k] = |X[k]|^2$ for $k = 0, \ldots, N/2$, where $X$ is the DFT of the windowed frame padded with zeros to $N$ points, and bin $k$ is at the frequency $k f_s / N$. The defaults of this page are $f_s = 16$ kHz, $W = 400$ samples (25 ms), a hop of 160 samples (10 ms), the symmetric Hamming window, $N = 512$, $f_{lo} = 0$ and $f_{hi} = f_s / 2$. The frames are cut without padding, so a signal of $L \ge 400$ samples gives $1 + \lfloor (L - 400) / 160 \rfloor$ frames. Common values of $M$ are 26 (HTK), 23 (Kaldi) and 40 (the input of many neural networks).

## The algorithm

With $\operatorname{mel}(f) = 2595 \log_{10}(1 + f / 700)$, the edge frequencies are equally spaced in mel and the filter $m$ is a triangle that is linear in Hz, with its foot at $f_{m-1}$ and $f_{m+1}$ and its top at $f_m$.

```pseudo id=main
MEL-FILTER-BANK(P, f_s, N, M, f_lo, f_hi)       ▷ P[0 .. N/2] is the power spectrum
L1  require M ≥ 1 and 0 ≤ f_lo < f_hi ≤ f_s / 2
L2  m_lo ← mel(f_lo); m_hi ← mel(f_hi); Δ ← (m_hi - m_lo) / (M + 1)
L3  for i ← 0 to M + 1 do f_i ← mel⁻¹(m_lo + i Δ)
L4  for m ← 1 to M do
L5      for k ← 0 to N/2 do f ← k f_s / N
L6          if f_{m-1} < f ≤ f_m then W[m][k] ← (f - f_{m-1}) / (f_m - f_{m-1})
L7          else if f_m < f < f_{m+1} then W[m][k] ← (f_{m+1} - f) / (f_{m+1} - f_m)
L8          else W[m][k] ← 0
L9  for m ← 1 to M do E[m] ← Σ_k W[m][k] P[k]
L10 return ln max(E[m], 10⁻¹⁰) for m ← 1 to M
```

Lines L1 to L8 depend only on $f_s$, $N$, $M$ and the range, so a program builds the weights once and reuses them for every frame. Lines L9 and L10 run once per frame. The floor $10^{-10}$ in line L10 keeps the log finite on silent frames; toolkits use similar small floors.

This page applies the filters to the power spectrum, as Kaldi and librosa do. HTK applies them to the magnitude $|X[k]|$, so its band energies are a different quantity. Slaney's Auditory Toolbox and librosa by default also use a different mel scale and scale each triangle to unit area; see the variants below.

## Example

Take $f_s = 8000$ Hz, $N = 16$ (bins every 500 Hz), $M = 4$ and the full range 0 to 4000 Hz. Then $\operatorname{mel}(4000) = 2146.06$, the step is $\Delta = 429.21$ mel, and line L3 gives the edges 0, 324.5, 799.3, 1494.3, 2511.4 and 4000 Hz. Lines L4 to L8 give these weights, rounded:

| bin $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| frequency (Hz) | 0 | 500 | 1000 | 1500 | 2000 | 2500 | 3000 | 3500 | 4000 |
| filter 1 | 0 | 0.630 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| filter 2 | 0 | 0.370 | 0.711 | 0 | 0 | 0 | 0 | 0 | 0 |
| filter 3 | 0 | 0 | 0.289 | 0.994 | 0.503 | 0.011 | 0 | 0 | 0 |
| filter 4 | 0 | 0 | 0 | 0.006 | 0.497 | 0.989 | 0.672 | 0.336 | 0 |
| sum | 0 | 1 | 1 | 1 | 1 | 1 | 0.672 | 0.336 | 0 |

Every bin between the first center (324.5 Hz) and the last center (2511.4 Hz) gets a total weight of 1. Filter 1 covers a single bin, because 16 points are too few for its narrow band; with $N = 512$ at 16 kHz and $M = 26$, the first filter runs from 0 to 143.7 Hz and covers 4 bins. For the power spectrum $P = (0, 4, 1, 0, 0, 0, 0, 0, 0)$, line L9 gives the energies 2.5214, 2.1899, 0.2887 and 0, and line L10 gives the log energies 0.9248, 0.7838, $-1.2422$ and $\ln 10^{-10} = -23.0259$.

## Correctness

The filter bank computes a defined transform, so correctness means that the weights have the shape the definition asks for. The full proofs are below.

- **The edges are equally spaced in mel.** Since $\operatorname{mel}$ is strictly increasing and line L3 applies its inverse, $\operatorname{mel}(f_i) = m_{lo} + i \Delta$, so the edges increase and $f_0 = f_{lo}$, $f_{M+1} = f_{hi}$ (theorem).
- **Each filter is a triangle.** Line L6 gives the rising side and line L7 the falling side, so $0 \le W[m][k] \le 1$, the weight is positive only for $f_{m-1} < f < f_{m+1}$, and it is 1 exactly when $f = f_m$ (theorem).
- **The filters overlap by half.** For every frequency $f$ with $f_1 \le f \le f_M$, the weights of all filters at $f$ sum to 1, and at most two of them are positive (theorem). So a flat power spectrum gives band energies that are proportional to the number of bins in each band.
- **The log turns gains into offsets.** If the spectrum is multiplied by $c > 0$ and the energies stay above the floor, every log energy grows by $\ln c$ (theorem). A fixed channel gain thus adds a constant to each band, which [cepstral mean normalization](/cepstral-mean-normalization/) removes later.

## Complexity

In the [real RAM](/real-ram/), the window costs $O(W)$, the FFT $O(N \log N)$ and line L9 $O(M N)$ with the dense weight table. Because each bin lies in at most two triangles, a sparse table of the nonzero weights makes line L9 cost $O(N)$, so the FFT dominates. Building the table in lines L1 to L8 costs $O(M N)$ once. The table takes $O(M N)$ memory, or $O(N)$ in sparse form. For one second of 16 kHz audio there are 98 frames, each with one FFT of 512 points.

## Properties

- **Fixed and linear before the log.** The band energies are a fixed linear map of the power spectrum, so they can be computed as one matrix product for all frames.
- **Resolution follows the ear.** At 16 kHz with 26 filters the bands are about 140 Hz wide at the low end and about 1500 Hz wide at the top.
- **Loses the fine structure.** The triangles are wider than the spacing of the pitch harmonics for most voices, so the energies follow the spectral envelope and mostly discard the pitch. This is useful for recognizing words and a loss for pitch or speaker work.
- **Correlated outputs.** Neighbouring log energies overlap and are strongly correlated. The DCT of [MFCC](/mel-frequency-cepstral-coefficients/) mostly removes this for models with diagonal covariances; neural networks take the log energies directly.

## Variants and improvements

- **Slaney's scale and unit-area filters.** The Auditory Toolbox of Slaney, and librosa by default, use a mel scale that is linear below 1 kHz with a step of $200/3$ Hz per mel and logarithmic above with a step of $\ln(6.4)/27$ per mel, and scale each triangle to unit area, so the high bands get smaller weights.
- **Magnitude in place of power.** HTK sums the magnitude $|X[k]|$. For a band with one strong bin the log energy is then about half the log energy from the power spectrum, and a model trained on one kind does not work on the other.
- **Band limits.** A low edge of 20 to 133 Hz removes hum and DC, and a high edge below $f_s / 2$ ignores the region where the anti-aliasing filter cuts.
- **Other warpings.** The Bark scale of [perceptual linear prediction](/perceptual-linear-prediction/) uses trapezoid-like masking curves in place of triangles, and gammatone filter banks model the cochlea more closely.
- **Learned front ends.** Some neural systems learn the filters from raw audio, often starting from mel triangles.
- **Data augmentation.** [SpecAugment](/specaugment/) masks blocks of bands and frames of the log energies during training.

## When to use it

Use a mel filter bank as the front end of a speech recognizer, a keyword spotter or an audio classifier, where the input is a spectrogram and the model is a neural network; 40 to 80 filters are common there. Use it as the first stage of [MFCC](/mel-frequency-cepstral-coefficients/) when the model wants decorrelated features, such as a [GMM-HMM](/gmm-hmm-acoustic-model/). Do not use it when the task needs the harmonics, such as [pitch detection](/pitch-detection/), or when the signal must be rebuilt from the bands: the triangles throw information away, and a perfect reconstruction [filter bank](/filter-bank/) is the tool for coding.

## Pitfalls

- **Mixing conventions.** The scale (O'Shaughnessy or Slaney), power or magnitude, the normalization of the triangles and the log floor all change the numbers. Features from two toolkits match only when all four match.
- **Empty filters.** With many filters and a short FFT, the lowest triangles can fall between two bins and get no weight at all, so their energy is always 0 and the log is the floor. Check that each row has a nonzero weight, or lower $M$ or raise $N$.
- **Log of zero.** Digital silence gives a zero energy; without the floor the log is minus infinity and the next layers fail.
- **Frame count.** Toolkits differ on padding. This page drops the last partial frame; librosa by default pads the signal by half the FFT length on each side, which adds frames.
- **Sample rate change.** Weights built for 16 kHz are wrong for 8 kHz audio, because the bin frequencies change with $f_s$.

## Implementations

## History

The mel scale comes from the listening experiments of Stevens, Volkmann and Newman in 1937. Filter banks with bands that widen with frequency were used in speech analysis long before digital computers, in vocoders and in the sound spectrograph. In 1980 Davis and Mermelstein computed 20 triangular filters, linear below 1 kHz and logarithmic above, on a DFT spectrum, took the cosine transform of their log outputs, and found that these mel-frequency cepstral coefficients gave the best recognition among the representations they compared. HTK, and later Kaldi, built the triangles on the formula $2595 \log_{10}(1 + f / 700)$, Kaldi in the form $1127 \ln(1 + f/700)$, which agrees with it to about 4 digits. With deep neural networks in the 2010s, the log filter bank energies themselves, without the cosine transform, became the most common input of speech recognizers.

## References
