---
tag: 5GV2JK
kind: concept
slug: boussinesq-eddy-viscosity
name: Boussinesq eddy viscosity hypothesis
aliases:
- eddy viscosity hypothesis
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: "Models the Reynolds stresses as a turbulent eddy viscosity times the mean strain rate, so closure needs only one scalar field."
model: real-ram
history:
  year: 1877
  people: [Joseph Boussinesq]
  note: Boussinesq proposed in his 1877 essay on running water that turbulent mixing acts on the mean flow like an increased viscosity. The tensor form with the turbulent kinetic energy term came later with the two-equation models.
prereqs: [reynolds-averaged-navier-stokes]
see_also: [reynolds-averaged-navier-stokes, mixing-length-model, k-epsilon-model, k-omega-model, k-omega-sst-model, spalart-allmaras-model, smagorinsky-model, navier-stokes-equations]
sources:
  - paper: "Joseph Boussinesq, Essai sur la théorie des eaux courantes, Mémoires présentés par divers savants à l'Académie des Sciences de l'Institut de France 23(1), 1877, 1-680"
    locator: the coefficient of turbulent mixing that replaces the molecular viscosity in the equations of the mean flow
  - book: isbn:9780521598866
    title: Stephen B. Pope, Turbulent Flows, Cambridge University Press, 2000
    locator: Section 4.4 (gradient-diffusion and turbulent-viscosity hypotheses), Section 7.1.6 (Reynolds stresses in channel flow) and Section 10.1 (the turbulent-viscosity hypothesis)
  - book: isbn:9781928729082
    title: David C. Wilcox, Turbulence Modeling for CFD, third edition, DCW Industries, 2006
    locator: Chapter 6 (beyond the Boussinesq approximation, its failures and nonlinear constitutive relations)
  - paper: doi:10.1016/j.crme.2007.08.004
    title: François G. Schmitt, About Boussinesq's turbulent viscosity hypothesis, historical remarks and a direct evaluation of its validity, Comptes Rendus Mécanique 335(9-10), 2007, 617-627
    locator: the history of the hypothesis and a test of the alignment of stress and strain against data
---

The Boussinesq eddy viscosity hypothesis is the assumption that the anisotropic part of the Reynolds stress tensor is proportional to the mean strain rate, with a scalar coefficient, the eddy viscosity $\nu_t$. It is the closure hypothesis of most turbulence models: the [Reynolds-averaged Navier-Stokes equations](/reynolds-averaged-navier-stokes/) are the exact averaged equations, and the hypothesis reduces their six unknown stresses to one unknown field. The [mixing length model](/mixing-length-model/), the [k-epsilon model](/k-epsilon-model/), the [k-omega model](/k-omega-model/), the [SST model](/k-omega-sst-model/) and the [Spalart-Allmaras model](/spalart-allmaras-model/) are different ways to compute $\nu_t$, and [wall functions](/wall-functions/) supply it next to walls. The hypothesis is a model, not a theorem, and measured stresses break it in many flows.

## In plain words

In a turbulent flow, eddies carry fast fluid into slow regions and slow fluid into fast ones. On average this evens out the flow, much as the stickiness of a fluid does, only far more strongly. Boussinesq proposed to treat the eddies as an extra stickiness. The flow then obeys the usual equations with a larger viscosity, and the turbulence model has one job: to find how large the extra viscosity is at each place. The idea is simple and often works for flows along walls. But the eddy stickiness is a property of the flow, not of the fluid, and it changes from place to place. The guess also forces the eddy stresses to line up with the stretching of the mean flow, which real turbulence often does not do.

## The idea

**Statement.** With the mean strain rate $S_{ij} = \frac{1}{2}\left(\partial U_i/\partial x_j + \partial U_j/\partial x_i\right)$ (1/s) and the turbulent kinetic energy $k = \frac{1}{2}\langle u_i' u_i' \rangle$ (m^2/s^2),
$$-\langle u_i' u_j' \rangle = 2\nu_t S_{ij} - \frac{2}{3} k\, \delta_{ij}.$$
The $k$ term is needed so that the trace of both sides agrees: the trace of $S_{ij}$ is zero for incompressible flow, and the trace of $\langle u_i' u_j' \rangle$ is $2k$.

