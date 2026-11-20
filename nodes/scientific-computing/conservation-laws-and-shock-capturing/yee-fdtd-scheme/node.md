---
tag: Z3QKRQ
kind: algorithm
slug: yee-fdtd-scheme
name: Yee FDTD scheme
aliases:
- finite-difference time-domain method
- FDTD
area: scientific-computing/conservation-laws-and-shock-capturing
level: core
summary: "Solves Maxwell's equations with E and H on staggered grids and leapfrog time steps. Second order, and the discrete divergence of the fields stays constant."
solves: [wave-equation]
model: real-ram
complexity:
  vars: {M: "the number of grid cells", N: "the number of time steps"}
  time: {worst: "Θ(N M)"}
  space: {extra: "Θ(M)"}
properties: {deterministic: true, explicit: true, order: "2 in space and time", divergence_preserving: true, dissipation: none, stability: "c Δt ≤ 1/sqrt(1/Δx² + 1/Δy² + 1/Δz²)"}
history:
  year: 1966
  people: [K. S. Yee, A. Taflove]
  note: Yee (1966) gave the staggered grid and the leapfrog scheme for Maxwell's equations. Taflove and coworkers developed it into a general tool for scattering and antenna problems from the 1970s on.
prereqs: [finite-difference-method, wave-equation, courant-friedrichs-lewy-condition]
see_also: [perfectly-matched-layer, von-neumann-stability-analysis, verlet-integration, symplectic-integrators, mac-grid, marker-and-cell-method, summation-by-parts-operators, discontinuous-galerkin-method]
sources:
  - paper: doi:10.1109/TAP.1966.1138693
    title: Kane S. Yee, Numerical solution of initial boundary value problems involving Maxwell's equations in isotropic media, IEEE Transactions on Antennas and Propagation 14(3) (1966) 302-307
    locator: the staggered positions of the E and H components, the difference equations, the stability condition
  - book: isbn:9781580538329
    title: Allen Taflove and Susan C. Hagness, Computational Electrodynamics, The Finite-Difference Time-Domain Method, 3rd edition, Artech House, 2005
    locator: Chapter 3 (the Yee algorithm), Chapter 4 (numerical dispersion and stability)
---

The Yee scheme, the basis of the finite-difference time-domain (FDTD) method, solves Maxwell's equations $\varepsilon E_t = \nabla\times H$, $\mu H_t = -\nabla\times E$ on a staggered grid. Each component of $E$ sits at the centre of a cell edge and each component of $H$ at the centre of a cell face, so every curl is a centred difference over one cell. $E$ is computed at whole time steps and $H$ at half steps, and the two updates leapfrog over each other. The scheme is explicit, second order in space and time, and has no numerical dissipation. It keeps the discrete divergences of $\varepsilon E$ (with no charges) and of $\mu H$ constant exactly. It is stable for $c\,\Delta t \le 1/\sqrt{1/\Delta x^2 + 1/\Delta y^2 + 1/\Delta z^2}$. Kane Yee published it in 1966. With absorbing boundaries such as the [perfectly matched layer](/perfectly-matched-layer/), it is the standard method for antennas, scattering, photonics and microwave circuits.

## In plain words

Electric and magnetic fields drive each other: a change in one makes a curl in the other. The Yee scheme puts the two fields on two grids, moved half a cell apart, so that each electric value sits in the middle of a loop of magnetic values, and the other way around. It also moves the two fields half a time step apart. Then each new electric value comes from the magnetic loop around it, and each new magnetic value comes from the electric loop around it. The steps go back and forth. Nothing needs to be solved, and the method uses only simple differences.

## The problem

Solve Maxwell's equations in a region with given $\varepsilon(x)$ and $\mu(x)$, initial fields and boundary conditions, for a time $T$. The reference code solves the two-dimensional transverse magnetic ($\text{TM}_z$) case, where only $E_z$, $H_x$ and $H_y$ are nonzero:

$$\varepsilon\,\partial_tE_z = \partial_xH_y - \partial_yH_x,\qquad \mu\,\partial_tH_x = -\partial_yE_z,\qquad \mu\,\partial_tH_y = \partial_xE_z,$$

