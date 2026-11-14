---
tag: JQ9ZE3
kind: technique
slug: common-centroid-layout
name: Common-centroid layout
aliases:
- common-centroid placement
- interdigitation
area: eda/fpga-analog-and-emerging-technologies
level: core
summary: Splits matched devices into unit cells arranged so that each device has the same centroid, cancelling linear process gradients in analog circuits.
prereqs: [analog-symmetry-constraint]
see_also: [pelgrom-mismatch-model, symmetric-feasible-sequence-pair, asf-b-star-tree, placement-problem, gradient, monte-carlo-tolerance-analysis]
sources:
  - book: isbn:9780131464100
    title: Alan Hastings, The Art of Analog Layout, second edition, Prentice Hall, 2006
    locator: the sections Gradients and Centroids and Common-Centroid Layout (the rules of coincidence, symmetry, dispersion and compactness), and Section 12.3.5, Common-Centroid Layout of MOS Transistors
  - paper: doi:10.1109/JSSC.1989.572629
    title: Marcel J. M. Pelgrom, Aad C. J. Duinmaijer and Anton P. G. Welbers, Matching properties of MOS transistors, IEEE Journal of Solid-State Circuits 24(5), 1433 to 1440, 1989
    locator: the split of mismatch into a random part that falls with the area and a part that grows with the distance between the devices
  - paper: doi:10.1109/5.899053
    title: Georges G. E. Gielen and Rob A. Rutenbar, Computer-aided design of analog and mixed-signal integrated circuits, Proceedings of the IEEE 88(12), 1825 to 1854, 2000
    locator: the section on analog layout (device matching, symmetry and common-centroid placement)
---

Common-centroid layout is a layout technique for matched devices: each device is split into equal unit cells, and the cells are placed so that the centroid (the mean position) of every device is the same point. Its topic is analog sizing and layout, one of the five topics of this sub-area. If a process parameter changes linearly across the die, the mean value over each device is then the same, so a linear [gradient](/gradient/) adds no mismatch, exactly. A quadratic change still leaves a mismatch, and this page gives its exact size.

## In plain words

Two capacitors on a chip must be equal. The oxide is a bit thicker on the left side of the die than on the right. If one capacitor sits on the left and one on the right, they differ.

Cut each capacitor into equal small pieces and wire the pieces of each one in parallel. Now arrange the pieces so that each capacitor has its pieces spread around the same middle point, for example in the order A, B, B, A. The extra thickness that one piece of A gets on the left, the other piece of A loses on the right. B gets the same average. The two capacitors stay equal for any steady change from one side to the other.

The trick does not remove a change that curves, and it does nothing against the random differences between pieces.

## When it applies

- Two or more devices must match in a ratio: the transistors of a differential pair or a current mirror, the capacitors of a switched-capacitor filter or a DAC, the resistors of a divider.
- Each device can be built from identical unit cells in parallel (or in series), so its value is the sum of the unit values, and the ratio of two devices is the ratio of their mean unit values.
- The process parameter (oxide thickness, sheet resistance, threshold voltage, temperature) changes smoothly over the area of the array, so a low-order Taylor series describes it.
- The units can share one orientation and one environment, so that only the gradient differs from cell to cell.

## The template

Model a parameter field $p(x, y)$ over the array. A device $D$ has $k_D$ unit cells with centers $r_1, \ldots, r_{k_D}$. Its parameter is the mean of the unit values,

$$P_D = \frac{1}{k_D} \sum_{i=1}^{k_D} p(r_i).$$

This is exact for a quantity that adds, such as a capacitance or a current at a fixed drive, and it holds to first order for the threshold voltage of parallel transistors. The centroid of $D$ is $c_D = \frac{1}{k_D} \sum_i r_i$.

1. Choose the unit cell, and the number of units of each device from the ratio.
2. Choose an array of $R$ rows and $C$ columns, with $R C$ equal to the total number of units (add dummy cells if needed).
3. Pair each cell with its point reflection through the center of the array, and give both cells of each pair to the same device. A device with an odd number of units takes the center cell.
4. Among such patterns, spread the devices so that their second moments are as close as possible (the dispersion rule).
5. Surround the array with dummy cells, so that every unit has the same neighbors, and route each device symmetrically.

