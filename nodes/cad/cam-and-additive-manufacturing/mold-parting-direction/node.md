---
tag: V3RT9B
kind: problem
slug: mold-parting-direction
name: Mold parting direction
aliases:
- moldability analysis
- castability
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Decide whether a part can be cast in a two-piece mold and find the directions in which the two halves separate, for polyhedra in O(n^2) or better.
prereqs: [accessibility-cone, convex-polytope]
see_also: [half-plane-intersection, linear-programming-problem, terrain-visibility, visibility-polygon, swept-volume, build-orientation, convex-hull-3d, set-cover]
sources:
  - paper: doi:10.1016/S0010-4485(01)00119-1
    title: Hee-Kap Ahn, Mark de Berg, Prosenjit Bose, Siu-Wing Cheng, Dan Halperin, Jiří Matoušek and Otfried Schwarzkopf, Separating an object from its cast, Computer-Aided Design 34(8), 2002, 547 to 559; conference version in the 13th ACM Symposium on Computational Geometry, 1997, doi 10.1145/262839.262974
    locator: the model with two opposite translations and an arbitrary parting surface, the characterization by the visibility of the upper and lower facets, the O(n log n) test for one direction, the O(n^4) computation of all directions and the matching lower bound example
  - paper: doi:10.1007/PL00014422
    title: Prosenjit Bose, David Bremner and Marc van Kreveld, Determining the castability of simple polyhedra, Algorithmica 19(1-2), 1997, 84 to 113; conference version in the 10th ACM Symposium on Computational Geometry, 1994, doi 10.1145/177424.177576
    locator: the model with a planar parting surface that splits the boundary into two terrains, the O(n^2 log n) time and linear space test for two single translations, the O(n^2) test for opposite directions, and a convex polyhedron with 12 vertices that has no such parting
  - paper: doi:10.1016/0010-4485(93)90103-U
    title: Lin-Lin Chen, Shuo-Yan Chou and Tony C. Woo, Parting directions for mould and die design, Computer-Aided Design 25(12), 1993, 762 to 768
    locator: visibility maps of pockets on the unit sphere and the choice of a pair of opposite parting directions with the fewest cores
---

In casting and injection molding, liquid material fills a cavity in a mold, hardens, and the mold is opened to take the part out. With a two-piece mold the two halves move apart along a direction $d$, one along $d$ and the other along $-d$, and neither half may be blocked by the part. The problem is to decide whether a given part can be made this way, and to find the directions $d$ that work. Whether a direction works depends on a stronger version of the [accessibility](/accessibility-cone/) of the faces of the part: the faces that the upper half covers must be visible from far away along $d$, and the faces of the lower half must be visible along $-d$. The answer also depends on the model: whether the surface between the two halves must be a plane, and whether the two halves move in opposite directions. Two papers set the main bounds. Bose, Bremner and van Kreveld (1997) require a planar parting surface and decide the question in $O(n^2 \log n)$ time for a polyhedron with $n$ vertices, and in $O(n^2)$ time for opposite directions. Ahn et al. (2002) allow any parting surface with opposite directions, test one direction in $O(n \log n)$ time, and find all directions in $O(n^4)$ time.

## In plain words

To make a plastic or metal part in a mold, you need a hollow of the shape of the part, split into two halves. You fill the hollow, wait, and pull the halves apart, one up and one down.

That only works if no part of the shape hooks into a half. A hole that goes through the part sideways, a groove on the side or a hook all catch the mold when it moves straight up or down. Turning the part may help: a sideways hole stops being a problem if the halves move along the hole.

So the question is: for a given shape, is there a direction in which the two halves can be pulled off, and what are all such directions? A good answer lets the designer pick the direction that needs no extra mold pieces.

## Definition

**Input.** A polyhedron $P$ in $\mathbb{R}^3$: a solid bounded by $n$ vertices and planar facets, given as a boundary representation. Each facet $f$ has an outward unit normal $n_f$.

**Model (Ahn et al. 2002).** A *mold* for $P$ is the closure of $B \setminus P$ for a large box $B$ around $P$, split into two pieces, the upper half $M^+$ and the lower half $M^-$. The surface between them is free. The mold is *removable in direction* $d$ if $M^+$ can be translated to infinity along $d$, and $M^-$ along $-d$, without the interior of either meeting the interior of $P$ during the motion. In other words, the [swept volume](/swept-volume/) of $M^+$ along the ray of $d$ meets $P$ only on the boundary.

**Model (Bose, Bremner and van Kreveld 1997).** In addition, the halves meet $P$ along a plane: there must be a plane that splits the boundary of $P$ into two polyhedral terrains, one for each half, and the halves are removed by one translation each, not necessarily opposite.

**Output.** The decision: is there a removable direction? And the set $D(P) \subseteq S^2$ of all removable directions, as a region of the sphere.

**Characterization.** Call a facet *upper* for $d$ if $n_f \cdot d > 0$ and *lower* if $n_f \cdot d < 0$. In the model of Ahn et al., $P$ has a removable two-piece mold in direction $d$ if and only if every upper facet is visible from infinity along $d$ and every lower facet is visible from infinity along $-d$. Here a facet is visible along $d$ when the open ray from each of its points along $d$ misses the interior of $P$, that is, when $d$ is in the [accessibility cone](/accessibility-cone/) of the facet. Facets parallel to $d$ give no condition.

