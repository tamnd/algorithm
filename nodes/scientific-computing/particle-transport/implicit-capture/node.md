---
tag: PNSAK6
kind: technique
slug: implicit-capture
name: Implicit capture
aliases:
- survival biasing
area: scientific-computing/particle-transport
level: core
summary: Never kills a particle at absorption but multiplies its weight by the scattering probability, which lowers the variance of tallies.
prereqs: [analog-monte-carlo-transport, russian-roulette]
see_also: [russian-roulette, particle-splitting, weight-window, exponential-transform, collision-estimator, track-length-estimator, importance-sampling, implicit-monte-carlo]
sources:
  - book: isbn:9780849360749
    title: Iván Lux and László Koblinger, Monte Carlo Particle Transport Methods, Neutron and Photon Calculations, CRC Press, 1991
    locator: the chapters on non-analog games and variance reduction (weights, survival biasing, Russian roulette and splitting)
  - book: isbn:9780486462936
    title: Jerome Spanier and Ely M. Gelbard, Monte Carlo Principles and Neutron Transport Problems, Dover edition, 2008
    locator: the chapters on non-analog random walks and the unbiasedness of weighted estimators
  - book: isbn:9783527407606
    title: Malvin H. Kalos and Paula A. Whitlock, Monte Carlo Methods, second edition, Wiley-VCH, 2008
    locator: Chapter 6, on radiation transport, with weights and the expected value of absorption
---

Implicit capture changes one step of [analog Monte Carlo transport](/analog-monte-carlo-transport/). In the analog game, a particle that collides is absorbed with probability $\Sigma_a/\Sigma_t$ and its history ends. With implicit capture, the particle always survives the collision, and its weight is multiplied by the survival probability $c = \Sigma_s/\Sigma_t$. The expected weight that leaves each collision is the same in both games, so every tally keeps its mean. The variance changes because an absorption, which is a random event worth all or nothing, is replaced by its expected value. Since weights now only decrease, the history never ends by itself, and implicit capture is always used together with [Russian roulette](/russian-roulette/) below a weight cutoff. It is one of the oldest and most common variance reduction methods of neutron and photon Monte Carlo.

## In plain words

In a normal simulation, a particle that hits an atom is either swallowed or bounces on. If half of the hits swallow the particle, half of the particles stop at each hit.

With implicit capture, no particle is ever swallowed. Instead, each particle carries a weight, which says how much of a real particle it stands for. At each hit, it bounces on, but its weight is cut in half. On average, the same amount of particle goes on as before.

When the weight gets very small, the particle is not worth the work to follow. Then a coin decides: either it stops, or it goes on with a larger weight. The coin is set so that, on average, nothing is lost.

## When it applies

- The medium absorbs a fair fraction at each collision, $c$ clearly below 1, and the tally is far from the source: leakage, transmission, or a detector behind an absorber. The analog game loses most histories before they reach the tally.
- The tally is an absorption rate. Then each collision can score its expected absorption $w\,\Sigma_a/\Sigma_t$ instead of a random all-or-nothing event.
- The code already carries particle weights for other methods, such as [splitting](/particle-splitting/), [weight windows](/weight-window/) or the [exponential transform](/exponential-transform/).

It does not apply directly when the physics at the collision is more than survive or die: fission and $(n, 2n)$ reactions make several particles, and the weight factor must then be the expected number of particles that leave the collision.

## The template

The template replaces the absorption step of the analog collision. The holes are the weight factor and the roulette parameters.

```pseudo id=main
IMPLICIT-CAPTURE-COLLISION(w)
L1  score collision tallies with w;  score absorption tallies with w · Σa/Σt
L2  w ← w · Σs/Σt                            ▷ hole: the expected number of particles that leave
L3  if w < w_low then                        ▷ hole: the cutoff w_low and the survival weight w_s
L4      draw u uniform in [0, 1);  if u < w / w_s then w ← w_s
L5      else end the history
L6  sample the new direction and energy as in the analog game
```

Typical choices are $w_s$ a little below the source weight and $w_{\mathrm{low}}$ a fraction of $w_s$, for example $w_s = 0.5$ and $w_{\mathrm{low}} = 0.25$ for a source weight of 1. With a [weight window](/weight-window/), the window replaces the roulette.

**Why the mean does not change.** This is a theorem. Let $W$ be the weight that leaves one collision. In the analog game $W = w$ with probability $c$ and $W = 0$ otherwise, so $E[W] = cw$. With implicit capture $W = cw$ exactly. Russian roulette keeps $E[W]$, because $(w/w_s) \cdot w_s = w$. By induction over collisions, the expected weight that reaches every point of phase space is the same in both games, and so is the expected score of every tally that is linear in the weight, which includes the [collision](/collision-estimator/) and [track-length](/track-length-estimator/) estimators.

