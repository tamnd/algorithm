---
tag: 21RHN1
kind: algorithm
slug: free-flight-sampling
name: Free-flight distance sampling
aliases:
- distance to collision sampling
area: scientific-computing/particle-transport
level: intro
summary: Samples the distance to the next collision as -ln(xi)/Sigma_t in a uniform medium, and by spending one sampled optical depth region by region in a heterogeneous one.
model: real-ram
complexity:
  vars: {M: the number of regions that the flight crosses}
  time: {worst: O(M)}
  space: {extra: O(1)}
properties: {deterministic: false, randomized: true, exact: true, iterative: true}
history:
  year: 1947
  people: [John von Neumann, Stanislaw Ulam, Nicholas Metropolis]
  note: The exponential flight distance was part of the first Monte Carlo neutron calculations at Los Alamos in 1947. Metropolis and Ulam described the method in 1949. Woodcock and others gave delta tracking in 1965.
prereqs: [inverse-transform-sampling, linear-boltzmann-transport-equation]
see_also: [delta-tracking, inverse-transform-sampling, analog-monte-carlo-transport, track-length-estimator, exponential-transform, volumetric-path-tracing, geometric-distribution, rejection-sampling]
sources:
  - book: isbn:9780849360749
    title: Ivan Lux and Laszlo Koblinger, Monte Carlo Particle Transport Methods, Neutron and Photon Calculations, CRC Press, 1991
    locator: the chapter on the simulation of the free flight, with the sampling of the path length in heterogeneous media
  - book: isbn:9783527407606
    title: Malvin H. Kalos and Paula A. Whitlock, Monte Carlo Methods, second edition, Wiley-VCH, 2008
    locator: Chapter 3 (sampling random variables) and Chapter 6 (radiation transport)
  - book: isbn:9780486462936
    title: Jerome Spanier and Ely M. Gelbard, Monte Carlo Principles and Neutron Transport Problems, Addison-Wesley, 1969, Dover reprint 2008
    locator: Chapter 2 (discrete and continuous random walk processes)
  - paper: doi:10.1080/01621459.1949.10483310
    title: Nicholas Metropolis and S. Ulam, The Monte Carlo method, Journal of the American Statistical Association 44(247), 1949, 335-341
    locator: the neutron chain as the first example of the method
---

Free-flight sampling draws the distance $s$ that a neutral particle (a neutron or a photon) travels before its next collision. In a uniform medium with total cross section $\Sigma_t$ the distance has the exponential law with mean $1/\Sigma_t$, and [inverse transform sampling](/inverse-transform-sampling/) gives $s = -\ln(\xi)/\Sigma_t$ with $\xi$ uniform on $(0, 1]$. In a medium made of regions with different cross sections, the method draws one optical depth $\tau = -\ln \xi$ and spends it along the path, region by region, until the depth is used up. [Delta tracking](/delta-tracking/) (also called Woodcock tracking) samples the same law in a different way: it takes flights at a constant majorant cross section and rejects some collisions, so it needs no distances to region faces. Free-flight sampling is the first step of every history in [analog Monte Carlo transport](/analog-monte-carlo-transport/).

## In plain words

A particle that moves through matter has a fixed chance per centimetre to hit an atom. That chance does not depend on how far the particle already went. So the distance to the next hit is random, short distances are the most likely, and the mean distance is the mean free path.

To sample it, draw a random number and turn it into a distance with a logarithm. A small number gives a long flight. If the path crosses layers of different materials, think of the random number as a budget of "hitting chance". Each layer uses some of the budget, more for dense layers. The particle collides in the layer where the budget runs out. If the budget is still left at the outer face, the particle escapes.

## The problem

A particle is at position $x$ in a slab made of regions $0, \ldots, M - 1$. Region $k$ is the interval $[b_k, b_{k+1}]$ and has a constant total cross section $\Sigma_k \ge 0$ in $\mathrm{cm}^{-1}$. The particle moves with direction cosine $\mu \ne 0$, so a path length $s$ moves it to $x + \mu s$. The optical depth along the path is

