---
tag: ZTB56H
kind: model
slug: elastically-deformable-models
name: Elastically deformable models
aliases:
- Terzopoulos deformable models
area: graphics-and-signals/deformable-body-simulation
level: core
summary: "Elastic curves, surfaces and solids whose energy measures the change of the metric and curvature tensors, discretized by finite differences and advanced by a semi-implicit step."
prereqs: [finite-difference-method]
see_also: [finite-element-method, hyperelastic-material, deformation-gradient, mass-spring-system, cloth-simulation, discrete-shells, cosserat-rod, backward-euler-method]
sources:
  - paper: doi:10.1145/37401.37427
    title: Demetri Terzopoulos, John Platt, Alan Barr and Kurt Fleischer, Elastically deformable models, SIGGRAPH 1987, Computer Graphics 21(4), 205 to 214
    locator: Section 3, Eq. 1 (the equation of motion); Section 4, Eqs. 2 to 8 (the fundamental forms and the energies); Section 5, Eqs. 9 to 13 (the applied forces); Section 6, Eqs. 14 to 31 (the simplified force, the finite differences and the semi-implicit step)
---

The elastically deformable models of Terzopoulos, Platt, Barr and Fleischer (1987) animate curves, surfaces and solids whose shape changes by the laws of elasticity, so that one set of equations describes both the shape and the motion.
A point with material coordinates $a$ in the domain $\Omega$ is at $r(a, t)$, and the motion follows the Lagrange form
$$\frac{\partial}{\partial t}\Bigl(\mu\frac{\partial r}{\partial t}\Bigr) + \gamma\frac{\partial r}{\partial t} + \frac{\delta\mathcal E(r)}{\delta r} = f(r, t),$$
with the mass density $\mu(a)$, the damping density $\gamma(a)$, the external force $f$ and the variational derivative of the deformation energy $\mathcal E$.
The energy compares the fundamental forms of the current shape with those of the rest shape $r^0$, so it is zero for every rigid motion.

## The machine

**The measures of deformation.** For a surface with coordinates $a = (a_1, a_2)$, the metric tensor is $G_{ij} = \frac{\partial r}{\partial a_i}\cdot\frac{\partial r}{\partial a_j}$, the first fundamental form.
The curvature tensor is $B_{ij} = n\cdot\frac{\partial^2r}{\partial a_i\partial a_j}$, with the unit normal $n$, the second fundamental form.
A solid has a $3 \times 3$ metric tensor and no curvature tensor; a space curve has the arc length, the curvature $\kappa$ and the torsion $\tau$.

**The energies.** With weighted matrix norms and the rest values marked by 0, the paper uses
$$\mathcal E_{\text{curve}} = \int_\Omega\alpha(s - s^0)^2 + \beta(\kappa - \kappa^0)^2 + \gamma(\tau - \tau^0)^2\,da,$$
$$\mathcal E_{\text{surface}} = \int_\Omega\lVert G - G^0\rVert_\alpha^2 + \lVert B - B^0\rVert_\beta^2\,da_1da_2, \qquad \mathcal E_{\text{solid}} = \int_\Omega\lVert G - G^0\rVert_\alpha^2\,da_1da_2da_3.$$

**The simplified force for a surface.** The paper takes $\mathcal E = \int\sum_{i,j}\eta_{ij}(G_{ij} - G^0_{ij})^2 + \xi_{ij}(B_{ij} - B^0_{ij})^2$ and replaces the variational derivative by
$$e(r) = \sum_{i,j = 1}^2 -\frac{\partial}{\partial a_i}\Bigl(\alpha_{ij}\frac{\partial r}{\partial a_j}\Bigr) + \frac{\partial^2}{\partial a_i\partial a_j}\Bigl(\beta_{ij}\frac{\partial^2r}{\partial a_i\partial a_j}\Bigr),$$
with $\alpha_{ij} = \eta_{ij}(G_{ij} - G^0_{ij})$ and $\beta_{ij} = \xi_{ij}(B_{ij} - B^0_{ij})$.
The weights $\eta_{11}$, $\eta_{22}$ resist stretch along the coordinate directions and $\eta_{12}$ resists shear; $\xi_{11}$, $\xi_{22}$ resist bending and $\xi_{12}$ resists twist.

**Finite differences.** The surface is an $M \times N$ grid with spacings $h_1$, $h_2$.
Forward and backward [differences](/finite-difference-method/) replace the derivatives in $\alpha_{ij}$, $\beta_{ij}$ and $e$, and the force of the whole grid takes the form $e = K(r)\,r$, with a sparse, banded stiffness matrix $K$ that depends on the current shape.
With the diagonal mass matrix $M$ and damping matrix $C$, the motion becomes $M\ddot r + C\dot r + K(r)\,r = f$.

**The semi-implicit step.** With central differences in time, $e$ evaluated at $t + \Delta t$ with $K$ frozen at $r_t$, and $f$ at $t$, each step solves one linear system
$$A_tr_{t+\Delta t} = g_t, \qquad A_t = K(r_t) + \frac1{\Delta t^2}M + \frac1{2\Delta t}C,$$
$$g_t = f_t + \Bigl(\frac1{\Delta t^2}M + \frac1{2\Delta t}C\Bigr)r_t + \Bigl(\frac1{\Delta t}M - \frac12C\Bigr)v_t, \qquad v_t = \frac{r_t - r_{t-\Delta t}}{\Delta t}.$$
The paper solves it by Cholesky decomposition or by Gauss-Seidel relaxation.

