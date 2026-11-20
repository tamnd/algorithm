---
tag: 3TP2T7
kind: algorithm
slug: normal-moveout-correction
name: Normal moveout correction
aliases:
- NMO correction
area: imaging-and-inverse-problems/seismic-imaging
level: intro
summary: "Map each sample of a trace at offset x from the time t = sqrt(t0^2 + x^2/v^2) back to its zero-offset time t0, so that reflections in a gather become flat."
model: real-ram
complexity:
  vars: {n: the number of samples per trace, m: the number of traces in the gather}
  time: {worst: O(m n), average: O(m n), best: O(m n)}
  space: {extra: O(m n)}
properties: {deterministic: true, linear_in_data: true, exact_for_one_flat_layer: true, needs_velocity: true}
history:
  year: 1955
  people: [C. Hewitt Dix]
  note: The hyperbolic moveout of a flat reflector is plain geometry. Dix (1955) related the velocity that fits the hyperbola to the rms velocity of flat layers. With common-depth-point stacking (Mayne 1962) the correction became a routine step before every stack.
prereqs: [seismic-reflection-model]
see_also: [common-midpoint-stacking, semblance-velocity-analysis, dix-formula, parabolic-radon-transform, snells-law, seismic-migration]
sources:
  - book: isbn:9781560800941
    title: Oz Yilmaz, Seismic Data Analysis, Society of Exploration Geophysicists, 2001, Investigations in Geophysics 10
    locator: the chapter on velocity analysis and statics corrections (normal moveout, NMO stretch and the stretch mute)
  - paper: doi:10.1190/1.1438126
    title: C. Hewitt Dix, Seismic velocities from surface measurements, Geophysics 20(1), 1955, 68 to 86
    locator: the hyperbolic approximation of the reflection time for flat layers and its velocity
  - paper: doi:10.1190/1.1440058
    title: M. Turhan Taner and Fulton Koehler, Velocity spectra, digital computer derivation and applications of velocity functions, Geophysics 34(6), 1969, 859 to 881
    locator: the series of the squared reflection time in powers of the squared offset, whose second coefficient is the rms velocity
  - book: isbn:9780521708425
    title: Peter M. Shearer, Introduction to Seismology, 2nd edition, Cambridge University Press, 2009
    locator: Chapter 7 (reflection seismology)
---

Normal moveout (NMO) correction removes the delay that offset adds to a reflection. In a common-midpoint gather, a flat reflector shows as a hyperbola: the farther the receiver is from the source, the later the echo comes. NMO maps every sample back to the time it would have at zero offset, so that the hyperbola becomes a flat line. It needs a velocity for each time. It is the step before [common-midpoint stacking](/common-midpoint-stacking/), and [semblance velocity analysis](/semblance-velocity-analysis/) is the scan that finds the velocity.

## In plain words

A shot sends sound down, a flat layer reflects it, and receivers at the surface record the echo. A receiver far from the shot hears the echo later than a receiver close to the shot, because the path is longer. The extra delay grows with the distance in a known way that depends on the speed of sound in the rock. NMO correction undoes that extra delay on each trace. After it, the same echo arrives at the same time on every trace, and the traces line up. The price is that the far traces get stretched in time, most of all near the top of the record, so very stretched parts are cut away.

## The problem

Input: a trace $d$ of $n$ samples $d_k = d(k\,\Delta t)$, recorded at the source-receiver offset $x$, and a velocity function $v(t_0)$ in m/s for the zero-offset two-way time $t_0$. Output: the trace $u$ with $u(t_0) = d(t(t_0))$, where
$$t(t_0) = \sqrt{t_0^2 + \frac{x^2}{v(t_0)^2}}$$
is the traveltime of the hyperbola through $t_0$. For one flat layer of constant velocity $v$ this hyperbola is the exact reflection time. For flat layers it is a second-order approximation in $x$ when $v$ is the rms velocity, and in a real earth $v$ is the stacking velocity, the velocity that best flattens the event. A gather of $m$ traces is corrected trace by trace, each with its own $x$.

## The algorithm

```pseudo id=main
NMO(d, Δt, x, v, s_max)                    ▷ s_max = stretch limit, or none
L1  for j ← 0 to n - 1 do
L2      t_0 ← j Δt
L3      t ← sqrt(t_0² + x² / v(t_0)²)       ▷ input time on the hyperbola
L4      if s_max given and t - t_0 > s_max t_0 then u_j ← 0; continue   ▷ stretch mute
L5      u_j ← linear interpolation of d at time t   ▷ 0 past the record end
L6  return u
```

The loop runs over output samples, not input samples. Each output time $t_0$ reads the input at a later time $t \ge t_0$, so the trace is pulled up toward smaller times, by more at small $t_0$ and at large $x$. Because $t$ is rarely a sample time, line L5 interpolates; linear interpolation is the cheapest choice, and sinc or spline interpolation is more accurate. Line L4 is the stretch mute: it sets to zero the samples whose relative stretch $(t - t_0)/t_0$ is above the limit. A common limit is between 0.2 and 0.5; it is a processing choice.

## Example

**The check value.** With $t_0 = 1$ s, $x = 1000$ m and $v = 2000$ m/s, line L3 gives $t = \sqrt{1 + 0.25} = 1.11803$ s. The output sample at 1 s takes the input value at 1.11803 s, a moveout of 118 ms.

**A spike that moves exactly.** Take $\Delta t = 4$ ms and a trace at $x = 800$ m with one spike of amplitude 1 at sample 125 (0.5 s), and $v = 2000$ m/s. The output sample $j = 75$ has $t_0 = 0.3$ s and $t = \sqrt{0.09 + 0.16} = 0.5$ s, which is sample 125, so the interpolation weight is zero and $u_{75} = 1$ exactly. The neighbors $j = 74$ and $76$ read times between samples 124 and 126 and pick up a part of the spike; all other output samples are zero. The spike moved up by 200 ms.

