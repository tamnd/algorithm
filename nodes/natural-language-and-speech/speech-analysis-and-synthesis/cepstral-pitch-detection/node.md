---
tag: AZJ97D
kind: algorithm
slug: cepstral-pitch-detection
name: Cepstral pitch detection
aliases:
- Noll cepstral pitch detector
area: natural-language-and-speech/speech-analysis-and-synthesis
level: core
summary: Estimate the pitch period of a voiced frame from the quefrency of the largest peak of the real cepstrum in the plausible range.
solves: [pitch-detection]
model: real-ram
complexity:
  vars: {M: "the FFT length, a power of two at least the frame length"}
  time: {worst: O(M log M)}
  space: {extra: O(M)}
properties: {deterministic: true, online: true, in_place: false, exact: false}
history:
  year: 1967
  people: [A. Michael Noll]
  note: Noll at Bell Telephone Laboratories used the cepstrum to find the pitch period of speech, with decision rules for voicing and for octave errors that he set by experiment, and used the result to drive a channel vocoder.
prereqs: [cepstrum, pitch-detection, fast-fourier-transform]
see_also: [yin-algorithm, pyin, rapt-pitch-tracker, source-filter-model, formant-estimation, mel-frequency-cepstral-coefficients, window-functions, minimum-phase]
sources:
  - paper: doi:10.1121/1.1910339
    title: A. Michael Noll, Cepstrum pitch determination, Journal of the Acoustical Society of America 41(2), 1967, 293 to 309
    locator: "the definition of the cepstrum as the power spectrum of the logarithm of the power spectrum, and the description of the pitch detector and its decision rules (section numbers not confirmed)"
  - paper: "A. Michael Noll, Short-time spectrum and cepstrum techniques for vocal-pitch detection, Journal of the Acoustical Society of America 36(2), 1964, 296 to 302"
    title: Short-time spectrum and cepstrum techniques for vocal-pitch detection
    locator: the whole paper, the first report of the method
  - book: isbn:9780132136037
    title: L. R. Rabiner and R. W. Schafer, Digital Processing of Speech Signals, Prentice Hall, 1978
    locator: Chapter 7 (homomorphic speech processing), the part on pitch detection with the cepstrum
---

Cepstral pitch detection finds the fundamental frequency of a voiced frame of speech from the largest peak of its real [cepstrum](/cepstrum/) inside the range of plausible pitch periods. It is one method for the problem of [pitch detection](/pitch-detection/): the cepstrum page defines the transform, and this page is the detector that A. Michael Noll built on it in 1964 and 1967. Inside this area it is the oldest of three trackers: [pYIN](/pyin/) works on the time-domain difference function of [YIN](/yin-algorithm/) and adds a hidden Markov model, and [RAPT](/rapt-pitch-tracker/) uses the normalized cross-correlation and a dynamic program over frames, while the cepstral detector decides each frame alone from the log spectrum. One frame costs two FFTs, $O(M \log M)$ operations for an FFT length $M$.

## In plain words

A voiced sound is a buzz from the vocal folds that passes through the mouth and throat. The buzz gives the spectrum many evenly spaced peaks, one per harmonic, and the mouth shapes the broad outline of those peaks. If you take the logarithm of the spectrum, the outline and the comb of harmonics no longer multiply but add. A second Fourier transform then puts the slow outline near zero and the fast comb at one place: the length of one buzz period. So the detector looks for the tallest peak among the lengths that a voice can have, and calls the frame unvoiced when that peak is too small.

## The problem

Given one frame $x[0 \ldots N-1]$ of a speech signal at a sample rate $f_s$ Hz, and a search range $f_{\min} \le F_0 \le f_{\max}$ (for example 50 to 500 Hz), decide whether the frame is voiced, and if it is, estimate its fundamental frequency $F_0$ in Hz. The frame should hold at least two periods of $f_{\min}$, so 40 ms or more for $f_{\min} = 50$ Hz. A tracker runs the detector on frames every 10 ms or so. The problem and its error measures (gross errors, octave errors, voicing errors) are on the [pitch detection](/pitch-detection/) page.

## The algorithm

For an FFT length $M \ge N$, a power of two, the real cepstrum of the windowed and zero padded frame $y$ is

$$c[q] = \frac{1}{M} \sum_{k=0}^{M-1} \ln |Y[k]|\, e^{2\pi i k q / M}, \qquad Y[k] = \sum_{n=0}^{M-1} y[n]\, e^{-2\pi i k n / M}.$$

The index $q$ is the quefrency in samples. A pitch period of $P$ samples belongs to the frequency $f_s / P$.

```pseudo id=main
CEPSTRAL-PITCH(x, fs, fmin, fmax, M, θ)       ▷ x is a frame of N ≤ M samples
L1  y[n] ← w[n] x[n] for n < N, and y[n] ← 0 for N ≤ n < M    ▷ w is the Hamming window
L2  Y ← the DFT of y, by the FFT
L3  L[k] ← ln |Y[k]| for 0 ≤ k < M, with a small floor so that ln 0 never occurs
L4  c ← the inverse DFT of L, by the FFT                        ▷ the real cepstrum
L5  q_min ← ⌈fs / fmax⌉; q_max ← ⌊fs / fmin⌋
L6  q* ← the q in [q_min, q_max] with the largest c[q], the smallest such q on ties
L7  if c[q*] ≤ θ then return unvoiced
L8  return fs / q*
```

