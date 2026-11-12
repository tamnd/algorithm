---
tag: Y968MV
kind: algorithm
slug: delta-tracking
name: Delta tracking
aliases: [Woodcock tracking]
area: graphics-and-signals/ray-tracing
level: advanced
summary: Sample the distance to the next real collision in a heterogeneous medium. Take exponential steps at a constant majorant rate and accept each step with probability sigma_t / majorant.
model: real-ram
complexity:
  vars: {m: "the majorant times the segment length", n: the number of samples}
  time: {per_sample: "O(1 + m) expected", estimate: "O(n(1 + m)) expected"}
  space: {extra: O(1)}
properties: {deterministic: false, randomized: true, recursive: false, exact: true}
history:
  year: 1965
  people: [E. R. Woodcock, T. Murphy, P. J. Hemmings, T. C. Longworth]
  note: Woodcock and his colleagues used fictitious collisions to track neutrons through reactors of complex geometry in the GEM code. Coleman proved the method exact in 1968.
prereqs: [participating-media, inverse-transform-sampling, rejection-sampling]
see_also: [volumetric-path-tracing, monte-carlo-integration, ray-marching, poisson-distribution, russian-roulette, next-event-estimation]
sources:
  - title: E. R. Woodcock, T. Murphy, P. J. Hemmings and T. C. Longworth, Techniques used in the GEM code for Monte Carlo neutronics calculations in reactors and other systems of complex geometry, Proceedings of the Conference on the Application of Computing Methods to Reactor Problems, Argonne National Laboratory report ANL-7050, 1965
    locator: the tracking of a particle with a fictitious cross section that makes the total cross section constant in all regions
  - paper: doi:10.13182/NSE68-1
    title: W. A. Coleman, Mathematical verification of a certain Monte Carlo sampling technique and applications of the technique to radiation transport problems, Nuclear Science and Engineering 32(1), 1968, 76 to 81
    locator: the proof that sampling with a majorant and rejecting fictitious collisions gives the exact free-flight distribution
  - paper: doi:10.1111/cgf.13383
    title: Jan Novák, Iliyan Georgiev, Johannes Hanika and Wojciech Jarosz, Monte Carlo methods for volumetric light transport simulation, Computer Graphics Forum 37(2), 2018, 551 to 576
    locator: the sections on null-collision (tracking) estimators of free-flight distance and of transmittance, including delta tracking and ratio tracking
  - url: https://pbr-book.org/4ed/Volume_Scattering/Transmittance
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, fourth edition, MIT Press, 2023
    locator: Section 11.2 Transmittance and Section 11.2.1 Null Scattering (the majorant, the null coefficient, delta tracking and ratio tracking)
---

Delta tracking samples the distance to the next real collision of a ray in a [participating medium](/participating-media/) whose extinction coefficient $\sigma_t(t)$ changes along the ray. It takes exponential steps with a constant rate $\mu \ge \sigma_t$, called the majorant, and at each step it accepts a real collision with probability $\sigma_t(t)/\mu$. The other steps are *null collisions*, and the walk goes on from them. The distance it returns has exactly the density $\sigma_t(t)\,e^{-\int_0^t \sigma_t}$, so the method is unbiased, with no step size and no quadrature. It is the free-flight sampler of most [volumetric path tracers](/volumetric-path-tracing/).

## In plain words

Light that goes through smoke or a cloud can hit a particle at any point. Where the smoke is thick, a hit is more likely. We want to pick the point of the first hit at random, with the correct chance for each point.

This is easy if the smoke has the same thickness everywhere. Delta tracking makes it easy for any smoke. It pretends that the smoke is as thick as its thickest part, everywhere. It picks a hit point for this thick, even smoke. Then it asks: is the real smoke at this point as thick as the pretend smoke? It accepts the hit with a chance equal to the ratio of the two. If it does not accept, the hit is a fake one, and the walk starts again from that point. The accepted hits fall exactly where real hits fall.

## The problem

A ray $x(t) = o + t\,\omega$ goes through a medium on the segment $0 \le t < s$. The extinction coefficient $\sigma_t(t) = \sigma_t(x(t)) \ge 0$ is known at each point. The optical depth to $t$ is $\tau(t) = \int_0^t \sigma_t(u)\,du$, and the transmittance is $T(t) = e^{-\tau(t)}$. The free-flight distance is the random distance $X$ with

$$P(X > t) = T(t), \qquad p(t) = \sigma_t(t)\,T(t) \quad \text{for } 0 \le t < s,$$

and with $P(X \ge s) = T(s)$, the probability that the ray leaves the segment with no collision. The task is to draw samples of $X$, and to estimate $T(s)$, given a number $\mu$ with $\sigma_t(t) \le \mu$ on the segment.