*Why the condition is necessary.* An upper facet $f$ is covered by the upper half near its points, since the lower half lies on the other side of the parting surface. If the open ray from a point of $f$ along $d$ met the interior of $P$, the bit of mold just above that point would run into $P$ as the upper half moves along $d$. The same holds for the lower facets and $-d$. The converse, that a mold can then be built, is the theorem of Ahn et al.

**Convex parts.** If $P$ is convex, every direction works in the model of Ahn et al.: an upper facet lies on a plane with $P$ below it, so its rays along $d$ stay out of $P$, and the same holds for lower facets and $-d$. In the model with a planar parting surface this is false: Bose, Bremner and van Kreveld (1997) give a convex polyhedron with 12 vertices that has no planar parting into two terrains.

## Variants

- **Opposite directions, free parting surface.** The model of Ahn et al., used for the bounds below.
- **Planar parting surface.** The model of Bose, Bremner and van Kreveld. A planar parting is simpler to machine into the mold.
- **Two independent translations.** The halves move in directions $d_1$ and $d_2$ that need not be opposite. Bose et al. treat this case.
- **Cores and side actions.** When no direction works, extra mold pieces, cores, are pulled out sideways before the halves open. Chen, Chou and Woo (1993) split the part into pockets and choose the pair of opposite directions that needs the fewest cores.
- **One-piece molds.** The mold is open at the top and the part is pulled out of one half, as in some kinds of gravity casting.
- **Draft.** In practice faces parallel to $d$ get a small draft angle so that they slide free. The geometric model ignores friction.

## Examples

**A cube with a side hole.** Let $P$ be the cube $[0, 2]^3$ with a square hole $(0.5, 1.5) \times (0.5, 1.5)$ in $y$ and $z$ drilled through it along the $x$ axis.

- Direction $d = (0, 0, 1)$. The ceiling of the hole, the facet $z = 1.5$ inside the hole, has outward normal $(0, 0, -1)$, pointing into the hole, so it is a lower facet. The ray from a point of the ceiling along $-d$ goes down through the hole and enters the material at the floor $z = 0.5$. The ceiling is not visible along $-d$, so this direction fails: the mold piece inside the hole would be caught.
- Direction $d = (1, 0, 0)$. The faces $x = 0$ and $x = 2$ are lower and upper facets, and their rays leave the cube at once. The four walls of the hole and the other four faces of the cube are parallel to $d$. So this direction works: the halves meet inside the hole and slide out of its two ends.
- Tilting $d$ away from the $x$ axis in the $xz$ plane by an angle $\theta$ makes the ceiling a lower facet again. A ray from the far end of the ceiling must cross the full length $2$ of the hole while dropping at most its height $1$, so $|\tan \theta| \le 1/2$ is needed.

**A convex part.** For a tetrahedron, every direction works in the model of Ahn et al., by the convexity argument above. The parting surface is the silhouette of the tetrahedron seen along $d$, which in general is not planar.

## Known algorithms

- **One direction.** Ahn et al. (2002) test whether a given direction works in $O(n \log n)$ time, using the characterization above.
- **All directions, free parting surface.** Ahn et al. (2002) compute the set of all directions that work in $O(n^4)$ time, and give a lower bound example of size $\Omega(n^4)$.
- **Planar parting surface.** Bose, Bremner and van Kreveld (1997) decide whether a planar parting with two translations exists in $O(n^2 \log n)$ time and linear space, and in $O(n^2)$ time when the directions are opposite.
- **Visibility maps.** Chen, Chou and Woo (1993) compute the visibility map of each pocket, a convex region of the unit sphere, and choose a pair of opposite directions that needs the fewest cores. A direction common to several convex regions of the sphere, each an intersection of hemispheres, is a point of an intersection like that of [half-planes](/half-plane-intersection/), and one such point is found by a small [linear program](/linear-programming-problem/).

These algorithms are exact for polyhedra with exact arithmetic. What is measured, such as the speed on industrial parts, is not covered here.

## Bounds

- $O(n \log n)$ to test one direction in the model of Ahn et al.
- $O(n^4)$ time to find all directions, with a lower bound example of size $\Omega(n^4)$ for the set.
- $O(n^2 \log n)$ time and $O(n)$ space with a planar parting surface and two translations, $O(n^2)$ time with opposite directions (Bose, Bremner and van Kreveld).
- No hardness result applies: all versions above are polynomial. With cores, choosing the fewest extra pieces is a covering question, see [set cover](/set-cover/); no complexity result for it is given here.

## Reductions

- **To visibility.** By the characterization, a direction works if and only if it is in the accessibility cone of every upper facet and in the opposite of the cone of every lower facet. For a convex part this is a condition on the normals alone, and the problem is trivial.
- **To terrains.** With a planar parting surface, each half of the boundary must be a polyhedral terrain in its direction: a surface that every line along the direction meets at most once.

## Applications

- Injection molding of plastic parts and die casting of metal parts, where a direction that needs no cores makes the mold cheaper.
- Choosing the build direction in some additive and hybrid processes, where the same visibility question decides where supports are needed, see [build orientation](/build-orientation/).
- Design feedback: the CAD system marks the faces that block every direction, so the designer can change them.

## References
