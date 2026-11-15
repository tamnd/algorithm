---
tag: 3NQTXX
kind: theorem
slug: rcc8-tractable-subclasses
name: Renz-Nebel tractability theorem for RCC8
aliases:
- maximal tractable subclasses of RCC8
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: research
summary: RCC8 consistency is NP-complete. Path consistency decides it for the 148 relations of H8, a maximal tractable class; with C8 and Q8 these are the only such classes with all base relations.
prereqs: [region-connection-calculus-rcc8, algebraic-closure, horn-sat]
see_also: [rcc5, nebel-burckert-theorem, ord-horn-subclass, interval-algebra-tractable-subclasses, qualitative-constraint-network, 3-sat]
sources:
  - paper: doi:10.1016/S0004-3702(99)00002-8
    title: Jochen Renz and Bernhard Nebel, On the complexity of qualitative spatial reasoning, a maximal tractable fragment of the Region Connection Calculus, Artificial Intelligence 108(1-2), 1999
    locator: pages 69 to 123 (NP-completeness of RSAT, the propositional encoding of RCC8, the class H8 of relations with a Horn encoding, the proof that path consistency decides RSAT(H8) through positive unit resolution, and the maximality of H8)
  - paper: "Jochen Renz, Maximal tractable fragments of the Region Connection Calculus, a complete analysis, Proceedings of IJCAI-99, Morgan Kaufmann, 1999"
    locator: pages 448 to 454 on the IJCAI site, 448 to 455 in dblp (Section 3, Definition 1, Lemma 2, Theorem 5 and Corollary 6 on reduction by refinement; Section 4, Lemma 7 to Lemma 12 and Definition 10 on NP8, P8, C8 and Q8; Section 5, Proposition 13, Proposition 16, Theorem 17 and Theorem 18)
  - paper: doi:10.1007/3-540-60343-3_40
    title: Bernhard Nebel, Computational properties of qualitative spatial reasoning, first results, KI-95, Lecture Notes in Artificial Intelligence 981, Springer, 1995
    locator: pages 233 to 244 (polynomial consistency for RCC8 base relations)
  - paper: "David A. Randell, Zhan Cui and Anthony G. Cohn, A spatial logic based on regions and connection, Proceedings of KR'92, Morgan Kaufmann, 1992"
    locator: pages 165 to 176 (the eight base relations)
  - paper: "Peter Jonsson and Thomas Drakengren, A complete classification of tractability in RCC-5, Journal of Artificial Intelligence Research 6, 1997"
    locator: pages 211 to 221 (the analogous classification for RCC5)
---

This theorem tells which [RCC8](/region-connection-calculus-rcc8/) constraint networks can be checked fast. Renz and Nebel (1999) proved that consistency is NP-complete in general, found a class $\widehat{\mathcal{H}}_8$ of 148 relations on which path consistency decides it in $O(n^3)$ time, and proved that this class cannot be enlarged. Renz (1999) then found two more maximal tractable classes, $\mathcal{C}_8$ and $\mathcal{Q}_8$, and showed that these three are the only maximal tractable classes that contain all base relations. It is the spatial counterpart of the [Nebel-Bürckert theorem](/nebel-burckert-theorem/) for Allen's interval algebra.

## Statement

**Setting.** A region is a non-empty regular closed subset of a topological space; a region need not be connected (Renz 1999, Section 2). The base relations are DC, EC, PO, EQ, TPP, NTPP, TPPi and NTPPi, and $\mathcal{B}$ is the set of these eight. An RCC8 relation is a set of base relations; there are 256. For a set $S$ of relations, RSAT$(S)$ is the problem: given a finite set $\Theta$ of constraints $x \mathrel{R} y$ with $R \in S$ over finitely many variables, is there an assignment of regions that meets every constraint? *Path consistency* is [algebraic closure](/algebraic-closure/) with the RCC8 composition table: repeat $R_{ij} \leftarrow R_{ij} \cap (R_{ik} \diamond R_{kj})$ until nothing changes, and report inconsistency if a label becomes empty. It runs in $O(n^3)$ time for $n$ variables. Path consistency *decides* RSAT$(S)$ if every path-consistent set over $S$ with no empty label is consistent.

Define, with $(N)TPP$ standing for TPP or NTPP:

