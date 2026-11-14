---
tag: 2SYWEW
kind: technique
slug: cut-finite-element-method
name: Cut finite element method
aliases:
- CutFEM
area: cad/cad-cae-integration
level: research
summary: Burman and coauthors' method that cuts a background mesh by the boundary, adds ghost penalty terms for stability and imposes conditions by Nitsche's method.
prereqs: [finite-element-method, galerkin-method, level-set-method]
see_also: [finite-cell-method, immersogeometric-analysis, trimmed-isogeometric-analysis, condition-number, signed-distance-function, poisson-equation, isogeometric-analysis, adaptive-quadrature]
sources:
  - paper: doi:10.1016/j.crma.2010.10.006
    title: E. Burman, Ghost penalty, Comptes Rendus Mathématique 348(21-22), 2010, 1217 to 1220
    locator: the whole note, which introduces the ghost penalty for fictitious domain methods
  - paper: doi:10.1016/j.apnum.2011.01.008
    title: E. Burman and P. Hansbo, Fictitious domain finite element methods using cut elements, II. A stabilized Nitsche method, Applied Numerical Mathematics 62(4), 2012, 328 to 341
    locator: the analysis of the method with Nitsche's conditions and the ghost penalty on the faces of the cut elements, for piecewise linear elements (coercivity with constants independent of the cut, a priori error estimates and the bound on the condition number)
  - paper: doi:10.1002/nme.4823
    title: E. Burman, S. Claus, P. Hansbo, M. G. Larson and A. Massing, CutFEM, discretizing geometry and partial differential equations, International Journal for Numerical Methods in Engineering 104(7), 2015, 472 to 501
    locator: the whole paper (the name, the general framework, the ghost penalty for higher degree elements, and applications to interfaces, surfaces and moving domains)
  - paper: doi:10.1016/S0045-7825(02)00524-8
    title: A. Hansbo and P. Hansbo, An unfitted finite element method, based on Nitsche's method, for elliptic interface problems, Computer Methods in Applied Mechanics and Engineering 191(47-48), 2002, 5537 to 5552
    locator: the whole paper, the unfitted Nitsche method on cut elements that CutFEM grew from
  - paper: doi:10.1007/BF02995904
    title: J. Nitsche, Über ein Variationsprinzip zur Lösung von Dirichlet-Problemen bei Verwendung von Teilräumen, die keinen Randbedingungen unterworfen sind, Abhandlungen aus dem Mathematischen Seminar der Universität Hamburg 36, 1971, 9 to 15
    locator: the weak imposition of Dirichlet conditions that is now called Nitsche's method
---

The cut finite element method (CutFEM) solves a boundary value problem on a domain $\Omega$ with a standard finite element space on a fixed background mesh that $\Omega$ cuts in an arbitrary way. Every element that meets $\Omega$ is kept, the integrals are taken over the cut parts only, the boundary conditions are imposed weakly by Nitsche's method, and a *ghost penalty* on the faces near the boundary restores the stability that the cut elements lose. With the ghost penalty, the error estimates and the [condition number](/condition-number/) of the system do not depend on how the boundary cuts the mesh. The boundary is most often given by a [level set](/level-set-method/) function. Burman and Hansbo built the method from the unfitted Nitsche method of Hansbo and Hansbo (2002) and the ghost penalty of Burman (2010), and Burman, Claus, Hansbo, Larson and Massing (2015) named the framework. It differs from the other immersed methods of this site by its ghost penalty: the [finite cell method](/finite-cell-method/) uses a high order basis and a small stiffness $\alpha$ in the void instead, [immersogeometric analysis](/immersogeometric-analysis/) keeps the exact CAD boundary in a background spline mesh, and [trimmed isogeometric analysis](/trimmed-isogeometric-analysis/) cuts the CAD patches themselves, with no background mesh.

## In plain words

Instead of building a mesh that follows a shape, lay a simple fixed grid over it and let the border of the shape cut through the cells wherever it falls. Each cell that touches the shape takes part, but only the part of it inside the shape counts when the energy is added up.

The trouble is the cells that the border only grazes. A cell with a tiny piece inside the shape has almost no say in the equations, so its unknowns are barely tied down, and the equations become very hard to solve. The fix is a ghost penalty: an extra term on the cell sides near the border that asks the solution to bend smoothly from one cell into the next. Then a grazed cell borrows its stability from its full neighbors, wherever the border falls.

## When it applies

- The domain is given implicitly, by a level set function $\phi$ with $\Omega = \{\phi < 0\}$, or by any inside test, and a fitted mesh is costly or changes often, as for moving interfaces, two phase flow, fracture or [topology optimization](/topology-optimization/).
- The problem is in weak form, so the boundary conditions can be imposed by integrals on the cut boundary.
- A standard Lagrange finite element space on a simplex or box mesh is wanted, with the same assembly code as a fitted method.
- The user needs guarantees: a priori error estimates and condition numbers that hold for every position of the boundary.

