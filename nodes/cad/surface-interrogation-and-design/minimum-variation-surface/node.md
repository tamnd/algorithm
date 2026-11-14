---
tag: VWP4BG
kind: technique
slug: minimum-variation-surface
name: Minimum variation surface
aliases:
- Moreton-Sequin surface
area: cad/surface-interrogation-and-design
level: research
summary: Moreton and Sequin's fair surfaces that minimise the variation of the principal curvatures, which reproduce circles, cylinders and spheres, by nonlinear optimisation.
prereqs: [surface-curvature, lines-of-curvature, energy-based-surface-fairing]
see_also: [energy-based-surface-fairing, knot-removal-fairing, surface-curvature, lines-of-curvature, reflection-lines, tangent-plane-continuity, levenberg-marquardt, fundamental-forms]
sources:
  - paper: doi:10.1145/142920.134035
    title: "Henry P. Moreton and Carlo H. Séquin, Functional optimization for fair surface design, Computer Graphics 26(2), 167 to 176, 1992 (SIGGRAPH 1992)"
    locator: the minimum variation surface functional, the integral of the squared derivatives of the principal curvatures along their principal directions, and its comparison with the minimum energy surface
  - paper: doi:10.1111/1467-8659.1330143
    title: "Günther Greiner, Variational design and fairing of spline surfaces, Computer Graphics Forum 13(3), 143 to 154, 1994"
    locator: fairness functionals made quadratic by a reference parametrization
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: principal curvatures, lines of curvature and surfaces of revolution
---

A minimum variation surface is a surface that minimizes how fast its principal curvatures change, measured along the principal directions. Moreton and Séquin introduced it in 1992 as a better measure of fairness than the bending energy. Its functional is zero on the sphere, the cylinder, the cone and the torus, so a designer who constrains a surface to fit such a shape gets that shape back. The thin plate energy of [energy-based fairing](/energy-based-surface-fairing/) does not do this in general: under the same constraints its minimizer is usually not the sphere. The price is that the functional depends on third derivatives of the surface and is not quadratic in the control points, so it needs nonlinear optimization.

## In plain words

Designers like surfaces whose bending changes slowly and evenly, because light reflects from them without sudden kinks. A ball and a pipe are perfect in this sense: their bending is the same everywhere. Older fairing methods make a surface bend as little as possible, which is a different aim: when only the rim of a part of a ball is held, they do not in general keep it round. The minimum variation idea asks instead that the bending stay the same as one walks along the surface in the directions of its strongest and weakest bending. A ball, a pipe, a cone and a ring all pass this test perfectly. The cost is that the measure is hard to compute, so the computer must search for the best surface step by step.

## When it applies

Use it when the shape between constraints must be of the highest quality and the time for a nonlinear optimization is acceptable: styling surfaces, blends between surfaces where circular shapes are expected, and surfaces that should reduce to spheres or cylinders when the constraints allow. It needs a surface representation with enough smoothness for third derivatives inside each patch, and constraints that fix position and possibly tangent planes and curvatures at points or along curves. It does not apply when the result must come from one linear solve, or at interactive rates on large models.

## The template

Let $\kappa_1$ and $\kappa_2$ be the principal curvatures of a surface $S$, with unit principal directions $e_1$ and $e_2$. Write $\kappa_{1, e_1}$ for the derivative of $\kappa_1$ along $e_1$, and $\kappa_{2, e_2}$ for that of $\kappa_2$ along $e_2$. The *minimum variation surface functional* of Moreton and Séquin is

$$E_{\mathrm{MVS}}(S) = \iint_S \kappa_{1, e_1}^2 + \kappa_{2, e_2}^2 \, dA.$$

Its curve analogue, $\int (d\kappa/ds)^2 \, ds$ for a planar curve, is zero exactly on lines and circles. The minimum energy surface, in contrast, minimizes $\iint \kappa_1^2 + \kappa_2^2 \, dA$.

```pseudo id=main
MVS(patch network with free parameters x, constraints)
L1  choose a network of patches with tangent plane continuity whose free parameters x keep the constraints
L2  repeat
L3      at sample points of each patch, compute κ1, κ2, e1, e2 from the fundamental forms
L4      estimate κ1 along e1 and κ2 along e2, by differentiation of the patch or by differences between samples
L5      E(x) ← Σ_s w_s (κ1,e1² + κ2,e2²) |S_u × S_v| at the samples          ▷ quadrature
L6      change x by a step of a nonlinear optimizer that lowers E              ▷ any descent method
L7  until E or x changes little
L8  return the patches
```

