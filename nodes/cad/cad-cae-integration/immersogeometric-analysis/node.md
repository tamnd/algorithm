---
tag: Q57GZX
kind: technique
slug: immersogeometric-analysis
name: Immersogeometric analysis
aliases:
- immersogeometric method
area: cad/cad-cae-integration
level: research
summary: Kamensky and coauthors' immersed method that keeps the exact CAD boundary inside a non-conforming background mesh, for fluid-structure interaction.
prereqs: [isogeometric-analysis, finite-cell-method, b-spline]
see_also: [trimmed-isogeometric-analysis, cut-finite-element-method, isogeometric-kirchhoff-love-shell, augmented-lagrangian-method, navier-stokes-equations, adaptive-quadrature, signed-distance-function, nurbs]
sources:
  - paper: doi:10.1016/j.cma.2014.10.040
    title: D. Kamensky, M.-C. Hsu, D. Schillinger, J. A. Evans, A. Aggarwal, Y. Bazilevs, M. S. Sacks and T. J. R. Hughes, An immersogeometric variational framework for fluid-structure interaction, application to bioprosthetic heart valves, Computer Methods in Applied Mechanics and Engineering 284, 2015, 1005 to 1053
    locator: the whole paper (the name and the idea, the spline background mesh for the fluid, the isogeometric shell for the leaflets, the weak kinematic constraint on the shell surface, and the heart valve simulations)
  - paper: doi:10.1016/j.compfluid.2015.08.027
    title: F. Xu, D. Schillinger, D. Kamensky, V. Varduhn, C. Wang and M.-C. Hsu, The tetrahedral finite cell method for fluids, immersogeometric analysis of turbulent flow around complex geometries, Computers and Fluids 141, 2016, 135 to 154
    locator: the whole paper, the immersogeometric idea for solid bodies in flow, with adaptive integration of cut cells against the exact boundary and weak boundary conditions
  - paper: doi:10.1007/s11831-014-9115-y
    title: D. Schillinger and M. Ruess, The finite cell method, a review in the context of higher-order structural analysis of CAD and image-based geometric models, Archives of Computational Methods in Engineering 22(3), 2015, 391 to 455
    locator: the parts on CAD models in the finite cell method and on weak boundary conditions, which immersogeometric analysis builds on
  - paper: doi:10.1017/S0962492902000077
    title: C. S. Peskin, The immersed boundary method, Acta Numerica 11, 2002, 479 to 517
    locator: the whole survey, the classical immersed boundary method with a regularized delta function, against which the immersogeometric method is set
---

Immersogeometric analysis computes a flow, or a fluid-structure interaction, on a background mesh that does not fit the body, while it represents the body by its exact CAD or spline surface. The background mesh is usually a spline mesh of a box, as in [isogeometric analysis](/isogeometric-analysis/). The surface of the body is used directly: its own spline parameterization places the quadrature points of the boundary terms, and an inside test against the same surface decides which points of a cut background element count. The boundary conditions are imposed weakly on that surface. Kamensky and coauthors (2015) coined the name for the simulation of heart valves, where thin leaflets modeled as an [isogeometric Kirchhoff-Love shell](/isogeometric-kirchhoff-love-shell/) move through a fixed fluid mesh. It differs from the other immersed methods of this site by keeping the CAD boundary itself, exactly, inside a background spline mesh: the [finite cell method](/finite-cell-method/) can use any inside test and puts a small stiffness $\alpha$ in the void, [CutFEM](/cut-finite-element-method/) stabilizes the cut elements with a ghost penalty, and [trimmed isogeometric analysis](/trimmed-isogeometric-analysis/) cuts the CAD patches themselves, with no background mesh.

## In plain words

To compute air flowing around a car, or blood flowing through a heart valve, the usual way is to build a mesh that fills the space around the body and follows its surface. For a moving valve, that mesh must be rebuilt as the valve opens and closes, which is slow and breaks easily.

This method uses a fixed grid for the fluid that ignores the body. The body is kept as the exact smooth surface that the design software made. Where the body touches the fluid, the method adds terms to the equations that make the fluid stick to the surface. These terms are computed at sample points spread over the true surface, not over a rough copy of it. When the body moves, only the sample points move, and the grid stays.

## When it applies

