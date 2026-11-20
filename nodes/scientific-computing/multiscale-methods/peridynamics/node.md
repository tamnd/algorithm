---
tag: 98VS73
kind: model
slug: peridynamics
name: Peridynamics
area: scientific-computing/multiscale-methods
level: research
summary: A nonlocal continuum theory in which material points interact by bonds within a horizon, so cracks need no special treatment.
model: real-ram
history:
  year: 2000
  people: [Stewart A. Silling]
  note: Silling proposed the bond-based theory in 2000 to model cracks without spatial derivatives. Silling and Askari gave a meshfree discretization in 2005, Silling and coworkers the state-based theory in 2007, and Silling and Lehoucq proved convergence to classical elasticity in 2008.
prereqs: [hyperelastic-material, molecular-dynamics]
see_also: [brittle-fracture, mass-spring-system, extended-finite-element-method, material-point-method, smoothed-particle-hydrodynamics, quasicontinuum-method, cauchy-born-rule, multiscale-modeling]
sources:
  - paper: doi:10.1016/S0022-5096(99)00029-0
    title: S. A. Silling, Reformulation of elasticity theory for discontinuities and long-range forces, Journal of the Mechanics and Physics of Solids 48(1), 2000, 175-209
    locator: the bond-based equation of motion, the pairwise force function, the horizon, and the Poisson ratio of 1/4 of bond-based isotropic materials
  - paper: doi:10.1016/j.compstruc.2004.11.026
    title: S. A. Silling and E. Askari, A meshfree method based on the peridynamic model of solid mechanics, Computers and Structures 83(17-18), 2005, 1526-1535
    locator: the discretization by nodes with volumes, the explicit time integration and the bond breaking by a critical stretch (general locator)
  - paper: doi:10.1007/s10659-007-9125-1
    title: S. A. Silling, M. Epton, O. Weckner, J. Xu and E. Askari, Peridynamic states and constitutive modeling, Journal of Elasticity 88(2), 2007, 151-184
    locator: the state-based theory, which removes the restriction on the Poisson ratio
  - paper: doi:10.1007/s10659-008-9163-3
    title: S. A. Silling and R. B. Lehoucq, Convergence of peridynamics to classical elasticity theory, Journal of Elasticity 93(1), 2008, 13-37
    locator: the limit of a vanishing horizon for smooth deformations
  - book: isbn:9781461484646
    title: Erdogan Madenci and Erkan Oterkus, Peridynamic Theory and Its Applications, Springer, 2014
    locator: the bond-based and state-based theories, their discretization and applications to fracture (general locator)
---

Peridynamics is a model of solids in which each material point interacts with all points within a fixed distance $\delta$, the horizon, through bonds, instead of through the stress at the point. The equation of motion is an integral over the horizon, with no spatial derivatives of the displacement, so it stays valid where the displacement jumps, and a crack is a set of broken bonds that forms and grows by itself. In graphics terms, a discretized bond-based peridynamic solid is a [mass-spring system](/mass-spring-system/) in which every particle is linked to all particles within the radius $\delta$; what peridynamics adds to the graphics methods for [brittle fracture](/brittle-fracture/) is that the spring stiffness and the breaking stretch are derived from the measured elastic modulus and fracture energy, and the model converges to classical elasticity as $\delta \to 0$, so the crack paths follow from the mechanics and not from a rule for cutting the mesh.

## The machine

**Unknowns.** The displacement $u(x, t)$ of each point $x$ of a body $\Omega$ in its reference shape, with the mass density $\rho$ and a body force $b(x, t)$ per unit volume.

