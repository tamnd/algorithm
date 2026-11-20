---
tag: ZFSET4
kind: algorithm
slug: plasma-particle-in-cell
name: Particle-in-cell plasma simulation
aliases:
- electrostatic particle-in-cell
- electromagnetic particle-in-cell
area: scientific-computing/n-body-and-particle-methods
level: core
summary: Moves charged macroparticles in fields computed on a grid from their deposited charge and current; the main method of kinetic plasma simulation.
model: real-ram
complexity:
  vars: {N: the number of particles, M: the number of grid points, T: the number of time steps}
  time: {worst: "Θ(T (N + M))"}
  space: {extra: "Θ(M)"}
properties: {deterministic: true, conservative: true, order: "2"}
history:
  year: 1962
  people: [John M. Dawson, Charles K. Birdsall, A. Bruce Langdon]
  note: Dawson's charge sheet model of 1962 showed that a modest number of simulated charges reproduces Debye shielding and Landau damping; grids with cloud-in-cell weighting followed in the late 1960s, and Birdsall and Langdon wrote the standard text.
prereqs: [particle-mesh-method, vlasov-poisson-system, boris-pusher]
see_also: [cloud-in-cell-assignment, yee-fdtd-scheme, particle-in-cell, fluid-implicit-particle, affine-particle-in-cell, courant-friedrichs-lewy-condition, monte-carlo-integration]
sources:
  - book: isbn:9780750310253
    title: Charles K. Birdsall and A. Bruce Langdon, Plasma Physics via Computer Simulation, Taylor and Francis, 2004 (reprint of the IOP edition of 1991)
    locator: Part 1 (the electrostatic program ES1 and the electromagnetic program EM1) and Part 2 (the effects of the spatial grid and of the finite time step)
  - book: isbn:9780852743928
    title: Roger W. Hockney and James W. Eastwood, Computer Simulation Using Particles, Adam Hilger, 1988
    locator: Chapter 9 (plasma simulation)
  - paper: doi:10.1063/1.1706638
    title: John Dawson, One-dimensional plasma model, The Physics of Fluids 5(4), 1962, 445-459
    locator: the charge sheet model and its measurements of Debye shielding and Landau damping
---

Particle-in-cell (PIC) plasma simulation solves the kinetic equations of a collisionless plasma by following a large number of charged macroparticles, each of which stands for many real electrons or ions, in fields that are computed on a grid. In each time step the code deposits the charge (and in electromagnetic codes the current) of the particles on the grid, solves the field equations on the grid, interpolates the fields back to the particles, and moves the particles with the [Boris pusher](/boris-pusher/) or the leapfrog. The particles sample the phase space density of the [Vlasov-Poisson system](/vlasov-poisson-system/) (or Vlasov-Maxwell system), so PIC captures kinetic effects such as Landau damping, beam instabilities and particle acceleration that fluid models miss. The graphics pages [particle-in-cell](/particle-in-cell/), [fluid-implicit-particle](/fluid-implicit-particle/) and [affine-particle-in-cell](/affine-particle-in-cell/) share the name and the particle to grid transfers, but they carry fluid velocity on the particles and project it to be divergence free; the plasma method carries charge and solves for electric and magnetic fields.

## In plain words

A plasma is a hot gas of charged particles, far too many to follow one by one. A PIC code follows a smaller number of heavy, highly charged stand-ins instead. Each stand-in moves like the real particles it represents.

The stand-ins never push each other directly. Instead each one leaves its charge on the nearby points of a fixed grid. The code then works out the electric field on the grid from all the charge at once, which is fast. Each stand-in reads the field at its own place from the same grid points and moves a short time forward. Then the cycle repeats. Because the grid smooths the field over a cell, close collisions between stand-ins are weak, which is what a hot, thin plasma needs.

## The problem

In the electrostatic case, the input is a periodic domain of length $L$ with $M$ grid points, and $N$ particles with positions $x_p$, velocities $v_p$, charge $q_p$ and mass $m_p$. The unknown is the phase space density $f(x, v, t)$ of the electrons, which obeys the Vlasov-Poisson system

$$\partial_t f + v \, \partial_x f + \frac{q}{m} E \, \partial_v f = 0, \qquad \partial_x E = \rho = 1 - \int f \, dv,$$

in normalized units: $\epsilon_0 = 1$, the electrons have $q/m = -1$, the ions are a fixed background of density 1, times are in units of $1/\omega_p$ and lengths in units of $v_{th} / \omega_p$, so the Debye length $\lambda_D = v_{th} / \omega_p$ is the thermal speed. The particles are a sample of $f$: each carries $q_p = -L / N$ and $m_p = L / N$, so that their mean density is 1. The output is the particle state and the grid field at each step, and from them the measured quantities, such as the field energy $W = \tfrac{1}{2} \sum_j E_j^2 \Delta x$.