## The template

```pseudo id=main
CUTFEM(background mesh T of a box around Ω, level set φ, weak form)
L1  keep the active elements T_h = {K ∈ T : K ∩ Ω ≠ ∅}; take the finite element space V_h on T_h
L2  for each cut element K: find Γ ∩ K, for example as the zero set of the interpolant of φ
L3  integrate the bulk terms over K ∩ Ω only
L4  add the Nitsche terms on Γ ∩ K for the boundary conditions
L5  collect the ghost faces F_G: the interior faces of T_h that belong to an element cut by Γ
L6  add the ghost penalty on the faces of F_G
L7  assemble and solve
```

For the model problem $-\Delta u = f$ in $\Omega$, $u = g$ on $\Gamma = \partial\Omega$ (the [Poisson equation](/poisson-equation/)), with continuous piecewise polynomials of degree $p$ on $T_h$, the method finds $u_h \in V_h$ with

$$ a_h(u_h, v) + g_h(u_h, v) = \int_\Omega f v - \int_\Gamma g \, \partial_n v + \frac{\gamma}{h} \int_\Gamma g v \qquad \text{for all } v \in V_h, $$

$$ a_h(u, v) = \int_\Omega \nabla u \cdot \nabla v - \int_\Gamma (\partial_n u) v - \int_\Gamma u \, \partial_n v + \frac{\gamma}{h} \int_\Gamma u v . $$

$a_h$ is Nitsche's form, defined also on the [trimmed analysis](/trimmed-isogeometric-analysis/) page, with a parameter $\gamma > 0$.

**The ghost penalty.** For degree $p$ it is

$$ g_h(u, v) = \sum_{F \in F_G} \sum_{j=1}^{p} \gamma_j \, h^{2j-1} \int_F [\partial_n^j u] \, [\partial_n^j v] \, ds, $$

where $[\partial_n^j u]$ is the jump of the $j$-th normal derivative across the face $F$ and $\gamma_j > 0$ are parameters. For piecewise linear elements only $j = 1$ is there: $g_h(u, v) = \gamma_1 \sum_F h \int_F [\partial_n u][\partial_n v] \, ds$. The exact solution is smooth, so its jumps are zero and the term does not change the consistency of the method.

**What it controls.** The ghost penalty extends the control of the bulk energy from the physical part $\Omega$ to the whole active mesh: there is a constant $C$ that depends on the shape of the elements and on $\gamma_j$, but not on how $\Gamma$ cuts the mesh, with

$$ \|\nabla v\|^2_{L^2(\Omega_h)} \le C \left( \|\nabla v\|^2_{L^2(\Omega)} + g_h(v, v) \right) \qquad \text{for all } v \in V_h, $$

where $\Omega_h$ is the union of the active elements. From this follow three results that hold uniformly in the position of the cut: (1) the form $a_h + g_h$ is coercive for $\gamma$ above a fixed threshold, (2) the a priori error estimates are optimal, of order $h^p$ in the energy norm, and (3) the condition number of the stiffness matrix is $O(h^{-2})$, as for a fitted mesh. Burman and Hansbo (2012) prove these for piecewise linear elements, and Burman and coauthors (2015) discuss the higher order form above. The 1D proof below shows the mechanism.

## Classic examples

**A 1D proof of the mechanism.** Take piecewise linear elements of size $h$ on $(0, \infty)$, $\Omega = (0, a)$ with $a = (k + \epsilon) h$ for an integer $k \ge 1$ and $0 < \epsilon \le 1$, $u(0) = 0$ imposed strongly, and Nitsche's condition at $a$. The last active element $K = [kh, (k+1)h]$ is cut, and only the length $\epsilon h$ of it is in $\Omega$. The ghost face is the node $kh$.

*Without the ghost penalty, the method fails for small cuts.* Let $v$ be the hat function of the node $(k+1)h$. Then $v' = 1/h$ on the inside part of $K$, $v(a) = \epsilon$, and

$$ a_h(v, v) = \frac{1}{h^2} \epsilon h - 2 \cdot \frac{1}{h} \cdot \epsilon + \frac{\gamma}{h} \epsilon^2 = \frac{\epsilon}{h} (\gamma \epsilon - 1). $$

This is negative for $\epsilon < 1/\gamma$. So for every fixed $\gamma$ some cut positions make the matrix indefinite, and $\epsilon = 1/\gamma$ makes it singular. Choosing $\gamma \sim 1/\epsilon$ restores coercivity but makes the matrix badly conditioned as $\epsilon \to 0$.

*With the ghost penalty, the bound holds for every cut.* Let $v \in V_h$, let $c$ be the slope of $v$ on $K$ and $b$ its slope on the full element to the left, which lies in $\Omega$. The jump at the ghost node is $c - b$, and $g_h(v, v) = \gamma_1 h (c - b)^2$. Then

