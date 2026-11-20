---
tag: 74M0XF
kind: technique
slug: weight-window
name: Weight window
aliases:
- weight windows
area: scientific-computing/particle-transport
level: core
summary: Keeps particle weights within bounds set for each region and energy, splitting heavy particles and playing roulette with light ones.
prereqs: [particle-splitting, implicit-capture]
see_also: [particle-splitting, russian-roulette, implicit-capture, adjoint-importance-function, cadis, fw-cadis, exponential-transform, analog-monte-carlo-transport]
sources:
  - paper: "Thomas E. Booth and John S. Hendricks, Importance estimation in forward Monte Carlo calculations, Nuclear Technology/Fusion 5(1), 1984, 90-100"
    locator: the weight window generator, which estimates the importance of each phase-space cell from a forward run and sets the window bounds from it
  - paper: "Thomas E. Booth, Genesis of the weight window and the weight window generator in MCNP, a personal history, Los Alamos National Laboratory report LA-UR-06-5807, 2006"
    locator: the origin of the weight window at Los Alamos in the late 1970s and its first publications
  - paper: doi:10.13182/NSE98-2
    title: John C. Wagner and Alireza Haghighat, Automated variance reduction of Monte Carlo shielding calculations using the discrete ordinates adjoint function, Nuclear Science and Engineering 128(2), 1998, 186-208
    locator: the window bounds from the adjoint function, the ratio of the upper to the lower bound, and the consistency of the windows with the biased source
  - book: isbn:9780849360749
    title: Ivan Lux and Laszlo Koblinger, Monte Carlo Particle Transport Methods, Neutron and Photon Calculations, CRC Press, 1991
    locator: the chapter on non-analog games, splitting and Russian roulette
---

A weight window is a band of weights $[w_L, w_U]$ attached to each cell of phase space: a region of space, often also an energy bin or a time bin. When a Monte Carlo particle is in a cell and its weight is above the band, it is split into copies with smaller weights; when its weight is below the band, it plays [Russian roulette](/russian-roulette/), and a survivor gets a weight inside the band. Both moves keep the expected score, so the method is unbiased. The bands are set low where particles are important and high where they are not, so the method does the work of [particle splitting](/particle-splitting/) and also keeps the weight spread under control that [implicit capture](/implicit-capture/), source biasing and the [exponential transform](/exponential-transform/) produce. Weight windows came from Los Alamos in the late 1970s (Booth 2006), and they are now the main variance reduction tool of production transport codes.

## In plain words

Each simulated particle carries a weight: how much of a real particle it stands for. A weight window is a rule that says, for each place and energy, which weights are normal.

If a particle is much heavier than normal, it is cut into several lighter copies, which together weigh the same. If it is much lighter than normal, a coin decides: either it is removed, or it goes on with a normal weight. The coin is fair, so on average nothing is lost or gained.

Near the detector the normal weight is small, so there are many light particles there. Far from the detector the normal weight is large, so there are few heavy particles. The work goes to where it matters.

## When it applies

- An [importance](/adjoint-importance-function/) estimate exists or can be made, from a deterministic adjoint solve ([CADIS](/cadis/)), from a forward Monte Carlo run (the weight window generator), or from experience.
- The importance changes in space and also in energy or direction. A splitting surface sees only space; a window can have energy bins.
- Other non-analog methods are in use and produce a wide spread of weights. A window removes very light particles that cost time and splits very heavy particles that would dominate a tally.
- Several tallies or a mesh tally must be good at the same time, with windows from [FW-CADIS](/fw-cadis/).

## The template

The template is the check that the code makes when a particle enters a new cell, after a collision, or both. The holes are the bounds, where they come from and where the check is made.

```pseudo id=main
WEIGHT-WINDOW-CHECK(particle with weight w in window cell j)
L1  (w_L, w_U, w_S) ← the bounds of cell j       ▷ hole: w_L proportional to 1 / I_j, w_U = c_u w_L
L2  if w > w_U then
L3      n ← min(⌈w / w_U⌉, n_max)                  ▷ hole: the cap n_max on copies per check
L4      continue with n copies of weight w / n, put n - 1 of them in the bank
L5  else if w < w_L then
L6      with probability w / w_S continue with weight w_S, else end the history
L7  else continue unchanged
```

A common choice is $c_u = w_U/w_L = 5$, with the survival weight $w_S$ between the bounds. The CADIS paper of Wagner and Haghighat (1998) sets a target weight $\bar w_j = R/\phi^+_j$ from the adjoint flux $\phi^+_j$ of the cell and the estimated response $R$, and centers the window on it: $w_L = 2\bar w_j/(c_u + 1)$, $w_U = c_u w_L$ and $w_S = \bar w_j$. These values are rules that the sources found to work, not results of an optimization.

**The mean does not change.** This is a theorem. The split replaces a weight $w$ by $n$ copies of weight $w/n$, for any $n \ge 1$, so the expected score $w V(P)$ of the particle at the point $P$ stays the same. The roulette gives $(w/w_S) \cdot w_S \cdot V(P) = w V(P)$. The cap $n_{\max}$ does not change this, since the copies still share the weight $w$; a particle that is still above the window after a capped split is split again at the next check.

**Why the variance falls.** This is a heuristic. If every particle in cell $j$ had exactly the weight $R/I_j$, where $I_j$ is the importance, then every particle would carry the same expected score $R$, and the score of a history would not depend on where its particles go. With the exact importance this leads to the zero variance game of the [CADIS](/cadis/) proof. A window of finite width with an approximate importance keeps the game close to this case.

