---
tag: 5Z5ZVV
kind: definition
slug: el-description-logic
name: EL description logic
aliases:
- EL family
- EL++
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: advanced
summary: The description logic with only conjunction, existential restriction and top, in which subsumption with general TBoxes is polynomial.
prereqs: [description-logic, tbox-and-abox]
see_also: [el-classification, alc-description-logic, dl-lite, sroiq, concept-subsumption, ontology-classification, horn-sat, structural-subsumption]
sources:
  - paper: "Sebastian Brandt, Polynomial time reasoning in a description logic with existential restrictions, GCI axioms, and what else?, Proceedings of the 16th European Conference on Artificial Intelligence (ECAI), IOS Press, 2004"
    locator: pages 298 to 302 (EL with general TBoxes and role hierarchies stays polynomial)
  - paper: "Franz Baader, Sebastian Brandt and Carsten Lutz, Pushing the EL envelope, Proceedings of the 19th International Joint Conference on Artificial Intelligence (IJCAI), 2005"
    locator: pages 364 to 369 (the extension with bottom, nominals, concrete domains and role inclusions, and the extensions that make subsumption EXPTIME-complete)
  - book: isbn:9780521695428
    title: Franz Baader, Ian Horrocks, Carsten Lutz and Ulrike Sattler, An Introduction to Description Logic, Cambridge University Press, 2017
    locator: Chapter 6 (reasoning in the EL family, general locator)
  - url: "https://www.w3.org/TR/owl2-profiles/"
    title: W3C OWL Working Group, OWL 2 Web Ontology Language Profiles (Second Edition), W3C Recommendation, 2012
    locator: the section on the OWL 2 EL profile
---

EL is the [description logic](/description-logic/) whose concepts are built only with the top concept $\top$, conjunction $\sqcap$ and existential restriction $\exists r.C$. It has no negation, no disjunction and no universal restriction. Because of this, subsumption with respect to a general TBox can be decided in polynomial time, while it is EXPTIME-complete for [ALC](/alc-description-logic/). Many large ontologies, for example in medicine, need little more than these constructors. The *EL family* is EL together with extensions that keep reasoning polynomial, the largest of which is the logic of Baader, Brandt and Lutz (2005). The OWL 2 EL profile of the Web Ontology Language is based on it.

## Definition

Let $\mathsf{N_C}$ be a set of concept names and $\mathsf{N_R}$ a set of role names. **EL concepts** are given by

$$C, D \;::=\; \top \;\mid\; A \;\mid\; C \sqcap D \;\mid\; \exists r.C, \qquad A \in \mathsf{N_C},\ r \in \mathsf{N_R}.$$

An interpretation $I = (\Delta^I, \cdot^I)$ has a non-empty domain, a set $A^I \subseteq \Delta^I$ for each concept name and a relation $r^I \subseteq \Delta^I \times \Delta^I$ for each role name. As in ALC,

$$\top^I = \Delta^I, \quad (C \sqcap D)^I = C^I \cap D^I, \quad (\exists r.C)^I = \{\, d : (d, e) \in r^I \text{ for some } e \in C^I \,\}.$$

An **EL TBox** is a finite set of general concept inclusions $C \sqsubseteq D$ between EL concepts, with $C \equiv D$ as a short form for both directions. Cycles are allowed. $C$ is *subsumed by* $D$ with respect to $\mathcal T$, written $C \sqsubseteq_{\mathcal T} D$, if $C^I \subseteq D^I$ in every model $I$ of $\mathcal T$ (see [TBoxes and ABoxes](/tbox-and-abox/)).

The **EL family** extends EL with constructors and axioms that keep subsumption polynomial. The extension of Baader, Brandt and Lutz (2005) adds:

- the bottom concept $\bot$, with $\bot^I = \emptyset$;
- nominals $\{a\}$ for individual names $a$, with $\{a\}^I = \{a^I\}$;
- role inclusions $r_1 \circ \cdots \circ r_k \sqsubseteq r$, which cover role hierarchies ($k = 1$), transitive roles ($r \circ r \sqsubseteq r$) and right identities such as $r \circ s \sqsubseteq r$;
- concrete domain restrictions over concrete domains that satisfy a condition that they call p-admissibility.

