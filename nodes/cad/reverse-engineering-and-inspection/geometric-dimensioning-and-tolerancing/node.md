---
tag: SXGF4Q
kind: concept
slug: geometric-dimensioning-and-tolerancing
name: Geometric dimensioning and tolerancing
aliases:
- GD&T
- geometric tolerancing
area: cad/reverse-engineering-and-inspection
level: intro
summary: A language of tolerance zones, datums and material conditions, set in ASME Y14.5 and ISO 1101, that states how far each feature of a part may vary.
see_also: [datum-reference-frame, tolerance-stack-up, requicha-tolerance-zone-theory, small-displacement-torsor, tolerance-map, form-error-evaluation, minimum-zone-flatness, three-two-one-locating-principle]
sources:
  - url: https://www.asme.org/codes-standards/find-codes-standards/y14-5-dimensioning-tolerancing
    title: ASME Y14.5-2018, Dimensioning and Tolerancing, The American Society of Mechanical Engineers, 2019
    locator: the standard as a whole (symbols, datum reference frames, material condition modifiers, and the tolerances of form, orientation, location, profile and runout)
  - url: https://www.iso.org/standard/66777.html
    title: ISO 1101:2017, Geometrical product specifications (GPS), Geometrical tolerancing, Tolerances of form, orientation, location and run-out, fourth edition
    locator: the standard as a whole (the tolerance characteristics, their symbols and their tolerance zones)
  - book: isbn:9780750667388
    title: Georg Henzold, Geometrical Dimensioning and Tolerancing for Design, Manufacturing and Inspection, second edition, Butterworth-Heinemann, 2006
    locator: the chapters on form, orientation, location and run-out tolerances, datums, and the maximum material requirement, with the ISO and ASME rules side by side
  - paper: "Aristides A. G. Requicha, Toward a theory of geometric tolerancing, The International Journal of Robotics Research 2(4), 1983, 45 to 60"
    locator: the tolerance zone as a region of space that the actual surface must lie in
  - paper: doi:10.1080/00207540210128242
    title: Y. S. Hong and T. C. Chang, A comprehensive review of tolerancing research, International Journal of Production Research 40(11), 2002, 2425 to 2459
    locator: the parts on tolerance specification and representation
---

Geometric dimensioning and tolerancing (GD&T) is the language that engineering drawings and 3D models of mechanical parts use to say how far each feature of a real part may differ from its ideal shape. Each requirement names a feature, a *tolerance zone* (a region of space of a given shape and size), and often a [datum reference frame](/datum-reference-frame/) that fixes where the zone is. The feature of the real part must lie inside its zone. The two main rule sets are ASME Y14.5 (in the United States, latest edition 2018) and the ISO system of geometrical product specification, whose core standard for this topic is ISO 1101 (latest edition 2017). This page is about mechanical parts. The "tolerance" of chip timing in electronic design automation is a different subject.

## In plain words

A drawing says that a plate is 100 millimeters long. No real plate is exactly 100 millimeters long, so the drawing must also say how much error is fine. The old way gives each dimension a plus or minus. That is not enough: it does not say how flat a face must be, how square two faces must be, or from which faces to measure a hole.

For each feature, it draws an imaginary region around the ideal shape: two parallel planes for a flat face, a thin cylinder for the axis of a hole. The real surface or axis must stay inside that region. A small set of reference faces, called datums, says where the region sits. Special symbols say that a region may grow when a hole is made larger than its smallest size, because a larger hole still lets the bolt go in.

## The idea

**Features and zones.** A *feature* is a physical portion of the part: a face, a hole, a slot, a pin. A *feature of size* is a feature with opposite points that a size can be measured across, such as a cylinder or two parallel faces. A *derived feature* is a point, line or plane that is computed from a real feature, such as the axis of a hole or the median plane of a slot. A geometric tolerance $t$ defines a zone $Z$ of one of a few shapes:

| zone | for |
| --- | --- |
| two parallel planes at distance $t$ | flatness, a flat face in orientation or location |
| two parallel lines at distance $t$, in a section | straightness of a line element |
| a cylinder of diameter $t$ | the axis of a hole or a pin, when the value has the sign $\varnothing$ |
| two coaxial cylinders with radial difference $t$ | cylindricity |
| two concentric circles with radial difference $t$, in each cross section | circularity (roundness) |
| the region between two surfaces offset by $\pm t/2$ from the true profile | profile of a surface (the bilateral default) |