Line L1 is a design choice: the unknowns are control points or other shape parameters of a patch network whose joins satisfy [tangent plane continuity](/tangent-plane-continuity/), and constraints are kept either by the choice of free parameters or by penalty terms. Lines L3 and L4 use the [fundamental forms](/fundamental-forms/) and the formulas of [surface curvature](/surface-curvature/). Line L6 can be any descent method, such as a gradient method or [Levenberg-Marquardt](/levenberg-marquardt/) on the residuals $\sqrt{w_s |S_u \times S_v|}\, \kappa_{i, e_i}$.

**Theorem 1 (surfaces of revolution).** Let $S$ be a surface of revolution without umbilical points, with profile curve of curvature $k(s)$ in arc length $s$. Then

$$E_{\mathrm{MVS}}(S) = \iint_S \Bigl(\frac{dk}{ds}\Bigr)^2 dA.$$

In particular $E_{\mathrm{MVS}} = 0$ exactly when the profile is a line or a circular arc: for a cylinder, a cone, and a torus or a part of one. A sphere, where every point is umbilical, also has $E_{\mathrm{MVS}} = 0$, because its principal curvatures are constant.

*Proof.* On a surface of revolution the meridians and the parallels are lines of curvature, so $e_1$ is tangent to the meridian and $e_2$ to the parallel, or the other way. The normal curvature in the meridian direction is the curvature $k$ of the profile, since the meridian lies in a plane that contains the surface normal. The curvature in the parallel direction depends only on the position along the meridian, by the rotational symmetry, so it is constant along each parallel and its derivative along $e_2$ is zero. The derivative of the meridian curvature along $e_1$ is $dk/ds$. So the integrand is $(dk/ds)^2$. It vanishes everywhere exactly when $k$ is constant along the profile, which makes the profile a line or a circle. On a sphere $\kappa_1 = \kappa_2 = 1/R$ everywhere, so every derivative of a principal curvature is zero, whatever directions are chosen. $\square$

In general, $E_{\mathrm{MVS}} = 0$ on a surface without umbilical points exactly when each principal curvature is constant along its own lines of curvature. By a classical result of differential geometry, these surfaces are the Dupin cyclides, a family that contains the torus, the cylinder and the cone.

**Theorem 2 (scaling and nonlinearity).** If $S$ is scaled by $c > 0$, then $E_{\mathrm{MVS}}(c S) = E_{\mathrm{MVS}}(S)/c^2$, while $\iint \kappa_1^2 + \kappa_2^2 \, dA$ does not change. $E_{\mathrm{MVS}}$ is not a quadratic form in the control points.

*Proof.* Under scaling by $c$, curvatures become $\kappa/c$, derivatives along the surface gain a factor $1/c$, and areas a factor $c^2$, so the integrand $\kappa_{i, e_i}^2$ gains $c^{-4}$ and the integral $c^{-2}$. The bending energy has integrand $\kappa^2$, which gains $c^{-2}$, and the area cancels it. Scaling about the origin scales the control points by $c$, and a quadratic form $Q$ satisfies $Q(c p) = c^2 Q(p)$. Take a surface with $E_{\mathrm{MVS}}(S) > 0$, such as the paraboloid of the worked example below. For $c = 2$ a quadratic form would give $4 E_{\mathrm{MVS}}(S)$, but the scaling law gives $E_{\mathrm{MVS}}(S)/4$, which is different. So $E_{\mathrm{MVS}}$ is not a quadratic form. $\square$

So the minimization of line L6 is a genuinely nonlinear problem, which is the main cost of the method compared with [energy-based fairing](/energy-based-surface-fairing/), where Theorem 1 of that page makes the problem linear.

**Worked example.** Take the cap of the paraboloid $z = \frac12 (x^2 + y^2)$ over the unit disk, a surface of revolution with the profile $z = \frac12 \rho^2$. The curvature of the profile at the radius $\rho$ is $k = (1 + \rho^2)^{-3/2}$, and the arc length satisfies $ds = \sqrt{1 + \rho^2} \, d\rho$, so $dk/ds = -3 \rho (1 + \rho^2)^{-3}$. With $dA = 2 \pi \rho \sqrt{1 + \rho^2} \, d\rho$, Theorem 1 gives

