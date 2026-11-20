---
tag: QJ60FZ
kind: model
slug: phase-field-model
name: Phase-field model
aliases:
- diffuse interface model
area: scientific-computing/multiscale-methods
level: core
summary: Describes interfaces such as solidification fronts by a smooth order parameter, evolved by Allen-Cahn or Cahn-Hilliard equations, so they move implicitly.
model: real-ram
history:
  year: 1958
  people: [John W. Cahn, John E. Hilliard, Samuel M. Allen]
  note: Cahn and Hilliard wrote the free energy of a nonuniform system with a gradient term in 1958, and Allen and Cahn gave the equation for the motion of antiphase boundaries in 1979. Phase-field models of solidification followed, and Karma and Rappel made them quantitative in 1998.
prereqs: [heat-equation, gradient-descent]
see_also: [level-set-method, volume-of-fluid-method, front-tracking-method, spectral-methods, operator-splitting, crank-nicolson-method, navier-stokes-equations, multiscale-modeling]
sources:
  - paper: doi:10.1063/1.1744102
    title: John W. Cahn and John E. Hilliard, Free energy of a nonuniform system. I. Interfacial free energy, The Journal of Chemical Physics 28(2), 1958, 258-267
    locator: the free energy with a gradient squared term and the interfacial energy of a flat interface
  - paper: doi:10.1016/0001-6160(79)90196-2
    title: Samuel M. Allen and John W. Cahn, A microscopic theory for antiphase boundary motion and its application to antiphase domain coarsening, Acta Metallurgica 27(6), 1979, 1085-1095
    locator: the equation for a nonconserved order parameter and the motion of the boundaries by their curvature
  - paper: doi:10.1002/cpa.3160450903
    title: L. C. Evans, H. M. Soner and P. E. Souganidis, Phase transitions and generalized motion by mean curvature, Communications on Pure and Applied Mathematics 45(9), 1992, 1097-1123
    locator: the convergence of the Allen-Cahn equation to the level set motion by mean curvature
  - paper: doi:10.1103/PhysRevE.57.4323
    title: Alain Karma and Wouter-Jan Rappel, Quantitative phase-field modeling of dendritic growth in two and three dimensions, Physical Review E 57(4), 1998, 4323-4349
    locator: the thin interface analysis that relates the model parameters to the capillary length and the interface kinetics
  - paper: doi:10.1146/annurev.matsci.32.112001.132041
    title: Long-Qing Chen, Phase-field models for microstructure evolution, Annual Review of Materials Research 32, 2002, 113-140
    locator: a review of the models for solidification, phase separation and solid state transformations
---

A phase-field model describes a system with two or more phases, such as solid and liquid or two mixed fluids, by an order parameter $u(x, t)$ that is near $+1$ in one phase, near $-1$ in the other, and changes smoothly across an interface of width about $\varepsilon$. The interface is not tracked: it is the region where $u$ is near $0$, and it moves because $u$ evolves by a partial differential equation, the gradient flow of a free energy. The Allen-Cahn equation is the flow for an order parameter that is not conserved, and it moves interfaces by their curvature; the Cahn-Hilliard equation conserves the integral of $u$, and it describes phase separation and coarsening. Topology changes, such as droplets that merge or break up, need no special treatment. The model links a microscopic free energy to the sharp interface laws of the continuum, as in the [level set method](/level-set-method/), but with a physical interface energy built in.

## The machine

**Unknowns and energy.** The order parameter $u(x, t)$ on a domain in $\mathbb{R}^d$ with periodic or no-flux boundary conditions, and the free energy
$$\mathcal{F}[u] = \int \Big( \frac{\varepsilon^2}{2} |\nabla u|^2 + W(u) \Big)\, dx, \qquad W(u) = \frac14 (u^2 - 1)^2 .$$
The double well $W$ has minima at the two phases $u = \pm 1$, and the gradient term penalizes sharp changes. The chemical potential is the variational derivative $\mu = \delta \mathcal{F} / \delta u = W'(u) - \varepsilon^2 \Delta u$, with $W'(u) = u^3 - u$.

