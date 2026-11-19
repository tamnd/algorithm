---
tag: K4C2TZ
kind: definition
slug: bgk-collision-operator
name: BGK collision operator
aliases:
- Bhatnagar-Gross-Krook operator
- single-relaxation-time collision
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: Relaxes particle distributions toward a local equilibrium with one time tau. In lattice Boltzmann it sets the viscosity nu = c_s^2 (tau - 1/2) dt, with tau in time steps.
prereqs: [lattice-boltzmann-method]
see_also: [multiple-relaxation-time-lattice-boltzmann, chapman-enskog-expansion, bounce-back-boundary-condition, direct-simulation-monte-carlo, linear-boltzmann-transport-equation, navier-stokes-equations]
sources:
  - paper: doi:10.1103/PhysRev.94.511
    title: "P. L. Bhatnagar, E. P. Gross and M. Krook, A model for collision processes in gases. I. Small amplitude processes in charged and neutral one-component systems, Physical Review 94 (1954) 511-525"
  - paper: doi:10.1209/0295-5075/17/6/001
    title: "Y. H. Qian, D. d'Humières and P. Lallemand, Lattice BGK models for Navier-Stokes equation, Europhysics Letters 17 (1992) 479-484"
  - paper: doi:10.1103/PhysRevA.45.R5339
    title: "Hudong Chen, Shiyi Chen and William H. Matthaeus, Recovery of the Navier-Stokes equations using a lattice-gas Boltzmann method, Physical Review A 45 (1992) R5339-R5342"
  - book: isbn:9783319446479
    title: "Timm Krüger, Halim Kusumaatmaja, Alexandr Kuzmin, Orest Shardt, Goncalo Silva and Erlend Magnus Viggen, The Lattice Boltzmann Method: Principles and Practice, Springer, 2017"
    locator: "Chapter 2 (the Boltzmann equation and the BGK model), Chapter 3 (the lattice BGK equation) and Chapter 4 (the viscosity from the Chapman-Enskog analysis)"
  - book: isbn:9780521408448
    title: "Sydney Chapman and T. G. Cowling, The Mathematical Theory of Non-uniform Gases, 3rd edition, Cambridge University Press, 1970"
---

The BGK collision operator replaces the collision integral of the Boltzmann equation by a relaxation toward a local equilibrium at one rate $1/\tau$. Bhatnagar, Gross and Krook introduced it in 1954 as a model of collisions in gases. It is the collision step of the standard [lattice Boltzmann method](/lattice-boltzmann-method/), where the single time $\tau$ fixes the viscosity. The [multiple-relaxation-time method](/multiple-relaxation-time-lattice-boltzmann/) generalizes it by giving each moment of the distribution its own rate; with all rates equal to $1/\tau$ it is BGK again.

## Definition

**Continuous form.** Let $f(x, \xi, t)$ be the density of particles at position $x$ with velocity $\xi$. Its moments give the density $\rho = \int f\,d\xi$, the momentum $\rho u = \int \xi f\,d\xi$ and the internal energy. Let $f^{\mathrm{eq}}$ be the Maxwell distribution with the same density, velocity and temperature as $f$. The BGK operator is

$$\Omega(f) = -\frac1\tau\bigl(f - f^{\mathrm{eq}}[f]\bigr), \qquad \partial_t f + \xi \cdot \nabla_x f = \Omega(f),$$

with a relaxation time $\tau > 0$. Because $f$ and $f^{\mathrm{eq}}$ have the same density, momentum and energy, $\int \Omega\,d\xi = 0$, $\int \xi\,\Omega\,d\xi = 0$ and $\int |\xi|^2\Omega\,d\xi = 0$: the operator conserves mass, momentum and energy, like the true collision integral. Bhatnagar, Gross and Krook also showed that it satisfies an H-theorem, so it drives $f$ to the local Maxwellian.

**Lattice form.** On a lattice with velocities $c_i$, weights $w_i$, sound speed $c_s$ and time step $\Delta t$, the lattice BGK update is

$$f_i(x + c_i\Delta t, t + \Delta t) = f_i(x, t) - \frac{\Delta t}{\tau}\bigl(f_i(x, t) - f_i^{\mathrm{eq}}(\rho, u)\bigr),$$

$$f_i^{\mathrm{eq}}(\rho, u) = w_i\rho\Bigl(1 + \frac{c_i \cdot u}{c_s^2} + \frac{(c_i \cdot u)^2}{2c_s^4} - \frac{|u|^2}{2c_s^2}\Bigr),$$

