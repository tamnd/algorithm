---
tag: V1STXV
kind: algorithm
slug: implicit-incompressible-sph
name: Implicit incompressible SPH
aliases:
- IISPH
area: graphics-and-signals/fluid-animation
level: advanced
summary: An SPH fluid solver that finds the pressures from a linear system, a discrete pressure Poisson equation, solved by relaxed Jacobi iteration so that the predicted density is the rest density.
solves: [fluid-simulation-for-animation]
model: real-ram
complexity:
  vars: {n: "the number of particles", q: "the number of neighbor pairs", k: "the number of Jacobi iterations"}
  time: {iteration: "O(n + q)", step: "O(k (n + q))"}
  space: {extra: "O(n + q)"}
properties: {deterministic: true, exact: false, conserves_linear_momentum: true, conserves_angular_momentum: true, iterative: true}
history:
  year: 2014
  people: [Markus Ihmsen, Jens Cornelis, Barbara Solenthaler, Christopher Horvath, Matthias Teschner]
  note: Ihmsen and his coauthors wrote the density condition of PCISPH as a linear system in the pressures and solved it with relaxed Jacobi.
prereqs: [smoothed-particle-hydrodynamics, jacobi-method, pcisph]
see_also: [weakly-compressible-sph, divergence-free-sph, position-based-fluids, incompressible-sph, poisson-equation, sph-smoothing-kernel, fluid-simulation-for-animation, particle-fluid-surfacing]
sources:
  - paper: doi:10.1109/TVCG.2013.105
    title: Markus Ihmsen, Jens Cornelis, Barbara Solenthaler, Christopher Horvath and Matthias Teschner, Implicit incompressible SPH, IEEE Transactions on Visualization and Computer Graphics 20(3), 426-435, 2014
    locator: the derivation of the pressure system, the relaxed Jacobi solver with omega = 0.5 and the results
  - paper: arxiv:2009.06944
    title: Dan Koschier, Jan Bender, Barbara Solenthaler and Matthias Teschner, Smoothed particle hydrodynamics techniques for the physics based simulation of fluids and solids, Eurographics tutorial, 2019
    locator: the section on pressure solvers (the operator form of the IISPH system)
  - paper: doi:10.1145/1531326.1531346
    title: Barbara Solenthaler and Renato Pajarola, Predictive-corrective incompressible SPH, ACM Transactions on Graphics 28(3), article 40, 2009
    locator: the whole paper (the density condition that IISPH writes as a linear system)
---

Implicit incompressible SPH (IISPH) is an SPH fluid solver that finds the pressures from a linear system.
The system says that after the step, the density of each particle predicted to first order is the rest density $\rho_0$.
It is a discrete form of the [pressure Poisson equation](/poisson-equation/), with one unknown pressure per particle.
IISPH solves it with relaxed [Jacobi iteration](/jacobi-method/), with no matrix in memory, and stops when the mean predicted compression is below a tolerance $\eta$ such as 0.1%.
Like [PCISPH](/pcisph/), it allows steps much larger than [weakly compressible SPH](/weakly-compressible-sph/).

## In plain words

Think of the water as many small balls.
First, every ball moves a little with gravity alone, and the method checks which balls would end up too crowded.
Then it looks for pressures that push the balls apart just enough to remove the crowding.
Each pressure has an effect on the neighbors too, so all the pressures are linked.
The method guesses all the pressures, checks the crowding that they give, and improves each guess a little.
After a few rounds the crowding is very small, and the balls move for real.
The pressures of the last step are a good first guess for the next step.

## The problem

The input is a set of $n$ particles with masses $m_i$, positions $x_i$ and velocities $v_i$, the rest density $\rho_0$, the smoothing length $h$, gravity $g = (0, -9.81)$ m/s², the step $\Delta t$ and the tolerance $\eta$.
The output is the state after one step and the pressures $p_i \ge 0$.
This is one method for [fluid simulation for animation](/fluid-simulation-for-animation/).
The kernel $W$ is the 2D cubic spline with support $2h$, as on [WCSPH](/weakly-compressible-sph/), $\nabla W_{ij}$ is its gradient with respect to $x_i$, and $\rho_i = \sum_j m_j W_{ij}$ with $j = i$ included.

The pressure acceleration and the operator $A$ are

$$a^p_i = -\sum_j m_j\left(\frac{p_i}{\rho_i^2} + \frac{p_j}{\rho_j^2}\right)\nabla W_{ij}, \qquad (Ap)_i = \Delta t^2\sum_j m_j\,(a^p_i - a^p_j)\cdot\nabla W_{ij}.$$

