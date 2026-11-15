---
tag: WBG748
kind: definition
slug: alc-description-logic
name: ALC
aliases:
- attributive concept language with complements
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: core
summary: The basic description logic with concept negation, conjunction, disjunction and existential and universal role restrictions.
prereqs: [description-logic]
see_also: [tbox-and-abox, concept-satisfiability, alc-tableau-algorithm, el-description-logic, alc-modal-k-correspondence, kripke-structure, bisimulation, sroiq]
sources:
  - paper: doi:10.1016/0004-3702(91)90078-X
    title: Manfred Schmidt-Schauß and Gert Smolka, Attributive concept descriptions with complements, Artificial Intelligence 48(1), 1991
    locator: pages 1 to 26 (the syntax and semantics of ALC, and the name, attributive concept language with complements)
  - book: isbn:9780521695428
    title: Franz Baader, Ian Horrocks, Carsten Lutz and Ulrike Sattler, An Introduction to Description Logic, Cambridge University Press, 2017
    locator: Chapter 2 (the syntax and semantics of ALC, negation normal form) and Chapter 3 (bisimulation and the expressive power of ALC)
  - book: isbn:9780521876254
    title: Franz Baader, Diego Calvanese, Deborah L. McGuinness, Daniele Nardi and Peter F. Patel-Schneider (eds.), The Description Logic Handbook, second edition, Cambridge University Press, 2007
    locator: Chapter 2, Basic Description Logics, by Franz Baader and Werner Nutt, Section 2.2 (the AL family of languages and their semantics)
  - paper: "Klaus Schild, A correspondence theory for terminological logics: preliminary report, Proceedings of the 12th International Joint Conference on Artificial Intelligence (IJCAI), 1991"
    locator: ALC as a notational variant of the multimodal logic K (general locator)
---

ALC is the [description logic](/description-logic/) whose concepts are built from concept names with $\top$, $\bot$, negation $\neg$, conjunction $\sqcap$, disjunction $\sqcup$, existential restriction $\exists r.C$ and universal restriction $\forall r.C$. Schmidt-Schauß and Smolka (1991) named it: AL is the attributive language, and C adds the complement of any concept. It is closed under all Boolean operations, and it is the base that most expressive description logics extend.

## Definition

Fix three disjoint sets: concept names $A, B, \ldots$, role names $r, s, \ldots$ and individual names $a, b, \ldots$.

**Syntax.** ALC concepts are given by the grammar

$$C, D ::= \top \mid \bot \mid A \mid \neg C \mid C \sqcap D \mid C \sqcup D \mid \exists r.C \mid \forall r.C,$$

where $A$ is a concept name and $r$ is a role name.

**Semantics.** An interpretation $I = (\Delta^I, \cdot^I)$ has a nonempty set $\Delta^I$, the domain, and a map $\cdot^I$ that gives each concept name $A$ a set $A^I \subseteq \Delta^I$, each role name $r$ a relation $r^I \subseteq \Delta^I \times \Delta^I$, and each individual name $a$ an element $a^I \in \Delta^I$. If $(x, y) \in r^I$, then $y$ is an $r$-successor of $x$. The map extends to all concepts:

| concept | extension $C^I$ |
|---|---|
| $\top$ | $\Delta^I$ |
| $\bot$ | $\emptyset$ |
| $\neg C$ | $\Delta^I \setminus C^I$ |
| $C \sqcap D$ | $C^I \cap D^I$ |
| $C \sqcup D$ | $C^I \cup D^I$ |
| $\exists r.C$ | $\{x \in \Delta^I : \text{some } r\text{-successor of } x \text{ is in } C^I\}$ |
| $\forall r.C$ | $\{x \in \Delta^I : \text{every } r\text{-successor of } x \text{ is in } C^I\}$ |

An element $x$ is an *instance* of $C$ in $I$ when $x \in C^I$. Two concepts $C$ and $D$ are *equivalent*, $C \equiv D$, when $C^I = D^I$ in every interpretation. Axioms about concepts and individuals, $C \sqsubseteq D$, $C(a)$ and $r(a, b)$, are on the page [TBox and ABox](/tbox-and-abox/).

