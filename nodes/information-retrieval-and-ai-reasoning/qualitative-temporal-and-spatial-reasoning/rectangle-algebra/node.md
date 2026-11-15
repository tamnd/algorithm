---
tag: M531Q4
kind: model
slug: rectangle-algebra
name: Rectangle algebra
aliases:
- rectangle calculus
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: advanced
summary: The qualitative calculus of axis-parallel rectangles, with one Allen relation per axis. It has 169 base relations, 2^169 relations, and NP-complete consistency.
prereqs: [allens-interval-algebra, qualitative-constraint-calculus]
see_also: [composition-table, ord-horn-subclass, nebel-burckert-theorem, interval-algebra-np-completeness, cardinal-direction-calculus, region-connection-calculus-rcc8, minimum-bounding-rectangle, r-tree]
sources:
  - paper: "Philippe Balbiani, Jean-François Condotta and Luis Fariñas del Cerro, A new tractable subclass of the rectangle algebra, Proceedings of IJCAI-99, Morgan Kaufmann, 1999, pages 442 to 447"
    locator: the rectangle algebra as a product of two interval algebras, its consistency problem, and a tractable subclass beyond products of tractable interval relations
  - paper: doi:10.1007/3-540-48159-1_6
    title: Philippe Balbiani, Jean-François Condotta and Luis Fariñas del Cerro, A tractable subclass of the block algebra, constraint propagation and preconvex relations, EPIA 1999, Lecture Notes in Computer Science, Springer, 1999
    locator: pages 75 to 89 (the block algebra in n dimensions and its preconvex relations)
  - paper: doi:10.1093/logcom/12.5.885
    title: Philippe Balbiani, Jean-François Condotta and Luis Fariñas del Cerro, Tractability results in the block algebra, Journal of Logic and Computation 12(5), 2002
    locator: pages 885 to 909 (tractable subclasses of the block algebra, where path consistency decides consistency)
  - paper: doi:10.1145/182.358434
    title: James F. Allen, Maintaining knowledge about temporal intervals, Communications of the ACM 26(11), 1983
    locator: pages 832 to 843 (the interval relations used on each axis)
  - paper: doi:10.1145/3038927
    title: Frank Dylla and others, A survey of qualitative spatial and temporal calculi, algebraic and computational properties, ACM Computing Surveys 50(1), 2017
    locator: pages 1 to 39 (the rectangle and block algebras among the surveyed calculi)
---

