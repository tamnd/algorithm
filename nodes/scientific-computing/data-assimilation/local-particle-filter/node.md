---
tag: 7NZNER
kind: algorithm
slug: local-particle-filter
name: Local particle filter
aliases:
- localized particle filter
area: scientific-computing/data-assimilation
level: research
summary: Weights and resamples particles at each grid point with nearby observations only, so the weights need not collapse as the state dimension grows.
solves: [data-assimilation-problem]
model: real-ram
complexity:
  vars: {n: the number of grid points, N: the number of particles, p: the number of observations, q: the largest number of observations inside the taper of one grid point}
  time: {worst: "Θ(N p + n N q)"}
  space: {extra: "Θ(N p + n N)"}
properties: {deterministic: false, gaussian_assumption: none, weights: local at each grid point, resampling: systematic with one offset u for all grid points, global_limit: "the bootstrap particle filter, for an infinite radius"}
history:
  year: 2016
  people: [Stephen G. Penny, Takemasa Miyoshi, Jonathan Poterjoy]
  note: Penny and Miyoshi gave a local particle filter with local weights and resampling at each grid point in 2016, and Poterjoy gave a localized particle filter that blends the resampled particles with the prior particles in the same year.
prereqs: [particle-filter, covariance-localization]
see_also: [particle-filter-weight-collapse, local-ensemble-transform-kalman-filter, resampling, effective-sample-size, sequential-monte-carlo, gaspari-cohn-function, curse-of-dimensionality, ensemble-kalman-filter]
sources:
  - paper: doi:10.5194/npg-23-391-2016
    title: S. G. Penny and T. Miyoshi, A local particle filter for high-dimensional geophysical systems, Nonlinear Processes in Geophysics 23 (2016) 391-405
    locator: the local weights and the resampling at each grid point
  - paper: doi:10.1175/MWR-D-15-0163.1
    title: J. Poterjoy, A localized particle filter for high-dimensional nonlinear systems, Monthly Weather Review 144(1) (2016) 59-76
    locator: the localized update that merges resampled and prior particles
  - paper: doi:10.1214/14-AAP1061
    title: P. Rebeschini and R. van Handel, Can local particle filters beat the curse of dimensionality?, Annals of Applied Probability 25(5) (2015) 2809-2866
    locator: the dimension-free error bounds of the block particle filter under decay of correlations
  - paper: doi:10.1175/2008MWR2529.1
    title: C. Snyder, T. Bengtsson, P. Bickel and J. Anderson, Obstacles to high-dimensional particle filtering, Monthly Weather Review 136(12) (2008) 4629-4640
    locator: the collapse of the global weights that motivates localization
  - paper: doi:10.1002/qj.3551
    title: P. J. van Leeuwen, H. R. Künsch, L. Nerger, R. Potthast and S. Reich, Particle filters for high-dimensional geoscience applications, a review, Quarterly Journal of the Royal Meteorological Society 145(723) (2019) 2335-2365
    locator: the survey of localized particle filters and their problems
---

A local particle filter gives each particle a separate weight at each grid point, computed only from the observations near that point, and resamples each grid point separately. The [particle filter](/particle-filter/) with global weights needs a number of particles that grows exponentially with the number of independent observations, because one particle soon takes almost all the weight (see [particle filter collapse in high dimensions](/particle-filter-weight-collapse/)). With local weights the number of observations that act on a weight is bounded by the size of the taper, so the local weights stay spread out as the state grows. The price is a localization bias, and new particles that are stitched together from parts of different old particles.

## In plain words

A particle filter keeps many guesses of the state and scores each guess by how well it fits the measurements. When there are many measurements, one guess almost always fits better than all others in total, and the filter keeps only copies of that one guess. The local filter scores each guess again for each place, with only the measurements near that place. At each place it then keeps the guesses that fit well there. A new guess can take its value at one place from one old guess and its value at another place from a different old guess, so it can fit the measurements at both places.

## The problem

**Input.** Particles $x_1, \ldots, x_N$ from the forecast, each a vector of values at $n$ grid points on a ring, and observations $(\mathrm{pos}_o, y_o, r_o)$, $o = 1, \ldots, p$: observation $o$ measures the value at grid point $\mathrm{pos}_o$ with Gaussian error of variance $r_o$. A taper $\rho$ with a radius: $\rho(0) = 1$, and $\rho(d) = 0$ for large distances $d$. Notation of Ide, Courtier, Ghil and Lorenc (1997), with $y$ for the observations.

