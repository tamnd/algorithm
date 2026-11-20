---
tag: VERVKH
kind: algorithm
slug: cadis
name: Consistent adjoint driven importance sampling
aliases:
- CADIS
area: scientific-computing/particle-transport
level: advanced
summary: Uses a deterministic adjoint solution to build a consistent biased source and weight windows for one Monte Carlo tally.
solves: [linear-boltzmann-transport-equation]
model: real-ram
complexity:
  vars: {N: the number of Monte Carlo histories, K: the mean number of flights per history, M: the number of mesh cells, A: the number of discrete directions, J: the number of source iterations of the adjoint solve}
  time: {average: O(J A M + N K)}
  space: {extra: O(A + M)}
properties: {deterministic: false, randomized: true, exact: true, iterative: true}
history:
  year: 1998
  people: [John C. Wagner, Alireza Haghighat]
  note: Wagner and Haghighat published CADIS in 1998, with the importance from a discrete ordinates adjoint solve. Haghighat and Wagner reviewed adjoint-based variance reduction in 2003.
prereqs: [adjoint-importance-function, weight-window, importance-sampling]
see_also: [fw-cadis, weight-window, adjoint-importance-function, discrete-ordinates-method, implicit-capture, particle-splitting, exponential-transform, analog-monte-carlo-transport]
sources:
  - paper: doi:10.13182/NSE98-2
    title: John C. Wagner and Alireza Haghighat, Automated variance reduction of Monte Carlo shielding calculations using the discrete ordinates adjoint function, Nuclear Science and Engineering 128(2), 1998, 186-208
    locator: the biased source q phi+ / R, the birth weights and window targets R / phi+, the window bounds from the target, and the shielding results
  - paper: doi:10.1016/S0149-1970(02)00002-1
    title: Alireza Haghighat and John C. Wagner, Monte Carlo variance reduction with deterministic importance functions, Progress in Nuclear Energy 42(1), 2003
    locator: the review of importance functions, the consistency of the source and the windows, and the zero variance argument
  - paper: doi:10.13182/NSE12-33
    title: John C. Wagner, Douglas E. Peplow and Scott W. Mosher, FW-CADIS method for global and regional variance reduction of Monte Carlo radiation transport calculations, Nuclear Science and Engineering 176(1), 2014, 37-57
    locator: the summary of CADIS for one tally before its extension to many tallies
  - book: isbn:9780849360749
    title: Ivan Lux and Laszlo Koblinger, Monte Carlo Particle Transport Methods, Neutron and Photon Calculations, CRC Press, 1991
    locator: the chapters on non-analog games and on zero variance schemes built from the importance
---

CADIS computes an approximate [importance](/adjoint-importance-function/) with a deterministic adjoint solve and uses it twice in a Monte Carlo run for one tally: to bias the source toward important places, and to set the [weight windows](/weight-window/). The word "consistent" means that source particles are born with exactly the weight that the window of their cell asks for, so the run does not split or kill them at birth. The Monte Carlo estimate stays unbiased whatever the quality of the adjoint; a good adjoint only makes the variance small, and an exact one would make it zero. John Wagner and Alireza Haghighat published the method in 1998 for shielding problems, with the adjoint from a [discrete ordinates](/discrete-ordinates-method/) code.

## In plain words

To make a Monte Carlo run for one detector fast, you need to know which particles matter. The importance map gives the answer: for each place, direction and energy, how much a particle there is expected to add to the detector.

CADIS gets a rough importance map from a cheap deterministic calculation that runs backward from the detector. Then it starts more particles where the map says they matter, with smaller weights so the average stays right. During the run, it gives every place a normal weight that is the inverse of the importance there. Heavy particles in important places are split, and light particles in unimportant places play roulette. In the ideal case every particle carries the same expected count, and the result has no noise at all.

## The problem

The model problem is one-speed transport in a slab $0 \le x \le L$ with vacuum faces, cut into $M$ cells of width $h = L/M$. The medium has the total cross section $\Sigma_t$ and the scattering cross section $\Sigma_s$, with $c = \Sigma_s/\Sigma_t$, and scattering is isotropic. The source has the density $q_i$ in cell $i$, isotropic, with $\sum_i q_i h = 1$ (one source particle). The detector has the response function $\sigma_{d,i}$, and the quantity to estimate is the response
$$R = \sum_i \sigma_{d,i} \int_{\text{cell } i} \phi(x)\, dx,$$
where $\phi$ is the scalar flux. With $\sigma_d = 1$ in the detector cells, $R$ is the expected track length of all particles of one history in the detector. A general code has a three-dimensional mesh, energy groups and a mesh of windows in space and energy, but the steps are the same.

