---
tag: W64KF5
kind: algorithm
slug: analog-monte-carlo-transport
name: Analog Monte Carlo particle transport
aliases:
- analog Monte Carlo simulation
area: scientific-computing/particle-transport
level: intro
summary: Follows each particle from birth through free flights, collisions and scattering by sampling the physical probabilities, and counts the events of interest.
solves: [linear-boltzmann-transport-equation]
model: real-ram
complexity:
  vars: {N: the number of histories, K: the mean number of collisions per history}
  time: {average: O(N K)}
  space: {extra: O(1)}
properties: {deterministic: false, randomized: true, exact: true, iterative: true}
history:
  year: 1947
  people: [John von Neumann, Stanislaw Ulam, Nicholas Metropolis]
  note: Von Neumann and Ulam proposed in 1947 to follow neutrons one by one with random numbers. Metropolis and Ulam published the method in 1949.
prereqs: [free-flight-sampling, monte-carlo-integration, linear-boltzmann-transport-equation]
see_also: [collision-estimator, track-length-estimator, implicit-capture, russian-roulette, path-tracing, monte-carlo-criticality, discrete-ordinates-method, central-limit-theorem]
sources:
  - paper: doi:10.1080/01621459.1949.10483310
    title: Nicholas Metropolis and S. Ulam, The Monte Carlo method, Journal of the American Statistical Association 44(247), 1949, 335-341
    locator: the neutron chain reaction as a branching random process sampled one history at a time
  - book: isbn:9780486462936
    title: Jerome Spanier and Ely M. Gelbard, Monte Carlo Principles and Neutron Transport Problems, Addison-Wesley, 1969, Dover reprint 2008
    locator: Chapter 1 (fundamentals) and Chapter 2 (discrete and continuous random walk processes)
  - book: isbn:9780849360749
    title: Ivan Lux and Laszlo Koblinger, Monte Carlo Particle Transport Methods, Neutron and Photon Calculations, CRC Press, 1991
    locator: the chapters on the simulation of particle histories and on analog games
  - book: isbn:9783527407606
    title: Malvin H. Kalos and Paula A. Whitlock, Monte Carlo Methods, second edition, Wiley-VCH, 2008
    locator: Chapter 6 (simulations of stochastic systems, radiation transport)
---

Analog Monte Carlo transport solves the [linear Boltzmann transport equation](/linear-boltzmann-transport-equation/) by simulating particles one at a time with the physical laws of the problem. A history starts a particle at the source, samples the distance to its next collision with [free-flight sampling](/free-flight-sampling/), samples the type of the collision from the cross sections (absorption or scattering), samples the new direction after a scattering, and goes on until the particle is absorbed or leaves the system. Every particle has weight 1 the whole time, which is what "analog" means: the simulation is a direct copy of the physics. The average of a count over $N$ histories is an unbiased estimate of its expected value, with an error that falls like $N^{-1/2}$. The [collision estimator](/collision-estimator/) and the [track-length estimator](/track-length-estimator/) turn the same histories into flux estimates, and [implicit capture](/implicit-capture/) is the first step away from the analog game.

## In plain words

Imagine you could watch one neutron. It flies a random distance, hits a nucleus, and then either disappears into the nucleus or bounces off in a new direction. It does this again and again until it is gone or out of the shield.

Analog Monte Carlo plays this game on a computer with random numbers, and uses the true chances at every step. After many neutrons, you count how many got through the shield, how many came back and how many were absorbed. The fraction that got through is an estimate of the true chance, and the estimate gets better as you play more games. Four times as many games halve the error. Nothing in the method is an approximation of the physics; the only error is the random one.

## The problem

The model problem is one-speed transport in a slab $0 \le x \le L$ with vacuum on both sides. The medium has total cross section $\Sigma_t$ and scattering cross section $\Sigma_s$ in $\mathrm{cm}^{-1}$, absorption $\Sigma_a = \Sigma_t - \Sigma_s$, and the scattering ratio $c = \Sigma_s / \Sigma_t$. Scattering is isotropic, so the new direction cosine $\mu$ is uniform on $[-1, 1]$. A source emits particles at a point $x_0$ with direction $\mu_0$, for example a beam with $x_0 = 0$ and $\mu_0 = 1$.

The questions are the probabilities $T$, $R$ and $A$ that a source particle is transmitted (leaves at $x = L$), reflected (leaves at $x = 0$) or absorbed, and the mean number of collisions per history. For $L = \infty$ in both directions (an infinite medium) there is no leakage, $A = 1$, and the number of collisions has a [geometric distribution](/geometric-distribution/) with mean $1/(1 - c)$. A general code has a three-dimensional geometry of cells, energy-dependent cross sections, several reactions and angular laws of scattering, but the loop is the same.

## The algorithm

