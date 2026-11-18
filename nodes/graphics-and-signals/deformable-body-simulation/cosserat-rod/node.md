---
tag: 914ZMF
kind: model
slug: cosserat-rod
name: Cosserat rod
aliases:
- Cosserat rod model
area: graphics-and-signals/deformable-body-simulation
level: advanced
summary: "A rod model with a centerline and an orthonormal frame at each point. Its six strains measure stretch, shear, bending and twist, and do not change under rigid motions."
prereqs: [hyperelastic-material, special-orthogonal-group]
see_also: [discrete-elastic-rods, frenet-frame, rotation-minimizing-frame, unit-quaternion-rotation, elastically-deformable-models, position-based-dynamics, mass-spring-system, finite-element-method]
sources:
  - paper: "Stuart S. Antman, Nonlinear Problems of Elasticity, second edition, Springer, 2005"
    locator: the chapter on the special Cosserat theory of rods, with the strains, the balance laws and the constitutive laws (general locator)
  - paper: doi:10.2312/SCA/SCA07/063-072
    title: Jonas Spillmann and Matthias Teschner, CoRdE, Cosserat rod elements for the dynamic simulation of one-dimensional elastic objects, Symposium on Computer Animation 2007, 63 to 72
    locator: continuous rod energies from the Cosserat theory, discretized per element with finite elements (general locator)
  - paper: doi:10.1145/1360612.1360662
    title: Miklós Bergou, Max Wardetzky, Stephen Robinson, Basile Audoly and Eitan Grinspun, Discrete elastic rods, ACM Transactions on Graphics 27(3), article 63, 2008
    locator: the Kirchhoff rod with an isotropic cross section, whose bending energy depends on the curvature and whose twist is measured against a reference frame (general locator)
---

A Cosserat rod is a model of a thin elastic body, such as a hair, a cable or a rope, as a curve that carries an orthonormal frame at each point.
For the arc length $s$ of the rest rod, the centerline is $r(s) \in \mathbb R^3$ and the frame is a rotation $Q(s) = [d_1\ d_2\ d_3]$ in [SO(3)](/special-orthogonal-group/), whose columns are the *directors*.
The director $d_3$ follows the rod, and $d_1$, $d_2$ span the cross section.
The rod has six strains at each point,
$$v = Q^Tr', \qquad [u]_\times = Q^TQ',$$
where $'$ is $d/ds$ and $[u]_\times$ is the skew matrix of the cross product with $u$.
$v$ measures stretch ($v_3$) and shear ($v_1$, $v_2$); $u$ measures bending ($u_1$, $u_2$) and twist ($u_3$).

## The machine

**State.** A curve $r$ and a frame $Q$ on $[0, L]$, so six degrees of freedom per point: three for the position and three for the rotation of the cross section.
The frame is free: $d_3$ need not be the tangent of $r$.
A [unit quaternion](/unit-quaternion-rotation/) per point is a common way to store $Q$, because it stays a rotation after normalization (heuristic).

**Strains in the frame.** $v = Q^Tr'$ are the components of the tangent in the frame, and $u$ are the components of the Darboux vector $\omega$, the rate at which the frame turns with $s$: $d_i' = \omega\times d_i$ with $\omega = Qu$.
The rest shape has its own strains $\hat v$, $\hat u$; a straight rod at rest has $\hat v = (0, 0, 1)$ and $\hat u = 0$.

**Energy.** A [hyperelastic](/hyperelastic-material/) rod has a stored energy $W = \int_0^LG(v, u, s)\,ds$.
The usual choice is quadratic,
$$G = \frac12(v - \hat v)^TS(v - \hat v) + \frac12(u - \hat u)^TB(u - \hat u),$$
with $S = \operatorname{diag}(k_1GA, k_2GA, EA)$ for shear and stretch, and $B = \operatorname{diag}(EI_1, EI_2, GJ)$ for bending and twist, where $E$ and $G$ are Young's modulus and the shear modulus, $A$ the area, $I_1$, $I_2$ the second moments of area, $J$ the torsion constant and $k_1$, $k_2$ shear factors of the cross section.

**Balance laws.** The resultant force $n(s)$ and moment $m(s)$ on the cross section satisfy, for a static rod with the distributed force $f$ and moment $l$,
$$n' + f = 0, \qquad m' + r'\times n + l = 0,$$
and for the quadratic energy $n = QS(v - \hat v)$ and $m = QB(u - \hat u)$.
A dynamic rod adds the linear and angular inertia of the cross section to these equations.

## What it counts

