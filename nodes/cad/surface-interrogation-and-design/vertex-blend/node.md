---
tag: HP9HSV
kind: technique
slug: vertex-blend
name: Vertex blend
aliases:
- corner blend
- setback vertex blend
area: cad/surface-interrogation-and-design
level: advanced
summary: Fills the corner where three or more edge blends meet with an n-sided patch, often after setting the blends back, so the result is tangent continuous.
prereqs: [blending-surface, rolling-ball-blend, n-sided-patch]
see_also: [n-sided-patch, gregory-patch, generalized-bezier-patch, rolling-ball-blend, blending-surface, tangent-plane-continuity, twist-compatibility, boundary-representation]
sources:
  - paper: "Tamás Várady and Alyn P. Rockwood, Geometric construction for setback vertex blending, Computer-Aided Design 29(6), 413 to 425, 1997"
    title: Várady and Rockwood 1997
    locator: setback vertex blends, represented by 2n-sided patches with odd special cases, built from polynomial patches by the setback split
  - paper: "Pei Zhou and Wen-Han Qian, Polyhedral vertex blending with setbacks using rational S-patches, Computer Aided Geometric Design 27(3), 233 to 244, 2010"
    title: Zhou and Qian 2010
    locator: a setback vertex blend as a single rational S-patch, and the twist compatibility problems of blends stitched from tensor product patches
  - paper: doi:10.1016/j.cag.2020.05.009
    title: "Ágoston Sipos, Tamás Várady, Péter Salvi and Márton Vaitkus, Multi-sided implicit surfacing with I-patches, Computers and Graphics 90, 29 to 42, 2020"
    locator: implicit multi-sided patches for setback vertex blends with conic boundaries (general locator)
  - paper: doi:10.1016/j.cagd.2024.102286
    title: "Tamás Várady, Péter Salvi and Márton Vaitkus, Genuine multi-sided parametric surface patches, a survey, Computer Aided Geometric Design 110, 102286, 2024"
    locator: single patch representations for multi-sided regions such as vertex blends (general locator)
---

A vertex blend is the surface that rounds a corner of a solid where three or more rounded edges meet. Each edge is rounded by an edge blend, for example by a [rolling ball blend](/rolling-ball-blend/), and near the shared vertex the edge blends overlap or leave a gap. The vertex blend removes the overlap and fills the gap with one more patch that meets the edge blends, and sometimes the original faces, with [tangent plane continuity](/tangent-plane-continuity/). In the simplest case, three equal radius blends at the corner of a box, the vertex blend is a part of a sphere. In general the hole has $n$ sides, and the vertex blend is an instance of the [n-sided patch](/n-sided-patch/) problem. The *setback* variant of Várady and Rockwood cuts the edge blends back from the vertex first. This gives the hole up to $2 n$ sides for $n$ edges and more room for a good shape.

## In plain words

Round the three edges at the corner of a box, and the three rounded strips run into each other at the corner. Something must cover the place where they meet. If all three strips have the same size, a piece of a ball fits exactly. If the sizes differ, or the edges meet at odd angles, no simple shape fits, and a special patch with several sides must close the corner smoothly. A useful trick is to stop each rounded strip a little before the corner, so the gap is larger. The larger gap has twice as many sides: one where each strip ends and one on each flat face between two strips. The patch then has more room to bend gently, and the corner looks soft instead of pinched.

## When it applies

Use a vertex blend in a [boundary representation](/boundary-representation/) modeler whenever three or more blended edges meet at a vertex, or a blended edge ends at a vertex where other edges are not blended. Its inputs are the primary faces at the vertex, the edge blends with their contact curves on the faces (the *springlines*) and their cross sections, and setback distances when the setback form is used. It assumes that the edge blends are themselves tangent continuous to the faces, and that the blends are long enough to cut back by the chosen setbacks.

## The template

```pseudo id=main
VERTEX-BLEND(vertex v, faces, edge blends E_1, …, E_n around v, setbacks σ_1, …, σ_n)
L1  for each edge blend E_i, find its springlines on its two faces and its cross section curves
L2  trim E_i at distance σ_i from v; its end cross section becomes a side of the hole      ▷ σ_i = 0: no setback
L3  for each face between E_i and E_{i+1}, join the trimmed ends of their springlines by a curve on the face; it becomes a side of the hole
L4  for each side, take the ribbon: the tangent plane of E_i along a cross section, the face plane along a face curve
L5  at each corner of the hole, check that the two sides are not tangent and that the two ribbons give one tangent plane
L6  fill the hole of at most 2n sides with an n-sided patch that meets every ribbon with G1
L7  trim the faces along the face curves and return the faces, the trimmed blends and the vertex patch
```

