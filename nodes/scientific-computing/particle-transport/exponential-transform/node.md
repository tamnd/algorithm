---
tag: 4R5WT6
kind: technique
slug: exponential-transform
name: Exponential transform
aliases:
- path stretching
area: scientific-computing/particle-transport
level: advanced
summary: Biases the free-flight distribution to stretch paths in a preferred direction and corrects the weight, for deep penetration problems.
prereqs: [free-flight-sampling, importance-sampling, analog-monte-carlo-transport]
see_also: [free-flight-sampling, importance-sampling, weight-window, implicit-capture, particle-splitting, adjoint-importance-function, cadis, variance]
sources:
  - book: isbn:9780849360749
    title: Ivan Lux and Laszlo Koblinger, Monte Carlo Particle Transport Methods, Neutron and Photon Calculations, CRC Press, 1991
    locator: the treatment of biased path length sampling and the exponential transform among the non-analog games
  - book: isbn:9780486462936
    title: Jerome Spanier and Ely M. Gelbard, Monte Carlo Principles and Neutron Transport Problems, Addison-Wesley, 1969, Dover reprint 2008
    locator: the chapters on non-analog random walks and on the exponential transformation
  - book: isbn:9783527407606
    title: Malvin H. Kalos and Paula A. Whitlock, Monte Carlo Methods, second edition, Wiley-VCH, 2008
    locator: Chapter 6, on radiation transport, with importance sampling of the flight distance
---

The exponential transform changes the law of the free flight in a Monte Carlo transport code. Instead of the true total cross section $\Sigma_t$, the flight distance is sampled with the biased cross section $\Sigma^* = \Sigma_t (1 - p\mu)$, where $\mu$ is the cosine between the flight direction and a preferred direction (toward the detector) and $0 \le p < 1$ is a parameter. Flights toward the detector get longer and flights away from it get shorter, and the weight of the particle is multiplied by the ratio of the true density to the biased one, so every tally keeps its mean. It is [importance sampling](/importance-sampling/) of the flight distance. For a beam in a pure absorber it can reach zero variance, but with scattering a large $p$ gives an infinite variance, so it is used with care, usually together with [implicit capture](/implicit-capture/) and [weight windows](/weight-window/).

## In plain words

A particle that must get through a thick wall to reach a detector usually stops early. The exponential transform cheats: it lets particles that fly toward the detector go further than they really would, and makes particles that fly away stop sooner.

To stay honest, each particle keeps a weight. A particle that was helped to go far gets a smaller weight, and one that was held back gets a larger weight. On average, the weights undo the cheating exactly.

The danger is the particles that move away from the detector and are then turned back by a collision. Their weights can grow very large. If the cheating is too strong, a few such particles decide the whole result, and the error estimate becomes wrong.

## When it applies

- Deep penetration: the tally is many mean free paths away from the source in one main direction, and the [importance](/adjoint-importance-function/) grows about exponentially in that direction.
- The medium absorbs a fair part of the particles at each collision, or the transform is used only in the thick part of the geometry.
- The code carries weights and has a way to control them, such as a [weight window](/weight-window/) or a weight cutoff with roulette.

It does not apply in voids or thin regions, where there are almost no collisions to bias, nor where the importance does not have one main direction, for example a detector that particles reach from many sides.

## The template

The template replaces the flight of [free-flight sampling](/free-flight-sampling/) in one cell. The holes are the preferred direction and the parameter $p$.

```pseudo id=main
EXPONENTIAL-TRANSFORM-FLIGHT(x, Ω, w)
L1  μ ← Ω · u                              ▷ hole: the preferred direction u
L2  Σ* ← Σt (1 - p μ)                      ▷ hole: the parameter p, with 0 ≤ p < 1
L3  s ← -ln(ξ) / Σ*                         ▷ ξ uniform in (0, 1]
L4  d ← the distance to the cell boundary along Ω
L5  if s ≥ d then w ← w · exp(-(Σt - Σ*) d), and the particle crosses the boundary
L6  else w ← w · (Σt / Σ*) · exp(-(Σt - Σ*) s), and the particle collides at x + s Ω
```

