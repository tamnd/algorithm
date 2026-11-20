---
tag: W145MS
kind: algorithm
slug: hyperdynamics
name: Hyperdynamics
area: scientific-computing/multiscale-methods
level: advanced
summary: Adds a bias potential that is zero at transition states, so MD escapes basins faster and the true time follows from the boost factor.
model: real-ram
complexity:
  vars: {n: the number of steps of the biased run, G: the cost of one force and bias evaluation, d: the number of coordinates}
  time: {worst: O(n (G + d))}
  space: {extra: O(d)}
properties: {deterministic: false, randomized: true, exact: false, iterative: true}
history:
  year: 1997
  people: [Arthur F. Voter]
  note: Voter gave hyperdynamics in 1997, with the boosted clock and a bias that is zero where the lowest curvature of the potential is negative.
prereqs: [molecular-dynamics, harmonic-transition-state-theory, canonical-ensemble]
see_also: [parallel-replica-dynamics, temperature-accelerated-dynamics, kinetic-monte-carlo, metadynamics, umbrella-sampling, langevin-dynamics, brownian-dynamics, importance-sampling]
sources:
  - paper: doi:10.1103/PhysRevLett.78.3908
    title: "Arthur F. Voter, Hyperdynamics: accelerated molecular dynamics of infrequent events, Physical Review Letters 78(20), 1997, 3908-3911"
    locator: the bias potential that vanishes at the dividing surfaces, the boosted time and the argument from transition state theory
  - paper: doi:10.1146/annurev.matsci.32.112601.141541
    title: Arthur F. Voter, Francesco Montalenti and Timothy C. Germann, Extending the time scale in atomistic simulation of materials, Annual Review of Materials Research 32, 2002, 321-346
    locator: the review of hyperdynamics, parallel replica dynamics and temperature accelerated dynamics, with the conditions on the bias
---

Hyperdynamics accelerates a molecular dynamics simulation of a system that moves by rare escapes from basins of its potential energy. It adds a bias potential $\Delta V \ge 0$ that raises the bottom of the basin and is exactly zero near every dividing surface that leads out of it. The biased system escapes sooner, and through the same exits with the same relative probabilities. Each step of length $h$ advances the physical clock by $h\, e^{\Delta V(x) / k_B T}$, so the sum over the run estimates the escape time of the unbiased system. The argument is exact for the rates of transition state theory; for real dynamics it is an approximation, and the speedup, called the boost, is a measured property of each run, not a guarantee.

## In plain words

A ball in a deep bowl shakes for a long time before it jumps over the rim. Most of the time is spent near the bottom. Fill the bottom of the bowl with sand, but do not touch the rim. Now the ball jumps out much sooner. Because the rim is the same, the ball leaves by the same gaps as before, in the same proportions.

The only thing that is wrong is the clock. When the ball is on the sand, time in the real bowl would pass faster, because the real ball would be lower and would take longer to get out. So each tick on the sand counts as more than one tick, by a factor that grows with the depth of the sand. Added up, the ticks give the real time of the jump.

## The problem

The input is a potential $V$, a dynamics that samples the canonical ensemble at temperature $T$ (here [Brownian dynamics](/brownian-dynamics/); in materials, [Langevin dynamics](/langevin-dynamics/) or [molecular dynamics](/molecular-dynamics/) with a thermostat), and a bias $\Delta V \ge 0$ for the current basin $A$. The output is the next state, the basin the system escapes to, and the escape time, so that a sequence of escapes is a sample of the state-to-state dynamics over times far beyond direct simulation. The method assumes that escapes are rare: the system equilibrates in $A$ long before it leaves, so the escape is a Poisson process with the rates of transition state theory.

## The algorithm

```pseudo id=main
HYPERDYNAMICS(x, V, ΔV, k_B T, h)
L1  t_hyper ← 0
L2  repeat
L3      evaluate ΔV(x) and ∇ΔV(x)                           ▷ zero near every dividing surface
L4      t_hyper ← t_hyper + h exp(ΔV(x) / k_B T)              ▷ the boosted clock
L5      x ← x - h ∇(V + ΔV)(x) + sqrt(2 k_B T h) ξ,  ξ standard normal
L6  until x has left the basin
L7  return x, t_hyper
```

