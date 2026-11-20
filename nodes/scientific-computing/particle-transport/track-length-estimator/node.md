---
tag: QW4YNY
kind: algorithm
slug: track-length-estimator
name: Track-length estimator
aliases:
- track-length tally
area: scientific-computing/particle-transport
level: core
summary: Estimates the scalar flux in a region by summing weight times the path length of every track segment inside it, divided by the number of histories and the volume.
solves: [linear-boltzmann-transport-equation]
model: real-ram
complexity:
  vars: {N: the number of histories, K: the mean number of flights per history, B: the number of bins that a flight crosses}
  time: {average: O(N K B)}
  space: {extra: O(B)}
properties: {deterministic: false, randomized: true, exact: true, iterative: true}
history:
  year: 1969
  people: [Jerome Spanier, Ely M. Gelbard]
  note: The flux is the track length per unit volume, an idea of early reactor physics. Spanier and Gelbard gave the track-length estimator next to the collision estimator, with variances, in 1969.
prereqs: [analog-monte-carlo-transport]
see_also: [collision-estimator, next-event-estimation, path-tracing, free-flight-sampling, delta-tracking, monte-carlo-criticality, implicit-capture, variance]
sources:
  - book: isbn:9780486462936
    title: Jerome Spanier and Ely M. Gelbard, Monte Carlo Principles and Neutron Transport Problems, Addison-Wesley, 1969, Dover reprint 2008
    locator: the estimators of linear functionals of the flux, with the track-length estimator
  - book: isbn:9780849360749
    title: Ivan Lux and Laszlo Koblinger, Monte Carlo Particle Transport Methods, Neutron and Photon Calculations, CRC Press, 1991
    locator: the chapter on estimators, with the track-length estimator and its comparison with the collision estimator
  - book: isbn:9780471092452
    title: E. E. Lewis and W. F. Miller, Jr., Computational Methods of Neutron Transport, Wiley, 1984
    locator: the chapter on the Monte Carlo method, with the flux tallies
---

The track-length estimator turns the histories of a Monte Carlo transport run into an estimate of the scalar flux in a region. Every straight flight of a particle of weight $w$ scores $w$ times the length of the part of the flight that lies inside the region; the sum divided by the number of histories $N$ and the volume $V$ is an unbiased estimate of the average flux. The reason is that the scalar flux is the total path length travelled per unit volume per source particle. The [collision estimator](/collision-estimator/) estimates the same quantity from collisions only. The track-length estimator scores from every particle that crosses the region, so it has a much lower variance in thin regions, and it is the only one of the two that works in a void; the collision estimator needs no path geometry and can be better in dense regions. [Next-event estimation](/next-event-estimation/) and [path tracing](/path-tracing/) score expected contributions at points instead.

## In plain words

The flux in a box tells how much travel happens in it. If ten particles each fly one centimetre in a box of one cubic centimetre, the flux is ten. So, to measure the flux, add up the length of every piece of path inside the box, and divide by the size of the box and the number of particles.

A particle that crosses the box without any collision still adds its path. That is why this method works well in a box of thin gas or even an empty box, where almost nobody hits an atom. The cost is geometry: the code must find where each flight enters and leaves each box.

## The problem

The problem is the same as for the [collision estimator](/collision-estimator/): estimate the average scalar flux per source particle

$$\bar\phi_j = \frac{1}{V_j} \int_{B_j} \phi(r)\, dr$$

over tally regions $B_j$, from $N$ histories of [analog Monte Carlo transport](/analog-monte-carlo-transport/) or of a fair weighted game. A history is a chain of straight flights. A flight starts at $r$ in direction $\Omega$ and has path length $s$; its track length in $B_j$ is the length of $\{r + t\Omega : 0 \le t \le s\} \cap B_j$. The code below uses a slab $0 \le x \le L$ cut into bins of width $\Delta x$. A flight from $x_0$ to $x_1$ with direction cosine $\mu$ has the track length $|x_1 - x_0|/|\mu|$, and it splits among the bins it crosses by the part of $[x_0, x_1]$ in each bin.

## The algorithm