- $N = \{R : PO \notin R$, $R$ contains TPP or NTPP, and $R$ contains TPPi or NTPPi$\}$, 72 relations;
- $NP_8 = N \cup \{\{EC, NTPP, EQ\}, \{EC, NTPPi, EQ\}, \{DC, EC, NTPP, EQ\}, \{DC, EC, NTPPi, EQ\}\}$, 76 relations, and $P_8$ = the other 180 relations;
- $\widehat{\mathcal{H}}_8 = P_8$ minus the relations $R$ with ($\{EQ, NTPP\} \subseteq R$ and $TPP \notin R$) or ($\{EQ, NTPPi\} \subseteq R$ and $TPPi \notin R$), 148 relations;
- $\mathcal{C}_8 = P_8$ minus the relations $R$ with $EC \in R$, $PO \notin R$ and $R \cap \{TPP, NTPP, TPPi, NTPPi, EQ\} \ne \emptyset$, 158 relations;
- $\mathcal{Q}_8 = P_8$ minus the relations $R$ with $EQ \in R$, $PO \notin R$ and $R \cap \{TPP, NTPP, TPPi, NTPPi\} \ne \emptyset$, 160 relations.

These are the definitions of Renz (1999, Definition 10 and Section 4); $\widehat{\mathcal{H}}_8$ is also the set of relations whose propositional encoding by Renz and Nebel (1999) is a Horn formula. The counts include the empty relation and were checked by enumeration.

**Theorem 1 (Renz and Nebel 1999).** (a) RSAT for all 256 relations is NP-complete. (b) RSAT$(\mathcal{B})$ is polynomial. (c) Path consistency decides RSAT$(\widehat{\mathcal{H}}_8)$, so it is solved in $O(n^3)$ time. (d) $\widehat{\mathcal{H}}_8$ is maximal: for every relation $R \notin \widehat{\mathcal{H}}_8$, RSAT$(\widehat{\mathcal{H}}_8 \cup \{R\})$ is NP-complete.

**Theorem 2 (Renz 1999, Theorems 17 and 18).** Path consistency decides RSAT$(\mathcal{C}_8)$ and RSAT$(\mathcal{Q}_8)$. For every set $S$ of RCC8 relations that contains all base relations and the universal relation, RSAT$(S)$ is polynomial if and only if $S \subseteq \widehat{\mathcal{H}}_8$, $S \subseteq \mathcal{C}_8$ or $S \subseteq \mathcal{Q}_8$; otherwise it is NP-complete.

## In plain words

Checking a set of topological facts about regions, such as "A touches B" or "C is inside D or overlaps it", is hard in general. But if every fact is one of 148 allowed kinds, a simple local rule, applied to every triple of regions until nothing changes, finds every contradiction. Adding any other kind of fact makes the problem hard again. Two other large sets of allowed kinds work in the same way, and no other set that contains the eight basic relations does.

## Proof

The full proofs are long and use computer checks, so this is a proof sketch with the exact locators.

*Membership in NP (Theorem 1a).* A set $\Theta$ is consistent exactly when one of its refinements to base relations is consistent, and by (b) such a refinement is checked in polynomial time. So a refinement is a certificate.

*Hardness (Theorem 1a, 1d) (Renz and Nebel 1999; summarized in Renz 1999, Lemma 7).* RSAT$(\mathcal{B} \cup \{R\})$ is NP-hard for every $R \in N$, and RSAT$(\widehat{\mathcal{H}}_8 \cup \{\{EQ, NTPP\}\})$ is NP-hard. Both are reductions from 3-SAT: each literal $L$ becomes a constraint $x_L \mathrel{R} y_L$ with $R = R_t \cup R_f$, true when $x_L \mathrel{R_t} y_L$ and false when $x_L \mathrel{R_f} y_L$; "polarity constraints" make a literal and its negation take opposite values, and "clause constraints" make at least one literal of each clause true. Maximality follows because the closure of $\widehat{\mathcal{H}}_8$ under intersection, converse and composition, plus any relation outside $\widehat{\mathcal{H}}_8 \cup N$, contains $\{EQ, NTPP\}$, and the closure can be simulated with extra variables when the universal relation is present.

*Tractability of $\widehat{\mathcal{H}}_8$ (Theorem 1b, 1c) (Renz and Nebel 1999).* Each RCC8 relation is encoded as a propositional formula over atoms that stand for region terms, following the encoding of RCC8 in modal logic. The relations of $\widehat{\mathcal{H}}_8$ are exactly those whose encoding is Horn, so RSAT$(\widehat{\mathcal{H}}_8)$ reduces to [Horn satisfiability](/horn-sat/), which is decided by positive unit resolution. Renz and Nebel relate positive unit resolution on the encoding to path consistency on the network, and show that positive unit resolution derives no empty clause from the encoding of a path-consistent set with no empty label. The base relations are in $\widehat{\mathcal{H}}_8$, which gives (b); Nebel (1995) had proved (b) earlier with an intuitionistic encoding.

