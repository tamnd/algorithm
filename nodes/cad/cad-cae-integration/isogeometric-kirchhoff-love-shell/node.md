---
tag: GD768N
kind: model
slug: isogeometric-kirchhoff-love-shell
name: Isogeometric Kirchhoff-Love shell
aliases:
- rotation-free isogeometric shell
area: cad/cad-cae-integration
level: research
summary: Kiendl and coauthors' thin shell model that uses the C1 continuity of splines to discretise curvature directly, with only displacement unknowns.
prereqs: [isogeometric-analysis, nurbs, fundamental-forms]
see_also: [subdivision-shell-elements, k-refinement, nurbs-approximation-estimates, trimmed-isogeometric-analysis, surface-curvature, galerkin-method, bezier-extraction, isogeometric-collocation]
sources:
  - paper: doi:10.1016/j.cma.2009.08.013
    title: J. Kiendl, K.-U. Bletzinger, J. Linhard and R. Wüchner, Isogeometric shell analysis with Kirchhoff-Love elements, Computer Methods in Applied Mechanics and Engineering 198(49-52), 2009, 3902 to 3914
    locator: the whole paper (the kinematics with the metric and the curvature of the NURBS midsurface, the strains, the discrete equations with displacement unknowns only, and the benchmark tests)
  - paper: doi:10.1016/j.cma.2010.03.029
    title: J. Kiendl, Y. Bazilevs, M.-C. Hsu, R. Wüchner and K.-U. Bletzinger, The bending strip method for isogeometric analysis of Kirchhoff-Love shell structures comprised of multiple patches, Computer Methods in Applied Mechanics and Engineering 199(37-40), 2010, 2403 to 2416
    locator: the bending strips, which add a bending stiffness across patch interfaces where the spline basis is only C0
  - paper: doi:10.1002/(SICI)1097-0207(20000430)47:12<2039::AID-NME872>3.0.CO;2-1
    title: F. Cirak, M. Ortiz and P. Schröder, Subdivision surfaces, a new paradigm for thin-shell finite-element analysis, International Journal for Numerical Methods in Engineering 47(12), 2000, 2039 to 2072
    locator: the same rotation-free Kirchhoff-Love model on Loop subdivision surfaces, nine years before the NURBS form
  - paper: doi:10.1016/j.cma.2012.10.018
    title: R. Echter, B. Oesterle and M. Bischoff, A hierarchic family of isogeometric shell finite elements, Computer Methods in Applied Mechanics and Engineering 254, 2013, 170 to 180
    locator: the comparison of the Kirchhoff-Love form with shear deformable forms, and membrane locking of low degree elements
---

The isogeometric Kirchhoff-Love shell, from Kiendl, Bletzinger, Linhard and Wüchner (2009), models a thin shell by its midsurface, and it uses the [NURBS](/nurbs/) surface of the CAD model as that midsurface. The unknowns are the three displacement components of each control point, and there are no rotation unknowns. The membrane strain is the change of the first fundamental form of the surface, and the bending strain is the change of the second fundamental form, see [fundamental forms](/fundamental-forms/). The second fundamental form holds second derivatives of the position, so the bending energy holds second derivatives of the displacement. A finite energy then requires a displacement that is $C^1$, which the standard $C^0$ [finite element](/finite-element-method/) basis does not give and which a spline of degree $p \ge 2$ gives inside a patch. That is the main use of the smoothness of [isogeometric analysis](/isogeometric-analysis/) in structural mechanics. The page states the model, its assumptions, why the basis must be $C^1$, and its relation to other shell models.

## The machine

The "machine" of a shell model is its representation of the shell and its assumptions about the deformation.

**The representation.** The reference midsurface is a NURBS patch $X(\theta^1, \theta^2) = \sum_A R_A(\theta) X_A$ with control points $X_A$ and rational basis functions $R_A$ of degree $p$ in each direction. The covariant base vectors are $A_\alpha = X_{,\alpha}$ for $\alpha = 1, 2$, and the unit normal is $A_3 = A_1 \times A_2 / |A_1 \times A_2|$. The metric (first fundamental form) and the curvature (second fundamental form) have the coefficients

$$ A_{\alpha\beta} = A_\alpha \cdot A_\beta, \qquad B_{\alpha\beta} = A_{\alpha,\beta} \cdot A_3 = X_{,\alpha\beta} \cdot A_3. $$

The displacement uses the same basis, $u(\theta) = \sum_A R_A(\theta) u_A$, with three unknowns $u_A \in \mathbb{R}^3$ per control point. The current midsurface is $x = X + u$, with base vectors $a_\alpha$, normal $a_3$, metric $a_{\alpha\beta}$ and curvature $b_{\alpha\beta}$, computed by the same formulas.