- The body is given as a spline or CAD surface, for example a [NURBS](/nurbs/) or T-spline model, and it is hard or costly to mesh the space around it, often because the body moves or deforms a lot.
- The physics is posed in weak form on a background domain, typically the incompressible [Navier-Stokes equations](/navier-stokes-equations/) for the fluid, so that interface conditions can be added as surface integrals.
- For fluid-structure interaction, the structure has its own discretization on the same surface, such as a rotation-free shell, so that the structure and the interface share one geometry.
- The accuracy near the surface matters, so the geometry error of a faceted or voxel boundary is not acceptable.

## The template

```pseudo id=main
IMMERSOGEOMETRIC(background box B with spline basis, body surface Γ with its spline map, weak form)
L1  build the spline basis on a mesh of B that ignores Γ
L2  place the boundary quadrature points by the spline map of Γ: Gauss points of each element of Γ, mapped to space
L3  find for each boundary quadrature point the background element that holds it
L4  classify the background elements as fluid, body or cut by inside tests against Γ (not needed for a thin shell)
L5  integrate the cut elements adaptively, keeping only the quadrature points on the fluid side of Γ
L6  add the interface terms on Γ at the points of L2: Nitsche, penalty or augmented Lagrangian terms
L7  for fluid-structure interaction, couple with the structure equations discretized on Γ
L8  assemble and solve; for a moving body, move Γ and repeat L2 to L6 on the same background mesh
```

**Step L2, the boundary quadrature.** This is the step that gives the method its name. The boundary integrals of L6 run over $\Gamma$, and $\Gamma$ is a spline surface $S(\xi, \eta)$. A Gauss rule on each element of $S$, with the weights times $|S_\xi \times S_\eta|$, integrates over the exact surface. In a classical immersed boundary method the body is a cloud of points with a smeared delta function, and in many fictitious domain codes the boundary is a set of facets or voxels.

**Step L5, cut elements.** For a solid body the fluid fills only the outside of $\Gamma$. A background element cut by $\Gamma$ is integrated by recursive bisection toward $\Gamma$, as in the [finite cell method](/finite-cell-method/) and [adaptive quadrature](/adaptive-quadrature/), with the exact surface in the inside test. For a thin structure such as a valve leaflet, the fluid lies on both sides, so the volume integrals run over all of $B$, and only the surface terms of L6 see the structure.

**Step L6, the weak interface conditions.** For the no-slip condition $u = u_\Gamma$ on $\Gamma$ (the fluid velocity $u$ equals the velocity of the body), Nitsche's method adds to the weak form, for a test function $w$,

$$ - \int_\Gamma w \cdot (\sigma(u, p) n) \, ds - \int_\Gamma (\sigma(w, q) n) \cdot (u - u_\Gamma) \, ds + \frac{\beta}{h} \int_\Gamma w \cdot (u - u_\Gamma) \, ds, $$

where $\sigma$ is the fluid stress and $n$ the normal of $\Gamma$. The first term is the traction from integration by parts, the second vanishes for the exact solution and makes the form symmetric (up to the sign convention for $q$), and the last, with $\beta > 0$, gives stability. Nitsche's method is defined on the [trimmed analysis](/trimmed-isogeometric-analysis/) page for the Laplace equation. Kamensky and coauthors use an augmented Lagrangian instead, a penalty term plus a Lagrange multiplier field on $\Gamma$ that stands for the traction the fluid puts on the shell, with the same idea as the [augmented Lagrangian method](/augmented-lagrangian-method/) of optimization, applied to a constraint on a surface.

## Classic examples

**Heart valves.** Kamensky and coauthors (2015) simulate bioprosthetic aortic valves over full heart cycles. The leaflets are isogeometric Kirchhoff-Love shells, the blood is on a fixed spline mesh of the vessel, and the leaflets open, close and touch each other. A mesh that follows the leaflets would have to be rebuilt many times per cycle, and the leaflets nearly touch when the valve closes, which makes a fitted fluid mesh very hard.

**Why the exact boundary matters.** Replace a circle of radius $R$ by a polygon with $N$ sides of length $h \approx 2\pi R / N$. Each side misses the arc by its sagitta $R - \sqrt{R^2 - h^2/4} \approx h^2 / (8R)$, and the polygon misses the area