Smaller members are named by letters added to EL, for example $\mathcal{EL}^{\bot}$ with bottom and $\mathcal{ELH}$ with role hierarchies.

Two facts make EL tractable.

- *Every EL concept is satisfiable with respect to every EL TBox.* Let $I_1$ have one element $d$ in every concept name, with $(d, d) \in r^{I_1}$ for every role $r$. By induction every EL concept contains $d$, so $I_1$ is a model of every EL TBox. With $\bot$ this fails, and satisfiability becomes a special case of subsumption, $C$ unsatisfiable if and only if $C \sqsubseteq_{\mathcal T} \bot$.
- *Subsumption with respect to a general TBox is in polynomial time* (Brandt 2004; Baader, Brandt and Lutz 2005). [EL classification](/el-classification/) computes all subsumptions between concept names with completion rules, and $C \sqsubseteq_{\mathcal T} D$ for complex $C$ and $D$ reduces to names by adding $A \equiv C$ and $B \equiv D$ for new names $A$ and $B$. Without a TBox, $C \sqsubseteq D$ holds if and only if there is a homomorphism from the description tree of $D$ to that of $C$.

## Examples and non-examples

- $\mathit{Pericarditis} \sqsubseteq \mathit{Inflammation} \sqcap \exists \mathit{hasLocation}.\mathit{Pericardium}$ is an EL inclusion. Medical terminologies such as SNOMED CT are written mostly in axioms of this form.
- With $\mathcal T = \{A \sqsubseteq \exists r.B,\ \exists r.B \sqsubseteq C\}$, $A \sqsubseteq_{\mathcal T} C$: an element of $A$ has an $r$-successor in $B$, so it is in $\exists r.B$, and so in $C$. The cyclic TBox $\{A \sqsubseteq \exists r.A\}$ is a valid EL TBox; its models contain infinite $r$-paths or $r$-cycles from each element of $A$.
- $\mathit{Parent} \equiv \mathit{Person} \sqcap \exists \mathit{hasChild}.\mathit{Person}$ is an EL definition. $\mathit{HappyParent} \equiv \mathit{Parent} \sqcap \forall \mathit{hasChild}.\mathit{Happy}$ is not, because it uses $\forall$.
- *Non-example:* $\neg A$, $A \sqcup B$ and $\forall r.\bot$ are not EL concepts, and no EL concept is equivalent to any of them. The interpretation $I_1$ above puts its element $d$ in every EL concept, but not in $\neg A$ or in $\forall r.\bot$. For $A \sqcup B$, take three elements with no edges: $a$ only in $A$, $b$ only in $B$, and $c$ in no name. An EL concept with an existential restriction as a conjunct contains none of them. Any other EL concept is $\top$ or a conjunction of names. If it contains $a$ and $b$ it can only be $\top$, and then it also contains $c$, which $A \sqcup B$ does not.
- *Non-example:* inverse roles $\exists r^-.C$ and universal restrictions are each enough to make subsumption EXPTIME-complete with general TBoxes (Baader, Brandt and Lutz 2005), so they are not in the EL family.

## Related definitions

- [ALC](/alc-description-logic/) adds negation, and so disjunction and universal restriction, to EL. With general TBoxes subsumption becomes [EXPTIME-complete](/alc-general-tbox-exptime/).
- [DL-Lite](/dl-lite/) is the other main tractable family. It allows inverse roles but only names and unqualified existentials $\exists r.\top$ on the left of inclusions, and it aims at query answering over large data instead of classification.
- [SROIQ](/sroiq/), the logic of OWL 2 DL, contains EL with bottom and nominals, and with the role inclusions that satisfy its regularity condition.
- [Concept subsumption](/concept-subsumption/) and [ontology classification](/ontology-classification/) are the reasoning tasks that EL makes polynomial.
- [Structural subsumption](/structural-subsumption/) decides subsumption without a TBox for small languages such as FL-, by comparing the parts of two concepts.
- An EL TBox in normal form behaves like a set of Horn rules; the completion rules work like the forward chaining of [Horn satisfiability](/horn-sat/).

## References
