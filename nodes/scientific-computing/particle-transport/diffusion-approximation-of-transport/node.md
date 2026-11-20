---
tag: P2WTRA
kind: model
slug: diffusion-approximation-of-transport
name: Diffusion approximation of transport
aliases:
- P1 approximation
- neutron diffusion equation
area: scientific-computing/particle-transport
level: intro
summary: "Approximates transport by a diffusion equation for the scalar flux, valid when scattering dominates and the flux is nearly isotropic."
model: real-ram
prereqs: [linear-boltzmann-transport-equation, heat-equation]
see_also: [spherical-harmonics-method, diffusion-synthetic-acceleration, k-eigenvalue-problem, discrete-ordinates-method, multigroup-approximation, finite-volume-method, thomas-algorithm, poisson-equation]
sources:
  - book: isbn:9780471092452
    title: E. E. Lewis and W. F. Miller, Jr., Computational Methods of Neutron Transport, Wiley, 1984
    locator: the sections on the P1 equations, the diffusion approximation and its boundary conditions
  - book: isbn:9780471223634
    title: J. J. Duderstadt and L. J. Hamilton, Nuclear Reactor Analysis, Wiley, 1976
    locator: the chapters on one-speed diffusion theory, the extrapolated boundary and the criticality of bare reactors
  - paper: doi:10.1063/1.1666510
    title: E. W. Larsen and J. B. Keller, Asymptotic solution of neutron transport problems for small mean free paths, Journal of Mathematical Physics 15(1), 1974, 75-81
    locator: the asymptotic limit in which the transport solution tends to the solution of a diffusion equation, with boundary layers
  - paper: "R. E. Marshak, Note on the spherical harmonic method as applied to the Milne problem for a sphere, Physical Review 71, 1947, 443-446"
    locator: the boundary conditions on half-range moments for the spherical harmonics equations
  - paper: doi:10.1016/S0149-1970(01)00023-3
    title: Marvin L. Adams and Edward W. Larsen, Fast iterative methods for discrete-ordinates particle transport calculations, Progress in Nuclear Energy 40(1), 2002, 3-159
    locator: the role of the diffusion limit in the analysis of source iteration and of diffusion synthetic acceleration
---