$$ \pi R^2 - \frac{N}{2} R^2 \sin \frac{2\pi}{N} \approx \frac{2\pi^3 R^2}{3 N^2} = \frac{\pi h^2}{6} . $$

For $R = 1$ and $N = 16$ the area error is $0.0801$, against $0.0807$ from the formula. A boundary condition imposed on the polygon is imposed up to $h^2 / (8R)$ away from the true boundary. As a model, not a theorem: a prescribed value is then off by about that distance times the gradient of the solution, which is of order $h^2$ for every degree $p$, while a degree $p$ basis can reach a pointwise error of order $h^{p+1}$. The geometry, not the basis, limits the accuracy. Immersogeometric analysis removes this term by using the exact surface in L2 and L5. Xu and coauthors (2016) report that the accurate representation of the geometry in the cut elements is what makes their immersed results for turbulent flow close to those on fitted meshes.

**Flow around complex bodies.** Xu and coauthors (2016) apply the idea to turbulent flow around solid bodies on tetrahedral background meshes, with adaptive integration of the cut elements and weak no-slip conditions. The background mesh there is a standard finite element mesh, which shows that the defining part of the method is the exact boundary, not the spline background.

## Variations

- **The background basis.** B-splines on a box, hierarchical splines refined near the body, or tetrahedral finite elements.
- **The interface condition.** Nitsche terms, a penalty only, or an augmented Lagrangian with the multiplier on the body surface.
- **Time stepping for moving bodies.** A semi-implicit or staggered coupling of the fluid and the structure, with the background mesh fixed and the quadrature points of L2 moving with the body.
- **The thin and the solid case.** Thin shells need no cut cell integration, since the fluid is on both sides. Solid bodies need L4 and L5 and the small cut care of the [finite cell method](/finite-cell-method/) or [CutFEM](/cut-finite-element-method/).
- **Contact.** Leaflets that touch need a contact model on the shell surfaces, separate from the fluid coupling.

## Pitfalls

- **Discontinuities across thin structures.** The pressure jumps across a thin leaflet, and the velocity gradient has a kink there, but a continuous background basis is smooth across the leaflet. The solution is smeared over about one background element on each side, and quantities such as the mass flux through a closed valve can leak. Refine the background mesh near the structure.
- **The penalty size.** A penalty or Nitsche parameter that is too small lets the fluid slip through the surface, and one that is too large makes the system stiff. It depends on the background element size, not on the size of the surface elements.
- **Point location.** Each boundary quadrature point must be found in the background mesh, at every step for a moving body. On a box with a uniform spline mesh this is a division, but on unstructured or refined meshes it needs a search structure.
- **Small cuts.** For solid bodies, background elements with a tiny fluid part make the system ill conditioned, as on the trimmed analysis page. They need stabilization.
- **Two resolutions.** The surface quadrature must be fine enough relative to the background mesh. If the surface elements are much larger than the background elements, some background functions near $\Gamma$ see no quadrature point, and the constraint does not act on them.

## Exercises

1. Show that the sagitta of a chord of length $h$ in a circle of radius $R$ is $R - \sqrt{R^2 - h^2/4}$, and that it is $h^2/(8R) + O(h^4/R^3)$.
2. Compute the area error of the inscribed regular polygon with 16 sides in the unit circle, and compare it with $\pi h^2 / 6$. *Answer:* $\pi - 8 \sin(\pi/8) \approx 0.0801$, with $h = 2 \sin(\pi/16) \approx 0.390$ and $\pi h^2/6 \approx 0.0797$.
3. A valve leaflet is a thin shell with fluid on both sides. Explain why the volume integrals of the fluid need no cut cell rule, and which integrals still see the leaflet.
4. Show that the Nitsche terms of Step L6 vanish for the exact solution, in the sense that the weak form with them still holds when $u = u_\Gamma$ on $\Gamma$ and the first term is the true traction.
5. The surface $\Gamma$ has elements of size $H$ and the background mesh has elements of size $h$. With $G$ Gauss points per direction on each surface element, give a condition on $H$, $h$ and $G$ such that each background element cut by $\Gamma$ holds at least one boundary quadrature point. *Hint:* the spacing of the points on $\Gamma$ is about $H / G$.

## References
