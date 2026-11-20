---
tag: NDP0HX
kind: algorithm
slug: collision-estimator
name: Collision estimator
aliases:
- collision tally
area: scientific-computing/particle-transport
level: core
summary: Estimates the flux in a region by summing weight over total cross section at each collision in that region, divided by the number of histories and the volume.
solves: [linear-boltzmann-transport-equation]
model: real-ram
complexity:
  vars: {N: the number of histories, K: the mean number of collisions per history, B: the number of tally bins}
  time: {average: O(N K)}
  space: {extra: O(B)}
properties: {deterministic: false, randomized: true, exact: true, iterative: true}
history:
  year: 1949
  people: [Nicholas Metropolis, Stanislaw Ulam]
  note: Scores at collisions are as old as Monte Carlo transport. Spanier and Gelbard gave the collision and track-length estimators with their variances in 1969.
prereqs: [analog-monte-carlo-transport]
see_also: [track-length-estimator, next-event-estimation, path-tracing, implicit-capture, monte-carlo-criticality, monte-carlo-integration, variance, importance-sampling]
sources:
  - book: isbn:9780486462936
    title: Jerome Spanier and Ely M. Gelbard, Monte Carlo Principles and Neutron Transport Problems, Addison-Wesley, 1969, Dover reprint 2008
    locator: the estimators of linear functionals of the flux, with the collision density as the basic quantity
  - book: isbn:9780849360749
    title: Ivan Lux and Laszlo Koblinger, Monte Carlo Particle Transport Methods, Neutron and Photon Calculations, CRC Press, 1991
    locator: the chapter on estimators, with the collision, track-length and next-event estimators
  - book: isbn:9783527407606
    title: Malvin H. Kalos and Paula A. Whitlock, Monte Carlo Methods, second edition, Wiley-VCH, 2008
    locator: Chapter 6 (radiation transport), the estimators of the flux
---

The collision estimator turns the histories of a Monte Carlo transport run into an estimate of the scalar flux $\phi$ in a region. Each time a particle of weight $w$ collides in the region, it scores $w/\Sigma_t$, where $\Sigma_t$ is the total cross section at the collision point; the sum of the scores divided by the number of histories $N$ and the volume $V$ is an unbiased estimate of the average flux in the region. The reason is that the collision rate density is $F = \Sigma_t \phi$, so $1/\Sigma_t$ turns a count of collisions into a flux. The [track-length estimator](/track-length-estimator/) estimates the same quantity from the path lengths and is better in thin regions and the only choice in a void, while the collision estimator is better in dense regions with many short flights. [Next-event estimation](/next-event-estimation/) scores the expected contribution to a point detector at each collision, and [path tracing](/path-tracing/) in graphics uses the same idea for the light that reaches the eye.

## In plain words

You want to know how many particles pass through a box, but you only see where they hit atoms. In a dense material the particles hit atoms often, so a lot of hits does not mean a lot of particles.

The fix is to give each hit a value of one over the density of hits per centimetre. In a dense box each hit counts for little; in a thin box each hit counts for a lot. Add up these values for all particles, divide by the number of particles and the size of the box, and you get the average flux in the box. The answer is right on average. In a box with almost no atoms there are few hits, each with a large value, so the answer is noisy, and in an empty box there are no hits at all.

## The problem

A Monte Carlo transport run follows $N$ independent histories, as in [analog Monte Carlo transport](/analog-monte-carlo-transport/). The geometry has tally regions (bins) $B_1, \ldots, B_m$ with volumes $V_j$. The quantity to estimate is the average scalar flux per source particle,

$$\bar\phi_j = \frac{1}{V_j} \int_{B_j} \phi(r)\, dr,$$

or a reaction rate $\int_{B_j} \Sigma_r \phi$ for a reaction $r$. Here $\phi(r) = \int \psi(r, \Omega)\, d\Omega$ is the scalar flux of the [linear Boltzmann transport equation](/linear-boltzmann-transport-equation/), in particles per $\mathrm{cm}^2$ per source particle for a fixed source problem. The code below uses a one-speed slab $0 \le x \le L$ with bins of width $\Delta x$, so the "volume" of a bin is its width, and the flux is in particles per cm per source particle.