where $\rho = \sum_i f_i$ and $\rho u = \sum_i c_i f_i$ at the node. On D2Q9 in lattice units ($\Delta x = \Delta t = 1$), $c_s^2 = \frac13$ and the weights are $\frac49$, $\frac19$ and $\frac1{36}$. The weights make $\sum_i f_i^{\mathrm{eq}} = \rho$ and $\sum_i c_i f_i^{\mathrm{eq}} = \rho u$ exact identities, so the lattice collision conserves mass and momentum at each node exactly (in exact arithmetic). It does not conserve energy; the isothermal lattice has no energy equation.

**Viscosity.** The [Chapman-Enskog expansion](/chapman-enskog-expansion/) of the lattice BGK equation gives the Navier-Stokes equations at low Mach number with kinematic viscosity

$$\nu = c_s^2\Bigl(\tau - \frac{\Delta t}2\Bigr), \qquad \text{in lattice units } \nu = \frac13\Bigl(\tau - \frac12\Bigr).$$

The $-\frac{\Delta t}2$ is a discretization effect. The explicit update is a second-order (trapezoidal) integration of the BGK equation along the characteristic after a change of variables, and that change of variables shifts the relaxation time by $\frac{\Delta t}2$. In the continuous BGK model with $c_s^2$ the isothermal sound speed squared, the same expansion gives $\nu = c_s^2\tau$ (the dynamic viscosity is $\tau p$). Stability needs $\tau > \frac{\Delta t}2$, so $\nu > 0$; near $\tau = \frac12$ the scheme becomes unstable in practice, which is the limit MRT relaxes.

## Examples and non-examples

**One D2Q9 collision by hand.** Take a node at rest with $f_i = w_i$, and add $\frac1{100}$ to $f_1$ and to $f_3$, the two populations along $\pm x$. Then $\rho = \frac{51}{50}$, $u = 0$ and $f_i^{\mathrm{eq}} = w_i\rho$.

| $\tau$ | $f_0^*$ | $f_1^* = f_3^*$ | $f_2^* = f_4^*$ | $f_5^*, \ldots, f_8^*$ | $\sum f_i^*$ |
|---|---|---|---|---|---|
| 1 | $\frac{34}{75} = 0.45333$ | $\frac{17}{150} = 0.11333$ | $\frac{17}{150} = 0.11333$ | $\frac{17}{600} = 0.02833$ | $1.02$ |
| 0.8 | $\frac{41}{90} = 0.45556$ | $\frac{401}{3600} = 0.11139$ | $\frac{41}{360} = 0.11389$ | $\frac{41}{1440} = 0.02847$ | $1.02$ |

With $\tau = 1$ the collision returns the equilibrium in one step. With $\tau = 0.8$ the step is $\frac54$ of the way to the equilibrium, so the excess along $\pm x$ changes sign: $f_1^* - f_2^* = -0.0025$. In both cases the density stays $1.02$ and the momentum stays 0. With $\tau = 0.8$ the viscosity is $\nu = \frac13 \cdot 0.3 = 0.1$.

**The diffusion example.** On D1Q3 with a zero-velocity equilibrium and $\tau = 1$, BGK followed by streaming is the FTCS scheme for the heat equation with $\mu = \frac16$; the [lattice Boltzmann page](/lattice-boltzmann-method/) works this out by hand.

**Non-examples.**
- Relaxation toward a fixed global state, $\Omega = -(f - f_{\mathrm{ref}})/\tau$ with $f_{\mathrm{ref}}$ the same everywhere, is not BGK. It does not conserve momentum, so the flow it models is damped by a friction force.
- The [MRT collision](/multiple-relaxation-time-lattice-boltzmann/) with different rates for different moments is not BGK, though it contains BGK as the case of equal rates.
- The collision term of the [linear Boltzmann transport equation](/linear-boltzmann-transport-equation/) for neutrons scatters particles off a fixed background. It conserves particle number but not momentum, and it has no local Maxwellian.
- [Direct simulation Monte Carlo](/direct-simulation-monte-carlo/) samples the full binary collision integral of a dilute gas instead of a relaxation model.

## Related definitions

- **Prandtl number.** The continuous BGK model has a single relaxation time for momentum and heat, so it predicts a Prandtl number of 1; a monatomic gas has a Prandtl number of about $\frac23$. Thermal kinetic models (for example the ellipsoidal statistical BGK and the Shakhov model) change the operator to fix this. Isothermal lattice Boltzmann does not need a Prandtl number.
- **Knudsen number.** The ratio of the mean free path $c_s\tau$ to a flow length. The Chapman-Enskog expansion is an expansion in it.
- **Collision invariants.** The functions $1$, $\xi$ and $|\xi|^2$ whose moments every collision operator must keep. The lattice BGK operator keeps the first two.
- **Halfway bounce-back.** The usual wall condition for BGK; its wall position depends on $\tau$, see [bounce-back boundary condition](/bounce-back-boundary-condition/).

## References
