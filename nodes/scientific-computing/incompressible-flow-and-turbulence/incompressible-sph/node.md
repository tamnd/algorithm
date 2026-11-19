---
tag: H0ZQP6
kind: algorithm
slug: incompressible-sph
name: Incompressible smoothed particle hydrodynamics
aliases:
- ISPH
area: scientific-computing/incompressible-flow-and-turbulence
level: advanced
summary: Enforces incompressibility in SPH by a projection step that solves a pressure Poisson equation on the particles, instead of a stiff equation of state.
solves: [navier-stokes-equations]
model: real-ram
complexity:
  vars: {N: "the number of particles", K: "the number of time steps", I: "the conjugate gradient iterations per step"}
  time: {worst: "Θ(K N I)"}
  space: {extra: "Θ(N)"}
properties: {deterministic: true, meshless: true, lagrangian: true, conserves_momentum_exactly: true, divergence_free: "approximately", linear_solve_per_step: true}
history:
  year: 1999
  people: [Sharen J. Cummins, Murray Rudman, Songdong Shao, Edmond Y. M. Lo]
  note: "Cummins and Rudman (1999) brought the projection method of Chorin to SPH. Shao and Lo (2003) applied it to free-surface flows with a density-invariance source term. Xu, Stansby and Laurence (2009) added particle shifting to keep the particles regular."
prereqs: [smoothed-particle-hydrodynamics, sph-smoothing-kernel, chorin-projection-method]
see_also: [weakly-compressible-sph, implicit-incompressible-sph, divergence-free-sph, pcisph, helmholtz-hodge-decomposition, conjugate-gradient-method, poisson-equation, monaghan-artificial-viscosity]
sources:
  - paper: doi:10.1006/jcph.1999.6246
    title: "Sharen J. Cummins and Murray Rudman, An SPH projection method, Journal of Computational Physics 152 (1999) 584-607"
    locator: "the fractional step, the approximate projection and the pressure Poisson equation on particles"
  - paper: doi:10.1016/S0309-1708(03)00030-7
    title: "Songdong Shao and Edmond Y. M. Lo, Incompressible SPH method for simulating Newtonian and non-Newtonian flows with a free surface, Advances in Water Resources 26 (2003) 787-800"
    locator: "the prediction-correction steps, the density-invariance source term and the free-surface condition"
  - paper: doi:10.1006/jcph.1997.5776
    title: "Joseph P. Morris, Patrick J. Fox and Yi Zhu, Modeling low Reynolds number incompressible flows using SPH, Journal of Computational Physics 136 (1997) 214-226"
    locator: "the SPH viscous term with the first derivative of the kernel"
  - paper: doi:10.1016/j.jcp.2009.05.032
    title: "Rui Xu, Peter Stansby and Dominique Laurence, Accuracy and stability in incompressible SPH (ISPH) based on the projection method and a new approach, Journal of Computational Physics 228 (2009) 6703-6725"
    locator: "divergence-free and density-invariant source terms, Taylor-Green tests and particle shifting"
  - paper: doi:10.1088/0034-4885/68/8/R01
    title: "Joseph J. Monaghan, Smoothed particle hydrodynamics, Reports on Progress in Physics 68 (2005) 1703-1759"
---

Incompressible SPH (ISPH) is [smoothed particle hydrodynamics](/smoothed-particle-hydrodynamics/) in which the pressure comes from a linear system instead of an equation of state. Each step moves the particles with a provisional velocity, then solves a pressure Poisson equation on the particles and subtracts the pressure gradient, as in the [projection method](/chorin-projection-method/) on a grid. The graphics solvers [IISPH](/implicit-incompressible-sph/), [DFSPH](/divergence-free-sph/) and [PCISPH](/pcisph/) also find pressures that keep the density or the divergence in check, with a few Jacobi-like sweeps per frame, and [weakly compressible SPH](/weakly-compressible-sph/) avoids the solve with a stiff equation of state and small steps. What the accurate method adds is a symmetric pressure system solved to a set tolerance by a Krylov solver, measured convergence on test flows, and an explicit account of the errors that remain because the discrete Laplacian is not the product of the discrete divergence and gradient.

## In plain words

Water hardly compresses, so a particle simulation of water must keep the particles from bunching up or spreading out. One way is to treat water as slightly compressible and let any bunching make a large pressure, but then the time step must be tiny. ISPH does it the other way. It first moves the particles as if there were no pressure, then asks: what pressure field would push the velocities back to a flow with no compression? That question is a Poisson equation, one unknown pressure per particle, linked to its neighbors. Solving it is the expensive part of each step. The pressure gradient is then taken off the velocities, and the particles move on. The result is a flow that is nearly incompressible at time steps set by the flow speed, not by the speed of sound.

