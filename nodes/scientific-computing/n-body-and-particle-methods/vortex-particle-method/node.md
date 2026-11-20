---
tag: 4WPAHS
kind: algorithm
slug: vortex-particle-method
name: Vortex particle method
aliases:
- vortex blob method
area: scientific-computing/n-body-and-particle-methods
level: advanced
summary: Represents an incompressible flow by particles that carry vorticity and moves them with the velocity from the Biot-Savart law, often summed by a tree or FMM.
model: real-ram
complexity:
  vars: {N: the number of vortex particles}
  time: {worst: "Θ(N^2)"}
  space: {extra: "Θ(N)"}
properties: {deterministic: true, conservative: true, order: "2"}
history:
  year: 1973
  people: [Alexandre J. Chorin]
  note: Chorin replaced point vortices by vortex blobs with a smoothed core in 1973, and added viscosity with a random walk.
prereqs: [navier-stokes-equations, direct-n-body-summation]
see_also: [particle-strength-exchange, vorticity-streamfunction-formulation, fast-multipole-method, barnes-hut-algorithm, gravitational-softening, vorticity-confinement, stable-fluids, smoothed-particle-hydrodynamics]
sources:
  - book: isbn:9780521621861
    title: Georges-Henri Cottet and Petros D. Koumoutsakos, Vortex Methods, Theory and Practice, Cambridge University Press, 2000
    locator: the 2D vortex blob method, its convergence, viscous vortex methods and remeshing
  - paper: doi:10.1017/S0022112073002016
    title: Alexandre Joel Chorin, Numerical study of slightly viscous flow, Journal of Fluid Mechanics 57(4), 1973, 785-796
    locator: the vortex blobs and the random walk for the viscous term
  - paper: doi:10.1090/S0025-5718-1982-0658213-7
    title: J. Thomas Beale and Andrew Majda, Vortex methods. II. Higher order accuracy in two and three dimensions, Mathematics of Computation 39(159), 1982, 29-52
    locator: the convergence of the blob method and kernels of higher order
---

A vortex particle method simulates an incompressible flow with particles that carry vorticity, the local spin of the fluid, instead of a velocity grid. The velocity at any point is the sum of the swirls induced by all the particles (the Biot-Savart law), each swirl smoothed over a small core so that it stays finite, and the particles simply move with that velocity. There is no pressure solve, no grid, and no numerical diffusion from advection, and the particles go only where the flow has vorticity, so wakes, vortex rings and mixing layers are cheap to follow. In computer graphics, vortex particles are added to a grid fluid solver to keep small swirls in smoke and fire, close to what [vorticity confinement](/vorticity-confinement/) does; the method on this page is the full flow solver, with a smoothed kernel whose error goes to zero as the cores and the spacing shrink, and with viscosity added by [particle strength exchange](/particle-strength-exchange/).

## In plain words

Think of the flow as many small whirlpools. Each whirlpool is a particle that knows how strong it is and which way it turns. Every whirlpool pushes every other one around it, more strongly when they are close. To move the flow forward, add up the push from all the whirlpools at each particle, move each particle a little, and repeat. A whirlpool keeps its strength as it moves, as long as the fluid has no friction. To stop two whirlpools from flinging each other away when they come very close, each one is a soft blob with a small round core.

## The problem

In 2D, an incompressible inviscid flow with velocity $u$ has the scalar vorticity $\omega = \partial_x u_2 - \partial_y u_1$, and the Euler equations become the transport equation

$$\frac{\partial \omega}{\partial t} + u \cdot \nabla \omega = 0, \qquad u = K * \omega, \qquad K(x) = \frac{1}{2 \pi} \frac{(-x_2, x_1)}{|x|^2},$$

where the second equation is the Biot-Savart law for a flow in the whole plane that is at rest at infinity. So vorticity is carried by the flow: each fluid element keeps its vorticity.

The method writes the vorticity as a sum of $N$ blobs, $\omega_h(x) = \sum_p \Gamma_p \zeta_\delta(x - x_p)$, with the circulations $\Gamma_p = \omega_0(x_p^0)\, \ell^2$ from the initial vorticity on a lattice of spacing $\ell$, and the Gaussian core $\zeta_\delta(x) = e^{-|x|^2 / \delta^2} / (\pi \delta^2)$. The velocity of this field is the sum over the smoothed kernel

$$K_\delta(x) = \frac{(-x_2, x_1)}{2 \pi |x|^2} \bigl(1 - e^{-|x|^2 / \delta^2}\bigr), \qquad u(x) = \sum_q \Gamma_q K_\delta(x - x_q),$$

and the particles solve $\dot x_p = u(x_p)$ with fixed $\Gamma_p$. The code on this page uses direct summation and the explicit midpoint rule in time.

## The algorithm

