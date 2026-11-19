---
tag: A8NPMG
kind: model
slug: reynolds-averaged-navier-stokes
name: Reynolds-averaged Navier-Stokes equations
aliases:
- RANS equations
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: "Equations for the mean flow obtained by averaging Navier-Stokes, with a Reynolds stress term that a turbulence model must close."
model: real-ram
history:
  year: 1895
  people: [Osborne Reynolds]
  note: Reynolds split the velocity into a mean and a fluctuation in 1895 and showed that averaging the equations of motion leaves extra stresses made of products of fluctuations, now called the Reynolds stresses.
prereqs: [navier-stokes-equations]
see_also: [boussinesq-eddy-viscosity, mixing-length-model, k-epsilon-model, k-omega-sst-model, spalart-allmaras-model, wall-functions, large-eddy-simulation, simple-algorithm]
sources:
  - paper: doi:10.1098/rsta.1895.0004
    title: Osborne Reynolds, On the dynamical theory of incompressible viscous fluids and the determination of the criterion, Philosophical Transactions of the Royal Society of London A 186, 1895, 123-164
    locator: the split into mean and fluctuating motion and the averaged equations with the extra stresses
  - book: isbn:9780521598866
    title: Stephen B. Pope, Turbulent Flows, Cambridge University Press, 2000
    locator: Section 4.1 (the Reynolds equations), Section 4.2 (the Reynolds stresses), Section 7.1.2 (the balance of mean forces in channel flow) and Section 8.2 (an overview of the approaches)
  - book: isbn:9781928729082
    title: David C. Wilcox, Turbulence Modeling for CFD, third edition, DCW Industries, 2006
    locator: Chapter 2 (the closure problem, the Reynolds-averaged equations and the Reynolds-stress equation)
---

The Reynolds-averaged Navier-Stokes (RANS) equations are the equations for the mean velocity and mean pressure of a turbulent flow, obtained by averaging the [Navier-Stokes equations](/navier-stokes-equations/) after splitting each variable into a mean and a fluctuation. They are exact, but the averaging leaves the Reynolds stresses $\langle u_i' u_j' \rangle$ as new unknowns, so the system has more unknowns than equations. A closure supplies them: the [Boussinesq eddy viscosity hypothesis](/boussinesq-eddy-viscosity/) turns them into one scalar eddy viscosity, which the [mixing length model](/mixing-length-model/), the [k-epsilon model](/k-epsilon-model/), the [k-omega model](/k-omega-model/), the [SST model](/k-omega-sst-model/) or the [Spalart-Allmaras model](/spalart-allmaras-model/) then compute, and [wall functions](/wall-functions/) bridge the thin layer next to a wall.

## The machine

**Unknowns.** The mean velocity $U_i(x, t)$ (m/s) and the mean pressure $P(x, t)$ (Pa) of an incompressible flow with constant density $\rho$ (kg/m^3) and kinematic viscosity $\nu$ (m^2/s).

**Reynolds decomposition.** Write $u_i = U_i + u_i'$ and $p = P + p'$, where $U_i = \langle u_i \rangle$. The average $\langle \cdot \rangle$ is an ensemble average, a time average in a statistically steady flow, or an average over a homogeneous direction. It is linear, it commutes with derivatives, and $\langle u_i' \rangle = 0$. The average of a product is not the product of averages: $\langle u_i u_j \rangle = U_i U_j + \langle u_i' u_j' \rangle$.

**Equations.** Average the continuity and momentum equations:
$$\frac{\partial U_i}{\partial x_i} = 0, \qquad \frac{\partial U_i}{\partial t} + U_j \frac{\partial U_i}{\partial x_j} = -\frac{1}{\rho}\frac{\partial P}{\partial x_i} + \frac{\partial}{\partial x_j}\left(\nu \frac{\partial U_i}{\partial x_j} - \langle u_i' u_j' \rangle\right).$$
The term $-\rho\langle u_i' u_j' \rangle$ acts on the mean flow like a stress. It is the Reynolds stress tensor, symmetric, with six independent entries. Half its trace is the turbulent kinetic energy $k = \frac{1}{2}\langle u_i' u_i' \rangle$ (m^2/s^2).

**Closure problem.** There are four equations and $4 + 6 = 10$ unknowns. An exact equation for $\langle u_i' u_j' \rangle$ can be derived from the Navier-Stokes equations, but it contains triple products $\langle u_i' u_j' u_k' \rangle$ and pressure terms, and the equation for those has fourth moments. The chain never closes. A turbulence model cuts it with assumptions.

**Parameters.** The averaged equations have no fitted constant; every term is derived. All fitted constants of a RANS computation come with the closure: none for the averaging, one or two for the mixing length, five for the standard k-epsilon model, and so on.