**Measures.** The *size* $|C|$ of a concept is the number of names and constructors in it. The *role depth* $\mathrm{rd}(C)$ is the largest number of nested restrictions: $\mathrm{rd}(A) = \mathrm{rd}(\top) = \mathrm{rd}(\bot) = 0$, $\mathrm{rd}(\neg C) = \mathrm{rd}(C)$, $\mathrm{rd}(C \sqcap D) = \mathrm{rd}(C \sqcup D) = \max(\mathrm{rd}(C), \mathrm{rd}(D))$, and $\mathrm{rd}(\exists r.C) = \mathrm{rd}(\forall r.C) = 1 + \mathrm{rd}(C)$.

**Negation normal form.** A concept is in negation normal form (NNF) when $\neg$ occurs only directly in front of concept names. The equivalences $\neg\neg C \equiv C$, $\neg(C \sqcap D) \equiv \neg C \sqcup \neg D$, $\neg(C \sqcup D) \equiv \neg C \sqcap \neg D$, $\neg \exists r.C \equiv \forall r.\neg C$, $\neg \forall r.C \equiv \exists r.\neg C$, $\neg \top \equiv \bot$ and $\neg \bot \equiv \top$ push each $\neg$ inward. So each concept $C$ has an equivalent concept $\mathrm{nnf}(C)$ in NNF, with $|\mathrm{nnf}(C)| \le 2|C|$ and the same role depth.

The constructors are not independent: $\top \equiv A \sqcup \neg A$, $\bot \equiv \neg \top$, $C \sqcup D \equiv \neg(\neg C \sqcap \neg D)$ and $\forall r.C \equiv \neg \exists r.\neg C$. So $\neg$, $\sqcap$ and $\exists r.C$ are enough to write every ALC concept, at the cost of a linear blowup.

## Examples and non-examples

Let $\Delta^I = \{1, 2, 3\}$, $r^I = \{(1, 2), (1, 3)\}$, $A^I = \{2\}$ and $B^I = \{2, 3\}$.

- $(\exists r.A)^I = \{1\}$, because 2 is an $r$-successor of 1 and is in $A^I$.
- $(\forall r.B)^I = \{1, 2, 3\}$. Element 1 has only successors in $B^I$, and 2 and 3 have no successors, so the condition holds for them with nothing to check.
- $(\forall r.A)^I = \{2, 3\}$, because the successor 3 of element 1 is not in $A^I$.
- $(\exists r.\neg A \sqcap \exists r.A)^I = \{1\}$. Element 1 has successors of both kinds.
- $\exists r.\top \sqcap \forall r.\bot$ is an ALC concept with an empty extension in every interpretation: an element with a successor cannot have all its successors in $\emptyset$.
- With names from a domain: $\mathit{Person} \sqcap \neg \mathit{Female} \sqcap \forall \mathit{hasChild}.(\mathit{Doctor} \sqcup \mathit{Professor})$ describes the men whose children are all doctors or professors.

These are not ALC concepts:

- $\geq 2\, r.A$, an element with at least two $r$-successors in $A$. This is a qualified number restriction (ALCQ). ALC cannot express it: the interpretations $\{x \to y\}$ and $\{x \to y_1, x \to y_2\}$ with all elements in $A$ are [bisimilar](/bisimulation/), and ALC concepts do not tell bisimilar elements apart.
- $\exists r^-.A$, with the inverse of a role (ALCI).
- $\{a\}$, the concept with the one element $a^I$, a nominal (ALCO).
- $\exists r.\mathit{Self}$, the elements with an $r$-edge to themselves (part of SROIQ).
- $r \sqsubseteq s$ and "$r$ is transitive". These are role axioms, not concepts. They are the H and the S of names such as SHIQ.
- $A(a)$ and $C \sqsubseteq D$. These are axioms, not concepts.

## Related definitions

- The family, the letters of its names and the translation to first-order logic: [description logic](/description-logic/).
- A sublanguage without $\neg$, $\sqcup$ and $\forall$, with polynomial reasoning: [EL](/el-description-logic/). A large extension: [SROIQ](/sroiq/).
- ALC with one modality for each role name is the modal logic K, and an interpretation is a [Kripke structure](/kripke-structure/): see [ALC and modal logic K](/alc-modal-k-correspondence/).
- The reasoning problems: [concept satisfiability](/concept-satisfiability/) and [concept subsumption](/concept-subsumption/). The standard decision procedure: [the tableau algorithm for ALC](/alc-tableau-algorithm/).

## References