**Why the variance usually falls.** This is a heuristic. The analog game spends randomness on the decision to absorb; implicit capture replaces that decision by its expected value, which by the law of total variance cannot increase the variance of what happens at that collision. The roulette adds randomness back, and the longer histories cost more time. So the gain per unit of work depends on the problem and must be measured.

## Classic examples

**Transmission through a slab.** A normal beam enters a slab with $\Sigma_t L$ mean free paths and isotropic scattering with survival probability $c$. The tally is the transmitted weight. With $10^5$ histories (`random.Random(5)`), $w_{\mathrm{low}} = 0.25$ and $w_s = 0.5$, the runs give (measurements):

| $\Sigma_t L$ | $c$ | analog $T$ | implicit capture $T$ | variance per history, analog | variance per history, implicit | collisions per history, analog | collisions per history, implicit |
|---|---|---|---|---|---|---|---|
| 2 | 0.5 | 0.1892 | 0.1897 | 0.1534 | 0.1228 | 1.40 | 2.22 |
| 5 | 0.5 | 0.0130 | 0.0129 | 0.0129 | 0.0091 | 1.74 | 2.95 |
| 5 | 0.9 | 0.0772 | 0.0765 | 0.0713 | 0.0374 | 5.12 | 8.40 |
| 2 | 0.2 | 0.1482 | 0.1484 | 0.1263 | 0.1190 | 1.02 | 1.18 |

The means agree within their errors. The variance per history always falls, by a factor from 1.06 to 1.9. But histories are longer, and if the cost is taken as one plus the number of collisions, the product of variance and cost falls only for $\Sigma_t L = 5$, $c = 0.9$ (by about 20%), and is a little worse in the other three cases. With only an absorber and transmission, implicit capture is not a large gain by itself; it pays when it is combined with methods that push particles toward the tally.

**Absorption tally in an infinite medium.** In an infinite medium with $c = 0.5$, a particle collides $1/(1 - c) = 2$ times on average and is absorbed once. The analog estimate of the absorption per source particle is always 1, with zero variance. With implicit capture, each collision scores $w(1 - c)$, and without roulette the total is $\sum_k c^k(1 - c) = 1$, again with zero variance, but only after an infinite history; with roulette the total is random with mean 1. This is a case where implicit capture can only add noise.

**Deep penetration with the exponential transform.** In shielding problems, the [exponential transform](/exponential-transform/) stretches flight paths toward the detector and changes weights; implicit capture keeps the stretched particles alive through the absorbing shield. The two together, with weight windows to control the weights, are the standard method of deep penetration.

## Variations

- **Continuous absorption.** Instead of a factor at each collision, the weight is reduced along the path by $e^{-\Sigma_a s}$, and collisions are sampled with $\Sigma_s$ only. Implicit Monte Carlo uses this to lower the noise of the absorbed energy.
- **Expected fission.** In a criticality code, a collision produces fission sites with the expected number $w\,\nu\Sigma_f/\Sigma_t$ instead of a random reaction choice, and the particle continues with weight $w\,\Sigma_s/\Sigma_t$.
- **Forced collision.** In a thin region the particle is split into an uncollided part with weight $w e^{-\tau}$ and a part forced to collide with weight $w(1 - e^{-\tau})$; it is the analogous expected-value idea for the flight instead of the collision.
- **Weight windows.** The window splits heavy particles and plays roulette with light ones in each region, so that the weight stays near a target given by an [importance](/adjoint-importance-function/) estimate.

## Pitfalls

- **No roulette.** Without a weight cutoff, a history in a medium with no leakage never ends.
- **A roulette that is too strict.** A high cutoff ends histories that would reach the tally, and the variance grows back toward the analog value; a low cutoff wastes time on tiny weights.
- **Integer counts.** Tallies of the number of absorptions or of particles that cross a surface must sum weights, not count particles.
- **Large weights in the tally.** If other methods raise weights, a few heavy particles can dominate a tally. Check the variance of the variance or the largest score.
- **Nonlinear tallies.** Pulse-height tallies, which bin the total energy a history deposits in a detector, are not linear in the weight; implicit capture biases them unless the code treats the history as a whole.

## Exercises

1. Show that with implicit capture and no roulette, in an infinite medium, the weight after $k$ collisions is $c^k$ and the expected number of collisions per unit source weight, $\sum_k c^k$, equals $1/(1 - c)$, as in the analog game.
2. For the roulette with survival weight $w_s$, compute the variance that one roulette adds to a particle of weight $w < w_s$. When is it smallest?
3. In the slab table, repeat the runs with $w_{\mathrm{low}} = 0.05$ and $w_{\mathrm{low}} = 0.5$ and compare the variance per history and the cost.
4. Give an example of a tally for which implicit capture increases the variance.
5. Write the factor that replaces $\Sigma_s/\Sigma_t$ when a collision can also be an $(n, 2n)$ reaction with cross section $\Sigma_{2n}$.

## References
