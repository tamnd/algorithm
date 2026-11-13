---
tag: QXNECT
kind: algorithm
slug: yin-algorithm
name: YIN algorithm
aliases:
- YIN pitch estimator
area: graphics-and-signals/signal-processing
level: advanced
summary: "A period estimator for pitch detection: a difference function, its cumulative mean normalization, an absolute threshold that avoids octave errors, and parabolic interpolation."
solves: [pitch-detection]
model: real-ram
complexity:
  vars: {W: the frame length, T: the largest lag searched}
  time: {worst: O(W T)}
  space: {extra: O(T)}
properties: {deterministic: true, online: true, in_place: false, exact: false}
history:
  year: 2002
  people: [Alain de Cheveigné, Hideki Kawahara]
  note: De Cheveigné and Kawahara built YIN from the autocorrelation method in a series of steps, each of which removes a class of errors, and evaluated it on speech with laryngograph references.
prereqs: [pitch-detection, autocorrelation]
see_also: [cepstrum, cross-correlation, fast-fourier-transform, prefix-sums, short-time-fourier-transform, hidden-markov-model, linear-predictive-coding]
sources:
  - paper: doi:10.1121/1.1458024
    title: Alain de Cheveigné and Hideki Kawahara, YIN, a fundamental frequency estimator for speech and music, Journal of the Acoustical Society of America 111(4), 2002, 1917 to 1930
    locator: Section II, steps 1 to 6 (the autocorrelation, the difference function, the cumulative mean normalized difference, the absolute threshold, the parabolic interpolation and the best local estimate), and the evaluation that follows (equation numbers not confirmed)
---

The YIN algorithm of de Cheveigné and Kawahara (2002) estimates the period of a nearly periodic signal in a frame, and so its fundamental frequency, for [pitch detection](/pitch-detection/). It computes the difference function $d(\tau)$, the energy of the frame minus a copy of itself delayed by $\tau$ samples, and divides it by its own running mean to get the cumulative mean normalized difference $d'(\tau)$. It then takes the first lag at which $d'$ dips below an absolute threshold, instead of the deepest dip, which removes most octave errors, and refines that lag by parabolic interpolation. The direct cost is $O(W T)$ operations per frame for a frame of $W$ samples and lags up to $T$, or $O((W + T) \log (W + T))$ with the FFT.

## In plain words

To find how often a sound repeats, slide a copy of a short piece of it along the original and measure how different the two are at each shift. Where the copy lines up with the next repeat, the difference is small. That shift is the period.

The trouble is that the copy also lines up two repeats later, and three, and there the difference can be even smaller. So YIN rescales the difference so that it is about 1 when nothing lines up, and then stops at the first shift where the rescaled value drops below a small limit, such as 0.1. That shift is the shortest repeat, not a long one. Last, YIN fits a curve through the three nearest shifts to find the period between two samples.

## The problem

Given a signal $x$ of numbers, a frame start $t$, a frame length $W$ and a largest lag $T$, estimate the period $P$ of $x$ near $t$ in samples, possibly a fraction. The samples $x[t \ldots t + W + T - 1]$ must exist. At a sample rate $f_s$ Hz the estimate of the fundamental frequency is $f_s / P$ Hz. A pitch tracker calls the algorithm once for each frame, every few milliseconds. The frame should hold at least two periods of the lowest pitch, and $T$ should be at least that period. The problem and its error measures are on the [pitch detection](/pitch-detection/) page.

## The algorithm

The difference function is

$$d(\tau) = \sum_{j=t}^{t+W-1} \bigl(x[j] - x[j + \tau]\bigr)^2, \qquad 0 \le \tau \le T,$$

and the cumulative mean normalized difference function is $d'(0) = 1$ and

$$d'(\tau) = \frac{d(\tau)}{\frac{1}{\tau} \sum_{j=1}^{\tau} d(j)}, \qquad 1 \le \tau \le T.$$

```pseudo id=main
YIN(x, t, W, T, θ)                          ▷ θ is the absolute threshold, often 0.1
L1  for τ ← 0 to T do d[τ] ← Σ_{j=t}^{t+W−1} (x[j] − x[j + τ])²
L2  d′[0] ← 1
L3  S ← 0; for τ ← 1 to T do
L4      S ← S + d[τ]
L5      d′[τ] ← τ · d[τ] / S, or 1 if S = 0
L6  τ* ← the smallest τ ≥ 1 with d′[τ] < θ
L7  if τ* exists then while τ* < T and d′[τ* + 1] < d′[τ*] do τ* ← τ* + 1
L8  else τ* ← the τ ≥ 1 with the smallest d′[τ], the smallest such τ on ties
L9  if 1 ≤ τ* < T and a ← d[τ* − 1] − 2 d[τ*] + d[τ* + 1] is not 0 then
L10     return τ* + (d[τ* − 1] − d[τ* + 1]) / (2a)
L11 return τ*
```

