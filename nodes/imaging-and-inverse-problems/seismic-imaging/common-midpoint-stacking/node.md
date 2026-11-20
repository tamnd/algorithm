---
tag: RJJQ5H
kind: algorithm
slug: common-midpoint-stacking
name: Common midpoint stacking
aliases:
- CMP stacking
area: imaging-and-inverse-problems/seismic-imaging
level: intro
summary: "Sort the traces of a survey by source-receiver midpoint, NMO-correct each gather and average it, which forms a zero-offset section and lowers random noise by the square root of the fold."
model: real-ram
complexity:
  vars: {m: the number of traces in the survey, n: the number of samples per trace}
  time: {worst: O(m n + m log m), average: O(m n + m log m), best: O(m n)}
  space: {extra: O(m n)}
properties: {deterministic: true, linear_in_data: true, needs_velocity: true, noise_gain: "sqrt(fold) for independent noise"}
history:
  year: 1962
  people: [W. Harry Mayne]
  note: Mayne described common reflection point (common-depth-point) horizontal stacking in Geophysics in 1962. Digital recording in the 1960s made it the standard way to form a seismic section.
prereqs: [normal-moveout-correction]
see_also: [semblance-velocity-analysis, seismic-reflection-model, parabolic-radon-transform, seismic-migration, kirchhoff-migration, dix-formula]
sources:
  - paper: doi:10.1190/1.1439118
    title: W. Harry Mayne, Common reflection point horizontal data stacking techniques, Geophysics 27(6), 1962, 927 to 938
    locator: the common reflection point geometry, the sum of corrected traces and its attenuation of multiples and random noise
  - book: isbn:9781560800941
    title: Oz Yilmaz, Seismic Data Analysis, Society of Exploration Geophysicists, 2001, Investigations in Geophysics 10
    locator: the chapter on velocity analysis and statics corrections (CMP sorting, fold, NMO and stacking)
  - paper: doi:10.1190/1.1440058
    title: M. Turhan Taner and Fulton Koehler, Velocity spectra, digital computer derivation and applications of velocity functions, Geophysics 34(6), 1969, 859 to 881
    locator: the stack along trial hyperbolas as a function of velocity
  - book: isbn:9780521708425
    title: Peter M. Shearer, Introduction to Seismology, 2nd edition, Cambridge University Press, 2009
    locator: Chapter 7 (reflection seismology, common midpoint stacking)
---

Common midpoint (CMP) stacking forms a seismic section from a multichannel survey. It collects the traces whose source and receiver share the same midpoint, corrects each one for its offset with [normal moveout correction](/normal-moveout-correction/), and averages them. The average is an estimate of the zero-offset trace at that midpoint, with random noise reduced and some multiples weakened. The number of traces in the average is the fold. The older name common-depth-point stacking assumes flat layers, where all traces of a midpoint reflect from the same point; with dip they do not, which is one reason for prestack [seismic migration](/seismic-migration/).

## In plain words

A survey shoots many times and records each shot on many receivers, so the same piece of ground under a surface point is seen many times, each time with a different distance between shot and receiver. Pick all the recordings whose shot and receiver are centered on that point. Correct each one for its extra travel time, so that the echoes line up. Then add them and divide by their number. The echoes are the same on every recording and stay. The random noise is different on every recording and partly cancels. Twelve recordings cut the random noise to less than a third. Echoes that bounced more than once line up less well and get weaker.

## The problem

Input: $m$ traces, each with a source position $s$, a receiver position $g$ and $n$ samples at the interval $\Delta t$; a bin width $b$; and a stacking velocity $v(t_0)$ for each bin, from [semblance velocity analysis](/semblance-velocity-analysis/). Output: for each midpoint bin, one trace $S$ at zero offset, and the fold $F_j$ of each sample. The model behind it is that after NMO every trace of the bin holds the same primary reflections $a_j$ plus noise $e_{ij}$ that is independent between traces. Under that model the stack is the average of $F_j$ independent measurements of $a_j$.

## The algorithm

```pseudo id=main
CMP-STACK(traces, Δt, v, b, s_max)
L1  bins ← group the traces by round(((s + g)/2 - origin) / b), keep x = |g - s|
L2  for each bin B in increasing order do
L3      total_j ← 0; fold_j ← 0 for every sample j
L4      for each trace (x, d) in B do
L5          (c, live) ← NMO(d, Δt, x, v_B, s_max)       ▷ live_j = 0 if muted or past the record
L6          for j ← 0 to n - 1 do if live_j then total_j ← total_j + c_j; fold_j ← fold_j + 1
L7      S_B,j ← total_j / fold_j where fold_j > 0, else 0
L8  return (S_B, fold_B) for every bin B
```

Line L1 is the CMP sort. Lines L4 to L6 correct and sum the traces of one bin, and line L7 divides by the live fold of each sample, not by the number of traces. Where the stretch mute removed the far traces, a shallow sample is the mean of fewer traces, but its amplitude is right. Line L6 counts a sample as dead when its input time falls after the end of the record, for the same reason.

## Example