Line L5 is one [Euler-Maruyama](/euler-maruyama-method/) step of overdamped Langevin dynamics on the biased potential, with mobility 1 and the time step $h$. Any dynamics that samples the canonical ensemble works here. Line L4 is the change of clock: a step at a point with a large bias counts for more physical time. Line L6 needs a test that the system has left the basin, for example a short minimization that ends in a different minimum. The outer loop repeats this from the new basin with a new bias, and adds the hyper times. The boost of a run is $t_{\mathrm{hyper}} / (n h)$ for $n$ steps.

The implementation provides one simple bias with a flat floor, $\Delta V = \max(0, V_c - V)$ inside the basin: the biased potential is $\max(V, V_c)$, and the bias is zero wherever $V \ge V_c$, which includes the barrier region if $V_c$ is below the lowest saddle. For many atoms this needs a bias defined from local quantities; Voter's bias of 1997 is zero where the lowest curvature of $V$ is negative, which is true near every saddle.

## Example

**The clock by hand.** Take $V(x) = (x^2 - 1)^2$ with the barrier $E_b = 1$ at $x = 0$, $k_B T = 0.25$, the flat floor $V_c = 0.6$ for $x < 0$, and $h = 0.02$. At the minimum $x = -1$, $\Delta V = 0.6$ and the biased potential is flat, so the drift is zero. Each step there advances the clock by $0.02\, e^{0.6/0.25} = 0.02 \times 11.0232 = 0.220464$. Two steps give $0.440927$. Where $V \ge 0.6$, for example at $x = -0.2$ where $V = 0.9216$, a step counts as $h$.

**Exact times.** For this one-dimensional dynamics the mean escape times have closed forms (the formula is in the proof). Let the escape be the first arrival at $x = 0.5$, beyond the barrier, from $x = -1$. With quadrature:

| $k_B T$ | $V_c$ | unbiased mean time | mean hyper time | mean simulated time | time boost | $Z_A / Z_A^b$ |
|---|---|---|---|---|---|---|
| 0.25 | 0.4 | 65.925 | 67.400 | 25.819 | 2.55 | 2.585 |
| 0.25 | 0.6 | 65.925 | 71.527 | 14.591 | 4.52 | 4.757 |
| 0.25 | 0.8 | 65.925 | 84.155 | 8.632 | 7.64 | 8.993 |
| 0.1667 | 0.6 | 477.635 | 505.383 | 36.886 | 12.95 | 13.439 |
| 0.125 | 0.6 | 3480.215 | 3597.905 | 89.391 | 38.93 | 39.816 |

The time boost is the unbiased time over the simulated time of the biased run. The last column is the boost of transition state theory, the ratio of the basin integrals of $e^{-\beta V}$ and $e^{-\beta V_b}$ over $x < 0$. Three facts show in the table. The boost grows like $e^{\beta V_c}$, so it is large at low temperature. The hyper time overestimates the true time, by 2.2 %, 8.5 % and 28 % at $k_B T = 0.25$ as the floor rises: this dynamics has recrossings, and the floor gets close to the barrier. At lower temperature, with the same floor, the error falls (5.8 % and 3.4 %).

**A measurement.** Runs of line L5 with `random.Random(1)`, $k_B T = 0.25$, $V_c = 0.6$ and $h = 0.005$, for $4 \times 10^5$ steps, gave 134 escapes with a mean hyper time of $72.2 \pm 6.2$ (one standard error), against $71.527$ from the formula, and a measured boost of $4.90$. This boost is a measurement of these runs.

## Correctness

The proof below is the argument of transition state theory. The TST rate through a dividing surface is the equilibrium flux through the surface over the probability of the basin, $k_j = \Phi_j / Z_A$. The bias does not change $V$ on the surfaces, so it does not change the fluxes. It only lowers the probability weight of the basin, from $Z_A$ to $Z_A^b$. So every rate is multiplied by the same factor $Z_A / Z_A^b = \langle e^{\beta \Delta V} \rangle_b$, the branching ratios are unchanged, and the average of $e^{\beta \Delta V}$ along the biased run, which line L4 computes, restores the time. This is exact for TST rates. For the true dynamics, it is as good as TST itself in the biased and the unbiased system: it needs the bias to be exactly zero where recrossings happen, and the biased basin to still hold the system long enough to equilibrate. The table above shows the size of the error for a diffusion with recrossings.

