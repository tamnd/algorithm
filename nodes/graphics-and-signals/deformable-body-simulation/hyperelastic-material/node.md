---
tag: 4EVPZY
kind: concept
slug: hyperelastic-material
name: Hyperelastic material
aliases:
- strain energy density function
area: graphics-and-signals/deformable-body-simulation
level: core
summary: A material whose stress is the derivative of a strain energy density of the deformation gradient, so that forces are minus the energy gradient.
prereqs: [deformation-gradient]
see_also: [st-venant-kirchhoff-model, neo-hookean-model, stable-neo-hookean, corotational-fem, invertible-finite-elements, finite-element-method, optimization-time-integration, mass-spring-system]
sources:
  - paper: doi:10.1145/2343483.2343501
    title: Eftychios Sifakis and Jernej Barbič, FEM simulation of 3D deformable solids, a practitioner's guide to theory, discretization and model reduction, SIGGRAPH 2012 Courses, article 20
    locator: the strain energy density, the first Piola-Kirchhoff stress P = ∂Ψ/∂F and the isotropic models in terms of invariants and singular values (general locator)
  - paper: "Javier Bonet and Richard D. Wood, Nonlinear Continuum Mechanics for Finite Element Analysis, second edition, Cambridge University Press, 2008"
    locator: the chapter on hyperelasticity, with objectivity, isotropy and the invariants (general locator)
---

A hyperelastic material is an elastic material that stores energy: there is a strain energy density $\Psi(F)$, a function of the [deformation gradient](/deformation-gradient/) $F$ only, and the stress is its derivative, $P = \partial\Psi/\partial F$.
The total elastic energy of a body is $\int\Psi(F)\,dX$ over the rest shape, and the elastic forces are minus its gradient.
So the work that the forces do over a closed path of deformations is zero, and a simulation without damping can conserve energy.
The [St. Venant-Kirchhoff](/st-venant-kirchhoff-model/), [neo-Hookean](/neo-hookean-model/) and [stable neo-Hookean](/stable-neo-hookean/) models are hyperelastic, and they differ only in the choice of $\Psi$.

## In plain words

Think of a rubber block.
When you stretch, twist or squeeze it, it stores energy, and it gives that energy back when you let go.
A hyperelastic material is a material described by one rule: how much energy a small piece stores for each way it can be deformed.
Everything else follows from that rule.
The push and the pull inside the material come from how fast the stored energy changes when the shape changes.
The forces on the points of a mesh come from the same rule, so they always point toward shapes with less energy.
Because the energy depends only on the present shape, and not on the path to it, a loop that ends at the start gives back exactly the energy that was put in.

## The idea

**The energy density.** $\Psi$ is the energy per unit rest volume, in J/m³ in 3D (J/m² in 2D).
It depends on $F$ only, not on the history of the deformation and not on the velocity.
Damping, plasticity and viscosity are not hyperelastic; a model adds them separately.

**The stress and the forces.** The first Piola-Kirchhoff stress $P = \partial\Psi/\partial F$ is the force per unit rest area.
On a linear element with rest volume $V_0$ the energy is $W = V_0\Psi(F)$ with $F = D_sD_m^{-1}$, and the forces on the vertices 1 to $d$ are the columns of $-V_0PD_m^{-T}$; vertex 0 gets minus their sum.
This is the exact gradient $-\partial W/\partial x$, because $dW = V_0P : dF = V_0(PD_m^{-T}) : dD_s$.
The second Piola-Kirchhoff stress is $S = F^{-1}P$, symmetric for an objective $\Psi$, and the Cauchy stress is $\sigma = J^{-1}PF^T$.

**Objectivity (frame indifference).** Turning the deformed body must not change the energy: $\Psi(QF) = \Psi(F)$ for every rotation $Q$.
This is a law of mechanics that every model must obey.
For $J > 0$ it holds exactly when $\Psi$ depends on $F$ only through $C = F^TF$, or through the stretch $S$ of the polar decomposition $F = RS$.
A consequence, from the derivative of $\Psi(QF)$ along a small rotation, is that $PF^T$ is symmetric, so the forces of an element have no net torque.

**Isotropy.** A material with no preferred direction has $\Psi(FQ) = \Psi(F)$ for every rotation $Q$ of the rest shape.
An isotropic objective $\Psi$ depends only on the invariants of $C$,

$$I_1 = \operatorname{tr}C, \qquad I_2 = \tfrac12\bigl((\operatorname{tr}C)^2 - \operatorname{tr}(C^2)\bigr), \qquad I_3 = \det C = J^2,$$

