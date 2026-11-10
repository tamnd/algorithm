---
tag: V5BYBD
kind: algorithm
slug: wang-landau
name: Wang-Landau algorithm
aliases:
- Wang-Landau sampling
- flat histogram method
area: randomized/markov-chain-monte-carlo
level: research
summary: Estimates the density of states g(E) with a walk that accepts with min(1, ĝ(E)/ĝ(E′)) and adds ln f to ln ĝ at each visit. For exact convergence, f must decay like 1/t.
solves: [partition-function-computation]
model: real-ram
complexity:
  vars: {S: the number of steps, N: the number of energy levels, c: the cost of one proposal and its energy, d: the size of one state}
  time: {worst: Θ(S c)}
  space: {extra: Θ(N + d)}
properties: {in_place: true, online: false, deterministic: false, recursive: false}
history:
  year: 2001
  people: [Fugao Wang, David P. Landau, R. E. Belardinelli, V. D. Pereyra]
  note: Wang and Landau introduced the algorithm in 2001. Belardinelli and Pereyra showed in 2007 that the error of the original schedule stops decreasing, and proposed the 1/t schedule.
prereqs: [metropolis-hastings]
see_also: [ising-model, parallel-tempering, swendsen-wang, random-walk-metropolis, partition-function, burn-in, mixing-time]
sources:
  - paper: doi:10.1103/PhysRevLett.86.2050
    title: Fugao Wang and David P. Landau, Efficient, multiple-range random walk algorithm to calculate the density of states, Physical Review Letters 86(10), 2001
    locator: pages 2050 to 2053 (the algorithm, the flatness test and the halving of ln f)
  - paper: doi:10.1103/PhysRevE.64.056101
    title: Fugao Wang and David P. Landau, Determining the density of states for classical statistical models, a random walk algorithm to produce a flat histogram, Physical Review E 64(5), 2001
    locator: article 056101 (a longer account with tests on Ising and Potts models)
  - paper: doi:10.1103/PhysRevE.75.046701
    title: R. E. Belardinelli and V. D. Pereyra, Fast algorithm to calculate density of states, Physical Review E 75(4), 2007
    locator: article 046701 (the saturation of the error and the 1/t schedule)
  - paper: doi:10.1063/1.2803061
    title: R. E. Belardinelli and V. D. Pereyra, Wang-Landau algorithm, a theoretical analysis of the saturation of the error, Journal of Chemical Physics 127(18), 2007
    locator: article 184105 (why the error of the halving schedule stops decreasing)
  - paper: doi:10.1090/S0025-5718-2015-02952-4
    title: Gersende Fort, Benjamin Jourdain, Estelle Kuhn, Tony Lelièvre and Gabriel Stoltz, Convergence of the Wang-Landau algorithm, Mathematics of Computation 84(295), 2015
    locator: pages 2297 to 2327 (almost sure convergence with a deterministic decreasing sequence of factors)
  - paper: doi:10.1214/12-AAP913
    title: Pierre E. Jacob and Robin J. Ryder, The Wang-Landau algorithm reaches the flat histogram criterion in finite time, Annals of Applied Probability 24(1), 2014
    locator: pages 34 to 53 (each stage of the halving schedule ends with probability 1)
  - paper: doi:10.1016/0370-2693(91)91256-U
    title: Bernd A. Berg and Thomas Neuhaus, Multicanonical algorithms for first order phase transitions, Physics Letters B 267(2), 1991
    locator: pages 249 to 253 (sampling with weights 1/g(E) for a flat energy histogram)
  - paper: doi:10.1103/PhysRevLett.76.78
    title: Paul D. Beale, Exact distribution of energies in the two-dimensional Ising model, Physical Review Letters 76(1), 1996
    locator: pages 78 to 81 (exact densities of states of finite Ising lattices, for checks)
---

