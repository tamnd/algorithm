---
tag: 46XK35
kind: problem
slug: undercut-detection
name: Undercut detection
aliases:
- undercut feature recognition
area: cad/manufacturing-process-planning
level: core
summary: Find the regions of a molded or cast part that block its release along the parting direction and so need side cores or a design change.
prereqs: [mold-parting-direction, accessibility-cone]
see_also: [parting-line-generation, draft-angle-analysis, hidden-surface-removal, ray-casting, depth-peeling, feature-recognition, manufacturability-analysis, terrain-visibility]
sources:
  - paper: doi:10.1016/S0010-4485(01)00119-1
    title: Hee-Kap Ahn, Mark de Berg, Prosenjit Bose, Siu-Wing Cheng, Dan Halperin, Jiri Matousek and Otfried Schwarzkopf, Separating an object from its cast, Computer-Aided Design 34(8), 2002, 547 to 559
    locator: the two-piece cast with opposite directions and a free parting surface, the characterization by the visibility of the upper facets along d and of the lower facets along -d, the O(n log n) test of one direction and the O(n^4) computation of all directions
  - title: M. W. Fu, J. Y. H. Fuh and A. Y. C. Nee, Undercut feature recognition in an injection mould design system, Computer-Aided Design 31(12), 1999, 777 to 790
    locator: the recognition of undercut features on a B-rep part from the faces that are not visible in the parting direction (general locator)
  - paper: doi:10.1016/0010-4485(93)90103-U
    title: Lin-Lin Chen, Shuo-Yan Chou and Tony C. Woo, Parting directions for mould and die design, Computer-Aided Design 25(12), 1993, 762 to 768
    locator: the visibility map of each pocket and the choice of the pair of opposite directions with the fewest cores
---

Undercut detection finds the parts of the surface of a molded or cast part that block the two halves of the mold when they move apart along the parting direction $d$. A point of the surface is an undercut when it is closed in from both sides: the ray from it along $+d$ and the ray along $-d$ both pass through the material of the part. Such a point can be formed by neither half, so the mold needs a side core or a lifter there, or the part needs a change. This page defines the undercut region, proves that it is empty exactly when the two-piece mold of Ahn and coauthors works, and gives the methods and bounds. The choice of $d$ is the problem of [mold parting direction](/mold-parting-direction/), and the curve where the halves meet is found by [parting line generation](/parting-line-generation/).

## In plain words

A mold opens in two halves, one moving up and one moving down. Each spot on the part must be formed by one of the halves, and that half must be able to pull away from it in a straight line. A spot on the top of a part can be formed by the upper half. A spot under a lip, or inside a hole that goes through the part sideways, is a problem. Above it there is material, so the upper half cannot reach it, and below it there is also material, so the lower half cannot reach it either.

Such spots are undercuts. The task is to find all of them, so that the designer can change the part or add a moving piece to the mold.

## Definition

**Input.** A solid $P$ in $\mathbb{R}^3$, the closure of a bounded open set, given as a polyhedron with $n$ vertices or as a B-rep, and a parting direction $d \ne 0$.

**Undercut region.** For a point $x$ on the boundary $\partial P$, let $r^+(x) = \{x + t d : t > 0\}$ and $r^-(x) = \{x - t d : t > 0\}$ be the open rays from $x$ along $+d$ and $-d$. The point $x$ is *free* along $+d$ if $r^+(x)$ does not meet the interior $\operatorname{int} P$, and likewise along $-d$. The undercut region is

$$\mathrm{U}(d) = \{x \in \partial P : r^+(x) \cap \operatorname{int} P \ne \emptyset \text{ and } r^-(x) \cap \operatorname{int} P \ne \emptyset\}.$$

The definition treats $+d$ and $-d$ the same way, so $\mathrm{U}(d) = \mathrm{U}(-d)$. An *undercut feature* is a connected group of faces, or parts of faces, in $\mathrm{U}(d)$, which one side core can form.

