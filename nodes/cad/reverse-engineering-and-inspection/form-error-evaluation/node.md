---
tag: QFVAR9
kind: problem
slug: form-error-evaluation
name: Form error evaluation
aliases:
- form tolerance evaluation
area: cad/reverse-engineering-and-inspection
level: core
summary: Compute the straightness, flatness, roundness or cylindricity of measured points as the width of the thinnest zone of the ideal shape that holds them all.
prereqs: [geometric-dimensioning-and-tolerancing, convex-hull, polygon-width]
see_also: [minimum-zone-flatness, minimum-zone-cylindricity, minimum-width-annulus, least-squares-reference-feature, circle-fitting, requicha-tolerance-zone-theory, cad-based-inspection, lp-type-problem]
sources:
  - url: https://www.iso.org/standard/66777.html
    title: ISO 1101:2017, Geometrical product specifications (GPS), Geometrical tolerancing, Tolerances of form, orientation, location and run-out, fourth edition
    locator: the standard as a whole (the tolerance zones of straightness, flatness, roundness and cylindricity); no clause is quoted
  - url: https://www.asme.org/codes-standards/find-codes-standards/y14-5-dimensioning-tolerancing
    title: ASME Y14.5-2018, Dimensioning and Tolerancing, The American Society of Mechanical Engineers, 2019
    locator: the standard as a whole (the form tolerances and their zones); no clause is quoted
  - paper: doi:10.1109/34.6790
    title: Michael E. Houle and Godfried T. Toussaint, Computing the width of a set, IEEE Transactions on Pattern Analysis and Machine Intelligence 10(5), 1988, 761 to 765
    locator: the width of a point set in two and three dimensions from antipodal pairs of the convex hull, which is the minimum zone of straightness and flatness
  - paper: "Mark T. Traband, Sanjay Joshi, Richard A. Wysk and Tom M. Cavalier, Evaluation of straightness and flatness tolerances using the minimum zone, Manufacturing Review 2(3), 1989, 189 to 195"
    locator: the minimum zone evaluation of straightness and flatness, compared with least-squares evaluation
  - paper: doi:10.1016/0141-6359(94)00018-U
    title: Kirsten Carr and Placid Ferreira, Verification of form tolerances part II, cylindricity and straightness of a median line, Precision Engineering 17(2), 1995, 144 to 156
    locator: the minimum zone, minimum circumscribed and maximum inscribed cylinders as a sequence of linear programs that converge to a local optimum
  - paper: doi:10.1007/s00454-001-0039-6
    title: Pankaj K. Agarwal, Boris Aronov and Micha Sharir, Exact and approximation algorithms for minimum-width cylindrical shells, Discrete and Computational Geometry 26(3), 2001, 307 to 320
    locator: the exact minimum width cylindrical shell in polynomial time, and a constant factor approximation
  - paper: doi:10.1007/BF02712871
    title: Pankaj K. Agarwal and Micha Sharir, Efficient randomized algorithms for some geometric optimization problems, Discrete and Computational Geometry 16(4), 1996, 317 to 337
    locator: the width in three dimensions and the minimum width annulus in O(n^(3/2+ε)) expected time
---

Form error evaluation is the problem of grading a measured feature against its ideal shape: given points measured on a nominally straight, flat, round or cylindrical feature, find the thinnest zone of the matching shape that holds all of them. The width of that zone is the straightness, flatness, roundness or cylindricity of the feature. The zone may move and turn freely, since a form tolerance does not refer to a datum. A tolerance is met when the form error is at most the tolerance value. This page is the problem; the methods are [minimum zone flatness](/minimum-zone-flatness/) for straightness and flatness, [minimum zone cylindricity](/minimum-zone-cylindricity/) for cylindricity, and the [minimum width annulus](/minimum-width-annulus/) for roundness. The [least-squares reference feature](/least-squares-reference-feature/) is a different evaluation, which gives an upper bound.

## In plain words

A shaft should be a perfect cylinder, but no real shaft is. A machine touches many points on it. To grade it, we look for two cylinders with the same axis, one inside the other, so that every point lies between them, and we make the gap between them as thin as possible. That gap is the cylindricity.

The same idea works for the other shapes. For a flat face, use two parallel planes. For an edge that should be straight, use two parallel lines. For a round section, use two circles with the same center. In each case we may move and tilt the pair freely, and the answer is the thinnest gap we can reach. A best-fit shape through the middle of the points also gives a gap, but it is never thinner, and it is often a little wider.

