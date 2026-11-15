---
tag: AQ4CJ2
kind: model
slug: rcc5
name: RCC5
aliases:
- RCC-5
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: core
summary: The calculus of five base relations between regions that ignores boundary contact, DR, PO, EQ, PP and PPi. It has 32 relations and NP-complete consistency.
prereqs: [qualitative-constraint-calculus, composition-table]
see_also: [region-connection-calculus-rcc8, qualitative-constraint-network, algebraic-closure, nine-intersection-model, point-algebra]
sources:
  - paper: "David A. Randell, Zhan Cui and Anthony G. Cohn, A spatial logic based on regions and connection, Proceedings of KR'92, Morgan Kaufmann, 1992"
    locator: pages 165 to 176 (the connection relation C, the relations defined from it, and the base relations of RCC8 and RCC5)
  - paper: "Peter Jonsson and Thomas Drakengren, A complete classification of tractability in RCC-5, Journal of Artificial Intelligence Research 6, 1997"
    locator: pages 211 to 221 (NP-completeness of RCC5 consistency and the four maximal tractable subclasses, one of which contains all base relations)
  - paper: doi:10.1016/S0004-3702(99)00002-8
    title: Jochen Renz and Bernhard Nebel, On the complexity of qualitative spatial reasoning, a maximal tractable fragment of the Region Connection Calculus, Artificial Intelligence 108(1-2), 1999
    locator: pages 69 to 123 (NP-hardness of RCC8 consistency and the tractable subclasses of RCC8, the finer calculus that RCC5 coarsens)
  - paper: doi:10.1145/3038927
    title: Frank Dylla and others, A survey of qualitative spatial and temporal calculi, algebraic and computational properties, ACM Computing Surveys 50(1), 2017
    locator: pages 1 to 39 (RCC5 among the surveyed calculi)
---

RCC5 is the [qualitative constraint calculus](/qualitative-constraint-calculus/) of five base relations between regions: discrete (DR), partial overlap (PO), equal (EQ), proper part (PP) and its converse (PPi). It is [RCC8](/region-connection-calculus-rcc8/) with boundary contact ignored: DC and EC become DR, TPP and NTPP become PP, and TPPi and NTPPi become PPi. It describes containment and overlap, as between counties, catchments or sets of documents, when touching does not matter. This page treats it as a model of computation for constraint networks.

## The machine

The domain is a set of regions, for example the non-empty regular closed subsets of the plane, with the relations defined from parthood $P$ and overlap $O$ as in Randell, Cui and Cohn (1992). For regions $x$ and $y$:

| relation | meaning |
| --- | --- |
| $x \mathrel{DR} y$ | $x$ and $y$ do not overlap (they may touch) |
| $x \mathrel{PO} y$ | they overlap and neither is part of the other |
| $x \mathrel{EQ} y$ | $x = y$ |
| $x \mathrel{PP} y$ | $x$ is part of $y$ and $x \ne y$ |
| $x \mathrel{PPi} y$ | $y \mathrel{PP} x$ |

The five relations are jointly exhaustive and pairwise disjoint. A relation is a set of base relations, so there are $2^5 = 32$ relations, with converse taken base by base: DR, PO and EQ are their own converses, and PP and PPi are converses of each other.

The [composition table](/composition-table/) gives the possible relations between $x$ and $z$ from $x \mathrel{r} y$ and $y \mathrel{s} z$. The table below has $r$ on the rows and $s$ on the columns; $\ast$ is the set of all five relations, and the EQ row and column are the identity.

| $r \diamond s$ | DR | PO | PP | PPi |
| --- | --- | --- | --- | --- |
| DR | $\ast$ | DR, PO, PP | DR, PO, PP | DR |
| PO | DR, PO, PPi | $\ast$ | PO, PP | DR, PO, PPi |
| PP | DR | DR, PO, PP | PP | $\ast$ |
| PPi | DR, PO, PPi | PO, PPi | PO, EQ, PP, PPi | PPi |

The table was computed in the model of non-empty sets, by listing every way three non-empty sets can share the seven cells of a Venn diagram, and it agrees with the published RCC5 table. Three cells are the full set $\ast$: DR with DR, PO with PO, and PP with PPi.

## What it counts

An input is a [qualitative constraint network](/qualitative-constraint-network/) on $n$ region variables, each pair labelled by one of the 32 relations. The questions are consistency, a solution (regions, or sets), and the minimal labels. Cost is counted in $n$, with a label stored in 5 bits on a word-RAM, so intersection, converse and a composition lookup are $O(1)$, and [algebraic closure](/algebraic-closure/) costs $O(n^3)$.

**Example.** The network $A \mathrel{PP} B$, $B \mathrel{PP} C$, $A \mathrel{DR} C$ is inconsistent: composition gives $A \mathrel{PP \diamond PP} C = A \mathrel{PP} C$, and the intersection with DR is empty, so algebraic closure finds the contradiction. The network $A \mathrel{PO} B$, $B \mathrel{PO} C$, $A \mathrel{DR} C$ is consistent: DR is in $PO \diamond PO$, and the sets $A = \{1, 2\}$, $B = \{2, 3\}$, $C = \{3, 4\}$ are a solution.

## Relation to other models

- **RCC8.** RCC5 is the coarsening of [RCC8](/region-connection-calculus-rcc8/) that merges each pair of relations that differ only in boundary contact. Every RCC5 relation is an RCC8 relation, so RCC5 networks are a special case of RCC8 networks.
- **Sets.** The RCC5 base relations are the relations between non-empty sets: disjoint, overlapping, equal, and proper subset either way. Reasoning in RCC5 is reasoning about the Boolean structure of the regions, with no topology.
- **Nine-intersection.** The [nine-intersection model](/nine-intersection-model/) can tell all eight RCC8 relations apart; RCC5 needs only whether the interiors meet and whether one region lies inside the other.
- **Point algebra.** The relations PP, EQ and PPi restricted to a chain of nested regions behave like $<, =, >$ of the [point algebra](/point-algebra/).

## Known results in the model

| problem | result | source |
| --- | --- | --- |
| consistency, all 32 relations | NP-complete | Jonsson and Drakengren 1997 |
| consistency, base relations only | polynomial | Jonsson and Drakengren 1997 |
| maximal tractable subclasses | exactly four, one of them containing all base relations | Jonsson and Drakengren 1997 |

**Membership in NP.** A network is consistent exactly when a refinement to base relations is consistent, and Jonsson and Drakengren (1997) show that this test is polynomial for base relations, so a refinement is a certificate.

**Classification.** Jonsson and Drakengren (1997) gave a complete classification: every subset of the 32 relations is either contained in one of four maximal tractable subclasses, or its consistency problem is NP-complete. The analogous question for RCC8 is answered by the [Renz-Nebel classification](/rcc8-tractable-subclasses/).

## References