```pseudo id=main
VORTEX-STEP(x, Γ, δ, h)
L1  for each particle p do
L2      u_p ← Σ_{q ≠ p} Γ_q K_δ(x_p - x_q)            ▷ Biot-Savart law with the blob kernel
L3  x_p* ← x_p + (h / 2) u_p for every p                ▷ half step
L4  u_p* ← Σ_{q ≠ p} Γ_q K_δ(x_p* - x_q*) for every p    ▷ velocity at the midpoint
L5  x_p ← x_p + h u_p* for every p
L6  return x;  the circulations Γ_p do not change
```

Lines L1 and L2 are an [N-body sum](/direct-n-body-summation/) like gravity, with the kernel turned by 90 degrees. The code visits each pair once and uses $K_\delta(-x) = -K_\delta(x)$ to add the two contributions. $K_\delta(0) = 0$, so a particle does not move itself. Lines L3 to L5 are the [explicit midpoint method](/explicit-midpoint-method/). For viscous flow, a diffusion step changes the $\Gamma_p$ after line L5, for example by [particle strength exchange](/particle-strength-exchange/).

## Example

**A pair of equal blobs.** Put $\Gamma = 2\pi$ at $(-0.5, 0)$ and at $(0.5, 0)$, with $\delta = 0.5$. Line L2 gives the right particle the velocity $\Gamma K_\delta(1, 0) = (0,\ 1 - e^{-4}) = (0, 0.98168)$ and the left one $(0, -0.98168)$. The pair turns counterclockwise about its centre at $\Omega = 2 \cdot 0.98168 / 1 = 1.9634$, a little slower than the $\Omega = \Gamma / (\pi d^2) = 2$ of two point vortices at distance $d = 1$. The code reproduces this rotation over 200 steps.

**The Lamb-Oseen vortex.** The vorticity $\omega = \Gamma / (4 \pi \nu t)\, e^{-r^2 / (4 \nu t)}$ has the azimuthal velocity $u_\theta = \Gamma / (2 \pi r)\, (1 - e^{-r^2 / (4 \nu t)})$, and every radial vorticity is a steady solution of the Euler equations. Take $\Gamma = 1$, $4 \nu t = 0.04$, a lattice with $\ell = 0.05$ cut to the disc $r \le 0.6$ (437 particles, total circulation 0.99984) and $\delta = 0.1$. A Gaussian blob of size $\delta$ convolved with a Gaussian vorticity of size $\sqrt{4 \nu t}$ is a Gaussian of size $\sqrt{4 \nu t + \delta^2}$, so the blob field should be the Lamb-Oseen vortex at the later time $t + \delta^2 / (4 \nu)$. The measured velocity at radii 0.05 to 0.5 matches that vortex within $3.3 \times 10^{-6}$; against the vortex at time $t$ the error is 0.065, and with $\delta = 0.05$ it is 0.018, close to the ratio 4 of a second order smoothing error (measurements; the largest speed is 0.51). In a run of 20 midpoint steps of $h = 0.05$ with $\ell = 0.1$ (109 particles) and $\delta = 0.15$, every particle stays on its circle within $10^{-4}$ and turns at the predicted rate.

## Correctness

The proofs of the facts below about the kernel, the Lamb-Oseen check and the invariants are in [the correctness proof](proofs/correctness.md).

**The method conserves the invariants of 2D Euler flow** (theorems for the particle equations $\dot x_p = u(x_p)$). Write $K_{pq} = K_\delta(x_p - x_q)$. Since $K_\delta(-x) = -K_\delta(x)$, the linear impulse $\sum_p \Gamma_p x_p$ has the derivative $\sum_{p, q} \Gamma_p \Gamma_q K_{pq} = 0$. Since also $x \cdot K_\delta(x) = 0$, the angular impulse $\sum_p \Gamma_p |x_p|^2$ has the derivative $2 \sum_{p, q} \Gamma_p \Gamma_q\, x_p \cdot K_{pq} = \sum_{p, q} \Gamma_p \Gamma_q (x_p - x_q) \cdot K_{pq} = 0$. The total circulation $\sum_p \Gamma_p$ is constant because no $\Gamma_p$ changes. The particle system is also Hamiltonian, with the interaction energy of the blobs as the Hamiltonian, and that energy is conserved. Each stage of the midpoint rule moves the points by a sum of the same antisymmetric terms, so the linear impulse stays exact to rounding; the angular impulse and the energy change by $O(h^3)$ per step.

**The velocity field is exact for the blob vorticity.** $K_\delta = K * \zeta_\delta$, so $u = \sum_q \Gamma_q K_\delta(\cdot - x_q)$ is the divergence free velocity whose curl is $\omega_h$ (a theorem; the tests check both by finite differences).

**Convergence.** The error of the method has two parts: the smoothing error, from replacing $\omega$ by $\omega * \zeta_\delta$, which is $O(\delta^2)$ for the Gaussian, and the quadrature error of the lattice sum, which is very small while the blobs overlap ($\ell < \delta$). Beale and Majda (1982) proved that for smooth flows over a finite time the blob method converges with the order of the kernel, if $\ell$ goes to zero faster than $\delta$; kernels of higher order give higher orders. Over long times the particles spread unevenly, the overlap is lost and the error grows, which is why practical codes remesh.

