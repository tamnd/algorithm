---
tag: 1C1F35
kind: definition
slug: deformation-gradient
name: Deformation gradient
aliases:
- deformation gradient tensor
area: graphics-and-signals/deformable-body-simulation
level: core
summary: The Jacobian F of the map from rest to deformed positions, constant on a linear triangle or tetrahedron, from which strain and stress are computed.
prereqs: [finite-element-method]
see_also: [hyperelastic-material, st-venant-kirchhoff-model, corotational-fem, invertible-finite-elements, singular-value-decomposition, deformation-transfer, as-rigid-as-possible-deformation, kabsch-algorithm]
sources:
  - paper: doi:10.1145/2343483.2343501
    title: Eftychios Sifakis and Jernej Barbič, FEM simulation of 3D deformable solids, a practitioner's guide to theory, discretization and model reduction, SIGGRAPH 2012 Courses, article 20
    locator: the deformation map and its gradient, and F = D_s D_m^(-1) for a linear tetrahedron (general locator)
  - paper: "Javier Bonet and Richard D. Wood, Nonlinear Continuum Mechanics for Finite Element Analysis, second edition, Cambridge University Press, 2008"
    locator: the chapter on kinematics, with the deformation gradient, the volume change J, the polar decomposition and the Green strain (general locator)
---

The deformation gradient $F$ is the Jacobian of the map that takes each point of a body in its rest shape to its point in the deformed shape.
It describes how a small neighborhood of the point is stretched, sheared and turned.
In a mesh of linear triangles or tetrahedra the map is affine on each element, so $F$ is one constant matrix per element, $F = D_sD_m^{-1}$, computed from the edge vectors.
All strain measures and all stresses of the elastic models on the neighboring pages start from $F$.

## Definition

Let a body occupy the rest region $\Omega \subset \mathbb R^d$ with $d = 2$ or 3, and let the deformation $\varphi: \Omega \to \mathbb R^d$ map each rest point $X$ to its current point $x = \varphi(X)$.
The deformation gradient is

$$F(X) = \frac{\partial\varphi}{\partial X}(X), \qquad F_{ij} = \frac{\partial\varphi_i}{\partial X_j}.$$

A small rest vector $dX$ at $X$ is mapped to $dx = F\,dX$ at first order.
The derived quantities are:

- $J = \det F$, the ratio of the current to the rest volume (in 2D, area) near $X$. $J > 0$ for a deformation that keeps the orientation, $J = 0$ for a flat element and $J < 0$ for an inverted one.
- The right Cauchy-Green tensor $C = F^TF$, with $|dx|^2 = dX^TC\,dX$.
- The Green strain $E = \frac12(F^TF - I)$, with $|dx|^2 - |dX|^2 = 2\,dX^TE\,dX$. With the displacement gradient $H = F - I$, $E = \frac12(H + H^T) + \frac12H^TH$; the first term alone is the linear (small) strain.
- The polar decomposition $F = RS$ with a rotation $R$ and a symmetric $S$, which is positive definite when $J > 0$. $R$ is the part of the deformation that only turns the neighborhood.

**Linear elements.** For a simplex with rest vertices $X_0, \dots, X_d$ and current vertices $x_0, \dots, x_d$, define the edge matrices

$$D_m = [X_1 - X_0, \dots, X_d - X_0], \qquad D_s = [x_1 - x_0, \dots, x_d - x_0].$$

If $\det D_m \ne 0$, the only affine map with $\varphi(X_k) = x_k$ has the gradient $F = D_sD_m^{-1}$, constant on the element.
$D_m^{-1}$ depends only on the rest shape, so a simulator computes it once per element.

**Properties.** These are proved properties, shown in the [proof](proofs/correctness.md).

- $F$ reproduces every affine map exactly and does not depend on the numbering of the vertices.
- $J = \det D_s/\det D_m$, the ratio of the signed measures.
- The gradient of a composition is the product: $F_{2 \circ 1} = F_2F_1$.
- $E(QF) = E(F)$ for every rotation $Q$, and $E = 0$ exactly when $F$ is orthogonal. A reflection, $\det F = -1$, also has $E = 0$: the Green strain does not see inversion.
- For a smooth $\varphi$ and a simplex of size $h$ at $X_0$, $F - \nabla\varphi(X_0) = O(h)$.
- In 2D, $R = \operatorname{rot}(\theta)$ with $\theta = \operatorname{atan2}(F_{10} - F_{01}, F_{00} + F_{11})$, the rotation that maximizes $\operatorname{tr}(R^TF)$.