## The problem

Solve the incompressible [Navier-Stokes equations](/navier-stokes-equations/) $\partial_tv + v \cdot \nabla v = -\nabla p/\rho_0 + \nu\nabla^2v + g$, $\nabla \cdot v = 0$, in Lagrangian form: particles at positions $x_i$ with velocities $v_i$ follow $\dot x_i = v_i$. The density is the constant $\rho_0$ (here $\rho_0 = 1$), so each of the $N$ particles carries the same volume $V$ in a periodic box of area $NV$. The output is the particle positions and velocities at time $K\Delta t$. Here $\nu$ is the kinematic viscosity; the Courant number is written $\mathrm{Co} = |v|_{\max}\Delta t/h$.

## The algorithm

```pseudo id=main
ISPH(x, v, Δt, K; ν, g)
L1  repeat K times
L2      find the pairs (i, j) with |x_i - x_j| < 2h                 ▷ cell list
L3      v* ← v + Δt (ν ∇²_h v + g)                                  ▷ viscous predictor
L4      x* ← x + Δt v
L5      at x*: solve -L φ = mean(D v*) - D v* by conjugate gradients  ▷ pressure Poisson equation
L6      v' ← v* - G φ                                               ▷ projection, p = φ / Δt
L7      x ← x + Δt (v + v') / 2;  v ← v'
L8  return x, v
```

The kernel is the cubic [SPH smoothing kernel](/sph-smoothing-kernel/) $W(r, h)$ in 2D with support $2h$ and $h = 1.2\Delta x$, where $\Delta x$ is the initial particle spacing. For a pair, $x_{ij} = x_i - x_j$ (with the minimum image in a periodic box), $v_{ij} = v_i - v_j$, and $\eta^2 = 0.01h^2$. The discrete operators are

$$(D v)_i = -\sum_j V\,v_{ij} \cdot \nabla_iW_{ij}, \qquad (G\phi)_i = \sum_j V(\phi_i + \phi_j)\nabla_iW_{ij},$$

$$(L\phi)_i = \sum_j \frac{2V\,x_{ij} \cdot \nabla_iW_{ij}}{r_{ij}^2 + \eta^2}(\phi_i - \phi_j), \qquad (\nu\nabla_h^2v)_i = \sum_j \frac{2\nu V\,x_{ij} \cdot \nabla_iW_{ij}}{r_{ij}^2 + \eta^2}\,v_{ij}.$$

$D$ is the standard SPH divergence; $G$ is the symmetric SPH gradient, whose pair terms are equal and opposite. $L$ is the compact SPH Laplacian, which uses only the first derivative of the kernel and so links only neighbors within $2h$; the same form gives the viscous term of Morris, Fox and Zhu (1997). This is a first-order projection in the form of Cummins and Rudman (1999).

Line L3 adds viscosity and body forces at the old positions. Line L4 moves the particles to provisional positions, and line L5 finds the neighbor pairs again there and solves the pressure equation. The matrix $-L$ is symmetric and positive semidefinite, with the constants as its null space, so the right-hand side has its mean removed; the solution $\phi$ is taken with zero mean. Line L6 is the projection. Line L7 moves the particles with the mean of the old and new velocities.

## Example

**Uniform flow, by hand.** If every particle has the same velocity $U$, every $v_{ij}$ is zero. Then the viscous term is zero, $Dv^* = 0$, the solver returns $\phi = 0$ in zero iterations, and the flow stays uniform; all particles move by $\Delta t\,U$. With gravity in a periodic box, every velocity becomes $U + \Delta t\,g$ in the same way. The tests check both cases on a randomly perturbed lattice to $10^{-14}$.

**One matrix entry, by hand.** On a $12 \times 12$ lattice in the unit box, $\Delta x = \frac1{12}$, $h = 0.1$ and $V = \frac1{144}$. Take two nearest neighbors, $r = \Delta x$ and $q = r/h = \frac56$. The 2D cubic spline has $W'(r) = \frac{10}{7\pi h^3}(-3q + \frac94q^2) = 454.728 \cdot (-0.9375) = -426.307$. The off-diagonal entry of $-L$ for this pair is

