---
tag: C4662N
kind: algorithm
slug: rasta-filtering
name: RASTA filtering
aliases:
- relative spectral filtering
- RASTA
area: natural-language-and-speech/speech-analysis-and-synthesis
level: advanced
summary: Band-pass filter the time series of each log spectral band to remove slow channel effects and fast frame-to-frame noise.
solves: [automatic-speech-recognition]
model: real-ram
complexity:
  vars: {T: the number of frames, B: the number of bands}
  time: {worst: O(T B)}
  space: {extra: O(B)}
properties: {deterministic: true, online: true, in_place: false, exact: true}
history:
  year: 1994
  people: [Hynek Hermansky, Nelson Morgan]
  note: Hermansky and Morgan filtered the log critical band trajectories of PLP with a fixed band-pass filter, so that a fixed channel, which adds a constant to each log band, is removed, and showed that this made recognition more robust to changes of microphone and telephone line.
prereqs: [iir-filter, mel-filter-bank, perceptual-linear-prediction]
see_also: [cepstral-mean-normalization, delta-features, mel-frequency-cepstral-coefficients, frequency-response, z-transform, spectral-subtraction, pre-emphasis, automatic-speech-recognition]
sources:
  - paper: doi:10.1109/89.326616
    title: Hynek Hermansky and Nelson Morgan, RASTA processing of speech, IEEE Transactions on Speech and Audio Processing 2(4), 1994, 578 to 589
    locator: "the RASTA band-pass filter of the log critical band trajectories, its transfer function with the pole at 0.98, and the J-RASTA variant for additive noise"
  - book: isbn:9780130226167
    title: Xuedong Huang, Alex Acero and Hsiao-Wuen Hon, Spoken Language Processing, Prentice Hall, 2001
    locator: "Chapter 10 (Environmental Robustness), the discussion of cepstral mean normalization and RASTA"
  - url: https://www.ee.columbia.edu/~dpwe/resources/matlab/rastamat/
    title: Daniel P. W. Ellis, PLP and RASTA (and MFCC, and inversion) in Matlab
    locator: "the function rastafilt.m, which uses a pole of 0.94"
---

RASTA filtering runs a fixed band-pass filter along time over the log energy of each spectral band, one value per frame, so that changes slower than about 0.3 Hz and faster than about 13 Hz are removed. [Cepstral mean normalization](/cepstral-mean-normalization/) removes only the mean of each trajectory over an utterance or a window; RASTA also removes slow drifts and fast jitter, and it works frame by frame with no look at the whole utterance. [Delta features](/delta-features/) are also a filter along time, but they are added as new features, while RASTA replaces the trajectories it filters. It was made for [perceptual linear prediction](/perceptual-linear-prediction/), where the filter runs on the log critical band spectrum before the all-pole fit, and it works the same way on the log energies of a [mel filter bank](/mel-filter-bank/).

## In plain words

A microphone or a telephone line acts like a fixed tone control: it makes some frequencies louder and some softer, and it does not change while a person talks. After the log, such a fixed change adds the same number to a band in every frame. Speech, on the other hand, changes the energy of a band a few times per second, as the syllables come and go. RASTA follows each band over time and keeps only the changes that happen at about the speed of speech. A level that stays the same, or that drifts very slowly, is removed, and so is very fast flicker from one frame to the next. The result is a set of band energies that depends less on the microphone and the line.

## The problem

Given the log band energies $X[t][j]$ of $T$ frames and $B$ bands, for example from a [mel filter bank](/mel-filter-bank/) or the critical band analysis of PLP at 100 frames per second, compute filtered trajectories $Y[t][j]$ such that a constant added to a band trajectory does not change the output, and the output keeps the modulation frequencies of speech while it removes very slow and very fast changes.

## The algorithm

Hermansky and Morgan use, for each band, the filter

$$H(z) = 0.1\, z^{4}\, \frac{2 + z^{-1} - z^{-3} - 2 z^{-4}}{1 - \rho z^{-1}}, \qquad \rho = 0.98.$$