**Theorem 1 (linear gradients cancel exactly).** Let $p(r) = p_0 + g \cdot r$ for a constant vector $g$. Then $P_D = p_0 + g \cdot c_D$. So $P_A = P_B$ for every $g$ if and only if $c_A = c_B$.

*Proof.* By linearity of the mean, $P_D = \frac{1}{k_D} \sum_i (p_0 + g \cdot r_i) = p_0 + g \cdot c_D$. If $c_A = c_B$, then $P_A - P_B = g \cdot (c_A - c_B) = 0$. If $c_A \neq c_B$, the gradient $g = c_A - c_B$ gives $P_A - P_B = |c_A - c_B|^2 > 0$. $\square$

**Lemma (step 3 works).** If the cells of $D$ are a union of point-reflection pairs about the center $c$, plus possibly the center cell itself, then $c_D = c$. Each pair $\{r, 2c - r\}$ has the mean $c$, and the center cell is $c$, so the mean over all cells is $c$. $\square$

**When step 3 is possible.** Pairs exist for every cell except the center cell, which exists only when $R$ and $C$ are both odd. So point-symmetric patterns exist exactly when every count is even, or when $R$ and $C$ are odd and exactly one count is odd. An odd count with an even $R$ cannot have the common centroid in any pattern, symmetric or not: the $y$ values of the cell centers are $\frac12, \frac32, \ldots$, so the sum of an odd number of them is half an odd integer, but the centroid $\frac{R}{2}$ needs the sum $k_D \frac{R}{2}$, which is an integer. The same holds for an even $C$. A pattern with the common centroid need not be point symmetric: in a $3 \times 5$ array, the offsets $\{(0,0), (-1,0), (1,0)\}$ and $\{(-2,0), (1,1), (1,-1)\}$ from the center give two devices of 3 cells each with the centroid at the center.

**Theorem 2 (the quadratic residual).** Let $c_A = c_B = c$, and let

$$p(r) = p_0 + g \cdot (r - c) + \tfrac12 (r - c)^\top H (r - c)$$

with a symmetric matrix $H = \begin{pmatrix} h_{xx} & h_{xy} \\ h_{xy} & h_{yy} \end{pmatrix}$. Let $S_D = \frac{1}{k_D} \sum_i (r_i - c)(r_i - c)^\top$ be the second moment of $D$ about $c$. Then

$$P_A - P_B = \tfrac12 \operatorname{tr}\big(H (S_A - S_B)\big) = \tfrac12 h_{xx} \Delta S_{xx} + h_{xy} \Delta S_{xy} + \tfrac12 h_{yy} \Delta S_{yy}.$$

This is zero for every $H$ if and only if $S_A = S_B$.

*Proof.* The mean of the linear term is $g \cdot (c_D - c) = 0$. For the quadratic term, $(r - c)^\top H (r - c) = \operatorname{tr}(H (r - c)(r - c)^\top)$, and the trace is linear, so the mean over $D$ is $\operatorname{tr}(H S_D)$. Subtracting gives the formula. If $S_A \neq S_B$, take $H = S_A - S_B$, which is symmetric, to get $\frac12 \operatorname{tr}((S_A - S_B)^2) > 0$. $\square$

For a smooth field, the Taylor series about $c$ shows that the third-order terms are left after this. So the error of a common-centroid pair is of second order in the size of the array, and of third order when the second moments also agree.

## Classic examples

The cells have pitch 1, and the numbers below use exact fractions.

**One row of four.** With $p(x) = x$ (a gradient of 1 per pitch), the order AABB gives $P_A - P_B = -2$, the alternating order ABAB gives $-1$, and the common-centroid order ABBA gives 0. With the curvature $p(x) = (x - 2)^2$ about the center, ABBA gives $P_A - P_B = 2$: A has its cells at the offsets $\pm \frac32$ and B at $\pm \frac12$, so $S_A = \frac94$, $S_B = \frac14$ and $\frac12 \cdot 2 \cdot 2 = 2$. ABAB is not common centroid, but it gives 0 for this curvature. No order of one row cancels both.

