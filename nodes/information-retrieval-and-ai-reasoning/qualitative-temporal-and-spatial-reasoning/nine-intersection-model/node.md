---
tag: VRVN0C
kind: model
slug: nine-intersection-model
name: Nine-intersection model
aliases:
- Egenhofer 9-intersection
- 9-IM
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: core
summary: Classifies the topological relation of two spatial objects by which of the nine intersections of their interiors, boundaries and exteriors are empty. For simple regions, 8 of 512 matrices occur.
prereqs: [simple-polygon, jordan-curve-theorem]
see_also: [region-connection-calculus-rcc8, rcc5, point-in-polygon, spatial-join, polygon, composition-table]
sources:
  - paper: doi:10.1080/02693799108927841
    title: Max J. Egenhofer and Robert D. Franzosa, Point-set topological spatial relations, International Journal of Geographical Information Systems 5(2), 1991
    locator: pages 161 to 174 (the 4-intersection of boundaries and interiors, its 16 combinations, and the 8 that occur between regions)
  - paper: doi:10.1007/3-540-54414-3_36
    title: Max J. Egenhofer, Reasoning about binary topological relations, SSD'91, Lecture Notes in Computer Science 525, Springer, 1991
    locator: pages 141 to 160 in Springer's listing (the 9-intersection with exteriors, and composition of topological relations)
  - paper: "Max J. Egenhofer, David M. Mark and John Herring, The 9-intersection, formalism and its use for natural-language spatial predicates, NCGIA Technical Report 94-1, 1994"
    locator: the 9-intersection for lines and regions, and the 19 relations between an unbranched line and a region
  - paper: "David A. Randell, Zhan Cui and Anthony G. Cohn, A spatial logic based on regions and connection, Proceedings of KR'92, Morgan Kaufmann, 1992"
    locator: pages 165 to 176 (the RCC8 base relations, which match the eight region relations)
---

The nine-intersection model of Egenhofer describes how two spatial objects $A$ and $B$ lie with respect to each other by a $3 \times 3$ matrix of bits: for each part of $A$ (interior, boundary, exterior) and each part of $B$, whether the two parts meet. There are $2^9 = 512$ matrices, but between two simple regions in the plane only 8 occur, and these are the eight base relations of [RCC8](/region-connection-calculus-rcc8/). The model is the basis of the topological predicates of spatial databases and geographic information systems, such as "touches", "within" and "overlaps".

## The machine

Let $A$ and $B$ be closed subsets of $\mathbb{R}^2$. Write $A^\circ$ for the interior, $\partial A$ for the boundary and $A^-$ for the exterior, the complement of $A$. The nine-intersection matrix is

$$M(A, B) = \begin{pmatrix} A^\circ \cap B^\circ & A^\circ \cap \partial B & A^\circ \cap B^- \\ \partial A \cap B^\circ & \partial A \cap \partial B & \partial A \cap B^- \\ A^- \cap B^\circ & A^- \cap \partial B & A^- \cap B^- \end{pmatrix},$$

with each entry replaced by 1 if the set is non-empty and 0 if it is empty. The relation of $A$ and $B$ is the matrix. The matrix is invariant under homeomorphisms of the plane, since they map interiors, boundaries and exteriors to the same parts of the images. The converse relation has the transposed matrix.

A *simple region* is a closed set homeomorphic to a closed disc: it is connected, has no holes, and its boundary is a [simple closed curve](/jordan-curve-theorem/). For two simple regions, the eight matrices that occur are these, with the rows $A^\circ, \partial A, A^-$ and the columns $B^\circ, \partial B, B^-$:

