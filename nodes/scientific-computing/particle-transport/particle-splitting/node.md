---
tag: FYFXVN
kind: technique
slug: particle-splitting
name: Particle splitting
aliases:
- geometry splitting
area: scientific-computing/particle-transport
level: core
summary: Splits a particle entering an important region into n copies of weight w/n, paired with Russian roulette in less important regions.
prereqs: [analog-monte-carlo-transport, russian-roulette]
see_also: [weight-window, russian-roulette, adjoint-importance-function, implicit-capture, subset-simulation, forward-flux-sampling, resampling, cadis]
sources:
  - paper: "Herman Kahn and Theodore E. Harris, Estimation of particle transmission by random sampling, National Bureau of Standards Applied Mathematics Series 12, 1951, 27-30"
    locator: splitting and Russian roulette as ways to estimate the transmission of particles through a shield
  - book: isbn:9780849360749
    title: Ivan Lux and Laszlo Koblinger, Monte Carlo Particle Transport Methods, Neutron and Photon Calculations, CRC Press, 1991
    locator: the chapter on non-analog games, with splitting and Russian roulette and the proof that they keep the expected score
  - book: isbn:9780486462936
    title: Jerome Spanier and Ely M. Gelbard, Monte Carlo Principles and Neutron Transport Problems, Addison-Wesley, 1969, Dover reprint 2008
    locator: the chapters on non-analog random walks and on importance and variance reduction
  - book: isbn:9783527407606
    title: Malvin H. Kalos and Paula A. Whitlock, Monte Carlo Methods, second edition, Wiley-VCH, 2008
    locator: Chapter 6, on radiation transport and the variance reduction methods used there
---

Particle splitting replaces one Monte Carlo particle of weight $w$ by $n$ copies of weight $w/n$ when it moves into a region where particles are more likely to score. Each copy then continues its own random walk. In regions of lower importance, [Russian roulette](/russian-roulette/) does the opposite: it ends the particle with some probability and raises the weight of the survivors. Both operations keep the expected score of every tally, so the method is unbiased, and the copies sample the important part of phase space more often. The splitting ratio at a surface comes from the [importance](/adjoint-importance-function/) of the two sides; the method is also called geometry splitting when the ratios are set per cell.

## In plain words

Suppose only one particle in a thousand gets through a wall to a detector. Most of the simulation time goes to particles that die in the wall. With splitting, the wall is cut into layers. Each time a particle gets through one layer, it is copied, for example into two. Each copy counts for half of the original. More copies reach the far side, and each one counts for less, so the average count stays the same, but it is less random.

Going the other way, a particle that moves into a layer that does not matter plays a game of chance. It may stop, or it may go on and count for more. This saves time without changing the average. The art is to choose how many copies to make at each layer.

## When it applies

- The tally is in a region that few particles reach: deep penetration through a shield, a small detector, a duct or a gap. The [importance](/adjoint-importance-function/) of a particle grows by a large factor between the source and the tally.
- The geometry can be cut into cells or layers so that the importance changes by a factor of about 2 to 4 between neighboring cells. The cells then carry importances $I_j$, and a particle that moves from cell $i$ into cell $j$ splits or plays roulette with the ratio $I_j/I_i$.
- The code carries weights and a bank of particles that wait to be followed.

Splitting does not help when the importance is about the same everywhere, or when it changes mostly with the direction or the energy and not with the position. Then the [exponential transform](/exponential-transform/) or a [weight window](/weight-window/) with energy bins fits better.

## The template

The template is the action at a surface between two cells. The holes are the importances and the rule that turns a non-integer ratio into a number of copies.

```pseudo id=main
SPLIT-OR-ROULETTE(particle with weight w, from cell i into cell j)
L1  r ← I_j / I_i                                ▷ hole: the importances of the cells
L2  if r > 1 then
L3      n ← ⌊r⌋, and n ← n + 1 with probability r - ⌊r⌋   ▷ hole: random or fixed rounding
L4      put n copies with weight w / r and the same position, direction and energy in the bank
L5  else if r < 1 then
L6      with probability r the particle goes on with weight w / r, else it ends
L7  else the particle goes on unchanged
```

With an integer ratio $n$, line L3 is $n$ copies of weight $w/n$. The variant with random rounding keeps the mean for any real ratio, because $E[n] \cdot w/r = r \cdot w/r = w$.

**The mean does not change.** This is a theorem. Let $V(P)$ be the expected score of a particle of unit weight at the phase-space point $P$, with all its descendants. The expected score of a particle of weight $w$ is $w V(P)$, because every tally is linear in the weight. After the split the expected score is $E[n] \cdot (w/r) \cdot V(P) = w V(P)$, and after the roulette it is $r \cdot (w/r) \cdot V(P) = w V(P)$. The copies are then independent random walks, so by induction over the splits and roulettes, the expected score of a source particle is the same as in the analog game.

**Splitting never raises the variance per history.** This is also a theorem, for a split into a fixed number $n$ of copies. Let $\mathcal{F}$ be the history up to the split and $S$ the total score. The law of total variance gives $\mathrm{Var}(S) = \mathrm{Var}(E[S \mid \mathcal{F}]) + E[\mathrm{Var}(S \mid \mathcal{F})]$. The split does not change $E[S \mid \mathcal{F}]$, and the score after the split is the mean of $n$ conditionally independent copies, so the second term is divided by $n$. Roulette has the opposite effect: it adds variance and saves time. Whether the product of variance and cost goes down is a question of the problem, so the gain is a measurement.