## Complexity

In the [real-RAM](/real-ram/) model, line L2 costs $\Theta(N^2)$ for $N$ particles, done twice per step, so one step costs $\Theta(N^2)$ time and $\Theta(N)$ extra space. A [Barnes-Hut tree](/barnes-hut-algorithm/) brings a step to $O(N \log N)$ and the [fast multipole method](/fast-multipole-method/) to $O(N)$ for a fixed accuracy; both are standard in vortex codes. The vortex-in-cell variant solves the Poisson equation for the stream function on a grid instead, at $O(N + M \log M)$ for $M$ grid nodes. The time step is limited by accuracy, not by a CFL condition on a grid: $h$ should be small against the turnover time $1 / \max |\omega|$.

## Properties

- **Lagrangian and grid free.** Advection is exact for the particles, so there is no numerical diffusion from the transport term.
- **Compact support of the work.** Particles are needed only where $\omega \ne 0$, which is a small part of the domain in many flows.
- **Divergence free by construction.** The velocity comes from the Biot-Savart law, so $\nabla \cdot u = 0$ exactly, with no projection step.
- **Boundary conditions at infinity are exact.** The kernel already has the flow at rest at infinity, so no artificial outer boundary is needed.
- **Conservation.** Circulation and linear impulse are exact, angular impulse and energy are conserved by the ODE.
- **Loss of overlap.** Strain stretches the particle distribution, and in time the blobs no longer overlap and the accuracy drops.

## Variants and improvements

- **Point vortices.** $\delta = 0$ gives the singular point vortex model of Helmholtz and Kirchhoff; it is a Hamiltonian system but it does not converge to smooth Euler flow without a core.
- **Kernels of higher order.** Beale and Majda built kernels with vanishing moments that give $O(\delta^m)$ smoothing errors.
- **Viscous diffusion.** Chorin's random walk, core spreading, [particle strength exchange](/particle-strength-exchange/), and the diffusion velocity method add the term $\nu \Delta \omega$.
- **Remeshing.** Interpolating the circulations back to a regular lattice every few steps restores the overlap; it is what makes long runs accurate.
- **3D vortex particles.** In 3D the particles carry a vector strength, and the stretching term $(\omega \cdot \nabla) u$ changes it; the vorticity can then lose its divergence free property, which needs a correction.
- **Vortex-in-cell.** A hybrid that puts the vorticity on a grid, solves for the stream function by FFT, and moves the particles with the grid velocity.
- **Boundaries.** Panels or a boundary element method enforce no flow through a wall, and the vorticity created at the wall is released as new particles.

## When to use it

Use a vortex particle method for flows dominated by compact vortical structures in large or unbounded domains: wakes of bluff bodies, rotor and wind turbine wakes, vortex rings, jets and mixing layers, and studies of vortex dynamics. Prefer a grid solver, such as the [vorticity-streamfunction formulation](/vorticity-streamfunction-formulation/) or a projection method, for confined flows with complex walls, for turbulence that fills the domain, and for compressible flow. In graphics, a few vortex particles on top of a grid solver are a cheap way to keep swirls; a full vortex method is worth it when the flow itself must be right.

## Pitfalls

- **Blobs that do not overlap.** With $\delta \le \ell$ for the particle spacing $\ell$, the lattice sum no longer approximates the convolution, and the velocity becomes noisy. Keep $\delta / \ell$ above 1, and remesh.
- **Point vortices for smooth flow.** Without a core, close pairs get huge velocities and the time step collapses.
- **Truncating the vortex.** Cutting the vorticity to a finite disc drops circulation; check $\sum_p \Gamma_p$ against the exact total.
- **Errors of the fast summation.** A tree or FMM with a loose accuracy parameter can spoil the conservation of the impulses, which direct summation keeps.
- **3D divergence.** In 3D, the particle vorticity field is not divergence free after stretching; ignoring this lets spurious vorticity grow.
- **Wrong sign convention.** The 2D kernel turns the separation by +90 degrees for counterclockwise vorticity; with the wrong sign the vortices spin backwards.

## Implementations

## History

Rosenhead (1931) followed the roll-up of a vortex sheet with point vortices by hand, and the instability of that computation stopped progress for decades. Chorin (1973) smoothed the core of each vortex into a blob and added viscosity with a random walk, which made the method a practical solver for slightly viscous flow. Hald (1979) and Beale and Majda (1982) proved convergence for the blob method. Fast summation with trees and the fast multipole method of Greengard and Rokhlin (1987), together with remeshing and particle strength exchange, made large and accurate simulations possible; Cottet and Koumoutsakos (2000) give the theory and the practice.

## References