**Output.** New particles $\tilde x_1, \ldots, \tilde x_N$, where the values at grid point $j$ are a resample of the old values at $j$ with the local weights

$$w_i(j) \propto \exp\Big(-\tfrac12\sum_{o} \rho(\mathrm{dist}(j, \mathrm{pos}_o))\,\frac{(y_o - x_{i,\mathrm{pos}_o})^2}{r_o}\Big).$$

## The algorithm

```pseudo id=main
LOCAL-PF-ANALYSIS({x_i}, {(pos_o, y_o, r_o)}, radius, u)
L1  n <- number of grid points ; N <- number of particles
L2  w_i(j) <- normalized exp(-1/2 sum_o rho(dist(j, pos_o)) (y_o - x_i[pos_o])^2 / r_o)
L3  new particles x~_1..x~_N
L4  for each grid point j
L5      a_j <- systematic resampling of w_.(j) with the points (i + u) / N
L6      for i = 1..N
L7          x~_i[j] <- x_(a_j(i))[j]
L8  return {x~_i}
```

The same offset $u$ is used at all grid points, so that neighboring points with similar weights pick the same old particles and the new particles stay smooth where the weights change slowly. In a filter cycle, each particle is first moved by a stochastic model step and the analysis step follows. The taper is the [Gaspari-Cohn function](/gaspari-cohn-function/) here; radius 0 uses only the observations at the point itself.

## Example

**Two grid points.** Take the particles $x_1 = (0, 0)$ and $x_2 = (1, 1)$, the observations $y = (1, 0)$ at the points 0 and 1 with $r = \tfrac12$, radius 0 and $u = 0.45$. At point 0 only $y_0 = 1$ acts: particle 1 has the misfit $1/\tfrac12 = 2$ and particle 2 has 0, so the weights are $w(0) = (e^{-1}, 1)/(1 + e^{-1}) = (0.269, 0.731)$. At point 1 the roles are swapped, $w(1) = (0.731, 0.269)$. The resampling points are $(0 + 0.45)/2 = 0.225$ and $(1 + 0.45)/2 = 0.725$. At point 0 they pick particles 1 and 2, because $0.225 \le 0.269 < 0.725$. At point 1 both are at most $0.731$, so both pick particle 1. The new particles are

$$\tilde x_1 = (0, 0), \qquad \tilde x_2 = (1, 0).$$

The new particle $(1, 0)$ fits both observations exactly, and neither old particle did. A global filter would give both particles the same weight, since the total misfits are equal, and could only copy whole old particles.

**Weight collapse.** The prior is $N(0, I)$ with $N = 100$ particles, and every grid point is observed with error variance 1. The table gives the mean largest weight over 10 cases, for the global weights and for the local weights with a Gaspari-Cohn taper of half-width 2 (a measurement):

| $n$ | global | local, mean over the grid points |
|---|---|---|
| 10 | 0.37 | 0.08 |
| 40 | 0.69 | 0.09 |
| 160 | 0.83 | 0.09 |

The largest global weight moves toward 1 as $n$ grows. The largest local weight does not change with $n$.

**A cycled twin.** Forty independent components follow $x_k = 0.9x_{k-1} + \eta_k$ with $\eta_k \sim N(0, 0.5)$, every component is observed with error variance 0.5 at each of 20 cycles, and $N = 50$. The root mean square error of the particle mean over the cycles 6 to 20 and 5 cases is 0.56 for the local filter with radius 0, 1.34 for the global bootstrap filter, and 0.55 for the exact [Kalman filter](/kalman-filter/) (a measurement). With no assimilation the error is about $\sqrt{0.5/0.19} = 1.62$.

## Correctness

