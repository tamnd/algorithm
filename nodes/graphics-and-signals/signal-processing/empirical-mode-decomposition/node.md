---
tag: H7DRYS
kind: algorithm
slug: empirical-mode-decomposition
name: Empirical mode decomposition
aliases:
- Hilbert-Huang transform
- EMD
area: graphics-and-signals/signal-processing
level: research
summary: "A heuristic that splits a signal into oscillating modes by sifting: subtract the mean of spline envelopes until a stopping rule holds. It has no convergence theory."
solves: [time-frequency-analysis]
model: real-ram
complexity:
  vars: {n: the length of the signal, K: the largest number of modes, S: the largest number of sifts per mode}
  time: {worst: O(K S n)}
  space: {extra: O(K n)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 1998
  people: [Norden E. Huang, Zheng Shen, Steven R. Long, Manli C. Wu, Hsing H. Shih, Quanan Zheng, Nai-Chyuan Yen, Chi Chao Tung, Henry H. Liu]
  note: Huang and coworkers defined intrinsic mode functions, the sifting process and the Hilbert spectrum of the modes for nonlinear and non-stationary data.
prereqs: [cubic-spline-interpolation, analytic-signal]
see_also: [hilbert-transform, natural-cubic-spline, thomas-algorithm, short-time-fourier-transform, continuous-wavelet-transform, discrete-wavelet-transform, filter-bank, time-frequency-uncertainty]
sources:
  - paper: doi:10.1098/rspa.1998.0193
    title: Norden E. Huang, Zheng Shen, Steven R. Long, Manli C. Wu, Hsing H. Shih, Quanan Zheng, Nai-Chyuan Yen, Chi Chao Tung and Henry H. Liu, The empirical mode decomposition and the Hilbert spectrum for nonlinear and non-stationary time series analysis, Proceedings of the Royal Society of London A 454(1971), 1998, 903 to 995
    locator: the definition of the intrinsic mode function, the sifting process with its SD stopping criterion, and the Hilbert spectrum of the modes (section numbers not confirmed)
  - paper: doi:10.1109/LSP.2003.821662
    title: Patrick Flandrin, Gabriel Rilling and Paulo Gonçalvès, Empirical mode decomposition as a filter bank, IEEE Signal Processing Letters 11(2), 2004, 112 to 114
    locator: the experiments with fractional Gaussian noise showing that EMD acts as a dyadic filter bank (general locator)
  - paper: doi:10.1142/S1793536909000047
    title: Zhaohua Wu and Norden E. Huang, Ensemble empirical mode decomposition, a noise-assisted data analysis method, Advances in Adaptive Data Analysis 1(1), 2009, 1 to 41
    locator: the ensemble method that averages the modes of many noisy copies to reduce mode mixing (general locator)
---

Empirical mode decomposition (EMD) splits a signal $x[0 \ldots n-1]$ into a few oscillating components, the intrinsic mode functions (IMFs), and a slowly varying residue, with $x = c_1 + c_2 + \cdots + c_K + r$. Huang and coworkers introduced it in 1998. Each IMF is found by sifting: draw a spline envelope through the maxima and one through the minima, subtract their mean, and repeat until a stopping rule holds; the first IMF holds the fastest oscillation, and later ones are slower. EMD is a heuristic. There is no theorem that sifting converges, that the stopping rule is ever met, or that the IMFs mean anything for a given signal; only the sum is exact by construction. With the [analytic signal](/analytic-signal/) of each IMF it gives the Hilbert-Huang transform, a [time-frequency analysis](/time-frequency-analysis/) of the signal.

## In plain words

Look at a wiggly curve and mark its peaks and its valleys. Draw a smooth line through the peaks and another through the valleys. Halfway between them runs a line that follows the slow drift of the curve. Subtract that middle line, and what is left wiggles around zero. Do it again a few times until the wiggle is clean. That wiggle is the first mode, the fastest part of the signal.

Take the first mode away and repeat on what is left. Each new mode is slower than the one before. Stop when what is left has no more wiggles, only a trend.

Nothing is fixed in advance, such as a set of sine waves or a window. The method follows the data. The price is that nobody has proved when or why it works, so its results need care.

## The problem

Given a real signal $x[0 \ldots n-1]$, write it as $x = \sum_{k=1}^{K} c_k + r$, where each $c_k$ is an intrinsic mode function and $r$ is monotone or has too few extrema to sift. Huang et al. define an IMF by two conditions: the numbers of extrema and of zero crossings are equal or differ by at most one, and the mean of the envelope through the maxima and the envelope through the minima is zero at every point. The second condition is never met exactly by a finite computation, so an implementation replaces it by a stopping rule. The problem is therefore not a well posed mathematical one: different envelopes, end treatments and stopping rules give different decompositions of the same signal.

## The algorithm

$\mathrm{SD}(p, h) = \sum_i (p[i] - h[i])^2 / \sum_i p[i]^2$ is the relative change of one sift, an interior extremum is an index $0 < i < n-1$ with $h[i]$ above (or below) its left neighbour and at least (or at most) its right neighbour, and a zero crossing is a sign change after exact zeros are dropped.

```pseudo id=main
EMD(x, K, S, ε)                             ▷ at most K modes, S sifts per mode
L1  r ← x; C ← empty list
L2  while |C| < K and r has at least 2 interior extrema do
L3      h ← r; s ← 0
L4      repeat
L5          U ← natural cubic spline through the maxima of h and both end samples; V ← the same through the minima
L6          p ← h; h ← h − (U + V)/2; s ← s + 1
L7      until (|#extrema(h) − #zero crossings(h)| ≤ 1 and SD(p, h) < ε) or s = S
L8      append h to C
L9      r ← r − h
L10 return C, r
```

Line L5 builds the envelopes. The splines are the [natural cubic splines](/natural-cubic-spline/) of [cubic spline interpolation](/cubic-spline-interpolation/), each found by one [tridiagonal solve](/thomas-algorithm/). Using the two end samples as knots is one of several end treatments; others mirror the extrema across the ends. Line L7 is the stopping rule: the first condition is the first IMF condition, and the second is the SD test of Huang et al. in the form of a ratio of sums. The paper sums the ratios point by point and suggests a limit between 0.2 and 0.3 for that form; the implementation uses $\varepsilon = 1/100$ for the ratio of sums. The cap $S$ in line L7 and the cap $K$ in line L2 are not in the original description, but every real code has them, because nothing guarantees that the loops end.

## Example

Take $n = 200$ samples of a fast tone, a slow tone and a trend,

$$x[i] = \operatorname{round}\bigl(100 \sin(2\pi i / 10)\bigr) + \operatorname{round}\bigl(60 \sin(2\pi i / 47)\bigr) + \lfloor i / 4 \rfloor,$$

all integers. With $K = 8$, $S = 50$ and $\varepsilon = 1/100$, the implementation gives 8 IMFs, and every one stopped by the rule, not by the cap:

| IMF | sifts | extrema | zero crossings |
|---|---|---|---|
| 1 | 2 | 40 | 39 |
| 2 | 5 | 9 | 8 |
| 3 | 5 | 5 | 4 |
| 4 | 5 | 3 | 2 |
| 5 | 9 | 2 | 1 |
| 6 | 23 | 2 | 1 |
| 7 | 28 | 2 | 1 |
| 8 | 32 | 2 | 1 |

The first IMF has two extrema for each period of 10 samples, so it is the fast tone. Its root mean square difference from $100 \sin(2\pi i/10)$ is 11.67 over all samples, but 1.14 on samples 20 to 179: the splines are poor near the ends, where they have no extrema to lean on. The second IMF should be the tone of period 47, but its root mean square difference from it is 50.6, and 40.2 on the interior: the slow tone and the trend share the modes 2 to 8, which is mode mixing. The sum $c_1 + \cdots + c_8 + r$ equals $x$ exactly in rational arithmetic, as it must.

## Correctness

There is no convergence theory for EMD. No theorem says that the sifting of lines L4 to L7 converges, that the limit is an IMF, that the outer loop of line L2 ends without the cap, or that the IMFs of a sum of tones are the tones. Analyses exist for special cases and for changed versions of the algorithm, but not for sifting as it is used. What holds for this algorithm, and what the tests check, is the following.

**Completeness.** After line L9, $x = \sum_{c \in C} c + r$. It holds before the loop, with $C$ empty and $r = x$, and each round adds $h$ to $C$ and removes it from $r$. This is exact whatever the envelopes are, provided the subtraction is exact, as it is with the rationals of the implementation.

**The stopping rule.** Every IMF that left the loop of line L7 because of the rule meets $|\#\text{extrema} - \#\text{zero crossings}| \le 1$ and $\mathrm{SD} < \varepsilon$ with respect to the sift before it; the others are marked as stopped by the cap after $S$ sifts.

**Termination.** Both loops end because of the caps $K$ and $S$. The proofs are below.

## Complexity

Line L5 finds the extrema in $O(n)$ and solves two tridiagonal systems of at most $n$ unknowns in $O(n)$, and line L6 is $O(n)$. So one sift costs $O(n)$ operations in the [real RAM](/real-ram/), one mode costs $O(S n)$, and the whole run costs $O(K S n)$ in the worst case, set by the caps. The observed counts are much smaller than the caps for the early modes: 2 to 9 sifts in the example, but 23 to 32 for the late ones. The modes and the residue take $O(K n)$ memory.

## Properties

- **Complete.** The modes and the residue add up to the input exactly.
- **Adaptive.** No basis, window or frequency grid is fixed in advance; the scale of each mode comes from the spacing of the extrema.
- **Not linear.** The decomposition of $x + y$ is in general not the sum of the decompositions, because the extrema of $x + y$ are not those of $x$ and $y$.
- **No orthogonality.** The modes are nearly orthogonal in many examples, but nothing makes them so; Huang et al. measure an index of orthogonality afterwards.
- **A filter bank on noise.** On white and fractional Gaussian noise, Flandrin, Rilling and Gonçalvès (2004) observed that the modes behave like a dyadic [filter bank](/filter-bank/), each mode with about half the mean frequency of the one before.
- **Sensitive to details.** Small changes of the signal, the stopping rule, the end treatment or the number of sifts change the modes, sometimes a lot.

## Variants and improvements

- **Hilbert spectral analysis.** The Hilbert-Huang transform takes the [analytic signal](/analytic-signal/) of each IMF, with the [Hilbert transform](/hilbert-transform/), and plots the envelope over time and instantaneous frequency. It works best when each mode is a single, slowly changing oscillation, which is the reason to sift first.
- **Ensemble EMD.** Wu and Huang (2009) add many copies of white noise to the signal, decompose each, and average the modes. This reduces mode mixing, at the cost of many runs and a residual noise.
- **Complete ensemble variants.** Later versions add the noise mode by mode so that the averaged modes still add up to the input.
- **Other stopping rules.** Fixed numbers of sifts, such as 10, or thresholds on the ratio of the envelope mean to the envelope amplitude at each point, are common alternatives to the SD test.
- **Multivariate and two-dimensional EMD.** Versions for vector signals and for images exist, with envelopes built from projections or surfaces.

## When to use it

Use EMD as an exploratory tool for short, non-stationary, possibly nonlinear records, such as geophysical, biomedical or mechanical signals, when no fixed basis suits the data and you want modes to look at. Check the result by eye and by changing the settings. When you need a decomposition with known properties, such as linearity, invertible frames, a known frequency resolution or error bounds, use the [short-time Fourier transform](/short-time-fourier-transform/) or a wavelet transform, such as the [continuous wavelet transform](/continuous-wavelet-transform/), instead.

## Pitfalls

- **Treating the modes as physical.** An IMF is what the procedure returned, not a proved component. Mode mixing, as in the example, puts one oscillation in several modes or several in one.
- **End effects.** The splines swing at the ends of the record, and the error spreads inward with every sift. Mirror the extrema or discard the edges.
- **No cap.** Without the caps $K$ and $S$ the loops may run for a very long time; stop on a sift count and report which modes stopped by the cap.
- **Reporting without settings.** The modes depend on the envelope, the end treatment and the stopping rule; state them, or another person cannot reproduce the result.
- **Over-sifting.** Many sifts flatten the amplitude of a mode toward a constant and push its amplitude changes into other modes.
- **Sampling.** The extrema of a sampled signal are only as accurate as the sampling; a tone with few samples per period has poorly placed extrema.

## Implementations

## History

Norden Huang and eight coworkers published EMD and the Hilbert spectrum in the Proceedings of the Royal Society of London A in 1998, after work on water waves at NASA; the combination was later called the Hilbert-Huang transform. The paper defined intrinsic mode functions so that their instantaneous frequency from the analytic signal makes sense, and gave the sifting process with an SD stopping criterion. In 2004 Flandrin, Rilling and Gonçalvès showed by experiment that EMD behaves like a filter bank on noise, and in 2009 Wu and Huang published ensemble EMD. A convergence theory for the original sifting is still missing.

## References
