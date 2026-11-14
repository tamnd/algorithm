---
tag: V3W9FP
kind: definition
slug: no-fit-polygon
name: No-fit polygon
aliases:
- NFP
area: cad/cam-and-additive-manufacturing
level: core
summary: For two polygons, the locus of a reference point of one as it slides around the other while touching, so a placement overlaps exactly when that point is inside.
prereqs: [minkowski-sum]
see_also: [nesting-problem, bottom-left-fill, configuration-space, minkowski-sum-convex-polygons, convex-decomposition, polygon-with-holes, mathematical-morphology, orientation-test]
sources:
  - paper: doi:10.1016/j.ejor.2006.11.038
    title: Julia A. Bennell and José F. Oliveira, The geometry of nesting problems, a tutorial, European Journal of Operational Research 184(2), 2008, 397 to 415
    locator: the section on the no-fit polygon (definition, the orbital, decomposition and Minkowski sum ways to compute it, and its degenerate cases) and the inner-fit polygon
  - paper: "Julia A. Bennell, Kathryn A. Dowsland and William B. Dowsland, The irregular cutting-stock problem, a new procedure for deriving the no-fit polygon, Computers and Operations Research 28(3), 2001, 271 to 287"
    locator: the no-fit polygon of nonconvex polygons from Minkowski sums of edge sequences, without a decomposition into convex pieces
  - paper: doi:10.1016/j.ejor.2006.03.011
    title: Edmund K. Burke, Robert S. R. Hellier, Graham Kendall and Glenn Whitwell, Complete and robust no-fit polygon generation for the irregular stock cutting problem, European Journal of Operational Research 179(1), 2007
    locator: the orbital method, with the cases of holes, of exact fits and of sliding into a narrow channel
  - paper: doi:10.1016/S0377-2217(02)00131-5
    title: Kathryn A. Dowsland, Subodh Vaid and William B. Dowsland, An algorithm for polygon placement using a bottom-left strategy, European Journal of Operational Research 141(2), 2002, 371 to 381
    locator: feasible positions as points outside every no-fit polygon and inside the inner-fit polygon, holes included
  - paper: doi:10.1016/S0925-7721(01)00041-4
    title: Pankaj K. Agarwal, Eyal Flato and Dan Halperin, Polygon decomposition for efficient construction of Minkowski sums, Computational Geometry 21(1-2), 2002, 39 to 61
    locator: Minkowski sums of nonconvex polygons by convex decomposition, pairwise convex sums and their union, with an experimental comparison of decompositions
---

The no-fit polygon (NFP) of two polygons $A$ and $B$ tells, for each translation of $B$, whether $B$ overlaps $A$. Fix $A$ and a reference point on $B$. Slide $B$ around $A$ so that the two always touch and never overlap: the reference point traces the boundary of the NFP. Placements with the reference point inside the NFP overlap, those outside are apart, and those on the boundary touch. As a set, the NFP is the [Minkowski sum](/minkowski-sum/) $A \oplus (-B)$, the same object that motion planning calls the configuration space obstacle of a translating robot. Solvers of the nesting problem compute an NFP for each pair of part shapes and each allowed rotation. After that, the test of a whole placement against a fixed part is a [point in polygon](/point-in-polygon/) test, and rules such as [bottom-left fill](/bottom-left-fill/) search for points outside a union of NFPs. The NFP is the main geometric tool of the [nesting problem](/nesting-problem/). The text above, like the stub, says that a placement overlaps "exactly when the point is inside". This is true for the open interiors of most pairs, but it fails on the degenerate parts described below.

## Definition

Let $A$ and $B$ be polygons in the plane, each a compact set equal to the closure of its interior (it may have holes). Write $B + t = \{b + t : b \in B\}$ for $B$ translated by $t \in \mathbb{R}^2$, and $-B = \{-b : b \in B\}$. The reference point of $B$ is the origin of its coordinates, so the reference point of $B + t$ is $t$.

**No-fit polygon.** The no-fit polygon of $B$ with respect to $A$ is
$$ \mathrm{NFP}_{AB} = A \oplus (-B) = \{a - b : a \in A,\ b \in B\}. $$

**The three relations.** For every $t$:

1. $(B + t) \cap A \ne \emptyset$ if and only if $t \in \mathrm{NFP}_{AB}$. Indeed $a = b + t$ for some $a \in A$, $b \in B$ is the same as $t = a - b$.
2. The interiors meet, $\operatorname{int}(B + t) \cap \operatorname{int} A \ne \emptyset$, if and only if $t \in \operatorname{int} A \oplus (-\operatorname{int} B)$, by the same computation with the interiors. This set is open, since it is a union of translates of the open set $\operatorname{int} A$, and its closure is $\mathrm{NFP}_{AB}$.
3. $B + t$ touches $A$, meaning the sets meet but the interiors do not, if and only if $t$ is in $\mathrm{NFP}_{AB}$ but not in $\operatorname{int} A \oplus (-\operatorname{int} B)$.

A placement of $B$ is feasible with respect to $A$ when the interiors do not meet, that is, when $B$ is apart from $A$ or touches it. So the feasible translations are the complement of the open set in item 2.

**Is "inside" the same as "overlap"?** The open set of item 2 is always contained in $\operatorname{int} \mathrm{NFP}_{AB}$. For two convex polygons the two sets are equal, so "the interiors overlap if and only if $t$ is strictly inside the NFP" is true. For nonconvex polygons the open set can be smaller. The difference is a set of segments and points inside the NFP where $B$ fits exactly into a slot or a cavity of $A$: there $B$ touches $A$ on two opposite sides, every nearby translation overlaps, and so $t$ is an interior point of the NFP that is still feasible. Codes that test "strictly inside the NFP" lose these exact fits. Codes that test "inside or on the boundary" lose all touching placements. The orbital method of Burke et al. (2007) treats exact fits as a special case of its output.

**Inner-fit polygon.** For a container $C$, such as a sheet or a strip, the inner-fit polygon is
$$ \mathrm{IFP}_{CB} = \{t : B + t \subseteq C\}, $$
the Minkowski difference of $C$ and $B$, which is the erosion of [mathematical morphology](/mathematical-morphology/). For a rectangular sheet $[0, W] \times [0, L]$ and a part whose bounding box is $[0, w] \times [0, h]$ in its own coordinates, $\mathrm{IFP} = [0, W - w] \times [0, L - h]$, empty if the part is too large.

**Feasible region.** With parts $A_1, \dots, A_k$ already placed (each as a fixed polygon), the feasible reference points of $B$ form
$$ \mathrm{IFP}_{CB} \setminus \bigcup_{i=1}^{k} \left( \operatorname{int} A_i \oplus (-\operatorname{int} B) \right). $$
This is the set that placement rules search, for example for its lowest, then leftmost point in [bottom-left fill](/bottom-left-fill/).

**Rotations.** The NFP is defined for translations only. A part that may turn through a finite set of angles, often $0$, $90$, $180$ and $270$ degrees, gets one NFP per pair of orientations. Free rotation makes the set of placements three-dimensional, and the NFP does not apply directly.

**Convex parts.** If $A$ and $B$ are convex with $n$ and $m$ edges, the NFP is a convex polygon with at most $n + m$ edges. Its edges are the edges of $A$ and of $-B$ sorted by direction, so it is computed by one merge in $O(n + m)$ time, see [Minkowski sum of convex polygons](/minkowski-sum-convex-polygons/). For nonconvex parts the NFP can have holes, many more edges, and the degenerate parts above. The [Minkowski sum](/minkowski-sum/) page gives the size bounds. Three ways to compute it are in use, all described in the tutorial of Bennell and Oliveira (2008):

- **Orbital.** Slide $B$ along $A$ and trace the reference point. Each step finds the touching pair of edges, the direction of sliding, and how far $B$ can go before it hits another edge. The holes need extra start points. Burke et al. (2007) treat the holes, the exact fits and the narrow channels.
- **Decomposition.** Cut $A$ and $B$ into convex pieces (see [convex decomposition](/convex-decomposition/)), take the NFP of each pair of pieces by the convex merge, and take the union. Agarwal, Flato and Halperin (2002) compare decompositions for this use.
- **Edge sequences.** Bennell, Dowsland and Dowsland (2001) sort the edges of $A$ and $-B$ by direction as in the convex case, and repair the result where the polygons are not convex, without a decomposition.

