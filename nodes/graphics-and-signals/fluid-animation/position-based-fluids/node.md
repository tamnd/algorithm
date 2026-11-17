---
tag: XH6YNA
kind: algorithm
slug: position-based-fluids
name: Position based fluids
aliases:
- PBF
area: graphics-and-signals/fluid-animation
level: advanced
summary: A particle fluid solver that keeps the SPH density of each particle near the rest density as a constraint on positions, solved by a few Jacobi passes of position based dynamics.
solves: [fluid-simulation-for-animation]
model: real-ram
complexity:
  vars: {n: "the number of particles", q: "the number of neighbor pairs", k: "the number of solver passes"}
  time: {pass: "O(n + q)", step: "O(k (n + q))"}
  space: {extra: "O(n + q)"}
properties: {deterministic: true, exact: false, conserves_linear_momentum: true, conserves_angular_momentum: false, iterative: true}
history:
  year: 2013
  people: [Miles Macklin, Matthias Müller]
  note: Macklin and Müller wrote the SPH density condition as a position constraint in the position based dynamics loop, for real time fluids on the GPU.
prereqs: [smoothed-particle-hydrodynamics, fluid-simulation-for-animation]
see_also: [pcisph, implicit-incompressible-sph, divergence-free-sph, vorticity-confinement, sph-smoothing-kernel, jacobi-method, fixed-radius-near-neighbors, particle-fluid-surfacing]
sources:
  - paper: doi:10.1145/2461912.2461984
    title: Miles Macklin and Matthias Müller, Position based fluids, ACM Transactions on Graphics 32(4), article 104, 2013
    locator: the density constraint, the relaxation eps, the artificial pressure s_corr with k = 0.1 and n = 4, XSPH viscosity, vorticity confinement and the simulation loop
  - paper: doi:10.1016/j.jvcir.2007.01.005
    title: Matthias Müller, Bruno Heidelberger, Marcus Hennix and John Ratcliff, Position based dynamics, Journal of Visual Communication and Image Representation 18(2), 109-118, 2007
    locator: the whole paper (the position based loop and the constraint projection)
  - paper: "Matthias Müller, David Charypar and Markus Gross, Particle-based fluid simulation for interactive applications, Symposium on Computer Animation 2003, 154-159"
    title: Matthias Müller, David Charypar and Markus Gross, Particle-based fluid simulation for interactive applications, Symposium on Computer Animation 2003, 154-159
    locator: the poly6 and spiky kernels
  - paper: doi:10.1016/0021-9991(89)90032-6
    title: Joe J. Monaghan, On the problem of penetration in particle methods, Journal of Computational Physics 82(1), 1-15, 1989
    locator: the whole paper (the XSPH velocity correction)
---

Position based fluids (PBF) is a particle fluid solver in the frame of [position based dynamics](/position-based-dynamics/).
Each particle has one constraint: its SPH density, computed at the predicted positions, must equal the rest density $\rho_0$.
A few passes move the predicted positions to satisfy these constraints, all particles at once, like a [Jacobi](/jacobi-method/) step.
The velocity is then the change of position divided by the step.
An artificial pressure term keeps particles from clumping, and XSPH viscosity smooths the velocities.
The method is stable at the large steps of real time graphics, at the cost of a fixed and inexact number of passes.

## In plain words

Think of the water as many small balls.
First every ball moves with gravity alone, to a guessed place.
At the guessed places, the method counts how crowded each ball is.
Where a ball is too crowded, it and its neighbors are pushed apart by a small amount, all at the same time.
After a few rounds of pushes, the balls are close to the right crowding.
The speed of each ball is then the distance it went in this step, divided by the time.
A small extra push keeps balls from sticking together, and a small blend of the speeds of neighbors makes the flow smooth.

## The problem

The input is a set of $n$ particles of equal mass $m$ with positions $x_i$ and velocities $v_i$, the rest density $\rho_0$, the kernel radius $h$, gravity $g = (0, -9.81)$ m/s², the step $\Delta t$ and the number of passes $k$.
The output is the state after one step.
This is one method for [fluid simulation for animation](/fluid-simulation-for-animation/).
PBF uses two kernels of the paper of Müller, Charypar and Gross (2003), both with support $h$. In 2D,

$$W_{poly6}(r) = \frac{4}{\pi h^8}(h^2 - r^2)^3, \qquad W_{spiky}(r) = \frac{10}{\pi h^5}(h - r)^3,$$

for $r < h$, so $4/\pi = 1.273240$ and $10/\pi = 3.183099$.
The density uses poly6, $\rho_i = \sum_j m\,W_{poly6}(|x_i - x_j|)$ with $j = i$ included, and the gradients use spiky, $\nabla W_{ij} = \nabla W_{spiky}(x_i - x_j)$.
The constraint and its gradients are

