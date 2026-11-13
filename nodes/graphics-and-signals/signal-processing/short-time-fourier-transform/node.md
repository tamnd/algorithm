---
tag: YJH16Z
kind: algorithm
slug: short-time-fourier-transform
name: Short-time Fourier transform
aliases:
- STFT
- spectrogram computation
area: graphics-and-signals/signal-processing
level: core
summary: "DFTs of windowed, overlapping frames of a signal. The squared magnitudes form the spectrogram, and overlap-add inverts it when the window meets the constant overlap-add condition."
solves: [time-frequency-analysis]
model: real-ram
complexity:
  vars: {L: the length of the signal, N: the window and DFT length, R: the hop between frames}
  time: {worst: O((L + N) N log N / R)}
  space: {extra: O((L + N) N / R)}
properties: {deterministic: true, online: true, in_place: false, exact: false}
history:
  year: 1977
  people: [Jont B. Allen, Lawrence R. Rabiner]
  note: Gabor proposed windowed Fourier analysis in 1946; Allen and Rabiner gave the unified account of DFT-based analysis and overlap-add synthesis in 1977.
prereqs: [discrete-fourier-transform, fast-fourier-transform, window-functions]
see_also: [time-frequency-uncertainty, griffin-lim-algorithm, overlap-add-method, spectral-leakage, welch-method, continuous-wavelet-transform, filter-bank, modified-discrete-cosine-transform]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 10.3, The Time-Dependent Fourier Transform
  - paper: doi:10.1109/PROC.1977.10770
    title: Jont B. Allen and Lawrence R. Rabiner, A unified approach to short-time Fourier analysis and synthesis, Proceedings of the IEEE 65(11), 1977, 1558 to 1564
    locator: the analysis by windowed DFTs and the overlap-add synthesis with its window condition
  - paper: doi:10.1109/TASSP.1984.1164317
    title: Daniel W. Griffin and Jae S. Lim, Signal estimation from modified short-time Fourier transform, IEEE Transactions on Acoustics, Speech, and Signal Processing 32(2), 1984, 236 to 243
    locator: Section II, equation (6), the least squares signal estimate from a modified STFT
  - book: isbn:9780123743701
    title: Stéphane Mallat, A Wavelet Tour of Signal Processing, The Sparse Way, third edition, Academic Press, 2009
    locator: Chapter 4, Time Meets Frequency (windowed Fourier transform)
---

The short-time Fourier transform (STFT) cuts a signal into frames of $N$ samples that start every $R$ samples, multiplies each frame by a window $w$, and takes the [discrete Fourier transform](/discrete-fourier-transform/) of each windowed frame. The result $X_m[k]$ tells how much of frequency $\omega_k = 2\pi k / N$ radians per sample is present near time $mR$, and $|X_m[k]|^2$ is the spectrogram. With a [fast Fourier transform](/fast-fourier-transform/) the cost is $O((N/R) \log N)$ operations per input sample. When the window meets the constant overlap-add condition, adding the inverse DFTs of the frames back in place gives the signal exactly.

## In plain words

One Fourier transform of a whole recording tells which notes occur, but not when. The STFT looks at the recording through a short window that slides along it. Each look sees only a few milliseconds of sound, fades smoothly to zero at its edges, and gets its own Fourier transform. Neighbouring looks overlap, so nothing falls between them.

Put the spectra side by side and you get a picture: time runs to the right, frequency runs up, and the brightness shows the strength. That picture is the spectrogram, the standard view of speech and music.

The process can run backwards. Undo each Fourier transform and add the pieces back where they came from. If the faded windows add up to a flat line where they overlap, the sum is the original recording, sample for sample.

## The problem

The input is a real or complex signal $x[0 \ldots L-1]$, a window $w[0 \ldots N-1]$ and a hop $R$ with $1 \le R \le N$. We set $x[i] = 0$ outside $0 \le i \le L - 1$. The output is, for every frame start $s_m = mR$ with $-N < s_m < L$, the spectrum