## The algorithm

```pseudo id=main
COLLISION-ESTIMATOR(N, SOURCE, bins)
L1  for n ← 1 to N do
L2      (x, μ) ← SOURCE(), w ← 1, h ← 0             ▷ h holds the scores of this history
L3      loop: fly to the next collision with free-flight sampling
L4          if the particle left the system then break
L5          j ← the bin of x
L6          h_j ← h_j + w / Σ_t(x)                   ▷ the collision score
L7          with probability Σ_a / Σ_t break           ▷ absorbed
L8          μ ← a new direction from the scattering law
L9      S_j ← S_j + h_j, Q_j ← Q_j + h_j² for every bin j
L10 return φ_j = S_j / (N V_j), with s_j = sqrt((Q_j / N - (S_j / N)²) / (N - 1)) / V_j
```

Line L6 is the only line that differs from an analog history. For a reaction rate it scores $w \Sigma_r / \Sigma_t$ instead, which is $w$ times the probability that the collision is of type $r$. Line L9 adds the total of one history, not the single scores, because the collisions of one history are correlated; the variance in line L10 is the variance of these totals. With [implicit capture](/implicit-capture/) line L7 is replaced by a weight change, and line L6 scores the weight before the collision.

## Example

**Two histories by hand.** A beam enters a slab of 2 cm with $\Sigma_t = 2\ \mathrm{cm}^{-1}$ and $\Sigma_s = 1\ \mathrm{cm}^{-1}$, with two bins of 1 cm. Each score is $1/\Sigma_t = 0.5$ cm.

| history | flight | collision at | bin | score | outcome |
|---|---|---|---|---|---|
| 1 | $\ln 2 / 2 = 0.3466$ | 0.3466 | 0 | 0.5 | scatters to $\mu = 1$ |
| 1 | $\ln 10 / 2 = 1.1513$ | 1.4979 | 1 | 0.5 | absorbed |
| 2 | $\ln 2 / 2 = 0.3466$ | 0.3466 | 0 | 0.5 | absorbed |

The totals are $S_0 = 1.0$ and $S_1 = 0.5$, so $\phi_0 = 1.0/(2 \cdot 1) = 0.5$ and $\phi_1 = 0.5/(2 \cdot 1) = 0.25$ per source particle.

**A pure absorber.** A beam on a slab of 2 cm with $\Sigma_t = 1\ \mathrm{cm}^{-1}$ and $\Sigma_s = 0$ has the flux $\phi(x) = e^{-x}$, so the average over a bin $[a, b]$ is $(e^{-a} - e^{-b})/(b - a)$. With four bins of 0.5 cm and $N = 20000$ (`random.Random(1)`):

| bin | exact | collision estimate | standard error |
|---|---|---|---|
| [0, 0.5] | 0.786939 | 0.7869 | 0.0069 |
| [0.5, 1] | 0.477302 | 0.4776 | 0.0060 |
| [1, 1.5] | 0.289499 | 0.2798 | 0.0049 |
| [1.5, 2] | 0.175590 | 0.1795 | 0.0040 |

All four estimates lie within 2 standard errors of the exact value.

**An infinite medium.** A slab of 2 cm with mirrors on both faces, $\Sigma_t = 1\ \mathrm{cm}^{-1}$, $c = 0.5$ and a uniform isotropic source of one particle per history ($Q = 1/2$ per cm) behaves as an infinite medium, where $\phi = Q/\Sigma_a = 1$. With $N = 20000$ (`random.Random(2)`) the four bins give $1.002$, $0.988$, $0.991$ and $1.022$, each with a standard error of about $0.012$.

## Correctness

