---
tag: WQC417
kind: model
slug: tolerance-map
name: Tolerance map
aliases:
- T-Map
area: cad/reverse-engineering-and-inspection
level: research
summary: Davidson, Mujezinovic and Shah's convex set in a space of feature deviations holding every variation a tolerance allows, combined by Minkowski sums in stack-ups.
prereqs: [small-displacement-torsor, minkowski-sum]
see_also: [convex-set, support-function, convex-polytope, requicha-tolerance-zone-theory, jacobian-torsor-model, tolerance-stack-up, geometric-dimensioning-and-tolerancing, datum-reference-frame]
sources:
  - paper: doi:10.1115/1.1497362
    title: Joseph K. Davidson, Amir Mujezinović and Jami J. Shah, A new mathematical model for geometric tolerances as applied to round faces, Journal of Mechanical Design 124(4), 609 to 622, 2002
    locator: the whole paper (the Tolerance-Map of a round face as a set of points in a space of deviations, its convexity, its subsets for orientation and form, and the accumulation of T-Maps by Minkowski sums)
  - paper: "Amir Mujezinović, Joseph K. Davidson and Jami J. Shah, A new mathematical model for geometric tolerances as applied to polygonal faces, Journal of Mechanical Design 126, 504 to 518, 2004"
    locator: the Tolerance-Maps of rectangular and triangular faces
  - book: isbn:9781107601017
    title: Rolf Schneider, Convex Bodies, the Brunn-Minkowski Theory, 2nd edition, Cambridge University Press, 2014
    locator: Chapter 1, the support function and its additivity under Minkowski addition
  - url: https://arxiv.org/abs/1106.6148
    title: Denis Teissandier, Vincent Delos and Yves Couétard, Operations on polytopes, application to tolerance analysis, arXiv 1106.6148, 2011 (a paper of the 6th CIRP Seminar on Computer Aided Tolerancing, 1999)
    locator: the whole paper (the polytope form of the same idea, with Minkowski sums and intersections of polytopes of torsors)
  - paper: doi:10.1016/j.cad.2014.02.014
    title: Hua Chen, Sun Jin, Zhimin Li and Xinmin Lai, A comprehensive study of three dimensional tolerance analysis methods, Computer-Aided Design 53, 1 to 13, 2014
    locator: the part on T-Maps and their comparison with the other 3D tolerance analysis methods
---

A Tolerance-Map, or T-Map, is the set of all positions of an ideal feature that its tolerances allow, drawn as a region in a space of a few deviation coordinates. Davidson, Mujezinović and Shah defined it in 2002 for round planar faces, and Mujezinović, Davidson and Shah extended it to polygonal faces in 2004. Each point of a T-Map is one possible plane (or axis, or line) of the actual feature, and the boundary of the map separates the deviations that pass from those that do not. Every T-Map is a [convex set](/convex-set/). In an assembly, the T-Maps of the features in a chain are added by [Minkowski sums](/minkowski-sum/) into an *accumulation map*, and the design meets a functional requirement when this map fits inside the *functional map* of the requirement. T-Map is a registered trademark of the authors' group. The model works with ideal features, like the [small displacement torsor](/small-displacement-torsor/), but it keeps the whole allowed set instead of bounds on each coordinate. [Requicha's zones](/requicha-tolerance-zone-theory/) describe the same tolerances on the real surface, and the [Jacobian-torsor model](/jacobian-torsor-model/) replaces the set by a box of intervals.

## The machine

The "machine" of a variation model is its representation of a part and its assumptions about the deviations.

**The representation.** Take a feature with a tolerance zone, for example a round planar face of radius $r$ in the plane $z = 0$ with the slab $|z| \le t/2$ as its size zone, and put the frame at the centre of the face. A plane near the face is $z = \sigma + \alpha x + \beta y$, with offset $\sigma$ at the centre and slope vector $g = (\alpha, \beta)$. The T-Map of the face is the set of $(\sigma, \alpha, \beta)$ for which this plane, over the face, lies in the zone. Davidson, Mujezinović and Shah use coordinates built from basis points on the face (areal coordinates), which are a linear change of these, so every statement below about shape and convexity carries over. Other features need other coordinates: an axis has four, and a polygonal face three. Tighter refinements of a tolerance, such as an orientation tolerance inside a size tolerance, are subsets of the map. A stack-up maps the T-Map of each feature into the coordinates of the target feature by a linear map and adds them by Minkowski sum.