**Assumptions.** The model takes these as given.

- **Kirchhoff-Love kinematics.** A straight fiber normal to the midsurface stays straight, normal to the deformed midsurface and of the same length. So there is no transverse shear strain, and the normal $a_3$ follows from the midsurface alone, which is why no rotation unknowns are needed.
- **Thin shell.** The thickness $t$ is small against the radii of curvature and the length of the shell. Transverse shear matters when $t$ is not small, and then the model is not valid.
- **Plane stress.** The normal stress through the thickness is zero.
- **Material.** Linear elastic in the strains below (Saint Venant-Kirchhoff). The strains are small, and the displacements and rotations can be large.
- **A regular midsurface.** $A_1 \times A_2 \ne 0$ on the whole patch, so the normal and the curvature are defined.
- **A $C^1$ basis.** Inside a patch the degree is $p \ge 2$ and each interior knot has multiplicity at most $p - 1$, so the basis is at least $C^1$. Across a patch interface, $C^1$ is not given and must be added, see Known results in the model.
- **Boundary conditions.** A simple support fixes the displacement of the boundary control points. A clamped edge also fixes the normal rotation, which here is a condition on the derivative of $u$: for a fixed clamped edge and an open knot vector, it holds when the displacements of the first two rows of control points at the edge are fixed.

## What it counts

The model measures the deformation by two strain tensors and counts the strain energy. The membrane strain and the change of curvature are

$$ \varepsilon_{\alpha\beta} = \tfrac12 (a_{\alpha\beta} - A_{\alpha\beta}), \qquad \kappa_{\alpha\beta} = B_{\alpha\beta} - b_{\alpha\beta}, $$

which Kiendl and coauthors use with large displacements. A point at the distance $\theta^3 \in [-t/2, t/2]$ from the midsurface on the normal has the strain $\varepsilon_{\alpha\beta} + \theta^3 \kappa_{\alpha\beta}$, to first order in $\theta^3$.

For a linear elastic material with the plane stress tensor $\mathbb{C}$ in the curvilinear frame and thickness $t$, integration through the thickness gives the strain energy

$$ \Pi_{\text{int}} = \frac12 \int_{\Omega} \Big( t \, \varepsilon : \mathbb{C} : \varepsilon + \frac{t^3}{12} \, \kappa : \mathbb{C} : \kappa \Big) \, dA. $$

The discrete equations are the stationary conditions of $\Pi_{\text{int}}$ minus the work of the loads, with respect to the control point displacements, solved by Newton's method for large displacements. They are a [Galerkin method](/galerkin-method/) for the shell equations. The cost per patch is that of a Galerkin system with $3 n$ unknowns for $n$ control points, three fifths of the $5 n$ of a shell with two rotations per node.

## Relation to other models

- **Reissner-Mindlin shells** have three displacements and two rotations per node, a transverse shear strain, and only first derivatives in the energy, so a $C^0$ basis is enough. They suffer from shear locking when $t$ is small. The Kirchhoff-Love model is their limit as $t / L \to 0$, and it has no shear locking because it has no shear strain.
- **[Subdivision shell elements](/subdivision-shell-elements/)** of Cirak, Ortiz and Schröder (2000) use the same rotation-free Kirchhoff-Love model nine years earlier, with Loop subdivision surfaces in place of NURBS. Their basis is smooth on closed surfaces of any topology, but CAD models are not stored in that form.
- **Classical plate and shell elements.** $C^1$ triangles such as Argyris elements exist but need high degree and many unknowns per node, and "discrete Kirchhoff" elements apply the Kirchhoff condition only at points. The spline basis gives $C^1$ inside a patch at no extra cost.
- **Kirchhoff plates.** For a flat midsurface and small displacements, the bending part is the Kirchhoff plate equation $D \Delta^2 w = q$ with $D = E t^3 / (12 (1 - \nu^2))$, and the membrane part decouples.
- **[Trimmed patches](/trimmed-isogeometric-analysis/).** Real CAD shells are trimmed and are made of many patches, so the model needs the trimmed and the multi-patch techniques of that page and of the bending strip method below.

## Known results in the model

**The bending energy needs $C^1$ (1D lemma).** Let $v$ be a continuous, piecewise polynomial function on a partition $a = x_0 < x_1 < \cdots < x_m = b$. Then $v$ has a second derivative in $L^2(a, b)$, that is $v \in H^2(a, b)$, if and only if $v'$ is continuous at every $x_k$.

