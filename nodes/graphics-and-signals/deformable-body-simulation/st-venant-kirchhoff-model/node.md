---
tag: H0C71P
kind: model
slug: st-venant-kirchhoff-model
name: St. Venant-Kirchhoff model
aliases:
- StVK material
- Saint Venant-Kirchhoff material
area: graphics-and-signals/deformable-body-simulation
level: core
summary: "A hyperelastic model with an energy quadratic in the Green strain. Rotations give no stress, but its resistance to strong compression weakens and then reverses."
prereqs: [hyperelastic-material]
see_also: [neo-hookean-model, stable-neo-hookean, corotational-fem, invertible-finite-elements, modal-reduction, brittle-fracture, deformation-gradient, finite-element-method]
sources:
  - paper: doi:10.1145/2343483.2343501
    title: Eftychios Sifakis and Jernej Barbič, FEM simulation of 3D deformable solids, a practitioner's guide to theory, discretization and model reduction, SIGGRAPH 2012 Courses, article 20
    locator: the St. Venant-Kirchhoff energy and its first Piola-Kirchhoff stress, and its behavior under compression (general locator)
  - paper: "Javier Bonet and Richard D. Wood, Nonlinear Continuum Mechanics for Finite Element Analysis, second edition, Cambridge University Press, 2008"
    locator: the chapter on hyperelasticity, with the Green strain and the second Piola-Kirchhoff stress (general locator)
  - paper: doi:10.1145/1073204.1073300
    title: Jernej Barbič and Doug L. James, Real-time subspace integration for St. Venant-Kirchhoff deformable models, ACM Transactions on Graphics 24(3), SIGGRAPH 2005, 982 to 990
    locator: the StVK internal forces as cubic polynomials of the reduced coordinates (general locator)
---

The St. Venant-Kirchhoff (StVK) model is the simplest [hyperelastic](/hyperelastic-material/) model that is correct under rotation.
It takes the energy of linear elasticity and puts the Green strain $E = \frac12(F^TF - I)$ in the place of the small strain:

$$\Psi(F) = \mu\lvert E\rvert_F^2 + \frac\lambda2(\operatorname{tr}E)^2, \qquad S = 2\mu E + \lambda\operatorname{tr}(E)I, \qquad P = FS.$$

Because $E$ is zero for every rotation, a turned body has no stress, which fixes the main defect of linear elasticity.
The energy is a polynomial of degree 4 in $F$, so the forces are cubic in the vertex positions, and this makes the model popular for [modal reduction](/modal-reduction/) and [brittle fracture](/brittle-fracture/).
Its weakness is strong compression: the restoring force has a largest value, falls to zero when an element is flat, and then pushes the element toward its mirror image.

## The machine

**State and parameters.** The input is a [deformation gradient](/deformation-gradient/) $F$, a $d \times d$ matrix with $d = 2$ or 3, and the two Lamé parameters $\mu > 0$ and $\lambda \ge 0$.
They come from Young's modulus $E_Y$ and Poisson's ratio $\nu$ by $\mu = E_Y/(2(1 + \nu))$ and $\lambda = E_Y\nu/((1 + \nu)(1 - 2\nu))$; for $E_Y = 1$ and $\nu = 0.3$, $\mu = 0.384615$ and $\lambda = 0.576923$.

**Energy and stress.** The formulas above give the energy per unit rest volume $\Psi$, the symmetric second Piola-Kirchhoff stress $S$, and the first Piola-Kirchhoff stress $P = \partial\Psi/\partial F$, the force per unit rest area.
$P = FS$ is the exact derivative for every $F$, also for flat and inverted elements; the model never divides by $\det F$.

**Forces of a linear element.** With the rest edge matrix $D_m$, the rest volume $V_0$ and $F = D_sD_m^{-1}$, the forces on the vertices 1 to $d$ are the columns of $-V_0PD_m^{-T}$, and vertex 0 gets minus their sum.
These are the exact gradient of $-V_0\Psi(F)$.
Each component of $F$ is linear in the vertex positions, $E$ is quadratic and $P$ is cubic, so the forces of a whole mesh are a cubic polynomial in the positions.

**The bar.** For a bar that is stretched along $x$ and cannot change its width, $F = \operatorname{diag}(s, 1, 1)$, and
$$\Psi = \Bigl(\mu + \frac\lambda2\Bigr)\frac{(s^2 - 1)^2}4, \qquad P_{xx} = \frac{2\mu + \lambda}2(s^3 - s).$$

## What it counts

$\Psi$ is the energy that a unit of rest volume stores; its integral over the rest shape is the elastic energy of the body.
The model counts only the change of lengths and angles, through $C = F^TF$, so it counts nothing for rotations and translations.
It also counts nothing for reflections: $\Psi(\operatorname{diag}(-1, 1, 1)) = 0$, so a mirror image of an element has the same zero energy as its rest shape.