The diffusion approximation replaces the [transport equation](/linear-boltzmann-transport-equation/) for the angular flux $\psi(x, \Omega)$ by a diffusion equation for the scalar flux $\phi(x)$ alone. Particles are assumed to move nearly the same amount in all directions, so the net current is proportional to the gradient of the flux (Fick's law), with the diffusion coefficient $D = 1/(3\Sigma_{tr})$. The result is the steady [heat equation](/heat-equation/) with absorption, $-\nabla\cdot D\nabla\phi + \Sigma_a\phi = q$. It is exact in an infinite homogeneous medium, accurate in large media where scattering dominates, and wrong within a few mean free paths of a boundary, a source or a strong absorber. Reactor core design in two energy groups, the low-order operator of [diffusion synthetic acceleration](/diffusion-synthetic-acceleration/) and radiative heat transfer in optically thick matter all use it. It is the lowest order of the [spherical harmonics method](/spherical-harmonics-method/).

## The machine

**Unknowns.** The scalar flux $\phi(x) = \int \psi(x, \Omega)\, d\Omega$ and the current $J(x) = \int \Omega\, \psi(x, \Omega)\, d\Omega$. In a slab with $\mu$ the cosine of the direction, $\phi = \int_{-1}^{1}\psi\, d\mu$ and $J = \int_{-1}^{1}\mu\,\psi\, d\mu$.

**Equations.** The balance and Fick's law,
$$\nabla\cdot J + \Sigma_a\,\phi = q, \qquad J = -D\,\nabla\phi, \qquad D = \frac{1}{3\Sigma_{tr}}, \quad \Sigma_{tr} = \Sigma_t - \bar\mu_0\,\Sigma_s,$$
so $-\nabla\cdot(D\nabla\phi) + \Sigma_a\phi = q$. Here $\Sigma_a = \Sigma_t - \Sigma_s$ is the absorption cross section, $\bar\mu_0$ is the mean cosine of the scattering angle, and $q$ is the isotropic source. For a [k-eigenvalue problem](/k-eigenvalue-problem/), $q = \nu\Sigma_f\phi/k$.

**Derivation from transport.** Take the slab equation $\mu\,\partial_x\psi + \Sigma_t\psi = (\Sigma_s\phi + 3\bar\mu_0\Sigma_s\mu J + q)/2$, with scattering that is linearly anisotropic. Integrate it over $\mu$ to get the balance $J' + \Sigma_a\phi = q$. Multiply it by $\mu$ and integrate to get $\frac{d}{dx}\int\mu^2\psi\, d\mu + \Sigma_t J = \bar\mu_0\Sigma_s J$. The $P_1$ closure takes $\psi$ linear in $\mu$, $\psi = (\phi + 3\mu J)/2$, which gives $\int\mu^2\psi\, d\mu = \phi/3$ and so $J = -\phi'/(3\Sigma_{tr})$. This is a theorem about the $P_1$ equations; the approximation is the closure itself.

**Boundary conditions.** A vacuum face has no incoming particles, but diffusion has only one condition per face, so it must approximate this:

- **Zero flux** at the face: simple, too low, since the true flux does not vanish there.
- **Marshak**: the incoming partial current $J^- = \phi/4 - J/2$ is zero, that is $J_{\mathrm{out}} = \phi/2$ (with the convention $\phi = \int\psi\, d\mu$). In the linear form this is the zero flux at the extrapolated distance $2D$ outside the face.
- **Milne extrapolation**: zero flux at the distance $0.7104/\Sigma_t$ outside the face, the value from the exact solution of the half-space (Milne) problem with $c = 1$ and isotropic scattering. Codes often use $0.7104/\Sigma_{tr}$ for anisotropic scattering, which is a rule of thumb.
- **Reflection**: $J = 0$.

At an interface between materials, $\phi$ and the normal current $D\,\partial_n\phi$ are continuous.

**Discretization.** The implementation uses cell-centered finite volumes ([finite volume method](/finite-volume-method/)) in a slab. The current through the face between cells $j$ and $j + 1$ is $(\phi_j - \phi_{j+1})/R$ with $R = \Delta x_j/(2D_j) + \Delta x_{j+1}/(2D_{j+1})$, a boundary face adds the resistance of its condition, and the tridiagonal system is solved by the [Thomas algorithm](/thomas-algorithm/). The $k$ value comes from [power iteration](/power-iteration/) on the fission source.

## What it counts

The model predicts the scalar flux, the reaction rates $\Sigma_x\phi$ and the currents, but not the angular distribution. It cannot represent a beam, a void, or the flux near a face. Its errors are measured against transport solutions or experiments.

The cost model is the [real RAM](/real-ram/), counting operations per cell. A diffusion solve has one unknown per cell, where a discrete ordinates solve has $N$ unknowns per cell and needs many sweeps. In a slab of $M$ cells the system is tridiagonal and costs $O(M)$ operations; in two and three dimensions it is a sparse symmetric positive definite system, solved by conjugate gradients or by the [multigrid method](/multigrid-method/) in close to $O(M)$ operations. A $k$-eigenvalue problem costs one solve per power iteration.

## Relation to other models

- **Transport.** The [linear Boltzmann transport equation](/linear-boltzmann-transport-equation/) is the exact one-particle model; diffusion is its $P_1$ truncation. In an infinite homogeneous medium with a uniform source, both give $\phi = q/\Sigma_a$.
- **The diffusion limit.** If $\Sigma_t$ is scaled by $1/\varepsilon$, and $\Sigma_a$ and $q$ by $\varepsilon$, the transport solution tends to the solution of the diffusion equation as $\varepsilon \to 0$, away from boundary layers of a few mean free paths (Larsen and Keller 1974; a theorem of asymptotic analysis). Spatial schemes that keep this limit on cells many mean free paths thick, such as linear discontinuous finite elements, are said to have the thick diffusion limit; Adams and Larsen (2002) review which schemes have it.
- **$P_N$ and $SP_N$.** The [spherical harmonics method](/spherical-harmonics-method/) keeps more moments. $P_1$ in steady state is diffusion; time dependent $P_1$ is a telegraph equation with a finite signal speed, while time dependent diffusion has an infinite one. The simplified $SP_N$ equations replace the one-dimensional derivatives of slab $P_N$ by gradients, which gives coupled diffusion equations.
- **Discrete ordinates.** In a thick diffusive medium the slow modes of [source iteration](/source-iteration/) are the smooth solutions of the diffusion equation, which is why [diffusion synthetic acceleration](/diffusion-synthetic-acceleration/) removes them.
- **Energy.** With the [multigroup approximation](/multigroup-approximation/), each group has its own $D_g$ and $\Sigma_{a,g}$, and the groups are coupled by scattering and fission. Two-group diffusion is the classical model of a thermal reactor.

## Known results in the model

**Fick's law from $P_1$ (theorem).** If $\psi$ is linear in $\mu$ and the scattering is at most linearly anisotropic, the first moment equation is exactly $J = -D\phi'$ with $D = 1/(3\Sigma_{tr})$ (the derivation above).

**The infinite medium (theorem).** With reflecting faces, $\Sigma_a = 0.1$, $D = 1/3$ and $q = 1$, the discrete solution is $\phi = 10$ in every cell, the value $q/\Sigma_a$ of transport.

**The bare slab (theorem and measurement).** A homogeneous slab with $\Sigma_t = 1$, $\Sigma_a = 0.1$, $\nu\Sigma_f = 0.12$ and width $L = 20$ cm has $k_\infty = 1.2$ and, with $\phi = 0$ at the faces, $k = \nu\Sigma_f/(\Sigma_a + D(\pi/L)^2) = 1.108804$. The finite volume $k$ is $1.1089776$, $1.1088478$, $1.1088153$ and $1.1088072$ with 20, 40, 80 and 160 cells, so the error falls by 4 per halving of the cells, which is second order. The boundary condition matters more than the mesh:

| face condition | width used for the buckling | $k$ |
|---|---|---|
| zero flux at the face | 20 | 1.108804 |
| Marshak, $2D$ outside | 21.3333 | 1.119103 |
| Milne, $0.7104$ outside | 21.4208 | 1.119719 |
| transport, $S_{16}$ with 320 cells | | 1.120062 |

The transport value is the measurement of the [k-eigenvalue problem](/k-eigenvalue-problem/) page. The Milne distance gives $k$ within $3.5 \times 10^{-4}$ of transport, and the zero flux condition is 1% low.

**A slab with a source (measurement).** Take $\Sigma_t = 1$, $c = 0.9$ ($\Sigma_a = 0.1$), $q = 1$ and vacuum faces. Diffusion with Marshak faces has an exact solution, and the transport values come from $S_{16}$ with diamond difference on 200 cells:

| width (mean free paths) | leakage per face, diffusion | leakage per face, transport | center flux, diffusion | center flux, transport |
|---|---|---|---|---|
| 2 | 0.770383 | 0.743626 | 2.668293 | 3.009311 |
| 10 | 1.329219 | 1.296145 | 9.054542 | 9.038785 |
| 40 | 1.337394 | 1.305766 | 9.999744 | 9.999639 |

In the thick slabs the center agrees to $2 \times 10^{-3}$ and better, and the leakage is about 2.5% high. In the thin slab of 2 mean free paths the center flux is 11% low, because most of the slab is boundary layer.

**The decay length (theorem).** In a source-free medium the flux far from sources decays like $e^{-\kappa\Sigma_t x}$. Diffusion gives $\kappa^2 = 3(1 - c)$, and exact one-speed transport gives the root of $c\,\mathrm{artanh}(\kappa)/\kappa = 1$. Both agree to first order in $1 - c$:

| $c$ | diffusion $\kappa$ | transport $\kappa$ | ratio |
|---|---|---|---|
| 0.5 | 1.224745 | 0.957504 | 1.2791 |
| 0.9 | 0.547723 | 0.525430 | 1.0424 |
| 0.99 | 0.173205 | 0.172511 | 1.0040 |
| 0.999 | 0.054772 | 0.054750 | 1.0004 |

So diffusion describes the flux well only when $c$ is near 1, that is when particles scatter many times before they are absorbed.

**The diffusion limit (measurement).** In a slab of width 1 with $\Sigma_t = 1/\varepsilon$, $\Sigma_a = \varepsilon$, $q = \varepsilon$ and vacuum faces, the center flux of $S_8$ with 300 cells and of diffusion with Marshak faces is $0.344242$ and $0.338627$ for $\varepsilon = 0.1$, $0.303371$ and $0.302126$ for $\varepsilon = 0.03$, and $0.291312$ and $0.290945$ for $\varepsilon = 0.01$. The gap shrinks as $\varepsilon \to 0$, as the theorem of Larsen and Keller predicts.

**Rules of thumb.** Diffusion is accurate more than about two or three mean free paths from boundaries, sources and strong absorbers, and when the absorption is small compared with the scattering. These are rules of thumb from reactor physics, not theorems; the tables above show their size in one-speed slabs.

## References
