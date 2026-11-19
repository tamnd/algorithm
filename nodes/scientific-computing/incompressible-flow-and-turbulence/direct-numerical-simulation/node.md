---
tag: 8EM7F7
kind: technique
slug: direct-numerical-simulation
name: Direct numerical simulation of turbulence
aliases:
- DNS of turbulence
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: "Resolves all scales down to the Kolmogorov scale. The grid needs about Re^(9/4) points and Re^(3/4) time steps, so the total cost grows like Re^3."
model: real-ram
history:
  year: 1972
  people: [Steven Orszag, G. S. Patterson, John Kim, Parviz Moin, Robert Moser]
  note: Orszag and Patterson computed isotropic turbulence on a 32^3 grid with a pseudo-spectral method in 1972. Kim, Moin and Moser computed turbulent channel flow in 1987, and the data became a standard test for turbulence models.
prereqs: [kolmogorov-1941-theory, navier-stokes-equations, spectral-methods]
see_also: [large-eddy-simulation, kolmogorov-1941-theory, spectral-methods, fast-fourier-transform, chorin-projection-method, reynolds-averaged-navier-stokes, courant-friedrichs-lewy-condition, navier-stokes-equations]
sources:
  - book: isbn:9780521598866
    title: Stephen B. Pope, Turbulent Flows, Cambridge University Press, 2000
    locator: Chapter 9 (9.1.1 the pseudo-spectral method, 9.1.2 the computational cost, 9.1.3 artificial modifications, 9.2.1 channel flow)
  - paper: doi:10.1103/PhysRevLett.28.76
    title: Steven A. Orszag and G. S. Patterson, Numerical simulation of three-dimensional homogeneous isotropic turbulence, Physical Review Letters 28(2), 1972, 76-79
    locator: the first direct simulation of isotropic turbulence, pseudo-spectral on a 32^3 grid
  - paper: doi:10.1017/S0022112087000892
    title: John Kim, Parviz Moin and Robert Moser, Turbulence statistics in fully developed channel flow at low Reynolds number, Journal of Fluid Mechanics 177, 1987, 133-166
    locator: the channel flow at a friction Reynolds number of 180, with Fourier and Chebyshev expansions
  - paper: doi:10.1146/annurev.fluid.30.1.539
    title: Parviz Moin and Krishnan Mahesh, Direct numerical simulation, a tool in turbulence research, Annual Review of Fluid Mechanics 30, 1998, 539-578
    locator: resolution requirements, numerical methods and the uses of the data
---

Direct numerical simulation (DNS) of turbulence is the numerical solution of the [Navier-Stokes equations](/navier-stokes-equations/) on a grid and with a time step fine enough to resolve every eddy, from the size of the flow down to the Kolmogorov scale, with no turbulence model. The [Kolmogorov 1941 theory](/kolmogorov-1941-theory/) gives the smallest scale $\eta = (\nu^3/\varepsilon)^{1/4}$ and the estimate that the number of grid points grows like $Re^{9/4}$, the number of time steps like $Re^{3/4}$, and the total work like $Re^3$. [Large eddy simulation](/large-eddy-simulation/) is the cheaper neighbor: it resolves only the large eddies and represents the rest by a subgrid model such as the [Smagorinsky model](/smagorinsky-model/) or the [dynamic subgrid model](/dynamic-subgrid-model/). [Reynolds-averaged models](/reynolds-averaged-navier-stokes/) resolve none of the eddies.

## In plain words

Turbulence is a tangle of eddies of all sizes. A direct simulation follows every one of them. It uses the flow equations as they are, with no extra rules, and it makes the grid so fine that even the smallest eddies span a few cells. This makes the result as good as an experiment for the flow it computes, and better in one way: every value at every point and time is available. The price is very high. When the flow gets faster or larger, the smallest eddies get smaller, so the grid needs many more points and the time steps must get shorter. A tenfold rise in speed costs about a thousand times more work. So direct simulation is a research tool for simple flows at moderate speeds, and its results are used to test the cheaper models.

## When it applies

- The flow is turbulent and the Reynolds number $Re = UL/\nu$ is low or moderate, so that $Re^{9/4}$ grid points fit in memory. Here $U$ and $L$ are the velocity and size of the large eddies and $\nu$ is the kinematic viscosity in m^2/s.
- The geometry is simple: a periodic box (homogeneous turbulence), a channel, a pipe, a boundary layer on a flat plate, a mixing layer or a jet.
- The aim is understanding or reference data: statistics such as the Reynolds stresses and the dissipation, which are hard to measure, and data to test [RANS](/reynolds-averaged-navier-stokes/) closures and subgrid models.
- It does not apply to most engineering flows. An airliner wing at $Re \approx 10^7$ would need of the order of $10^{16}$ points by the estimate below.

## The template

**Resolution (rule of thumb).** Choose the grid spacing $\Delta x$ so that the smallest resolved wavenumber band reaches the dissipation range. For a pseudo-spectral method with $N$ points per side of a box of side $\mathcal L$, the largest wavenumber after dealiasing is $k_{max} = \frac{\sqrt 2}{3} N \frac{2\pi}{\mathcal L}$, and the usual criterion is $k_{max}\eta \ge 1.5$. This criterion is a rule fitted to how well the dissipation spectrum converges; values near 1 are also in use. Choose the box several integral scales wide, so that the largest eddies do not feel the periodicity.

**Time step (rule of thumb).** For an explicit time stepping, keep the Courant number $Co = |u|_{max}\Delta t / \Delta x$ below about 1 (the [CFL condition](/courant-friedrichs-lewy-condition/) sets the hard limit for the scheme, and accuracy for the small eddies wants a step near $\tau_\eta$ or smaller).