in a rectangle with perfectly conducting walls ($E_z = 0$ on the boundary).

## The algorithm

$E_z$ sits at the nodes $(i\Delta x, j\Delta y)$, $H_x$ at $(i\Delta x, (j + \tfrac12)\Delta y)$, and $H_y$ at $((i + \tfrac12)\Delta x, j\Delta y)$. $E_z$ is known at $t_n = n\Delta t$ and $H$ at $t_{n-1/2}$. One step:

```pseudo id=main
YEE-STEP(E_z, H_x, H_y, Δx, Δy, Δt)
L1  for each (i, j+1/2) do H_x ← H_x - (Δt/μΔy)(E_z[i, j+1] - E_z[i, j])
L2  for each (i+1/2, j) do H_y ← H_y + (Δt/μΔx)(E_z[i+1, j] - E_z[i, j])
L3  for each interior node (i, j) do E_z ← E_z + (Δt/ε)((H_y[i+1/2, j] - H_y[i-1/2, j])/Δx - (H_x[i, j+1/2] - H_x[i, j-1/2])/Δy)
L4  on the conducting walls set E_z ← 0
```

In three dimensions there are six such updates, one for each component, and each uses the four values of the other field on the loop around it. The staggered positions make each difference centred in space, and the half-step offset makes each update centred in time.

## Example

**The magic time step by hand.** In one dimension with $c = 1$, $E$ at $i$ and $H$ at $i + \tfrac12$, the scheme is $H_{i+1/2} \leftarrow H_{i+1/2} + \lambda(E_{i+1} - E_i)$, then $E_i \leftarrow E_i + \lambda(H_{i+1/2} - H_{i-1/2})$, with $\lambda = c\Delta t/\Delta x$. Take $\lambda = 1$ and a wave moving right: $E^0_i = f_i$ and $H^{-1/2}_{i+1/2} = -f_{i+1}$. Then $H^{1/2}_{i+1/2} = -f_{i+1} + f_{i+1} - f_i = -f_i$ and $E^1_i = f_i + (-f_i + f_{i-1}) = f_{i-1}$. The pulse moves exactly one cell per step, with no error. For $\lambda < 1$ the scheme has numerical dispersion: a mode $e^{i(\kappa x - \omega t)}$ has $\sin(\omega\Delta t/2) = \lambda\sin(\kappa\Delta x/2)$, so short waves are slower than $c$.

**Cavity mode (measurement).** The $\text{TM}_{11}$ mode of the unit square, $E_z = \sin\pi x\sin\pi y\cos\omega t$ with $\omega = \pi\sqrt2 = 4.442883$, $\Delta t = \tfrac14\Delta x$ (0.354 of the CFL limit), $T = 0.5$. The scheme has the discrete mode with $\sin(\omega_h\Delta t/2) = \Delta t\sqrt{\sin^2(\pi\Delta x/2)/\Delta x^2 + \sin^2(\pi\Delta y/2)/\Delta y^2}$, which it reproduces to rounding.

| cells per side | largest error of $E_z$ | ratio | discrete $\omega_h$ |
|---|---|---|---|
| 8 | 9.987e-3 | | 4.417898 |
| 16 | 2.488e-3 | 4.01 | 4.436638 |
| 32 | 6.213e-4 | 4.00 | 4.441322 |
| 64 | 1.553e-4 | 4.00 | 4.442493 |

The error falls by 4 per halving of the grid, which is second order. The frequency error $\omega - \omega_h$ also falls by 4. With random initial fields on a $20\times20$ grid, the scheme stays bounded for 400 steps at the CFL limit and blows up at 1.02 times the limit.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows that every difference in L1 to L3 is centred in space and time, so the local truncation error is $O(\Delta t^2 + \Delta x^2 + \Delta y^2)$. It shows that the discrete divergence of $H$ at the cell centres does not change, because the discrete divergence of a discrete curl is zero. It gives a conserved discrete energy, which is positive definite and so bounds the fields when $c\Delta t \le 1/\sqrt{1/\Delta x^2 + 1/\Delta y^2}$. Above that limit, the mode with the shortest wavelength grows geometrically, and the same eigenvalue analysis gives the discrete dispersion relation.

