---
tag: X96A2P
kind: algorithm
slug: code-excited-linear-prediction
name: Code-excited linear prediction
aliases:
- CELP
area: natural-language-and-speech/speech-analysis-and-synthesis
level: core
summary: Speech coding by an LPC synthesis filter driven by an excitation chosen from codebooks to minimize perceptually weighted error.
model: real-ram
complexity:
  vars: {S: the number of subframes, L: the subframe length, Q: the number of pitch lags, C: the size of the fixed codebook, p: the LPC order}
  time: {worst: O(S (Q + C) L^2 + S L p)}
  space: {extra: O(C L + Q)}
properties: {deterministic: true, online: true, in_place: false, exact: false}
history:
  year: 1985
  people: [Manfred R. Schroeder, Bishnu S. Atal]
  note: Schroeder and Atal drove an LPC synthesis filter with vectors from a codebook of Gaussian noise, chosen by synthesizing every candidate and measuring a perceptually weighted error. The idea became the basis of most speech codecs in mobile phones.
prereqs: [linear-predictive-coding, vector-quantization, levinson-durbin-recursion]
see_also: [linear-prediction, scalar-quantization, source-filter-model, pitch-detection, autocorrelation, iir-filter, mean-opinion-score, formant-synthesis]
sources:
  - paper: doi:10.1109/ICASSP.1985.1168147
    title: Manfred R. Schroeder and Bishnu S. Atal, Code-excited linear prediction (CELP), high-quality speech at very low bit rates, Proceedings of the IEEE International Conference on Acoustics, Speech, and Signal Processing (ICASSP), 1985, 937 to 940
    locator: the description of the coder (the random codebook, the long-delay pitch predictor, the perceptual weighting and the exhaustive search) and the reported speech quality
  - book: isbn:9780132136037
    title: Lawrence R. Rabiner and Ronald W. Schafer, Digital Processing of Speech Signals, Prentice-Hall, 1978
    locator: Chapter 8 (linear predictive coding of speech, the autocorrelation method and the synthesis filter)
---

Code-excited linear prediction, CELP, is a method of speech coding in which the decoder passes an excitation through an all-pole synthesis filter $1/A(z)$, and the encoder chooses that excitation from codebooks by trying every entry and keeping the one whose synthesized output is closest to the input under a perceptual weighting. The filter comes from [linear predictive coding](/linear-predictive-coding/), as in the older LPC vocoder, but the LPC vocoder drives it with pulses or noise and sends only a voicing flag and a pitch. CELP sends the index of a code vector, which makes it [vector quantization](/vector-quantization/) of the excitation, with the error measured after the filter instead of on the vector itself.

## In plain words

Speech is a buzz or a hiss shaped by the mouth. A CELP coder sends the shape of the mouth, a few numbers every 20 ms, and a description of the buzz. To describe the buzz, both sides keep the same book of short noise patterns. For each piece of 5 ms, the coder tries every pattern in the book: it plays each one through the mouth filter and compares the result with the real speech. It sends the number of the pattern that sounds closest and a loudness. It also tries copies of the buzz it sent a little earlier, because voiced speech repeats at the pitch. The receiver looks up the same pattern and plays it through the same filter. The comparison ignores errors that the ear does not hear well, near the loud parts of the spectrum.

## The problem

Given speech sampled at $f_s$ (8 kHz for telephone speech), send it at a low bit rate, such as 4.8 to 16 kbit/s, so that the decoded speech sounds as close to the input as possible. The quality is measured by listeners with the [mean opinion score](/mean-opinion-score/) or by objective measures. The encoder may look at the whole input; the decoder has only the bits.

## The algorithm

Speech is cut into frames of $N$ samples (20 ms) and each frame into subframes of $L$ samples (5 ms). For each frame the encoder computes LPC coefficients $a_1, \ldots, a_p$ with $A(z) = 1 - \sum_k a_k z^{-k}$, by the autocorrelation method and the [Levinson-Durbin recursion](/levinson-durbin-recursion/). The perceptual weighting filter is

$$W(z) = \frac{A(z/\gamma_1)}{A(z/\gamma_2)}, \qquad 0 < \gamma_2 < \gamma_1 \le 1,$$

for example $\gamma_1 = 0.9$ and $\gamma_2 = 0.6$. It lowers the weight of the error near the formants, where the loud speech masks it, and raises it between them. The values of $\gamma$ are a heuristic choice.