*Reduction by refinement (Renz 1999, Definition 1 and Lemma 2).* Say that $S$ *reduces by refinement* to $T$ if each $R \in S$ has a sub-relation $T_R \in T$, and every path-consistent set $\Theta$ over $S$ can be refined, by replacing each $x_i \mathrel{R} x_j$ ($i < j$) with $x_i \mathrel{T_R} x_j$, to a set $\Theta'$ on which path consistency does not produce an empty label. **Lemma.** If path consistency decides RSAT$(T)$ and $S$ reduces by refinement to $T$, then path consistency decides RSAT$(S)$. *Proof.* Let $\Theta$ over $S$ be path consistent with no empty label. Refine it to $\Theta'$ as in the definition. Path consistency on $\Theta'$ gives a path-consistent set over $T$ with no empty label, which is consistent because path consistency decides RSAT$(T)$. A solution of a refinement of $\Theta$ is a solution of $\Theta$. $\square$

*Tractability of $\mathcal{C}_8$ and $\mathcal{Q}_8$ (Renz 1999, Proposition 13, Proposition 16, Theorem 17).* Every relation $R \in P_8 \setminus \widehat{\mathcal{H}}_8$ contains EQ, and $R \setminus \{EQ\}$ is in $\widehat{\mathcal{H}}_8$ (Proposition 13). Take the refinement that removes EQ from every such label. The procedure CHECK-REFINEMENTS (Renz 1999, Section 3, Lemma 4 and Theorem 5) tests, on every path-consistent triple of relations of the class, that the refinements stay consistent under path consistency, and it reaches a fixed point; the computer check succeeds for $\mathcal{C}_8$ and for $\mathcal{Q}_8$ (Proposition 16). So both classes reduce by refinement to $\widehat{\mathcal{H}}_8$, and the lemma gives Theorem 2, first part.

*Completeness of the list (Renz 1999, Lemmas 8, 9 and 12).* RSAT$(S)$ is NP-hard if $S \supseteq \mathcal{B}$ contains $\{EQ, NTPP\}$ together with $\{EC, NTPP\}$ or with $\{EC, TPP\}$ (Lemmas 8 and 9, again by 3-SAT), and RSAT$(\mathcal{B} \cup \{R\})$ is NP-hard for $R \in NP_8$ (Corollary 11). A computer enumeration of the closures of all sets that contain the base relations, the universal relation and two more relations shows that each is inside $\widehat{\mathcal{H}}_8$, $\mathcal{C}_8$ or $\mathcal{Q}_8$, or is NP-hard by these results (Lemma 12). With the tractability of the three classes, this gives Theorem 2. $\blacksquare$

## Consequences

- **Fast checks for most relations.** Networks whose labels are in $\widehat{\mathcal{H}}_8$, $\mathcal{C}_8$ or $\mathcal{Q}_8$ are decided by algebraic closure in $O(n^3)$ time. Since $\widehat{\mathcal{H}}_8 \cup \mathcal{C}_8 = P_8$, every relation outside $NP_8$ lies in one of the classes.
- **Better search.** A backtracking search for general RCC8 networks only needs to split each label into relations of one tractable class, not into base relations, and can run path consistency at each node as an exact test of the leaves.
- **A solution, not only a yes.** Gerevini and Renz (1998) gave an $O(n^3)$ algorithm that finds a consistent scenario for a set over $\widehat{\mathcal{H}}_8$, by removing EQ and then refining in a fixed order; by the refinement result it also applies to $\mathcal{C}_8$ and $\mathcal{Q}_8$ (Renz 1999, Section 6).
- **Base relations.** A network of base relations is decided by path consistency. This is used in every RCC8 reasoner.

## Tightness

- **Maximality.** Each of the three classes is maximal: adding any relation makes RSAT NP-complete.
- **Not unique.** Unlike the interval algebra, where the [ORD-Horn class](/ord-horn-subclass/) is the only maximal tractable class with all base relations, RCC8 has three. Their intersection is not maximal.
- **Hypotheses matter.** The classification covers sets that contain all base relations and the universal relation. Sets without some base relations are outside it. The results are about regular closed regions that may have several pieces; if regions must be connected, or be discs in the plane, the consistency problem changes.
- **Path consistency is not enough in general.** For the full set of 256 relations, path consistency runs in $O(n^3)$ but cannot decide an NP-complete problem unless P = NP.

## History

Randell, Cui and Cohn (1992) introduced the region connection calculus and its eight base relations. Nebel (1995) showed that networks of base relations are decided in polynomial time, using Bennett's encoding in intuitionistic logic. Renz and Nebel (1999) proved NP-completeness of the full calculus and found the maximal tractable class $\widehat{\mathcal{H}}_8$. Renz (1999) introduced reduction by refinement, found $\mathcal{C}_8$ and $\mathcal{Q}_8$, and completed the classification for sets with all base relations. The analogous classification of [RCC5](/rcc5/) is due to Jonsson and Drakengren (1997).

## References
