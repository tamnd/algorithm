---
tag: Y0N4QC
kind: algorithm
slug: pcisph
name: Predictive-corrective incompressible SPH
aliases: [PCISPH]
area: graphics-and-signals/fluid-animation
level: advanced
summary: An SPH fluid solver that finds each pressure by a loop that predicts the next positions and densities and corrects the pressure by a fixed factor times the predicted density error.
solves: [fluid-simulation-for-animation]
model: real-ram
complexity:
  vars: {n: "the number of particles", q: "the number of neighbor pairs", k: "the number of correction iterations"}
  time: {iteration: "O(n + q)", step: "O(k (n + q))"}
  space: {extra: "O(n + q)"}
properties: {deterministic: true, exact: false, conserves_linear_momentum: true, conserves_angular_momentum: true, iterative: true}
history:
  year: 2009
  people: [Barbara Solenthaler, Renato Pajarola]
  note: Solenthaler and Pajarola presented PCISPH at SIGGRAPH 2009 as a way to take larger steps than WCSPH at the same density error.
prereqs: [weakly-compressible-sph, smoothed-particle-hydrodynamics]
see_also: [implicit-incompressible-sph, divergence-free-sph, position-based-fluids, incompressible-sph, jacobi-method, sph-smoothing-kernel, fluid-simulation-for-animation, particle-fluid-surfacing]
sources:
  - paper: doi:10.1145/1531326.1531346
    title: Barbara Solenthaler and Renato Pajarola, Predictive-corrective incompressible SPH, ACM Transactions on Graphics 28(3), article 40, 2009
    locator: "Section 2.3 (the pressure update and delta, equations 8 and 9), Section 2.4 (Algorithm 2, the reuse of neighbors and the minimum of 3 iterations) and Section 4 (results)"
  - paper: doi:10.2312/SCA/SCA07/209-218
    title: Markus Becker and Matthias Teschner, Weakly compressible SPH for free surface flows, Symposium on Computer Animation 2007, 209-217
    locator: the whole paper (the WCSPH baseline)
  - paper: arxiv:2009.06944
    title: Dan Koschier, Jan Bender, Barbara Solenthaler and Matthias Teschner, Smoothed particle hydrodynamics techniques for the physics based simulation of fluids and solids, Eurographics tutorial, 2019
    locator: the section on pressure solvers
---

Predictive-corrective incompressible SPH (PCISPH) is an SPH fluid solver that does not use an equation of state.
Each step starts with zero pressure and runs a loop: predict where the particles go with the current pressure force, compute the densities there, and raise the pressure of each particle by a fixed factor $\delta$ times its predicted density error.
The loop stops when the largest predicted compression is below a tolerance $\eta$, for example 1% of the rest density.
The time step can be much larger than in [weakly compressible SPH](/weakly-compressible-sph/), because the pressure is no longer a stiff function of the density.

## In plain words

Think of the water as many small balls.
Before the balls move, the method makes a guess of where they would go in this step.
At the guessed places it counts how crowded each ball is.
Where a ball is too crowded, its pressure goes up a little.
With the new pressures it makes a better guess, and counts again.
After a few rounds, no ball is too crowded, and the balls move for real.
The size of each pressure change comes from one sample ball with a full ring of neighbors, worked out once before the run.
The guesses cost time, but the steps can be much longer than in the simple method, so the total work is often smaller.

## The problem

The input is a set of $n$ particles of equal mass $m$ with positions $x_i$ and velocities $v_i$, the rest density $\rho_0$, the smoothing length $h$, gravity $g = (0, -9.81)$ m/s², the step $\Delta t$ and the tolerance $\eta$.
The output is the state after one step, in which the predicted density of each particle is at most $(1 + \eta)\rho_0$.
This is the SPH form of an incompressible fluid with a free surface, one method for [fluid simulation for animation](/fluid-simulation-for-animation/).
The kernel $W$ is the 2D cubic spline with support $2h$, as on [WCSPH](/weakly-compressible-sph/), and $\nabla W_{ij}$ is its gradient with respect to $x_i$.

## The algorithm

Before the run, compute the factor $\delta$ on a prototype particle with a full neighborhood on a square lattice of spacing $\Delta x$:

$$\beta = 2\left(\frac{\Delta t\, m}{\rho_0}\right)^2, \qquad \delta = \frac{1}{\beta\left(\left|\sum_j \nabla W_{ij}\right|^2 + \sum_j |\nabla W_{ij}|^2\right)}.$$

```pseudo id=main
PCISPH-STEP(x, v, Δt)
L1  P ← neighbor pairs at time t; store ∇Wᵢⱼ for each pair
L2  for each i: fᵢ ← g + other non-pressure accelerations
L3  for each i: pᵢ ← 0; aᵖᵢ ← 0
L4  while iter < 3 or (max error > η ρ₀ and iter < max) do
L5      for each i: v*ᵢ ← vᵢ + Δt (fᵢ + aᵖᵢ)
L6      for each i: x*ᵢ ← xᵢ + Δt v*ᵢ, clamped to the walls
L7      for each i: ρ*ᵢ ← m W(0) + Σ over pairs of m W(|x*ᵢ - x*ⱼ|)
L8      for each i: eᵢ ← ρ*ᵢ - ρ₀
L9      for each i: pᵢ ← max(0, pᵢ + δ eᵢ)
L10     for each i: aᵖᵢ ← -m Σⱼ (pᵢ + pⱼ) / ρ₀² ∇Wᵢⱼ
L11 for each i: vᵢ ← vᵢ + Δt (fᵢ + aᵖᵢ)
L12 for each i: xᵢ ← xᵢ + Δt vᵢ, clamped to the walls
```

Line L1 finds the pairs with the grid search and keeps them for the whole loop, as Section 2.4.1 of the paper does.
Line L2 holds gravity and any viscosity or external force; the tests use gravity only.
Lines L5 to L7 predict the state with the current pressure.
Line L8 is the predicted density error, and line L9 corrects the pressure.
The clamp at 0 in line L9 is the choice of this page: at the free surface a particle has fewer neighbors and a low density, and a negative pressure there would pull the surface into clumps.
Line L10 is the symmetric pressure force with $\rho_0$ in place of $\rho_i$ and $\rho_j$, the same approximation that gives $\delta$.
The loop runs at least 3 times, as in the paper, and stops when $\max_i e_i \le \eta\rho_0$.
Lines L11 and L12 are symplectic Euler with the final pressure force.

The formula for $\delta$ comes from a linear guess.
A pressure $\tilde p$ on particle $i$, with the same pressure on its neighbors, moves $i$ by $-\Delta t^2 m (2\tilde p/\rho_0^2)\sum_j \nabla W_{ij}$ and moves each neighbor $j$ by $\Delta t^2 m (2\tilde p/\rho_0^2)\nabla W_{ij}$.
To first order this lowers $\rho_i$ by $\tilde p\,\beta\,(|\sum_j \nabla W_{ij}|^2 + \sum_j|\nabla W_{ij}|^2)$.
Setting the drop equal to the error $e_i$ gives $\tilde p = \delta e_i$.
On a full symmetric lattice $\sum_j \nabla W_{ij} = 0$, so only the second term is left.

## Example

Take $\Delta x = 0.02$ m, $h = 1.3\Delta x$, $\rho_0 = 1000$ kg/m², $m = \rho_0\Delta x^2 = 0.4$ kg and $\Delta t = 0.004$ s.
The prototype gives $\delta = 53.05$ m²/s².
Put 25 particles at rest on a 5 by 5 lattice with spacing $0.95\Delta x$, so the block is squeezed, and set $g = 0$ and $\eta = 0.01$.
The table gives the largest predicted compression $\max_i e_i/\rho_0$ of line L8 in each pass of the loop.

| pass | max error |
|---|---|
| 1 | 10.96% |
| 2 | 0.62% |
| 3 | 1.57% |
| 4 | 0.99% |

The first pass has no pressure, so it sees the squeeze of the block.
The second pass already has a small error, but the loop runs at least 3 times.
The third pass overshoots at some particles, because $\delta$ comes from a full neighborhood and the block has edges.
The fourth pass is below 1%, so the loop stops.

## Correctness

PCISPH is a fixed point iteration on the pressure, and it has no proof of convergence in general.
The paper states it with a linear model of one particle and reports that it converges in practice; the tests here check it on a small dam break.
These things are exact:

- **Exit condition.** If the loop stops before the cap, every predicted density of line L7 is at most $(1 + \eta)\rho_0$.
- **Momentum.** The pressure force of line L10 is a sum of pair terms with opposite signs on $i$ and $j$, parallel to $x_i - x_j$. So without walls and gravity, the step keeps the total linear and angular momentum, by the argument of [WCSPH](/weakly-compressible-sph/).
- **First order.** For a small error $e$ on the prototype particle, the pressure $\delta e$ lowers its predicted density by $e + O(e^2)$.

The final positions of line L12 use the pressure after the last correction, so the real density error is usually a little smaller than the last measured one.
The [proof](proofs/correctness.md) gives the three arguments.

## Complexity

One pass of the loop costs $O(n + q)$ time for $q$ pairs: lines L5 to L10 do constant work per particle and per pair.
A step with $k$ passes costs $O(k(n + q))$, and the grid search of line L1 adds $O(n + q)$ once.
With a density near $\rho_0$, $q = O(n)$.
The number $k$ is a measurement, not a bound. In the small dam break of the tests, most steps need a few passes, and the steps where the front hits the wall need many more.
The memory is $O(n + q)$ for the pairs and their gradients.

## Properties

- **Larger steps.** The step is limited by the flow speed, not by a numerical speed of sound. The paper measured steps 35 times larger than WCSPH at $\eta = 1\%$ and 151 times larger at $0.1\%$, on its scenes.
- **Tolerance.** The user sets the density error $\eta$ directly.
- **Momentum.** Linear and angular momentum are kept by the pressure force (proved).
- **No convergence proof.** The loop is a Jacobi-like iteration with one factor $\delta$ for all particles. Particles with few neighbors get a $\delta$ that is too large, so the error can overshoot, as in the example.
- **Fixed neighbors.** The pairs of time $t$ are reused in the loop, so a pair that comes closer than $2h$ during the step is missed until the next step.

## Variants and improvements

- **Local factor.** Compute $\delta_i$ per particle from its own neighbors instead of the prototype. This costs one more pass over the pairs.
- **Implicit incompressible SPH.** [IISPH](/implicit-incompressible-sph/) writes the same density condition as a linear system in the pressures and solves it with relaxed Jacobi, with a per-particle diagonal.
- **Divergence-free SPH.** [DFSPH](/divergence-free-sph/) adds a second solver for the velocity divergence, which allows still larger steps.
- **Boundary particles.** Fixed particles on the walls that add to the density and get a pressure give smoother walls than the clamped walls of lines L6 and L12.
- **Other methods.** [Position based fluids](/position-based-fluids/) write the same density condition as a constraint on positions.

## When to use it

Use PCISPH when [WCSPH](/weakly-compressible-sph/) is too slow because of its small steps, and you want a solver that is still easy to write.
It needs only the SPH sums and a loop, with no matrix.
For large scenes, [IISPH](/implicit-incompressible-sph/) or [DFSPH](/divergence-free-sph/) usually converge in fewer passes.

## Pitfalls

- **Pressure not reset.** Line L3 sets $p_i = 0$ at the start of each step. If the pressures of the last step are kept without care, the first pass overshoots.
- **Prototype too small.** The lattice of the prototype must cover the full support $2h$. A partial neighborhood gives a too large $\delta$ and the loop of line L4 oscillates.
- **Unclamped surface pressure.** Without the clamp of line L9, free surface particles get negative pressures and clump.
- **Error sign.** Line L8 is $\rho^* - \rho_0$. With the opposite sign, line L9 lowers the pressure where the fluid is squeezed.
- **Gradients at the predicted positions.** Line L10 uses the gradients of time $t$, as in the derivation of $\delta$. Mixing predicted gradients with $\delta$ from time $t$ breaks the linear model.

## Implementations

## History

Before PCISPH, graphics used [WCSPH](/weakly-compressible-sph/) (Becker and Teschner 2007) or projection methods from engineering ([incompressible SPH](/incompressible-sph/)).
WCSPH needs a stiff equation of state and small steps, and projection methods need a linear solve.
Solenthaler and Pajarola (2009) took a middle path: a loop that predicts the density and corrects the pressure, with one precomputed factor.
Ihmsen et al. (2014) then wrote the same condition as a linear system in IISPH, and Bender and Koschier (2015) added a divergence solver in DFSPH.

## References
