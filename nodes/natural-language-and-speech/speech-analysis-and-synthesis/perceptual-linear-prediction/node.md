---
tag: H7TRFV
kind: algorithm
slug: perceptual-linear-prediction
name: Perceptual linear prediction
aliases:
- PLP
- PLP analysis
area: natural-language-and-speech/speech-analysis-and-synthesis
level: advanced
summary: 'Hermansky''s features: a Bark-scale critical band spectrum with equal loudness and cube-root compression, modeled by an all-pole fit.'
solves: [automatic-speech-recognition]
model: real-ram
complexity:
  vars: {N: the FFT length, M: the number of critical band samples, p: the model order}
  time: {worst: O(N log N + M N + M p + p^2)}
  space: {extra: O(M N)}
properties: {deterministic: true, online: true, in_place: false, exact: true}
history:
  year: 1990
  people: [Hynek Hermansky]
  note: Hermansky combined three ideas from hearing research, critical band integration, equal loudness and the cube root law of loudness, with an all-pole model of the resulting spectrum, and found that a 5th order model gave features that depend less on the speaker than plain linear prediction.
prereqs: [linear-predictive-coding, levinson-durbin-recursion, short-time-fourier-transform, cepstrum]
see_also: [rasta-filtering, mel-frequency-cepstral-coefficients, mel-filter-bank, linear-prediction, formant-estimation, autocorrelation, cepstral-mean-normalization, automatic-speech-recognition]
sources:
  - paper: doi:10.1121/1.399423
    title: Hynek Hermansky, Perceptual linear predictive (PLP) analysis of speech, Journal of the Acoustical Society of America 87(4), 1990, 1738 to 1752
    locator: "the steps of the analysis (the Bark warping, the critical band curve, the equal loudness curve, the cube root law and the all-pole model fitted through the inverse DFT) and the experiments that recommend a 5th order model"
  - paper: "Steve Young et al., The HTK Book (for HTK version 3.4), Cambridge University Engineering Department, 2006"
    title: The HTK Book, version 3.4
    locator: "Chapter Speech Input/Output, section Perceptual Linear Prediction (PLP computed on a mel filter bank)"
  - book: isbn:9780130226167
    title: Xuedong Huang, Alex Acero and Hsiao-Wuen Hon, Spoken Language Processing, Prentice Hall, 2001
    locator: "Chapter 6 (Speech Signal Representations), sections Linear Predictive Coding and Perceptually Motivated Representations"
  - paper: doi:10.1109/TASSP.1980.1163420
    title: S. B. Davis and P. Mermelstein, Comparison of parametric representations for monosyllabic word recognition in continuously spoken sentences, IEEE Transactions on Acoustics, Speech, and Signal Processing 28(4), 1980, 357 to 366
    locator: "Section II.C, Eq. (3): the cepstrum computed directly from the linear prediction coefficients"
---

Perceptual linear prediction, or PLP, is the feature extractor of Hermansky (1990): it warps the power spectrum of a frame to the Bark scale, smooths it with a critical band curve, weights it by an equal loudness curve and takes its cube root, and then fits an all-pole model to the result. Plain [linear predictive coding](/linear-predictive-coding/) fits the all-pole model to the spectrum as it is, with the same resolution at all frequencies; PLP fits it to a spectrum that has first been reshaped to match hearing, so a low model order such as 5 is enough. [MFCC](/mel-frequency-cepstral-coefficients/) shape the spectrum with a [mel filter bank](/mel-filter-bank/) and a log and then use a cosine transform, where PLP uses the cube root and the all-pole fit. [RASTA filtering](/rasta-filtering/) is often added to PLP to remove slow channel effects.

## In plain words

PLP first changes the spectrum of a short frame of speech the way the ear would. It spreads the frequencies on a scale where equal steps sound like equal steps, and it sums the energy in bands about as wide as the ear's own filters. It then lowers the very low and very high frequencies, which the ear hears less, and compresses loud and soft parts with a cube root, as loudness grows with the cube root of power. On this reshaped spectrum it fits a smooth curve with only a few peaks, using the same method that linear prediction uses on the raw spectrum. The curve's few numbers, usually turned into cepstral coefficients, are the features. Because the reshaping hides details that differ between speakers, a curve with just two peaks describes the vowel well.

## The problem

Given a frame of speech at a sample rate of $f_s$ Hz and a model order $p$, compute the cepstrum $c_0, \ldots, c_K$ of an all-pole model of the auditory spectrum of the frame. Hermansky's analysis has these steps. The frame is windowed (Hamming) and its power spectrum $P(\omega)$ is computed by the FFT. The frequency $f$ in Hz goes to the Bark value

$$\Omega(f) = 6 \ln\Bigl(\frac{f}{600} + \sqrt{\Bigl(\frac{f}{600}\Bigr)^2 + 1}\Bigr) = 6 \operatorname{asinh}(f / 600).$$

The critical band curve, with $z$ in Bark, is