## The algorithm

```pseudo id=main
ES-PIC(x[1..N], v[1..N], M, L, h, T)                ▷ v given at t = 0
L1  ρ ← CIC-DEPOSIT(x, q_p) + 1                     ▷ electrons plus ion background
L2  E ← GAUSS(ρ)                                    ▷ E_{j+1/2} - E_{j-1/2} = Δx ρ_j, mean zero
L3  E_p ← CIC-INTERPOLATE(E, x_p) for every p
L4  v_p ← v_p - (h / 2)(q/m) E_p for every p        ▷ start the leapfrog at t = -h/2
L5  for n ← 1 to T do
L6      v_p ← v_p + h (q/m) E_p for every p
L7      x_p ← (x_p + h v_p) mod L for every p
L8      ρ ← CIC-DEPOSIT(x, q_p) + 1
L9      E ← GAUSS(ρ)
L10     E_p ← CIC-INTERPOLATE(E, x_p) for every p
L11     record W_n = ½ Σ_j E_j² Δx
L12 return x, v, W
```

Lines L1 and L8 use [cloud-in-cell assignment](/cloud-in-cell-assignment/). Lines L2 and L9 solve Gauss's law with a running sum on the half points, remove the mean, and average to the grid points; this equals minus the centred difference of the potential of the 3-point Poisson equation, so the field kernel is odd. Lines L6 and L7 are the leapfrog; with a magnetic field, line L6 becomes the Boris step. In an electromagnetic code, line L8 also deposits the current, and lines L9 and L10 advance $\mathbf{E}$ and $\mathbf{B}$ with the [Yee scheme](/yee-fdtd-scheme/) instead of solving Gauss's law.

## Example

Take $M = 4$, $L = 4$ ($\Delta x = 1$) and $N = 4$ electrons, so $q_p = -1$. At $x = 0.5, 1.5, 2.5, 3.5$ each grid point gets $-1$ from the electrons and $+1$ from the ions, so $\rho = 0$ and $E = 0$.

Now move the first electron to $x = 0$. Line L1 gives $\rho = (-0.5, 0.5, 0, 0)$: point 0 has an extra half electron and point 1 a missing half. Line L2 gives $E = (-0.125, -0.125, 0.125, 0.125)$, and line L3 gives the fields $-0.125, 0, 0.125, 0$ at the four electrons. The forces $q_p E_p$ are $0.125, 0, -0.125, 0$: the electrons at 0 and 2.5 move toward point 1, where positive charge is in excess, and the forces sum to 0. With $h = 0.5$, line L4 gives $v_1 = -0.03125$, line L6 gives $v_1 = 0.03125$, and line L7 moves the first electron to $x = 0.015625$.

A measurement with this code (with lines L1 to L12 and the mode amplitude of $E$ recorded): with $k = 0.5$, $L = 4\pi$, $M = 32$, $h = 0.1$, $N = 100\,000$ electrons, a density perturbation of 1 percent and a quiet start (velocities from the inverse normal distribution at bit-reversed quantiles), the amplitude of the mode $k = 0.5$ of $E$ decays at the rate 0.147, fitted over its peaks for $t$ from 2.5 to 18, and oscillates at about 1.42. Linear theory gives $\gamma = -0.1534$ and $\omega = 1.4157$ (see the [Vlasov-Poisson system](/vlasov-poisson-system/)).

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). It shows these facts (theorems on the scheme, in exact arithmetic):

- The grid charge is neutral: $\sum_j \rho_j \Delta x = 0$ at every step, because each electron deposits exactly $q_p$ and $N q_p = -L$.
- Lines L2 and L9 return $E_j = -(\phi_{j+1} - \phi_{j-1}) / (2\Delta x)$ for the mean-free solution of $-(\phi_{j+1} - 2\phi_j + \phi_{j-1}) / \Delta x^2 = \rho_j - \bar\rho$.
- The total momentum $\sum_p m_p v_p$ does not change in any step, including the start in line L4, because the forces sum to zero (the argument of the cloud-in-cell page).

What PIC computes is a statistical estimate of the solution of the Vlasov equation, not the solution itself. As $N$ grows with the grid and the step fixed, the particle density converges to the solution of the semi-discrete Vlasov equation, with a statistical error of order $N_c^{-1/2}$ for $N_c$ particles per cell (a heuristic from the central limit theorem, as in [Monte Carlo integration](/monte-carlo-integration/)). The grid and the leapfrog add errors of order $\Delta x^2$ and $h^2$.

