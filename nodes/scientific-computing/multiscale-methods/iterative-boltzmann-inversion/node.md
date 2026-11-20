---
tag: JKHDRS
kind: algorithm
slug: iterative-boltzmann-inversion
name: Iterative Boltzmann inversion
area: scientific-computing/multiscale-methods
level: advanced
summary: Fits a coarse-grained pair potential to a target radial distribution function, by adding kT ln(g/g_target) to the potential after each simulation until g matches.
model: real-ram
complexity:
  vars: {I: the number of iterations, M: the number of grid points of the potential, S: the cost of one simulation with its histogram}
  time: {worst: O(I (S + M))}
  space: {extra: O(M)}
properties: {deterministic: true, randomized: false, exact: false, iterative: true}
history:
  year: 2003
  people: [Dirk Reith, Mathias Putz, Florian Muller-Plathe]
  note: Reith, Putz and Muller-Plathe gave the method in 2003 for coarse-grained polymer models. The uniqueness of a pair potential for a given g(r) is a theorem of Henderson from 1974.
prereqs: [radial-distribution-function, molecular-dynamics]
see_also: [force-matching-coarse-graining, mori-zwanzig-formalism, dissipative-particle-dynamics, canonical-ensemble, partition-function, fixed-point-iteration, lennard-jones-potential, interatomic-potential]
sources:
  - paper: doi:10.1002/jcc.10307
    title: Dirk Reith, Mathias Putz and Florian Muller-Plathe, Deriving effective mesoscale potentials from atomistic simulations, Journal of Computational Chemistry 24(13), 2003, 1624-1636
    locator: the iterative update of the potential from the ratio of the distribution functions, for bonded and nonbonded coarse-grained interactions
  - paper: doi:10.1016/0375-9601(74)90847-0
    title: R. L. Henderson, A uniqueness theorem for fluid pair correlation functions, Physics Letters A 49(3), 1974, 197-198
    locator: the theorem that at fixed density and temperature a pair potential is fixed by g(r) up to a constant
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Section 2.6 (the radial distribution function and its estimate from a histogram)
---

Iterative Boltzmann inversion (IBI) builds a pair potential $V(r)$ for coarse-grained beads, so that a simulation of the beads reproduces a target radial distribution function $g^*(r)$, usually the one of the beads mapped from an atomistic simulation. It starts from the potential of mean force $-k_B T \ln g^*(r)$, runs a simulation with the current potential, and corrects the potential at each distance by $k_B T \ln(g(r) / g^*(r))$: where the beads are found too often, the potential goes up. It stops when the simulated $g$ agrees with the target. Each iteration costs one simulation. Henderson's theorem says that the answer, if it exists, is unique up to a constant, but no theorem says that the iteration converges.

## In plain words

You have a detailed simulation of a liquid, and you want a simple model in which each molecule is one ball. You measure how often two molecules sit at each distance in the detailed run. Now you guess a force law for the balls and run the simple model.

At distances where the balls meet more often than the molecules did, you make the balls repel a bit more. Where they meet less often, you make them repel less. You run the simple model again and repeat. The size of each correction comes from the ratio of the two counts. When the counts match at every distance, you stop. You then have a force law that gives the right structure, but not always the right pressure.

## The problem

The input is a target $g^*(r)$ on a grid $r_0, \dots, r_{M-1}$ up to a cutoff $r_c$, the temperature $T$ (with $\beta = 1 / (k_B T)$), the density $\rho$ of the beads, and a simulator: a function that takes a tabulated pair potential $V$ and returns the radial distribution function $g_V$ of an equilibrium run with it, in the canonical ensemble at the same $\rho$ and $T$. The output is a potential $V$ with $g_V = g^*$ to a tolerance. The beads interact only by the pair potential; three-body terms are outside the model, so a target from a system with many-body forces can be matched in $g$, but other properties then need not match.

Two facts frame the problem. First, $w(r) = -k_B T \ln g(r)$ is the pair potential of mean force: the free energy of two beads at distance $r$, averaged over all others. In the limit $\rho \to 0$, $g(r) = e^{-\beta V(r)}$, so $V = w$. At finite density, $g(r) = e^{-\beta V(r)} y(r)$ with the cavity function $y \ne 1$, so $V \ne w$. Second, by Henderson's theorem (1974), for a fluid of pairwise additive particles at fixed $\rho$ and $T$, two pair potentials with the same $g$ differ only by a constant. So the problem has at most one solution with $V(r_c) = 0$.

## The algorithm