## The algorithm

```pseudo id=main
CADIS-PARAMETERS(q, σ_d, c_u)
L1  φ⁺ ← the scalar adjoint flux of the S_N solve with the source σ_d
L2  R̂ ← Σ_i q_i φ⁺_i h                          ▷ the deterministic estimate of R
L3  p_i ← q_i φ⁺_i h / R̂ for every cell i        ▷ the biased source
L4  w̄_i ← R̂ / φ⁺_i                               ▷ the birth weight and the window target
L5  w_L,i ← 2 w̄_i / (c_u + 1), w_U,i ← c_u w_L,i

CADIS-RUN(N)
L6  for n ← 1 to N do
L7      draw cell i with probability p_i, x uniform in cell i, μ uniform on [-1, 1], put (x, μ, w̄_i) in the bank, S ← 0
L8      while the bank is not empty do take a particle (x, μ, w) in cell i from the bank, and repeat until it ends:
L9          s ← -ln(ξ) / Σ_t, d ← the distance to the edge of cell i along μ
L10         S ← S + w σ_d,i min(s, d); if s ≥ d, move to the next cell (end on leakage), else collide: w ← c w, μ ← 2ξ' - 1
L11         if w > w_U,i then k ← min(⌈w / w_U,i⌉, k_max), w ← w / k, put k - 1 copies in the bank
L12         else if w < w_L,i then w ← w̄_i with probability w / w̄_i, else the particle ends
L13     add S and S² to the sums
    return the mean of S and its standard error
```

Lines L1 to L5 are the deterministic part. Line L1 solves $L^+\phi^+ = \sigma_d$. In a one-speed slab with isotropic scattering, the scalar adjoint flux is the forward scalar flux with the source $\sigma_d$ (see the [importance](/adjoint-importance-function/) page), so the same discrete ordinates solver does both. Line L3 biases the source in proportion to the importance, and line L4 gives the birth weight $q_i h/p_i = \hat R/\phi^+_i$, which is also the center of the window. The ratio $c_u = w_U/w_L$ is usually 5.

Lines L6 to L13 are a Monte Carlo run with [implicit capture](/implicit-capture/) (line L10 multiplies the weight by $c$ instead of killing the particle) and the window check of lines L11 and L12 after every cell crossing and every collision. At a collision the new direction is sampled before the window check, so each copy that line L11 puts in the bank has the new direction. Line L13 adds the total score of the history, with all its copies.

## Example

**The parameters.** Take $L = 10$ cm, $M = 40$, $\Sigma_t = 1\ \mathrm{cm}^{-1}$, $c = 0.5$, the source uniform on $[0, 1]$ (cells 0 to 3, $q_i = 1$) and the detector on $[9, 10]$ (cells 36 to 39, $\sigma_d = 1$). An $S_{16}$ solve with diamond differences gives:

| cell | $\phi^+_i$ | target $\bar w_i$ | $w_{L,i}$ | $w_{U,i}$ |
|---|---|---|---|---|
| 0 | $4.492 \times 10^{-5}$ | 1.642 | 0.5474 | 2.737 |
| 3 | $1.062 \times 10^{-4}$ | 0.6943 | 0.2314 | 1.157 |
| 4 | $1.370 \times 10^{-4}$ | 0.5384 | 0.1795 | 0.8973 |
| 5 | $1.761 \times 10^{-4}$ | 0.4189 | 0.1396 | 0.6982 |
| 8 | $3.707 \times 10^{-4}$ | 0.1990 | 0.06634 | 0.3317 |
| 20 | $7.428 \times 10^{-3}$ | $9.932 \times 10^{-3}$ | $3.311 \times 10^{-3}$ | $1.655 \times 10^{-2}$ |
| 36 | 0.8660 | $8.519 \times 10^{-5}$ | $2.840 \times 10^{-5}$ | $1.420 \times 10^{-4}$ |

