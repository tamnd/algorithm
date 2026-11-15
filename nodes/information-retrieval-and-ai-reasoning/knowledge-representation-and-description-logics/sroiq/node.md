---
tag: 790R66
kind: definition
slug: sroiq
name: SROIQ
aliases:
- SROIQ(D)
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: advanced
summary: An expressive description logic with role chains, nominals, inverses and qualified number restrictions, the logic behind OWL 2 DL.
prereqs: [alc-description-logic, tbox-and-abox]
see_also: [hypertableau, tableau-blocking, el-description-logic, dl-lite, alc-general-tbox-exptime, unique-name-assumption, open-world-assumption, ontology-knowledge-representation]
sources:
  - paper: "Ian Horrocks, Oliver Kutz and Ulrike Sattler, The even more irresistible SROIQ, Proceedings of the 10th International Conference on Principles of Knowledge Representation and Reasoning (KR), 2006"
    locator: pages 57 to 67 (the syntax and semantics of SROIQ, regular role inclusions, simple roles, and a tableau algorithm)
  - paper: "Yevgeny Kazakov, RIQ and SROIQ are harder than SHOIQ, Proceedings of the 11th International Conference on Principles of Knowledge Representation and Reasoning (KR), 2008"
    locator: pages 274 to 284 (SROIQ is N2EXPTIME-complete)
  - url: "https://www.w3.org/TR/owl2-overview/"
    title: W3C OWL Working Group, OWL 2 Web Ontology Language Document Overview (Second Edition), W3C Recommendation, 2012
    locator: the overview of OWL 2 DL, its direct semantics and its profiles
  - paper: doi:10.1613/jair.2811
    title: Boris Motik, Rob Shearer and Ian Horrocks, Hypertableau reasoning for description logics, Journal of Artificial Intelligence Research 36, 2009
    locator: pages 165 to 228 (a hypertableau calculus for expressive description logics with nominals, inverse roles and number restrictions)
---

SROIQ is the [description logic](/description-logic/) of Horrocks, Kutz and Sattler (2006) on which OWL 2 DL is based. It extends [ALC](/alc-description-logic/) with transitive roles and complex role inclusions such as $\mathit{hasParent} \circ \mathit{hasBrother} \sqsubseteq \mathit{hasUncle}$, nominals, inverse roles, qualified number restrictions, the universal role, self restrictions and properties of roles such as reflexivity and disjointness. With datatypes it is written SROIQ(D). To keep it decidable, role inclusions must be *regular*, and number restrictions and a few other constructors may only use *simple* roles. Reasoning is N2EXPTIME-complete (Kazakov 2008).

## Definition

The name lists the parts. S is ALC with transitive roles, R stands for complex role inclusions and the other role axioms, O for nominals, I for inverse roles, and Q for qualified number restrictions.

**Roles.** A role is a role name $P$, an inverse $P^-$, or the universal role $U$, with $(P^-)^I = \{(e, d) : (d, e) \in P^I\}$ and $U^I = \Delta^I \times \Delta^I$.

**Role axioms (the RBox).**

- role inclusions $R_1 \circ \cdots \circ R_k \sqsubseteq R$, with $(R_1 \circ \cdots \circ R_k)^I \subseteq R^I$ for the composition of relations;
- disjointness $\mathrm{Dis}(S_1, S_2)$, meaning $S_1^I \cap S_2^I = \emptyset$;
- the role properties reflexive $\mathrm{Ref}(R)$, irreflexive $\mathrm{Irr}(S)$ and asymmetric $\mathrm{Asy}(S)$.

Transitivity is the inclusion $R \circ R \sqsubseteq R$, and symmetry is $R^- \sqsubseteq R$.

**Concepts.** For concept names $A$, individual names $a$, roles $R$, simple roles $S$ and $n \ge 0$:

$$C ::= \top \mid \bot \mid A \mid \{a\} \mid \neg C \mid C \sqcap C \mid C \sqcup C \mid \exists R.C \mid \forall R.C \mid {\geq} n\, S.C \mid {\leq} n\, S.C \mid \exists S.\mathrm{Self},$$

