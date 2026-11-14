---
tag: EGVHRP
kind: model
slug: requicha-tolerance-zone-theory
name: Requicha's tolerance zone theory
aliases:
- offset zone tolerancing
area: cad/reverse-engineering-and-inspection
level: advanced
summary: Requicha's meaning of tolerances as zones bounded by offsets of the nominal boundary, inside which the actual surface of the part must lie.
prereqs: [r-set, solid-offsetting, geometric-dimensioning-and-tolerancing]
see_also: [offset-surface, hausdorff-distance, small-displacement-torsor, tolerance-map, jacobian-torsor-model, datum-reference-frame, minimum-zone-flatness, form-error-evaluation]
sources:
  - paper: doi:10.1177/027836498300200403
    title: Aristides A. G. Requicha, Toward a theory of geometric tolerancing, The International Journal of Robotics Research 2(4), 45 to 60, 1983
    locator: the whole paper (a tolerance specification as a set of constraints on surface features, tolerance zones built by offsetting the nominal boundary, variational classes, and the remark that RFS position tolerances have no counterpart in offset solids)
  - paper: "Aristides A. G. Requicha and Stephen C. Chan, Representation of geometric features, tolerances, and attributes in solid modelers based on constructive geometry, IEEE Journal of Robotics and Automation 2(3), 156 to 166, 1986"
    locator: the representation of surface features and of their tolerances as attributes attached to a CSG solid
  - paper: doi:10.1016/0167-8396(86)90017-8
    title: Jaroslaw R. Rossignac and Aristides A. G. Requicha, Offsetting operations in solid modelling, Computer Aided Geometric Design 3(2), 129 to 148, 1986
    locator: the definitions of growing and shrinking a solid, and their use to build tolerance zones
  - paper: doi:10.1145/356827.356833
    title: Aristides A. G. Requicha, Representations for rigid solids, theory, methods, and systems, ACM Computing Surveys 12(4), 437 to 464, 1980
    locator: r-sets, the model of a solid that the theory uses for both the nominal and the actual part
  - paper: "Rangarajan Jayaraman and Vijay Srinivasan, Geometric tolerancing, I. Virtual boundary requirements, IBM Journal of Research and Development 33(2), 90 to 104, 1989"
    locator: the virtual boundary requirements, a later formulation of tolerances by bounding solids
  - paper: doi:10.1080/00207540210128242
    title: Y. S. Hong and T. C. Chang, A comprehensive review of tolerancing research, International Journal of Production Research 40(11), 2425 to 2459, 2002
    locator: the part on tolerance representation, where the offset zone model is one of the classes of models
---

Requicha's tolerance zone theory, from his 1983 paper "Toward a theory of geometric tolerancing", gives a tolerance an exact meaning as a set. The nominal part is an [r-set](/r-set/) $S$. A tolerance on a surface feature of $S$ defines a *tolerance zone*, the region between an outward and an inward [offset](/solid-offsetting/) of the nominal boundary. An actual part is in tolerance when each of its toleranced surface features lies inside its zone. The set of all parts that pass is the *variational class* of the specification. The model is a pass or fail test on the whole surface. It uses no linearization and no statistics, so it is exact for any size of deviation, and it is the most direct reading of a profile tolerance in [GD&T](/geometric-dimensioning-and-tolerancing/). The other three variation models on this site describe a deviation by a few numbers: [small displacement torsors](/small-displacement-torsor/), [Tolerance-Maps](/tolerance-map/) and [Jacobian torsors](/jacobian-torsor-model/). Requicha's model describes it by the surface itself, so it also covers form error, which they do not.

## The machine

The "machine" of a variation model is its representation of a part and its assumptions about the deviations.

**The representation.** Write $d(p, A)$ for the Euclidean distance from a point $p$ to a set $A$. For a solid $S$ and a distance $r \ge 0$, Rossignac and Requicha define the grown solid $S \uparrow r = \{p : d(p, S) \le r\}$ and the shrunk solid $S \downarrow r$, the points whose ball of radius $r$ stays in $S$. For an outward tolerance $t_+ \ge 0$ and an inward tolerance $t_- \ge 0$ the zone of the whole boundary is the region between the two offsets:

$$ Z(S; t_+, t_-) = \{p : d(p, S) \le t_+ \text{ and } d(p, E^3 \setminus S) \le t_-\}. $$

A point outside $S$ is in $Z$ when it is at most $t_+$ from $S$, and a point inside $S$ is in $Z$ when it is at most $t_-$ from the outside. In Requicha's theory a tolerance acts on a *surface feature*, a two-dimensional subset $F$ of the boundary $\partial S$, such as one face or the cylinder of a hole. The zone of $F$ is built from offsets of $S$ and of nearby features by Boolean operations, so that it is a thick shell around $F$ only. A specification is a list of pairs (feature, zone). An actual part $X$, also an r-set, satisfies it when the matching feature of $X$ lies in each zone. The *variational class* $V$ of the specification is the set of all r-sets that satisfy it. The zones are placed in the [datum reference frame](/datum-reference-frame/) of the drawing, which fixes where the nominal $S$ is.