## Complexity

A run of $n$ biased steps costs $n$ evaluations of the force and the bias, $O(n (G + d))$ in the [real RAM](/real-ram/) model, and $O(d)$ memory. It reaches the physical time $B n h$ for the boost $B$. The cost of the bias matters: a bias from the lowest Hessian eigenvalue needs several extra force calls per step (a [dimer](/dimer-method/) style rotation), which can cancel much of the boost; biases from bond lengths cost little. The boost is a measurement: values from a few to $10^6$ are reported in the literature for low temperature and simple systems, and it falls fast as the temperature rises or the system grows, because a safe bias must stay below the lowest barrier anywhere in the system.

## Properties

- **Exact under TST.** With a bias that is zero on the dividing surfaces, the TST rates of all exits are divided by the same boost. No knowledge of the exits is needed.
- **Randomized.** The output is one sample of the escape; averages need many escapes.
- **Serial.** It accelerates one trajectory. It can be combined with [parallel replica dynamics](/parallel-replica-dynamics/).
- **Boost limited by the lowest barrier.** The bias must vanish near every saddle, including the lowest one, so the boost is at most of order $e^{\beta E_{\min}}$ for the lowest barrier $E_{\min}$ of the basin.

## Variants and improvements

- **Flat bias.** The bias $\max(0, V_c - V)$ of the example costs nothing but needs a floor below every saddle of the basin, which is known only in small models.
- **Hessian based bias.** Voter's bias of 1997 depends on the lowest eigenvalue of the Hessian, which is negative near every first-order saddle, so the bias vanishes there without knowing the saddles.
- **Bond boost.** For materials, a bias that depends on the largest change of bond length in the system is cheap, and is zero when one bond is stretched far, which is what happens at a saddle.
- **Accelerated MD in biomolecules.** A flat bias on the total energy or on the dihedral energy is used to sample conformations; the boosted time there is often not physical, because the conditions above do not hold.
- **[Metadynamics](/metadynamics/)** and [umbrella sampling](/umbrella-sampling/) also add a bias, but to compute free energies; the bias there does not vanish on the dividing surfaces, so the time is not preserved.

## When to use it

Use hyperdynamics for a system with rare escapes, at a low temperature where the boost is large, and when you can build a bias that is provably zero near all saddles of the basin, for example for surface diffusion and small defect clusters. Use [kinetic Monte Carlo](/kinetic-monte-carlo/) when the event catalog is known, [parallel replica dynamics](/parallel-replica-dynamics/) when many processors are available and the bias is hard to build, and [temperature accelerated dynamics](/temperature-accelerated-dynamics/) when harmonic TST is accurate for all events.

## Pitfalls

- **A bias that does not vanish at a saddle.** The system escapes through a lowered barrier, and both the time and the choice of exit are wrong. Nothing in the run shows this.
- **A bias that is too high.** If the floor comes close to the barrier, the biased basin no longer holds the system, the escape is no longer a Poisson process with TST rates, and the hyper time is biased, by 28 % in the table for $V_c = 0.8$.
- **Few escapes.** A single hyper time is one sample of an exponential law, with a relative standard deviation of 1. Averages need many escapes.
- **Confusing the boost with an error bar.** A large boost says nothing about the accuracy; check against direct MD at a higher temperature where both are possible.

## Implementations

## History

Voter introduced hyperdynamics in 1997, as the first of his accelerated molecular dynamics methods, with the boosted clock and a bias based on the lowest curvature of the potential. He then gave parallel replica dynamics in 1998 and, with Sorensen, temperature accelerated dynamics in 2000. The review of Voter, Montalenti and Germann in 2002 compares the three methods and the conditions under which each is accurate.

## References
