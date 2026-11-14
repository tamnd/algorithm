---
tag: MC9X71
kind: definition
slug: bend-allowance
name: Bend allowance
aliases: []
area: cad/manufacturing-process-planning
level: intro
summary: The length of the neutral axis through a bend, BA = theta (R + K t) for bend angle theta in radians, inside radius R, thickness t and K-factor K, added to the flat flange lengths.
prereqs: [k-factor]
see_also: [flat-pattern-development, springback-compensation, bend-sequence-planning, a-star-bend-sequencing, developable-surface]
sources:
  - book: isbn:9780133128741
    title: Serope Kalpakjian and Steven R. Schmid, Manufacturing Engineering and Technology, 7th edition, Pearson, 2014
    locator: Chapter 16 (sheet-metal forming), the part on bending of sheets and plates, with the bend allowance L_b = alpha (R + k T) and the range of k (general locator; the section number is not confirmed)
  - title: Serope Kalpakjian and Steven R. Schmid, Manufacturing Processes for Engineering Materials, 5th edition, Pearson Prentice Hall, 2008
    locator: Chapter 7 (sheet-metal forming processes), the part on bending, with the same bend allowance formula (general locator)
  - title: DIN 6935, Kaltbiegen von Flacherzeugnissen aus Stahl (cold bending of flat rolled steel products), Beuth, 2011
    locator: the correction factor k for the position of the neutral line and the compensation value v, the length that is added to the outer dimensions
---

The bend allowance of a sheet metal bend is the length of the neutral axis through the bend zone. For a bend that turns the flange by the angle $\theta$, with inside radius $R$, sheet thickness $t$ and [K-factor](/k-factor/) $K$, it is $\mathrm{BA} = \theta (R + K t)$. It is the length that the bend takes in the flat blank, so the blank is the flat flange lengths plus one bend allowance per bend. This is the base of [flat pattern development](/flat-pattern-development/). The bend deduction, a different length that is subtracted from the outer dimensions, is defined below.

## Definition

**The bend.** A flat sheet of thickness $t$ is bent along a straight line into two flat flanges and a bend zone between them. In the model of the bend, the bend zone is a circular sector of an annulus with inside radius $R$ and outside radius $R + t$, the thickness does not change, and the flanges are tangent to the arcs at the ends of the zone. The *bend angle* $\theta$ is the angle by which the second flange turns relative to the first, in radians, with $0 < \theta \le \pi$. It is $\pi$ minus the included angle between the flanges: a right-angle bend has $\theta = \pi/2$.

**Neutral axis and K-factor.** Bending stretches the outer fibres and compresses the inner ones. The *neutral axis* is the fibre in the cross-section whose length does not change. In the model it is the arc of radius $R + K t$, where the [K-factor](/k-factor/) $K$ is the distance from the inside face to the neutral axis divided by $t$.

**Bend allowance.**

$$\mathrm{BA} = \theta \, (R + K t).$$

*Proof that this is the arc length of the neutral axis.* The neutral axis in the bend zone is a circular arc of radius $\rho = R + K t$ about the bend centre $C$. Its two ends are on the radii of $C$ where the bend zone meets the flanges. The tangent of a circle is perpendicular to the radius, so the direction of the tangent turns by the same angle as the radius. At each end the tangent is the direction of a flange, and the flange direction turns by $\theta$. So the arc has central angle $\theta$ and length $\theta \rho$. $\square$

**Flat length of one bend.** Let $a$ and $b$ be the lengths of the flat parts of the two flanges, from the free edge to the start of the bend zone. The neutral axis does not change its length, so the blank length is its length before the bend:

$$L = a + b + \mathrm{BA}.$$

**Outside setback and bend deduction.** Part drawings give the *outer dimensions* $A$ and $B$: the distance from each free edge to the *mold point* $M$, where the planes of the two outer faces meet. The *outside setback* is the distance from the end of the outer arc to $M$:

$$\mathrm{OSSB} = (R + t) \tan(\theta/2).$$

*Proof.* Let $T_1$ and $T_2$ be the ends of the outer arc of radius $R + t$. The outer faces of the flanges are tangent to this arc at $T_1$ and $T_2$, so $C T_1 \perp T_1 M$ and $C T_2 \perp T_2 M$. The angle $T_1 C T_2$ is the central angle $\theta$. The triangles $C T_1 M$ and $C T_2 M$ are right triangles with the same hypotenuse $CM$ and equal legs $|CT_1| = |CT_2| = R + t$, so they are congruent, and $CM$ bisects the angle $T_1 C T_2$. In the right triangle $C T_1 M$, $|T_1 M| = |C T_1| \tan(\theta/2) = (R + t)\tan(\theta/2)$. $\square$

The boundary of the bend zone is a radius of $C$, and so it is perpendicular to the flange. So $a$ is also the distance from the free edge to $T_1$ along the outer face, and $A = a + \mathrm{OSSB}$, $B = b + \mathrm{OSSB}$. Substitution in $L = a + b + \mathrm{BA}$ gives

