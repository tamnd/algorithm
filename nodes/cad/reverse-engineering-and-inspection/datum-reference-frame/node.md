---
tag: XH1EVT
kind: definition
slug: datum-reference-frame
name: Datum reference frame
aliases:
- datum system
area: cad/reverse-engineering-and-inspection
level: core
summary: The coordinate frame fixed by up to three datum features in order of precedence, against which the position and orientation of other features are toleranced.
prereqs: [geometric-dimensioning-and-tolerancing, rigid-body-transformation]
see_also: [three-two-one-locating-principle, kinematic-fixture-analysis, small-displacement-torsor, special-euclidean-group, degrees-of-freedom-analysis, least-squares-reference-feature, inspection-localization]
sources:
  - url: https://www.asme.org/codes-standards/find-codes-standards/y14-5-dimensioning-tolerancing
    title: ASME Y14.5-2018, Dimensioning and Tolerancing, The American Society of Mechanical Engineers, 2019
    locator: the standard as a whole (datum features, datum feature simulators, datum precedence, degrees of freedom constrained by datums)
  - url: https://www.iso.org/standard/40358.html
    title: ISO 5459:2011, Geometrical product specifications (GPS), Geometrical tolerancing, Datums and datum systems
    locator: the standard as a whole
  - book: isbn:9780750667388
    title: Georg Henzold, Geometrical Dimensioning and Tolerancing for Design, Manufacturing and Inspection, second edition, Butterworth-Heinemann, 2006
    locator: the chapter on datums and datum systems
  - paper: doi:10.1016/S0007-8506(07)61687-4
    title: P. Bourdet and A. Clement, A study of optimal-criteria identification based on the small-displacement screw model, CIRP Annals 37(1), 1988, 503 to 506
    locator: the small displacement screw of a surface and the components that a surface cannot fix
---

A datum reference frame is the coordinate system of a part drawing, built from up to three *datum features* of the real part taken in a fixed order of precedence: primary, secondary and tertiary. Each datum feature is matched by an ideal *datum feature simulator* (a perfect plane, cylinder or point), and the frame is the one that these simulators fix. The [basic dimensions](/geometric-dimensioning-and-tolerancing/) of a feature control frame are measured in it, so it says where each orientation and location zone sits. For three planar datums on a prismatic part, the primary removes 3 of the 6 degrees of freedom of a rigid body, the secondary 2 and the tertiary 1. This page defines the frame, proves that count with its exact conditions, and shows the cases where the count is different.

## Definition

**Rigid motions.** A proper rigid motion of space is a map $g(x) = Rx + t$ with $R$ a rotation ($R^{\mathsf T} R = I$, $\det R = 1$) and $t \in \mathbb{R}^3$ (see [rigid body transformation](/rigid-body-transformation/)). The proper rigid motions form a group of dimension 6, the [special Euclidean group](/special-euclidean-group/) $SE(3)$: 3 parameters for $R$ and 3 for $t$.

**Datum feature and simulator.** A *datum feature* is a real feature of the part named on the drawing, such as a face or a hole. Its *datum feature simulator* is an ideal geometric element of the stated type (a plane, a cylinder of fixed or adjustable size, a sphere, two parallel planes), placed in contact with the datum feature on the side away from the material by a stated rule. The *datum* is the plane, axis, center plane or point that the simulator defines. A real face is never flat, so a plane can rock on it, and the standards give rules that pick one contact position. One common computational choice for a planar datum feature is the tangent plane on the side away from the material that minimizes the largest distance to the measured points.

**Datum reference frame.** Let $D_1, D_2, D_3$ be the datums in order of precedence. The simulators are placed in this order: $D_1$ makes the best contact it can with its datum feature. $D_2$ is then placed under the constraint of a basic orientation (often $90°$) relative to $D_1$, and makes contact with its own datum feature. $D_3$ is placed last, under the constraints of both. The datum reference frame is the Cartesian frame attached to the three placed datums: for three mutually perpendicular planes, the origin is their common point and the axes are their normals. A later datum never moves an earlier one. So the order changes the frame on a real part, even though the three nominal faces are the same.

**Degrees of freedom removed.** An ideal geometric element $E$ is unchanged by some rigid motions. Write