For each subframe, the excitation is $e = g_a v_T + g_f c_k$, where $v_T$ is the past excitation delayed by $T$ samples (the adaptive codebook, which models the pitch) and $c_k$ is entry $k$ of a fixed codebook. The weighted error is $W(z)(s - \hat s)$ with $\hat s = e / A(z)$. It is affine in $e$:

$$e_w = t - H e,$$

where $t$ is the weighted error when $e = 0$, which the filter states from the past subframes still produce, and $H$ is the lower triangular matrix of the zero-state impulse response $h$ of $W(z)/A(z)$. For one vector $y = H c$ the best gain is $g = \langle t, y \rangle / \langle y, y \rangle$, and the error energy falls from $\|t\|^2$ to

$$\|t\|^2 - \frac{\langle t, y \rangle^2}{\langle y, y \rangle}.$$

So the search picks the vector with the largest $\langle t, y \rangle^2 / \langle y, y \rangle$. The two codebooks are searched one after the other.

```pseudo id=main
CELP-ENCODE(s, fixed codebook c_1 .. c_C, lags T_1 .. T_Q)
L1  for each frame: a <- LPC of the frame; W(z) <- A(z/gamma1) / A(z/gamma2)
L2      h <- the first L samples of the impulse response of W(z) / A(z)
L3      for each subframe: t <- the weighted error with zero excitation, from the current filter states
L4          for each lag T: y_T <- h * v_T; pick T with the largest <t, y_T>^2 / <y_T, y_T>; g_a <- <t, y_T> / <y_T, y_T>
L5          t <- t - g_a y_T
L6          for each k: y_k <- h * c_k; pick k with the largest <t, y_k>^2 / <y_k, y_k>; g_f <- <t, y_k> / <y_k, y_k>
L7          e <- g_a v_T + g_f c_k; run the filters on e; append e to the past excitation
L8          send (a, T, g_a, k, g_f), quantized
```

The decoder builds the same $e$ from the received values and passes it through $1/A(z)$. The encoder contains this decoder, in line L7, so both keep the same filter states and the same past excitation. Real coders quantize $a$ (usually as line spectral pairs) and the gains, and add a postfilter after the decoder; the code on this page does not quantize.

## Example

**One search.** Take a subframe of $L = 4$ with target $t = (1, 0.5, -0.25, 0)$, so $\|t\|^2 = 1.3125$, impulse response $h = (1, 0.5, 0.25, 0.125)$, and a codebook of four vectors:

| $k$ | $c_k$ | $y_k = h * c_k$ | $\langle t, y_k \rangle$ | $\langle y_k, y_k \rangle$ | score | gain |
|---|---|---|---|---|---|---|
| 0 | (1, 0, 0, 0) | (1, 0.5, 0.25, 0.125) | 1.1875 | 1.328125 | 1.0618 | 0.8941 |
| 1 | (0, 1, 0, 0) | (0, 1, 0.5, 0.25) | 0.375 | 1.3125 | 0.1071 | 0.2857 |
| 2 | (1, -1, 0, 0) | (1, -0.5, -0.25, -0.125) | 0.8125 | 1.328125 | 0.4971 | 0.6118 |
| 3 | (0.5, 0.5, 0.5, 0.5) | (0.5, 0.75, 0.875, 0.9375) | 0.65625 | 2.45703 | 0.1753 | 0.2671 |

The encoder sends $k = 0$ with gain 0.8941, and the weighted error energy falls from 1.3125 to $1.3125 - 1.0618 = 0.2507$. After the filter, vector 2 matches the first sample of $t$ as well as vector 0 does, but its second sample has the wrong sign, so it fits worse. The search compares the outputs of the filter, not the code vectors.

**A vowel.** A pulse train at 125 Hz with a little noise, through a resonance at 500 Hz, at 8 kHz, coded with LPC order 10, frames of 160 and subframes of 40 samples, a Gaussian codebook of 128 vectors and lags 20 to 147, gives a signal to noise ratio of 9.9 dB without quantization. Most subframes choose the lag 64, the period, or 128, twice the period. With the adaptive codebook off, the ratio is 4.2 dB. Both numbers are measurements on this one signal.

## Correctness

