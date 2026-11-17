---
tag: XB7CYE
kind: algorithm
slug: weakly-compressible-sph
name: Weakly compressible SPH
aliases: [WCSPH]
area: graphics-and-signals/fluid-animation
level: advanced
summary: An SPH fluid solver that computes pressure from density with a stiff Tait equation of state, so the fluid compresses by about 1% and needs no pressure solve, at the cost of small time steps.
solves: [fluid-simulation-for-animation]
model: real-ram
complexity:
  vars: {n: "the number of particles", q: "the number of neighbor pairs", c: "the numerical speed of sound", h: "the smoothing length"}
  time: {step: "O(n + q)", steps_per_unit_time: "Θ(c / h)"}
  space: {extra: "O(n + q)"}
properties: {deterministic: true, exact: false, conserves_linear_momentum: true, conserves_angular_momentum: true, implicit: false}
history:
  year: 1994
  people: [Joe J. Monaghan, Markus Becker, Matthias Teschner]
  note: Monaghan used the Tait equation for free surface SPH in 1994. Becker and Teschner brought the weakly compressible form to computer graphics in 2007.
prereqs: [smoothed-particle-hydrodynamics, fluid-simulation-for-animation, symplectic-euler-method]
see_also: [pcisph, implicit-incompressible-sph, divergence-free-sph, position-based-fluids, incompressible-sph, sph-smoothing-kernel, particle-fluid-surfacing, uniform-grid]
sources:
  - paper: doi:10.1006/jcph.1994.1034
    title: Joe J. Monaghan, Simulating free surface flows with SPH, Journal of Computational Physics 110(2), 399-406, 1994
    locator: the whole paper (the Tait equation of state and the choice of the speed of sound)
  - paper: doi:10.2312/SCA/SCA07/209-218
    title: Markus Becker and Matthias Teschner, Weakly compressible SPH for free surface flows, Symposium on Computer Animation 2007, 209-217
    locator: the whole paper (the Tait equation with gamma = 7 for graphics fluids)
  - paper: doi:10.1146/annurev.aa.30.090192.002551
    title: Joe J. Monaghan, Smoothed particle hydrodynamics, Annual Review of Astronomy and Astrophysics 30, 543-574, 1992
    locator: the whole paper (the cubic spline kernel, the symmetric pressure term and the artificial viscosity)
  - paper: arxiv:2009.06944
    title: Dan Koschier, Jan Bender, Barbara Solenthaler and Matthias Teschner, Smoothed particle hydrodynamics techniques for the physics based simulation of fluids and solids, Eurographics tutorial, 2019
    locator: the sections on the state equation and on time stepping
---

Weakly compressible SPH (WCSPH) moves a fluid as a set of particles and computes the pressure of each particle directly from its density.
It uses the stiff Tait equation of state $p = B((\rho/\rho_0)^7 - 1)$, so a small compression gives a large pressure that pushes the particles apart.
With a numerical speed of sound $c$ about ten times the largest flow speed, the density stays within about 1% of the rest density $\rho_0$.
There is no linear system to solve, but the time step must shrink as $c$ grows, and this is the main cost of the method.

## In plain words

Think of the water as many small balls.
Each ball looks at the balls near it and counts how crowded its place is.
That count is its density.
If the place is more crowded than water at rest, the ball gets a high pressure.
High pressure pushes the neighbors away, and the push between two balls is equal and opposite.
Gravity pulls all balls down.
Then each ball changes its speed and moves a short distance, and the loop starts again.
The pressure rule is very stiff, so water is squeezed only a little.
A stiff rule needs very short steps, or the balls fly apart.
So the method is simple to write, but it takes many steps for each second of motion.

## The problem

The input is a set of $n$ particles with positions $x_i$, velocities $v_i$ and masses $m_i$, a rest density $\rho_0$, the smoothing length $h$, gravity $g = (0, -9.81)$ m/s², and a time step $\Delta t$.
The output is the state after one step.
The particles carry the [smoothed particle hydrodynamics](/smoothed-particle-hydrodynamics/) approximation of the Euler equations of a fluid with a free surface, as one method for [fluid simulation for animation](/fluid-simulation-for-animation/).
The page works in 2D, where a density is in kg/m².

The kernel is the cubic spline of Monaghan with support $2h$ and the 2D constant $\sigma = 10/(7\pi)$, so $W(0, h) = 0.454728/h^2$ (see [SPH smoothing kernel](/sph-smoothing-kernel/)).
We write $W_{ij} = W(|x_i - x_j|, h)$ and $\nabla W_{ij}$ for its gradient with respect to $x_i$.
This gradient is antisymmetric: $\nabla W_{ji} = -\nabla W_{ij}$, and it points along $x_i - x_j$.

## The algorithm

