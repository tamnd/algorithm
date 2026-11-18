---
tag: DY1W7J
kind: model
slug: neo-hookean-model
name: Neo-Hookean model
aliases:
- neo-Hookean material
- compressible neo-Hookean model
area: graphics-and-signals/deformable-body-simulation
level: core
summary: "A hyperelastic model with an energy in tr(F^T F) and log J. Its energy and its restoring force grow without bound as J goes to 0, and it is undefined for J ≤ 0."
prereqs: [hyperelastic-material]
see_also: [st-venant-kirchhoff-model, stable-neo-hookean, invertible-finite-elements, corotational-fem, deformation-gradient, optimization-time-integration, incremental-potential-contact, finite-element-method]
sources:
  - paper: "Javier Bonet and Richard D. Wood, Nonlinear Continuum Mechanics for Finite Element Analysis, second edition, Cambridge University Press, 2008"
    locator: the chapter on hyperelasticity, the compressible neo-Hookean material (general locator)
  - paper: doi:10.1145/2343483.2343501
    title: Eftychios Sifakis and Jernej Barbič, FEM simulation of 3D deformable solids, a practitioner's guide to theory, discretization and model reduction, SIGGRAPH 2012 Courses, article 20
    locator: the neo-Hookean energy and its first Piola-Kirchhoff stress among the isotropic models (general locator)
  - paper: doi:10.1145/3180491
    title: Breannan Smith, Fernando de Goes and Theodore Kim, Stable neo-Hookean flesh simulation, ACM Transactions on Graphics 37(2), article 12, 2018
    locator: the discussion of earlier neo-Hookean energies, their rest state and their behavior for J ≤ 0 (general locator)
---

The neo-Hookean model is a [hyperelastic](/hyperelastic-material/) model for rubber-like materials that adds a logarithmic term in the volume ratio $J = \det F$.
This page uses the compressible form of Bonet and Wood, which is common in graphics:

$$\Psi(F) = \frac\mu2(I_1 - 3) - \mu\log J + \frac\lambda2(\log J)^2, \qquad P = \mu(F - F^{-T}) + \lambda\log(J)F^{-T},$$

with $I_1 = \operatorname{tr}(F^TF)$; in 2D, $I_1 - 3$ becomes $I_1 - 2$.
The energy is zero for every rotation, and its linear limit has exactly the Lamé parameters $\mu$ and $\lambda$.
As an element is squeezed toward zero volume, the energy and the restoring force grow without bound.
The price is that $\Psi$ and $P$ are undefined for $J \le 0$, so a flat or inverted element stops the simulation unless a solver keeps $J > 0$ or the model is changed.

## The machine

**State and parameters.** The input is a [deformation gradient](/deformation-gradient/) $F$ with $J > 0$ and the Lamé parameters $\mu > 0$ and $\lambda \ge 0$, from Young's modulus $E_Y$ and Poisson's ratio $\nu$ by $\mu = E_Y/(2(1 + \nu))$ and $\lambda = E_Y\nu/((1 + \nu)(1 - 2\nu))$.
For $E_Y = 1$ and $\nu = 0.3$, $\mu = 0.384615$ and $\lambda = 0.576923$.

**The three terms.** $\frac\mu2(I_1 - 3)$ penalizes the change of the squared lengths, but it is not zero only for rotations: a uniform shrink lowers $I_1$ below 3.
$-\mu\log J$ cancels the stress $\mu I$ that the first term has at rest, so $P(I) = 0$.
$\frac\lambda2(\log J)^2$ penalizes the change of volume, and is the same for $J$ and $1/J$.

**Forces of a linear element.** With $F = D_sD_m^{-1}$ and the rest volume $V_0$, the forces on the vertices 1 to $d$ are the columns of $-V_0PD_m^{-T}$, and vertex 0 gets minus their sum.
A simulator computes $F^{-T}$ once per element and step, which needs $J \ne 0$.

## What it counts

$\Psi$ is the energy per unit rest volume.
It depends on $F$ only through $I_1$ and $J$, so it counts the change of lengths and of volume, and nothing for rotations and translations.
Unlike the [St. Venant-Kirchhoff model](/st-venant-kirchhoff-model/), it counts a mirror image as an infinite cost: there is no path of $F$ with $J > 0$ to it, and $\Psi$ has no value there.

