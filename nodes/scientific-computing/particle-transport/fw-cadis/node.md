---
tag: GNWTPH
kind: algorithm
slug: fw-cadis
name: Forward-weighted CADIS
aliases:
- FW-CADIS
area: scientific-computing/particle-transport
level: research
summary: Weights the adjoint source by the inverse forward flux, so variance reduction gives a uniform relative error over a mesh tally.
solves: [linear-boltzmann-transport-equation]
model: real-ram
complexity:
  vars: {N: the number of Monte Carlo histories, K: the mean number of flights per history, B: the number of tally bins, M: the number of mesh cells, A: the number of discrete directions, J: the number of source iterations of one deterministic solve}
  time: {average: O(J A M + N (K + B))}
  space: {extra: O(A + M + B)}
properties: {deterministic: false, randomized: true, exact: true, iterative: true}
history:
  year: 2014
  people: [John C. Wagner, Douglas E. Peplow, Scott W. Mosher]
  note: Wagner, Peplow and Mosher described FW-CADIS for global and regional variance reduction in Nuclear Science and Engineering in 2014, as an extension of CADIS to many tallies.
prereqs: [cadis]
see_also: [cadis, weight-window, adjoint-importance-function, discrete-ordinates-method, track-length-estimator, implicit-capture, particle-splitting, analog-monte-carlo-transport]
sources:
  - paper: doi:10.13182/NSE12-33
    title: John C. Wagner, Douglas E. Peplow and Scott W. Mosher, FW-CADIS method for global and regional variance reduction of Monte Carlo radiation transport calculations, Nuclear Science and Engineering 176(1), 2014, 37-57
    locator: the adjoint source weighted by the inverse forward response, the argument for a uniform density of Monte Carlo particles, and the test problems
  - paper: doi:10.13182/NSE98-2
    title: John C. Wagner and Alireza Haghighat, Automated variance reduction of Monte Carlo shielding calculations using the discrete ordinates adjoint function, Nuclear Science and Engineering 128(2), 1998, 186-208
    locator: CADIS, the biased source and the weight windows that FW-CADIS reuses
  - paper: doi:10.1016/S0149-1970(02)00002-1
    title: Alireza Haghighat and John C. Wagner, Monte Carlo variance reduction with deterministic importance functions, Progress in Nuclear Energy 42(1), 2003
    locator: the review of importance functions and of the contributon density
---

FW-CADIS is [CADIS](/cadis/) for many tallies at once: a mesh tally over a large region, or a set of detectors with very different responses. CADIS makes one tally good and can leave the others with no score at all. FW-CADIS first runs a deterministic forward solve to estimate every tally, then sets the adjoint source of each tally to the inverse of its estimate, so that every tally counts with the same relative weight in the importance. The rest is CADIS: a biased source and [weight windows](/weight-window/) from the adjoint flux. The goal is about the same relative error in every bin. John Wagner, Douglas Peplow and Scott Mosher described the method in 2014.

## In plain words

Suppose you want a map of the radiation in a whole building, not one number at one detector. Near the source the map is easy, because many particles go there. Far away, almost no particles arrive, and the map there is pure noise.

CADIS can make one far spot good, but it does so by sending particles toward that spot only. FW-CADIS first makes a cheap rough map. Then it tells the importance calculation: a place where the rough map is small needs more help, so give it a large weight. Particles are then pushed toward the weak places as much as toward the strong ones, and every part of the map gets about the same accuracy.

## The problem

The model problem is the slab of the CADIS page: one-speed transport in $0 \le x \le L$ with vacuum faces, $M$ cells of width $h = L/M$, total cross section $\Sigma_t$, scattering ratio $c$, isotropic scattering, and a source $q_i$ with $\sum_i q_i h = 1$. The tally is a mesh of $B$ equal bins, each made of $M/B$ cells, and the quantity in bin $j$ is
$$T_j = \int_{\text{bin } j} \phi(x)\, dx,$$
the expected track length per source particle in the bin. The goal is to estimate all $T_j$ with relative errors $\varepsilon_j = \sigma_j/T_j$ that are about equal, or equivalently to make the largest $\varepsilon_j$ small for a given amount of work. The $T_j$ can differ by many orders of magnitude.

## The algorithm

