---
tag: 7MV41Z
kind: technique
slug: isogeometric-shape-optimization
name: Isogeometric shape optimization
aliases:
- CAD-based shape optimization
area: cad/cad-cae-integration
level: research
summary: Uses CAD control points as design variables and the same spline basis for analysis, so the optimised shape is a CAD model with no remeshing, as Wall and coauthors did.
prereqs: [isogeometric-analysis, nurbs, gradient-descent]
see_also: [topology-optimization, adjoint-sensitivity-analysis, volumetric-spline-parameterization, isogeometric-kirchhoff-love-shell, boehm-knot-insertion, automatic-differentiation, kkt-conditions, level-set-topology-optimization]
sources:
  - paper: doi:10.1016/j.cma.2008.01.025
    title: W. A. Wall, M. A. Frenzel and C. Cyron, Isogeometric structural shape optimization, Computer Methods in Applied Mechanics and Engineering 197(33-40), 2008, 2976 to 2988
    locator: the whole paper (control points as design variables, the analysis on the same NURBS basis, and the gradient based optimization of 2D structures)
  - paper: doi:10.1016/j.cma.2010.03.005
    title: X. Qian, Full analytical sensitivities in NURBS based isogeometric shape optimization, Computer Methods in Applied Mechanics and Engineering 199(29-32), 2010, 2059 to 2071
    locator: the whole paper, the analytical derivatives of the stiffness with respect to control points and weights
  - paper: doi:10.1016/j.cma.2014.02.001
    title: J. Kiendl, R. Schmidt, R. Wüchner and K.-U. Bletzinger, Isogeometric shape optimization of shells using semi-analytical sensitivity analysis and sensitivity weighting, Computer Methods in Applied Mechanics and Engineering 274, 2014, 148 to 167
    locator: the whole paper, shape optimization of isogeometric shells with semi-analytical sensitivities and a weighting that removes the dependence of the result on the control net
  - paper: doi:10.1016/j.cma.2004.10.008
    title: T. J. R. Hughes, J. A. Cottrell and Y. Bazilevs, Isogeometric analysis, CAD, finite elements, NURBS, exact geometry and mesh refinement, Computer Methods in Applied Mechanics and Engineering 194(39-41), 2005, 4135 to 4195
    locator: the isogeometric idea of one spline basis for the geometry and the analysis, and refinement by knot insertion and degree elevation
---

Isogeometric shape optimization changes the shape of a part to improve a measure of its behavior, such as its stiffness or its peak stress, by moving the control points of its CAD model. The analysis uses the same spline basis, as in [isogeometric analysis](/isogeometric-analysis/), so each new design is analyzed with no remeshing, the derivatives of the analysis with respect to the design follow exactly from the spline map, and the result is a CAD model that can go back to the designer. Wall, Frenzel and Cyron (2008) introduced the method for 2D structures. This page defines the adjoint method it uses to compute gradients, because no page of this site covers shape optimization or the adjoint method for this setting. The [adjoint sensitivity analysis](/adjoint-sensitivity-analysis/) page covers the same idea for circuit equations; here the state equation is the discrete elasticity system, and the design variables move the geometry through the spline map. Unlike [topology optimization](/topology-optimization/), the method keeps the topology of the part: it moves boundaries but does not create holes.

## In plain words

A designer wants a part that is as stiff as possible for a given amount of material, or one whose highest stress is as low as possible. The shape of the part is set by a few control points, the handles that a CAD program uses to bend curves and surfaces.

The method treats those handles as the knobs of the design. For each setting of the knobs, it computes how the part behaves, using the same smooth shapes that the CAD model uses, so no new mesh is ever needed. It then works out in which direction each knob should turn to improve the part. A clever trick gives all these directions at the cost of about one extra computation, however many knobs there are. The knobs move a little, and the steps repeat until no move helps. The final shape is again a CAD model.

## When it applies

- The part is a spline or NURBS model, and its boundary shape, not its topology, is to be optimized.
- The behavior is computed by a discretized linear or nonlinear boundary value problem, such as elasticity, heat flow or potential flow.
- The objective and the constraints are smooth functions of the state and the control points, so gradient based optimizers apply.
- A valid interior parameterization can follow the boundary as it moves: trivially for shells and planar patches, and with care for solids, see [volumetric spline parameterization](/volumetric-spline-parameterization/).

## The template

