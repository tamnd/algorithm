---
tag: CK9WZM
kind: definition
slug: multipole-acceptance-criterion
name: Multipole acceptance criterion
aliases:
- opening angle criterion
area: scientific-computing/n-body-and-particle-methods
level: core
summary: The rule that lets a tree code use a cell's expansion instead of opening it, such as s/d < theta for cell size s, distance d and opening angle theta.
prereqs: [multipole-expansion, octree]
see_also: [barnes-hut-algorithm, multipole-truncation-error-bound, fast-multipole-method, hashed-oct-tree, multipole-to-local-translation, adaptive-fast-multipole-method, treepm-method, direct-n-body-summation]
sources:
  - paper: doi:10.1038/324446a0
    title: "Josh Barnes and Piet Hut, A hierarchical O(N log N) force-calculation algorithm, Nature 324, 1986, 446-449"
    locator: the opening criterion l/D < theta
  - paper: doi:10.1006/jcph.1994.1050
    title: "John K. Salmon and Michael S. Warren, Skeletons from the treecode closet, Journal of Computational Physics 111(1), 1994, 136-155"
    locator: the unbounded errors of the Barnes-Hut criterion and the criteria built on error bounds
  - paper: doi:10.1111/j.1365-2966.2005.09655.x
    title: "Volker Springel, The cosmological simulation code GADGET-2, Monthly Notices of the Royal Astronomical Society 364(4), 2005, 1105-1134"
    locator: Section 3.1.1, Equation (18), the relative opening criterion
  - book: isbn:9780521432726
    title: Sverre J. Aarseth, Gravitational N-Body Simulations, Tools and Algorithms, Cambridge University Press, 2003
    locator: Chapter 6 (tree codes), Section 6.2 (basic formulation)
---

A multipole acceptance criterion (MAC) is the test that a tree code applies to a cell and a target point to decide whether the [multipole expansion](/multipole-expansion/) of the cell is accurate enough at that point. If the cell is accepted, its expansion gives its whole contribution to the force; if not, the cell is opened and its children are tested. The criterion sets both the accuracy and the cost of the [Barnes-Hut algorithm](/barnes-hut-algorithm/) and of related tree codes. The original form compares the angle under which the cell is seen with a fixed opening angle $\theta$.

## Definition

**Setting.** A tree code stores the bodies in a hierarchy of cells, such as an [octree](/octree/). Each cell $C$ has a size $s_C$ (the side of its cube), a geometric center $\mathbf{c}_C$, a total mass $M_C$, a center of mass $\mathbf{z}_C$ and the moments of its expansion about $\mathbf{z}_C$. Let $\mathbf{x}$ be the target point and $d = |\mathbf{x} - \mathbf{z}_C|$.

**Definition.** A *multipole acceptance criterion* is a predicate $\mathrm{MAC}(C, \mathbf{x})$. The tree walk for the target $\mathbf{x}$ starts at the root; a cell $C$ with $\mathrm{MAC}(C, \mathbf{x})$ true contributes its truncated expansion, a leaf with the predicate false contributes its bodies by direct summation, and any other cell with the predicate false is replaced by its children.

**The Barnes-Hut criterion.** With an opening angle $\theta > 0$ (often 0.5 to 1),

$$\mathrm{MAC}_{\mathrm{BH}}(C, \mathbf{x}) \iff \frac{s_C}{d} < \theta.$$

With $\theta = 0$ no cell is accepted, and the walk reduces to [direct summation](/direct-n-body-summation/).

**Common refinements.**

- *Offset criterion.* Let $\delta_C = |\mathbf{z}_C - \mathbf{c}_C|$ be the distance from the center of mass to the geometric center. Accept if $d > s_C / \theta + \delta_C$. This forbids the acceptance of a cell that contains the target or nearly touches it.
- *Error-bound criteria (Salmon and Warren 1994).* Let $b_C$ be the radius of the smallest ball about $\mathbf{z}_C$ that holds all bodies of $C$. A truncated expansion of degree $p$ has an a priori error bound that depends on $M_C$, $b_C$, $d$ and higher moments of $C$. Accept if the bound is below a tolerance $\Delta$. For the monopole of the potential the bound is $\frac{G M_C b_C^2}{d^2 (d - b_C)}$ for $d > b_C$ (theorem; the proof is in the [Barnes-Hut](/barnes-hut-algorithm/) proof file).
- *Relative criterion (Springel 2005).* Let $|\mathbf{a}_{\mathrm{old}}|$ be the acceleration of the target at the previous step and $\alpha$ a tolerance. Accept if $\frac{G M_C}{d^2} \left(\frac{s_C}{d}\right)^2 \le \alpha |\mathbf{a}_{\mathrm{old}}|$. The quadrupole error of a cell scales as the left side, so the criterion asks for a fixed relative error of the force. GADGET-2 adds a test that opens any cell whose slightly enlarged box contains the target.

## Examples and non-examples

**Example.** A cell of side $s = 1$ has its center of mass at distance $d = 2.5$ from the target. Then $s / d = 0.4$, and the cell is accepted for $\theta = 0.5$ and opened for $\theta = 0.3$. If its bodies lie within $b = 0.6$ of the center of mass, the relative error of the monopole potential is at most $b^2 / (d (d - b)) = 0.36 / 4.75 \approx 0.076$ of $G M / d$.

**Non-example: a target inside the accepted cell.** Take the cell $[0, 1]^3$, with almost all of its mass near the corner $(0, 0, 0)$, and the target $\mathbf{x} = (0.95, 0.95, 0.95)$ inside the cell. Then $d \approx 0.95 \sqrt{3} \approx 1.645$ and $s / d \approx 0.608 < 0.7$, so the Barnes-Hut criterion with $\theta = 0.7$ accepts the cell. If the cell also holds a small mass $m$ at distance $\eta$ from the target, its true force $G m / \eta^2$ is replaced by a part of the monopole, so the error has no bound as $\eta \to 0$. The same holds for any $\theta > 1/\sqrt{3}$, because $d$ can reach $\sqrt{3}\, s$ inside the cell (theorem). Salmon and Warren (1994) show that this failure of the criterion occurs in realistic mass distributions, not only in constructed ones. The offset criterion opens this cell: $\delta \approx 0.866$ and $s / \theta + \delta \approx 2.29 > 1.645$.

**Non-example: a criterion on the geometric center only.** Accepting when $|\mathbf{x} - \mathbf{c}_C| > s_C / \theta$ ignores where the mass is. For $\theta < 2/\sqrt{3}$ it keeps the target outside the cell, because the half diagonal of the cube is $\frac{\sqrt{3}}{2} s_C$. But the error bound needs $b_C$, which can be up to $\sqrt{3}\, s_C$ when the center of mass is at a corner, so the test does not bound the error by itself.

## Related definitions

- The [multipole expansion](/multipole-expansion/) and the [multipole truncation error bound](/multipole-truncation-error-bound/) give the error that the criterion controls.
- In the [fast multipole method](/fast-multipole-method/) the analogue is the well-separated condition between two cells, which decides when a [multipole-to-local translation](/multipole-to-local-translation/) is used.
- In a [hashed oct-tree](/hashed-oct-tree/) the criterion decides which cells a processor must fetch from other processors.
- The cost of the walk grows as $\theta$ falls, about as $\theta^{-3}$ for a uniform distribution in three dimensions (heuristic: the number of cells of size $s$ seen under angle $\theta$ in each level is of order $\theta^{-3}$).

## References