$$E_{\mathrm{MVS}} = \int_0^1 \frac{9 \rho^2}{(1 + \rho^2)^6} \, 2 \pi \rho \sqrt{1 + \rho^2} \, d\rho = \frac{\pi}{7} \Bigl(4 - \frac{11}{8 \sqrt 2}\Bigr) \approx 1.359,$$

by the substitution $w = 1 + \rho^2$. A spherical cap has $E_{\mathrm{MVS}} = 0$. So if the constraints at the rim allow a spherical cap, that cap has a lower value of the functional than the paraboloid, and no surface has a lower value than $0$. The thin plate energy of a spherical cap of radius $R$ is not zero: it is $\frac{2}{R^2}$ times its area.

## Classic examples

- **The paper of Moreton and Séquin.** They compare minimum variation surfaces with minimum energy surfaces on the same constraints, with examples where the first keep circular and spherical shapes and the second do not.
- **Fair blends and fillets.** Blends between surfaces often should have circular cross sections, as a [rolling ball blend](/rolling-ball-blend/) has by construction. Circles and cylinders have zero energy, so the functional does not penalize such sections.
- **Curves.** The minimum variation curve, which minimizes $\int (d\kappa/ds)^2 \, ds$, gives circular arcs where the constraints allow, while the elastic curve, which minimizes $\int \kappa^2 \, ds$, does not.
- **Simplified functionals.** Greiner makes fairness functionals quadratic with a reference parametrization, which keeps the cost of one linear solve per iteration.

## Variations

- **Mean curvature variation.** $\iint |\nabla H|^2 \, dA$, with $H$ the mean curvature, is zero on surfaces of constant mean curvature, such as spheres and cylinders, but not on the torus.
- **Third derivative energies.** Replace the geometric derivatives by third derivatives in the parameters, $\iint |S_{uuu}|^2 + 3 |S_{uuv}|^2 + 3 |S_{uvv}|^2 + |S_{vvv}|^2$, which is quadratic but depends on the parametrization.
- **Discrete versions.** On meshes, discrete curvatures and their differences give discrete minimum variation energies.
- **Scale invariant versions.** Multiplying $E_{\mathrm{MVS}}$ by the area, or using $\iint \kappa_{i, e_i}^2 / \kappa^2$ where curvature does not vanish, removes the scale dependence of Theorem 2.

## Pitfalls

- **The measure is a design criterion.** $E_{\mathrm{MVS}}$ encodes one view of fairness. A minimum is not a proof that the surface is fair, and designers still judge the result with [reflection lines](/reflection-lines/) and curvature plots.
- **Umbilical points.** Where $\kappa_1 = \kappa_2$ the principal directions are not defined, and the integrand is not defined from the formulas above. An implementation must treat such points with care.
- **Cost.** The functional needs third derivatives and principal directions at every sample, and each optimizer step needs it again, so the method is much slower than a linear solve.
- **Local minima.** The problem is nonlinear, and the optimizer can stop at a local minimum that depends on the start. A start from a minimum energy surface is a common choice.
- **Scale.** Theorem 2 means that the same weights behave differently on large and small parts, which matters when the functional is combined with other terms.
- **Discretization.** Too few samples, or patches of too low degree to represent changing curvature, give a value of the functional that does not represent the surface.

## Exercises

1. Show that a planar curve with $\int (d\kappa/ds)^2 \, ds = 0$ is a line segment or a circular arc.
2. Prove that the torus with radii $R > r > 0$ has $E_{\mathrm{MVS}} = 0$, by writing its principal curvatures as functions of the angle along the small circle.
3. Compute $\iint \kappa_1^2 + \kappa_2^2 \, dA$ for the paraboloid cap of the worked example, and compare it with that of a spherical cap with the same rim and the same height.
4. Show that $E_{\mathrm{MVS}}$ of the elliptic cylinder $(a \cos t, b \sin t, z)$, $0 \le z \le 1$, with $a \ne b$, is positive, and find which term of the integrand is not zero.

## References
