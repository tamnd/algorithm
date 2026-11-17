---
tag: 9VJ2XT
kind: algorithm
slug: divergence-free-sph
name: Divergence-free SPH
aliases:
- DFSPH
area: graphics-and-signals/fluid-animation
level: research
summary: An SPH fluid solver with two Jacobi-like solvers in each step, one that keeps the density at the rest density and one that makes the velocity field divergence free.
solves: [fluid-simulation-for-animation]
model: real-ram
complexity:
  vars: {n: "the number of particles", q: "the number of neighbor pairs", k: "the number of solver iterations in a step"}
  time: {iteration: "O(n + q)", step: "O(k (n + q))"}
  space: {extra: "O(n + q)"}
properties: {deterministic: true, exact: false, conserves_linear_momentum: true, conserves_angular_momentum: true, iterative: true}
history:
  year: 2015
  people: [Jan Bender, Dan Koschier]
  note: Bender and Koschier presented DFSPH at the Symposium on Computer Animation 2015, with a divergence solver added to a density solver of the IISPH kind.
prereqs: [smoothed-particle-hydrodynamics, implicit-incompressible-sph]
see_also: [pcisph, weakly-compressible-sph, position-based-fluids, incompressible-sph, jacobi-method, courant-friedrichs-lewy-condition, fluid-simulation-for-animation, particle-fluid-surfacing]
sources:
  - paper: doi:10.1145/2786784.2786796
    title: Jan Bender and Dan Koschier, Divergence-free smoothed particle hydrodynamics, Symposium on Computer Animation 2015, 147-155
    locator: the factor alpha, the two solvers, the simulation loop and the results
  - paper: arxiv:2009.06944
    title: Dan Koschier, Jan Bender, Barbara Solenthaler and Matthias Teschner, Smoothed particle hydrodynamics techniques for the physics based simulation of fluids and solids, Eurographics tutorial, 2019
    locator: the section on pressure solvers
  - paper: doi:10.1109/TVCG.2013.105
    title: Markus Ihmsen, Jens Cornelis, Barbara Solenthaler, Christopher Horvath and Matthias Teschner, Implicit incompressible SPH, IEEE Transactions on Visualization and Computer Graphics 20(3), 426-435, 2014
    locator: the whole paper (the density system that the density solver of DFSPH also solves)
---

Divergence-free SPH (DFSPH) is an SPH fluid solver with two solvers in each step.
The density solver changes the velocities until the predicted density of each particle is at most the rest density $\rho_0$, on average within a tolerance $\eta$.
After the particles move, the divergence solver changes the velocities until the rate of change of the density is near 0, so the velocity field is divergence free.
Both solvers use one factor $\alpha_i$ per particle that depends only on the positions, so it is computed once for each solver.
The divergence solver is the main change from [IISPH](/implicit-incompressible-sph/), and the paper reports that it allows larger steps with fewer iterations.

## In plain words

Think of the water as many small balls.
First every ball gets its speed from gravity.
Then the method checks which balls would end up too crowded, and gives those balls a push away from their neighbors.
It does this a few times, until almost no ball would be too crowded.
Now the balls move.
At the new places, the method checks if the balls are still coming closer to each other.
If they are, it gives them a second kind of push, so they stop coming closer.
This second step stops the crowding before it starts in the next step, so the next step needs less work.

## The problem

The input is a set of $n$ particles with masses $m_i$, positions $x_i$ and velocities $v_i$, the rest density $\rho_0$, the smoothing length $h$, gravity $g = (0, -9.81)$ m/s², the step $\Delta t$ and the tolerances $\eta$ and $\eta_v$.
The output is the state after one step.
This is one method for [fluid simulation for animation](/fluid-simulation-for-animation/).
The kernel $W$ is the 2D cubic spline with support $2h$, as on [WCSPH](/weakly-compressible-sph/), $\nabla W_{ij}$ is its gradient with respect to $x_i$, and $\rho_i = \sum_j m_j W_{ij}$ with $j = i$ included.

The density rate and the factor of the paper are

$$\frac{D\rho_i}{Dt} = \sum_j m_j (v_i - v_j)\cdot\nabla W_{ij}, \qquad \alpha_i = \frac{\rho_i}{\left|\sum_j m_j\nabla W_{ij}\right|^2 + \sum_j\left|m_j\nabla W_{ij}\right|^2}.$$