Lines L1 to L4 compute the real cepstrum. Since $y$ is real, $|Y[k]| = |Y[M-k]|$, so $L$ is real and even, and its inverse DFT is real and equals its forward DFT divided by $M$; the code uses the same FFT twice. Line L5 turns the frequency range into a range of periods, which must stay below $M / 2$. Line L6 is the peak search. Line L7 is the voicing decision with a threshold $\theta$; its value is a heuristic, set on labeled speech, and this page does not take one from Noll. The floor in line L3 is $10^{-12}$ times the largest magnitude.

Noll squared the log of the power spectrum and transformed again, so his cepstrum is $(2 c[q])^2$ in the notation here, up to a constant. Its largest peak is at the same quefrency whenever that peak of $c$ is positive, so the two forms pick the same period.

## Example

Take $f_s = 8000$ Hz and one resonance at 500 Hz with pole radius $r = 0.9$, so the bandwidth is $-(f_s / \pi) \ln r = 268.3$ Hz. In the sign convention $A(z) = 1 - a_1 z^{-1} - a_2 z^{-2}$ the coefficients are $a_1 = 2r \cos(2\pi \cdot 500 / 8000) = 1.662983$ and $a_2 = -r^2 = -0.81$. A pulse train at $F_0 = 160$ Hz, one pulse every 50 samples, passes through $1 / A(z)$. The frame is the 400 samples (50 ms) from sample 100 on, with a Hamming window and $M = 512$. The search range 60 to 400 Hz gives $q_{\min} = 20$ and $q_{\max} = 133$.

| $q$ | 1 | 2 | 3 | 20 | 49 | 50 | 51 | 62 | 100 | 133 |
|---|---|---|---|---|---|---|---|---|---|---|
| $c[q]$ | 0.8079 | 0.3034 | 0.0862 | 0.0028 | 0.0249 | 1.2539 | 0.0018 | 0.1366 | 0.4304 | -0.0016 |

The low quefrencies hold the resonance. Inside the range, the largest values are $c[50] = 1.2539$ and then the second rahmonic $c[100] = 0.4304$, so line L6 gives $q^* = 50$ and line L8 returns $8000 / 50 = 160$ Hz, the true pitch. The same frame at 100, 125 and 200 Hz gives exactly those values. At 150 Hz the period is 53.33 samples, and the detector returns $q^* = 53$, which is 150.94 Hz: the answer is a whole number of samples.

The theory is exact for a model signal. Take six pulses at the samples $0, 50, \ldots, 250$ with the amplitudes $0.8^j$, filter them by the same $1 / A(z)$, and take the cepstrum with no window and $M = 4096$. The filter alone has the cepstrum $\hat h[n] = (p^n + \bar p^n) / n$ for its poles $p$ and $\bar p$, which gives $\hat h[1] = 1.6630$, $\hat h[2] = 0.5728$ and $\hat h[3] = 0.1860$. The computed values are $c[3] = 0.09299 = \hat h[3] / 2$, $c[50] = 0.40007 = (\hat h[50] + 0.8) / 2$ and $c[100] = 0.16000 = (\hat h[100] + 0.8^2 / 2) / 2$, as the lemmas of the proof predict.

## Correctness

The detector is an estimator, so no theorem says that it finds the true pitch of real speech. What can be proved is what the cepstrum of a model voiced signal is, and when its largest peak in the range is the pitch period. The full proof is in proofs/correctness.md; this is the outline.

Lines L2 to L4 compute the real cepstrum, because $\ln |Y|$ is real and even, so its inverse DFT is real and is the forward DFT divided by $M$.

For the model, let $h$ be the impulse response of an all-pole filter $1 / A(z)$ with all poles $p_i$ inside the unit circle, and let $e[n] = \sum_{j=0}^{K-1} \beta^j \delta[n - jP]$ be $K$ pulses of period $P$ with $0 < \beta < 1$. The signal is $x = h * e$, with no window. The log of the transform of a convolution is the sum of the logs, so the complex cepstrum is $\hat x = \hat h + \hat e$. Expanding the logarithms in power series gives $\hat h[n] = \sum_i p_i^n / n$ for $n \ge 1$, and $\hat e$ is 0 except at the multiples of $P$, where $\hat e[jP] = \beta^j / j$, minus $\beta^j K / j$ when $K$ divides $j$. Both are causal, because both factors are [minimum phase](/minimum-phase/), so the real cepstrum is $c[n] = \hat x[n] / 2$ for $n \ge 1$.

**Theorem.** Let $K \ge 2$ and $\rho = \max |\hat h[n]|$ over the range $q_{\min} \le n \le q_{\max}$, which holds $P$. If $\beta - \beta^2 / 2 > 2\rho$, the cepstrum of the model signal, without aliasing, has its unique largest value in the range at $n = P$.

