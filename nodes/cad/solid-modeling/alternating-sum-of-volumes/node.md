---
tag: 7SFHP7
kind: algorithm
slug: alternating-sum-of-volumes
name: Alternating sum of volumes
aliases:
- ASV decomposition
- Woo-Kim convex decomposition
area: cad/solid-modeling
level: advanced
summary: Woo's and Kim's decomposition of a solid into convex hulls and their differences with alternating signs, from which form features are read off.
solves: [feature-recognition]
model: word-ram
complexity:
  vars: {n: the number of vertices of the polygon}
  time: {worst: "O(n^2 log n)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, recursive: true, exact: true}
history:
  year: 1982
  people: [Tony C. Woo]
  note: Woo proposed writing a solid as its convex hull minus the hull of the deficiency, plus the hull of the next deficiency, and so on, and reading features from the terms.
prereqs: [convex-hull, regularized-set-operations, feature-recognition]
see_also: [convex-decomposition, andrew-monotone-chain, convex-hull-3d, volume-decomposition-feature-recognition, hint-based-feature-recognition, feature-interaction, brep-to-csg-conversion, inclusion-exclusion-principle]
sources:
  - paper: "Tony C. Woo, Feature extraction by volume decomposition, Proceedings of the Conference on CAD/CAM Technology in Mechanical Engineering, MIT, Cambridge, Massachusetts, 1982"
    locator: the alternating sum of convex hulls and the reading of features from its terms (page numbers differ between citing sources and were not checked)
  - paper: doi:10.1016/0010-4485(91)90029-v
    title: Kai Tang and Tony C. Woo, Algorithmic aspects of alternating sum of volumes, part 1, data structure and difference operation, Computer-Aided Design 23(5), 357 to 366, 1991
    locator: the representation of the ASV terms and the difference operation between a hull and its region
  - paper: doi:10.1016/0010-4485(91)90011-k
    title: Kai Tang and Tony C. Woo, Algorithmic aspects of alternating sum of volumes, part 2, nonconvergence and its remedy, Computer-Aided Design 23(6), 435 to 443, 1991
    locator: why the series need not end in three dimensions, and a remedy
  - paper: doi:10.1115/1.2926574
    title: Yong Se Kim and D. J. Wilde, A convex decomposition using convex hulls and local cause of its non-convergence, Journal of Mechanical Design 114(3), 459 to 467, 1992
    locator: the convex decomposition by convex hulls and set differences, and the local cause of its non-convergence
  - paper: doi:10.1115/1.2926575
    title: Yong Se Kim and D. J. Wilde, A convergent convex decomposition of polyhedral objects, Journal of Mechanical Design 114(3), 468 to 476, 1992
    locator: ASVP, the alternating sum of volumes with partitioning, which cuts at concave edges where needed, and its proof of convergence
  - paper: doi:10.1016/0010-4485(92)90027-8
    title: Yong Se Kim, Recognition of form features using convex decomposition, Computer-Aided Design 24(9), 461 to 476, 1992
    locator: the conversion of the ASVP decomposition into a form feature decomposition by combining its terms
---

The alternating sum of volumes, or ASV, writes a solid as a signed sum of convex solids. Take the [convex hull](/convex-hull/) $H_0$ of the solid $Q$. What the hull adds is the *deficiency* $Q_1 = H_0 -^* Q$. Take its hull $H_1$, the deficiency of that, and so on. Then
$$Q = H_0 - (H_1 - (H_2 - \cdots)) = H_0 - H_1 + H_2 - \cdots$$
when the series ends, with the sum meant as a sum of indicator functions. Woo proposed it in 1982 for feature recognition. Each term is convex, the outer terms give the overall shape, and the inner terms are depressions and protrusions such as slots, pockets and bosses. A convex solid ends in one step. In three dimensions the series need not end: a hull and its deficiency can have the same hull, and then the terms repeat forever. Kim and Wilde found the local cause of this and fixed it with partitioning, the ASVP decomposition, in 1992. This page gives the method for simple polygons in the plane, where it always ends. It proves the expression, gives a 3D solid on which the plain series cycles, and shows how a cut fixes it.

## In plain words

Stretch a rubber band around a shape. The band encloses the shape plus some extra regions, the dents. Write the shape as "the band's area minus the dents".

Now each dent is a shape too, and it may have dents of its own. Stretch a band around each dent and repeat. Every band encloses a convex region, so the shape becomes plus a convex region, minus some, plus some more, and so on.

A plain rectangle needs only one band. An L shape needs two: the band around the L, minus a triangle. A stepped slot cut into a block needs three levels. In the plane this always stops. In 3D it can loop forever, unless you cut the solid into pieces first.

## The problem

The input is a simple polygon $Q$, given counterclockwise with integer or rational vertices and no three consecutive vertices collinear. The output is a tree. Each node stands for a polygon $R$ and holds its convex hull $\mathrm{CH}(R)$, and its children are the nodes of the pockets of $R$. The tree must satisfy
$$R = \mathrm{CH}(R) -^* \bigcup_{\text{children } R'} R'$$
at every node, so that $Q = \sum_{\text{nodes } v} (-1)^{\operatorname{depth}(v)} \mathrm{CH}(R_v)$ as indicator functions, off the boundaries.

## The algorithm

A vertex of $R$ *touches* the hull if it lies on the boundary of $\mathrm{CH}(R)$, at a hull corner or inside a hull edge. Line L2 finds these. Line L3 takes two touching vertices that come one after the other along $R$. If the boundary chain between them has two or more edges, the region between the chain and the segment joining its ends is a *pocket*, and the segment is its *lid*. The chain runs inside the hull, and the lid lies on its boundary. Line L5 reverses the chain to make the pocket counterclockwise, and line L6 recurses on it.

```pseudo id=main
ASV(R)
L1  H ← CONVEX-HULL(vertices of R)
L2  T ← the indices of the vertices of R that lie on the boundary of H, in order along R
    node ← (R, H, children ← empty)
    for each pair i, j of consecutive indices in T, cyclically, do
L3      chain ← R[i], R[i + 1], ..., R[j]
L4      if chain has only one edge then continue
L5      pocket ← chain reversed, closed by the lid from R[i] to R[j]
L6      append ASV(pocket) to the children of node
    return node

CONTAINS(node, p)
L7  return p is inside node.H and CONTAINS(c, p) is false for every child c
```

The hull is computed exactly with the [monotone chain](/andrew-monotone-chain/), removing collinear points. A vertex that lies inside a hull edge counts as touching, which matters for rectilinear parts. A slot cut into the top face of a block has its upper corners on the top edge of the hull, and they split the boundary into the pocket and the flat pieces around it.

## Example

Take the block $[0, 8] \times [0, 6]$ with a stepped slot in its top: a wide upper slot $[2, 6] \times [4, 6]$ over a narrow lower one $[3, 5] \times [2, 4]$. The vertices are
$$(0,0), (8,0), (8,6), (6,6), (6,4), (5,4), (5,2), (3,2), (3,4), (2,4), (2,6), (0,6).$$

| depth | hull | sign | area |
|---|---|---|---|
| 0 | the block, $(0,0), (8,0), (8,6), (0,6)$ | $+$ | 48 |
| 1 | the hull of the slot, $(2,4), (3,2), (5,2), (6,4), (6,6), (2,6)$ | $-$ | 14 |
| 2 | the triangle $(3,2), (3,4), (2,4)$ | $+$ | 1 |
| 2 | the triangle $(6,4), (5,4), (5,2)$ | $+$ | 1 |

At depth 0, the vertices $(6,6)$ and $(2,6)$ touch the top edge of the hull. The chain between them runs down through the slot, and it is the one pocket, the whole stepped slot. Its hull is a hexagon that cuts off the two inner corners of the step. Those corners are the two triangles at depth 2, which are convex and end the recursion. The series gives $48 - 14 + 1 + 1 = 36 = 48 - 12$, the area of the part.

This shows how the terms relate to features. The depth 1 term is the envelope of the whole slot. The depth 2 terms add back the two ledges of the step, the material between the narrow lower slot and the hull of the slot. A feature reader groups the terms back into machining features. Here that gives a wide slot and a narrow slot below it.

## Correctness

The proof file proves the planar claims, and the 3D example.

1. **Pockets tile the hull.** The touching vertices appear in the same cyclic order along $R$ and along the boundary of the hull, because two disjoint arcs of $R$ that joined interleaved boundary points would have to cross inside the hull. So the flat pieces of $R$ and the lids go once around the hull. Adding winding numbers, the hull's is the sum of $R$'s and the pockets', and each simple counterclockwise polygon has winding number 0 or 1. So every point inside the hull and on no boundary is in exactly one of $R$ and the pockets.
2. **The expression is exact.** By 1, $R = \mathrm{CH}(R) -^* \bigcup$ pockets at every node. Unfolding the recursion gives the signed sum of hulls, and line L7 decides membership exactly for points on no edge of the tree.
3. **It ends.** A pocket's lid is an edge of the pocket's own hull, so the pocket's own pockets lie along strictly shorter pieces of its chain. A pocket has at most $n - 1$ vertices when its parent has $n$, so the depth is at most $n - 2$.
4. **Convex inputs end in one step.** All vertices of a convex polygon touch its hull, so there are no pockets and the tree is a single node, $Q = H_0$. Conversely, a polygon with no pockets equals its hull by 1.
5. **Non-convergence in three dimensions, and the fix.** Let $H$ be the regular tetrahedron $A = (0,0,0)$, $B = (1,1,0)$, $C = (1,0,1)$, $D = (0,1,1)$, and $O$ its centre. Let $P = OABC \cup OACD$. Its deficiency is $OABD \cup OBCD$. Both contain all four corners of $H$, so both have hull $H$. The series is $H - H + H - \cdots$, and the deficiencies alternate between the two forever. Cutting $P$ by the plane $z = x$, which contains $O$, $A$ and $C$, gives the two convex tetrahedra $OABC$ and $OACD$, each of which ends in one step. That is the idea of partitioning in ASVP.

The tests check the planar claims with exact arithmetic against oracles that do not use the code. For 250 random rectilinear polygons with up to 22 cells and 4 levels, and 200 random star-shaped polygons with integer vertices, the tree's membership and the signed sum of hulls both agree with the polygon's membership at 25 or 20 rational points each. Those are points on no line through two vertices, over 10,000 in all. The signed sum of hull areas equals the polygon's area exactly, and every pocket has fewer vertices than its parent. All 300 random convex polygons give a single node. A 3D test samples 1,000 exact points in the tetrahedron and checks the cycle and the cut.

## Complexity

A node for a polygon with $s$ vertices costs $O(s \log s)$ for the hull. The touching vertices are the points left on the boundary when the monotone chain is run again keeping collinear points, which also costs $O(s \log s)$. The pockets of one node have disjoint chains, so all nodes at one depth have $O(n)$ vertices in total, and there are at most $n - 2$ depths. That gives $O(n^2 \log n)$ time and $O(n^2)$ space in the worst case. The bound on depth is loose, but deep nesting, as in a spiral, does need many levels. Typical parts have depth 2 to 4, and then the cost is $O(n \log n)$. The code uses a simpler touching test, $O(s h)$ per node for $h$ hull edges.

In 3D the hulls cost $O(s \log s)$ each with a [3D hull](/convex-hull-3d/) algorithm, but the difference operations between a hull and its region are full [Boolean operations](/regularized-set-operations/) on polyhedra, and with non-convergence the plain series has no bound at all.

## Properties

- **Exact.** All operations are hulls and orientation tests on the input coordinates, so integer or rational input gives an exact tree.
- **Unique.** The tree depends only on the polygon, not on a choice. This is the opposite of [volume decomposition](/volume-decomposition-feature-recognition/), where several covers can give the same part.
- **Outside in.** The terms are ordered from the outer envelope to the deepest detail. That matches how features nest, and it suits process planning from the stock inward.
- **Convex terms.** Every term is a convex polygon or polyhedron, the easiest kind of solid to machine, measure or test points against.

## Variants and improvements

- **One hull per deficiency, or one per piece.** The step can take a single hull of the whole deficiency, or one hull per connected piece of it. This page takes one per pocket, which gives a tree rather than a single series, and its proofs are for that form. With a single hull, separate dents are merged into one big convex term, which is worse for reading features.
- **ASVP.** Kim and Wilde showed that non-convergence has a local cause. Their remedy, remedial partitioning, cuts the solid at concave edges where the plain step would not make progress, and the pieces are decomposed in turn. They proved that this alternating sum of volumes with partitioning always ends.
- **Form feature decomposition.** Kim combined the terms of the ASVP into volumetric form features, and these can be converted further into a negative feature decomposition for machining. Later work used them for machining features and for ordering machining steps.
- **Data structures.** Tang and Woo gave the data structure and the difference operation for computing the series, and their second paper studied non-convergence and a remedy.
- **Orthogonal polyhedra.** For solids with all faces axis-parallel, other exact representations can be converted to an ASV directly.

## When to use it

Use ASV when a part should be described from the outside in, as a stock-like convex envelope with nested depressions and protrusions, and when a unique answer is wanted. It works best for polyhedral parts with moderate nesting. In 3D, use ASVP rather than the plain series, since non-convergence is a real case and not a rare corner. If the goal is a set of machining volumes accessible from given directions, [volume decomposition](/volume-decomposition-feature-recognition/) or [hint-based recognition](/hint-based-feature-recognition/) fit more directly. ASV terms are convex but not necessarily machinable shapes, and they need a further grouping step.

## Pitfalls

- **Vertices inside hull edges.** If only hull corners count as touching, a vertex in the middle of a hull edge is treated as inside the hull. The pocket then contains a flat piece of the boundary of $R$, and it can have zero area. Count every vertex on the hull boundary.
- **Floating-point hulls.** A hull built with rounding can drop a vertex that is just on the boundary, or keep one just inside, which changes the tree. Use exact arithmetic or snap carefully.
- **Assuming convergence in 3D.** The plain series can cycle, as the tetrahedron example shows. An implementation must detect a deficiency whose hull equals its parent's hull and switch to partitioning.
- **Terms are not features.** A single hull term can mix several features, as the slot hull above mixes the wide and narrow slots. Features come only after the terms are grouped.
- **Curved faces.** The hull of a solid with curved faces is hard to compute and represent exactly. That is why the early methods were limited to polyhedra, and later work added special handling for blends and cylinders.

## Implementations

## History

Woo presented the alternating sum of volumes at an MIT conference on CAD/CAM in 1982, as a way to extract features from a solid by convex hulls and differences. Tang and Woo studied its data structures and its non-convergence in two papers in 1991. Kim, in his Stanford thesis and in two papers with Wilde in 1992, located the local cause of non-convergence and introduced ASVP, which adds partitioning and always converges. In the same year Kim converted the ASVP into a form feature decomposition, and with coauthors went on to machining features, curved faces and incremental updates during the 1990s.

## References
