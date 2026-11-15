---
tag: SKAWD9
kind: model
slug: cardinal-direction-calculus
name: Cardinal direction calculus
aliases:
- cardinal direction relations
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: advanced
summary: Qualitative relations such as north and southwest between points or regions, defined by projections on the axes or by the 3x3 grid around the bounding box of the reference object.
prereqs: [point-algebra, qualitative-constraint-calculus]
see_also: [rectangle-algebra, minimum-bounding-rectangle, region-connection-calculus-rcc8, qualitative-constraint-network, composition-table, algebraic-closure, double-cross-calculus]
sources:
  - paper: doi:10.1007/978-3-642-46752-3_17
    title: Andrew U. Frank, Qualitative spatial reasoning with cardinal directions, 7th Austrian Conference on Artificial Intelligence, Informatik-Fachberichte 287, Springer, 1991
    locator: pages 157 to 167 (cone-based and projection-based cardinal directions between points, and their composition)
  - paper: doi:10.1006/jvlc.1997.9999
    title: Gérard Ligozat, Reasoning about cardinal directions, Journal of Visual Languages and Computing 9(1), 1998
    locator: pages 23 to 44 (the nine base relations between points, the 512 relations, and the preconvex relations as a maximal tractable subset)
  - paper: doi:10.1016/S0004-3702(03)00137-1
    title: Spiros Skiadopoulos and Manolis Koubarakis, Composing cardinal direction relations, Artificial Intelligence 152(2), 2004
    locator: pages 143 to 171 (the relations between extended regions, the 218 basic relations for connected regions, and their composition)
  - paper: "Spiros Skiadopoulos and Manolis Koubarakis, On the consistency of cardinal direction constraints, Artificial Intelligence 163(1), 2005"
    locator: pages 91 to 135 (an O(n^5) consistency check for basic constraints, and NP-completeness for disjunctive ones)
  - paper: "Roop K. Goyal and Max J. Egenhofer, Similarity of cardinal directions, SSTD 2001, Lecture Notes in Computer Science 2121, Springer, 2001"
    locator: the direction-relation matrix of a target region with respect to the bounding box of a reference region
---

The cardinal direction calculus describes where one object lies with respect to another in terms of the compass: north, northeast, east and so on. For points it is the product of two copies of the [point algebra](/point-algebra/), one per axis, with nine base relations (Frank 1991, Ligozat 1998). For extended regions, the plane is cut into nine tiles by the bounding box of the reference region, and the relation is the set of tiles that the other region occupies (Goyal and Egenhofer, Skiadopoulos and Koubarakis). It is used in geographic information systems and in spatial queries such as "find the lakes north of the city".

## The machine

**Points.** Let $a = (x_a, y_a)$ and $b = (x_b, y_b)$ be points of $\mathbb{R}^2$. The base relation of $a$ to $b$ is the pair of point relations $(x_a \mathrel{?} x_b, \; y_a \mathrel{?} y_b)$ with each $? \in \{<, =, >\}$, so there are $3 \times 3 = 9$ base relations:

| | $x_a < x_b$ | $x_a = x_b$ | $x_a > x_b$ |
| --- | --- | --- | --- |
| $y_a > y_b$ | NW | N | NE |
| $y_a = y_b$ | W | Eq | E |
| $y_a < y_b$ | SW | S | SE |

These are the projection-based directions of Frank (1991). The nine relations are jointly exhaustive and pairwise disjoint, and a relation is a set of them, so there are $2^9 = 512$ relations. The converse swaps N and S, E and W, and so on. Composition of base relations works axis by axis: if $a \mathrel{(r_1, r_2)} b$ and $b \mathrel{(s_1, s_2)} c$, then $a$ and $c$ satisfy $(r_1 \diamond s_1) \times (r_2 \diamond s_2)$, with $\diamond$ the point algebra [composition](/composition-table/). For example, N composed with E is NE, and NE composed with SW is the set of all nine relations.

Frank also gave a cone-based version, in which the plane around $b$ is cut into four or eight cones of equal angle. It is closer to how people use the words, but it is not a product of axis relations.