```pseudo id=main
ANALOG-HISTORY(x, μ, L, Σ_t, Σ_s)          ▷ one particle with weight 1
L1  k ← 0                                     ▷ collisions so far
L2  loop
L3      s ← -ln(ξ) / Σ_t                       ▷ free flight, ξ uniform in (0, 1]
L4      x ← x + μ s
L5      if x > L then return (TRANSMITTED, k)
L6      if x < 0 then return (REFLECTED, k)
L7      k ← k + 1
L8      with probability Σ_a / Σ_t return (ABSORBED, k)
L9      μ ← 2ξ' - 1                            ▷ isotropic scattering, ξ' uniform in [0, 1)

ANALOG-MONTE-CARLO(N, SOURCE)
L10 for n ← 1 to N do (x, μ) ← SOURCE(), (e, k) ← ANALOG-HISTORY(x, μ, L, Σ_t, Σ_s)
L11     count[e] ← count[e] + 1, add k and k² to the sums
L12 return p_e = count[e] / N with s_e = sqrt(p_e (1 - p_e) / (N - 1)), and the mean of k with its error
```

Lines L3 to L6 sample the flight and test for leakage. In a slab the faces are planes, so the test is a comparison of $x$ with $0$ and $L$. Line L8 draws one uniform number and compares it with $\Sigma_a / \Sigma_t = 1 - c$. Line L9 samples the new direction; in three dimensions it samples a polar cosine and an azimuth and rotates the direction. For anisotropic scattering it samples the cosine from the angular law of the reaction, and in a code with energy dependence line L9 also samples the new energy. Line L12 gives each estimate with its standard error from the sample variance.

## Example

**One history by hand.** Take $L = 2$ cm, $\Sigma_t = 1\ \mathrm{cm}^{-1}$ and $\Sigma_s = 0.5\ \mathrm{cm}^{-1}$, a beam at $x = 0$ with $\mu = 1$, and use $\xi = 1 - r$ for the flights:

| line | random number $r$ | result |
|---|---|---|
| L3, L4 | 0.5 | $s = \ln 2 = 0.693147$, $x = 0.693147$ |
| L8 | 0.7 | $0.7 \ge 0.5$: the particle scatters |
| L9 | 0.1 | $\mu = -0.8$ |
| L3, L4 | 0.4 | $s = -\ln 0.6 = 0.510826$, $x = 0.693147 - 0.8 \cdot 0.510826 = 0.284487$ |
| L8 | 0.2 | $0.2 < 0.5$: absorbed after $k = 2$ collisions |

With $r = 0.9$ in the fourth row instead, the flight is $\ln 10 = 2.302585$ cm long, $x$ becomes negative, and the particle is reflected after one collision.

**A pure absorber.** With $\Sigma_s = 0$ and $L = 2$ cm (two mean free paths), the exact transmission is $e^{-2} = 0.135335$. A run with `random.Random(1)` gives:

| $N$ | $\hat T$ | standard error | relative error $R$ |
|---|---|---|---|
| 100 | 0.1000 | 0.0302 | 0.30 |
| 1000 | 0.1310 | 0.0107 | 0.081 |
| 10000 | 0.1375 | 0.0034 | 0.025 |
| 100000 | 0.13625 | 0.0011 | 0.0080 |

The relative error of a binomial count is $\sqrt{(1 - T)/(N T)}$, which is $0.0253$ for $N = 10^4$, close to the measured value. Each factor of 10 in $N$ divides it by about $\sqrt{10} = 3.16$.

**Scattering.** With $c = 0.5$ in the same slab and $N = 10^5$ (`random.Random(2)`), the run gives $\hat T = 0.1887 \pm 0.0012$, $\hat R = 0.1139 \pm 0.0010$ and $\hat A = 0.6973 \pm 0.0015$, with $1.399 \pm 0.003$ collisions per history. The three counts add up to $N$ exactly. The uncollided part of the transmission is $0.1361 \pm 0.0011$, which agrees with $e^{-\Sigma_t L} = 0.135335$ whatever $c$ is. In an infinite medium the mean number of collisions is $1/(1 - c)$; the runs give $1.9996 \pm 0.0045$ for $c = 0.5$ (exact 2), $5.014 \pm 0.014$ for $c = 0.8$ (exact 5) and $99.28 \pm 0.31$ for $c = 0.99$ (exact 100).

## Correctness

The claim is a theorem: each history is an exact sample of the random path of one particle in the transport model, so each count of line L12 is an unbiased estimate of the probability of its event, and the mean of $k$ is an unbiased estimate of the expected number of collisions. The expected number of collisions in a region, summed over all histories and divided by $N$, is the integral of the collision density $F = \Sigma_t \phi$ over the region, where $\phi$ is the scalar flux that solves the transport equation. The argument writes the collision density as the sum over $k$ of the densities of the $k$-th collision, which is the [Neumann series](/neumann-series/) of the integral form of the transport equation. The history ends with probability 1 when $c < 1$ or when the slab is finite. The full proof is below.