The Wang-Landau algorithm estimates the density of states $g(e)$ of a system: the number of states $x$ with energy $E(x) = e$. With $g$ known, the partition function $Z(\beta) = \sum_eg(e)e^{-\beta e}$ and the mean of every function of the energy follow at every temperature at once. The algorithm runs a random walk with the acceptance probability

$$\min\Big(1,\ \frac{\hat g(E(x))}{\hat g(E(y))}\Big)$$

for a move from $x$ to $y$, where $\hat g$ is the current estimate. After each step it multiplies $\hat g$ at the current energy by a factor $f > 1$. Energies that the walk visits often become expensive, and the walk is pushed toward energies that it has visited less. When $\hat g = g$, the walk visits all energies equally often, which is the multicanonical law of Berg and Neuhaus (1991). Wang and Landau (2001) halved $\ln f$ each time the histogram of visits was flat. Belardinelli and Pereyra (2007) showed that the error of this schedule stops decreasing at a fixed level, and that a factor that decays like $\ln f = N/t$ makes the estimate converge.

## In plain words

Imagine that you want to know how many rooms of a big building lie on each floor, but you can only walk from room to room. A plain walk spends most of its time on the floors with the most rooms and almost never visits the small floors.

Wang-Landau leaves a mark on the floor each time it stands on it, and it does not like to walk to floors with many marks. In this way it is pushed to the floors that it has not seen much. When it visits all floors about equally often, the marks tell how big each floor is: a big floor needed many marks before the walk stopped going there. The marks are made smaller and smaller as the walk goes on. They must shrink slowly enough, or the walk freezes with the wrong answer.

## The problem

The input is a finite set of energy levels $e_1, \dots, e_N$, a symmetric proposal kernel on the states (with $q(x, y) = q(y, x)$), a start $x_0$ and a final factor $\varepsilon > 0$. The output is an estimate $\ln\hat g(e)$, up to one additive constant, of $\ln g(e)$, where $g(e) = |\{x : E(x) = e\}|$ for a finite state space, or the volume of the level set for a continuous one. This solves the [partition function computation](/partition-function-computation/) for all temperatures at once: $Z(\beta) = \sum_eg(e)e^{-\beta e}$. The constant is fixed by one known value, such as the total number of states or the two ground states of the Ising model. The model of randomness is one proposal and one uniform real per step.

## The algorithm

```pseudo id=main
WANG-LANDAU(levels e_1, …, e_N, symmetric proposal q, x, ε)
L1  ln ĝ(e) ← 0 and H(e) ← 0 for every level; ln f ← 1; t ← 0
L2  while ln f > ε do
L3      draw y from q(x, ·)
L4      draw u uniformly from [0, 1); if u < exp(ln ĝ(E(x)) − ln ĝ(E(y))) then x ← y
L5      ln ĝ(E(x)) ← ln ĝ(E(x)) + ln f; H(E(x)) ← H(E(x)) + 1; t ← t + 1
L6      if the 1/t stage has begun then ln f ← N/t
L7      else if min H ≥ 0.8 · mean H then ln f ← ln f / 2, H ← 0, and if ln f ≤ N/t then begin the 1/t stage
L8  return ln ĝ
```

Line L5 updates $\hat g$ at the state after the test, also when the move was rejected. Line L7 is the flatness test, done every 1000 steps in the implementation. With the option `one_over_t` off, the 1/t stage never begins, and the algorithm is the original one of Wang and Landau, which halves $\ln f$ at each flat histogram. The quantity $t/N$ is the time in Monte Carlo sweeps of the energy levels, so the 1/t stage sets $\ln f$ to the inverse of this time.

## Example

**The density of states of a small Ising model.** Take the [Ising model](/ising-model/) on the $4 \times 4$ torus, with $E(\sigma) = -\sum_{uv}\sigma_u\sigma_v$ over the 32 edges, and single spin flips as proposals. Counting all $2^{16}$ states gives 15 levels:

| $E$ | $-32$ | $-24$ | $-20$ | $-16$ | $-12$ | $-8$ | $-4$ | $0$ |
|---|---|---|---|---|---|---|---|---|
| $g(E)$ | 2 | 32 | 64 | 424 | 1728 | 6688 | 13568 | 20524 |

and $g(-E) = g(E)$. The table gives the largest error $\max_e|\ln\hat g(e) - \ln g(e)|$, after fixing the constant so that $\sum\hat g = 2^{16}$, for runs with seed 1 that start with all spins up.

| final $\ln f$ | halving: steps | halving: error | 1/t: steps | 1/t: error |
|---|---|---|---|---|
| $10^{-4}$ | 103000 | 0.268 | 150000 | 0.189 |
| $10^{-5}$ | 199000 | 0.201 | 1500000 | 0.054 |
| $10^{-6}$ | 252000 | 0.197 | 15000000 | 0.011 |
| $10^{-8}$ | 501000 | 0.196 | | |

The halving schedule stops quickly, but its error is frozen near 0.2: with seeds 2 and 3 it stays at 0.143 and 0.226 down to $\ln f = 10^{-8}$. The 1/t schedule needs $N/\varepsilon$ steps, and its error keeps falling, roughly like $\sqrt{\ln f}$. With seeds 2 and 3 it gives 0.047 and 0.046 at $10^{-5}$.

**All temperatures from one run.** From the 1/t estimate at $\varepsilon = 10^{-5}$, the mean energy at the critical coupling $\beta_c = \frac12\ln(1 + \sqrt2)$ is $-24.987$, against the exact $-25.050$, and the specific heat per spin is $0.793$, against $0.783$. The tests check the exact counts, the errors of both schedules and the mean energy.

## Correctness

The Wang-Landau chain is not a Markov chain with a fixed kernel, because $\hat g$ changes at every step. Its correctness has three parts.

**The frozen walk.** For a fixed $\hat g$, lines L3 and L4 are [Metropolis-Hastings](/metropolis-hastings/) with a symmetric proposal for the law $\pi_{\hat g}(x) \propto 1/\hat g(E(x))$. Under this law the energy has the distribution $\pi_{\hat g}(E = e) \propto g(e)/\hat g(e)$. So if $\hat g = g$ up to a constant, the energy is uniform on the $N$ levels, and the histogram becomes flat. The tests check this with an exact rational transition matrix on the cycle of 5 spins.

**The fixed point.** If $\hat g$ is not proportional to $g$, the walk visits the levels with $g(e)/\hat g(e)$ above average more often, and line L5 raises $\hat g$ there. Write $\theta_e = \ln\hat g(e)$ and $p_\theta(e) = g(e)e^{-\theta_e}/\sum_jg(j)e^{-\theta_j}$. The average motion of $\theta$, after removing a common shift, is $\dot\theta_e = p_\theta(e) - 1/N$. Its only fixed points are $\theta = \ln g + \text{const}$, and the convex function $V(\theta) = \ln\sum_jg(j)e^{-\theta_j} + \frac1N\sum_j\theta_j$ decreases along it. The proof file gives the details.

**The schedule.** The algorithm is a stochastic approximation of this motion with step sizes $\ln f$. Such schemes converge when the sum of the step sizes is infinite and the sum of their squares is finite, as for $\ln f \propto 1/t$. Fort, Jourdain, Kuhn, Lelièvre and Stoltz (2015) proved almost sure convergence for a version with a deterministic decreasing sequence of this kind. With the halving schedule, the total of all the increments is finite when the stages do not grow too fast. Then $\ln\hat g$ converges to a random limit, which is in general not $\ln g$, and this is the saturation in the table. Jacob and Ryder (2014) proved that, under conditions, each stage of the halving schedule ends, so the original algorithm stops.

No test of flatness can prove that the estimate is correct: a level that the walk never reached has no weight in the histogram, and a slow mode of the walk can give a flat histogram with a wrong $\hat g$.

## Complexity

