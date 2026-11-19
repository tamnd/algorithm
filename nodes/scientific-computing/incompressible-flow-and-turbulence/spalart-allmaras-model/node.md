---
tag: R68Z0Z
kind: model
slug: spalart-allmaras-model
name: Spalart-Allmaras model
area: scientific-computing/incompressible-flow-and-turbulence
level: advanced
summary: "A one-equation turbulence model for a modified eddy viscosity, built for aerodynamic flows over wings."
model: real-ram
history:
  year: 1992
  people: [Philippe Spalart, Steven Allmaras]
  note: Spalart and Allmaras presented the model at the AIAA Aerospace Sciences Meeting in 1992 and published the reference version in La Recherche Aérospatiale in 1994. Spalart and coworkers used it in 1997 as the base of detached eddy simulation.
prereqs: [boussinesq-eddy-viscosity]
see_also: [k-omega-sst-model, k-omega-model, k-epsilon-model, mixing-length-model, boussinesq-eddy-viscosity, reynolds-averaged-navier-stokes, large-eddy-simulation]
sources:
  - paper: "P. R. Spalart and S. R. Allmaras, A one-equation turbulence model for aerodynamic flows, AIAA Paper 92-0439, 30th Aerospace Sciences Meeting, Reno, 1992"
    locator: the first version of the model and its calibration
  - paper: "P. R. Spalart and S. R. Allmaras, A one-equation turbulence model for aerodynamic flows, La Recherche Aérospatiale 1994(1), 1994, 5-21"
    locator: the reference version, with the transport equation, the functions f_v1, f_v2, f_w and f_t2, and the constants
  - paper: "S. R. Allmaras, F. T. Johnson and P. R. Spalart, Modifications and clarifications for the implementation of the Spalart-Allmaras turbulence model, Seventh International Conference on Computational Fluid Dynamics, ICCFD7-1902, Big Island, Hawaii, 2012"
    locator: the treatment of negative values of the working variable and the recommended free-stream values
  - book: isbn:9780521598866
    title: Stephen B. Pope, Turbulent Flows, Cambridge University Press, 2000
    locator: Section 10.5.2 (the Spalart-Allmaras model)
---

The Spalart-Allmaras model is a one-equation closure of the [Reynolds-averaged Navier-Stokes equations](/reynolds-averaged-navier-stokes/) that solves a single transport equation for a working variable $\tilde\nu$, from which the eddy viscosity is $\nu_t = \tilde\nu f_{v1}$. It applies the [Boussinesq hypothesis](/boussinesq-eddy-viscosity/) like the two-equation [k-epsilon](/k-epsilon-model/), [k-omega](/k-omega-model/) and [SST](/k-omega-sst-model/) models, but it carries no turbulent kinetic energy and no length scale of its own: the length comes from the distance to the wall, as in the [mixing length model](/mixing-length-model/). It was built and calibrated for attached and mildly separated flows over wings, and it is integrated to the wall rather than used with [wall functions](/wall-functions/).

## The machine

**Unknowns.** The mean flow and $\tilde\nu$ (m^2/s), plus the distance $d$ to the nearest wall. The kinematic viscosity is $\nu$ and the vorticity magnitude of the mean flow is $\Omega$ (1/s).

**Equation (the standard form, with the trip term).**
$$\frac{D\tilde\nu}{Dt} = c_{b1}(1 - f_{t2})\tilde S\tilde\nu - \left(c_{w1}f_w - \frac{c_{b1}}{\kappa^2}f_{t2}\right)\left(\frac{\tilde\nu}{d}\right)^2 + \frac{1}{\sigma}\left[\nabla\cdot\left((\nu + \tilde\nu)\nabla\tilde\nu\right) + c_{b2}|\nabla\tilde\nu|^2\right].$$
The terms are production, destruction near walls, and diffusion with a nonlinear part.

**Functions.**

- $\chi = \tilde\nu/\nu$, $f_{v1} = \chi^3/(\chi^3 + c_{v1}^3)$, $\nu_t = \tilde\nu f_{v1}$.
- $f_{v2} = 1 - \chi/(1 + \chi f_{v1})$ and $\tilde S = \Omega + \tilde\nu f_{v2}/(\kappa^2 d^2)$.
- $r = \min\left(\tilde\nu/(\tilde S\kappa^2 d^2), 10\right)$, $g = r + c_{w2}(r^6 - r)$, $f_w = g\left(\frac{1 + c_{w3}^6}{g^6 + c_{w3}^6}\right)^{1/6}$.
- $f_{t2} = c_{t3}\exp(-c_{t4}\chi^2)$, which keeps a laminar region with $\tilde\nu \approx 0$ laminar.

**Parameters.**