**Regions.** Let $b$ be a bounded region with [bounding box](/minimum-bounding-rectangle/) $[x_1, x_2] \times [y_1, y_2]$. The four lines $x = x_1$, $x = x_2$, $y = y_1$ and $y = y_2$ cut the plane into nine tiles, named B (the box itself), N, NE, E, SE, S, SW, W and NW. The relation of a region $a$ to $b$ is the set of tiles in which $a$ has a part of positive area, written for example $N{:}NE$ when $a$ lies above the box and reaches past its right side. Goyal and Egenhofer write this set as a $3 \times 3$ matrix of bits, the direction-relation matrix.

Any non-empty set of tiles can be the relation of a region that may have several pieces, so there are $2^9 - 1 = 511$ basic relations. For connected regions without holes, the set of tiles must be connected through shared tile edges, and Skiadopoulos and Koubarakis (2004) count 218 basic relations. A direct count agrees: of the 511 non-empty subsets of the $3 \times 3$ grid, exactly 218 are connected through shared edges.

## What it counts

An input is a [qualitative constraint network](/qualitative-constraint-network/) on $n$ objects with direction relations as labels. The questions are consistency, a solution, and the minimal labels. Cost is counted in $n$.

**Points.** A network of base relations is consistent if and only if each of its two axis networks is consistent, since the axes are independent. Each axis network is a network of the point algebra, so the check takes $O(n^2)$ time for a complete network, for example by merging the points that must be equal and testing the order for a cycle.

**Example.** The points $a \mathrel{NE} b$, $b \mathrel{NE} c$, $c \mathrel{NE} a$ are inconsistent, since the $x$ axis needs $x_a > x_b > x_c > x_a$. The network $a \mathrel{N} b$, $b \mathrel{E} c$, $a \mathrel{NE} c$ is consistent: $a = (1, 1)$, $b = (1, 0)$, $c = (0, 0)$.

**Regions.** Computing the relation of two polygons takes time linear in their sizes: one pass over $b$ finds its bounding box, and clipping $a$ against the four lines finds the tiles with positive area. The relations between regions are not closed under converse: from $a \mathrel{N} b$ the relation of $b$ to $a$ can be S, S:SW, S:SE and others, depending on the widths, so the converse of a basic relation is in general a disjunction.

## Relation to other models

- **Point algebra.** Each axis of the point calculus is the [point algebra](/point-algebra/), and the point calculus is their product.
- **Rectangle algebra.** The [rectangle algebra](/rectangle-algebra/) applies the same product idea to intervals, with Allen's 13 relations on each axis. The region relation of $a$ to $b$ depends only on $a$ and the bounding box of $b$, so it is coarser than the rectangle relation of the two boxes in some cases and finer in others.
- **Topology.** [RCC8](/region-connection-calculus-rcc8/) says whether regions touch or overlap and has no notion of direction; combinations of RCC8 and cardinal directions have been studied for this reason.
- **Relative orientation.** Cardinal directions use a fixed frame. The [double-cross calculus](/double-cross-calculus/) and other relative calculi describe a point with respect to the direction defined by two other points.

## Known results in the model

| problem | result | source |
| --- | --- | --- |
| points, base relations | polynomial, axis by axis | Ligozat 1998 |
| points, preconvex relations | algebraic closure decides; maximal tractable | Ligozat 1998 |
| points, all 512 relations | NP-complete | Ligozat 1998 |
| regions, composition of basic relations | computed; the result can be a relation that is not basic | Skiadopoulos and Koubarakis 2004 |
| regions, basic constraints, regions may be disconnected | $O(n^5)$ | Skiadopoulos and Koubarakis 2005 |
| regions, disjunctive constraints | NP-complete | Skiadopoulos and Koubarakis 2005 |

**Preconvexity.** As for the interval algebra, a point relation is convex if it is an interval in the lattice of base relations ordered axis by axis, and preconvex if it becomes convex when relations of lower dimension, those with an $=$ on some axis, are added. For networks of preconvex relations, [algebraic closure](/algebraic-closure/) decides consistency (Ligozat 1998).

**Composition for regions.** Skiadopoulos and Koubarakis (2004) give an algorithm for the composition of two basic region relations. The result is in general a disjunction of basic relations, and because a region relation uses only the bounding box of the reference region, the composition must be computed with care: the box of $b$ does not fix where the parts of $b$ lie inside it.

## References