$$X_m[k] = \sum_{j=0}^{N-1} x[mR + j]\, w[j]\, e^{-2\pi i jk/N}, \qquad 0 \le k \le N - 1.$$

Bin $k$ is the frequency $\omega_k = 2\pi k / N$ in radians per sample, or $f_k = k f_s / N$ in Hz at a sample rate $f_s$. The frames with $s_m < 0$ or $s_m + N > L$ are padded with zeros; they are needed so that every sample is seen by the same number of window copies. This computes the discrete [time-frequency analysis](/time-frequency-analysis/) of $x$ on the grid of frames and bins.

The inverse problem is to get $x$ back from the frames. It is solvable exactly when no sample is missed, $\sum_m w[n - mR]^2 > 0$ for $0 \le n \le L - 1$. The plain overlap-add inverse below needs more, the constant overlap-add (COLA) condition

$$\sum_{m \in \mathbb{Z}} w[n - mR] = C \quad \text{for all } n, \text{ with a constant } C \ne 0,$$

where $w[j] = 0$ outside $0 \le j \le N - 1$.

## The algorithm

FFT$_N$ and IFFT$_N$ are the DFT and its inverse of length $N$, IFFT$_N$ with the factor $1/N$.

```pseudo id=main
STFT(x, w, R)                              ▷ x has length L, w has length N
L1  F ← empty list
L2  for m ← −⌊(N − 1)/R⌋ to ⌊(L − 1)/R⌋ do
L3      s ← m · R                          ▷ −N < s < L
L4      u[j] ← x[s + j] · w[j] for 0 ≤ j ≤ N − 1      ▷ x[i] = 0 outside 0 .. L − 1
L5      append (s, FFT_N(u)) to F
L6  return F

ISTFT-OLA(F, L, C)                         ▷ C is the COLA constant of w and R
L7  y ← L zeros
L8  for each (s, X) in F do
L9      v ← IFFT_N(X)
L10     for j ← 0 to N − 1 do
L11         if 0 ≤ s + j < L then y[s + j] ← y[s + j] + v[j] / C
L12 return y
```

Lines L2 and L3 list every frame whose window overlaps the signal, including the partial frames at both ends. Line L4 multiplies by the window, and line L5 stores the frame start with its spectrum. The squared magnitudes $|X|^2$ of the spectra are the spectrogram. In the inverse, line L9 gives back the windowed frame $u$ exactly, and lines L10 and L11 add it at its place, as in the [overlap-add method](/overlap-add-method/). Each sample then holds $x[n] \sum_m w[n - mR] = C x[n]$, so the division by $C$ gives $x[n]$.

When the window does not meet the COLA condition, or when the spectra were changed, use the weighted overlap-add (WOLA) inverse: multiply $v$ by the window again in line L11 and divide each sample by $\sum_m w[n - mR]^2$ instead of $C$. This is the least squares estimate of Griffin and Lim (1984), and it inverts the STFT for every window that covers each sample.

## Example

Let $x = [1, 2, 3, 4]$ ($L = 4$), $N = 4$, $R = 2$, and the periodic Hann window $w[j] = \frac{1}{2}(1 - \cos(2\pi j/4))$, which is $w = [0, \tfrac{1}{2}, 1, \tfrac{1}{2}]$. The overlap sums are $w[0] + w[2] = 1$ and $w[1] + w[3] = 1$, so the COLA condition holds with $C = 1$. Line L2 runs $m$ from $-1$ to $1$.

| start $s$ | $x[s \ldots s+3]$ | windowed frame $u$ | $X = \text{FFT}_4(u)$ | spectrogram $\lvert X \rvert^2$ |
|---|---|---|---|---|
| $-2$ | [0, 0, 1, 2] | [0, 0, 1, 1] | [2, $-1+i$, 0, $-1-i$] | [4, 2, 0, 2] |
| $0$ | [1, 2, 3, 4] | [0, 1, 3, 2] | [6, $-3+i$, 0, $-3-i$] | [36, 10, 0, 10] |
| $2$ | [3, 4, 0, 0] | [0, 2, 0, 0] | [2, $-2i$, $-2$, $2i$] | [4, 4, 4, 4] |