$$ \mathrm{Stab}(E_1, \dots, E_k) = \{ g \in SE(3) : g(E_i) = E_i \text{ for } i = 1, \dots, k \} $$

for the subgroup of motions that maps each element to itself, and $d_k$ for its dimension (as a manifold), with $d_0 = 6$. A motion in this subgroup moves the frame and leaves all the simulators in place, so the simulators cannot tell the two frames apart. The datum $D_k$ *removes* $d_{k-1} - d_k$ degrees of freedom. The frame is fully fixed when $d_k = 0$. These are the motions that the [small displacement torsor](/small-displacement-torsor/) calls the invariant (undetermined) components of a surface, after Bourdet and Clément (1988).

**Theorem (3, 2, 1 for planes).** Let $P_i = \{x : n_i \cdot x = c_i\}$ be planes with unit normals $n_i$, each with its material side fixed (a motion must map $P_i$ to itself and keep its sides). Then:

1. $d_1 = 3$: the primary plane removes 3 degrees of freedom.
2. If $n_2 \ne \pm n_1$, then $d_2 = 1$: the secondary plane removes 2. If $n_2 = \pm n_1$, then $d_2 = 3$ and it removes none.
3. If $n_1, n_2, n_3$ are linearly independent, then $d_3 = 0$: the tertiary plane removes the last 1. If $n_2 \ne \pm n_1$ and $n_3$ lies in the span of $n_1$ and $n_2$, then $d_3 = 1$ and it removes none.

*Proof.* The motion $g(x) = Rx + t$ maps $P_i$ to the plane $\{y : (Rn_i) \cdot y = c_i + (Rn_i) \cdot t\}$, with the material side on the side of $Rn_i$. This is $P_i$ with the same sides if and only if $Rn_i = n_i$ and $n_i \cdot t = 0$.

(1) For one plane, $R$ must fix $n_1$, so $R$ is a rotation about the axis $n_1$, a one-parameter set. The translation must satisfy $n_1 \cdot t = 0$, a plane of translations, two parameters. So the subgroup is the set of rotations about $n_1$ combined with translations in $P_1$, of dimension $1 + 2 = 3$, and $d_1 = 3$.

(2) Let $n_2 \ne \pm n_1$. Then $n_1$ and $n_2$ are linearly independent, and $R$ fixes both. A rotation preserves the cross product, $R(n_1 \times n_2) = Rn_1 \times Rn_2 = n_1 \times n_2$, so $R$ fixes the basis $n_1, n_2, n_1 \times n_2$, and $R = I$. The translation satisfies $n_1 \cdot t = n_2 \cdot t = 0$, so $t = s\,(n_1 \times n_2)$ for a real $s$. The subgroup is the line of translations along the intersection of the two planes, and $d_2 = 1$. If $n_2 = \pm n_1$, the conditions $Rn_2 = n_2$ and $n_2 \cdot t = 0$ follow from those of $P_1$, so the subgroup does not change and $d_2 = 3$.

(3) With $R = I$ and $t = s\,(n_1 \times n_2)$ from (2), the third plane adds $s\, n_3 \cdot (n_1 \times n_2) = 0$. The triple product $n_3 \cdot (n_1 \times n_2)$ is the determinant of $(n_1, n_2, n_3)$. It is nonzero exactly when the normals are linearly independent. Then $s = 0$, the subgroup is $\{\mathrm{id}\}$, and $d_3 = 0$. If $n_3$ lies in the span of $n_1$ and $n_2$, the determinant is zero, every $s$ is allowed, and $d_3 = 1$. $\square$

The proof does not use perpendicularity. Any three planes with independent normals fix the frame. Perpendicular datums are the usual choice because they make the error of each datum act on separate axes.

The count is exact for the ideal simulators. It is a statement about which motions the simulators can detect. The [3-2-1 locating principle](/three-two-one-locating-principle/) proves the matching first-order statement for six point contacts in a fixture, through the rank of the locator Jacobian, and also shows that point contacts locate a part but do not hold it.

## Examples and non-examples

**The prismatic part.** A block with datum A its base ($n_1 = e_3$), datum B a long side ($n_2 = e_2$) and datum C an end ($n_3 = e_1$). The subgroup dimensions are $6, 3, 1, 0$, so the datums remove $3, 2, 1$. A removes the translation along $z$ and the rotations about $x$ and $y$. B removes the translation along $y$ and the rotation about $z$. C removes the translation along $x$.