$$ h c^2 \le 2 h b^2 + 2 h (c - b)^2 = 2 \|v'\|^2_{L^2(kh - h, kh)} + \frac{2}{\gamma_1} g_h(v, v), $$

so $\|v'\|^2_{L^2(\Omega_h)} \le C (\|v'\|^2_{L^2(\Omega)} + g_h(v, v))$ with $C = 1 + \max(2, 2/\gamma_1)$, independent of $\epsilon$. The same step bounds the boundary term: $h |v'(a)|^2 = h c^2$. For coercivity, Young's inequality with $\delta = 1/(2C')$, $C' = \max(2, 2/\gamma_1)$, gives

$$ a_h(v, v) + g_h(v, v) \ge \tfrac12 \left( \|v'\|^2_{L^2(\Omega)} + g_h(v, v) \right) + (\gamma - 2C') \frac{v(a)^2}{h}, $$

so $\gamma > 2 C'$ is enough, for every $\epsilon$. With $\gamma_1 = 1$ that means $\gamma > 4$.

*Measured.* For $h = 0.1$, $k = 5$ and $\gamma = 10$, a short script computes the eigenvalues of the stiffness matrix. Without the ghost penalty the matrix is singular at $\epsilon = 0.1$ and indefinite for $\epsilon = 0.01$ and below, as the formula says. With $\gamma_1 = 1$ the condition number is $33$, $53$, $67$, $69$ and $70$ for $\epsilon = 0.5$, $0.1$, $0.01$, $10^{-3}$ and $10^{-6}$, so it stays bounded. With $\gamma_1 = 0.1$ we have $C' = 20$ and the condition $\gamma > 40$ fails, and the matrix is indeed indefinite for $\epsilon \le 10^{-3}$.

**Interface problems.** Hansbo and Hansbo (2002) solve $-\nabla \cdot (k \nabla u) = f$ with a jump of $k$ across an interface that cuts the mesh. Each cut element carries two copies of the basis, one for each side, and Nitsche terms on the interface tie them together. This is the origin of CutFEM.

**Surface PDEs.** The same idea solves equations on a surface $\Gamma$ given by a level set, with the trace of a bulk finite element space on $\Gamma$ as the space. The ghost penalty then also controls the functions that the surface only grazes.

## Variations

- **Other ghost penalties.** Instead of jumps of derivatives on faces, penalize the difference between the polynomials of a cut element and its neighbor on their union (the patch form), or penalize the projection error onto a coarser space. All give the bound of the "What it controls" paragraph.
- **Cell agglomeration.** Merge each badly cut element with a full neighbor, so that no small cuts remain. This is the main other way to get cut-independent stability.
- **Higher order geometry.** A piecewise linear $\Gamma_h$ from the interpolant of $\phi$ gives a geometry error of order $h^2$. For $p \ge 2$, use a higher order description of the boundary or a mapping of the cut elements.
- **Spline spaces.** The same terms work with B-splines on a background box, which leads toward [immersogeometric analysis](/immersogeometric-analysis/).
- **Moving domains.** For a moving boundary the active mesh changes with time, and the ghost penalty also extends the solution into newly active elements.

## Pitfalls

- **Forgetting the ghost penalty.** Without it, a fixed Nitsche parameter fails for some cut positions, as the 1D example shows. The failure depends on the geometry and appears only for some meshes.
- **Too small a ghost parameter.** The bound depends on $\gamma_j$, and the Nitsche parameter must be large compared with $1/\gamma_1$. Too large a ghost parameter adds consistency error of high order but stiffens the solution near the boundary.
- **The faces in F_G.** Take the interior faces of the active mesh that belong to a cut element. Missing faces leave some cut elements without control.
- **Geometry error.** A piecewise linear boundary limits the error to second order, whatever the degree of the elements.
- **Quadrature on cut elements.** The integrals of L3 and L4 over curved cut parts need care. In 3D the intersection of a tetrahedron with a planar level set has several cases.

## Exercises

1. In the 1D example, show that the hat function $v$ of the last node gives $a_h(v, v) = (\epsilon / h)(\gamma \epsilon - 1)$.
2. Show that the ghost penalty term vanishes for a function that is a single polynomial of degree $p$ on the whole active mesh, and so for the smooth exact solution up to the jumps of its interpolant.
3. Prove the inequality $h c^2 \le 2 h b^2 + 2 h (c - b)^2$ and explain why it does not depend on $\epsilon$.
4. For piecewise linear elements on triangles, which faces are in $F_G$ for a circle that cuts a structured mesh? Draw them.
5. Why is the condition number of a fitted mesh stiffness matrix $O(h^{-2})$, and why can a cut element make it unbounded without stabilization? Compare with the small cut formulas on the [trimmed isogeometric analysis](/trimmed-isogeometric-analysis/) page.

## References