$$C_i = \frac{\rho_i}{\rho_0} - 1, \qquad \nabla_{x_i} C_i = \frac{m}{\rho_0}\sum_j \nabla W_{ij}, \qquad \nabla_{x_j} C_i = -\frac{m}{\rho_0}\nabla W_{ij}.$$

## The algorithm

```pseudo id=main
PBF-STEP(x, v, Δt)
L1  for each i: vᵢ ← vᵢ + Δt g; x*ᵢ ← xᵢ + Δt vᵢ, clamped to the walls
L2  P ← neighbor pairs of x* within h
L3  repeat k times
L4      for each i: Cᵢ ← ρᵢ(x*) / ρ₀ - 1, or max(0, ρᵢ(x*) / ρ₀ - 1)
L5      for each i: λᵢ ← -Cᵢ / (Σₖ |∇ₖ Cᵢ|² + ε)
L6      for each i: Δxᵢ ← (m/ρ₀) Σⱼ (λᵢ + λⱼ + s_corr,ᵢⱼ) ∇Wᵢⱼ
L7      for each i: x*ᵢ ← x*ᵢ + Δxᵢ, clamped to the walls
L8  for each i: vᵢ ← (x*ᵢ - xᵢ) / Δt
L9  for each i: vᵢ ← vᵢ + c Σⱼ (m/ρ₀) (vⱼ - vᵢ) W_poly6(|x*ᵢ - x*ⱼ|)
L10 for each i: xᵢ ← x*ᵢ
```

Line L1 is the prediction of position based dynamics.
Line L2 finds the neighbors once per step, as in the paper; pairs that come within $h$ during the passes are missed until the next step.
Line L5 is the Newton step for one constraint, $C_i + \nabla C_i\cdot\Delta x = 0$ with $\Delta x$ along $\nabla C_i$, softened by the relaxation $\varepsilon$.
Without $\varepsilon$, a particle with few neighbors has a denominator near 0 and a huge $\lambda_i$.
Line L6 adds the corrections of the constraint of $i$ and of the constraints of its neighbors.
The artificial pressure of the paper is

$$s_{corr,ij} = -k_s\left(\frac{W_{poly6}(|x_i - x_j|)}{W_{poly6}(\Delta q)}\right)^{n_s},$$

with $k_s = 0.1$, $n_s = 4$ and $|\Delta q|$ from $0.1h$ to $0.3h$ in the paper. These are tuning values.
It is a small push between close pairs, and it makes the flow less likely to clump at the free surface.
Line L8 is the velocity of position based dynamics.
Line L9 is XSPH viscosity, which pulls the velocity of each particle toward the mean of its neighbors.
The paper then adds [vorticity confinement](/vorticity-confinement/) to put back rotation lost to damping; the code here does not.

Line L4 gives two forms.
The paper uses $C_i = \rho_i/\rho_0 - 1$ for all particles.
The code also has the one-sided form $\max(0, C_i)$, which pushes only where the fluid is compressed, and the tests use it.
In the units of this page $\lambda$ has the unit m², so the code scales $\varepsilon$ and $k_s$ by the denominator $D_0 = \sum_k|\nabla_k C_i|^2$ of a particle in a full lattice: $\varepsilon = 0.01 D_0$ and $k_s = 0.1/D_0$. This scaling and $c = 0.01$ are tuning choices of this page.

## Example

Take $\Delta x = 0.02$ m, $h = 1.8\Delta x$, $\rho_0 = 1000$ kg/m² and $m = \rho_0\Delta x^2 = 0.4$ kg.
A particle in a full lattice of spacing $\Delta x$ then has the density 1000.53 kg/m² and $D_0 = 1102.68$ m⁻².
Put 25 particles at rest on a 5 by 5 lattice with spacing $0.95\Delta x$, and set $g = 0$, $\Delta t = 0.004$ s, $\varepsilon = 0.01D_0$ and no artificial pressure.
The table gives the mean of $\max(0, C_i)$ at line L4 of each pass, for the one-sided and the two-sided form.

| pass | one-sided mean | one-sided largest | two-sided mean |
|---|---|---|---|
| 1 | 4.313% | 11.98% | 4.313% |
| 2 | 0.520% | 3.251% | 8.319% |
| 3 | 0.173% | 1.084% | 3.531% |
| 4 | 0.058% | 0.365% | 8.304% |
| 5 | 0.020% | 0.124% | 3.731% |
| 6 | 0.007% | 0.042% | 6.778% |

