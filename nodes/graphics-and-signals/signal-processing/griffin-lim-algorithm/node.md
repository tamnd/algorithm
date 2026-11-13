---
tag: KC8JAJ
kind: algorithm
slug: griffin-lim-algorithm
name: Griffin-Lim algorithm
aliases:
- Griffin-Lim phase reconstruction
area: graphics-and-signals/signal-processing
level: advanced
summary: "Rebuilds a signal from STFT magnitudes alone by alternating projections. The spectral distance never increases, but it can stop at a local minimum far from the true signal."
solves: [phase-retrieval]
model: real-ram
complexity:
  vars: {L: the length of the signal, N: the window and DFT length, R: the hop between frames, T: the number of iterations}
  time: {worst: O(T (L + N) N log N / R)}
  space: {extra: O((L + N) N / R)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 1984
  people: [Daniel W. Griffin, Jae S. Lim]
  note: Griffin and Lim derived the least squares inverse of a modified STFT and the magnitude-only iteration, and proved that its distance does not increase.
prereqs: [short-time-fourier-transform, phase-retrieval]
see_also: [overlap-add-method, window-functions, projected-gradient-descent, fixed-point-iteration, time-frequency-analysis, signal-reconstruction]
sources:
  - paper: doi:10.1109/TASSP.1984.1164317
    title: Daniel W. Griffin and Jae S. Lim, Signal estimation from modified short-time Fourier transform, IEEE Transactions on Acoustics, Speech, and Signal Processing 32(2), 1984, 236 to 243
    locator: Section II, equation (6), the least squares estimate; Section III, equations (13) and (14), the magnitude-only iteration and its distance; Appendix, the proof that the distance does not increase
  - paper: doi:10.1109/WASPAA.2013.6701851
    title: Nathanaël Perraudin, Peter Balazs and Peter L. Søndergaard, A fast Griffin-Lim algorithm, IEEE Workshop on Applications of Signal Processing to Audio and Acoustics, 2013, 1 to 4
    locator: the accelerated iteration with an extrapolation step
  - paper: "R. W. Gerchberg and W. O. Saxton, A practical algorithm for the determination of phase from image and diffraction plane pictures, Optik 35(2), 1972, pages 237 to 246"
    locator: the iteration between the image plane and the diffraction plane
---

The Griffin-Lim algorithm finds a real signal whose [short-time Fourier transform](/short-time-fourier-transform/) has given magnitudes $A_m[k]$, when the phases are lost. It alternates two steps: put the target magnitudes on the current spectra and keep their phases, then go back to the nearest real signal by a least squares overlap-add. Griffin and Lim (1984) proved that the spectral distance $D = \sum_{m,k} (|X_m[k]| - A_m[k])^2$ never increases from one iteration to the next. It does not promise the global minimum: the iteration often stops in a local minimum, and even at $D = 0$ the answer is only defined up to the sign of the signal.

## In plain words

A spectrogram says how strong each frequency is at each moment, but not how the waves line up. To play it as sound you need that missing alignment. Griffin-Lim guesses it.

Start from any guess, even all waves lined up the same way. Build the sound that comes closest to the guess, then look at that sound through the same sliding window. Its strengths will be wrong, so replace them by the wanted strengths and keep the alignment the sound now has. Repeat.

Each round fixes one requirement while it breaks the other a little, but the mismatch can never grow. After some dozens of rounds the sound is often usable. It may still differ from the true sound, because several sounds can have nearly the same spectrogram and the method can settle on the wrong one.

## The problem

The input is a window $w[0 \ldots N-1]$, a hop $R$, a length $L$ and an array of target magnitudes $A_m[k] \ge 0$, one row for each frame start $s_m = mR$ with $-N < s_m < L$ and one entry for each bin $0 \le k \le N - 1$. The window must cover every sample, $\sum_m w[n - mR]^2 > 0$ for $0 \le n \le L - 1$. The output is a real signal $x[0 \ldots L-1]$ whose STFT $X$ makes the distance

$$D(x) = \sum_m \sum_{k=0}^{N-1} \bigl(|X_m[k]| - A_m[k]\bigr)^2$$

small. This is the STFT case of [phase retrieval](/phase-retrieval/). If $A$ is the STFT magnitude of some signal $x_0$, then $D(x_0) = 0$ and $D(-x_0) = 0$, so the best possible answer is $\pm x_0$. If $A$ was changed, for example by a denoiser, then $D = 0$ may be impossible.

## The algorithm

STFT is the analysis of the [short-time Fourier transform](/short-time-fourier-transform/), and IFFT$_N$ is the inverse DFT with the factor $1/N$.

```pseudo id=main
GRIFFIN-LIM(A, w, R, L, T)                 ▷ T iterations
L1  Y ← A with a start phase on each bin   ▷ zero phase, or random phases
L2  x ← LSEE(Y, w, R, L)
L3  for t ← 1 to T do
L4      X ← STFT(x, w, R)
L5      Y_m[k] ← A_m[k] · X_m[k] / |X_m[k]| for all m, k    ▷ A_m[k] if X_m[k] = 0
L6      x ← LSEE(Y, w, R, L)
L7  return x

LSEE(Y, w, R, L)                           ▷ the real signal whose STFT is nearest to Y
L8  num ← L zeros; den ← L zeros
L9  for each frame m, with start s = mR do
L10     y ← IFFT_N(Y_m)
L11     for j ← 0 to N − 1 with 0 ≤ s + j < L do num[s + j] ← num[s + j] + w[j] · Re y[j]; den[s + j] ← den[s + j] + w[j]²
L12 return num / den, entry by entry
```

Line L5 is the projection onto the set of arrays with magnitude $A$: of all complex numbers of modulus $A_m[k]$, the one with the phase of $X_m[k]$ is the nearest to $X_m[k]$. Lines L8 to L12 are the projection onto the set of STFTs of real signals: they return the signal whose STFT is nearest to $Y$ in the sum of squares, by the weighted overlap-add formula. The distance $D$ after iteration $t$ is the squared distance between $X$ of line L4 and $Y$ of line L5.

## Example

Take $x_0 = [1, 2, 3, 4]$, $N = 4$, $R = 2$ and the periodic Hann window $[0, \tfrac{1}{2}, 1, \tfrac{1}{2}]$, as in the example of the [short-time Fourier transform](/short-time-fourier-transform/). The target magnitudes of the frames at $s = -2, 0, 2$ are $[2, \sqrt{2}, 0, \sqrt{2}]$, $[6, \sqrt{10}, 0, \sqrt{10}]$ and $[2, 2, 2, 2]$. With zero start phases, the inverse DFTs of the three rows are $\frac{1}{4}[2 + 2\sqrt{2}, 2, 2 - 2\sqrt{2}, 2]$, $\frac{1}{4}[6 + 2\sqrt{10}, 6, 6 - 2\sqrt{10}, 6]$ and $[2, 0, 0, 0]$, and line L2 gives $x = [\frac{1 - \sqrt{2}}{2}, 2, \frac{3 - \sqrt{10}}{2}, \frac{3}{2}]$.

| iteration $t$ | $D$ | $x$, rounded |
|---|---|---|
| 0 | 48.3984 | [−0.2071, 2.0000, −0.0811, 1.5000] |
| 1 | 21.7603 | [0.3566, 4.1963, 1.0119, 1.9961] |
| 2 | 6.3933 | [0.6185, 3.8608, 2.5704, 2.3363] |
| 3 | 1.9362 | [0.7157, 3.1229, 3.0159, 3.0504] |
| 5 | 0.2265 | [0.8625, 2.3988, 3.0673, 3.7084] |
| 10 | 0.0017 | [0.9878, 2.0352, 3.0075, 3.9768] |
| 50 | below $10^{-18}$ | [1.0000, 2.0000, 3.0000, 4.0000] |

Here the iteration finds $x_0$ itself. On larger random signals it usually does not. For random signals of length $L = 64$ with $N = 16$, $R = 4$, uniform samples in $[-1, 1]$ and random start phases, the relative error $\sqrt{D / \sum A^2}$ fell from about 0.7 to 0.131, 0.218, 0.222, 0.163 and 0.225 after 200 iterations on five seeds. $D$ decreased at every step, and the returned signals were far from both $x_0$ and $-x_0$.

## Correctness

Let $\mathcal{C}$ be the set of STFTs of real signals of length $L$ and $\mathcal{A}$ the set of arrays with $|Y_m[k]| = A_m[k]$. With the norm $\|Z\|^2 = \sum |Z_m[k]|^2$, line L5 maps $X$ to a nearest point $P_\mathcal{A}(X)$ of $\mathcal{A}$, so $D(x) = \|X - P_\mathcal{A}(X)\|^2$. Lines L8 to L12 map $Y$ to the nearest point $P_\mathcal{C}(Y)$ of $\mathcal{C}$. Write $X_t$ for the STFT of the estimate after iteration $t$. Then

$$\|X_{t+1} - P_\mathcal{A}(X_{t+1})\| \le \|X_{t+1} - P_\mathcal{A}(X_t)\| \le \|X_t - P_\mathcal{A}(X_t)\|.$$

The first step holds because $P_\mathcal{A}(X_{t+1})$ is the point of $\mathcal{A}$ nearest to $X_{t+1}$. The second holds because $X_{t+1} = P_\mathcal{C}(P_\mathcal{A}(X_t))$ is the point of $\mathcal{C}$ nearest to $P_\mathcal{A}(X_t)$, and $X_t$ is also in $\mathcal{C}$. So $D$ does not increase. The full proof, with the least squares step, is below. The set $\mathcal{A}$ is not convex, so nothing here makes the limit a global minimum.

## Complexity

Each iteration does one STFT and one inverse, that is $2F$ FFTs of length $N$ with $F = \lfloor (L-1)/R \rfloor + \lfloor (N-1)/R \rfloor + 1$ frames, plus $O(FN)$ other operations. Per input sample and per iteration this is about $\frac{N}{R}(\log_2 N + 3)$ multiplications. The total is $O(T (L + N) N \log N / R)$ in the worst case in the [real RAM](/real-ram/), for $T$ iterations; $T$ is chosen by the user, and values of 50 to 200 are common. The memory holds the target magnitudes and one array of spectra, $O((L + N) N / R)$ numbers.

## Properties

- **Monotone.** The distance $D$ never increases. Griffin and Lim also show that the estimates approach a set of critical points of $D$.
- **No global guarantee.** The magnitude set is not convex, so the iteration can stop at a local minimum with $D > 0$, or move very slowly, even when a signal with $D = 0$ exists.
- **Sign ambiguity.** $x$ and $-x$ have the same STFT magnitudes, and both are fixed points of the iteration.
- **Depends on the start.** With a fixed start phase the algorithm is deterministic; different random starts give different answers.
- **Needs overlap.** The overlap of the frames is what ties the phases of neighbouring frames together. In practice an overlap of 75 percent works much better than 50 percent.

## Variants and improvements

- **Fast Griffin-Lim.** Perraudin, Balazs and Søndergaard (2013) add an extrapolation step, $Y_t + \alpha (Y_t - Y_{t-1})$ with $\alpha$ near 0.99, before the projection onto consistent STFTs. It converges much faster in practice and often to a better point.
- **Better start phases.** A start phase that is consistent between frames, for example from phase-gradient heuristics, needs far fewer iterations than zero or random phases.
- **Online versions.** Real-time variants update only the newest frames, with a fixed number of iterations per frame.
- **Plain overlap-add.** Replacing the least squares step by a plain overlap-add without the division by $\sum w^2$ is the variant that Griffin and Lim call OA-MSTFTM. It has no proof that the distance does not increase.
- **Other phase retrieval methods.** The same alternation with other constraints is the Gerchberg-Saxton and the Fienup iterations of [phase retrieval](/phase-retrieval/). Gradient methods on $D$ and convex relaxations give other trade-offs.

## When to use it

Use Griffin-Lim to turn a magnitude spectrogram back into sound when no phase is available: after time-scale or pitch modification of the magnitudes, after a model that predicts spectrograms, or to listen to a spectrogram. It needs no training and works on any STFT with enough overlap. Expect some phase artefacts, a metallic or rough sound. When the original phase is available, use the plain inverse of the [short-time Fourier transform](/short-time-fourier-transform/) instead. When the best audio quality matters, trained vocoders now do better.

## Pitfalls

- **Treating it as exact.** A small $D$ does not mean that $x$ is close to the original signal. In the tests above the relative error of the magnitudes was about 0.2 while the signals themselves were not close.
- **The window and hop of the target.** The STFT in line L4 must use the same window, hop, DFT length and frame alignment as the one that made $A$. A mismatch keeps $D$ high whatever the number of iterations.
- **Too little overlap.** With $R = N/2$ or larger, the magnitudes leave much freedom, and the result sounds worse.
- **Comparing $D$ across settings.** $D$ depends on the scale of $A$. Report the relative error $\sqrt{D / \sum A^2}$.
- **Inconsistent targets.** A spectrogram that was edited, or computed with a different window, is not the STFT magnitude of any signal. Then $D$ stays above zero, and the decrease of $D$ says nothing about quality.

## Implementations

## History

Daniel Griffin and Jae Lim published the method in 1984. They first derived the least squares estimate of a signal from a modified STFT, which is the weighted overlap-add, and then the iteration for a given STFT magnitude, with a proof that the distance does not increase and an application to the time-scale modification of speech. The alternation between a magnitude constraint and another constraint goes back to the 1972 algorithm of Gerchberg and Saxton for optics. In 2013 Perraudin, Balazs and Søndergaard published the fast Griffin-Lim algorithm. Griffin-Lim became the standard simple way to turn the spectrograms of text-to-speech systems into sound.

## References