With zero setbacks the face curves of line L3 shrink to points, and the hole is bounded by the $n$ end cross sections only. Line L6 is the [n-sided patch](/n-sided-patch/) problem, solved by any of its methods: a split into [Gregory patches](/gregory-patch/) or polynomial patches (the setback split of Várady and Rockwood uses polynomial patches), a single [Generalized Bézier patch](/generalized-bezier-patch/), a rational S-patch, or an implicit patch.

**Theorem 1 (the corners of the hole are consistent).** Suppose each edge blend is tangent to its faces along its springlines. At a corner of the hole where the end cross section of $E_i$ meets the face curve on a face $F$, the ribbon of $E_i$ and the ribbon of $F$ give the same tangent plane, the plane of $F$. If, in addition, the face curve does not leave the corner in the direction of the cross section, the corner meets the corner conditions of the n-sided patch problem.

*Proof.* The corner is the end of a springline of $E_i$ on $F$, a point where $E_i$ touches $F$, so the tangent plane of $E_i$ there is the tangent plane of $F$. The cross section lies on $E_i$ and the face curve lies on $F$, so both tangents at the corner lie in this plane. By the theorem on the [n-sided patch](/n-sided-patch/) page, a solution needs these two tangents to be independent and the two ribbons to lie in the plane they span. Both hold when the face curve does not leave in the direction of the cross section. $\square$

**Theorem 2 (the spherical corner).** Let the vertex be the corner of the octant $x, y, z \ge 0$, with its three edges along the axes, and round each edge with a rolling ball blend of the same radius $r$. Cut each blend at distance $r$ from the vertex. Then the part of the sphere of radius $r$ about $(r, r, r)$ that lies in the cube $[0, r]^3$ fills the hole with tangent plane continuity.

*Proof.* The blend of the $x$ axis is the cylinder of radius $r$ about the line $y = z = r$, the part with $y \le r$ and $z \le r$. It ends at the plane $x = r$ in the quarter circle $(r, r - r \cos t, r - r \sin t)$, $0 \le t \le \pi / 2$. Each point of it is at distance $r$ from $(r, r, r)$, so the circle lies on the sphere. At such a point the unit normal of the cylinder is the vector from the nearest point of the axis, which is $(r, r, r)$ itself, so it equals the unit normal of the sphere, $(p - (r, r, r))/r$. So the sphere and the cylinder share the tangent plane along the whole quarter circle. The other two blends are the same up to a permutation of the coordinates. The quarter circles meet at the points $(r, 0, r)$, $(0, r, r)$ and $(r, r, 0)$, where the sphere touches the three faces, so the three circles close the hole and the sphere part inside $[0, r]^3$ is its fill. $\square$

**Theorem 3 (unequal radii).** In the setting of Theorem 2, let the blends of the $x$, $y$ and $z$ axes have radii $r_1$, $r_2$ and $r_3$, without setback. The springlines on the face $y = 0$ are $z = r_1$ and $x = r_3$, and they cross at $(r_3, 0, r_1)$. A sphere that touches the three faces exactly at the three crossings of springlines exists only when $r_1 = r_2 = r_3$.

*Proof.* The blend of the $x$ axis touches $y = 0$ along $z = r_1$, and that of the $z$ axis touches it along $x = r_3$, which gives the crossing. A sphere tangent to the three planes $x = 0$, $y = 0$, $z = 0$, inside the octant, has centre $(\rho, \rho, \rho)$ and radius $\rho$, and touches $y = 0$ at $(\rho, 0, \rho)$. This is $(r_3, 0, r_1)$ only if $r_3 = r_1 = \rho$. The face $z = 0$, with crossing $(r_2, r_1, 0)$, gives $r_2 = r_1$ in the same way. $\square$

So unequal radii, which are common, already need a general $n$-sided patch, and Theorem 1 says what its corner data must satisfy.

**Worked example.** Take the corner of Theorem 2 with $r = 1$ and the setback $\sigma = 2$ on each edge. The blend of the $x$ axis is cut at $x = 2$, and its end cross section runs from $(2, 0, 1)$ to $(2, 1, 0)$. The blends of the $y$ and $z$ axes give the sections from $(1, 2, 0)$ to $(0, 2, 1)$ and from $(0, 1, 2)$ to $(1, 0, 2)$. On each face, a curve joins the ends of the two springlines: on $y = 0$ from $(1, 0, 2)$ to $(2, 0, 1)$, on $z = 0$ from $(2, 1, 0)$ to $(1, 2, 0)$, and on $x = 0$ from $(0, 2, 1)$ to $(0, 1, 2)$. The hole has six sides and the six corners