The inverse adds the windowed frames back in place: $y[0] = 1 + 0$, $y[1] = 1 + 1$, $y[2] = 3 + 0$, $y[3] = 2 + 2$, which is $[1, 2, 3, 4]$. The frame at $s = -2$ is necessary: without it, $y[0] = 0$ and $y[1] = 1$, because samples 0 and 1 are covered only by the right half of a window.

## Correctness

The inverse DFT of line L9 returns the windowed frame, $v[j] = x[s + j]\, w[j]$. Line L11 adds it at position $n = s + j$, so after the loop $y[n] = \frac{1}{C} \sum_m x[n]\, w[n - mR]$, summed over the frames of line L2. Every $m$ with $w[n - mR] \ne 0$ for some $0 \le n \le L - 1$ has $-N < mR < L$, so line L2 lists all of them, and the sum equals $\frac{1}{C} x[n] \sum_{m \in \mathbb{Z}} w[n - mR] = x[n]$ by the COLA condition. The WOLA inverse is correct by the same count with $w^2$ in place of $w$. The full proofs are below.

## Complexity

Line L2 runs $F = \lfloor (L - 1)/R \rfloor + \lfloor (N - 1)/R \rfloor + 1$ times, which is $(L + N)/R$ up to one frame. Each frame costs $N$ multiplications for the window and $\frac{N}{2} \log_2 N$ complex multiplications for a radix-2 FFT. Per input sample this is

$$\frac{N}{R}\left(1 + \tfrac{1}{2} \log_2 N\right)$$

multiplications, counting a complex one as one. For $N = 1024$ and $R = 256$ (an overlap of 75 percent) this is $4 \cdot 6 = 24$ per sample. The total is $O((L + N) N \log N / R)$ in the worst case in the [real RAM](/real-ram/), and the inverse has the same cost. The output has $F \cdot N$ complex numbers, so the transform is $N/R$ times redundant; for real $x$ only the bins $0 \le k \le N/2$ need to be stored, because $X_m[N - k]$ is the conjugate of $X_m[k]$. The algorithm needs one frame of $N$ samples as working memory, and it runs online with a delay of $N$ samples.

## Properties

- **Linear.** The STFT of $a x + b y$ is $a X + b Y$.
- **Shift by a hop.** Shifting $x$ by $R$ samples shifts the frame index by one. A shift that is not a multiple of $R$ gives different frames, so the spectrogram is not shift invariant in general.
- **Resolution.** The bins are $2\pi/N$ radians per sample apart, and each frame spans $N$ samples. A longer window gives finer frequency and coarser time. The [time-frequency uncertainty principle](/time-frequency-uncertainty/) bounds the product of the two spreads; the window shape sets the [spectral leakage](/spectral-leakage/) between the bins, see [window functions](/window-functions/).
- **Not every array is an STFT.** The frames overlap, so the $F \times N$ numbers are not free: an array of spectra is a consistent STFT only if it equals the STFT of some signal. Changing magnitudes or phases breaks this, which is why the WOLA inverse is a least squares fit, and why the [Griffin-Lim algorithm](/griffin-lim-algorithm/) must iterate.
- **COLA windows.** The periodic Hann window of length $N$ meets the COLA condition for every hop $R = N/K$ with an integer $K \ge 2$, with $C = N/(2R)$. The rectangular window meets it for every $R$ that divides $N$, with $C = N/R$. The periodic triangle $w[j] = 1 - |2j - N|/N$ of even length $N$ meets it at $R = N/2$ with $C = 1$.
- **Filter bank.** For fixed $k$, the sequence $X_m[k]$ over $m$ is the output of a bandpass filter with impulse response $w[-n] e^{2\pi i kn/N}$, sampled every $R$ samples. So the STFT is a uniform DFT [filter bank](/filter-bank/), and its synthesis is the matching bank.

## Variants and improvements

