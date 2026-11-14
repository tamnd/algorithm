---
tag: 0VQP8H
kind: definition
slug: analog-symmetry-constraint
name: Symmetry constraint in analog layout
aliases:
- device symmetry constraint
- symmetry group
area: eda/fpga-analog-and-emerging-technologies
level: core
summary: Matched devices of an analog circuit must be placed in mirror pairs about a common axis, and self-symmetric devices on it, to cancel gradients and parasitics.
prereqs: [placement-problem, floorplanning]
see_also: [symmetric-feasible-sequence-pair, asf-b-star-tree, common-centroid-layout, pelgrom-mismatch-model, sequence-pair, b-star-tree-floorplan, gradient]
sources:
  - paper: doi:10.1109/5.899053
    title: Georges G. E. Gielen and Rob A. Rutenbar, Computer-aided design of analog and mixed-signal integrated circuits, Proceedings of the IEEE 88(12), 1825 to 1854, 2000
    locator: the section on analog layout (symmetry, matching and the placers that keep them)
  - paper: "John M. Cohn, David J. Garrod, Rob A. Rutenbar and L. Richard Carley, KOAN/ANAGRAM II: New tools for device-level analog placement and routing, IEEE Journal of Solid-State Circuits 26(3), 330 to 342, 1991"
    title: J. M. Cohn, D. J. Garrod, R. A. Rutenbar and L. R. Carley, KOAN/ANAGRAM II, new tools for device-level analog placement and routing, IEEE JSSC 26(3), 330 to 342, March 1991
    locator: the placement with mirror-symmetric and self-symmetric devices, and the mirror-symmetric and self-symmetric wiring
  - paper: doi:10.1109/43.851988
    title: Florin Balasa and Koen Lampaert, Symmetry within the sequence-pair representation in the context of placement for analog design, IEEE Transactions on Computer-Aided Design 19(7), 721 to 731, 2000
    locator: the formal definition of a symmetric set with symmetric pairs and self-symmetric cells about one axis
  - paper: doi:10.1109/TCAD.2009.2017433
    title: Po-Hung Lin, Yao-Wen Chang and Shyh-Chang Lin, Analog placement based on symmetry-island formulation, IEEE Transactions on Computer-Aided Design 28(6), 791 to 804, 2009
    locator: the definition of the symmetry island, a symmetric set placed as one connected region
  - book: isbn:9780131464100
    title: Alan Hastings, The Art of Analog Layout, second edition, Prentice Hall, 2006
    locator: the chapters on matching (the rules for matched devices, including symmetry, orientation and thermal gradients)
---

A symmetry constraint is a rule on the placement, and often the routing, of an analog circuit: given sets of matched devices, each set must be mirror-symmetric about one axis. The two devices of a *symmetric pair* get mirror positions, and a *self-symmetric* device is centered on the axis. Its topic is analog sizing and layout, one of the five topics of this sub-area. The constraint makes the matched halves of a differential circuit see the same parasitics and the same symmetric variations of the process and the temperature, so it is an input to every analog placer, and the placers [symmetric-feasible sequence pairs](/symmetric-feasible-sequence-pair/) and [ASF-B*-trees](/asf-b-star-tree/) are built around it.

## Definition

The devices are rectangles with widths $w_u$ and heights $h_u$, placed at lower-left corners $(x_u, y_u)$ without overlap. A *symmetric set* $G$ is a set of devices with a map $\mathrm{sym} : G \to G$ that is an involution: $\mathrm{sym}(\mathrm{sym}(u)) = u$. A *symmetric pair* is $\{u, \mathrm{sym}(u)\}$ with $u \neq \mathrm{sym}(u)$, and its two devices have the same size and the same layout up to a mirror. A *self-symmetric* device has $\mathrm{sym}(s) = s$, and its own layout is mirror-symmetric. Each set has an axis direction, vertical or horizontal.

A placement satisfies the symmetry constraint of $G$ with a vertical axis if there is a number $X_G$ such that

- for each symmetric pair $\{u, v\}$: $y_u = y_v$ and $(x_u + \frac{w_u}{2}) + (x_v + \frac{w_v}{2}) = 2 X_G$, and $v$ is laid out as the mirror image of $u$;
- for each self-symmetric device $s$: $x_s + \frac{w_s}{2} = X_G$.

