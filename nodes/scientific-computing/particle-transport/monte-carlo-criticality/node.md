---
tag: 1ER0M9
kind: algorithm
slug: monte-carlo-criticality
name: Monte Carlo criticality calculation
aliases:
- Monte Carlo power iteration
area: scientific-computing/particle-transport
level: core
summary: Finds k_eff by tracking generations of fission neutrons, using the fission sites of each generation as the source of the next.
solves: [k-eigenvalue-problem]
model: real-ram
complexity:
  vars: {N: the number of neutrons per cycle, G: the number of cycles, K: the mean number of collisions per neutron}
  time: {average: O(G N K)}
  space: {extra: O(N K)}
properties: {deterministic: false, randomized: true, exact: false, iterative: true}
history:
  year: 1968
  people: [J. Lieberoth]
  note: Lieberoth described the generation method with a fixed number of neutrons per cycle and studied its source convergence in Nukleonik in 1968; the method was in use in reactor codes before that.
prereqs: [k-eigenvalue-problem, analog-monte-carlo-transport, power-iteration]
see_also: [k-eigenvalue-problem, fission-source-entropy, power-iteration, analog-monte-carlo-transport, resampling, mcmc-autocorrelation, effective-sample-size, adjoint-importance-function]
sources:
  - paper: "J. Lieberoth, A Monte Carlo technique to solve the static eigenvalue problem of the Boltzmann transport equation, Nukleonik 11, 1968, 213"
    locator: the generation method with a fixed number of source neutrons and the convergence of the fission source
  - paper: doi:10.1016/0306-4549(86)90095-2
    title: R. J. Brissenden and A. R. Garlick, Biases in the estimation of Keff and its error by Monte Carlo methods, Annals of Nuclear Energy 13(2), 1986, 63-83
    locator: the bias of k of order 1/N from the normalization of each generation, and the bias of the error estimate from the correlation between generations
  - paper: "Taro Ueki, Forrest B. Brown, D. Kent Parsons and Drew E. Kornreich, Autocorrelation and dominance ratio in Monte Carlo criticality calculations, Nuclear Science and Engineering 145, 2003, 279"
    locator: the correlation between cycles and its relation to the dominance ratio
  - book: isbn:9780849360749
    title: Ivan Lux and Laszlo Koblinger, Monte Carlo Particle Transport Methods, Neutron and Photon Calculations, CRC Press, 1991
    locator: the chapter on the Monte Carlo solution of eigenvalue problems
  - book: isbn:9780486462936
    title: Jerome Spanier and Ely M. Gelbard, Monte Carlo Principles and Neutron Transport Problems, Addison-Wesley, 1969, Dover reprint 2008
    locator: the chapter on the Monte Carlo solution of the criticality problem
---

A Monte Carlo criticality calculation estimates the effective multiplication factor $k_{\mathrm{eff}}$ of a reactor or of any system with fissile material, the largest eigenvalue of the [k-eigenvalue problem](/k-eigenvalue-problem/). It is [power iteration](/power-iteration/) done with particles. A cycle follows $N$ neutrons from their birth to their absorption or leakage, by the same analog rules as in a fixed-source run, and stores the sites where they cause fission. The number of new neutrons per starting neutron is the estimate of $k$ for the cycle. The next cycle starts $N$ neutrons from the stored sites. After the first cycles, the inactive ones, the distribution of the sites is close to the fundamental mode, and the mean of $k$ over the remaining active cycles is the result. Each cycle is cheap, but the cycles are correlated, the result has a small bias of order $1/N$, and the source can take many cycles to converge in a large system.

## In plain words

In a reactor, each neutron can cause a fission, and a fission makes new neutrons. One batch of neutrons is one generation. If the next generation is larger, the system grows; if it is smaller, the system dies out. The factor $k$ is the ratio of the two sizes.

A computer cannot follow all neutrons, so it follows a sample of, say, a thousand. It counts how many new neutrons they make, and it notes where they were made. Then it takes a thousand of these new places at random and starts again. After some generations the places settle into a fixed pattern, and from then on the counts give $k$.

## The problem

The model is one-speed transport in a bare slab $0 \le x \le L$ with vacuum faces: total cross section $\Sigma_t$, scattering cross section $\Sigma_s$, production cross section $\nu\Sigma_f$ (fission neutrons made per unit path), isotropic scattering and isotropic fission emission. Let $\mathcal{F}$ be the operator that maps a density $s$ of fission neutrons to the density of the fission neutrons of the next generation that they cause. The task is the largest eigenvalue of
$$\mathcal{F} s = k\, s, \quad s \ge 0,$$
which is $k_{\mathrm{eff}}$, with its eigenfunction, the fundamental fission source. The [k-eigenvalue problem](/k-eigenvalue-problem/) page gives the existence of a positive, simple largest eigenvalue for this kind of operator.

## The algorithm