- **Weighted overlap-add.** The WOLA inverse above works for any window that covers each sample, and is the least squares inverse of a modified STFT. With a synthesis window $g$ instead of $w$, the condition becomes $\sum_m w[n - mR]\, g[n - mR] = 1$.
- **Zero padding.** An FFT of length $M > N$ of the zero-padded frame samples the same spectrum more densely. It does not improve the resolution.
- **Sliding DFT.** For $R = 1$ or a few bins, update each bin from the previous frame in $O(1)$ operations, or use the [Goertzel algorithm](/goertzel-algorithm/) for single bins.
- **Real input.** A [real-valued FFT](/real-valued-fft/) halves the work and the storage.
- **Critically sampled transforms.** The [modified discrete cosine transform](/modified-discrete-cosine-transform/) uses frames with 50 percent overlap and keeps only $R$ numbers per frame, with [perfect reconstruction](/perfect-reconstruction/) by time-domain alias cancellation. Audio codecs use it instead of the redundant STFT.
- **Gabor transform.** With a Gaussian window, the continuous STFT is the Gabor transform, the window with the smallest time-frequency spread.
- **Multiresolution.** The [continuous wavelet transform](/continuous-wavelet-transform/) uses short windows at high frequency and long windows at low frequency.

## When to use it

Use the STFT to see how the spectrum of a signal changes over time: spectrograms of speech and music, features for classifiers, and the front end of [pitch detection](/pitch-detection/). Use it as the domain for frame-by-frame processing that must be undone, such as [spectral subtraction](/spectral-subtraction/) and Wiener filtering of noise, followed by the WOLA inverse. For the power spectrum of a stationary signal, the average of the frames is the [Welch method](/welch-method/). When the signal has short events at high frequency and long ones at low frequency, a wavelet transform fits better than one fixed window.

## Pitfalls

- **The symmetric Hann window.** The symmetric Hann window $\frac{1}{2}(1 - \cos(2\pi j/(N - 1)))$ is the common default in filter design, and it does not meet the COLA condition. For $N = 16$ at $R = 8$ its overlap sums range from 0.898 to 0.989, and plain overlap-add of a random signal in $[-1, 1]$, divided by the mean sum 0.9375, gives a maximum error of 0.054. The periodic form with $N$ in the denominator gives an error of $3 \times 10^{-16}$ in the same test.
- **A hop that does not fit.** The rectangular window of length 16 at $R = 6$ has overlap sums 3, 3, 3, 3, 2, 2, repeating; with $C$ the mean sum $8/3$, overlap-add returns $\frac{9}{8} x[n]$ or $\frac{3}{4} x[n]$, so it is wrong by up to 25 percent. The periodic Hann window at $R = 6$ has sums from 1.29 to 1.38. Use the WOLA inverse, or a hop of $N/K$.
- **Missing edge frames.** Frames that start only at $s \ge 0$ and end at $s + N \le L$ leave the first and last $N - R$ samples with too few window copies. Pad the signal, or list the partial frames as in line L2.
- **The wrong gain.** The COLA constant is $C = N/(2R)$ for the periodic Hann window, not 1. Forgetting it scales the output.
- **Conventions.** Libraries differ in whether the frame time is its start or its centre, whether the phase is measured from the frame start or from sample 0, and whether the window is normalized. Phase-based processing breaks when two of them are mixed.
- **Modified spectra.** After a change to the magnitudes, the OLA inverse of the changed frames is not the closest signal, and the frames of the result have different magnitudes again. The WOLA inverse is the closest signal in the least squares sense.

## Implementations

## History

Dennis Gabor proposed in 1946 to analyse signals by Fourier transforms of short pieces, with Gaussian windows, and drew the time-frequency plane as a grid of cells. The sound spectrograph of Bell Laboratories, described in the same year, made the spectrogram an analogue instrument for speech research. After the FFT, Jont Allen and Lawrence Rabiner in 1977 gave a unified account of STFT analysis by windowed DFTs and of synthesis by overlap-add and by filter banks, with the window conditions for exact reconstruction. Daniel Griffin and Jae Lim in 1984 derived the weighted overlap-add as the least squares estimate of a signal from a modified STFT, and used it in their iteration for signals from STFT magnitudes.

## References