$$\psi(z) = \begin{cases} 0 & z < -1.3 \\ 10^{2.5 (z + 0.5)} & -1.3 \le z < -0.5 \\ 1 & -0.5 \le z \le 0.5 \\ 10^{-(z - 0.5)} & 0.5 < z \le 2.5 \\ 0 & z > 2.5, \end{cases}$$

the equal loudness curve, with $\omega = 2\pi f$ in rad/s, is

$$E(\omega) = \frac{(\omega^2 + 56.8 \cdot 10^6)\, \omega^4}{(\omega^2 + 6.3 \cdot 10^6)^2\, (\omega^2 + 0.38 \cdot 10^9)},$$

and the intensity-to-loudness law is $\Phi = \Xi^{0.33}$. The all-pole model is $g / |A(e^{j\omega})|^2$ with $A(z) = 1 - \sum_{k=1}^{p} a_k z^{-k}$.

## The algorithm

The band centers $\Omega_0, \ldots, \Omega_{M-1}$ are $M = \lceil \Omega(f_s/2) \rceil + 1$ points evenly spaced from 0 to $\Omega(f_s/2)$, a little under 1 Bark apart. Bin $k$ of the FFT is at $f_k = k f_s / N$.

```pseudo id=main
PLP(frame, f_s, p, K)
L1  P[k] ← |FFT_N(Hamming · frame)[k]|² for k ← 0 to N/2
L2  W[i][k] ← ψ(Ω_i - Ω(f_k)) for i ← 0 to M - 1 and k ← 0 to N/2
L3  θ[i] ← Σ_k W[i][k] P[k]                         ▷ critical band integration
L4  ξ[i] ← E(2π · Ω⁻¹(Ω_i)) · θ[i]                  ▷ equal loudness
L5  φ[i] ← ξ[i]^0.33                                ▷ cube root law
L6  φ[0] ← φ[1]; φ[M - 1] ← φ[M - 2]
L7  r[τ] ← (φ[0] + 2 Σ_{i=1}^{M-2} φ[i] cos(π τ i / (M - 1)) + φ[M - 1] cos(π τ)) / (2(M - 1)) for τ ← 0 to p
L8  (a_1 … a_p, g) ← LEVINSON-DURBIN(r, p)
L9  c_0 ← ln g; c_m ← a_m + Σ_{k=1}^{m-1} (k/m) c_k a_{m-k} for m ← 1 to K   ▷ a_j = 0 for j > p
```

Line L2 sums over the FFT bins with the weight $\psi(\Omega_i - \Omega(f_k))$; a bin contributes to band $i$ when it lies between 2.5 Bark below and 1.3 Bark above the center, the same reach as the integration of the paper, which resamples the warped spectrum instead. Line L6 copies the end values, because the two end bands have no data beyond the band edges; the paper does the same. Line L7 is the inverse DFT of the even extension of $\phi$ over $2(M-1)$ points, so $r$ is the autocorrelation of a signal whose power spectrum on the Bark axis is $\phi$. Line L8 is the [Levinson-Durbin recursion](/levinson-durbin-recursion/), as in [linear predictive coding](/linear-predictive-coding/), and $g$ is its final prediction error. Line L9 turns the model into its cepstrum, the usual output. The model lives on the Bark axis: $\omega = \pi$ in $A(e^{j\omega})$ means $f_s / 2$, and $\omega = \pi \Omega / \Omega(f_s/2)$ in general.

## Example

Take $f_s = 8000$ Hz, so $\Omega(4000) = 15.58$ Bark, $M = 17$ bands 0.973 Bark apart, centered at 0, 98, 198, 304, 417, 542, 681, 838, 1017, 1222, 1460, 1737, 2059, 2436, 2877, 3394 and 4000 Hz. The equal loudness weight is $-32.8$ dB at 100 Hz, $-12.0$ dB at 500 Hz, $-7.7$ dB at 1 kHz, $-4.3$ dB at 2 kHz and $-1.8$ dB at 4 kHz, relative to its limit at high frequencies.

A pulse train of 100 Hz through one resonance at 1000 Hz with a bandwidth of 80 Hz gives, for a frame of 200 samples (25 ms), the auditory spectrum $\phi$ = 0.194, 0.194, 0.468, 0.750, 1.066, 1.473, 2.073, 4.153, 6.955, 5.356, 3.201, 1.973, 1.583, 1.388, 1.280, 1.240, 1.240, with its peak in the band at 1017 Hz. A 5th order model gives $a = (-0.2828, -0.5812, -0.2315, -0.0571, -0.0879)$, $g = 1.4723$, and the cepstrum $c_0$ to $c_5$ = 0.3869, $-0.2828$, $-0.5413$, $-0.0747$, 0.1325, $-0.0384$. The peak of the model spectrum, mapped back from the Bark axis, is at 1104 Hz. For resonances at 500, 1500 and 2000 Hz the peaks are at 531, 1577 and 2059 Hz, all within 0.6 Bark of the resonance.

## Correctness

PLP computes a defined feature, so correctness means that lines L7 to L9 do what they claim for the auditory spectrum built in lines L1 to L6. The full proofs are below.