Line L1 is step 2 of the paper. With the windowed energies $e(s) = \sum_{j=s}^{s+W-1} x[j]^2$, it is the same as

$$d(\tau) = e(t) + e(t + \tau) - 2 r_t(\tau), \qquad r_t(\tau) = \sum_{j=t}^{t+W-1} x[j]\, x[j + \tau],$$

where $r_t$ is the [cross-correlation](/cross-correlation/) of the frame with the delayed signal, the step 1 [autocorrelation](/autocorrelation/) of the paper. The energies come from [prefix sums](/prefix-sums/) of $x^2$, and all values of $r_t$ come from one [FFT](/fast-fourier-transform/) product. Lines L2 to L5 are step 3: the division removes the zero at $\tau = 0$, which would always be the minimum of $d$, and makes $d'$ start near 1. Lines L6 to L8 are step 4. Line L7 moves from the first lag below the threshold to the bottom of its dip. Lines L9 to L11 are step 5, a parabola through the three values of $d$ (not $d'$) around $\tau^*$; the paper uses $d$ there because the normalization shifts the minimum. Step 6 of the paper, the best local estimate, is a variant below.

## Example

Take a sum of two harmonics with period $10.5$ samples, rounded to integers,

$$x[n] = \operatorname{round}\Bigl(1000 \cos\frac{2\pi n}{10.5} + 600 \cos\Bigl(\frac{4\pi n}{10.5} + 1\Bigr)\Bigr),$$

which repeats exactly every 21 samples. At $f_s = 8000$ Hz its fundamental is $8000 / 10.5 = 761.9$ Hz. With $t = 0$, $W = 63$ and $T = 40$, line L1 gives these values:

| $\tau$ | $d(\tau)$ | $d'(\tau)$, rounded |
|---|---|---|
| 1 | 25348170 | 1.0000 |
| 8 | 103422414 | 0.9831 |
| 9 | 51460818 | 0.5186 |
| 10 | 6741768 | 0.0749 |
| 11 | 6741768 | 0.0818 |
| 12 | 51460818 | 0.6446 |
| 20 | 25348170 | 0.2817 |
| 21 | 0 | 0 |
| 22 | 25348170 | 0.3056 |

No lag has an exact repeat below 21, because the period is not an integer. With $\theta = 0.1$, line L6 finds $\tau^* = 10$, and line L7 stops there because $d'(11) > d'(10)$. Line L10 gives

$$10 + \frac{51460818 - 6741768}{2\,(51460818 - 2 \cdot 6741768 + 6741768)} = 10 + \frac{1}{2} = \frac{21}{2},$$

the exact period. If lines L6 and L7 are skipped and line L8 is always used, the global minimum is $d'(21) = 0$, and the estimate is 21 samples, 381.0 Hz: an octave error. For frames of $W = 50$ and $W = 70$, which are not multiples of 21, the estimates are 10.4963 and 10.49995.

## Correctness

YIN is an estimator, and there is no theorem that it finds the true period of every signal. What can be proved is that each step computes what it claims, and that the estimate is exact on two families of periodic signals.

The identity of line L1 is the expansion $(a - b)^2 = a^2 + b^2 - 2ab$ summed over $j$, so the direct sum and the energy and correlation form give the same numbers. Each $d(\tau) \ge 0$, so in line L5 $S \ge d(\tau)$ and $0 \le d'(\tau) \le \tau$; also $d'(1) = 1$ whenever $d(1) > 0$.

Suppose $x$ repeats with an integer period $Q$ and $W$ is a multiple of $Q$. Then $d(\tau + Q) = d(\tau)$ and $d(Q - \tau) = d(\tau)$ for $0 \le \tau \le Q$, because the sum of a $Q$-periodic function over $W$ consecutive indices does not depend on where it starts. Two facts follow. If $Q = P$ is the fundamental period, $2 \le P < T$, then $d(P) = 0$ and $d(P - 1) = d(P + 1)$, so whenever lines L6 to L8 give $\tau^* = P$, line L10 returns exactly $P$. And if a lag $1 \le \tau < T$ has $d(\tau) = d(\tau + 1)$, as $\tau = (Q - 1)/2$ does for odd $Q$, and $\tau^*$ is that lag, line L10 returns exactly $\tau + \frac{1}{2}$ whenever $d(\tau - 1) \ne d(\tau)$. The example is the second case with $Q = 21$. The proofs are below. For a signal with an integer fundamental period, line L8 also returns $P$, because all multiples of $P$ tie at $d' = 0$ and ties go to the smallest lag; the octave error of the global minimum shows up when the period is not an integer or when there is noise.