$W$ counts how much each cross section has moved and turned relative to its neighbors, compared with the rest shape.
It counts nothing for a rigid motion of the whole rod.

**Example.** Strains of some rods, with $d_3$ along the tangent unless stated:

| rod | $v$ | $u$ |
|---|---|---|
| straight, stretched by 10% | $(0, 0, 1.1)$ | $0$ |
| straight, frame turning about $d_3$ at the rate $\theta'$ | $(0, 0, 1)$ | $(0, 0, \theta')$ |
| circle of radius $R$, $d_1$ toward the center, $d_2$ normal to the plane | $(0, 0, 1)$ | $(0, 1/R, 0)$ |
| helix $(\cos\frac s{\sqrt2}, \sin\frac s{\sqrt2}, \frac s{\sqrt2})$ with the [Frenet frame](/frenet-frame/) $d_1 = N$, $d_2 = B$ | $(0, 0, 1)$ | $(0, 0.5, 0.5)$ |
| straight along $e_3$, frame turned by the angle $\phi$ about $d_1$ | $(0, \sin\phi, \cos\phi)$ | $0$ |

The helix row is the curvature $\kappa = 0.5$ and the torsion $\tau = 0.5$ of that curve.
A rod of length $2\pi R$ bent into the circle has the energy $\frac12EI_2(1/R)^2\cdot2\pi R = \pi EI_2/R$.
The last row is pure shear: the tangent is not along $d_3$.

## Relation to other models

- **Kirchhoff rod.** The limit with no shear and no stretch, $v = (0, 0, 1)$, so $d_3 = r'$ and $\lvert r'\rvert = 1$. Then $n$ is no longer given by the strains; it is the force that keeps the constraint.
- **[Discrete elastic rods](/discrete-elastic-rods/).** Bergou et al. (2008) discretize the Kirchhoff rod with an isotropic cross section: a polyline for the centerline and one angle per edge for the frame, with the twist measured against a [rotation-minimizing](/rotation-minimizing-frame/) reference frame.
- **CoRdE.** Spillmann and Teschner (2007) discretize the Cosserat energies per element with finite elements, for interactive simulation of rods with torsion.
- **[Elastically deformable models](/elastically-deformable-models/).** Their curve energy uses the arc length, the curvature and the torsion of the centerline only, so it has no frame and no twist of the cross section.
- **[Mass-spring systems](/mass-spring-system/) and [position-based dynamics](/position-based-dynamics/).** Chains of particles model stretch and bending, but without a frame they have no twist.

## Known results in the model

- **Rigid motions cost nothing (proved).** For $r \mapsto Rr + c$ and $Q \mapsto RQ$ with a fixed rotation $R$, $v = Q^TR^TRr'$ and $Q^TR^TRQ'$ do not change, so $v$, $u$ and $W$ are the same.
- **Six strains determine the shape (proved).** Given $v(s)$, $u(s)$ and the frame and position at $s = 0$, the equations $Q' = Q[u]_\times$ and $r' = Qv$ are linear ordinary differential equations with a unique solution, so the strains fix the rod up to one rigid motion.
- **Constant strains give a helix (proved).** If $u$ and $v$ are constant, then $\omega = Qu$ has $\omega' = Q[u]_\times u = 0$, so the frame turns about the fixed axis $\omega$ at the constant rate $\lvert u\rvert$, and $r' = Qv$ turns with it. The centerline is a helix about that axis, or a circle or a straight line in the limit cases.
- **Isotropic bending sees only the curvature (proved).** In the Kirchhoff limit, where $\kappa > 0$, write $d_1 = \cos\theta N + \sin\theta B$ and $d_2 = -\sin\theta N + \cos\theta B$ with the Frenet frame. Then $\omega = \kappa B + (\tau + \theta')T$, so $u = (\kappa\sin\theta, \kappa\cos\theta, \tau + \theta')$. With $EI_1 = EI_2 = EI$ and $\hat u_1 = \hat u_2 = 0$, the bending energy is $\frac12EI\kappa^2$ for every $\theta$, and only the twist term depends on the frame.
- **Balance laws (law).** The equations for $n$ and $m$ are the balance of force and of moment on each piece of the rod.
- **A conserved moment (proved).** With no distributed loads, $n$ is constant and $(m + r\times n)' = m' + r'\times n = 0$, so $m + r\times n$ is constant along the rod.
- **Choice of stiffness (heuristic).** The quadratic energy with the moduli of the cross section is the linear theory of beams applied to each cross section. For large strains, or for a rope made of fibers, the stiffness values are a measurement for that material.

## References