Line L5 uses the ratio of the probabilities to reach the boundary, $e^{-\Sigma_t d} / e^{-\Sigma^* d}$. Line L6 uses the ratio of the densities of a collision at $s$, $\Sigma_t e^{-\Sigma_t s} / (\Sigma^* e^{-\Sigma^* s})$.

**The mean does not change.** This is a theorem. Let $f$ be the weight factor of one flight. Over the two outcomes,
$$E[f \cdot g] = \int_0^d \Sigma^* e^{-\Sigma^* s} \cdot \frac{\Sigma_t e^{-\Sigma_t s}}{\Sigma^* e^{-\Sigma^* s}}\, g(s)\, ds + e^{-\Sigma^* d} \cdot \frac{e^{-\Sigma_t d}}{e^{-\Sigma^* d}}\, g(d) = \int_0^d \Sigma_t e^{-\Sigma_t s} g(s)\, ds + e^{-\Sigma_t d} g(d)$$
for any function $g$ of the outcome, which is the analog expectation. So each flight is an importance sampling step with the correct weight, and by induction over the flights every linear tally keeps its mean. This needs $\Sigma^* > 0$, which holds for $p < 1$.

## Classic examples

**A beam through a pure absorber.** A beam enters a pure absorber of optical thickness $\tau = \Sigma_t L = 10$ along $u$, so $\mu = 1$ and $\Sigma^* = \Sigma_t(1 - p)$. The particle gets through with probability $e^{-(1 - p)\tau}$, and then it has the weight $e^{-\tau}/e^{-(1 - p)\tau} = e^{-p\tau}$. The score is $e^{-p\tau}$ with probability $e^{-(1 - p)\tau}$ and 0 otherwise. Its mean is $e^{-\tau} = 4.540 \times 10^{-5}$ for every $p$, and its relative variance per history is $e^{(1 - p)\tau} - 1$:

| $p$ | probability to get through | relative variance per history |
|---|---|---|
| 0 (analog) | $4.54 \times 10^{-5}$ | 22 025 |
| 0.5 | 0.00674 | 147.4 |
| 0.9 | 0.368 | 1.718 |
| 0.99 | 0.905 | 0.105 |

As $p \to 1$ every particle gets through with the exact weight $e^{-\tau}$, which is a zero variance game. Here the importance grows like $e^{\Sigma_t x}$, and $p = 1$ makes the stretched flight follow it exactly.

**An infinite medium with scattering: infinite variance.** This is a theorem, with a short proof. Take an infinite medium with isotropic scattering and scattering ratio $c$, a source with an isotropic direction, analog absorption, and the tally $S$ = the sum of the weights at all collisions, whose mean is $1/(1 - c)$ in every game. With the transform, the weight factor of a flight in the direction $\mu$ is $f = e^{-p\Sigma_t \mu s}/(1 - p\mu)$, and
$$E[f^2 \mid \mu] = \int_0^\infty \Sigma^* e^{-\Sigma^* s} \frac{e^{-2p\Sigma_t\mu s}}{(1 - p\mu)^2}\, ds = \frac{\Sigma^*}{(1 - p\mu)^2 (\Sigma^* + 2p\Sigma_t\mu)} = \frac{1}{1 - p^2\mu^2}.$$
With $\mu$ uniform on $[-1, 1]$, $g = E[f^2] = \operatorname{artanh}(p)/p$, and $E[f] = 1$. The weight at collision $k$ is a product of $k$ independent factors, so $E[W_k^2] = g^k$ and $E[W_j W_k] = g^j$ for $j < k$. Collision $k$ happens with probability $c^{k - 1}$. Summing,
$$E[S^2] = \sum_{k \ge 1} g^k c^{k - 1} + 2 \sum_{j \ge 1} g^j \sum_{k > j} c^{k - 1} = \frac{g (1 + c)}{(1 - c)(1 - cg)},$$
if $cg < 1$, and $E[S^2] = \infty$ if $cg \ge 1$. For $p = 0$, $g = 1$ and this is the second moment $(1 + c)/(1 - c)^2$ of the geometric number of collisions. The variance is infinite for $c \ge p/\operatorname{artanh}(p)$:

| $p$ | 0.3 | 0.5 | 0.7 | 0.9 | 0.99 |
|---|---|---|---|---|---|
| $g = \operatorname{artanh}(p)/p$ | 1.0317 | 1.0986 | 1.2390 | 1.6358 | 2.6734 |
| largest $c$ with finite variance | 0.969 | 0.910 | 0.807 | 0.611 | 0.374 |

The cause is the flights with $\mu < 0$: they are made short, but if they are long anyway, the factor $e^{p\Sigma_t|\mu|s}$ is huge.

**The sample variance can be wrong even when the variance is finite.** In the same medium with $c = 0.5$, $10^5$ histories (`random.Random(4)`) give the mean $1.9954$ and the sample second moment $7.202$ for $p = 0.5$ (exact $7.313$), and the mean $1.9860$ and the sample second moment $13.80$ for $p = 0.9$ (exact $26.95$). Both variances are finite, but the same computation with $f^4$ gives $\Sigma^* + 4p\Sigma_t\mu$ in the denominator, which is negative for $\mu$ near $-1$ when $p > 1/3$, so $E[f^4] = \infty$ for one flight. The variance of the variance is then infinite, and the sample variance underestimates the true one in most runs (a measurement for these seeds, explained by the infinite fourth moment).

**Deep penetration in practice.** In shielding codes the transform is used in the thick layers of a shield, with $p$ chosen so that $p\Sigma_t$ is close to the rate at which the importance grows toward the detector, together with [implicit capture](/implicit-capture/) to keep the stretched particles alive and a [weight window](/weight-window/) to remove the heavy backward particles. This choice of $p$ is a rule of thumb from the beam example. Methods that use an adjoint solve, such as [CADIS](/cadis/), often replace it by windows alone.

## Variations

- **A fixed stretching rate.** $\Sigma^* = \Sigma_t - \kappa\mu$ with a constant $\kappa$ instead of $p\Sigma_t$, matched to the decay rate of the importance.
- **With angle biasing.** The direction after a collision is also biased toward $u$, with its own weight factor, so that more flights are stretched. This raises the risk of large weights further.
- **Local transforms.** Different $u$ and $p$ in different cells, or a transform only in the cells of the shield.
- **Forced collisions and path length biasing in thin cells.** The opposite case: the flight is biased to collide in a thin region instead of passing through it.
- **Transforms from an adjoint.** The parameters can come from the gradient of an approximate adjoint, as in some automated variance reduction schemes.

## Pitfalls

- **Infinite variance.** With scattering, a $p$ above the limit of the table makes the variance infinite. The run still prints a mean and an error, and the error looks fine. Use a weight window or a weight cutoff with roulette, and check the largest scores.
- **Unreliable error bars.** Even with a finite variance, the fourth moment can be infinite for $p > 1/3$, so the estimated error and its convergence can be far off. Check the variance of the variance.
- **The wrong weight at a boundary.** At a boundary crossing the factor is $e^{-(\Sigma_t - \Sigma^*)d}$, not the density ratio of line L6. Using the density ratio there biases the tally.
- **Preferred direction that is wrong.** If the importance grows in another direction, the transform pushes particles the wrong way, and the variance rises.
- **$p$ close to 1 with scattering.** Backward flights get $\Sigma^* = \Sigma_t(1 + p|\mu|)$, so they are very short, and the few long ones carry enormous weights.

## Exercises

1. Show that $E[f] = 1$ for one flight in a cell of finite thickness, with both outcomes of lines L5 and L6.
2. Derive $E[f^2 \mid \mu] = 1/(1 - p^2\mu^2)$ and its average over $\mu$.
3. Derive the second moment of $S$ in the infinite medium, and find the largest $c$ with a finite variance for $p = 0.8$.
4. In the beam example, show that the relative variance $e^{(1 - p)\tau} - 1$ is the analog value for a slab of optical thickness $(1 - p)\tau$.
5. Show that $E[f^4 \mid \mu] = \infty$ for $\mu = -1$ when $p \ge 1/3$, and explain what this means for the error bar of a run.

## References