**The fold.** A 2D line has a spread of $n_r = 48$ receivers every $\Delta g = 25$ m, and the shots are $\Delta s = 50$ m apart. The bin width is $\Delta g/2 = 12.5$ m. Each shot moves the 48 midpoints by $50/12.5 = 4$ bins, so a bin in the middle of the line is hit by every fourth trace position of 48, and the full fold is
$$F = \frac{n_r\,\Delta g}{2\,\Delta s} = \frac{48 \cdot 25}{2 \cdot 50} = 12.$$
Near the ends of the line the fold ramps up from 1 to 12.

**A gather.** Take 12 traces at offsets 0, 100, ..., 1100 m with $\Delta t = 4$ ms, and one reflection with a 25 Hz Ricker wavelet at $t_0 = 0.6$ s on the hyperbola with $v = 2200$ m/s. The stack at $t_0 = 0.6$ s, for several trial velocities:

| $v$ (m/s) | 1700 | 2000 | 2200 | 2400 | 3000 |
|---|---|---|---|---|---|
| stack at 0.6 s | 0.161 | 0.247 | 0.947 | 0.276 | 0.188 |

With the correct velocity the stack keeps 95 percent of the amplitude; the loss of 5 percent is the error of linear interpolation of a 25 Hz wavelet at 4 ms. A velocity 10 percent off leaves residual moveout, and the misaligned wavelets cancel. This sensitivity is what velocity analysis uses.

**The noise.** Add independent Gaussian noise with $\sigma = 0.5$ to each trace (seed 3). In a window after the event, the standard deviation is 0.485 on the zero-offset trace and 0.141 on the stack, close to $0.5/\sqrt{12} = 0.144$. The ratio of the peak to the noise rises from about 2 to about 6.7, a gain of 3.4, near $\sqrt{12} = 3.46$. This is a measurement on one seed; Claim 3 of the proof gives the expected value.

## Correctness

Line L1 puts every trace in the bin of its midpoint, and lines L3 to L7 return, at each sample, the mean of the live NMO-corrected samples of the bin. If after NMO every live sample is $a_j + e_{ij}$ with the same $a_j$ and independent noise of variance at most $\sigma^2$, the stack has mean $a_j$ and variance at most $\sigma^2/F_j$: the amplitude ratio of signal to noise grows by at least $\sqrt{F_j}$. Linear interpolation does not break the hypothesis, because it mixes samples of the same trace only and does not raise their variance. For a fixed spread rolled along the line, the full fold is $n_r \Delta g / (2 \Delta s)$ when $2\Delta s/\Delta g$ divides $n_r$. The proofs are in proofs/correctness.md.

## Complexity

In the real-RAM model, the NMO correction and the sum cost $O(n)$ per trace, so $O(m n)$ for the survey. The sort costs $O(m \log m)$ with a comparison sort and $O(m)$ expected with a hash table. The output has one trace per bin, at most $O(m n)$ numbers; a survey with fold $F$ has about $m/F$ bins. Stacking is cheap next to migration; most of the work of a stacked section is the velocity analysis that comes before it.

## Properties

- Linear in the data, for fixed velocities and mutes.
- It reduces $F$ traces to one: the stack throws away the offset dimension, and with it the information on amplitude change with offset.
- The gain of $\sqrt{F}$ in signal to noise is a theorem under the noise model of independent traces, not a property of every data set.
- Primaries flattened by NMO add in phase. Multiples have a lower stacking velocity, keep residual moveout and are attenuated, which Mayne pointed out; the attenuation depends on the offset range and is not complete.
- With dipping layers, the traces of a midpoint reflect from different points (reflection point smear).

## Variants and improvements

- Weighted stacks: weight the traces by an estimate of their noise level, or use a median or trimmed mean against bursts of noise.
- Common reflection surface and multifocusing stacks: sum along surfaces over neighboring midpoints, with more parameters than one velocity.
- Dip moveout before stacking removes the dip dependence of the stacking velocity.
- Prestack migration replaces NMO and stacking when the subsurface is complex; the stack is then formed after migration, in common image gathers.

## When to use it

Use it to get a first image of a survey with many folds and reflectors that are close to flat, and as the input of poststack [Kirchhoff migration](/kirchhoff-migration/). It is also the quality control of a velocity model: a good velocity gives a sharp stack.

## Pitfalls

- A bin with low fold, at the ends of the line or in gaps, has more noise. Do not compare amplitudes across bins with different fold without care.
- Wrong velocities lower the stack amplitude and the frequency content, even when the event is still visible.
- The divisor must be the live fold. Dividing by the number of traces makes the muted top of the section too weak.
- Coherent noise, such as ground roll, does not fall by $\sqrt{F}$. Remove it before the stack.
- Static shifts from the near surface misalign the traces just as a wrong velocity does. Correct them before the stack.

## Implementations

## History

Mayne (1962) described the common reflection point method: record each subsurface point several times with different source-receiver pairs, correct for moveout and sum. He showed that the sum attenuates multiples and random noise. The method spread with digital recording and processing in the 1960s. Taner and Koehler (1969) made the choice of the stacking velocity a computed velocity spectrum.

## References