**Output.** The region $\mathrm{U}(d)$, as parts of faces, or the list of faces that meet it, or only the answer to "is $\mathrm{U}(d)$ empty, up to a set of zero area?".

**Lemma (one side is always blocked).** Let $x$ be in the relative interior of a facet $f$ with outward normal $n_f$. If $n_f \cdot d > 0$, then $r^-(x)$ meets $\operatorname{int} P$. If $n_f \cdot d < 0$, then $r^+(x)$ meets $\operatorname{int} P$.

*Proof.* Near $x$, $P$ is the half-space $n_f \cdot (y - x) \le 0$, since $x$ is in the relative interior of $f$. For small $t > 0$, $n_f \cdot (-t d) = -t\, n_f \cdot d < 0$, so $x - t d$ is in the interior of that half-space near $x$, and so in $\operatorname{int} P$. The other case is the same with $+d$. $\square$

**Theorem.** For a point $x$ in the relative interior of an upper facet ($n_f \cdot d > 0$), $x \in \mathrm{U}(d)$ if and only if $x$ is not free along $+d$. For a lower facet, $x \in \mathrm{U}(d)$ if and only if $x$ is not free along $-d$. So $\mathrm{U}(d)$ meets the relative interior of no facet that is not parallel to $d$ if and only if every upper facet is visible along $d$ and every lower facet is visible along $-d$, which is the condition under which Ahn and coauthors prove that a two-piece mold with opposite directions and a free parting surface exists.

*Proof.* By the lemma, the ray on the other side is always blocked, so membership in $\mathrm{U}(d)$ depends only on the ray on the own side. The second sentence follows facet by facet. $\square$

So the definition with two opposite directions and the facet-by-facet condition of Ahn and coauthors give the same parts. The two-sided form does not need the face normals, so it also applies at edges, vertices and faces parallel to $d$.

## Variants

- **Faces parallel to $d$.** A face with $n \cdot d = 0$ is free if one of its rays leaves the part. In practice such faces also need a draft angle, which is a different test, [draft angle analysis](/draft-angle-analysis/).
- **External and internal undercuts.** An external undercut is on the outside of the part, such as a lip or a side hole, and is formed by a side core that moves out sideways. An internal undercut is inside, such as a snap hook on an inner wall, and needs a lifter or a collapsible core.
- **Undercut features.** Fu, Fuh and Nee group the undercut faces of a B-rep part into features, so that each feature can get one side core, and the mold design can count them.
- **All directions.** Over all directions, the problem is to find $d$ with $\mathrm{U}(d)$ empty, or with the fewest undercut features. Chen, Chou and Woo use visibility maps of the pockets on the sphere, and Ahn and coauthors compute all directions with an empty $\mathrm{U}(d)$.
- **Planar parting.** If the parting surface must be a plane, a part can fail even with $\mathrm{U}(d)$ empty. That is the model of Bose, Bremner and van Kreveld on the [mold parting direction](/mold-parting-direction/) page.

## Examples

**A spool.** Let $P$ be a base $[0,4]^2 \times [0,1]$, a post $[1,3]^2 \times [1,3]$ and a cap $[0,4]^2 \times [3,4]$, glued into one solid, like an I-beam turned on its end.

- With $d = (0, 0, 1)$: the underside of the cap, the ring $z = 3$ outside the post, has area $16 - 4 = 12$. It is a lower facet, and its ray along $-d$ meets the base. By the theorem it is an undercut. The top of the base, the ring $z = 1$ of area 12, is an upper facet whose ray along $+d$ meets the cap, so it is an undercut too. The four walls of the post are parallel to $d$, and both of their rays run into the cap and the base, so they are in $\mathrm{U}(d)$ as well, with area $4 \times 2 \times 2 = 16$. The total is 40. The top of the cap, the bottom of the base and the outer walls are free.
- With $d = (1, 0, 0)$: every point has a free ray. For example, the post face $x = 3$ is an upper facet, and its ray along $+x$ at a height between 1 and 3 passes between the base and the cap. A point of the ring $z = 1$ with $x < 1$ is free along $-x$, and one with $x > 3$ is free along $+x$. So $\mathrm{U}(d)$ is empty and the spool can be molded in two halves that part along $x$.