## Complexity

In the [real-RAM](/real-ram/) model, lines L1 and L8 cost $\Theta(N + M)$, lines L2 and L9 cost $\Theta(M)$, lines L3, L6, L7 and L10 cost $\Theta(N)$, and line L11 costs $\Theta(M)$. So $T$ steps cost $\Theta(T (N + M))$ time with $\Theta(M)$ extra space beyond the particle arrays. In 2D and 3D with an FFT field solve the cost is $\Theta(T (N + M \log M))$, and the particle part dominates in practice because $N$ is tens to hundreds of times $M$.

## Properties

- **Momentum conserving.** With the same weights in deposit and interpolation and an odd field kernel, the total momentum is exact (Birdsall and Langdon, Part 2).
- **Energy approximately conserved.** The total energy is not an exact invariant of the momentum-conserving scheme. It drifts slowly, and much faster when $\Delta x$ is large compared with $\lambda_D$, which is the finite grid instability or grid heating. Keep $\Delta x \lesssim \lambda_D$ (a rule of thumb, Birdsall and Langdon, Part 2).
- **Noisy.** The field has statistical noise of relative size about $N_c^{-1/2}$. Quiet starts reduce the initial noise, but the noise returns as particle orbits mix.
- **Time step limit.** The leapfrog on a plasma oscillation is stable only for $\omega_p h < 2$; for accuracy, $\omega_p h \approx 0.1$ to 0.2 is usual.
- **Collisionless by design.** The grid smooths the force below a cell, so close collisions are much weaker than in a real plasma with the same number of particles per Debye sphere; collisions are added by a separate Monte Carlo step when needed.
- **Deterministic.** With a fixed initial loading, the run has no random choices.

## Variants and improvements

- **Electromagnetic PIC.** The fields $\mathbf{E}$ and $\mathbf{B}$ are advanced on a staggered Yee grid, the particles with the Boris pusher. The current is deposited with charge-conserving weights, so that Gauss's law stays true without a separate correction.
- **Implicit and energy-conserving PIC.** Implicit time steps allow $\omega_p h \gg 1$, and some implicit schemes conserve the total energy exactly at the cost of a nonlinear solve per step.
- **delta-f PIC.** The particles carry only the deviation of $f$ from a known equilibrium, which cuts the noise when the deviation is small.
- **Higher order shapes.** TSC and higher B-splines reduce aliasing and grid heating.
- **Monte Carlo collisions.** Binary collision models between particles in the same cell add Coulomb collisions or collisions with a neutral gas.
- **Gyrokinetic PIC.** For strongly magnetized plasmas, the particles follow gyrocentres, which removes the fast gyration from the time step.

## When to use it

Use PIC when the physics is kinetic: when the velocity distribution is far from a Maxwellian, when wave-particle resonances matter (Landau damping, beam-plasma instabilities), or when particles are accelerated, as in laser-plasma interaction, magnetic reconnection and plasma sheaths. For a smooth $f$ in low dimension, a grid in phase space (a semi-Lagrangian Vlasov solver) has no statistical noise and is often more accurate per unit of cost. For large-scale behaviour close to equilibrium, a fluid model such as magnetohydrodynamics is far cheaper.

## Pitfalls

- **Grid heating.** With $\Delta x$ several times $\lambda_D$, a thermal plasma heats up on its own. Resolve the Debye length, or use an energy-conserving or a higher order scheme.
- **Too few particles per cell.** With a few particles per cell, the noise hides small signals such as a 1 percent wave; a damping rate fitted to noise is meaningless.
- **Recurrence and beam instabilities from quiet starts.** A start that loads particles in a few cold beams is quiet at first but can become unstable later, so check the result against a second loading.
- **Wrong start of the leapfrog.** Without the half step back in line L4, the method is only first order and the phase of oscillations is wrong.
- **Mixing up the half steps for diagnostics.** The kinetic energy must be computed from the mean of the velocities at $n - 1/2$ and $n + 1/2$, not from one of them.
- **Not neutral.** A periodic Poisson problem needs zero net charge; forgetting the ion background makes the mean mode undefined.

## Implementations

## History

Dawson (1962) followed a large number of charged sheets in one dimension and measured Debye shielding and the Landau damping of the Fourier modes, which showed that a simulation with far fewer particles than a real plasma can reproduce its collective behaviour. Grid-based methods with charge assignment came next, and Birdsall and Fuss (1969) introduced the clouds-in-cells weighting that is now standard. Birdsall and Langdon (1985, reprinted 1991) wrote the standard text, with the programs ES1 and EM1, and Hockney and Eastwood (1981, second edition 1988) treated plasma simulation together with the other particle-mesh methods.

## References