$$(2, 0, 1),\ (2, 1, 0),\ (1, 2, 0),\ (0, 2, 1),\ (0, 1, 2),\ (1, 0, 2),$$

which all lie in the plane $x + y + z = 3$. Take the face curves to be straight segments. At the corner $(2, 0, 1)$ the cross section $(2, 1 - \cos t, 1 - \sin t)$ leaves with the tangent $(0, 0, -1)$, and the segment arrives with the direction $(1, 0, -1)$. Their cross product is $(0, -1, 0)$, the normal of the face $y = 0$, as Theorem 1 says. At $(2, 1, 0)$ the section arrives with the tangent $(0, 1, 0)$ and the segment on $z = 0$ leaves with $(-1, 1, 0)$, with cross product $(0, 0, 1)$. Across each end section the ribbon is the direction of the blend axis toward the vertex, $(-1, 0, 0)$ for the blend of the $x$ axis, and across each segment it is the plane of the face. A six sided patch with these ribbons is the vertex blend. A sphere does not fit: the patch must be tangent to the face $y = 0$ along the whole segment from $(1, 0, 2)$ to $(2, 0, 1)$, and a sphere touches a plane in one point only.

## Classic examples

- **The ball corner.** Equal radius blends at a corner of three planes that meet at right angles, filled by a part of a sphere, as in Theorem 2.
- **Setback vertex blends.** Várady and Rockwood represent the vertex blend of $n$ edges by a $2 n$ sided patch, with odd numbers of sides in special cases, built from standard polynomial patches by the setback split. The setbacks are free parameters for the shape.
- **A single S-patch.** Zhou and Qian fill polyhedral setback vertex blends with one rational S-patch, to avoid the twist compatibility problems of blends stitched from tensor product patches.
- **Implicit vertex blends.** I-patches of Sipos, Várady, Salvi and Vaitkus give setback vertex blends as multi-sided implicit surfaces.

## Variations

- **Zero setback.** The hole has one side per edge blend, and the patch must meet the blends exactly where they cross. This is the simplest form, but the patch has little room, and its shape depends entirely on how the blends cross.
- **Setback.** Each blend is cut back, and the hole has sides on the blends and on the faces. Larger setbacks give gentler corners and change more of the faces.
- **Mixed convexity.** Some edges at the vertex are convex and some concave. Rounds and fillets then meet at the vertex, and the face curves and setbacks must be chosen for each kind of edge.
- **Curvature continuous corners.** The ribbons carry curvature, and the patch meets the blends with $G^2$ continuity, for high quality surfaces.
- **Choice of patch.** A split into four sided patches is easy to export to other systems, while a single multi-sided patch has no inner joins.

## Pitfalls

- **Tangent sides at a corner.** If a face curve leaves its corner along the cross section of the blend, the corner condition of Theorem 1 fails and no regular patch over a polygon domain fills the hole.
- **Twist compatibility.** A fill made of polynomial patches must meet [twist compatibility](/twist-compatibility/) at every corner. Rational patches such as Gregory patches or S-patches avoid this condition.
- **Setbacks too small or too large.** Too small, and the blends still overlap or meet at sharp angles. Too large, and the face curves leave their faces, or the blends are cut back beyond their own ends.
- **Faces that change.** The setback form trims the primary faces, so the faces of the solid change near the vertex, and the topology of the model changes.
- **Shape quality.** Many patches meet all the conditions, and their shapes differ. Fairness measures used to choose one are design criteria, not proofs of quality, and designers still check the result with reflection lines.
- **Unequal radii.** Theorem 3 shows that a sphere is the exception, so code that assumes the ball corner fails on common input.

## Exercises

1. In Theorem 2, show that the sphere part inside $[0, r]^3$ is tangent to the face $y = 0$ only at $(r, 0, r)$, so the vertex blend has three sides and touches the faces at three points.
2. In the worked example, find the corners of the hole for a general setback $\sigma > 1$, and show that they lie in the plane $x + y + z = \sigma + 1$.
3. For radii $r_1 = r_2 = 1$ and $r_3 = 2$, list the crossings of springlines on the three faces and explain why the hole cannot be closed by the three end cross sections alone.
4. Show that at a convex vertex where four faces meet, the setback form gives a hole with eight sides, and write the corner condition of Theorem 1 at each of its corners.

## References