*Proof.* Write $J_k = v'(x_k^+) - v'(x_k^-)$ for the jump of $v'$ at an interior node. For a smooth test function $\varphi$ that vanishes near $a$ and $b$, integration by parts on each piece gives

$$ \int_a^b v' \varphi' \, dx = -\int_a^b v''_{\text{pw}} \varphi \, dx - \sum_{k=1}^{m-1} J_k \varphi(x_k), $$

where $v''_{\text{pw}}$ is the second derivative taken piece by piece, a bounded function. So the weak second derivative of $v$ is $v''_{\text{pw}} + \sum_k J_k \delta_{x_k}$. If all $J_k = 0$, it is the bounded function $v''_{\text{pw}}$, and $v \in H^2$. If some $J_k \ne 0$, suppose it were equal to a function $g \in L^2$. Take $\varphi_\epsilon$ with $\varphi_\epsilon(x_k) = 1$, $0 \le \varphi_\epsilon \le 1$ and support in $(x_k - \epsilon, x_k + \epsilon)$. Then $|\int (g - v''_{\text{pw}}) \varphi_\epsilon| \le \|g - v''_{\text{pw}}\|_{L^2(x_k - \epsilon, x_k + \epsilon)} \sqrt{2 \epsilon} \to 0$, while the Dirac part gives $J_k \ne 0$ for each $\epsilon$. This is a contradiction, so $v \notin H^2$. $\square$

The same argument works across an edge $e$ of a 2D mesh: integration by parts leaves the term $\int_e [\partial_i v] \, n_j \varphi \, ds$ with the jump $[\partial_i v]$ of the gradient, and a test function concentrated near $e$ shows that it is not given by an $L^2$ function unless the jump is zero. In the shell, the change of curvature $\kappa_{\alpha\beta}$ holds $u_{,\alpha\beta} \cdot a_3$, so the bending energy $\frac{t^3}{24} \int \kappa : \mathbb{C} : \kappa \, dA$ is finite for all displacements of the discrete space only if they are $C^1$. A $C^0$ basis makes the energy infinite, or, if one integrates the curvature only inside the elements, it drops the energy of the kinks at the element edges, and the result is not a conforming method. A spline of degree $p$ is $C^{p - m}$ at a knot of multiplicity $m$, so $p \ge 2$ and $m \le p - 1$ give $C^1$ inside a patch. This is why the rotation-free form needs at least quadratic splines and simple enough knots, and why it cannot use the $C^0$ Lagrange basis.

**Across patches.** At a patch interface with matching knots and control points the basis is only $C^0$, and the lemma says that the bending energy of the kink is lost: the interface acts as a hinge. Kiendl, Bazilevs, Hsu, Wüchner and Bletzinger (2010) add *bending strips*, narrow fictitious patches across each interface that carry bending stiffness only, which restores the rotation coupling in a penalty sense. Other ways are a $G^1$ or $C^1$ construction of the multi-patch basis, and weak coupling with a Nitsche type term, which adds an interface integral of the averaged bending moment times the jump of rotation and a penalty on that jump.

**Error.** For a well-posed linear problem the Galerkin error in the energy norm is at most a constant times the best approximation error in that norm (Céa's lemma). The energy norm of bending is an $H^2$ norm, and splines of degree $p$ approximate a smooth function with an error $O(h^{p-1})$ in $H^2$, see [NURBS approximation estimates](/nurbs-approximation-estimates/). So the expected order in the energy norm is $p - 1$ for smooth solutions. This is a statement about the linear plate and shell problems that are coercive, and it is not proved here for curved shells.

**A check value.** For a simply supported square plate of side $a$ under a uniform load $q$, the Navier series gives the center deflection

$$ w_c = \frac{16 q a^4}{\pi^6 D} \sum_{m, n \text{ odd}} \frac{\sin(m \pi / 2) \sin(n \pi / 2)}{m n (m^2 + n^2)^2} \approx 0.0040624 \, \frac{q a^4}{D}, $$

where the value comes from summing the series over $m, n < 400$. The flat form of the model is the Kirchhoff plate, so this is a check for the bending part.

**Locking.** The model has no shear locking. With low degree on curved shells it can show membrane locking, a too stiff answer when the bending deformation needs membrane strain to be zero at many points. Echter, Oesterle and Bischoff (2013) report it for low degree isogeometric shells and propose mixed forms. Higher degree reduces it.

**Benchmarks.** Kiendl and coauthors (2009) report results for linear benchmark tests of thin shells and for large deformation tests. These are numerical results.

## References