**Equation of motion (bond-based).** With the bond $\xi = x' - x$ and its relative displacement $\eta = u(x', t) - u(x, t)$,
$$\rho\, \ddot u(x, t) = \int_{H_x} f(\eta, \xi)\, dV_{x'} + b(x, t), \qquad H_x = \{x' \in \Omega : |x' - x| < \delta\}.$$
The pairwise force $f$ (a force per unit volume squared) satisfies $f(-\eta, -\xi) = -f(\eta, \xi)$, so linear momentum is conserved, and it is parallel to $\xi + \eta$, so angular momentum is conserved.

**The prototype microelastic brittle (PMB) material.** The bond stretch is $s = (|\xi + \eta| - |\xi|) / |\xi|$, and
$$f(\eta, \xi) = c\, s\, \mu(\xi, t)\, \frac{\xi + \eta}{|\xi + \eta|},$$
where $\mu = 1$ while the bond is intact and $\mu = 0$ for all later times once $s$ has exceeded the critical stretch $s_0$. Each bond is a spring with the energy $w = c\, s^2 |\xi| / 2$, and the energy density at a point is $W = \frac12 \int_{H_x} w\, dV$.

**Parameters.** The micromodulus $c$, the horizon $\delta$ and the critical stretch $s_0$. The horizon is a choice: a numerical length of a few grid spacings, or a physical length when the model must reproduce wave dispersion. The micromodulus is derived: for an isotropic expansion $s$ in three dimensions, $W = \frac{c s^2}{4} \int_0^\delta r \cdot 4 \pi r^2\, dr = \frac{\pi c\, s^2 \delta^4}{4}$, and matching the classical $W = \frac92 \kappa s^2$ for the bulk modulus $\kappa$ gives $c = 18 \kappa / (\pi \delta^4)$. The critical stretch is derived from the fracture energy $G_0$, the energy to break all bonds across a unit area of a plane: summing $w$ over the bonds that cross the plane gives $G_0 = \pi c\, s_0^2 \delta^5 / 10$, so $s_0 = \sqrt{5 G_0 / (9 \kappa \delta)}$. So $\kappa$ and $G_0$ are fitted to experiment, and $c$ and $s_0$ follow; the Poisson ratio is not free.

**State-based theory.** Silling and coworkers (2007) let the force on a bond depend on the deformation of all bonds of the point, through force states. This allows any Poisson ratio and plasticity models, and contains the bond-based theory as a special case.

**Discretization.** Silling and Askari (2005) replace the integral by a sum over nodes $x_j$ with volumes $V_j$ within the horizon, $\rho \ddot u_i = \sum_j f(u_j - u_i, x_j - x_i) V_j + b_i$, and integrate in time with an explicit scheme. There is no mesh and no element: a node is a particle, and the bonds are its springs. A step costs $O(N m)$ for $N$ nodes with $m$ nodes per horizon.

## What it counts

The model predicts the displacement field, the forces between points, and the damage: the fraction of broken bonds at each point, $\varphi(x) = 1 - \int_{H_x} \mu\, dV / \int_{H_x} dV$, which is near $1/2$ on the faces of a crack. From these follow the crack paths, branching, fragmentation, and the energy dissipated by fracture. It also predicts waves with dispersion, which classical elasticity does not have.

## Relation to other models

- **Classical elasticity.** For smooth deformations, the peridynamic equation converges to the equation of linear or nonlinear elasticity as $\delta \to 0$ (Silling and Lehoucq 2008). The one-dimensional calculation below shows the mechanism: the integral of the bond forces is a second difference over the horizon.
- **Molecular dynamics.** The equation has the form of [molecular dynamics](/molecular-dynamics/) with a pair potential of cutoff $\delta$, but the bonds join material points, not atoms, and the stiffness scales with $\delta$ so that the elastic constants do not change.
- **Mass-spring systems.** A [mass-spring system](/mass-spring-system/) with springs between nearest neighbors on a mesh has an elastic response that depends on the mesh. The peridynamic discretization has springs to all neighbors within $\delta$, with stiffness $c V_j$, and its response depends on $\delta$ but, for small grid spacing, not on the arrangement of the nodes.
- **Graphics fracture.** The [brittle fracture](/brittle-fracture/) method of O'Brien and Hodgins splits the stress of each element and cuts the mesh where a separation tensor exceeds the toughness. Peridynamics needs no stress and no remeshing: bonds break one at a time.
- **Other methods for cracks.** The [extended finite element method](/extended-finite-element-method/) adds discontinuous functions to the elements, which is accurate for one crack but needs a criterion for its growth. The [material point method](/material-point-method/) lets material separate on a background grid. [Smoothed particle hydrodynamics](/smoothed-particle-hydrodynamics/) is also a particle method with a kernel radius, but it approximates the derivatives of the classical equations.
- **Atomistic models.** Peridynamics with a horizon of a few lattice spacings is between atomistic models and a continuum, as are the [quasicontinuum method](/quasicontinuum-method/) and the [Cauchy-Born rule](/cauchy-born-rule/).

## Known results in the model

**Theorem 1 (the one-dimensional micromodulus).** Take a bar with the linear bond-based model $\rho \ddot u = \int_{-\delta}^{\delta} C\, (u(x + \xi) - u(x))\, d\xi$ with a constant $C$. For every polynomial $u$ of degree at most $3$, the integral equals $E u''(x)$ exactly if and only if $C = 3 E / \delta^3$. For smooth $u$ the error is $O(\delta^2)$.

*Proof.* By Taylor's formula, $u(x + \xi) - u(x) = u' \xi + u'' \xi^2 / 2 + u''' \xi^3 / 6 + O(\xi^4)$. The odd terms integrate to zero over $(-\delta, \delta)$, so the integral is $C u'' \int_{-\delta}^{\delta} \xi^2 / 2\, d\xi + O(C \delta^5) = C \delta^3 u'' / 3 + O(C \delta^5)$, with no remainder for degree at most $3$. This is $E u''$ if and only if $C = 3 E / \delta^3$, and then the remainder is $O(\delta^2)$. $\square$

*Check by hand.* For $u = x^2$, $u(x + \xi) - u(x) = 2 x \xi + \xi^2$, and $\int_{-\delta}^{\delta} C (2 x \xi + \xi^2)\, d\xi = 2 C \delta^3 / 3 = 2 E = E u''$.

**Theorem 2 (dispersion).** In the model of Theorem 1, a plane wave $u = e^{i (k x - \omega t)}$ solves the equation if and only if
$$\rho\, \omega^2 = 2 C \Big( \delta - \frac{\sin k \delta}{k} \Big) = E k^2 \cdot \frac{6 (k \delta - \sin k \delta)}{(k \delta)^3} = E k^2 \Big( 1 - \frac{(k \delta)^2}{20} + O((k \delta)^4) \Big).$$

*Proof.* Insert the wave: $\int_{-\delta}^{\delta} C (e^{i k \xi} - 1)\, d\xi = -2 C (\delta - \sin(k \delta) / k)$, and $\ddot u = -\omega^2 u$. The series follows from $\sin z = z - z^3 / 6 + z^5 / 120 - \dots$ and $C = 3E / \delta^3$. $\square$

So long waves ($k \delta \to 0$) travel at the classical speed $\sqrt{E / \rho}$, and short waves are slower. At $k \delta = 1$ the factor is $6 (1 - \sin 1) = 0.951174$, against $1 - 1/20 = 0.95$ from the series; at $k \delta = 2$ it is $0.818027$ against $0.8$. As $k \to \infty$, $\omega^2 \to 6 E / (\rho \delta^2)$, so the frequencies are bounded, unlike in classical elasticity. A physical horizon can be fitted to a measured dispersion curve.

**Theorem 3 (the Poisson ratio of bond-based models).** An isotropic bond-based material in three dimensions with small deformations has the Poisson ratio $1/4$ (Silling 2000). The reason is that pairwise central forces give elastic constants that satisfy the Cauchy relations, which for an isotropic material force the Lamé constants to be equal, $\lambda = \mu$, and $\nu = \lambda / (2 (\lambda + \mu)) = 1/4$. The state-based theory removes this restriction.

**Theorem 4 (convergence to elasticity).** Silling and Lehoucq (2008) proved that, for smooth deformations and a family of pairwise or state-based constitutive models scaled with the horizon, the peridynamic stress converges to a Piola-Kirchhoff stress and the equation of motion converges to that of classical elasticity as $\delta \to 0$. The proof is in that paper and is not repeated here. With cracks, the limit is a model of fracture in which the energy release rate is $G_0$; this is a statement about the calibration of $s_0$, not a theorem of convergence on this page.

**Theorem 5 (the bond energy and the fracture energy).** The values $c = 18 \kappa / (\pi \delta^4)$ and $G_0 = \pi c\, s_0^2 \delta^5 / 10$ above follow from the bond energy $w = c s^2 |\xi| / 2$. For the second, a point at distance $z < \delta$ below a plane has bonds of length $\xi \in (z, \delta)$ across the plane within the cone of half angle $\arccos(z / \xi)$, a solid angle of $2 \pi (1 - z / \xi)$. So
$$G_0 = \int_0^\delta \int_z^\delta \frac{c s_0^2 \xi}{2}\, 2 \pi \xi^2 \Big(1 - \frac{z}{\xi}\Big)\, d\xi\, dz = \pi c s_0^2 \int_0^\delta \Big( \xi^4 - \frac{\xi^4}{2} \Big) d\xi = \frac{\pi c s_0^2 \delta^5}{10},$$
where the order of integration was exchanged.

**Practice.** The discretized equation is solved with explicit time steps limited by the stiffest bonds, as in molecular dynamics. The damage near a crack and the crack path depend on the ratio of $\delta$ to the node spacing and on the arrangement of the nodes; convergence studies refine both (measurement, reported in the literature on the method, not a theorem).

## References