```pseudo id=main
WCSPH-STEP(x, v, m, Δt)                                   ▷ one step, 2D
L1  P ← all pairs (i, j), i < j, with |xᵢ - xⱼ| < 2h      ▷ uniform grid search
L2  for each i: ρᵢ ← Σⱼ mⱼ Wᵢⱼ                             ▷ j = i included
L3  for each i: pᵢ ← B ((ρᵢ / ρ₀)^γ - 1), B = ρ₀ c² / γ    ▷ γ = 7
L4  for each i: aᵢ ← g
L5  for each pair (i, j) in P do
L6      s ← pᵢ / ρᵢ² + pⱼ / ρⱼ²
L7      if (vᵢ - vⱼ)·(xᵢ - xⱼ) < 0 then s ← s + Πᵢⱼ     ▷ artificial viscosity
L8      aᵢ ← aᵢ - mⱼ s ∇Wᵢⱼ;  aⱼ ← aⱼ + mᵢ s ∇Wᵢⱼ
L9  for each i: vᵢ ← vᵢ + Δt aᵢ                           ▷ symplectic Euler
L10 for each i: xᵢ ← xᵢ + Δt vᵢ                           ▷ uses the new velocity
L11 apply the walls
```

Line L1 puts the particles in a [uniform grid](/uniform-grid/) with cells of side $2h$ and tests only the 3 by 3 block of cells around each particle.
Line L2 is the SPH density sum, and line L3 is the Tait equation of state with $\gamma = 7$.
Lines L5 to L8 add the pressure force of each pair once, with opposite signs on the two particles.
The term in line L6 is the symmetric form of the pressure gradient $-\nabla p / \rho$.
Line L7 adds the artificial viscosity of Monaghan, $\Pi_{ij} = -\alpha c \mu_{ij} / \bar\rho_{ij}$ with $\mu_{ij} = h\,(v_i - v_j)\cdot(x_i - x_j) / (|x_i - x_j|^2 + 0.01 h^2)$ and $\bar\rho_{ij} = (\rho_i + \rho_j)/2$.
It acts only on pairs that approach each other, and $\alpha$ is a tuning constant (the tests use 0.1).
Lines L9 and L10 are [symplectic Euler](/symplectic-euler-method/): the position update uses the velocity of the new step.
Line L11 is a simple wall model, outside the method: it clamps each particle into the box and removes the velocity into the wall.
Better wall models use fixed boundary particles that add to the density.

The constants come from two rules.
The speed of sound is $c \approx 10\,v_{\max}$, where $v_{\max}$ is the largest expected speed, for example $(2 g H)^{1/2}$ for a column of height $H$.
The step obeys $\Delta t \le \lambda h / (c + v_{\max})$ with $\lambda \approx 0.4$.
Both are heuristics.

## Example

Take two particles of mass 1 at $x_1 = (0, 0)$ and $x_2 = (1, 0)$, at rest, with $h = 1$, $\rho_0 = 0.5$, $c = 1$, no gravity and $\Delta t = 0.1$.
Then $W(0) = 0.454728$ and $W(1) = 0.113682$, so line L2 gives $\rho_1 = \rho_2 = 0.568411$.
This is above $\rho_0$, so line L3 gives a positive pressure.
At $r = 1$ the kernel slope is $dW/dr = -0.341046$, and $\nabla W_{12} = (0.341046, 0)$.
Line L8 pushes particle 1 to the left and particle 2 to the right with equal and opposite accelerations.

| step | $x_1$ | $v_1$ | $\rho_1$ | $p_1$ | $a_1$ |
|---|---|---|---|---|---|
| 0 | $(0, 0)$ | $(0, 0)$ | 0.568411 | 0.103845 | $(-0.219233, 0)$ |
| 1 | $(-0.002192, 0)$ | $(-0.021923, 0)$ | 0.566922 | 0.100657 | $(-0.211750, 0)$ |
| 2 | $(-0.006502, 0)$ | $(-0.043098, 0)$ | 0.564033 | 0.094611 | $(-0.197610, 0)$ |

Particle 2 is the mirror image: $x_2 = (1, 0) - x_1$ and $v_2 = -v_1$ in each row.
The particles move apart, the density drops toward $\rho_0$, and the pressure falls.
The sum $m_1 v_1 + m_2 v_2$ stays 0.

## Correctness

WCSPH does not solve the incompressible equations exactly.
It solves a slightly compressible fluid, and the stiff equation of state keeps the compression small.
Three things are exact for the discrete method.

- **Linear momentum.** Without walls and gravity, each pair in line L8 adds $-m_i m_j s\nabla W_{ij}$ to the momentum of $i$ and $+m_i m_j s\nabla W_{ij}$ to that of $j$. The sum is 0, so $\sum_i m_i v_i$ does not change in line L9. This is a proved property.
- **Angular momentum.** The pair force is parallel to $x_i - x_j$, because $\nabla W_{ij}$ is. So the internal torques cancel, and under symplectic Euler $\sum_i m_i\, x_i \times v_i$ is the same after the step. This is a proved property.
- **Rest state.** A particle with a density of exactly $\rho_0$ has $p = 0$.