The requirement is $F \subseteq Z$, where $F$ is the real feature (or the derived feature computed from it). For form tolerances the zone may float and turn freely. The measured value is then the width of the thinnest zone of the given shape that holds the feature, the *minimum zone*, which the [form error evaluation](/form-error-evaluation/) and [minimum zone flatness](/minimum-zone-flatness/) pages compute. Requicha (1983) made the zone idea exact for solid models, as regions between offsets of the nominal boundary ([Requicha's tolerance zone theory](/requicha-tolerance-zone-theory/)).

**The five types.** The characteristics fall into five families. Each family says what the zone may do.

| family | characteristics | needs a datum | what the zone is tied to |
| --- | --- | --- | --- |
| form | straightness, flatness, circularity, cylindricity | no | nothing: the zone floats and turns |
| orientation | parallelism, perpendicularity, angularity | yes | the angle to the datums; the zone can still shift |
| location | position (ISO also lists coaxiality, concentricity and symmetry) | yes, in most uses | the angle and the place, from the datums with basic (exact) dimensions |
| profile | profile of a line, profile of a surface | optional | the true profile; with datums it also fixes orientation and place |
| runout | circular runout, total runout | yes, a datum axis | the indicator reading while the part turns about the datum axis |

A location zone also limits orientation and form, and an orientation zone also limits form. So the families form a hierarchy, and a refinement such as a flatness value inside a position value must be smaller to have any effect. ISO 1101:2017 has 14 characteristics. ASME Y14.5-2018 removed concentricity and symmetry, which leaves 12, and directs the designer to position, profile or runout instead. *Basic dimensions*, shown in a box on the drawing, are exact values that place a zone. They have no tolerance of their own, because the zone carries it.

**Datums.** A datum is a theoretically exact point, axis or plane derived from a real feature of the part, the *datum feature*. A feature control frame lists up to three datums in order of precedence: primary, secondary and tertiary. They define a [datum reference frame](/datum-reference-frame/), a coordinate system in which the basic dimensions place the zone. ISO describes datums in a separate standard, ISO 5459.

**Material condition modifiers.** A feature of size has a *maximum material condition* (MMC, the size at which the part has the most material: the smallest hole, the largest pin) and a *least material condition* (LMC, the opposite limit). A modifier in the feature control frame says at which size the stated tolerance holds:

| modifier | ASME name | ISO name | meaning |
| --- | --- | --- | --- |
| none | regardless of feature size (RFS) | (independent) | the tolerance is the same at every size |
| circled M | maximum material condition | maximum material requirement | the tolerance holds at MMC, and grows by the departure of the actual size from MMC (the *bonus*) |
| circled L | least material condition | least material requirement | the tolerance holds at LMC, and grows by the departure from LMC |

A modifier can also apply to a datum feature of size. Then the datum frame may shift relative to the part by the departure of the datum feature from its stated condition (the *datum shift*).

*Virtual condition.* For a hole with MMC size $d_M$ and a position tolerance $t$ at MMC, the *virtual condition* is $V = d_M - t$. For a pin it is $V = d_M + t$. It is the size of the worst boundary that the feature can present to a mating part.

*Why the bonus rule is right.* Assume a hole of perfect form, of actual diameter $d \ge d_M$, with its axis at distance $e$ from the true position. The cylinder of diameter $V = d_M - t$ on the true axis lies inside the hole if and only if $e + V/2 \le d/2$, that is, $2e \le t + (d - d_M)$. The left side is the diameter of the smallest zone, centered on the true position, that holds the axis. So "the axis lies in a zone of diameter $t$ plus the bonus $d - d_M$" is exactly the condition that a fixed pin of size $V$ at the true position enters the hole. This is why a fixed functional gauge checks a position tolerance at MMC, and why the bonus costs nothing in function. For a hole of imperfect form the equivalence fails, and the standards define the requirement through the boundary of size $V$.

**Rule 1 and independence.** ASME Y14.5 has a default rule (often called Rule 1, the envelope principle): when only a size tolerance is given, the surface of a feature of size may not pass the boundary of perfect form at MMC. So a size tolerance also limits form. ISO 8015 sets the opposite default, the independence principle: size and form are separate requirements unless the envelope modifier (circled E) is given. A drawing must say which system it follows, because the same symbols then mean different parts.

**What GD&T is not.** It is a language for a requirement, not a method of analysis. To find out whether parts made within their tolerances will assemble, one needs a model of variation: the [tolerance stack-up](/tolerance-stack-up/) for one-dimensional chains, and the [small displacement torsor](/small-displacement-torsor/), [tolerance maps](/tolerance-map/) or the [Jacobian-torsor model](/jacobian-torsor-model/) for the 3D case. To find out whether a measured part meets them, one needs [form error evaluation](/form-error-evaluation/) and a datum frame built from the measured points.

## Examples

**A diameter zone and a square zone.** A hole is placed with coordinates $\pm 0.05$ mm in $x$ and $y$. The allowed centers form a square of side $0.1$, whose diagonal is $0.1\sqrt 2 \approx 0.1414$. A position tolerance of $\varnothing 0.1414$ has a circular zone that holds the square, and its area is larger by the factor $\pi/2 \approx 1.571$. Every hole that the coordinate tolerance accepts is still accepted, and the holes at the same distance from the true position in a diagonal direction and along an axis are treated the same, which is what the mating pin sees.

**Bonus tolerance, worked.** A hole has a size of $10.0$ to $10.2$ mm and a position tolerance of $\varnothing 0.1$ at MMC relative to datums A, B and C. The MMC is $d_M = 10.0$ and the virtual condition is $V = 9.9$.

| actual size $d$ | bonus $d - 10.0$ | allowed position zone |
| --- | --- | --- |
| $10.00$ | $0.00$ | $\varnothing 0.10$ |
| $10.15$ | $0.15$ | $\varnothing 0.25$ |
| $10.20$ (LMC) | $0.20$ | $\varnothing 0.30$ |

A mating pin of size $9.7$ to $9.8$ with position $\varnothing 0.1$ at MMC has virtual condition $9.8 + 0.1 = 9.9$. The two virtual conditions are equal, so every pair of good parts goes together when their datum frames coincide, and the worst pair touches with zero clearance.

**Circular runout.** A shaft section is a perfect circle of radius $12.5$ mm whose center is $e = 0.02$ mm from the datum axis. As the shaft turns, the radius seen by a fixed dial indicator is $r(\theta) = e\cos\theta + \sqrt{R^2 - e^2 \sin^2\theta}$, which runs from $R - e$ to $R + e$. The full indicator movement is $2e = 0.04$ mm. So a circular runout tolerance of $0.04$ holds this section exactly. Runout mixes the error of center (location) and the error of roundness (form) into one number.

**Non-example: a plus or minus on an angle.** "Perpendicular to the base $\pm 0.5°$" is not a GD&T requirement. An angle tolerance gives a wedge-shaped zone that grows with the length of the feature, and it does not say from which line on the real, imperfect base the angle is measured. A perpendicularity tolerance of $0.05$ to datum A gives a zone of two parallel planes $0.05$ apart, perpendicular to the datum plane established from the base.

**Non-example: a flatness smaller than nothing.** A face with a position tolerance of $0.1$ and a flatness of $0.2$ has a useless flatness: the position zone already limits the form to $0.1$. A refinement must be smaller than the tolerance it refines.

## Where it is used

- **Design.** The designer writes the function of each feature as zones and datums: the faces that locate the part in its assembly become the datums, and the holes for fasteners get position tolerances at MMC.
- **Tolerance analysis and allocation.** A stack-up reads its chain of dimensions from the GD&T callouts. The [direct linearization method](/direct-linearization-method/), [Monte Carlo tolerance analysis](/monte-carlo-tolerance-analysis/) and [tolerance allocation](/tolerance-allocation/) need a model that turns each zone into a variation of the feature.
- **Inspection.** A coordinate measuring machine measures points. Software builds the [datum reference frame](/datum-reference-frame/) from the datum features, fits each toleranced feature ([least-squares reference features](/least-squares-reference-feature/) or minimum zone fits), and compares the result with the zone. The choice of fit changes the reported value, and only the minimum zone matches the definition of a form tolerance.
- **Fixturing and process planning.** The datum faces of the drawing are often the faces that the [3-2-1 locating principle](/three-two-one-locating-principle/) uses in the fixture, so that the frame of the machine and the frame of the drawing agree.
- **Solid modeling.** Product manufacturing information in a 3D model attaches the same callouts to faces of the [boundary representation](/boundary-representation/).

## References