## Definition

The input is a set of points $x_1, \dots, x_n$ measured on a feature, corrected for the probe radius, and a form type. Each type has an ideal feature with free parameters $\theta$ and a signed deviation $e_i(\theta)$ of each point from it:

| form | zone shape | free parameters $\theta$ | deviation $e_i(\theta)$ |
| --- | --- | --- | --- |
| straightness (in a plane) | between two parallel lines | unit normal $u$ of the line | $u \cdot x_i$ |
| flatness | between two parallel planes | unit normal $u$ of the plane | $u \cdot x_i$ |
| roundness (in a section) | between two concentric circles | center $c$ | $\lvert x_i - c \rvert$ |
| cylindricity | between two coaxial cylinders | axis line $L$ (four numbers) | distance from $x_i$ to $L$ |

The position along $u$ and the radius are not free parameters, because the width does not depend on them. The zone of $\theta$ is the region between the levels $\min_i e_i(\theta)$ and $\max_i e_i(\theta)$, and its width is
$$ W(\theta) = \max_i e_i(\theta) - \min_i e_i(\theta). $$
The objective is the **minimum zone** form error
$$ E = \min_\theta W(\theta), $$
together with a minimizer $\theta^*$. This is a minimax, or Chebyshev, fit. The [tolerance zone theory of Requicha](/requicha-tolerance-zone-theory/) gives the same meaning to the zone of a form tolerance: the surface must lie in some zone of the given shape and width.

**A least-squares fit is not a minimum zone fit.** The least-squares reference feature minimizes $\sum_i (e_i(\theta) - m)^2$ over $\theta$ and the level $m$, not $W(\theta)$. Its zone, between the extreme deviations from it, is the zone of one particular $\theta$, so $W(\theta_{\mathrm{LS}}) \ge E$. Its zone is never narrower than the minimum zone, and it is equal only when the least-squares parameters also minimize $W$.

## Variants

- **The reference.** The minimum zone is the reference that standards use to define form tolerances, as in ISO 1101 and ASME Y14.5, cited here as whole standards. Other references are used in practice and can be stated on a drawing: the least-squares (Gaussian) feature, and for round features the minimum circumscribed and the maximum inscribed circle or cylinder. Each gives a valid zone of the same shape, so each width is at least $E$.
- **Straightness in space.** The straightness of a line in space, or of the median line of a cylinder, has a cylindrical zone: the least radius of a cylinder that holds the points, doubled. Carr and Ferreira treat the median line.
- **Profile tolerances.** A profile of a line or a surface has a zone of constant width around the CAD shape. When the zone may float, the problem includes the rigid motion of the CAD model, which is [inspection localization](/inspection-localization/).
- **Orientation and location.** With a datum, the direction or the position of the zone is fixed by the [datum reference frame](/datum-reference-frame/), and fewer parameters are free. For example, parallelism to a datum plane is the extent of the points along the datum normal, with no minimization.
- **Vertical and linearized forms.** If the deviations are measured along a fixed axis, or are linearized for small errors, the problem becomes a [linear program](/linear-programming-problem/). These are approximations of the true zone.

## Examples

**Straightness.** The points $(0,0), (1,0), (2,0), (3,0), (4,1)$ in a plane. Their convex hull is the triangle $(0,0), (3,0), (4,1)$. The thinnest strip is bounded by the line through $(0,0)$ and $(4,1)$ and the parallel line through $(3,0)$, so the straightness is $3/\sqrt{17} \approx 0.7276$. The least-squares line through the centroid $(2, 0.2)$ has slope about $0.208$, and the strip between the extreme points parallel to it has the width $0.7754$. The vertical regression line, of slope $0.2$, gives a strip of orthogonal width $0.7845$.

**Flatness.** The four vertices of the regular tetrahedron $(0,0,0), (1,1,0), (1,0,1), (0,1,1)$ have flatness $1$, attained by two opposite edges in the planes $z = 0$ and $z = 1$. Resting a plane on a face gives $2/\sqrt 3 \approx 1.155$. The [minimum zone flatness](/minimum-zone-flatness/) page proves that one of these two kinds of contact always gives the optimum.