The [proof](proofs/correctness.md) shows four facts. Systematic resampling gives each particle $\lfloor Nw_k\rfloor$ or $\lceil Nw_k\rceil$ copies, $Nw_k$ on average. The values at each grid point are a resample of the local weighted marginal. With the taper equal to 1 everywhere, the step is the global bootstrap analysis. For independent components with radius 0, the local weights are the exact importance weights of the marginal posteriors, which depend only on the local observations (all theorems). For correlated states with a taper of positive radius, the local filter is a heuristic with a bias from the localization. Rebeschini and van Handel (2015) prove dimension-free error bounds for a related block particle filter under a decay of correlations condition. The tests check the resampling against a brute force inverse of the cumulative weights, the infinite radius against a separate global bootstrap step, the local weighted mean against the Kalman filter mean, and the example.

## Complexity

The misfits of all particles to all observations cost $\Theta(Np)$. The local log weights at one grid point sum over at most $q$ observations for each particle, $\Theta(nNq)$ in total. Each systematic resampling is one pass over $N$ points and $N$ cumulative weights, $\Theta(nN)$ in total. So the time is $\Theta(Np + nNq)$ and the memory, for the misfits and the new particles, is $\Theta(Np + nN)$. Without a taper $q = p$, and the cost is $n$ times that of a global step, which computes the weights once.

## Properties

- **No Gaussian assumption.** The weights use the full likelihood, so the analysis can represent skewed and multimodal local distributions, unlike the [ensemble Kalman filter](/ensemble-kalman-filter/).
- **Local weights do not collapse with $n$.** The number of observations in a local weight is bounded by $q$, and the local largest weight stays the same as $n$ grows (a theorem for independent components, a measurement above).
- **Global limit.** With an infinite radius and one offset $u$, the step is the global bootstrap analysis (a theorem).
- **Stitched particles.** A new particle takes its values at different points from different old particles. This can break physical balances and make discontinuities where the weights change fast.
- **Localization bias.** Observations beyond the taper are ignored, even if the state is correlated over longer distances.

## Variants and improvements

- **Weight smoothing.** Penny and Miyoshi (2016) smooth the local weights over neighboring grid points to reduce the discontinuities of the stitched particles.
- **Merging with the prior.** Poterjoy (2016) updates the particles as a mix of the resampled particles and the prior particles, with a weight that goes from the resampled value at the observation to the prior value far away, and processes the observations one at a time.
- **Block particle filter.** Divide the grid into blocks and resample each block with the observations inside it, as analyzed by Rebeschini and van Handel (2015).
- **Hybrids with the LETKF.** Use a particle filter step for part of the update and the [LETKF](/local-ensemble-transform-kalman-filter/) for the rest, or a tempered sequence of local steps.
- **Optimal transport resampling.** Replace the random resampling by a deterministic map from the weighted to the equally weighted particles, which keeps the new particles closer to the old ones.

## When to use it

Use a local particle filter when the state is large, the errors are not Gaussian, and the correlations decay with distance, for example in geophysical models with strongly nonlinear observation operators. If the errors are close to Gaussian, the [LETKF](/local-ensemble-transform-kalman-filter/) is cheaper and usually more accurate with the same number of members. If the state is small, a global [particle filter](/particle-filter/) with enough particles has no localization bias.

## Pitfalls

- **A different offset at each grid point (line L5).** Then neighboring points pick unrelated particles even when their weights are equal, and the new particles are noise from point to point.
- **Weights without a shift (line L2).** The log weights can be very negative; subtract their maximum before taking exponentials, or all weights underflow to zero.
- **Too large a radius (line L2).** The local weights then see many observations and collapse like the global weights.
- **No model noise or jitter.** After resampling, many particles are equal at a grid point. Without stochastic model errors or a small jitter, the particle set loses its spread over the cycles.
- **Discontinuous new particles (line L7).** Where the weights change fast, stitched particles can violate physical balances and excite spurious waves in the next forecast; smooth the weights or merge with the prior.

## Implementations

## History

Snyder, Bengtsson, Bickel and Anderson (2008) showed that the global particle filter needs a number of particles that grows exponentially with the variance of the log likelihood, which grows with the number of observations, and so cannot work for weather models. Rebeschini and van Handel (2015) proved that a block particle filter can have errors that do not depend on the dimension under a decay of correlations condition. In 2016, Penny and Miyoshi gave a local particle filter that weights and resamples at each grid point, and Poterjoy gave a localized particle filter that merges resampled and prior particles. van Leeuwen and coworkers (2019) review these and other methods for high-dimensional geoscience problems.

## References