The one-sided form lowers the error by about a factor of 3 in each pass.
In the two-sided form, the particles on the edge of the small block have a low density, so their constraints pull them inward, and the error goes up and down.
In a large body of water most particles are inside, and the paper uses the artificial pressure against this pull.

## Correctness

PBF is an inexact solver with a fixed number of passes, and it has no proof of convergence.
These things hold, and the [proof](proofs/correctness.md) gives the arguments:

- **The Newton step.** For one constraint alone and $\varepsilon = 0$, the move $\Delta x_k = \lambda_i\nabla_k C_i$ of line L5 makes the linear model of $C_i$ zero. It is the shortest such move.
- **Linear momentum.** Each pair term of lines L6 and L9 is opposite on $i$ and $j$. So without walls and gravity, the step keeps $\sum_i m v_i$ exactly, for any $k$, $\varepsilon$ and $s_{corr}$.
- **Angular momentum.** It is not kept exactly. The pair moves of line L6 are along $x^*_i - x^*_j$, and the angular momentum of line L8 is measured about the old positions $x_i$; the difference is of order $\Delta t$ times the moves.

The tests check the kernels, the value of $\lambda$, the drop of the error over the passes, the momentum law and a small dam break.

## Complexity

One pass costs $O(n + q)$ time for $q$ pairs: line L4 is one sweep over the pairs for the densities, line L5 one sweep for the gradients and line L6 one sweep for the moves.
A step costs $O(k(n + q))$, and the neighbor search adds $O(n + q)$.
With a density near $\rho_0$, $q = O(n)$.
The memory is $O(n + q)$.
In the small dam break of the tests, 4 passes per step at $\Delta t = 0.004$ s keep the measured mean compression below 0.2% (a measurement).

## Properties

- **Stable at large steps.** The passes move positions by bounded amounts, and the velocity is derived from them, so there is no stiff force. This is a heuristic; the paper shows it on its scenes.
- **Inexact.** A fixed number of passes leaves an error. Jacobi passes remove local errors fast and smooth errors slowly, so the error grows with the depth of the fluid (a heuristic).
- **Parallel.** Each pass is a Jacobi step, with no order between particles, so it runs well on a GPU.
- **Momentum.** Linear momentum is kept (proved); angular momentum is not kept exactly.
- **Damping.** Position based velocities and XSPH lose energy, which is why the paper adds vorticity confinement.

## Variants and improvements

- **Vorticity confinement.** The paper computes the vorticity $\omega_i = \sum_j (v_j - v_i)\times\nabla W_{ij}$ and adds a force along the gradient of $|\omega|$; see [vorticity confinement](/vorticity-confinement/).
- **One-sided constraints.** $\max(0, C_i)$, as in line L4, avoids the inward pull at a free surface.
- **Gauss-Seidel order.** Projecting the constraints one at a time converges faster per pass but is hard to run in parallel.
- **Unified solvers.** The same loop can hold cloth, rigid and granular constraints next to the fluid ones, in the [position based dynamics](/position-based-dynamics/) frame.
- **Pressure solvers.** [PCISPH](/pcisph/), [IISPH](/implicit-incompressible-sph/) and [DFSPH](/divergence-free-sph/) iterate on pressures until a tolerance, instead of a fixed number of passes on positions.

## When to use it

Use PBF for real time particle fluids, for example in games, where a fixed cost per step and stability matter more than an exact density.
For offline work with a tolerance on the density error, use [IISPH](/implicit-incompressible-sph/) or [DFSPH](/divergence-free-sph/).

## Pitfalls

- **No relaxation.** With $\varepsilon = 0$ in line L5, a particle with one neighbor gets a very large $\lambda$ and the step explodes.
- **Kernel support.** Poly6 and spiky here have support $h$, not $2h$ as the cubic spline. Line L2 must search with radius $h$.
- **Gradient of poly6.** Line L6 uses the spiky gradient. The poly6 gradient is 0 at $r = 0$ and gives almost no push between very close particles.
- **Velocity before the walls.** Line L7 clamps the positions, and line L8 then gives the velocity. Clamping only the velocity leaves particles in the walls.
- **Units of the tuning values.** $\varepsilon$ and $k_s$ of lines L5 and L6 have the unit of $\lambda$. Values from the paper change meaning when $m$, $\rho_0$ or $h$ change.

## Implementations

## History

Position based dynamics (Müller, Heidelberger, Hennix and Ratcliff 2007) moves positions to satisfy constraints and derives velocities from the moves.
Macklin and Müller (2013) added the SPH density as a constraint, with the poly6 and spiky kernels of Müller, Charypar and Gross (2003), XSPH viscosity of Monaghan (1989) and vorticity confinement.
The method ran fluids with large steps in real time on a GPU, and the same loop became part of unified particle solvers for games.

## References
