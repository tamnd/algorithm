---
tag: Y8XKSA
kind: algorithm
slug: particle-mesh-method
name: Particle-mesh method
aliases:
- PM method
area: scientific-computing/n-body-and-particle-methods
level: core
summary: Assigns particle mass or charge to a grid, solves Poisson's equation on the grid by FFT and interpolates the forces back, in O(N + M log M) per step for M grid points.
model: real-ram
complexity:
  vars: {N: the number of particles, M: the number of grid points}
  time: {worst: "Θ(N + M log M)"}
  space: {extra: "Θ(M)"}
properties: {deterministic: true, conservative: true, order: "2"}
history:
  year: 1981
  people: [Roger W. Hockney, James W. Eastwood]
  note: Particle-mesh codes were in use for plasma and galaxy simulation in the 1960s; the book of Hockney and Eastwood (first edition 1981) gave the standard account of the method and its errors.
prereqs: [cloud-in-cell-assignment, poisson-equation, fast-fourier-transform]
see_also: [p3m-method, treepm-method, plasma-particle-in-cell, direct-n-body-summation, barnes-hut-algorithm, gravitational-softening, particle-mesh-ewald, gravitational-n-body-problem]
sources:
  - book: isbn:9780852743928
    title: Roger W. Hockney and James W. Eastwood, Computer Simulation Using Particles, Adam Hilger, 1988
    locator: Chapter 5 (the particle-mesh force calculation) and Chapter 6 (the solution of the field equations)
  - book: isbn:9780750310253
    title: Charles K. Birdsall and A. Bruce Langdon, Plasma Physics via Computer Simulation, Taylor and Francis, 2004 (reprint of the IOP edition of 1991)
    locator: Part 2, the chapters on the effects of the spatial grid and on energy-conserving models
  - paper: doi:10.1086/191003
    title: George Efstathiou, Marc Davis, Simon D. M. White and Carlos S. Frenk, Numerical techniques for large cosmological N-body simulations, The Astrophysical Journal Supplement Series 57, 1985, 241-260
    locator: the tests of the force accuracy of particle-mesh schemes in a periodic cube
---

The particle-mesh (PM) method computes the gravitational or electrostatic forces among $N$ particles in a periodic box with a grid of $M$ points. It assigns the particle masses or charges to the grid, solves Poisson's equation on the grid with the [fast Fourier transform](/fast-fourier-transform/), takes the gradient of the potential on the grid, and interpolates the field back to the particles. One force evaluation costs $\Theta(N + M \log M)$, against $\Theta(N^2)$ for [direct summation](/direct-n-body-summation/). The price is resolution: the grid cannot resolve forces at separations of a few cells or less, so PM suits systems where the long-range collective field matters most, such as collisionless plasmas and the large-scale structure of the universe.

## In plain words

Adding up the pull of every particle on every other particle is slow when there are millions of particles. The particle-mesh method avoids this. It first lays a regular grid over the box and lets each particle share its mass with the nearby grid points, so the grid holds a smooth picture of where the mass is.

On a regular grid, the equation that turns mass into a pull can be solved very fast with a standard tool for waves. The method then has the pull at every grid point. Each particle reads the pull at its own place from the same nearby points, and moves. The cost grows only a little faster than the number of grid points plus the number of particles. The pull between two particles that are very close is too weak, because the grid blurs it.

## The problem

The input is a periodic box $[0, L_x) \times [0, L_y)$ with an $n_x \times n_y$ grid, $M = n_x n_y$, spacings $\Delta x = L_x / n_x$ and $\Delta y = L_y / n_y$, and $N$ particles with positions $\mathbf{x}_i$, inertial masses $m_i$ and source weights $w_i$. The field is the solution of

$$\nabla^2 \phi = s \, (\rho - \bar\rho), \qquad \mathbf{g} = -\nabla \phi, \qquad \mathbf{F}_i = w_i \, \mathbf{g}(\mathbf{x}_i),$$

where $\rho$ is the density of the weights and $\bar\rho$ its mean. For gravity in units with $G = 1$, $s = 4\pi$ and $w_i = m_i$. For a plasma in normalized units with $\epsilon_0 = 1$, $s = -1$, $w_i = q_i$ and $\mathbf{g}$ is the electric field $\mathbf{E}$. The mean is removed because a periodic Poisson problem has a solution only for a source of zero mean; for a plasma it is the uniform neutralizing background, and in cosmology it is the background density of the expanding universe. With $n_y = 1$ the method is the 1D method. The output is the force on each particle and, with a time integrator, the trajectories.

## The algorithm

The grid step uses the 5-point Laplacian and the centred difference. Its eigenvalue for the Fourier mode $(k_x, k_y)$ is