**The ratio.** This is a rule of thumb. If the ratio across each surface equals the ratio of the importances, the expected number of particles in each cell stays about constant from the source to the tally, which keeps both the work and the weights under control. A larger ratio makes the population grow, a smaller one lets it die out before the tally.

## Classic examples

**Two cells by hand.** A pure absorber slab of two cells, each one mean free path thick, with a beam at the left face. The tally is the transmission, $T = e^{-2} = 0.135335$. Let $p = e^{-1}$ be the chance to cross one cell. In the analog game the score is 1 with probability $p^2$, so the variance per history is $p^2(1 - p^2) = 0.117020$, and a history has $1 + p = 1.3679$ flights on average (one in the first cell, one more if it gets through). With a split into $n$ copies of weight $1/n$ at the inner surface, the score is the fraction of the $n$ copies that cross the second cell, if the first one got through. So $E[S^2] = p \cdot (np + n(n-1)p^2)/n^2 = (p^2 + (n-1)p^3)/n$, and there are $1 + np$ flights per history. The figure of merit per flight, $1/(R^2 \cdot \text{flights})$, with $R^2$ the relative variance per history:

| $n$ | variance per history | relative variance | flights per history | FOM per flight |
|---|---|---|---|---|
| 1 (analog) | 0.117020 | 6.389 | 1.3679 | 0.1144 |
| 2 | 0.074246 | 4.054 | 1.7358 | 0.1421 |
| 3 | 0.059988 | 3.275 | 2.1036 | 0.1451 |
| 4 | 0.052858 | 2.886 | 2.4715 | 0.1402 |
| 5 | 0.048581 | 2.652 | 2.8394 | 0.1328 |

The variance falls with $n$ every time, as the theorem says, but the cost rises, and the best integer ratio is 3. The importance ratio of the two cells is $e = 2.718$ (see the beam example on the [importance](/adjoint-importance-function/) page), so the rule of thumb picks the right ratio. A run with $2 \times 10^5$ histories (`random.Random(1)`) gives $0.13488$ with a variance of $0.11668$ for the analog game and $0.13415$ with $0.07362$ for $n = 2$, which agrees with the table.

**A deep shield.** The same absorber with 10 cells of one mean free path has $T = e^{-10} = 4.540 \times 10^{-5}$. The analog game has the relative variance $(1 - T)/T = 22\,025$ and $1.582$ flights per history, so its figure of merit per flight is $2.87 \times 10^{-5}$. With a split of ratio $e$ at every surface (2 or 3 copies by random rounding), a run with $2 \times 10^4$ histories (`random.Random(2)`) gives $T = 4.589 \times 10^{-5}$ with a standard error of $0.136 \times 10^{-5}$, a relative variance of $17.5$ per history and $10.1$ flights per history. The figure of merit per flight is $5.6 \times 10^{-3}$, about 200 times the analog value (a measurement on this toy). The number of particles stays about 1 per cell, as the rule of thumb predicts.

**Rare events outside transport.** The same idea, under the name of multilevel or importance splitting, estimates small probabilities in queues, in reliability and in molecular simulation. [Forward flux sampling](/forward-flux-sampling/) splits trajectories at a sequence of interfaces between two states, and [subset simulation](/subset-simulation/) restarts Markov chains from the samples that reached the last level. The resampling step of a [particle filter](/particle-filter/) splits heavy particles and removes light ones in the same way.

## Variations

- **Cell importances.** Each cell has an importance $I_j$, and the ratio at a surface is $I_j/I_i$. This is geometry splitting in the narrow sense, as in many production codes.
- **Weight windows.** The [weight window](/weight-window/) decides by the weight of the particle, not by the surface it crosses, and splits or plays roulette until the weight is inside a band. It also controls weights that other methods produce.
- **Energy and angle splitting.** The importances depend on energy bins or direction bins, and the split happens when a collision moves the particle into a more important bin.
- **Importances from an adjoint solve.** [CADIS](/cadis/) computes the importances from a deterministic adjoint calculation instead of guessing them.
- **Fixed effort splitting.** In rare-event simulation, a fixed number of copies is started at each level, whatever number of particles reached it, which keeps the work per level constant.

## Pitfalls

- **Population explosion.** A ratio larger than the importance ratio, repeated over many cells, makes the number of particles grow geometrically. The run then spends its time in one history.
- **Errors per copy instead of per history.** The copies of one source particle are correlated. The variance must use the total score of each source history, with all its copies, not the score of each copy.
- **Importance that changes inside a cell.** Splitting acts only at the surfaces. If the importance changes by a factor of 100 inside one cell, the population there still falls by that factor.
- **Splitting in direction, not in space.** Copies that start at the same point with the same direction are strongly correlated in their first flight. If the importance depends on the direction, splitting at a surface wastes copies that move away from the tally.
- **Roulette back and forth.** A particle that crosses a surface many times plays roulette each time it moves to the less important side. The game stays unbiased, but it can spend more time than it saves.

## Exercises

1. In the two-cell example, derive $E[S^2] = (p^2 + (n - 1)p^3)/n$ and find the real $n$ that maximizes the figure of merit per flight.
2. Show that with the ratio $r$ at each surface of a pure absorber with cells of optical thickness $\tau$, the expected number of particles in cell $k$ is $(r e^{-\tau})^k$. Which $r$ keeps it constant?
3. Show that roulette with survival probability $r$ and weight $w/r$ adds the variance $w^2 V^2 (1 - r)/r$ to a particle with a deterministic future score $wV$.
4. Give a geometry in which splitting at a surface raises the variance of a tally per unit of work.
5. Explain why random rounding of a non-integer ratio adds variance compared to a fixed integer ratio, and when it is still the better choice.

## References