**Cost (heuristic).** With $\Delta x \sim \eta$ and $\varepsilon \sim U^3/L$:

- grid points: $(L/\eta)^3 \sim Re^{9/4}$;
- time step: $\Delta t \sim \Delta x / U \sim \eta / U$, so a run over one large-eddy time $L/U$ takes $L/\eta \sim Re^{3/4}$ steps;
- work: about $Re^{9/4} \cdot Re^{3/4} = Re^3$, times a factor $\log N$ for the [FFT](/fast-fourier-transform/) in a spectral code.

The constants depend on the definition of $Re$, the resolution criterion and the number of large-eddy times needed for converged statistics (often tens). The exponents follow from the K41 scaling and are as reliable as it is.

**Steps.**

1. Pick the domain, the boundary conditions and the forcing (a fixed pressure gradient in a channel, a forcing of the lowest wavenumbers in a box, or none for decaying turbulence).
2. Discretize in space with a high-accuracy method: [spectral methods](/spectral-methods/) in periodic directions, Chebyshev polynomials across a channel, or high-order finite differences on a staggered grid.
3. Advance in time with a [Runge-Kutta method](/runge-kutta-methods/) for the nonlinear term and often an implicit step for the viscous term, and enforce $\nabla \cdot u = 0$ by a [projection](/chorin-projection-method/) or by working with divergence-free basis functions.
4. In a pseudo-spectral code, compute the product $u \cdot \nabla u$ in physical space and remove aliasing errors by the 2/3 rule or by phase shifts.
5. Start from a random field with a chosen spectrum, run until the statistics stop drifting, then average over time and over the homogeneous directions.
6. Check the resolution: the energy and dissipation spectra fall off by several decades at $k_{max}$, the mean dissipation matches the energy input, and statistics do not change when the grid is refined.

## Classic examples

**Isotropic turbulence in a box.** Orszag and Patterson (1972) used a pseudo-spectral method on a $32^3$ grid, the first direct simulation of three-dimensional turbulence. Later box simulations reached grids of several thousand points per side and are used to measure the Kolmogorov constant and intermittency.

**Channel flow.** Kim, Moin and Moser (1987) simulated a channel at friction Reynolds number $Re_\tau = u_\tau \delta / \nu = 180$, with Fourier modes along the walls and Chebyshev polynomials across. The grid had about $4 \times 10^6$ points. Their mean profile and Reynolds stresses became the reference for near-wall models and for [wall functions](/wall-functions/).

**Cost table (by hand).** With points $Re^{9/4}$ and steps $Re^{3/4}$ per large-eddy time and all constants set to one:

| $Re$ | grid points | steps | work |
|---|---|---|---|
| $10^3$ | $5.6 \times 10^6$ | 178 | $10^9$ |
| $10^4$ | $10^9$ | 1000 | $10^{12}$ |
| $10^5$ | $1.8 \times 10^{11}$ | 5623 | $10^{15}$ |
| $10^6$ | $3.2 \times 10^{13}$ | 31623 | $10^{18}$ |

For example $10^{4 \cdot 9/4} = 10^9$ and $10^{4 \cdot 3/4} = 10^3$. Each tenfold rise in $Re$ multiplies the work by 1000.

## Variations

- **Pseudo-spectral DNS** in periodic boxes, the most accurate per grid point for homogeneous turbulence.
- **Finite difference and finite volume DNS** on staggered grids (the [MAC grid](/mac-grid/)), with second- or higher-order central schemes that conserve kinetic energy. These handle more complex geometry, at the price of more points per eddy.
- **Forced and decaying turbulence.** Forcing the large scales gives a statistically steady state; decaying runs mimic grid turbulence.
- **Scalars and other physics.** DNS can carry temperature, a passive scalar, buoyancy, particles or a reacting species, each with its own small scale (for a scalar with low diffusivity, the Batchelor scale, smaller than $\eta$).
- **Quasi-DNS or under-resolved DNS.** A grid with $k_{max}\eta$ somewhat below 1 captures most of the energy but not the dissipation spectrum. It is a different method and must be reported as such.

## Pitfalls

- **Under-resolution.** A grid too coarse for $\eta$ piles up energy at the highest wavenumbers and gives wrong dissipation and intermittency statistics. Check the spectrum.
- **Aliasing.** Without dealiasing, the nonlinear term in a pseudo-spectral code feeds false energy into resolved modes and can make the run unstable.
- **Box too small.** If the box is not several integral scales wide, or a channel is too short in the stream direction, the large eddies interact with their periodic copies and the statistics change.
- **Unconverged statistics.** Averages over too few large-eddy times, or taken before the start-up transient has gone, have large random errors. Report the averaging time.
- **Comparing at different Reynolds numbers.** DNS is often at lower $Re$ than the experiment it is compared with; low-$Re$ effects, such as a short inertial range, are real features of the DNS, not errors.

## Exercises

1. Water at 20 C has $\nu = 1.0 \times 10^{-6}$ m^2/s. For $\varepsilon = 10^{-2}$ m^2/s^3, find $\eta$. (Answer: $(10^{-18}/10^{-2})^{1/4} = 10^{-4}$ m.)
2. A code runs a flow at $Re = 2000$ in one day. Estimate the time for $Re = 20\,000$ on the same machine. (Answer: about $10^3$ days, from the $Re^3$ estimate.)
3. A pseudo-spectral run in a box of side $2\pi$ m has $N = 512$ and $\eta = 0.004$ m. Does it meet $k_{max}\eta \ge 1.5$? (Answer: $k_{max} = \frac{\sqrt 2}{3} \cdot 512 = 241$ 1/m, so $k_{max}\eta = 0.97$; it does not.)

## References
