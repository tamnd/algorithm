---
tag: 8B18AH
kind: algorithm
slug: semblance-velocity-analysis
name: Semblance velocity analysis
aliases:
- velocity spectrum
- semblance
area: imaging-and-inverse-problems/seismic-imaging
level: core
summary: "Scan trial stacking velocities over a common-midpoint gather, measure the semblance (normalized stack energy) along each hyperbola in a time window, and pick the velocities of the peaks."
model: real-ram
complexity:
  vars: {n: the number of scanned zero-offset times, k: the number of trial velocities, m: the number of traces in the gather, w: the number of samples in the window}
  time: {worst: O(n k m w), average: O(n k m w), best: O(n k m w)}
  space: {extra: O(n k)}
properties: {deterministic: true, output_range: "between 0 and 1", scale_invariant: true, noise_level: 1/m}
history:
  year: 1971
  people: [N. S. Neidell, M. Turhan Taner]
  note: Taner and Koehler (1969) computed velocity spectra by stacking along trial hyperbolas. Neidell and Taner (1971) defined semblance as a normalized coherence measure for multichannel data and compared it with other measures.
prereqs: [normal-moveout-correction]
see_also: [common-midpoint-stacking, dix-formula, parabolic-radon-transform, cross-correlation, hough-transform, seismic-reflection-model]
sources:
  - paper: doi:10.1190/1.1440186
    title: N. S. Neidell and M. Turhan Taner, Semblance and other coherency measures for multichannel data, Geophysics 36(3), 1971, 482 to 497
    locator: the definition of semblance as a ratio of output to input energy and its comparison with other coherence measures
  - paper: doi:10.1190/1.1440058
    title: M. Turhan Taner and Fulton Koehler, Velocity spectra, digital computer derivation and applications of velocity functions, Geophysics 34(6), 1969, 859 to 881
    locator: velocity spectra from stacks along trial hyperbolas, and their use for picking stacking velocities
  - book: isbn:9781560800941
    title: Oz Yilmaz, Seismic Data Analysis, Society of Exploration Geophysicists, 2001, Investigations in Geophysics 10
    locator: the chapter on velocity analysis and statics corrections (velocity spectra, semblance, velocity picking)
---

Semblance velocity analysis finds the stacking velocity of the reflections in a common-midpoint gather. For each zero-offset time and each trial velocity it reads the traces along the hyperbola of [normal moveout](/normal-moveout-correction/) and measures how alike they are with the semblance, a number between 0 and 1. The table of semblance over time and velocity is the velocity spectrum. Its peaks give the velocities that flatten the reflections, which [common-midpoint stacking](/common-midpoint-stacking/) needs, and which the [Dix formula](/dix-formula/) converts to interval velocities.

## In plain words

A reflection in a gather lies on a curve whose bend depends on the speed of sound in the rock. Guess a speed, follow the curve that this speed predicts, and look at the traces along it. If the guess is right, the traces show the same wiggle at the same time, and adding them gives a big result. If the guess is wrong, the wiggles do not line up and partly cancel. Semblance turns this into a score from 0 to 1: the energy of the sum, divided by what the sum would have if all traces agreed perfectly. Try many speeds at many times and draw the scores as a map. Bright spots on the map mark the reflections and their speeds.

## The problem

Input: a gather of $m$ traces $d_i$ with offsets $x_i$ and sample interval $\Delta t$; a list of trial velocities $v_1, \ldots, v_k$; a half window $W$ in samples; the times to scan. Output: the velocity spectrum $S(t_0, v)$, and for each time of interest the velocity of the largest peak. For one window and one velocity, with $a_i(\tau) = d_i\big(\sqrt{\tau^2 + x_i^2/v^2}\big)$,
$$S(t_0, v) = \frac{\sum_{\tau} \big(\sum_{i=1}^{m} a_i(\tau)\big)^2}{m \sum_{\tau} \sum_{i=1}^{m} a_i(\tau)^2},$$
where $\tau$ runs over the $w = 2W + 1$ samples of the window centered at $t_0$.

## The algorithm

```pseudo id=main
VELOCITY-SPECTRUM(d, x, Δt, v_1..v_k, W, times)
L1  for each zero-offset index j in times do
L2      row_j ← [SEMBLANCE(d, x, Δt, j, v_ℓ, W) for ℓ ← 1 to k]
    SEMBLANCE(d, x, Δt, j, v, W)
L3      A ← 0; B ← 0
L4      for τ ← j - W to j + W do
L5          a_i ← d_i at time sqrt((τ Δt)² + x_i² / v²) for every trace i   ▷ linear interpolation
L6          A ← A + (Σ_i a_i)²;  B ← B + Σ_i a_i²
L7      return A / (m B), or 0 if B = 0
L8  return the rows; pick the v_ℓ with the largest value in each row
```

The window $W$ smooths the measure over a few samples, about half a period of the wavelet, so that a zero crossing of the wavelet does not make the score jump. The scan does not change the data: it is a search over a grid of velocities, one stack per pair. The pick is a separate step, done by a person or an automatic picker, and it can follow the strongest peak or a smooth velocity trend.