[Inverse transform sampling](/inverse-transform-sampling/) solves $\tau(X) = -\ln(1 - \xi)$ for $X$. That needs $\tau$ in closed form, or a numeric integral along the ray, which [ray marching](/ray-marching/) gives only with a bias that depends on the step.

## The algorithm

Each $\xi$ and $\xi'$ is a new uniform random number in $[0, 1)$.

```pseudo id=main
DELTA-TRACKING(σt, μ, s)                  ▷ needs 0 ≤ σt(t) ≤ μ on [0, s)
L1  t ← 0
L2  loop
L3      t ← t − ln(1 − ξ) / μ             ▷ exponential step with rate μ
L4      if t ≥ s then return ESCAPE
L5      draw ξ′
L6      if ξ′ · μ < σt(t) then return t   ▷ real collision, probability σt(t)/μ
L7      ▷ null collision: go on from t

RATIO-TRACKING(σt, μ, s)                  ▷ an estimate of T(s)
L8  t ← 0, w ← 1
L9  loop
L10     t ← t − ln(1 − ξ) / μ
L11     if t ≥ s then return w
L12     w ← w · (1 − σt(t) / μ)
```

A sample of $T(s)$ from delta tracking is the indicator of ESCAPE. It is 1 or 0. This is the *track-length* estimator. Ratio tracking does not stop at a collision. It visits each tentative collision on the segment and multiplies the weight by the probability $1 - \sigma_t/\mu$ of a null collision there. The difference $\sigma_n = \mu - \sigma_t \ge 0$ is the coefficient of the null medium, a fictitious medium that scatters straight forward and so does not change the light.

## Example

Take $\sigma_t(t) = 0.5 + 1.5 \sin^2(2t)$ on the segment $0 \le t < 1.3$, and the tight majorant $\mu = 2$. The optical depth has the closed form $\tau(t) = 0.5t + 1.5\,(t/2 - \sin(4t)/8)$, so $\tau(1.3) = 1.79065$ and $T(1.3) = 0.166852$.

One walk, with seed 3 of Python's `random.Random`:

| step | $\xi$ | $t$ | $\sigma_t(t)$ | $\sigma_t/\mu$ | $\xi'$ | result |
|---|---|---|---|---|---|---|
| 1 | 0.238 | 0.136 | 0.608 | 0.304 | 0.544 | null |
| 2 | 0.370 | 0.367 | 1.173 | 0.586 | 0.604 | null |
| 3 | 0.626 | 0.858 | 1.968 | 0.984 | 0.066 | real, return 0.858 |

With seed 2 the first step is $t = -\ln(1 - 0.956)/2 = 1.562 \ge 1.3$, so the walk returns ESCAPE and the track-length sample is 1.

The mean of $n$ samples, with its standard error, from seed 1:

| $n$ | delta tracking | ratio tracking |
|---|---|---|
| 100 | 0.130 ± 0.034 | 0.155 ± 0.028 |
| 1000 | 0.172 ± 0.012 | 0.1707 ± 0.0093 |
| 10000 | 0.1673 ± 0.0037 | 0.1682 ± 0.0029 |
| 100000 | 0.1689 ± 0.0012 | 0.16756 ± 0.00092 |

Both converge to 0.166852 at the rate $n^{-1/2}$. The variance of one track-length sample is $T(1 - T) = 0.1390$. The variance of one ratio tracking sample is 0.0840 with $\mu = 2$ and 0.0164 with $\mu = 6$. The expected number of tentative collisions of delta tracking is 1.379 with $\mu = 2$ and 4.136 with $\mu = 6$.

## Correctness

The tentative collisions of lines L3 and L4 are the points of a Poisson process of rate $\mu$ on the segment, because the gaps are independent exponential numbers with rate $\mu$. Line L6 keeps each point with probability $\sigma_t(t)/\mu$, independently. A thinned Poisson process of this kind is a Poisson process with the rate $\sigma_t(t)$, and delta tracking returns its first point. The first point of a Poisson process of rate $\sigma_t$ is past $t$ with probability $e^{-\int_0^t \sigma_t} = T(t)$, which is the free-flight law. The proof in the proof file does not use this fact. It writes the escape probability from a point $x$ as a Volterra integral equation, shows that $e^{-\int_x^s \sigma_t}$ solves it, and shows that the solution is unique. For ratio tracking, the expected product over a Poisson process of rate $\mu$ is $e^{-\mu s}\sum_k (\int_0^s (\mu - \sigma_t))^k / k! = e^{-\int_0^s \sigma_t}$. So both estimators of $T(s)$ are unbiased.