```pseudo id=main
ISOGEOMETRIC-SHAPE-OPTIMIZATION(CAD model with control points P, objective J, constraints)
L1  choose the design variables s, a subset of control point coordinates and weights, with P = P(s) (linked for symmetry)
L2  build the analysis model by knot insertion and degree elevation: Q = T P with a fixed refinement matrix T
L3  solve the state equation K(s) u = F(s)
L4  solve the adjoint equation K(s)^T λ = ∂J/∂u
L5  compute dJ/ds = ∂J/∂s + λ^T (∂F/∂s − (∂K/∂s) u), element by element from ∂x/∂Q_j = R_j
L6  update s by a gradient based optimizer, with move limits and the constraints, and check det J > 0
L7  repeat L2 to L6 until the optimality conditions hold; return the CAD model with the control points P(s)
```

**Step L2, two levels.** The design model has few control points and the analysis model many. [Knot insertion](/boehm-knot-insertion/) and degree elevation leave the geometry unchanged and make the refined control points a fixed linear function of the coarse ones, $Q = T P$, so $\partial Q / \partial s = T \, \partial P / \partial s$. The design stays coarse and smooth while the analysis is accurate.

**Steps L4 and L5, the adjoint method.** Let $J(s) = j(u(s), s)$, where $u(s)$ solves $K(s) u = F(s)$ and $K$ is non-singular. Differentiating the state equation gives $K \, u' = F' - K' u$, with primes for $\partial / \partial s_k$. So

$$ \frac{dJ}{ds_k} = \frac{\partial j}{\partial s_k} + \left(\frac{\partial j}{\partial u}\right)^T K^{-1} (F' - K' u) = \frac{\partial j}{\partial s_k} + \lambda^T \left(F' - K' u\right), \qquad K^T \lambda = \frac{\partial j}{\partial u}. $$

The vector $\lambda$ does not depend on $k$. So one adjoint solve gives the gradient with respect to all design variables, while finite differences need one extra state solve per variable. For the compliance $J = F^T u$ with a symmetric $K$, $\lambda = u$, and $dJ/ds_k = 2 u^T F' - u^T K' u$. The compliance is *self-adjoint*.

**The derivative of the stiffness.** The geometry map is $x(\xi) = \sum_j R_j(\xi) Q_j$ (for fixed weights), so $\partial x / \partial Q_{j,a} = R_j(\xi) e_a$ and $\partial (\partial x / \partial \xi) / \partial Q_{j,a} = e_a \otimes \nabla_\xi R_j$. The element stiffness depends on $Q$ only through the Jacobian of this map, so $K'$ follows exactly, element by element, over the elements in the support of $R_j$, as Qian (2010) derives in full, including the weights. No mesh velocity has to be approximated, because the mesh is the spline map. Semi-analytical variants take finite differences of the element matrices instead, as Kiendl and coauthors (2014) do for shells.

**Step L6, the optimizer.** Common choices are sequential quadratic programming and the method of moving asymptotes, with the [KKT conditions](/kkt-conditions/) as the stopping test. A plain step along the negative gradient, as in [gradient descent](/gradient-descent/), also works for small problems.

## Classic examples

**A bar defined by a quadratic B-spline.** Take the bar $(0, L)$ with $-u'' = 1$, $u(0) = 0$ and a free end, so $u = L x - x^2 / 2$ and the compliance is $C = \int_0^L u \, dx = L^3 / 3$. Let the geometry be one quadratic Bézier element with the control points $(0, P_1, P_2)$, so $L = P_2$, and use the same basis for $u$. A short script computes the discrete compliance $C_h$, its adjoint gradient by the formula above, and central differences:

| $P_1$ | $C_h$ | $dC_h / dP_1$ | $dC_h / dP_2$ |
|---|---|---|---|
| 0.5 | 0.3333333 | 0.0000000 | 1.0000000 |
| 0.3 | 0.3251737 | 0.0833415 | 0.9505187 |
| 0.7 | 0.3251737 | −0.0833415 | 1.0338601 |

The adjoint and the finite difference values agree to the 8 digits shown. For $P_1 = \tfrac12$ the map is linear, the exact solution is in the space, and the gradient $dC/dL = L^2 = 1$ is exact. For $P_1 \ne \tfrac12$ the domain is the same, but the map is not linear, so the basis in $x$ is not polynomial and the discrete compliance changes. The interior control point $P_1$ does not change the shape, yet it has a nonzero gradient. This is the pitfall of the next paragraph.

