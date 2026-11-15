---
tag: W56YNG
kind: model
slug: double-cross-calculus
name: Double-cross calculus
aliases:
- Freksa double cross
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: advanced
summary: Locates a point relative to an oriented segment by which side of it and of the two perpendiculars at its ends the point lies on. Its consistency problem is NP-hard even for base relations.
prereqs: [orientation-test, qualitative-constraint-calculus]
see_also: [cardinal-direction-calculus, qualitative-constraint-network, composition-table, cylindrical-algebraic-decomposition, region-connection-calculus-rcc8]
sources:
  - paper: doi:10.1007/3-540-55966-3_10
    title: Christian Freksa, Using orientation information for qualitative spatial reasoning, Theories and Methods of Spatio-Temporal Reasoning in Geographic Space, Lecture Notes in Computer Science 639, Springer, 1992
    locator: pages 162 to 178 (the single cross and the double cross, the 15 positions of a point relative to an oriented segment, and reasoning with them)
  - paper: doi:10.1007/3-540-45424-1_29
    title: Alexander Scivos and Bernhard Nebel, Double-crossing, decidability and computational complexity of a qualitative calculus for navigation, COSIT 2001, Lecture Notes in Computer Science 2205, Springer, 2001
    locator: pages 431 to 446 (NP-hardness of consistency for networks of base relations, and that the calculus is not closed under composition)
  - paper: doi:10.1145/3038927
    title: Frank Dylla and others, A survey of qualitative spatial and temporal calculi, algebraic and computational properties, ACM Computing Surveys 50(1), 2017
    locator: pages 1 to 39 (the double-cross calculus among the ternary calculi)
---

The double-cross calculus of Freksa (1992) describes the relative orientation of three points: where a point $c$ lies as seen by someone who walks from $a$ to $b$. The line through $a$ and $b$ tells left from right, and the two lines perpendicular to it at $a$ and at $b$ tell behind, beside and ahead. These three lines form a double cross, and they split the plane into 15 positions for $c$. The calculus was made for navigation, where an agent knows the way it is facing but not distances. Its relations are ternary, and Scivos and Nebel (2001) showed that deciding the consistency of a set of base relations is NP-hard.

## The machine

Let $a \ne b$ be points of $\mathbb{R}^2$ and let $c$ be a third point. Write $d = b - a$. The relation of $c$ to the oriented segment $(a, b)$ is a pair (side, position):

- *side*: the sign of the cross product $d \times (c - a)$, which is left if positive, straight (on the line) if zero, and right if negative; this is the [orientation test](/orientation-test/);
- *position*: from the dot products $p = d \cdot (c - a)$ and $q = d \cdot (c - b)$, it is back if $p < 0$, at $a$ if $p = 0$, between if $p > 0$ and $q < 0$, at $b$ if $q = 0$, and front if $q > 0$.

This gives $3 \times 5 = 15$ base relations for $a \ne b$. Two of them are single points: straight and at $a$ means $c = a$, and straight and at $b$ means $c = b$. The others are open regions, open rays or open segments of lines. Later formalizations add base relations for the cases in which $a = b$, so that every triple of points has exactly one relation.

Freksa built the double cross from two *single crosses*, one at $a$ and one at $b$, each made of the line through $a$ and $b$ and the perpendicular at that point. Each single cross alone describes the position of $c$ relative to one end.

**Example.** Let $a = (0, 0)$ and $b = (4, 0)$, so $d = (4, 0)$.

| $c$ | cross product | $p$ | $q$ | relation |
| --- | --- | --- | --- | --- |
| $(2, 1)$ | $4$ | $8$ | $-8$ | left, between |
| $(5, -1)$ | $-4$ | $20$ | $4$ | right, front |
| $(-1, 0)$ | $0$ | $-4$ | $-20$ | straight, back |
| $(0, 3)$ | $12$ | $0$ | $-16$ | left, at $a$ |
| $(4, -2)$ | $-8$ | $16$ | $0$ | right, at $b$ |

With integer coordinates all three values are exact, so the relation is computed in $O(1)$ time with no rounding error.

## What it counts

An input is a set of $n$ point variables and a set of ternary constraints, each saying that a triple $(a, b, c)$ is in one base relation or in a set of them. The question is consistency: are there points in the plane that meet every constraint? Cost is counted in $n$ and in the number of constraints.

The constraints are sign conditions on polynomials of degree 2 in the coordinates, so consistency is a question in the existential theory of the reals, and it is decidable, for example by [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/). Hardness lies in the other direction: Scivos and Nebel (2001) show that the problem is NP-hard even when every constraint is a base relation.

**Reasoning with tables.** Freksa (1992) reasoned with tables: for the permutations of the three points, and for combining two relations that share two points into a relation on a new triple, in the manner of a [composition table](/composition-table/). Scivos and Nebel (2001) show that the calculus is not closed under composition, so such tables can only give a relation that contains the true one, and local propagation with them does not decide consistency.

## Relation to other models

- **Cardinal directions.** The [cardinal direction calculus](/cardinal-direction-calculus/) uses a fixed frame, the axes of the plane, and binary relations. The double cross uses a frame defined by two of the points, so its relations are ternary and invariant under rotation, translation and scaling.
- **Other ternary calculi.** The LR calculus keeps only the line through $a$ and $b$, and the OPRA calculi of Moratz relate points that carry their own orientation. They share the use of the orientation test.
- **Binary calculi.** For binary calculi such as [RCC8](/region-connection-calculus-rcc8/), a [qualitative constraint network](/qualitative-constraint-network/) of base relations is often decided by algebraic closure in polynomial time. The double cross is an example in which this fails already for base relations.

## Known results in the model

| problem | result | source |
| --- | --- | --- |
| relation of a given triple | $O(1)$ arithmetic operations | Freksa 1992, with the formulas above |
| consistency, base relations only | NP-hard | Scivos and Nebel 2001 |
| consistency, any constraints | decidable, through the existential theory of the reals | Scivos and Nebel 2001 |
| closure under composition | no | Scivos and Nebel 2001 |

The tables of Freksa (1992) give a sound method: a contradiction that they find is real. By the hardness result, unless P = NP, no polynomial propagation with them finds every inconsistent network of base relations.

## References