```pseudo id=main
TRACK-LENGTH-ESTIMATOR(N, SOURCE, bins)
L1  for n ← 1 to N do
L2      (x, μ) ← SOURCE(), w ← 1, h ← 0             ▷ h holds the scores of this history
L3      loop
L4          s ← -ln(ξ) / Σ_t                         ▷ free flight
L5          for each bin j that the flight crosses do h_j ← h_j + w · (path length of the flight in bin j)
L6          if the particle left the system then break
L7          with probability Σ_a / Σ_t break           ▷ absorbed
L8          μ ← a new direction from the scattering law
L9      S_j ← S_j + h_j, Q_j ← Q_j + h_j² for every bin j
L10 return φ_j = S_j / (N V_j), with s_j = sqrt((Q_j / N - (S_j / N)²) / (N - 1)) / V_j
```

Line L5 is the difference with the collision estimator. A flight that leaves the system scores only up to the face. With reflecting faces, the flight scores each straight piece between reflections. In a heterogeneous medium, the flight crosses region faces during [free-flight sampling](/free-flight-sampling/), and the code scores each piece as it crosses; with [delta tracking](/delta-tracking/) there are no face crossings, and the code must find the bin crossings in a separate step. For a reaction rate, line L5 scores $w \Sigma_r \ell$ instead of $w \ell$.

## Example

**Two histories by hand.** A beam enters a pure absorber of 2 cm with $\Sigma_t = 1\ \mathrm{cm}^{-1}$, with two bins of 1 cm. The first history draws a flight $-\ln 0.75 = 0.287682$ cm and is absorbed in bin 0, which scores $0.287682$. The second history draws a flight $\ln 10 = 2.302585$ cm and leaves at $x = 2$, which scores 1 cm in each bin. So $\phi_0 = 1.287682/2 = 0.643841$ and $\phi_1 = 1.0/2 = 0.5$ per source particle.

**A slanted flight.** A flight from $x = 0.25$ with $\mu = 0.5$ and a path length of 1 cm ends at $x = 0.75$. With bins of 0.5 cm, it lies for $0.25$ cm in $x$ in each of the first two bins, so each bin scores $0.25/0.5 = 0.5$ cm of path.

**Against the collision estimator.** The two estimators were run on the same problems with $N = 20000$ (`random.Random(1)` to `random.Random(3)`). For a beam on a pure absorber of 2 cm with $\Sigma_t = 1\ \mathrm{cm}^{-1}$ and four bins:

| bin | exact | collision | track length |
|---|---|---|---|
| [0, 0.5] | 0.786939 | 0.7869 ± 0.0069 | 0.7836 ± 0.0023 |
| [0.5, 1] | 0.477302 | 0.4776 ± 0.0060 | 0.4774 ± 0.0032 |
| [1, 1.5] | 0.289499 | 0.2798 ± 0.0049 | 0.2927 ± 0.0030 |
| [1.5, 2] | 0.175590 | 0.1795 ± 0.0040 | 0.1805 ± 0.0026 |

In a slab of 1 cm with $c = 0.5$ and four bins, the first bin gives these values as $\Sigma_t$ goes down:

| $\Sigma_t$ ($\mathrm{cm}^{-1}$) | beam, collision | beam, track length | isotropic source, collision | isotropic source, track length |
|---|---|---|---|---|
| 1 | 1.149 ± 0.016 | 1.177 ± 0.006 | 0.795 ± 0.014 | 0.804 ± 0.010 |
| 0.1 | 1.136 ± 0.048 | 1.071 ± 0.007 | 1.638 ± 0.058 | 1.658 ± 0.028 |
| 0.01 | 1.160 ± 0.152 | 1.011 ± 0.004 | 2.780 ± 0.238 | 2.737 ± 0.103 |

The collision estimator gets worse as the slab gets thinner, because fewer particles collide and each score $1/\Sigma_t$ is larger. For a beam the track-length error even goes down, because an uncollided particle scores exactly $\Delta x$. For an isotropic source the track-length error also grows, but more slowly: a particle that flies almost parallel to the faces has a long path in one bin. These numbers are measurements, not bounds.

## Correctness