```pseudo id=main
ITERATIVE-BOLTZMANN-INVERSION(g*, SIMULATE, k_B T, α, tol)
L1  V(r) ← -k_B T ln g*(r) at each grid point                          ▷ the potential of mean force
L2  repeat
L3      g ← SIMULATE(V)                                                 ▷ MD or MC with V, then a histogram of pair distances
L4      if max_r |g(r) - g*(r)| < tol then return V
L5      for each grid point r with g(r) > 0 and g*(r) > 0
L6          V(r) ← V(r) + α k_B T ln(g(r) / g*(r))
L7  return V                                                            ▷ the iteration budget is spent
```

Line L1 is plain Boltzmann inversion. It is exact at zero density and a good start at moderate density. Line L3 is the expensive step: an equilibrium simulation, long enough that the histogram noise in $g$ is below the corrections that line L6 makes. Line L6 is the update of Reith, Putz and Muller-Plathe (2003) with $\alpha = 1$; a factor $\alpha < 1$ damps it. Line L5 skips the points where a logarithm is not defined: inside the core, where no pair is seen, the potential keeps its start value (in practice it is extrapolated from the points outside).

## Example

**One step by hand.** The implementation has a closed form simulator for tests: a one-dimensional fluid of density $\rho$ to first order in $\rho$, with $g(r) = e^{-\beta V(r)} (1 + \rho (f * f)(r))$, where $f = e^{-\beta V} - 1$ is the Mayer function and $f * f$ is the convolution on the line. This is the density expansion of the cavity function, cut after the first term; it is a model of a simulator, not a simulation. Take $k_B T = 1$, $\rho = 0.1$, a grid with $\Delta r = 0.05$ from $0$ to $4$ (81 points), and the true potential $V^*(r) = 2 e^{-r^2} - 0.5 e^{-4 (r - 1.5)^2}$, a soft core with a well near $r = 1.5$. The target has $g^*(0) = 0.152865$. Line L1 gives $V_0(0) = -\ln 0.152865 = 1.878199$, below the true $V^*(0) = 1.999938$, because the neighbors push pairs together and raise $g$ above $e^{-\beta V}$. The simulator with $V_0$ gives $g_0(0) = 0.171437$, more than the target, so line L6 raises the potential: $V_1(0) = 1.878199 + \ln(0.171437 / 0.152865) = 1.878199 + 0.114660 = 1.992859$. Over the whole grid, the largest error of the potential falls from $0.1217$ for $V_0$ to $0.0071$ for $V_1$.

**Convergence.** On the same problem, the largest error $\max |g_i - g^*|$ in the iterations $i = 0, 1, 2, \dots$ is

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 10 | 16 |
|---|---|---|---|---|---|---|---|---|
| $\max \lvert g_i - g^* \rvert$ | $2.79 \times 10^{-2}$ | $5.31 \times 10^{-3}$ | $1.43 \times 10^{-3}$ | $4.04 \times 10^{-4}$ | $1.16 \times 10^{-4}$ | $3.35 \times 10^{-5}$ | $6.49 \times 10^{-8}$ | $3.55 \times 10^{-11}$ |

so the error falls by a factor of about $0.29$ per iteration, and after 17 simulations the potential matches $V^*$ to $4 \times 10^{-11}$. At $\rho = 0.2$ the factor is about $0.58$ and 37 simulations are needed; with the damping $\alpha = 0.5$ at $\rho = 0.1$, 45 are needed. In the dilute model $g = e^{-\beta V}$, line L1 is already exact and the loop stops after one simulation. These are measurements on a model, without the noise of a real simulation.

## Correctness