**Other datum types.** The same subgroup count gives the number for each type of simulator.

| datum features in order | subgroup after each | removed |
| --- | --- | --- |
| plane, plane, plane (independent normals) | rotations about $n_1$ and translations in $P_1$; translations along $n_1 \times n_2$; none | 3, 2, 1 |
| cylinder axis (a hole as primary), plane perpendicular to it, a slot whose center plane contains the axis | rotations about and translations along the axis; rotations about the axis; none | 4, 1, 1 |
| plane, hole perpendicular to it, second hole | rotations about $n_1$ and translations in $P_1$; rotations about the hole axis; none | 3, 2, 1 |
| sphere center (a point) | rotations about the point | 3 |

For the cylinder: a motion that maps a line to itself, keeping its direction, is a rotation about the line combined with a translation along it, two parameters, so the primary removes $6 - 2 = 4$. A plane perpendicular to the axis removes the translation along the axis, and a slot removes the rotation. So the numbers 3, 2 and 1 belong to the planar case only.

**Order of precedence changes the frame.** In a section through a block, datum face A is the line $y = 0$ from $x = 0$ to $x = 100$, and datum face B runs from $(0, 0)$ to $(-0.05, 50)$: it leans back by $0.001$ rad. A hole has basic coordinates $(20, 30)$. With A primary and B secondary, the frame is the usual one, and the true position of the hole is $(20, 30)$. With B primary, the first axis follows B, and the simulator of A, perpendicular to B, touches A at its far corner $(100, 0)$. The true position is then $(19.970, 29.920)$, at a distance of $0.085$ mm from the first one. That is close to a typical position tolerance of $0.1$ mm, so the same hole can pass in one frame and fail in the other. This is why the order of the letters in a feature control frame is part of the requirement.

**Non-example: two parallel faces as primary and secondary.** If A and B are opposite faces of a plate, $n_2 = -n_1$, and the theorem gives $d_2 = d_1 = 3$: B adds nothing to A. The two faces together are a feature of size (a width), and a datum on it is the center plane of a simulator of two parallel planes. That is one datum that removes 3 degrees of freedom, not two datums.

**Non-example: a tertiary face parallel to the edge of the first two.** If A is $z = 0$, B is $y = 0$ and C is a face whose normal is $(0, 1, 1)/\sqrt 2$ (a chamfer along the $x$ edge), then $n_3$ lies in the span of $n_1$ and $n_2$, and the translation along $x$ stays free. The frame has no origin along $x$, and a location requirement along $x$ cannot be checked.

**Non-example: one face on a rocking simulator.** A convex datum face, slightly domed, touches a simulator plane at one point, and the plane can rock. The ideal count still says 3 degrees of freedom, but the frame is not repeatable from one measurement to the next. The rule that fixes the contact position (stabilization) is part of the definition of the simulator, and a different rule gives a different frame.

## Related definitions

- **Datum feature, datum feature simulator, datum.** The real feature, the ideal element in contact with it, and the plane, axis or point derived from the ideal element. Inspection software computes the simulator from measured points, often with a constrained fit (compare [least-squares reference features](/least-squares-reference-feature/), which do not keep to the material side).
- **Datum target.** A point, line or small area of the datum feature named on the drawing as the only contact. Three targets on A, two on B and one on C give the six contacts of the [3-2-1 locating principle](/three-two-one-locating-principle/).
- **Datum shift.** When a datum feature of size is given with a material condition modifier, the simulator has a fixed size, and the part can move relative to it by the gap between them. The frame is then a set of frames, not one.
- **Invariance class.** The subgroup of a surface type, as in the table above. The [small displacement torsor](/small-displacement-torsor/) of a surface has one undetermined component for each dimension of this subgroup, to first order.
- **Degrees of freedom in a mechanism.** The [degrees of freedom analysis](/degrees-of-freedom-analysis/) page counts the freedoms of a linkage or a constraint system. The count on this page is the same idea for the frame of one part.
- **Inspection localization.** [Inspection localization](/inspection-localization/) finds the rigid motion that best matches measured points to the whole CAD model. A datum reference frame instead uses only the datum features, in order, which is what the drawing asks for.

## References