```pseudo id=main
FW-CADIS-PARAMETERS(q, B, c_u)
L1  φ ← the scalar flux of the forward S_N solve with the source q
L2  q⁺_i ← 1 / T̂_j(i), where T̂_j = Σ_{i in bin j} φ_i h and j(i) is the bin of cell i
L3  φ⁺ ← the scalar adjoint flux of the S_N solve with the source q⁺
L4  R̂ ← Σ_i q_i φ⁺_i h, and p_i ← q_i φ⁺_i h / R̂
L5  w̄_i ← R̂ / φ⁺_i, w_L,i ← 2 w̄_i / (c_u + 1), w_U,i ← c_u w_L,i

FW-CADIS-RUN(N)
L6  for n ← 1 to N do run one history of CADIS-RUN, lines L7 to L12 of the CADIS page, with these parameters
L7      during the history, add w times the track length in each cell to the score S_j of its bin j
L8      add each S_j and S_j² to the sums of bin j
    return the mean of S_j and its standard error for every bin j
```

Line L1 is the only new solve. Line L2 is the forward weighting: the adjoint source of bin $j$ is the inverse of its deterministic estimate, so the adjoint problem asks for the importance of a particle for the sum $\sum_j T_j/\hat T_j$ of relative tallies. Lines L3 to L5 are lines L1 to L5 of CADIS with this source. Lines L6 to L8 are the CADIS Monte Carlo run with a score for each bin. In a slab with isotropic scattering both solves are forward solves of the same code, as in CADIS.

## Example

Take $L = 16$ cm, $M = 64$, $B = 16$ bins of 1 cm, $\Sigma_t = 1\ \mathrm{cm}^{-1}$, $c = 0.5$, and a source uniform on $[7.5, 8.5]$, in the middle of the slab. An $S_{16}$ forward solve gives the bin estimates
$$\hat T_1, \ldots, \hat T_8 = 3.408 \times 10^{-4},\ 9.636 \times 10^{-4},\ 2.624 \times 10^{-3},\ 7.193 \times 10^{-3},\ 0.02007,\ 0.05788,\ 0.1809,\ 0.7298,$$
and the bins 9 to 16 are the mirror image. The center bins have more than 2000 times the flux of the end bins.

**The response by hand.** The adjoint source is $1/\hat T_j$ in bin $j$. By reciprocity, $\hat R = \langle q, \phi^+ \rangle = \langle q^+, \phi \rangle = \sum_j (1/\hat T_j) \cdot \hat T_j = B = 16$. The solver gives $15.999999999$. So in FW-CADIS the estimated response is always the number of bins, and each bin adds exactly 1 to it.

**The parameters.** The scalar adjoint flux is $2556$ in the end cells and $15.6$ to $16.5$ in the source cells, so the importance is 160 times larger at the faces than at the source. The birth weights in the four source cells are $0.972, 1.029, 1.029, 0.972$, with biased probabilities $0.257, 0.243, 0.243, 0.257$: the source changes little, and the windows do the work of pushing particles outward. The target weight in the end cells is $0.00626$.

**Measured errors.** Runs with `random.Random(5)` give the relative errors of six bins, the ratio of the largest to the smallest relative error over all 16 bins, and the figure of merit of the worst bin, $1/(\varepsilon_{\max}^2 \cdot \text{flights})$:

| method | histories | flights | $\varepsilon_1$ | $\varepsilon_4$ | $\varepsilon_8$ | $\varepsilon_9$ | $\varepsilon_{13}$ | $\varepsilon_{16}$ | $\max/\min$ | worst-bin FOM |
|---|---|---|---|---|---|---|---|---|---|---|
| analog | $10^5$ | 604 242 | 0.251 | 0.048 | 0.004 | 0.004 | 0.048 | 0.206 | 60.5 | $2.6 \times 10^{-5}$ |
| CADIS for bin 16 | $10^4$ | 260 217 | no score | 0.786 | 0.016 | 0.011 | 0.038 | 0.050 | none | none |
| FW-CADIS | $10^4$ | 171 415 | 0.084 | 0.051 | 0.011 | 0.011 | 0.053 | 0.082 | 7.4 | $8.3 \times 10^{-4}$ |

CADIS for the last bin makes that bin good and the bins on the other side bad; three of the left bins get no score at all in this run. FW-CADIS gives both end bins about the same error, the ratio of the largest to the smallest error falls from 60.5 to 7.4, and the worst bin has a figure of merit 32 times the analog one. These are measurements on one toy problem. The errors are not fully uniform: the product $\phi\phi^+$ integrated over a bin, which is the expected density of Monte Carlo tracks in the ideal case, runs from $1.08$ in the end bins to $12.5$ in the center bins, because the adjoint of a slab with leakage cannot follow $1/\phi$ exactly.

## Correctness