**Example.** The bar with $E_Y = 1$ and $\nu = 0.3$, so $\mu + \lambda/2 = 0.673077$ and $2\mu + \lambda = 1.346154$.
The last column is the stress $(2\mu + \lambda)(s - 1)$ of linear elasticity for the same bar.

| $s$ | $\Psi$ | $P_{xx}$ | $P_{yy}$ | linear $P_{xx}$ |
|---|---|---|---|---|
| 1.5 | 0.262921 | 1.262019 | 0.360577 | 0.673077 |
| 1.2 | 0.032577 | 0.355385 | 0.126923 | 0.269231 |
| 1.0 | 0 | 0 | 0 | 0 |
| 0.8 | 0.021808 | $-0.193846$ | $-0.103846$ | $-0.269231$ |
| 0.577350 | 0.074786 | $-0.259067$ | $-0.192308$ | $-0.568952$ |
| 0.3 | 0.139344 | $-0.183750$ | $-0.262500$ | $-0.942308$ |
| 0 | 0.168269 | 0 | $-0.288462$ | $-1.346154$ |
| $-0.5$ | 0.094651 | 0.252404 | $-0.216346$ | $-2.019231$ |
| $-1.0$ | 0 | 0 | 0 | $-2.692308$ |

Under tension StVK is stiffer than linear elasticity.
Under compression the stress has its largest size, 0.259067, at $s = 1/\sqrt3 = 0.577350$, falls to zero at $s = 0$, and changes sign for $-1 < s < 0$.
In that range the force pushes the bar toward $s = -1$, the mirror image, which has zero energy.
The energy at the flat state $s = 0$ is only 0.168269, so a moderate load can push an element through it.

## Relation to other models

- **Linear elasticity.** StVK has the same energy with $E$ in the place of the small strain $\frac12(H + H^T)$, $H = F - I$. The two agree at first order near rest, but linear elasticity gives a stress for a pure rotation and StVK does not.
- **[Corotational FEM](/corotational-fem/).** It also removes rotations, but by the polar factor $R$ of each element, and then applies linear elasticity to $R^TF$. Its forces are not polynomial, and for the bar with $0 < s < 1$ its stress is the linear one, with no reversal.
- **[Neo-Hookean model](/neo-hookean-model/).** It adds a $\log J$ term, so the energy grows without bound as an element becomes flat. It is a better model of rubber under large compression, but it is undefined for $J \le 0$.
- **[Stable neo-Hookean model](/stable-neo-hookean/).** It keeps a finite energy at $J \le 0$ and a force that pushes toward $J > 0$.
- **[Invertible finite elements](/invertible-finite-elements/).** They take any isotropic model, StVK included, and change the energy for inverted elements, so that the force pushes them back.
- **[Modal reduction](/modal-reduction/) and [brittle fracture](/brittle-fracture/).** Barbič and James use the cubic StVK forces to precompute the reduced forces, and O'Brien and Hodgins use the Green strain with a linear stress, which is StVK.

## Known results in the model

- **Exact gradient (proved).** $P = FS$ is $\partial\Psi/\partial F$ for every $F$, and the element forces are minus the gradient of the element energy. See the [proof](proofs/correctness.md), Steps 1 and 2.
- **Objective and isotropic (proved).** $\Psi(QF) = \Psi(FQ) = \Psi(F)$ for every rotation $Q$, and $PF^T$ is symmetric. Proof, Step 3.
- **Rest states (proved).** $P = 0$ and $\Psi = 0$ exactly when $F^TF = I$, which includes every rotation and every reflection. Proof, Step 4.
- **Linear limit (proved).** $P(I + \varepsilon H) = \varepsilon(2\mu\operatorname{sym}H + \lambda\operatorname{tr}(H)I) + O(\varepsilon^2)$, so $\mu$ and $\lambda$ are the Lamé parameters without a remap. Proof, Step 5.
- **Weak compression (proved).** In the bar the compressive stress has its largest size $(2\mu + \lambda)/(3\sqrt3)$ at $s = 1/\sqrt3$, is zero at $s = 0$, and for $-1 < s < 0$ pushes toward the mirror image. Proof, Step 6.
- **Not convex (proved).** $d^2\Psi/ds^2 < 0$ for $\lvert s\rvert < 1/\sqrt3$ in the bar, so $\Psi$ is not convex in $F$, and Newton steps need a fix of the stiffness, such as projecting it to be positive semidefinite. The fix is a heuristic.
- **Use in practice (heuristic).** StVK works well when the strains stay moderate, such as stiff objects, cloth in its plane and reduced models. When elements can be strongly compressed, simulators use a model with a barrier or an inversion fix instead.

## References