With $v^{adv}_i = v_i + \Delta t\,g$, the density after the step is $\rho^{adv}_i + (Ap)_i$ to first order, where $\rho^{adv}_i = \rho_i + \Delta t\sum_j m_j(v^{adv}_i - v^{adv}_j)\cdot\nabla W_{ij}$.
IISPH solves $Ap = s$ with $s_i = \rho_0 - \rho^{adv}_i$.
This operator form is the one of the tutorial of Koschier et al.; the paper writes the same system with displacement terms $d_{ii}$ and $d_{ij}$.

## The algorithm

```pseudo id=main
IISPH-STEP(x, v, p_prev, Δt)
L1  P ← neighbor pairs; store ∇Wᵢⱼ; ρᵢ ← Σⱼ mⱼ Wᵢⱼ
L2  for each i: vᵃᵈᵛᵢ ← vᵢ + Δt g
L3  for each i: sᵢ ← ρ₀ - ρᵢ - Δt Σⱼ mⱼ (vᵃᵈᵛᵢ - vᵃᵈᵛⱼ)·∇Wᵢⱼ
L4  for each i: aᵢᵢ ← -(Δt²/ρᵢ²) (|Σⱼ mⱼ ∇Wᵢⱼ|² + mᵢ Σⱼ mⱼ |∇Wᵢⱼ|²)
L5  for each i: pᵢ ← 0.5 p_prevᵢ
L6  while iter < 2 or (err > η ρ₀ and iter < max) do
L7      compute aᵖ from p, then (Ap)ᵢ for each i
L8      for each i: pᵢ ← max(0, pᵢ + ω (sᵢ - (Ap)ᵢ) / aᵢᵢ)
L9      err ← mean over i of max((Ap)ᵢ - sᵢ, 0)
L10 for each i: vᵢ ← vᵃᵈᵛᵢ + Δt aᵖᵢ
L11 for each i: xᵢ ← xᵢ + Δt vᵢ, clamped to the walls
```

Line L1 finds the pairs with the grid search and keeps them for the step.
Line L2 adds the non-pressure forces; the tests use gravity only.
Line L3 is the right side: the density error that the advected velocities would give.
Line L4 is the diagonal of $A$, the coefficient of $p_i$ in $(Ap)_i$.
It has two parts: $p_i$ pushes $i$ away from all neighbors, and it pushes each neighbor away from $i$.
Line L5 is the warm start of the paper, half the pressure of the last step.
Lines L7 and L8 are one step of Jacobi with relaxation $\omega = 0.5$, the value of the paper.
Line L8 also clamps each pressure at 0, so a particle at the free surface does not pull its neighbors.
Line L9 measures the mean predicted compression $\rho^{adv}_i + (Ap)_i - \rho_0$, counted only where it is positive.
The loop runs at least 2 times, as in the paper.
Lines L10 and L11 are symplectic Euler with the final pressure acceleration.

## Example

Take $\Delta x = 0.02$ m, $h = 1.3\Delta x$, $\rho_0 = 1000$ kg/m², $m_i = \rho_0\Delta x^2 = 0.4$ kg and $\Delta t = 0.004$ s.
Put 25 particles at rest on a 5 by 5 lattice with spacing $0.95\Delta x$, so the block is squeezed, and set $g = 0$, $p_{prev} = 0$ and $\eta = 0.05\%$.
The table gives the error of line L9 in each pass, as a fraction of $\rho_0$, and the largest pressure after the pass.

| pass | mean error | max pressure |
|---|---|---|
| 1 | 3.124% | 6389.0 |
| 2 | 0.079% | 4273.3 |
| 3 | 0.398% | 5205.6 |
| 4 | 0.161% | 5739.7 |
| 5 | 0.163% | 6198.9 |
| 6 | 0.095% | 6515.5 |
| 7 | 0.063% | 6724.9 |
| 8 | 0.054% | 6903.4 |
| 9 | 0.048% | 7061.8 |

Pass 1 starts from $p = 0$, so its error is the squeeze of the block itself.
The error does not fall in each pass: the clamp of line L8 changes the system as pressures reach 0, and the edge particles of the block have few neighbors.
Pass 9 is below $\eta$, so the loop stops.
With $\eta = 0.1\%$ the loop stops after pass 2.

## Correctness

IISPH solves a linear system, but the clamp of line L8 makes the iteration nonlinear, and the paper gives no proof that the clamped loop converges.
The tests check these facts, and the [proof](proofs/correctness.md) gives the arguments:

- **The system is the density condition.** $(Ap)_i$ is the first order change of $\rho_i$ when every particle $j$ moves by $\Delta t^2 a^p_j$, which is what the pressure does to the positions in lines L10 and L11. So $Ap = s$ means that the predicted density is $\rho_0$.
- **The diagonal.** Line L4 is the coefficient of $p_i$ in $(Ap)_i$, and it is negative when $i$ has a neighbor.
- **Fixed points.** Without the clamp, a fixed point of line L8 solves $Ap = s$. The tests compare the result with Gaussian elimination.
- **Exit condition.** If the loop stops before the cap, the mean predicted compression is at most $\eta\rho_0$.
- **Momentum.** The pressure acceleration is a sum of pair terms, opposite on $i$ and $j$ and parallel to $x_i - x_j$. So without walls and gravity, the step keeps the total linear and angular momentum, for any $p$.

The predicted density is a first order model.
The measured compression after the step is larger: in the squeezed block above it is 0.57% after the step with $\eta = 0.1\%$.

## Complexity

One pass costs $O(n + q)$ time for $q$ pairs: line L7 is two sweeps over the pairs, and line L8 is one sweep over the particles.
A step with $k$ passes costs $O(k(n + q))$, and lines L1 to L4 add $O(n + q)$ once.
With a density near $\rho_0$, $q = O(n)$.
The memory is $O(n + q)$; the matrix $A$ is never stored.
The number $k$ is a measurement, not a bound. The paper reports fewer passes and larger steps than PCISPH on its scenes, at $\eta = 0.1\%$.

## Properties

- **Matrix free.** Line L7 computes $Ap$ from the SPH sums, so the cost per pass is the cost of two SPH sums.
- **Per-particle diagonal.** Each particle has its own $a_{ii}$, so a particle with few neighbors gets a smaller step than in PCISPH, where one factor $\delta$ is used for all.
- **Not symmetric.** With different masses or densities, $A$ is not symmetric, so the [conjugate gradient method](/conjugate-gradient-method/) does not apply directly.
- **Momentum.** Linear and angular momentum are kept by the pressure force (proved).
- **Slow smooth errors.** Jacobi removes local errors fast and smooth errors over many particles slowly. So deep fluids need more passes (a heuristic). In the tests, the unclamped solve of 16 particles needs about 200 passes for a relative error of $10^{-5}$ (measured).

## Variants and improvements

- **Displacement form.** The paper computes the same system with the terms $d_{ii} = -\Delta t^2\sum_j (m_j/\rho_i^2)\nabla W_{ij}$ and $\sum_j d_{ij}p_j$, which are the pressure displacements.
- **Divergence-free SPH.** [DFSPH](/divergence-free-sph/) uses a density solver of the same kind and adds a second solver that makes the velocity field divergence free.
- **Boundary particles.** Fixed particles on the walls take part in $\rho_i$ and in $A$, and give smoother walls than the clamp of line L11.
- **Other solvers.** Conjugate gradient or multigrid on a symmetric form of the system, as in projection methods of [incompressible SPH](/incompressible-sph/) in engineering.

## When to use it

Use IISPH for SPH liquids with a small density error, such as 0.1%, at large steps.
It is a good default when [PCISPH](/pcisph/) needs too many passes, because the per-particle diagonal handles the free surface better.
For deep or large scenes, add the divergence solver of [DFSPH](/divergence-free-sph/), or use a grid method such as [FLIP](/fluid-implicit-particle/).

## Pitfalls

- **Sign of the diagonal.** The diagonal of line L4 is negative. Line L8 divides by $a_{ii}$, so with a positive diagonal the pressure goes the wrong way.
- **Missing self term.** Line L4 has the term $m_i\sum_j m_j|\nabla W_{ij}|^2$, the push of $p_i$ on the neighbors. Without it, the diagonal is near 0 inside the fluid, where $\sum_j \nabla W_{ij} \approx 0$.
- **Error with the clamp.** Line L9 counts only compression. If it also counts the low density at the free surface, the loop never reaches $\eta$.
- **Predicted is not measured.** The error of line L9 is a first order prediction. Do not report it as the density error of the result.
- **No minimum.** Without the 2 passes of line L6, a warm start can stop the loop at once with a pressure from the last step.

## Implementations

## History

[PCISPH](/pcisph/) (Solenthaler and Pajarola 2009) corrects the pressure with one factor from a prototype particle.
Ihmsen, Cornelis, Solenthaler, Horvath and Teschner (2014) wrote the same density condition as a linear system with a per-particle diagonal and solved it with relaxed Jacobi.
Bender and Koschier (2015) then added a divergence solver in [DFSPH](/divergence-free-sph/).
The tutorial of Koschier, Bender, Solenthaler and Teschner (2019) writes the IISPH system in the operator form used here.

## References