The claim is a theorem: for an analog game, or for any fair weighted game, $E[\phi_j] = \bar\phi_j$ exactly for every $N$, provided $\Sigma_t > 0$ everywhere in the bin. The proof uses the collision density $F$ of the game: the expected number of collisions in a small volume $dr$ around $r$ is $F(r)\, dr$, and the [analog Monte Carlo](/analog-monte-carlo-transport/) proof shows that $F = \Sigma_t \phi$ with $\phi$ the solution of the transport equation. Then the expected score is $\int_{B_j} F/\Sigma_t = \int_{B_j} \phi$. In a fair weighted game the expected weight that collides in $dr$ is again $\Sigma_t \phi\, dr$, and the same argument applies. The full proof is below.

The variance of one history total is finite, because the number of collisions has a geometric tail and each score is bounded by $w/\min \Sigma_t$. So the error bar of line L10 is valid in the limit of large $N$ by the [central limit theorem](/central-limit-theorem/).

## Complexity

The tally adds $O(1)$ work per collision with uniform bins, or $O(\log B)$ with a search over $B$ bins of any size, to the $O(N K)$ cost of the histories, where $K$ is the mean number of collisions per history. It needs $O(B)$ space for the sums and the scores of the current history. The cost that matters is the variance per history, which depends on the problem:

- **Dense regions.** Many collisions per history in the bin give a low variance, often lower than the track-length estimator, because each score is small.
- **Thin regions.** With $\Sigma_t \Delta x \ll 1$, only a fraction of about $\Sigma_t \Delta x$ of the particles that cross the bin collide in it, and each score $1/\Sigma_t$ is large. The relative variance then grows like $1/(\Sigma_t \Delta x)$. The track-length page has a table of this effect.

## Properties

- **Unbiased.** Exactly, for every $N$, where $\Sigma_t > 0$.
- **No geometry work.** The score needs only the collision point, not the path, so it is cheap in complex geometry and needs no distances to the bin faces.
- **Same histories.** It uses the histories of the run as they are, so several estimators can score from one run, and their difference is a check on the code.
- **Point quantities.** It cannot estimate the flux at a point or on a surface, because no collision happens exactly there. [Next-event estimation](/next-event-estimation/) does this.

## Variants and improvements

- **Reaction rates.** Score $w \Sigma_r(E)/\Sigma_t(E)$ for reaction $r$, for example $w \nu \Sigma_f / \Sigma_t$ for the fission source in a [criticality](/monte-carlo-criticality/) run.
- **Absorption estimator.** Score $w/\Sigma_a$ at each absorption only. It is also unbiased, but it has fewer scores and a higher variance in a scatterer.
- **Next-event estimator.** At each collision, score the probability that the next flight reaches a point detector. It is unbiased but has an infinite variance for collisions close to the detector.
- **Combined estimators.** A linear combination of the collision and track-length estimates with weights that minimise the sample variance has a lower variance than either one. This is a measured gain that depends on the problem.

## When to use it

Use the collision estimator in thick regions with many collisions, for reaction rates in fuel and absorbers, and in geometries where computing path lengths in tally cells is expensive. Use the [track-length estimator](/track-length-estimator/) in thin regions, in gases and in voids. In a k-eigenvalue run it is common to compute both and their combination.

## Pitfalls

- **Voids.** In a region with $\Sigma_t = 0$ there are no collisions, and the estimator gives 0 for a flux that is not 0. It is unbiased only where $\Sigma_t > 0$.
- **Energy dependence.** The score uses $\Sigma_t$ at the energy of the particle before the collision. Using the energy after the collision gives a biased result.
- **The score of the weight.** With implicit capture or roulette, the score uses the weight before the collision changes it.
- **Per-collision variance.** A variance computed from the individual scores instead of the history totals is too small when a history collides many times in the bin.
- **Bin volumes.** The volume in line L10 must be the true volume of the tally region. In complex geometry, a wrong or estimated volume biases the result, even if the scores are right.

## Implementations

## History

Collision scores are as old as Monte Carlo transport: the first neutron calculations at Los Alamos in the late 1940s counted collisions and absorptions in regions. The theory of estimators as unbiased functionals of the random walk was worked out in the 1950s and 1960s. Spanier and Gelbard gave the collision and track-length estimators side by side with their variances in their 1969 book, and Lux and Koblinger gave a general theory of estimators for transport in 1991.

## References
