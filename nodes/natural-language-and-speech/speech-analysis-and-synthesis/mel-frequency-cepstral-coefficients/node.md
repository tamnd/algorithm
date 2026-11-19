---
tag: 85RNE7
kind: algorithm
slug: mel-frequency-cepstral-coefficients
name: Mel-frequency cepstral coefficients
aliases:
- MFCC
- mel cepstrum
area: natural-language-and-speech/speech-analysis-and-synthesis
level: core
summary: Speech features from the discrete cosine transform of the log mel filter bank energies of each frame, keeping the first dozen or so.
solves: [automatic-speech-recognition]
model: real-ram
complexity:
  vars: {T: the number of frames, N: the FFT length, M: the number of filters, K: the number of coefficients kept}
  time: {worst: O(T (N log N + M N + K M))}
  space: {extra: O(M N + T K)}
properties: {deterministic: true, online: true, in_place: false, exact: true}
history:
  year: 1980
  people: [Steven Davis, Paul Mermelstein]
  note: Davis and Mermelstein took the cosine transform of the log outputs of 20 mel-spaced triangular filters, and found these coefficients better for recognizing words in sentences than linear frequency cepstra, linear prediction coefficients and their cepstra.
prereqs: [mel-filter-bank, pre-emphasis, discrete-cosine-transform, cepstrum]
see_also: [delta-features, cepstral-mean-normalization, perceptual-linear-prediction, mel-scale, gmm-hmm-acoustic-model, dynamic-time-warping, speaker-verification, linear-predictive-coding]
sources:
  - paper: doi:10.1109/TASSP.1980.1163420
    title: S. B. Davis and P. Mermelstein, Comparison of parametric representations for monosyllabic word recognition in continuously spoken sentences, IEEE Transactions on Acoustics, Speech, and Signal Processing 28(4), 1980, 357 to 366
    locator: "Section II.C (Parametric Representations): Eq. (1), the cosine transform of the log energies of the 20 filters of Fig. 1"
  - paper: "Steve Young et al., The HTK Book (for HTK version 3.4), Cambridge University Engineering Department, 2006"
    title: The HTK Book, version 3.4
    locator: "Chapter Speech Input/Output, sections Filterbank Analysis and Cepstral Features (the DCT of the log filter bank amplitudes and the sine lifter with CEPLIFTER)"
  - book: isbn:9780130226167
    title: Xuedong Huang, Alex Acero and Hsiao-Wuen Hon, Spoken Language Processing, Prentice Hall, 2001
    locator: "Chapter 6 (Speech Signal Representations), sections Cepstral Processing and Perceptually Motivated Representations"
  - book: isbn:9780136034285
    title: Lawrence R. Rabiner and Ronald W. Schafer, Theory and Applications of Digital Speech Processing, Pearson, 2010
    locator: Chapter 8 (the cepstrum and homomorphic speech processing)
  - paper: doi:10.1121/1.1914702
    title: B. S. Atal, Effectiveness of linear prediction characteristics of the speech wave for automatic speaker identification and verification, Journal of the Acoustical Society of America 55(6), 1974, 1304 to 1312
    locator: the comparison of parameters derived from linear prediction, in which the cepstrum did best
---

Mel-frequency cepstral coefficients, or MFCC, are a short vector of numbers per frame of speech, usually 13, that describe the shape of the spectral envelope. They are computed by [pre-emphasis](/pre-emphasis/), a [mel filter bank](/mel-filter-bank/) with a log, and a discrete cosine transform of the log energies, of which only the first coefficients are kept. They differ from the log mel energies of the [mel filter bank](/mel-filter-bank/) only by that last transform, which decorrelates them and drops the fine detail, and from [PLP](/perceptual-linear-prediction/) cepstra, which smooth a Bark-scale spectrum with an all-pole model in place of the cosine transform. [Delta features](/delta-features/) and [cepstral mean normalization](/cepstral-mean-normalization/) are usually applied to MFCC afterwards.

## In plain words

A speech sound is shaped mostly by the mouth and throat, and that shape shows as a smooth outline of the spectrum, with peaks at the resonances. MFCC describe that outline with a few numbers. First, the high frequencies are boosted a little. Then the signal is cut into short overlapping pieces, and for each piece the energy in about 26 bands is measured, with narrow bands at low pitch and wide bands at high pitch, as the ear does. The logs of these energies are then described as a sum of cosine waves across the bands. The first cosine gives the overall loudness, the next ones give the broad tilt and the large bumps, and the later ones give finer detail. Keeping only the first 13 keeps the outline and drops the ripples that come from the pitch of the voice.

## The problem