or, the same, on the singular values of $F$ (the principal stretches), in any order.
Isotropy is a property of the material, not a law; wood, muscle and fabric are anisotropic and add terms with a fiber direction.

**Rest state and linear limit.** At rest, $F = I$, a model should have $P(I) = 0$, so the rest shape is in equilibrium.
Near rest, every isotropic hyperelastic model with $P(I) = 0$ agrees at first order with linear elasticity, $P \approx 2\mu\varepsilon + \lambda\operatorname{tr}(\varepsilon)I$ with the small strain $\varepsilon = \frac12(H + H^T)$, $H = F - I$.
The Lamé parameters $\mu$ and $\lambda$ come from Young's modulus $E$ and Poisson's ratio $\nu$ by

$$\mu = \frac{E}{2(1 + \nu)}, \qquad \lambda = \frac{E\nu}{(1 + \nu)(1 - 2\nu)}.$$

For $E = 1$ and $\nu = 0.3$, $\mu = 0.384615$ and $\lambda = 0.576923$.
Each model has its own $\mu$ and $\lambda$ in its formula, and a model may need a remap of these parameters to have the right linear limit, as the [stable neo-Hookean model](/stable-neo-hookean/) does.

**Large deformation.** The models differ far from rest: how they resist strong compression, whether $\Psi$ is defined for $J \le 0$, and whether $\Psi$ is convex along a path.
An objective $\Psi$ cannot be convex in $F$ and also grow without bound as $J \to 0$: in 3D, $I$ and the rotation $\operatorname{diag}(-1, -1, 1)$ have the same finite energy, and their midpoint $\operatorname{diag}(0, 0, 1)$ is flat, so convexity would bound its energy by that finite value.
This is a proved property, and models choose between these goals.

## Examples

| Model | $\Psi(F)$ in 3D | Defined for $J \le 0$ | Behavior under strong compression |
|---|---|---|---|
| [St. Venant-Kirchhoff](/st-venant-kirchhoff-model/) | $\mu\lvert E\rvert_F^2 + \frac{\lambda}{2}(\operatorname{tr}E)^2$ | yes | the restoring force weakens and then reverses |
| [Neo-Hookean](/neo-hookean-model/) | $\frac{\mu}{2}(I_1 - 3) - \mu\log J + \frac{\lambda}{2}(\log J)^2$ | no | the energy grows without bound as $J \to 0$ |
| [Stable neo-Hookean](/stable-neo-hookean/) | $\frac{\mu}{2}(I_1 - 3) + \frac{\lambda}{2}(J - \alpha)^2 - \frac{\mu}{2}\log(I_1 + 1)$ | yes | finite energy, and the force keeps pushing toward $J > 0$ |
| Corotated ([corotational FEM](/corotational-fem/)) | $\mu\lvert F - R\rvert_F^2 + \frac{\lambda}{2}\operatorname{tr}(R^TF - I)^2$ | yes, with care | grows like a linear spring in the stretches |

All four are objective and isotropic, and all have $P(I) = 0$.
A model that is not hyperelastic: linear elasticity written with $\varepsilon = \frac12(H + H^T)$ is the quadratic energy $\mu\lvert\varepsilon\rvert_F^2 + \frac{\lambda}{2}(\operatorname{tr}\varepsilon)^2$, so it is hyperelastic as a function of $F$, but it is not objective: a pure rotation gives a nonzero strain and a nonzero force.
A [mass-spring system](/mass-spring-system/) has an energy too, but of the edges of a mesh, not a density of $F$, so its behavior depends on the mesh.

## Where it is used

- **Finite element simulation in graphics.** Every element computes $F$, then $P$, then its forces; the same $\Psi$ gives the stiffness $\partial^2W/\partial x^2$ for implicit steps.
- **Energy based solvers.** [Optimization time integration](/optimization-time-integration/) and [incremental potential contact](/incremental-potential-contact/) minimize an energy per step, which needs a $\Psi$ and not only a force.
- **Inversion handling.** [Invertible finite elements](/invertible-finite-elements/) write $\Psi$ in terms of the singular values of $F$, and the [stable neo-Hookean model](/stable-neo-hookean/) was designed to be defined for inverted elements.
- **Rods, shells and reduced models.** The same idea, an energy and its gradient, gives the bending and twisting forces of [discrete elastic rods](/discrete-elastic-rods/) and [discrete shells](/discrete-shells/), and the cubic forces of [modal reduction](/modal-reduction/) for the St. Venant-Kirchhoff model.

## References