**Assumptions.** The model takes these as given.

- The nominal part and each actual part are r-sets: bounded, closed, regular and semianalytic. Roughness below the scale of the tolerance is not part of the model; the actual surface is the measured or idealized boundary.
- The correspondence between a nominal feature and the feature of the actual part is known. The theory does not say how to cut the actual boundary into features.
- A zone that comes only from offsets of $S$ is fixed in space in the datum frame. A deviation of any kind, size, form, orientation or location, counts against the same zone.
- The test is deterministic. There is no distribution of deviations, so the model answers "does this part pass", not "what fraction of parts pass".
- There is no small-angle or first-order approximation. A large rotation is judged exactly by where the rotated surface lies.

## What it counts

A variation model counts no cost. This section says which variations the model can express.

- **Size and form together.** The zone of a feature of size, such as a pin of nominal radius $R$ with $t_+ = t_- = t$, is the shell between the cylinders of radius $R + t$ and $R - t$ about the nominal axis. A pin whose surface lies in it has every surface point at a distance from the nominal axis in $[R - t, R + t]$ and a cylindricity error of at most $2t$, because the minimum zone is never wider than one particular zone. Size and form are controlled by one tolerance, as in an envelope requirement.
- **Location and orientation against the datums.** The zone is fixed in the datum frame, so a shift or a tilt of the feature also uses up the tolerance. A flat face of length 50 that is tilted by 0.002 rad has ends that move by 0.05 in opposite directions, so it needs a zone at least 0.1 wide even when it is perfectly flat.
- **Profile tolerances.** A bilateral profile of a surface with total width $t$ is exactly the fixed zone with $t_+ = t_- = t/2$, for any shape of surface. This is the case the model covers most directly.
- **Material condition boundaries.** A hole at maximum material condition with a position tolerance is accepted when its surface does not enter a fixed cylinder of the virtual condition size at the true position, plus its size limits. For a nominal hole of radius $R$ and a virtual condition diameter $v < 2R$, that cylinder is the cavity that the hole leaves in the grown solid $S \uparrow (R - v/2)$, so this tolerance has a direct offset form.
- **What fixed offset zones cannot express.** A form tolerance alone, such as flatness 0.02 on a face that may sit anywhere within a size tolerance of 0.2, needs a zone that may move with the face. An orientation tolerance needs a zone that may translate but not rotate. Requicha states in the paper that he could not give an offset counterpart for a position tolerance regardless of feature size (RFS), because that tolerance needs a bounded zone, while zones made from offset solids are in general unbounded on one side. Statistical tolerances are outside the model.

The usual way to express form and orientation in the same language lets the zone of a feature move under a subgroup $G$ of rigid motions: the feature $F_X$ passes when $F_X \subseteq g(Z_F)$ for some $g \in G$. With $G$ trivial this is the fixed zone of the theory, with $G$ the translations it is an orientation zone, and with $G$ all rigid motions it is a form zone. The subgroups are the stabilizers that a datum reference frame leaves free.

## Relation to other models

- **[Small displacement torsor](/small-displacement-torsor/).** The torsor model replaces a feature by an ideal feature of the nominal shape and records only its small rigid motion, six numbers. Requicha's model keeps the whole surface, so form error is part of it, and it needs no small-angle approximation. The torsor model gives linear constraints that are easy to add up along an assembly; the offset zone does not.
- **[Tolerance-Map](/tolerance-map/).** A T-Map is the set of all positions of an ideal feature that fit in a tolerance zone. For a planar face the zone is the slab between two parallel planes, the fixed offset zone of this page, and the T-Map is the set of planes inside it. So the T-Map is the image of a Requicha zone in a space of a few parameters, and it drops form error.
- **[Jacobian-torsor model](/jacobian-torsor-model/).** It writes the zone of each feature as intervals on the six torsor components and pushes them through a linear map. A box of intervals is a coarse outer bound of the set of ideal features that fit in the zone.
- **[GD&T](/geometric-dimensioning-and-tolerancing/) and the standards.** Profile tolerances and the envelope at maximum material are fixed or one-sided offset zones. Form and orientation tolerances are floating zones, which need the extension above. Jayaraman and Srinivasan wrote tolerances as virtual boundary requirements on solids, a later formulation in the same language of bounding sets.
- **Measurement.** Checking a part against a fixed zone is a [Hausdorff distance](/hausdorff-distance/) bound, see below. Checking a floating zone is a minimum zone problem, such as [minimum zone flatness](/minimum-zone-flatness/), and the general task is [form error evaluation](/form-error-evaluation/).

## Known results in the model