$$-c_{ij} = \frac{2V\,rW'(r)}{r^2 + \eta^2} = \frac{2 \cdot \frac1{144} \cdot \frac1{12} \cdot (-426.307)}{\frac1{144} + 0.0001} = -70.04,$$

the value the implementation produces. The diagonal entry is the sum over all 20 neighbors, 404.26.

**The operators on a lattice.** Applied to $\cos 2\pi x$ and $\sin 2\pi x$ on an $n \times n$ lattice, the operators give the right shape, with an amplitude below the exact one:

| $n$ | 12 | 24 | 48 |
|---|---|---|---|
| $L$, amplitude / $4\pi^2$ | 0.919 | 0.965 | 0.977 |
| $G$ and $D$, amplitude / $2\pi$ | 0.900 | 0.967 | 0.985 |

The error falls as the particles are refined, but more slowly than $h^2$, because the lattice sums of the kernel do not match the integrals exactly at a fixed ratio $h/\Delta x$ (see the lattice table on the [kernel page](/sph-smoothing-kernel/)).

**Projecting out a gradient.** Take the Taylor-Green field $v_{TG} = (-\cos 2\pi x\sin 2\pi y,\ \sin 2\pi x\cos 2\pi y)$, which has zero divergence, and add the gradient of $\sin(2\pi x)\sin(2\pi y)/(2\pi)$. One projection (lines L5 and L6) should give back $v_{TG}$. The table gives the root mean square distance to $v_{TG}$ after the projection; before it, the distance is 0.707. The jitter is a random shift of each particle of up to the given fraction of $\Delta x$ in each direction.

| $n$ | 12 | 16 | 24 |
|---|---|---|---|
| lattice | 0.118 | 0.068 | 0.031 |
| jitter 0.1 | 0.128 | 0.117 | 0.135 |
| jitter 0.3 | 0.231 | 0.298 | 0.403 |

On a lattice the projection converges at about second order. On disordered particles it does not converge: the error of the SPH operators on a disordered set grows like the disorder divided by $h$. This is the main accuracy problem of ISPH, and the reason for particle shifting (see below).

**Taylor-Green decay.** In the unit periodic box with $\nu = 0.05$, the Taylor-Green vortex keeps its shape and its kinetic energy decays like $e^{-16\pi^2\nu t}$. Runs from a lattice with $\Delta t = 0.002$ ($\mathrm{Co} \approx 0.02$ to $0.06$) for 20 steps gave:

| $n$ | 12 | 16 | 24 | 32 |
|---|---|---|---|---|
| decay rate / exact | 0.936 | 0.959 | 0.976 | 0.983 |
| max velocity error | 0.0090 | 0.0061 | 0.0030 | 0.0025 |
| max $\lvert Dv^*\rvert$ before, after | 0.17, 0.087 | 0.18, 0.059 | 0.18, 0.043 | 0.18, 0.039 |
| CG iterations, last step | 8 | 15 | 24 | 31 |

The particle density $\sum_jVW_{ij}$ stayed within 0.3% of its lattice value. The total momentum stayed at zero to $10^{-17}$. The divergence is reduced by a factor of 2 to 5 by each projection, not removed.

## Correctness

The [proof file](proofs/correctness/) shows four exact properties of the update. The matrix $-L$ is symmetric and positive semidefinite, with the constants as its null space when the neighbor graph is connected, so the pressure system with the mean removed has a solution, and conjugate gradients from zero finds the zero-mean one. The pair terms of $G$ and of the viscous term are equal and opposite, so total momentum changes by exactly $NV\Delta t\,g$ per step. The viscous term only removes kinetic energy. A uniform flow stays uniform. The proof does not claim $Dv' = 0$, which is false for this approximate projection.

## Complexity

With a cell list, finding the pairs costs $\Theta(N)$ for a bounded number of neighbors per particle (about 20 in 2D at $h = 1.2\Delta x$). Building the matrix and each conjugate gradient iteration also cost $\Theta(N)$. So a step costs $\Theta(NI)$ and a run $\Theta(KNI)$, with $\Theta(N)$ memory. Without a preconditioner, $I$ grows like the square root of the condition number of the Laplacian, so like $n = \sqrt N$ in 2D (the table above: 8 to 31 iterations for $n = 12$ to 32). Production codes use preconditioned CG, BiCGSTAB, or [algebraic multigrid](/algebraic-multigrid/), which keep $I$ almost constant.

## Properties

- **Momentum is conserved exactly**, for any solver tolerance, because the pressure and viscous forces act in equal and opposite pairs.
- **Approximately incompressible.** The density stays within a fraction of a percent of its rest value in smooth flows, much less than the 1% of weakly compressible SPH, but the discrete divergence is not zero.
- **Time step set by the flow**, through a limit on $\mathrm{Co} = |v|\Delta t/h$, and by viscosity, not by a sound speed.
- **Smooth pressure.** The pressure comes from an elliptic solve, so it has much less noise than an equation of state applied to density errors.
- **Galilean invariant**: only velocity differences enter $D$, $L$ and the viscous term.

## Variants and improvements

- **Source term.** Cummins and Rudman (1999) use the divergence of $v^*$, as here. Shao and Lo (2003) use a source proportional to the density error, $(\rho_0 - \rho^*)/(\rho_0\Delta t^2)$, which keeps the density on target but gives noisy pressures. Xu, Stansby and Laurence (2009) compare the two on Taylor-Green and spin-down tests.
- **Particle shifting.** Xu, Stansby and Laurence (2009) move each particle slightly away from crowded neighbors after each step and correct its velocity by a Taylor expansion. This keeps the particles regular, so the disorder error of the table above does not grow. Lind and co-authors later based the shift on Fick's law of diffusion.
- **Free surfaces.** Particles whose density or neighbor count is below a threshold are marked as surface particles and get $p = 0$ as a Dirichlet condition, which also removes the null space.
- **Exact projection.** Using $DG$ itself as the Laplacian makes $Dv' = 0$ exact, with a stencil that reaches $4h$. In a test run with the operators above, one such step on the moved particles of the $12 \times 12$ Taylor-Green case cut the kinetic energy from 0.25 to $5 \cdot 10^{-6}$, so the exact discrete projection is not a cure. Practical codes use the compact Laplacian.
- **Graphics solvers.** [IISPH](/implicit-incompressible-sph/) solves a pressure equation with the density error as source by relaxed Jacobi; [DFSPH](/divergence-free-sph/) runs a divergence solve and a density solve each step; [PCISPH](/pcisph/) corrects pressures by a fixed factor in a predict-correct loop. They stop after a few iterations or a density error of 0.1% to 1%, which is what animation needs.
- **Semi-implicit particle methods** of the same family solve a similar Poisson equation with a different weight function.

## When to use it

Use ISPH for liquids where the pressure matters: wave loads on structures, sloshing tanks, dam breaks, flows at low Reynolds number. There the noise of a weakly compressible pressure is a problem and the time step of a stiff equation of state is too small. Use weakly compressible SPH when the code must be explicit and simple to run in parallel, or when the flow has violent splashing and fragmentation where the pressure solve is hard to set up. For graphics, the faster IISPH and DFSPH are the usual choice. For flows in a fixed domain without free surfaces, a grid projection method is usually more accurate for the same work.

## Pitfalls

- **Particle disorder.** The table shows that on disordered particles the projection error does not go down with refinement. Without shifting or another regularization, a long run becomes noisy and the particles form clumps and voids.
- **An inconsistent right-hand side.** In a periodic box, or with only Neumann conditions, $\sum_i(Dv^*)_i = -2V\sum_iv^*_i \cdot \sum_j\nabla_iW_{ij}$, which is zero on a lattice but not on disordered particles. Without removing the mean, the pressure system has no solution and the solver stalls.
- **Expecting zero divergence.** The compact Laplacian is not $DG$, so $Dv'$ is reduced but not zero. Test with the density error and with flows that have exact solutions, not with $Dv'$ alone.
- **The sign of $L$.** $L$ is negative semidefinite. Conjugate gradients needs the positive matrix $-L$, so the right-hand side changes sign too, as on line L5.
- **Solving at the wrong positions.** The pressure equation of line L5 must use the neighbor pairs at $x^*$, not at $x$, or the correction is applied to a different particle arrangement than the one it was computed for.
- **Mixing the time scale into the pressure.** With $\phi = p\,\Delta t/\rho_0$, a change of $\Delta t$ changes $\phi$; plot $p = \phi/\Delta t$.
- **Kernel truncation at free surfaces.** Near a free surface the kernel support is only partly filled, so $D$ and $L$ are wrong there. Surface detection and the Dirichlet condition must be done with care.

## Implementations

## History

Cummins and Rudman (1999) wrote SPH as a projection method: integrate the velocity without the pressure, then project it onto a divergence-free field by a pressure Poisson equation, in the spirit of the [Helmholtz-Hodge decomposition](/helmholtz-hodge-decomposition/). Shao and Lo (2003) applied the idea to dam breaks and mudflows with free surfaces, using a source term from the density error. Xu, Stansby and Laurence (2009) analyzed the accuracy of the variants and introduced particle shifting, which made long ISPH runs stable and accurate. In computer graphics, PCISPH (2009), IISPH (2014) and DFSPH (2015) brought pressure solves on particles to animation, with simpler solvers and looser tolerances.

## References