**The optimizer can exploit the discretization error.** For a symmetric positive definite problem with loads that do not depend on $u$, $C = a(u, u)$ and $C_h = a(u_h, u_h)$, and Galerkin orthogonality $a(u - u_h, u_h) = 0$ gives

$$ C = C_h + a(u - u_h, u - u_h), \qquad \text{so} \qquad C_h = C - \|u - u_h\|_E^2 \le C . $$

So if the design variables include control points that only change the parameterization, minimizing $C_h$ over them maximizes the discretization error, with no change of the shape. In the table, moving $P_1$ from $0.5$ to $0.3$ lowers $C_h$ by $0.0082$, which is exactly the squared energy error of the distorted map. Keep such control points out of the design variables, or tie them to the boundary by a fixed linear rule.

**A plate with a hole.** The hole in a large plate under the remote stresses $S_1$ along $x$ and $S_2$ along $y$, with $0 < S_2 \le S_1$, is a common test because the answer is known in closed form. For an elliptic hole with the semi-axes $a$ along $x$ and $b$ along $y$, Inglis's solution gives the hoop stress $S_2 (1 + 2a/b) - S_1$ at the ends of the $a$ axis and $S_1 (1 + 2b/a) - S_2$ at the ends of the $b$ axis. They are equal when $a / b = S_1 / S_2$, and then both are $S_1 + S_2$. This ellipse is the classical hole with a constant hoop stress along its edge. An isogeometric optimization of the hole that minimizes the peak stress should approach it.

**Shells.** Kiendl and coauthors (2014) optimize the shape of [isogeometric Kirchhoff-Love shells](/isogeometric-kirchhoff-love-shell/), where the control points of the midsurface are both the design variables and the analysis unknowns of the geometry. They weight the sensitivities so that the result does not depend on how densely the control points are placed.

## Variations

- **Design variables.** Control point positions only, positions and weights, or the coefficients of a few shape modes built from the control points.
- **Gradients.** Analytical (Qian 2010), semi-analytical by finite differences of element matrices, or [automatic differentiation](/automatic-differentiation/) of the assembly code.
- **Objectives.** Compliance, peak or aggregated stress (a $p$-norm of the stress), eigenfrequencies, or the drag of a body in a flow, each with its own adjoint equation.
- **Solids.** The inner control points of a volume patch move with the boundary by a linear rule, by a pseudo-elastic smoothing of the control net, or as extra variables with a quality constraint.
- **Multi-patch and trimmed models.** Shared control points keep patches conforming, and trimmed models use the methods of [trimmed isogeometric analysis](/trimmed-isogeometric-analysis/) for the analysis.

## Pitfalls

- **Exploiting the discretization.** As shown above, variables that only change the parameterization have gradients that come from the discretization error. Leave them out or tie them to the boundary.
- **An invalid map.** Large steps can make $\det J$ negative inside a patch. Use move limits, add the Bernstein coefficients of $\det J$ as constraints, or reparameterize between steps.
- **Wavy boundaries.** With many control points as variables, the optimizer can produce oscillating boundaries that the analysis does not resolve. Use a coarse design model, a smoothing of the gradient, or a sensitivity weighting.
- **The analysis level.** An optimum on a coarse analysis model can be far from the optimum of the real problem. Refine the analysis (L2) until the optimum stops moving.
- **Weights.** The map is rational in the weights, so derivatives with respect to them are nonlinear and weights must stay positive. Many codes keep the weights fixed.
- **Topology.** The method cannot create holes. Start from a topology found by [topology optimization](/topology-optimization/) or the [level set method](/level-set-topology-optimization/) if the right one is not known.

## Exercises

1. Derive the adjoint formula $dJ/ds = \partial j/\partial s + \lambda^T (F' - K' u)$ with $K^T \lambda = \partial j / \partial u$, and count the linear solves for $n$ design variables, against central finite differences.
2. Show that for the compliance $J = F^T u$ with a symmetric $K$, $\lambda = u$, and that for loads that do not depend on $s$, $dJ/ds_k = -u^T K' u \le 0$ whenever $K'$ is positive semi-definite.
3. Prove $C_h = C - \|u - u_h\|_E^2$ from Galerkin orthogonality.
4. Using the Inglis values above, show that the hoop stresses at the two ends of the axes are equal if and only if $a / b = S_1 / S_2$. What happens as $S_2 \to 0$?
5. For one quadratic Bézier element with the control points $(0, P_1, P_2)$, show that the map is linear if and only if $P_1 = P_2 / 2$, and compute $\partial x' / \partial P_1$.

## References