## Complexity

Delta tracking examines a tentative collision at $t$ only if it has not yet stopped, so the expected number of evaluations of $\sigma_t$ is

$$\int_0^s \mu\, T(t)\, dt \le \mu s.$$

In the example this is 1.379 for $\mu = 2$. Ratio tracking examines all tentative collisions on the segment, $\mu s$ of them on average. Each step costs $O(1)$ plus one evaluation of $\sigma_t$, so a sample costs $O(1 + \mu s)$ expected time and $O(1)$ space. The number of steps is random with no worst case bound.

With $n$ independent samples the estimate of $T(s)$ has the variance $v/n$ and the standard error $O(n^{-1/2})$, with

$$v_{\text{track}} = T(1 - T), \qquad v_{\text{ratio}} = e^{-\int_0^s (2\sigma_t - \sigma_t^2/\mu)} - T^2 \le T(1 - T).$$

The bound holds because the ratio tracking weight is in $[0, 1]$, so its second moment is at most its mean $T$. A larger $\mu$ lowers $v_{\text{ratio}}$ toward 0, but it increases the number of steps in proportion.

## Properties

- **Unbiased.** Each returned distance has exactly the free-flight law, for any majorant $\mu \ge \max \sigma_t$. There is no step size and no discretization error.
- **Needs only point values.** The method evaluates $\sigma_t$ at points. It never integrates $\sigma_t$. So it works for procedural media and for grids of any resolution.
- **Randomized running time.** The work per sample is random. A loose majorant gives many null collisions.
- **Binary transmittance.** The track-length estimate is 0 or 1. Ratio tracking gives a real value in $[0, 1]$ with a variance that is never larger.

## Variants and improvements

- **Ratio tracking.** Lines L8 to L12. Use it for the transmittance of a shadow ray, where a binary estimate is noisy.
- **Residual ratio tracking.** Split $\sigma_t$ into a known control part $\sigma_c$, whose transmittance is analytic, and a residual. Track only the residual. Novák, Selle and Jarosz described it in 2014.
- **Local majorants.** Store a majorant for each cell of a coarse grid and walk the grid with [Amanatides-Woo traversal](/amanatides-woo-traversal/), so that the majorant stays tight. PBRT does this with a majorant grid.
- **Spectral and decomposition tracking.** When $\sigma_t$ depends on the wavelength, one walk with a majorant over all wavelengths can serve several wavelengths with weights. Kutz and others described these methods in 2017.
- **Weighted delta tracking.** A majorant that is smaller than $\sigma_t$ at some points is possible if the walk carries a signed weight instead of a strict accept or reject. The weights can then be negative.

## When to use it

Use delta tracking to sample the next scattering event in a heterogeneous medium, for example in a [volumetric path tracer](/volumetric-path-tracing/). Use ratio tracking for transmittance along a connection to a light, as in [next event estimation](/next-event-estimation/). If $\sigma_t$ is constant along the ray, sample the exponential law directly. If the optical depth has a closed form, invert it. Use ray marching only when a small bias is acceptable and the medium is smooth.

## Pitfalls

- **A majorant that is too small.** If $\sigma_t(t) > \mu$ at a point, line L6 accepts with probability 1 there instead of $\sigma_t/\mu > 1$. The walk then samples the medium $\min(\sigma_t, \mu)$, and the transmittance is too high. Compute the majorant from the data, for example the maximum over each grid cell, and include the interpolation.
- **A majorant that is too large.** It stays unbiased, but each sample takes more steps. In the example, $\mu = 6$ takes three times as many steps as $\mu = 2$.
- **$\ln 0$.** If $\xi$ can be 0, write the step as $-\ln(1 - \xi)/\mu$, because $1 - \xi > 0$.
- **Reuse of one random number.** The accept test of line L6 needs a new $\xi'$. A test that reuses $\xi$ from line L3 couples the step and the decision, and the result is biased.
- **A spectral $\sigma_t$ with one sampled wavelength and a gray majorant.** Each wavelength needs its own acceptance probability, or a weight as in spectral tracking.

## Implementations

## History

Woodcock, Murphy, Hemmings and Longworth described the method in 1965 for the GEM code of the United Kingdom Atomic Energy Authority, at a conference at Argonne National Laboratory. They added a fictitious cross section in each region of a reactor so that the total cross section was the same everywhere, and tracked neutrons through the complex geometry without computing the distance to each boundary. Coleman gave the mathematical proof in 1968. Graphics took up the method for heterogeneous media in the 2000s and 2010s, and the survey of Novák, Georgiev, Hanika and Jarosz in 2018 puts delta tracking, ratio tracking and their variants in one framework of null collisions.

## References