The size of the compression is an estimate, not a theorem.
For a small relative compression $e$, $p \approx \rho_0 c^2 e$.
The pressure needed to turn a flow of speed $v$ is of order $\rho_0 v^2$, so $e$ is of order $(v/c)^2$, and $c = 10\,v_{\max}$ gives about 1% (Monaghan 1994).
The [proof](proofs/correctness.md) gives the momentum arguments in full.

## Complexity

One step costs $O(n + q)$ time for $q$ neighbor pairs: the grid search in line L1 visits each particle and its candidate pairs, and lines L2 to L10 do constant work per particle and per pair.
If the density stays near $\rho_0$, each particle has a bounded number of neighbors in its disk of radius $2h$, so $q = O(n)$ and the step costs $O(n)$.
A test of all pairs would cost $\Theta(n^2)$.
The memory is $O(n + q)$ for the grid and the pair list.

The time step is the real cost.
The step limit is proportional to $h/c$, so a simulated time $T$ needs $\Theta(T c / h)$ steps.
Halving the density error needs about $\sqrt{2}$ times larger $c$, so about $\sqrt{2}$ times more steps.

## Properties

- **Explicit.** No linear system and no iteration. Each step is one pass over the pairs.
- **Momentum.** Linear and angular momentum are conserved by the internal forces (proved above). The walls of line L11 do not conserve them.
- **Compressible.** The density error is of order $(v/c)^2$ and is not bounded by a user tolerance. The incompressible solvers [PCISPH](/pcisph/), [IISPH](/implicit-incompressible-sph/) and [DFSPH](/divergence-free-sph/) iterate to a stated tolerance instead.
- **Stiff.** The step limit falls as $1/c$. In a measured comparison, PCISPH took steps 35 times larger at the same 1% density error (Solenthaler and Pajarola 2009).
- **Tensile instability.** Negative pressures at the free surface pull particles into clumps. Clamping $p$ at 0 removes the pull but makes the surface less smooth.

## Variants and improvements

- **Clamped pressure.** Set $p_i = \max(p_i, 0)$ in line L3. The tests use this for the dam break, so the free surface does not clump.
- **Other equations of state.** The linear law $p = c^2(\rho - \rho_0)$ is less stiff and allows larger steps for the same $c$, but compresses more under the same load.
- **Physical viscosity.** Replace $\Pi_{ij}$ by a Laplacian form for a given kinematic viscosity, as in [smoothed particle hydrodynamics](/smoothed-particle-hydrodynamics/).
- **Incompressible solvers.** [PCISPH](/pcisph/) predicts and corrects the pressure, and [IISPH](/implicit-incompressible-sph/) and [DFSPH](/divergence-free-sph/) solve a pressure equation. [Incompressible SPH](/incompressible-sph/) in engineering uses a projection.
- **Position based fluids.** [PBF](/position-based-fluids/) enforces the density as a constraint on positions and takes large steps.

## When to use it

Use WCSPH for small scenes, for teaching, and as a reference to test other SPH solvers.
It is short to write, it runs on GPUs with one pass per step, and its forces conserve momentum.
For large scenes with deep water, the stiff step limit makes it slow; use an incompressible solver.
For a surface to render, add a [surfacing](/particle-fluid-surfacing/) step.

## Pitfalls

- **Too small c.** If $c$ is close to the flow speed, line L3 gives too little pressure and the fluid compresses by much more than 1%.
- **Too large step.** A step above $\lambda h/(c + v_{\max})$ makes lines L9 and L10 unstable, and the particles explode.
- **Missing neighbors at walls.** With the clamp walls of line L11, particles near a wall have fewer neighbors, so line L2 gives a low density there. Boundary particles fix this.
- **One-sided pair update.** Line L8 must change both particles by the same pair term. A loop over each particle with its own form of the term loses momentum conservation.
- **Wrong cell size.** The grid of line L1 needs a cell side at least $2h$, the kernel support. A smaller cell misses neighbors.

## Implementations

## History

Lucy (1977) and Gingold and Monaghan (1977) introduced SPH for astrophysics.
Monaghan (1992) reviewed the method, with the cubic spline kernel and the artificial viscosity.
Monaghan (1994) used the Tait equation of state to simulate free surface flows with a small compression.
Becker and Teschner (2007) used the weakly compressible form with $\gamma = 7$ for fluids in computer graphics.
Later solvers in graphics, such as PCISPH (2009), IISPH (2014) and DFSPH (2015), keep the SPH sums but replace the equation of state by a pressure iteration.

## References