$$\lambda(k_x, k_y) = -\frac{4}{\Delta x^2} \sin^2 \frac{\pi k_x}{n_x} - \frac{4}{\Delta y^2} \sin^2 \frac{\pi k_y}{n_y},$$

which is zero only for the mode $(0, 0)$.

```pseudo id=main
PM-FORCES(x[1..N], w[1..N], grid, s)
L1  ρ ← CIC-DEPOSIT(x, w)                          ▷ density on the n_x × n_y grid
L2  ρ̂ ← FFT2(ρ)
L3  φ̂(k) ← s ρ̂(k) / λ(k) for k ≠ (0, 0);  φ̂(0, 0) ← 0
L4  φ ← inverse FFT2(φ̂)
L5  g_x[i, j] ← -(φ[i+1, j] - φ[i-1, j]) / (2 Δx);  g_y[i, j] ← -(φ[i, j+1] - φ[i, j-1]) / (2 Δy)
L6  g(x_p) ← CIC-INTERPOLATE(g, x_p) for p = 1, ..., N
L7  return F_p = w_p g(x_p) for p = 1, ..., N

PM-RUN(x, v, m, w, grid, s, h, T)
L8  F ← PM-FORCES(x, w, grid, s)
L9  for n ← 1 to T do
L10     v_p ← v_p + (h / 2) F_p / m_p for every p
L11     x_p ← (x_p + h v_p) mod (L_x, L_y) for every p
L12     F ← PM-FORCES(x, w, grid, s)
L13     v_p ← v_p + (h / 2) F_p / m_p for every p
L14 return x, v
```

Line L1 is [cloud-in-cell assignment](/cloud-in-cell-assignment/), which gives each particle bilinear weights on the 4 grid points around it. Lines L2 to L4 solve the discrete Poisson equation exactly: the Fourier modes are the eigenvectors of the periodic 5-point Laplacian, so dividing each coefficient by its eigenvalue inverts it on the mean-free part. Line L5 differences the potential, and line L6 reads the field at the particles with the same CIC weights as line L1. Lines L8 to L14 are the kick-drift-kick form of the leapfrog ([Verlet](/verlet-integration/)) integrator with step $h$.

## Example

Take a 1D grid with $M = 8$, $L = 8$ (so $\Delta x = 1$), $s = 1$ and two unit masses on the grid points $x = 2$ and $x = 5$. Line L1 gives $\rho = (0, 0, 1, 0, 0, 1, 0, 0)$ with mean $\bar\rho = 0.25$. Lines L2 to L4 give

$$\phi = (0.375, \; 0.125, \; -0.375, \; -0.125, \; -0.125, \; -0.375, \; 0.125, \; 0.375).$$

At point 2, $(\phi_1 - 2\phi_2 + \phi_3) / \Delta x^2 = 0.125 + 0.75 - 0.125 = 0.75 = \rho_2 - \bar\rho$, as the equation requires. Line L5 gives

$$g = (0.125, \; 0.375, \; 0.125, \; -0.125, \; 0.125, \; -0.125, \; -0.375, \; -0.125).$$

Both particles sit on grid points, so line L6 reads $g_2 = 0.125$ and $g_5 = -0.125$. The particles attract each other along the short way round the ring (distance 3, not 5), and the two forces cancel. The continuum answer for two masses on a periodic line at distance $d$ is $s \, m_1 m_2 (1/2 - d / L) = 1/2 - 3/8 = 0.125$, so the grid force is exact here. This holds for any two particles on grid points at least 2 cells apart in both directions round the ring, because the discrete potential of one particle is the continuum quadratic at the grid points, and the centred difference of a quadratic is exact.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). It shows three facts (all theorems).