$$L = A + B - \mathrm{BD}, \qquad \mathrm{BD} = 2\,\mathrm{OSSB} - \mathrm{BA}.$$

The *bend deduction* $\mathrm{BD}$ is the length to subtract from the sum of the outer dimensions. It is not the bend allowance: $\mathrm{BA}$ is a length of material, and $\mathrm{BD}$ is a correction to dimensions measured to a mold point. For $\theta = \pi$ (a hem) the outer faces are parallel, there is no mold point, and only $\mathrm{BA}$ is defined. For a part with several bends, the formulas add: $L$ is the sum of the flat flange lengths plus the sum of the $\mathrm{BA}_i$, or the sum of the outer dimensions minus the sum of the $\mathrm{BD}_i$.

**The value of $K$ is empirical.** Kalpakjian and Schmid give $K$ (their $k$) from about 0.33 for $R < 2t$ to 0.5 for $R > 2t$. These are ranges from tests, not exact values. The model ignores the thinning of the sheet in the bend, the fact that the bend zone is not exactly circular, the spread of the bend zone beyond the tangent lines, the width of the sheet (plane strain against plane stress) and [springback](/springback-compensation/), which opens the bend after release. Shops measure $K$ for each material, thickness, radius and tool, as the [K-factor](/k-factor/) page shows.

## Examples and non-examples

**A right-angle bend.** Steel sheet with $t = 2$ mm, inside radius $R = 3$ mm, bend angle $\theta = \pi/2$, outer dimensions $A = 50$ mm and $B = 30$ mm. Since $R < 2t$, take $K = 0.33$ from the range above.

| quantity | formula | value (mm) |
|---|---|---|
| neutral radius | $R + K t$ | 3.66 |
| bend allowance | $\theta (R + K t)$ | 5.7491 |
| outside setback | $(R + t)\tan(\theta/2)$ | 5.0000 |
| bend deduction | $2\,\mathrm{OSSB} - \mathrm{BA}$ | 4.2509 |
| flat flanges | $a = A - \mathrm{OSSB}$, $b = B - \mathrm{OSSB}$ | 45, 25 |
| blank, from the flanges | $a + b + \mathrm{BA}$ | 75.7491 |
| blank, from the outer dimensions | $A + B - \mathrm{BD}$ | 75.7491 |

The two routes give the same blank, as the proof says. With $K = 0.5$ instead, $\mathrm{BA} = 6.2832$ and the blank is 76.2832 mm, 0.53 mm longer. So the choice of $K$ matters at the tolerance of a sheet metal part.

**Other angles.** With the same sheet and outer dimensions, a bend of $60$ degrees ($\theta = \pi/3$) has $\mathrm{BA} = 3.8327$, $\mathrm{OSSB} = 2.8868$, $\mathrm{BD} = 1.9408$ and blank 78.0592 mm. A bend of $120$ degrees has $\mathrm{BA} = 7.6655$, $\mathrm{OSSB} = 8.6603$, $\mathrm{BD} = 9.6550$ and blank 70.3450 mm. For a bend of more than 90 degrees the mold point is far from the part, so a dimension to it is hard to measure. Some standards, such as DIN 6935, then measure the outer dimension to a tangent of the outer face, and the correction formula changes with it.

**Non-examples.**

- The inner arc $\theta R$ and the outer arc $\theta (R + t)$ are not the bend allowance. They are the cases $K = 0$ and $K = 1$, which no real bend has. In the example they are 4.7124 and 7.8540 mm.
- The bend deduction is not a bend allowance. In the example $\mathrm{BD} = 4.2509$ and $\mathrm{BA} = 5.7491$, and for a $120$ degree bend $\mathrm{BD}$ is even larger than $\mathrm{BA}$.
- A sharp bend with $R = 0$ still has a bend allowance $\theta K t$, not zero, because the neutral axis is inside the material.
- The bend angle is not the included angle. A bend to an included angle of 60 degrees has $\theta = 120$ degrees, and the two readings give blanks of 70.3450 and 78.0592 mm in the example.

## Related definitions

- [K-factor](/k-factor/): the K-factor is a dimensionless position of the neutral axis, a material and process parameter, while the bend allowance is the length of one bend that is computed from it.
- [Flat pattern development](/flat-pattern-development/): the problem of computing the whole blank of a part, which adds one bend allowance per bend.
- [Springback compensation](/springback-compensation/): the bend opens when the tool is released, so the tool bends to a smaller radius and a larger angle than the part has.
- [Bend sequence planning](/bend-sequence-planning/) and [A* bend sequencing](/a-star-bend-sequencing/): the order in which the bends of a part are made on a press brake.
- [Developable surface](/developable-surface/): the faces and bend zones of a sheet metal part are developable, so they unfold to the plane without stretch in the model.

## References
