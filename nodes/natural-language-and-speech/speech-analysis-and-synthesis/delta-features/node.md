---
tag: AZKQ3W
kind: technique
slug: delta-features
name: Delta features
aliases:
- delta and delta-delta coefficients
- dynamic features
- acceleration coefficients
area: natural-language-and-speech/speech-analysis-and-synthesis
level: core
summary: Append to each frame the slopes of its features over a few neighbouring frames, and the slopes of those, found by linear regression.
prereqs: [linear-regression, mel-frequency-cepstral-coefficients]
see_also: [cepstral-mean-normalization, rasta-filtering, mel-filter-bank, perceptual-linear-prediction, savitzky-golay-filter, fir-filter, gmm-hmm-acoustic-model, automatic-speech-recognition]
sources:
  - paper: "S. Furui, Speaker-independent isolated word recognition using dynamic features of speech spectrum, IEEE Transactions on Acoustics, Speech, and Signal Processing 34(1), 1986, 52 to 59"
    title: S. Furui, Speaker-independent isolated word recognition using dynamic features of speech spectrum
    locator: the regression coefficients of the cepstrum over neighbouring frames, used together with the cepstrum itself
  - paper: "Steve Young et al., The HTK Book (for HTK version 3.4), Cambridge University Engineering Department, 2006"
    title: The HTK Book, version 3.4
    locator: "Chapter Speech Input/Output, section Delta, Acceleration and Third Differential Coefficients (the regression formula with the window size Θ)"
  - url: https://github.com/kaldi-asr/kaldi/blob/master/src/feat/feature-functions.cc
    title: Kaldi speech recognition toolkit, src/feat/feature-functions.cc
    locator: "the class DeltaFeatures: the regression window normalized by the sum of j squared, and frames outside the utterance clamped to the first and last frames"
---

Delta features add to each frame of a speech feature sequence, such as [MFCC](/mel-frequency-cepstral-coefficients/), the local slope of each coefficient over time, and delta-delta features add the slope of that slope. The slope is the least squares slope of a line fitted to a few frames on each side, so it is a short [FIR filter](/fir-filter/) along time, applied to each coefficient. [RASTA filtering](/rasta-filtering/) also filters along time, but it replaces the trajectories, while deltas are appended to the static features; [cepstral mean normalization](/cepstral-mean-normalization/) changes only the mean, which the deltas ignore. With 13 static coefficients the result is the standard 39 numbers per frame.

## In plain words

One frame of MFCC describes the sound in a 25 ms slice, but speech is about change: a vowel glides into a consonant, and the change tells as much as the slice. The delta of a coefficient says how fast it is rising or falling at this frame. It is found by looking two frames back and two frames ahead and fitting a straight line through the five values; the slope of that line is the delta. The delta-delta does the same to the deltas, so it says whether the change is speeding up or slowing down. At the start and the end of the recording there are no frames to look at, so the first and last frames are repeated.

## When it applies

- The features form a sequence of vectors at a fixed frame rate, usually 100 frames per second, and the model treats frames as if they were independent given their state, as a [GMM-HMM](/gmm-hmm-acoustic-model/) does. Deltas put information about the neighbours into each frame.
- The features change smoothly over a few frames, so that a local line is a good summary of the trajectory.
- The slope should be robust to frame-to-frame noise. A plain difference of two frames is noisier than a regression over five.
- Neural acoustic models that see many frames at once, by stacking frames or by convolution and recurrence, gain little from deltas, and they are often left out there.

## The template

For a sequence $c_0, \ldots, c_{T-1}$ of feature vectors and a half width $\Theta \ge 1$, the delta of frame $t$ is

$$d_t = \frac{\sum_{n=1}^{\Theta} n\,(c_{t+n} - c_{t-n})}{2 \sum_{n=1}^{\Theta} n^2},$$

computed for each coefficient on its own, with $c_t = c_0$ for $t < 0$ and $c_t = c_{T-1}$ for $t \ge T$. The usual value is $\Theta = 2$, for which the denominator is 10. The delta-deltas are the deltas of the deltas.

```pseudo id=main
DELTAS(c, Θ)          ▷ c[t][j] for t = 0 .. T-1 and j = 1 .. D, with Θ ≥ 1
L1  den ← 2 (1² + 2² + … + Θ²); s[t][j] ← 0 for all t and j
L2  for t ← 0 to T - 1, j ← 1 to D, n ← 1 to Θ do a ← c[min(t + n, T - 1)][j]; b ← c[max(t - n, 0)][j]
L3      s[t][j] ← s[t][j] + n (a - b)
L4  return d with d[t][j] ← s[t][j] / den
ADD-DELTAS(c, Θ)
L5  d ← DELTAS(c, Θ)
L6  dd ← DELTAS(d, Θ); return the frames (c[t], d[t], dd[t]) for t ← 0 to T - 1
```

**Why it is a slope (theorem).** For the $2\Theta + 1$ points $(n, c_{t+n})$ with $n = -\Theta, \ldots, \Theta$, the least squares line $c \approx \alpha + \beta n$ has $\beta = \sum_n n\, c_{t+n} / \sum_n n^2$, because the $n$ are centered, $\sum_n n = 0$. Pairing $n$ with $-n$ gives exactly $d_t$. So a straight line $c_t = \alpha + \beta t$ gives $d_t = \beta$ wherever no edge frame is repeated, and a constant gives 0 everywhere.