## Complexity

Line L1 costs $W$ multiplications for each of the $T + 1$ lags, so a frame costs $O(W T)$ operations in the worst case in the [real RAM](/real-ram/). With prefix sums for the energies and one FFT of length at least $W + T$ for the correlations, it costs $O((W + T) \log(W + T))$. Lines L2 to L11 cost $O(T)$. The extra memory is the $T + 1$ values of $d$ and $d'$, $O(T)$, plus $O(W + T)$ for the FFT. A tracker with frames every $R$ samples costs $O(W T / R)$ per input sample directly. On integer input every quantity can be kept exact: $d$ is an integer and $d'$ and the estimate are rationals, as in the tests.

## Properties

- **Deterministic and local.** The estimate depends only on the samples $x[t \ldots t + W + T - 1]$, so a tracker can run on a stream with a delay of $W + T$ samples.
- **Scale invariant.** Multiplying $x$ by $c \ne 0$ multiplies $d$ by $c^2$ and leaves $d'$ and the estimate unchanged, so the threshold does not depend on the loudness.
- **Prefers the shortest period.** The threshold rule returns the first good dip, so a lag $2P$ with a slightly deeper dip than $P$ does not win.
- **Not exact in general.** The estimate is exact for the families above. In other cases, the parabola, the window length and noise give small errors, and gross errors remain when the threshold is wrong for the signal.
- **Aperiodicity measure.** The value $d'(\tau^*)$ is near 0 for clean periodic frames and near 1 for noise, so it serves as a voicing confidence.

## Variants and improvements

- **Best local estimate.** Step 6 of the paper looks for the smallest $d'(\tau^*)$ among the estimates of nearby frames and repeats the search near that period, which removes isolated errors.
- **Threshold choice.** A lower threshold gives fewer errors toward high frequencies but more frames that fall back to the global minimum; values near 0.1 are the common default.
- **Probabilistic YIN.** pYIN, from Mauch and Dixon in 2014, uses a distribution of thresholds to get several candidates with probabilities per frame and chooses a track with a [hidden Markov model](/hidden-markov-model/).
- **Fast lags.** Computing $r_t$ by FFT, as in line L1's identity, is the usual way in real-time code.
- **Other detectors.** The [cepstrum](/cepstrum/), the plain autocorrelation and spectral methods are the alternatives listed on the [pitch detection](/pitch-detection/) page.

## When to use it

Use YIN for monophonic pitch, such as one voice or one instrument, when you need a simple and fast detector with few octave errors and no training data. It works well in tuners and in analysis of speech intonation. For polyphonic music it is the wrong tool, because one difference function cannot show several periods. For noisy recordings or when a smooth track matters, combine it with tracking, as in pYIN, or use a trained estimator.

## Pitfalls

- **Taking the global minimum.** This is the octave error of the example. Use the threshold of line L6, and keep line L8 only as a fallback.
- **Interpolating $d'$ instead of $d$.** The normalization bends $d'$, and the vertex of a parabola on $d'$ is biased.
- **Stopping at the first lag below the threshold.** Without line L7, the estimate sits on the falling side of the dip, too short by up to a few samples.
- **A frame that is too short.** If $W + T$ samples do not hold two periods of the lowest pitch, the true dip is outside the searched lags, and line L8 picks a wrong lag.
- **Searching lags that are too small.** Lags below the shortest expected period can have small $d'$ for signals with a strong high harmonic, which gives an octave error upward. Limit $\tau$ to the expected range.
- **Floating-point cancellation.** The energy and correlation form subtracts large numbers; in floating point $d(\tau)$ can come out slightly negative. Clamp it at 0.

## Implementations

## History

Alain de Cheveigné and Hideki Kawahara published YIN in the Journal of the Acoustical Society of America in 2002. The paper starts from the autocorrelation method and adds one step at a time, the difference function, the cumulative mean normalization, the absolute threshold, the parabolic interpolation and the best local estimate, and reports the error rate after each step on speech databases with laryngograph signals as reference. The name refers to the yin and yang of Chinese philosophy, for the interplay between autocorrelation and cancellation in the method. YIN became a standard baseline for monophonic pitch detection, and pYIN extended it in 2014.

## References