The factor $z^4$ only moves the output 4 frames earlier, so this page uses the causal filter without it, and its output is the same signal 4 frames later. The numerator is a smoothed slope over 5 frames, and the pole at $\rho$ is a leaky integrator. Before the first frame, the input is taken equal to the first value of the trajectory and the output to 0.

```pseudo id=main
RASTA(X, ρ)          ▷ X[t][j] for t = 0 .. T-1 and j = 1 .. B, with 0 ≤ ρ < 1
L1  for j ← 1 to B do
L2      x ← (X[0][j], …, X[T-1][j]); x[-4], …, x[-1] ← x[0]; y[-1] ← 0
L3      for t ← 0 to T - 1 do u ← 0.1 (2 (x[t] - x[t-4]) + (x[t-1] - x[t-3]))
L4          y[t] ← u + ρ y[t-1]; Y[t][j] ← y[t]
L5  return Y
```

Line L3 is the numerator $0.1(2 + z^{-1} - z^{-3} - 2z^{-4})$, with the taps written in pairs so that the four differences are exactly 0 on a constant. Line L4 is the denominator. Only the 4 last inputs and the last output of each band must be kept, so the filter runs as the frames arrive.

## Example

The impulse response $h[n]$ and the step response $g[n] = \sum_{s \le n} h[s]$ with $\rho = 0.98$ are:

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $h[n]$ | 0.2 | 0.296 | 0.2901 | 0.1843 | $-0.0194$ | $-0.0190$ | $-0.0186$ | $-0.0183$ |
| $g[n]$ | 0.2 | 0.496 | 0.7861 | 0.9704 | 0.951 | 0.932 | 0.9133 | 0.8951 |

Take one band whose log energy is 3 in every frame except frame 3, where a short burst makes it 4. Lines L3 and L4 give the output 0, 0, 0, 0.2, 0.296, 0.2901, 0.1843, $-0.0194$, and so on: the constant 3 is gone and the burst comes out as the impulse response. If the channel adds 10 to this band, so the input is 13 with a burst of 14, the output is the same. If the level jumps from 3 to 4 at frame 3 and stays there, the output is the step response: it rises to 0.97 within 4 frames and then decays by the factor 0.98 per frame, to half its peak after about 34 frames, or 0.34 s at 100 frames per second.

The magnitude of $H$ at 100 frames per second, with $\rho = 0.98$:

| modulation frequency (Hz) | 0.1 | 0.5 | 1 | 2 | 5 | 10 | 20 | 30 |
|---|---|---|---|---|---|---|---|---|
| $\lvert H \rvert$ | 0.300 | 0.849 | 0.960 | 0.989 | 0.957 | 0.814 | 0.365 | 0.028 |
| dB | $-10.5$ | $-1.4$ | $-0.4$ | $-0.1$ | $-0.4$ | $-1.8$ | $-8.7$ | $-31.1$ |

The peak is 0.9895 at 2.22 Hz, and the gain stays within 3 dB of the peak from 0.31 Hz to 12.8 Hz. The numerator factors as $(1 - z^{-2})(2 + z^{-1} + 2 z^{-2})$, so $H$ is exactly 0 at 0 Hz, at 50 Hz, and at the frequency $\frac{100}{2\pi} \arccos(-\frac14) = 29.0$ Hz, where the zeros of $2 + z^{-1} + 2z^{-2}$ lie on the unit circle.

## Correctness

The filter computes a defined transform, so correctness means that lines L1 to L5 compute it and that it has the properties the problem asks for. The full proofs are below.

- **The recursion is the filter.** Let $\tilde x[t] = x[t] - x[0]$ for $t \ge 0$ and $\tilde x[t] = 0$ for $t < 0$. Because the numerator taps sum to 0, line L3 gives the same $u$ for $x$ and for $\tilde x$, so $y[t] = \sum_{s=0}^{t} h[s]\, \tilde x[t - s]$, where $h$ is the impulse response of $H$ without $z^4$ (theorem).
- **Offsets are removed exactly.** A constant trajectory gives $y = 0$ from the first frame on, and adding a constant to a trajectory does not change any output (theorem).
- **A fixed channel is removed approximately.** A fixed linear filter multiplies the spectrum by a fixed $|C(f)|^2$. It adds a constant to a log band only when $|C(f)|$ is nearly flat inside the band and the frames are much longer than the impulse response of the channel, so in practice RASTA removes most, not all, of a channel (heuristic).
- **Stable.** The only pole is at $\rho$ with $0 \le \rho < 1$, so $\sum_n |h[n]|$ is finite and a bounded input gives a bounded output (theorem).
- **Same on cepstra.** The filter is linear and the same for every band, and the DCT of [MFCC](/mel-frequency-cepstral-coefficients/) is a fixed linear map, so filtering the log bands and then taking the DCT gives the same result as filtering each cepstral coefficient (theorem).

