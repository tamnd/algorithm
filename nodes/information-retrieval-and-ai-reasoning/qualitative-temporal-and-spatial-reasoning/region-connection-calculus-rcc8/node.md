---
tag: Q13CY9
kind: model
slug: region-connection-calculus-rcc8
name: RCC8
aliases:
- region connection calculus
- RCC-8
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: core
summary: The calculus of eight base relations between regions, from disconnected to non-tangential proper part. It has 256 relations, weak composition and NP-complete consistency.
prereqs: [qualitative-constraint-calculus, composition-table]
see_also: [rcc5, rcc8-tractable-subclasses, nine-intersection-model, qualitative-constraint-network, algebraic-closure, rectangle-algebra, cardinal-direction-calculus]
sources:
  - paper: "David A. Randell, Zhan Cui and Anthony G. Cohn, A spatial logic based on regions and connection, Proceedings of KR'92, Morgan Kaufmann, 1992"
    locator: pages 165 to 176 (the primitive connection relation, the relations defined from it, and the eight base relations)
  - paper: doi:10.1016/S0004-3702(99)00002-8
    title: Jochen Renz and Bernhard Nebel, On the complexity of qualitative spatial reasoning, a maximal tractable fragment of the Region Connection Calculus, Artificial Intelligence 108(1-2), 1999
    locator: pages 69 to 123 (NP-completeness of RCC8 consistency, the modal encoding, and the maximal tractable subclass H8)
  - paper: doi:10.1007/3-540-60343-3_40
    title: Bernhard Nebel, Computational properties of qualitative spatial reasoning, first results, KI-95, Lecture Notes in Artificial Intelligence 981, Springer, 1995
    locator: pages 233 to 244 (polynomial consistency for networks of RCC8 base relations, through an encoding in intuitionistic logic)
  - paper: "Jochen Renz, Maximal tractable fragments of the Region Connection Calculus, a complete analysis, Proceedings of IJCAI-99, Morgan Kaufmann, 1999"
    locator: pages 448 to 454 (the three maximal tractable subclasses of RCC8 that contain all base relations)
  - paper: doi:10.1007/11564751_40
    title: Jochen Renz and Gérard Ligozat, Weak composition for qualitative spatial and temporal reasoning, CP 2005, Lecture Notes in Computer Science 3709, Springer, 2005
    locator: pages 534 to 548 (weak composition, and that the RCC8 composition table is weak)
  - paper: doi:10.1145/3038927
    title: Frank Dylla and others, A survey of qualitative spatial and temporal calculi, algebraic and computational properties, ACM Computing Surveys 50(1), 2017
    locator: pages 1 to 39 (RCC8 among the surveyed calculi)
---

RCC8 is the [qualitative constraint calculus](/qualitative-constraint-calculus/) of the region connection calculus of Randell, Cui and Cohn (1992). It has eight base relations between regions: disconnected (DC), externally connected (EC), partial overlap (PO), equal (EQ), tangential and non-tangential proper part (TPP, NTPP) and their converses (TPPi, NTPPi). It is the most used calculus for topology in geographic information systems, spatial databases and robotics. Consistency of RCC8 networks is NP-complete, but it is polynomial for the base relations and for the large subclass $\widehat{\mathcal{H}}_8$ of [Renz and Nebel](/rcc8-tractable-subclasses/).

## The machine

The domain is a set of regions, usually the non-empty regular closed subsets of a topological space such as $\mathbb{R}^2$. The one primitive is *connection*: $C(x, y)$ holds when the closures of $x$ and $y$ share a point. The other relations are defined from it (Randell, Cui and Cohn 1992):

- $P(x, y)$, $x$ is part of $y$: every region connected to $x$ is connected to $y$;
- $O(x, y)$, overlap: some region is part of both;
- $DC(x, y) = \lnot C(x, y)$; $EC(x, y) = C(x, y) \land \lnot O(x, y)$;
- $PO(x, y)$: $O(x, y)$ and neither is part of the other; $EQ(x, y)$: each is part of the other;
- $TPP(x, y)$: $x$ is a proper part of $y$ and some region is externally connected to both; $NTPP(x, y)$: $x$ is a proper part of $y$ and no such region exists;
- TPPi and NTPPi are the converses of TPP and NTPP.