The [central limit theorem](/central-limit-theorem/) then gives the error bars: for large $N$ the estimate is close to normal with standard deviation $\sigma / \sqrt{N}$, where $\sigma^2$ is the variance of one history. The confidence statement is asymptotic, and it needs a finite variance, which holds for counts.

## Complexity

In the [real RAM](/real-ram/) model each collision costs $O(1)$ in a slab, so a run of $N$ histories costs $O(N K)$ with $K$ the mean number of collisions per history, and $O(1)$ extra space for the sums. In an infinite medium $K = 1/(1 - c)$, which grows without bound as $c \to 1$. In a slab of pure scatterer, a beam history is a random walk that starts near a face, and $K$ grows about linearly with the thickness $\Sigma_t L$; a source inside the slab gives $K$ of order $(\Sigma_t L)^2$. These two growth rates are heuristics from the random walk picture, not exact results. In a three-dimensional geometry each flight also costs a search for the distance to the next surface.

The quantity that matters in practice is the cost per unit of accuracy. The figure of merit $\mathrm{FOM} = 1/(R^2 T_{\text{cpu}})$, with $R$ the relative error and $T_{\text{cpu}}$ the run time, is about constant in $N$ for one problem and one code, so it compares methods. It is a measurement and depends on the machine.

## Properties

- **Unbiased.** Every estimate is unbiased for every $N$, with no discretization of space, angle or energy.
- **Exact physics.** The method can use continuous energy cross sections and exact geometry, which deterministic methods such as the [discrete ordinates method](/discrete-ordinates-method/) cannot.
- **Embarrassingly parallel.** Histories are independent, so they run in parallel with separate random number streams.
- **Slow convergence.** The error falls like $N^{-1/2}$. A rare event of probability $p$ needs about $1/(p R^2)$ histories for a relative error $R$, so a shield with transmission $10^{-8}$ is out of reach for analog play.
- **Exact balance.** The counts of transmission, reflection and absorption add up to $N$, so the estimates satisfy $\hat T + \hat R + \hat A = 1$ exactly.

## Variants and improvements

- **Non-analog play.** The particle carries a weight that the method changes at each event to keep the mean the same. [Implicit capture](/implicit-capture/), [Russian roulette](/russian-roulette/), [particle splitting](/particle-splitting/), [weight windows](/weight-window/) and the [exponential transform](/exponential-transform/) are the standard tools. Their goal is a lower variance per unit of computer time.
- **Better tallies.** The [collision estimator](/collision-estimator/), the [track-length estimator](/track-length-estimator/) and [next-event estimation](/next-event-estimation/) all score from the same histories, with different variances.
- **Criticality.** For a multiplying medium the histories run in generations, with fission sites as the next source; see [Monte Carlo criticality](/monte-carlo-criticality/).
- **Light transport.** [Path tracing](/path-tracing/) in computer graphics is the same random walk for photons with surfaces and materials, written for the [rendering equation](/rendering-equation/).

## When to use it

Use analog Monte Carlo as a reference for small problems, to test a deterministic code, and when the quantity of interest has a probability that is not small: the absorption in a fuel pin, the leakage of a small assembly. It is also the base that every variance reduction scheme is compared to. Do not use it for deep penetration problems, small detectors far from the source or rare reactions; there a biased game with weights is many orders of magnitude cheaper for the same error.

## Pitfalls

- **Error bars for one history.** The collisions inside a history are correlated. The variance must be computed from the per-history totals, not from the individual scores.
- **Small $N$.** For a rare event the run may see no event at all, and then the estimate is 0 with a standard error of 0. A zero estimate with a zero error is not a result.
- **Infinite loops.** With $c = 1$ in an infinite medium a history never ends. A code needs a limit on the number of collisions or a time cutoff.
- **Random number streams.** Two parallel processes with the same [seed](/seed/) give the same histories, and the error bar then hides the correlation. Use independent streams.
- **Statistical checks.** The error bar is only valid if the variance is finite and the run is long enough to sample the tail. Production codes run extra tests on the tally fluctuations; a single error bar can hide a missing rare path.

## Implementations

## History

In 1947 John von Neumann wrote to Robert Richtmyer with a plan to follow neutrons in a fission device one at a time, with random numbers for the flight distances and the collision types, and Stanislaw Ulam had the same idea while he thought about the odds of solitaire. Nicholas Metropolis gave the method its name. The first such calculations ran on the ENIAC in 1948. Metropolis and Ulam published the method in 1949, with the neutron chain as the main example. Herman Kahn wrote in the early 1950s the first systematic text on the sampling methods for transport, and the books of Spanier and Gelbard (1969) and of Lux and Koblinger (1991) give the theory as it is used today.

## References