**The stretch.** For $x = 1000$ m and $v = 2000$ m/s, the stretch factor $t/t_0$ and the relative stretch $(t - t_0)/t_0$ are:

| $t_0$ (s) | $t$ (s) | $t/t_0$ | $(t - t_0)/t_0$ |
|---|---|---|---|
| 0.2 | 0.5385 | 2.693 | 1.693 |
| 0.5 | 0.7071 | 1.414 | 0.414 |
| 1.0 | 1.1180 | 1.118 | 0.118 |
| 2.0 | 2.0616 | 1.031 | 0.031 |

A 30 Hz wavelet at $t_0 = 0.5$ s comes out with a dominant frequency near $30 / 1.414 = 21$ Hz. With a stretch limit of 0.3, line L4 mutes the samples of this trace with $t_0$ below about 0.6 s and keeps the later ones.

**Two layers.** A layer 400 m thick with 2000 m/s lies over a layer 600 m thick with 3000 m/s. Each layer takes 0.4 s of two-way time, so $t_0 = 0.8$ s and the rms velocity is $V = \sqrt{(0.4 \cdot 2000^2 + 0.4 \cdot 3000^2)/0.8} = 2549.5$ m/s. Exact ray tracing through the two layers against the hyperbola with $V$ gives:

| $x$ (m) | exact $t$ (s) | hyperbola (s) | difference (ms) |
|---|---|---|---|
| 500 | 0.82364 | 0.82369 | -0.05 |
| 1000 | 0.89024 | 0.89098 | -0.74 |
| 2000 | 1.11199 | 1.12044 | -8.45 |

At small offsets the hyperbola is very close. At 2000 m it is 8 ms late, a quarter of a period at 30 Hz, and the event is no longer flat after NMO. This is the residual moveout of the next sections.

## Correctness

For one flat layer the reflection time is $\sqrt{t_0^2 + x^2/v^2}$ by Pythagoras. The map $t_0 \mapsto t(t_0)$ is strictly increasing, so an event on the hyperbola through $\tau$ comes out with its peak at $t_0 = \tau$ on every trace: the event is flat. Near $t_0$ the output is the input stretched by $t/t_0$, because $dt/dt_0 = t_0/t$. Linear interpolation adds an error of at most $\Delta t^2 \max|d''|/8$. For flat layers, the ray parameter gives $t^2 = t_0^2 + x^2/V^2 + O(x^4)$ with the rms velocity $V$, and the $x^4$ term is negative unless all layer velocities are equal. The proofs are in proofs/correctness.md.

## Complexity

Each output sample costs a square root, a test and an interpolation, so a trace costs $O(n)$ and a gather of $m$ traces costs $O(m n)$ in the real-RAM model. The output needs $O(n)$ space per trace. A sinc interpolator of length $L$ raises the cost to $O(m n L)$.

## Properties

- Linear in the data: the correction of a sum of traces is the sum of the corrections.
- Not invertible in general: the stretch mute throws samples away, and at the top of a far trace many input samples map into few output samples.
- Exact for one flat layer of constant velocity. For flat layers it is a second-order approximation in offset (a theorem, Claim 5 of the proof). For one dipping layer of constant velocity the best fitting velocity is $v / \cos\phi$ with the dip $\phi$, so a dipping event and a flat event at the same time need different velocities; the correction for dip is a separate step (dip moveout).
- The stretch is $t/t_0$, largest at shallow times and far offsets.

## Variants and improvements

- Higher-order moveout: add a term in $x^4$ to the hyperbola, as in the series of Taner and Koehler, to correct far offsets in layered media.
- Anisotropic moveout: a nonhyperbolic term with an anellipticity parameter for transversely isotropic layers.
- Stretch-free NMO: methods that shift whole wavelets instead of single samples, to avoid the loss of frequency at far offsets.
- Inverse NMO: put the hyperbolic moveout back, for example after a [parabolic Radon transform](/parabolic-radon-transform/) removed the multiples.

## When to use it

Use it on common-midpoint gathers before stacking and before velocity analysis by stacking, when the reflectors are close to flat and the velocity changes mainly with depth. For strong dips or strong lateral velocity changes, prestack [seismic migration](/seismic-migration/) replaces NMO and stacking.

## Pitfalls

- A wrong velocity leaves residual moveout: too low a velocity over-corrects (the event curves up at far offsets), too high a velocity under-corrects.
- Without a stretch mute, the shallow far-offset part of the stack is dominated by stretched, low-frequency noise. The mute limit is a heuristic choice.
- Multiples have a lower stacking velocity than primaries at the same time. After NMO with the primary velocity they remain curved; this difference is what the parabolic Radon transform uses.
- Linear interpolation of a signal close to the Nyquist frequency smooths it. Use a longer interpolator for high-frequency data.
- The velocity $v$ of NMO is the stacking velocity, not the interval velocity of a layer. The [Dix formula](/dix-formula/) converts rms velocities to interval velocities.

## Implementations

## History

The hyperbola of a flat reflector follows from the geometry of one layer. Dix (1955) showed that for flat layers and small offsets the reflection time fits a hyperbola whose velocity is the rms velocity of the layers above, and used it to get interval velocities. Mayne (1962) described common-depth-point stacking, in which every trace is NMO-corrected and then summed. Taner and Koehler (1969) wrote the squared reflection time as a series in the squared offset and made the scan over velocities a routine computer step.

## References