**Assumptions.** The model takes these as given.

- Each feature is an ideal feature: a plane, an axis or a line. Form error is not a coordinate of the map. A form tolerance enters only through the room it leaves for the ideal feature, as in the result on form below.
- Rotations are small. The slope coordinates are exact for one plane, but adding slopes and offsets of features in a chain, and identifying a slope with a rotation angle, is a first-order (small-angle) approximation.
- The maps of the features in a chain are independent, so every combination of their points can occur. This is a worst-case model; the map holds no probabilities.
- The datums are fixed by a [datum reference frame](/datum-reference-frame/), and the coordinates of each T-Map are taken in it.

## What it counts

A variation model counts no cost. This section says which variations the model can express.

- **Size, orientation and location of ideal features, together.** One T-Map holds every combination of offset and tilt that a set of tolerances allows on one feature. The coupling between them is kept: a face that uses up its size tolerance by offset has no room left to tilt, and the map shows it, where a list of separate bounds does not.
- **Refinements as subsets.** An orientation tolerance, a form tolerance or a tighter tolerance on the same feature cuts the map down to a subset, and a set of rules on one feature is the intersection of their maps.
- **Accumulation in an assembly.** The deviations a chain of parts allows at a target face are the Minkowski sum of the mapped T-Maps. Comparing this with the functional map answers a worst-case analysis question.
- **What it cannot express.** Form error inside a feature, beyond the room it takes, is not a coordinate. Large rotations are outside the first-order model. The map has no probabilities, so a statistical analysis needs a layer on top of it. Computing the maps and their Minkowski sums in four or more dimensions is the hard part of using the model, and the papers derive the map of each class of feature separately.

## Relation to other models