**Unbiasedness.** This is a theorem: the Monte Carlo part is CADIS with another positive adjoint, so the proof of [CADIS](/cadis/) applies to the score of every bin. The mean of each $S_j$ is the exact $T_j$, whatever the errors of the forward and adjoint solves. The proof is below.

**The response is $B$.** This is a theorem about the deterministic part: with $q^+ = 1/\hat T_j$ on bin $j$, the discrete reciprocity $\langle q, \phi^+ \rangle = \langle q^+, \phi \rangle$ of the solver gives $\hat R = B$.

**Why the errors become uniform.** This is a heuristic, the one of Wagner, Peplow and Mosher. If each particle at a point $P$ carried exactly the target weight $\hat R/\phi^+(P)$, the expected density of Monte Carlo tracks at $P$ would be the physical flux divided by the weight, $\phi(P)\phi^+(P)/\hat R$. A relative error that is the same in every bin needs about the same number of tracks in every bin, so $\phi\phi^+$ should be about constant over the tally region. The forward weighting of the adjoint source is a cheap way to come close to this: where $\phi$ is small, the adjoint source $1/\phi$ is large. The example shows that the result is closer to uniform than analog play or CADIS, but not uniform.

## Complexity

In the [real RAM](/real-ram/) model, the two deterministic solves cost $O(JAM)$ each, with $J$ source iterations, $A$ directions and $M$ cells. The Monte Carlo run costs $O(NK)$ for the flights and $O(NB)$ for the sums of line L8, so $O(N(K + B))$ in all. A code that keeps a list of the bins a history touched pays only for those. The memory is $O(M)$ for the windows and the fluxes, $O(B)$ for the sums, and $O(A)$ for the angular sweep. As for CADIS, the time to a given worst-bin error is a measurement.

## Properties

- **Unbiased** in every bin, for any positive forward and adjoint estimates.
- **One run for many tallies.** All bins come from one run with one set of windows.
- **Balanced, not optimal.** The method aims at a uniform relative error. It does not minimize a stated error measure, and it can give a worse error than CADIS for the one bin that CADIS was made for.
- **Two deterministic solves.** The forward solve is extra work, usually small next to the Monte Carlo run.

## Variants and improvements

- **Response-weighted tallies.** For a dose or a reaction rate with the response function $\sigma_d(E)$, the adjoint source is $\sigma_d / \int \sigma_d \phi$, the response function divided by the forward estimate of the response.
- **A few detectors.** For a set of point or region tallies, the adjoint source is the sum of their response functions, each divided by its forward estimate.
- **A tally over the whole problem.** For a global flux map, $q^+ = 1/\phi$ in every cell.
- **Iterative forward methods.** Other methods set the windows from the flux map of a previous Monte Carlo run instead of a deterministic adjoint, and repeat; they reach a similar goal without a deterministic code.

## When to use it

Use FW-CADIS when a single run must give a map of the flux or the dose over a large region, or several tallies with very different values, for example a dose map in a building around a reactor or an accelerator. Use plain [CADIS](/cadis/) when one tally matters, and analog or lightly biased play when all tallies are close to the source.

## Pitfalls

- **A zero or tiny forward estimate (line L2).** A bin that the forward solve gives as almost zero gets an enormous adjoint source, and the windows then send the run into that bin. Put a floor on $\hat T_j$, or leave bins outside the region of interest out of the adjoint source.
- **The adjoint source cell by cell (line L2).** Using $1/\phi_i$ in each cell instead of $1/\hat T_j$ for the bin weights the cells of a bin in a different way from the tally; for a bin with a steep flux inside it, the importance then favors the low-flux edge of the bin.
- **An inaccurate forward solve (line L1).** Ray effects or a coarse mesh in the forward solve put the wrong weights on bins. The mean stays right, but the errors are no longer balanced.
- **Errors per copy (line L8).** The variance of each bin must use the total score of the history in that bin, with all its copies.
- **Sums for every bin of every history (line L8).** With a large mesh, adding $B$ numbers per history costs more than the flights. Keep the list of bins that the history touched.

## Implementations

## History

Wagner, Peplow and Mosher described FW-CADIS in Nuclear Science and Engineering in 2014, for "global" problems (a flux map over the whole geometry) and "regional" problems (several tallies), as an extension of the [CADIS](/cadis/) method of Wagner and Haghighat (1998). The paper gives the argument that a uniform density of Monte Carlo particles over the tally region gives uniform relative errors, and the forward weighting of the adjoint source as a way to reach it.

## References