with $\{a\}^I = \{a^I\}$, $({\geq} n\, S.C)^I$ the elements with at least $n$ $S$-successors in $C$, $({\leq} n\, S.C)^I$ those with at most $n$, and $(\exists S.\mathrm{Self})^I = \{d : (d, d) \in S^I\}$. A TBox is a finite set of general concept inclusions, and an ABox may also contain $\neg P(a, b)$, $a \approx b$ and $a \not\approx b$. There is no [unique name assumption](/unique-name-assumption/), and the semantics follows the [open world assumption](/open-world-assumption/).

**Regularity.** Let $\prec$ be a strict partial order on roles, with $S \prec R$ if and only if $S^- \prec R$. A role inclusion with right side a role name $R$ is $\prec$-*regular* if its left side has one of the forms

$$R \circ R, \qquad R^-, \qquad S_1 \circ \cdots \circ S_n, \qquad R \circ S_1 \circ \cdots \circ S_n, \qquad S_1 \circ \cdots \circ S_n \circ R,$$

with $S_i \prec R$ for all $i$. An RBox is regular if one order $\prec$ makes every inclusion regular. Then, for each role, the chains of roles that imply it form a regular language, which a tableau algorithm can follow with a finite automaton.

**Simple roles.** A role is *non-simple* if it is the right side of an inclusion with a chain of length at least 2, or if it is implied by a non-simple role, also through inverses. All other roles are simple. Number restrictions, $\exists S.\mathrm{Self}$, $\mathrm{Dis}$, $\mathrm{Irr}$ and $\mathrm{Asy}$ may only use simple roles.

**Reasoning.** Satisfiability, subsumption and knowledge base consistency are decidable and N2EXPTIME-complete. Horrocks, Kutz and Sattler gave a tableau algorithm with [blocking](/tableau-blocking/), and practical reasoners such as HermiT use the [hypertableau](/hypertableau/) calculus.

## Examples and non-examples

- $\mathit{hasParent} \circ \mathit{hasBrother} \sqsubseteq \mathit{hasUncle}$ is regular, with $\mathit{hasParent} \prec \mathit{hasUncle}$ and $\mathit{hasBrother} \prec \mathit{hasUncle}$. It makes $\mathit{hasUncle}$ non-simple.
- $\mathit{hasAncestor} \circ \mathit{hasAncestor} \sqsubseteq \mathit{hasAncestor}$ makes the role transitive. Then ${\leq} 2\, \mathit{hasAncestor}.\mathit{Person}$ is not allowed, because $\mathit{hasAncestor}$ is not simple.
- ${\geq} 2\, \mathit{hasChild}.\mathit{Female}$ (at least two daughters), $\exists \mathit{hasNationality}.\{\mathit{italy}\}$ (a nominal) and $\exists \mathit{loves}.\mathrm{Self}$ (loves oneself) are SROIQ concepts.
- *Non-example:* the RBox $\{R \circ S \sqsubseteq R,\ S \circ R \sqsubseteq S\}$ is not regular. The first inclusion has the form $R \circ S_1$ and needs $S \prec R$; the second has the form $S \circ S_1$ and needs $R \prec S$. No strict order has both.
- *Non-example:* $R \circ S \circ R \sqsubseteq R$ does not have any of the allowed forms, so it is not regular for any order.

## Related definitions

- SHOIN is the logic of the first version of OWL, OWL DL. SROIQ adds complex role inclusions, qualified number restrictions, self restrictions and the other role axioms.
- [ALC](/alc-description-logic/) is the base. Its satisfiability problem with general TBoxes is [EXPTIME-complete](/alc-general-tbox-exptime/), and Kazakov's title, RIQ and SROIQ are harder than SHOIQ, refers to the higher bounds that complex role inclusions bring.
- The OWL 2 profiles are fragments of OWL 2 DL with lower complexity: OWL 2 EL is based on [EL](/el-description-logic/) and OWL 2 QL on [DL-Lite](/dl-lite/). OWL 2 RL is a third profile designed for rule engines, and it is not based on either of them.

## References