A stiffness $\kappa_i$ on each particle changes the velocities by

$$v_i \leftarrow v_i - \Delta t\sum_j m_j\left(\frac{\kappa_i}{\rho_i} + \frac{\kappa_j}{\rho_j}\right)\nabla W_{ij}.$$

This is the symmetric SPH pressure force with the pressure $p_i = \kappa_i\rho_i$.

## The algorithm

```pseudo id=main
DFSPH-STEP(x, v, Δt)
L1  P ← neighbor pairs; ∇Wᵢⱼ; ρᵢ; αᵢ at x
L2  for each i: v*ᵢ ← vᵢ + Δt g
L3  while iter < 2 or (err > η ρ₀ and iter < max) do
L4      for each i: eᵢ ← max(ρᵢ + Δt (Dρᵢ/Dt)(v*) - ρ₀, 0); err ← mean of eᵢ
L5      for each i: κᵢ ← eᵢ αᵢ / Δt²
L6      for each i: v*ᵢ ← v*ᵢ - Δt Σⱼ mⱼ (κᵢ/ρᵢ + κⱼ/ρⱼ) ∇Wᵢⱼ
L7  for each i: xᵢ ← xᵢ + Δt v*ᵢ, clamped to the walls
L8  P ← neighbor pairs; ∇Wᵢⱼ; ρᵢ; αᵢ at the new x
L9  while iter < 1 or (err > η_v ρ₀ and iter < max) do
L10     for each i: dᵢ ← max((Dρᵢ/Dt)(v*), 0); err ← Δt × mean of dᵢ
L11     for each i: κᵢ ← dᵢ αᵢ / Δt
L12     for each i: v*ᵢ ← v*ᵢ - Δt Σⱼ mⱼ (κᵢ/ρᵢ + κⱼ/ρⱼ) ∇Wᵢⱼ
L13 return x, v ← v*
```

Line L1 computes the pairs, the densities and the factors.
In a full run they come from line L8 of the last step, as in the loop of the paper.
Line L2 adds the non-pressure forces; the tests use gravity only.
Lines L3 to L6 are the density solver.
Line L4 predicts the density with the current velocities, and line L5 picks $\kappa_i$ so that particle $i$ alone would remove its error exactly.
Line L7 moves the particles with symplectic Euler.
Line L8 finds the new neighbors and the new factors.
Lines L9 to L12 are the divergence solver, with $\kappa_i$ picked so that particle $i$ alone would make its density rate 0.
The minimum of 2 density passes and 1 divergence pass is the rule of the paper.
Both solvers here count only compression ($e_i > 0$ and $d_i > 0$), so a particle at the free surface gets no pull. This is a choice of this page.
The tolerance $\eta_v$ is a fraction of $\rho_0$ per step.
The step size comes from a CFL condition $\Delta t \le \lambda\,\Delta x / v_{max}$ with $\lambda = 0.4$ and a cap.

## Example

Take $\Delta x = 0.02$ m, $h = 1.3\Delta x$, $\rho_0 = 1000$ kg/m², $m_i = \rho_0\Delta x^2 = 0.4$ kg and $\Delta t = 0.004$ s.
Put 25 particles at rest on a 5 by 5 lattice with spacing $0.95\Delta x$, so the block is squeezed, and set $g = 0$.
The table follows the predicted density $\rho^*$ of line L4 in the density solver.

| pass | mean error | largest $\rho^*$ | $\rho^*$ of the center | compressed particles |
|---|---|---|---|---|
| 1 | 3.124% | 1109.56 | 1109.56 | 9 of 25 |
| 2 | 0% | 934.50 | 757.72 | 0 of 25 |

Pass 1 starts from rest, so it sees the squeeze of the block: the 9 inner particles are above $\rho_0$.
Line L5 gives each of them the stiffness that would remove its own error if it were alone.
But all 9 push at the same time, so the center particle gets the pushes of its neighbors too, and its predicted density falls far below $\rho_0$.
Pass 2 sees no compression, and the solver stops.
In a running simulation the error of each step is small, and this overshoot is small too.

## Correctness

The density solver and the divergence solver are Jacobi-like iterations without a proof of convergence in general.
The tests check these facts, and the [proof](proofs/correctness.md) gives the arguments:

- **One particle.** With equal masses, a stiffness $\kappa_i$ from line L5 on particle $i$ alone moves its predicted density to exactly $\rho_0$. The stiffness of line L11 alone moves its density rate to exactly 0.
- **Jacobi with weight 1.** With equal masses and without the max of line L4, one pass of lines L4 to L6 is one Jacobi pass with $\omega = 1$ on the pressure system of [IISPH](/implicit-incompressible-sph/), with $p_i = \rho_i\kappa_i$ summed over the passes. IISPH uses $\omega = 0.5$; the weight 1 explains the overshoot of the example.
- **Exit conditions.** If a solver stops before the cap, its mean error is at most its tolerance.
- **Momentum.** The update of lines L6 and L12 is a sum of pair terms, opposite on $i$ and $j$ and parallel to $x_i - x_j$. So without walls and gravity, the step keeps the total linear and angular momentum, for any $\kappa$.

## Complexity

One pass of either solver costs $O(n + q)$ time for $q$ pairs: one sweep over the pairs for the density rate and one for the update.
A step with $k$ passes in total costs $O(k(n + q))$, and lines L1 and L8 add $O(n + q)$ each.
With a density near $\rho_0$, $q = O(n)$.
The memory is $O(n + q)$.
The number $k$ is a measurement. In the small dam break of the tests, 50 steps of 0.004 s with $\eta = \eta_v = 0.1\%$ take 2 density passes and at most 4 divergence passes per step, and the measured mean compression stays below 0.7%.

## Properties

- **Factor once per solver.** $\alpha_i$ depends only on the positions, so lines L1 and L8 compute it once, and each pass costs two sweeps over the pairs.
- **Two errors.** The density solver removes the density error, and the divergence solver removes the rate at which it grows. Without the divergence solver, the density solver must remove the error that the velocity field builds up in each step.
- **Momentum.** Linear and angular momentum are kept by both updates (proved).
- **Overshoot.** With weight 1, a strongly squeezed block overshoots in one pass, as in the example.
- **Larger steps.** The paper reports larger steps and less total work than IISPH and PCISPH on its scenes. These are measurements.

## Variants and improvements

- **Warm start.** The paper starts each solver with the stiffness values of the last step, which lowers the number of passes. The code here starts from zero.
- **Relaxation.** A weight below 1 on line L5 lowers the overshoot and needs more passes, as in IISPH.
- **Boundary particles.** Fixed particles on the walls take part in $\rho_i$, $\alpha_i$ and the update, and give smoother walls than the clamp of line L7.
- **Without the divergence solver.** Lines L1 to L7 alone are a density solver of the IISPH kind; see [IISPH](/implicit-incompressible-sph/) and [PCISPH](/pcisph/).

## When to use it

Use DFSPH for SPH liquids with a small density error at large steps, in particular in deep or fast scenes, where the divergence solver saves passes in the density solver.
For small scenes, [IISPH](/implicit-incompressible-sph/) is simpler.
For a solver on positions, see [position based fluids](/position-based-fluids/).

## Pitfalls

- **Old factors in the divergence solver.** Line L8 must compute $\alpha_i$ at the new positions. Factors of line L1 belong to the old neighbors.
- **Small denominator.** A particle with no neighbors has a denominator 0 in $\alpha_i$. Clamp the denominator at a small value, as the code does with $10^{-6}$, or skip the particle.
- **Different powers of the step.** Line L5 divides by $\Delta t^2$ and line L11 by $\Delta t$. With the same power in both, one solver is off by a factor $\Delta t$.
- **Divergence of the wrong velocities.** Line L10 uses the velocities after line L7, at the new positions. Using the velocities of line L2 repeats the density solve.
- **Surface pull.** Without the max of lines L4 and L10, particles at the free surface get a negative stiffness and the surface clumps.

## Implementations

## History

[PCISPH](/pcisph/) (Solenthaler and Pajarola 2009) and [IISPH](/implicit-incompressible-sph/) (Ihmsen et al. 2014) solve for a pressure that keeps the density near $\rho_0$.
Bender and Koschier (2015) added a second solver for the velocity divergence, with one factor $\alpha_i$ for both solvers.
Their open source library SPlisHSPlasH and the tutorial of Koschier, Bender, Solenthaler and Teschner (2019) put DFSPH next to the other pressure solvers.

## References