The rectangle algebra describes how two rectangles with sides parallel to the axes lie relative to each other, by giving one relation of [Allen's interval algebra](/allens-interval-algebra/) for their projections on the $x$ axis and one for their projections on the $y$ axis. "A is left of B and overlaps it vertically" is the base relation $(b, o)$. It is the standard [qualitative constraint calculus](/qualitative-constraint-calculus/) for layouts, maps and documents, where objects are often summarised by their [minimum bounding rectangles](/minimum-bounding-rectangle/). This page treats it as a model: what a problem in it may say, what is counted, and what is known about its complexity.

## The machine

The domain is the set of rectangles $A = X_A \times Y_A$, where $X_A = (x_A^-, x_A^+)$ and $Y_A = (y_A^-, y_A^+)$ are intervals with $x_A^- < x_A^+$ and $y_A^- < y_A^+$. The base relations are the pairs $(r, s)$ of interval base relations, with

$$A \mathrel{(r, s)} B \iff X_A \mathrel{r} X_B \text{ and } Y_A \mathrel{s} Y_B.$$

There are $13 \times 13 = 169$ base relations, and they are jointly exhaustive and pairwise disjoint because the interval relations are. A relation is any set of base relations, so there are $2^{169}$ relations. The identity is $(eq, eq)$. Converse and composition work axis by axis:

$$(r, s)^{\smile} = (r^{\smile}, s^{\smile}), \qquad (r_1, s_1) \diamond (r_2, s_2) = (r_1 \diamond r_2) \times (s_1 \diamond s_2),$$

so the $169 \times 169$ [composition table](/composition-table/) is read off the interval table and never stored. Composition is strong, because it is strong on each axis and the axes are independent.

A relation of the form $R \times S$, with $R$ and $S$ interval relations, is a *product relation*; there are $8191^2 + 1$ of them, counting the empty relation. Most relations are not products: "A is left of B or above B" is $(\{b\} \times \mathcal{B}) \cup (\mathcal{B} \times \{bi\})$, a union that no product equals.

## What it counts

An input is a [qualitative constraint network](/qualitative-constraint-network/) on $n$ rectangles. The questions are the usual ones: consistency, a solution (rectangles with real or integer coordinates), and minimal labels. Cost is measured in $n$. A label is a set of up to 169 base relations, so a word-RAM implementation stores it as 169 bits, or as a pair of 13-bit masks when it is a product.

## Relation to other models

- **Interval algebra.** Each axis is an interval network. A network whose labels are all products $R_{ij} \times S_{ij}$ is consistent exactly when the $x$ network with labels $R_{ij}$ and the $y$ network with labels $S_{ij}$ are both consistent, since the two axes do not interact.
- **Block algebra.** The same construction in $k$ dimensions has $13^k$ base relations (Balbiani, Condotta and Fariñas del Cerro 1999, 2002).
- **Cardinal directions.** The [cardinal direction calculus](/cardinal-direction-calculus/) for points is the same product idea with the [point algebra](/point-algebra/) on each axis, $3 \times 3 = 9$ base relations.
- **Topology.** [RCC8](/region-connection-calculus-rcc8/) describes contact and containment of arbitrary regions. For rectangles, each RCC8 relation is a union of rectangle relations; for example, two closed rectangles are disconnected exactly when their projections are in the interval relation $b$ or $bi$ on at least one axis.
- **Spatial indexes.** An [R-tree](/r-tree/) query such as "all boxes that intersect B" is a rectangle relation: the base relations whose projections intersect on both axes.

## Known results in the model

| problem | result | source |
|---|---|---|
| consistency, all $2^{169}$ relations | NP-complete | by embedding the interval algebra |
| product relations $R \times S$ with $R$, $S$ in a tractable interval class | polynomial, axis by axis | follows from the interval results |
| product relations with $R$, $S$ ORD-Horn | algebraic closure decides, $O(n^3)$ | Nebel and Bürckert 1995 on each axis |
| strongly preconvex relations (not only products) | algebraic closure decides | Balbiani, Condotta and Fariñas del Cerro 1999 |
| block algebra, $k$ dimensions | analogous tractable subclasses | Balbiani, Condotta and Fariñas del Cerro 2002 |

**Hardness.** Membership in NP: guess the order of the $2n$ endpoints on each axis, then check each label. Hardness: map an interval network $N$ with labels $C_{ij}$ to the rectangle network with labels $C_{ij} \times \{eq\}$. All rectangles then have the same $y$ projection, and a solution of one network gives a solution of the other. So consistency is at least as hard as for intervals, which is [NP-complete](/interval-algebra-np-completeness/).

**Products of ORD-Horn relations.** If every label is $R_{ij} \times S_{ij}$ with $R_{ij}$, $S_{ij}$ in the [ORD-Horn subclass](/ord-horn-subclass/), algebraic closure of the rectangle network keeps product labels, since intersection, converse and composition of products are products. If the closure has no empty label, then $R_{ij} \subseteq R_{ik} \diamond R_{kj}$ on each axis, so each axis network is closed, and by the [Nebel-Bürckert theorem](/nebel-burckert-theorem/) each is consistent. So closure decides these networks in $O(n^3)$ time.

**Beyond products.** Balbiani, Condotta and Fariñas del Cerro (1999) defined the strongly preconvex rectangle relations, a class that contains relations that are not products, and showed that algebraic closure decides consistency for it.

## References