The facts below are proved here from the definitions. Requicha's paper also states a conjecture: variational classes are regular closed sets in a hyperspace whose points are r-sets. As far as the sources here show, it is still a conjecture. There are no standard benchmarks for tolerance models, and no measured results are claimed.

**The symmetric zone is a tube about the boundary.** For an r-set $S$ and $t_+ = t_- = t$, $Z(S; t, t) = \{p : d(p, \partial S) \le t\}$. *Proof.* If $p \notin S$, then $d(p, E^3 \setminus S) = 0$, and $d(p, S) = d(p, \partial S)$ because the nearest point of the closed set $S$ to an outside point is on its boundary. If $p \in S$, then $d(p, S) = 0$, and $d(p, E^3 \setminus S) = d(p, \partial S)$ by the same argument applied to the closure of the complement, whose boundary is $\partial S$ when $S$ is regular. In both cases the two conditions of $Z$ reduce to $d(p, \partial S) \le t$. $\square$

**A fixed zone test is a one-sided Hausdorff bound.** By the last result, $\partial X \subseteq Z(S; t, t)$ holds if and only if $\sup_{x \in \partial X} d(x, \partial S) \le t$. This is the directed Hausdorff distance from $\partial X$ to $\partial S$. The other direction, from $\partial S$ to $\partial X$, is not tested directly. The next result shows that it follows when the part fills the inner solid.

**Boundary zones and solid envelopes agree.** Let $I = \{p : d(p, E^3 \setminus S) > t_-\}$, the open inner solid, and $O = \{p : d(p, S) > t_+\}$, the open outside of the outer solid. Then $Z = E^3 \setminus (I \cup O)$.

- If $I \subseteq X \subseteq E^3 \setminus O$, then $\partial X \subseteq Z$. *Proof.* A point $p$ of $\partial X$ is in $X$, so it is not in $O$. The open set $I$ lies in $X$, so it lies in the interior of $X$, and $p$, which is not an interior point, is not in $I$. $\square$
- Conversely, let $\partial X \subseteq Z$, let $I$ be connected and meet $X$, and let $O$ be connected. Then $I \subseteq X \subseteq E^3 \setminus O$. *Proof.* $I$ does not meet $\partial X$, so it is the union of the two disjoint open sets $I \cap \operatorname{int} X$ and $I \setminus X$. As $I$ is connected, one of them is empty. $I$ meets $X$ but not $\partial X$, so it meets $\operatorname{int} X$, and therefore $I \subseteq X$. In the same way $O$ lies in the interior of $X$ or outside $X$. $O$ is unbounded and $X$ is bounded, so $O$ is outside $X$, and $X \subseteq E^3 \setminus O$. $\square$

So for a part without inner voids that cross the zone, "the boundary lies in the zone" and "the part lies between the shrunk and the grown solid" are the same condition. This is how a CSG modeler can test a tolerance with the solid operations of Requicha and Chan.

**Monotone and additive.** If $t_+ \le t_+'$ and $t_- \le t_-'$, then $Z(S; t_+, t_-) \subseteq Z(S; t_+', t_-')$, so a looser tolerance gives a larger variational class. Growing adds, $(S \uparrow a) \uparrow b = S \uparrow (a + b)$, by the triangle inequality and a point on the segment to the nearest point, and shrinking adds in the same way. A grow followed by a shrink by the same amount is not the identity, because it fills concave edges, so the two offsets of a zone are both taken from the nominal $S$.

**Example, the zone of a rectangle.** Take the 2D nominal plate $S = [0, 100] \times [0, 50]$ with $t_+ = t_- = 0.1$. The shrunk plate is the rectangle $[0.1, 99.9] \times [0.1, 49.9]$ with sharp corners, of area $99.8 \cdot 49.8 = 4970.04$. The grown plate has rounded corners of radius 0.1. Its area follows from Steiner's formula $A + P r + \pi r^2$ for a convex set of area $A$ and perimeter $P$: the offset is $S$ plus one strip of width $r$ on each edge (area $P r$) plus a circular sector at each corner, and the sector angles are the exterior angles, which sum to $2 \pi$ (area $\pi r^2$). It is $5000 + 300 \cdot 0.1 + 0.01 \pi \approx 5030.031$. The zone has area about $5030.031 - 4970.04 = 59.991$, slightly less than perimeter times width, $300 \cdot 0.2 = 60$, because the rounded outer corners add $\pi r^2 \approx 0.031$ while the inner rectangle loses $4 r^2 = 0.04$ at its corners. A perfect plate of $100.1 \times 50.05$ placed with one corner at $(-0.05, 0)$ passes: each edge is at most 0.05 outside the nominal edge, and each corner is at most $0.05 \sqrt 2 \approx 0.071$ from $S$. A perfect nominal plate turned by 0.003 rad about its centre fails: the corner at $(100, 50)$ moves to about $(99.925, 50.150)$, which is 0.150 outside the nominal top edge.

## References