$$\tau(s) = \int_0^s \Sigma(x + \mu s')\, ds'.$$

The probability of no collision on the first $s$ centimetres of path is $e^{-\tau(s)}$. This follows from the definition of the cross section: the probability of a collision in $[s, s + ds)$, given none before, is $\Sigma\, ds$. The task is to draw the collision point with this law, or to report that the particle leaves the slab first, which has probability $e^{-\tau_{\text{face}}}$, with $\tau_{\text{face}}$ the optical depth to the outer face. In three dimensions the regions are cells of a geometry and the faces are surfaces, but the method is the same.

## The algorithm

```pseudo id=main
FREE-FLIGHT-UNIFORM(Σ_t)                     ▷ a uniform medium, Σ_t > 0
L1  draw ξ uniform in (0, 1]
L2  return s = -ln(ξ) / Σ_t

FREE-FLIGHT(x, μ, i, b, Σ, ξ)               ▷ particle at x in region i, ξ uniform in (0, 1]
L3  τ ← -ln ξ                                ▷ optical depth to spend
L4  loop
L5      d ← path length from x to the face of region i in direction μ
L6      if Σ_i d > τ then
L7          return collision at x + μ τ / Σ_i, in region i
L8      τ ← τ - Σ_i d                        ▷ the particle crosses region i
L9      x ← the face, i ← the next region along μ
L10     if i is outside the slab then return escape at x
```

Line L5 is $(b_{i+1} - x)/\mu$ for $\mu > 0$ and $(b_i - x)/\mu$ for $\mu < 0$. In a void region $\Sigma_i = 0$, so line L6 is false and the particle always crosses it. The comparison uses a strict inequality, so a depth that ends exactly on a face counts as a crossing, which has probability 0. The method needs one random number per flight however many regions the flight crosses. In a uniform medium FREE-FLIGHT reduces to FREE-FLIGHT-UNIFORM.

## Example

**A uniform medium.** With $\Sigma_t = 2\ \mathrm{cm}^{-1}$ the mean free path is $0.5$ cm. The number $\xi = 0.5$ gives $s = \ln 2 / 2 = 0.346574$ cm, the median of the law. The number $\xi = 0.01$ gives $s = 2.302585$ cm, a flight of 4.6 mean free paths, which happens with probability 0.01.

**Two regions.** Region 0 is $[0, 1)$ with $\Sigma_0 = 0.5\ \mathrm{cm}^{-1}$ and region 1 is $[1, 3]$ with $\Sigma_1 = 2\ \mathrm{cm}^{-1}$. A particle starts at $x = 0$ with $\mu = 1$ and $\xi = 0.1$:

| line | region | $d$ (cm) | $\Sigma_i d$ | $\tau$ before | action |
|---|---|---|---|---|---|
| L3 | | | | 2.302585 | draw the depth |
| L6, L8 | 0 | 1 | 0.5 | 2.302585 | cross, $\tau \leftarrow 1.802585$ |
| L6, L7 | 1 | 2 | 4.0 | 1.802585 | collide at $1 + 1.802585/2 = 1.901293$ |

The total optical depth of the slab is $0.5 + 4 = 4.5$, so the particle escapes with probability $e^{-4.5} = 0.011109$. It collides in region 0 with probability $1 - e^{-0.5} = 0.393469$ and in region 1 with probability $e^{-0.5} - e^{-4.5} = 0.595422$. With $\mu = 0.5$ every path length doubles for the same depth in $x$, and the same $\xi$ gives the collision at $x = 1 + 0.5 \cdot 1.302585 / 2 = 1.325646$.

## Correctness

The claim is a theorem: for exact arithmetic and an exact uniform $\xi$, FREE-FLIGHT returns a collision point $x + \mu S$ whose path length $S$ satisfies $P(S > s) = e^{-\tau(s)}$ for every $s$ before the face, and it returns escape with probability $e^{-\tau_{\text{face}}}$. The reason is that $T = -\ln \xi$ has the exponential law with mean 1, $P(T > t) = e^{-t}$, and that the loop stops at the first path length $S$ with $\tau(S) = T$. Because $\tau$ is continuous and does not decrease, $S > s$ holds exactly when $T > \tau(s)$, which has probability $e^{-\tau(s)}$. The full proof is below.

## Complexity

In the [real RAM](/real-ram/) model, FREE-FLIGHT-UNIFORM costs $O(1)$: one random number and one logarithm. FREE-FLIGHT costs $O(1)$ per region crossed, so $O(M)$ for a flight that crosses $M$ regions, with $O(1)$ extra space. In three dimensions each crossing needs a distance to the surfaces of the current cell, which is usually the most expensive part of a transport code. Delta tracking removes these distance computations, but it takes about $\Sigma_{\max}/\Sigma$ tentative flights per real collision.

## Properties

- **Exact.** The sample has the exact law of the physical flight, with no discretization of the path.
- **Memoryless.** The exponential law has no memory: given that the particle has gone $s_0$ without collision, the rest of the flight has the same law. This is why the method can stop at a face and go on with the depth that is left.
- **One random number per flight.** The number of regions crossed does not change the number of random numbers.
- **Monotone in $\xi$.** A smaller $\xi$ always gives a longer flight. This is useful for correlated sampling, where two problems use the same random numbers.

## Variants and improvements

- **[Delta tracking](/delta-tracking/).** Fly with a majorant $\Sigma_{\max} \ge \Sigma(x)$ everywhere and accept a tentative collision with probability $\Sigma(x)/\Sigma_{\max}$. It suits geometries with many small cells, and it is the method of choice in volume rendering ([volumetric path tracing](/volumetric-path-tracing/)).
- **Continuously varying media.** If $\Sigma$ varies inside a region, solve $\tau(s) = T$ by integration and root finding, or use delta tracking.
- **[Exponential transform](/exponential-transform/).** Sample the flight with a modified cross section and correct the weight. This is a variance reduction method, not an analog flight.
- **Forced collision.** Sample the flight from the law conditioned on a collision inside a region, and multiply the weight by the collision probability. It gives collisions in thin regions.

## When to use it

Use free-flight sampling with optical depth accumulation in any Monte Carlo transport code with a geometry of cells with piecewise constant cross sections, which is the usual case in reactor physics and shielding. Use delta tracking when the geometry has many cells per mean free path, or when the cross section varies continuously. In a void, the flight goes straight to the next face.

## Pitfalls

- **The logarithm of zero.** Draw $\xi$ in $(0, 1]$, for example as $1 - u$ with $u$ from a generator in $[0, 1)$. A value $\xi = 0$ gives an infinite flight.
- **A new random number at each face.** Some codes draw a new $\xi$ at each face. By the memoryless property this is also correct, but it uses more random numbers and breaks correlated sampling. Mixing both methods in one flight, for example by keeping the old depth after a direction change, is wrong.
- **Path length and depth in $x$.** In slab geometry the path length is the change in $x$ divided by $|\mu|$. A code that forgets the factor $1/|\mu|$ gives flights that are too short for slanted particles.
- **A particle parallel to the faces.** With $\mu = 0$, line L5 gives an infinite distance. The flight ends with a collision in the current region if $\Sigma_i > 0$, and never ends in a void. The code must test this case.
- **Rounding on faces.** After line L9 the particle sits exactly on a face. A geometry code must place it in the next region and not in the region it left, or it can loop on the face.

## Implementations

## History

Free-flight sampling is as old as the Monte Carlo method. In 1947 von Neumann proposed to follow neutrons in a fission device one by one, with flight distances from the exponential law and collisions sampled from the cross sections, and the first such calculations ran at Los Alamos in the following years. Metropolis and Ulam described the method in 1949 with the neutron chain as their example. Woodcock and coworkers gave delta tracking in 1965 for reactor geometries with many regions.

## References