| constant | value | status |
|---|---|---|
| $c_{b1}$ | 0.1355 | fitted to the shear stress level of a mixing layer |
| $\sigma$ | 2/3 | fitted, with $c_{b2}$, to the spreading of wakes and mixing layers |
| $c_{b2}$ | 0.622 | fitted |
| $\kappa$ | 0.41 | measured von Karman constant |
| $c_{w1}$ | $c_{b1}/\kappa^2 + (1 + c_{b2})/\sigma = 3.239$ | derived from the log layer (below) |
| $c_{w2}$ | 0.3 | fitted to the skin friction of a flat plate |
| $c_{w3}$ | 2 | fitted, with $c_{w2}$ |
| $c_{v1}$ | 7.1 | fitted to the intercept of the log law |
| $c_{t3}$, $c_{t4}$ | 1.2, 0.5 | chosen for the trip term |

The 1992 conference paper and the 1994 journal version differ slightly in some constants and terms; codes usually follow the 1994 version, and a page or code must say which.

**Boundary values.** At a wall $\tilde\nu = 0$. In the free stream a small value is used; $\tilde\nu_\infty$ of 3 to 5 times $\nu$ is a common rule for fully turbulent runs. Implementations need a guard for negative $\tilde\nu$, which the discrete equations can produce; the 2012 paper by Allmaras, Johnson and Spalart gives one.

## What it counts

The model gives the mean flow, the eddy viscosity and the Boussinesq stresses, and from them lift, drag, wall shear stress and separation. It gives no turbulent kinetic energy, so any quantity that needs $k$ (for example the isotropic part of the stress) must be dropped or estimated.

## Relation to other models

- **Mixing length.** In the log layer the model gives $\nu_t = \kappa u_\tau y$, and its length scale is the wall distance $d$, so it is a transported version of the [mixing length](/mixing-length-model/) idea.
- **Two-equation models.** [k-epsilon](/k-epsilon-model/), [k-omega](/k-omega-model/) and [SST](/k-omega-sst-model/) carry a second variable that sets the length scale; SA is cheaper and more robust but cannot predict a length scale away from walls.
- **Detached eddy simulation.** Replacing $d$ by $\min(d, C_{DES}\Delta)$, with $\Delta$ the grid size, turns the model into a subgrid model away from walls. This was the first detached eddy simulation, a hybrid of RANS and [large eddy simulation](/large-eddy-simulation/).
- **Corrections.** Versions exist for rotation and curvature, for compressibility and for rough walls; the base model has none of these effects.

## Known results in the model

**Log layer (exact in the model).** In a constant-stress layer with $\tilde\nu = \kappa u_\tau y$ and $\Omega = u_\tau/(\kappa y)$ (with $d = y$), $\chi$ is large, so $f_{v1} \approx 1$ and $\tilde S \approx \Omega$. Then $r = \kappa u_\tau y/(\Omega\kappa^2 y^2) = 1$, so $g = 1$ and $f_w = 1$. Ignoring $f_{t2}$, the three terms are
$$c_{b1}u_\tau^2 \ (\text{production}), \qquad c_{w1}\kappa^2 u_\tau^2 \ (\text{destruction}), \qquad \frac{1 + c_{b2}}{\sigma}\kappa^2 u_\tau^2 \ (\text{diffusion}),$$
since $\frac{d}{dy}(\tilde\nu\,\frac{d\tilde\nu}{dy}) = \kappa^2 u_\tau^2$ and $c_{b2}(\frac{d\tilde\nu}{dy})^2 = c_{b2}\kappa^2u_\tau^2$. The balance holds when $c_{w1} = c_{b1}/\kappa^2 + (1 + c_{b2})/\sigma = 0.1355/0.1681 + 1.622/0.6667 = 0.806 + 2.433 = 3.239$. This is why $c_{w1}$ is derived, not fitted. The function $f_{v2}$ is built so that $\tilde\nu = \kappa u_\tau y$ stays a solution down into the buffer layer.

**Damping function by hand.** With $c_{v1} = 7.1$, $c_{v1}^3 = 357.9$:

| $\chi$ | $f_{v1}$ | $f_{v2}$ |
|---|---|---|
| 1 | $1/358.9 = 0.0028$ | 0.0028 |
| 7.1 | 0.5 | $1 - 7.1/4.55 = -0.560$ |
| 10 | $1000/1357.9 = 0.736$ | $1 - 10/8.36 = -0.196$ |

So $\nu_t \approx \tilde\nu$ well inside the turbulent region, and $\nu_t$ is much smaller than $\tilde\nu$ near the wall, where $\chi$ is small. The negative $f_{v2}$ is intended: it lowers $\tilde S$ in the buffer layer.

**Agreement with experiment (measurement).** For attached boundary layers, wakes and mildly separated airfoil flows, the model predicts lift, drag and skin friction close to measurements, which made it a standard in external aerodynamics. It is less accurate for free shear flows such as round jets, for massive separation, and for flows with strong rotation or curvature unless a correction is added. These are measured comparisons for the fitted constants.

## References