Given a signal $x[0 \ldots L-1]$ with samples in $[-1, 1]$ at $f_s$ Hz, compute one vector $c_0, \ldots, c_{K-1}$ per frame. The defaults of this page are those of HTK where it has one: $f_s = 16$ kHz, pre-emphasis with $\alpha = 0.97$, frames of $W = 400$ samples with a hop of 160 and no padding, so $1 + \lfloor (L - 400)/160 \rfloor$ frames, the symmetric Hamming window, an FFT of $N = 512$ points, $M = 26$ triangular filters from 0 Hz to $f_s/2$ on the scale $2595 \log_{10}(1 + f / 700)$, the natural log with a floor of $10^{-10}$, $K = 13$ coefficients $c_0$ to $c_{12}$, and a sine lifter with $Q = 22$. Kaldi uses 23 filters by default. This page applies the filters to the power spectrum; HTK applies them to the magnitude, and its numbers differ.

## The algorithm

The orthonormal DCT-II of the $M$ log energies $\ell_1, \ldots, \ell_M$ is

$$c_n = s_n \sum_{m=1}^{M} \ell_m \cos\Bigl(\frac{\pi n (m - \frac{1}{2})}{M}\Bigr), \qquad s_0 = \sqrt{1/M},\ s_n = \sqrt{2/M} \text{ for } n \ge 1,$$

and the sine lifter multiplies $c_n$ by $1 + \frac{Q}{2} \sin(\pi n / Q)$.

```pseudo id=main
MFCC(x, f_s, M, K, Q)
L1  y[0] ← x[0]; y[n] ← x[n] - 0.97 x[n - 1] for n ≥ 1     ▷ pre-emphasis
L2  W ← the M triangular mel weights for N = 512 and f_s       ▷ MEL-FILTER-BANK lines L1 to L8
L3  for each frame v of y (400 samples, hop 160, no padding) do
L4      u[i] ← v[i] · (0.54 - 0.46 cos(2π i / 399)) for i ← 0 to 399
L5      P[k] ← |Σ_i u[i] e^{-2π j k i / 512}|² for k ← 0 to 256   ▷ by the FFT
L6      E[m] ← Σ_k W[m][k] P[k] for m ← 1 to M
L7      ℓ[m] ← ln max(E[m], 10⁻¹⁰)
L8      c ← the first K values of the orthonormal DCT-II of ℓ
L9      output c'[n] ← (1 + (Q/2) sin(π n / Q)) c[n] for n ← 0 to K - 1
```

Line L1 runs over the whole signal; HTK applies it inside each frame, which changes only the first sample of each frame. Line L4 uses the symmetric Hamming window, which is 0.08 at both ends. Lines L6 and L7 are lines L9 and L10 of the [mel filter bank](/mel-filter-bank/). Line L8 is the [discrete cosine transform](/discrete-cosine-transform/) of type II. Davis and Mermelstein wrote it without the factors $s_n$, as $\sum_{k=1}^{20} X_k \cos[i (k - \frac{1}{2}) \pi / 20]$; HTK uses $\sqrt{2/M}$ for every $n$, including $c_0$. The orthonormal form of this page makes the transform an orthogonal matrix. Many systems replace $c_0$ by the log energy of the frame.

## Example

A frame of digital silence gives $E[m] = 0$ for all $m$, so line L7 gives $\ell_m = \ln 10^{-10} = -23.026$ in every band. The DCT of a constant vector is zero except for $c_0 = \sqrt{M} \cdot (-23.026)$, which for $M = 26$ is $-117.41$, and the lifter leaves $c_0$ unchanged. So silence is the vector $(-117.41, 0, 0, \ldots, 0)$.

If a frame is multiplied by 3, every power value is multiplied by 9 and every log energy grows by $\ln 9$. Again only $c_0$ changes, by $\sqrt{26} \ln 9 = 11.204$. All of $c_1$ to $c_{12}$ stay the same, so they do not depend on the loudness.

The lifter weights for $Q = 22$ are, for $n = 0$ to 12: 1, 2.565, 4.099, 5.570, 6.947, 8.203, 9.313, 10.254, 11.006, 11.554, 11.888, 12 and 11.888. They raise the higher coefficients, which are small, to a size like the lower ones.

For a sine of 440 Hz and amplitude 1 at 16 kHz, the first frame gives, rounded, $c = (-20.88, 25.09, 7.73, -14.20, -37.94, -55.69, -57.34, -42.73, -15.04, 14.12, 35.33, 41.53, 33.93)$. One second of this signal gives 98 such vectors.

## Correctness

MFCC are a defined transform, so correctness means that each line computes its part. The full proofs are below.

- **The DCT is orthogonal.** With the factors $s_n$, the full $M \times M$ DCT-II matrix $C$ has $C C^{\mathsf T} = I$ (theorem). So with $K = M$ and no lifter, $\sum_n c_n^2 = \sum_m \ell_m^2$, and no information is lost before the truncation to $K$ coefficients.
- **Loudness goes into $c_0$ only.** A gain $g$ on the frame adds $2 \ln |g|$ to every $\ell_m$ above the floor. The DCT of a constant vector is zero in every coefficient but $c_0$, so only $c_0$ changes, by $2 \sqrt{M} \ln |g|$ (theorem).
- **A fixed channel becomes an additive constant, approximately.** A linear filter with frequency response $H$ multiplies $P[k]$ by about $|H(f_k)|^2$. If $|H|$ is nearly constant inside each band, every $\ell_m$ grows by a fixed amount $\ln |H(f_m)|^2$, and every frame's $c$ by one fixed vector (heuristic: exact only for a flat response in each band and a filter much shorter than the frame). [Cepstral mean normalization](/cepstral-mean-normalization/) uses this.
- **Truncation smooths.** Keeping the first $K$ of $M$ coefficients and inverting gives the least squares fit of $\ell$ by the first $K$ cosines, a smoothed version of the log spectrum (theorem, from the orthogonality).