For a horizontal axis, exchange $x$ and $y$, and $w$ and $h$. A circuit can have several sets, each with its own axis. A common case asks all sets of a differential signal path to share one axis, $X_G = X$ for all $G$. Symmetric routing asks the same of the wires: the nets of a symmetric pair of nets are mirror images, and a self-symmetric net is its own mirror.

**What the constraint cancels.** Let $p(x, y)$ be a process or temperature field, and let a device take the value of $p$ at its center. For a pair at the centers $(X - d, y)$ and $(X + d, y)$, the difference is $p(X + d, y) - p(X - d, y)$. This is zero for every pair if and only if $p$ is symmetric about the axis: $p(X + d, y) = p(X - d, y)$. So a field that changes only along the axis, a field that depends on $|x - X|$ (such as the heat of a device centered on the axis), and every parasitic that the mirrored layout makes equal, cancel. A linear gradient across the axis, $p = p_0 + g_x x + g_y y$, gives the difference $2 g_x d$: it does not cancel, and it grows with the distance $d$ from the axis. These two statements are proved by the substitution above. Nothing on this page is measured.

## Examples and non-examples

**A differential amplifier.** A five-transistor amplifier has the input pair M1 and M2, the load pair M3 and M4, and the tail current source M5. The symmetric set is $\{M1, M2, M3, M4, M5\}$ with $\mathrm{sym}(M1) = M2$, $\mathrm{sym}(M3) = M4$ and $\mathrm{sym}(M5) = M5$. One placement on the axis $X = 4$: M5 of size $4 \times 1$ at $(2, 0)$, M1 and M2 of size $2 \times 2$ at $(1, 1)$ and $(5, 1)$, and M3 and M4 of size $2 \times 2$ at $(2, 3)$ and $(4, 3)$. The centers of M1 and M2 are at $x = 2$ and $x = 6$, which add to $2X$. The centers of M3 and M4 are at $3$ and $5$. The center of M5 is at $4$. This placement satisfies the constraint.

**A placement from a sequence pair.** The example on the [symmetric-feasible sequence pair](/symmetric-feasible-sequence-pair/) page places a pair at $x = 1$ and $x = 2$ (width 1), and a self-symmetric device of width 2 at $x = 1$, with the axis at $X = 2$. A free device to the left of the set is not part of the constraint.

**Non-example: a pair at two heights.** If M1 is at $(1, 1)$ and M2 at $(5, 2)$, the $x$ condition holds but $y_{M1} \neq y_{M2}$. A gradient along the axis then gives the two devices different values.

**Non-example: a self-symmetric device off the axis.** If M5 is at $(1, 0)$, its center is at $x = 3 \neq X$. The two halves of M5 then feel the two halves of the amplifier differently.

**Non-example: a common centroid.** The cross-quad pattern, A and B in one row and B and A in the next, gives two devices the same centroid, but it is a point reflection, not a mirror pair about a line. It does not satisfy this constraint, and it cancels more: a linear gradient in every direction. See [common-centroid layout](/common-centroid-layout/).

**Non-example: the same size, the wrong orientation.** Two devices at mirror positions, but one rotated by 90 degrees, satisfy the position conditions but not the condition that $v$ is laid out as the mirror of $u$.

## Related definitions

- **Symmetry island.** A symmetric set whose devices form one connected region around the axis, as in the placer of Lin, Chang and Lin. It adds closeness to the constraint, so that the matched devices also see the same local surroundings.
- **Proximity constraint.** A set of devices that must be placed close to one another, without a symmetry.
- **Common-centroid constraint.** The devices of a set are split into unit cells with one centroid. It cancels linear gradients in both directions, which mirror symmetry does not. See [common-centroid layout](/common-centroid-layout/).
- **Matching.** Devices with the same size, orientation and surroundings, whose random mismatch falls with the area as in the [Pelgrom mismatch model](/pelgrom-mismatch-model/). Symmetry removes systematic differences, not the random part.
- **Same orientation.** Some layout rules ask matched devices to have the same orientation instead of mirrored layouts, because an implant at an angle to the wafer affects a device and its mirror image differently. Then the positions are mirrored and the layouts are copied.
- **Symmetric-feasible placement representations.** A representation of placements, such as a [sequence pair](/sequence-pair/) or a [B*-tree](/b-star-tree-floorplan/), is symmetric-feasible if each of its codes in a chosen subset has a placement that satisfies the constraint. The [symmetric-feasible sequence pair](/symmetric-feasible-sequence-pair/) and the [ASF-B*-tree](/asf-b-star-tree/) are the two standard ones.

## References