## Examples and non-examples

Take the rest triangle $(0, 0)$, $(2, 0)$, $(0, 1)$, so $D_m = \operatorname{diag}(2, 1)$ and $D_m^{-1} = \operatorname{diag}(0.5, 1)$.

| Current vertices | $F$ | $J$ | $E$ | $R$ |
|---|---|---|---|---|
| $(0, 0)$, $(3, 0)$, $(0, 1)$ | $\begin{pmatrix}1.5 & 0\\0 & 1\end{pmatrix}$ | 1.5 | $\begin{pmatrix}0.625 & 0\\0 & 0\end{pmatrix}$ | $I$ |
| $(1, 1)$, $(3, 1)$, $(1.5, 2)$ | $\begin{pmatrix}1 & 0.5\\0 & 1\end{pmatrix}$ | 1 | $\begin{pmatrix}0 & 0.25\\0.25 & 0.125\end{pmatrix}$ | $\operatorname{rot}(-0.244979)$ |
| $(0, 0)$, $(0, 2)$, $(-1, 0)$ | $\begin{pmatrix}0 & -1\\1 & 0\end{pmatrix}$ | 1 | 0 | $\operatorname{rot}(\pi/2)$ |
| $(0, 0)$, $(2, 0)$, $(1, 0)$ | $\begin{pmatrix}1 & 1\\0 & 0\end{pmatrix}$ | 0 | $\begin{pmatrix}0 & 0.5\\0.5 & 0\end{pmatrix}$ | $\operatorname{rot}(-\pi/4)$ |
| $(0, 0)$, $(2, 0)$, $(0.5, -1)$ | $\begin{pmatrix}1 & 0.5\\0 & -1\end{pmatrix}$ | $-1$ | $\begin{pmatrix}0 & 0.25\\0.25 & 0.125\end{pmatrix}$ | $\operatorname{rot}(-\pi/2)$ |

- The first row is a stretch by 1.5 along $x$: $E_{00} = (1.5^2 - 1)/2 = 0.625$, while the linear strain would be 0.5.
- The second row is a translation by $(1, 1)$ and a shear. The translation does not appear in $F$, and the shear has $J = 1$, so the area does not change.
- The third row is a rotation by 90 degrees. $F$ is far from $I$, but $E = 0$, so a model built on $E$ gives no force. The linear strain $\frac12(H + H^T) = -I$ is not zero; this is why linear elasticity fails under rotation.
- The fourth row is flat, $J = 0$, so $F$ has no inverse.
- The fifth row is inverted, $J = -1$, but its $E$ equals the $E$ of the shear in the second row. So $E$ alone cannot tell an inverted element from a valid one; the sign of $J$ can. Its $S$ has one negative eigenvalue.

A non-example: the matrix $D_s$ alone is not the deformation gradient, because it also depends on the size and the shape of the rest element. Another non-example: on a quadratic element the map is not affine, so $F$ changes inside the element, and one matrix per element is only an approximation.

## Related definitions

- **Hyperelastic stress.** A [hyperelastic material](/hyperelastic-material/) has an energy density $\Psi(F)$, and the first Piola-Kirchhoff stress is $P = \partial\Psi/\partial F$. The [St. Venant-Kirchhoff model](/st-venant-kirchhoff-model/) uses $E$, and the [neo-Hookean model](/neo-hookean-model/) uses $\operatorname{tr}C$ and $J$.
- **Polar decomposition.** The rotation $R$ of $F = RS$ is what [corotational finite elements](/corotational-fem/) remove before applying a linear model. It is also the best rotation of a set of points, as in the [Kabsch algorithm](/kabsch-algorithm/) and in [as-rigid-as-possible deformation](/as-rigid-as-possible-deformation/).
- **Singular values.** $F = U\hat FV^T$ by the [singular value decomposition](/singular-value-decomposition/), with the principal stretches on the diagonal. [Invertible finite elements](/invertible-finite-elements/) use a signed form of it.
- **Deformation transfer.** [Deformation transfer](/deformation-transfer/) copies the per-triangle deformation gradients of one mesh to another.
- **Velocity gradient.** $\dot FF^{-1}$ is the gradient of the velocity in the current shape; its symmetric part is the rate of deformation, used by damping and plasticity models.

## References