## Complexity

In the [real RAM](/real-ram/), each frame costs $O(W)$ for lines L4 and line L1's share, $O(N \log N)$ for the FFT, $O(M N)$ for line L6 with dense weights (or $O(N)$ with sparse weights), and $O(K M)$ for the DCT done directly, so $T$ frames cost $O(T (N \log N + M N + K M))$. The weights take $O(M N)$ memory and the output $O(T K)$. With the defaults, one second of audio is 98 FFTs of 512 points, which is small work for any processor.

## Properties

- **Compact.** 13 numbers per 10 ms describe the envelope; with the [delta features](/delta-features/) the usual vector has 39.
- **Nearly decorrelated.** The DCT is close to the principal components of log filter bank energies of speech (a measurement, not a theorem), so the coefficients are nearly uncorrelated, and a [Gaussian mixture](/gaussian-mixture-model/) with diagonal covariances fits them well.
- **Gain invariant except $c_0$.** By the second claim above.
- **Sensitive to additive noise.** Noise adds to the power, not to the log, so it changes the coefficients in a nonlinear way; low energy bands are hit hardest.
- **Not invertible.** The pitch harmonics and the phase are gone, so speech cannot be rebuilt well from MFCC alone.

## Variants and improvements

- **Energy in place of $c_0$.** HTK and many systems append the log energy of the frame and drop $c_0$, or keep both.
- **Number of filters and coefficients.** 20 filters (Davis and Mermelstein), 23 (Kaldi), 26 (HTK) or 40; 12 or 13 coefficients for recognition, more for speaker work.
- **Liftering.** The sine lifter with $Q = 22$ is HTK's; others use no lifter, because a diagonal-covariance model removes the scale anyway.
- **Normalization.** [Cepstral mean normalization](/cepstral-mean-normalization/) and variance normalization over the utterance or a sliding window, and [vocal tract length normalization](/vocal-tract-length-normalization/), which warps the filter frequencies per speaker.
- **Relatives.** [PLP](/perceptual-linear-prediction/) cepstra replace the filter bank and DCT by a Bark spectrum and an all-pole fit; [RASTA filtering](/rasta-filtering/) filters the log bands over time before the transform; LPC cepstra come from [linear predictive coding](/linear-predictive-coding/).
- **No DCT.** Neural network recognizers mostly take the log mel energies directly, because they do not need decorrelated inputs.

## When to use it

Use MFCC for classical speech recognition with [GMM-HMM](/gmm-hmm-acoustic-model/) models, for template matching with [dynamic time warping](/dynamic-time-warping/), and for speaker features such as [i-vectors](/i-vector/), where decorrelated low-dimensional inputs matter. They are also a cheap and robust feature for audio classification with small data. For neural networks trained on large data, log mel filter bank energies usually work as well or better. For tasks that need pitch, such as intonation or tone languages, add a pitch feature, because MFCC remove most of it.

## Pitfalls

- **Comparing toolkits.** Power or magnitude, the mel formula, the filter count, the DCT scaling, the lifter, the log floor and per-frame or whole-signal pre-emphasis all differ between HTK, Kaldi and librosa, and change the numbers.
- **Too many filters for the FFT.** With 40 or more filters and a short FFT, the lowest filters can be empty. Check that every filter has a nonzero weight.
- **Silence and the floor.** Digital silence gives $c_0$ at the floor and the other coefficients 0; frames near silence give large, noisy values. Many systems add a tiny dither noise before the analysis.
- **Mismatched sample rates.** Features of 8 kHz audio and 16 kHz audio are not comparable, because the filter range changes.
- **Expecting noise robustness.** MFCC are not robust to additive noise; use noise reduction, such as [spectral subtraction](/spectral-subtraction/), or train on noisy data.

## Implementations

## History

The cepstrum of Bogert, Healy and Tukey (1963) and Noll's use of it for pitch led to cepstral features for speech, and in 1974 Atal found the LPC cepstrum the best of the linear prediction parameters for speaker recognition. In 1980 Davis and Mermelstein put the cepstrum on the mel scale: they took the cosine transform of the log outputs of 20 triangular filters, linear below 1 kHz and logarithmic above, and found these mel-frequency cepstral coefficients the best of the representations they compared for recognizing monosyllabic words in sentences. HTK made 26 filters, 12 or 13 coefficients, the lifter with 22 and the 39-dimensional vector with [delta features](/delta-features/) a standard in the 1990s. MFCC were the main feature of speech recognition until the move to neural networks in the 2010s, and they remain common in speaker recognition and audio classification.

## References