**Allen-Cahn (nonconserved).** The $L^2$ gradient flow with mobility $M$:
$$\partial_t u = -M \mu = M \big( \varepsilon^2 \Delta u - W'(u) \big).$$

**Cahn-Hilliard (conserved).** The $H^{-1}$ gradient flow, a conservation law with the flux $-M \nabla \mu$:
$$\partial_t u = \nabla \cdot \big( M \nabla \mu \big), \qquad \mu = W'(u) - \varepsilon^2 \Delta u .$$

**Solidification.** Models of solidification couple $u$ to a temperature or a concentration field $T$, which obeys a diffusion equation with a source from the latent heat, $\partial_t T = D \Delta T + \frac12 \partial_t u$ in dimensionless form, and tilt the double well by a term proportional to $T$, so that the phase with the lower free energy grows. Anisotropy of the interface energy enters through an $\varepsilon$ that depends on the direction of $\nabla u$.

**Parameters, fitted and derived.** With physical units the energy is $\int (\frac{\kappa}{2} |\nabla u|^2 + H W(u))\, dx$. The interface energy $\sigma$ is measured (fitted), and the width is chosen; then $\kappa$ and the barrier height $H$ are derived from $\sigma = \frac{2 \sqrt 2}{3} \sqrt{\kappa H}$ and the width $\sqrt{2 \kappa / H}$ (Known result 3 with $\varepsilon^2 = \kappa / H$). The mobility $M$ is fitted to the measured speed of the interface or, in alloys, derived from the diffusion coefficient. In quantitative solidification models, the width is a numerical parameter much larger than the physical width, and the thin interface analysis of Karma and Rappel (1998) derives the coupling constant and the relaxation time from the capillary length and the diffusivity, so that the results do not depend on the width to leading order.

**Discretization.** Finite differences or Fourier [spectral methods](/spectral-methods/) in space. The equations are stiff, because the gradient term is a diffusion with coefficient $M \varepsilon^2$ for Allen-Cahn and a fourth order term for Cahn-Hilliard, so time stepping treats the linear part implicitly, for example by semi-implicit Fourier steps or [Crank-Nicolson](/crank-nicolson-method/), and the nonlinear part explicitly or by a convex splitting. The grid must resolve the interface with a few points per $\varepsilon$.

## What it counts

The model predicts the position and the shape of the interfaces as functions of time: the speed of a front, the radius of a shrinking grain, the growth rate and the tip radius of a dendrite, the length scale of a pattern of phase separation and its coarsening in time. It also gives the free energy of a configuration, which decreases in time.

## Relation to other models

- **Sharp interface models.** As $\varepsilon \to 0$, the Allen-Cahn interface moves by mean curvature (Known result 4), and the Cahn-Hilliard interface obeys a Mullins-Sekerka free boundary problem (formal asymptotics, not proved here). Solidification models reduce to the Stefan problem with the Gibbs-Thomson condition at the interface. The phase-field model is a regularization of these sharp interface problems.
- **Level set.** The [level set method](/level-set-method/) also represents the interface implicitly, by the zero set of a function, but the function has no physical meaning away from the interface and the speed of the interface must be given. In the phase-field model, the speed follows from the energy.
- **Volume of fluid and front tracking.** The [volume of fluid method](/volume-of-fluid-method/) carries the fraction of one phase per cell, and [front tracking](/front-tracking-method/) carries the interface as a mesh. Both keep the interface sharp. The phase field has a finite width, which costs grid points but makes topology changes automatic.
- **Two-phase flow.** Coupling Cahn-Hilliard to the [Navier-Stokes equations](/navier-stokes-equations/), with the capillary force $-u \nabla \mu$ or $\mu \nabla u$ added to the momentum equation, gives a diffuse interface model of two immiscible fluids with surface tension.
- **Fracture and microstructure.** The same construction, an order parameter with a gradient energy, is used for fracture (the order parameter is the damage), for grain growth with many order parameters, and for martensitic transformations with an elastic energy added.

## Known results in the model

**Known result 1 (energy decreases).** With periodic or no-flux boundary conditions, smooth solutions satisfy
$$\frac{d \mathcal{F}}{dt} = -\int M \mu^2\, dx \le 0 \quad \text{(Allen-Cahn)}, \qquad \frac{d \mathcal{F}}{dt} = -\int M |\nabla \mu|^2\, dx \le 0 \quad \text{(Cahn-Hilliard)}.$$

*Proof.* $\frac{d \mathcal{F}}{dt} = \int (\varepsilon^2 \nabla u \cdot \nabla \partial_t u + W'(u) \partial_t u)\, dx = \int \mu\, \partial_t u\, dx$ after an integration by parts, whose boundary term is zero. For Allen-Cahn, $\partial_t u = -M \mu$. For Cahn-Hilliard, $\int \mu \nabla \cdot (M \nabla \mu)\, dx = -\int M |\nabla \mu|^2\, dx$ by one more integration by parts. $\square$

**Known result 2 (conservation and bounds).** Cahn-Hilliard conserves the mass $\int u\, dx$, because $\partial_t u$ is a divergence with zero flux through the boundary. Allen-Cahn does not conserve it, but it keeps $|u| \le 1$ if $|u| \le 1$ at the start, by the maximum principle: at a point where $u$ has a new maximum above $1$, $\Delta u \le 0$ and $-W'(u) = u - u^3 < 0$, so $u$ cannot grow. Cahn-Hilliard has no maximum principle, and $u$ can leave $[-1, 1]$ slightly.

**Known result 3 (the flat interface).** In one dimension, $u(x) = \tanh\big( x / (\sqrt 2\, \varepsilon) \big)$ is a stationary solution of both equations that joins $-1$ to $+1$, and its excess energy, the interface energy, is
$$\sigma = \int_{-\infty}^{\infty} \Big( \frac{\varepsilon^2}{2} u'^2 + W(u) \Big) dx = \frac{2 \sqrt 2}{3}\, \varepsilon = 0.942809\, \varepsilon .$$

*Proof.* With $u' = (1 - u^2) / (\sqrt 2 \varepsilon)$, $u'' = -2 u u' / (\sqrt 2 \varepsilon) = -u (1 - u^2) / \varepsilon^2$, so $\varepsilon^2 u'' = u^3 - u = W'(u)$ and $\mu = 0$. The profile also satisfies $\frac{\varepsilon^2}{2} u'^2 = \frac14 (1 - u^2)^2 = W(u)$, so the energy density is $2 W(u) = \varepsilon u' \sqrt{2 W(u)}$, and $\sigma = \int_{-1}^{1} \varepsilon \sqrt{2 W(u)}\, du = \varepsilon \int_{-1}^{1} \frac{1 - u^2}{\sqrt 2}\, du = \frac{\varepsilon}{\sqrt 2} \cdot \frac43$. $\square$

*Check by hand.* The profile passes from $u = -0.9$ to $u = 0.9$ over the width $2 \sqrt 2\, \varepsilon\, \operatorname{artanh}(0.9) = 4.164\, \varepsilon$. A midpoint sum of the energy density with $\varepsilon = 1$ over $[-20, 20]$ gives $0.942809$.

**Known result 4 (motion by mean curvature).** For Allen-Cahn with $M = 1 / \varepsilon^2$, that is $\partial_t u = \Delta u - W'(u) / \varepsilon^2$, the interface moves, as $\varepsilon \to 0$, with normal speed equal to its mean curvature (the sum of the principal curvatures), toward its center of curvature. Evans, Soner and Souganidis (1992) proved the convergence to the level set solution of motion by mean curvature, for all times, including after singularities. With a general $M$ the speed is $M \varepsilon^2$ times the curvature.

*Check by hand.* A circle of radius $R$ in two dimensions has curvature $1 / R$, so $dR / dt = -1 / R$ and $R(t)^2 = R_0^2 - 2 t$. A disk of radius $1$ disappears at $t = 1/2$; in three dimensions a ball has curvature $2 / R$ and disappears at $t = R_0^2 / 4$.

**Known result 5 (spinodal decomposition).** Linearize Cahn-Hilliard with a constant $M$ about a uniform state $u_0$: a perturbation $e^{i k \cdot x + s t}$ grows at the rate
$$s(k) = -M |k|^2 \big( W''(u_0) + \varepsilon^2 |k|^2 \big), \qquad W''(u_0) = 3 u_0^2 - 1 .$$
So the uniform state is unstable if and only if $W''(u_0) < 0$, that is $|u_0| < 1 / \sqrt 3 = 0.577350$ (the spinodal region), and then the waves with $0 < |k| < \sqrt{-W''(u_0)} / \varepsilon$ grow. The fastest one has $|k|^2 = -W''(u_0) / (2 \varepsilon^2)$ and the rate $M W''(u_0)^2 / (4 \varepsilon^2)$, which sets the length scale of the first pattern. For $u_0 = 0$: $|k| = 1 / (\sqrt 2 \varepsilon)$ and $s = M / (4 \varepsilon^2)$.

*Proof.* Put $u = u_0 + v$ with small $v$; then $\mu \approx W'(u_0) + W''(u_0) v - \varepsilon^2 \Delta v$ and $\partial_t v = M \Delta (W''(u_0) v - \varepsilon^2 \Delta v)$. A Fourier mode gives $s = M (-|k|^2)(W''(u_0) + \varepsilon^2 |k|^2)$. The maximum over $|k|^2$ is where $-W''(u_0) - 2 \varepsilon^2 |k|^2 = 0$. $\square$

**Known result 6 (time step of explicit schemes).** Forward Euler for Allen-Cahn on a grid of spacing $\Delta x$ in $d$ dimensions needs $\Delta t \le \Delta x^2 / (2 d M \varepsilon^2)$ for the diffusion part, as for the [heat equation](/heat-equation/), and Cahn-Hilliard needs $\Delta t = O(\Delta x^4)$. This is why the linear part is treated implicitly.

## References