- Lines L2 to L4 return the unique mean-free grid function $\phi$ whose 5-point Laplacian is $s (\rho - \bar\rho)$, because the Fourier modes diagonalize the periodic 5-point Laplacian and only the mode $(0, 0)$ has eigenvalue 0.
- The forces of line L7 sum to zero exactly in exact arithmetic, and a lone particle feels no force. The map from $\rho$ to $g$ is a convolution with an odd kernel (an even Green's function followed by an odd difference), and lines L1 and L6 use the same weights, so the argument of the cloud-in-cell page applies.
- Lines L10 to L13 then change the total momentum $\sum_p m_p \mathbf{v}_p$ by $h \sum_p \mathbf{F}_p = 0$ in each step, and the integrator is time reversible: running $T$ steps, reversing all velocities and running $T$ steps again returns the start.

Convergence is a separate claim. For a smooth density, the 5-point Laplacian and the centred difference are both second order in the grid spacing, so the grid field has an error of $O(\Delta x^2 + \Delta y^2)$ (a theorem on the truncation error). The tests measure an error ratio between 3.8 and 4.2 when $M$ doubles in 1D.

## Complexity

In the [real-RAM](/real-ram/) model with $M = n_x n_y$ and $n_x$, $n_y$ powers of 2: line L1 costs $\Theta(N + M)$, lines L2 and L4 cost $\Theta(M \log M)$ each (row transforms then column transforms), lines L3 and L5 cost $\Theta(M)$, and lines L6 and L7 cost $\Theta(N)$. So one force evaluation costs $\Theta(N + M \log M)$ time and $\Theta(M)$ extra space, and $T$ steps of PM-RUN cost $\Theta(T (N + M \log M))$. The same holds in 3D with 8 grid points per particle. For comparison, direct summation costs $\Theta(N^2)$ per step, and a [Barnes-Hut tree](/barnes-hut-algorithm/) $O(N \log N)$ for a fixed opening angle.

## Properties

- **Momentum is conserved exactly.** This needs the same assignment function in lines L1 and L6 and an odd difference operator in line L5 (Hockney and Eastwood, chapter 5).
- **Energy is not conserved exactly.** The force of this scheme is not the exact gradient of an energy of the particle positions, so the total energy drifts slowly. In plasma runs with a Debye length well below a cell, the drift shows as grid heating. Birdsall and Langdon describe energy-conserving variants that give up exact momentum conservation.
- **Softened at the grid scale.** The force between two particles is close to the true force at separations of several cells, and much weaker at separations of one cell or less (a heuristic; the size of the error depends on the assignment function and the Green's function). The mesh acts as a [softening](/gravitational-softening/) of about one cell.
- **Not translation invariant.** The force between two particles at a fixed separation changes a little as the pair moves relative to the grid.
- **Periodic.** The FFT solve gives the field of the periodic box. Isolated systems need a doubled grid with a truncated Green's function.
- **Deterministic.** The method has no random choices; the run is fixed by the initial data.

## Variants and improvements

- **Other assignment functions.** Nearest grid point (NGP) is cheaper but noisier; triangular shaped cloud (TSC) uses 27 points per particle in 3D and gives a smoother force (see [cloud-in-cell assignment](/cloud-in-cell-assignment/)).
- **Spectral differences and optimized Green's functions.** Line L5 can be done in Fourier space by multiplying by $-i k$, and the Green's function $1 / \lambda$ can be replaced by one that also divides out the smoothing of the assignment function. Hockney and Eastwood derive an optimal influence function that minimizes the force error for a given assignment.
- **P3M.** The [P3M method](/p3m-method/) adds a direct sum of the short-range force over near pairs, which restores the force at separations below a few cells.
- **TreePM.** The [TreePM method](/treepm-method/) uses a tree code for the short-range part instead of a direct sum.
- **Adaptive grids.** Adaptive mesh codes refine the grid where the density is high and solve Poisson's equation on each level.
- **Particle mesh Ewald.** In molecular dynamics, [particle mesh Ewald](/particle-mesh-ewald/) uses the same steps for the long-range part of the Ewald sum.

## When to use it

Use PM when the long-range field of many particles matters and the short-range force does not, as in a collisionless plasma ([plasma particle-in-cell](/plasma-particle-in-cell/)) or a dark matter simulation on scales above the grid spacing. It is also a cheap first stage inside P3M and TreePM. Do not use plain PM when close encounters matter, for example in star clusters or in molecular dynamics at short range, and do not use it for a strongly clustered system unless the grid is refined, because most of the grid then holds almost no mass.

## Pitfalls

- **A wrong sign of $s$.** Gravity has $\nabla^2 \phi = +4\pi G \rho$ and electrostatics $\nabla^2 \phi = -\rho / \epsilon_0$. With the wrong sign, like masses repel.
- **Not removing the mean.** If line L3 divides by $\lambda(0, 0) = 0$, the result is infinite or NaN. The mode $(0, 0)$ must be set to zero.
- **Different weights in L1 and L6.** Using CIC to deposit and NGP to interpolate gives self-forces and a drift of the total momentum.
- **A one-sided difference in L5.** A forward difference of $\phi$ is not odd, so the forces no longer sum to zero.
- **Too few cells.** The method resolves nothing below a cell. Results at those scales are an artefact of the grid, not physics.
- **A large time step.** The leapfrog is stable only for $h$ below about $2 / \omega$, where $\omega$ is the fastest frequency, for example the plasma frequency $\omega_p$ in a plasma.

## Implementations

## History

Particle-mesh codes were used for plasma simulation and for the dynamics of galaxies in the 1960s, when the FFT made fast Poisson solvers on grids practical. Hockney and Eastwood (first edition 1981, second edition 1988) gave the standard treatment of the method, with the assignment functions NGP, CIC and TSC, the conditions for momentum conservation and the optimal influence function. Efstathiou, Davis, White and Frenk (1985) compared the force accuracy of particle-mesh schemes for cosmological simulations in a periodic cube, and made P3M a standard tool in cosmology.

## References