## Complexity

In the [real RAM](/real-ram/), line L3 costs 4 additions and 2 multiplications and line L4 one multiplication and one addition, so the work is $O(T B)$, about 8 operations per band and frame. The state is 4 past inputs and 1 past output per band, $O(B)$ numbers, beyond the output. The implementation here copies each band into a list, which uses $O(T)$ more memory but does not change the time.

## Properties

- **Causal and online.** The causal form needs no future frames; its output is the noncausal filter of the paper delayed by 4 frames.
- **Linear and time invariant along time.** The filter commutes with any fixed linear map across the bands, such as the DCT.
- **Not a linear phase filter.** The pole makes the group delay change with the modulation frequency, so peaks of the trajectories move by different amounts. Recognizers trained on RASTA features learn this shape.
- **Long memory.** With $\rho = 0.98$ the time constant is about 50 frames, or 0.5 s. The filter needs about this long to forget an old level.

## Variants and improvements

- **Pole 0.94.** Ellis's widely used rastamat code uses $\rho = 0.94$, which shortens the memory to about 16 frames and moves the 3 dB band to 0.88 Hz to 13.5 Hz.
- **J-RASTA.** Hermansky and Morgan also describe filtering $\ln(1 + J S)$ in place of $\ln S$, where $J$ depends on the noise level. For small $J S$ this is nearly linear in $S$, so additive noise becomes closer to an offset that the filter can reduce.
- **RASTA on cepstra.** Many systems filter the cepstral coefficients in place of the log bands. By the linearity argument above the result is the same up to the truncation of the DCT.
- **Learned temporal filters.** Later work designed the filter along time from data, for example with linear discriminant analysis on long spans of log band energies.

## When to use it

Use RASTA when the channel changes between training and test, for example different microphones or telephone lines, and the system must process speech as it arrives, so that the mean over a whole utterance is not available. For offline recognition with utterances of a few seconds, [cepstral mean normalization](/cepstral-mean-normalization/) over the utterance is simpler and removes a constant offset just as well. Do not expect RASTA to remove additive noise: noise adds to the power, not to the log, and [spectral subtraction](/spectral-subtraction/) or a [Wiener filter](/wiener-filter/) addresses it.

## Pitfalls

- **Filter the log, not the energy.** The channel becomes an offset only after the log. RASTA on the power spectrum does not remove it.
- **Frame rate.** The coefficients are designed for 100 frames per second. At another frame rate every frequency of the response scales with the rate, so the pass band moves.
- **Start up.** The first frames depend on the initial state. This page repeats the first input and sets the past output to 0, so a constant start gives 0; other toolkits start differently, and their first frames do not match.
- **Delay.** The causal output is 4 frames late compared with the filter of the paper. When RASTA features are combined with unfiltered features, align them first.
- **Short utterances.** With $\rho = 0.98$ a change of channel is forgotten only after about half a second, so utterances shorter than that keep part of the channel.

## Implementations

## History

Hermansky and colleagues introduced RASTA in the early 1990s as an addition to [perceptual linear prediction](/perceptual-linear-prediction/), and Hermansky and Morgan gave the full account in 1994. The idea came from hearing: listeners pay little attention to a sound whose spectrum does not change, and the spectrum of speech changes at the rate of syllables. A filter along time on the log spectrum copies this, and since a fixed channel is an offset in the log domain, the same filter removes the channel. RASTA-PLP was widely used for telephone speech in the 1990s, and the idea of filtering band trajectories along time led to later work on modulation spectrum features.

## References