The proof in the proofs file shows three things. First, a returned potential satisfies the stop test of line L4, and a fixed point of line L6 with $\alpha > 0$ is exactly a potential with $g_V = g^*$ at every updated grid point. By Henderson's theorem, if the simulator is exact and the target comes from a pair potential at the same state, this fixed point is that potential up to a constant. Second, in the dilute limit $g_V = e^{-\beta V}$, line L1 is the exact answer. Third, the update is a Newton step for the equation $\ln g_V = \ln g^*$ with the Jacobian $\partial \ln g_V(r) / \partial V(r') \approx -\beta \delta_{r r'}$, which is the exact Jacobian at zero density. So IBI is a quasi-Newton method whose Jacobian is right in the dilute limit and wrong by terms of order $\rho$ at finite density. This explains the fast convergence in the example and the rate that grows with $\rho$, but it is a heuristic, not a proof: there is no general convergence theorem for IBI, and with a noisy simulator the iteration converges at best to a neighborhood of the answer whose size is set by the noise.

## Complexity

Each iteration runs one simulation and one update of $M$ grid points, so the cost is $O(I (S + M))$ in the [real RAM](/real-ram/) model, with memory $O(M)$ beyond the simulation. The simulation dominates by far: a run of $N$ beads for many steps, with a cutoff and a [linked cell list](/linked-cell-list/), costs $O(N)$ per step. The number of iterations $I$ depends on the density and on the noise, and no bound on it is known. The coarse-grained run is much cheaper than the atomistic run that produced the target, because the beads are fewer and softer and allow a longer time step.

## Properties

- **Structure-based.** IBI matches $g(r)$, a structural target. It does not match forces, as [force matching](/force-matching-coarse-graining/) does, and it does not use the atomistic forces at all.
- **Unique target, uncertain path (theorem and heuristic).** The solution is unique up to a constant by Henderson's theorem. Convergence of the iteration is not proved.
- **State dependent.** The potential depends on the density and temperature of the target, because it absorbs the effect of the removed degrees of freedom; it is a free energy, not an energy.
- **Pressure.** A potential that gives the right $g$ can give the wrong pressure, because the pressure comes from $r V'(r)$ weighted by $g$, and small changes of $V$ at large $r$ change the pressure much and $g$ little.
- **Several interactions.** With bonds, angles and nonbonded pairs, each distribution has its own update, and the updates are done one after the other or together.

## Variants and improvements

- **Damping and smoothing.** A factor $\alpha < 1$ in line L6 and a smoothing of the update reduce oscillations and the effect of noise.
- **Pressure correction.** A common correction adds a small linear term $A (1 - r / r_c)$ to the potential, with the sign of $A$ chosen to move the pressure toward the target. This is a heuristic; the amplitude is a choice.
- **Inverse Monte Carlo.** The inverse Monte Carlo method of Lyubartsev and Laaksonen (1995) uses the cross correlations of the histogram from the same simulation as the full Jacobian of $g$ with respect to $V$. It is a Newton method with the right Jacobian, at the cost of more statistics per iteration.
- **Relative entropy and force matching.** Other ways to fit a coarse-grained model minimize the relative entropy between the mapped and coarse-grained distributions, or fit the mean forces by least squares ([force matching](/force-matching-coarse-graining/)). The [Mori-Zwanzig formalism](/mori-zwanzig-formalism/) explains what all of them leave out: the memory and the noise of the removed variables.

## When to use it

Use IBI when the target is structural, for example to build a bead model of a polymer melt or of a liquid that keeps the packing of the atomistic model, and when the atomistic forces are not at hand or too noisy. Use [force matching](/force-matching-coarse-graining/) when the atomistic forces are available and many-body effects matter, since it needs one least squares solve in place of many simulations. Neither gives the right dynamics; for that, add friction and noise, as in [dissipative particle dynamics](/dissipative-particle-dynamics/).

## Pitfalls

- **The sign of the update.** Writing line L6 as $V \leftarrow V - k_B T \ln(g / g^*)$ drives the potential away from the answer: where $g > g^*$ it lowers $V$ and draws more pairs to that distance. The right line is $V \leftarrow V + \alpha k_B T \ln(g / g^*)$.
- **The core region.** Where no pair is seen, $g = 0$ and the logarithm is undefined. Line L5 must skip these points, and the potential there must stay repulsive; extrapolate it from the first points with good statistics.
- **Noise.** Histogram noise in $g$ goes straight into $V$ through the logarithm. Run each simulation long enough, smooth the update, and stop when the change is below the noise, not at a tolerance the data cannot reach.
- **An approximate simulator.** Henderson's theorem holds for the exact $g$ of a fluid. In the example simulator, which is not a real fluid, at $\rho = 0.6$ IBI converged to a potential that differs from $V^*$ by up to $1.25\, k_B T$ but gives the same $g$ to $10^{-10}$. A short or biased simulation can do the same.
- **Transfer to another state.** The potential is fitted at one density and temperature. Using it at another state point without a check is a common source of error.
- **The constant and the cutoff.** The potential is unique only up to a constant; fix $V(r_c) = 0$ and make the potential and its derivative go to zero at $r_c$.

## Implementations

## History

Boltzmann inversion of a distribution function into a potential of mean force is old in liquid state theory. Henderson proved in 1974 that a pair potential is fixed by its $g(r)$ at a given density and temperature, up to a constant. Reith, Putz and Muller-Plathe turned the inversion into an iteration in 2003 and used it to derive mesoscale potentials for polymers from atomistic simulations, for bonded and nonbonded interactions. It became one of the standard structure-based coarse-graining methods, next to inverse Monte Carlo and force matching.

## References