## Example

**A hand example.** One window holds two time samples and three traces: $(1, 1, 1)$ at the first time and $(2, 2, 0)$ at the second. Then $A = 3^2 + 4^2 = 25$, $B = 3 + 8 = 11$, and $S = 25/(3 \cdot 11) = 0.758$. The first row alone gives $S = 1$, because its traces agree. A window where only one of three traces is live gives $S = 1/3$.

**A gather with two reflections.** Take 16 traces at offsets 0 to 1500 m every 100 m, $\Delta t = 4$ ms, and two reflections with a 25 Hz Ricker wavelet: amplitude 1 at $t_0 = 0.4$ s with $v = 1900$ m/s, and amplitude $-1$ at $t_0 = 0.9$ s with $v = 2600$ m/s. Add Gaussian noise with $\sigma = 0.4$ (seed 6). Scan $v$ from 1500 to 3100 m/s in steps of 50 m/s with $W = 5$:

| $v$ (m/s) | 1700 | 1800 | 1900 | 2000 | 2300 | 2500 | 2600 | 2700 | 2900 |
|---|---|---|---|---|---|---|---|---|---|
| $S$ at 0.4 s | 0.049 | 0.101 | 0.683 | 0.108 | 0.098 | 0.055 | 0.051 | 0.153 | 0.084 |
| $S$ at 0.9 s | 0.072 | 0.146 | 0.064 | 0.074 | 0.140 | 0.460 | 0.764 | 0.518 | 0.207 |

The peaks are at 1900 and 2600 m/s, the true values. The noise level $1/m = 0.0625$ is the floor of the spectrum. The peak at 0.9 s is wider in velocity, because the moveout of a deep, fast reflection changes slowly with $v$: the velocity resolution falls with depth. Without noise the peaks are 0.877 and 0.993; the first is lower because the stretch of the shallow event at far offsets makes the traces differ next to the peak.

## Correctness

By the Cauchy-Schwarz inequality, $(\sum_i a_i)^2 \le m \sum_i a_i^2$ at each time, so $0 \le S \le 1$, with $S = 1$ exactly when all traces agree at every time of the window after the moveout with $v$. One live trace gives $S = 1/m$, and for independent noise of equal variance the expected numerator over the expected denominator is $1/m$. $S$ does not change when all traces are scaled by the same factor. These are theorems about the measure. That the peak of $S$ is at the best stacking velocity is a heuristic: it holds when the event is a hyperbola with that velocity, the noise is weaker than the event, and no other event crosses the window. The proofs are in proofs/correctness.md.

## Complexity

In the real-RAM model each semblance value reads $m w$ samples, so the spectrum costs $O(n k m w)$ for $n$ times and $k$ velocities. The sums over the window can be updated in $O(m)$ as the window slides, which removes the factor $w$ when all times are scanned. The spectrum needs $O(n k)$ space. In practice it is computed on a coarse grid of midpoints, for example every 20th to 50th gather, and the velocities are interpolated in between.

## Properties

- The output is between 0 and 1 and does not depend on the overall amplitude, so spectra of different gathers and times can be compared.
- The noise floor is about $1/m$.
- Velocity resolution is a heuristic matter: it gets worse with depth (small moveout) and with a short spread (small largest offset), and better with high frequencies.
- Multiples show as peaks at lower velocities than the primaries at the same time.

## Variants and improvements

- Other coherence measures: the plain stack amplitude or power, the normalized or unnormalized cross-correlation sum (Neidell and Taner 1971 compare them).
- AB semblance and weighted semblance: they allow the amplitude to change with offset, so that a reflection whose polarity changes with offset still gives a peak.
- High-resolution spectra based on eigenvalues of the data covariance in the window, in the spirit of high-resolution array processing.
- Higher-order or anisotropic moveout: scan two parameters, the velocity and a nonhyperbolic term.
- Automatic picking along a smooth trend, by dynamic programming over the spectrum.

## When to use it

Use it to build the stacking velocity field before CMP stacking, and as the first velocity model for time migration and for the Dix conversion to interval velocities. It assumes hyperbolic moveout, so it is suited to reflections from gentle structures.

## Pitfalls

- A peak of a multiple can be picked as a primary, which gives too low a velocity. Follow the expected increase of velocity with depth.
- Velocities picked at the peak are stacking velocities. They equal rms velocities only for flat layers and small offsets, and Dix conversion amplifies their errors.
- A window much longer than the wavelet mixes events; a window much shorter makes the spectrum noisy.
- Strong amplitude decay with offset lowers the semblance of a good velocity; apply a gain first.
- The velocity grid must be fine enough to sample the peak; a step of 50 m/s on a peak a few hundred m/s wide is enough, a step of 200 m/s may miss it.

## Implementations

## History

Taner and Koehler (1969) computed velocity spectra by digital stacks along trial hyperbolas and used them to pick stacking velocities. Neidell and Taner (1971) defined semblance and compared it with the stack amplitude and the cross-correlation measures; semblance became the standard measure of velocity analysis in seismic processing.

## References