## Complexity

Each step updates every field component once with a few additions and multiplications, so it costs $\Theta(M)$ for $M$ cells, and $N$ steps cost $\Theta(NM)$. Memory is the six field arrays (three in $\text{TM}_z$) and the material coefficients. Because $\Delta t$ is tied to the smallest cell by the CFL condition, a fine feature in one place forces small steps everywhere. The method parallelizes well: each update needs only nearest neighbours.

## Properties

- Second order in space and time on uniform grids; first order at staircased curved boundaries.
- No dissipation: the discrete energy $\sum \varepsilon E^n\cdot E^n + \mu H^{n-1/2}\cdot H^{n+1/2}$ is conserved exactly.
- The discrete divergence of $\mu H$, and of $\varepsilon E$ without sources, stays constant, so no spurious charges appear.
- Numerical dispersion depends on the direction and the wavelength. It is the main source of error, and about 10 to 20 cells per wavelength are needed in practice.
- Stable exactly for $c\Delta t \le 1/\sqrt{\sum_d 1/\Delta x_d^2}$. In one dimension $c\Delta t = \Delta x$ gives the exact shift.
- The leapfrog in time is the [Verlet](/verlet-integration/) method for the linear system, and it is [symplectic](/symplectic-integrators/).

## Variants and improvements

- **Absorbing boundaries.** The [perfectly matched layer](/perfectly-matched-layer/) of Berenger (1994) and its convolutional form (CPML) are the standard ways to model open space.
- **Dispersive materials.** Auxiliary differential equations or recursive convolutions add Debye, Drude and Lorentz media.
- **Subcell models.** Conformal methods change the coefficients in the cells cut by a curved conductor, which avoids the first-order staircase error.
- **Total-field and scattered-field formulation.** A plane wave is injected through a closed surface, so only the scattered field enters the absorbing layer.
- **Unconditionally stable versions.** ADI-FDTD and locally one-dimensional schemes remove the CFL limit at the cost of an implicit solve and larger dispersion errors.
- **Higher order.** Wider stencils such as the (2,4) scheme cut the dispersion error. Discontinuous Galerkin and finite element methods handle complex geometry with high order.
- **The same staggering elsewhere.** The [MAC grid](/mac-grid/) of incompressible flow puts velocities on faces and pressure at centres for the same reason.

## When to use it

Use it for broadband time-domain problems in electromagnetics and acoustics on simple, mostly structured geometry: antennas, waveguides, photonic crystals, radar cross sections, biological tissue, ground-penetrating radar. One run with a short pulse gives the response at all frequencies through a Fourier transform. For problems at a single frequency with large scale differences, frequency-domain finite element or integral equation methods are often more efficient. For curved geometry with high accuracy, use conformal FDTD or [discontinuous Galerkin](/discontinuous-galerkin-method/) methods.

## Pitfalls

- **Wrong positions of the components.** Putting $E$ and $H$ at the same points gives a non-centred scheme with spurious modes. Each component has its own position.
- **Time step above the limit.** A few percent above the CFL limit, the highest mode grows by a large factor per step and the run blows up.
- **Too few cells per wavelength.** Phase errors build up with distance. A wave crossing 100 wavelengths needs more resolution than one that crosses 5.
- **Initial fields at the wrong time.** $H$ must be given at $t = -\Delta t/2$, not at $t = 0$. Otherwise the error is first order.
- **Staircased conductors.** Curved metal surfaces on a Cartesian grid give first-order errors in resonance frequencies.
- **Simple absorbing conditions.** First-order boundary conditions reflect waves at grazing angles. Use a PML.

## Implementations

## History

Kane Yee (1966) proposed the staggered grid and the leapfrog scheme and stated its stability condition, with computations of a pulse scattered by a perfectly conducting obstacle. Taflove and coworkers developed the method from the 1970s on, with absorbing boundaries, the total-field and scattered-field formulation and applications to scattering, and the name finite-difference time-domain became standard. Berenger's perfectly matched layer (1994) removed the main remaining weakness, the reflection at the outer boundary.

## References