**Why offsets do not matter (theorem).** Adding the same vector $v$ to every frame adds $n(v - v) = 0$ to each term, so the deltas, and so the delta-deltas, do not change. A fixed channel that [cepstral mean normalization](/cepstral-mean-normalization/) removes from the static features is thus already absent from the dynamic ones.

**As a filter (theorem).** For $\Theta = 2$, the delta is the FIR filter $0.1(2z^2 + z - z^{-1} - 2z^{-2})$ along time. On a sine with $\omega$ radians per frame its gain is $|\sin\omega + 2 \sin 2\omega| / 5$, which is about $\omega$ for small $\omega$, like a derivative, peaks at 0.547 near 13.8 Hz at 100 frames per second, and is 0 at 0 Hz, at 50 Hz and where $\cos\omega = -\frac14$, near 29.0 Hz. The numerator of the RASTA filter is the same 5 taps.

## Classic examples

**A quadratic.** For one coefficient with the values $c = 1, 3, 6, 10, 15$, lines L1 to L4 with $\Theta = 2$ give $d = 1.2, 2.3, 3.5, 3.3, 2.3$. At $t = 2$, the only frame with two real neighbours on each side, $d_2 = ((10 - 3) + 2(15 - 1))/10 = 3.5$, which is the slope of the quadratic $c_t = (t+1)(t+2)/2$ at $t = 2$. The other values are pulled down by the repeated edge frames. The delta-deltas are $0.57, 0.65, 0.32, -0.12, -0.34$; for a long quadratic sequence they would be the constant second difference 1 away from the edges, but 5 frames are too few for any frame to be clear of the edges in both passes.

**A ramp.** For $c_t = 2t + 5$ over 20 frames, $d_t = 2$ for $2 \le t \le 17$ and $dd_t = 0$ for $4 \le t \le 15$.

**The 39-dimensional vector.** Thirteen MFCC $c_0, \ldots, c_{12}$ per frame, their 13 deltas and their 13 delta-deltas give 39 numbers per frame, the standard input of GMM-HMM recognizers. Many recipes use the log energy of the frame in place of $c_0$.

**A tone at the syllable rate.** A coefficient that oscillates at 4 Hz with amplitude 1, at 100 frames per second, has $\omega = 0.2513$ and a delta of amplitude 0.2425 per frame, close to the amplitude $\omega$ of the derivative. The taps are odd around frame $t$, so the phase of the delta is exactly that of the derivative, with no added delay.

## Variations

- **Window size.** $\Theta = 1$ gives the central difference $(c_{t+1} - c_{t-1}) / 2$; $\Theta = 3$ smooths more. HTK and Kaldi both take $\Theta$ as an option, and 2 is the common choice.
- **Delta-deltas in one pass.** Kaldi computes the second order coefficients by applying the combined 9-tap filter to the static features, with the clamp on the static frames. In the interior this equals the deltas of the deltas; within 4 frames of an edge the two differ.
- **Savitzky-Golay deltas.** librosa estimates the derivative with a [Savitzky-Golay filter](/savitzky-golay-filter/) of width 9 by default, a local polynomial fit that contains the linear regression above as its first order case.
- **Third differentials.** HTK can add the deltas of the delta-deltas, for 52 numbers per frame.
- **Frame stacking and projection.** In place of deltas, stack the static features of 7 to 11 frames and reduce the dimension with linear discriminant analysis. This learns the temporal filters from data.

## Pitfalls

- **Units.** The deltas are per frame. A model trained at 100 frames per second sees different numbers at another frame rate, or when the frames are counted in seconds.
- **Edge frames.** Repeating the first and last frames, as here and in Kaldi, makes the deltas of the first and last $\Theta$ frames smaller. Padding with zeros instead creates large false slopes at the edges, because the features are not near 0.
- **Different delta-delta conventions.** Deltas of deltas and the combined filter agree only away from the edges, so two toolkits can disagree on the first and last frames.
- **Normalizing after deltas.** Mean normalization does not change the deltas, but variance normalization does. Apply it to the full 39-dimensional vector if the model expects unit variances.
- **Streaming.** The delta needs $\Theta$ frames of the future, and the delta-delta $2\Theta$. A streaming recognizer must wait 4 frames, 40 ms, before it can emit a frame.

## Exercises

1. Show that for $\Theta = 2$ the delta of $c_t = t^2$ away from the edges is $2t$, and that the delta-delta is 2.
2. Prove that the delta of any sequence is the least squares slope of a line fitted to the $2\Theta + 1$ frames around $t$, after the edge frames are repeated.
3. Write the delta and the delta-delta as one FIR filter of 9 taps for $\Theta = 2$, and find its coefficients.
4. Find the gain of the $\Theta = 1$ filter on a sine of $\omega$ radians per frame, and compare it with the $\Theta = 2$ filter at 5 Hz and at 25 Hz at 100 frames per second.
5. Show that adding a fixed vector to every frame leaves both the deltas and the delta-deltas unchanged, and explain why this means mean normalization can come before or after the delta computation.

## References