- **Line L7 gives a valid autocorrelation.** If every $\phi[i] > 0$, the Toeplitz matrix of $r[0], \ldots, r[p]$ is positive definite (theorem), so the Levinson-Durbin recursion runs without division by zero, every reflection coefficient has $|k| < 1$, and $A$ has all its zeros inside the unit circle.
- **Line L9 is the cepstrum of the model.** With $A$ minimum phase, the numbers of line L9 are the Fourier coefficients of $\ln(g / |A(e^{j\omega})|^2)$: $\ln(g/|A|^2) = \sum_{m=-\infty}^{\infty} c_{|m|} e^{-j\omega m}$ (theorem).
- **Loudness moves only $c_0$.** A gain $s$ on the frame multiplies $\theta$ and $\xi$ by $s^2$, $\phi$ and $r$ by $s^{0.66}$, leaves $a$ unchanged and multiplies $g$ by $s^{0.66}$, so only $c_0$ changes, by $0.66 \ln |s|$ (theorem).
- **The model peak follows a formant.** A 5th order model has room for two resonances, and on vowel-like inputs its peaks sit near the formants on the Bark axis, as in the example (measurement). Hermansky's experiments that favour order 5 for speaker-independent features are measurements too.

## Complexity

In the [real RAM](/real-ram/), line L1 costs $O(N \log N)$, line L2 $O(M N)$ but only once per sample rate, line L3 $O(M N)$ with the dense weights or $O(N)$ with only the nonzero ones, lines L4 to L6 $O(M)$, line L7 $O(M p)$, line L8 $O(p^2)$ and line L9 $O(K p)$. With $M$ about 17 to 21 and $p = 5$ to 12, the FFT dominates. The weight table takes $O(M N)$ memory.

## Properties

- **Low order.** The reshaped spectrum is smooth enough that a 5th order model describes the first two formants, against 10 to 14 for plain LPC at 8 to 10 kHz.
- **Gain separated.** The predictor $a$ does not depend on the loudness, and all of it goes to $g$ and $c_0$.
- **Less speaker dependent.** By smoothing over critical bands, PLP hides details such as the exact higher formants, which vary between speakers more than between vowels (measurement in the paper).
- **Not robust to the channel by itself.** A fixed filter still changes the spectrum; [RASTA filtering](/rasta-filtering/) or [cepstral mean normalization](/cepstral-mean-normalization/) is needed for that.

## Variants and improvements

- **RASTA-PLP.** Filter the log critical band trajectories over time with the [RASTA filter](/rasta-filtering/) between lines L3 and L4, then exponentiate; this removes slow channel effects and is the common form in noisy and telephone speech.
- **PLP on mel filters.** HTK computes PLP from its mel filter bank, with the equal loudness curve and the cube root applied to the filter outputs, and allows higher orders such as 12 for recognition.
- **Order and number of cepstra.** Order 5 for speaker independence, orders 8 to 14 when more detail is wanted; usually 13 cepstra with [delta features](/delta-features/).
- **Other loudness laws.** Some front ends use a log or a smaller power in place of the cube root; the all-pole fit then models a more compressed spectrum.

## When to use it

Use PLP in place of or beside [MFCC](/mel-frequency-cepstral-coefficients/) for GMM-HMM speech recognition, especially in the RASTA-PLP form for telephone or noisy speech, and when features should depend little on the speaker. Systems that combine several front ends often include it. For neural network recognizers trained on large data the log mel energies of a [mel filter bank](/mel-filter-bank/) are simpler and usual. Do not use a 5th order PLP model when speaker identity matters: the point of the low order is to hide it.

## Pitfalls

- **Forgetting the Bark axis.** The model spectrum is a function of the warped frequency. Its peaks must be mapped back through $\Omega^{-1}$ before they are compared with formants in Hz.
- **Zero bands.** A band with $\phi = 0$, from digital silence, makes the Toeplitz matrix singular. Add a tiny dither or a floor before line L5.
- **The cube root of negative values.** Numerical noise can make a filtered (RASTA) band slightly negative; clamp before the power.
- **Mixing implementations.** The paper's resampling, the HTK mel version and the rastamat code give different numbers; the end band handling and the equal loudness form differ too.
- **The sign of $a$.** With $A(z) = 1 + \sum a_k z^{-k}$, as in some code, the recursion of line L9 changes sign. This page uses $A(z) = 1 - \sum a_k z^{-k}$.

## Implementations

## History

Linear prediction came to speech in the late 1960s and early 1970s with the work of Itakura and Saito and of Atal and Hanauer, and its all-pole fit follows the spectrum with the same accuracy at all frequencies, unlike the ear. Hynek Hermansky published PLP in the Journal of the Acoustical Society of America in 1990. The paper joined three approximations from psychoacoustics with an all-pole model and, from its experiments, recommended a 5th order model for features that should not depend on the speaker. In 1994 Hermansky and Morgan added [RASTA filtering](/rasta-filtering/), and RASTA-PLP became a standard front end of the 1990s, used next to MFCC in many recognizers.

## References