**Effect on the mean equations.** Put the hypothesis into the RANS momentum equation. The stress term becomes $\partial_j\left(2(\nu + \nu_t) S_{ij}\right)$, and the $k$ term is absorbed into a modified pressure $P + \frac{2}{3}\rho k$. So the mean flow obeys the [Navier-Stokes equations](/navier-stokes-equations/) with an effective viscosity $\nu + \nu_t$ that varies in space.

**What sets the eddy viscosity (dimensional reasoning, heuristic).** $\nu_t$ has units m^2/s, so it is a velocity scale times a length scale of the eddies. The closures differ in how they get these scales: from the distance to the wall ([mixing length](/mixing-length-model/)), from $k$ and its dissipation rate $\varepsilon$ ($\nu_t = C_\mu k^2/\varepsilon$), from $k$ and $\omega$ ($\nu_t = k/\omega$), or from a transport equation for $\nu_t$ itself.

**Consequences that are exact within the hypothesis.**

- The principal axes of the stress anisotropy are those of the mean strain rate.
- The production of $k$ is $\mathcal P = 2\nu_t S_{ij} S_{ij} \ge 0$ when $\nu_t \ge 0$, so energy can only flow from the mean flow to the turbulence.
- In a simple shear flow $U(y)$, every diagonal entry of $S_{ij}$ is zero, so the three normal stresses are equal, each $\frac{2}{3}k$.

**Where it fails (measurement).** In channel flow the measured normal stresses are far from equal: the stream-wise one is the largest and the wall-normal one the smallest (Pope 7.1.6). Flows with strong curvature, rotation, swirl or secondary motions in non-circular ducts show stresses that are not aligned with the strain, and some flows, such as wall jets, have regions where $-\langle u'v' \rangle$ and the mean velocity gradient $dU/dy$ have opposite signs, which no positive $\nu_t$ can give. The hypothesis is a working rule that is good for thin shear layers and poor for these flows.

## Examples

**Shear stress in a simple shear.** Take $U(y)$ with $dU/dy = 10$ 1/s and $\nu_t = 0.01$ m^2/s. Then $S_{12} = 5$ 1/s and
$$-\langle u'v' \rangle = 2 \times 0.01 \times 5 = 0.1\ \text{m}^2/\text{s}^2.$$
In water ($\rho = 1000$ kg/m^3) the Reynolds shear stress is 100 Pa. The molecular stress $\rho\nu\, dU/dy$ with $\nu = 10^{-6}$ m^2/s is 0.01 Pa, ten thousand times smaller. The production is $\mathcal P = \nu_t (dU/dy)^2 = 1$ m^2/s^3.

**Equal normal stresses.** In the same flow with $k = 0.15$ m^2/s^2, the hypothesis gives $\langle u'^2 \rangle = \langle v'^2 \rangle = \langle w'^2 \rangle = 0.1$ m^2/s^2. A measurement in a real shear flow gives three different values with the same sum.

**A stress that cannot exist.** Take a strong plane strain with $\partial U/\partial x = 4$ 1/s, so $S_{11} = 4$, and $k = 1$ m^2/s^2 with $\nu_t = 0.1$ m^2/s. Then
$$\langle u'^2 \rangle = \frac{2}{3}k - 2\nu_t S_{11} = 0.667 - 0.8 = -0.133\ \text{m}^2/\text{s}^2.$$
A mean square cannot be negative, so the hypothesis breaks realizability here. This happens near stagnation points, and it is one reason for the limiters in the [SST model](/k-omega-sst-model/) and the realizable variants of the k-epsilon model.

## Where it is used

- **Algebraic and one-equation RANS models:** the [mixing length model](/mixing-length-model/) and the [Spalart-Allmaras model](/spalart-allmaras-model/).
- **Two-equation RANS models:** the [k-epsilon model](/k-epsilon-model/), the [k-omega model](/k-omega-model/) and the [SST model](/k-omega-sst-model/), which also use $k$ in the isotropic part.
- **Subgrid models in LES:** the [Smagorinsky model](/smagorinsky-model/) has the same form, with the subgrid stress in place of the Reynolds stress and a viscosity built from the grid size.
- **Heat and mass transfer:** the analogous gradient-diffusion hypothesis writes the turbulent heat flux as $-\langle u_i'\theta' \rangle = (\nu_t/\sigma_t)\,\partial\Theta/\partial x_i$, with a turbulent Prandtl number $\sigma_t$ near 0.85 as a rule of thumb for air.
- **Beyond it:** nonlinear eddy viscosity models add products of strain and rotation, and Reynolds stress models solve for all six stresses, for flows where the hypothesis fails.

## References