- **[Small displacement torsor](/small-displacement-torsor/).** The coordinates of a T-Map are the determined components of the torsor of the feature, up to a linear change. A T-Map is the domain of that torsor: the set of all its allowed values, not one value.
- **Polytopes of torsors.** Teissandier, Delos and Couétard write each specification as a [convex polytope](/convex-polytope/) of torsors, cut by linear inequalities at sample points of the zone, and combine them by Minkowski sums and intersections. A T-Map with curved boundary, such as the double cone below, is the limit of these polytopes as the sample points fill the boundary of the face.
- **[Jacobian-torsor model](/jacobian-torsor-model/).** It keeps only an interval for each torsor component, the smallest box around the T-Map. A box is easy to propagate with interval arithmetic but holds points that the T-Map excludes, so it overestimates the accumulation.
- **[Requicha's tolerance zone theory](/requicha-tolerance-zone-theory/).** A Requicha zone is a set of real surfaces; the T-Map is the set of ideal features that fit inside it. The T-Map loses form and gains a space of a few dimensions.
- **[Tolerance stack-up](/tolerance-stack-up/).** For a chain of one-dimensional dimensions every T-Map is an interval, the Minkowski sum of intervals adds their widths, and the T-Map analysis is the worst-case stack-up.

## Known results in the model

Davidson, Mujezinović and Shah state that every T-Map is convex and derive the maps of round faces; Mujezinović, Davidson and Shah derive those of polygonal faces. The results below are proved here in the slope coordinates of this page. There are no standard benchmarks for tolerance models, and no measured results are claimed.

**Convexity.** For any face $F$ and any slab zone $|z| \le t/2$, the set of $(\sigma, \alpha, \beta)$ with $|\sigma + \alpha x + \beta y| \le t/2$ for all $(x, y) \in F$ is convex. *Proof.* For a fixed point $(x, y)$ the condition is a pair of linear inequalities in $(\sigma, \alpha, \beta)$, so it defines a slab. The set is the intersection of these slabs over all points of $F$, and an intersection of convex sets is convex. $\square$

**The round face with a size tolerance is a double cone.** For a round face of radius $r$ and the zone $|z| \le t/2$, the T-Map is

$$ T(t) = \{(\sigma, g) : |\sigma| + r |g| \le t/2\}, \qquad |g| = \sqrt{\alpha^2 + \beta^2}. $$

*Proof.* The plane over the face takes its largest and smallest values where $(x, y)$ points along $g$ and against $g$ on the rim, so its range is $[\sigma - r|g|, \sigma + r|g|]$. This range lies in $[-t/2, t/2]$ exactly when $|\sigma| + r|g| \le t/2$. $\square$ In the space $(\sigma, \alpha, \beta)$ this is two right circular cones base to base: the apexes are at $\sigma = \pm t/2$ with zero tilt, and the common base is the disk $\sigma = 0$, $|g| \le t/(2r)$. For a face of diameter 20 mm with $t = 0.1$ mm, the face may tilt by 0.005 rad when it is centred, but only by $(0.05 - 0.03)/10 = 0.002$ rad when its centre is 0.03 mm off. For a rectangular face the same argument with corners in place of the rim gives an octahedron, as the [plane example of the SDT page](/small-displacement-torsor/) shows.

**An orientation tolerance is a cylinder cut.** Add a parallelism tolerance $t_o < t$ to the same face. The face, at any offset, must lie between two parallel planes $t_o$ apart parallel to the datum, so its range $2 r |g|$ is at most $t_o$. The T-Map becomes $T(t) \cap \{r |g| \le t_o / 2\}$, the double cone with its rim cut off by a cylinder. For $t = 0.1$ and $t_o = 0.04$ on the 20 mm face, the tilt is capped at 0.002 rad, and the cap is active exactly where $|\sigma| \le 0.03$.

**A form tolerance shrinks the map of the zone.** A flatness tolerance $t_f < t$ lets the actual face lie in some slab of width $t_f$ that floats inside the size zone. To first order, the mid-plane of that floating slab must satisfy $|\sigma| + r|g| \le (t - t_f)/2$, so the map of positions of the flatness zone is $T(t - t_f)$, a smaller double cone. *Proof.* The floating slab covers the range $[\sigma - r|g| - t_f/2, \sigma + r|g| + t_f/2]$ over the face, measured along $z$. This lies in $[-t/2, t/2]$ exactly when the inequality holds. Measuring the width along $z$ instead of along the normal of the tilted plane is the first-order step. $\square$

**Scaled copies add.** For a convex set $K$ and $a, b \ge 0$, $aK \oplus bK = (a + b) K$. *Proof.* Each point of $(a+b)K$ is $a k + b k$ with $k \in K$. Conversely, $a x + b y = (a + b)\big(\tfrac{a}{a+b} x + \tfrac{b}{a+b} y\big)$ lies in $(a + b) K$ by convexity. $\square$ All double cones $T(t)$ of one radius are scaled copies of $T(2)$, so $T(t_1) \oplus T(t_2) = T(t_1 + t_2)$.

**Worst cases add.** The [support function](/support-function/) of a set $A$ is $h_A(c) = \max_{x \in A} c \cdot x$. For any sets $A$ and $B$, $h_{A \oplus B} = h_A + h_B$, because the maximum of $c \cdot (a + b)$ over independent $a$ and $b$ is the sum of the two maxima. So the worst value of any linear functional, such as the height of one point of the target face, over an accumulation map is the sum of its worst values over the feature maps. This is why a T-Map analysis reduces to the worst-case formula of the [stack-up](/tolerance-stack-up/) for each single linear output, and differs from it only when several outputs are judged together.

**Example, two stacked plates.** Plate 1 has its top face at $10 \pm 0.05$ above the datum face, and plate 2, of the same diameter 20 mm, is $5 \pm 0.025$ thick and sits on it. To first order the offset and the slope of the top of plate 2 relative to the datum are the sums of those of the two faces, so the accumulation map is $T(0.1) \oplus T(0.05) = T(0.15)$. A functional requirement "the top face lies within $15 \pm 0.1$" has the functional map $T(0.2)$, which contains $T(0.15)$, so the design passes. If the requirement adds parallelism 0.05 to the datum, its functional map is $T(0.2) \cap \{10 |g| \le 0.025\}$. The accumulation map holds the point $\sigma = 0$, $|g| = 0.0075$, so the design fails. Parallelism tolerances on the plates must then cut their maps, for example to $10|g| \le 0.0125$ each.

## References