**Computation.** In practice the equations are discretized by the [finite volume method](/finite-volume-method/) and solved for a steady mean flow by a pressure-correction scheme such as the [SIMPLE algorithm](/simple-algorithm/), with the closure equations solved alongside. Because only the mean is computed, the grid needs to resolve the mean gradients, not the eddies, which is why RANS is the cheapest of the three main approaches.

## What it counts

Given a closure, the model gives the mean velocity and mean pressure, and from them the wall shear stress, drag and lift, pressure drop, separation points and, with the averaged energy equation, mean heat transfer. With a two-equation closure it also gives $k$ and a turbulence time or length scale. It does not give spectra, the instantaneous flow or the probability of extreme events, because the averaging removes them.

## Relation to other models

- **Closure hypothesis.** The [Boussinesq hypothesis](/boussinesq-eddy-viscosity/) writes the anisotropic part of $\langle u_i' u_j' \rangle$ as an eddy viscosity times the mean strain rate. Most engineering closures use it.
- **Closures.** Algebraic: the [mixing length model](/mixing-length-model/). One equation: the [Spalart-Allmaras model](/spalart-allmaras-model/). Two equations: the [k-epsilon model](/k-epsilon-model/), the [k-omega model](/k-omega-model/) and the [SST model](/k-omega-sst-model/). Reynolds stress models solve modeled equations for all six stresses and drop the Boussinesq hypothesis.
- **Walls.** [Wall functions](/wall-functions/) replace the near-wall part of the solution by the log law, so that the grid need not resolve the viscous sublayer.
- **LES and DNS.** [Large eddy simulation](/large-eddy-simulation/) uses a spatial filter instead of an average, and the filtered equations have the same form with a subgrid stress in place of the Reynolds stress. [Direct numerical simulation](/direct-numerical-simulation/) solves the unaveraged equations and supplies the reference data on which RANS closures are tested.
- **Unsteady RANS.** If the flow has a slow, organized unsteadiness, such as vortex shedding behind a cylinder, the average can be taken over an ensemble or over short times, and the mean equations are integrated in time.

## Known results in the model

**Averaging by hand (exact arithmetic).** Four samples of the velocity $(u, v)$ in m/s at one point are $(1.2, -0.1)$, $(0.8, 0.1)$, $(1.1, -0.2)$ and $(0.9, 0.2)$. Then $U = 1.0$ and $V = 0$, the fluctuations are $u' = 0.2, -0.2, 0.1, -0.1$ and $v' = -0.1, 0.1, -0.2, 0.2$, and
$$\langle u'v' \rangle = -0.02, \qquad \langle u'^2 \rangle = \langle v'^2 \rangle = 0.025\ \text{m}^2/\text{s}^2.$$
For water with $\rho = 1000$ kg/m^3, the Reynolds shear stress is $-\rho\langle u'v' \rangle = 20$ Pa. The product of the means, $UV = 0$, misses this entirely.

**Realizability (theorem).** The Reynolds stress tensor is symmetric positive semidefinite: for any vector $a$, $a_i a_j \langle u_i' u_j' \rangle = \langle (a \cdot u')^2 \rangle \ge 0$. So the normal stresses are nonnegative and $\langle u'v' \rangle^2 \le \langle u'^2 \rangle \langle v'^2 \rangle$. The samples above satisfy it: $0.0004 \le 0.000625$. A closure that breaks this inequality predicts a flow that cannot exist.

**Channel flow stress balance (theorem).** In fully developed flow between walls at $y = 0$ and $y = 2\delta$, every mean quantity depends on $y$ alone and $V = 0$. The averaged stream-wise equation becomes $0 = -\frac{1}{\rho}\frac{dP}{dx} + \frac{d}{dy}\left(\nu \frac{dU}{dy} - \langle u'v' \rangle\right)$. Integrating from the wall, with the friction velocity $u_\tau = \sqrt{\tau_w/\rho}$,
$$\nu\frac{dU}{dy} - \langle u'v' \rangle = u_\tau^2\left(1 - \frac{y}{\delta}\right).$$
The total stress is linear in $y$ whatever the closure. For $u_\tau = 0.05$ m/s, it is $0.00125$ m^2/s^2 at $y = \delta/2$. Near the wall the viscous term carries it, farther out the Reynolds stress does; how it is shared is what a closure must predict.

**Energy exchange (theorem).** The equations for the mean kinetic energy and for $k$ share the term $\mathcal P = -\langle u_i' u_j' \rangle \partial U_i / \partial x_j$ with opposite signs. It is the production of turbulence: energy that the mean flow loses to the fluctuations. In the hand example with a mean shear $dU/dy = 10$ 1/s, $\mathcal P = 0.02 \times 10 = 0.2$ m^2/s^3.

**Agreement with experiment (measurement).** RANS with standard closures predicts the drag of attached flows, such as flat plates, pipes and wings at small angles, to within a few percent, and is much less reliable for separated and strongly curved flows. These are measurements of particular closures, not properties of the averaged equations.

## References