**Roundness.** For points on a circle, the form error is $0$. For a section with lobes, the two minimum zone circles together touch at least four points, at least one on each circle: three on one circle and one on the other, or two and two. The optimal center is a vertex of the nearest point or the farthest point Voronoi diagram, or a crossing of their edges, as the [minimum width annulus](/minimum-width-annulus/) page shows.

## Known algorithms

| form | method | result | guarantee |
| --- | --- | --- | --- |
| straightness | hull edge against the farthest vertex, [polygon width](/polygon-width/) | exact | $O(n \log n)$ |
| flatness | [minimum zone flatness](/minimum-zone-flatness/), face-vertex and edge-edge pairs of the hull | exact | $O(n^2)$; Houle and Toussaint $O(n \log n + I)$ |
| flatness | width by parametric search or randomization | exact | $O(n^{3/2+\varepsilon})$ expected (Agarwal and Sharir) |
| roundness | [minimum width annulus](/minimum-width-annulus/) from the overlay of the nearest and farthest point Voronoi diagrams | exact | $O(n^2)$, and subquadratic bounds |
| cylindricity | [minimum zone cylindricity](/minimum-zone-cylindricity/), sequential linear programming | local optimum | none global |
| cylindricity | minimum width cylindrical shell (Agarwal, Aronov and Sharir) | exact, or within a constant factor | polynomial, of high degree |
| all | [least-squares reference feature](/least-squares-reference-feature/) | upper bound | closed form for lines and planes, iterative for circles and cylinders |

The least-squares fits of circles and cylinders are the subject of [circle fitting](/circle-fitting/) and [geometric primitive fitting](/geometric-primitive-fitting/). Their zones are upper bounds of $E$, and they are good starting points for a local minimum zone method.

## Bounds

- **Monotone in the points.** $W(\theta)$ is a maximum over the points, so adding points never lowers $E$. The form error of a sample is a lower bound for the form error of the surface it was taken from. How close it comes depends on the sample size and spread, which is why [sampling plans](/hammersley-sampling-for-cmm/) matter.
- **Other references.** For every $\theta$, $W(\theta) \ge E$. This holds for the least-squares feature, the minimum circumscribed and maximum inscribed features, and any approximate optimizer, so every such method reports an upper bound of the minimum zone value of the sample.
- **Vertical flatness.** If the vertical Chebyshev plane has vertical thickness $V^*$ and the minimum zone plane has slope $g$, then $E \le V^* \le E \sqrt{1 + \lvert g \rvert^2}$. The proof is on the [minimum zone flatness](/minimum-zone-flatness/) page.
- **Exactness.** Straightness, flatness and roundness have exact polynomial algorithms, with the optimum at a finite set of contact configurations. Cylindricity also has an exact polynomial algorithm, but its high degree makes local methods the practical choice; those carry no global guarantee.

## Reductions

- **Flatness is the width of a point set** in three dimensions, and straightness in a plane is the width of a planar set, which is attained by an edge and an antipodal vertex of the hull.
- **Roundness is the minimum width annulus**, the thinnest ring between two concentric circles that holds a planar point set.
- **Cylindricity is the minimum width cylindrical shell.** With the axis fixed, the width is the range of the distances to the axis, so the problem is a minimization over the four parameters of a line.
- **Least-squares references reduce to eigenproblems and nonlinear least squares.** The plane and the line through the centroid come from the smallest or the largest eigenvector of the covariance matrix; circles and cylinders need iterations.
- **Linearized forms are linear programs.** For small deviations, the minimum zone problems with a fixed reference direction have a constant number of variables, so they are [LP-type problems](/lp-type-problem/) solvable in expected linear time.

## Applications

- **Inspection with coordinate measuring machines.** After the points are measured and the part is aligned, each toleranced feature is evaluated; see [CAD-based inspection](/cad-based-inspection/) and [geometric dimensioning and tolerancing](/geometric-dimensioning-and-tolerancing/).
- **Acceptance of parts.** A part conforms to a form tolerance if $E$ is at most the tolerance. A least-squares evaluation may reject a good part, since it overstates $E$, but it never accepts a part whose sampled points violate the minimum zone tolerance.
- **Testing measurement software.** Reference data sets with known minimum zone and least-squares values are used to check the algorithms in CMM software.
- **Process control.** Flatness and cylindricity of machined faces and bores are tracked over time to detect tool wear and machine errors.

## References