**Applied forces.** Gravity $\mu g$, a Hookean spring $k(r_0 - r(a_0))$ to a point, a viscous fluid force $c(n\cdot v)n$ with the velocity $v = u - \partial r/\partial t$ relative to a stream $u$, and a collision force from the potential $c\exp(-f(r)/\epsilon)$ of the inside-outside function $f$ of a fixed obstacle.

## What it counts

$\mathcal E$ counts how far the lengths and the angles (through $G$) and the bending (through $B$) of the body are from those of its rest shape.
It does not count where the body is or how it is turned.
The weights select the material: a large $\eta$ with $\xi = 0$ gives a cloth that resists stretch, a small $\eta$ with $\xi = 0$ a rubber sheet, a large $\eta$ with a modest $\xi$ paper, and a larger $\xi$ a spring-like metal sheet.

**Example.** For one linear mode with stiffness $\omega^2$, unit mass and no damping, the step gives $(1 + \Delta t^2\omega^2)x_{n+1} = 2x_n - x_{n-1}$.
The amplitude falls by the factor $(1 + \Delta t^2\omega^2)^{-1/2}$ per step, for every $\Delta t$:

| $\Delta t\,\omega$ | 0.1 | 1 | 10 |
|---|---|---|---|
| factor per step | 0.995037 | 0.707107 | 0.099504 |

So the step is stable for every step size, and it damps the fast modes strongly.

## Relation to other models

- **[Finite element method](/finite-element-method/).** The paper names finite elements as the other way to discretize Eq. 1 and uses finite differences on a regular grid. Many later methods use finite elements on meshes with a [hyperelastic](/hyperelastic-material/) energy of the [deformation gradient](/deformation-gradient/).
- **[Hyperelastic materials](/hyperelastic-material/).** If the material coordinates are the rest positions, the metric tensor of a solid is the right Cauchy-Green tensor $F^TF$, and $G - G^0 = 2E$ with the Green strain $E$. So the solid energy is a weighted quadratic energy of $E$, like the [St. Venant-Kirchhoff model](/st-venant-kirchhoff-model/), but with weights that need not be isotropic.
- **[Mass-spring systems](/mass-spring-system/).** The finite difference terms of $\eta_{11}$ and $\eta_{22}$ couple neighbors along the grid lines, like springs, but the energy is quadratic in the change of the squared length.
- **[Discrete shells](/discrete-shells/) and [cloth](/cloth-simulation/).** Later surface models also split the energy into a stretch part and a bending part.
- **Spline under tension.** The paper notes that with $\alpha_{12} = \alpha_{21} = 0$ and with $\alpha_{11}$, $\alpha_{22}$ and $\beta_{ij}$ independent of $r$, the force is that of a thin plate surface under tension, and for curves that of a spline under tension.
- **[Backward Euler](/backward-euler-method/).** The step has the same idea: the elastic force at the new time makes the step stable for stiff materials, at the cost of one linear solve and of numerical damping.

## Known results in the model

- **Rigid motions cost nothing (proved).** For $r \mapsto Rr + c$ with a rotation $R$, the derivatives of $r$ turn by $R$ and $n$ turns by $R$, so $G$ and $B$ do not change and $\mathcal E$ is the same; it is zero at every rigid motion of the rest shape.
- **The stretch term is an exact gradient (proved).** For symmetric $\eta$, $\delta G_{ij} = \delta r_{,i}\cdot r_{,j} + r_{,i}\cdot\delta r_{,j}$ gives $\delta\bigl(\frac14\int\sum\eta_{ij}(G_{ij} - G^0_{ij})^2\bigr) = \int\sum\alpha_{ij}r_{,j}\cdot\delta r_{,i}$, and integration by parts gives the first sum of $e(r)$. So the $\alpha$ part is the variational derivative of the stretch energy with the weight $\frac14\eta$.
- **The bending term is a simplification (stated in the paper).** The exact variational derivative of the $B$ term is long, because $n$ depends on $r$. The $\beta$ part of $e(r)$ is chosen by analogy with the $\alpha$ part, so it is not in general the gradient of an energy (heuristic).
- **One linear solve per step (proved).** $A_t$ and $g_t$ use only $r_t$ and $r_{t-\Delta t}$, so each step is one sparse linear system in $3MN$ unknowns for a surface in space. If $\alpha$ and $\beta$ do not depend on $r$, then $A_t$ is constant and one decomposition serves all steps, as the paper notes.
- **The step and the paper's form agree (proved).** Putting the central differences into $M\ddot r + C\dot r + K(r_t)r_{t+\Delta t} = f_t$ and writing $r_{t-\Delta t} = r_t - \Delta t\,v_t$ gives exactly $A_t$ and $g_t$ above.
- **Stable and damping for a linear mode (proved).** The roots of $(1 + \Delta t^2\omega^2)z^2 - 2z + 1 = 0$ are complex with $\lvert z\rvert^2 = 1/(1 + \Delta t^2\omega^2) < 1$, which gives the table above.
- **Self-collision (stated in the paper).** The paper avoids self-intersection only with a repulsive force around the surface, and notes that this is expensive without a hierarchy of bounding boxes.

## References