**The cross-quad.** The $2 \times 2$ pattern AB over BA puts each device on one diagonal. It cancels gradients in $x$, in $y$ and in any direction. Its second moments are $S_{xx} = S_{yy} = \frac14$ for both devices, but $S_{xy} = \frac14$ for A and $-\frac14$ for B. So a pure $x^2$ or $y^2$ curvature cancels, and a curvature $h_{xy}$ leaves $P_A - P_B = h_{xy} \cdot \frac12$.

**A $2 \times 4$ array with four units each.** Of the 70 assignments, 8 have the common centroid. Of these, 6 also cancel the curvature $x^2$, and only 2 cancel both $x^2$ and $xy$: the pattern ABBA over BAAB and its swap, whose second moments are equal. The construction of the implementation gives ABAB over BABA, which cancels $x^2$ and leaves $\frac12$ for $h_{xy} = 1$.

**An odd count.** A $3 \times 3$ array with 4 units of A and 5 of B: B takes the center. The construction gives ABA, BBB, ABA. A row of 6 with 3 units each has no common-centroid pattern, by the parity argument.

**A binary-weighted capacitor array.** A ratio 1 : 1 : 2 with 4, 4 and 8 units fills a $4 \times 4$ array. The construction gives the rows ABCC, ABCC, CCBA, CCBA, in which all three devices have the centroid at the center.

## Variations

- **Alternating rows.** A one-dimensional order such as ABAB reduces the effect of a gradient along the row, but it is common centroid only for special counts and orders.
- **Higher-order cancellation.** Match the second moments as well (Theorem 2), with larger arrays and more units, to cancel a quadratic field.
- **Dispersion.** Spread the units of each device evenly, so that no device has long runs of its own cells. This lowers the effect of the higher-order terms and of local defects.
- **Automatic generation.** Placement tools search among the common-centroid patterns for one that also keeps the routing short and the dispersion high.
- **Symmetry about an axis.** A placement in which each device is mirrored about one axis cancels gradients across the axis only. See [symmetry constraints](/analog-symmetry-constraint/), and the placers [symmetric-feasible sequence pairs](/symmetric-feasible-sequence-pair/) and [ASF-B*-trees](/asf-b-star-tree/).

## Pitfalls

- **Random mismatch remains.** Common centroid cancels systematic gradients. The random mismatch of each unit is not reduced by the arrangement, only by the total area, as the [Pelgrom mismatch model](/pelgrom-mismatch-model/) says.
- **Edge effects.** A unit at the edge of the array etches differently from one inside. Without dummy cells around the array, the outer units differ, and the cancellation fails.
- **Routing.** The wires that join the units of one device add resistance and capacitance. If the routing of A and B differs, the routing makes a new mismatch.
- **Orientation.** MOS units must share one orientation, because stress and the angle of implants make the orientation matter.
- **The mean is an approximation for transistors.** For parallel transistors, the drain current is not linear in the threshold voltage, so Theorem 1 holds only to first order in the spread of the threshold.
- **Curvature over large arrays.** The quadratic residual grows with the square of the array size. A large array of a few devices can be worse than a compact one.

## Exercises

1. Show that the pattern ABBA over BAAB has $S_A = S_B$, so it cancels every quadratic field.
2. For a row of 8 cells with 4 units each, find all orders with the common centroid. Which of them has the smallest residual for $p(x) = (x - 4)^2$?
3. Find a $3 \times 3$ pattern of three devices with 3 units each, all with the centroid at the center (there are 12). Show that none of them is point symmetric, so step 3 of the template cannot make them.
4. A field has $h_{xx} = 0.3$ per square pitch, and $h_{xy} = h_{yy} = 0$. Compute the mismatch of the cross-quad and of the one-row ABBA.

## References