Each step costs one proposal and one energy, $c$, plus $O(1)$ for the updates, so $S$ steps take $\Theta(Sc)$ time. With the 1/t stage, the run ends when $N/t \le \varepsilon$, so $S \ge N/\varepsilon$, and the error decreases like $\sqrt\varepsilon$, which is the usual Monte Carlo rate in the number of steps. The memory is $\Theta(N)$ for $\hat g$ and $H$, plus $\Theta(d)$ for the state.

The time to cross all levels matters as much as the schedule. Even with $\hat g = g$, the walk on the energy levels is a random walk, so it needs of the order of $N^2$ steps per crossing, or more if some level is hard to reach by local moves. For large systems the energy range is often split into windows, each with its own walk, and the pieces are joined at the overlaps, as Wang and Landau did.

## Properties

- **Estimates counts, not samples.** The output is $\ln\hat g$. It gives $Z(\beta)$, the free energy, the mean energy and the specific heat at every temperature.
- **Adaptive.** The chain changes its own target, so the usual Markov chain theory does not apply directly.
- **Exact only in the limit, with the right schedule.** The 1/t schedule converges. The halving schedule does not.
- **Crosses barriers in energy.** The walk visits high energies, where the barriers are low, as often as low energies, so it escapes from local minima.
- **Local moves only.** It uses a symmetric proposal, such as single spin flips, and needs no gradient.

## Variants and improvements

- **The 1/t schedule** (Belardinelli and Pereyra 2007). Halve $\ln f$ until it reaches $N/t$, then set $\ln f = N/t$.
- **Energy windows.** Run separate walks on overlapping ranges of energy, in parallel, and join the estimates.
- **Continuous energies.** Use bins of energy. The bin width adds a bias.
- **Multicanonical sampling** (Berg and Neuhaus 1991). Fix the weights $1/\hat g$ from a first run and then run plain Metropolis with these weights, which is a true Markov chain, and reweight the samples to any temperature.
- **Stochastic approximation Monte Carlo.** A statistics version of the same idea, for a general partition of the state space.
- **Combination with [parallel tempering](/parallel-tempering/).** Exchange states between walks on neighbour windows of energy.

## When to use it

Use Wang-Landau to compute the density of states of a discrete system, such as Ising, Potts or lattice protein models, when you need thermodynamic quantities over a whole range of temperatures, or when low temperatures have barriers that trap ordinary Metropolis. For sampling at one fixed temperature, plain MCMC, cluster methods such as [Swendsen-Wang](/swendsen-wang/), or [parallel tempering](/parallel-tempering/) are usually simpler. For high-dimensional continuous energies, the binning and the number of levels make it hard to use.

## Pitfalls

- **Halving to a very small $\ln f$.** It does not make the estimate better than its saturation level, as the table shows. Use the 1/t stage.
- **Levels that do not exist.** If a listed level has no state, its histogram stays empty and the flatness test is never passed. List only levels that exist, or test flatness only over visited levels.
- **Reading the histogram as a proof.** A flat histogram is necessary but not sufficient for a correct estimate.
- **Updating before the test.** Line L5 must update the level of the state after the test, also after a rejection.
- **A proposal that is not symmetric.** The acceptance ratio assumes $q(x, y) = q(y, x)$. Otherwise a Hastings factor is needed.
- **The constant.** $\hat g$ is known only up to a factor. Fix it with a known count before you compute $Z$.

## Implementations

## History

Berg and Neuhaus (1991) introduced multicanonical sampling, with weights $1/g(E)$ found by iteration. Wang and Landau (2001) proposed to change the weights at every step and to reduce the change each time the energy histogram is flat, and tested the method on Ising and Potts models against exact counts such as those of Beale (1996). Belardinelli and Pereyra (2007) showed that the error of the original schedule saturates and proposed the 1/t schedule. Jacob and Ryder (2014) proved that the flatness test is passed in finite time, and Fort and coworkers (2015) proved convergence for a decreasing sequence of factors.

## References