**A side hole.** The cube with a square hole along $x$ from the [mold parting direction](/mold-parting-direction/) page has the ceiling and the floor of the hole in $\mathrm{U}(z)$, and nothing in $\mathrm{U}(x)$.

**Non-example.** A face that is blocked along one direction only is not an undercut. The bottom face of the base of the spool, for $d = z$, is blocked along $+d$ by the material of the part, as the lemma says for every lower face, but it is free along $-d$, so the lower half forms it.

## Known algorithms

- **One direction, decision.** Ahn and coauthors test whether a direction gives a two-piece mold in $O(n \log n)$ time. By the theorem this decides whether $\mathrm{U}(d)$ meets the interior of a facet that is not parallel to $d$.
- **The exact region.** Project along $d$ onto a plane normal to $d$. The part of an upper facet $f$ that is not free along $+d$ is the part of $f$ under the projections of the facets that lie above it along $d$. This is the hidden part of $f$ seen from far away along $d$, the output of [hidden surface removal](/hidden-surface-removal/) in an orthographic view. Computing it for all facets gives $\mathrm{U}(d)$, by the theorem.
- **Rays and depth maps.** On meshes, systems cast rays along $\pm d$ from sample points with [ray casting](/ray-casting/), or render the part along $+d$ and $-d$ with a [z-buffer](/z-buffer/) or with [depth peeling](/depth-peeling/), and mark a point as an undercut when it lies behind the first surface in both views. This is fast on graphics hardware, but its answer has the resolution of the sampling.
- **Feature recognition.** Fu, Fuh and Nee find the faces that are not visible in the parting direction on a B-rep and group them into undercut features. This works on the faces of a CAD model and returns features that a designer can name, at the cost of rules for each kind of feature.
- **Choice of direction.** Chen, Chou and Woo compute visibility maps of pockets, which are [accessibility cones](/accessibility-cone/) of groups of faces, and choose the opposite pair of directions with the fewest undercut pockets.

## Bounds

- **Decision.** $O(n \log n)$ time for one direction, by Ahn and coauthors.
- **Output size.** The region $\mathrm{U}(d)$ can have $\Theta(n^2)$ pieces. Take $k$ bars along $x$, held by a frame at their ends at a height above $k$ bars along $y$, with a gap between the two layers and gaps between the bars. With $d = z$, the top face of each lower bar is undercut where an upper bar crosses over it and free in the gaps, so $\mathrm{U}(d)$ has $k^2$ separate pieces for $n = \Theta(k)$. Any method that outputs the region explicitly needs $\Omega(n^2)$ time on this part, and the $O(n^2)$ worst case of hidden surface removal is the matching upper bound for the size.
- **All directions.** $O(n^4)$ time, with a matching example of size $\Omega(n^4)$, by Ahn and coauthors, as on the [mold parting direction](/mold-parting-direction/) page.

## Reductions

- The facet-by-facet test reduces to visibility from a point at infinity along $d$, that is, to [hidden surface removal](/hidden-surface-removal/) for an orthographic view, once for $+d$ and once for $-d$.
- For a part whose upper surface is a [terrain](/terrain-visibility/) over the plane normal to $d$, every upper point is free along $+d$, so $\mathrm{U}(d)$ lies in the lower faces only.
- The choice of a direction with no undercut is the problem of [mold parting direction](/mold-parting-direction/), and a direction with no undercut is a direction in the intersection of the [accessibility cones](/accessibility-cone/) of the faces, with the sign chosen per face.

## Applications

In mold and die design, the undercut features decide the number of side cores and lifters, which set the cost and the cycle time of the mold. A [manufacturability analysis](/manufacturability-analysis/) reports them to the designer, who can often remove an undercut with a small change, such as a hole through the floor under a snap hook. Undercut detection is run together with [draft angle analysis](/draft-angle-analysis/), which checks the free faces for enough taper, and before [parting line generation](/parting-line-generation/).

## References