All three make sign decisions on the [orientation](/orientation-test/) of edge pairs, so rounding errors can break them. Exact rational coordinates avoid this.

## Examples and non-examples

The examples were checked by an exact rational test of the three relations on a grid of translations (spacing $1/3$ and $1/4$), with the overlap of convex pieces decided by separating axes.

- **A square and a triangle.** $A = [0, 4]^2$, and $B$ is the triangle with vertices $(0, 0)$, $(2, 0)$ and $(0, 2)$, with the reference point at its right angle. Then $-B$ has vertices $(0, 0)$, $(-2, 0)$ and $(0, -2)$, and
$$ \mathrm{NFP}_{AB} = \text{the pentagon } (-2, 0), (0, -2), (4, -2), (4, 4), (-2, 4), $$
of area $34$. It has $5$ edges, not $4 + 3 = 7$, because the two short edges of $-B$ are parallel to edges of the square and merge with them. At $t = (-1, -1)$, on the slanted edge, the hypotenuse of $B + t$ touches the corner $(0, 0)$ of $A$. At $t = (3, 3)$, inside, the parts overlap. At $t = (5, 0)$, outside, they are apart.
- **A hole in the NFP.** Let $A$ be the square $[0, 6]^2$ with a square cavity $(1, 5)^2$ cut out of it and a slot of width $1$, $(3, 4) \times (5, 6]$, that joins the cavity to the top. Let $B$ be a $2 \times 2$ square with the reference point at its lower left corner. Then $\mathrm{NFP}_{AB} = [-2, 6]^2$ with the open square $(1, 3)^2$ removed. The hole is the set of positions where $B$ sits inside the cavity without touching it. $B$ is too wide to pass through the slot, so the hole cannot be reached from outside by sliding, and an orbital method that starts from the outside never finds it. The hole is where solvers of the nesting problem put small parts inside the cut-outs of large ones.
- **An exact fit.** Make the cavity of the previous example $(1, 3) \times (1, 5)$, which is exactly as wide as $B$, and close the slot. The positions $t = (1, y)$ for $1 \le y \le 3$ put $B$ in the cavity, touching both side walls. They are feasible. But moving $t$ by $\pm 1/100$ in $x$ makes $B$ overlap a wall, so the segment lies in the interior of the NFP. The NFP has no hole here, only a slit of feasible points inside it. This is the non-example to "overlap if and only if strictly inside".
- **Inner fit.** A $2 \times 1$ rectangle on a sheet $[0, 10] \times [0, 4]$ has $\mathrm{IFP} = [0, 8] \times [0, 3]$. The point $(8, 3)$ puts the rectangle in the upper right corner.
- **Not symmetric.** $\mathrm{NFP}_{BA} = B \oplus (-A) = -\mathrm{NFP}_{AB}$. In the first example, $\mathrm{NFP}_{BA}$ is the pentagon reflected through the origin, not the same pentagon. The reference points also matter: moving the reference point of $B$ by $v$ translates $\mathrm{NFP}_{AB}$ by $-v$.

## Related definitions

- **[Minkowski sum](/minkowski-sum/).** The NFP is $A \oplus (-B)$. The Minkowski sum page gives the algorithms and the size bounds, and this page adds the reference point, the touching case and the inner-fit polygon.
- **[Configuration space](/configuration-space/).** In motion planning, the obstacle $A$ for a robot $B$ that only translates is the same set $A \oplus (-B)$. Motion planning asks for a path through the free space. The nesting problem asks for a good point in it.
- **[Mathematical morphology](/mathematical-morphology/).** The inner-fit polygon is an erosion of the container by $B$, and the NFP is a dilation of $A$ by $-B$.
- **[Nesting problem](/nesting-problem/).** The problem that the NFP serves. Its feasibility constraints are "the reference point of each part is in its IFP and outside the open NFP of every other part".
- **[Bottom-left fill](/bottom-left-fill/).** Places each part at the lowest, then leftmost, feasible point of the region above.
- **[Polygon with holes](/polygon-with-holes/).** NFPs of nonconvex parts can have holes, so a code needs this representation for its output.

## References