| relation (RCC8) | Egenhofer name | row $A^\circ$ | row $\partial A$ | row $A^-$ |
| --- | --- | --- | --- | --- |
| DC | disjoint | 0 0 1 | 0 0 1 | 1 1 1 |
| EC | meet | 0 0 1 | 0 1 1 | 1 1 1 |
| PO | overlap | 1 1 1 | 1 1 1 | 1 1 1 |
| EQ | equal | 1 0 0 | 0 1 0 | 0 0 1 |
| TPP | coveredBy | 1 0 0 | 1 1 0 | 1 1 1 |
| NTPP | inside | 1 0 0 | 1 0 0 | 1 1 1 |
| TPPi | covers | 1 1 1 | 0 1 1 | 0 0 1 |
| NTPPi | contains | 1 1 1 | 0 0 1 | 0 0 1 |

The other 504 matrices cannot occur, for reasons such as these: $A^- \cap B^-$ is never empty for bounded sets, and if $A^\circ$ meets both $B^\circ$ and $B^-$, then it meets $\partial B$, since $A^\circ$ is connected.

**The 4-intersection.** Egenhofer and Franzosa (1991) used only the four entries for interiors and boundaries, which give $2^4 = 16$ matrices. Between simple regions, 8 of them occur, and they separate the same eight relations. The exterior row and column are needed for objects of other kinds, such as lines and points.

## What it counts

The model is a classification, not a reasoning system. One question is to compute the matrix for two given geometries. For two simple polygons with $n$ and $m$ edges, the matrix follows from the intersections of their boundaries and from a few [point-in-polygon](/point-in-polygon/) tests: a [plane sweep](/bentley-ottmann-algorithm/) finds the $k$ boundary intersections in $O((n + m) \log(n + m) + k)$ time, and if the boundaries do not cross, one point of each polygon tested against the other decides the containment. A [spatial join](/spatial-join/) evaluates such a predicate for many pairs, first filtering by bounding boxes.

The other question is reasoning over relations, as in a [qualitative constraint network](/qualitative-constraint-network/): given the relation of $A$ and $B$ and of $B$ and $C$, which relations are possible between $A$ and $C$? Egenhofer (1991) derived this [composition table](/composition-table/) from the matrices; for simple regions it is the RCC8 table.

## Relation to other models

- **RCC8.** For simple regions, the eight matrices are exactly the RCC8 base relations, as in the table. RCC8 is axiomatic, with one primitive, connection, while the nine-intersection model is defined by point-set topology; they agree on these objects. See [RCC8](/region-connection-calculus-rcc8/) and [RCC5](/rcc5/).
- **Lines and points.** For an unbranched line and a simple region in the plane the 9-intersection gives 19 relations, and for two unbranched lines 33, where the 4-intersection gives fewer (Egenhofer, Mark and Herring 1994).
- **Dimension.** The dimensionally extended nine-intersection (DE-9IM) of Clementini and others records the dimension of each intersection (empty, 0, 1 or 2) in place of one bit. It is the basis of the relate predicate in the OGC Simple Features standard, where patterns such as "T*F**F***" select a set of matrices.
- **Regions with holes.** For regions with holes, or with several pieces, more matrices occur and a single matrix no longer fixes the relation up to homeomorphism; extended models split the boundary into parts.

## Known results in the model

| object types in the plane | realizable relations | source |
| --- | --- | --- |
| simple region, simple region, 4-intersection | 8 of 16 | Egenhofer and Franzosa 1991 |
| simple region, simple region, 9-intersection | 8 of 512 | Egenhofer 1991 |
| unbranched line, simple region | 19 | Egenhofer, Mark and Herring 1994 |
| unbranched line, unbranched line | 33 | Egenhofer, Mark and Herring 1994 |

**Composition.** The composition of two region relations, computed from the matrices, is a set of matrices, and reasoning with these sets is reasoning in RCC8. So consistency of a network of such relations between regions is the RCC8 consistency problem, NP-complete in general and polynomial for the classes of the [Renz-Nebel theorem](/rcc8-tractable-subclasses/); if the regions must be simple, connectedness and the absence of holes can add constraints that RCC8 alone does not express.

## References