**Example.** The bar $F = \operatorname{diag}(s, 1, 1)$, which cannot change its width, with $E_Y = 1$ and $\nu = 0.3$.
Here $\Psi = \frac\mu2(s^2 - 1) - \mu\log s + \frac\lambda2(\log s)^2$ and $P_{xx} = \mu(s - 1/s) + \lambda\log(s)/s$.

| $s$ | $\Psi$ | $P_{xx}$ | $P_{yy}$ | StVK $P_{xx}$ |
|---|---|---|---|---|
| 1.5 | 0.131860 | 0.476461 | 0.233922 | 1.262019 |
| 1.2 | 0.024081 | 0.228680 | 0.105186 | 0.355385 |
| 1.0 | 0 | 0 | 0 | 0 |
| 0.8 | 0.030957 | $-0.333998$ | $-0.128737$ | $-0.193846$ |
| 0.577350 | 0.170106 | $-0.993015$ | $-0.316907$ | $-0.259067$ |
| 0.3 | 0.706206 | $-3.481999$ | $-0.694600$ | $-0.183750$ |
| 0.1 | 2.224619 | $-17.091837$ | $-1.328414$ | $-0.066635$ |
| 0.01 | 7.696506 | $-304.140588$ | $-2.656829$ | $-0.006730$ |

Both models agree at first order near $s = 1$.
Under compression the neo-Hookean stress grows without bound, while the St. Venant-Kirchhoff stress has its largest size at $s = 0.577350$ and then falls.
The energy grows only like $(\log s)^2$, slowly; the stress, like $1/s$, is what stops the element.

## Relation to other models

- **[St. Venant-Kirchhoff model](/st-venant-kirchhoff-model/).** Same linear limit, a polynomial energy, defined for every $F$, but weak and then reversed under strong compression.
- **[Stable neo-Hookean model](/stable-neo-hookean/).** Smith, de Goes and Kim replace the log terms by a quadratic in $J$ and a $\log(I_1 + 1)$ term, so the energy is finite and smooth for every $F$, also for $J \le 0$.
- **[Invertible finite elements](/invertible-finite-elements/).** Irving, Teran and Fedkiw write the model in the singular values of $F$ and extend it past a small threshold of the smallest singular value, so that inverted elements get a force back toward $J > 0$.
- **Incompressible neo-Hookean.** For rubber, $J = 1$ is a constraint, and $\Psi = \frac\mu2(I_1 - 3)$ on that set. The compressible form above replaces the constraint by the $\lambda$ term, and many other compressible forms exist; they differ far from rest.
- **Barrier based solvers.** [Optimization time integration](/optimization-time-integration/) and [incremental potential contact](/incremental-potential-contact/) use line searches that keep every $J > 0$, and then the barrier of this model is an advantage.

## Known results in the model

- **Exact gradient for $J > 0$ (proved).** $P = \partial\Psi/\partial F$, and the element forces are minus the gradient of the element energy. See the [proof](proofs/correctness.md), Steps 1 and 2.
- **Objective and isotropic (proved).** $\Psi(QF) = \Psi(FQ) = \Psi(F)$ for every rotation $Q$, $P(QF) = QP(F)$, and $PF^T$ is symmetric. Proof, Step 3.
- **Rest state (proved).** $\Psi = 0$ and $P = 0$ for every rotation. Without the term $-\mu\log J$, the form $\frac\mu2(I_1 - 3) + \frac\lambda2(J - 1)^2$ has $P(I) = \mu I \ne 0$, so its rest shape is not in equilibrium. Proof, Step 4.
- **Linear limit (proved).** $P(I + \varepsilon H) = \varepsilon(2\mu\operatorname{sym}H + \lambda\operatorname{tr}(H)I) + O(\varepsilon^2)$, with no remap of $\mu$ and $\lambda$. Proof, Step 5.
- **Barrier (proved).** $\Psi \to \infty$ as $J \to 0^+$, and in the bar the compressive stress grows monotonically and without bound. So no finite value at $J = 0$ continues $\Psi$, and the model is undefined for $J \le 0$. Proof, Step 6.
- **Convexity of the volume term (proved).** $(\log J)^2$ is convex in $J$ only for $J < e$, so a Newton solver must project the element stiffness to be positive semidefinite in general; the projection is a heuristic. Proof, Step 7.
- **Failure with inverted elements (heuristic).** An explicit step or an unguarded Newton step can move a vertex past the opposite face, and then the simulation stops; in practice large time steps and collisions cause this. The fixes are a guarded line search, the inversion handling of [invertible finite elements](/invertible-finite-elements/), or the [stable neo-Hookean](/stable-neo-hookean/) energy.

## References