The claim is a theorem: for an analog game or a fair weighted game, $E[\phi_j] = \bar\phi_j$ for every $N$, with no condition on $\Sigma_t$; it holds in a void too. The proof uses the track-length density: the expected total weighted path length that histories travel in a small volume $dr$ around $r$, with directions in $d\Omega$, is $\psi(r, \Omega)\, dr\, d\Omega$, where $\psi$ is the angular flux. This holds because a flight from a collision or source point carries its weight along the path with survival probability $e^{-\tau}$, which is the uncollided part of the transport solution, and the sum over flights is the Neumann series again. Integration over the bin and all directions gives $\int_{B_j} \phi$. The full proof is below.

The score of one flight is at most the flight length, so the variance is finite when the flights have finite second moments, which holds when $\Sigma_t$ is bounded below by a positive constant or the region is bounded. In an unbounded void a flight can be infinite, but then the particle leaves and the score is the bounded chord of the bin.

## Complexity

Each flight costs $O(1)$ plus the work to find its crossings with the bins. With uniform bins in a slab this is $O(1)$ per crossed bin, so a run costs $O(N K B)$ with $K$ flights per history and $B$ bins crossed per flight; with a mesh tally that is not aligned with the geometry, a ray walk through the mesh does the same work. The space is $O(B)$ for the sums. In a code where the tally regions are the cells of the geometry, the crossings are found anyway by free-flight sampling, and the tally is almost free.

## Properties

- **Unbiased everywhere.** Including voids and thin regions, where the collision estimator fails or is noisy.
- **Scores without collisions.** Every particle that crosses the region scores, so the number of scores per history is high in thin regions.
- **Bounded scores.** The score of one flight is at most its length, or the longest chord of the region. A long chord near a grazing direction is the main source of variance for an isotropic source in a thin region.
- **Path geometry.** It needs the intersection of each flight with the tally regions, which costs more than the collision estimator when the tally mesh is not the geometry.

## Variants and improvements

- **Reaction rates.** Score $w \Sigma_r(E) \ell$ for the rate of reaction $r$; this is the usual estimator of the fission source and of heating in production codes.
- **Expected track length.** Score at each flight the expected track length in the region along the ray, the integral of $e^{-\tau(t)}$ over the path lengths $t$ at which the ray is inside the region, instead of the sampled one. It has a lower variance, at the cost of an integral per flight.
- **Surface current and surface flux.** On a surface, count crossings with weight $w$ for the current, and with weight $w/|\mu|$ for the surface flux, the limit of the track-length estimator for a thin bin. The surface flux estimator has an infinite variance for grazing crossings, so codes cut off small $|\mu|$.
- **Combined estimators.** A weighted combination of the track-length, collision and absorption estimates with weights from the sample covariance has a lower variance than each one; it is used for $k_{\mathrm{eff}}$ in [criticality](/monte-carlo-criticality/) codes.

## When to use it

Use the track-length estimator for fluxes and reaction rates in cells of the geometry, in thin regions, in gases, in voids and on fine mesh tallies in optically thin parts of the problem. Use the [collision estimator](/collision-estimator/) in dense regions with many short flights and when path lengths in the tally regions are expensive to find. For a flux at a point, use [next-event estimation](/next-event-estimation/).

## Pitfalls

- **The factor $1/|\mu|$.** In slab geometry the path length in a bin is the depth in $x$ divided by $|\mu|$. A code that scores the depth in $x$ underestimates the flux.
- **Truncated flights.** A flight that leaves the system or reaches a reflecting face must score only to the face, and then the rest after the reflection.
- **Delta tracking.** With delta tracking the tentative flights do not stop at region faces, so the tally must clip each flight to the bins itself. Scoring at the tentative collisions instead gives a collision estimator with the majorant cross section.
- **Grazing flights.** For an isotropic source in a thin bin, rare flights almost parallel to the faces give large scores. The estimate stays unbiased, but its error falls slowly and the error bar converges slowly.
- **Per-flight variance.** As for every tally, the variance must come from the history totals.

## Implementations

## History

The interpretation of the scalar flux as the track length per unit volume is old in reactor physics, and early Monte Carlo codes scored track lengths in their cells. Spanier and Gelbard gave the track-length and collision estimators side by side, with their variances, in their 1969 book. Lux and Koblinger gave a general theory of transport estimators, including expected-value variants, in 1991. The track-length estimator is the standard flux tally of production codes today.

## References