CELP is a lossy coder, so correctness means that each step does what it claims; the proofs are in proofs/correctness.md. The weighted error is affine in the excitation, $e_w = t - He$, because the filters are linear and their states from the past act as a fixed input. For a fixed vector $y \ne 0$, the error $\|t - g y\|^2$ is a quadratic in $g$ with its least value $\|t\|^2 - \langle t, y \rangle^2 / \langle y, y \rangle$ at $g = \langle t, y \rangle / \langle y, y \rangle$, so picking the largest score picks the least error over all vectors and gains. This is a theorem, and the tests compare it with a brute force search. The search of the two codebooks one after the other is not jointly optimal: a search over all pairs with both gains solved together can only be better. Since the encoder runs the decoder, the decoded output is exactly the $\hat s$ that the encoder measured. If the true excitation is a gain times a code vector and $A$ is known, the search finds it with zero error.

That this error measure predicts what listeners hear is a heuristic, supported by listening tests.

## Complexity

Line L1 costs $O(N p + p^2)$ per frame. In the [real RAM](/real-ram/), lines L4 and L6 filter every candidate, which costs $O(L^2)$ per vector by direct convolution, so a subframe costs $O((Q + C) L^2)$, and the whole input $O(S (Q + C) L^2)$ for $S$ subframes. The filtered fixed codebook can be computed once per frame, as the code does, since $h$ changes only with $A$. The memory is $O(C L)$ for the filtered codebook. With $L = 40$, $C = 1024$ and $Q = 128$, this is about a million multiplications per subframe, which was the main obstacle of CELP in 1985. Later coders cut it with structured codebooks: overlapping, sparse or algebraic vectors whose filtered versions can be updated in $O(L)$ each, or searched without filtering every one.

## Properties

- **Analysis by synthesis.** The encoder judges each choice by its output after the decoder's filter, not by a distance in the parameter space.
- **Perceptual error.** The weighting hides the noise under the formants, so the coded speech sounds better than its plain signal to noise ratio suggests.
- **Low delay.** The delay is one frame plus any look-ahead, often 20 to 30 ms; the variant LD-CELP of ITU-T G.728 works with a delay of a few milliseconds by using backward-adapted LPC.
- **Not for music.** The source-filter model fits one voice. Music and several talkers are coded poorly at the same rate.

## Variants and improvements

- **Algebraic CELP (ACELP).** The fixed codebook has a few pulses of $\pm 1$ at structured positions, so it needs no storage and can be searched fast. ITU-T G.729 and the AMR codecs of mobile phones use it.
- **VSELP and other structured codebooks.** Vectors built as sums of a few basis vectors, so the search over $2^M$ vectors costs about $M$ filterings.
- **LD-CELP.** Backward adaptation of LPC from the decoded speech, for low delay (ITU-T G.728, 16 kbit/s).
- **Postfilter.** A filter like $W(z)$ at the decoder deepens the valleys between formants and makes the noise less audible.
- **Joint search.** Searching the two codebooks together, or keeping several candidates from the first search, lowers the error at a higher cost.

## When to use it

Use CELP for speech at 4 to 16 kbit/s where a delay of tens of milliseconds is acceptable, such as mobile telephony and voice over IP. For high quality wideband speech and music at higher rates, transform coders and hybrid codecs such as Opus are a better fit. At very low rates, under about 2 kbit/s, parametric and neural codecs do better.

## Pitfalls

- **Encoder and decoder out of step.** The encoder must update its filter states and its past excitation from the decoded values, not from the input. Otherwise the adaptive codebook of the two sides differs and the error grows.
- **Lags shorter than the subframe.** If $T < L$, the delayed excitation is not yet known for the whole subframe; repeat the first $T$ samples, as the code does.
- **Unstable filters.** Rounding or quantizing $a$ can move a pole outside the unit circle. Interpolate and quantize line spectral pairs, whose order guarantees a stable filter, instead of the $a_k$.
- **Gains that are not quantized jointly.** Gains are large in voiced onsets; quantizing them on a fixed scale clips them. Real coders quantize the two gains together with a vector quantizer.
- **The search cost.** Filtering every vector of a large random codebook in each subframe is slow; use a structured codebook.

## Implementations

## History

Bishnu Atal and Joel Remde introduced multipulse excitation in 1982, which first chose the excitation by analysis by synthesis. Manfred Schroeder and Bishnu Atal at Bell Laboratories published CELP at ICASSP 1985, with a codebook of Gaussian noise vectors, a pitch predictor and a perceptual weighting filter, and reported high quality speech at low bit rates, with an exhaustive search that was then far too slow for real time. Structured codebooks made it practical. The US federal standard FS-1016 (4.8 kbit/s, 1991), ITU-T G.728 (16 kbit/s, 1992) and G.729 (8 kbit/s, 1996), and the AMR codecs of GSM and UMTS are all CELP coders.

## References