## Classic examples

**The window game by hand.** Let a cell have $w_L = 1$, $w_U = 5$ and $w_S = 3$. A particle with $w = 12$ is split into $\lceil 12/5 \rceil = 3$ copies of weight 4, and $3 \cdot 4 = 12$. A particle with $w = 0.6$ survives with probability $0.6/3 = 0.2$ and then has weight 3, so its expected weight is $0.2 \cdot 3 = 0.6$; with the random number $0.19$ it survives, with $0.21$ it ends. A particle with $w = 2$ goes on unchanged. The roulette adds the variance $0.2 \cdot 3^2 - 0.6^2 = 1.44$ to the weight, which is the cost of the saved time.

**Windows from importances, by hand.** In a pure absorber of two cells of one mean free path each, with a beam at the left and the transmission $T = e^{-2}$ as the tally, the importance of a particle that enters cell 1 is $I_1 = e^{-2} = 0.1353$ and of one that enters cell 2 is $I_2 = e^{-1} = 0.3679$. The weight window generator estimates exactly these numbers from a forward run, as the total score of the particles that enter a cell divided by their total weight. The targets $T/I_j$ are 1 in cell 1 and $e^{-1} = 0.3679$ in cell 2. With $c_u = 5$, the window of cell 2 is $w_L = 2 \cdot 0.3679/6 = 0.1226$ and $w_U = 5 w_L = 0.6131$. A particle of weight 1 that enters cell 2 is above it, so it splits into $\lceil 1/0.6131 \rceil = 2$ copies of weight 0.5, which are inside the window. This is the split of ratio 2 of the [particle splitting](/particle-splitting/) page.

**Windows with a biased source.** In the 10 cm shielding slab of the [CADIS](/cadis/) page (scattering ratio 0.5, detector 9 cm from the source), source biasing alone gives a figure of merit per flight of $2.18 \times 10^{-5}$, about the analog value of $2.0 \times 10^{-5}$. Adding the CADIS windows, checked at every collision and every cell boundary, with implicit capture, gives $1.14 \times 10^{-3}$, about 57 times the analog value (measurements with fixed seeds, $10^5$ analog histories and $10^4$ CADIS histories). The windows, not the source biasing, do most of the work in this problem.

**Uniform errors over a mesh.** With [FW-CADIS](/fw-cadis/), the windows come from an adjoint whose source is the inverse of the forward flux. In a 16 cm slab with 16 tally bins, the ratio of the largest to the smallest relative error over the bins falls from 60.5 (analog) to 7.4, and the figure of merit of the worst bin rises by a factor of about 32 (measurements on that page).

## Variations

- **Weight cutoff.** A window with no upper bound, often used with implicit capture: only the roulette below $w_L$.
- **Space-energy and space-time windows.** The cell index includes an energy bin or a time bin, so the window can follow the importance of slow and fast particles.
- **Mesh windows.** The bounds are given on a Cartesian mesh laid over the geometry, independent of the geometry cells. This is the usual form for windows from a deterministic adjoint.
- **The weight window generator.** Booth and Hendricks (1984) estimate the importance of each cell from a forward run, $I_j = $ (score from particles that enter $j$) / (weight that enters $j$), and iterate: each run with windows gives better estimates for the next run.
- **Windows from an adjoint solve.** [CADIS](/cadis/) and [FW-CADIS](/fw-cadis/) set the bounds from a discrete ordinates adjoint and bias the source so that particles are born inside their windows.
- **Where to check.** At surface crossings only, at collisions only, or both. Checks at collisions control the weights in thick cells; checks at surfaces follow the change in importance from cell to cell.

## Pitfalls

- **Source and windows that do not agree.** If source particles are born with weight 1 in a cell whose window is $[0.01, 0.05]$, each one is split into many copies at once, and the run spends its time there. The source must be biased so that its weights fall inside the windows, which is the point of the consistent source of CADIS.
- **Windows too high.** If the bounds are far above the weights that reach a region, most particles there are removed by roulette, and the tally sees few particles with large weights.
- **Windows too narrow.** A small $c_u$ causes many splits and roulettes for little gain.
- **Noisy generator estimates.** A cell that no particle reached in the generator run has no estimate. With no window there, the particles in that cell are not controlled. The game stays unbiased, but a few heavy particles can then dominate the tally.
- **No cap on the copies.** A particle with a huge weight in a cell with a low window can make thousands of copies at once. A cap keeps the bank small, and the mean is still right.
- **Errors from copies.** As with splitting, the variance must be computed from the total score of each source history.

## Exercises

1. Show that the window game keeps the mean when the number of copies is $\lceil w/w_U \rceil$, when it is capped at $n_{\max}$, and when it is random with mean $w/\bar w$.
2. For the window $[1, 5]$ with $w_S = 3$, compute the variance that the roulette adds to a particle of weight $w < 1$ as a function of $w$. Compare it with a survival weight of 1.
3. In the two-cell absorber, run the weight window generator by hand with 4 histories and the random numbers of your choice. How large is the error of the estimate of $I_2$?
4. Prove that if $w \cdot I_j$ is the same for every particle in every cell, then the expected score of each particle is the same, and explain why this does not yet give zero variance.
5. Explain why, at a collision, the window check should come after the new direction is sampled. What goes wrong if all copies keep the direction from before the collision?

## References