The estimate is $\hat R = 7.377 \times 10^{-5}$. The biased source probabilities of cells 0 to 3 are $0.1522, 0.2106, 0.2771, 0.3601$, so the source moves toward the detector. Check by hand: $p_0 \bar w_0 = 0.1522 \cdot 1.642 = 0.2500 = q_0 h$, the true probability of cell 0. The target falls by a factor of about 2.7 per cm, so there is one split of about 2.7 for each centimeter a particle moves toward the detector.

**One particle.** A particle born in cell 3 has the weight 0.6943. It flies to the right into cell 4, whose window is $[0.1795, 0.8973]$, so nothing happens. It collides in cell 5: implicit capture gives $0.5 \cdot 0.6943 = 0.3472$, inside $[0.1396, 0.6982]$. If it then reaches cell 8 with this weight, it is above $w_U = 0.3317$, and line L11 splits it into $\lceil 0.3472/0.3317 \rceil = 2$ copies of weight 0.1736, inside the window of cell 8. If instead it flies back into cell 2 (window $[0.3007, 1.503]$), it is still inside; a second collision there gives $0.1736 < 0.3007$, and line L12 lets it survive with probability $0.1736/0.9021 = 0.192$ with the weight 0.9021.

**Measured gain.** Runs with `random.Random(7)` and the flight count as the cost, $\mathrm{FOM} = 1/(\text{relative error}^2 \cdot \text{flights})$:

| $c$ | method | histories | mean | relative error | flights | FOM |
|---|---|---|---|---|---|---|
| 0.5 | analog | $10^5$ | $1.129 \times 10^{-4}$ | 0.345 | 418 950 | $2.0 \times 10^{-5}$ |
| 0.5 | source biasing only | $10^5$ | $1.431 \times 10^{-4}$ | 0.323 | 438 629 | $2.2 \times 10^{-5}$ |
| 0.5 | CADIS | $10^4$ | $7.677 \times 10^{-5}$ | 0.0565 | 274 045 | $1.14 \times 10^{-3}$ |
| 0.9 | analog | $10^5$ | $9.938 \times 10^{-3}$ | 0.0561 | 1 328 399 | $2.39 \times 10^{-4}$ |
| 0.9 | source biasing only | $10^5$ | $1.022 \times 10^{-2}$ | 0.0566 | 1 400 767 | $2.23 \times 10^{-4}$ |
| 0.9 | CADIS | $10^4$ | $1.137 \times 10^{-2}$ | 0.0280 | 848 244 | $1.51 \times 10^{-3}$ |

A finer reference ($M = 160$ and $S_{32}$) gives $R = 7.613 \times 10^{-5}$ for $c = 0.5$ and $0.011172$ for $c = 0.9$. The runs differ from it by 0.15 to 2.2 standard errors (the largest is the analog run for $c = 0.9$), which is a normal spread for six runs. The gain of CADIS over analog is a factor of 57 in the figure of merit for $c = 0.5$ and 6.3 for $c = 0.9$, where more particles reach the detector without help. Source biasing alone gains almost nothing here; the windows do the work. Note also that the CADIS mean agrees with the fine reference, not with the coarse estimate $\hat R = 7.377 \times 10^{-5}$: an error in the adjoint changes the variance, never the mean.

## Correctness

There are two claims, both theorems; the proofs are below.

**Unbiasedness.** If $\phi^+_i > 0$ in every cell where $q_i > 0$, and the expected number of flights per history is finite, then the expected value of $S$ is the exact response $R$ of the transport problem, for any positive $\phi^+$ at all. The biased source with the weights $q_i h/p_i$ has the same expected weight in each cell as the true source; implicit capture keeps the expected weight of each collision; the split and the roulette keep the expected weight in each cell. A martingale argument over the events of a history turns these local facts into the global one.

**Zero variance in the limit.** In a discrete model, where a particle moves between states with the probabilities $P_{ij}$ and scores at its end, the biased game with the exact importance $v$, the source $q_i v_i/R$, the transitions $P_{ij} v_j / v_i$ and the weight $R/v_i$ in state $i$ scores exactly $R$ in every history. CADIS imitates this game: its weights are $\hat R/\phi^+_i$, and the windows push each particle back toward that weight. With an approximate adjoint and windows of finite width, the variance is not zero, and the gain is a measurement, as in the table above.