In the plane, $x \mathrel{TPP} y$ means that $x$ lies inside $y$ and touches its boundary, and $x \mathrel{NTPP} y$ means that $x$ lies in the interior of $y$. The eight base relations are jointly exhaustive and pairwise disjoint. A relation is a set of them, so there are $2^8 = 256$ relations, including the empty one.

**Composition.** The $8 \times 8$ [composition table](/composition-table/) lists the base relations possible between $x$ and $z$ given $x \mathrel{r} y$ and $y \mathrel{s} z$. Some entries: $NTPP \diamond NTPP = NTPP$; $TPP \diamond TPP = \{TPP, NTPP\}$; $EC \diamond NTPP = \{PO, TPP, NTPP\}$; $DC \diamond DC$ is the set of all eight relations. The table is a *weak* composition: each entry is the smallest relation that contains the true composition, but in some models the true composition of two base relations is not a union of base relations, so the inclusion is strict (Renz and Ligozat 2005). [Algebraic closure](/algebraic-closure/) for RCC8 therefore uses weak composition, and it is called path consistency in most of the RCC8 literature.

## What it counts

An input is a [qualitative constraint network](/qualitative-constraint-network/) on $n$ region variables with RCC8 labels. The questions are consistency, the minimal labels, and a realization by regions. Cost is counted in $n$. On a word-RAM a label is an 8-bit mask, a composition of two labels is a union of at most 64 table entries, which can be stored as a $256 \times 256$ table of bytes, and algebraic closure costs $O(n^3)$.

**Example.** $A \mathrel{TPP} B$, $B \mathrel{NTPP} C$, $A \mathrel{EC} C$ is inconsistent: $TPP \diamond NTPP = NTPP$, so closure sets the label of $(A, C)$ to $NTPP \cap EC = \emptyset$. The network $A \mathrel{EC} B$, $B \mathrel{EC} C$, $A \mathrel{EC} C$ is consistent: three sectors of a disc that meet at its centre touch pairwise along their boundaries.

## Relation to other models

- **RCC5.** Merging DC with EC, TPP with NTPP and TPPi with NTPPi gives [RCC5](/rcc5/), which ignores boundary contact.
- **Nine-intersection.** For simple regions in the plane, the eight RCC8 relations are exactly the eight relations of the [nine-intersection model](/nine-intersection-model/) of Egenhofer, which records which intersections of interiors, boundaries and exteriors are empty.
- **Rectangles and directions.** The [rectangle algebra](/rectangle-algebra/) and the [cardinal direction calculus](/cardinal-direction-calculus/) describe orientation, which RCC8 does not; for rectangles, each RCC8 relation is a union of rectangle relations.
- **Logic.** Bennett encoded RCC8 relations in intuitionistic propositional logic, which Nebel (1995) used for the base relations, and Renz and Nebel (1999) used a modal encoding, where regions are propositions and the interior of a region is read as a modal operator. These encodings give the polynomial results below.

## Known results in the model

| problem | result | source |
| --- | --- | --- |
| consistency, base relations | polynomial; algebraic closure decides | Nebel 1995; Renz and Nebel 1999 |
| consistency, all 256 relations | NP-complete | Renz and Nebel 1999 |
| the class $\widehat{\mathcal{H}}_8$ of 148 relations | algebraic closure decides; maximal tractable | Renz and Nebel 1999 |
| maximal tractable subclasses with all base relations | exactly three, $\widehat{\mathcal{H}}_8$, $\mathcal{C}_8$ and $\mathcal{Q}_8$ | Renz 1999 |
| composition | weak | Renz and Ligozat 2005 |

**Hardness and membership.** Renz and Nebel (1999) prove NP-hardness by a reduction from propositional satisfiability, and the problem is in NP because a network is consistent exactly when some refinement of its labels to base relations is, and that refinement can be checked in polynomial time. The exact statement of the tractability results, with a proof sketch, is on the page [maximal tractable subclasses of RCC8](/rcc8-tractable-subclasses/).

**Realization.** Consistency here means a solution by regular closed regions, which may have several pieces. If every region must be connected in the plane, the problem is a different one; with thin curves as regions, deciding which pairs may be DC and which must meet is close to the recognition of string graphs, the intersection graphs of curves in the plane.

## References