```pseudo id=main
MC-CRITICALITY(N, I, A)
L1  source ← N sites drawn uniformly in the fissile region; k ← 1
L2  for g ← 1 to I + A do
L3      bank ← empty; total ← 0
L4      for each site x in source do start a neutron at x with a direction uniform on [-1, 1]
L5          repeat: fly the distance s = -ln(ξ) / Σt; if the neutron leaves the slab, stop
L6              total ← total + νΣf / Σt                           ▷ the collision estimate of k
L7              put ⌊νΣf / (Σt k) + ξ⌋ copies of the collision site in the bank
L8              with probability Σs / Σt scatter into a new direction, else stop
L9      k ← k_g ← total / N
L10     source ← N sites drawn from the bank with replacement
L11 keep the values k_g of the active cycles g = I + 1, ..., I + A
L12 return their mean and its standard error
```

Line L6 scores the expected number of fission neutrons of a collision, $\nu\Sigma_f/\Sigma_t$, which is the collision estimator of the production. Line L7 divides by the $k$ of the previous cycle so that the bank stays near $N$ sites, and the random rounding $\lfloor a + \xi \rfloor$ has the mean $a$. Line L10 keeps the number of neutrons per cycle fixed at $N$. Lines L11 and L12 drop the inactive cycles, in which the source is still far from the fundamental mode.

## Example

**One neutron by hand.** Take $L = 2$ cm, $\Sigma_t = 1\ \mathrm{cm}^{-1}$, $\Sigma_s = 0.5$, $\nu\Sigma_f = 0.6$, $k = 1$ and one site at $x = 1$, with the random numbers $0.75, 0.5, 0.3, 0.2, 0.0, 0.6, 0.7, 0.9$.

- Line L4: $\mu = 2 \cdot 0.75 - 1 = 0.5$.
- Line L5: $s = -\ln(1 - 0.5) = 0.693147$, so $x = 1 + 0.5 \cdot 0.693147 = 1.346574$. Line L6 adds $0.6$.
- Line L7: $\lfloor 0.6 + 0.3 \rfloor = 0$ sites. Line L8: $0.2 < 0.5$, so the neutron scatters, and $\mu = 2 \cdot 0.0 - 1 = -1$.
- Line L5: $s = -\ln(1 - 0.6) = 0.916291$, so $x = 0.430283$. Line L6 adds $0.6$, so the total is $1.2$.
- Line L7: $\lfloor 0.6 + 0.7 \rfloor = 1$ site at $x = 0.430283$. Line L8: $0.9 \ge 0.5$, so the neutron is absorbed.

The cycle gives $k_g = 1.2$ and a bank with one site. This is the first test of the implementation.

**An infinite medium.** With $\Sigma_t = 1$, $\Sigma_s = 0.9$ and $\nu\Sigma_f = 0.12$, the exact value is $k_\infty = \nu\Sigma_f/(\Sigma_t - \Sigma_s) = 1.2$. A run with $N = 500$, 2 inactive and 20 active cycles (`random.Random(1)`) gives $1.1888 \pm 0.0077$.

**A bare slab.** The same material in a slab of $L = 20$ cm has $k_{\mathrm{eff}} = 1.12006$ from a discrete ordinates solve ($S_{16}$, 320 cells). A run with $N = 500$, 10 inactive and 30 active cycles (`random.Random(2)`) gives $1.1171 \pm 0.0086$.

**A bad first source.** Start all $N = 2000$ neutrons at $x = 1$, near the left face (`random.Random(3)`). Many of them leak, so the first cycles give small values of $k$:

| cycle | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $k_g$ | 0.734 | 0.835 | 0.956 | 0.994 | 1.078 | 1.093 | 1.141 | 1.102 | 1.134 | 1.142 |

From cycle 7 on, the values scatter about the right answer, but the source shape needs more cycles: its [Shannon entropy](/fission-source-entropy/) rises from 2.51 to about 4.15 by cycle 18, near the value $4.185$ of the fundamental mode. With 20 inactive and 40 active cycles, the run gives $1.1175 \pm 0.0040$. The values in the first cycles would bias the mean low, so they must be inactive.

**The error estimate is too small.** Over 25 independent runs (seeds 100 to 124, $N = 500$, 20 inactive and 50 active cycles), the spread of the 25 values of $k$ is $0.00712$ and the mean naive standard error of line L12 is $0.00696$, a ratio of $1.02$. For the fraction of sites in $x < 2$, a local tally, the spread is $0.00404$ and the naive error is $0.00193$, a ratio of $2.10$. The global $k$ is almost not affected by the correlation between cycles, but a local tally is. These are measurements on this problem.

## Correctness

The proofs are below. Three statements, with different status:

- **One cycle is correct in expectation.** This is a theorem: given the source, the expected bank is the next-generation fission density divided by the old $k$, and the expected $k_g$ is the number of fission neutrons per source neutron.
- **For large $N$, the cycles are power iteration.** This is a theorem in the limit $N \to \infty$ with a fixed number of cycles: the source follows $s \mapsto \mathcal{F}s/\|\mathcal{F}s\|$ and $k_g \to \|\mathcal{F}s\|$, so the source tends to the fundamental mode and $k_g$ to $k_{\mathrm{eff}}$, with the error in the shape reduced by about the dominance ratio per cycle.
- **For finite $N$, there are two biases.** The mean of $k$ has a bias of order $1/N$, because each cycle is normalized to $N$ neutrons (Brissenden and Garlick 1986, cited, not proved here). The naive standard error of line L12 treats correlated cycles as independent; the proof shows the exact formula, and positive correlations make the naive error too small.

The number of inactive cycles is a rule of thumb, checked with a diagnostic such as the [fission source entropy](/fission-source-entropy/). No such diagnostic proves that the source has converged.

## Complexity

In the [real RAM](/real-ram/) model, one neutron costs $O(K)$ steps of lines L5 to L8, where $K$ is the mean number of collisions; in an infinite medium $K = \Sigma_t/(\Sigma_t - \Sigma_s)$, which is 10 in the example. A cycle costs $O(NK)$, and $G = I + A$ cycles cost $O(GNK)$. The bank holds at most one site per collision for $\nu\Sigma_f/(\Sigma_t k) < 1$, so the memory is $O(NK)$ in the worst case and about $N$ sites in a normal cycle. The statistical error of $k$ falls like $1/\sqrt{AN}$ when the cycles are about independent, and more slowly when the dominance ratio is close to 1.

## Properties

- **Not exact.** The result has a statistical error and a bias of order $1/N$.
- **Analog transport inside a cycle.** Lines L4 to L8 use the same flight and collision rules as a fixed-source run, so the method works with any geometry and any cross section data.
- **Correlated cycles.** Each source comes from the previous bank, so the $k_g$ and every tally are serially correlated, and the more so as the dominance ratio approaches 1.
- **Slow source convergence in large systems.** The error in the shape falls by about the dominance ratio per cycle, which is $0.99$ for a 100 cm slab of the example material in diffusion theory.

## Variants and improvements

- **Other estimators of $k$.** The absorption estimator scores $\nu\Sigma_f/\Sigma_a$ at each absorption, and the track-length estimator scores $\nu\Sigma_f$ times each flight length. Production codes combine the three with weights from their covariances.
- **Implicit capture.** Neutrons survive collisions with a reduced weight, and the bank uses the weight in line L7.
- **Other source normalizations.** Line L10 can take every banked site and change the weights instead of resampling, or keep a variable number of neutrons per cycle.
- **Faster convergence.** Wielandt shifts, the fission matrix method and coarse mesh finite difference acceleration reduce the effective dominance ratio, at the cost of extra work per cycle.
- **Better error bars.** Batching cycles, or estimating the correlations between cycles and correcting the variance, gives honest error bars for local tallies.

## When to use it

Use a Monte Carlo criticality calculation when $k_{\mathrm{eff}}$ or the power distribution of a system must be known with exact geometry and continuous energy data, for example for the safety of fuel storage and transport, for reactor design checks, and as a reference for deterministic codes. A deterministic eigenvalue solve is cheaper when the geometry and the cross sections can be simplified, and it gives the whole flux shape without noise.

## Pitfalls

- **Too few inactive cycles (line L11).** The first cycles have the wrong source and a biased $k$. Check the [fission source entropy](/fission-source-entropy/) and the local tallies, not only $k$.
- **A first source far from the fissile material (line L1).** If the first sites are in a region with no fuel, line L7 banks few or no sites; spread the first source over all fissile regions.
- **Too few neutrons per cycle (line L10).** The bias is of order $1/N$, and with small $N$ some fuel regions can lose all their sites. Use at least some thousands of neutrons per cycle in a real problem.
- **The naive error bar (line L12).** It assumes independent cycles. For local tallies in large systems it can be several times too small.
- **No division by the old $k$ (line L7).** Without it, the bank grows or shrinks by a factor $k$ per cycle. Resampling then still gives $N$ sites, but the bank cost and the variance of the resampling change from cycle to cycle.
- **An empty bank (line L10).** In a strongly subcritical system with few neutrons, a cycle can bank no sites. The implementation stops with an error.

## Implementations

## History

The method of successive generations was among the first uses of Monte Carlo for reactors. Lieberoth (1968) described the method with a fixed number of neutrons per cycle and studied the convergence of the source. Brissenden and Garlick (1986) analyzed the bias of $k$ that comes from the normalization of each generation and the bias of its error estimate. Ueki, Brown, Parsons and Kornreich (2003) related the correlation between cycles to the dominance ratio, and Ueki and Brown introduced the Shannon entropy of the source as a convergence diagnostic.

## References