## Complexity

In the [real RAM](/real-ram/) model, one source iteration of the adjoint solve costs $O(AM)$ for $A$ directions and $M$ cells, and the solve takes $J$ iterations, about $\ln(\text{tolerance})/\ln c$ without acceleration. The Monte Carlo part costs $O(NK)$ for $N$ histories with $K$ flights each, including the copies made by line L11. The windows and the source need $O(M)$ memory, and the solve needs $O(A + M)$ beyond the flux arrays. In three dimensions with $G$ energy groups the adjoint costs $O(J A M G)$ per solve, which is usually small next to the Monte Carlo time.

The cost that matters is the time to reach a given relative error. CADIS makes the variance per history smaller and the work per history different (more copies near the detector, fewer flights far from it). The product is the figure of merit, a measurement for each problem.

## Properties

- **Unbiased** for any positive adjoint, any $c_u > 1$ and any cap $k_{\max} \ge 1$.
- **Consistent.** The source particles are born at the center of their windows, so the window check at birth does nothing.
- **One tally.** The importance is for one response. Other tallies of the same run get no help and may get worse.
- **Automatic.** The user gives the source and the detector, not importances by hand.
- **Depends on the adjoint.** A coarse mesh, few directions or ray effects in the discrete ordinates adjoint lower the gain, but never bias the result.

## Variants and improvements

- **[FW-CADIS](/fw-cadis/)** weights the adjoint source by the inverse of a forward estimate, so that many tallies or a mesh tally get about the same relative error.
- **Space-energy CADIS.** With a multigroup adjoint, the windows and the biased source depend on the energy group as well, which is the form used for shielding.
- **Angle-dependent importance.** Variants use the angular adjoint flux, or the product of the forward and adjoint angular fluxes, to set windows that depend on the direction, for streaming paths and ducts.
- **Other adjoint solvers.** A diffusion or a coarse Monte Carlo adjoint is cheaper and can replace the discrete ordinates solve when the gain still pays.
- **Source biasing only, or windows only.** Each part alone is a valid unbiased game. The example shows that the windows give most of the gain in a slab.

## When to use it

Use CADIS for one detector response that analog Monte Carlo reaches with too few particles: shielding, dose behind a wall, a detector far from a source, a response in a small region. It needs a deterministic adjoint code on a mesh that covers the problem. Do not use it for many tallies at once or for a map of the flux over a large region; use FW-CADIS there. For a k-eigenvalue problem it does not apply directly, because there is no fixed source and no single detector.

## Pitfalls

- **Birth weight not equal to the target (line L4 or L7).** If source particles start with weight 1 instead of $\bar w_i$, the first window check splits or kills them at once. The mean stays right, but the time goes into the source cells. This is the inconsistency that CADIS removes.
- **Window check before the new direction (line L10 before L11).** If a collision puts copies in the bank before it samples the new direction, the copies keep the direction from before the collision, which is a scattering that did not happen. This biases the tally.
- **Zero adjoint in a cell (line L4).** Where $\phi^+_i = 0$, for example in a region that cannot reach the detector, the target is infinite. Use a floor on $\phi^+$, or a window that only plays roulette there.
- **Errors per copy (line L13).** The variance must use the total score of each history, with all its copies, not each copy alone.
- **Wrong adjoint source (line L1).** The adjoint source must be the response function $\sigma_d$ of the tally. A forward flux, or the adjoint of another detector, gives valid but poor windows.
- **Ray effects (line L1).** In two and three dimensions a discrete ordinates adjoint with few directions has streaks of high and low importance. The windows then split and kill particles along the streaks, which wastes time.

## Implementations

## History

John Wagner and Alireza Haghighat published CADIS in Nuclear Science and Engineering in 1998, with the importance from a discrete ordinates adjoint solve and the consistent biased source and windows. The use of the adjoint as an importance function was much older; the new step was to compute it automatically and to make the source and the windows agree. Haghighat and Wagner reviewed adjoint-based variance reduction in 2003, and Wagner, Peplow and Mosher extended the method in 2014 to many tallies as [FW-CADIS](/fw-cadis/).

## References