The reason is that $c[P] \ge (\beta - \rho) / 2$, while every other $n$ in the range has $c[n] \le (\rho + \beta^2 / 2) / 2$, since $\hat e[jP] \le \beta^j / j \le \beta^2 / 2$ for $j \ge 2$. The bound $\rho \le \sum_i |p_i|^{q_{\min}} / q_{\min}$ shows that the filter part dies out fast: the vocal tract lives at low quefrency. With a finite $M$ the DFT cepstrum is the aliased sum $\sum_l c[q + lM]$, and the theorem holds when the margin is larger than twice the aliased tail. The Hamming window of line L1 breaks the exact model, because it multiplies $x$ and not only the pulses; that the peak survives windowing is a measurement, as in the example, not a theorem.

## Complexity

Lines L1 and L3 cost $O(M)$, lines L2 and L4 are two FFTs of length $M$, and lines L5 to L8 cost $O(q_{\max} - q_{\min}) \subseteq O(M)$. A frame costs $O(M \log M)$ operations in the [real RAM](/real-ram/), and the extra memory is $O(M)$ for $Y$, $L$ and $c$. A track of $T$ frames costs $O(T M \log M)$. At $f_s = 16$ kHz with $f_{\min} = 50$ Hz, the frame is at least 640 samples and $M = 1024$.

## Properties

- **One frame at a time.** The estimate depends only on the frame, so the detector runs on a stream with a delay of one frame. There is no smoothing across frames.
- **Scale invariant in the peak.** Multiplying $x$ by $g > 0$ adds $\ln g$ to every $L[k]$, which changes only $c[0]$. The peak and the voicing value do not change with the loudness.
- **Separates source and filter.** The vocal tract response adds to the low quefrencies and the excitation adds peaks at multiples of the period. The same split, kept to the low quefrencies, gives cepstral features such as [MFCCs](/mel-frequency-cepstral-coefficients/).
- **Integer periods.** The estimate is $f_s / q^*$ for a whole number $q^*$. At 8 kHz and 150 Hz one sample of period is about 2.8 Hz.
- **Not exact in general.** The model theorem needs a minimum-phase excitation and a resonance that decays fast. Real speech meets it only roughly.

## Variants and improvements

- **Interpolated peak.** A parabola through $c[q^* - 1]$, $c[q^*]$ and $c[q^* + 1]$ gives a fractional period, as YIN does for its difference function. A longer FFT does not help, because it only interpolates the spectrum.
- **Liftering.** Setting $c[q] = 0$ outside the pitch range and transforming back gives the smoothed spectral envelope, which serves [formant estimation](/formant-estimation/).
- **Tracking.** A median filter or a dynamic program over the candidate peaks of nearby frames removes isolated octave errors, which is the idea of RAPT and of the hidden Markov model in pYIN.
- **Noll's rules.** Noll compared the peak with thresholds that he set by experiment, and added rules against octave errors. The exact rules and their values are in the 1967 paper; they are heuristics.
- **Clipping and power forms.** Noll's squared form, $(2c)^2$, and the plain $c$ give the same period when the peak is positive.

## When to use it

Use the cepstral detector when you want a simple frame-by-frame pitch estimate for clean voiced speech with a known pitch range, or when you already compute a cepstrum for other features. It needs no training and only FFTs. For noisy speech, for music, or when a smooth track matters, prefer [pYIN](/pyin/) or [RAPT](/rapt-pitch-tracker/), which keep several candidates per frame and choose a track over time.

## Pitfalls

- **Searching the low quefrencies.** The resonances give large values near $q = 1$, here $c[1] = 0.8079$. Without the lower limit of line L5 the detector can return a pitch of thousands of Hz.
- **A frame that is too short.** If the frame holds fewer than two periods, the harmonics are not resolved in the spectrum and there is no pitch peak. Use at least two periods of $f_{\min}$.
- **A range up to M / 2.** The cepstrum of a real frame is even, so $c[q] = c[M - q]$, and quefrencies above $M / 2$ are copies. Keep $q_{\max} < M / 2$.
- **Taking the log of zero.** Zero padding and silence give spectral values of 0. Put a floor under $|Y[k]|$ before the log.
- **High voices.** A high pitch puts few harmonics in the spectrum and makes the peak near the resonance part, so the peak is weak and the detector says unvoiced.
- **Integer period bias.** For a period of 53.33 samples the estimate is 53 samples. Interpolate when you need better than one sample.

## Implementations

## History

Bogert, Healy and Tukey named the cepstrum in 1963 in work on echoes in seismic signals. A. Michael Noll, at Bell Telephone Laboratories, applied it to the pitch of speech in a short paper in 1964 and in a full paper in the Journal of the Acoustical Society of America in 1967. His detector took the power spectrum of the log power spectrum of short frames, picked the largest peak with rules found by experiment, and drove a channel vocoder. Oppenheim and Schafer gave the theory of homomorphic deconvolution at the same time, and Rabiner and Schafer made the cepstral detector a standard method in their 1978 book.

## References
